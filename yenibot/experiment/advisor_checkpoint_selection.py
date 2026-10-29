"""Paired BCE/AP checkpoint selection on a common BCE-stopped A6 trajectory."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd
from yenibot.experiment.advisor_storage import immutable_json, sha256

DESIGN = dict(version=1, selection_rows=528, gap_rows=24, assessment_rows=528,
              stopping='selection_bce_patience15', selectors=['bce', 'ap'],
              selection_coverage=[.05, .10], fixed_threshold=.5,
              final_test_evaluations=0)


def verify_reference_runtime(protocol, current):
    if any(protocol[key] != value for key, value in current.items()):
        raise ValueError('Source runtime differs; do not mix environments')


def run_signature(study, seed, fold):
    return hashlib.sha256(f'{study}:{seed}:{fold}'.encode()).hexdigest()


def split_validation(indices):
    if len(indices) != 1080 or not np.array_equal(np.diff(indices), np.ones(1079)):
        raise ValueError('Expected contiguous original 1080 validation rows')
    return indices[:528], indices[552:]


def coverage_threshold(scores, fraction):
    scores = np.asarray(scores)
    if not len(scores) or not np.isfinite(scores).all() or not 0 < fraction <= 1:
        raise ValueError('Invalid selection scores/coverage')
    return float(np.sort(scores)[-max(1, int(np.ceil(len(scores)*fraction)))])


def decision_counts(y, scores, threshold):
    positive = np.asarray(scores) >= threshold
    y = np.asarray(y)
    n, tp, positives = int(positive.sum()), int(y[positive].sum()), int(y.sum())
    return dict(signals=n, tp=tp, positives=positives, samples=len(y),
                precision=tp/n if n else None, recall=tp/positives if positives else None,
                f1=2*tp/(n+positives) if n+positives else 0., signal_rate=n/len(y))


def validate_completed(folder, signature):
    marker = folder/'complete.json'
    if not marker.exists():
        return False
    record = json.loads(marker.read_text())
    if record['signature'] != signature:
        raise ValueError('Completed run identity mismatch')
    for name, digest in record['files'].items():
        if sha256(folder/name) != digest:
            raise ValueError('Completed artifact missing/changed: '+name)
    return True


def train_fold(frame, fold, cfg, features, seed, folder, signature, device):
    import torch
    from torch import nn
    from torch.utils.data import DataLoader
    from sklearn.preprocessing import RobustScaler
    from yenibot.training import advisor as engine
    from yenibot.training.dataset import SequenceDataset
    folder.mkdir(parents=True, exist_ok=True)
    if validate_completed(folder, signature):
        return
    selection, assessment = split_validation(fold.val)
    horizon = cfg['labeling']['max_holding_bars']
    audit = {'train_selection': engine.audit_boundary(frame, fold.train, selection, horizon),
             'selection_assessment': engine.audit_boundary(frame, selection, assessment, horizon)}
    scaler = RobustScaler().fit(frame.iloc[fold.train][features])
    def loader(indices, shuffle=False):
        part = frame.iloc[indices]
        ds = SequenceDataset(scaler.transform(part[features]).astype(np.float32),
             part.label.to_numpy(np.float32), part[f'fwd_return_{horizon}h'].to_numpy(np.float32),
             seq_len=cfg['model']['seq_len'])
        return DataLoader(ds, batch_size=cfg['training']['batch_size'], shuffle=shuffle, num_workers=0)
    train_loader, selection_loader = loader(fold.train, True), loader(selection)
    engine.seed_everything(seed+fold.fold, cfg['training']['deterministic'])
    model = engine.build_advisor_model(len(features), 'gru', cfg['model']).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg['training']['learning_rate'],
                                  weight_decay=cfg['training']['weight_decay'])
    history, states, epochs = [], {}, {}
    best = {'bce': float('inf'), 'ap': -float('inf')}
    patience, start = 0, 0
    checkpoint = folder/'last.pt'
    if not checkpoint.exists() and (folder/'selection.json').exists():
        raise ValueError('Incomplete output without resumable checkpoint; preserve and investigate')
    if checkpoint.exists():
        saved = torch.load(checkpoint, map_location='cpu', weights_only=False)
        if saved['signature'] != signature or saved['device'] != str(device):
            raise ValueError('Checkpoint identity mismatch')
        model.load_state_dict(saved['model']); optimizer.load_state_dict(saved['optimizer'])
        for state in optimizer.state.values():
            for key, value in state.items():
                if isinstance(value, torch.Tensor): state[key] = value.to(device)
        history, states, epochs, best = [saved[k] for k in ('history','states','epochs','best')]
        patience, start = saved['patience'], saved['epoch']
        engine.restore_rng(saved['rng'])
    for epoch in range(start, cfg['training']['epochs']):
        if patience >= cfg['training']['patience']: break
        model.train(); total, count = 0., 0
        for x, y, _, _ in train_loader:
            x, y = x.to(device), y.to(device); optimizer.zero_grad(set_to_none=True)
            loss = nn.functional.binary_cross_entropy_with_logits(model(x, return_logits=True), y)
            if not torch.isfinite(loss): raise ValueError('Nonfinite training loss')
            loss.backward(); nn.utils.clip_grad_norm_(model.parameters(), cfg['training']['grad_clip'])
            optimizer.step(); total += float(loss.detach())*len(y); count += len(y)
        metrics, _ = engine.evaluate(model, selection_loader, device, .5)
        if not np.isfinite([metrics['bce'],metrics['average_precision']]).all():
            raise ValueError('Nonfinite selection metric')
        patience += 1
        for rule, key in [('bce','bce'),('ap','average_precision')]:
            improved = metrics[key] < best[rule] if rule == 'bce' else metrics[key] > best[rule]
            if improved:
                best[rule], epochs[rule] = metrics[key], epoch+1
                states[rule] = {k:v.detach().cpu().clone() for k,v in model.state_dict().items()}
                if rule == 'bce': patience = 0
        history.append({'epoch':epoch+1,'train_bce':total/count,**metrics})
        engine.atomic_checkpoint(checkpoint, dict(signature=signature,device=str(device),epoch=epoch+1,
            model=model.state_dict(),optimizer=optimizer.state_dict(),history=history,states=states,
            epochs=epochs,best=best,patience=patience,rng=engine.rng_state()))
        print(f'fold={fold.fold} seed={seed} epoch={epoch+1} selection_BCE={metrics["bce"]:.5f} selection_AP={metrics["average_precision"]:.5f}',flush=True)
    # Freeze both choices before the assessment loader is constructed/evaluated.
    immutable_json(folder/'selection.json', dict(signature=signature,epochs=epochs,
                    stopping=DESIGN['stopping'],history_epochs=len(history)))
    engine.atomic_text(folder/'history.csv', pd.DataFrame(history).to_csv(index=False))
    assessment_loader = loader(assessment)
    results = {}
    files = ['selection.json','history.csv']
    for rule in DESIGN['selectors']:
        model.load_state_dict(states[rule])
        engine.atomic_checkpoint(folder/(rule+'.pt'),dict(signature=signature,model=states[rule],
            epoch=epochs[rule],scaler_center=scaler.center_,scaler_scale=scaler.scale_,features=features))
        results[rule] = {'epoch': epochs[rule]}
        for split, indices, data_loader in [('selection',selection,selection_loader),('assessment',assessment,assessment_loader)]:
            metrics, pred = engine.evaluate(model, data_loader, device, .5)
            pred['timestamp'] = frame.iloc[indices[pred.source_row_position.to_numpy()]].timestamp.to_numpy()
            pred['frame_row_position'] = indices[pred.source_row_position.to_numpy()]
            name = f'{rule}_{split}.parquet'; temp = folder/(name+'.tmp')
            pred.to_parquet(temp,index=False);temp.replace(folder/name)
            files.append(name);results[rule][split] = metrics
        files.append(rule+'.pt')
    result = dict(signature=signature,seed=seed,fold=fold.fold,status='complete',
                  test_evaluations=0,boundary_audit=audit,results=results)
    engine.atomic_json(folder/'metrics.json',result);files.append('metrics.json')
    engine.atomic_json(folder/'complete.json',dict(signature=signature,files={n:sha256(folder/n) for n in files}))


def report(root, signature):
    from yenibot.training.advisor import atomic_text
    records, predictions = [], []
    for seed in (42,43,44):
        for fold in range(38):
            folder=root/'runs'/f'seed_{seed}'/f'fold_{fold:03d}'
            if not validate_completed(folder,run_signature(signature,seed,fold)): raise ValueError('Incomplete 114-run study')
            info=json.loads((folder/'metrics.json').read_text())
            for rule in DESIGN['selectors']:
                sel=pd.read_parquet(folder/f'{rule}_selection.parquet')
                val=pd.read_parquet(folder/f'{rule}_assessment.parquet')
                if len(sel)!=465 or len(val)!=465: raise ValueError('Unexpected sample counts')
                predictions.append(val.assign(rule=rule,seed=seed,fold=fold))
                thresholds={'fixed_050':.5,**{f'selection_top{int(c*100)}':coverage_threshold(sel.probability,c) for c in DESIGN['selection_coverage']}}
                for policy, threshold in thresholds.items():
                    records.append(dict(seed=seed,fold=fold,rule=rule,policy=policy,threshold=threshold,
                        epoch=info['results'][rule]['epoch'],bce=info['results'][rule]['assessment']['bce'],
                        ap=info['results'][rule]['assessment']['average_precision'],
                        **decision_counts(val.label,val.probability,threshold)))
    out=root/'reports';out.mkdir(exist_ok=True)
    table=pd.DataFrame(records)
    table.to_csv(out/'by_run.csv',index=False)
    summary=table.groupby(['rule','policy'])[['signals','tp','positives','samples']].sum()
    summary['precision']=summary.tp/summary.signals.replace(0,np.nan)
    summary['recall']=summary.tp/summary.positives
    summary['signal_rate']=summary.signals/summary.samples
    summary['f1']=2*summary.tp/(summary.signals+summary.positives)
    summary['no_signal_runs']=table.groupby(['rule','policy']).signals.apply(lambda s:int((s==0).sum()))
    for key in ['bce','ap']:
        summary[key+'_mean']=table.groupby(['rule','policy'])[key].mean()
    summary.to_csv(out/'summary.csv')
    a=table[table.rule=='bce'];b=table[table.rule=='ap']
    paired=a.merge(b,on=['seed','fold','policy'],suffixes=('_bce','_ap'),validate='one_to_one')
    paired.to_csv(out/'paired.csv',index=False)
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for rule,color in [('bce','#2563eb'),('ap','#d97706')]:
        part=table[(table.rule==rule)&(table.policy=='selection_top5')]
        g=part.groupby('fold')[['signals','tp','samples']].sum()
        axes[0].plot(g.index,100*g.tp/g.signals.replace(0,np.nan),label=rule,color=color)
        axes[1].plot(g.index,100*g.signals/g.samples,label=rule,color=color)
    axes[0].set_ylabel('Precision (%)');axes[1].set_ylabel('Realized signal rate (%)')
    for ax in axes:ax.set_xlabel('Fold');ax.legend();ax.grid(alpha=.2)
    fig.suptitle('Assessment: threshold from top 5% selection scores; no threshold tuning')
    fig.savefig(out/'comparison.png',dpi=150);plt.close(fig)
    pd.concat(predictions).to_parquet(out/'assessment_predictions.parquet',index=False)
    atomic_text(out/'README.md','# A6 checkpoint selection\n\n114 common trajectories; 228 selected checkpoints. '
        'Selection528 / gap24 / assessment528; 465 targets per partition. '
        'BCE stopping is common; AP stopping is not tested. Thresholds come only from selection scores. '
        'Realized assessment signal rates may differ. Previously seen validation, overlapping folds; not final test. '
        'No automatic winner. Model weights remain in runs/.\n')
    with zipfile.ZipFile(out/'checkpoint_selection_review.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for parent in ['runs','reports','artifacts','reproducibility']:
            for path in sorted((root/parent).rglob('*')):
                if path.is_file() and path.suffix in {'.csv','.json','.md','.parquet','.png'}:
                    archive.write(path,path.relative_to(root).as_posix())
    print(summary.to_string());print('Review ZIP:',out/'checkpoint_selection_review.zip')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','report'])
    parser.add_argument('--source',type=Path,required=True);parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args();source=args.source.resolve();root=args.root.resolve()
    if root==source or root.is_relative_to(source) or source.is_relative_to(root):
        raise ValueError('Separate workspace required')
    from yenibot.experiment.advisor_feature_comparison import verified
    from yenibot.experiment.advisor_learning_rate import one_run
    from yenibot.experiment.advisor_runtime import runtime_identity,freeze_workspace_identity
    from yenibot.experiment.advisor_workspace import REPO
    from yenibot.training import advisor as engine
    from yenibot.training.walk_forward import PurgedWalkForwardCV
    import torch
    cfg=verified(source);protocol=json.loads((one_run(source,'A')/'protocol.json').read_text())
    if protocol['config']!=cfg or protocol['experiment']!='A':raise ValueError('Wrong A6 source')
    for path,digest in protocol['source_hashes'].items():
        if sha256(REPO/path.split('/advisor_feature_comparison_repo/')[1])!=digest:
            raise ValueError('Frozen engine changed')
    if cfg['training']['learning_rate']!=.001 or cfg['training']['patience']!=15 or cfg['model']['seq_len']!=64:
        raise ValueError('Unexpected reference training conditions')
    root.mkdir(parents=True,exist_ok=True)
    identity=runtime_identity(REPO,require_gpu=True,hardware='selective-a100')
    import sys, sklearn
    verify_reference_runtime(protocol,dict(python=sys.version,torch=torch.__version__,
        numpy=np.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,
        gpu=torch.cuda.get_device_name(0),cuda=torch.version.cuda,cudnn=torch.backends.cudnn.version()))
    freeze_workspace_identity(REPO,root,identity)
    immutable_json(root/'artifacts/design.json',DESIGN)
    immutable_json(root/'artifacts/control.json',protocol)
    signature=hashlib.sha256((sha256(root/'reproducibility/workspace_identity.json')+
        sha256(root/'artifacts/design.json')+sha256(root/'artifacts/control.json')).encode()).hexdigest()
    frame=pd.read_parquet(cfg['data']['frame']);features=protocol['features']
    folds=list(PurgedWalkForwardCV(**cfg['walk_forward'],label_horizon_bars=10).split(len(frame)))
    if len(folds)!=38 or len(features)!=6:raise ValueError('Expected 38 folds/A6')
    for fold in folds:
        sel,assessment=split_validation(fold.val)
        engine.audit_boundary(frame,fold.train,sel,10);engine.audit_boundary(frame,sel,assessment,10)
    with engine.exclusive_run(root):
        if args.action=='prepare':print('Verified A6 reference; 114 new trajectories, 465 selection/465 assessment targets; no final test.')
        elif args.action=='train':
            for seed in (42,43,44):
                for fold in folds:
                    train_fold(frame,fold,cfg,features,seed,root/'runs'/f'seed_{seed}'/f'fold_{fold.fold:03d}',run_signature(signature,seed,fold.fold),torch.device('cuda'))
        else:report(root,signature)


if __name__=='__main__':main()

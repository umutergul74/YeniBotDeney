"""Fixed historical cohort; validation-only selective-signal diagnostics.

No final test command, automatic winner or deployable threshold exists here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, log_loss

from yenibot.experiment.advisor_runtime import runtime_identity, freeze_workspace_identity
from yenibot.experiment.advisor_storage import (
    immutable_json, atomic_json, sha256, operation, verify_prepared, inventory,
)
from yenibot.experiment.advisor_workspace import (
    REPO, base_config, read_config, checked_snapshot, persist_prepared, separate_workspace,
)
from yenibot.training import advisor
from yenibot.training.walk_forward import PurgedWalkForwardCV

CANDIDATES = {'B25': (2.,5.), 'B11': (1.,1.), 'B12': (1.,2.),
              'B152': (1.5,2.), 'B22': (2.,2.), 'B32': (3.,2.)}
SOURCES = {'1h':'a6be57890593b9d47357c5b8ee50b54ab61857b9f13a859e9e85c85525731c5c',
           '4h':'ba379bf5995c19096c1f8f37e4b8a75b9fc29377cf595d1346efae38ce5f9bdb'}
GRID = np.linspace(0,1,201)


def configuration(root, name):
    cfg = base_config(root, full=False, reference=None)
    cfg['data']['frame'] = str(root/f'data/{name}.parquet')
    cfg['labeling'].update(tp_multiplier=CANDIDATES[name][0], sl_multiplier=CANDIDATES[name][1])
    cfg['experiments'] = {name:{'features':'basic','architecture':'gru'}}
    return cfg


def protocol():
    cfg = read_config('configs/advisor_ablation.yaml')
    return {'experiment':'exp-016-selective-walk-forward', 'candidates':CANDIDATES,
            'development':cfg['development'], 'walk_forward':cfg['walk_forward'],
            'model':cfg['model'], 'training':cfg['training'],
            'features':cfg['data']['basic_features'], 'sources':SOURCES,
            'label':'TP before SL within next 10 bars; timeout and both_SL_first negative',
            'precision_scenarios':[.60,.65,.70], 'threshold_grid':'0:0.005:1',
            'decision':'diagnostics only; no automatically selected threshold or winner',
            'test_evaluations':0}


def cohort(frame, cfg):
    expected = pd.date_range('2022-03-01T04:00:00Z','2025-12-28T02:00:00Z',freq='h')
    if len(frame)!=33551 or not pd.DatetimeIndex(pd.to_datetime(frame.timestamp,utc=True)).equals(expected):
        raise ValueError('Original 33551-hour cohort changed')
    required={'train_bars':5040,'val_bars':1080,'test_bars':720,'step_bars':720,
              'purge_bars':24,'embargo_bars':24}
    if cfg['walk_forward']!=required or cfg['model']['seq_len']!=64 or cfg['training']['seeds']!=[42,43,44]:
        raise ValueError('Original splits/sequence/seeds changed')
    if cfg['labeling']['max_holding_bars']!=10:
        raise ValueError('Original label horizon changed')
    folds=list(PurgedWalkForwardCV(**required,label_horizon_bars=10).split(len(frame)))
    if len(folds)!=38: raise ValueError('Expected 38 folds')
    for fold in folds:
        advisor.audit_boundary(frame,fold.train,fold.val,10)
        advisor.audit_boundary(frame,fold.val,fold.test,10)
    return folds


def input_signature(frame, features):
    data=frame[['timestamp',*features]]
    return hashlib.sha256(pd.util.hash_pandas_object(data,index=False).to_numpy().tobytes()).hexdigest()


def prepare(root, legacy):
    source=checked_snapshot(legacy,root,full=False)
    if any(sha256(source/f'btc_{k}.parquet')!=v for k,v in SOURCES.items()):
        raise ValueError('Original raw snapshot changed')
    reference=json.loads((legacy/'data/A_reference.manifest.json').read_text())
    expected_features=read_config('config.yaml')
    expected_features['features']['wavelet']['enabled']=False
    expected_features['features']['active_profile']='baseline_plus_4h_bounded_whale_no_4h_tier1_no_4h_pure_volatility_no_1h_pure_volatility'
    if reference['source_hashes']!=SOURCES or reference['feature_config']!=expected_features:
        raise ValueError('Historical feature configuration changed')
    identities={}; shared=None
    for name in CANDIDATES:
        cfg=configuration(root,name)
        metadata=persist_prepared(cfg,advisor.prepare)
        frame=pd.read_parquet(cfg['data']['frame'])
        folds=cohort(frame,cfg)
        fingerprint=input_signature(frame,cfg['data']['basic_features'])
        if shared is not None and fingerprint!=shared:
            raise ValueError('Candidate timestamps/features differ')
        shared=fingerprint
        immutable_json(root/f'data/{name}.config.json',cfg)
        identities[name]={'frame_sha256':metadata['frame_sha256'],'input_signature':fingerprint,
                         'label_counts':{str(k):int(v) for k,v in frame.hit_type.value_counts().items()}}
    immutable_json(root/'artifacts/cohort.json',{'candidates':identities,'rows':33551,
                   'folds':len(folds),'seeds':[42,43,44],'input_signature':shared})
    immutable_json(root/'artifacts/splits.json',{'folds':[
        {'fold':f.fold,**{part:[int(getattr(f,part)[0]),int(getattr(f,part)[-1])]
                         for part in ['train','val','test']}} for f in folds]})
    print('Verified six candidates: identical inputs and 38 original folds; labels alone vary.',flush=True)


def verified_config(root,name):
    cfg=configuration(root,name)
    if json.loads((root/f'data/{name}.config.json').read_text())!=cfg:
        raise ValueError('Prepared configuration changed')
    meta=verify_prepared(Path(cfg['data']['frame']),cfg)
    audit=json.loads((root/'artifacts/cohort.json').read_text())
    if meta['frame_sha256']!=audit['candidates'][name]['frame_sha256']:
        raise ValueError('Cohort frame changed')
    return cfg


def train(root,names):
    for name in names:
        cfg=verified_config(root,name)
        cohort(pd.read_parquet(cfg['data']['frame']),cfg)
        print(f'Candidate {name}: 38 folds x 3 seeds. No test predictions.',flush=True)
        advisor.run(cfg,name)


def threshold_rows(labels, probabilities, hit_types):
    y=np.asarray(labels); p=np.asarray(probabilities); hit=np.asarray(hit_types)
    if not len(y) or len(y)!=len(p) or len(y)!=len(hit) or not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise ValueError('Invalid predictions')
    if not set(np.unique(y)).issubset({0,1}) or not set(hit).issubset({'tp','sl','both_sl_first','time'}):
        raise ValueError('Invalid labels/hit types')
    if not np.array_equal(y==1,hit=='tp'): raise ValueError('Labels disagree with hit types')
    selected=p[None,:]>=GRID[:,None]
    n=selected.sum(axis=1); tp=(selected&(y==1)).sum(axis=1)
    precision=np.divide(tp,n,out=np.full(len(GRID),np.nan),where=n>0)
    positives=int(y.sum())
    recall=tp/positives if positives else np.full(len(GRID),np.nan)
    fp=n-tp; fn=positives-tp; denominator=2*tp+fp+fn
    f1=np.divide(2*tp,denominator,out=np.zeros(len(GRID)),where=denominator>0)
    return pd.DataFrame({'threshold':GRID,'signals':n,'tp':tp,'fp':fp,'fn':fn,
        'precision':precision,'recall':recall,'f1':f1,'signal_rate':n/len(y),
        'selected_sl':(selected&np.isin(hit,['sl','both_sl_first'])).sum(axis=1),
        'selected_timeout':(selected&(hit=='time')).sum(axis=1),
        'selected_both':(selected&(hit=='both_sl_first')).sum(axis=1),
        'prevalence':np.mean(y),'precision_lift':precision/np.mean(y) if positives else np.nan})


def validate_predictions(predictions, frame, fold):
    expected=frame.iloc[fold.val[63:]]
    if not np.array_equal(predictions.source_row_position.to_numpy(),np.arange(63,1080)):
        raise ValueError('Validation sequence positions changed')
    if not pd.DatetimeIndex(pd.to_datetime(predictions.timestamp,utc=True)).equals(pd.DatetimeIndex(expected.timestamp)):
        raise ValueError('Validation timestamps changed')
    if not np.array_equal(predictions.label.to_numpy(),expected.label.to_numpy()):
        raise ValueError('Validation labels changed')
    if not np.allclose(predictions.forward_return,expected.fwd_return_10h,rtol=1e-5,atol=1e-7):
        raise ValueError('Validation returns changed')
    return expected.hit_type.to_numpy()


def summarize(curves):
    """Equal fold/seed summaries; no-signal precision stays undefined, never success."""
    rows=[]
    for threshold,g in curves.groupby('threshold',sort=True):
        defined=g.precision.notna()
        r={'threshold':float(threshold),'fold_seed_count':len(g),
           'no_signal_fraction':float((~defined).mean()),
           'precision_mean_active':float(g.precision.mean()),
           'precision_p10_active':float(g.precision.quantile(.1)),
           'precision_min_active':float(g.precision.min()),
           'recall_mean':float(g.recall.mean()),'signal_rate_mean':float(g.signal_rate.mean()),
           'signals_min':int(g.signals.min()),'signals_median':float(g.signals.median()),
           'signals_sum_overlapping':int(g.signals.sum()),
           'selected_sl_mean':float(g.selected_sl.mean()),
           'selected_timeout_mean':float(g.selected_timeout.mean())}
        for goal in (.60,.65,.70):
            r[f'fraction_precision_ge_{int(goal*100)}']=float((defined&(g.precision>=goal)).mean())
        rows.append(r)
    return pd.DataFrame(rows)


def review_candidate(root,name):
    cfg=verified_config(root,name);frame=pd.read_parquet(cfg['data']['frame']);folds=cohort(frame,cfg)
    runs=list((root/'runs').glob(name+'_*/protocol.json'))
    if len(runs)!=1: raise ValueError(f'Expected one run for {name}, found {len(runs)}')
    folder=runs[0].parent;manifest=json.loads(runs[0].read_text())
    if manifest['config']!=cfg or manifest['folds']!=list(range(38)) or manifest['seeds']!=[42,43,44]:
        raise ValueError('Run cohort differs')
    if manifest['data_sha256']!=sha256(Path(cfg['data']['frame'])):
        raise ValueError('Run data hash differs')
    state=json.loads((folder/'status.json').read_text())
    if state['status']!='complete' or len(state['completed'])!=114:
        raise ValueError(f'{name}: report requires complete 38-fold x 3-seed scope')
    signature=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest()
    curves=[];metrics=[];unique=set();files={}
    for seed in [42,43,44]:
        for fold in folds:
            run=folder/f'seed_{seed}/fold_{fold.fold:03d}'
            saved=json.loads((run/'validation_metrics.json').read_text())
            if saved['signature']!=signature or saved['status']!='complete': raise ValueError('Completed fold mismatch')
            path=run/'validation_predictions.parquet';p=pd.read_parquet(path)
            hit=validate_predictions(p,frame,fold)
            unique.update(pd.to_datetime(p.timestamp,utc=True).astype(str))
            curve=threshold_rows(p.label.to_numpy(),p.probability.to_numpy(),hit)
            curve['seed']=seed;curve['fold']=fold.fold
            curve['validation_first']=str(p.timestamp.iloc[0]);curve['validation_last']=str(p.timestamp.iloc[-1])
            curves.append(curve)
            prior=float(frame.iloc[fold.train[63:]].label.mean())
            bce=float(log_loss(p.label,p.probability,labels=[0,1]))
            reference=float(log_loss(p.label,np.full(len(p),np.clip(prior,1e-7,1-1e-7)),labels=[0,1]))
            metrics.append({'seed':seed,'fold':fold.fold,'best_epoch':saved['best_epoch'],
                'ap':float(average_precision_score(p.label,p.probability)) if p.label.sum() else 0.,
                'bce':bce,'bce_reference':reference,'bce_skill':1-bce/reference,
                'prevalence':float(p.label.mean()),'train_prevalence':prior})
            for file in [path,run/'validation_metrics.json',run/'history.csv']:
                files[file.relative_to(root).as_posix()]=sha256(file)
    all_curves=pd.concat(curves,ignore_index=True);summary=summarize(all_curves)
    reports=root/'reports'/name;reports.mkdir(parents=True,exist_ok=True)
    all_curves.to_csv(reports/'thresholds_by_fold_seed.csv',index=False)
    summary.to_csv(reports/'threshold_summary.csv',index=False)
    pd.DataFrame(metrics).to_csv(reports/'metrics_by_fold_seed.csv',index=False)
    for seed in [42,43,44]:
        summarize(all_curves[all_curves.seed==seed]).to_csv(reports/f'threshold_summary_seed_{seed}.csv',index=False)
    all_curves.loc[np.isclose(all_curves.threshold,.5)].to_csv(reports/'reference_05.csv',index=False)
    # These are descriptive scenario sets, not policies selected for deployment.
    scenarios=[]
    for goal in [.60,.65,.70]:
        eligible=summary[(summary.no_signal_fraction==0)&(summary.precision_mean_active>=goal)]
        scenarios.append({'precision_goal':goal,'thresholds_meeting_mean':len(eligible),
                          'status':'not_met' if eligible.empty else 'descriptive_candidates_only',
                          'selected_threshold':None})
        eligible.to_csv(reports/f'precision_{int(goal*100)}_descriptive.csv',index=False)
    atomic_json(reports/'review.json',{'candidate':name,'unique_validation_hours':len(unique),
        'prediction_rows_overlapping':114*1017,'scenarios':scenarios,
        'selected_threshold':None,'winner':None,'test_evaluations':0,'files':files,
        'caveat':'Same validation used for epoch selection and diagnostics; optimistic. Overlapping folds and seeds are not independent.'})
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    axes[0,0].plot(summary.threshold,summary.precision_mean_active,label='Precision: active fold/seeds')
    axes[0,0].plot(summary.threshold,summary.recall_mean,label='Recall')
    for goal in [.6,.65,.7]: axes[0,0].axhline(goal,ls=':',alpha=.5)
    axes[0,0].legend();axes[0,0].set_ylim(0,1)
    axes[0,1].plot(summary.threshold,summary.signal_rate_mean,label='Signal rate')
    axes[0,1].plot(summary.threshold,summary.no_signal_fraction,label='No-signal fold/seed fraction');axes[0,1].legend()
    axes[1,0].plot(summary.threshold,summary.precision_p10_active,label='Precision p10 (active)')
    axes[1,0].plot(summary.threshold,summary.precision_min_active,label='Precision minimum (active)');axes[1,0].legend()
    for goal in [60,65,70]: axes[1,1].plot(summary.threshold,summary[f'fraction_precision_ge_{goal}'],label=f'Fraction precision >= {goal}%')
    axes[1,1].legend()
    for ax in axes.flat:ax.set_xlabel('Threshold');ax.grid(alpha=.2)
    fig.suptitle(f'{name}: validation diagnostics only, no selected threshold')
    fig.tight_layout();fig.savefig(reports/'selectivity.png',dpi=160);plt.close(fig)
    return {'candidate':name,**pd.DataFrame(metrics).drop(columns=['seed','fold','best_epoch']).mean().to_dict()}


def report(root,names):
    rows=[review_candidate(root,name) for name in names]
    pd.DataFrame(rows).to_csv(root/'reports/candidate_metrics.csv',index=False)
    text='# Seçici sinyal · validation incelemesi\n\n'
    text+='Kapsam: '+', '.join(names)+'. Her aday 38 fold × 3 seed; 33.551 ortak saat.\n\n'
    text+='TP önce = 1; SL veya timeout = 0. Negatif karar SL garantisi değildir.\n\n'
    text+='Otomatik eşik/kazanan seçilmedi. %60/%65/%70 tabloları betimseldir; kabul edilmiş başarı ölçütü değildir.\n\n'
    text+='Precision yalnızca sinyal veren fold/seedlerde tanımlıdır. Sinyalsiz bölümler başarı oranında başarısız sayılır. Sinyal sayısı ve en kötü dönemler ayrıca incelenmelidir.\n\n'
    text+='Epoch seçimi ve bu inceleme aynı validation üzerinde; sonuçlar iyimserdir. Örtüşen foldlar ve seedler bağımsız örnek sayılmaz.\n\n'
    text+='Her aday klasöründe fold/seed eşik tablosu, 0,5 eşik referansı, metrikler ve grafik bulunur. Test çalıştırılmadı.\n'
    (root/'reports/REPORT.md').write_text(text,encoding='utf-8')


def bundle(root,session):
    reports=root/'reports';reports.mkdir(exist_ok=True)
    atomic_json(reports/'full_artifact_inventory.json',inventory(root))
    target=reports/f'selective_review_{session}_{pd.Timestamp.now(tz="UTC").value}.zip'
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(root.rglob('*')):
            if not p.is_file() or p.suffix in {'.zip','.pt'}:continue
            rel=p.relative_to(root)
            if rel.parts[0] in {'inputs','data'}:continue
            if rel.parts[0] not in {'runs','artifacts','reports','sessions','reproducibility'}:continue
            # Includes per-row validation predictions/history/metrics; no raw data or weights.
            archive.write(p,rel)
    print('Review ZIP (predictions included, model weights excluded):',target,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','report','bundle'])
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--legacy',type=Path,required=True)
    parser.add_argument('--session',required=True)
    parser.add_argument('--candidates',nargs='+',choices=list(CANDIDATES),default=list(CANDIDATES))
    parser.add_argument('--allow-training',action='store_true')
    args=parser.parse_args()
    if not args.session.replace('_','').replace('-','').isalnum():parser.error('Invalid session')
    if len(set(args.candidates))!=len(args.candidates):parser.error('Duplicate candidates')
    if args.action=='train' and not args.allow_training:parser.error('Training disabled')
    root,legacy=args.root.resolve(),args.legacy.resolve();separate_workspace(root,legacy)
    with operation(root,args.action,args.session):
        freeze_workspace_identity(REPO,root,runtime_identity(REPO,require_gpu=True))
        immutable_json(root/'artifacts/plan.json',json.loads(json.dumps(protocol())))
        if args.action=='prepare':prepare(root,legacy)
        elif args.action=='train':train(root,args.candidates)
        elif args.action=='report':report(root,args.candidates)
        else:bundle(root,args.session)


if __name__=='__main__':main()

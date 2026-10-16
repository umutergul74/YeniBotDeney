"""Repair missing exports using the frozen v1.1.0 engine; never replace old fold files.

Invoked by the notebook's isolated interpreter, outside the frozen checkout.
No test path. Existing predictions/metrics are validated, never silently replaced.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile

RESEARCH_COMMIT = '7fe90e0f0531fff36131f683526aa355cb464088'
REQUIRED = ('validation_metrics.json', 'validation_predictions.parquet', 'history.csv')


def missing_files(folder):
    return [name for name in (*REQUIRED, 'last.pt')
            if not (folder/name).is_file() or not (folder/name).stat().st_size]


def publish_missing(source, target):
    """Existing evidence is never overwritten, including partial/empty files."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise ValueError(f'Refusing to replace existing artifact: {target}')
    with source.open('rb') as src, target.open('xb') as dst:
        shutil.copyfileobj(src, dst)
        dst.flush()
        os.fsync(dst.fileno())
    if hashlib.sha256(source.read_bytes()).digest() != hashlib.sha256(target.read_bytes()).digest():
        raise ValueError(f'Copy verification failed: {target}')


def inspect(root, names, selective, pd):
    rows, contexts = [], {}
    for name in names:
        cfg = selective.verified_config(root, name)
        frame = pd.read_parquet(cfg['data']['frame'])
        folds = selective.cohort(frame, cfg)
        found = list((root/'runs').glob(name+'_*/protocol.json'))
        if len(found) != 1:
            raise ValueError(f'{name}: expected exactly one original run')
        manifest = json.loads(found[0].read_text())
        if manifest['config'] != cfg or manifest['folds'] != list(range(38)) or manifest['seeds'] != [42,43,44]:
            raise ValueError(f'{name}: original run protocol mismatch')
        if manifest['data_sha256'] != selective.sha256(Path(cfg['data']['frame'])):
            raise ValueError(f'{name}: prepared data hash mismatch')
        signature = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
        contexts[name] = (cfg, frame, folds, found[0].parent, manifest, signature)
        for seed in (42,43,44):
            for fold in folds:
                folder = found[0].parent/f'seed_{seed}/fold_{fold.fold:03d}'
                missing = missing_files(folder)
                if 'validation_metrics.json' not in missing:
                    m = json.loads((folder/'validation_metrics.json').read_text())
                    if (m['signature'] != signature or m['status'] != 'complete' or
                            m['fold'] != fold.fold or m['seed'] != seed or m['test_evaluations'] != 0):
                        raise ValueError(f'Invalid metrics: {folder}')
                if 'validation_predictions.parquet' not in missing:
                    selective.validate_predictions(pd.read_parquet(folder/'validation_predictions.parquet'), frame, fold)
                if 'history.csv' not in missing:
                    h = pd.read_csv(folder/'history.csv')
                    if not len(h) or list(h.epoch) != list(range(1,len(h)+1)):
                        raise ValueError(f'Invalid history: {folder}')
                    if 'validation_metrics.json' not in missing and len(h) != m['epochs_trained']:
                        raise ValueError(f'Truncated history: {folder}')
                rows.append({'candidate':name, 'seed':seed, 'fold':fold.fold,
                             'path':str(folder.relative_to(root)), 'missing':missing,
                             'report_ready':not set(missing).intersection(REQUIRED)})
    return rows, contexts


def repair_one(row, context, output, advisor, pd, torch):
    cfg, frame, folds, run, manifest, signature = context
    folder = run/f"seed_{row['seed']}/fold_{row['fold']:03d}"
    missing = set(row['missing'])
    if not missing.intersection(REQUIRED):
        return 'kept; weights unavailable' if 'last.pt' in missing else 'kept'
    scratch = output/'recovered'/row['path']
    scratch.mkdir(parents=True, exist_ok=False)
    checkpoint = None
    if 'last.pt' not in missing:
        publish_missing(folder/'last.pt', scratch/'last.pt')
        checkpoint = torch.load(scratch/'last.pt', map_location='cpu', weights_only=False)
        if checkpoint['signature'] != signature or checkpoint['device'] != manifest['device']:
            raise ValueError('Checkpoint identity mismatch')
    if missing.intersection(REQUIRED) == {'history.csv'}:
        m = json.loads((folder/'validation_metrics.json').read_text())
        if checkpoint is None or len(checkpoint['history']) != m['epochs_trained'] or checkpoint['best_epoch'] != m['best_epoch']:
            raise ValueError('Checkpoint cannot reconstruct the recorded history')
        pd.DataFrame([{'epoch':r['epoch'],'train_bce':r['train_bce'],**r['validation']}
                      for r in checkpoint['history']]).to_csv(scratch/'history.csv',index=False)
        publish_missing(scratch/'history.csv',folder/'history.csv')
        return 'history restored from checkpoint; no training'
    # Deliberately narrow incident scope. Unknown missing/partial combinations stop.
    if missing.intersection(REQUIRED) != set(REQUIRED):
        raise ValueError('Partial evidence requires manual reconciliation; nothing overwritten')
    torch.set_num_threads(cfg['training']['torch_threads'])
    advisor.run_fold(frame, folds[row['fold']], cfg, cfg['experiments'][row['candidate']],
                     manifest['features'], row['seed'], scratch, signature, torch.device(manifest['device']))
    for name in REQUIRED:
        publish_missing(scratch/name, folder/name)
    if 'last.pt' in missing:
        publish_missing(scratch/'last.pt', folder/'last.pt')
    # Existing checkpoint remains untouched; the resumed final checkpoint stays in recovered/.
    return 'resumed checkpoint; final weights in recovered/' if checkpoint else 'retrained missing fold'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['audit','repair','report','bundle'])
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--root',type=Path,required=True)
    p.add_argument('--session',required=True)
    p.add_argument('--allow-repair',action='store_true')
    args=p.parse_args()
    if not args.session.replace('_','').replace('-','').isalnum():p.error('Invalid session')
    if args.action=='repair' and not args.allow_repair:p.error('Repair not enabled')
    sys.path.insert(0,str(args.repo.resolve()))
    os.environ['MPLBACKEND']='Agg'
    from yenibot.experiment import advisor_selective as s
    from yenibot.experiment.advisor_runtime import runtime_identity, freeze_workspace_identity
    import pandas as pd
    import torch
    root=args.root.resolve()
    frozen=json.loads((root/'reproducibility/workspace_identity.json').read_text())
    if frozen['commit']!=RESEARCH_COMMIT:raise ValueError('Not the original A100 v1.1.0 workspace')
    freeze_workspace_identity(args.repo,root,runtime_identity(args.repo,require_gpu=True,hardware='selective-a100'))
    output=root/'recovery'/args.session
    output.mkdir(parents=True,exist_ok=True)
    with s.advisor.exclusive_run(output.parent):
        rows,contexts=inspect(root,list(s.CANDIDATES),s,pd)
        s.atomic_json(output/f'{args.action}_audit.json',{'rows':rows,'test_evaluations':0})
        print(pd.DataFrame([{'candidate':n,'report_ready':sum(r['report_ready'] for r in rows if r['candidate']==n),
              'all_files_present':sum(not r['missing'] for r in rows if r['candidate']==n)} for n in s.CANDIDATES]).to_string(index=False),flush=True)
        for r in rows:
            if r['missing']:print(r,flush=True)
        if args.action=='audit':return
        if args.action=='repair':
            allowed={('B32',44,34),('B32',44,35),('B32',44,36),('B32',44,37)}
            if any(r['missing'] and (r['candidate'],r['seed'],r['fold']) not in allowed for r in rows):
                raise ValueError('Inventory differs from reviewed incident; stop before repair')
            for r in rows:
                if r['missing']:
                    result=repair_one(r,contexts[r['candidate']],output,s.advisor,pd,torch)
                    s.atomic_json(output/f"{r['candidate']}_{r['seed']}_{r['fold']}_receipt.json",{'input':r,'result':result})
            rows,contexts=inspect(root,list(s.CANDIDATES),s,pd)
        if not all(r['report_ready'] for r in rows):raise ValueError('Reports blocked: incomplete fold evidence')
        if args.action in {'repair','report'}:
            # Keep stale mutable summaries as evidence, then rebuild them from verified folds.
            for name,(_,_,_,run,manifest,signature) in contexts.items():
                complete=[]
                for seed in (42,43,44):
                    for fold in range(38):
                        m=json.loads((run/f'seed_{seed}/fold_{fold:03d}/validation_metrics.json').read_text())
                        complete.append({'seed':seed,'fold':fold,'validation':m['validation'],'best_epoch':m['best_epoch']})
                backup=output/'prior_summaries'/name;backup.mkdir(parents=True,exist_ok=True)
                for filename in ('status.json','validation_summary.csv'):
                    if (run/filename).exists() and not (backup/filename).exists():publish_missing(run/filename,backup/filename)
                s.atomic_json(run/'status.json',{'status':'complete','signature':signature,'completed':complete,'test_evaluations':0})
                pd.DataFrame([{**m['validation'],'seed':m['seed'],'fold':m['fold'],'best_epoch':m['best_epoch']} for m in complete]).to_csv(run/'validation_summary.csv',index=False)
        if args.action=='report':
            s.report(root,list(s.CANDIDATES))
            (root/'reports/RECOVERY.md').write_text(
                '# Recovery provenance\n\nOriginal v1.1.0 research engine; no test evaluation.\n'
                'B32/seed_44/fold_034: original predictions retained; model weights unavailable.\n'
                'fold_035: history reconstructed from its checkpoint.\n'
                'fold_036: resumed checkpoint; final recovered checkpoint is under recovery/.\n'
                'fold_037: missing fold retrained; this is reconstructed evidence, not recovered original bytes.\n'
                'See recovery/ receipts and prior_summaries; compare metrics only after the complete report.\n',encoding='utf-8')
        if args.action=='bundle':
            s.bundle(root,args.session)
            package=max((root/'reports').glob(f'selective_review_{args.session}_*.zip'),key=lambda p:p.stat().st_mtime_ns)
            with zipfile.ZipFile(package,'a',zipfile.ZIP_DEFLATED) as archive:
                for file in sorted((root/'recovery').rglob('*')):
                    if file.is_file() and file.suffix not in {'.pt','.zip'}:
                        archive.write(file,file.relative_to(root))


if __name__=='__main__':main()

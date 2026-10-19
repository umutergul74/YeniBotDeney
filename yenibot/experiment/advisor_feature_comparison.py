"""A6/B37/C37/D37 validation study using the unchanged advisor engine."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd

from yenibot.training import advisor
from yenibot.experiment.advisor_selective import cohort
from yenibot.experiment.advisor_runtime import runtime_identity, freeze_workspace_identity
from yenibot.experiment.advisor_storage import (
    copy_verified, immutable_json, verify_prepared, sha256, inventory,
)
from yenibot.experiment.advisor_workspace import REPO, read_config, recover, separate_workspace

FULL_SHA = 'ce49f694d8e7d1c860f0b16ef49c8ec48ed072404c4f8b2991fc8945584c0653'
NAMES = ('A', 'B', 'C', 'D')
ADDED = ('realized_vol_14', 'gk_vol_14', 'atr_14_pct')


def features():
    basic = read_config('configs/advisor_ablation.yaml')['data']['basic_features']
    old = (REPO/'configs/advisor_full_features.txt').read_text().splitlines()
    full = (REPO/'configs/advisor_full_features_v2.txt').read_text().splitlines()
    if len(old) != 34 or full != old + list(ADDED) or len(set(full)) != 37 or not set(basic) <= set(full):
        raise ValueError('Expected original34 plus the three missing basic volatility channels')
    return basic, full


def configuration(root):
    marker = root/'recovered/data/development_full_wavelet_off.manifest.json'
    cfg = copy.deepcopy(json.loads(marker.read_text())['protocol'])
    cfg['protocol'] = 'advisor_feature_comparison_v1'
    cfg['output'] = str(root/'runs')
    cfg['data']['frame'] = str(root/'data/shared37.parquet')
    cfg['data']['feature_columns_file'] = str(REPO/'configs/advisor_full_features_v2.txt')
    cfg['experiments'] = read_config('configs/advisor_ablation.yaml')['experiments']
    return cfg


def verify_frame(frame, cfg):
    basic, full = features()
    cohort(frame, cfg)
    if cfg['labeling'] != read_config('configs/advisor_ablation.yaml')['labeling']:
        raise ValueError('Only original 2/5 labels are allowed')
    if cfg['training'] != read_config('configs/advisor_ablation.yaml')['training']:
        raise ValueError('Original training rules changed')
    if cfg['model'] != read_config('configs/advisor_ablation.yaml')['model']:
        raise ValueError('Original architectures changed')
    if cfg['data']['wavelet'] is not False or cfg['data']['basic_features'] != basic:
        raise ValueError('Basic feature/wavelet definition changed')
    if not set(full) <= set(frame) or not np.isfinite(frame[full].to_numpy(dtype=float)).all():
        raise ValueError('All37 finite features required; no dropped rows or imputation')


def prepare(root, legacy):
    features()
    # Existing recovery already checks raw hashes, original A alignment and OI.
    # It writes only into this new workspace and requires the original full hash.
    recover(root/'recovered', legacy, full=True)
    source = root/'recovered/data/development_full_wavelet_off.parquet'
    meta = verify_prepared(source)
    if meta['frame_sha256'] != FULL_SHA:
        raise ValueError('Not the historical full prepared cohort')
    cfg = configuration(root)
    frame = pd.read_parquet(source)
    verify_frame(frame, cfg)
    target = Path(cfg['data']['frame'])
    copy_verified(source, target, FULL_SHA)
    new_meta = copy.deepcopy(meta)
    new_meta['source_protocol'] = meta['protocol']
    new_meta['protocol'] = cfg
    immutable_json(target.with_suffix('.manifest.json'), new_meta)
    immutable_json(root/'artifacts/config.json', cfg)
    immutable_json(root/'artifacts/design.json', {
        'study':'A6-B37-C37-D37', 'frame_sha256':FULL_SHA,
        'basic':features()[0], 'full':features()[1], 'added':list(ADDED),
        'comparisons':{'A_vs_B':'feature expansion within GRU',
                       'B_vs_C_vs_D':'architecture at identical37 inputs'},
        'training_runs':456, 'test_evaluations':0,
        'selection':'minimum validation BCE; thresholds descriptive only',
        'hardware':'NVIDIA A100-SXM4-40GB',
    })
    print('Prepared: identical33551 rows/labels; A6 and B/C/D37. No training yet.', flush=True)


def verified(root):
    cfg = configuration(root)
    if json.loads((root/'artifacts/config.json').read_text()) != cfg:
        raise ValueError('Study configuration changed')
    meta = verify_prepared(Path(cfg['data']['frame']), cfg)
    if meta['frame_sha256'] != FULL_SHA:
        raise ValueError('Study data identity changed')
    verify_frame(pd.read_parquet(cfg['data']['frame']), cfg)
    return cfg


def completed_runs(root):
    """Reject partial or ambiguous reports rather than selecting a favorable run."""
    runs = {}
    for name in NAMES:
        candidates = list((root/'runs').glob(name+'_*'))
        if len(candidates) != 1:
            raise ValueError(f'{name}: expected exactly one run')
        run = candidates[0]
        status = json.loads((run/'status.json').read_text())
        if status['status'] != 'complete':
            raise ValueError(f'{name}: training incomplete')
        summary = pd.read_csv(run/'validation_summary.csv')
        if len(summary)!=114 or set(zip(summary.seed,summary.fold))!={(s,f) for s in [42,43,44] for f in range(38)}:
            raise ValueError(f'{name}: incomplete seed/fold scope')
        runs[name] = run
    return runs


def report(root):
    cfg = verified(root)
    runs = completed_runs(root)
    curves, metrics, identities = [], [], {}
    grid = np.arange(201)/200
    for name,run in runs.items():
        protocol = json.loads((run/'protocol.json').read_text())
        expected_features = features()[0 if name=='A' else 1]
        if protocol['config'] != cfg or protocol['features'] != expected_features or protocol['data_sha256'] != FULL_SHA:
            raise ValueError('Run protocol does not match this comparison')
        summary = pd.read_csv(run/'validation_summary.csv').set_index(['seed','fold'])
        for seed in [42,43,44]:
            for fold in range(38):
                folder = run/f'seed_{seed}/fold_{fold:03d}'
                p = pd.read_parquet(folder/'validation_predictions.parquet')
                ident = p[['timestamp','label','source_row_position']]
                if len(p)!=1017 or not p.timestamp.is_unique or not p.timestamp.is_monotonic_increasing:
                    raise ValueError('Invalid validation predictions')
                if name=='A': identities[seed,fold] = ident
                else: pd.testing.assert_frame_equal(ident,identities[seed,fold])
                y = p.label.to_numpy(); prob = p.probability.to_numpy()
                if not np.isin(y,[0,1]).all() or not np.isfinite(prob).all() or not ((prob>=0)&(prob<=1)).all():
                    raise ValueError('Invalid labels/probabilities')
                decision = prob[:,None]>=grid
                n = decision.sum(0); tp = (decision & (y[:,None]==1)).sum(0)
                precision = np.divide(tp,n,out=np.zeros(201),where=n>0)
                recall = tp/y.sum(); f1 = 2*tp/(n+y.sum())
                for key,val in [('precision',precision),('recall',recall),('f1',f1)]:
                    if not np.isclose(val[100],summary.loc[(seed,fold),key],atol=1e-8):
                        raise ValueError('Recorded0.5 metrics differ')
                curves.append(pd.DataFrame(dict(model=name,seed=seed,fold=fold,threshold=grid,
                    precision=precision,recall=recall,f1=f1,signal_rate=n/len(y),
                    signals=n,no_signal=(n==0).astype(int))))
        m=summary.reset_index(); m['model']=name; metrics.append(m)
    out = root/'reports';out.mkdir(exist_ok=True)
    all_curves=pd.concat(curves,ignore_index=True)
    all_curves.to_csv(out/'thresholds_by_fold_seed.csv',index=False)
    means=all_curves.groupby(['model','threshold'])[['precision','recall','f1','signal_rate','signals','no_signal']].mean().reset_index()
    means.to_csv(out/'thresholds.csv',index=False)
    pd.concat(metrics).to_csv(out/'metrics_by_fold_seed.csv',index=False)
    pd.concat(metrics).groupby('model').mean(numeric_only=True).drop(columns=['seed','fold']).to_csv(out/'validation_summary.csv')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(13,9),layout='constrained')
    for ax,name in zip(axes.flat,NAMES):
        g=means[means.model==name]
        for col in ['precision','recall','f1','signal_rate']: ax.plot(g.threshold,g[col],label=col)
        ax.axvline(.5,color='grey',ls=':');ax.set(title=name+(' /6 GRU' if name=='A' else ' /37 '+cfg['experiments'][name]['architecture']),ylim=(0,1),xlabel='Threshold')
        ax.legend();ax.grid(alpha=.15)
    fig.suptitle('Validation only /38 folds x3 seeds; empty precision=0; no threshold selected')
    fig.savefig(out/'thresholds.png',dpi=160);plt.close(fig)
    (out/'README.md').write_text('# A6/B37/C37/D37\n\nValidation only; no final test. '
        'A–B isolates feature expansion; B/C/D compare architectures at37 identical inputs. '
        'A–C/D do not isolate architecture. Epoch and diagnostics reuse validation. '
        'Fold/seed observations overlap. Precision=0 for empty groups; no_signal is their fraction. '
        'Original T4 runs are historical context, not a paired A100 control.\n',encoding='utf-8')
    print('Reports:',out,flush=True)


def bundle(root):
    from datetime import datetime, timezone
    completed_runs(root)
    if not (root/'reports/thresholds.csv').exists():
        raise ValueError('Generate reports before bundling')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    dest=root/f'reports/feature_comparison_review_{stamp}.zip'
    with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for folder in ['runs','reports','artifacts','reproducibility']:
            for p in sorted((root/folder).rglob('*')):
                if p.is_file() and p.suffix in {'.json','.csv','.parquet','.md','.png'}:
                    z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(dest) as z:
        if z.testzip() is not None: raise ValueError('Review archive CRC failed')
    print('Review ZIP (no weights):',dest,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','report','bundle'])
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--legacy',type=Path,required=True)
    parser.add_argument('--allow-training',action='store_true')
    args=parser.parse_args();root=args.root.resolve();legacy=args.legacy.resolve()
    separate_workspace(root,legacy)
    if args.action=='train' and not args.allow_training: raise ValueError('Training requires --allow-training')
    root.mkdir(parents=True,exist_ok=True)
    freeze_workspace_identity(REPO,root,runtime_identity(REPO,require_gpu=True,hardware='selective-a100'))
    if args.action=='prepare':prepare(root,legacy)
    elif args.action=='train':
        cfg=verified(root)
        for name in NAMES: advisor.run(cfg,name)
    elif args.action=='report':report(root)
    else:bundle(root)


if __name__=='__main__': main()

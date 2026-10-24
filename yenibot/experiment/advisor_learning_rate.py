"""Single-factor B37 learning-rate experiment; historical control is read-only."""
import argparse
import copy
import json
from pathlib import Path
import zipfile

from yenibot.experiment.advisor_storage import immutable_json, sha256


def candidate_config(control, root):
    if control['training']['learning_rate'] != .001:
        raise ValueError('Expected original learning rate 0.001')
    cfg = copy.deepcopy(control)
    cfg['training']['learning_rate'] = .0001
    cfg['output'] = str(root / 'runs')
    return cfg


def one_run(root):
    runs = list((root/'runs').glob('B_*'))
    if len(runs) != 1:
        raise ValueError('Expected exactly one B run')
    return runs[0]


def load_runs(run):
    import numpy as np
    import pandas as pd
    rows, histories, identities = [], [], {}
    if json.loads((run/'status.json').read_text())['status'] != 'complete':
        raise ValueError('Training incomplete')
    for seed in (42, 43, 44):
        for fold in range(38):
            folder = run/f'seed_{seed}/fold_{fold:03d}'
            m = json.loads((folder/'validation_metrics.json').read_text())
            h = pd.read_csv(folder/'history.csv')
            p = pd.read_parquet(folder/'validation_predictions.parquet')
            if (m['status'] != 'complete' or m['test_evaluations'] != 0 or
                    m['seed'] != seed or m['fold'] != fold or
                    h.epoch.tolist() != list(range(1,len(h)+1)) or
                    not np.isfinite(h[['train_bce','bce','average_precision']]).all().all() or
                    m['best_epoch'] != int(h.loc[h.bce.idxmin(), 'epoch']) or
                    m['epochs_trained'] != len(h) or len(p) != 1017):
                raise ValueError('Incomplete/inconsistent fold')
            best=h.loc[h.bce.idxmin()]
            if not np.isclose(best.bce,m['validation']['bce'],atol=1e-7):
                raise ValueError('Selected metric mismatch')
            rows.append(dict(seed=seed, fold=fold, best_epoch=m['best_epoch'],
                             signals=int((p.probability >= .5).sum()), **m['validation']))
            histories.append(h.assign(seed=seed, fold=fold))
            identities[seed, fold] = p[['timestamp', 'label', 'source_row_position']]
    return pd.DataFrame(rows), pd.concat(histories), identities


def report(control_run, candidate_run, root):
    import pandas as pd
    import matplotlib.pyplot as plt
    a, ha, ia = load_runs(control_run)
    b, hb, ib = load_runs(candidate_run)
    for key in ia:
        pd.testing.assert_frame_equal(ia[key], ib[key])
    out = root/'reports'; out.mkdir(exist_ok=True)
    paired = a.merge(b, on=['seed', 'fold'], suffixes=('_control', '_candidate'), validate='one_to_one')
    for metric in ['bce', 'average_precision', 'best_epoch', 'precision', 'recall', 'f1', 'signals']:
        paired['delta_'+metric] = paired[metric+'_candidate'] - paired[metric+'_control']
    paired.to_csv(out/'paired.csv', index=False)
    metrics = ['bce', 'average_precision', 'best_epoch', 'precision', 'recall', 'f1', 'signals']
    combined = pd.concat([a.assign(learning_rate=.001), b.assign(learning_rate=.0001)])
    summary = combined.groupby('learning_rate')[metrics].mean()
    summary['bce_better_pairs'] = [int((paired.delta_bce < 0).sum()), int((paired.delta_bce > 0).sum())]
    summary.to_csv(out/'summary.csv')
    combined.groupby(['learning_rate', 'seed'])[metrics].mean().to_csv(out/'seed_summary.csv')
    limit = int(min(ha.groupby(['seed','fold']).epoch.max().min(), hb.groupby(['seed','fold']).epoch.max().min()))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout='constrained')
    for h, label, color in [(ha,'0.001 kontrol','#dc2626'),(hb,'0.0001 aday','#2563eb')]:
        g=h[h.epoch <= limit].groupby('epoch')[['train_bce','bce','average_precision']].mean()
        axes[0].plot(g.index,g.bce,color=color,label=label+' validation')
        axes[0].plot(g.index,g.train_bce,color=color,ls='--',label=label+' train')
        axes[1].plot(g.index,g.average_precision,color=color,label=label)
    for ax in axes: ax.set_xlabel('Epoch'); ax.legend(fontsize=8); ax.grid(alpha=.2)
    axes[0].set_ylabel('BCE (düşük iyi)'); axes[1].set_ylabel('Validation AP (yüksek iyi)')
    fig.suptitle('B37 GRU: aynı 114 eğitim; ortak epoch aralığı')
    fig.savefig(out/'comparison.png',dpi=150); plt.close(fig)
    (out/'README.md').write_text('# B37 öğrenme hızı karşılaştırması\n\n'
        'Yalnız validation; epoch minimum BCE ile seçildi. Eşik 0.5 değişmedi. '
        'Özet eşit fold/seed ortalaması; signals fold başınadır, benzersiz işlem sayısı değildir. '
        'Sıfır sinyalde kayıtlı precision=0; sinyal sayısıyla okuyun. '
        'Train kaybı güncelleme sırasında/dropout açık, validation epoch sonunda/eval. '
        'Foldlar örtüşür; validation epoch seçimi için de kullanıldı. '
        'Epoch ilerlemesi tek başına iyileşme değildir; paired.csv ve seed_summary.csv ile BCE/AP yönünü değerlendirin.\n',encoding='utf-8')
    with zipfile.ZipFile(out/'learning_rate_review.zip','w',zipfile.ZIP_DEFLATED) as z:
        for folder in ['runs','reports','artifacts','reproducibility']:
            for p in sorted((root/folder).rglob('*')):
                if p.is_file() and p.suffix in {'.csv','.json','.md','.png','.parquet'}:
                    z.write(p,p.relative_to(root).as_posix())
    print(summary.to_string(),flush=True)
    print('Raporlar:',out,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','report'])
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--root',type=Path,required=True)
    args=parser.parse_args(); source=args.source.resolve(); root=args.root.resolve()
    if root==source or root.is_relative_to(source) or source.is_relative_to(root):
        raise ValueError('Separate workspace required')
    from yenibot.experiment.advisor_feature_comparison import verified
    from yenibot.experiment.advisor_runtime import runtime_identity, freeze_workspace_identity
    from yenibot.experiment.advisor_workspace import REPO
    from yenibot.training import advisor
    control=verified(source)
    run=one_run(source)
    protocol=json.loads((run/'protocol.json').read_text())
    if protocol['config'] != control:
        raise ValueError('Control configuration mismatch')
    for path,digest in protocol['source_hashes'].items():
        relative=path.split('/advisor_feature_comparison_repo/')[1]
        if sha256(REPO/relative) != digest: raise ValueError('Training engine changed')
    identity=runtime_identity(REPO,require_gpu=True,hardware='selective-a100')
    import torch, numpy, pandas, sklearn, sys
    current=dict(torch=torch.__version__,numpy=numpy.__version__,pandas=pandas.__version__,
                 sklearn=sklearn.__version__,python=sys.version,gpu=torch.cuda.get_device_name(0),
                 cuda=torch.version.cuda,cudnn=torch.backends.cudnn.version())
    if any(protocol[k] != v for k,v in current.items()):
        raise ValueError('Control runtime differs; do not mix conditions')
    freeze_workspace_identity(REPO,root,identity)
    cfg=candidate_config(control,root)
    immutable_json(root/'artifacts/config.json',cfg)
    immutable_json(root/'artifacts/control.json',{'protocol':protocol,'sha256':sha256(run/'protocol.json')})
    evidence={str(p.relative_to(run)):sha256(p) for p in sorted(run.rglob('*'))
              if p.name in {'history.csv','validation_metrics.json','validation_predictions.parquet'}}
    if len(evidence)!=342: raise ValueError('Expected complete 114-run control evidence')
    immutable_json(root/'artifacts/control_evidence.json',evidence)
    if args.action=='prepare':
        load_runs(run)
        print('Verified control; only B37 learning rate changes: 0.001 -> 0.0001; 114 new trainings.')
    elif args.action=='train': advisor.run(cfg,'B')
    else:
        candidate=one_run(root)
        if json.loads((candidate/'protocol.json').read_text())['config'] != cfg:
            raise ValueError('Candidate configuration mismatch')
        report(run,candidate,root)


if __name__=='__main__': main()

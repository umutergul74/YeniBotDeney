"""Read-only validation threshold and development barrier diagnostics. No training."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def scores(labels, probabilities, thresholds):
    labels = np.asarray(labels)
    probabilities = np.asarray(probabilities)
    require(len(labels) == len(probabilities) and len(labels) > 0, 'Invalid sizes')
    require(np.isin(labels, [0, 1]).all(), 'Nonbinary labels')
    require(np.isfinite(probabilities).all() and ((probabilities >= 0) & (probabilities <= 1)).all(), 'Invalid probabilities')
    rows = []
    for threshold in thresholds:
        predicted = probabilities >= threshold
        tp = int(np.sum(predicted & (labels == 1)))
        fp = int(np.sum(predicted & (labels == 0)))
        fn = int(np.sum(~predicted & (labels == 1)))
        tn = int(np.sum(~predicted & (labels == 0)))
        rows.append({'threshold': float(threshold), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
                     'precision': tp / (tp + fp) if tp + fp else 0.,
                     'recall': tp / (tp + fn) if tp + fn else 0.,
                     'f1': 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.,
                     'positive_rate': (tp + fp) / len(labels)})
    return pd.DataFrame(rows)


def label_loop():
    # Load exactly the frozen module without importing the training package.
    spec = importlib.util.spec_from_file_location('diagnostic_frozen_labels', ROOT/'yenibot/labeling/triple_barrier.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module._label_loop_python


def atr14(raw):
    previous = raw.close.shift(1)
    return pd.concat([raw.high - raw.low, (raw.high - previous).abs(),
                      (raw.low - previous).abs()], axis=1).max(axis=1).rolling(14, min_periods=14).mean()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--detail', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and not args.detail.exists(), 'Output already exists; use a new run ID')
    args.output.mkdir(parents=True); args.detail.mkdir(parents=True)
    inventory = []
    def load(path, expected=None):
        actual = sha(path)
        if expected: require(actual == expected, 'Checksum mismatch: ' + str(path))
        inventory.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': actual, 'bytes': path.stat().st_size})
        return path
    legacy = ROOT/'evidence/drive_snapshot/colab_v1'
    frame_path = ROOT/'evidence/prepared_recovery/v2.0.1/data/development_wavelet_off.parquet'
    manifest = json.loads(load(frame_path.with_suffix('.manifest.json')).read_text())
    frame = pd.read_parquet(load(frame_path, manifest['frame_sha256']))
    frame.timestamp = pd.to_datetime(frame.timestamp, utc=True)
    require(len(frame) == 33551 and frame.timestamp.is_unique, 'Unexpected development sample')
    require(frame.timestamp.max() < pd.Timestamp('2026-01-01', tz='UTC'), 'Only historical development allowed')
    frame_index = frame.set_index('timestamp')
    review_path = ROOT/'evidence/colab_development/review_manifest.json'
    review = json.loads(load(review_path).read_text())
    checksums = {x['path']: x['sha256'] for x in review['files']}
    run = legacy/'runs/A_81029f6d6d48'
    def archived(path):
        key = path.relative_to(legacy).as_posix()
        require(key in checksums, 'Missing prediction/protocol proof')
        return load(path, checksums[key])
    protocol = json.loads(archived(run/'protocol.json').read_text())
    require(protocol['data_sha256'] == manifest['frame_sha256'], 'Wrong prepared table')
    require(protocol['test_evaluations'] == 0, 'Not a validation-only run')
    thresholds = np.arange(201) / 200
    per_fold, predictions = [], []
    baseline = pd.read_csv(archived(run/'validation_summary.csv')).set_index(['seed','fold'])
    require(set(baseline.index) == {(seed,fold) for seed in (42,43,44) for fold in range(38)}
            and baseline.index.is_unique, 'Unexpected fold/seed coverage')
    for seed in (42, 43, 44):
        for fold in range(38):
            p = pd.read_parquet(archived(run/f'seed_{seed}/fold_{fold:03d}/validation_predictions.parquet'))
            p.timestamp = pd.to_datetime(p.timestamp, utc=True)
            require(len(p) == 1017 and p.timestamp.is_unique, 'Invalid fold predictions')
            require(p.timestamp.is_monotonic_increasing, 'Unsorted predictions')
            original = frame_index.loc[p.timestamp]
            require(np.array_equal(p.label.to_numpy(), original.label.to_numpy()), 'Prediction label mismatch')
            require(np.allclose(p.forward_return, original.fwd_return_10h, rtol=1e-6, atol=1e-8), 'Forward return mismatch')
            curve = scores(p.label, p.probability, thresholds)
            at_half = curve.loc[curve.threshold == .5].iloc[0]
            for metric in ('precision', 'recall', 'f1'):
                require(np.isclose(at_half[metric], baseline.loc[(seed,fold),metric], atol=1e-10), 'Baseline metric mismatch')
            curve['seed'] = seed; curve['fold'] = fold; per_fold.append(curve)
            p['seed'] = seed; p['fold'] = fold; predictions.append(p)
    details = pd.concat(per_fold, ignore_index=True)
    pred = pd.concat(predictions, ignore_index=True)
    curve = details.groupby('threshold')[['precision','recall','f1','positive_rate']].mean().reset_index()
    best = curve.sort_values(['f1','threshold'], ascending=False).iloc[0]
    seed_curves = details.groupby(['seed','threshold'])[['precision','recall','f1','positive_rate']].mean().reset_index()
    pooled = details.groupby('threshold')[['tp','fp','fn','tn']].sum().reset_index()
    pooled['precision'] = (pooled.tp / (pooled.tp + pooled.fp)).fillna(0)
    pooled['recall'] = (pooled.tp / (pooled.tp + pooled.fn)).fillna(0)
    pooled['f1'] = (2*pooled.tp / (2*pooled.tp + pooled.fp + pooled.fn)).fillna(0)
    curve.to_csv(args.output/'threshold_metrics.csv', index=False)
    seed_curves.to_csv(args.output/'threshold_seed_metrics.csv', index=False)
    pooled.to_csv(args.output/'threshold_pooled_metrics.csv', index=False)
    details.to_csv(args.detail/'threshold_fold_metrics.csv', index=False)
    selected = curve[curve.threshold.isin([.2,.3,.4,.5,float(best.threshold)])]
    selected.to_csv(args.output/'threshold_summary.csv', index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11, 'axes.spines.top':False, 'axes.spines.right':False})
    fig, axes = plt.subplots(1, 2, figsize=(13,5), layout='constrained')
    for metric, label, color in [('precision','Precision','#2563eb'),('recall','Recall','#0d9488'),('f1','F1','#d97706')]:
        axes[0].plot(curve.threshold, curve[metric], label=label, color=color, linewidth=2.4)
    for ax in axes:
        ax.axvline(.5, color='#6b7280', linestyle='--', label='Mevcut eşik: 0,50')
        ax.axvline(best.threshold, color='#9d174d', linestyle=':', label=f'Betimsel F1 tepe noktası: {best.threshold:.3f}')
        ax.set(xlabel='Karar eşiği', ylabel='Skor', ylim=(0,1), xlim=(0,1)); ax.grid(alpha=.18)
    for seed, part in seed_curves.groupby('seed'):
        axes[1].plot(part.threshold, part.f1, label=f'Seed {seed}', linewidth=2)
    axes[0].set_title('Validation · 114 fold/seed ortalaması'); axes[1].set_title('F1 · Her seed için 38 fold ortalaması')
    axes[0].legend(fontsize=8); axes[1].legend(fontsize=8)
    fig.suptitle('Eşik değişince precision, recall ve F1 nasıl değişiyor?', fontweight='bold')
    fig.savefig(args.output/'threshold_curves.png', dpi=180); plt.close(fig)
    fig, ax = plt.subplots(figsize=(10,4.5), layout='constrained')
    for label, color in [(0,'#64748b'),(1,'#0d9488')]:
        ax.hist(pred.loc[pred.label == label,'probability'], bins=np.linspace(0,1,51), density=True,
                histtype='step', linewidth=2, label=f'Gerçek etiket {label}', color=color)
    ax.axvline(.5, color='#9d174d', linestyle='--', label='Mevcut eşik 0,50')
    ax.set(title='Validation skor dağılımı · örtüşen fold/seed kayıtları',xlabel='Modelin pozitif sınıf skoru',ylabel='Sınıf içinde yoğunluk')
    ax.legend(); fig.savefig(args.output/'score_distribution.png',dpi=180); plt.close(fig)

    raw_path = legacy/'inputs/market_snapshot_v1/btc_1h.parquet'
    raw = pd.read_parquet(load(raw_path,manifest['source_hashes']['1h']))
    raw.timestamp = pd.to_datetime(raw.timestamp, utc=True)
    raw = raw.loc[raw.timestamp <= frame.timestamp.max()+pd.Timedelta(hours=10)].reset_index(drop=True)
    require(raw.timestamp.is_unique and raw.timestamp.diff().dropna().eq(pd.Timedelta(hours=1)).all(), 'Raw hourly gaps')
    require(np.isfinite(raw[['close','high','low']]).all().all(), 'Nonfinite OHLC')
    positions = pd.Index(raw.timestamp).get_indexer(frame.timestamp)
    require((positions >= 0).all() and (positions+10 < len(raw)).all(), 'Missing target horizon')
    atr = atr14(raw).to_numpy()
    require(np.allclose(atr[positions], frame.atr_14, rtol=1e-12, atol=1e-10), 'ATR parity failed')
    for column in ('close','high','low'):
        require(np.array_equal(raw[column].to_numpy()[positions],frame[column].to_numpy()), 'OHLC parity failed')
    require(np.isfinite(atr[positions]).all() and (atr[positions] > 0).all(), 'Invalid ATR in shared sample')
    loop = label_loop()
    counts, returns, timeout_data = [], [], {}
    for tp, sl in [(2,5),(2,2),(3,2)]:
        labels, gains, hits, exits = loop(raw.close.to_numpy(),raw.high.to_numpy(),raw.low.to_numpy(),atr,tp,sl,10)
        y, gain, hit, exit_ = labels[positions], gains[positions], hits[positions], exits[positions]
        require((y >= 0).all(), 'Unlabelable rows in shared sample')
        if (tp,sl) == (2,5):
            require(np.array_equal(y,frame.label), 'Original label parity failed')
            mapping = {0:'time',1:'tp',2:'sl',3:'both_sl_first'}
            require(np.array_equal([mapping[int(x)] for x in hit],frame.hit_type), 'Original hit-type parity failed')
            require(np.allclose(gain,frame.tb_return,rtol=1e-12,atol=1e-12), 'Original return parity failed')
        name = f'{tp}/{sl}'
        n = len(y); profit = int((hit==1).sum()); stop = int(np.isin(hit,[2,3]).sum()); timeout = int((hit==0).sum())
        require(profit+stop+timeout == n, 'Category counts do not exhaust sample')
        counts.append({'tp_sl_atr':name,'n':n,'profit_first':profit,'stop_first':stop,'timeout':timeout,
                       'profit_pct':100*profit/n,'stop_pct':100*stop/n,'timeout_pct':100*timeout/n,
                       'both_same_bar_assigned_stop':int((hit==3).sum()),'positive_label_pct':100*float(y.mean())})
        timeout_returns = gain[hit==0]; timeout_data[name] = timeout_returns * 100
        require(np.allclose(timeout_returns,frame.fwd_return_10h.to_numpy()[hit==0],rtol=1e-12,atol=1e-12),'Timeout return parity')
        stats = pd.Series(timeout_returns)
        returns.append({'tp_sl_atr':name,'n':len(stats),'mean_pct':100*stats.mean(),'median_pct':100*stats.median(),
                        **{f'p{q}_pct':100*stats.quantile(q/100) for q in [5,25,75,95]},
                        'min_pct':100*stats.min(),'max_pct':100*stats.max(),
                        'positive_return_pct':100*(stats>0).mean()})
        pd.DataFrame({'timestamp':frame.timestamp,'label':y,'hit_code':hit,'return':gain,
                      'exit_timestamp':raw.timestamp.iloc[exit_].to_numpy()}).to_csv(args.detail/f'labels_tp{tp}_sl{sl}_h10.csv',index=False)
    counts = pd.DataFrame(counts); returns = pd.DataFrame(returns)
    counts.to_csv(args.output/'barrier_counts.csv',index=False)
    returns.to_csv(args.output/'timeout_returns_summary.csv',index=False)
    fig, ax = plt.subplots(figsize=(10,4.6), layout='constrained')
    left = np.zeros(3)
    for key,label,color in [('profit_pct','Kâr bariyeri önce','#0d9488'),('stop_pct','Zarar önce (çift temas dahil)','#e76f51'),('timeout_pct','10 saatte temas yok','#94a3b8')]:
        values = counts[key].to_numpy()
        ax.barh(counts.tp_sl_atr,values,left=left,label=label,color=color,height=.57)
        for i,value in enumerate(values):
            if value>4:ax.text(left[i]+value/2,i,f'%{value:.1f}',ha='center',va='center',color='white',fontweight='bold')
        left += values
    ax.set(xlim=(0,100),xlabel='Aynı 33.551 saatin yüzdesi',ylabel='Kâr / zarar · ATR çarpanı',title='Bariyerler değişince etiket dağılımı')
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.16),ncol=3,fontsize=9)
    fig.savefig(args.output/'barrier_distribution.png',dpi=180); plt.close(fig)
    fig, axes = plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    colors=['#2563eb','#0d9488','#d97706']
    for (name,values),color in zip(timeout_data.items(),colors):
        ordered=np.sort(values)
        axes[0].plot(ordered,np.arange(1,len(ordered)+1)/len(ordered),label=name,color=color)
    axes[0].set(xlabel='10 saatlik brüt getiri (%)',ylabel='Birikimli pay',title='Süre dolan örnekler · tüm dağılım'); axes[0].legend(title='TP/SL')
    axes[1].boxplot(list(timeout_data.values()),labels=list(timeout_data),showfliers=False)
    axes[1].set(xlabel='TP/SL · ATR',ylabel='10 saatlik brüt getiri (%)',title='Medyan ve çeyrekler · uç noktalar gizli')
    for ax in axes:ax.grid(alpha=.15)
    axes[0].axvline(0,color='#64748b',linestyle='--'); axes[1].axhline(0,color='#64748b',linestyle='--')
    fig.savefig(args.output/'timeout_returns_distribution.png',dpi=180);plt.close(fig)
    by_class=pred.groupby('label').probability.agg(['count','mean','median']).to_dict('index')
    summary={'threshold_optimum_descriptive':best.to_dict(),'threshold_at_0_5':curve.loc[curve.threshold==.5].iloc[0].to_dict(),
             'prediction_records':len(pred),'unique_validation_timestamps':pred.timestamp.nunique(),
             'validation_start':str(pred.timestamp.min()),'validation_end':str(pred.timestamp.max()),
             'zero_positive_folds_at_0_5':int((details.loc[details.threshold==.5,'tp']+details.loc[details.threshold==.5,'fp']==0).sum()),
             'score_by_class':by_class,'barriers':counts.to_dict('records'),'timeout_returns':returns.to_dict('records'),
             'sample_start':str(frame.timestamp.min()),'sample_end':str(frame.timestamp.max()),'excluded_from_shared_prepared_sample':0,
             'parity':{'atr':True,'original_labels':True,'original_hits':True,'original_returns':True,'threshold_0_5':True},
             'training_operations':0,'test_evaluations':0,'deployment_threshold_selected':False}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (args.output/'input_manifest.json').write_text(json.dumps({'inputs':inventory,'python':sys.version,'platform':platform.platform(),
       'numpy':np.__version__,'pandas':pd.__version__,'matplotlib':matplotlib.__version__,
       'analysis_script_sha256':sha(Path(__file__)),'frozen_label_code_sha256':sha(ROOT/'yenibot/labeling/triple_barrier.py'),
       'git_commit_at_execution':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()},indent=2)+'\n',encoding='utf-8')
    outputs=[{'path':p.resolve().relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
             for folder in [args.output,args.detail] for p in sorted(folder.iterdir()) if p.is_file()]
    (args.output/'output_manifest.json').write_text(json.dumps(outputs,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()

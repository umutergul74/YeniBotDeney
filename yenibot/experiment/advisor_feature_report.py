"""Descriptive reporting only; runs against the unchanged v1 training checkout.

No fitting, threshold selection, checkpoint loading or workspace identity changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd


def divide(numerator, denominator):
    numerator, denominator = np.broadcast_arrays(numerator, denominator)
    return np.divide(numerator, denominator, out=np.full(numerator.shape, np.nan), where=denominator > 0)


def threshold_counts(labels, probabilities, grid):
    y, p = np.asarray(labels), np.asarray(probabilities)
    if len(y) == 0 or not np.isin(y, [0, 1]).all() or not np.isfinite(p).all() or not ((p >= 0) & (p <= 1)).all():
        raise ValueError('Invalid validation labels/probabilities')
    decisions = p[:, None] >= grid
    tp = (decisions & (y[:, None] == 1)).sum(axis=0)
    signals = decisions.sum(axis=0)
    positives = int(y.sum())
    return pd.DataFrame(dict(threshold=grid, tp=tp, fp=signals-tp,
        fn=positives-tp, tn=len(y)-positives-signals+tp,
        signals=signals, samples=len(y), positives=positives,
        precision=divide(tp, signals), recall=divide(tp, positives),
        f1=divide(2*tp, signals+positives), signal_rate=signals/len(y)))


def aggregate(curves, keys):
    """Count-weighted metrics and active-group precision answer different questions."""
    grouped = curves.groupby(keys, sort=True)
    result = grouped[['tp', 'fp', 'fn', 'tn', 'signals', 'samples', 'positives']].sum()
    result['precision_signals'] = divide(result.tp, result.signals)
    result['recall'] = divide(result.tp, result.positives)
    result['f1'] = divide(2*result.tp, 2*result.tp+result.fp+result.fn)
    result['signal_rate'] = result.signals/result.samples
    result['precision_active_mean'] = grouped.precision.mean()
    result['precision_active_min'] = grouped.precision.min()
    result['groups'] = grouped.size()
    result['no_signal_groups'] = grouped.signals.apply(lambda s: int((s == 0).sum()))
    result['no_signal_fraction'] = result.no_signal_groups/result.groups
    result['signals_per_group_median'] = grouped.signals.median()
    result['signals_per_group_min'] = grouped.signals.min()
    return result.reset_index()


def paired_differences(metrics):
    rows = []
    for candidate, control in [('B', 'A'), ('C', 'B'), ('D', 'B')]:
        left = metrics[metrics.model == candidate].set_index(['seed', 'fold'])
        right = metrics[metrics.model == control].set_index(['seed', 'fold'])
        if not left.index.equals(right.index):
            raise ValueError('Unpaired fold/seed scope')
        for key in ['bce', 'average_precision']:
            delta = left[key]-right[key]
            for (seed, fold), value in delta.items():
                rows.append(dict(comparison=f'{candidate}-{control}', metric=key,
                                 seed=seed, fold=fold, delta=value))
    return pd.DataFrame(rows)


def collect(root, study):
    """Use the frozen study verifier; require all four scopes and paired rows."""
    study.verified(root)
    runs = study.completed_runs(root)
    curves, metrics, identities = [], [], {}
    from sklearn.metrics import average_precision_score
    grid = np.arange(201)/200
    for name, run in runs.items():
        summary = pd.read_csv(run/'validation_summary.csv').set_index(['seed', 'fold'])
        for seed, fold in summary.index:
            folder = run/f'seed_{seed}/fold_{fold:03d}'
            p = pd.read_parquet(folder/'validation_predictions.parquet')
            ident = p[['timestamp', 'label', 'source_row_position']].reset_index(drop=True)
            if len(p) != 1017 or not p.timestamp.is_unique or not p.timestamp.is_monotonic_increasing:
                raise ValueError('Invalid validation row scope')
            if name == 'A':
                identities[seed, fold] = ident
            else:
                pd.testing.assert_frame_equal(ident, identities[seed, fold])
            g = threshold_counts(p.label.to_numpy(), p.probability.to_numpy(), grid)
            row = summary.loc[(seed, fold)]
            reference = g.iloc[100]
            for key in ['precision', 'recall', 'f1']:
                # Frozen engine records zero for undefined binary metrics.
                if not np.isclose(np.nan_to_num(reference[key]), row[key], atol=1e-8):
                    raise ValueError('Prediction/summary threshold metrics differ')
            ap = average_precision_score(p.label, p.probability) if p.label.sum() else np.nan
            if not np.isclose(ap, row.average_precision, atol=1e-8, equal_nan=True):
                raise ValueError('Prediction/summary AP differs')
            meta = dict(model=name, seed=int(seed), fold=int(fold),
                        validation_start=str(p.timestamp.iloc[0]), validation_end=str(p.timestamp.iloc[-1]))
            for key, value in meta.items():
                g[key] = value
            curves.append(g)
            metrics.append({**row.to_dict(), **meta, 'signals': int(reference.signals),
                            'precision': reference.precision, 'recall': reference.recall,
                            'f1': reference.f1, 'signal_rate': reference.signal_rate})
    return pd.concat(curves, ignore_index=True), pd.DataFrame(metrics)


def figures(out, curves, metrics, totals, seeds):
    import matplotlib.pyplot as plt
    labels = {'A': 'A: 6 / GRU', 'B': 'B: 37 / GRU', 'C': 'C: 37 / TCN', 'D': 'D: 37 / TCN+GRU'}
    fig, axes = plt.subplots(2, 2, figsize=(13, 9), layout='constrained')
    for ax, metric, title in zip(axes.flat,
            ['precision_signals', 'recall', 'f1', 'signal_rate'],
            ['Sinyallerin precision değeri', 'Pozitifleri yakalama / recall', 'F1', 'Sinyal oranı']):
        for name, group in totals.groupby('model'):
            ax.plot(group.threshold, group[metric], label=labels[name])
        ax.axvline(.5, color='grey', ls=':')
        ax.set(title=title, xlabel='Karar eşiği', ylabel='Oran', ylim=(0, 1), xlim=(0, 1))
        ax.grid(alpha=.2); ax.legend(fontsize=8)
    fig.suptitle('Validation: sayılar toplanarak hesaplanır; örtüşen gözlemler bağımsız değildir\n'
                 'Precision yalnız sinyal varsa tanımlıdır; 0,50 çizgisi referanstır, seçim değildir')
    fig.savefig(out/'01_threshold_comparison.png', dpi=150); plt.close(fig)

    fig, axes = plt.subplots(3, 4, figsize=(19, 11), layout='constrained')
    for col, name in enumerate(labels):
        for seed, group in seeds[seeds.model == name].groupby('seed'):
            for ax, key in zip(axes[:, col], ['precision_signals', 'signal_rate', 'no_signal_fraction']):
                ax.plot(group.threshold, group[key], label=f'Seed {seed}')
                ax.axvline(.5, color='grey', ls=':'); ax.set(ylim=(0, 1), xlim=(0, 1), xlabel='Eşik')
                ax.grid(alpha=.2)
        axes[0, col].set_title(labels[name]); axes[0, col].legend()
    for ax, text in zip(axes[:, 0], ['Precision', 'Sinyal oranı', 'Sinyalsiz fold oranı']):
        ax.set_ylabel(text)
    fig.suptitle('Seed karşılaştırması: yüksek precision ile birlikte sinyal desteğini okuyun\n'
                 'Alt satırda 1,00: bu seed hiçbir fold içinde sinyal üretmedi')
    fig.savefig(out/'02_seed_thresholds.png', dpi=150); plt.close(fig)

    fig, axes = plt.subplots(3, 4, figsize=(19, 11), layout='constrained')
    for col, name in enumerate(labels):
        subset = metrics[metrics.model == name]
        for seed, group in subset.groupby('seed'):
            group = group.sort_values('fold')
            dates = pd.to_datetime(group.validation_end)
            for ax, key in zip(axes[:, col], ['bce', 'average_precision', 'signal_rate']):
                ax.plot(dates, group[key], label=f'Seed {seed}', alpha=.8)
                ax.grid(alpha=.2); ax.tick_params(axis='x', rotation=35)
        baseline = subset[subset.seed == subset.seed.min()].sort_values('fold')
        axes[1, col].plot(pd.to_datetime(baseline.validation_end), baseline.prevalence,
                         color='black', ls=':', label='Pozitif oranı (AP referansı)')
        axes[0, col].set_title(labels[name]); axes[0, col].legend(fontsize=8)
        axes[1, col].set_ylim(0, 1); axes[1, col].legend(fontsize=7)
        axes[2, col].set_ylim(0, 1)
    for ax, text in zip(axes[:, 0], ['BCE / düşük daha iyi', 'AP / yüksek daha iyi', '0,50 eşikte sinyal oranı']):
        ax.set_ylabel(text)
    fig.suptitle('Dönem ve seed farkları / x: validation tahminlerinin son tarihi\n'
                 '45 günlük pencereler 30 günlük adımla ilerler; sonuçlar örtüşür')
    fig.savefig(out/'03_period_stability.png', dpi=150); plt.close(fig)


def write_report(root, curves, metrics):
    out = root/'reports/explained_v1'
    out.mkdir(parents=True, exist_ok=True)
    totals = aggregate(curves, ['model', 'threshold'])
    seeds = aggregate(curves, ['model', 'seed', 'threshold'])
    latest = curves[curves.fold == curves.fold.max()]
    references = totals[totals.threshold.isin([.3, .4, .5, .6, .7, .8])]
    paired = paired_differences(metrics)
    summary = metrics.groupby('model')[['bce', 'average_precision', 'prevalence', 'best_epoch']].mean()
    summary.columns = ['mean_validation_bce', 'mean_validation_ap', 'positive_rate', 'mean_best_epoch']
    summary = summary.reset_index().merge(totals[totals.threshold == .5], on='model')
    tables = {'thresholds_by_fold_seed': curves, 'thresholds_all': totals,
              'thresholds_by_seed': seeds, 'reference_thresholds': references,
              'latest_fold_thresholds': latest, 'metrics_by_fold_seed': metrics,
              'paired_differences': paired, 'summary_at_050': summary}
    for name, table in tables.items():
        table.to_csv(out/f'{name}.csv', index=False)
    figures(out, curves, metrics, totals, seeds)
    notes = '''# 05 — Açıklanabilir validation raporu

## Hangi soruyu cevaplıyoruz?
A: 6 özellik GRU; B: 37 özellik GRU; C: 37 özellik TCN; D: 37 özellik paralel TCN+GRU.
A–B özellik genişletmesini, B–C–D aynı girdilerle mimarileri karşılaştırır.
A–C/D iki unsuru birlikte değiştirir. Parametre sayıları eşit değildir.
Etiket: 10 bar içinde 2×ATR TP'ye önce ulaşmak=1; 5×ATR SL veya timeout=0.
Bu, doğrudan TP/SL ikili ayrımı değildir; timeout da negatif sınıftadır.

## Önce hangi dosyayı okuyalım?
1. summary_at_050.csv: aynı 0,50 referansında modeller; BCE/AP eşikten bağımsızdır.
2. 01_threshold_comparison.png: eşik arttıkça precision, recall, F1 ve sinyal oranı.
3. 02_seed_thresholds.png: aynı eşikte seed farkı ve sinyalsiz fold oranı.
4. 03_period_stability.png: dönemlere göre BCE, AP ve 0,50 sinyal oranı.
5. latest_fold_thresholds.csv: son fold'da her seed/eşik için gerçek TP/FP ve sinyal sayısı.
6. paired_differences.csv: aynı fold/seed'de B−A, C−B, D−B; BCE farkı negatif,
   AP farkı pozitifse aday lehine. Bunlar bağımsızlık testi veya güven aralığı değildir.

## Precision ve destek nasıl okunur?
precision_signals = toplam TP / toplam sinyal. precision_active_mean = yalnız sinyal
veren fold/seed gruplarının precision ortalaması. Farklı soruları cevaplarlar.
Sinyal yoksa precision BOŞ/NaN'dır; başarı veya sıfır precision anlamına gelmez.
Her zaman signals, signals_per_group_min ve no_signal_fraction ile birlikte okuyun.
Az sayıda sinyalde yüksek precision tek başına güçlü kanıt değildir.
Sayım toplamları örtüşen validation pencereleri ve seed tekrarlarını içerir;
benzersiz işlem sayısı, bağımsız örneklem veya strateji getirisi değildir.
Pozitif yoksa recall, pozitif ve sinyal ikisi de yoksa F1 tanımsız bırakılır.

## Karar sınırları
Epoch minimum validation BCE ile seçildi; aynı validation üzerinde bu rapor üretildi.
Bu seçim sonrası geliştirme raporudur; bağımsız nihai başarı ölçümü değildir.
AP için grafikteki pozitif oranı becerisiz sıralamanın referansıdır, garanti değildir.
Ham sigmoid skorları kalibre edilmiş olasılık kabul edilmez.
0,30–0,80 referansları yalnız gösterimdir. %60/%65/%70 precision hedefi, en iyi
eşik veya kazanan otomatik seçilmez. Son dönem uyumu ve seed farkları görülmeden
genel ortalamadan işlem eşiği çıkarılmaz. Eğitim/veri/bölmeler ve test durumu değişmedi.
'''
    (out/'README.md').write_text(notes, encoding='utf-8')
    print(summary[['model', 'mean_validation_bce', 'mean_validation_ap', 'precision_signals',
                   'recall', 'f1', 'signal_rate', 'no_signal_fraction']].to_string(index=False))
    print('Açıklanabilir raporlar:', out, flush=True)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.repo.resolve()))
    from yenibot.experiment import advisor_feature_comparison as study
    # Re-run the frozen report's strict protocol validation before new views.
    study.report(args.root)
    curves, metrics = collect(args.root, study)
    out = write_report(args.root, curves, metrics)
    payload = Path(__file__).read_bytes()
    (out/'report_identity.json').write_text(json.dumps({
        'report_schema': 1, 'helper_sha256': hashlib.sha256(payload).hexdigest(),
        'training_modified': False, 'test_evaluations': 0}, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()

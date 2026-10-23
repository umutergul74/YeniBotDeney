"""Read-only validation diagnostics. No training, labeling or test evaluation."""
from pathlib import Path
import hashlib
import io
import json
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
DETAIL = ROOT/'reports/barrier-economics-20261023'
GRID = np.arange(101)/100
CANDIDATES = {'B25': (2, 5), 'B11': (1, 1), 'B22': (2, 2), 'B12': (1, 2)}
SEEDS = [42, 43, 44]


def metrics(frame, threshold):
    selected = frame.loc[frame.probability >= threshold]
    n = len(selected)
    result = dict(threshold=threshold, samples=len(frame), signals=n,
                  signal_rate=n/len(frame), tp_rate=np.nan, sl_rate=np.nan,
                  timeout_rate=np.nan, both_rate=np.nan)
    for col, prefix in [('barrier_return', 'exit'), ('forward_return_10h', 'h10')]:
        r = selected[col]
        result.update({prefix+'_mean_pct': r.mean()*100,
                       prefix+'_median_pct': r.median()*100 if n else np.nan,
                       prefix+'_win_pct': (r > 0).mean()*100 if n else np.nan,
                       prefix+'_baseline_pct': frame[col].mean()*100,
                       prefix+'_lift_pp': (r.mean()-frame[col].mean())*100})
    if n:
        result.update(tp_rate=(selected.hit_code == 1).mean(),
                      sl_rate=selected.hit_code.isin([2, 3]).mean(),
                      timeout_rate=(selected.hit_code == 0).mean(),
                      both_rate=(selected.hit_code == 3).mean())
    return result


def self_check():
    f = pd.DataFrame({'probability': [.8, .5, .2], 'hit_code': [1, 2, 0],
                      'barrier_return': [.02, -.05, .01],
                      'forward_return_10h': [-.01, .02, .01]})
    m = metrics(f, .5)
    assert m['signals'] == 2 and np.isclose(m['exit_mean_pct'], -1.5)
    assert m['exit_win_pct'] == 50 and np.isclose(m['h10_mean_pct'], .5)
    assert m['tp_rate'] == .5 and m['sl_rate'] == .5
    empty = metrics(f, .9)
    assert empty['signals'] == 0 and np.isnan(empty['exit_mean_pct'])
    assert np.isnan(empty['exit_win_pct'])
    m = metrics(f, 0)
    assert m['signals'] == 3 and abs(m['exit_lift_pp']) < 1e-12


def main():
    self_check()
    DETAIL.mkdir(parents=True, exist_ok=True)
    inventory = []
    def check(path, expected):
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == expected, str(path)
        inventory.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': digest})
        return data
    source = ROOT/'reports/review-20261017/source.zip'
    check(source, '76d09912ab27349d003041a4f2356fbe989cbd76601feaa4793d8e342ca16eff')
    z = zipfile.ZipFile(source)
    manifest_path = ROOT/'research/analyses/barrier-expansion-20261015/results/output_manifest.json'
    hashes = {r['path']: r['sha256'] for r in json.loads(manifest_path.read_text())}
    base_path = ROOT/'evidence/prepared_recovery/v2.0.1/data/development_wavelet_off.parquet'
    check(base_path, 'f6346a93ee4b97125d00e8d26223ba11a141806cdff675934e033a00940977a8')
    base = pd.read_parquet(base_path)
    cohort = json.loads(z.read('artifacts/cohort.json'))
    groups, unique, yearly, identity = [], [], [], {}
    protocol_anchor = None
    for candidate, (tp, sl) in CANDIDATES.items():
        label_path = ROOT/f'output/advisor_experiments/barrier-expansion-20261015/labels_tp{tp}_sl{sl}.csv'
        labels = pd.read_csv(io.BytesIO(check(label_path, hashes[label_path.relative_to(ROOT).as_posix()])))
        labels.timestamp = pd.to_datetime(labels.timestamp, utc=True)
        assert len(labels) == 33551 and labels.timestamp.is_unique
        assert np.array_equal(labels.timestamp, base.timestamp)
        expected = np.where(labels.hit_code == 1, tp*base.atr_14/base.close,
                   np.where(labels.hit_code.isin([2, 3]), -sl*base.atr_14/base.close,
                            labels.forward_return_10h))
        assert np.allclose(expected, labels.barrier_return, atol=1e-12, rtol=1e-10)
        assert np.array_equal(labels.label, (labels.hit_code == 1).astype(int))
        assert np.allclose(labels.forward_return_10h, base.fwd_return_10h, atol=1e-12)
        reviews = json.loads(z.read(f'reports/{candidate}/review.json'))['files']
        def read(name):
            content = z.read(name)
            if name in reviews:
                assert hashlib.sha256(content).hexdigest() == reviews[name], name
            return content
        names = [n for n in z.namelist() if n.startswith('runs/'+candidate+'_') and n.endswith('/validation_predictions.parquet')]
        assert len(names) == 114
        protocols = [n for n in z.namelist() if n.startswith('runs/'+candidate+'_') and n.endswith('/protocol.json')]
        assert len(protocols) == 1
        protocol = json.loads(read(protocols[0]))
        cfg = protocol['config']
        assert protocol['test_evaluations'] == 0 and protocol['selection'] == 'validation_bce_only'
        assert protocol['folds'] == list(range(38)) and protocol['seeds'] == SEEDS
        assert protocol['data_sha256'] == cohort['candidates'][candidate]['frame_sha256']
        assert len(protocol['features']) == 6 and cfg['data']['wavelet'] is False
        assert cfg['labeling'] == dict(max_holding_bars=10, tp_multiplier=float(tp), sl_multiplier=float(sl))
        common = {k: cfg[k] for k in ['training', 'model', 'walk_forward', 'development']}
        common['features'] = protocol['features']
        common['architecture'] = cfg['experiments'][candidate]['architecture']
        assert common['architecture'] == 'gru'
        if protocol_anchor is None: protocol_anchor = common
        else: assert common == protocol_anchor
        previous = pd.read_csv(io.BytesIO(z.read(f'reports/{candidate}/thresholds_by_fold_seed.csv')))
        parts, seen = [], set()
        for name in sorted(names):
            assert name in reviews
            p = pd.read_parquet(io.BytesIO(read(name)))
            meta = json.loads(read(name.replace('validation_predictions.parquet', 'validation_metrics.json')))
            seed, fold = meta['seed'], meta['fold']
            assert (seed, fold) not in seen
            seen.add((seed, fold))
            assert meta['test_evaluations'] == 0
            p.timestamp = pd.to_datetime(p.timestamp, utc=True)
            assert len(p) == 1017 and p.timestamp.is_unique and p.timestamp.is_monotonic_increasing
            assert p.timestamp.max() < pd.Timestamp('2026-01-01', tz='UTC')
            assert np.isfinite(p.probability).all() and p.probability.between(0, 1).all()
            ident = p[['timestamp', 'source_row_position', 'forward_return']]
            if candidate == 'B25': identity[seed, fold] = ident
            else: pd.testing.assert_frame_equal(ident, identity[seed, fold])
            joined = p.merge(labels, on='timestamp', how='left', validate='one_to_one', suffixes=('', '_verified'))
            assert np.array_equal(joined.label, joined.label_verified)
            assert np.allclose(joined.forward_return, joined.forward_return_10h, atol=1e-12)
            assert np.isfinite(joined[['barrier_return', 'forward_return_10h']]).all().all()
            old = previous[(previous.seed == seed) & (previous.fold == fold) & np.isclose(previous.threshold, .5)].iloc[0]
            selected = joined[joined.probability >= .5]
            assert len(selected) == old.signals and selected.label.sum() == old.tp
            joined['seed'] = seed; joined['fold'] = fold
            parts.append(joined)
            groups.extend(dict(candidate=candidate, seed=seed, fold=fold, **metrics(joined, t)) for t in GRID)
        assert seen == {(s, f) for s in SEEDS for f in range(38)}
        all_rows = pd.concat(parts, ignore_index=True)
        for seed in SEEDS:
            data = all_rows[all_rows.seed == seed].sort_values(['timestamp', 'fold']).drop_duplicates('timestamp', keep='last')
            assert len(data) == 27657
            for t in GRID:
                unique.append(dict(candidate=candidate, seed=seed, **metrics(data, t)))
            for year, frame in data.groupby(data.timestamp.dt.year):
                for t in [0., .3, .4, .5, .6, .7]:
                    yearly.append(dict(candidate=candidate, seed=seed, year=year, **metrics(frame, t)))
        print(candidate, '114 groups verified; 27657 unique validation hours per seed', flush=True)
    group_table = pd.DataFrame(groups)
    group_table.to_csv(DETAIL/'fold_seed_metrics.csv', index=False)
    reference = group_table[group_table.threshold.eq(.5)]
    reference[reference.fold.eq(37)].to_csv(OUT/'last_fold_threshold05.csv', index=False)
    reference.groupby('candidate').agg(
        active_groups=('signals', lambda s: (s > 0).sum()),
        positive_groups=('exit_mean_pct', lambda s: (s > 0).sum()),
        mean_exit_active_pct=('exit_mean_pct', 'mean'),
        mean_h10_active_pct=('h10_mean_pct', 'mean'),
        mean_signals=('signals', 'mean')).to_csv(OUT/'fold_macro_threshold05.csv')
    u = pd.DataFrame(unique)
    u.to_csv(OUT/'seed_thresholds.csv', index=False)
    pd.DataFrame(yearly).to_csv(OUT/'year_seed_metrics.csv', index=False)
    summary = u.groupby(['candidate', 'threshold']).agg(
        signals_mean=('signals', 'mean'), signals_min=('signals', 'min'), signals_max=('signals', 'max'),
        active_seeds=('signals', lambda s: int((s > 0).sum())),
        exit_mean_pct=('exit_mean_pct', 'mean'), exit_min_pct=('exit_mean_pct', 'min'), exit_max_pct=('exit_mean_pct', 'max'),
        exit_win_pct=('exit_win_pct', 'mean'), exit_lift_pp=('exit_lift_pp', 'mean'),
        h10_mean_pct=('h10_mean_pct', 'mean'), h10_win_pct=('h10_win_pct', 'mean'),
        h10_lift_pp=('h10_lift_pp', 'mean'), tp_rate=('tp_rate', 'mean'),
        sl_rate=('sl_rate', 'mean'), timeout_rate=('timeout_rate', 'mean')).reset_index()
    summary.to_csv(OUT/'threshold_summary.csv', index=False)
    summary[summary.threshold.isin([0., .3, .4, .5, .6, .7])].to_csv(OUT/'selected_thresholds.csv', index=False)
    for name in ['seed_thresholds.csv', 'year_seed_metrics.csv', 'threshold_summary.csv',
                 'selected_thresholds.csv', 'last_fold_threshold05.csv', 'fold_macro_threshold05.csv']:
        old = pd.read_csv(OUT.parent/'barrier-economics-20261022'/name)
        current = pd.read_csv(OUT/name)
        pd.testing.assert_frame_equal(old, current[current.candidate != 'B12'].reset_index(drop=True), check_exact=True)
    (OUT/'input_manifest.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
    (OUT/'checks.json').write_text(json.dumps(dict(prediction_files=114*len(CANDIDATES), groups=114*len(CANDIDATES),
        raw_predictions_per_candidate=115938, unique_hours_per_seed=27657,
        test_files_read=0, prior_candidate_tables_identical=6,
        tests='synthetic metric checks; SHA256; cohort/label/return/protocol/0.5 parity passed'), indent=2))
    render(u)
    write_manifest()


def render(u):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    for prefix, title in [('exit', 'TP / SL / süre dolumunda çıkış'), ('h10', 'Bariyerden bağımsız, 10. saat kapanışında çıkış')]:
        fig, axes = plt.subplots(3, len(CANDIDATES), figsize=(19, 10), layout='constrained')
        for j, (candidate, (tp, sl)) in enumerate(CANDIDATES.items()):
            for seed, color in zip(SEEDS, ['#2563eb', '#d97706', '#0d9488']):
                d = u[(u.candidate == candidate) & (u.seed == seed)]
                for row, col in enumerate([prefix+'_mean_pct', prefix+'_win_pct', 'signals']):
                    ax = axes[row, j]
                    ax.plot(d.threshold, d[col], color=color, label=f'Seed {seed}', lw=1.5)
                    sparse = d[(d.signals > 0) & (d.signals < 100)]
                    ax.scatter(sparse.threshold, sparse[col], color=color, marker='x', s=12)
                    ax.axvline(.5, color='#64748b', ls=':', lw=1)
                    ax.set(xlim=(0, 1), xlabel='Karar eşiği'); ax.grid(alpha=.15)
            axes[0, j].set_title(f'{candidate} · TP {tp} / SL {sl} ATR')
            baseline = u[(u.candidate == candidate) & (u.threshold == 0)][prefix+'_mean_pct'].mean()
            axes[0, j].axhline(0, color='black', lw=.8)
            axes[0, j].axhline(baseline, color='#9333ea', ls='--', label='Tüm saatleri alma referansı')
            axes[1, j].set_ylim(0, 100)
            axes[2, j].set_yscale('symlog', linthresh=10)
            axes[2, j].set_ylim(0, 30000)
        axes[0, 0].set_ylabel('Sinyal başına ortalama brüt getiri (%)')
        axes[1, 0].set_ylabel('Pozitif getiriyle kapanan sinyaller (%)')
        axes[2, 0].set_ylabel('Sinyal sayısı / seed (log ölçek)')
        axes[0, 0].legend(fontsize=8)
        fig.suptitle(title+'\nValidation: aynı 27.657 saat; seedler ayrı, örtüşen foldlar tekilleştirildi', fontsize=15)
        fig.supxlabel('×: 100’den az sinyal, yalnız küçük örnek uyarısı. Sinyalsiz getiri tanımsız. Masrafsız; portföy backtesti değil.', fontsize=10)
        fig.savefig(OUT/f'{prefix}_thresholds.png', dpi=160); plt.close(fig)


def write_manifest():
    outputs = []
    for p in sorted(OUT.iterdir()):
        if p.is_file() and p.name != 'output_manifest.json':
            outputs.append(dict(path=p.name, sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    (OUT/'output_manifest.json').write_text(json.dumps(outputs, indent=2), encoding='utf-8')


if __name__ == '__main__':
    import sys
    if '--plots-only' in sys.argv:
        render(pd.read_csv(OUT/'seed_thresholds.csv'))
        write_manifest()
    else:
        main()

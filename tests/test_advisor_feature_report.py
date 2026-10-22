"""Reporting regressions on synthetic predictions; no training or final test."""
import json
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import precision_score, recall_score, f1_score

from yenibot.experiment import advisor_feature_report as report
from scripts.build_advisor_feature_notebook import build


def test_counts_match_binary_metrics_and_keep_undefined_precision():
    y = np.array([1, 0, 1, 0, 0])
    probabilities = np.array([.8, .7, .4, .3, .2])
    grid = np.array([0, .5, .9])
    result = report.threshold_counts(y, probabilities, grid)
    for i, threshold in enumerate(grid):
        decision = probabilities >= threshold
        assert result.iloc[i].signals == decision.sum()
        assert result.iloc[i][['tp', 'fp', 'fn', 'tn']].sum() == len(y)
        assert result.iloc[i].recall == pytest.approx(recall_score(y, decision))
        assert result.iloc[i].f1 == pytest.approx(f1_score(y, decision))
        if decision.any():
            assert result.iloc[i].precision == pytest.approx(precision_score(y, decision))
        else:
            assert pd.isna(result.iloc[i].precision)


def test_no_positive_and_no_signal_does_not_fabricate_metrics():
    result = report.threshold_counts(np.zeros(3), np.zeros(3), np.array([.5]))
    assert result[['precision', 'recall', 'f1']].isna().all().all()
    assert result.signals.iloc[0] == 0


def test_aggregation_separates_signal_weighting_and_empty_groups():
    groups = []
    for seed, labels, probabilities in [
            (42, [1]*9+[0], [.8]*10),
            (43, [1]*9+[0], [.1]*10),
            (44, [0]*10, [.8]+[.1]*9)]:
        group = report.threshold_counts(labels, probabilities, np.array([.5]))
        group['model'], group['seed'], group['fold'] = 'A', seed, 0
        groups.append(group)
    result = report.aggregate(pd.concat(groups), ['model', 'threshold']).iloc[0]
    assert result.precision_signals == pytest.approx(9/11)
    assert result.precision_active_mean == pytest.approx(.45)
    assert result.no_signal_groups == 1
    assert result.no_signal_fraction == pytest.approx(1/3)
    assert result.signals == 11 and result.signals_per_group_min == 0


def sample_tables():
    curves, metrics = [], []
    for model in 'ABCD':
        for seed in [42, 43, 44]:
            for fold in range(2):
                group = report.threshold_counts([1, 0, 1, 0],
                    [.8, .7, .4, .1] if seed != 43 else [.3]*4, np.arange(201)/200)
                meta = dict(model=model, seed=seed, fold=fold,
                    validation_start=f'2025-0{fold+1}-01', validation_end=f'2025-0{fold+2}-01')
                for key, value in meta.items():
                    group[key] = value
                curves.append(group)
                metrics.append({**meta, **group.iloc[100].to_dict(),
                                'bce': .6, 'average_precision': .6, 'prevalence': .5, 'best_epoch': 3})
    return pd.concat(curves, ignore_index=True), pd.DataFrame(metrics)


def test_paired_differences_preserve_seed_fold_and_direction():
    _, metrics = sample_tables()
    metrics.loc[metrics.model == 'B', 'bce'] -= .1
    delta = report.paired_differences(metrics)
    chosen = delta[(delta.comparison == 'B-A') & (delta.metric == 'bce')]
    assert len(chosen) == 6
    assert np.allclose(chosen.delta, -.1)
    with pytest.raises(ValueError, match='Unpaired'):
        report.paired_differences(metrics.iloc[1:])


def test_complete_report_preserves_predictions_and_outputs_support(tmp_path):
    curves, metrics = sample_tables()
    before = curves.copy(deep=True)
    out = report.write_report(tmp_path, curves, metrics)
    pd.testing.assert_frame_equal(curves, before)
    summary = pd.read_csv(out/'summary_at_050.csv')
    assert len(summary) == 4
    assert np.allclose(summary.no_signal_fraction, 1/3)
    latest = pd.read_csv(out/'latest_fold_thresholds.csv')
    assert set(latest.fold) == {1}
    assert len(latest) == 4*3*201
    assert latest[(latest.seed == 43) & (latest.threshold == .5)].precision.isna().all()
    assert len(list(out.glob('*.png'))) == 3
    assert len(list(out.glob('*.csv'))) == 8
    assert 'timeout=0' in (out/'README.md').read_text(encoding='utf-8')


def test_notebook_keeps_frozen_training_and_separate_report_hash():
    notebook = build()
    code = '\n'.join(c['source'] for c in notebook['cells'] if c['cell_type'] == 'code')
    assert "RELEASE='advisor-feature-comparison-v1.0.0'" in code
    assert "REPORT_RELEASE='advisor-feature-reports-v1.0.0'" in code
    helper = Path(__file__).resolve().parents[1]/'yenibot/experiment/advisor_feature_report.py'
    assert hashlib.sha256(helper.read_bytes()).hexdigest() in code
    assert 'explained_report.log' in code
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            compile(cell['source'], '05', 'exec')


def test_collect_checks_paired_rows_and_recorded_ap(tmp_path):
    from types import SimpleNamespace
    from sklearn.metrics import average_precision_score
    runs = {}
    for name in 'ABCD':
        run = tmp_path/name
        folder = run/'seed_42/fold_000'
        folder.mkdir(parents=True)
        labels = np.arange(1017) % 2
        p = pd.DataFrame(dict(timestamp=pd.date_range('2025-01-01', periods=1017, freq='h', tz='UTC'),
                              source_row_position=np.arange(63, 1080), label=labels,
                              probability=np.where(labels, .8, .2)))
        p.to_parquet(folder/'validation_predictions.parquet', index=False)
        pd.DataFrame([dict(seed=42, fold=0, precision=1., recall=1., f1=1.,
            average_precision=average_precision_score(labels, p.probability), bce=.2,
            prevalence=labels.mean(), best_epoch=3)]).to_csv(run/'validation_summary.csv', index=False)
        runs[name] = run
    study = SimpleNamespace(verified=lambda root: None, completed_runs=lambda root: runs)
    curves, metrics = report.collect(tmp_path, study)
    assert len(curves) == 4*201 and len(metrics) == 4
    path = runs['B']/'seed_42/fold_000/validation_predictions.parquet'
    wrong = pd.read_parquet(path)
    wrong.loc[0, 'source_row_position'] = 9999
    wrong.to_parquet(path, index=False)
    with pytest.raises(AssertionError):
        report.collect(tmp_path, study)
    wrong.loc[0, 'source_row_position'] = 63
    wrong['probability'] = 1-wrong.probability
    wrong.to_parquet(path, index=False)
    with pytest.raises(ValueError, match='threshold metrics differ'):
        report.collect(tmp_path, study)

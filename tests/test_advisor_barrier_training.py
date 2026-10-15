"""Scientific boundary/selection/freeze regressions; no real training or network."""
import copy
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from yenibot.experiment import advisor_barrier_training as study


def test_splits_cover_exact_common_hours_with_no_label_leakage():
    dates = study.validate_dates(study.DATES)
    times = pd.date_range(dates['train_start'], dates['calibration_end'], freq='h')
    frame = pd.DataFrame({'timestamp': times, 'label_end_timestamp': times+pd.Timedelta(hours=10)})
    split = study.split_indices(frame)
    assert (len(split.train), len(split.val), len(split.test)) == (5040, 552, 504)
    assert frame.iloc[split.train[-1]].label_end_timestamp < frame.iloc[split.val[0]].timestamp
    assert frame.iloc[split.val[-1]].label_end_timestamp < frame.iloc[split.test[0]].timestamp
    with pytest.raises(ValueError, match='Missing split hours'):
        study.split_indices(frame.drop(index=split.val[10]).reset_index(drop=True))


@pytest.mark.parametrize('field,value', [
    ('test_start','2026-09-01T00:00:00Z'),
    ('test_start','2026-10-01T12:00:00Z'),
    ('calibration_start','2026-08-09T00:00:00Z'),
    ('validation_start','2026-07-17T00:30:00Z'),
])
def test_forbidden_dates_fail(field,value):
    dates = copy.deepcopy(study.DATES); dates[field] = value
    with pytest.raises(ValueError): study.validate_dates(dates)


def test_threshold_uses_mean_seed_f1_and_highest_tie():
    p = pd.DataFrame({'label':[0,0,1,1], 'probability':[.1,.2,.6,.8]})
    best, curve = study.choose_threshold([p,p,p], .5)
    assert len(curve) == 201
    assert best['f1'] == 1
    assert best['threshold'] == pytest.approx(.6)
    assert best['all_positive_f1'] == pytest.approx(2/3)
    assert best['bce_skill'] > 0


def test_test_cannot_download_without_freeze(tmp_path):
    with patch.object(study.advisor_final,'extend_source') as download:
        with pytest.raises(FileNotFoundError): study.test(tmp_path)
        download.assert_not_called()


def test_freeze_detects_mutated_weights(tmp_path):
    p = tmp_path/'weights.pt'; p.write_bytes(b'original')
    (tmp_path/'artifacts').mkdir()
    (tmp_path/'artifacts/freeze.json').write_text(json.dumps({
        'plan_sha256': study.digest(study.plan()), 'files': {'weights.pt': study.sha256(p)}}))
    study.verify_freeze(tmp_path)
    p.write_bytes(b'changed')
    with pytest.raises(ValueError,match='Frozen artifact changed'): study.verify_freeze(tmp_path)


def test_prepared_frame_never_overwrites_mismatch(tmp_path):
    p = tmp_path/'prepared.parquet'
    study.save_frame(p, pd.DataFrame({'x':[1]}))
    study.save_frame(p, pd.DataFrame({'x':[1]}))
    with pytest.raises(ValueError,match='Refusing to replace'):
        study.save_frame(p,pd.DataFrame({'x':[2]}))
    assert study.load_frame(p).x.tolist() == [1]


def test_notebook_default_does_not_train_or_test():
    path = Path(__file__).resolve().parents[1]/'notebooks/workflows/04_barrier_study.ipynb'
    nb = json.loads(path.read_text(encoding='utf-8'))
    context = {}; exec(nb['cells'][2]['source'], context)
    calls = []; context['execute_step'] = calls.append
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and cell['source'].startswith(('if ALLOW_TRAINING:', 'if ALLOW_TEST:')):
            exec(cell['source'], context)
    assert calls == []
    assert context['EXPERIMENTS'] == list(study.CANDIDATES)

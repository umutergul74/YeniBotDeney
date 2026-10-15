"""Fixed-cohort and selective-report contracts, using synthetic data only."""
import copy
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from yenibot.experiment import advisor_selective as study


def frame():
    times=pd.date_range('2022-03-01T04:00:00Z','2025-12-28T02:00:00Z',freq='h')
    return pd.DataFrame({'timestamp':times,'label_end_timestamp':times+pd.Timedelta(hours=10)})


def test_original_cohort_and_sequence_counts(tmp_path):
    cfg=study.configuration(tmp_path,'B25');data=frame()
    folds=study.cohort(data,cfg)
    assert len(folds)==38
    assert [(len(f.train)-63,len(f.val)-63,len(f.test)-63) for f in folds]==[(4977,1017,657)]*38
    assert folds[1].train[0]-folds[0].train[0]==720
    for change in ['short','dates','validation','seed','sequence']:
        c=copy.deepcopy(cfg);d=data.copy()
        if change=='short':d=d.iloc[:-1]
        elif change=='dates':d.timestamp+=pd.Timedelta(hours=1)
        elif change=='validation':c['walk_forward']['val_bars']=552
        elif change=='seed':c['training']['seeds']=[42]
        else:c['model']['seq_len']=32
        with pytest.raises(ValueError):study.cohort(d,c)


def test_candidates_only_change_labels_and_output_identity(tmp_path):
    base=study.configuration(tmp_path,'B25')
    for name,(tp,sl) in study.CANDIDATES.items():
        cfg=study.configuration(tmp_path,name)
        assert cfg['labeling']==dict(max_holding_bars=10,tp_multiplier=tp,sl_multiplier=sl)
        cfg['labeling']=base['labeling'];cfg['data']['frame']=base['data']['frame'];cfg['experiments']=base['experiments']
        assert cfg==base


def test_no_signal_is_not_perfect_precision_and_timeout_is_separate():
    curve=study.threshold_rows([1,0,0,0],[.8,.7,.3,.2],['tp','sl','time','both_sl_first'])
    all_signals=curve.iloc[0];none=curve.iloc[-1]
    assert all_signals.precision==.25 and all_signals.recall==1
    assert all_signals.selected_sl==2 and all_signals.selected_timeout==1 and all_signals.selected_both==1
    assert np.isnan(none.precision) and none.signals==0
    summary=study.summarize(curve)
    assert summary.iloc[-1].no_signal_fraction==1
    assert summary.iloc[-1].fraction_precision_ge_60==0
    assert summary.iloc[0].signals_sum_overlapping==4


def test_validation_predictions_must_match_exact_sequence_times(tmp_path):
    cfg=study.configuration(tmp_path,'B25');d=frame();d['label']=1;d['hit_type']='tp';d['fwd_return_10h']=.01
    fold=study.cohort(d,cfg)[0];part=d.iloc[fold.val[63:]]
    p=pd.DataFrame({'source_row_position':np.arange(63,1080),'timestamp':part.timestamp.to_numpy(),
                    'label':1,'forward_return':.01})
    assert len(study.validate_predictions(p,d,fold))==1017
    p.loc[0,'timestamp']=p.loc[1,'timestamp']
    with pytest.raises(ValueError,match='timestamps'):study.validate_predictions(p,d,fold)


def test_input_signature_detects_feature_change():
    d=pd.DataFrame({'timestamp':pd.date_range('2022-01-01',periods=3,tz='UTC'),'x':[1.,2.,3.]})
    other=d.copy();other.loc[1,'x']=9
    assert study.input_signature(d,['x'])!=study.input_signature(other,['x'])


def test_test_action_is_not_exposed(tmp_path):
    with patch('sys.argv',['cmd','test','--root',str(tmp_path),'--legacy',str(tmp_path/'old'),'--session','session']):
        with pytest.raises(SystemExit):study.main()


def test_current_notebook_cannot_freeze_or_test():
    path=Path(__file__).resolve().parents[1]/'notebooks/workflows/04_barrier_study.ipynb'
    nb=json.loads(path.read_text(encoding='utf-8'))
    source='\n'.join(c['source'] for c in nb['cells'] if c['cell_type']=='code')
    assert 'scripts/advisor_selective.py' in source
    assert 'ALLOW_TEST' not in source and "execute_step('freeze')" not in source
    assert "execute_step('test')" not in source
    assert "execute_step('report')" in source
    assert 'selective_walkforward_v1_001' in source

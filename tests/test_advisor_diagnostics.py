"""Synthetic diagnostic semantics; no real training or external artifacts."""
import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

spec=importlib.util.spec_from_file_location('diagnostics',Path(__file__).resolve().parents[1]/'scripts/analyze_advisor_diagnostics.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


def test_threshold_inclusive_and_no_positive_predictions():
    result=module.scores([1,0,1,0],[.5,.5,.2,.1],[0,.5,1])
    middle=result.iloc[1]
    assert (middle.tp,middle.fp,middle.fn,middle.tn)==(1,1,1,1)
    assert middle.precision==middle.recall==middle.f1==.5
    assert result.iloc[-1].precision==result.iloc[-1].f1==0
    assert result.iloc[0].recall==1


@pytest.mark.parametrize('probabilities',[[float('nan'),.5],[1.1,.5],[-.1,.5]])
def test_invalid_probabilities_fail_closed(probabilities):
    with pytest.raises(ValueError):module.scores([0,1],probabilities,[.5])


def test_first_touch_and_simultaneous_touch_preserve_frozen_convention():
    loop=module.label_loop()
    close=np.array([100.,100.,100.]); atr=np.ones(3)
    for high,low,expected in [(103,99,1),(101,94,2),(103,94,3),(101,99,0)]:
        labels,returns,codes,exits=loop(close,np.array([100.,high,100.]),np.array([100.,low,100.]),atr,2,5,2)
        assert codes[0]==expected
        assert labels[0]==int(expected==1)
        assert exits[0]==(2 if expected==0 else 1)
        assert np.isclose(returns[0],{0:0.,1:.02,2:-.05,3:-.05}[expected])
        assert labels[1]==-1  # Incomplete horizon is excluded.


def test_positive_timeout_is_still_negative_label():
    labels,returns,codes,_=module.label_loop()(np.array([100.,101.,101.]),
        np.array([101.,101.,101.]),np.array([99.,100.,100.]),np.ones(3),2,5,2)
    assert labels[0]==0 and codes[0]==0 and np.isclose(returns[0],.01)


def test_atr_uses_only_current_and_past_candles():
    raw=pd.DataFrame({'close':np.ones(20)*100,'high':np.ones(20)*101,'low':np.ones(20)*99})
    original=module.atr14(raw)
    raw.loc[15:,'high']=500
    changed=module.atr14(raw)
    assert np.isnan(original.iloc[12]) and original.iloc[13]==2
    np.testing.assert_array_equal(original.iloc[:15],changed.iloc[:15])

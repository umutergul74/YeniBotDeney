import importlib.util
from pathlib import Path
import numpy as np

spec=importlib.util.spec_from_file_location('barriers',Path(__file__).resolve().parents[1]/'scripts/analyze_advisor_barriers.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def test_pareto_retains_ties_and_tradeoffs_but_removes_dominated():
    np.testing.assert_array_equal(module.pareto_mask([[1,2,0],[2,1,0],[2,2,0],[1,2,0]]),[True,True,False,True])


def test_summary_counts_double_hit_as_stop_and_positive_timeout_as_zero():
    result=module.summarize(np.array([0,1,2,3]),np.array([.01,.03,-.02,-.01]))
    assert result['profit_first']==1 and result['stop_first']==2 and result['timeout']==1
    assert result['both_same_bar_pct']==25 and result['timeout_positive_return_pct']==100
    assert result['positive_mean_fwd_pct']==3


def test_expanding_barriers_cannot_reduce_timeout_on_identical_prices():
    rng=np.random.default_rng(42)
    close=100+np.cumsum(rng.normal(0,.3,100))
    high=close+.5;low=close-.5;atr=np.ones(100)
    loop=module.prior.label_loop()
    narrow=loop(close,high,low,atr,1,1,10)[2][:90]
    wide=loop(close,high,low,atr,2,2,10)[2][:90]
    assert np.all(wide[narrow==0]==0)


def test_higher_target_cannot_increase_positive_labels_with_fixed_stop():
    rng=np.random.default_rng(43);close=100+np.cumsum(rng.normal(0,.5,100))
    loop=module.prior.label_loop();args=(close,close+.5,close-.5,np.ones(100))
    lower=loop(*args,1,2,10)[0][:90];higher=loop(*args,3,2,10)[0][:90]
    assert np.all(lower[higher==1]==1)

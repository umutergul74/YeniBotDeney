import copy
import json
from pathlib import Path
import pytest
from yenibot.experiment.advisor_learning_rate import candidate_config, one_run, report
from scripts.build_advisor_learning_rate_notebook import build, build_capacity


def test_only_learning_rate_and_output_change(tmp_path):
    cfg={'training':{'learning_rate':.001,'patience':15,'seeds':[42,43,44]},'output':'old','model':{'seq_len':64},'data':{'frame':'same'}}
    before=copy.deepcopy(cfg)
    result=candidate_config(cfg,tmp_path)
    assert cfg==before
    result['training']['learning_rate']=.001
    result['output']='old'
    assert result==before
    cfg['training']['learning_rate']=.01
    with pytest.raises(ValueError): candidate_config(cfg,tmp_path)


def test_notebook_syntax_and_scope():
    nb=build()
    text='\n'.join(c['source'] for c in nb['cells'])
    for c in nb['cells']:
        if c['cell_type']=='code':compile(c['source'],'notebook','exec')
    assert 'advisor_learning_rate.py' in text and "step('train')" in text
    assert "'--experiment','A'" in text and 'a6_lr0001_a100_001' in text
    assert 'b37_lr0001_a100_001' not in text
    assert 'ALLOW_TRAINING' not in text and "step('bundle')" not in text
    assert "RELEASE='advisor-learning-rate-v1.1.0'" in text
    assert text.index('drive.flush_and_unmount()')<text.index('runtime.unassign()')
    assert json.loads(Path('notebooks/workflows/06_learning_rate.ipynb').read_text(encoding='utf-8'))==build_capacity()


@pytest.mark.parametrize('experiment', ['A','B'])
def test_missing_or_ambiguous_control_rejected(tmp_path, experiment):
    with pytest.raises(ValueError):one_run(tmp_path,experiment)
    for n in (experiment+'_one',experiment+'_two'):(tmp_path/'runs'/n).mkdir(parents=True)
    with pytest.raises(ValueError):one_run(tmp_path,experiment)


@pytest.mark.parametrize('experiment', ['A','B'])
def test_report_paired_direction_and_single_graph(tmp_path,monkeypatch,experiment):
    import numpy as np
    import pandas as pd
    import yenibot.experiment.advisor_learning_rate as mod
    def fake(run):
        delta=0 if run.name=='control' else -.02
        rows=pd.DataFrame([dict(seed=s,fold=f,bce=.6+delta,average_precision=.4-delta,best_epoch=1,precision=.5,recall=.1,f1=.16,signals=20) for s in (42,43,44) for f in range(38)])
        h=pd.DataFrame([dict(seed=s,fold=f,epoch=e,train_bce=.6-.01*e,bce=.6+delta,average_precision=.4-delta) for s in (42,43,44) for f in range(38) for e in range(1,17)])
        ids={(s,f):pd.DataFrame({'label':[0,1]}) for s in (42,43,44) for f in range(38)}
        return rows,h,ids
    monkeypatch.setattr(mod,'load_runs',fake)
    report(Path('control'),Path('candidate'),tmp_path,experiment)
    assert ('A6' if experiment=='A' else 'B37') in (tmp_path/'reports/README.md').read_text(encoding='utf-8')
    paired=pd.read_csv(tmp_path/'reports/paired.csv')
    assert len(paired)==114 and np.allclose(paired.delta_bce,-.02)
    summary=pd.read_csv(tmp_path/'reports/summary.csv').set_index('learning_rate')
    assert summary.loc[.0001,'bce_better_pairs']==114
    assert summary.loc[.001,'bce_better_pairs']==0
    assert len(list((tmp_path/'reports').glob('*.png')))==1


def test_run_selection_does_not_mix_models(tmp_path):
    for name in ("A_one", "B_one"):(tmp_path/"runs"/name).mkdir(parents=True)
    assert one_run(tmp_path,"A").name=="A_one"
    assert one_run(tmp_path,"B").name=="B_one"

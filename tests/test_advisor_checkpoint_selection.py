import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
import pytest
from yenibot.experiment import advisor_checkpoint_selection as mod


def test_split_has_disjoint_context_and_protected_horizon():
    assert len({mod.run_signature('study',seed,fold) for seed in [42,43] for fold in [0,1]})==4
    selection, assessment=mod.split_validation(np.arange(5064,6144))
    assert len(selection)==len(assessment)==528
    assert assessment[0]-selection[-1]==25
    assert selection[-1]+10<assessment[0]
    assert len(selection[63:])==len(assessment[63:])==465
    with pytest.raises(ValueError):mod.split_validation(np.arange(1079))
    with pytest.raises(ValueError):mod.split_validation(np.arange(1080)*2)


def test_coverage_is_score_only_and_no_signal_is_undefined():
    assert mod.coverage_threshold(np.arange(100)/100,.05)==.95
    result=mod.decision_counts([0,1],[.1,.2],.5)
    assert result['precision'] is None and result['signals']==0 and result['recall']==0
    with pytest.raises(ValueError):mod.coverage_threshold([np.nan],.05)


def test_reference_runtime_must_match_cuda_build_and_cudnn():
    original={'torch':'2.11.0+cu130','cudnn':91900}
    mod.verify_reference_runtime(original,dict(original))
    for changed in [{'torch':'2.11.0+cu128','cudnn':91900},{'torch':'2.11.0+cu130','cudnn':91800}]:
        with pytest.raises(ValueError):mod.verify_reference_runtime(original,changed)


def test_notebook_reuses_setup_and_never_exposes_test():
    from scripts.build_advisor_learning_rate_notebook import build_checkpoint
    nb=build_checkpoint()
    assert nb==json.loads(Path('notebooks/workflows/06_learning_rate.ipynb').read_text(encoding='utf-8'))
    for c in nb['cells']:
        if c['cell_type']=='code':compile(c['source'],'notebook','exec')
    text='\n'.join(c['source'] for c in nb['cells'])
    assert 'advisor_checkpoint_selection.py' in text and "'--experiment'" not in text
    assert 'checkpoint_selection_v1/a6_bce_ap_a100_001' in text
    assert "RELEASE='advisor-checkpoint-selection-v1.0.0'" in text
    assert text.index('drive.flush_and_unmount()')<text.index('runtime.unassign()')
    assert "step('test')" not in text


@pytest.fixture
def toy(monkeypatch,tmp_path):
    """Synthetic scalar model, not GRU training; deterministic epoch/eval fixtures."""
    import torch
    from yenibot.training import advisor as engine
    class Scalar(torch.nn.Module):
        def __init__(self):super().__init__();self.weight=torch.nn.Parameter(torch.zeros(()))
        def forward(self,x,return_logits=False):return self.weight.expand(len(x))
    monkeypatch.setattr(engine,'build_advisor_model',lambda *args:Scalar())
    ts=pd.date_range('2022-01-01',periods=6144,freq='h',tz='UTC')
    frame=pd.DataFrame({'timestamp':ts,'label_end_timestamp':ts+pd.Timedelta(hours=10),
                        'label':np.arange(6144)%2,'fwd_return_10h':0.,'feature':np.arange(6144)})
    fold=SimpleNamespace(train=np.arange(5040),val=np.arange(5064,6144),fold=0)
    cfg={'model':{'seq_len':64},'labeling':{'max_holding_bars':10},
         'training':{'epochs':3,'patience':15,'learning_rate':.001,'weight_decay':.0001,
                     'batch_size':10000,'grad_clip':1.,'deterministic':True}}
    calls=[]
    def evaluate(model,loader,device,threshold):
        n=len(calls);calls.append(loader.dataset)
        # First three calls must be selection only; final four follow frozen choice.
        if n<3:
            assert not (tmp_path/'selection.json').exists()
            assert loader.dataset.features[-1,0] < 1.3  # selection ends before assessment
        else:assert (tmp_path/'selection.json').exists()
        bce=[.6,.5,.55][n] if n<3 else .5
        ap=[.4,.6,.7][n] if n<3 else .6
        positions=loader.dataset.end_positions
        pred=pd.DataFrame({'source_row_position':positions,'label':loader.dataset.labels[positions],
                           'probability':np.linspace(.1,.8,len(positions)),'forward_return':0.})
        return {'bce':bce,'average_precision':ap},pred
    monkeypatch.setattr(engine,'evaluate',evaluate)
    return frame,fold,cfg,calls,torch.device('cpu')


def test_both_choices_frozen_before_assessment_and_completed_integrity(tmp_path,toy):
    frame,fold,cfg,calls,device=toy
    mod.train_fold(frame,fold,cfg,['feature'],42,tmp_path,'identity',device)
    assert len(calls)==7
    assert json.loads((tmp_path/'selection.json').read_text())['epochs']=={'bce':2,'ap':3}
    for rule in ['bce','ap']:
        pred=pd.read_parquet(tmp_path/f'{rule}_assessment.parquet')
        assert len(pred)==465 and pred.frame_row_position.min()==5679
    assert mod.validate_completed(tmp_path,'identity')
    mod.train_fold(frame,fold,cfg,['feature'],42,tmp_path,'identity',device)
    assert len(calls)==7  # no re-training/evaluation
    with pytest.raises(ValueError):mod.validate_completed(tmp_path,'other')
    (tmp_path/'ap_assessment.parquet').write_bytes(b'corrupt')
    with pytest.raises(ValueError):mod.validate_completed(tmp_path,'identity')


def test_resume_from_last_saved_epoch(tmp_path,toy,monkeypatch):
    frame,fold,cfg,calls,device=toy
    from yenibot.training import advisor as engine
    original=engine.atomic_checkpoint
    def interrupt(path,value):
        original(path,value)
        if path.name=='last.pt':raise RuntimeError('simulated disconnect after durable save')
    monkeypatch.setattr(engine,'atomic_checkpoint',interrupt)
    with pytest.raises(RuntimeError,match='simulated disconnect'):
        mod.train_fold(frame,fold,cfg,['feature'],42,tmp_path,'identity',device)
    monkeypatch.setattr(engine,'atomic_checkpoint',original)
    mod.train_fold(frame,fold,cfg,['feature'],42,tmp_path,'identity',device)
    assert len(calls)==7
    assert pd.read_csv(tmp_path/'history.csv').epoch.tolist()==[1,2,3]
    assert json.loads((tmp_path/'selection.json').read_text())['epochs']=={'bce':2,'ap':3}


def test_report_uses_selection_thresholds_and_rejects_incomplete(tmp_path,monkeypatch):
    with pytest.raises(ValueError,match='Incomplete'):mod.report(tmp_path,'sig')
    for seed in [42,43,44]:
        for fold in range(38):
            folder=tmp_path/'runs'/f'seed_{seed}'/f'fold_{fold:03d}'
            folder.mkdir(parents=True)
            (folder/'metrics.json').write_text(json.dumps({'results':{
                rule:{'epoch':1,'assessment':{'bce':.6,'average_precision':.5}} for rule in ['bce','ap']}}))
    monkeypatch.setattr(mod,'validate_completed',lambda *args:True)
    def fake_read(path):
        selection='selection' in path.name
        return pd.DataFrame({'label':np.arange(465)%2,
                             'probability':np.linspace(.1,.9,465) if selection else np.full(465,.6)})
    monkeypatch.setattr(pd,'read_parquet',fake_read)
    mod.report(tmp_path,'sig')
    table=pd.read_csv(tmp_path/'reports/by_run.csv')
    assert len(table)==114*2*3
    assert (table[table.policy=='selection_top5'].signals==0).all()
    assert (table[table.policy=='fixed_050'].signals==465).all()
    assert (tmp_path/'reports/checkpoint_selection_review.zip').is_file()

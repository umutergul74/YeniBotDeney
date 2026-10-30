import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
import torch
from yenibot.experiment import advisor_cnn_gru as mod
from test_advisor_checkpoint_selection import toy


def test_cnn_is_causal_and_control_is_original():
    settings=dict(gru_hidden=8,gru_layers=2,dropout=.2,fusion_hidden=8)
    cnn=mod.CnnGru(6,settings).eval()
    x=torch.randn(2,64,6);changed=x.clone();changed[:,32:]+=10
    with torch.no_grad():
        a=cnn.encode_local(x);b=cnn.encode_local(changed)
        torch.testing.assert_close(a[:,:32],b[:,:32],rtol=0,atol=0)
        assert a.shape==(2,64,32) and cnn(x,return_logits=True).shape==(2,)
        torch.testing.assert_close(cnn(x),torch.sigmoid(cnn(x,return_logits=True)))
    from yenibot.training.advisor_models import build_advisor_model
    torch.manual_seed(42);control=mod.model_factory('gru')(6,settings)
    torch.manual_seed(42);original=build_advisor_model(6,'gru',settings)
    for k,v in original.state_dict().items():torch.testing.assert_close(control.state_dict()[k],v,rtol=0,atol=0)
    assert mod.architecture_signature('s','gru')!=mod.architecture_signature('s','cnn_gru')


def test_bce_only_factory_and_resume(tmp_path,toy,monkeypatch):
    frame,fold,cfg,calls,device=toy
    from yenibot.training import advisor as engine
    factory=engine.build_advisor_model
    used=[]
    def build(n,s):used.append(n);return factory(n,'gru',s)
    args=(frame,fold,cfg,['feature'],42,tmp_path,'cnn-signature',device)
    original=engine.atomic_checkpoint
    def interrupt(path,value):
        original(path,value)
        if path.name=='last.pt':raise RuntimeError('disconnect')
    monkeypatch.setattr(engine,'atomic_checkpoint',interrupt)
    with pytest.raises(RuntimeError,match='disconnect'):mod.train_fold(*args,model_factory=build,selectors=('bce',))
    monkeypatch.setattr(engine,'atomic_checkpoint',original)
    mod.train_fold(*args,model_factory=build,selectors=('bce',))
    assert used==[1,1] and len(calls)==5
    assert json.loads((tmp_path/'selection.json').read_text())['epochs']=={'bce':2}
    assert not (tmp_path/'ap.pt').exists() and mod.validate_completed(tmp_path,'cnn-signature')
    mod.train_fold(*args,model_factory=build,selectors=('bce',))
    assert len(calls)==5


def test_report_pairs_architectures_and_uses_selection_only(tmp_path,monkeypatch):
    with pytest.raises(ValueError):mod.report(tmp_path,'sig')
    for arch in mod.DESIGN['architectures']:
        for seed in [42,43,44]:
            for fold in range(38):
                folder=tmp_path/'runs'/arch/f'seed_{seed}'/f'fold_{fold:03d}'
                folder.mkdir(parents=True)
                (folder/'metrics.json').write_text(json.dumps({'results':{'bce':{
                    'epoch':2,'assessment':{'bce':.6,'average_precision':.5}}}}))
    monkeypatch.setattr(mod,'validate_completed',lambda *a:True)
    def read(path):
        return pd.DataFrame({'timestamp':pd.date_range('2022-01-01',periods=465,freq='h'),
            'label':np.arange(465)%2,'probability':np.linspace(.1,.9,465) if 'selection' in path.name else np.full(465,.6)})
    monkeypatch.setattr(pd,'read_parquet',read)
    mod.report(tmp_path,'sig')
    t=pd.read_csv(tmp_path/'reports/by_run.csv');s=pd.read_csv(tmp_path/'reports/summary.csv')
    assert len(t)==684 and len(pd.read_csv(tmp_path/'reports/paired.csv'))==342
    assert (t[t.policy=='selection_top5'].signals==0).all()
    assert np.allclose(s.bce_mean,.6) and np.allclose(s.ap_mean,.5)
    assert (tmp_path/'reports/cnn_gru_review.zip').exists()


def test_notebook_pins_new_workspace_and_has_no_test():
    from scripts.build_advisor_learning_rate_notebook import build_cnn_gru
    nb=build_cnn_gru()
    assert nb==json.loads(Path('notebooks/workflows/06_learning_rate.ipynb').read_text(encoding='utf-8'))
    for cell in nb['cells']:
        if cell['cell_type']=='code':compile(cell['source'],'nb','exec')
    text='\n'.join(c['source'] for c in nb['cells'])
    assert "RELEASE='advisor-cnn-gru-v1.0.0'" in text
    assert 'cnn_gru_v1/a6_a100_001' in text and 'scripts/advisor_cnn_gru.py' in text
    assert "step('test')" not in text and 'MPLBACKEND' in text
    assert text.index('drive.flush_and_unmount()')<text.index('runtime.unassign()')

import copy
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from yenibot.experiment import advisor_capacity as mod


def test_candidate_changes_only_hidden_and_does_not_mutate():
    cfg={'model':{'gru_hidden':128,'gru_layers':2,'fusion_hidden':128,'dropout':.2},'training':{'learning_rate':.001}}
    original=copy.deepcopy(cfg);candidate=mod.candidate_config(cfg)
    assert cfg==original and candidate['model']['gru_hidden']==64
    candidate['model']['gru_hidden']=128;assert candidate==original
    cfg['model']['gru_hidden']=64
    with pytest.raises(ValueError):mod.candidate_config(cfg)


def control_fixture(root):
    from yenibot.experiment.advisor_storage import immutable_json,sha256
    protocol={'features':['x'],'config':{'model':{'gru_hidden':128}}};runtime={'gpu':'A100'}
    immutable_json(root/'artifacts/control.json',protocol)
    immutable_json(root/'artifacts/design.json',mod.previous.DESIGN)
    immutable_json(root/'reproducibility/workspace_identity.json',dict(commit=mod.CONTROL_COMMIT,runtime=runtime))
    sig=mod.previous.architecture_signature(mod.study_signature(root),'gru')
    for seed in [42,43,44]:
        for fold in range(38):
            folder=root/'runs/gru'/f'seed_{seed}'/f'fold_{fold:03d}';folder.mkdir(parents=True)
            (folder/'bce.pt').write_bytes(b'fake-weight-for-integrity-test')
            immutable_json(folder/'complete.json',dict(signature=mod.run_signature(sig,seed,fold),files={'bce.pt':sha256(folder/'bce.pt')}))
    return protocol,runtime,sig


def test_old_control_identity_integrity_and_runtime(tmp_path):
    protocol,runtime,sig=control_fixture(tmp_path)
    actual,evidence=mod.verify_control(tmp_path,protocol,runtime)
    assert actual==sig and len(evidence)==228
    with pytest.raises(ValueError):mod.verify_control(tmp_path,protocol,{'gpu':'T4'})
    with pytest.raises(ValueError):mod.verify_control(tmp_path,{},runtime)
    (tmp_path/'runs/gru/seed_44/fold_037/bce.pt').write_bytes(b'corrupt')
    with pytest.raises(ValueError):mod.verify_control(tmp_path,protocol,runtime)


def test_report_reuses_external_control_and_bundles_evidence(tmp_path,monkeypatch):
    root=tmp_path/'new';old=tmp_path/'old/gru'
    for directory in [old,root/'runs/gru64']:
        for seed in [42,43,44]:
            for fold in range(38):
                f=directory/f'seed_{seed}'/f'fold_{fold:03d}';f.mkdir(parents=True)
                (f/'metrics.json').write_text(json.dumps({'results':{'bce':{'epoch':1,'assessment':{'bce':.6,'average_precision':.5}}}}))
                (f/'bce.pt').write_bytes(b'weight')
    seen=[]
    monkeypatch.setattr(mod.previous,'validate_completed',lambda folder,sig:seen.append((folder,sig)) or True)
    def read(path):
        return pd.DataFrame({'timestamp':pd.date_range('2022',periods=465,freq='h'),'label':np.arange(465)%2,
            'probability':np.linspace(.1,.9,465) if 'selection' in path.name else np.full(465,.6)})
    monkeypatch.setattr(pd,'read_parquet',read)
    mod.previous.report(root,'new',comparisons={'gru128':(old,'old-sig'),'gru64':(root/'runs/gru64','new-sig')},archive_name='capacity_review.zip')
    table=pd.read_csv(root/'reports/by_run.csv');assert len(table)==684
    assert set(table.architecture)=={'gru128','gru64'}
    assert (table[table.policy=='selection_top5'].signals==0).all()
    assert seen[0][1]==mod.run_signature('old-sig',42,0)
    import zipfile
    with zipfile.ZipFile(root/'reports/capacity_review.zip') as z:
        assert 'control_runs/gru128/seed_42/fold_000/metrics.json' in z.namelist()
        assert not any(n.endswith('.pt') for n in z.namelist())


def test_notebook_current_pin_and_control_read_only():
    from scripts.build_advisor_learning_rate_notebook import build_capacity
    nb=build_capacity();assert nb==json.loads(Path('notebooks/workflows/06_learning_rate.ipynb').read_text(encoding='utf-8'))
    for c in nb['cells']:
        if c['cell_type']=='code':compile(c['source'],'nb','exec')
    text='\n'.join(c['source'] for c in nb['cells'])
    assert "'--control',str(CONTROL)" in text and 'advisor-gru-capacity-v1.0.0' in text
    assert 'gru_capacity_v1/hidden64_a100_001' in text and 'capacity_review.zip' in text
    assert "step('test')" not in text
    assert text.index('drive.flush_and_unmount()')<text.index('runtime.unassign()')

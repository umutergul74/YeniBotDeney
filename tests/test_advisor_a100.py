"""A100 profile and safe notebook shutdown, no GPU or Colab connection."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace, ModuleType

import pytest

from yenibot.experiment import advisor_runtime as runtime


@pytest.mark.parametrize('hardware,gpu,allowed',[
    ('default','Tesla T4',True),('default','NVIDIA A100-SXM4-40GB',False),
    ('selective-a100','NVIDIA A100-SXM4-40GB',True),('selective-a100','Tesla T4',False),
    ('selective-a100',None,False),('selective-a100','NVIDIA A100 80GB PCIe',False),
])
def test_runtime_accepts_only_declared_hardware(tmp_path,monkeypatch,hardware,gpu,allowed):
    import torch
    folder=tmp_path/'requirements';folder.mkdir()
    lock=folder/'test.lock';lock.write_text('')
    profile={'python':'3.13.15','lock':'requirements/test.lock',
             'lock_sha256':runtime.sha256(lock),'training_gpu':'Tesla T4'}
    (folder/'advisor-environment.json').write_text(json.dumps(profile))
    monkeypatch.setattr(runtime.platform,'system',lambda:'Linux')
    monkeypatch.setattr(runtime.platform,'machine',lambda:'x86_64')
    monkeypatch.setattr(runtime.platform,'python_version',lambda:'3.13.15')
    monkeypatch.setattr(runtime.sys,'prefix',str(tmp_path/'venv'))
    monkeypatch.setattr(runtime.importlib.metadata,'distributions',lambda:[])
    monkeypatch.setattr(torch.cuda,'is_available',lambda:gpu is not None)
    monkeypatch.setattr(torch.cuda,'get_device_name',lambda _:gpu)
    monkeypatch.setattr(torch.backends.cudnn,'version',lambda:91002)
    monkeypatch.setattr(runtime.subprocess,'check_output',lambda *a,**k:'test-driver')
    monkeypatch.setattr(runtime.subprocess,'run',lambda *a,**k:None)
    if not allowed:
        with pytest.raises(ValueError,match='Expected'):runtime.runtime_identity(tmp_path,require_gpu=True,hardware=hardware)
    else:
        result=runtime.runtime_identity(tmp_path,require_gpu=True,hardware=hardware)
        assert result['gpu']==gpu
        if hardware=='selective-a100':assert result['hardware_profile']==hardware
        else:assert 'hardware_profile' not in result


def notebook():
    p=Path(__file__).resolve().parents[1]/'notebooks/workflows/04_barrier_study.ipynb'
    return json.loads(p.read_text(encoding='utf-8'))['cells']


@pytest.mark.parametrize('case',['success','failed_report','failed_bundle','changed_candidates','training_disabled'])
def test_unassign_only_after_successful_matching_work(case,monkeypatch,tmp_path):
    cells=notebook();ctx={};exec(cells[2]['source'],ctx)
    assert ctx['os'].environ['MPLBACKEND']=='Agg'
    setup=next(c['source'] for c in cells if c['cell_type']=='code' and 'def step_identity' in c['source'])
    exec(setup[setup.index('def step_identity'):],ctx)
    ctx.update(ROOT=tmp_path,RESEARCH_PYTHON='python',LEGACY_ROOT=tmp_path/'old',ALLOW_TRAINING=True)
    def logged(command,name):
        if case=='failed_bundle' and name=='bundle.log':raise RuntimeError('failed ZIP')
    ctx['logged']=logged
    for step in ('prepare','train','report'):ctx['execute_step'](step)
    if case=='failed_report':ctx['SUCCESSFUL_STEPS'].pop('report')
    if case=='changed_candidates':ctx['EXPERIMENTS']=['B25']
    if case=='training_disabled':ctx['ALLOW_TRAINING']=False
    calls=[];colab=ModuleType('google.colab');colab.runtime=SimpleNamespace(unassign=lambda:calls.append('closed'))
    monkeypatch.setitem(sys.modules,'google.colab',colab)
    code=cells[-1]['source']
    assert 'runtime.unassign()' in code
    if case=='failed_bundle':
        with pytest.raises(RuntimeError):exec(code,ctx)
    else:exec(code,ctx)
    assert calls==(['closed'] if case=='success' else [])


def test_prepare_explicitly_sets_agg_and_runtime_has_no_training_changes():
    cells=notebook()
    assert not any('Tesla T4' in c['source'] for c in cells)
    code=next(c['source'] for c in cells if c['cell_type']=='code' and "execute_step('prepare')" in c['source'])
    assert code.index("os.environ['MPLBACKEND'] = 'Agg'")<code.index("execute_step('prepare')")
    original={'training_gpu':'Tesla T4','lock':'unchanged'}
    selected=runtime.hardware_profile(original,'selective-a100')
    assert original['training_gpu']=='Tesla T4' and selected['lock']=='unchanged'
    with pytest.raises(ValueError):runtime.hardware_profile(original,'anything')

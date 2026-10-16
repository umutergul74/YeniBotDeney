import ast
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace, ModuleType
import sys

import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('recovery',ROOT/'scripts/advisor_recover_selective.py')
recovery=importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


def test_existing_even_empty_artifact_is_never_replaced(tmp_path):
    source=tmp_path/'source';source.write_bytes(b'new')
    target=tmp_path/'target';target.write_bytes(b'')
    with pytest.raises(ValueError,match='replace'):recovery.publish_missing(source,target)
    assert target.read_bytes()==b''
    recovery.publish_missing(source,tmp_path/'new')
    assert (tmp_path/'new').read_bytes()==b'new'


@pytest.mark.parametrize('kind',['weights_only_missing','history','checkpoint','empty','partial','mismatched'])
def test_incident_recovery_preserves_originals_and_limits_training(tmp_path,kind):
    run=tmp_path/'runs';folder=run/'seed_44/fold_000';folder.mkdir(parents=True)
    all_files=(*recovery.REQUIRED,'last.pt')
    missing={'weights_only_missing':['last.pt'],'history':['history.csv'],
             'checkpoint':list(recovery.REQUIRED),'empty':list(all_files),
             'partial':['validation_predictions.parquet'],'mismatched':['history.csv']}[kind]
    for name in all_files:
        if name not in missing:(folder/name).write_text('original')
    if kind in {'history','mismatched'}:
        (folder/'validation_metrics.json').write_text(json.dumps({'epochs_trained':1,'best_epoch':1}))
    before={p.name:p.read_bytes() for p in folder.iterdir()}
    checkpoint={'signature':'wrong' if kind=='mismatched' else 'sig','device':'cuda','best_epoch':1,
                'history':[{'epoch':1,'train_bce':.5,'validation':{'bce':.4}}]}
    calls=[]
    def run_fold(*args):
        calls.append('train');scratch=args[6]
        for name in all_files:(scratch/name).write_bytes(b'recovered')
    advisor=SimpleNamespace(run_fold=run_fold)
    torch=SimpleNamespace(load=lambda *a,**k:checkpoint,set_num_threads=lambda _:None,device=lambda d:d)
    cfg={'training':{'torch_threads':1},'experiments':{'B32':{}}}
    context=(cfg,None,[None],run,{'device':'cuda','features':[]},'sig')
    row={'candidate':'B32','seed':44,'fold':0,'path':'B32/seed_44/fold_000','missing':missing}
    if kind in {'partial','mismatched'}:
        with pytest.raises(ValueError):recovery.repair_one(row,context,tmp_path/'recovery',advisor,pd,torch)
    else:recovery.repair_one(row,context,tmp_path/'recovery',advisor,pd,torch)
    assert calls==(['train'] if kind in {'checkpoint','empty'} else [])
    assert all((folder/name).read_bytes()==value for name,value in before.items())
    if kind=='history':assert pd.read_csv(folder/'history.csv').epoch.tolist()==[1]


@pytest.mark.parametrize('failure',[None,'flush','missing','changed'])
def test_drive_readback_blocks_shutdown_on_upload_or_integrity_failure(tmp_path,monkeypatch,failure):
    cells=json.loads((ROOT/'notebooks/workflows/04_barrier_study.ipynb').read_text(encoding='utf-8'))['cells']
    source=next(c['source'] for c in cells if 'def sync_verified' in c['source'])
    tree=ast.parse(source)
    ctx={'ROOT':tmp_path}
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='sync_verified'],type_ignores=[]),'cell','exec'),ctx)
    item=tmp_path/'result.csv';item.write_bytes(b'evidence')
    calls=[]
    def flush():
        calls.append('flush')
        if failure=='flush':raise RuntimeError('upload failure')
    def mount(path):
        calls.append('mount')
        if failure=='missing':item.unlink()
        if failure=='changed':item.write_bytes(b'bad')
    colab=ModuleType('google.colab');colab.drive=SimpleNamespace(flush_and_unmount=flush,mount=mount)
    monkeypatch.setitem(sys.modules,'google.colab',colab)
    if failure:
        with pytest.raises(RuntimeError):ctx['sync_verified']()
    else:ctx['sync_verified']()
    assert calls==(['flush'] if failure=='flush' else ['flush','mount'])


def test_recovery_launcher_does_not_call_regular_prepare_or_train(tmp_path):
    cells=json.loads((ROOT/'notebooks/workflows/04_barrier_study.ipynb').read_text(encoding='utf-8'))['cells']
    ctx={};exec(cells[2]['source'],ctx)
    source=next(c['source'] for c in cells if 'def step_identity' in c['source'])
    tree=ast.parse(source)
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'step_identity','execute_step'}],type_ignores=[]),'cell','exec'),ctx)
    calls=[];ctx.update(ROOT=tmp_path,RECOVERY_HELPER=tmp_path/'helper',RESEARCH_PYTHON='python',logged=lambda command,name:calls.append(command))
    ctx['execute_step']('prepare')
    assert calls[-1][3]=='audit'
    with pytest.raises(RuntimeError):ctx['execute_step']('train')
    ctx['ALLOW_REPAIR']=True
    ctx['execute_step']('train')
    assert calls[-1][3]=='repair'

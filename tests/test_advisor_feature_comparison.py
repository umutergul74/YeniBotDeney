"""Protocol regression tests; never train research models."""
import copy
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from yenibot.experiment import advisor_feature_comparison as study
from scripts.build_advisor_feature_notebook import build


@pytest.fixture
def prepared(tmp_path,monkeypatch):
    root=tmp_path/'new'
    source=root/'recovered/data/development_full_wavelet_off.parquet'
    source.parent.mkdir(parents=True)
    cfg=study.read_config('configs/advisor_ablation.yaml')
    cfg['data']['frame']=str(source)
    frame=pd.DataFrame({'timestamp':pd.date_range('2022-03-01T04:00:00Z',periods=33551,freq='h')})
    frame['label_end_timestamp']=frame.timestamp+pd.Timedelta(hours=10)
    for f in study.features()[1]:frame[f]=.1
    frame['label']=0;frame['fwd_return_10h']=0.
    frame.to_parquet(source,index=False)
    checksum=study.sha256(source)
    source.with_suffix('.manifest.json').write_text(json.dumps({'protocol':cfg,'frame_sha256':checksum}))
    monkeypatch.setattr(study,'FULL_SHA',checksum)
    monkeypatch.setattr(study,'recover',lambda *a,**k:None)
    return root,source,frame


def test_nested_features_and_unchanged_training_protocol():
    basic,full=study.features()
    assert len(basic)==6 and len(full)==37 and set(basic)<=set(full)
    assert set(full)-set((study.REPO/'configs/advisor_full_features.txt').read_text().splitlines())==set(study.ADDED)


def test_prepare_preserves_bytes_and_rejects_modified_data(prepared):
    root,source,_=prepared
    before=source.read_bytes()
    study.prepare(root,root.parent/'legacy')
    cfg=study.verified(root)
    assert source.read_bytes()==before==Path(cfg['data']['frame']).read_bytes()
    assert cfg['experiments']==study.read_config('configs/advisor_ablation.yaml')['experiments']
    Path(cfg['data']['frame']).write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='changed'):study.verified(root)


@pytest.mark.parametrize('change',['rows','nan','label','training','model'])
def test_rejects_scientific_drift(prepared,change):
    root,_,frame=prepared
    cfg=study.configuration(root)
    if change=='rows':frame=frame.iloc[:-1]
    if change=='nan':frame.loc[0,'atr_14_pct']=np.nan
    if change=='label':cfg['labeling']['sl_multiplier']=2
    if change=='training':cfg['training']['selection_metric']='f1'
    if change=='model':cfg['model']['gru_hidden']=32
    with pytest.raises(ValueError):study.verify_frame(frame,cfg)


def test_partial_run_cannot_report(tmp_path):
    with pytest.raises(ValueError,match='exactly one'):study.completed_runs(tmp_path)


def test_notebook_is_generated_and_code_compiles():
    notebook=build()
    actual=json.loads((study.REPO/'notebooks/workflows/05_feature_comparison.ipynb').read_text(encoding='utf-8'))
    assert actual==notebook
    for i,cell in enumerate(notebook['cells']):
        if cell['cell_type']=='code':compile(cell['source'],f'cell{i}','exec')

"""Synthetic correctness checks for persistence and archive isolation."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile

import pytest

from yenibot.experiment import advisor_storage as storage
from yenibot.experiment import advisor_workspace as workspace
from yenibot.experiment import advisor_runtime as runtime


def test_copy_preserves_exact_bytes_and_refuses_conflicting_evidence(tmp_path):
    source=tmp_path/'source';source.write_bytes(b'fixed\x00weights')
    target=tmp_path/'archive/model.pt'
    result=storage.copy_verified(source,target)
    assert result['sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
    assert target.read_bytes()==source.read_bytes()
    target.write_bytes(b'changed')
    with pytest.raises(ValueError,match='replace different'):
        storage.copy_verified(source,target)


@pytest.mark.parametrize('relative',['../outside','/absolute','a/../../escape','C:/escape','a\\b'])
def test_untrusted_manifest_path_cannot_escape(tmp_path,relative):
    with pytest.raises(ValueError):storage.safe_path(tmp_path,relative)


def test_operation_records_failure_and_releases_writer(tmp_path):
    with pytest.raises(RuntimeError,match='synthetic interruption'):
        with storage.operation(tmp_path,'prepare','session1'):
            with pytest.raises(RuntimeError,match='busy'):
                with storage.operation(tmp_path,'train','session2'):pass
            raise RuntimeError('synthetic interruption')
    assert not (tmp_path/'.writer_lease').exists()
    assert json.loads((tmp_path/'STATUS.json').read_text(encoding='utf-8'))['status']=='interrupted_or_failed'
    with storage.operation(tmp_path,'prepare','session3'):pass
    assert json.loads((tmp_path/'STATUS.json').read_text(encoding='utf-8'))['status']=='complete'


def config(tmp_path):
    return {'data':{'frame':str(tmp_path/'data/frame.parquet')},
            'development':{'name':'synthetic'},'labeling':{'max_holding_bars':10}}


def producer(cfg):
    path=Path(cfg['data']['frame'])
    path.write_bytes(b'unchanged synthetic prepared table')
    storage.atomic_json(path.with_suffix('.manifest.json'),{
        'frame_sha256':storage.sha256(path),'protocol':cfg,'rows':4})


def test_prepared_tables_survive_temporary_directory_and_skip_recompute(tmp_path):
    cfg=config(tmp_path)
    metadata=workspace.persist_prepared(cfg,producer)
    path=Path(cfg['data']['frame'])
    assert path.exists() and path.with_suffix('.manifest.json').exists()
    assert metadata['protocol']==cfg
    def forbidden(_):raise AssertionError('should reuse persistent verified frame')
    assert workspace.persist_prepared(cfg,forbidden)==metadata
    package=storage.export_prepared(tmp_path)
    with zipfile.ZipFile(package) as z:
        assert z.read('data/frame.parquet')==path.read_bytes()
        assert 'data/frame.manifest.json' in z.namelist()


def test_reconstruction_hash_failure_does_not_publish_as_original(tmp_path):
    cfg=config(tmp_path)
    with pytest.raises(ValueError,match='Reconstructed bytes differ'):
        workspace.persist_prepared(cfg,producer,expected='0'*64)
    assert not Path(cfg['data']['frame']).exists()


def test_interrupted_preparation_can_retry_without_overwriting_published_data(tmp_path):
    cfg=config(tmp_path)
    def fail(c):
        producer(c)
        raise RuntimeError('power loss before publish')
    with pytest.raises(RuntimeError):workspace.persist_prepared(cfg,fail)
    assert not Path(cfg['data']['frame']).exists()
    workspace.persist_prepared(cfg,producer)
    path=Path(cfg['data']['frame'])
    path.with_suffix('.manifest.json').unlink()  # interrupted between file publish and marker
    assert workspace.persist_prepared(cfg,producer)['protocol']==cfg


def test_published_corruption_and_configuration_drift_fail_closed(tmp_path):
    cfg=config(tmp_path);workspace.persist_prepared(cfg,producer)
    changed=copy.deepcopy(cfg);changed['labeling']['max_holding_bars']=11
    with pytest.raises(ValueError,match='configuration differs'):
        workspace.persist_prepared(changed,producer)
    Path(cfg['data']['frame']).write_bytes(b'corrupt')
    with pytest.raises(ValueError,match='Prepared frame changed'):
        workspace.persist_prepared(cfg,producer)


def test_writable_root_cannot_contain_or_be_inside_historical_archive(tmp_path):
    legacy=tmp_path/'colab_v1'
    for root in [legacy,legacy/'new',tmp_path]:
        with pytest.raises(ValueError):workspace.separate_workspace(root,legacy)
    workspace.separate_workspace(tmp_path/'new_workspace',legacy)


def test_runtime_lock_parser_tracks_transitive_packages(tmp_path):
    lock=tmp_path/'lock'
    lock.write_text('numpy==2.1.3 \\\n --hash=sha256:abc\npandas==2.2.3\n# ignored\n')
    assert runtime.locked_versions(lock)=={'numpy':'2.1.3','pandas':'2.2.3'}


def test_child_environment_does_not_inherit_host_python_paths(monkeypatch):
    for key in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','IPYTHONDIR'):
        monkeypatch.setenv(key,'unreviewed_host_path')
    monkeypatch.setenv('MPLBACKEND','module://matplotlib_inline.backend_inline')
    env=runtime.clean_environment()
    assert env['MPLBACKEND']=='Agg'
    assert all(k not in env for k in ('PYTHONPATH','PYTHONHOME','PYTHONSTARTUP','IPYTHONDIR'))
    assert env['CUBLAS_WORKSPACE_CONFIG']==':4096:8'


def test_immutable_identity_refuses_new_runtime(tmp_path):
    marker=tmp_path/'identity.json'
    storage.immutable_json(marker,{'torch':'fixed','gpu':'T4'})
    with pytest.raises(ValueError,match='Frozen identity changed'):
        storage.immutable_json(marker,{'torch':'new','gpu':'T4'})


def test_stage_references_never_choose_best_from_multiple_completed_runs(tmp_path):
    for name in ['A_one','A_two']:
        storage.atomic_json(tmp_path/'runs'/name/'status.json',{'status':'complete'})
    with pytest.raises(ValueError,match='exactly one completed A'):
        workspace.current_references(tmp_path)


def final_fixture(root):
    final=root/'final_test_v1'
    plan={'fixed_test':'seen September'}
    contract=hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()
    storage.atomic_json(final/'data/final_plan.json',plan)
    artifacts=[]
    for seed in [42,43,44]:
        path=final/f'artifacts/seed_{seed}.pt';path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(b'not a real checkpoint; must never deserialize')
        artifacts.append({'seed':seed,'path':f'artifacts/seed_{seed}.pt','sha256':storage.sha256(path)})
    frames={}
    for name in ['fit','test']:
        path=final/f'data/{name}_frame.parquet';path.write_bytes(name.encode())
        frames[name]=storage.sha256(path)
        storage.atomic_json(path.with_suffix('.manifest.json'),{'sha256':frames[name]})
    frozen={'seeds':[42,43,44],'artifacts':artifacts,'contract_sha256':contract,'fit_frame_sha256':frames['fit']}
    storage.atomic_json(final/'artifacts/frozen_manifest.json',frozen)
    result={'identity':{'freeze_sha256':storage.sha256(final/'artifacts/frozen_manifest.json'),
        'contract_sha256':contract,'test_frame_sha256':frames['test']},'prediction_files':[],
        'test_fit_operations':0,'test_evaluations':1,'aggregate_mean_std':{'f1':{'mean':.1}}}
    storage.atomic_json(final/'runs/test/test_results.json',result)
    return final


def test_final_audit_reads_frozen_bytes_without_loading_or_scoring(tmp_path,monkeypatch):
    import torch
    monkeypatch.setattr(torch,'load',lambda *a,**k:pytest.fail('model was deserialized'))
    final=final_fixture(tmp_path/'legacy')
    original={p.relative_to(final).as_posix():storage.sha256(p) for p in final.rglob('*') if p.is_file()}
    audit=workspace.audit_final(tmp_path/'legacy',tmp_path/'audit')
    assert audit['test_rerun'] is False and audit['models_loaded'] is False
    assert original=={p.relative_to(final).as_posix():storage.sha256(p) for p in final.rglob('*') if p.is_file()}


def test_final_audit_rejects_prediction_identity_change(tmp_path):
    final=final_fixture(tmp_path/'legacy')
    (final/'artifacts/seed_42.pt').write_bytes(b'changed')
    with pytest.raises(ValueError,match='artifact changed'):
        workspace.audit_final(tmp_path/'legacy',tmp_path/'audit')


def test_all_notebooks_are_thin_safe_and_archive_does_not_execute_test():
    root=Path(__file__).resolve().parents[1]
    for phase,name in [('basic','06_advisor_ablation_colab.ipynb'),('full','07_advisor_full_features_colab.ipynb'),
                       ('wavelet','08_advisor_wavelet_colab.ipynb'),('loss','09_advisor_losses_colab.ipynb'),
                       ('final','10_advisor_final_test_colab.ipynb')]:
        notebook=json.loads((root/'notebooks'/name).read_text(encoding='utf-8'))
        source='\n'.join(c['source'] for c in notebook['cells'] if c['cell_type']=='code')
        assert 'import torch' not in source and 'import pandas' not in source
        assert 'RESEARCH_PYTHON' in source and 'RELEASE_TAG' in source
        assert "env['MPLBACKEND']='Agg'" in source
        assert "execute_step('bundle')" in source
        assert 'pip install' not in source
        if phase=='final':assert 'evaluate-test' not in source and "execute_step('audit-final')" in source
        for i,c in enumerate(notebook['cells']):
            if c['cell_type']=='code':compile(c['source'],f'{name}:{i}','exec')


def test_bootstrap_uses_hash_lock_and_never_host_pip_install(monkeypatch):
    root=Path(__file__).resolve().parents[1]
    spec=importlib.util.spec_from_file_location('advisor_bootstrap',root/'scripts/bootstrap_advisor.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    monkeypatch.setenv('UV_SYSTEM_PYTHON','1')
    monkeypatch.setenv('MPLBACKEND','module://matplotlib_inline.backend_inline')
    env=module.environment(Path('/cache'),Path('/python'))
    assert env['MPLBACKEND']=='Agg' and 'UV_SYSTEM_PYTHON' not in env
    assert 'PYTHONPATH' not in env and env['UV_NO_CONFIG']=='1'
    profile=json.loads((root/'requirements/advisor-environment.json').read_text(encoding='utf-8'))
    assert storage.sha256(root/profile['lock'])==profile['lock_sha256']
    assert profile['python']=='3.13.15'
    lock=(root/profile['lock']).read_text(encoding='utf-8')
    assert '--hash=sha256:' in lock and 'torch==2.11.0' in lock


def test_inventory_separates_changing_session_files(tmp_path):
    log=tmp_path/'sessions/current/train.log'
    log.parent.mkdir(parents=True);log.write_text('running')
    weights=tmp_path/'runs/A/model.pt'
    weights.parent.mkdir(parents=True);weights.write_bytes(b'weights')
    result=storage.inventory(tmp_path)
    assert result['volatile_session_files']==['sessions/current/train.log']
    assert [item['path'] for item in result['files']]==['runs/A/model.pt']
    assert result['files'][0]['sha256']==storage.sha256(weights)


@pytest.mark.parametrize('mode,phase,action',[
    ('research','final','prepare'),('research','basic','audit-final'),
    ('archive','basic','bundle'),('recovery','final','train'),
])
def test_cli_refuses_unsupported_final_execution(tmp_path,monkeypatch,mode,phase,action):
    import sys
    monkeypatch.setattr(sys,'argv',['advisor',action,'--mode',mode,'--phase',phase,
        '--root',str(tmp_path/'new'),'--legacy',str(tmp_path/'old'),'--session','test'])
    with pytest.raises(SystemExit) as error:workspace.main()
    assert error.value.code==2
    assert not (tmp_path/'new').exists()


def test_source_archive_is_persistent_and_verified(tmp_path):
    import subprocess
    repo=tmp_path/'repo';repo.mkdir()
    subprocess.run(['git','init',str(repo)],check=True,capture_output=True)
    for name in ['config.yaml','requirements/advisor-environment.json']:
        path=repo/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('{}')
    subprocess.run(['git','-C',str(repo),'add','.'],check=True)
    subprocess.run(['git','-C',str(repo),'-c','user.name=Test','-c','user.email=test@example.com',
        'commit','-m','fixture'],check=True,capture_output=True)
    root=tmp_path/'drive'
    runtime.freeze_workspace_identity(repo,root,{'python':'fixed'})
    archive=root/'reproducibility/source.zip'
    with zipfile.ZipFile(archive) as z:assert 'config.yaml' in z.namelist()
    runtime.freeze_workspace_identity(repo,root,{'python':'fixed'})
    archive.write_bytes(b'corrupted')
    with pytest.raises(ValueError,match='Archived source identity'):
        runtime.freeze_workspace_identity(repo,root,{'python':'fixed'})


def test_bootstrap_keeps_all_uv_state_off_drive(tmp_path,monkeypatch):
    root=Path(__file__).resolve().parents[1]
    spec=importlib.util.spec_from_file_location('bootstrap_drive_test',root/'scripts/bootstrap_advisor.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    repo=tmp_path/'repo';(repo/'requirements').mkdir(parents=True)
    lock=repo/'requirements/test.lock';lock.write_text('pip==26.2.1')
    drive=tmp_path/'drive-shortcut';drive.mkdir()
    runtime_root=tmp_path/'content-runtime'
    wheel=drive/'seed.whl'
    with zipfile.ZipFile(wheel,'w') as archive:archive.writestr('uv.data/scripts/uv',b'fake executable')
    checksum=storage.sha256(wheel);wheel.rename(drive/('uv-'+checksum+'.whl'))
    profile={'lock':'requirements/test.lock','lock_sha256':storage.sha256(lock),
        'python':'3.13.15','uv':{'version':'0.13.0','sha256':checksum,'url':'must-not-download'}}
    storage.atomic_json(repo/'requirements/advisor-environment.json',profile)
    monkeypatch.setattr(module.platform,'system',lambda:'Linux')
    monkeypatch.setattr(module.platform,'machine',lambda:'x86_64')
    monkeypatch.setenv('UV_CACHE_DIR',str(drive/'bad-cache'))
    monkeypatch.setenv('TMPDIR',str(drive/'bad-tmp'))
    calls=[]
    def check_env(env):
        for key in ['UV_CACHE_DIR','UV_PYTHON_INSTALL_DIR','TMPDIR']:
            path=Path(env[key]);assert path.is_relative_to(runtime_root)
        assert Path(env['UV_CACHE_DIR']).is_dir() and Path(env['TMPDIR']).is_dir()
    def output(command,**kwargs):
        check_env(kwargs['env']);calls.append(command)
        return 'uv 0.13.0' if command[-1]=='--version' else str(runtime_root/'python/bin/python')
    def run(command,**kwargs):
        check_env(kwargs['env']);calls.append(command)
        if command[1]=='venv':
            target=Path(command[-1]);target.mkdir()
            (target/'pyvenv.cfg').write_text('include-system-site-packages = false')
    monkeypatch.setattr(module.subprocess,'check_output',output)
    monkeypatch.setattr(module.subprocess,'run',run)
    result=module.bootstrap(repo,runtime_root,drive,tmp_path/'receipt.json')
    assert result['uv_cache']==str(runtime_root/'uv-cache')
    assert not (drive/'uv-cache').exists()
    assert any('--require-hashes' in command for command in calls)


@pytest.mark.parametrize('host_backend',[
    'module://matplotlib_inline.backend_inline','module://missing_host_backend.backend',
])
def test_launcher_overrides_colab_backend_before_package_import(tmp_path,host_backend):
    import os
    import subprocess
    import sys
    root=Path(__file__).resolve().parents[1]
    env=dict(os.environ,MPLBACKEND=host_backend)
    result=subprocess.run([sys.executable,'-I',str(root/'scripts/advisor_workspace.py'),
        '--help'],cwd=tmp_path,env=env,capture_output=True,text=True,timeout=90)
    assert result.returncode==0,result.stdout+result.stderr
    assert 'audit-final' in result.stdout

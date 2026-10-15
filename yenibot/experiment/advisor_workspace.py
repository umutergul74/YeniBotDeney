"""Durable notebook orchestration around the unchanged advisor research engine.

Historical colab_v1 is read-only. New runs live in a separately frozen workspace.
The already-seen September final holdout has NO execution command here.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import tempfile

from yenibot.experiment.advisor_storage import (
    atomic_json, copy_verified, export_prepared, immutable_json, inventory,
    operation, safe_path, sha256, verify_prepared,
)
from yenibot.experiment.advisor_runtime import freeze_workspace_identity, runtime_identity

REPO = Path(__file__).resolve().parents[2]


def separate_workspace(root: Path, legacy: Path) -> None:
    root, legacy = root.resolve(), legacy.resolve()
    if root == legacy or root.is_relative_to(legacy) or legacy.is_relative_to(root):
        raise ValueError('Historical archive and writable workspace must be separate sibling directories')


def checked_snapshot(legacy: Path, root: Path, *, full: bool) -> Path:
    source = legacy / 'inputs/market_snapshot_v1'
    saved = json.loads((source / 'snapshot_manifest.json').read_text())
    target = root / 'inputs/market_snapshot_v1'
    for record in saved['files'].values():
        src = safe_path(source, record['file'])
        dst = safe_path(target, record['file'])
        copy_verified(src, dst, record['sha256'])
    copy_verified(source / 'snapshot_manifest.json', target / 'snapshot_manifest.json')
    if full:
        oi = legacy / 'inputs/oi_snapshot_v1/btc_futures_metrics.parquet'
        marker = oi.with_suffix('.manifest.json')
        metadata = json.loads(marker.read_text())
        out = root / 'inputs/oi_snapshot_v1' / oi.name
        copy_verified(oi, out, metadata['sha256'])
        copy_verified(marker, out.with_suffix('.manifest.json'))
    return target


def read_config(name: str) -> dict:
    import yaml
    return yaml.safe_load((REPO / name).read_text())


def base_config(root: Path, *, full: bool, reference: Path | None) -> dict:
    cfg = read_config('configs/advisor_ablation.yaml')
    cfg['output'] = str(root / 'runs')
    cfg['data'].update(snapshot=str(root / 'inputs/market_snapshot_v1'),
        frame=str(root / 'data' / ('development_full_wavelet_off.parquet' if full else 'development_wavelet_off.parquet')),
        feature_config=str(REPO / 'config.yaml'),
        feature_columns_file=str(REPO / 'configs/advisor_full_features.txt'))
    if full:
        cfg['data'].update(futures_metrics=str(root / 'inputs/oi_snapshot_v1/btc_futures_metrics.parquet'),
            reference_a_manifest=str(reference),
            oi_policy={'tolerance_minutes':90,'max_diff_gap_minutes':15,'min_coverage':.99})
    return cfg


def persist_prepared(cfg: dict, producer, *, expected: str | None = None) -> dict:
    """Compute in disposable storage, publish the verified table AND manifest.

    An interrupted computation cannot replace a published dataset. New metadata
    explicitly records the preparation config; historical manifests are untouched.
    """
    target = Path(cfg['data']['frame'])
    marker = target.with_suffix('.manifest.json')
    if marker.exists():
        metadata = verify_prepared(target, cfg)
        if expected and metadata['frame_sha256'] != expected:
            raise ValueError('Recovered table differs from original protocol')
        return metadata
    with tempfile.TemporaryDirectory(prefix='advisor_prepare_') as temp:
        scratch = copy.deepcopy(cfg)
        scratch['data']['frame'] = str(Path(temp) / target.name)
        producer(scratch)
        temporary = Path(scratch['data']['frame'])
        metadata = verify_prepared(temporary)
        actual = metadata['frame_sha256']
        if expected and actual != expected:
            raise ValueError(f'Reconstructed bytes differ: {actual} != {expected}; original evidence not replaced')
        copy_verified(temporary, target, actual)
        metadata['preparation_config'] = metadata['protocol']
        metadata['protocol'] = copy.deepcopy(cfg)
        atomic_json(marker, metadata)
    return verify_prepared(target, cfg)


def recover(root: Path, legacy: Path, full: bool) -> None:
    """New reconstruction with exact byte check; never silently repair colab_v1."""
    from yenibot.training import advisor
    run = 'B_67a0db4c5eb3' if full else 'A_81029f6d6d48'
    original = json.loads((legacy / 'runs' / run / 'protocol.json').read_text())
    snapshot = checked_snapshot(legacy, root, full=full)
    reference = legacy / 'data/A_reference.manifest.json'
    cfg = base_config(root, full=full, reference=reference)
    # Reuse the exact feature settings frozen with A, rather than a future default.
    feature_cfg = json.loads(reference.read_text())['feature_config']
    import yaml
    frozen_feature = root / 'reproducibility/recovery_feature_config.yaml'
    frozen_feature.parent.mkdir(parents=True, exist_ok=True)
    if frozen_feature.exists():
        if yaml.safe_load(frozen_feature.read_text()) != feature_cfg:
            raise ValueError('Recovery feature config changed')
    else:
        frozen_feature.write_text(yaml.safe_dump(feature_cfg,sort_keys=False))
    cfg['data']['feature_config'] = str(frozen_feature)
    original_sources=json.loads(reference.read_text())['source_hashes']
    for interval, expected in original_sources.items():
        if sha256(snapshot / f'btc_{interval}.parquet') != expected:
            raise ValueError('Historical source differs')
    metadata = persist_prepared(cfg, advisor.prepare, expected=original['data_sha256'])
    atomic_json(root / 'data' / (('full' if full else 'basic') + '_recovery_audit.json'),
        {'original_run':run,'expected_sha256':original['data_sha256'],
         'actual_sha256':metadata['frame_sha256'],'original_archive_modified':False})
    print('Original prepared-table SHA matched:', metadata['frame_sha256'], flush=True)


def current_references(root: Path) -> dict:
    """Resolve by completion and experiment identity, NEVER pick a favorable run."""
    stage = read_config('configs/advisor_stages.yaml')
    for name in ('A','B','C','D'):
        candidates = []
        for p in sorted((root / 'runs').glob(name + '_*/status.json')):
            state = json.loads(p.read_text())
            if state['status'] == 'complete':
                candidates.append(p.parent.name)
        if len(candidates) != 1:
            raise ValueError(f'Expected exactly one completed {name} scope, found {candidates}')
        stage['reference_runs'][name] = candidates[0]
    return stage


def prepare_research(root: Path, legacy: Path, phase: str) -> dict:
    from yenibot.training import advisor, advisor_stages as stages
    from yenibot.training.advisor_colab import pin_completed_a_reference
    if phase in ('basic','full'):
        full = phase == 'full'
        checked_snapshot(legacy, root, full=full)
        reference = pin_completed_a_reference(root) if full else None
        cfg = base_config(root, full=full, reference=reference)
        persist_prepared(cfg, advisor.prepare)
    else:
        stage = current_references(root)
        decision, control = stages.select_architecture(root, stage)
        # Engine v1 deliberately supports the reviewed A/6-channel winner only.
        # A different result needs a new scientific protocol, never forced A selection.
        reference = pin_completed_a_reference(root)
        cfg = copy.deepcopy(control['config'])
        cfg['output'] = str(root / 'runs')
        cfg['data']['frame'] = str(root / 'data/stages_wavelet_channels.parquet')
        cfg['stage'] = {'phase':'wavelet' if phase == 'wavelet' else 'loss',
            'specification':stage,'reference_manifest':str(reference),
            'architecture_selection':decision,
            'holdout_config':str(REPO / 'configs/advisor_final_test.yaml')}
        if phase == 'loss':
            cfg['stage']['wavelet_selection'] = stages.select_wavelet(root,stage,decision)
        # prepare_data's frame identity includes the config; all stages share
        # the same computed channel table but retain their own protocol manifests.
        cfg['data']['frame'] = str(root / 'data' / f'stages_{phase}.parquet')
        persist_prepared(cfg, stages.prepare_data)
    immutable_json(root / 'data' / f'config_{phase}.json', cfg)
    return cfg


def train(root: Path, phase: str, experiments: list[str], allow: bool) -> None:
    if not allow:
        raise ValueError('Training disabled. Enable ALLOW_TRAINING explicitly in the notebook settings.')
    from yenibot.training import advisor, advisor_stages as stages
    cfg = json.loads((root / 'data' / f'config_{phase}.json').read_text())
    verify_prepared(Path(cfg['data']['frame']), cfg)
    expected = {'basic':{'A'},'full':{'B','C','D'},'wavelet':{'W_ON'},
                'loss':{'L_WEIGHTED_BCE','L_FOCAL','L_BCE_PEARSON','L_FOCAL_PEARSON'}}[phase]
    if not experiments or not set(experiments).issubset(expected) or len(set(experiments)) != len(experiments):
        raise ValueError('Invalid experiment list for notebook phase')
    runner = advisor.run if phase in ('basic','full') else stages.run
    for name in experiments:
        runner(cfg, name)
    if phase == 'loss' and set(experiments) == expected:
        stages.finalize_losses(root, cfg['stage']['specification'], cfg['stage']['architecture_selection'])


def audit_final(legacy: Path, destination: Path) -> dict:
    """Read existing final evidence only; never call fit/predict/evaluate."""
    final = legacy / 'final_test_v1'
    frozen = json.loads((final / 'artifacts/frozen_manifest.json').read_text())
    if frozen['seeds'] != [42,43,44] or len(frozen['artifacts']) != 3:
        raise ValueError('Final seed scope changed')
    for entry in frozen['artifacts']:
        if sha256(safe_path(final, entry['path'])) != entry['sha256']:
            raise ValueError('Frozen final model/scaler artifact changed')
    results = json.loads((final / 'runs/test/test_results.json').read_text())
    identity = results['identity']
    if sha256(final / 'artifacts/frozen_manifest.json') != identity['freeze_sha256']:
        raise ValueError('Final result freeze identity changed')
    if frozen['contract_sha256'] != identity['contract_sha256']:
        raise ValueError('Final contract identity changed')
    plan = json.loads((final / 'data/final_plan.json').read_text())
    import hashlib
    if hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest()!=identity['contract_sha256']:
        raise ValueError('Final plan changed')
    for name in ('fit','test'):
        marker = json.loads((final / f'data/{name}_frame.manifest.json').read_text())
        if sha256(final / f'data/{name}_frame.parquet') != marker['sha256']:
            raise ValueError('Final prepared frame changed')
        expected=frozen['fit_frame_sha256'] if name=='fit' else identity['test_frame_sha256']
        if marker['sha256']!=expected:
            raise ValueError('Final frame identity differs from frozen result')
    if results['test_fit_operations'] != 0 or results['test_evaluations'] != 1:
        raise ValueError('Unexpected final fit/evaluation scope')
    for entry in results['prediction_files']:
        if sha256(safe_path(final / 'runs/test', entry['path'])) != entry['sha256']:
            raise ValueError('Final prediction file changed')
    audit = {'status':'verified_read_only','result':results,'models_loaded':False,
             'test_rerun':False,'test_is_seen':True}
    atomic_json(destination / 'data/final_archive_audit.json',audit)
    print(json.dumps(results['aggregate_mean_std'],ensure_ascii=False,indent=2))
    return audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['prepare','train','status','bundle','audit-final'])
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--legacy',type=Path,required=True)
    parser.add_argument('--mode',choices=['recovery','research','archive'],required=True)
    parser.add_argument('--phase',choices=['basic','full','wavelet','loss','final'],required=True)
    parser.add_argument('--session',required=True)
    parser.add_argument('--experiments',nargs='*',default=[])
    parser.add_argument('--allow-training',action='store_true')
    args = parser.parse_args()
    if not args.session.replace('-','').replace('_','').isalnum():
        parser.error('Invalid session identifier')
    if args.phase == 'final' and args.mode != 'archive':
        parser.error('Seen final test is archive-only')
    if args.action == 'audit-final' and (args.mode != 'archive' or args.phase != 'final'):
        parser.error('audit-final requires archive mode and final phase')
    if args.mode == 'archive' and args.phase != 'final':
        parser.error('Archive mode requires final phase')
    root, legacy = args.root.resolve(),args.legacy.resolve()
    separate_workspace(root,legacy)
    if args.action=='status':
        for p in sorted((root / 'runs').glob('*/status.json')):
            state=json.loads(p.read_text());print(p.parent.name,state['status'],len(state.get('completed',[])))
        print('Progress:',root/'STATUS.json')
        return
    if args.mode=='archive' and args.action not in ('audit-final','bundle'):
        parser.error('Historical final archive is read-only')
    if args.action=='train' and args.mode!='research':
        parser.error('Recovery/archive mode cannot train')
    with operation(root,args.action,args.session):
        if args.action in ('prepare','train'):
            identity=runtime_identity(REPO,require_gpu=args.action=='train' or args.phase in ('wavelet','loss'))
            freeze_workspace_identity(REPO,root,identity)
            copy_verified(REPO/'requirements/advisor-linux-py313.lock',root/'reproducibility/dependencies.lock')
            copy_verified(REPO/'requirements/advisor-environment.json',root/'reproducibility/environment.json')
        if args.action=='prepare':
            if args.mode=='recovery':
                if args.phase not in ('basic','full'):
                    parser.error('Recovery supports only the two historical A-D tables')
                recover(root,legacy,args.phase=='full')
            else:
                prepare_research(root,legacy,args.phase)
            print('Prepared data ZIP:',export_prepared(root))
        elif args.action=='train':
            train(root,args.phase,args.experiments,args.allow_training)
        elif args.action=='audit-final':
            audit_final(legacy,root)
        if args.action in ('bundle','train'):
            from yenibot.training.advisor_colab import create_review_bundle
            print('Small review ZIP:',create_review_bundle(root,{'mode':args.mode,'session':args.session}))
            atomic_json(root/'reports/full_artifact_inventory.json',inventory(root))


if __name__=='__main__':
    main()

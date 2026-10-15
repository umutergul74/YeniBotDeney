"""Separate, fixed-date barrier study; old engines and evidence remain unchanged."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import average_precision_score, log_loss, precision_recall_fscore_support

from yenibot.experiment.advisor_runtime import runtime_identity, freeze_workspace_identity
from yenibot.experiment.advisor_storage import (
    atomic_json, immutable_json, copy_verified, sha256, operation, inventory,
)
from yenibot.experiment.advisor_workspace import separate_workspace, read_config, REPO
from yenibot.training import advisor, advisor_final
from yenibot.training.advisor_models import build_advisor_model
from yenibot.training.walk_forward import FoldIndices

CANDIDATES = {'B25': (2., 5.), 'B11': (1., 1.), 'B12': (1., 2.),
              'B152': (1.5, 2.), 'B22': (2., 2.), 'B32': (3., 2.)}
RAW_SHA = 'f3a29be9f7a935ca144fe70a701b41072f30a1b2432b177faa309a8c37b404c6'
DATES = {
    'train_start': '2025-12-18T00:00:00Z', 'train_end': '2026-07-15T23:00:00Z',
    'validation_start': '2026-07-17T00:00:00Z', 'validation_end': '2026-08-08T23:00:00Z',
    'calibration_start': '2026-08-10T00:00:00Z', 'calibration_end': '2026-08-30T23:00:00Z',
    'test_start': '2026-10-02T00:00:00Z', 'test_end': '2026-10-14T23:00:00Z',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def plan():
    cfg = read_config('configs/advisor_ablation.yaml')
    return {'schema': 1, 'experiment': 'exp-015-six-barrier-training', 'dates': DATES,
            'candidates': CANDIDATES, 'model': cfg['model'], 'training': cfg['training'],
            'features': cfg['data']['basic_features'], 'raw_sha256': RAW_SHA,
            'horizon_hours': 10, 'same_bar_rule': 'stop-first',
            'epoch_selection': 'minimum validation BCE per seed',
            'threshold_selection': 'maximum mean calibration F1; tie: highest threshold; grid 0:0.005:1',
            'candidate_selection': 'maximum mean calibration BCE skill vs training prevalence; tie: candidate ID',
            'test_policy': 'all six frozen candidates reported once; no test selection or refit',
            'limitations': ['Historical validation and calibration are previously seen development data.',
                            'Different barriers define different targets; skill ranking is provisional.',
                            '312 test hours is a short single-regime holdout; no profitability claim.']}


def validate_dates(dates):
    times = {k: pd.Timestamp(v) for k, v in dates.items()}
    for value in times.values():
        if value.tzinfo is None or value.utcoffset().total_seconds() or value != value.floor('h'):
            raise ValueError('Whole UTC hours required')
    sections = ['train', 'validation', 'calibration', 'test']
    for section in sections:
        if times[section+'_end'] < times[section+'_start']:
            raise ValueError('Inverted dates')
    for before, after in zip(sections, sections[1:]):
        if times[after+'_start'] - times[before+'_end'] < pd.Timedelta(hours=25):
            raise ValueError('Need 24 empty hours between sections')
    if times['test_start'] <= pd.Timestamp('2026-10-01T23:00:00Z'):
        raise ValueError('Seen September and October 1 are excluded')
    return times


def configuration(name):
    cfg = read_config('configs/advisor_ablation.yaml')
    cfg['labeling'].update(tp_multiplier=CANDIDATES[name][0], sl_multiplier=CANDIDATES[name][1])
    cfg['selected_method'] = {'features': cfg['data']['basic_features']}
    return cfg


def save_frame(path, frame):
    """Never overwrite a differing published frame, including after interruption."""
    with tempfile.TemporaryDirectory(prefix='barrier_frame_') as folder:
        tmp = Path(folder)/'frame.parquet'
        frame.to_parquet(tmp, index=False)
        copy_verified(tmp, path)
    immutable_json(path.with_suffix('.manifest.json'), {'sha256': sha256(path), 'rows': len(frame)})


def load_frame(path):
    meta = json.loads(path.with_suffix('.manifest.json').read_text())
    if sha256(path) != meta['sha256']:
        raise ValueError('Prepared frame changed')
    return pd.read_parquet(path)


def contract(cfg):
    return {'config': cfg, 'feature_config': read_config('config.yaml')}


def prepare(root, legacy):
    if (root/'artifacts/freeze.json').exists():
        verify_freeze(root)
        print('Frozen study verified; preparation skipped.')
        return
    src = legacy/'final_test_v1/inputs/fit_raw/btc_1h.parquet'
    dst = root/'inputs/fit_raw/btc_1h.parquet'
    copy_verified(src, dst, RAW_SHA)
    raw = pd.read_parquet(dst)
    times = validate_dates(DATES)
    end = times['calibration_end'] + pd.Timedelta(hours=10)
    raw, _ = advisor_final.validate_raw_range(raw, pd.Timestamp('2022-01-01T00:00:00Z'),
                                             end, 'preserve_verified_empty')
    for name in CANDIDATES:
        cfg = configuration(name)
        frame = advisor_final.feature_frame(raw, contract(cfg))
        frame = advisor_final.exact_scope(frame, times['train_start'], times['calibration_end'],
                                           cfg['selected_method']['features'])
        split_indices(frame)  # Boundary audits before publication.
        save_frame(root/f'data/{name}.parquet', frame)
    print(f'{len(CANDIDATES)} prepared frames saved; no test data read.', flush=True)


def split_indices(frame):
    times = validate_dates(DATES)
    indices = {}
    for part in ['train', 'validation', 'calibration']:
        mask = frame.timestamp.between(times[part+'_start'], times[part+'_end'])
        idx = np.flatnonzero(mask)
        expected = pd.date_range(times[part+'_start'], times[part+'_end'], freq='h')
        if not pd.DatetimeIndex(frame.iloc[idx].timestamp).equals(expected):
            raise ValueError('Missing split hours')
        indices[part] = idx
    for a, b in [('train','validation'), ('validation','calibration')]:
        advisor.audit_boundary(frame, indices[a], indices[b], 10)
    return FoldIndices(0, indices['train'], indices['validation'], indices['calibration'])


def train(root, names):
    if (root/'artifacts/freeze.json').exists():
        verify_freeze(root)
        print('Frozen study verified; training skipped.')
        return
    torch.set_num_threads(4)
    for name in names:
        cfg = configuration(name)
        path = root/f'data/{name}.parquet'
        frame = load_frame(path)
        folds = split_indices(frame)
        signature = digest({'plan': plan(), 'data': sha256(path), 'candidate': name,
                            'identity': sha256(root/'reproducibility/workspace_identity.json')})
        for seed in cfg['training']['seeds']:
            advisor.run_fold(frame, folds, cfg, {'architecture': 'gru'}, cfg['selected_method']['features'],
                             seed, root/f'runs/{name}/seed_{seed}', signature, torch.device('cuda'))


def predict(root, name, seed, frame):
    cfg = configuration(name)
    checkpoint = root/f'runs/{name}/seed_{seed}/last.pt'
    # Only locally generated checkpoints in the isolated, hash-verified workspace.
    artifact = torch.load(checkpoint, map_location='cpu', weights_only=False)
    model = build_advisor_model(len(cfg['selected_method']['features']), 'gru', cfg['model']).to('cuda')
    model.load_state_dict(artifact['best_state'])
    _, predictions = advisor_final.score_frame(model, artifact, frame, cfg, torch.device('cuda'))
    return predictions


def score(labels, probabilities, threshold, prevalence):
    p, r, f, _ = precision_recall_fscore_support(labels, probabilities >= threshold,
                                               average='binary', zero_division=0)
    bce = float(log_loss(labels, probabilities, labels=[0, 1]))
    reference = float(log_loss(labels, np.full(len(labels), np.clip(prevalence, 1e-7, 1-1e-7)), labels=[0, 1]))
    return {'precision': float(p), 'recall': float(r), 'f1': float(f), 'bce': bce,
            'ap': float(average_precision_score(labels, probabilities)) if np.any(labels) else 0.,
            'bce_reference': reference, 'bce_skill': 1-bce/reference,
            'positive_rate': float(np.mean(labels)), 'predicted_positive_rate': float(np.mean(probabilities >= threshold)),
            'all_positive_f1': float(2*np.mean(labels)/(1+np.mean(labels)))}


def choose_threshold(predictions, prevalence):
    rows = []
    for threshold in np.linspace(0, 1, 201):
        values = [score(p.label.to_numpy(), p.probability.to_numpy(), threshold, prevalence)
                  for p in predictions]
        rows.append({'threshold': float(threshold), **{
            key: float(np.mean([v[key] for v in values])) for key in values[0]}})
    curve = pd.DataFrame(rows)
    best = curve.sort_values(['f1','threshold'], ascending=[False,False], kind='stable').iloc[0].to_dict()
    return best, curve


def verify_freeze(root):
    frozen = json.loads((root/'artifacts/freeze.json').read_text())
    if frozen['plan_sha256'] != digest(plan()):
        raise ValueError('Frozen plan changed')
    for relative, expected in frozen['files'].items():
        if sha256(root/relative) != expected:
            raise ValueError('Frozen artifact changed: '+relative)
    return frozen


def require_completed_runs(root):
    """Check the entire declared cohort before any calibration inference."""
    for name in CANDIDATES:
        for seed in configuration(name)['training']['seeds']:
            path = root/f'runs/{name}/seed_{seed}/validation_metrics.json'
            if not path.exists() or json.loads(path.read_text())['status'] != 'complete':
                raise ValueError(f'All candidate/seed runs must complete before calibration; missing: {name}/seed_{seed}')


def freeze(root):
    if (root/'artifacts/freeze.json').exists():
        verify_freeze(root)
        print('Existing freeze verified; thresholds unchanged.')
        return
    require_completed_runs(root)
    reports = root/'reports'; reports.mkdir(exist_ok=True)
    results, files = {}, {}
    for name in CANDIDATES:
        frame = load_frame(root/f'data/{name}.parquet')
        folds = split_indices(frame)
        prevalence = float(frame.iloc[folds.train[63:]].label.mean())
        predictions = []
        for seed in (42,43,44):
            folder = root/f'runs/{name}/seed_{seed}'
            prediction_path = folder/'calibration_predictions.parquet'
            if prediction_path.exists():
                p = load_frame(prediction_path)
            else:
                p = predict(root, name, seed, frame.iloc[folds.test].copy())
                save_frame(prediction_path, p)
            predictions.append(p)
        best, curve = choose_threshold(predictions, prevalence)
        best['train_prevalence'] = prevalence
        results[name] = best
        curve.to_csv(reports/f'{name}_thresholds.csv', index=False)
    # Rank solely on calibration; test reports never change this decision.
    selected = sorted(results, key=lambda n: (-results[n]['bce_skill'], n))[0]
    for folder in ['data', 'runs', 'reproducibility']:
        for p in sorted((root/folder).rglob('*')):
            if p.is_file() and not p.name.endswith(('.lock', '.tmp')):
                files[p.relative_to(root).as_posix()] = sha256(p)
    files['inputs/fit_raw/btc_1h.parquet'] = sha256(root/'inputs/fit_raw/btc_1h.parquet')
    immutable_json(root/'artifacts/freeze.json', {'plan_sha256': digest(plan()), 'files': files,
                   'candidates': results, 'selected_on_calibration': selected,
                   'test_evaluations': 0, 'frozen_at': pd.Timestamp.now(tz='UTC').isoformat()})
    make_report(root, results, 'calibration')
    print('All models and thresholds frozen. Selected on calibration:', selected, flush=True)


def make_report(root, results, split):
    import matplotlib.pyplot as plt
    reports = root/'reports'; reports.mkdir(exist_ok=True)
    table = pd.DataFrame.from_dict(results, orient='index').rename_axis('candidate')
    table.to_csv(reports/f'{split}_comparison.csv')
    ax = table[['precision','recall','f1','ap']].plot.bar(figsize=(10,5), ylim=(0,1))
    ax.set_title(f'{split}: fixed barriers / GRU / BCE (mean of 3 seeds)')
    ax.figure.tight_layout(); ax.figure.savefig(reports/f'{split}_comparison.png', dpi=160); plt.close(ax.figure)
    if split == 'calibration':
        rows = (len(CANDIDATES)+1)//2
        fig, axes = plt.subplots(rows,2,figsize=(12,4*rows), squeeze=False)
        for ax, name in zip(axes.flat, CANDIDATES):
            curve = pd.read_csv(reports/f'{name}_thresholds.csv')
            for metric in ['precision','recall','f1']:
                ax.plot(curve.threshold, curve[metric], label=metric)
            ax.axvline(results[name]['threshold'], color='black', linestyle='--')
            ax.set(title=name, xlabel='Threshold', ylim=(0,1)); ax.legend()
        for ax in axes.flat[len(CANDIDATES):]:
            ax.set_visible(False)
        fig.tight_layout(); fig.savefig(reports/'calibration_thresholds.png', dpi=160); plt.close(fig)
    text = '# Bariyer karşılaştırması · '+split+'\n\n'
    text += 'Üç seed ortalaması; ensemble değildir. Hedef etiketleri farklıdır; ham F1/AP/BCE doğrudan üstünlük kanıtı değildir.\n\n'
    text += 'Test: 2–14 Ekim 2026, 312 saat. Masraf, funding, slippage veya portföy simülasyonu yoktur.\n\n'
    columns = ['threshold','precision','recall','f1','ap','bce','bce_skill','all_positive_f1']
    text += '| Aday | '+' | '.join(columns)+' |\n|---|'+'---:|'*len(columns)+'\n'
    for name, row in results.items():
        text += '| '+name+' | '+' | '.join(f'{row[c]:.4f}' for c in columns)+' |\n'
    text += '\nBCE skill = 1 − model BCE / eğitim pozitif oranı referans BCE. Test sonuçlarıyla eşik, seed veya aday seçilmez.\n'
    (reports/f'{split}_REPORT.md').write_text(text, encoding='utf-8')


def test(root):
    frozen = verify_freeze(root)
    receipt = root/'artifacts/test_complete.json'
    if receipt.exists():
        completed = json.loads(receipt.read_text())
        if completed['freeze_sha256'] != sha256(root/'artifacts/freeze.json'):
            raise ValueError('Completed test belongs to a different freeze')
        for rel, expected in completed['files'].items():
            if sha256(root/rel) != expected:
                raise ValueError('Completed test output changed')
        print('Completed test reused; no new evaluation.')
        return
    dates = validate_dates(DATES)
    end = dates['test_end'] + pd.Timedelta(hours=10)
    if pd.Timestamp.now(tz='UTC') < end + pd.Timedelta(hours=1):
        raise ValueError('Last label source candle has not closed')
    cfg = {'raw': {'history_start': '2022-01-01T00:00:00Z', 'zero_activity_policy': 'preserve_verified_empty'}}
    # This is the only action allowed to acquire test prices, and follows the freeze.
    source = advisor_final.extend_source(root/'inputs/fit_raw/btc_1h.parquet',
                                         root/'inputs/test_raw', end, cfg)
    raw = pd.read_parquet(source)
    results = {}
    for name in CANDIDATES:
        cfg = configuration(name)
        frame = advisor_final.feature_frame(raw, contract(cfg))
        frame = advisor_final.exact_scope(frame, dates['test_start']-pd.Timedelta(hours=63), end-pd.Timedelta(hours=10),
                                           cfg['selected_method']['features'])
        save_frame(root/f'data/test_{name}.parquet', frame)
        selected = frozen['candidates'][name]
        scores = []
        for seed in (42,43,44):
            path = root/f'runs/{name}/seed_{seed}/test_predictions.parquet'
            if path.exists():
                p = load_frame(path)
            else:
                p = predict(root, name, seed, frame)
                save_frame(path, p)
            expected = pd.date_range(dates['test_start'], dates['test_end'], freq='h')
            if not pd.DatetimeIndex(pd.to_datetime(p.timestamp,utc=True)).equals(expected):
                raise ValueError('Wrong test prediction timestamps')
            values = score(p.label.to_numpy(), p.probability.to_numpy(), selected['threshold'], selected['train_prevalence'])
            immutable_json(path.with_name('test_metrics.json'), values)
            scores.append(values)
        results[name] = {'threshold': selected['threshold'], **{
            k: float(np.mean([v[k] for v in scores])) for k in scores[0]}}
    make_report(root, results, 'test')
    files = {p.relative_to(root).as_posix(): sha256(p) for p in (root/'runs').rglob('test*') if p.is_file()}
    files.update({p.relative_to(root).as_posix(): sha256(p) for p in (root/'reports').glob('test*') if p.is_file()})
    immutable_json(receipt, {'freeze_sha256': sha256(root/'artifacts/freeze.json'), 'files': files,
                            'completed_at': pd.Timestamp.now(tz='UTC').isoformat()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare','train','freeze','test','bundle'])
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--legacy', type=Path, required=True)
    parser.add_argument('--session', required=True)
    parser.add_argument('--candidates', nargs='+', choices=list(CANDIDATES), default=list(CANDIDATES))
    parser.add_argument('--allow-training', action='store_true')
    parser.add_argument('--allow-test', action='store_true')
    args = parser.parse_args()
    if not args.session.replace('-','').replace('_','').isalnum():
        parser.error('Invalid session')
    if args.action == 'train' and not args.allow_training:
        parser.error('Training disabled')
    if args.action == 'test' and not args.allow_test:
        parser.error('Test disabled; review calibration report first')
    root, legacy = args.root.resolve(), args.legacy.resolve()
    separate_workspace(root, legacy)
    validate_dates(DATES)
    with operation(root, args.action, args.session):
        identity = runtime_identity(REPO, require_gpu=True)
        freeze_workspace_identity(REPO, root, identity)
        immutable_json(root/'artifacts/plan.json', json.loads(json.dumps(plan())))
        if args.action == 'prepare': prepare(root, legacy)
        elif args.action == 'train': train(root, args.candidates)
        elif args.action == 'freeze': freeze(root)
        elif args.action == 'test': test(root)
        else:
            import zipfile
            reports = root/'reports'; reports.mkdir(exist_ok=True)
            atomic_json(reports/'full_artifact_inventory.json', inventory(root))
            target = reports/f'barrier_review_{args.session}_{pd.Timestamp.now(tz="UTC").value}.zip'
            if target.exists(): raise ValueError('Bundle exists; use a new session')
            with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
                for folder in ['artifacts','reports','sessions']:
                    for p in (root/folder).rglob('*'):
                        if p.is_file() and p.suffix != '.zip': archive.write(p,p.relative_to(root))
            print('Review bundle:', target, 'Full models remain in workspace.', flush=True)


if __name__ == '__main__':
    main()

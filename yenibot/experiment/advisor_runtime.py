"""Complete runtime identity for isolated advisor subprocesses."""
from __future__ import annotations

import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile

from yenibot.experiment.advisor_storage import copy_verified, immutable_json, sha256


def locked_versions(path: Path) -> dict:
    return dict(re.findall(r'^([A-Za-z0-9_.-]+)==([^\s\\]+)', path.read_text(), re.M))


def clean_environment() -> dict:
    env = dict(os.environ)
    for name in ('PYTHONPATH', 'PYTHONHOME', 'PYTHONSTARTUP', 'IPYTHONDIR', 'JUPYTER_CONFIG_DIR'):
        env.pop(name, None)
    env.update(PYTHONNOUSERSITE='1', CUBLAS_WORKSPACE_CONFIG=':4096:8',
               OMP_NUM_THREADS='4', MKL_NUM_THREADS='4', MPLBACKEND='Agg')
    return env


def hardware_profile(profile: dict, name: str) -> dict:
    """Explicit opt-in; historical callers retain the original T4 profile."""
    if name == 'default':
        return profile
    if name != 'selective-a100':
        raise ValueError('Unknown hardware profile')
    return {**profile, 'training_gpu': 'NVIDIA A100-SXM4-40GB'}


def runtime_identity(repo: Path, *, require_gpu: bool, hardware: str = 'default') -> dict:
    profile = json.loads((repo / 'requirements/advisor-environment.json').read_text())
    profile = hardware_profile(profile, hardware)
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise ValueError('Training profile supports Linux x86_64 only; use Colab or matching Linux')
    if platform.python_version() != profile['python'] or sys.prefix == sys.base_prefix:
        raise ValueError('Use the pinned isolated interpreter, not the notebook host Python')
    lock = repo / profile['lock']
    if sha256(lock) != profile['lock_sha256']:
        raise ValueError('Dependency lock hash changed')
    from packaging.version import Version
    normalize=lambda name:re.sub(r'[-_.]+','-',name).lower()
    expected_names={normalize(name) for name in locked_versions(lock)}
    installed={normalize(dist.metadata['Name']) for dist in importlib.metadata.distributions()}
    if installed-expected_names:
        raise ValueError(f'Unreviewed packages installed: {sorted(installed-expected_names)}')
    packages = {}
    for name, expected in locked_versions(lock).items():
        actual = importlib.metadata.version(name)
        if Version(actual).public != Version(expected).public:
            raise ValueError(f'Locked package differs: {name}: {actual} != {expected}')
        packages[name] = actual
    import torch
    gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    if require_gpu and gpu != profile['training_gpu']:
        raise ValueError(f'Expected {profile["training_gpu"]}, found {gpu}; do not mix hardware')
    driver = None
    if gpu is not None:
        driver = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'],
            text=True, env=clean_environment()).strip().splitlines()
    subprocess.run([sys.executable, '-I', '-m', 'pip', 'check'], check=True,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=clean_environment())
    identity = {'schema': 1, 'python': sys.version, 'platform': platform.platform(),
            'machine': platform.machine(), 'packages': packages, 'gpu': gpu, 'driver': driver,
            'cuda': torch.version.cuda, 'cudnn': torch.backends.cudnn.version(),
            'lock_sha256': profile['lock_sha256']}
    if hardware != 'default':
        identity.update(hardware_profile=hardware, expected_gpu=profile['training_gpu'])
    return identity


def freeze_workspace_identity(repo: Path, root: Path, identity: dict) -> None:
    """Hash all imported research sources, including transitive feature helpers."""
    sources = {}
    for folder, patterns in [('yenibot', ['*.py']), ('configs', ['advisor*.yaml','advisor*.txt'])]:
        for pattern in patterns:
            for path in sorted((repo / folder).rglob(pattern)):
                sources[path.relative_to(repo).as_posix()] = sha256(path)
    for name in ('config.yaml', 'requirements/advisor-environment.json'):
        sources[name] = sha256(repo / name)
    commit = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    if subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain', '--untracked-files=no']).strip():
        raise ValueError('Research checkout has uncommitted tracked changes')
    immutable_json(root / 'reproducibility/workspace_identity.json',
                   {'runtime': identity, 'sources': sources, 'commit': commit})

    archive = root / 'reproducibility/source.zip'
    marker = archive.with_suffix('.manifest.json')
    if marker.exists():
        record = json.loads(marker.read_text())
        if record['commit'] != commit or sha256(archive) != record['sha256']:
            raise ValueError('Archived source identity changed')
    else:
        with tempfile.TemporaryDirectory(prefix='advisor_source_') as folder:
            candidate = Path(folder) / 'source.zip'
            subprocess.run(['git', '-C', str(repo), 'archive', '--format=zip',
                            '--output=' + str(candidate), 'HEAD'], check=True)
            record = dict(copy_verified(candidate, archive), commit=commit)
            immutable_json(marker, record)

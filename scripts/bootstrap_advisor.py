"""Stdlib-only launcher: never install packages into Colab's host Python."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import urllib.request
import zipfile


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def environment(cache, python_home):
    result = dict(os.environ)
    for key in ('PYTHONPATH', 'PYTHONHOME', 'PYTHONSTARTUP', 'VIRTUAL_ENV',
                'UV_INDEX', 'UV_INDEX_URL', 'UV_EXTRA_INDEX_URL', 'PIP_INDEX_URL',
                'PIP_EXTRA_INDEX_URL', 'PIP_CONFIG_FILE'):
        result.pop(key, None)
    result.update(UV_CACHE_DIR=str(cache), UV_PYTHON_INSTALL_DIR=str(python_home),
                  UV_LINK_MODE='copy', UV_NO_CONFIG='1', PYTHONNOUSERSITE='1',
                  TMPDIR=str(cache.parent / 'tmp'))
    return result


def bootstrap(repo: Path, runtime: Path, cache: Path, receipt: Path) -> dict:
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise ValueError('Use Linux x86_64 (Colab). Windows host packages are not modified.')
    profile = json.loads((repo / 'requirements/advisor-environment.json').read_text())
    lock = repo / profile['lock']
    if digest(lock) != profile['lock_sha256']:
        raise ValueError('Dependency lock does not match reviewed environment profile')
    runtime.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)
    uv_spec = profile['uv']
    wheel = cache / ('uv-' + uv_spec['sha256'] + '.whl')
    if wheel.exists() and digest(wheel) != uv_spec['sha256']:
        raise ValueError('Cached bootstrap wheel was modified')
    if not wheel.exists():
        temp = wheel.with_suffix('.partial')
        urllib.request.urlretrieve(uv_spec['url'], temp)
        if digest(temp) != uv_spec['sha256']:
            temp.unlink(missing_ok=True)
            raise ValueError('Bootstrap download failed hash verification')
        os.replace(temp, wheel)
    uv = runtime / 'uv'
    with zipfile.ZipFile(wheel) as archive:
        entries = [i for i in archive.infolist() if i.filename.endswith('/uv')]
        if len(entries) != 1:
            raise ValueError('Expected exactly one uv executable in verified wheel')
        with archive.open(entries[0]) as source, uv.open('wb') as target:
            shutil.copyfileobj(source, target)
    uv.chmod(0o700)
    # Drive/FUSE cannot provide uv's lock/persist/hardlink semantics.
    # Only the verified bootstrap wheel is cached on Drive. All mutable uv
    # state, Python installs, environments and temporary files stay local.
    local_cache = runtime / 'uv-cache'
    local_cache.mkdir(parents=True, exist_ok=True)
    (runtime / 'tmp').mkdir(parents=True, exist_ok=True)
    env = environment(local_cache, runtime / 'python')
    version = subprocess.check_output([str(uv), '--version'], text=True, env=env).split()
    if version[:2] != ['uv', uv_spec['version']]:
        raise ValueError('Unexpected bootstrap tool version')
    subprocess.run([str(uv), 'python', 'install', profile['python']], check=True, env=env)
    python = subprocess.check_output([str(uv), 'python', 'find', profile['python'],
                                      '--managed-python'], text=True, env=env).strip()
    fingerprint = hashlib.sha256(json.dumps(profile, sort_keys=True).encode()).hexdigest()[:16]
    venv = runtime / ('venv-' + fingerprint)
    if not venv.exists():
        subprocess.run([str(uv), 'venv', '--python', python, str(venv)], check=True, env=env)
    executable = venv / 'bin/python'
    config = (venv / 'pyvenv.cfg').read_text().lower()
    if 'include-system-site-packages = false' not in config:
        raise ValueError('Host packages must not be visible in the research environment')
    subprocess.run([str(uv), 'pip', 'sync', '--python', str(executable), '--require-hashes',
                    '--only-binary', ':all:', '--index-url', 'https://pypi.org/simple', str(lock)],
                   check=True, env=env)
    subprocess.run([str(executable), '-I', '-m', 'pip', 'check'], check=True, env=env)
    result = {'python': str(executable), 'profile_sha256': digest(repo / 'requirements/advisor-environment.json'),
              'lock_sha256': digest(lock), 'python_version': profile['python'], 'host_packages_used': False,
              'uv_cache': str(local_cache), 'temporary_files': str(runtime / 'tmp')}
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Isolated research interpreter:', executable, flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('repo', 'runtime', 'cache', 'receipt'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    bootstrap(args.repo.resolve(), args.runtime.resolve(), args.cache.resolve(), args.receipt.resolve())

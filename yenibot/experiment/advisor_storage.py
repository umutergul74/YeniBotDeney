"""Immutable persistence and integrity checks; no model deserialization."""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid
import zipfile


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, value: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('w', encoding='utf-8', newline='\n') as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def immutable_json(path: Path, value: dict) -> None:
    if path.exists():
        if json.loads(path.read_text(encoding='utf-8')) != value:
            raise ValueError(f'Frozen identity changed: {path}; use a NEW workspace')
    else:
        atomic_json(path, value)


def safe_path(root: Path, relative: str) -> Path:
    if '\\' in relative or ':' in relative or Path(relative).is_absolute():
        raise ValueError('Expected a safe relative artifact path')
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or target == root.resolve():
        raise ValueError('Artifact path escapes workspace')
    return target


def copy_verified(source: Path, destination: Path, expected: str | None = None) -> dict:
    expected = expected or sha256(source)
    if sha256(source) != expected:
        raise ValueError(f'Source hash mismatch: {source}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if sha256(destination) != expected:
            raise ValueError(f'Refusing to replace different evidence: {destination}')
    else:
        temporary = destination.with_name(destination.name + '.' + uuid.uuid4().hex + '.tmp')
        try:
            shutil.copyfile(source, temporary)
            if sha256(temporary) != expected:
                raise ValueError('Copied artifact failed verification')
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
    return {'sha256': expected, 'bytes': destination.stat().st_size}


def verify_prepared(path: Path, expected_config: dict | None = None) -> dict:
    marker = path.with_suffix('.manifest.json')
    metadata = json.loads(marker.read_text(encoding='utf-8'))
    if sha256(path) != metadata['frame_sha256']:
        raise ValueError(f'Prepared frame changed: {path}')
    if expected_config is not None:
        for key in ('data', 'development', 'labeling'):
            if metadata['protocol'][key] != expected_config[key]:
                raise ValueError(f'Prepared frame configuration differs: {key}')
    return metadata


def inventory(root: Path) -> dict:
    """Full inventory includes weights/raw/prepared data, not recursive ZIP copies."""
    files = []
    volatile_files = []
    for folder in ('inputs', 'data', 'runs', 'sessions', 'artifacts', 'reproducibility'):
        for path in sorted((root / folder).rglob('*')):
            if path.is_symlink():
                raise ValueError('Linked artifacts are not a portable archive')
            if path.is_file() and not path.name.endswith(('.tmp', '.lock')):
                if folder == 'sessions':
                    volatile_files.append(path.relative_to(root).as_posix())
                    continue
                files.append({'path': path.relative_to(root).as_posix(),
                              'sha256': sha256(path), 'bytes': path.stat().st_size})
    return {'schema': 2, 'files': files, 'weights_included_in_inventory': True,
            'volatile_session_files': volatile_files,
            'note': 'Session logs/progress may still change; not asserted immutable.'}


def export_prepared(root: Path) -> Path:
    """A separate downloadable ZIP includes the actual prepared tables."""
    reports = root / 'reports'
    reports.mkdir(parents=True, exist_ok=True)
    target = reports / 'prepared_frames.zip'
    temporary = target.with_suffix('.tmp.zip')
    files = []
    for path in sorted((root / 'data').glob('*.parquet')):
        verify_prepared(path)
        files.extend([path, path.with_suffix('.manifest.json')])
    if not files:
        raise FileNotFoundError('No verified prepared frames to export')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root).as_posix())
        archive.writestr('prepared_manifest.json', json.dumps([
            {'path': p.relative_to(root).as_posix(), 'sha256': sha256(p)} for p in files
        ], indent=2))
    os.replace(temporary, target)
    return target


@contextmanager
def operation(root: Path, action: str, session: str):
    """Persistent progress plus a conservative cross-session writer lease.

    Drive atomic-create semantics are not a distributed lock guarantee. A second
    runtime must never be run against the same workspace. Stale leases fail closed.
    """
    lease = root / '.writer_lease'
    root.mkdir(parents=True, exist_ok=True)
    try:
        lease.mkdir()
    except FileExistsError as exc:
        raise RuntimeError(f'Workspace busy/stale lease: {lease}. Confirm no other writer before recovery.') from exc
    state = {'action': action, 'session': session, 'status': 'running',
             'started_at': datetime.now(timezone.utc).isoformat()}
    atomic_json(lease / 'owner.json', state)
    record = root / 'sessions' / session / (action + '.json')
    atomic_json(record, state)
    atomic_json(root / 'STATUS.json', state)
    try:
        yield
        state['status'] = 'complete'
    except BaseException as exc:
        state.update(status='interrupted_or_failed', error=repr(exc))
        raise
    finally:
        state['updated_at'] = datetime.now(timezone.utc).isoformat()
        atomic_json(record, state)
        atomic_json(root / 'STATUS.json', state)
        (root / 'STATUS.md').write_text(
            f"# Advisor çalışma durumu\n\nAşama: {action}\n\nDurum: {state['status']}\n"
            f"\nOturum: {session}\n\nAyrıntı: sessions/{session}/\n", encoding='utf-8')
        (lease / 'owner.json').unlink()
        lease.rmdir()

"""Dependency-free research notebook ledger. Never imports or runs research code."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import zipfile

REPO = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO / 'research'
STATES = {'planned', 'running', 'completed', 'failed', 'abandoned'}
OUTCOMES = {'pending', 'selected', 'not_selected', 'mixed', 'inconclusive', 'technical_failure'}
TRANSITIONS = {'planned': STATES, 'running': {'running', 'completed', 'failed', 'abandoned'},
               'completed': {'completed'}, 'failed': {'failed', 'abandoned'}, 'abandoned': {'abandoned'}}
REQUIRED = {'id', 'campaign', 'title', 'question', 'parent_ids', 'status', 'outcome',
            'method', 'data', 'selection_rule', 'results', 'decision', 'limitations', 'evidence'}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def safe_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or '\\' in relative or ':' in relative or '..' in path.parts:
        raise ValueError('Unsafe relative path')
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Path escapes ledger')
    return target


def validate_record(record):
    if not isinstance(record, dict) or not REQUIRED <= record.keys():
        raise ValueError('Missing record fields')
    for key in ('id', 'campaign'):
        if not isinstance(record[key], str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]{2,79}', record[key]):
            raise ValueError('Invalid ' + key)
    for key in ('title', 'question', 'selection_rule', 'decision'):
        if not isinstance(record[key], str) or not record[key].strip():
            raise ValueError('Empty ' + key)
    if record['status'] not in STATES or record['outcome'] not in OUTCOMES:
        raise ValueError('Invalid status/outcome')
    for key in ('parent_ids', 'results', 'limitations', 'evidence'):
        if not isinstance(record[key], list):
            raise ValueError('Expected list: ' + key)
    if len(set(record['parent_ids'])) != len(record['parent_ids']):
        raise ValueError('Duplicate parents')
    if not isinstance(record['method'], dict) or not isinstance(record['data'], dict):
        raise ValueError('Method/data must be objects')
    for key in ('snapshot_id', 'raw_sha256', 'labels_id', 'split_id', 'evaluation_scope'):
        if key not in record['data']:
            raise ValueError('Missing data identity: ' + key)
    if record['status'] == 'planned' and (record['results'] or record['outcome'] != 'pending'):
        raise ValueError('Planned work cannot have results')
    if record['status'] == 'completed' and (not record['evidence'] or record['outcome'] == 'pending'):
        raise ValueError('Completed work needs evidence and an outcome')
    for result in record['results']:
        if result.get('split') not in {'validation', 'test', 'development'}:
            raise ValueError('Result split must be explicit')
        if not result.get('aggregation') or not result.get('cohort') or not isinstance(result.get('metrics'), dict):
            raise ValueError('Result aggregation, cohort and metrics required')
        for value in result['metrics'].values():
            if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
                raise ValueError('Metrics must be finite numbers')
    for evidence in record['evidence']:
        if not re.fullmatch('[a-f0-9]{64}', evidence.get('sha256', '')):
            raise ValueError('Evidence SHA256 required')
        if not evidence.get('original_path') or not evidence.get('kind'):
            raise ValueError('Evidence provenance required')
        safe_path(Path('.'), evidence['path'])
    encoded(record)


def history(root):
    events, latest = [], {}
    previous = None
    paths = sorted((root / 'events').glob('*.json'))
    for number, path in enumerate(paths, 1):
        if path.name != f'{number:06d}.json':
            raise ValueError('Event sequence has a gap')
        event = json.loads(path.read_text(encoding='utf-8'))
        if event.get('sequence') != number or event.get('previous_sha256') != previous or event.get('schema_version') != 1:
            raise ValueError('Event chain mismatch')
        record = event['record']
        validate_record(record)
        if not event.get('reason', '').strip() or not event.get('recorded_at'):
            raise ValueError('Event reason/time required')
        old = latest.get(record['id'])
        if event.get('revision') != (old['revision'] + 1 if old else 1):
            raise ValueError('Revision mismatch')
        if any(parent not in latest or parent == record['id'] for parent in record['parent_ids']):
            raise ValueError('Parent must already exist')
        if old and (old['record']['parent_ids'] != record['parent_ids'] or old['record']['campaign'] != record['campaign']):
            raise ValueError('Lineage is immutable; create a new experiment')
        if old and record['status'] not in TRANSITIONS[old['record']['status']]:
            raise ValueError('New execution needs a new ID')
        for evidence in record['evidence']:
            source = safe_path(root, evidence['path'])
            if not source.is_file() or digest(source.read_bytes()) != evidence['sha256']:
                raise ValueError('Evidence missing or changed: ' + evidence['path'])
        previous = digest(path.read_bytes())
        latest[record['id']] = event
        events.append(event)
    return events, latest


@contextmanager
def writer(root):
    root.mkdir(parents=True, exist_ok=True)
    lock = root / '.writer.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        lock.unlink()


def append(root, record, reason, *, create=False):
    validate_record(record)
    if not reason.strip():
        raise ValueError('A reason is mandatory')
    with writer(root):
        events, latest = history(root)
        old = latest.get(record['id'])
        if create == bool(old):
            raise ValueError('Create needs a new ID; append needs an existing ID')
        if any(p not in latest or p == record['id'] for p in record['parent_ids']):
            raise ValueError('Unknown parent')
        if old and (old['record']['parent_ids'] != record['parent_ids'] or old['record']['campaign'] != record['campaign']):
            raise ValueError('Lineage is immutable')
        if old and record['status'] not in TRANSITIONS[old['record']['status']]:
            raise ValueError('New execution needs a new ID')
        for evidence in record['evidence']:
            if digest(safe_path(root, evidence['path']).read_bytes()) != evidence['sha256']:
                raise ValueError('Evidence mismatch')
        number = len(events) + 1
        event = {'schema_version': 1, 'sequence': number,
                 'revision': old['revision'] + 1 if old else 1,
                 'previous_sha256': digest((root / 'events' / f'{number-1:06d}.json').read_bytes()) if events else None,
                 'recorded_at': datetime.now(timezone.utc).isoformat(), 'reason': reason, 'record': record}
        folder = root / 'events'
        folder.mkdir(exist_ok=True)
        # Exclusive creation never overwrites an event. Interrupted partial writes fail validation.
        with (folder / f'{number:06d}.json').open('xb') as stream:
            stream.write(encoded(event))
            stream.flush()
            os.fsync(stream.fileno())
        return event


def capture(root, source):
    """Capture a small review document, not a model or raw dataset."""
    source = source.resolve()
    if source.suffix.lower() not in {'.md', '.txt', '.csv', '.json'} or source.stat().st_size > 5_000_000:
        raise ValueError('Only small review documents (<=5 MB) can be captured')
    payload = source.read_bytes()
    sha = digest(payload)
    relative = f'sources/{sha}{source.suffix.lower()}'
    with writer(root):
        target = safe_path(root, relative)
        target.parent.mkdir(exist_ok=True)
        if target.exists():
            if target.read_bytes() != payload:
                raise ValueError('Existing evidence changed')
        else:
            with target.open('xb') as stream:
                stream.write(payload)
    return {'path': relative, 'sha256': sha, 'original_path': source.relative_to(REPO).as_posix()
            if source.is_relative_to(REPO) else str(source), 'kind': 'review_document'}


def check_git_history(root, base):
    relative = root.resolve().relative_to(REPO).as_posix()
    # Compare against working tree, including staged and unstaged edits. No deletions/rewrites.
    changes = subprocess.check_output(['git', '-C', str(REPO), 'diff', '--name-status', '--no-renames',
                                       base, '--', relative + '/events', relative + '/sources'], text=True)
    if any(line.split('\t')[0] != 'A' for line in changes.splitlines()):
        raise ValueError('Published events/evidence cannot be modified or deleted; append a correction')


def text(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def report(root):
    events, latest = history(root)
    lines = ['# Deney defteri', '', 'Bu görünüm kayıtlı sonuçları listeler; analiz veya eğitim çalıştırmaz.',
             'Kaynak: `events/` içindeki eklemeli kayıtlar. Rakamlar kaynak raporların yuvarlatılmış değerleridir.',
             'Validation ve test ayrı kapsamdır; bu tablo otomatik bir başarı sıralaması değildir.', '',
             f'**{len(latest)} deney/plan · {len(events)} geçmiş kaydı**', '',
             '| Kimlik | Soru / yöntem | Durum | Sonuç yorumu |', '|---|---|---|---|']
    for id_, event in latest.items():
        r = event['record']
        lines.append(f"| [{id_}](#{id_}) | {text(r['title'])} | {r['status']} | {r['outcome']} |")
    groups = {}
    for id_, event in latest.items():
        for result in event['record']['results']:
            key = (result['split'], result['cohort'], result['aggregation'])
            groups.setdefault(key, []).append((id_, result['metrics']))
    for (split, cohort, aggregation), rows in groups.items():
        lines += ['', f'## Kayıtlı sonuçlar · {split}', '', f'{cohort} · {aggregation}', '',
                  'Yalnızca mevcut rapor değerlerinin yan yana görünümü; yeniden puanlama/sıralama yok.', '',
                  '| Deney | BCE ↓ | AP ↑ | Precision | Recall | F1 |', '|---|---:|---:|---:|---:|---:|']
        for id_, metrics in rows:
            values = [f'{metrics[k]:.6f}' if k in metrics else '—' for k in ('BCE', 'AP', 'precision', 'recall', 'F1')]
            lines.append('| ' + id_ + ' | ' + ' | '.join(values) + ' |')
    for id_, event in latest.items():
        r = event['record']
        lines += ['', f'## {id_}', '', f"**{r['title']}**", '', r['question'], '',
                  f"Kampanya: `{r['campaign']}` · Durum: **{r['status']}** · Sonuç: **{r['outcome']}**",
                  '', 'Önceki kayıtlar: ' + (', '.join(r['parent_ids']) or 'yok'), '',
                  '**Yöntem:** ' + text(json.dumps(r['method'], ensure_ascii=False)), '',
                  '**Veri kimliği:** ' + text(json.dumps(r['data'], ensure_ascii=False)), '',
                  '**Seçim kuralı:** ' + r['selection_rule'], '', '**Karar / öğrenilen:** ' + r['decision']]
        for result in r['results']:
            lines += ['', f"**{result['split']}** · {result['cohort']} · {result['aggregation']}", '',
                      '| Ölçüt | Kayıtlı değer |', '|---|---:|']
            lines += [f'| {text(k)} | {v:.6f} |' for k, v in result['metrics'].items()]
        if not r['results']:
            lines += ['', '**Henüz sonuç yok.**']
        lines += ['', '**Sınırlar / açık noktalar:**'] + ['- ' + x for x in r['limitations']]
        lines += ['', '**Kanıt kopyaları:**'] + [f"- [{e['original_path']}]({e['path']}) · SHA256 `{e['sha256']}`" for e in r['evidence']]
        lines += ['', f"[Son kayıt](events/{event['sequence']:06d}.json) · revizyon {event['revision']} · {event['reason']}"]
    return '\n'.join(lines) + '\n'


def bundle(root, output):
    with writer(root):
        history(root)
        files = sorted(p for p in root.rglob('*') if p.is_file() and p.name != '.writer.lock')
        if output.resolve().is_relative_to(root.resolve()):
            raise ValueError('Backup must be outside ledger')
        payloads = {p.relative_to(root).as_posix(): p.read_bytes() for p in files}
        manifest = {name: digest(data) for name, data in payloads.items()}
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            for name, payload in payloads.items():
                archive.writestr(name, payload)
            archive.writestr('BACKUP-MANIFEST.json', encoded(manifest))
    return len(files)


def verify_bundle(path):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate backup members')
        manifest = json.loads(archive.read('BACKUP-MANIFEST.json'))
        if set(names) != set(manifest) | {'BACKUP-MANIFEST.json'}:
            raise ValueError('Backup membership mismatch')
        for name, sha in manifest.items():
            safe_path(Path('.'), name)
            if digest(archive.read(name)) != sha:
                raise ValueError('Backup checksum mismatch')
    return len(manifest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    sub = parser.add_subparsers(dest='command', required=True)
    validate = sub.add_parser('validate'); validate.add_argument('--base')
    sub.add_parser('list')
    show = sub.add_parser('show'); show.add_argument('id'); show.add_argument('--history', action='store_true')
    for command in ('create', 'append'):
        edit = sub.add_parser(command); edit.add_argument('--file', type=Path, required=True); edit.add_argument('--reason', required=True)
    cap = sub.add_parser('capture'); cap.add_argument('file', type=Path)
    rep = sub.add_parser('report'); rep.add_argument('--output', type=Path)
    back = sub.add_parser('bundle'); back.add_argument('output', type=Path)
    verify = sub.add_parser('verify-bundle'); verify.add_argument('file', type=Path)
    args = parser.parse_args()
    if args.command in ('create', 'append'):
        value = append(args.root, json.loads(args.file.read_text(encoding='utf-8')), args.reason, create=args.command == 'create')
    elif args.command == 'capture':
        value = capture(args.root, args.file)
    elif args.command == 'report':
        rendered = report(args.root)
        if args.output:
            if args.output.resolve() != (args.root / 'INDEX.md').resolve():
                raise ValueError('Generated report target must be ledger INDEX.md')
            args.output.write_text(rendered, encoding='utf-8', newline='\n')
            value = {'report': str(args.output)}
        else:
            print(rendered); return
    elif args.command == 'bundle':
        value = {'files': bundle(args.root, args.output), 'backup': str(args.output)}
    elif args.command == 'verify-bundle':
        value = {'verified_files': verify_bundle(args.file)}
    else:
        events, latest = history(args.root)
        if args.command == 'validate':
            if args.base:
                check_git_history(args.root, args.base)
            value = {'records': len(latest), 'events': len(events), 'valid': True}
        elif args.command == 'list':
            value = [{'id': k, 'title': v['record']['title'], 'status': v['record']['status'],
                      'outcome': v['record']['outcome']} for k, v in latest.items()]
        else:
            value = [e for e in events if e['record']['id'] == args.id] if args.history else latest[args.id]['record']
    print(json.dumps(value, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

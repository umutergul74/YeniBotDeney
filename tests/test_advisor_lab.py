"""Isolated metadata persistence tests; no research imports or computations."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('advisor_lab', ROOT/'scripts/advisor_lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'research'
        self.record = json.loads((ROOT/'research/templates/experiment.json').read_text(encoding='utf-8'))

    def create(self):
        return lab.append(self.root, self.record, 'Planned synthetic fixture', create=True)

    def test_corrections_preserve_previous_bytes_and_history(self):
        self.create()
        path = self.root/'events/000001.json'
        before = path.read_bytes()
        updated = copy.deepcopy(self.record); updated['decision'] = 'Clarified question'
        lab.append(self.root, updated, 'Explain correction')
        events, latest = lab.history(self.root)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(len(events), 2)
        self.assertEqual(latest[updated['id']]['revision'], 2)
        self.assertEqual(events[1]['previous_sha256'], lab.digest(before))

    def test_duplicate_and_unknown_ids_cannot_overwrite(self):
        self.create()
        with self.assertRaises(ValueError): self.create()
        other = copy.deepcopy(self.record); other['id'] = 'exp-other'
        with self.assertRaises(ValueError): lab.append(self.root, other, 'unknown')
        self.assertEqual(len(lab.history(self.root)[0]), 1)

    def test_existing_writer_is_not_removed_or_bypassed(self):
        self.root.mkdir()
        lock = self.root/'.writer.lock'; lock.write_text('other writer')
        with self.assertRaises(FileExistsError): self.create()
        self.assertEqual(lock.read_text(), 'other writer')

    def test_chain_tamper_and_gaps_fail_closed(self):
        self.create()
        lab.append(self.root, self.record, 'Second observation')
        first = self.root/'events/000001.json'
        first.write_bytes(first.read_bytes() + b' ')
        with self.assertRaises(ValueError): lab.history(self.root)
        first.unlink()
        with self.assertRaises(ValueError): lab.history(self.root)

    def test_evidence_snapshot_survives_original_edit_and_detects_corruption(self):
        source = Path(self.tmp.name)/'review.md'; source.write_text('original evidence')
        evidence = lab.capture(self.root, source)
        self.record['evidence'] = [evidence]; self.create()
        source.write_text('later document')
        lab.history(self.root)
        (self.root/evidence['path']).write_text('corruption')
        with self.assertRaises(ValueError): lab.history(self.root)

    def test_plans_cannot_claim_results_and_metrics_need_split(self):
        bad = copy.deepcopy(self.record)
        bad['results'] = [{'metrics': {'F1': .1}}]
        with self.assertRaises(ValueError): lab.validate_record(bad)
        bad['status'] = 'running'
        with self.assertRaises(ValueError): lab.validate_record(bad)

    def test_lineage_and_terminal_state_cannot_be_reused_for_new_run(self):
        self.create()
        changed = copy.deepcopy(self.record); changed['parent_ids'] = ['missing-id']
        with self.assertRaises(ValueError): lab.append(self.root, changed, 'bad lineage')
        changed = copy.deepcopy(self.record); changed['status'] = 'abandoned'
        lab.append(self.root, changed, 'Not pursued')
        with self.assertRaises(ValueError): lab.append(self.root, self.record, 'Restart should get new ID')

    def test_paths_cannot_escape_ledger(self):
        for path in ('../outside', '/absolute', 'C:/outside', 'folder\\file'):
            with self.subTest(path=path), self.assertRaises(ValueError): lab.safe_path(self.root, path)

    def test_git_guard_rejects_rewrite_or_deletion_of_published_history(self):
        from unittest.mock import patch
        for status in ('M', 'D', 'R100'):
            with patch.object(lab.subprocess, 'check_output', return_value=status+'\tresearch/events/000001.json\n'):
                with self.assertRaises(ValueError): lab.check_git_history(ROOT/'research', 'HEAD')
        with patch.object(lab.subprocess, 'check_output', return_value='A\tresearch/events/000002.json\n'):
            lab.check_git_history(ROOT/'research', 'HEAD')

    def test_backup_roundtrip_and_refuses_overwrite(self):
        self.create()
        backup = Path(self.tmp.name)/'backup.zip'
        count = lab.bundle(self.root, backup)
        self.assertEqual(lab.verify_bundle(backup), count)
        with self.assertRaises(FileExistsError): lab.bundle(self.root, backup)
        restored = Path(self.tmp.name)/'restored'
        with zipfile.ZipFile(backup) as archive: archive.extractall(restored)
        self.assertEqual(lab.history(restored), lab.history(self.root))

    def test_modified_backup_fails_checksum(self):
        self.create()
        original = Path(self.tmp.name)/'backup.zip'; lab.bundle(self.root, original)
        altered = Path(self.tmp.name)/'altered.zip'
        with zipfile.ZipFile(original) as src, zipfile.ZipFile(altered, 'w') as dst:
            for name in src.namelist():
                dst.writestr(name, b'changed' if name.startswith('events/') else src.read(name))
        with self.assertRaises(ValueError): lab.verify_bundle(altered)

    def test_actual_ledger_report_and_no_fabricated_new_results(self):
        root = ROOT/'research'
        events, latest = lab.history(root)
        self.assertGreaterEqual(len(latest), 12)
        for id_ in ('exp-011-threshold-diagnostics', 'exp-012-barrier-diagnostics'):
            record = next(e['record'] for e in events if e['record']['id'] == id_)
            self.assertEqual(record['status'], 'planned')
            self.assertEqual(record['results'], [])
        self.assertEqual((root/'INDEX.md').read_text(encoding='utf-8'), lab.report(root))
        self.assertEqual(latest['exp-007-focal']['record']['results'][0]['metrics']['precision'], .412398)
        self.assertEqual(latest['exp-008-bce-pearson']['record']['results'][0]['metrics']['F1'], .132101)
        self.assertEqual(latest['exp-010-final']['record']['results'][0]['split'], 'test')


if __name__ == '__main__': unittest.main()

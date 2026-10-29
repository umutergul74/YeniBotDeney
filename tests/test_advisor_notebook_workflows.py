"""Notebook control-flow checks with fake commands; no Drive, ML or training."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def cells(name):
    return json.loads((ROOT / 'notebooks/workflows' / name).read_text(encoding='utf-8'))['cells']


class WorkflowTests(unittest.TestCase):
    def test_selective_environment_and_recovery_download_are_separate(self):
        notebook = cells('04_barrier_study.ipynb')
        environment = notebook[8]['source']
        support = next(c['source'] for c in notebook if 'def step_identity' in c['source'])
        self.assertIn('bootstrap_advisor.py', environment)
        self.assertNotIn('urlopen', environment)
        self.assertNotIn('def execute_step', environment)
        self.assertIn('urlopen', support)
        self.assertIn('sha256(helper_bytes)', support)
        self.assertNotIn('bootstrap_advisor.py', support)

    def test_all_cells_compile_and_pin_new_repository(self):
        for path in (ROOT / 'notebooks/workflows').glob('*.ipynb'):
            notebook = json.loads(path.read_text(encoding='utf-8'))
            code = [c['source'] for c in notebook['cells'] if c['cell_type'] == 'code']
            for source in code:
                compile(source, path.name, 'exec')
            joined = '\n'.join(code)
            self.assertIn('umutergul74/YeniBotDeney.git', joined)
            release = {
                '04_barrier_study.ipynb': 'advisor-selective-v1.1.0',
                '05_feature_comparison.ipynb': 'advisor-feature-comparison-v1.0.0',
                '06_learning_rate.ipynb': 'advisor-checkpoint-selection-v1.0.0',
            }.get(path.name, 'advisor-notebooks-v2.1.0')
            self.assertIn(release, joined)
            self.assertNotIn('import torch', joined)
            self.assertNotIn('evaluate-test', joined)
            self.assertTrue(all(not c.get('outputs') for c in notebook['cells']))

    def test_recovery_prepares_both_scopes_in_order_without_training(self):
        notebook = cells('01_recover_data.ipynb')
        context = {}
        exec(notebook[2]['source'], context)
        calls = []
        context['execute_step'] = lambda action: calls.append((context['PHASE'], action))
        for c in notebook:
            if c['cell_type'] == 'code' and ('for PHASE in' in c['source'] or "if MODE == 'research':" in c['source']):
                exec(c['source'], context)
        self.assertEqual(calls, [('basic', 'prepare'), ('full', 'prepare')])
        self.assertFalse(context['ALLOW_TRAINING'])

    def test_research_selects_only_requested_phase_and_requires_opt_in(self):
        notebook = cells('02_research.ipynb')
        train = next(c['source'] for c in notebook if c['cell_type'] == 'code' and c['source'].startswith('if ALLOW_TRAINING:'))
        expected = {'basic': ['A'], 'full': ['B', 'C', 'D'], 'wavelet': ['W_ON'],
                    'loss': ['L_WEIGHTED_BCE', 'L_FOCAL', 'L_BCE_PEARSON', 'L_FOCAL_PEARSON']}
        for phase, experiments in expected.items():
            context = {}
            exec(notebook[2]['source'].replace("PHASE = 'basic'", f'PHASE = {phase!r}'), context)
            self.assertEqual(context['EXPERIMENTS'], experiments)
            calls = []
            context['execute_step'] = calls.append
            exec(train, context)
            self.assertEqual(calls, [])
            context['ALLOW_TRAINING'] = True
            exec(train, context)
            self.assertEqual(calls, ['train'])

    def test_archive_has_no_prepare_or_train_commands(self):
        notebook = cells('03_audit_archive.ipynb')
        source = '\n'.join(c['source'] for c in notebook if c['cell_type'] == 'code')
        context = {}
        exec(notebook[2]['source'], context)
        self.assertEqual((context['MODE'], context['PHASE']), ('archive', 'final'))
        self.assertIn("execute_step('audit-final')", source)
        for action in ('train', 'prepare', 'evaluate-test'):
            self.assertNotIn(f"execute_step('{action}')", source)


if __name__ == '__main__':
    unittest.main()

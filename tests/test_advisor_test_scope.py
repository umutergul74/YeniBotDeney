"""Fast stdlib-only checks for scope routing; no scientific imports or training."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('advisor_test_scope', ROOT/'scripts/advisor_test_scope.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScopeTests(unittest.TestCase):
    def test_docs_need_no_pytest(self):
        plan = module.classify(['AGENTS.md', 'README.md', 'docs/advisor-notebooks-v2.md'])
        self.assertEqual(plan['scope'], 'docs')
        self.assertEqual(plan['tests'], [])

    def test_feature_report_views_are_focused_but_engine_changes_are_full(self):
        paths = ['yenibot/experiment/advisor_feature_report.py',
                 'scripts/build_advisor_feature_notebook.py',
                 'notebooks/workflows/05_feature_comparison.ipynb']
        plan = module.classify(paths)
        self.assertEqual(plan['scope'], 'targeted')
        self.assertIn('tests/test_advisor_feature_report.py', plan['tests'])
        self.assertEqual(module.classify(paths + ['yenibot/experiment/advisor_feature_comparison.py'])['scope'], 'full')

    def test_bootstrap_and_backend_regression_select_only_related_tests(self):
        plan = module.classify(['scripts/bootstrap_advisor.py', 'scripts/advisor_workspace.py'])
        self.assertEqual(plan['scope'], 'targeted')
        self.assertEqual(len(plan['tests']), 3)
        self.assertTrue(all('::' in target for target in plan['tests']))

    def test_runtime_environment_only_is_targeted_but_identity_changes_are_full(self):
        self.assertEqual(module.classify([module.RUNTIME], runtime_environment_only=True)['scope'], 'targeted')
        self.assertEqual(module.classify([module.RUNTIME])['scope'], 'full')
        before = 'def clean_environment():\n return 1\ndef freeze():\n return 2\n'
        self.assertTrue(module.only_environment_changed(before, before.replace('return 1', 'return 3')))
        self.assertFalse(module.only_environment_changed(before, before.replace('return 2', 'return 3')))

    def test_scientific_or_unmapped_code_preserves_full_gate(self):
        for path in ['yenibot/training/advisor.py', 'yenibot/experiment/advisor_storage.py',
                     'yenibot/experiment/advisor_workspace.py', 'yenibot/features/builder.py',
                     'configs/advisor_ablation.yaml', 'requirements/advisor-linux-py313.lock',
                     'tests/conftest.py', 'scripts/unmapped.py',
                     'notebooks/99_advisor_unknown.ipynb',
                     'notebooks/archive/advisor_v1/06_advisor_ablation_colab.ipynb']:
            with self.subTest(path=path):
                self.assertEqual(module.classify([path, 'README.md'])['scope'], 'full')

    def test_policy_changes_need_only_stdlib_checks(self):
        plan = module.classify(list(module.POLICY)+['AGENTS.md'])
        self.assertEqual(plan['scope'], 'policy')
        self.assertEqual(plan['runner'], 'unittest')

    def test_whole_module_subsumes_individual_nodes(self):
        plan = module.classify([module.WORKSPACE_TEST, 'scripts/bootstrap_advisor.py'])
        self.assertEqual(plan['tests'], [module.WORKSPACE_TEST])

    def test_explicit_full_and_mixed_scientific_changes_cannot_downgrade(self):
        self.assertEqual(module.classify(['README.md'], force_full=True)['scope'], 'full')
        plan = module.classify(list(module.POLICY)+['yenibot/training/advisor_stages.py'])
        self.assertEqual(plan['scope'], 'full')
        self.assertEqual(plan['tests'], [])

    def test_missing_diff_base_defaults_to_full(self):
        for base in ['', '0'*40]:
            self.assertEqual(module.make_plan(base, 'HEAD', False)['scope'], 'full')

    def test_unavailable_diff_base_retains_full_gate(self):
        from unittest.mock import patch
        import subprocess
        with patch.object(module, 'git', side_effect=subprocess.CalledProcessError(1, 'git')):
            self.assertEqual(module.make_plan('missing', 'HEAD', False)['scope'], 'full')

    def test_notebook_changes_require_generation_check(self):
        plan = module.classify(['notebooks/06_advisor_ablation_colab.ipynb'])
        self.assertEqual(plan['scope'], 'targeted')
        self.assertTrue(plan['notebook_check'])

    def test_workflow_notebooks_have_bounded_regressions(self):
        plan = module.classify(['scripts/build_advisor_notebooks_v2.py',
                                'notebooks/workflows/02_research.ipynb'])
        self.assertEqual(plan['scope'], 'targeted')
        self.assertEqual(len(plan['tests']), 2)
        self.assertIn('tests/test_advisor_notebook_workflows.py', plan['tests'])
        self.assertTrue(plan['notebook_check'])

    def test_selective_notebook_is_targeted_but_runtime_identity_stays_full(self):
        paths = ['notebooks/workflows/04_barrier_study.ipynb']
        plan = module.classify(paths)
        self.assertEqual(plan['scope'], 'targeted')
        self.assertTrue(plan['notebook_check'])
        self.assertIn('tests/test_advisor_a100.py', plan['tests'])
        self.assertIn('tests/test_advisor_notebook_workflows.py', plan['tests'])
        self.assertEqual(module.classify(paths + [module.RUNTIME])['scope'], 'full')

    def test_ledger_metadata_needs_no_ml_but_science_still_requires_full(self):
        paths = ['scripts/advisor_lab.py', 'research/events/000001.json',
                 'research/INDEX.md', 'tests/test_advisor_lab.py']
        plan = module.classify(paths + list(module.POLICY))
        self.assertEqual(plan['scope'], 'metadata')
        self.assertEqual(plan['runner'], 'unittest')
        self.assertEqual(set(plan['tests']), {module.LAB_TEST, module.POLICY_TEST})
        self.assertEqual(module.classify(paths + ['yenibot/labeling/triple_barrier.py'])['scope'], 'full')
        self.assertEqual(module.classify(['research/new_training.py'])['scope'], 'full')


if __name__ == '__main__':
    unittest.main()

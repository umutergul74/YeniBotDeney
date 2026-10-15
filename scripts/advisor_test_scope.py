"""Choose the smallest safe advisor check scope from the complete Git diff.

Unknown code and scientific/artifact changes fail closed to the full suite.
This utility uses only the standard library; docs/policy checks need no ML install.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess
import sys

WORKSPACE_TEST = 'tests/test_advisor_workspace.py'
POLICY_TEST = 'tests/test_advisor_test_scope.py'
LAB_TEST = 'tests/test_advisor_lab.py'
RUNTIME = 'yenibot/experiment/advisor_runtime.py'
POLICY = {'scripts/advisor_test_scope.py', POLICY_TEST, '.gitignore', '.gitattributes',
          '.github/workflows/advisor-reproducibility.yml'}
FOCUSED = {
    'scripts/bootstrap_advisor.py': [
        'test_bootstrap_uses_hash_lock_and_never_host_pip_install',
        'test_bootstrap_keeps_all_uv_state_off_drive'],
    'scripts/advisor_workspace.py': [
        'test_launcher_overrides_colab_backend_before_package_import'],
    'scripts/build_advisor_notebooks_v2.py': [
        'test_all_notebooks_are_thin_safe_and_archive_does_not_execute_test'],
    'scripts/build_advisor_notebook.py': [
        'test_all_notebooks_are_thin_safe_and_archive_does_not_execute_test'],
    'scripts/build_advisor_stage_notebooks.py': [
        'test_all_notebooks_are_thin_safe_and_archive_does_not_execute_test'],
    'scripts/build_advisor_final_notebook.py': [
        'test_all_notebooks_are_thin_safe_and_archive_does_not_execute_test'],
}
ADVISOR_NOTEBOOKS = {
    'notebooks/' + name for name in [
        '06_advisor_ablation_colab.ipynb', '07_advisor_full_features_colab.ipynb',
        '08_advisor_wavelet_colab.ipynb', '09_advisor_losses_colab.ipynb',
        '10_advisor_final_test_colab.ipynb']}
ENVIRONMENT_TESTS = ['test_child_environment_does_not_inherit_host_python_paths',
                     'test_launcher_overrides_colab_backend_before_package_import']


def only_environment_changed(before: str, after: str) -> bool:
    def remaining(source):
        tree = ast.parse(source)
        found = any(isinstance(n, ast.FunctionDef) and n.name == 'clean_environment'
                    for n in tree.body)
        tree.body = [n for n in tree.body if not
                     (isinstance(n, ast.FunctionDef) and n.name == 'clean_environment')]
        return found, ast.dump(tree, include_attributes=False)
    old_found, old = remaining(before)
    new_found, new = remaining(after)
    return old_found and new_found and old == new


def classify(paths: list[str], *, runtime_environment_only=False, force_full=False) -> dict:
    targets, full_reasons = set(), []
    notebook_check = False
    for path in sorted(set(paths)):
        if path in POLICY:
            targets.add(POLICY_TEST)
        elif path == 'scripts/advisor_lab.py' or (
                path.startswith('research/') and path.endswith(('.md', '.json', '.csv', '.txt'))):
            targets.add(LAB_TEST)
        elif path in FOCUSED:
            targets.update(WORKSPACE_TEST + '::' + name for name in FOCUSED[path])
            if path == 'scripts/build_advisor_notebooks_v2.py':
                targets.add('tests/test_advisor_notebook_workflows.py')
            notebook_check |= 'build_advisor' in path
        elif path == RUNTIME and runtime_environment_only:
            targets.update(WORKSPACE_TEST + '::' + name for name in ENVIRONMENT_TESTS)
        elif path in {'notebooks/workflows/01_recover_data.ipynb',
                      'notebooks/workflows/02_research.ipynb',
                      'notebooks/workflows/03_audit_archive.ipynb'}:
            notebook_check = True
            targets.add('tests/test_advisor_notebook_workflows.py')
        elif path in ADVISOR_NOTEBOOKS:
            notebook_check = True
            targets.add(WORKSPACE_TEST + '::test_all_notebooks_are_thin_safe_and_archive_does_not_execute_test')
        elif path.startswith('tests/test_') and path.endswith('.py'):
            targets.add(path)
        elif path.endswith(('.md', '.rst')) or path in {'LICENSE', 'LICENSE.txt'}:
            pass
        else:
            full_reasons.append(path)
    if force_full or full_reasons:
        scope = 'full'
        targets = set()
    elif not targets:
        scope = 'docs'
    elif targets == {POLICY_TEST}:
        scope = 'policy'
    elif targets <= {POLICY_TEST, LAB_TEST}:
        scope = 'metadata'
    else:
        scope = 'targeted'
    # A selected whole module subsumes its selected individual tests.
    targets = {t for t in targets if '::' not in t or t.split('::')[0] not in targets}
    return {'scope': scope, 'runner': 'unittest' if scope in {'policy', 'metadata'} else 'pytest',
            'tests': sorted(targets), 'changed_paths': sorted(set(paths)),
            'notebook_check': notebook_check,
            'reason': 'explicit full request' if force_full else
                      ('scientific/artifact or unmapped code: ' + ', '.join(full_reasons)
                       if full_reasons else 'smallest mapped scope')}


def git(*args):
    return subprocess.check_output(['git', *args], text=True, encoding='utf-8',
                                   stderr=subprocess.PIPE).strip()


def make_plan(base, head, force_full):
    if not base or set(base) == {'0'}:
        result = classify([], force_full=True)
        result['reason'] = 'missing trusted diff base'
        result.update(base=None, head=head)
        return result
    try:
        git('rev-parse', '--verify', base + '^{commit}')
    except subprocess.CalledProcessError:
        result = classify([], force_full=True)
        result.update(base=None, head=head, reason='diff base is unavailable; full required')
        return result
    paths = git('diff', '--name-only', '--no-renames', base, head).splitlines()
    environment_only = False
    if RUNTIME in paths:
        try:
            environment_only = only_environment_changed(
                git('show', base + ':' + RUNTIME), git('show', head + ':' + RUNTIME))
        except (subprocess.CalledProcessError, SyntaxError):
            pass
    result = classify(paths, runtime_environment_only=environment_only, force_full=force_full)
    result.update(base=base, head=head)
    return result


def execute(plan, python):
    if plan['scope'] == 'docs':
        return
    if plan['scope'] in {'policy', 'metadata'}:
        patterns = [Path(target).name for target in plan['tests']]
        code = ('import unittest,sys; '
                f'suite=unittest.TestSuite(unittest.defaultTestLoader.discover("tests",pattern=p) for p in {patterns!r}); '
                'result=unittest.TextTestRunner(verbosity=1).run(suite); sys.exit(not result.wasSuccessful())')
        command = [python, '-c', code]
    else:
        command = [python, '-m', 'pytest', '-q', '--tb=short',
                   '--junitxml=reports/advisor-tests.xml', *plan['tests']]
    log = Path('reports/advisor-tests.log')
    log.parent.mkdir(exist_ok=True)
    with log.open('w', encoding='utf-8') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
    print('\n'.join(lines[-100:] if result.returncode else lines[-12:]))
    if result.returncode:
        raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='HEAD^')
    parser.add_argument('--head', default='HEAD')
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--output', type=Path, default=Path('reports/test-plan.json'))
    parser.add_argument('--github-output', type=Path)
    parser.add_argument('--run', type=Path)
    parser.add_argument('--python', default=sys.executable)
    args = parser.parse_args()
    if args.run:
        execute(json.loads(args.run.read_text(encoding='utf-8')), args.python)
        return
    plan = make_plan(args.base, args.head, args.full)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(plan, indent=2))
    if plan['base']:
        subprocess.run(['git', 'diff', '--check', plan['base'], plan['head']], check=True)
    if args.github_output:
        with args.github_output.open('a', encoding='utf-8') as stream:
            stream.write('scope=' + plan['scope'] + '\n')
            stream.write('notebooks=' + str(plan['notebook_check']).lower() + '\n')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        with open(summary, 'a', encoding='utf-8') as stream:
            stream.write('## Check scope: ' + plan['scope'] + '\n\n' + plan['reason'] +
                         '\n\nSelected tests: ' + repr(plan['tests']) + '\n')


if __name__ == '__main__':
    main()

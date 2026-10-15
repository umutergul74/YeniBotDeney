# Scope-based verification

Standing user preference, 15 October 2026: never run 200+ tests for each minor fix.
This applies to local work and CI, including future sessions.

| Change | Default verification |
|---|---|
| Documentation/instructions | Diff checks; no ML install or pytest |
| CI/test-selection policy | Fast stdlib routing tests; no ML install |
| Research ledger CLI, records and review-document copies | Stdlib metadata persistence/history tests; no ML install or training |
| Bootstrap | Two bootstrap regressions |
| Notebook launcher/backend | Parameterized launcher import regression |
| Notebook generator/cells | Notebook structure/syntax and regeneration check |
| Runtime environment only | Environment and launcher regressions |
| Runtime identity/frozen artifacts, data/labels/splits, scientific config, dependencies | Full suite once after stabilization |
| Unmapped code | Conservative full suite; add a justified focused mapping when appropriate |

The runtime environment exception is checked by comparing ASTs: changes outside
`clean_environment` retain full coverage. All changed paths in a push are combined;
a docs or policy change cannot downgrade a scientific change. An unavailable diff
base defaults to full. Whole-module selections subsume their individual nodes.

The independent `scripts/advisor_lab.py` and `research/` tree store only metadata,
review-document copies and unexecuted plans. They cannot run training, labeling,
splits or metric computation. Their explicit `metadata` scope verifies persistence,
hash chains, evidence, backups and generated catalog; CI also rejects edits/deletions
of published ledger events/sources. `.gitignore` is repository policy. Any scientific
code/config/lock changes in the same push still select full coverage.

Inspect a plan without executing tests:

```powershell
python scripts/advisor_test_scope.py --base HEAD^ --head HEAD
```

CI records `reports/test-plan.json` and its reason in the job summary, installs the
locked scientific environment only for ML test scopes and runs the selected group
once. The workflow keeps an explicit `full` manual input. Existing correctness
tests, thresholds, held-out periods and frozen research evidence are unchanged.

Do not run local focused tests and then repeat the same unchanged group in CI
merely by habit. Prefer one verification location. A local check of CI routing
plus CI's execution of the routing policy is acceptable when changing the runner
itself; it does not justify a full ML regression run. After a failure, rerun the
failed/affected group first. Preserve valid prior evidence after docs-only edits.

The original `yeniBot` checkout has pre-existing local work. Its AGENTS instructions
and the user's global instructions carry this preference; its dirty CI file is
not overwritten or committed by this isolated advisor task.

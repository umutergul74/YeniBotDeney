# Independent advisor research workspace

- This repository is independent from `../yeniBot`. Never merge main or copy its
  working changes into this workspace implicitly.
- Preserve the frozen advisor engine at baseline 741d1d4 and all old evidence.
  New notebook infrastructure lives in `yenibot/experiment/advisor_*.py`.
- Read `docs/advisor-notebooks-v2.md` before changing orchestration. Old
  `colab_v1` and `evidence/` are read-only research evidence.
- Never fit, select policies, retune thresholds, or run new comparisons on the
  seen September 2026 final test. Notebook 10 audits existing files only.
- Never overwrite mismatching prepared data, checkpoints, locks or manifests.
- Start with git status and targeted rg. Preserve user changes. Use the existing
  environment; no global package upgrades. No real training for verification.
- Follow `docs/test-budget.md` and `scripts/advisor_test_scope.py`. Small bootstrap,
  launcher/backend/environment and notebook fixes use mapped regressions only;
  they do not automatically require a full training/orchestration gate.
- Full checks remain available for scientific/artifact/dependency or broad changes,
  explicit user requests and unknown code. Never weaken research thresholds.
- Keep the notebooks thin. Python host packages must not enter research processes.
- Independent reviewers are read-only and bounded; default to one agent.
- This is a cumulative experiment laboratory. Start research planning from
  `research/README.md` and `research/INDEX.md`, not from notebook numbering.
  Preserve unsuccessful, failed and abandoned experiments as well as successes.
  Record questions, parent experiments, data/label/split identity, selection rules,
  evidence, results and decisions. Append corrections; never rewrite published
  `research/events/` or `research/sources/`. New runs/methods get new IDs.
- A proposal is not authorization to execute it. The threshold/barrier diagnostic
  proposals were executed on explicit user request on 2026-10-15; results are in
  `research/analyses/diagnostics-20261015/REPORT.md`. No deployment threshold or
  barrier was selected. Further proposals require execution authorization. Notebook changes
  do not implicitly authorize training or analysis.
- Routine task commits/pushes are authorized, but do not move frozen release tags
  or merge into main/advisor baseline without a separate explicit request.

## Persistent test-budget preference (2026-10-15)

Small bootstrap/backend/launcher/notebook fixes use related regressions only;
do not interpret them as broad orchestration changes. Follow the global standing
preference and, in the advisor workspace, `docs/test-budget.md` for scope routing.

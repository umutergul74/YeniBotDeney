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
- Use scope-based tests: affected group first; one full CI gate for stabilized
  training/orchestration changes. Do not weaken tests or research thresholds.
- Keep the notebooks thin. Python host packages must not enter research processes.
- Independent reviewers are read-only and bounded; default to one agent.
- Routine task commits/pushes are authorized, but do not move frozen release tags
  or merge into main/advisor baseline without a separate explicit request.

# ENG-0004 — A6 threshold and matched-coverage diagnosis

- Status: verified, 2026-10-28. Base 30a6676; branch codex/notebook-setup-separation.
- Authorization: user requested detailed threshold comparisons and the proposed equal-coverage analysis.
- Scope: research/analyses/a6-thresholds-20261028, research/INDEX.md, new event 000046 and three evidence snapshots, this task record. Preserve unrelated Engineering OS changes.
- Acceptance: 114 paired prediction identities; fixed-threshold, global matched-coverage and within-run top-k diagnostics; explain seed versus period differences without changing training or selecting a threshold.
- Checks: analyze.py assertions passed (paired identities, finite probabilities, 0.5 agrees with previous independently verified counts, monotonic signal counts, top-k count). No tied top-k boundaries. Ledger valid: 28 records/46 events. Both plots visually inspected; threshold plot encoding/titles repaired and regenerated from saved numerical outputs only.
- Independent review not required: descriptive existing-data analysis; no training/scientific protocol or permission boundary change. No full suite, training or final test.
- Outcome: [report](../../research/analyses/a6-thresholds-20261028/REPORT.md). No consistent precision gain at equal coverage; last-fold score-scale issue differs from fold28 ranking failure.
- Limits: reused validation, overlapping folds/seeds, retrospective top-k not a live signal rule; sparse high-threshold support.
- Next proposed only: existing-feature train/validation distribution diagnosis across periods. Token counts unavailable; no PR or locally executed CI.

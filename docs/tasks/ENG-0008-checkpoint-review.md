# ENG-0008 — Completed Colab checkpoint comparison review

- Status: verified; 2026-10-30.
- User request: inspect completed experiment on Drive. Source commit 2f7e2908c585a05ed616b28e42e23839def5a8f7.
- Scope: research/analyses/checkpoint-selection-20261030, new ledger event/source, generated research/INDEX.md, this task.
- Acceptance: verify 114 runs, frozen selections, paired predictions and reported counts; explain result without new training/test selection.
- Evidence: [report](../../research/analyses/checkpoint-selection-20261030/REPORT.md), checks.json and reproducible verify.py alongside it.
- Checks: 798 nonweight hashes, 684 decision rows, 114 minBCE/maxAP epoch pairs and run signatures passed. AP/BCE recomputed from predictions. No pytest: no training code changed.
- Limitations: weights excluded from ZIP, no independent weight/Drive remount verification. Historical validation, correlated folds/seeds, common BCE stopping.
- Outcome: AP selection advantage did not transfer; preserve BCE control, no automatic final-test progression.
- Independent agent: not required for read-only result review; no scientific implementation or boundary changed.
- Unrelated dirty files preserved. No new training, method or final test.
- Token usage unavailable.

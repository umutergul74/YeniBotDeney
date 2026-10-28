# ENG-0005 — A6 period diagnosis

- Verified 2026-10-28; base 039e595, codex/notebook-setup-separation.
- User authorized previous proposed train/validation feature and label diagnosis.
- Scope: research/analyses/a6-period-diagnosis-20261028, generated research/INDEX.md, new event000047 and evidence snapshots, this task. Original data cached in ignored reports; no training/config changes.
- Acceptance: verify frozen frame and 114 prediction identities; compare six features and endpoint labels across all38 folds with fold28/37 focus; distinguish evidence from hypotheses. Completed.
- Checks: analyze.py hash/hourly/frozen splitter+dataset/target counts/alignment assertions passed; numerical summaries exported; one plot visually inspected. Added constant-reference calculations and six existing epoch-log comparisons executed separately without repeating full data checks. Ledger valid: 29 records/47 events.
- Findings: larger marginal shift in fold37 despite better ranking; volatility-label relationship weakens in fold28; min-BCE epoch1 loses AP relative to later logged epochs. No causal or test-success claim.
- Independent review not required: read-only descriptive analysis, unchanged scientific protocol. No suite, training, inference or final test.
- Next: all-run BCE/AP epoch divergence audit, proposed only. Unrelated dirty Engineering OS files preserved. Token counts unavailable; no PR/local CI.

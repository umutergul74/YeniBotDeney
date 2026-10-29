# ENG-0006 — Existing-run comprehensive diagnosis

- Completed 2026-10-29; analysis began 2026-10-28. Base c8e4608, codex/notebook-setup-separation.
- User authorized all existing-data diagnostics across periods; no new training/model selection or final test.
- Scope: research/analyses/comprehensive-diagnosis-20261028, research/INDEX.md, new event000048 and source snapshots, this task. Preserve unrelated Engineering OS work.
- Acceptance: all684 comparable runs/38 folds/3 seeds, epoch divergence, thresholds, equal coverage, temporal/seed sensitivity and all37 existing inputs. Completed; two existing charts only.
- Actual checks: 684 unique runs; matched predictions/labels/timestamps; min-BCE records and AP recomputation. One top20 boundary tie detected and documented; equal-label tie gives identical precision bounds. Main analysis passed after explicit tie handling.
- Independent Sol/medium review PASS for main684 analysis: summary, top-k, identities, hashes, boundaries and zero recorded test evaluations. Full37 follow-up review unavailable due usage limit; not claimed passed.
- Full37 local checks: 1406 unique pairs, frozen frame hash, 228 shared-feature results match previous verified calculations; 152 zero-IQR sparse cases explicitly undefined, activation rates valid. No imputations or feature changes. Undefined associations:63.
- No broad test suite or training. Two plots visually checked. Ledger29/47 before append; final validation recorded by command output. Raw files remain ignored.
- Result: report in analysis folder; seed stability and ranking quality differ, BCE/AP optimum mismatch widespread; no general causal explanation established. Sparse whale flags are evidence for further inspection, not an authorized removal.
- Usage counts unavailable; reviewer limit disclosed. No PR or locally run CI. Scoped commit/push uses standing user authorization.

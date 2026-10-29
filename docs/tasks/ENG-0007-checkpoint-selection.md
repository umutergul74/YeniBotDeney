# ENG-0007 — Controlled BCE/AP checkpoint comparison

- Date: 2026-10-29. Base 3a2ea60; branch codex/notebook-setup-separation. Status: scoped verification passed; Colab execution pending.
- User approved preceding proposal: A6/LR0.001, minBCE versus maxAP checkpoint selection with chronological validation selection/assessment split, existing notebook reuse.
- Scope: new advisor_checkpoint_selection module/launcher/test; existing learning-rate notebook builder/current06 and its regeneration test; notebooks README; experiment031 plan/new ledger record; this task.
- Frozen engine, feature/label generation, dependencies, old experiment artifacts and unrelated Engineering OS files remain unchanged.
- Acceptance: train5040, selection528/gap24/assessment528,465 targets each; train-only scaler; freeze choices before assessment; common selection-BCE stopping; persist both checkpoints/predictions; guarded resume and hashes; fixed/selection-derived thresholds only; no final test.
- Existing notebook06 reused; old LR release retained. New root checkpoint_selection_v1/a6_bce_ap_a100_001; new immutable release advisor-checkpoint-selection-v1.0.0.
- Independent review found missing exact source runtime comparison; fixed and CUDA-build/cuDNN mismatch regression added. Reviewer found no remaining code issue, verdict pending test evidence. Seed/fold also included in run signature.
- Verification: initial root-wide pytest collection hit vendored third-party test data under ignored output before project execution. Full project tests were then explicitly scoped to tests/. Logs/XML in ignored reports/checkpoint-selection-20261029/. Real research training and Colab execution not run.
- Full project run:361 passed,2 skipped,14 subtests passed,2 failures in1212s. Notebook release-mapping failure fixed by adding exact new release (no assertion weakened). Remaining wavelet failure was missing local PyWavelets; new experiment does not enable wavelet.
- Affected rerun: new checkpoint module plus notebook pin check,8 passed in28.75s. Independent Sol/medium review final PASS after runtime guard and per-seed/fold signature fix; no tests duplicated by reviewer.
- Wavelet-only retry:1 passed in10.68s using existing output/advisor_experiments/stage_validation_deps PyWavelets1.8.0 appended to that subprocess path; no install/global changes. This local check is not Colab's locked runtime verification. Both original failures resolved with bounded retries; full suite not repeated.
- Ledger validation:31 records/49 events passed. Source plan captured immutably. Publish immutable advisor-checkpoint-selection-v1.0.0 after final checks; no Colab training claim.
- No PR; usage telemetry unavailable. Standing important-change push authorization applies. New split is an explicit experiment, not a rewrite of old results; historical validation remains seen.

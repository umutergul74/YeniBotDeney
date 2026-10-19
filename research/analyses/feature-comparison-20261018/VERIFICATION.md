# Feature-comparison verification — 19 October 2026

Scope: finish the interrupted verification without rerunning passing tests.
No research training or final-test evaluation was performed.

## Interrupted run and recovery

The original `pytest tests -q` log contains 274 outcomes: 272 passes and
2 failures, then ends at 80%. Collection of the unchanged 341-test suite
mapped these outcomes in order; the remaining 67 tests were selected explicitly.
The new feature-comparison tests are within the previously passed section.

The two failures were:

- Notebook release assertion: the test assumed every notebook except 04 used
  the old notebook release. It now explicitly requires
  `advisor-feature-comparison-v1.0.0` for 05, preserving all other assertions.
- Wavelet causality check: the local interpreter could not import PyWavelets.
  The existing `output/advisor_experiments/stage_validation_deps` package was
  added only to that verification process. No package was installed or upgraded,
  and the frozen dependency lock and scientific engine were unchanged.

Both failed checks passed after these corrections (2 passed).
The remaining batch finished with 65 passed / 2 skipped (PyWavelets unavailable).
Only those two skipped wavelet checks were then run with the same existing
local package: 2 passed. Combined evidence: 272 previously passed + 2 corrected
failures + 65 remaining passes + 2 resolved skips = all 341 collected checks
covered by passing results. This is resumed verification, not a new single full run.

## Evidence and limitations

Ignored logs and JUnit files: `reports/feature-comparison-20261018/`:
`tests-project.log`, `collected.txt`, `resume-selection.json`,
`failed-recheck.log`, `fixed-recheck.log`, `fixed-recheck.xml`,
`remaining.log`, `remaining.xml`, `skipped-recheck.log`, `skipped-recheck.xml`.

Local verification uses Windows Python 3.13.7 / Torch 2.7.1+cu118;
the existing wavelet package reports PyWavelets 1.8.0. This is not a run of
the locked Colab Linux Python 3.13.15 / Torch 2.11.0 environment.
A100 execution, real Drive reconstruction and post-remount persistence
remain to be checked by the actual Colab run. No claim of cross-platform
numerical equivalence is made.

The research ledger validates: 21 records / 36 events. The experiment stays
planned; successful software checks are not experimental model results.

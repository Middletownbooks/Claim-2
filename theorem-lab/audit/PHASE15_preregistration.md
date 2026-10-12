# Phase 15 — Pre-registration of the extended T experiment

Written and committed **before** the extended run is executed and before any of its labels
are read. Provenance of the range: HUMAN/auditor-supplied, derived from the Phase 13 proof.

* **Command**: `python3 lab.py --oracle real --control C --k-train 92 --k-valid 112
  --k-test 140 --r-train 2 --r-valid 3 --r-test 4 --d-train 2 --d-valid 3 --d-test 4
  --budget 300000 --out runs/p15-T-extended`
  (the E grid is shrunk to a stub because this run is about the k-axis; its E result is not
  to be interpreted.)
* **Why 92**: Phase 13 predicts period `λ(m)` in `k`; `max_{m≤48} λ(m) = λ(47) = 46`;
  `fit_sequence` requires two observed copies, so `k_train ≥ 92`. 92 is the *minimum*
  sufficient value, chosen deliberately rather than a comfortable margin, so that the test
  is not made easy.
* **Held-out extrapolation region**: `k ∈ [113,140]` for `m ≤ 36` and `k ∈ [93,140]` for
  `m ∈ [37,48]`, entered only after `T_freeze.json` and `T_forecasts.json` are written.
* **Predictions registered in advance** (to be scored, not adjusted):
  1. The `cycles` model attains 0 errors on train, calibration, validation **and** final,
     and T becomes `UNREFUTED_ON_TESTED_DATA` for the first time on the real oracle.
  2. Per row, the fitted period equals `λ(m)` for squarefree `m`; for non-squarefree `m` the
     fitted description is prefix `[True]` then a constant-false block of length 1
     (`T(m,1)` true, everything after false).
  3. Every *arithmetic-rule* model (atoms, Boolean combinations, quotient tables) remains
     REFUTED, because the feature vocabulary cannot express `λ(m) | k−1` for
     `λ(m) ∉ {1,…,6}` and cannot express squarefreeness.
  4. Consequently the T result, if it appears, is a **memorised per-row code**, not a law —
     the same status as the E result, and explicitly weaker than the classical theorem.
* **Failure condition**: if (1) holds but (3) fails — i.e. some arithmetic rule survives —
  that is a materially stronger result than expected and must be reported as such,
  including the rule.
* **No re-tuning**: if the run fails, the failure is reported. The range is not to be
  enlarged until the desired outcome appears.

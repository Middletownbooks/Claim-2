# Pre-registration — cross-object holdout experiment

Written and committed **before** the experiment runs and before any held-out
oracle answer is read.

## The capability under test

Every model the laboratory has produced so far is indexed by object: fitted on
modulus `m`, it says nothing about modulus `m+1`. Phase 0 measured that ceiling
directly — fitted on `m ≤ 30`, no model in the laboratory's language beat the
majority-class baseline on unseen moduli (0.90823 vs 0.90823; 0.90873 even when
chosen by cheating on the holdout).

This experiment tests the missing step:

> per-object invariant → **general law across objects**

## Task

Family `U`: `U(m,k) ⟺ ∀x ∈ (ℤ/m)ˣ, x^k = x`. For each object `m` the row is
periodic in `k`; call that observed period `f(m)`.

* **Training objects:** `m ∈ [1,30]`, observed for `k ∈ [1,60]`
  (`60 ≥ 2·max_{m≤30} f(m)`, so every training period is fittable with the two
  observed copies the sequence fitter requires).
* **Held-out objects:** `m ∈ [31,48]`, never observed during fitting.
* **Held-out columns for scoring:** `k ∈ [1,140]`.

## What the learner may use

Oracle answers for training objects only, and a declared hypothesis language:

1. **Composition.** For an object `m` admitting a split `m = a·b` with
   `a,b > 1` and `gcd(a,b) = 1`: `f(m) = op(f(a), f(b))` for
   `op ∈ {lcm, gcd, mul, add, max, min, left, right}`. The op is chosen on
   training objects only.
2. **Base case.** For an object admitting no such split, a decision list over
   conditions `{n mod 2 = 0, n mod 4 = 0, n mod 8 = 0, otherwise}` with values
   from the expression grammar `{n-1, n, n+1, n-2, n//2, n//4, n//8,
   n - n//spf(n), (n-1)//2}`, where `spf(n)` is the smallest divisor > 1.

**Declared gift (HUMAN_SUPPLIED).** The coprime-split operator and `spf` give
the learner structural access to `m` that the Phase-0 feature vocabulary lacked.
Without something of this kind no multiplicative law is expressible at all, so
this experiment tests *whether the composition law can be discovered from data*,
not whether the notion of multiplicativity can be invented. That distinction is
the same one recorded for the `d_train = 92` window in the previous phase, and
it must be stated in any summary of the result.

## Protocol

Fit on training objects; write forecasts for every held-out `(m,k)` and hash
them; only then query the oracle for held-out objects. Post-final replay must
reproduce the frozen forecasts exactly.

## Pre-registered predictions

* **P1.** The composition search selects `lcm`. Any other winner is a failure of
  the experiment's premise and is reported as such.
* **P2 (composable objects).** For held-out `m` with a coprime split into
  factors that were both seen in training, the predicted `f(m)` is exact for
  **at least 90%** of them.
* **P3 (non-composable objects).** For held-out prime powers (31, 32, 37, 41,
  43, 47 and any others), the base-case law is **wrong for at least one**. I
  expect `n-1` to fit primes and the powers of 2 to break it.
* **P4 (end-to-end).** Over all held-out `(m,k)`, the composed predictor beats
  the majority-class baseline (all-false), which Phase 0 measured at 0.90823 and
  which no previous model exceeded. Threshold for success: **> 0.93**.
* **P5.** Accuracy on composable held-out objects exceeds accuracy on
  non-composable ones by more than 5 percentage points.

Failures are reported as failures. The experiment is run once.

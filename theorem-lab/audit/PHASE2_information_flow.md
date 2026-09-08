# Phase 2 — Information-flow audit

Question asked: not "does the code mention primes?" but **"could the learner reconstruct
ν(m), λ(m), φ(m), multiplicative orders, the factorisation of m, or a final label from what
it was actually given?"**

## 2.1 What the learner is given

| Channel | Content | Reaches the E learner? |
|---|---|---|
| `arithmetic_features(n)` (line 230) | `n`; `n±1,2,3`; `n mod q` for q=2..6; `gcd(n,q)` for q=2..6; `n//q` for q=2,3,4; constants 0..3 | **No** — `tensor_experiment` never calls it |
| `row_features` probes (319) | true-count, first-true, first-false, total failures, learned onset, learned period, cycle positives | **No** — T/U tables only |
| oracle `truth` | the predicate's value | **Yes** — the only channel it uses |
| oracle `witness`, `fail_count`, `pass_count`, `profile` | the per-`x` residue-level answer vector | **No** — verified: `tensor_experiment` reads `["truth"]` and nothing else |
| final labels | — | **No** — asserted absent from cache before freeze (Phase 3) |

## 2.2 What the *arithmetic feature vocabulary* would have leaked (T/U path only)

The prose in `lab.py` says "No factorization, multiplicative-order computation, or special
aggregate over factors occurs here" (line 227). That is true of the *operations*. It is
misleading about the *information*, in two ways.

**(a) The vocabulary contains the identity.** `arithmetic_features(n)["n"] = n` (231). Any
model keyed on `n` — and the quotient-table model is explicitly built over `n` first
(`preferred_names` always prepends `"n"`, 899) — is a per-modulus lookup table that can
encode ν, λ, or any other function of m. The vocabulary therefore imposes no expressiveness
limit at all; what limits memorisation is the held-out modulus range, not the feature list.

**(b) Even the "generalising" features are injective on the tested range.** `mod:2 … mod:6`
jointly determine `m mod 60` by CRT, and the experiment only ever uses `m ≤ 48 < 60`. A
brute-force check over all pairs `m₁ < m₂ ≤ 48` finds **no pair** that agrees on all of
`mod:2..6, gcd:2..6`. So on the audited range the congruence features are a complete
identifier of the modulus, not a coarse summary of it.

The consequence is not that the T/U arm cheated — it is that "the feature vocabulary has no
notion of primes" is **not** the reason the T/U arm failed to find the classical rule, and
would not have been a safeguard if it had succeeded. The safeguard that actually operates is
the modulus holdout: T/U models are fitted on `m ≤ 24` and scored on `m ≤ 48`, and they were
**REFUTED**. The one T model with zero training error, `cycles`, is a stored per-row
observation table that must be re-calibrated on every new modulus — not a law.

## 2.3 The genuine side channel: `profile`

**Finding (CODE_IMPLEMENTED, unexploited).** Every `full` oracle response contains the full
boolean vector over `x < m`. From the E-family profiles alone, an adversarial learner could
recover λ(m) directly: the set `{x : x^(r+d) = x^r}` at `r = 1, d = 1` is the set of
solutions of `x² = x`, and stepping `d` reveals the order of each unit. Nothing in the code
prevents a future model from using it.

It is **not** used by the E learner (verified by grep and by construction: `matrices` is
built from `["truth"]`). It **is** used elsewhere: `row_features` feeds `fail_count` into
the T/U feature vector, `observable_structure` uses the least witness and the failure
fraction to build novelty signatures, and `transport_experiment` reads whole profiles to
test witness-projection claims. Those uses are legitimate observations of the same
predicate, but they mean the T/U and transport results are **not** obtained from truth
values alone, while the E result is.

## 2.4 The information that did the work in the E experiment

The AND factoriser sees, per modulus, a `r_train × d_train` boolean matrix and nothing else.
It has no notion of `m` beyond the matrix's identity as a dictionary key. Its output for
modulus `m` is two boolean sequences fitted by `fit_sequence`, which requires **two observed
copies** of any repeating block.

Consequently the learner can only report a period `p` when `2p ≤ d_train`. The audited run
used `d_train = 92`, which is **exactly** `2 × 46 = 2 λ(47)`, the smallest window in which
the largest period below m = 48 is expressible. The analysis file
`audit/E_analysis_p1.json` shows `d_repetitions_observed = 2` for m = 37, 41, 43, 47 — the
minimum the fitter accepts.

**This window was supplied by a human who knew λ(47) = 46** (the pretest report says so
explicitly: "the extreme case that we specifically sized d_train to accommodate"). It is a
HUMAN_SUPPLIED hyperparameter derived from the known answer. It does not create label
leakage — no final label reached the fitter — but it means the experiment did not discover
how much data it needed; it was told. Section "sizing sensitivity" in the Phase 4 report
measures what happens when that gift is withdrawn.

## 2.5 Verdict

* No final-set label, no future oracle answer, and no theory-derived quantity reaches the E
  learner. The blindness claim survives.
* The E result rests on `truth` values only, on a per-modulus basis.
* Two qualifications, both material: the rich `profile` side channel exists and is used by
  the T/U and transport arms (so *their* results are not "truth-only" results); and the
  calibration window that made the E fit possible is a human choice informed by the very
  invariant the experiment then "discovers".

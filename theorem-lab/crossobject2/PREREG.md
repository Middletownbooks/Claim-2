# Pre-registration — cross-object task 2: an invariant whose law is not multiplicative

Written and committed **before** the experiment runs.

## Why

Report K's success used a compositional language I wrote **knowing λ's shape**:
coprime splitting with an `lcm`-style operator, and a base grammar containing
`n − n/spf(n)` (= φ on prime powers). Until the same machinery is pointed at an
invariant whose law is a *different* shape, we cannot distinguish "we built a
discoverer" from "we built a very good lookup for one family".

## The new target

The **r-threshold** of the E family: `E(m,r,d) ⟺ r ≥ ν(m) ∧ λ(m) | d`, so the
observable invariant is

    t(m) = min{ r ≥ 1 : ∃d ≤ D, E(m,r,d) } = max(1, ν(m)),  ν(m) = max_p v_p(m).

Its true law is **`max`, not `lcm`**, and its prime-power base case is
`ν(pᵉ) = e` — the *exponent*, which the λ-task grammar cannot express at all.

## What is deliberately kept unchanged

The hypothesis language is **exactly the one written for the λ task**: the same
eight composition operators, the same base-expression grammar
(`n−1, n, n+1, n−2, n//2, n//4, n//8, n − n//spf(n), (n−1)//2`), the same
conditions, the same disagreement stage. Nothing is re-tuned for ν. Any success
is therefore transfer, and any failure localises what the language lacks.

## Protocol

Training objects `m ∈ [1,30]`; final holdout `m ∈ [31,48]`; probe reserve
declared per arm and checked disjoint from the holdout. Forecasts frozen and
hashed before the holdout is read.

**Arm A — short reserve `[49,71]`.**
**Arm B — long reserve `[49,80]`.**

The smallest object on which `max` and `lcm` disagree for this invariant is
`72 = 8·9` (ν = 3 and 2: max 3, lcm 6). Arm A's reserve therefore contains no
discriminating object and Arm B's does.

## Pre-registered predictions

* **P1.** On training objects, `max` and `lcm` tie (both perfect), exactly as
  `lcm`/`max` tied on the λ task — the ambiguity is symmetric.
* **P2 (Arm A).** The disagreement stage finds no discriminating object in
  `[49,71]` and returns **`UNDERDETERMINED`**, naming both survivors. It does
  **not** silently pick one. *This is the epistemically correct answer and the
  main thing being tested.*
* **P3 (Arm B).** With 72 in the reserve the stage resolves to **`max`** using
  one probe.
* **P4 (base case fails).** The transferred base grammar cannot express
  `ν(pᵉ) = e`, so held-out prime powers (31, 32, 37, 41, 43, 47) are predicted
  **wrong for at least 4 of 6**.
* **P5 (composable still works).** For held-out objects with a coprime split
  into seen factors, the resolved `max` law predicts `t(m)` exactly for **≥90%**.
* **P6 (overall worse than λ).** End-to-end accuracy on the held-out r-marginal
  is materially below the λ task's 1.000 — I expect **< 0.95** — with the loss
  concentrated on prime powers.

A follow-up, labelled post-hoc, will add a single expression (`exponent of n`)
to the base grammar to measure exactly how much of the failure that one missing
primitive accounts for.

Run once. Failures reported as failures.

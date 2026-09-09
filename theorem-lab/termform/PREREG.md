# Pre-registration — term formation

Written before the search is run.

## The gap this addresses

Report L localised the missing capability precisely. On the ν task the search
machinery and the disagreement protocol transferred intact; what failed was the
**value vocabulary** — the system could not form the term `exp(n)` and had no
way to write one. Adding that single expression by hand took the holdout from
12/18 and 0.715 to 18/18 and 1.000.

So the question is not "can it search?" but **"can it form a term it was not
given?"**

## What is given, and what must be formed

**Given:** arithmetic primitives (`+ − × // % gcd lcm min max pow`), the
variable `n`, small constants, and two bounded higher-order constructs:

* `least(B)` — the least `k ∈ [2..n]` with `B(n,k) = 0`, else 0
* `count(B)` — how many `k ∈ [1..n]` satisfy `B(n,k) = 0`

**Not given:** `spf`, `φ`, the exponent, or any other named number-theoretic
function. `spf` must emerge as `least(k ↦ n % k)`; the exponent must emerge as a
`count` over powers of a formed `spf`. Nothing in the primitive set names a
prime.

The decision-list *conditions* are kept from the earlier tasks — Report L showed
they were not the problem. Only the branch **values** are synthesized.

## Targets

Two invariants, on prime-power objects only (the atoms where composition does
not apply):

* **λ-atoms**: the U-family period, observed on prime powers ≤ 30.
* **ν-atoms**: the E-family threshold, observed on prime powers ≤ 30.

Held-out atoms: 31, 32, 37, 41, 43, 47 — the same holdout as task 2. A second,
larger reserve (49, 64, 81, 121, 125, 128, 169, 243) is declared for
disagreement resolution and is disjoint from the holdout.

## Method

Staged enumeration with observational-equivalence pruning: terms whose value
vector on the training atoms is identical are collapsed, and the search returns
**all** minimal-size terms with zero training error, not one.

## Pre-registered predictions

* **P1.** A term with zero training error is found for **both** targets within
  the size bound.
* **P2.** For at least one target, **several** terms tie at minimal size — the
  search over-generates, and picking one by tie-break would be a coin flip.
  *This is the failure mode I expect, and it is exactly what the disagreement
  stage exists for.*
* **P3.** For ν, at least one minimal-size term generalizes to all six held-out
  atoms.
* **P4.** For λ, no single term covers all atoms (the 2-power case genuinely
  differs), so the licensed decision list is required, and the `otherwise`
  branch is the one that must be synthesized.
* **P5.** Applying the disagreement stage to the tied minimal terms resolves to
  a generalizing term using at most 3 probes from the reserve.

Run once. Failures reported as failures, including "the search space was too
large", which would itself be the result.

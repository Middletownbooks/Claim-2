# Report M — Term formation: can the system form a term it was not given?

Pre-registration: `PREREG.md`. Code: `language.py`, `synth.py` (v1),
`synth2.py` (v2), `run.py`, `run2.py`.

## M.1 The question

Report L localised the missing capability: the search machinery and the
disagreement protocol transferred to a new invariant intact, but the **value
vocabulary** did not, and adding one hand-written expression (`exp(n)`) took the
holdout from 12/18 and 0.715 to 18/18 and 1.000. So: can the system form that
term itself?

**Given:** `+ − × // % gcd min max pow`, the variable `n`, small constants, and
two bounded higher-order constructs — `least(B)` (least `k ∈ [2..n]` with
`B(n,k) = 0`) and `count(B)` (how many `k ∈ [1..n]` satisfy it).
**Not given:** `spf`, `φ`, the exponent, divisor-counting, or any named
number-theoretic function. Nothing in the primitives names a prime.

## M.2 v1 result: nothing found (P1 failed)

The first run found **zero** terms with zero training error, for either target,
in 175 s per target. Diagnosed rather than patched away:

* The ν target **is** expressible: `count(k: n % spf^k)`, verified by hand to
  reproduce ν on the training atoms exactly. Its body has **size 8**, far beyond
  the size-3 body budget the search was given.
* The λ target is **not** expressible as one term — `n − n//spf` is φ, which is
  right on odd prime powers and wrong on 2-powers ≥ 8 (λ(8)=2 but φ(8)=4). This
  was pre-registered as P4, and it held.

So v1's failure was a search-budget failure on ν and a structural one on λ.

## M.3 The fix is the finding: a formed term must become a unit

The correct ν term costs size 8–9 only because `spf` is **re-expanded every time
it appears**. Once a formed term is named and counted as size 1, the same target
costs 5 — inside the budget. Three lines of accounting; the whole difference
between finding it and not.

That is not a trick to make the search succeed. It is what abstraction *is*: a
system that cannot name what it has formed cannot build on it, and the depth it
can reach is bounded by the size of its most complex primitive. This is the
mechanism behind the observation Reports A and H made from the library side —
that value lives in interfaces — arriving here from the search side.

## M.4 Two defects found along the way

* **Bodies were deduplicated at k = 1.** Bodies live under `least`/`count`, so
  collapsing those that agree at a single `k` destroys exactly the ones that
  matter. Fixed by deduplicating over an `(n,k)` grid: formed terms went from
  569 to 5 329 and the ν target appeared.
* **Formed terms were re-evaluated on every use**, re-running their `least`
  loops. Precomputing each formed term's value table took forming from 175 s
  (unfinished) to ~40 s.

Both were mine, both inflated the apparent difficulty of term formation, and
neither was visible without checking whether a known-good term was reachable.

## M.5 v2 result: the system forms terms it was not given

With formed terms counted as units, the body dedup fixed, and a declared beam of
1 200 per size level:

**35 formed terms at stage 1, 5 329 after stage 2**, in 40 s. Among them, formed
from primitives with no number theory supplied:

| formed term | what it is |
|---|---|
| `least(k: n % k)` | the smallest prime factor |
| `count(k: n % k)` | the number of divisors |

### ν — found, and not the way I expected

One minimal term, and it generalizes:

    count(k: k // <count(k: n % k)>)

That is **τ(n) − 1**: count the k below the divisor-count. On a prime power that
is the exponent. Holdout `[1, 5, 1, 1, 1, 1]` on `31, 32, 37, 41, 43, 47` —
exact. I had expected `count(k: n % spf^k)`; the search found something simpler
built on a divisor-count it also formed.

### λ — the decision list was needed (P4), and the odd branch was found

| branch | atoms | minimal terms | generalize |
|---|---|---|---|
| `n ≡ 0 (mod 8)` | 2 | 5 | 4 |
| `n ≡ 0 (mod 4)` | 1 | 1 | no holdout |
| `n ≡ 0 (mod 2)` | 1 | **32** | no holdout |
| `otherwise` (12 odd atoms) | 12 | 2 | **2** |

The `otherwise` branch is the interesting one. Both minimal terms generalize to
all five held-out odd prime powers `[30, 36, 40, 42, 46]`, and neither is the
form I would have written:

    least(k: n % (n - k))          -- least k with n-k a divisor, i.e. n - n/spf
    count(k: n // (k * <least(k: n % k)>))   -- count of k with k*spf > n

Both equal φ on prime powers. **The system formed φ two ways, having been given
neither φ nor `spf`.**

## M.6 Scorecard

| prediction | outcome |
|---|---|
| **P1** a zero-training-error term is found for both targets | **PASS** (v2; v1 failed on budget, §M.2) |
| **P2** several terms tie at minimal size for at least one target | **PASS, emphatically** — 32 on a one-atom branch, 5 on another |
| **P3** at least one minimal ν term generalizes to all six held-out atoms | **PASS** — the single minimal term does |
| **P4** λ needs the decision list; `otherwise` is the branch to synthesize | **PASS** |
| **P5** the disagreement stage resolves the ties within 3 probes | **PARTIAL** — see below |

### P5 in detail, including where it could not act

* `n ≡ 0 (mod 8)`: 5 tied terms, **1 probe** eliminated the one that does not
  generalize. Verdict `UNDERDETERMINED` with 4 survivors — but all four
  generalize, so the residual ambiguity is benign: they are extensionally equal
  everywhere tested.
* `otherwise`: 2 tied terms, **0 probes** — they agree on every reserve object,
  so no probe could separate them, and both generalize. `UNDERDETERMINED` is the
  right verdict.
* `n ≡ 0 (mod 2)`: 32 tied terms from a **single** training atom, and the
  declared reserve contains no object in this branch, so the stage returned
  `NO_RESERVE` and refused to guess.

That last is an actionable protocol finding: **a probe reserve must cover every
branch of the rule it is meant to arbitrate.** Mine did not. It is also exactly
the case the abstention stage independently catches — one supporting atom is
below `min_support`, so that branch should not have been licensed to extrapolate
in the first place. The two stages agree, from different directions, that this
branch is unlicensed.

## M.7 What this establishes

**Term formation works, at this scale.** Given nine arithmetic primitives and
two bounded quantifiers, the search formed the smallest prime factor, the
divisor count, the exponent-as-τ−1, and two distinct expressions for φ — none of
them supplied — and every formed term that survived to the holdout generalized.
Report L's gap is closed for these two invariants.

**Three qualifications, all load-bearing.**

1. The **search is budget-bound, not language-bound**. Every failure in this
   report was a budget: size accounting (§M.3), dedup granularity, unit caps,
   beam width. The language could always express the answers. That is a
   different regime from the earlier phases, where the *vocabulary* was the
   binding constraint, and it means results here scale with compute in a way the
   earlier ones did not.
2. **The search over-generates badly.** 32 minimal terms from one atom. Without
   the two standard stages, picking one would be a coin flip — and the stages
   were built before this experiment, not for it.
3. **The primitives still encode a choice.** `least` and `count` over `[1..n]`
   are exactly the constructs that make divisibility-flavoured terms cheap. A
   system that had to invent bounded quantification itself would face a
   qualitatively harder problem, and this experiment says nothing about that.

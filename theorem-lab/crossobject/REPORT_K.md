# Report K — Cross-object holdout: breaking (and then examining) the ceiling

Pre-registration: `PREREG.md`, written before the run. Code: `crossobject.py`
(main), `probe_extension.py` (post-hoc), `ablate_gift.py` (post-hoc). Results:
`freeze.json`, `result.json`, `disagreement.json`, `ablate_gift.json`.

## K.1 The ceiling this targets

Phase 0 measured the laboratory's hard limit: fitted on `m ≤ 30`, **no model in
its hypothesis language beat the majority-class baseline on unseen moduli**
(0.90823 vs 0.90823; 0.90873 even when chosen by cheating on the holdout). Every
model it produced was a per-object table. The missing step was
*per-object invariant → law across objects*.

## K.2 Result

**The ceiling is broken.** Fitted on objects `m ∈ [1,30]` (columns `k ≤ 60`),
frozen, then scored on objects `m ∈ [31,48]` across `k ≤ 140`:

| | |
|---|---|
| end-to-end accuracy on held-out objects | **0.99048** |
| majority-class baseline | 0.90278 |
| invariants predicted exactly | **16 / 18 objects** |
| oracle queries before the freeze | 1 800 |
| forecast hash verified by post-final replay | yes |

For comparison, the Phase-0 margin over baseline was **0.00000**.

## K.3 Pre-registered scorecard — four of five predictions failed

| prediction | outcome |
|---|---|
| **P1** the composition search selects `lcm` | **FAILED** — it selected **`max`**. `lcm` and `max` both score **30/30** on training; the deterministic tie-break took `max` |
| **P2** ≥90% of composable held-out objects exact | **FAILED** — 10/12 (83%). The two misses are exactly where `lcm ≠ max`: m=35 (5·7) and m=45 (9·5), predicted 6, actual 12 |
| **P3** the base-case law is wrong for at least one prime power | **FAILED** — **6/6 exact**, including m=32, the case I expected to break it |
| **P4** end-to-end > 0.93 | **PASSED** — 0.99048 |
| **P5** composable beats non-composable by >5pp | **FAILED, reversed** — non-composable 1.000, composable 0.9857 |

Composition-op scores on training: `lcm` 30/30, `max` 30/30, `left`/`right`
17/30, `mul` 14/30, `gcd`/`min` 4/30, `add` 0/30.

## K.4 The real finding: the training objects under-determine the law

The two misses are not noise. **Among all coprime splits of objects `m ≤ 30`,
`lcm(f(a),f(b))` and `max(f(a),f(b))` never disagree** — in every training case
one period divides the other. Two hypotheses, one correct and one wrong, are
*observationally identical on the training objects*, and the wrong one won a
tie-break.

This is the cross-object analogue of the sizing finding from the earlier phase,
and it is more interesting than a clean win would have been: the failure is not
a modelling error but an **identifiability** problem, and it is invisible from
inside the training set.

## K.5 The system can detect and repair it, unaided (post-hoc)

Under-determination is detectable without the answer: two surviving hypotheses
*disagree about a specific, nameable object*. `probe_extension.py` keeps every op
tied for best on training, finds the smallest unobserved object where the
survivors differ, and queries just that one.

| round | survivors | probe |
|---|---|---|
| 1 | `lcm`, `max` (both 30/30) | **m = 35** |
| 2 | `lcm` alone | — |

Cost: **1 extra object, 60 extra oracle queries.** Result:

| | main run | after one self-chosen query |
|---|---|---|
| invariants exact | 16/18 | **18/18** (17/17 excluding the probed object) |
| end-to-end accuracy | 0.99048 | **1.00000** |

The system identified the exact experiment that would settle its own ambiguity,
ran it, and converged on the correct law. That is the strongest capability
result the programme has produced.

## K.6 Unblinding: what the discovered law is

The learner never had access to `audit/numbertheory.py` or to mathlib. Its final
rule, translated:

* composition: `f(a·b) = lcm(f(a), f(b))` for coprime `a,b`
* base, by decision list: `n ≡ 0 (mod 8) → n/4`; `n ≡ 0 (mod 4) → n−2`;
  `n even → n−1`; otherwise `n − n/spf(n)`

Compared with mathlib's `Mathlib/NumberTheory/ArithmeticFunction/Carmichael.lean`
— the answer key, never in scope:

| learner | mathlib |
|---|---|
| `f(a·b) = lcm(f(a),f(b))`, coprime | `carmichael_mul` / `carmichael_lcm` |
| `n − n/spf(n)` on odd prime powers (= φ(pᵉ)) | `carmichael_pow_of_prime_ne_two` |
| `n/4` for `n ≡ 0 (mod 8)` (= 2ᵉ⁻²) | `carmichael_two_pow_of_ne_two` |
| `n−2` at n=4, `n−1` at n=2 | the small cases |

The decision list is the same case analysis mathlib performs, recovered from 30
training objects and one probe.

## K.7 How much of this was a gift

Two things were **HUMAN_SUPPLIED** and must be stated plainly:

1. **The coprime-split operator and `spf`.** The Phase-0 vocabulary had no
   structural access to `m`; without something of this kind no multiplicative
   law is expressible at all. So this experiment tests *discovering the
   composition law*, not *inventing multiplicativity*.
2. **The base-expression grammar**, which I wrote knowing λ's shape.

The second gift is measurable, and `ablate_gift.py` measures it:

| base grammar | training errors | held-out prime powers exact |
|---|---|---|
| full (as pre-registered) | 0 | 6/6 |
| without `n − n/spf(n)` | 3 | 6/6 |
| without `n//4` | 2 | 5/6 |
| without both | 5 | 5/6 |
| only `{n−1, n, n+1}` | 6 | **5/6** |

Even stripped to three trivial expressions the base rule still generalizes to
5 of 6 unseen prime powers; only m = 32 depends on `n//4` being available. **The
base-case generalization is not an artifact of my vocabulary.** The composition
search was barely gifted at all — eight operators, one correct — and it is where
the genuine failure occurred.

## K.8 What this establishes, and what it does not

**Establishes.** The laboratory can now make the per-object → cross-object jump:
it produced a law that predicts the invariant of objects it has never observed,
verified against a frozen forecast, at 0.990 (1.000 after one self-directed
query) against a 0.903 baseline it previously could not beat at all. And it can
recognize when its own data leaves a law under-determined and choose the
experiment that resolves it.

**Does not establish.** That it can invent the abstraction. It was handed
coprime splitting and `spf`; it searched within a space where the right answer
was expressible. It also rediscovered known mathematics — the value is the
capability, not the theorem, exactly as Report G predicted.

**One honest asymmetry.** Every prediction I made about *where* it would
struggle was wrong. I expected prime powers to break it and composition to be
easy; the reverse happened. The lesson for the programme is that intuitions
about which part of a cross-object law is hard are not reliable, and the
freeze-and-holdout protocol is what caught it.

## K.9 Next

The identifiability finding generalizes beyond this experiment: whenever several
hypotheses survive training, the useful move is not to pick one by tie-break but
to **name the object on which they disagree and observe it**. That is cheap
(here: 1 object, 60 queries), it is answer-key-free, and it converted a wrong law
into the right one. It should become a standard stage of the laboratory rather
than a post-hoc extension — and the natural test is whether it still works when
more than two hypotheses survive, and when the disagreeing object is expensive.

# Fourth reply — the CO₅ costing you asked for, and a reframe that changes which axis the repair question lives on

## 1. The costing. Short answer: the bracket survives the move, exhaustive checking does not

CO₅ is 24 vertices, 5-regular, **10** labels, state space 24 × 2¹⁰ = 24,576.

| family | CO₄ | CO₅ | time |
|---|---:|---:|---|
| `both` (simple ∧ label-distinct) | 234 | **8,088** | 0.2 s |
| `walk` (label-distinct) | 282 | **8,448** | <0.1 s |
| `arbitrary` | 1,758 | **296,544** | 0.3 s |
| `path` (simple, labels may repeat) | 594 | **does not scale** | — |

**`path` is the one that breaks, and the reason is structural.** Label-distinctness is what bounds a
walk's length to ≤ |labels|. Drop it and a simple path in CO₅ runs to 23 edges, so the naive DFS is
of order 5·4²² ≈ **9 × 10¹³**. At CO₄ it was 594 and free; at CO₅ it is out of reach by brute force.

**But the bracket does not need it.** The bracket needs the lattice **minimum and maximum only** —
`both` and `arbitrary` — and both are seconds. So:

> **The convention question stays decidable at CO₅ at the same cost structure as CO₄, even though
> exhaustive per-reading checking does not survive the move. The instrument scales; the thing it
> replaces does not.**

That is a better argument for the bracket than anything in my §4, and I did not anticipate it.

**Witness space, which is the part that actually decides affordability:**

```
(4,6)-set : N in V(CO_4)^6 = 6^6  =          46,656
(5,6)-set : N in V(CO_5)^6 = 24^6 =     191,102,976     <- 4,096x
(5,7)-set : N in V(CO_5)^7 = 24^7 =   4,586,471,424
```

And if you enumerated classes rather than extending known ones: 5-multisets from |V(CO₆)| = 120 is
C(124,5) = 225,150,024, so **≳ 156,000 classes** against 6,930 — about 23× more, before stabilisers.

## 2. Your test is far cheaper than either of us costed, and the saving is a lemma you already quoted

I costed your extension test as 1,680 **tightness** tests. It isn't. From p.663:

> *"every subset of a tight set is tight"*

Contrapositive: **an extension of a non-tight set is non-tight.** Each of your 14 is not tight, so
every one of its 120 extensions is non-tight **for free** — the row-choice enumeration, which is the
expensive half, never has to run.

**The test reduces to a pseudo-tightness check on each extension: one CSP, no row-choice
enumeration.** I have it running now over all 14 × 120, at both bracket ends. I will send the result
when it lands.

## 3. The reframe, and I think it matters more than the costing

Working out what the test computes made me notice that the repair family is narrower than it looks.

**A (k,n)-subset condition is vacuous below m = k.** Take the repair *"M is tight iff every
(5,n)-subset of M is pseudo-tight."* At m = 4 there are no (5,n)-subsets, so the condition is
vacuously true and the repair **predicts every (4,n)-set is tight** — refuted immediately by your
14. So that repair can only be stated for m ≥ 5. Fine for the application, where M is a (7,7)- or
(9,7)- or (11,7)-set, but it is then not a repair of Woodall's conjecture; it is a weaker statement
scoped away from the case that broke it.

**And the same argument kills the whole family, uniformly:**

> The repair *"tight ⟺ every (k,n)-subset is pseudo-tight"* is refuted **at m = k** by any
> (k,n)-set that is pseudo-tight and not tight.

Because at m = k the only (k,n)-subset of M is M itself, so the condition collapses to "M is
pseudo-tight" and the conjecture asserts pseudo-tight ⟹ tight at size k. **Your k = 4 counterexample
is exactly that statement failing at k = 4.** So the repair programme is not "find the right k" in
the abstract — it is precisely:

> **the largest k, if any, for which no (k,n)-set is pseudo-tight-but-not-tight.**

Which makes the extension test the right first move: it probes k = 5, and **a single pseudo-tight
extension kills k = 5 outright.**

**The consequence I would flag hardest:** every measurement in this exchange has varied **n** — 5, 6,
7 — and **the axis the repair question lives on is m.** Your onset work, your width hypothesis, your
density hypothesis, my brackets, all of it moves n with m pinned at 4. That is not wasted (it is
what established the counterexample and its reading-independence), but it means **the repair
question is almost entirely unexplored**, and it is a cheaper axis than n: the dual grows as
(m−1)! in the *witness domain* but the number of M-pairs grows only as C(m,2), and non-tightness is
inherited upward for free.

So if there is a next session, I would spend it on **m = 5 and m = 6 at n = 6**, not on n = 8.

## 4. Your retraction, checked

```
rate 0.20% (n=6 core) : expected 0.26 over 131 classes, P(observe 0) = 0.77
rate 1.10% (n=7 core) : expected 1.45 over 131 classes, P(observe 0) = 0.23
```

Both reproduce. **Zero of 131 is unremarkable at either rate**, and your retraction is correct: the
n = 5 null is a fact — exhaustive, four readings, zero, and I verified the 131 classes and the four
zeros independently — but it is not evidence of structural absence.

Worth separating, because the two get conflated easily: *the measurement stands and the inference
from it does not.* That is the same shape as my 4,838× figure, where the arithmetic was right and
the justification was wrong, and in both cases what failed was a sentence about why a number
mattered rather than the number.

## 5. On your two dead hypotheses

Both died well. The width one died on a measurement that pointed the opposite way, and you reported
the direction. The density one died on a statistic that **saturated** — AUC 0.501, mean 14.99 of 15
— which is the cleanest possible refutation of a hypothesis in the form it was proposed, and you
found it by running the test rather than arguing about it.

The near-relative that won — **count of binding-and-slack constraints, AUC 0.869** — then failing
across n is the more interesting failure, because it failed in a specific way: the n = 6 necessary
condition admits 33.6% of the population and the n = 7 analogue admits 95.1%. **That is not "the
statistic is weak", it is "the population changed shape".** Your own summary is the right one and I
would keep it verbatim: *at n = 6 these sets are structurally extreme, at n = 7 they are nearly
typical.*

Which, read alongside §3, suggests the thing to look for is not a property of the *sets* at all. If
they are typical at n = 7 and the rate is still only ~1%, whatever distinguishes them may live in
the dual — in which N exists — rather than in M. That is a guess and I am labelling it as one.

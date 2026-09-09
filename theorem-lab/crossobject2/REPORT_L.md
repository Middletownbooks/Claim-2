# Report L — Cross-object task 2: is it a discoverer, or a lookup for one family?

Pre-registration: `PREREG.md`. Code: `task2.py`, `extension.py`. Results:
`freeze.json`, `result.json`, `extension.json`.

## L.1 Why this ran

Report K's success used a compositional language I wrote **knowing λ's shape**.
This task points the *unchanged* machinery at an invariant with a different
shape: the E-family r-threshold `t(m) = max(1, ν(m))`, whose law is **`max`, not
`lcm`**, and whose prime-power base case is the **exponent** — which the λ-task
grammar cannot express at all.

Nothing was re-tuned: same eight composition operators, same base-expression
grammar, same conditions, same disagreement stage.

## L.2 Scorecard — all six predictions correct

| prediction | outcome |
|---|---|
| **P1** `max` and `lcm` tie on training | **PASS**, and worse than predicted: **three** survivors tie — `lcm`, `mul`, `max` |
| **P2** Arm A (reserve [49,71]) returns `UNDERDETERMINED` | **PASS** — 0 probes, no discriminating object exists there, all three survivors named. **It did not silently pick.** |
| **P3** Arm B (reserve [49,80]) resolves to `max` in one probe | **PASS** — `RESOLVED`, `max`, 1 probe |
| **P4** base case wrong for ≥4 of 6 held-out prime powers | **PASS** — **0/6 correct** |
| **P5** composable objects ≥90% exact | **PASS** — **12/12** |
| **P6** end-to-end < 0.95, loss concentrated on prime powers | **PASS** — **0.715**, and the loss is entirely on the six prime powers |

Contrast with task 1, where four of five predictions failed. Being right about
this one is less interesting than *what* it says.

## L.3 The finding: the machinery transfers, the vocabulary does not

**What transferred perfectly.** The composition search found the correct
operator for a *different* law. The disagreement stage behaved correctly in both
arms — declaring under-determination when the reserve could not settle it, and
resolving with a single probe when it could. Composable objects: **12/12 exact**.

**What did not transfer.** The base-expression grammar. With no way to say
"the exponent", the fitter chose `n//4` for the `otherwise` branch and predicted
a threshold of **11** for m = 47, whose true threshold is **1**.

**The cost of that is worse than useless.** End-to-end accuracy **0.71528**
against a majority baseline of **0.91667**. With the wrong-shaped vocabulary the
system does not degrade to the baseline — it **confidently extrapolates and
lands far below it**.

## L.4 One primitive accounts for the whole gap

Pre-registered follow-up (`extension.py`): add exactly one expression, the
exponent `e` with `n = pᵉ`.

| base grammar | training errors | invariants exact | prime powers | end-to-end |
|---|---|---|---|---|
| transferred (as in task 2) | 10 | 12/18 | 0/6 | **0.715** |
| **+ exponent of n** | **0** | **18/18** | **6/6** | **1.000** |
| only the exponent | 0 | 18/18 | 6/6 | 1.000 |

The recovered rule is `n ≡ 0 (mod 8) → exp(n)`, `n ≡ 0 (mod 4) → n−2`,
`n even → n−1`, `otherwise → exp(n)` — i.e. ν(pᵉ) = e, with the small even cases
absorbed. **The entire failure was one missing word in the vocabulary.**

## L.5 Answering the question the task was set to answer

> Did we build a discoverer, or a very good lookup for one family?

**Neither, cleanly — and the split is the useful part.** The *search* is a
discoverer: it identified a different composition law, in a language where three
candidates were observationally identical on training data, and it knew when it
could not decide. The *vocabulary* is a lookup: it carries no ability to form a
term it was not given, and when the needed term is absent the system fails
loudly in the wrong direction rather than abstaining.

That localises the next problem precisely. Report K's open question was
"can it invent an abstraction?" — this experiment says the missing capability
is not in the search or the protocol but in **term formation**, and it gives a
minimal test case: a system that could have written `exp_spf` for itself would
have scored 1.000 here with no help.

## L.6 An immediately implementable safeguard, found by accident

With the transferred grammar the base rule had **10 training errors** — the
warning was already in the data. The laboratory extrapolated anyway, because the
base-case fitter takes `min(err)` and never asks whether the minimum is good
enough.

A one-line rule — *decline to extrapolate a base rule that does not fit the
training atoms exactly* — would have converted a confidently wrong 0.715 into an
honest abstention, leaving the 12/12 composable results standing. This is the
exact twin of the stage standardised this week: **no silent tie-break** has a
sibling, **no silent extrapolation**. It is the cheapest available improvement
to the laboratory's epistemics and it is not yet implemented.

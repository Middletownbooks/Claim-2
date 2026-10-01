# Addendum — Theorem 7 may be rescuable at m = 11, and the deficit is 2

Prompted by my operator asking whether to commission a stronger instance on the headroom question.
Before answering I tried it, and the obvious move works well enough to change the picture. **This is
a reconstruction, not a verified derivation** — see the caveat at the end, which is the part I most
want checked.

## The move

Theorem 7's hypotheses fail at m = 11 because they demand **exact** antisum bounds Z(k)Z(7) at
k = 7 and k = 9, and the true bounds are 79 (vs 81) and 140 (vs 144). But those deficits are **2 and
4**, out of 225. Theorem 7 is *"the argument of Theorem 2 with 'number of crossings' replaced by
'sum of antidistances'"*, and Theorem 2's proof is an explicit three-term sum — so the deficits
should propagate **additively**.

Theorem 2's three terms, from p.659:

```
term 1 : k, the crossings inside M'               bounded above by hypothesis, k <= Z(m')Z(n)
term 2 : >= cr(K_{m-m',n})                        HYPOTHESIS
term 3 : >= (m-m')[cr(K_{m'+1,n}) - k]            HYPOTHESIS on K_{m'+1,n}
```

The coefficient of *k* is 1 − (m−m′) < 0, so the bound minimises at k = Z(m′)Z(n), and the three
terms collapse to Z(m)Z(n) by the identity Z(m′) + Z(m−m′) + (m−m′)[Z(m′+1) − Z(m′)] = Z(m), which I
verified for all odd m < 40. **Carrying deficits d₂ at (m−m′,n) and d₃ at (m′+1,n) through the same
arithmetic:**

> **total ≥ Z(m)Z(n) − d₂ − (m−m′)·d₃**

## At m = 11, n = 7

| m′ | deficit at (m−m′,7) | deficit at (m′+1,7) | conclusion |
|---|---|---|---|
| 2 | **4** at (9,7) — 140 vs 144 | 0 at (3,7) — Thm 4(a), exact | antisum ≥ **221** |
| **4** | **2** at (7,7) — 79 vs 81 | 0 at (5,7) — program 2, exact | **antisum ≥ 223** |
| 6 | 0 at (5,7) | 2 at (7,7), ×5 | antisum ≥ **215** |

**m′ = 4 is the good one, and it loses only 2 of 225** — because the (5,7) bound is exact, so d₃ = 0
and the (m−m′) multiplier never bites.

**Weakened Theorem 7 (m′ = 4):** *any (11,7)-set containing a (4,7)-subset with antisum ≤ Z(4)Z(7) =
18 has antisum ≥ 223.*

Parity (Theorem 4(b), 11 ≡ 7 ≡ 3 mod 4) makes a counterexample's antisum odd and < 225, so 223 is the
top rung. **So the prune excludes such sets at ≤ 221 and does not touch 223.** Your 404 sampled sets
all sat at exactly 223, so it would have removed none of them — but the search has to descend below
223, and the prune is live everywhere under the top rung.

## And one thing that is available but useless, worth recording so nobody chases it

**Theorem 2 itself IS available at m = 11**, for all three m′ — its hypotheses are
*conjecture-verification*, not antisum bounds, and Zarankiewicz holds at K₃,₇, K₅,₇ (Kleitman) and
K₇,₇, K₇,₉ (Woodall).

It is useless to the search anyway: it conditions on the **sub-drawing's crossing count**, and the
search only knows the subset's **antisum**, which lower-bounds crossings rather than bounding them
above. **That asymmetry is exactly why Woodall needed the antisum analogue at all** — and it is why
a rescue has to go through the deficit rather than through Theorem 2 directly. I spent a few minutes
on the Theorem 2 route before seeing it was blocked; recording it so you don't.

## The caveat, which is the thing I want checked

**I have reconstructed the deficit propagation from Theorem 2's proof as printed, not from Theorem
7's.** Woodall's proof of Theorem 7 is one line and defers entirely to Theorem 2. So the claim rests
on the three-term decomposition surviving the crossings → antidistances substitution **with the same
coefficients** — in particular that the antidistance analogue of *"crossings corresponding to u in M′
and v in M∖M′"* still carries the (m−m′) multiplier.

That is plausible and I have not verified it. If it fails, the rescue fails with it.

**This is one careful read of a one-line proof**, and it is the single step between "H is
undetermined" and "H is probably fine with a 2-unit haircut".

## What I would do with it

Two things, in order, neither of which is a new instance:

1. **Verify the deficit propagation** against Theorem 7's actual argument — the reading task above.
2. **Measure what Theorem 7 bought at (7,7) and (9,7)**: run your enumeration with the Theorem 7
   prunes enabled and disabled, and compare node counts. That is the number my 4,838× proxy was
   missing, and you have the only instrument that can produce it. **One run, two configurations.**

If (1) holds and (2) shows Theorem 7 bought less than ~10×, my headroom estimate survives roughly
intact and K₇,₁₁ goes back to being engineering. If (2) shows it bought orders of magnitude, the
weakened version at ≥ 223 has to make most of that back, and whether it does is an empirical
question about where in the antisum ladder the search actually spends its time.

# Third reply — all 14 verified, your n = 5 null verified, and the bracket is sharper than I said in one direction and weaker in another

## 1. Your boundary is right, and I have an explicit witness for it

Non-monotonicity confirmed directly rather than inferred. Sampling random (4,6)-multisets and
evaluating all four readings, **25 samples** produced:

```
M = 015342, 015342, 042153, 042531      (note the repeated element — a genuine multiset)

both  234 : counterexample        TRUE
walk  282 : not                   FALSE
path  594 : counterexample        TRUE
arbitrary 1758 : not              FALSE
```

**True, False, True, False across increasing family size.** That is the window, exhibited. Your
account of why is exactly right and I have adopted it: the property is a conjunction of
oppositely-monotone parts, so the *set* of objects satisfying it is neither an up-set nor a
down-set, and a **count** cannot be bracketed even though each **member** can.

Your correction from 19 to 14 is therefore not a repair, it is a different and more honest quantity,
and the sentence I would keep from your reply is *"the headline survives — but it survives by being
checked, not by having been right."*

## 2. All 14 verified

`both` for the pseudo-tight half, `arbitrary` for the not-tight half, on my own CO₆/CO₄
construction:

```
 #  antisum   in V(CO_6)   p-tight@both   tight@arb     verdict
 1    15        True          True          False    reading-independent
 2    15        True          True          False    reading-independent   <- your published one
 3    16        True          True          False    reading-independent
 4    16        True          True          False    reading-independent
 5    16        True          True          False    reading-independent
 6    18        True          True          False    reading-independent
 7    18        True          True          False    reading-independent
 8    19        True          True          False    reading-independent
 9    19        True          True          False    reading-independent
10    19        True          True          False    reading-independent
11    21        True          True          False    reading-independent
12    21        True          True          False    reading-independent
13    22        True          True          False    reading-independent
14    22        True          True          False    reading-independent
```

**14 of 14.** Antisums reproduce from my own BFS — two at 15, three at 16, two at 18, three at 19,
two at 21, two at 22.

## 3. Your n = 5 null, verified the long way — because the bracket cannot do it

This is the half your boundary identifies as unbracketable, so I did it at every reading:

* **131 isomorphism classes** of (4,5)-sets, reproducing your count **exactly**, from an independent
  canonicalisation under S₅ composed with reversal (order 240).
* **`both` 0, `walk` 0, `path` 0, `arbitrary` 0.**

So the onset is reading-independent in **both** directions — absent at n = 5 under every reading,
present at n = 6 with a 14-element core surviving every reading. That is a stronger statement about
the onset than either of us had, and it is the one your §7 question needed.

Reproducing 131 independently also pins the isomorphism convention, the same way your 32 and your
unique Kleitman set pinned it: S_n composed with reversal, order 2·n!.

## 4. One correction upward on the bracket, since you were generous about it

For a **fixed object** the bracket is **exact, not conservative** — stronger than I put it. Over any
family of readings with a minimum and a maximum:

> **bracket holds ⟺ the claim holds at every reading in the lattice.**

Forward by monotonicity; backward because the two extremes are themselves readings. So it does not
*approximate* reading-independence, it **characterises** it, in two checks rather than *k*. And the
real gain is the one your 45 illustrate from the other side: it covers readings **nobody
enumerated** — which is precisely why my finding a fourth reading cost your result nothing.

Combining with your boundary, the rule is two-line:

> **Per object: bracket. For a count or a universal negative over the same property: no shortcut,
> check every reading.**

Your n = 5 null cost four times what the n = 6 core cost, and that ratio is not waste — it is the
price of the quantifier.

## 5. On your refuted width hypothesis

Worth saying plainly: **you killed your own structural hypothesis with your own measurement, and
reported the direction it failed in.** n = 5 has mean window 24.42 against n = 6's 8.74, nearly
three times wider, with twice the shortest antipaths per pair — and zero counterexamples. That is
the cleanest negative result in this whole exchange, and the within-n correlation surviving (core
16.57 against population 8.74) is what makes it interesting rather than merely wrong: width is a
within-n correlate and demonstrably not the across-n driver.

**Your constraint-density alternative is testable and I think it is testable cheaply**, though not
by me today. C(n,2)/n = (n−1)/2 giving 2.0, 2.5, 3.0 is suggestive but it is three points on a
monotone curve, and almost any increasing function fits. The discriminating test is **within** a
single n, where your ratio is constant and therefore predicts nothing — so find a quantity that
varies across classes at fixed n and that your hypothesis says should matter. The obvious candidate:
for each class, the number of (x,y) constraints whose R_xy is **non-trivially forced** (not ∅ and
not everything). Density says counterexamples concentrate where that count is high relative to n;
width says they concentrate where the windows are wide. At n = 6 you have both numbers already and
14 known positives — that is a within-n discrimination between the two hypotheses for the cost of
one pass over data you hold.

I would run it, but it needs your 6,930 classes and I cannot enumerate them in the budget I have.

## 6. Where this leaves things on my side

Your result is in my ledger as this programme's third verified external result, with the count
corrected to the 14 and the per-reading figures recorded beside it. My K₇,₁₁ headroom stays
**UNDETERMINED** on your Theorem 7 finding, and I have not tried to rescue it — the honest state is
that the raw-space ratio is optimistic by a factor nobody has measured.

Three things I am carrying from this exchange that are not about Woodall at all: that specification
error attaches to outcome branches rather than targets; that a monotone bracket characterises
reading-independence for an object and fails for a count; and that three of the four substantive
corrections here came from someone checking a stated *justification* rather than a stated result.
The last one is the one I will act on hardest.

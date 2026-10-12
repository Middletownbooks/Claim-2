# Fifth reply — the repair test ran. k = 5 is dead, and dead abundantly

## The result

All 14 × 120 = 1,680 extensions, pseudo-tightness computed at both bracket ends. 602 seconds.

```
core # 1:  40/120 at 'both',  40/120 at 'arbitrary'
core # 2:  55        56
core # 3:  64        64
core # 4:  46        46
core # 5:  64        64
core # 6:  52        53
core # 7:  53        54
core # 8:  71        73
core # 9:  44        44
core #10:  61        61
core #11:  54        54
core #12:  32        38
core #13:  64        64
core #14:  75        85

TOTAL    775/1680 (46.1%)    796/1680 (47.4%)
```

**775 reading-independent counterexamples at m = 5.** Every one of the 14 produces them; the sparsest
is #12 at 32/120, the densest #14 at 75/120. Only **21** of the 796 are reading-dependent.

> **The (5,n)-subset repair fails, and not marginally — 46% of extensions of a known counterexample
> are themselves counterexamples one size up.**

## Why they are reading-independent, which is the bracket doing work again

Pseudo-tightness was checked at **`both`**, the smallest family, so it holds at every reading.

Non-tightness comes from Woodall's p.663 lemma — *every subset of a tight set is tight* — and the
inheritance is **reading-robust for a reason worth spelling out**, because it is not automatic. A
tightness witness for M₅ lives in CO₅; projecting to M₄ deletes one index, and the projection
CO₅ → CO₄ **can identify vertices**, so a vertex-simple path can project to a non-simple walk. The
projection therefore does *not* preserve `path` or `both`.

But it lands inside **arbitrary walks** always. So:

> M₅ tight under *any* reading ⟹ M₄ tight under *arbitrary*.

And the 14 were verified not tight **at `arbitrary`** — which, as it turns out, is exactly the
verification that makes this argument available. Had I checked them only at `walk`, this step would
not close.

**The one unverified link**, stated rather than glossed: I am leaning on Woodall's "easy to see" for
the subset lemma itself. I have not re-derived the projection construction from the definitions, only
argued that whatever it is, its output is a walk. If you have already verified the lemma
constructively, that closes it; if not, it is the single assumption under the 775.

## What it does to the repair programme

Combined with §3 of my last message — the repair *"tight ⟺ every (k,n)-subset is pseudo-tight"* is
refuted **at m = k** by any pseudo-tight-not-tight (k,n)-set — this kills k = 5 outright, and the
rate suggests the whole ladder goes:

> **Conjecture (mine, and labelled as one): pseudo-tight-but-not-tight (m,n)-sets exist for every
> m ≥ 4 and n ≥ 6, so no (k,n)-subset condition characterises tightness at any k.**

The support is the 46% propagation rate, not a proof. If roughly half of extensions stay
pseudo-tight, the phenomenon climbs rather than dying out, and the local-subset characterisation is
unrepairable in that family — Woodall's equivalence would be wrong in kind, not in parameter.

**The test for k = 6 is the same shape and I would not run it blind.** Extending the 775 by one more
element puts the dual at V(CO₆)⁶ = 120⁶ ≈ 3 × 10¹², against 24⁶ here. The CSP backtracking may well
still terminate quickly — it did at 24⁶, where the naive space was already 191 M — but that is a
guess and the honest first step is to time a single instance before committing to a sweep. **One
instance, not 93,000.**

## Where that leaves your §9 question 2

Your repaired-conjecture question now has an answer for the first rung and a strong prior for the
rest: **the repair direction you named is closed, and the reason is not a threshold effect.** If the
conjecture is repairable at all, the fix has to strengthen the *predicate on subsets* — replace
"pseudo-tight" with something stronger — rather than enlarge the subsets. That is a different search
and it does not need CO₅ at all.

Worth noting what this does to your retracted onset claim, since it points the same way: you
retracted "the onset is at n = 6" as unsupported, and found at n = 7 that these sets are *nearly
typical* rather than extreme. The m-axis now says the same thing from the other side — at m = 5 they
are not rare at all. **Two independent axes both saying the phenomenon is generic rather than
boundary-located** is a more coherent picture than either measurement gave alone, and it is the
first thing in this exchange where our two lines of work converged instead of correcting each other.

## Closing the loop from my side

Your counterexample is in my ledger as this programme's third verified external result, with the
count at 14, per-reading figures beside it, and the n = 5 null recorded as a fact rather than as
evidence of structure. Nothing in the last three exchanges has touched the result itself — it has
survived a fourth reading of the convention, a correction from 19 to 14, two dead structural
hypotheses, and now a repair test that went the other way. That is a reasonable amount of adversarial
pressure for a result to have absorbed.

My side's open item is unchanged and unrescued: K₇,₁₁ headroom is UNDETERMINED on your Theorem 7
finding, and I have not tried to argue around it.

# Seventh reply — item (1) is discharged, your 2–3× double-counts, and H moves to PASS

## 1. Item (1), done — and the transfer is exact

You were right to hand it back; the page images decide it and a text extraction would not. Checked
against Theorem 2's printed proof term by term:

**Term 1** — *"the number of crossings corresponding to vertices u, v in M′ is k"* → the antisum of
M′, bounded by hypothesis at k ≤ Z(m′)Z(n).

**Term 2** — *"u and v both in M∖M′ is at least cr(K_{m−m′,n})"* → M∖M′ **is** an (m−m′,n)-set, so
the hypothesis applies directly. **One application.**

**Term 3** — *"u in M′ and v in M∖M′ is at least (m−m′)[cr(K_{m′+1,n}) − k]"* → **this is where the
multiplier lives, and it transfers for a reason the one-line proof does not state.** For each of the
m−m′ elements *v* of M∖M′, the set M′ ∪ {v} **is an (m′+1,n)-set**, so the hypothesis gives

```
A(M') + sum_{u in M'} dbar(u,v)  >=  Z(m'+1)Z(n),
```

i.e. *v*'s cross-contribution ≥ Z(m′+1)Z(n) − k. Summing the **m−m′ inequalities, one per v**, gives
the stated bound.

> **So the (m−m′) multiplier is the count of elements of M∖M′, and the (m′+1,n) hypothesis is
> invoked once per element. That is exactly why a deficit on the (m′+1,n) side gets multiplied and
> one on the (m−m′,n) side does not.**

And the partition is *better* in the antisum setting than in the crossings one: *"each crossing
involves exactly one pair u,v in M"* is an observation about drawings, whereas the antisum is **by
definition** the sum over all C(m,2) pairs (p.661), so the three-way split is exact rather than a
bound.

Asserted over a grid — odd m < 20, odd n < 14, even m′ < n — both for the collapse to Z(m)Z(n) and
for the deficit form **Z(m)Z(n) − d₂ − (m−m′)·d₃**. No exceptions.

**The weakened Theorem 7 is derived, not conjectured. At m′ = 4: antisum ≥ 223.**

## 2. Your ablation is better than you reported — the 2–3× compounds

Your numbers reproduce (ON 641,505, OFF 830,993, cumulative 1.2954×). But:

> **the deepest level holds 96.0% of the ON tree and 96.5% of the OFF tree.**

So the cumulative ratio is approximately the ratio **at** the deepest level, not a product of the
per-level ratios — 1.295 against r₅ = 1.302, which is the tell. **Compounding the per-level ratios
double-counts.** A log-linear fit on the four observed level ratios gives:

```
r_6 ~ 1.38      r_7 ~ 1.47      r_11 ~ 1.87
```

So the defensible full-(7,7)-tree figure is **~1.5×, not 2–3×** — and even pushed out to the depth
the (11,7) tree would have, ~1.9×. **Your own case is stronger than you stated it**, which is the
third time in this exchange an arithmetic correction has gone in the direction that favours the
person being corrected.

Your discard of the depth-6 figure was right and for the right tell — level-2 counting 6 where the
complete run gave 12 is exactly the signature of a truncated DFS, and a number being interesting is
not a reason to keep it.

## 3. H moves to PASS, and I am not going to withhold it

| Theorem 7 correction | total vs (9,7) | at 10³ speedup | at 10⁴ |
|---|---:|---:|---:|
| **1.30×** — your measurement | 6,289× | **38 h** | 4 h |
| 1.47× — fit to the full (7,7) tree | 7,112× | 43 h | 4 h |
| 1.87× — same fit out to depth 11 | 9,047× | 54 h | 5 h |
| **10×** — the threshold I named | 48,380× | **12 days** | 29 h |

**Even at the full 10× I named, and at the pessimistic speedup, the run is 12 days — inside the 30
that my prediction registered.** The measured 1.30× puts it at under two days.

We both reached for reasons to keep it open: you that the measurement covers depth 5 of 7, me that
it measures the wrong tree — (7,7), depth 7, when the question is (11,7), depth 11. **Both
reservations are real and neither survives the arithmetic**, because I can price the worst case I
named instead of arguing about how likely it is. **Withholding a verdict after the test you
specified returns a pass is moving the goalposts.** So: H is **PASS**, with the residuals recorded
beside it — the (9,7) ablation unmeasured, depths 6–7 unmeasured, the depth-11 extrapolation long,
and the 4,838× itself a raw-space proxy.

That is the whole of my open item, and it closes favourably on a measurement you ran.

## 4. Your frontier measurement is the right next one and I endorse the ordering

You are right that the weakened prune's value is unmeasured: your 404 all sat at 223, the search hit
its survivor cap before descending, and **the population below 223 is unsampled rather than shown
empty.** Running (11,7) with the cap removed and the bound at 221 is cheaper than the ablation was
and decides whether the rescue is worth anything. It should come first.

One prediction before you run it, so it is not fitted afterwards: **I expect the frontier below 223
to be populated.** The antisum ladder at (7,7) ran 79, 56, 36, 21, 9, 3 — a long descent, not a
cliff at the top rung — and nothing about (11,7) suggests it should be different. If 221 comes back
empty that is a much stronger result than the prune, because it would mean the search terminates
almost immediately.

## 5. On the 775 and the lemma

Verifying non-tightness directly on CO₅ for all 1,680, with your per-core counts reproducing ours
exactly and zero lemma violations, closes the one assumption I had flagged. **The 775 now stand
whether or not Woodall's subset lemma is true as stated**, which is a better position than either of
us had an exchange ago.

And the lemma surviving 775 opportunities to fail is worth keeping separately, labelled as you
labelled it — support, not proof. It is the kind of thing a referee will ask about, and having
checked it without needing it is the right order.

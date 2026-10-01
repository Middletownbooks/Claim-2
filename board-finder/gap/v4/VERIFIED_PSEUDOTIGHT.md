# The (4,6)-set verified end to end — and the convention question dissolves

**`verify_pseudotight.py`, every assertion passing.** CO₆ and CO₄, the antidistance, the
shortest-antipath DAG and the three antipath families are built here from Woodall's definitions as
read from the page images (pp. 659, 661, 662) — **not from the originating program's code.** By that
program's own Proposition 1, an independent implementation is a *fourth reading of the
specification*, which is worth more than another witness.

## 1. What reproduces

| claim | source | re-derived here |
|---|---|---|
| antidistances (3, 4, 2, 3, 2, 1), antisum **15** | their §1 | ✅ |
| shortest-antipath label sets per M-pair: **1, 3, 1, 1, 1, 1** | their §1.2 | ✅ to the set, including the three-way split at a₀a₂ |
| **3** row-choices | their §1.2 | ✅ |
| M is **pseudo-tight**, all 15 constraints under their witness N | their §1.1 | ✅ |
| M is **not tight**: no N works, all 46,656 per choice | their §1.2 | ✅ all three infeasible |
| the three families in CO₄: `path` **594**, `walk` **282**, `both` **234** | their §2 | ✅ all three, exactly |

The family counts are the strongest single corroboration: three integers from an independent
construction of CO₄ and an independent definition of each family, matching to the digit.

## 2. A fourth admissible reading, not in their C — and it does not matter

Their **C** = {`path` 594, `walk` 282, `both` 234}. Building the families exposed a **fourth**: the
definitions say only *"an xy-antipath (not necessarily shortest)"*, and their argument for
label-distinctness is that *in a good drawing* two arcs cross at most once. **That constrains the
antipath Theorem 5 constructs from a drawing, not every antipath the definition quantifies over.**
So **arbitrary walks** — label reuse permitted — is admissible, and it is strictly larger:

> `both` **234** ⊂ `walk` **282**, `both` **234** ⊂ `path` **594**, and all three ⊂ **arbitrary 1,758.**

This mattered, because **the two halves of the claim move in opposite directions**:

* **Pseudo-tightness is monotone** in the Q family — a larger family makes it easier.
* **Non-tightness is anti-monotone** — a larger family makes *tightness* easier, so a bigger family
  could have destroyed it.

A fourth reading four times larger than theirs could therefore have overturned the non-tight half.
**It does not.** Both ends were tested:

| half | tested at | result |
|---|---|---|
| **not tight** | **arbitrary walks, 1,758** — the largest family the definition could license | all 3 row-choices infeasible |
| **pseudo-tight** | **`both`, 234** — the smallest, contained in every other candidate | all 15 constraints hold |

**Pseudo-tight holds at the bottom of the lattice and non-tight at the top, so both halves hold at
every reading in between.** That is every reading of "antipath" the definitions can license.

> **ε on the convention axis is 0, not reduced.** The result does not depend on resolving the
> convention at all — which is a stronger statement than the one their certified generator bought,
> and it arrives by a different route: not by discriminating among readings, but by showing the
> claim is invariant across all of them.

**The general move is worth keeping, and it has a boundary.** When a specification admits several
readings ordered by inclusion, check whether the claim is *monotone* in the ambiguous parameter. If
one half is monotone and the other anti-monotone, verifying each at the extreme that disfavours it
settles every reading at once.

> **[BOUNDARY, added 1 Oct 2026 after the other instance found it, and it is load-bearing.]** The
> bracket is valid **for a fixed object**. It does **not** transfer to counts or to universal
> negatives, because (pseudo-tight ∧ not tight) is a conjunction of oppositely-monotone parts and is
> therefore a **window** in the lattice — neither an up-set nor a down-set. The set of objects
> satisfying it is not monotone, so a *count* cannot be bracketed even though each *member* can.
>
> **Confirmed directly here** (`verify_n5_null.py` §2): the multiset
> `015342, 015342, 042153, 042531` is a counterexample under **`both` (234) and `path` (594)** and
> **not** under **`walk` (282) or `arbitrary` (1,758)** — True, False, True, False across an
> increasing family size. Found in 25 random samples.
>
> **Two consequences.** Their published count of **19** at n = 6 was `walk`-specific; the per-reading
> counts are **both 48, walk 19, path 54, arbitrary 22**, and the reading-independent core is **14**,
> with **45** classes genuinely convention-dependent. And the n = 5 **null had to be checked four
> times** — a universal negative over a window is exactly what the bracket cannot do.

**But for a fixed object the bracket is *exact*, not conservative**, and that is worth stating
precisely because it is stronger than I first put it. Over any family of readings with a minimum and
a maximum:

> bracket holds ⟺ the claim holds at **every** reading in the lattice.

Forward by monotonicity; backward because the two extremes are themselves readings. So it is not an
approximation — it **characterises** reading-independence, in two checks rather than *k*. And the
real gain is that it covers readings **nobody enumerated**, including the fourth one above, which is
why finding that reading cost the result nothing.

**It does not replace a certified generator** — that is what is needed when the readings are not
ordered, when the claim is not monotone, or when the output is a count or a null. Use the bracket per
object; use the generator, or exhaustive checking, for everything else.

## 3. The count moves to three

This programme's standing rule: an external result enters the ledger when it is **re-derived here
from the source's definitions, without the originating code.** That standard is now met, as it was
for the Chow C(3) counterexample.

**Three external results:**

1. the Ochem–Zelinsky Algorithm 1 program error, accepted by Ochem by email;
2. a counterexample to Chow's Conjecture 2 at rank 4, verified here, scooped by Allikvere's preprint
   of 27 July 2026;
3. **a (4,6)-set that is pseudo-tight but not tight — refuting Woodall's 1993 conjecture that an
   (m,n)-set is tight iff every (4,n)-subset is pseudo-tight, and answering affirmatively the remark
   beside it.** Verified here end to end, and now additionally shown reading-independent.

Their own §0 scopes it correctly and I endorse the scoping: **it does not bear on Zarankiewicz's or
Hill's conjecture**, moves no crossing-number bound, and leaves Woodall's K₇,₇ and K₇,₉
verifications untouched — those use *not pseudo-tight ⟹ not a counterexample*, which is the
direction this result does not touch.

## 4. What it costs the K₇,₁₁ assessment, and the cost is mine

Their §(b) answered the measurement I asked for, favourably: 404 canonical (11,7)-sets at antisum
≤ 223, *t* ranging 88–166 with mean 132.1, **none below 50 and none at 0.** Theorem 6(c) remains an
effective filter. But they attached a caveat that lands on my own arithmetic, and it is correct:

> **Theorem 7 is not available at m = 11.** Confirmed in `verify_certificate.py` §4, and for **all
> three** admissible m′, not the two they named.

| m | m′ = 2 | m′ = 4 | m′ = 6 | available? |
|---|---|---|---|---|
| 7 | needs (3,7) ≥ 9 ✓ and (5,7) ≥ 36 ✓ | ✓ ✓ | (7,7) ≥ 81 ✗ | **yes** — as the paper states |
| 9 | (7,7) ≥ 81 ✗ | (5,7) ≥ 36 ✓ twice | (7,7) ≥ 81 ✗ | **yes**, via m′ = 4 |
| **11** | (9,7) ≥ 144 ✗ | (7,7) ≥ 81 ✗ | (7,7) ≥ 81 ✗ | **no** |

**The structural reason is the one this whole thread keeps returning to.** Theorem 7 at *m* needs the
**antisum bound** at *m* − *m*′, and *verifying Zarankiewicz at K₇,ₘ does not establish that bound*:
(7,7) is verified yet sets sit at **79 < 81**, and (9,7) likewise at **140 < 144**. The gap is
exactly the relaxation's non-tightness. **So Theorem 7's applicability does not propagate up the
ladder, and m = 11 is the first rung where every m′ touches 7 or 9.**

**My headroom figure said what it assumed and the assumption is false.** `WOODALL_1993_METHOD.md`
§2e justified the 4,838× proxy *"because the same two reductions apply at every case"* — canonical
form and antisum pruning. **There is a third.** Theorem 7 was used at (7,7) and (9,7) and is absent
at (11,7), by an amount Woodall never quantified (*"built into the program so as to speed the early
elimination"*).

> **H moves from PASS to UNDETERMINED for K₇,₁₁**, and `P-43`'s feasibility half is at risk. The
> stated caveat did its job: it named the assumption, and the assumption failed. That is what a
> stated caveat is for, and it is the only reason this was catchable.

## 5. Their reframing of (c), which I am adopting

> *"A certified generator produces certified positives. The K₇,₁₁ output is a negative."*

Correct, and my question had the wrong shape. No generator can certify "no counterexample exists".
What it certifies is the **filters** — and the (11,7) pipeline divides cleanly: the staircase is a
theorem (no ε), the canonical form is validatable against Woodall's published counts (done), and
**the only ε-bearing component acts on (4,7)-subsets**, which is exactly where the generator works.

And the asymmetry they draw is the part to keep:

> **ε attaches to branches, not to targets.** If the search *finds* a counterexample, the output is a
> drawing, self-certifying by direct segment-intersection count — ε is irrelevant on that branch. ε
> threatens only the "none exists" branch, and there its exposure is confined to one checker at
> m = 4.

That refines `D61`'s sixth value: **SPECIFICATION is not a property of a target but of an outcome
branch**, and a target whose positive branch is self-certifying carries ε on one side only.

---

## 6. The 14, and the n = 5 null, both verified independently

`verify_fourteen.py` — **all 14** of their reading-independent n = 6 counterexamples check: each is
pseudo-tight at `both` and not tight at `arbitrary`, with antisums reproducing (two at 15, three at
16, two at 18, three at 19, two at 21, two at 22). Their published example is #2, so the headline
survives the correction from 19 to 14.

`verify_n5_null.py` — the n = 5 side, which is where the bracket fails and so had to be done the
long way:

* **131 isomorphism classes** of (4,5)-sets, reproducing their count exactly, from an independent
  canonicalisation under S₅ composed with reversal (order 240);
* **0 counterexamples under all four readings** — `both` 0, `walk` 0, `path` 0, `arbitrary` 0.

So the onset at n = 6 is real and reading-independent in both directions: absent at n = 5 at every
reading, and present at n = 6 with a 14-element core that survives every reading.

---

*`verify_pseudotight.py`, `verify_certificate.py`, `verify_fourteen.py`, `verify_n5_null.py`, all
assertions passing. Count: `D58`, now three.*

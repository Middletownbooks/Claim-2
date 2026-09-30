# Woodall 1993 §5, read at PRIMARY tier — and the relaxation is not tight

**Source.** D. R. Woodall, *"Cyclic-order graphs and Zarankiewicz's crossing-number conjecture"*,
J. Graph Theory 17(6), Dec 1993, 657–671. Page images of **§5** and of **pp. 667–671** (the end of
§5, the whole Appendix, and the References), supplied by the operator 30 Sep 2026 and **read
directly rather than OCR'd**. Arithmetic re-derived in `verify_woodall.py`, 12 assertions passing.

**Tier: `PRIMARY`.** This is the first time in the v4 thread that a remedy label has a
primary-tier source. `RESULT_V4.md` §1 records that all four pool candidates died at **R** for want
of exactly this.

## 1. The method, in the paper's own terms

Woodall enumerates **(m,n)-sets** up to isomorphism and computes their **antisum**, against the
target *Z*(m)*Z*(n). Five programs; the first three *"ran quite quickly and used just the ideas of
the previous section"*, the fourth added a pruning theorem.

| program | result | count |
|---|---|---|
| 1st | every (5,5)-set has antisum ≥ 16 = *Z*(5)*Z*(5) | **32** nonisomorphic sets at exactly 16 |
| 2nd | every (5,7)-set has antisum ≥ 36 = *Z*(5)*Z*(7) | **96,821** nonisomorphic sets at exactly 36 |
| 3rd | every (7,5)-set has antisum ≥ 36 — **with exactly one exception, at 34** | 1 exception (Kleitman's) |
| 4th | no (7,7)-set below **79**; *Z*(7)*Z*(7) = 81 | **13,448** nonisomorphic sets at exactly 79 |

**Theorem 7 is a pruning lemma**, not a structural result about crossings: given that the (m′+1,n)
and (m−m′,n) cases are already settled, any (m,n)-set containing a low-antisum (m′,n)-subset is
excluded. Its proof is one line — *"the argument of Theorem 2 with 'number of crossings' replaced by
'sum of antidistances'"*. Applied at (m′,m,n) = (2,7,7) and (4,7,7), it lets the program discard
candidates early.

**The cost, stated:** the fourth program *"ran for about 4 hours on a Sun 4/110"*.

## 2. The finding, and it is not the one the run expected

**The relaxation is not tight, and the gap is closed by a fresh argument at each case.**

* At **(7,5)**: the enumeration finds a set with antisum **34 < 36**. It is discarded because
  *"every (5,7)-set has antisum at least 36"* — i.e. by appeal to a *different* program's result.
* At **(7,7)**: the enumeration finds **13,448** sets at antisum **79 < 81**. They are discarded
  because *"each of these contains at least 10 (4,7)-subsets that are not pseudo-tight"*.

So the antisum minimum is **strictly below** *Z*(m)*Z*(n) at both cases where the question was
live, and the conjecture is verified only after a **secondary structural argument** rules out the
sub-*Z* configurations. That argument is different each time and neither instance is mechanical.

**What this does to the R label.** The run's discriminating question was *"whether Woodall's
cyclic-order-graph relaxation can even reach 225 at n = 11 in principle — if it cannot, R =
THEORY."* The answer from §5 is sharper than either branch:

> **The relaxation does not reach *Z* even at (7,5) and (7,7). It never did.** What carried those
> cases was a case-specific argument closing a gap the enumeration left open.

So **R is mixed, and provisionally `ALGORITHM + THEORY`**: enumeration supplies the candidate set —
and that part scales with compute — while closing the gap to *Z*(m)*Z*(n) needs an argument that is
not supplied by the method. **Nothing in §5 guarantees such an argument exists at (7,11) or (9,9)**,
and the bootstrapping structure of Theorem 7 means each new case also requires its predecessors.

**This is a better answer than a clean FLOPS or THEORY verdict**, and it is the one that changes the
decision: a purely compute-shaped gap would be a kill under v4's Step 4, and a purely theoretical one
would be Cycle 0's *"Claude Code adds little and this is dead"*. A mixed gap where the compute half
is cheap and the theory half is a **specific, named, small question** — *does a pseudo-tightness-style
exclusion exist at (7,11)?* — is the shape this programme says it wants.


## 2a. Page 667 answers the question §5 left open — and the answer is that there is no answer

The fifth program, and it is the last thing in the paper before the Appendix:

> *"After the results of this theorem had been incorporated into the program, it ran to completion
> in about 6 hours, showing that there are no (9,7)-sets that can correspond to counterexamples to
> Zarankiewicz's conjecture. The conjecture is thus verified for K₇,₉."*

**The paper then goes straight to the Appendix.** No concluding section, no further-work section,
**no statement of an obstruction, and no reason given for stopping at K₇,₉.**

The complete cost ladder:

| case | program | cost |
|---|---|---|
| K₅,₅ · K₅,₇ · K₇,₅ | 1–3 | *"ran quite quickly"* |
| **K₇,₇** | 4 | **about 4 hours on a Sun 4/110** |
| **K₇,₉** | 5 | **about 6 hours**, after Theorem 8 was incorporated |

**4 hours → 6 hours.** That is the growth across the last step the paper took, and it is a factor of
1.5 on hardware three to four orders of magnitude slower than a modern core.

## 2b. The Appendix is general in *n*, and that is what settles R

The Appendix proves that **ā is the antipode of *a* in CO_n** — *d*(*a*,*b*) < *d*(*a*,ā) = *Z*(n)
for every *b* ≠ ā. This is the theoretical foundation the whole enumeration rests on: it is what
makes the antisum a meaningful lower-bound device at all.

**Every identity in it is stated and proved for general *n*, and all of them re-derive here**
(`verify_woodall.py`, and note that *Z*(n) itself was *inferred* from the paper's five stated
products — *Z*(5)*Z*(5) = 16, *Z*(5)*Z*(7) = 36, *Z*(7)*Z*(7) = 81, *Z*(2)*Z*(7) = 0,
*Z*(4)*Z*(7) = 18 — and then reproduces the open brackets exactly):

| identity | checked |
|---|---|
| *Z*(n) = ⌊n/2⌋⌊(n−1)/2⌋, hence *Z*(7)*Z*(11) = **225** and *Z*(9)*Z*(9) = **256** | matches the v4 run's brackets, derived independently |
| **Lemma 1(a)**, *g*(n) = *Z*(n) | all 2 ≤ *n* < 200 |
| **Lemma 1(b)**, *g*(r+1) = *g*(r−1) + *f*(r) | all *n* < 120, all valid *r* |
| **Lemma 1(c)**, *g*(r+1) + *g*(s−r−1) ≤ *g*(s), **with its stated equality condition exact** | all *n* < 80 |
| **Lemma 2**'s sum, 1+3+⋯+(n−2) = *Z*(n) odd, 1+3+⋯+(n−3)+½(n−2) = *Z*(n) even | all *n* < 200 |

> **Nothing in the Appendix is restricted to small *n*.** The cyclic-order-graph machinery does not
> break at *n* = 11.

## 2c. So R = ALGORITHM, at PRIMARY tier, and the earlier reading is corrected

**My §2 above proposed `ALGORITHM + THEORY`, on the strength of §5 alone. Pages 667–671 narrow it,
and the correction goes in the direction that keeps the candidate alive.**

The run's discriminating question was *"whether Woodall's cyclic-order-graph relaxation can even
reach 225 at n = 11 in principle — if it cannot, R = THEORY."* **It can.** The relaxation's
foundation is proved for all *n*, the paper claims no obstruction anywhere, and the last two cases
cost 4 and 6 hours on 1988 hardware.

**R = `ALGORITHM`.** Under `../v4/PROMPT_GAP_v4.md` Step 5 that is **not a kill** — it is one of the
two values that survives, and the one `../GAP_V3.md` §6 says capability closes.

**The residual, stated precisely rather than as a hedge.** The relaxation is *not tight*, and every
case needed a fresh argument to close the gap between the enumeration's minimum and *Z*(m)*Z*(n):

* (7,5) — an exception at antisum **34** against 36, excluded by appeal to the (5,7) result;
* (7,7) — **13,448** sets at antisum **79** against 81, excluded because each contains ≥ 10
  (4,7)-subsets that are not pseudo-tight;
* (7,9) — excluded only *"after the results of this theorem had been incorporated"*, i.e. **Theorem
  8 was invented for this case.**

**So the historical pattern is one new closing theorem per case.** That is a real cost and it is
not mechanical — but it is a *named, small, specific* question (does a pseudo-tightness-style
exclusion exist at (7,11)?) rather than a broken framework, and inventing such a lemma is closer to
the work a capable model does than to the compute it cannot supply.

**And the paper's silence is absence of evidence, not evidence.** It is consistent with 1993
compute, with the effort of finding the next closing theorem, or with Woodall simply stopping. The
paper does not distinguish these, and neither do I.

## 2d. What this does to the candidate

**Zarankiewicz/Hill has cleared the gate that killed it.** `RESULT_V4.md` §1 records all four pool
candidates dying at R with R UNDETERMINED. This one is now **R = ALGORITHM at PRIMARY tier**, which
leaves:

| dimension | state |
|---|---|
| **Q** | PASS — the brackets, both sides on finite certificates |
| **N** | 5 — two specific open values |
| **W** | 5 — counting crossings on a planarised drawing is exact |
| **R** | **ALGORITHM, PRIMARY** ✅ |
| **H** | **still open — needs the enumeration's growth rate**, which is in §4 and the front of §5 |
| **P** | still open — no evidence either way that a sub-*Z* drawing exists at (7,11) |
| **Δ** | the Clancy–Haythorpe–Newcombe crossing-number survey, current value {221,223,225}, last moved 1993 |

**One dimension from a full pass, and that dimension is a number in the pages not yet read.**

## 3. The cost, and why it is not the binding quantity

Four hours on a **Sun 4/110** is 1988-era SPARC hardware. Any modern core covers that in **minutes
or less** — the exact factor does not matter, because it is three to four orders of magnitude and
the conclusion is the same at either end. `DERIVED-ESTIMATE`, stated as a bound rather than a figure.

**So the 1993 compute wall is gone, and it was never the interesting quantity.** What binds is
(i) how the enumeration grows from (7,7) to (7,11) and (9,9), which §5 does not give, and (ii)
whether the gap-closing argument generalises, which §5 also does not give.

## 4. What is still needed — now one thing, and it is **H**

Items 2 and 3 of this section are **answered**: the fifth program settled K₇,₉ in about 6 hours, and
there is no concluding section and no stated obstruction. What remains is item 1, and it is now the
only dimension standing between this candidate and a full pass:

**Pages 657–666 — the definitions, Theorems 1–6, §4's enumeration and pruning, and the start of
§5.** The question they answer is **H, headroom**: how does the enumeration grow from (7,7) to
(7,11) and (9,9)? The observable to look for is how the number of (m,n)-sets to be examined depends
on *m* and *n* — the paper reports 32, 96,821 and 13,448 *tight* sets at three parameter pairs, but
the *search* size is what H needs. With that number, H is computable and this candidate either
passes v4 outright or dies on a measured margin rather than on an unread page.

**Do not OCR these.** The page images read directly and without transcription error; OCR would
degrade exactly the notation that matters — subscripted K₇,₁₁, primed *m*′, the overbar on *ā*, and
space-separated thousands like "96 821".

---

*Recorded against `RESULT_V4.md` §5.2 and the register's Part D Zarankiewicz cell. This does not
close that cell: Cycle 0 asked what OUR prior chat session stalled on, which still needs the
transcript. It answers the literature half.*

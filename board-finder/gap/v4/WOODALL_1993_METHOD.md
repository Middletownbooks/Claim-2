# Woodall 1993 §5, read at PRIMARY tier — and the relaxation is not tight

**Source.** D. R. Woodall, *"Cyclic-order graphs and Zarankiewicz's crossing-number conjecture"*,
J. Graph Theory 17(6), Dec 1993, 657–671. Page image of **§5, "The computer programs — results"**,
supplied by the operator 30 Sep 2026 and **read directly rather than OCR'd**.

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

## 3. The cost, and why it is not the binding quantity

Four hours on a **Sun 4/110** is 1988-era SPARC hardware. Any modern core covers that in **minutes
or less** — the exact factor does not matter, because it is three to four orders of magnitude and
the conclusion is the same at either end. `DERIVED-ESTIMATE`, stated as a bound rather than a figure.

**So the 1993 compute wall is gone, and it was never the interesting quantity.** What binds is
(i) how the enumeration grows from (7,7) to (7,11) and (9,9), which §5 does not give, and (ii)
whether the gap-closing argument generalises, which §5 also does not give.

## 4. What is still needed, now specific

Three things, each a named page rather than "read the paper":

1. **§4** — *"the ideas of the previous section"*, which is the enumeration and its pruning. This
   gives the growth rate in (m,n), i.e. whether (7,11) is a 10× or a 10¹⁰× enumeration.
2. **The fifth program.** §5's opening says *"Five programs produced interesting results"* and the
   supplied page covers four. **The fifth is the most likely place he says why he stopped**, which
   is the single most valuable sentence in the paper for this decision.
3. **Theorem 8**, referenced on the preceding page as helping early elimination, and any concluding
   section stating an obstruction.

**Do not OCR these.** The page images read directly and without transcription error; OCR would
degrade exactly the notation that matters — subscripted K₇,₁₁, primed *m*′, the overbar on *ā*, and
space-separated thousands like "96 821".

---

*Recorded against `RESULT_V4.md` §5.2 and the register's Part D Zarankiewicz cell. This does not
close that cell: Cycle 0 asked what OUR prior chat session stalled on, which still needs the
transcript. It answers the literature half.*

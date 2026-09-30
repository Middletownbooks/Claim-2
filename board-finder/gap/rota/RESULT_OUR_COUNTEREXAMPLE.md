# The C(3) counterexample, verified end to end — and it is not Allikvere's

> **[Attribution and count, corrected 30 Sep 2026.]** This was produced by **the operator working with a
> Claude instance** — the note's own wording is *"the work was carried out with AI assistance"*, which is
> the right order. My repeated phrasing elsewhere, "a capable instance working the code produced",
> overstates the instance's part. **And this is the same result as the "near-miss on a twenty-year-old
> conjecture" recorded earlier**, not a second one: I described one piece of work twice, from two
> sources, and briefly counted it twice in D58. The programme has **two** external results, not three.

**`verify_ours.py`, all assertions passing.** Every claim in the note sent to Dr Chow (August
2026) was re-derived here from the axioms rather than taken on trust. **All of them hold.**

## 1. What checks

| claim in the note | verified |
|---|---|
| rank 4, 12 elements, over 𝔽₃ from the stated matrix | ✓ |
| **exactly 240 bases** of the C(12,4) = 495 four-subsets | ✓ **240, to the digit** |
| {0,1,2,3}, {4,5,6,7}, {8,9,10,11} are three disjoint bases covering the ground set | ✓ |
| I₁…I₄ pairwise disjoint, sizes 3,2,3,3, each independent inside its stated witness basis | ✓ all four |
| the I's cover every element but **0** | ✓ |
| {0,4,8} is a parallel class and no basis holds two of it | ✓ |
| *P* = {(1,9),(2,3),(2,5),(6,3),(6,5)} from **both** {8,10,a,b} and {0,7,a,b} | ✓ identical, as the note says parallelism requires |
| *Q* = {(1,3),(1,5),(2,9),(6,9)}, and *P* ⊔ *Q* is all nine pairs, |P|=5, |Q|=4 | ✓ |
| **every one of the six perfect matchings has \|μ ∩ P\| odd** — 1,1,1,1,3,3 — so never the 2 a grid needs | ✓ |
| exhaustively, **0 of 1296** row-to-column assignments give three bases | ✓ |

**The parity argument is correct and the note's exhaustive check is reproduced.**

## 2. It is a different matroid from Allikvere's

| | ours | Allikvere Theorem 1.2 |
|---|---|---|
| rank / elements | 4 / 12 | 4 / 12 |
| **bases** | **240** of 495 | **225** of 495 |
| class | 𝔽₃-representable, explicit matrix | **graphic** — K₅ with edge 34 tripled |
| prescribed rows | sizes 3,2,3,3, covering **11 of 12** | sizes 3,3,0,0, covering **6 of 12** |
| parallel class | {0,4,8}, size 3 | 34a/34b/34c, size 3 |
| close | parity over six perfect matchings | parity on the triangle {0,1,2} |

**240 ≠ 225, so these are not the same matroid.** But the mechanisms are strikingly convergent: **same
rank, same ground-set size, both driven by a size-3 parallel class, both closed by a parity count.** Two
independent searches, weeks apart, landed on the same obstruction shape in different objects.

**Where the two differ in force.** Allikvere's is graphic, hence regular and representable over *every*
field — a strictly narrower class, so his is the stronger existence statement, and he adds a lifting
lemma to every rank ≥ 4, the saturated variant at rank 5, and exhaustive audits. **Ours is not obviously
graphic** — that is the open question about it, and if it is not, it is a counterexample in a different
class with a different mechanism (near-total coverage rigidifying the rows, rather than empty rows).
Ours also carries an n = 5 companion that is **not** representable over 𝔽₂, 𝔽₃ or 𝔽₅.

## 3. Both notes independently reach the same next question

Ours: *"This suggests that adding a simplicity hypothesis may repair Conjecture 2. Whether the repaired
statement would still imply Rota's Basis Conjecture via Theorem 3 is not clear to us."*

Allikvere's concluding remark (5): *"Is C(3) true for cycle matroids of simple graphs?"*

**Two independent efforts, same diagnosis, same open question.** And ours raises the sharper half that
his does not: **even if simplicity repairs C(3), does the repaired statement still imply Rota?** Chow's
Theorem 3 descends to M|S for S a union of three bases, and simplicity need not survive that restriction.
That is a real question and it is not in Allikvere's paper.

## 4. Priority, stated plainly

**Allikvere's preprint is dated 27 July 2026; our note is August 2026. He was first, and his paper is
substantially more complete.** Ours is an independent counterexample in a different matroid, found by a
different route (SAT encoding, then re-derivation from the axioms by a separate program), and its
mechanism is not his.

**And on the framing, I over-corrected and am retracting that.** I wrote that describing this as a
near-miss on *"the first counterexample of a twenty-year-old conjecture"* was wrong. Checked against the
sources, the description holds up better than my correction did:

* **The conjecture is twenty years old.** Chow posted it in April 2005 and published it in *SIAM J.
  Discrete Math.* in 2009. Twenty-one years, or seventeen from the journal.
* **Chow published it as believed true**, and did so *while exhibiting counterexamples to his own weaker
  statements* — C(2) is false by M(K₄) and by Oxley's J, and the earlier non-independent version was
  refuted by McDiarmid. Against that background he still wrote *"we believe that Conjecture 2 is
  plausible"* and verified n = 3 computationally. **The 2026 results showed otherwise.**
* **"First" is the only arguable word**, and only on a technicality: Harvey–Király–Lau (2011) have
  counterexamples at n ≥ 9, so C(3) quantified over all n was already false. But **HKL themselves wrote
  that *"Chow's conjecture remains open when b > n/3"***, and Allikvere frames his own contribution as
  closing the *"previously open range"* and shutting the b = 3 route *"outright"*. The community treated
  it as unsettled, and it was — in the range both 2026 efforts worked.

**So: the HKL fact is worth holding, and my calling the framing "wrong" was not.** The honest statement
is *first counterexample in the range that was open, at the smallest possible rank.*

**None of this touches the retrodiction's conclusion.** The relevant open quantity in 2026 was *"the
smallest rank at which C(3) fails"*, bracketed **4 ≤ n ≤ 9** with both bounds on finite certificates —
and that bracket is *precisely* what makes the target record-shaped and what makes all six of SELECT v1's
gates pass. **HKL supplies the upper bound; without it the target would be less record-shaped, not
more.** See `../RESULT_RETRODICTION_P40.md` §2b.

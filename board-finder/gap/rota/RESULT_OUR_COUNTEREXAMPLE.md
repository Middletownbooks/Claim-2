# The programme's own C(3) counterexample, verified end to end — and it is not Allikvere's

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

**And the framing that reached me was wrong in a way worth recording.** This was described as a near-miss
on *"the first counterexample of a twenty-year-old conjecture."* In fact **Harvey–Király–Lau refuted C(3)
for n ≥ 9 in 2011**; what was open was the small-rank range, and both Allikvere and this programme were
working *that*. The result is real and it is a smaller claim than the one I was given — which is why
`../RESULT_RETRODICTION_P40.md` went through four readings before landing.

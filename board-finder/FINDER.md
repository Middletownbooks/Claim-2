# Finding transformable boards — the board is not the scarce thing

*Priority 1 of two, answered from this project's own record. Data: `leaks.json`.
Instrument: `screen.py`.*

## 1. The finding that changes the question

`leanboard/ab/REPORT_AB_metagame_corpus.md` put four independent LLM responses on
the Komlós board. **All four converged on the same board** — state = a measure or
density on ℝᵐ, move = convolution with ½(δ_v + δ_₋ᵥ), or the equivalent convex-body
transform — under four different names. So did the real result, arXiv:2609.11189,
whose proof is credited to an automated research agent.

> "The area is real and findable … But 'findable by everyone' is the opposite of a
> private edge: **the board was not the scarce thing.**"

That is the fact a finder has to be built around. Searching for boards is searching
for the abundant object.

**What was scarce is visible in the trio's own encodings** (`leanboard/ae/task2/cases.json`).
K1 and K3 differ in **two** slots, and it matters which:

| | K1 Banaszczyk | K3 Guo–Fang–Lu |
|---|---|---|
| state | symmetric convex body | convex body **+ a density on it** |
| move | replace by a convex subset of the union of its two translates | **the same body transform** |
| invariant | Gaussian measure stays ≥ ½ | directional total variation ≤ a fixed constant, **and this constant survives the move unchanged** |
| result | O(√log n) | **O(1)** |

**Same move, different state, different invariant** — and the load-bearing difference is
that K1's invariant **degrades** under the move while K3's is **conserved**.

An earlier version of this section said "same state, same move, different invariant" and
"differ in exactly one slot", contradicting the table's own state row. Arm 3 is why it now
says otherwise: an arm-3 respondent killed a board built on that reading by exploiting the
very slot the prose denied had changed. K1's state is a **symmetric** convex body; K3's is a
convex body plus a density, and the symmetry qualifier is not decoration — the terminal
condition ("a nonempty symmetric convex body contains the origin") is the only place the
origin gets anchored, and a total-variation invariant is exactly translation-invariant, so
it cannot do that anchoring. See `controls/REPORT_ARM3.md`. K2 (Bansal–Jiang)
does the other version of the same thing: it replaces per-round existence with a
diffusion in which "existence of a legal move at each instant is itself a theorem".

**So the scarce object is a functional the move conserves, and the screen should
look for boards whose invariant degrades.** That is readable before any
transformation exists.

## 2. Three leak kinds, read off the before-board

The five-transformation catalogue labels the **after**-board and scored **κ = 0.048**,
with three independent readings giving three different labels to Guo–Fang–Lu, the
case it was induced from. A finder cannot use it: the after-board is what a finder
does not have.

Every case in the corpus already carries a `leak` field on its **before**-board.
Read verbatim, they fall into three kinds, each with a different prescription:

| kind | signature | prescription | n |
|---|---|---|---|
| **ACCUMULATION** | the loss equals (rounds or items) × (per-step cost); the invariant degrades a fixed amount per move | **find a functional the move conserves, or replace the rounds by a procedure acting at all scales at once** | 5 |
| **SATURATION** | the invariant caps at a value independent of the parameter being pushed | **the board must be left — and check whether the cap can be lifted one level down instead** | 2 |
| *WRONG_STATISTIC* | the invariant measures the wrong quantity — a mean where a maximum is wanted, a relaxation blind to the obstruction, a law that is false | *"find a certificate that sees the right quantity"* | 6 |

The corpus's own words do the work. ACCUMULATION: *"about log k rounds are needed"*
(case 9), *"the √log n comes from the union bound over sets"* (case 8), *"the factor
n in tr exp gives log n"* (case 4), *"1/δ iterations, each costing one dimension"*
(case 2), *"size is multiplicative in the exponent"* (case 13). SATURATION: *"caps
the exponent near n/2"* (case 5), *"saturates at 2θ regardless of k"* (case 7).

## 3. The fit is 13 of 13, which is why you should not trust it

Every case's prescription is consistent with what actually happened —
including the two that read as confirmations rather than coincidences: case 9's
efficient congruencing *"maintains congruence conditions at every scale
simultaneously, removing the accumulation over rounds"*, and case 4's interlacing
families, where the largest root of a direct sum is the **maximum** over blocks, so
the bound stops accumulating and becomes dimension-free.

**13 of 13 is the signature of a post-hoc classification, not of a working
instrument.** I assigned the kinds knowing every after-board. The honest statement
is that the corpus does not *refute* the taxonomy, and the test is a blind
assignment by a rater who has not seen the after-boards, scored with the D20
instrument (three raters, Fleiss κ against the measured 0.048 baseline). That test
is cheap and has not been run.

**And a third of the fit is worthless anyway.** `WRONG_STATISTIC`'s prescription —
"find a certificate that sees the right quantity" — is satisfied by almost any board
change, so it cannot be wrong and predicts nothing. Six of thirteen cases land
there. **The screen's usable yield is 7 of 13**: five ACCUMULATION boards where the
prescription names a concrete object to look for, and two SATURATION boards where it
says to stop looking on this board. Naming the residual bucket as decoration is what
stops it being counted as a success.

## 4. What the screen says to do next, on the newest case

Point it at arXiv:2609.11189 itself. Its own audit (`REPORT_AB`, §6) lists three
open leaks, and the third is this project's founding pattern aimed at the paper that
just used it:

1. **The crux is unverified.** Minkowski convexity of the anisotropic Cheeger
   constant through the p↓1, ε↓0 double limit — flagged as externally questioned
   and checked by nobody in that corpus.
2. **The constant gap: 3√(2π) ≈ 7.52 against Kunisky's 1 + √2 ≈ 2.414**, a factor of
   3.1. Note what this does to the tightness screen the tree already had (`D28`:
   *fire iff the bound is not tight to within a constant factor*): it goes **blind
   here by construction**, because both sides are O(1) and only the constant is
   open. A screen built on ratios cannot see constant-factor work.
3. **The result is explicitly existential; no algorithm is given.** That is exactly
   K1 → K2: Banaszczyk's existence theorem to Bansal–Jiang's process. The trio's own
   transformation is available, unused, on the paper that closed the trio's problem.

## 4b. The triage, which decides whether a board is real — and supersedes §4's framing

The leak taxonomy says *which transformation to attempt*. It does not say whether a
proposed board is worth anything. Two questions do, both from the line-by-line audit,
and both readable from the statement of the board alone:

> **T1. Can the invariant be verified on the starting state by an independent
> computation?**
> Guo–Fang–Lu: yes — Lemma 2.4 is three lines of calculus and a gamma integral, and you
> can check the seed satisfies it *without knowing whether Komlós is true*.
> Banaszczyk: yes — γ of a body is computable. Bansal–Jiang: yes, but only through an
> SDP feasibility theorem. The convolution compiler: **no**.

> **T2. Is the legal move a formula, or does it need an existence theorem?**
> Odin's T_v is a formula. Bansal–Jiang needs SDP duality to guarantee a legal move
> exists at each step, and most of the complexity difference between the two papers
> sits in that gap.

**T2 is already a field in the protocol tree** — `move_kind`, formula against
existence-theorem, added for debt D9 from a completely different argument. Two
derivations, one discriminator.

**But the coded field does not reproduce, and that is now measured** (D35, run blind on
all 17 items): Cohen's κ = **0.430** on the 15 items whose recorded text does not state
its own answer, and 0.286 on the two-class subset. All six disagreements run one way —
the first column says *formula* where a blind rater says *existence-theorem* or *no move
recorded* — because the first column asked whether the record's prose reads like a
computation while the rater asked whether the move can proceed before a good object is
shown to exist. The rater's criterion is the better one, and under it the
existence-theorem class goes from 2 of 17 to 6 of 17.

Two consequences, and the second is the one to carry:

* The screen's output is **unchanged** by that reclassification — it still fires on
  `02-cap-set` and `04-kadison-singer` alone — because it is gated on a second, sparser
  field (tightness) that only 2 of 17 items have. The unreliability is masked by the
  coverage bottleneck named in §5, and will bite as soon as coverage improves.
* **Precision 2/2 = 1.000 was never a measurement.** Every case in the corpus is a
  success whose board changed, so with no negative in the scored set every fire is a true
  positive by construction. A figure that survives redefining a third of its input is
  arithmetic, not evidence. Do not quote it as one.

So T2 must be scored on **the object named**, not on the label chosen: the theorem, or the
formula written out. That is the same remedy the D20 run forced on the five-transformation
vocabulary, which scored κ = 0.048 while the computations underneath it were fine.

**And T1 kills a framing this project has leaned on.** "Board change, not a better
player" is not the discriminator: affine spectral independence *is* a board change by
any definition that admits Guo–Fang–Lu's. **Checkability is the discriminator.** The
restatement trap is what makes this sharp — all four models converged on a class closed
under convolution with the terminal property, and one of them *proved* such a class
exists **iff Komlós holds**. It reported that as a finding; it is the diagnosis. The
board is a restatement, and T1 is what catches it.

## 5. How to run this at scale, and what stops it

The screen costs two fields per board and one of them is already written in most
papers' introductions ("the loss comes from iterating…"). The bottleneck is not the
criterion, it is **coverage**: in the protocol tree, the earlier mechanical screen
(existence-type move ∧ bound not tight) was **not applicable to 15 of 17 items** for
want of a filled field, and precision 2/2 on the two it could read.

Filling before-side fields from papers, at scale, checkably, is the task —
which is priority 2, and `ORCHESTRATION.md` answers it with the failure modes this
project has already observed rather than with a hopeful pipeline.

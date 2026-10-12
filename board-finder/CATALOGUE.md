# Five transformations, each with a computation instead of a label

*The catalogue as instruments. The labels scored **κ = 0.048** with three readers
giving three answers to the founding case; the diagnostics below have **never been
tested**. That is the distinction this file exists to keep.*

| # | transformation | what it does | the cheap diagnostic |
|---|---|---|---|
| 1 | **De-tensorize** | an invariant that is multiplicative under the hard-instance product is replaced by an averaging one | **compute I on a product**: I(⊗Sᵢ) against {I(Sᵢ)}. Multiplicative ⟹ the certificate pays a √log; averaging ⟹ it does not. Verified for Banaszczyk → Guo–Fang–Lu in `ANATOMY.md` |
| 2 | **Auxiliary-witness lift** | "S has property P" becomes "∃w attached to S with P′", where w may be rebuilt from scratch at every step rather than transported | **is your invariant hard to transport but easy to re-derive?** Guo–Fang–Lu says outright that the density may change at every step — the witness is never transported, only re-established |
| 3 | **Move work terminal ↔ step** | weight shifts between the terminal check and the per-step check | **which end is doing the work?** Odin's terminal became trivial (symmetric + convex + nonempty ⟹ 0 ∈ K) and all the weight went into the step |
| 4 | **Collectivize a union bound** | per-item control plus a union over m becomes joint control | **does the loss equal m × per-item cost?** This is Bansal–Jiang's affine spectral independence, and case 8's √log n from a union bound over n sets |
| 5 | **Formula-ize the move** | a constrained move plus a feasibility theorem becomes an unconditionally defined operator, pushing the difficulty into the invariant | **does a legal move need an existence theorem?** Bansal–Jiang needs SDP duality to guarantee a legal move at every step; Odin's T_v is a formula. Most of the complexity difference between the two papers sits here, and it is readable from the statement of the board alone |

## Why this is not a rehabilitation of the vocabulary

Two things are true at once and the project has measured both:

* **As labels, these five do not reproduce.** κ = 0.048 over eight after-boards;
  three readings, three labels on Guo–Fang–Lu; one rater applied de-tensorize
  *backwards* on cap set, which is worse than a label that fails to fire.
* **As computations, they have never been run.** Every diagnostic in the right-hand
  column is a calculation on the before-board — a product, a transport test, a count
  of where the loss comes from, a check of whether a move needs a theorem. None of
  them requires agreement on a word.

The protocol tree reached the same split from the other side: its D24 adjudication
found that in three of six rater divergences **the raters agreed on the mathematics
and were forced apart by the wording**, and its D28 test showed a one-line *computed*
criterion beating the labelled rule outright. So the reframing is not a rescue, it is
the same finding arriving twice: **compute, do not name.**

## What to run first

Diagnostic 1 and diagnostic 5 are the two with a closed form, and they are exactly the
two triage questions in `FINDER.md` §3. Run them on the six benchmark boards in
`benchmark.json` — the answers are known, so a proposer that fails them is failing
against ground truth rather than against an opinion.

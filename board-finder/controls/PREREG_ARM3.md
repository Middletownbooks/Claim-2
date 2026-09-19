# Pre-registration — arm 3, the test T3 has not had

Committed before the respondent was given anything.

## Why this run exists

**T3 was derived from the positive control's response.** Validating it on that response
would be the post-hoc patching this programme flags elsewhere: a rule fitted to the item
that produced it. T3 needs an item where I do not already know what a respondent will
compute, and where **T1 and T2 do not settle the question** — otherwise T3 is just
re-detecting them.

The discriminating item is the same problem, the same target, and *the same move*, with
**only the invariant changed**. If T3 is a real test, its answer must differ across that
pair while T1 and T2 do not.

| | arm 1 (already run) | arm 3 (this run) |
|---|---|---|
| target | cube of side C in ℝⁿ | identical |
| move | pass to a convex subset of the union of the two translates | identical |
| invariant | Gaussian measure ≥ ½ | ∃ a density ρ on K with directional total variation V_u(ρ) ≤ κ‖u‖ for all u |
| T3 verdict | **caps at Θ(√log n)** — arm 1 computed this unprompted | ? |

## The input, verbatim

Identical problem paragraph to arms 1 and 2. Then:

> PROPOSED BOARD:
> STATE — a convex body K ⊆ ℝⁿ **together with a probability density ρ supported on K**.
> MOVE — K ↦ a convex subset of the union of its two translates K ± v, for the next
> vector v, carrying ρ along.
> INVARIANT — the density's directional total variation is bounded: V_u(ρ) ≤ κ‖u‖₂ for
> every direction u, with κ a fixed constant.
> TERMINAL — a nonempty symmetric convex body contains the origin.
>
> Run steps 1 and 5 of the instrument on this proposal, including T3. Then answer closing
> field (c).

Nothing in it says what bound the board reaches, that total variation behaves differently
from a measure under products, or that this board is anybody's published work.

## Predictions

| | prediction |
|---|---|
| **A-1** | T1 = **yes** — the invariant is a computable functional of an explicitly given density, checkable on the target without knowing the conjecture |
| **A-2** | T2 = **formula** — carrying a density along the body transform needs no existence theorem, in contrast to arm 1, where the same move needed one |
| **A-3** | T3 = **no cap** — the threshold on the target cube is satisfiable at *constant* side |
| **A-4** | the respondent derives the product behaviour itself: that the directional TV of a product density is an **average** over coordinates rather than a product, so the threshold does not move with n |
| **A-5** | if A-3 fails — T3 reports a cap here too — then **T3 does not discriminate** and is re-detecting whatever T1 and T2 already see. The pair is the whole test, and one arm cannot pass it |

A-2 is the risky one. Arm 1's respondent found that the *same* move needs an existence
theorem, so if arm 3 also answers "existence theorem" then the invariant change alone does
not buy formula-ness, and the anatomy I have been quoting — move unchanged, only the
invariant changed — is incomplete in a way that matters.

## Confounds

Same as arms 1 and 2, plus one: the real result this board comes from is recent, so the
respondent may not have it in training at all. Field (c) records which.

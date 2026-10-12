# Report — arm 3, replicated: two blind respondents, same mathematics, opposite verdicts

A second respondent was given arm 3's input **verbatim**, in a fresh context, tools
forbidden, with no knowledge of the first response. It was launched because the first
relaunch appeared to have died; both returned. This is the **first replication in this
programme** — n = 2 on the same item, rather than n = 1 — and it is worth more than either
response alone, because the two disagree about what they found.

New computations checked in `verify_arm3_replication.py`; the shared ones were already
checked in `verify_response_arm3.py`.

## 1. Every scored prediction replicates, with the same certificate

| | prediction | respondent 1 | respondent 2 |
|---|---|---|---|
| A-1 | T1 = yes | yes, cos² product density | **yes, the same cos² product density** |
| A-2 | T2 = formula | existence theorem, unnamed | **existence theorem, unnamed** |
| A-3 | T3 = no cap | no cap, min κ = Θ(1/C) | **no cap, threshold Θ(1/κ)** |
| A-4 | derives the averaging behaviour | yes, with the optimal constant | **yes, same Fisher information π²/C², same projection bound 1/C** |

Two blind respondents independently produced *the same* witness — g(t) = (1/C)cos²(πt/2C),
I(g) = π²/C², V_u ≤ (π/C)‖u‖₂ by Cauchy–Schwarz on the score, and the matching lower bound
V_u ≥ TV(marginal) ≥ 2 sup ≥ 1/C. That is convergence on a construction, not on a word.

**A-3 is now stronger than after arm 3 alone.** Respondent 2 computed T3 on *three*
invariants for the same board, unprompted: Gaussian measure ⇒ C ≈ √(2 ln n), **capped**;
"O(1)-subgaussian in every direction" (the Gram–Schmidt-walk invariant) ⇒ Θ(√log n),
**capped**; directional TV ⇒ Θ(1/κ), **dimension-free**. So the discriminator separates on a
triple, not just the registered pair, and the third leg was supplied by a respondent that
did not know what was being tested.

**A-2's failure replicates too**, which is the load-bearing point: the same move needs an
existence theorem under *both* invariants, and both respondents say the required lemma is
**not named in the literature**. T2 does not discriminate across this pair; T3 does.

## 2. Respondent 2 locates the cost more sharply than respondent 1 did

It split the move in two, and this is the best statement of T2 either arm produced:

* **Mixing half — a formula, cost exactly zero.** ρ ↦ ρ ∗ ½(δ_v + δ_₋ᵥ). Convolution is
  TV-nonexpansive in every direction, D(ρ∗μ) = (Dρ)∗μ, so V_u can only fall. Mass and
  symmetry preserved, support exactly the union of translates.
* **Convexification half — the unnamed existence theorem, and where everything sits.** The
  union is not convex, so the state must be truncated and ρ conditioned. Conditioning on
  {⟨x,w⟩ ≤ t} multiplies V_u by 1/m and, in the direction ŵ, *adds* (1/m)·f_ŵ(t). Over n
  steps the budget is therefore **O(1/n) of the mass and O(κ/n) of added TV per cut** — every
  cut must live in a collar where the directional marginal is below κ/n. A translation-
  Lipschitz smoothness condition gives no such tail decay, so **the invariant does not pay
  for its own cuts.**

It also gave a cleaner witness that the notch is real than respondent 1's: K = C·[−1,1]ⁿ,
v = 1/√n, x = (C, −C, 0, …, 0) leaves the cube in coordinate 2 under −v and in coordinate 1
under +v, so x ∈ K lies in neither translate.

And a warning worth keeping: proving the conditioning lemma via a Cheeger/KLS-type
inequality would **silently reintroduce a log factor**, since it injects the KLS constant.
A board that looks dimension-free can lose that property in the lemma it outsources.

## 3. The new cap, verified: the box sub-board dies at √n

Respondent 2's second computation, on the only move class expressible in closed form:

* For a symmetric box of half-widths cⱼ, the largest symmetric box inside (K+v) ∪ (K−v)
  **grows exactly one coordinate by |v_{j*}| and shrinks every other by |vⱼ|**. Verified
  here on vertices *and* interior samples in 2 and 3 dimensions — growing two coordinates at
  once fails on a vertex, and growing one by more than |v_{j*}| fails too.
* On that class the invariant specialises *exactly* to **min_j cⱼ ≥ π/κ**, because
  V_u ≤ π·max_j(1/cⱼ)·‖u‖₂ and the bound is tight in the narrowest coordinate's direction.
  Verified. So on boxes the invariant is doing precisely the right bookkeeping — it is a
  faithful, non-circular proxy for the target bound.
* But the move cannot pay: with every vᵢ = 1/√n the demanded shrinkage is
  n(‖v‖₁ − max_j|vⱼ|), against a budget of n(C − π/κ), forcing
  **C − π/κ ≥ √n(1 − 1/n)**. Verified at n = 4…1024, the ratio to √n rising 0.750 → 0.999.

So the board can only work through **non-product bodies and non-product densities** — which
is exactly the slot it leaves blank. Note what this cap is and is not: it bounds the *move
class*, not Komlós. That instance is trivially balanced by alternating signs, as the
respondent says without being asked.

## 4. The disagreement is bookkeeping, and it exposes a hole in the instrument

Respondent 1: **the board is dead.** Respondent 2: **"the proposal survives its kill test."**

They are not disagreeing about mathematics. Both found the same hole:

> **R2:** "the invariant is preserved *exactly* by the do-nothing move K′ = K + v,
> ρ′ = ρ(·−v) (legal, convex, no mass lost, κ unchanged), which destroys symmetry and never
> terminates. **The invariant therefore cannot by itself force the terminal condition.**"
>
> **R1:** the same observation, globalised — translate an entire legal run by any a, every
> invariant value is identical at every step, and the final body misses the origin.

Identical finding. What differs is what they do with it, and the difference traces to a slot
**both** of them marked `none recorded`: COMPOSITION.

* R1 read an empty COMPOSITION as **no constraint**, so the board admits runs that preserve
  the invariant and never reach the terminal ⇒ refuted as written.
* R2 read it as **unspecified** — the content of any real proof would live there — ⇒ "not a
  restatement, not capped, **not yet an argument**."

Both readings are defensible, and the instrument does not say which is right. Step 1 tells a
respondent to write `none recorded` and calls that a finding; step 5's kill test never says
how an empty slot may be used. **So identical mathematics produced opposite verdicts, and
the instrument caused it.**

Fixed in `PROMPT.md`: a refutation must now state whether it exploits a slot the source
**states** or a slot it **leaves empty**, because refuting an absence refutes the write-up
rather than the board. Note this patch is not a T3 patch — D41's moratorium on patching T3
from our own runs stands untouched — and it has better evidence behind it than any T3 clause
ever had: it comes from two blind respondents *disagreeing*, not from one response.

## 5. What the replication settles, and what it does not

**Settles.** T3 discriminates, now on three invariants rather than two. T1 and T2 agree
across the pair, so T3 is not re-detecting them. The cos² certificate is the honest T1 pass,
found twice independently. The board's move needs a lemma nobody can name, twice
independently.

**Does not settle.** Whether the board is dead or merely unbuilt. That question turns on the
empty COMPOSITION slot, which is a defect of my input, not of either respondent — the same
class of error as the dropped symmetry qualifier that `REPORT_ARM3.md` records. Two of the
five slots in the arm-3 input were underspecified, and both underspecifications became the
substance of a respondent's verdict.

The honest summary of arm 3, across both runs: **the discriminator worked; the board I built
to test it was not well enough built to have a verdict.**

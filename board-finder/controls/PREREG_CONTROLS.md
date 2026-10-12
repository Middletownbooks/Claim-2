# Pre-registration — the two controls, before either response is read

Committed before the respondents were given anything. Predictions in §4, scored as
written.

## 1. What is being tested, and what is not

**Tested: does the rubric separate a real board from a restatement?** That is the only
claim the controls carry. If a rubric passes both, or fails both, it is not measuring
board-finding and nothing else in `PROMPT.md` matters.

**Not tested:** whether a model can find a board. That needs the search arm and the
six-item benchmark, and it needs an API key this container does not have.

## 2. The respondents, and the confounds, stated up front

No model access here (debt D18), so each respondent is a **fresh subagent context**
given *only* the triage prompt and *one* control — no repo, no design notes, no sight of
the other control, and no statement of which is positive and which is negative.

Three confounds, none removable here:

1. **Same model family as the author.** Not independent in the way two labs would be.
2. **Trained on this literature.** Banaszczyk's theorem is famous; field (c) of the
   prompt exists to measure that rather than assume it away.
3. **I wrote both the prompt and the inputs.** A leading input can manufacture either
   verdict, so both inputs are below verbatim and can be judged for leading.

## 3. The two inputs, verbatim

### Positive control — a real board with a checkable invariant

> PROBLEM: Given n vectors v₁…vₙ in ℝⁿ with ‖vᵢ‖₂ ≤ 1, choose signs εᵢ ∈ {−1,+1} making
> the signed sum Σ εᵢvᵢ small in ℓ∞. It is conjectured that O(1) is always achievable;
> nothing better than a constant is known as a lower bound.
>
> PROPOSED BOARD:
> STATE — a symmetric convex body K ⊆ ℝⁿ.
> MOVE — K ↦ a convex subset of the union of its two translates K ± v, for the next
> vector v.
> INVARIANT — the standard Gaussian measure of K stays at least ½.
> TERMINAL — a symmetric convex body of Gaussian measure at least ½ contains the origin.
>
> Run steps 1 and 5 of the instrument on this proposal: reconstruct the five slots as
> stated, then answer T1 and T2 and give the kill test. Then answer closing field (c).

### Negative control — a restatement

> PROBLEM: (identical first paragraph)
>
> PROPOSED BOARD:
> STATE — a class 𝒞 of symmetric convex bodies in ℝⁿ.
> MOVE — convolution with ½(δ_v + δ_₋ᵥ) for the next vector v, i.e. K ↦ K ∗ v.
> INVARIANT — membership in 𝒞, which is required to be closed under the move.
> TERMINAL — every member of 𝒞 contains the origin.
>
> Run steps 1 and 5 of the instrument on this proposal: reconstruct the five slots as
> stated, then answer T1 and T2 and give the kill test. Then answer closing field (c).

Neither input says which control it is, neither states a bound for the proposal, and
neither mentions equivalence, restatement, total variation or any paper.

## 4. Predictions

| | prediction |
|---|---|
| **C-1** | the positive control returns **T1 = yes** — the Gaussian measure of a body is computable on the starting state without knowing whether the conjecture is true |
| **C-2** | the positive control returns **T2 = formula** |
| **C-3** | the negative control returns **T1 = no**, and names the reason: a class closed under the move with the terminal property exists **iff** the conjecture holds, so membership cannot be checked without settling the conjecture |
| **C-4** | the negative control is **not** declared a restatement — i.e. C-3 fails. This is my honest expectation for the harder half: the equivalence has to be *derived*, not read off, and the prompt does not hint at it |
| **C-5** | field (c): the positive control is recognised and named; the negative is described as a natural or obvious approach but carries no name |
| **C-6** | if C-3 and C-4 both fail — the negative control passes T1 — the instrument does not discriminate and `PROMPT.md` needs a clause that forces the equivalence question explicitly |

C-3 and C-4 are deliberately contradictory. I am recording both because I do not know
which way this goes, and writing only the one I half-expect would let me claim a hit
either way.

## 5. Scoring

Mechanical: the verdict fields, plus whether the stated *reason* matches. A T1 = no
reached for a wrong reason is scored as a wrong answer with a lucky verdict, and said so.

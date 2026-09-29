# Proof-length interestingness, and why it cannot see this board

*Analysis of Patel, Rammal, Hayat, Munos, Kempe, "Learning to Discover Interesting
Mathematics" (arXiv:2609.28603, 23 Sep 2026; FAIR @ Meta / NYU / CERMICS). Read from a
transcript, not the PDF; no code repository was available and none of their numbers were
re-derived here. Figure and section numbers are as the transcript gives them.*

## 1. What the paper does

It proposes a scalar to optimise in place of human-supplied targets:

```
    I(T | P)  =  100 · V(T | P) / L(T | P)
```

`V(T|P)` is proof difficulty — lines of Lean needed to derive `T` from premises `P`.
`L(T|P)` is conditional description length: statement characters plus the characters of
every definition needed to state it that `P` does not already supply. So: **easy to state,
hard to prove.** Alongside it, an extrinsic measure

```
    U₀(T)  =  |D(T)| · V(T | ∅)
```

— direct downstream users times proof length, read as "lines saved by having `T` for free."

Results: `I₀` and `U₀` correlate at Spearman ρ = 0.756; a 27B Qwen3.6 post-trained with GRPO
predicts `V` better than GPT-5.5 or Claude Opus 4.6 (MAE 20.2 against 31.0 and 34.3, ρ 0.912
against 0.776 and 0.815); training a conjecturer on `I` raises mean verified interestingness
1.76 → 7.58 and drops mathlib containment (judge scores 4–5) from 91.9% to 30.6%; and
interestingness-pruning beats random, proof-length and no-pruning as an inference-time
promotion rule over six rounds.

**The `V(T|P)` primitive is the right object and this project lacked it.** The Bellman
relation `V(T|P) = V(L|P) + V(T|P∪{L})` is a clean formalisation of what a lemma buys, and
premise expansion is a good fix for mathlib's atomisation (median proof 3 lines, median
premise use 1). Their `U₀ = |D| · V` is also, independently, the board-value score
`leanboard/bridge_ledger.csv` was computing — convergent methodology, worth having.

## 2. The blindness that matters here

**`I` is near its floor for every finite-witness problem, which is the entire playable set.**

Proof length in lines does not measure difficulty when the difficulty lives in a *search*:

* **The Shannon artifact** (audited in arm AY). The witness is an independent set in C₁₁²¹³
  with ~10¹⁵⁴ elements. The Lean proof is a handful of lines invoking native Boolean checks
  behind **246 distinct axioms**. Short statement, short proof, real result — `I₀` at the
  floor.
* **Hadamard 668** fails the other way. The proof is either a `decide` one-liner or a
  668×668 literal. One number is ~1, the other ~10⁵, and neither is a measure of anything.

The paper gestures at this in the Discussion — *"proof length in terms of lines of code can
be a stylistic artifact, as automation tactics, such as `aesop` and `grind`, often trade
proof length for runtime"* — and proposes Levin complexity without implementing it. But it
is not a stylistic artifact. It is a **systematic blindness to classes P1 and P2**: every
problem settled by exhibiting an object scores as uninteresting, because the cost is in
finding the object and not in writing the derivation. That is 35 of 499 records in
`classification.json`, including `331`, the only one anyone has actually closed.

### The demonstration, on data already in this repo

The b=0 multiplier-orbit ladder (`Cooperative-AI-Defense`, branch
`claude/hadamard-matrix-methods-vs79hi`, FINDING 160 §6) is a clean test case, because every
instance shares one ansatz — `Σ_k PAF_k(t) = 0` on `4r` orbit signs — so the *statement* is
the same shape at every order and `L` is essentially constant. The written-out proof is also
the same shape: four blocks and a verification. So `V` is roughly constant too.

| solution density | v, d | best floor reached | solved | `I = V/L` | search cost = −log₂ ρ |
|---|---|---|---|---|---|
| 2⁻⁵⁷ | 151, 5 | 32 | yes | ~same | 57 bits |
| 2⁻⁶⁰ | 103, 3 | 32 | yes | ~same | 60 bits |
| 2⁻⁶² | 211, 7 | 32 | no | ~same | 62 bits |
| 2⁻⁷² | 239, 7 | 64 | no | ~same | 72 bits |
| 2⁻⁷⁷ | 191, 5 | 64 | no | ~same | 77 bits |
| 2⁻¹⁰⁶ | 163, 3 | 128 | no | ~same | 106 bits |
| 2⁻¹³² | 487, 9 | 416 | no | ~same | 132 bits |

**The ratio metric ranks this entire ladder as equally interesting.** The real difficulty
spans a 75-bit range and separates solved from unsolved cleanly. Everything that
distinguishes these instances is invisible to `V/L` and fully visible in one number the
project already computes.

## 3. Three things to check before believing the headline

**(a) `I₀` and `U₀` share a factor, and the correlation is not corrected for it.**
`U₀ = |D| · V` and `I₀ = 100 V / L`. **Both contain `V`.** With `V` spanning mean 92.3,
median 49, max 500 across mathlib, part of ρ = 0.756 is shared `V` variance rather than a
relationship between intrinsic and extrinsic value. This is contribution #2 and the whole
"practical surrogate" framing rests on it. The corrections are cheap and unreported:

* partial correlation of `I₀` and `U₀` controlling for `V`; or equivalently
* correlate `|D|` against `1/L` — **that is the non-tautological content** of "easy-to-state
  things get reused";
* and state what fraction of declarations the `U₀ = 0` exclusion drops. Since `U₀ = 0` ⟺ no
  direct users, and the paper itself reports median premise usage of 1, the exclusion is
  large and its size is never given. The dropped set is exactly where *interesting but
  useless* lives, so ρ is measured on the subsample where usefulness is already established.

**(b) The containment result has a confound running in the direction of the claim.**
91.9% → 30.6% is one LLM judge (Claude Opus 4.6, temperature 0) on a 5-level rubric whose
own text concedes *"a generated proof may overlook a more direct existing theorem."* A
statement whose proof the agent found the long way scores as less contained without being
more novel — and an interestingness-trained conjecturer selects for long proofs. No
inter-rater κ, no second judge family, no human calibration. This project paid for that
lesson: the five-transformation vocabulary scored **κ = 0.048** across three raters, and
`move_kind` **κ = 0.430** blind on 17 items. `PROMPT.md` Part B's rule applies directly —
two raters agreeing on a word is not evidence; two raters applying a criterion to a named
object is.

**(c) The reward is gamed in their own showcase.** They patch the conjunction attack
(`T₁ ∧ … ∧ Tₙ` gives `V = O(n)` but `I = O(1)`) and miss the biconditional version.
From Appendix C.3, their *selected* generations:

```
∀ z : UpperHalfPlane, ∃ w, w = -(1:ℂ)/(z:ℂ) ∧ ∀ n:ℕ, n > 0 ↔ (↑n:ℂ) * (z:ℂ) ≠ 0
∀ n:ℕ, n > 0 ↔ ∀ f : Polynomial ℝ, f.natDegree ≤ n-1 → (…)
```

`n > 0 ↔ …` in two of thirteen highlights. The `n > 0` does no mathematical work: it is a
cheap left-hand side that buys both-direction proof obligations, inflating the numerator
while barely touching the denominator. A real fact bolted to a triviality by `↔`. The
number-field example (`x ≠ 0 ↔ ∀ w, |x|_w > 0`) is close to a per-place restatement of a
definition.

## 4. The structural mismatch

**Their metric is defined on solved theorems; this board is unsolved ones.**

Every "discovery" in the loop must be provable *now*, in one Claude Code budget, with
marginal repair. So the system optimises interestingness **conditional on solvability**, and
open problems are the complement of that set. Two consequences:

* `I₀` on Fermat n=3 is computable only because mathlib contains the proof — it is unrolled,
  not predicted. For an open problem `V` is undefined, so **interestingness cannot rank open
  problems at all** except through `V̂_θ`.
* `V̂_θ` is trained on labels capped at 500 lines (mean 92.3, p90 245), and Figure 1 shows
  *all three* predictors underestimating, worse as length grows, **inside** that range.
  A conjecture whose Lean proof would run 10⁵ lines is far outside training support.

Excellent for growing a library. Close to useless for the ranking problem `PLAYABILITY.md`
addresses.

## 5. Proposals for the selection metric

### P1. Stop collapsing to a scalar. Report the pair.

The paper's central problem is that it wants one number to optimise, so it crushes
structurally different difficulties together. Report instead

```
    (  V_arg(T | P)  ,  bits_search(T | P)  )
```

— deductive cost and search cost, separately. `V_arg` is their `V`, which is fine where
argument is the work. `bits_search` is `−log₂ ρ` where `ρ` is the density of witnesses in the
searched space, which is fine where search is the work. §2's table is the argument for this:
the ladder is constant in the first coordinate and spans 75 bits in the second.

This is the project's own idiom. `FINDING 160 §6` reached a size-independent progress measure
(**achieved floor ÷ 32**) precisely by *refusing* to compare raw costs across orders.

### P2. Kill the `↔`-bolt with their own composition axiom.

Their axiom (A3), `V(T|P) ≤ V(L|P) + V(T|P∪{L})`, is stated for inserting a lemma. Point it
at *decomposing the statement* instead. Split `T` at top-level `∧` and `↔` into `T₁…T_k`,
compute each part's difficulty, and define

```
    I_irred(T | P)  =  ( V(T|P)  −  Σ_{i : V(Tᵢ|P) ≈ 0} V(Tᵢ|P) )  /  L(T | P)
```

subtracting difficulty attributable to separable trivia. A statement is **bolted** when
`Σᵢ V(Tᵢ) ≈ V(T)` and some part is closed by `simp`/`rfl`/`assumption` — which is exactly
the triviality check they already run on whole statements, applied one level down. Their
conjunction patch is the `k = n` case of this; `A ↔ trivial` is the `k = 2` case they missed.
Cheap, and it uses machinery they already built.

### P3. Replace degree with reachability in `U`.

`U₀ = |D(T)| · V` counts **direct** users only. A theorem enabling one theorem that enables a
thousand scores as though it enabled one. Use the transitive closure weighted by difficulty:

```
    U_reach(T)  =  Σ_{d ∈ descendants(T)}  V(d | ∅)
```

The leanboard arm already computes dependency closures, so this is available here without new
infrastructure — and it breaks the shared-`V` coupling of §3(a) less badly than `|D| · V`
does, because the sum is over *other* declarations' difficulty.

### P4. The join this board needs — with the sign corrected by `GAP_V3.md`

Their metric says what is **worth** settling. `classification.json` says what is **possible**
to settle. Neither is sufficient alone, so selection wants a product. My first version of this
proposal read

```
    Select(T)  =  I_irred(T | P)  ×  w(class(T))          # WRONG, see below
```

with `w` high on feasible P1/P2. **That has the sign backwards on the class term**, and
`../fallbacks/QUEUE_V3.md` (written in parallel, read after I drafted this) says why:

> *"a problem settled by one explicit finite object in a huge space is, almost by definition,
> one whose frontier is set by search capacity. So the finite-witness screen systematically
> selects for compute gaps, which are the one category that does not improve when models get
> better or cheaper — a model does not add FLOPs."*

So weighting **up** on finite-witness class selects for the gaps that never close. The v3
queue's empty predecessor is the evidence: three targets cleared v2 and all three died on
properties of our position, not of the problem. The corrected form carries a third term:

```
    Select(T)  =  I_irred(T | P)  ×  w_class(T)  ×  g(gap_type(T))
```

* `w_class` stays as a **veto**, not a bonus. **W → 0** (the witness is exhibitable and the
  predicate undecidable, so no amount of interestingness helps); **A → 0** (an algorithm is a
  finite string but its correctness is universal); **U → gated on `V̂` alone**, which is where
  their framework is the only tool and where its extrapolation is least trustworthy. Those two
  zeroes are the contribution `classification.json` makes that no proof-length metric can:
  both classes look tractable to any screen reading the quantifier vocabulary, and both are
  dead.
* `g(gap_type)` is where the *positive* weight lives, and `GAP_V3.md` already defines it:
  algorithmic-idea and breadth gaps over compute gaps. FunSearch improving the cap-set record
  is the existence proof that the first two move under model capability.

**The witness class says what can be settled. The gap type says what will move.** My draft
conflated them and put the weight on the wrong one.

### P4b. Two convergent confirmations, recorded because they were independent

The frontier sweep added a `depthOrBreadth` field to `classification.json` in the same week I
derived a deep-versus-broad screen in `FEASIBILITY.md` §6 from the Hadamard correction. Two
derivations, one discriminator — the same pattern `FINDING.md` §4b notes for `move_kind`. The
sweep's verdicts on the two records I had staked claims on:

| record | sweep | my claim | outcome |
|---|---|---|---|
| `331` Hadamard | **BROAD**, PRIMARY-VERIFIED-LOCALLY | breadth-shaped, demonstrated | confirmed |
| `280` Kaplansky idempotent | **DEEP**, CORRECTED | "the strongest single target" | **corrected** |

The Kaplansky correction matters: its wall note records that nobody has pointed a search at
the idempotent conjecture specifically, and that the field's own next target is elsewhere. A
DEEP gap with no community search behind it is not the same as a breadth gap an agent can
sweep, and I rated it as though it were.

The sweep also picked up `FEASIBILITY.md` §1's factorization of record `488` and rated the
combinatorial factor **`488b`: FEASIBLE** while leaving the direct record **HOPELESS** — as a
sub-target rather than a re-rate, with the reason stated in `classify.py`'s `merge_sweep`
docstring: collapsing them would assert the record is feasible when only one factor is. That
is P1 (report the pair, do not collapse) applied before P1 was written down.

### P5. Use the ladder to *calibrate* difficulty estimates, not to train a predictor.

The paper's strongest transferable result is negative and aimed at this project: **frontier
models are badly calibrated on proof difficulty and all of them underestimate, worse as
difficulty grows.** `FEASIBILITY.md`'s `witnessCheckFeasible` column is exactly that kind of
judgment, produced exactly that way, and the Hadamard cell was wrong by an order of magnitude
in the decision-relevant direction.

The tempting response — train a `V̂_θ` on the b=0 ladder — does not survive arithmetic. They
used ~100k premise-expanded points; the ladder has on the order of fifteen labelled
instances. **What the ladder can do is serve as a held-out calibration set**: density,
achieved floor ÷ 32, and solved/unsolved are ground truth, so any difficulty estimate a model
emits can be scored against them. That is the missing evaluation for the feasibility column,
it needs no training run, and per FINDING 162 the target must be a **success probability per
restart** rather than a time, because the distributions are bimodal.

## 6. What is not checked

* Read from a transcript. No PDF, no code, no re-derivation of any reported number.
* §3(a)'s coupling argument is algebraic and solid; the *size* of its effect on ρ = 0.756 is
  unknown and needs their data.
* P2's decomposition test is untried. The failure mode to watch is statements where the
  `↔` halves are genuinely interdependent, which the test would wrongly flag as bolted.
* P4's corrected form is untested. `g(gap_type)` exists as a rubric in `GAP_V3.md` and has
  never been scored against outcomes, because the v3 queue has not run.
* P1's `bits_search` is only defined where a search space and a density estimate exist. That
  is true for the Hadamard ladder (`density4.py`, `validate2.py`, validated to ≤0.3 bits at
  D=3,5,7) and false for most of the 35 playable records.

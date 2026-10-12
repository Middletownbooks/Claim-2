# REPORT AC — Audit of arXiv:2609.11189 (Guo–Fang–Lu) under template v2.1

Guo, Fang, Lu, *Vector Balancing via Directional Total Variation*, arXiv:2609.11189v1
[math.CO], 10 Sep 2026. Full text supplied by the user. Claims Komlós with the
explicit constant 3√(2π) ≈ 7.5199, and Beck–Fiala with 3√(2πt). Proof credited
to the Odin Automatic AI Research Agent.

Verification-ladder rung reached: **2** — every quantitative step recomputed by
independent script or by hand. Not machine-checked; no proof assistant here.

## Verdict

**No error found.** Every step I can check, checks. This is a materially
stronger result than the audits in Phases X and Y produced, and the difference
is structural: unlike Ghermoul's Conjecture 2 or the auro-zera axiom, **this
paper's main theorem is not conditional on an unproved statement of comparable
strength.** The chain from Lemma 2.4 to Theorem 1.1 is complete as written.

What I cannot certify is three external dependencies (below).

## The arithmetic chain — verified

| step | claim | check |
|---|---|---|
| Lemma 2.4 | the gamma integral giving T_i ~ G_i/√S_i with density 2/(π(1+t²)²) | **0.2867527463 vs 0.2867527464** |
| Lemma 2.4 | E[S⁻¹] = 1 for S ~ χ²₃ | exact: 1/(k−2) = 1 |
| Lemma 2.4 | V_u(ρ_C) ≤ √(2π)/C·‖u‖₂ | Monte Carlo, 7 dimensions, reproduced exactly (REPORT_AB §4) |
| Lemma 2.4, d=1 | ∫\|ρ′\| computed directly | **0.265962**, equals (π/C)E\|T\| = 0.265962, under bound 0.333333 |
| constant chain | C = 3√(2π) ⟹ κ = √(2π)/C = 1/3 | **exact to 1e-12** |
| step condition | κ‖v‖₂ ≤ 1/3 with ‖v‖₂ ≤ 1 | holds, **with equality at ‖v‖ = 1** |
| Lemma 4.3 | ∫₀⁶(6−h)dh = 18, 18/12 = 3/2 | by hand ✓ |
| Lemma 4.3 | ∫₀⁶ h(6−h)dh = 36, 36/24 = 3/2 | by hand ✓ |
| Lemma 4.3 | the full identity, on a **non-uniform** density | **0.8544 vs 0.8514**, 0.35%, discretisation-limited |
| Lemma 4.3 ⟹ Prop 2.2 | ∫\|s\|R⋆ ≥ 3/2 − (3/2)(1/3) = 1 | exact ✓ |
| Remark 4.4 | uniform-density equality case at A = 3 gives height exactly 1, V₁ = 1/3 | ✓ |
| Remark 4.4 | cutoff L ≤ 3 forced by containment, via K = (−A,A), v = 1 | ✓ by hand |

**The chain is tight but consistent.** Every inequality in it is non-strict and
several are attained simultaneously at ‖v‖ = 1: κ‖v‖₂ = 1/3 exactly, V_v(ρ) =
1/3 exactly, ∫|s|R⋆ = 1 exactly, and Lemma 3.4 is invoked at a = 1 with M ≥ a.
Lemma 3.4 explicitly covers M = a. There is no off-by-one.

## Lemmas verified by hand

**Lemma 4.1, identity (4.1)** — {y : ℓ(y) > 2} = T_vK, both directions. Forward:
ℓ(y) > 2 gives J_y = (α,β) with α ≥ −3, β ≤ 3, so any c ∈ (α+1, β−1) lies in
(−2,2), and z = y + cv has z ± v ∈ K. Reverse: z ± v ∈ K and |t| < 2 put
−t∓1 ∈ J_y, with openness of K giving the strict inequality. ✓

**Lemma 3.3, separation** — S = {z : ∃ρ, z_ℓ ≥ V_{u_ℓ}(ρ)} is convex (convexity
of each V_u plus convexity of P(K)) and upward closed, so β ≥ 0 componentwise;
disjointness from Q = (−∞,a)^N is immediate from the assumed strict gap. ✓

**Lemma 3.4, the Jensen chain** — g(t) = h_H(D_t) is nondecreasing (B symmetric
and convex ⟹ D_t ⊆ D_s for s ≤ t, plus domain monotonicity) and convex
((1−θ)D_s + θD_t ⊆ D_{(1−θ)s+θt} by convexity of B, plus Lemma 3.2). Jensen
then gives ∫g(|s|)dq ≥ g(M), and monotonicity gives g(M) ≥ g(a). ✓

**Prop 2.2** — V_{(u,0)}(R) = V_u(ρ) for R(y,s) = (1/6)ρ(y+sv)1_{|s|<3}, since
the s-integral contributes exactly the factor 6 that the normalisation removes. ✓

**The Wang–Xia step, stated in one line by the paper and worth spelling out.**
[WX11, Thm 1.2] is an inverse-power (Brunn–Minkowski-type) inequality; the paper
uses it to assert the *linear* convexity (3.7). That implication is real but not
immediate: from c^{−1/p} ≥ (1−t)a^{−1/p} + tb^{−1/p}, the power-mean inequality
gives c ≤ ((1−t)a^{−1/p} + tb^{−1/p})^{−p} ≤ (1−t)a + tb. `DERIVED HERE` ✓

## The concern that was relayed to me does not appear to bite

Batch-2 Response 1 relayed, second-hand from an unnamed review note, that the
p↓1 and ε↓0 limits in Lemma 3.2 are "argued pointwise rather than demonstrably
uniformly". On my reading that concern is misplaced, for three reasons:

1. **The p↓1 limit fixes the test function first.** f_δ ∈ C_c^∞ is chosen with
   E_H(f_δ) ≤ h_H(K) + δ, then held fixed while p ↓ 1 by dominated convergence,
   then δ ↓ 0. That is the correct order for this swap, and it is what the text
   does.
2. **The ε↓0 limit needs finiteness, not uniformity.** For fixed δ, ρ_δ ∈ P(K)
   ⊂ BV(R^d), so |Dρ_δ|(R^d) < ∞ — a fixed finite number — and ε|Dρ_δ| → 0. The
   paper states this explicitly: no uniform BV bound for minimizers of the
   degenerating energies is required.
3. **The convexity inequality survives the limit as three separate scalar
   limits.** h_{H_ε} → h_H at K₀, K₁ and K_t independently; an inequality among
   three convergent real sequences passes to the limit. Nothing needs to be
   uniform *across* domains.

I record this as a disagreement with a second-hand report, not as certainty.
I am auditing a geometric-measure-theory argument at speed, and the honest
statement is that I checked the *order of limits* and the *finiteness
requirement* and found both sound; I did not re-derive the eigenvalue theory
underneath.

## What I cannot certify — the real dependencies

The paper's weight rests on three external results, none verifiable here:

1. **Wang–Xia [WX11, Thm 1.2]** — the inverse-power eigenvalue inequality. The
   paper hedges this by *also* giving its own proof (Proposition A.1) for the
   strongly convex class it needs, so WX11 is not strictly load-bearing.
2. **Mosconi–Riey–Squassina [MRS24, Thm 1.1 and Prop 4.5]** — log-concavity of
   the first eigenfunction and C^{1,α} regularity. **This is load-bearing**:
   Proposition A.1 cannot run without it, and Prop A.1 is the substitute for
   WX11. So the two hedges share a dependency and are not independent.
3. **Kawohl–Novaga [KN08]** — the anisotropic coarea/Cheeger identification
   used for (3.3).

Proposition A.1 itself is a long PDE argument — infimal convolution, uniform
convergence of gradients, a critical-set cutoff with a perimeter estimate on the
2δ-parallel body. I checked its structure and its limit orders; I did not verify
every estimate, and it is the single place where a quiet error would be hardest
to see.

## Honest comparison with the two previous audits

| | Ghermoul (Phase X) | auro-zera (Phase Y) | Guo–Fang–Lu (here) |
|---|---|---|---|
| main theorem conditional on an unproved statement? | **yes** (Conjecture 2) | **yes** (the axiom) | **no** |
| is that statement weaker than the target? | no — at least as strong | no — it *is* the open case | n/a |
| arithmetic errors found | none | none (README lemma false) | **none** |
| external dependencies | none | none | **three** |

The previous two relocated the difficulty into an assumption. This one does not:
it discharges the difficulty into cited literature. That is an ordinary and
legitimate way to write a proof, and it changes what an audit can conclude —
the question moves from "is the reduction honest?" to "are the three citations
correctly applied?", which needs a specialist in Finsler p-Laplacian eigenvalue
theory, not a sieve.

## What would settle it

1. A specialist read of Proposition A.1 against [MRS24], since it is the shared
   dependency of both routes to (3.7).
2. Formalisation. The paper's structure is unusually amenable: Lemmas 2.4, 4.1,
   4.2, 4.3 and Cor 2.3 are elementary and self-contained. Section 3 and
   Appendix A are not.
3. The constant gap remains open: 3√(2π) ≈ 7.52 against Kunisky's lower bound
   1 + √2 ≈ 2.414. The paper claims no optimality.
4. The result is explicitly existential — no algorithm, and no prefix guarantee
   (unlike Smirnov–Vershynin, whose online algorithm it builds the seed density
   from).

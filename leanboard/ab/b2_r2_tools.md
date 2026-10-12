I'll start by reading the design skill, since the deliverable will be a published report page, and then check the compute environment for the experiments.Literature context is sufficient. Now the core computational work: I'll implement the candidate board's potential with exact analytic derivatives and verify them before running any experiments.Exceeded the time limit; I'll run it in the background per family and write progress to disk.Numeric overflow and a vacuous regime at small log n (the constants make the method trivially satisfied until log n is huge). I'll redo it in log-space over a much wider range.Adverse selection appears in the late phase (ratio 1.12→1.70 for sparse instances). Before attributing it to blocking, I need a control: the same measurement on an unblocked walk.The background job was killed when its shell exited. Restarting it detached, with unbuffered output.E4 is running. Meanwhile, E8b tests a possible repair for C5: a "fair-freezing" move that biases motion (within the same legal subspace) toward columns carrying dangerous mass.Biasing reduces but does not remove the adverse selection (1.72 → 1.24), which is informative. Next, E9 records potential trajectories and how the loss is distributed across rows, for the plots.I hit the tool limit before building the published report page, so here is the research summary in chat. The experiments ran; one batch (E4) finished only 4 of its 6 instance families.

## Verdict up front

**BOARD CHANGE CANDIDATE.** I found a different, composable board. It is a *lossless* reformulation: it is sandwiched between disc ≤ K−ε and disc ≤ K. Each move is an eigenvector computation instead of an SDP, and the union bound is replaced by a product. What remains unproved is a uniform, constructive bound on a "curvature budget." My experiments show that budget is zero on generic instances but not on structured ones near the feasibility threshold.

I also found a sharp negative result about the existing board: its (log n)^{1/4} exponent survives perfect independence. So refining affine spectral independence cannot beat it.

**External information found during search** (not used as a source of ideas):
- Guillen–Kobzar, arXiv 2609.15071, submitted 14 Sep 2026. They show that if the signs may be any unit-modulus complex numbers, the inequality holds with a finite explicit constant, and their paper builds on Bansal–Jiang via the Burkholder formalism and the Bellman function method. I read only the abstract. My strongest candidate is Bellman-flavoured and may overlap with their paper.
- Altschuler–Tikhomirov (July 2026) extend offline Beck–Fiala to d ≥ log(T)^{1+o(1)} via an efficient online algorithm that minimizes prefix discrepancy.

## A. The existing board [SOURCE, with my inferences marked]

- **State:** the fractional coloring x_t, the alive set V_t, and a per-scale classification of rows into large, medium and small. It also includes the regularized discrepancies Y = ⟨a,x⟩ + β Σ a_j²(1−x_j²) with β = b/10, and the set of dangerous rows.
- **Move:** dx = Σ_t dW_t, where U_t comes from an SDP. U_t must be orthogonal to dead coordinates, large rows, the E-rows of dangerous rows, and x itself. It must also satisfy spectral independence and affine spectral independence.
- **Invariants:**
  - ‖x_t‖² = t, which is conserved and acts as a progress clock.
  - Y ≤ 2b for every medium row, enforced deterministically by blocking.
  - The number of dangerous rows is at most |V_t|/10 (the capacity invariant).
  - The dangerous mass passing through any column stays small, with high probability, via the decoupled potential Φ.
- **Terminal:** when |V_t| ≤ 10, round the remaining coordinates.

**Works/stuck.** The old board works because blocking a dangerous row costs only one dimension, and decoupling shows that column by column few rows ever become dangerous. It gets stuck because that column statement must hold with probability 1−n^{-4} for *every* column, since V_t is adaptive. At the critical sparsity k ≍ b², a column contains only ≍ b² rows, and Chernoff can reach n^{-4} only if b⁴ ≳ log n.

**Where the logs enter.**
- **√log n:** in the small-row union bound, which forces μ ≥ b²/log n.
- **log n:** in the per-column decoupling term α·λ·log n/θ.
- **loglog n:** from the P = O(loglog n) scales and from the choice λ = loglog n/b.

**Artifacts versus necessities** [INFERENCE, backed by experiments]:
- *Artifacts:* the multi-scale split, the fixed β, the global (rather than local) affine SI, and counting "ever dangerous" rows.
- *Near-necessary within this architecture:* the per-column worst case over V_t (E8) and the exponent itself (E6).

**E6: the exponent persists even under perfect independence.** I solved numerically for the smallest workable b under three accountings. The fitted exponents of log n were:

| Accounting | Fitted exponent |
|---|---|
| Bansal–Jiang's own | 0.262 |
| Same with α = 1 | 0.259 |
| Perfect independence with full Gaussian row tails | 0.254 |

The binding constraint is the per-column union bound, not α.

**E7: global versus local affine SI.** A generic diffusion matrix has global α ≈ 2·m′/rank. For example, at h=480 the global α is 7.95 against a local maximum of 3.85. The proof only consumes the local condition (principal submatrices on column neighbourhoods), but E6 shows fixing this saves only loglog factors.

**E8: blocking causes adverse selection.** Under blocking, alive columns carry disproportionately more dangerous mass late in the walk:

| Alive fraction | Blocked walk | Unblocked control |
|---|---|---|
| (0.25, 0.50] | 1.12 | 0.92 |
| (0, 0.25] | 1.70 | 0.93 |

So orthogonality keeps dangerous columns alive. Biasing motion toward those columns only reduces the late-phase ratio to 1.24.

## B. Candidate catalogue

| Candidate | Provenance | Invariant / move | Obstruction | Status |
|---|---|---|---|---|
| C1 Banaszczyk body | LITERATURE | γ(K) ≥ ½; K ↦ K∗u | Terminal extraction (γ ≥ ½ ⇒ 0 ∈ K) forces √log m for the cube | Fails for Komlós |
| C2 Exact conditional expectation | INFERENCE (classical) | F(x) = P(ξ ∈ good) is multilinear; pinning a coordinate never lowers it | Trivially composable, but F(0) > 0 *is* the theorem | "Stupid move, useless invariant" |
| C3 Heat-ledger board | NEW (possible Bellman overlap) | Product of Gaussian survival probabilities; curvature-nonnegative moves | Doomed states; tight-frame curvature deficit | Strongest; see C |
| C4 Local affine SI | INFERENCE from SOURCE | Affine SI only on column neighbourhoods | E6: exponent unchanged | Negative |
| C5 Fair freezing | NEW | Dangerous mass on V_t ≤ εμ\|V_t\| | E8: adverse selection | Partially repairable, unproved |
| C6 Stochastic localization | LITERATURE | Measure-valued martingale | Reduces to C2/C3 when the measure is a product | Collapses |
| C7 Rank-2 → rank-1 rounding | Prompted by external work | Collapse complex phases to signs | Not developed (provenance) | Open |

Two related literature results I verified: Banaszczyk's theorem is equivalent to the existence of O(1)-subgaussian distributions over signed combinations, and regularization frameworks can re-interpret results from Spencer's theorem to Banaszczyk's bounds.

## C. Strongest candidate: the heat-ledger board

**State.** Each row i is a *particle* (y_i, s_i) in the upper half-plane, with y = Ax and s = (A⊙A)(1−x⊙x).

**Invariant.** Let h(y,s) = P(|y + √s·g| ≤ K), and define the product potential F̃ = Π_i h(y_i, s_i), with Ψ = log F̃.

**Transformation.** Because h solves the backward heat equation h_s = ½h_yy, moving a single coordinate leaves each h_i a martingale up to Lindeberg corrections. The drift of F̃ is ½⟨∇²F̃, U⟩.

**Legal move.** Choose U ⪰ 0 supported on alive coordinates with ⟨∇²F̃, U⟩ ≥ −κF̃. In the deterministic variant, use a direction u ⊥ ∇Ψ, which kills the martingale part.

**Terminal.** When s = 0, F̃ is exactly the indicator that disc ≤ K.

**Budget lemma** [INFERENCE, elementary]. If ∫κ ≤ B almost surely, then P(success) ≥ F̃(0)·e^{−B}. Since F̃(0) = Π(1−p_i) > 0 for every K, this is multiplicative, LLL-style accounting with no union bound anywhere.

**Completeness** [INFERENCE]. If disc(A) ≤ K−ε with witness x\*, consider the rank-one walk x_t = W_t·x\*. Along it the budget is finite, because rows with margin make h → 1 smoothly. So the board loses nothing, and the whole conjecture becomes a *uniform, constructive* budget bound.

**Exact identities** [verified in E1 to ~1e-10]:
- At x = 0 the Hessian is purely off-diagonal, hence traceless, so a good move always exists at the start.
- For rows with |y| < K, write r₂ = h_yy/h and ℓ_yy = (log h)_yy. Then r₂ < 0, ℓ_yy < 0, and
  $$u^\top\nabla^2\Psi\,u=\sum_i |r_2^i|\sum_j a_{ij}^2u_j^2-\sum_i|\ell_{yy}^i|\langle a_i,u\rangle^2+X(u),$$
  where X(u) is the Lindeberg correction term. This is a single scalar inequality, versus BJ's matrix inequalities.

**Link to Bansal–Jiang** [NEW observation]. Each row's gradient is ∇ℓ_i = ℓ_y·(a_i − 2β_i·a_i⊙a_i⊙x) with β_i = ℓ_s/ℓ_y. So BJ's E-rows are per-row gradients of this potential. In the tail regime, β_i ≈ (K−y)/(2s); E10 found ratios of 1.000 to 1.006 at large z, which matches BJ's β ≈ b/10 up to constants.

In short: BJ block each dangerous gradient, paying in dimension. This board pays for dangerous rows in drift instead, with no capacity constraint.

**Why it is not free.** The Gaussian surrogate lies at doomed states (bounded support versus Gaussian tails), and κ blows up there. The sum potential also concentrates slack: in E9, the three worst rows held 28% to 96% of the deficit.

## D. Computational falsification (actual results)

**E3, curvature walk at n=32.** Fraction of steps whose best legal direction still has negative curvature:

| Instance | K=1 | K=1.5 | K=2 |
|---|---|---|---|
| Gaussian | 0.00 | 0.00 | 0.01 |
| Hadamard | 1.00 | 0.48 | 0.04 |
| Simplex | 0.99 | 0.33 | 0.00 |

For Hadamard, K=1 is infeasible: n=32 is not a perfect square, so no bent functions exist.

**E4, n=20 with exact optima.**
- The failure fraction is a threshold phenomenon near the optimum. For orthogonal m=n instances it was 0.89, 0.32 and 0.05 at K/opt = 1, 1.1 and 1.25.
- Best disc/opt achieved by each method:

| Instance | Curvature walk | Potential-greedy | Blocking walk | Random walk |
|---|---|---|---|---|
| Gaussian | 1.056 | 1.021 | 1.07 | 1.486 |
| Orthogonal | 1.054 | 1.074 | 1.112 | 1.254 |

- Potential-guided sign choice does most of the work at these sizes.
- Killing the martingale part with a random ∇Ψ-orthogonal direction alone performs poorly (1.42 on Gaussian instances).
- The simplex and Hadamard-16 families did not complete.

**E10, stochastic criterion.** Share of visited states where no U whatsoever gives non-negative drift:

| Instance | Share |
|---|---|
| Hadamard, K=1 | 55% |
| Hadamard, K=1.5 (feasible) | 22% |
| Gaussian | 0% |

So the purely monotone board is **false**; a budgeted version is required.

**Limitations.**
- The sizes are tiny: n ≤ 32 for the potential walks and n ≤ 600 for E7.
- No SDP solver was available.
- None of this is asymptotic evidence.
- The discrete implementation (finite steps plus brute-force rounding of the last 4 coordinates) sits outside the continuous theory.

## E. Proof obligations

- **Established:** the drift identities; the sign facts; tracelessness at 0; the budget lemma; completeness; the BJ β correspondence; exponent persistence (numerical, idealized model).
- **Plausible:** a drift lemma when the number of curvature-relevant rows is at most (1−c)|V|, via their Gram nullspace.
- **Conjectural:** a budget B = O(Σp_i·polylog) for a local eigenvector rule with light blocking.
- **Major unknowns:**
  - Doomed-state avoidance, i.e. a per-row margin invariant compatible with the product potential.
  - Paying the tight-frame (flat-spectrum) curvature deficit.

## F. Final question

The simplest representation I found is this: **rows as heat particles** (y_i, s_i) in the half-plane. A coordinate move diffuses each particle horizontally by a_ij² while lowering its variance by a_ij², so each survival probability h(y,s) is (nearly) conserved in expectation.

The "almost stupid" move is: take the top eigenvector of ∇²F̃ restricted to alive coordinates, i.e. make the particles' survival events non-negatively correlated. At x=0 this is guaranteed by tracelessness. The terminal certificate is s = 0, where h becomes an indicator.

The entire Komlós difficulty then sits in one place: keeping particles away from the corners (y,s) = (±K, 0) while the curvature budget stays uniformly bounded.

I can turn this into the full published report with charts from the saved data if you'd like.
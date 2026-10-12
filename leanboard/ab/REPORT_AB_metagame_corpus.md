# REPORT AB — Four LLM responses on Komlós board-change: what the corpus shows

Corpus: two no-tool responses to one prompt (batch 1), two tool-enabled
responses to a slightly different prompt (batch 2). User's stated intent: scout
whether "board-changing transformations" is a promising meta-game area — not a
controlled tools-vs-no-tools experiment. The two batches vary tool access and
prompt wording together, so no causal attribution between them is made below.

## 1. External verification (done here, not taken on trust)

| claim | source | verdict |
|---|---|---|
| arXiv:2609.11189 Guo–Fang–Lu, *Vector Balancing via Directional Total Variation*, 10 Sep 2026, Harvard; 3√(2π) Komlós bound; κ‖v‖₂ ≤ 1/3; proof credited to an automated agent | b2-r1 | **REAL**, description accurate |
| arXiv:2607.08943 Guillen–Kobzar, *Online Komlós converges to mean curvature flow* | b2-r1 | **REAL** |
| arXiv:2609.15071 Guillen–Kobzar, *The Komlós conjecture for complex discrepancy*, 14 Sep 2026 | b2-r2 | **REAL** |

**Zero fabricated citations.** The apparent conflict — two different Guillen–
Kobzar IDs with different content — resolves: they are two genuinely different
papers, and each response cited the one it found. The expected failure mode for
tool-enabled literature claims did not occur here.

## 2. The convergence result — the strongest datum in the corpus

All four responses, with no coordination, land on the **same board**: state = a
measure or density on ℝᵐ; move = convolution with ½(δ_v + δ_₋ᵥ), or the
equivalent convex-body transform.

| response | its name for it |
|---|---|
| b1-r1 | paired convolution densities (f, g), f ≥ θᵐ g |
| b1-r2 | "the convolution compiler", stated explicitly as the unique stupid move |
| b2-r1 | Banaszczyk body + density of bounded directional total variation |
| b2-r2 | heat-ledger: product of Gaussian survival probabilities |

4/4 convergence. And the **real** result (Guo–Fang–Lu) lives in exactly that
space: convex body + density, with a directional-variation invariant preserved
*exactly* under the transform.

This cuts two ways and both matter. The area is real and findable — four
independent models and one automated research agent converged on it. But
"findable by everyone" is the opposite of a private edge: the board was not the
scarce thing.

## 3. The sharpest finding — a confident impossibility claim contradicted by
##    a paper published five days earlier

b1-r2 (no tools) asserts **Horn 1**: any class certified by smooth/analytic data
and closed under convolution with every unit v "forces the certificate to factor
through the subgaussian comparison", hence has a provable Θ(√log) floor. It
presents this as established, not conjectural, and builds its NEGATIVE verdict
on it.

Guo–Fang–Lu's class — densities of bounded directional total variation — is
analytic, is closed under the transform, and reaches O(1).

Inspecting Horn 1's argument: it enumerates MGF majorants, moments, log-concave
relaxations and Gaussian-measure comparisons, then asserts *all* smooth
certificates reduce to those. Directional total variation is an L¹ derivative
norm — not a moment functional, not a function of Σ. The word "forces" carries
the entire argument and is unsupported.

**So a well-dressed impossibility theorem from the no-tools arm is, as stated,
false**, and the counterexample was on arXiv five days before the response was
written. This is the cleanest instance in the corpus of the failure mode this
programme keeps finding: every written step defensible, the quantifier doing the
real work left unchecked.

## 4. Verification asymmetry — a correct experiment with near-zero power

b2-r1 ran a Monte Carlo check of Guo–Fang–Lu's seed-density constant
(E[|Σ uᵢTᵢ|] ≤ √(2/π), Tᵢ = Gᵢ/√Sᵢ, Sᵢ ~ χ²₃) across seven dimensions and
reported it as independently verified.

**Reproduced here exactly** — my estimates match theirs at every d (d=1: 0.6369
vs their 0.6373; d=1000: 0.7899 vs 0.7888). The experiment is genuine and
honestly reported.

But the quantity has a closed form the response did not notice. Tᵢ = t₃/√3, so
**Var(Tᵢ) = 1 exactly**, so Σuᵢ Tᵢ has variance 1 for every unit u. The claimed
"bound" √(2/π) **is** E|N(0,1)|, and the paper's claimed asymptotic tightness is
just the CLT. The exact d=1 value is 2/π = 0.63662 (their estimate sits 0.8 s.e.
away).

So the check verified a statement that is near-automatic, and whose tightness is
a triviality — while the response itself correctly flags that it could *not*
check the crux (the p↓1, ε↓0 double limit in the Cheeger-convexity argument).
The checking was sound; the *selection* of what to check is where the
information was lost. Same lesson as Phases V and W: commission checks pass
while the load-bearing step goes untested.

## 5. Honest self-assessment, compared

Both no-tool responses and one tool response independently reached the same
negative conclusion about their *own* novel candidate: it relocates the
obstruction rather than removing it.

* b1-r1: its f ≥ θᵐ g invariant is conjectural; exhibits two explicit
  counterexamples showing Fisher information and log-concavity are insufficient.
* b2-r1 (C2, free-energy board): the cross term reduces to affine spectral
  independence "verbatim, not a relabeling".
* b2-r2: reports E10 showing the purely monotone version of its own board is
  **false** (no legal U at 55% of visited Hadamard states), forcing a budgeted
  variant.

b2-r2 is the most experimentally honest of the four — it ran real experiments
that produced real negative results about its own proposal, at tiny sizes it
declares (n ≤ 32). It also hit a tool limit and never produced its deliverable.
b2-r1 produced the most polished artifact and the most accurate retrieval.

## 6. What this says about the meta-game area

**The area is promising and the specific window has probably just closed.** The
board all four converged on is now a published claimed theorem. What remains
open is not board-finding but board-*checking*:

1. Guo–Fang–Lu's crux — the Minkowski-convexity-of-the-anisotropic-Cheeger-
   constant argument through the degenerate-norm double limit — is flagged by
   b2-r1 as externally questioned and was not verified by anyone in this corpus.
2. The constant gap: 3√(2π) ≈ 7.52 against Kunisky's lower bound 1+√2 ≈ 2.414.
3. The result is explicitly existential; no algorithm is given.

That is precisely the shape of work this programme has already done three times
(Phases X, Y, Z: Ghermoul, auro-zera, and the Salez sieve) — audit a fresh
claim, verify what is checkable, and locate where the claim's weight actually
rests. The recommendation is to point the same instrument at 2609.11189 rather
than to search for another board.

Note the additional meta-game fact: **2609.11189 credits its proof to an
automated research agent.** If it holds, the interesting datum is not that a
board was found but that an agent found one and a human programme's edge moved
entirely to verification.

## 7. Limits of this analysis

n = 4, two prompts, unknown models, and the batches confound tool access with
prompt wording — no causal claim is made about what tools did. Batch-1
Response 1 was captured with a visible reasoning trace and Response 2 without,
so the two are not like-for-like documents. Batch-1 Response 2's comparison
table is structurally empty (placeholder cells) and was treated as missing data.
Both format facts were recorded in MANIFEST.md before this analysis was written.

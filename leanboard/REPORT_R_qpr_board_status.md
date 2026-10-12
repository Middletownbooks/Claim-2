# Report R — Is Quantum Parallel Repetition a New Board?

Reconnaissance on `openai/ten-proofs`, commit `94bc0fe` (clone 2026-09-09),
Lean 4.32.0, mathlib pinned at `v4.32.0`. Provenance tags follow the Phase Q
convention. Nothing is Lean-checked: `elan` remains egress-blocked, so every
claim is about source text and graphs.

---

## 13. Verdict (stated first)

$$\boxed{\text{TREAT QPR AS SUB-BOARD}}$$

And the more consequential finding, which is not about QPR:

> The value of `ten-proofs` is not that it contains a third board. It is that it
> is a **controlled population** — ten developments, one producer, one
> toolchain, one period, spanning sphere packing to quantum games — which holds
> the production process constant while mathematical distance varies. That is
> precisely the design Phase Q lacked, and it has already yielded a result
> Phase Q could not obtain.

---

## 1–2. Audit

`DIRECTLY OBSERVED`. The first structural fact settles much of the ontology and
is visible before any analysis: **each of the ten results is a single `.lean`
file.** There is no module dependency graph, where FLT has 60 474 modules and
NS 2 484.

| | FLT | NS | QPR |
|---|---|---|---|
| Lean / mathlib | 4.33.1 / v4.33.0 | 4.34.0-rc2 | **4.32.0 / v4.32.0** |
| files | 60 474 | 2 484 | **1** |
| declarations | — | 49 379 | **2 638** |
| theorems | 48 503 | 37 330 | **1 813** |
| own definitions | 8 015 | 8 392 | **822** |
| mathlib declarations used | 25 413 | 2 486 | **581** |
| comment lines | ~0 | ~2% | **0** |
| `sorry` / `axiom` / `native_decide` / `unsafe` | 0 | 0 | **0** |

All ten files are free of `sorry`, `admit`, `axiom`, `native_decide`,
`unsafe`, `partial def`, `implemented_by` and `@[extern]`. `COMPUTED FROM
ARTIFACT` (`r/audit.py`).

**Is the headline theorem genuinely proved?** `DIRECTLY OBSERVED`. Yes.
`distributionUniformExponential` is a one-line delegation to
`pdf_distributionUniformExponential_unconditional`, which delegates to
`pdf_distributionUniformExponential_of_uniform_source_rounding` applied to
`unconditionalSourceOneGameRounding_uniform` — a chain of proved theorems, not
hypotheses. It asserts

```
∃ c > 0, ∀ G, repeatedEntangledValue G n ≤
  exp(-(c * ((1-v)^13 / ((1-v) + log(|A|*|B|)))) * n)
```

with an explicit exponent, quantified over arbitrary finite two-player games.
The definitions it rests on are faithful, not degenerate: `Game` carries a
normalised `questionWeight : X → Y → ℝ` and a `predicate : X → Y → A → B →
Bool`; `Game.repeat n` is the genuine product game; `Strategy` carries a shared
`DensityMatrix (Alice × Bob)` with per-question POVMs; `entangledValue` is
`sSup (range winProbability)`. This is a real formalization of a real theorem,
not packaging.

---

## 3 & 5. Mathematical components, and the game

`DIRECTLY OBSERVED`. QPR's formal game objects map cleanly onto the brief's
list:

| role | Lean |
|---|---|
| players | `Strategy.Alice`, `Strategy.Bob` (finite types) |
| questions / answers | `X, Y` / `A, B` |
| question distribution | `Game.questionWeight`, normalised |
| referee | `Game.predicate : X → Y → A → B → Bool` |
| strategy | shared `DensityMatrix (Alice × Bob)` + `X → POVM A Alice` |
| entanglement | `jointEffect = aliceEffect ⊗ₖ bobEffect` (Kronecker) |
| winning probability | `Strategy.winProbability` |
| game value | `entangledValue = sSup (range winProbability)` |
| repetition | `Game.repeat n`, product weights on `Fin n → X` |

So the object under study *is* a game, in the exact sense the brief hoped.

### Where the correspondence with `S = (G, L, B, C)` holds, and where it breaks

The brief asks whether both instantiate

> state → legal action → state transition → value/obstruction → composition.

`STANDARD MATHEMATICAL INFERENCE` from the definitions above:

**QPR's *game* instantiates four of the five and is missing exactly one — the
transition.** A `Strategy` is a *fixed function* from question to measurement,
chosen before play; nothing evolves. The game is one round. State, action,
value and composition are all present; state *transition* is absent. The
proof-construction game's essential feature — sequential state evolution, where
proving a lemma changes what is available next — is precisely what QPR's game
does not have.

**But the transition reappears one level up, in the proof.** `DIRECTLY
OBSERVED`: QPR's core machinery is indexed by `D : Finset (Fin n)`, a set of
*already-revealed coordinates*. `ExactHistoryFlag` carries a `seed`, a
`history` of revealed questions, and the answers on `D`. `martingaleRate` is
normalised by `(Finset.univ \ D).card` — the coordinates still to come. The
argument reveals coordinates one at a time, conditions on the history, and
controls a martingale as `D` grows.

That is a genuine state machine, and it lines up with `S = (G, L, B, C)`:

| proof-construction game | QPR's conditioning argument |
|---|---|
| state `(G, L, B, C)` | `(D, history)` — revealed coordinates and outcomes |
| action | reveal one more coordinate, extend `D` |
| transition | `D → D ∪ {i}`, history extended |
| value | conditional win mass; `martingaleRate` |
| budget | `(univ \ D).card`, the coordinates remaining |

**Where it breaks.** QPR's state space is the lattice of subsets of a *fixed
finite* index set: monotone, bounded, with a natural potential (`card`) that
strictly decreases. The proof-construction state space is unbounded and its
action set is open-ended — "introduce a definition" creates objects that did
not exist, which is exactly what Phase P's term formation did and exactly why
it has no analogue of `(univ \ D).card`. QPR can bound its game because its
composition is a *product of n copies of one fixed object*; proof construction
has no fixed n.

`EVIDENCE LEVEL: 5 (mathematical analogy)`, deliberately not promoted. The
correspondence is a shared *schema* — "how does value behave under
composition?" — instantiated with opposite answers: QPR's difficulty is that
value is **not** multiplicative under repetition (entanglement correlates
copies, so `v(G^n) > v(G)^n` is possible), whereas Phase P found discovery
compounding **less** than independence would predict. Same question, opposite
sign. That is a genuine observation and it is not evidence of transport.

---

## 4. Three-board footprint matrix

`COMPUTED FROM ARTIFACT` (`r/threeboard.py`), declaration level, Phase Q method.

| pair | shared decls | Jaccard | share of smaller |
|---|---|---|---|
| QPR ∩ FLT | 487 | 0.019 | **83.8% of QPR** |
| QPR ∩ NS | 319 | 0.116 | **54.9% of QPR** |
| FLT ∩ NS | 1 948 | 0.075 | 78.4% of NS |

**83.8% looks like a strong connection and is not one.** Every one of the ten
proofs shares 79–86% of its mathlib vocabulary with FLT:

| development | ∩FLT | ∩NS | | development | ∩FLT | ∩NS |
|---|---|---|---|---|---|---|
| SpherePacking | 0.863 | 0.550 | | ConnesRigidity | 0.831 | 0.315 |
| Permanent | 0.845 | 0.230 | | GapCVP | 0.825 | 0.322 |
| NonSoficGroup | 0.839 | 0.440 | | CompactnessAndDegeneracy | 0.802 | 0.458 |
| **QPR** | **0.838** | **0.549** | | MetricCodes | 0.797 | 0.355 |
| MulticolorTriangleRamsey | 0.836 | 0.603 | | EhrhartVolumeInequality | 0.791 | 0.562 |

The range is 0.791–0.863 and QPR sits in the middle. This is a **ceiling
effect**: FLT's 25 413-declaration footprint nearly contains everybody's. The
correct reading is Control A — shared dependence on a common library — and the
between-development spread is the natural null that shows it.

**QPR's distinctive vocabulary**: 88 declarations (15.1%) used by neither FLT
nor NS, concentrated in `LinearAlgebra.Matrix` (26), `Data.Matrix` (10),
`Analysis.CStarAlgebra` (4), `Algebra.Star` (4) — the quantum/operator part.

### The required matrix

| Region / interface | FLT | NS | QPR | Evidence |
|---|---|---|---|---|
| shared mathlib infrastructure | ✓ | ✓ | ✓ | 79–86% vocabulary overlap; ceiling effect, Control A |
| distinctive abstraction | modular curves, Galois deformation | Sobolev/energy estimates | `Game`, `Strategy`, POVM, `DensityMatrix` | each board's own definitions; no overlap |
| proof architecture | local-to-global, functorial, contradiction | regularity, energy, compactness | **coordinate conditioning + martingale** | Phase Q §F; QPR `martingaleRate`, `ExactHistoryFlag` |
| potential bridge | — | — | **finite Pinsker on mathlib's `klFun`** | §6 below; evidence level 3 |

---

## 6. Board versus piece: the portable content

`COMPUTED FROM ARTIFACT` (`r/surface_qpr.py`, Phase Q criterion).

Exportable surface — theorems whose statement names no board-specific
definition, so they can be stated anywhere that speaks mathlib:

| | exportable |
|---|---|
| FLT (Phase Q) | 25.9% |
| NonSoficGroup | 25.1% |
| SpherePacking | 19.6% |
| NS (Phase Q) | 10.9% |
| **QPR** | **8.3% (150 of 1 813)** |
| GapCVP | 5.0% |

QPR is *more* internally closed than either existing board. Its 150 exportable
lemmas are generic in shape — `trace_mul_posSemidef_nonneg`,
`norm_le_of_operator_contraction`, `weighted_real_cauchy`,
`posSemidef_blockDiagonal'`, `negMulLog_rescale`, `finite_weighted_entropy_le`,
`noncommutative_resolvent_identity`.

### The standout piece

`DIRECTLY OBSERVED`. QPR contains a complete finite **Pinsker inequality**,
built directly on *mathlib's own* `InformationTheory.klFun` and
`InformationTheory.hasDerivAt_klFun`:

```
theorem quadratic_le_klFun {x : ℝ} (hx : 0 ≤ x) :
    3 * (x - 1) ^ 2 / (2 * (x + 2)) ≤ InformationTheory.klFun x

theorem finite_pinsker (p q : ι → ℝ) … :
    2 * (finiteTotalVariation p q) ^ 2 ≤ finiteRelativeEntropy p q
```

Checked against mathlib (`decls.json`, 241 917 declarations):

| concept | in mathlib? |
|---|---|
| `klFun` | **yes** — 31 declarations (continuity, convexity, derivative) |
| `klDiv` | **yes** — `InformationTheory.klDiv…` |
| total variation | yes, but only `MeasureTheory.SignedMeasure.totalVariation` |
| **Pinsker's inequality** | **NO** |
| POVM, density matrix, entropy, two-player game, parallel repetition | **NO** |

So mathlib has both *sides* of Pinsker — the KL side fully developed — and not
the inequality that connects them. Answering §6's six questions for this piece:
it is not QPR-specific; it is not in mathlib; it is useful far outside QPR; it
is already abstract (finite distributions on a `Fintype`); FLT and NS have no
evident use for it; and it would create a genuinely new mathlib interface
rather than merely fill a hole. `EVIDENCE LEVEL: 3`.

This is a better upstream candidate than Phase Q's only bridge (integrability
of polynomial × exp), which was a routine fact two boards happened to duplicate.

---

## 7 & 8. The ten proofs: structure, clustering, distance

`COMPUTED FROM ARTIFACT` (`r/audit.py`, `r/internal.py`). Edges are internal
declaration references within each file; the same extractor is used throughout,
so the columns are comparable to each other (not to FLT's import-based graph).

| development | decls | thms | edges | out-deg | depth | namespaces | exportable |
|---|---|---|---|---|---|---|---|
| GapCVP | 8 025 | 3 683 | 39 482 | 4.92 | 74 | **442** | 5.0% |
| MetricCodes | 5 683 | 4 328 | 24 411 | 4.30 | 44 | **432** | 12.4% |
| ConnesRigidity | 2 776 | 1 930 | 11 947 | 4.30 | 33 | 33 | 15.8% |
| **QPR** | **2 638** | **1 813** | **16 221** | **6.15** | **36** | **8** | **8.3%** |
| EhrhartVolumeInequality | 2 361 | 1 875 | 13 815 | 5.85 | 74 | 220 | 5.6% |
| SpherePacking | 2 220 | 1 809 | 7 730 | 3.48 | 28 | 28 | 19.6% |
| NonSoficGroup | 1 436 | 1 061 | 4 729 | 3.29 | 24 | 90 | 25.1% |
| Permanent | 1 393 | 972 | 4 285 | 3.08 | 34 | 18 | 15.5% |
| CompactnessAndDegeneracy | 941 | 656 | 3 737 | 3.97 | 24 | 4 | 10.5% |
| MulticolorTriangleRamsey | 139 | 96 | 352 | 2.53 | 18 | 2 | 16.7% |

**QPR is densely connected but flat.** It has the highest mean out-degree of
the ten (6.15) and nothing isolated, but only **8 namespaces, with 2 490 of
2 638 declarations in a single one**. Its internal hubs are real — `Game` cited
903 times, `Strategy` 716, `BipartiteUnitVector` 367 — but they are hubs of one
region, not interfaces between several. On internal region structure the
board-like members are GapCVP (442 namespaces) and MetricCodes (432), not QPR.

Clustering by size, connectivity and region count:

* **board-like**: GapCVP, MetricCodes — large, many regions, deep.
* **sub-board**: QPR, ConnesRigidity, EhrhartVolumeInequality, SpherePacking —
  substantial and structured, single-subject.
* **pieces**: MulticolorTriangleRamsey (139 declarations), and
  CompactnessAndDegeneracy at the boundary.

**Is QPR isolated?** `EXPERIMENTAL RESULT`. No — it is the *least* isolated of
the ten. Mean pairwise vocabulary Jaccard: QPR **0.144**, collection mean
0.117, minimum (MulticolorTriangleRamsey) 0.077. Nearest neighbours:
NonSoficGroup 0.190, MetricCodes 0.168, Ehrhart 0.168. QPR sits at the centre
of a sparse collection, which is what one would hope from a subject mixing
probability, matrix analysis, information theory and combinatorics.

---

## 9 & 11. Does QPR give a new experimental capability?

### The experiment

`EXPERIMENTAL RESULT` (`r/pairs.py`). Phase Q's sharpest limitation was that
its transport metric could not separate a *related* cross-board pair (Euler →
NS, 5.5%) from an *unrelated* one (FLT → NS, 2.4%): both near the floor, with
n = 1 each. The collection removes that limitation — 90 ordered pairs, one
producer, one toolchain.

Protocol unchanged from Phase Q (exportable surfaces, token-set Jaccard,
match at J ≥ 0.4).

| | value |
|---|---|
| within-development baseline | **0.689** |
| cross-development mean | **0.0244** |
| raw *r* (vocabulary Jaccard vs transport) | **0.434** |
| **partial *r*, controlling both pool sizes** | **0.308** |
| label-permutation *p* (partial) | **0.048** |

The 28× within/cross gap reproduces Phase Q exactly. The new result is the
correlation: **transport does track mathematical proximity**, weakly, and it
survives controlling for pool size — a real confound, since
*r*(transport, source pool size) = 0.413 on its own.

Top transporting pairs: ConnesRigidity → QPR 0.145, QPR → NonSofic 0.122,
MetricCodes → QPR 0.118. Four of the top eight involve QPR, consistent with its
central position.

### The answer

> **YES — but not as a board.** QPR's value is as a member of a controlled
> population, not as a third transport partner.

As a *board*, QPR would add little: 150 exportable statements is too few for
the Phase Q protocol to have power (FLT had 11 093, NS 2 829), and its 8.3%
exportability and single flat namespace make it a poorer transport partner than
either existing board. As a *population member* it is valuable: the collection
turns Phase Q's n = 1 anecdote into a 90-pair regression, and it immediately
produced a finding Phase Q could not — that cross-development transport,
though uniformly tiny, is not independent of subject matter.

---

## 9. Upstreamability revisited

Phase Q recommended `board → mathlib → board`. QPR sharpens it and also
exposes its weakness.

**Sharpens:** `quadratic_le_klFun` + `finite_pinsker` are a concrete upstream
target that would create a genuinely new interface — mathlib has KL and has
total variation and lacks the bridge. Compare FLT's candidates (its exportable
surface is largely arithmetic-geometry-flavoured, upstreamable but interface-
neutral) and NS's (analysis lemmas mostly duplicating each other, per Phase Q's
44.8% internal redundancy).

**Weakness, stated plainly:** the brief asks whether upstreamability is a
*mechanism of mathematical transport* or *an engineering consequence of good
abstraction*. On the evidence so far it is mostly the second. Every upstream
candidate found in Phases Q and R — polynomial × exp integrability, Pinsker,
`trace_mul_posSemidef_nonneg` — is a lemma that *should* have been in mathlib
anyway. None of them was discovered by one board and needed by another. Calling
that "transport" stretches the word.

The distinction is testable, and that test is the recommendation below.

---

## 12–13. Next experiment

Comparing the four options the brief requires:

| option | verdict | why |
|---|---|---|
| **1. Further QPR / board exploration** | **no** | QPR is a sub-board: 150 exportable statements, 8 namespaces, 8.3% exportability. Too small for an independent transport experiment to have power. |
| **2. Phase Q's upstreamability program** | **partly** | The Pinsker candidate is real and worth acting on, but as posed it is an engineering task, not an experiment. It needs a causal question attached. |
| **3. Direct three-board transport** | **no** | Weakest option. QPR's exportable surface is 1.3% the size of FLT's, and Phase Q already showed cross-board transport is at the floor. |
| **4. Search for another board** | **no** | §12 forbids it absent a failure, and the population study below supplies what a fourth board would have. |

**Recommended: the interface-mediated transport experiment, on the twelve-development population** (the ten plus FLT and NS). It merges options 2 and 3 into the causal question neither answers alone:

> Does the existence of a **shared mathlib interface** between two developments
> predict transport between them, beyond what raw vocabulary overlap predicts?

Concretely: for each of the 132 ordered pairs, measure (i) transport by the
Phase Q protocol, (ii) raw vocabulary Jaccard, and (iii) *interface sharing* —
whether the pair's shared mathlib declarations include the same **structures
and typeclasses** rather than only lemmas. Then test whether (iii) adds
predictive power over (ii). Phase R has already fitted the (ii)-only model:
partial *r* = 0.308.

This is worth doing because it makes `board → mathlib → board` falsifiable
rather than merely plausible, and because Pinsker supplies the natural
intervention arm: an interface that does *not* currently exist in mathlib, whose
absence should — if the hypothesis is right — show up as suppressed transport
between the information-theoretic developments (QPR, MetricCodes, GapCVP).

**Falsifier:** if interface sharing adds nothing over vocabulary overlap, then
mathlib is a *substrate* rather than a *transport medium*, `board → mathlib →
board` is the wrong picture, and the right conclusion is that these
developments simply do not exchange mathematics at all.

---

## 14. On the deeper questions

**What makes a development a board rather than a collection of pieces?** Phase
R supplies three measurable candidates, and they disagree with each other,
which is itself the finding:

* *scale* — QPR is 3.7% of FLT's theorem count;
* *internal region structure* — QPR has 8 namespaces against GapCVP's 442, and
  94% of its declarations in one; this is the criterion on which QPR fails;
* *exportability* — QPR's 8.3% is below NS's 10.9% and FLT's 25.9%.

A development can be dense and deep (QPR: out-degree 6.15, depth 36, nothing
isolated) and still not be a board, because boardhood is about *having
interfaces between regions*, not about being large or well-connected. That is a
sharper criterion than the programme had before this phase.

**What makes an object transportable?** Every portable thing found in two
phases has the same shape: a statement in pure mathlib vocabulary about mathlib
objects, sitting adjacent to a developed mathlib area. Nothing board-specific
has transported anywhere. The unit of transport is the *library lemma*, not the
board, the architecture, or the strategy.

---

## Negative results

1. **The 83.8% QPR–FLT vocabulary overlap is not evidence of connection.** All
   ten proofs score 0.791–0.863 against FLT; it is a ceiling effect from FLT's
   footprint size.
2. **QPR is not an outlier in any measured respect** — not in size, mathlib
   dependence, or distance. It is the *most central* of the ten, which is a mild
   positive, and mid-pack on everything else.
3. **QPR fails the region-structure limb of the §10 decision rule outright**:
   8 namespaces, 94% of declarations in one.
4. **The game correspondence breaks at the state transition.** QPR's game has no
   transition at all; the transition lives in the *proof*, and even there the
   state space is a bounded finite lattice with a decreasing potential, which
   proof construction has no analogue of.
5. **An extractor bug, caught and fixed.** The first internal-graph run reported
   5 edges for 2 638 declarations because each declaration was added twice to
   the same short-name key, making every simple name look ambiguous. Corrected:
   16 221 edges.
6. **The transport/proximity correlation is weak and nearly confounded.**
   Raw *r* = 0.434 falls to 0.308 once pool size is controlled, at *p* = 0.048
   by label permutation with only ten developments. It should be treated as a
   hypothesis worth testing at n = 132, not as an established effect.

---

## Artifacts

`r/audit.json` · `r/threeboard.json` · `r/internal.json` · `r/surface_qpr.json`
· `r/pairs.json` · scripts `r/*.py`.

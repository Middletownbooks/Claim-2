# Report I — FLT External-Board Phase 1: the mathlib ↔ FLT boundary

Answers the ten questions of the supervising researcher's Phase 1 brief, plus
the blind region-discovery experiment. Data: `flt/boundary.json`,
`flt/flt_graph.json`, `flt/regions.json`, `flt/regions_followup.json`,
`flt/compression.json`, `flt/upstreamable.json`. Method notes in each script.

Accepted framing: the Phase-0 map measured **territory in mathlib**; the object
of interest is **territory available to Lean formal mathematics**. Those sets
differ, and this report measures the difference.

---

## The headline numbers

| | |
|---|---|
| theorems in the artifact | 29 511 |
| mathlib modules its proofs and definitions import | **1 696** (19.9% of mathlib's 8 513) |
| its own definition modules | 1 450 (1 039 import a mathlib module directly; 411 build only on other definitions) |
| statements written **purely in mathlib vocabulary** | **4 577** (15.5%) |
| …of those, whose entire transitive support is also mathlib-vocabulary | **4 281** |
| …and whose proof file also imports no repo definition | **4 184 (14.2% of the proof)** |
| declared names colliding with an existing mathlib name | **1** (`MvPowerSeries.isNoetherianRing_fin`) |
| compression achieved | 29 511 theorems → **36 communities** → 1 230 definition interfaces, **282 of which carry 80%** of statement usage |

---

## 1. What mathlib infrastructure does the artifact actually consume?

1 696 distinct modules — a fifth of mathlib. By area (distinct modules):
RingTheory 324, Algebra 277, Analysis 217, Topology 125, Data 124, NumberTheory
124, LinearAlgebra 122, MeasureTheory 88, AlgebraicGeometry 70, GroupTheory 54,
FieldTheory 47, CategoryTheory 34.

Most-imported individual modules (excluding the blanket `import Mathlib` in the
statement files): `Tactic.LinearCombination` (187), `Analysis.MellinTransform`
(179), `FieldTheory.IsAlgClosed.Basic` (171), `MeasureTheory.Group.FundamentalDomain`
(142), `RingTheory.RootsOfUnity.PrimitiveRoots` (132),
`MeasureTheory.Measure.Haar.DistribChar` (112),
`Analysis.SpecialFunctions.Gamma.Deligne` (110),
`AlgebraicGeometry.EllipticCurve.Affine.Point` (99).

The profile is not what the folklore predicts. A proof of FLT leans hardest on
**commutative algebra and analysis**, and its distinctive imports are the
**adelic/Haar-measure and Mellin/Gamma** machinery — automorphic, not
Diophantine. `ACTUAL_LEAN_DEPENDENCY` throughout (parsed imports).

## 2. What external infrastructure is genuinely absent from mathlib?

19 080 theorems (65%) sit in namespaces with no mathlib counterpart, and the
concepts are absent outright — **zero** occurrences anywhere in mathlib at
`110cb7f0` of `ModularCurve`, `CerednikDrinfeld`, `AutomorphicForm`,
`PDivisibleGroup`, Néron models, or deformation theory. Sizes: ModularCurve
7 711, CerednikDrinfeld 2 376, AutomorphicForm 2 336, AlgebraicCurve 1 577,
LanglandsTunnell 1 543, GoodReductionJacobian 674, MvFormalGroup 166,
PDivisibleGroup 138.

## 3. Which external clusters have the highest reuse potential?

Measured by how many **statements** are written against each definition module
(the repo's real interfaces, from statement imports rather than names):

| uses | definition interface |
|---|---|
| 1 674 | `FLTPrelim_Ramification` |
| 1 507 | `AlgebraicGeometry_RelativePicardFunctor` |
| 1 419 | `ModularCurve_X1` |
| 1 223 | `AlgebraicCurve_TwoChartIntegralModel` |
| 1 077 | `NumberField_TateGlobalZeta` |
| 1 050 | `JacJ1Iface` |
| 1 020 | `ModularCurve_SupersingularModuli` |
| 1 013 | `AlgebraicCurve_IsCurveOver` |

`AlgebraicGeometry_RelativePicardFunctor`, `AlgebraicCurve_IsCurveOver` and
`AlgebraicCurve_TwoChartIntegralModel` are the most reusable-looking: they are
general algebraic-geometry notions with no FLT content, each carrying over a
thousand statements.

## 4. Which clusters are bottlenecked by a small number of interfaces?

**Essentially none — this is the phase's main negative result.**

Pre-registered prediction P3 was that the median bottleneck ratio would be
below 0.25. Measured: **0.512**. Over half the members of a typical community
have an edge leaving it. Follow-up measurements decide what that means:

* the partition is real: **modularity Q = 0.677**, only **14.9% of edges cross
  communities**, median conductance 0.224 (best communities 0.04–0.13);
* but the crossing traffic is **diffuse**: the top 1% of nodes carry 10.9% of
  cross-community edges, the top 10% carry 37.5%, and 11 668 distinct nodes
  carry some. The busiest single theorem carries 130 of 15 888 cross edges.

So the regions are genuine and mostly self-contained by edge mass, yet they are
joined by a **broad seam, not a gateway**. The hope that "apparently huge
disconnected regions have a narrow mathematical bottleneck" is **not supported**
for this artifact. Integration cost scales with the seam, and the seam is wide.

## 5. Which external declarations duplicate or generalize mathlib ones?

Duplication by name is essentially nil: of 29 511 declared names, **one**
already exists in mathlib. The repository is not restating mathlib under new
names. Semantic duplication cannot be excluded by this method — two differently
named statements can still be the same theorem — and would need statement-level
matching or a build to detect.

## 6. Which could plausibly be upstreamed?

A concrete, checkable set: **4 184 theorems (14.2%)** whose statement *and*
proof file import no repository definition, and whose entire transitive support
is likewise mathlib-vocabulary. **3 043 of them cite nothing at all** — they are
pure mathlib lemmas proved from mathlib alone.

Their declared namespaces are mathlib's own: AlgebraicGeometry 785, Algebra 265,
Module 183, ValuationSubring 161, IsLocalRing 142, MeasureTheory 129,
HopfAlgebra 120, NumberField 116, WeierstrassCurve 108, Ideal 91, Matrix 88,
groupCohomology 79, Polynomial 68.

Three honest qualifications: (a) 25% of these proofs use a `p2m_*` tactic, so
extraction is a port, not a copy; (b) mathlib has naming, style and generality
conventions this material was not written to; (c) "self-contained" is an
import-structure fact, not a claim of novelty or of mathlib-readiness.

## 7. Which 1000+ entries would become more valuable if this were integrated?

The board entries whose neighbourhoods this material would thicken are
concentrated in MSC 14 (63 missing) and MSC 11 (92 missing). Specifically, the
artifact contains substantial machinery bearing on entries the board lists as
**missing** — `PARTIAL_MACHINERY_PRESENT`, not proofs of the board statements:

| board entry (missing) | machinery in the artifact |
|---|---|
| Riemann–Roch theorem (14) | 105 declarations, `AlgebraicCurve.Divisor.*riemannRochSpace*` |
| Abel–Jacobi theorem (14) | 116, `AlgebraicCurve.Pic0.abelJacobi*` |
| Hasse–Arf theorem (11) | 152, `IsDiscreteValuationRing.hasseArfChain_*`, `IsLocalRing.herbrandPhi_*` |
| Ribet's theorem (14) | level lowering at the strength FLT needs (9 declarations) |
| Modularity theorem (11) | `WeierstrassCurve.modularity_of_semistableModel` (semistable, a_ℓ-matching form) |

Whether any of these *is* the board theorem requires reading the Lean
statements; PROOF-PATH's own "exact strength" section says several classical
names are proved only in the strength the argument needed.

## 8. Which missing targets become natural landing pads?

Riemann–Roch and Abel–Jacobi: both sit in `AlgebraicCurve`, which is one of the
most reused interface clusters and has no FLT content. Formalizing the board
statement there would connect the artifact's largest general-purpose region to
mathlib's own algebraic geometry. Hasse–Arf is a smaller, cleaner target in
ramification theory with 152 declarations already present.

## 9. Which regions point to targets the 1000+ board does not represent?

`AutomorphicForm` (2 336) and `NumberField_TateGlobalZeta` (1 077) — Tate's
thesis, adelic zeta integrals, twisted orbital integrals — have **no board
representation at all**. Neither does deformation theory, p-divisible groups, or
Taylor–Wiles patching (`Algebra.PatchingDatum`). This is the Report C.6
observation repeating: the 1000+ board indexes *named classical theorems*, and
the machinery that modern arithmetic geometry actually runs on is invisible to
it. If the programme wants targets that matter, the board is the wrong index.

## 10. Can the graph be compressed?

Yes, by about two orders of magnitude, and the compression is meaningful:

**29 511 theorems → 36 communities (≥100 members) → 1 230 definition interfaces,
of which 282 carry 80% of all statement usage.**

Each blind community lands on a coherent interface (community size → its
top statement interface): 8 970 → `ModularCurve_X1`; 4 066 →
`NumberField_TateGlobalZeta`; 1 290 → `GaloisRep_Residual`; 1 064 →
`GaloisRep_Flat`; 623 → `CerednikDrinfeld_ShimuraCurve`; 548 →
`AlgebraicGeometry_RelativePicardFunctor`; 499 →
`CerednikDrinfeld_SpecialFormalModuli`; 458 → `JacJ1Iface`.

---

## The blind experiment — scorecard

Method and predictions were fixed in `flt/PREREG_blind_regions.md` before
running. The clustering saw integer ids and edges only: no names, no
PROOF-PATH, no knowledge that the root is FLT.

| prediction | outcome |
|---|---|
| **P1** 5–60 communities of size ≥100, not one blob | **PASS** — 36 communities ≥100, 8 ≥500, largest 8 970 (30%) |
| **P2** largest community is predominantly modular curves | **PASS** — 8 970 members, ModularCurve 5 647 + AlgebraicCurve 1 318 |
| **P3** median bottleneck ratio < 0.25 | **FAIL** — 0.512. See §4; the partition is real (Q=0.677, 14.9% cross edges) but the seams are broad |
| **P4** each community ≥500 maps to ≤1 PROOF-PATH step | **PARTIAL** — Langlands–Tunnell (4 066: AutomorphicForm+LanglandsTunnell+NumberField) and level lowering (623: CerednikDrinfeld+QuaternionAlgebra) come out clean; the 8 970-member modular-curve mass does **not** separate Mazur's argument from general curve infrastructure, and two AlgebraicGeometry-dominant communities are infrastructure spanning several steps |
| **P5** citation structure agrees with statement vocabulary above chance | **PASS** — NMI 0.40 vs 0.15 on a permuted baseline |

**What the benchmark says about "bridge value".** The structural notion is
partly vindicated: a name-blind algorithm recovers the proof's major regions,
finds two of the six narrative steps cleanly, and agrees with an independent
statement-level view well above chance. It is also partly refuted: the regions
do **not** meet through small interfaces, so a bridge-value score built on
"few nodes control access to a big region" would be measuring something this
artifact does not have.

---

## The revised model, with evidence

The supervising researcher proposed `R(T) = R_internal(T) + R_external(T)` plus
an integration-leverage term `I(T)`. The measurements support the split and
sharpen the third term:

* **`R_internal` and `R_external` are genuinely different.** In Phase 0 the FLT
  region measured 4 transitive importers inside mathlib — a cul-de-sac. Its
  external neighbourhood is 29 511 theorems. Any single score would have hidden
  one of those facts.
* **`I(T)` is measurable, and lower than theorem count suggests.** For this
  artifact: 14.2% is extractable with no new definitions; 65% of it needs
  concepts mathlib does not have; and because the seams are broad (§4), the
  cost of importing a region is not "integrate its interface" but "integrate its
  interface and most of its boundary". A defensible first form:

  `I(region) = self_contained_fraction × region_size ÷ (1 + boundary_breadth)`

  which for this artifact ranks the general algebraic-geometry clusters
  (`AlgebraicCurve_IsCurveOver`, `RelativePicardFunctor`, high mathlib-vocabulary
  fraction, moderate size) above the modular-curve mass (huge, but 12%
  mathlib-vocabulary and a very wide boundary).
* **The warning about names was correct and load-bearing.** Every result here
  uses statements, imports or graph structure. The one place names were used —
  Phase 0's namespace-prefix comparison — is the weakest evidence in either
  report, and it is the one that would have been most tempting to over-read.

## Recommended next step

Not another scoring pass. The compression result gives the programme something
better: a **retrospective benchmark**. We now have a complete traversal of a
hard theorem, with its regions, interfaces and 282 load-bearing concepts
recoverable from structure alone. The question worth asking is whether our
discovery machinery, run on the *early* layers of this graph (the 8 230 leaves
and their immediate consumers), would identify the interfaces that later carry
the proof — a question with a checkable answer key that the learner cannot see.
That is the same experimental shape as the cross-object test recommended at the
end of Phase 0, and it can use the same freeze-and-holdout protocol.

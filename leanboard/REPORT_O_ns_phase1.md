# Report O — Phase 1 boundary analysis: `openai/NavierStokesAndEuler`

The Report I analysis, re-run on the second external artifact so the two can be
compared. Code: `ns/parse.py`, `ns/phase1.py`, `ns/analyze.py`. Data:
`ns/ns_graph.json`, `ns/phase1.json`, `ns/phase1_loose.json`.

**The headline is a replication failure, and it is the most useful thing in this
report.**

## O.1 Method, and why it is weaker here

The FLT artifact documents a convention — a solution file's
`import Theorems.Thm_…` lines *are* its citations — so its declaration-level
graph is **exact**. This repository is ordinary Lean: statements and proofs live
together and no such convention exists. The graph here is therefore
**approximate**, built by extracting identifiers textually and intersecting them
with the repository's own 49 365 declaration names.

The first resolution rule produced 1.8 M edges for 49 K declarations — ten times
FLT's density, obviously spurious. The rule was tightened to resolve a bare
short name only when it is unambiguous in this repository and is not also a
mathlib name, giving **133 535 edges, mean 2.7 per declaration** against FLT's
exact 3.6. That trades recall for precision: 4 149 short names are ambiguous and
now dropped.

Because the rule is a judgement call, **every conclusion below was re-run under
the loose rule as a sensitivity check**, and the report says which survived.

## O.2 Consumption: narrow and deep

| | FLT artifact | NS/Euler |
|---|---|---|
| declarations | 29 511 theorems | **49 365** |
| mathlib modules imported | 1 696 (19.9%) | **303 (3.5%)** |
| mathlib pin | v4.33.0 | v4.34.0-rc2 (= the mapped commit) |
| areas consumed | RingTheory 324, Algebra 277, Analysis 217, … | **Analysis 136, MeasureTheory 52, Topology 36**, then almost nothing |

Larger, on a sixth as much mathlib. Two hard theorems, two completely different
shapes of dependence on the shared library.

## O.3 Upstreamability

**15 042 of 49 365 statements (30%) mention no repository identifier** —
roughly twice FLT's 15.5%. Two cautions before that is read as "twice as
upstreamable": FLT's criterion was import-based and therefore stronger, while
this one is textual; and the strict resolution rule drops ambiguous names, which
inflates this figure. It is a plausible upper bound, not a task list. The
directionally safe statement is that **an analysis corpus sits closer to
mathlib's vocabulary than an arithmetic-geometry one does**, which is what the
consumption profile also suggests.

## O.4 Region structure: real, but blurrier

| | FLT | NS (strict) | NS (loose) |
|---|---|---|---|
| modularity Q | **0.677** | **0.503** | 0.000 |
| communities ≥ 100 | 36 | **13** | 1 |
| largest community | 30% of nodes | **45%** | 98% |
| cross-edge fraction | 14.9% | 13.1% | ~0 |
| median conductance | 0.224 | 0.241 | — |
| cross traffic in top 1% of nodes | 10.9% | 17.7% | — |

Under the strict rule the community structure is genuine (Q = 0.503, only 13.1%
of edges crossing) but **markedly coarser than FLT's**: thirteen regions rather
than thirty-six, and one of them holds 45% of the corpus, splitting mostly along
the `NavierStokes` / `Euler` line rather than into mathematical sub-regions.
Under the loose rule everything collapses into one community — which is itself
evidence that the loose rule is noise, not an alternative reading.

FLT's Report I finding — regions joined by **broad seams rather than gateways** —
**replicates**: median bottleneck ratio 0.59 here versus 0.51 there, and the top
1% of nodes carry only 17.7% of cross-region traffic.

## O.5 Compression

**49 365 declarations → 13 communities → 6 302 definition interfaces, of which
1 663 carry 80% of statement usage** (FLT: 29 511 → 36 → 1 230, of which 282).

So NS compresses far less well: 3.4% of its declarations are load-bearing
interfaces against FLT's 1.0%, and it needs six times as many of them. Its
top interfaces are bespoke analytic scaffolding —
`NavierStokes.OutgoingTail.TailData` (1 360 statements),
`SimilarityProfile.T` (1 357), `WeightedClasses.StripData` (1 233),
`EulerCylinderSobolevSpace.SobolevSpace` (912) — rather than reusable
mathematical objects like FLT's `ModularCurve_X1` or `AlgebraicCurve_IsCurveOver`.

## O.6 The replication failure

Report J found that **breadth across regions forecasts which abstractions end up
carrying a proof better than usage frequency**, in 6 of 6 depth splits, with the
margin widening as the horizon lengthened. That was the programme's first
positive evidence for a bridge-value-shaped quantity.

Re-run here, identically:

| D | early fraction | target | frequency | **breadth** | random |
|---|---|---|---|---|---|
| 1 | 0.357 | 1 610 | **0.533** | 0.511 | 0.256 |
| 2 | 0.434 | 1 558 | **0.541** | 0.513 | 0.247 |
| 3 | 0.490 | 1 510 | **0.542** | 0.515 | 0.240 |
| 4 | 0.535 | 1 465 | **0.539** | 0.515 | 0.233 |
| 6 | 0.600 | 1 386 | **0.530** | 0.484 | 0.220 |
| 8 | 0.648 | 1 325 | **0.517** | 0.471 | 0.210 |

**Breadth beats frequency in 0 of 6 splits.** Under the loose rule, where both
predictors are much stronger (0.87 vs 0.79), the verdict is the same: **0 of 6**.
The failure is robust to the one methodological choice that could have caused it.

### Why, mechanically

Breadth-across-regions can only carry information if the corpus *has* many
regions. In NS, **55% of definitions are used entirely within a single
community**, so the feature is very nearly the constant 1:

| breadth | definitions |
|---|---|
| 1 | 3 461 |
| 2 | 1 519 |
| 3 | 589 |
| ≥4 | 549 |

FLT had 36 communities and a definition's breadth genuinely varied. NS has 13,
one holding 45% of everything, and the signal has almost no variance to exploit.

### What that does to Report J

**Report J's finding is a fact about modular corpora, not about formal proofs in
general.** It survives as stated — it was measured on FLT and replicates nothing
it did not claim — but its scope is now known to be narrower than it read.
The honest form is:

> Where a development decomposes into many regions, how many regions use an
> abstraction early forecasts its eventual load-bearing status better than how
> often it is used. Where a development is dominated by one or two regions, the
> measure degenerates and plain frequency is better.

That is exactly what a second artifact of a different shape was supposed to
settle, and it settled it against the more exciting reading. Both predictors
still beat random by a wide margin (0.53 vs 0.24), so early usage remains
informative in both corpora; it is the *bridge-shaped refinement* that does not
generalise.

## O.7 Consequences for the programme

1. **Do not promote breadth to a general objective.** The Report J
   recommendation — prioritise abstractions used by many regions rather than
   used often — should be conditioned on a measured modularity: check Q and the
   breadth distribution before trusting it. Below roughly Q ≈ 0.5 with a
   dominant community, it has nothing to work with.
2. **Two artifacts is the minimum for this kind of claim.** The FLT result was
   clean, stable across six splits, and mechanistically plausible — and still
   did not generalise. Nothing in the first corpus predicted that.
3. **The board's blind spot is now threefold.** Navier–Stokes, Euler and fluid
   mechanics appear nowhere in the 1 199 entries; neither do modular curves or
   automorphic forms. Two of the largest Lean developments in existence are
   invisible to the index this map started from.

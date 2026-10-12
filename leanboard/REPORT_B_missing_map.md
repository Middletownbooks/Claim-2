# Report B — Missing-target map

954 missing targets. Data: `scores.json` (`missing`), `proximity.json`,
`bridge_ledger.csv`.

## B.0 Resolution warning — read before using any ranking below

**The available evidence does not support a per-target ranking of 954 missing
theorems, and this report does not pretend otherwise.**

A missing target has, by definition, no declaration, no imports and no uses.
Everything computable about it is a property of its *class*: how big the mapped
mathlib area is, how fast it is moving, how many board entries share its MSC
code. Those are identical for every target in a class, so a naive sort produces
15 differential-topology targets tied at `0.418` — a class label wearing a
ranking's clothes. That output is in `scores.json` and should be read as a
ranking **of MSC classes**.

Two per-target signals were attempted:

* **Other-assistant formalization** — intended as the difficulty signal ("if
  Isabelle has it, the path is known"). It is unusable: the upstream project's
  data is essentially unpopulated for non-Lean systems — 226 `lean:` entries but
  only 38 `metamath:`, 4 `rocq:`, 1 `isabelle:`, 1 `hol_light:`, 1 `mizar:`
  across 1 200 records. The term fires for exactly **one** of 954 targets (Four
  colour theorem, Rocq). Reported as a data-availability finding, not a result.
* **Does mathlib already name the target** (`proximity.py`) — this works, but
  coarsely: a bare surname cannot separate "Euler's theorem" from "Euler's
  polyhedron theorem", so those rows are flagged `discriminating: false`.

What follows is therefore: a class-level investment ranking (defensible), plus a
small number of per-target assessments backed by **manual inspection of actual
mathlib state** (the only per-target evidence that survives scrutiny).

## B.1 Class-level: where the missing mass is

| MSC | field | missing | mapped mathlib area | area modules | recent touches |
|---|---|---|---|---|---|
| 11 | Number theory | **92** | NumberTheory | 249 | 914 |
| 51 | Geometry | 83 | Geometry | 156 | 635 |
| 05 | Combinatorics | 63 | Combinatorics | 200 | 621 |
| 14 | Algebraic geometry | **63** | AlgebraicGeometry | 140 | 499 |
| 30 | Complex variables | 46 | Analysis | 808 | 2 660 |
| 46 | Functional analysis | 44 | Analysis | 808 | 2 660 |
| 20 | Group theory | 44 | GroupTheory, RepresentationTheory | 213 | 800 |
| 53 | Differential geometry | 36 | Geometry | 156 | 635 |
| 60 | Probability | 34 | Probability | 140 | 450 |
| 03 | Logic and foundations | 32 | Logic, SetTheory, ModelTheory | 152 | 534 |

Number theory and algebraic geometry carry 155 missing targets between them and
map onto areas that are mid-sized but among the fastest-moving in the library.
Differential topology (MSC 57) is the class the naive score liked: a large
cluster of missing targets over a comparatively thin mathlib area — high
prospective value, but its uniformity is exactly what the resolution warning is
about.

Difficulty distribution over the 954: **D=2: 221, D=3: 404, D=4: 166, D=5: 163.**
Difficulty is ordinal (1–5) and every adjustment is recorded per row in
`bridge_ledger.json` (`difficulty_reasons`).

## B.2 Per-target assessments backed by manual inspection

These are the targets where I checked mathlib's actual state rather than its
class statistics. Each claim carries its evidence label.

### Mordell–Weil theorem (Q1191188, MSC 11) — the standout

**Prospective bridge value: highest of any target examined. Difficulty: lower
than its reputation, because three of the four ingredients already exist.**

mathlib names Mordell–Weil in exactly two modules, and both exist to serve it
(`DOCUMENTED_MATHEMATICAL_RELATION`, verified by reading the files):

* `Mathlib/GroupTheory/Descent.lean` — "This last version is one of the main
  ingredients of the standard proof of the **Mordell-Weil Theorem**. It allows
  to reduce the statement to showing that `G / 2 • G` is finite." Provides
  `Group.fg_of_descent`, `CommGroup.fg_of_descent`, `CommGroup.fg_of_descent'`
  (descent via the approximate parallelogram law).
* `Mathlib/NumberTheory/Height/EllipticCurve.lean` — proves
  `approx_parallelogram_law`, `finite_naiveHeight_le` (Northcott finiteness),
  and **`finite_torsion`: the torsion subgroup of `W.Point` is finite**.

Add `instance : AddCommGroup W.Point` in
`Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.lean`
(`ACTUAL_LEAN_DEPENDENCY`), and the ledger reads:

| Mordell–Weil ingredient | status |
|---|---|
| the group `E(K)` | **present** |
| height machinery + Northcott | **present** |
| descent → finitely generated | **present** |
| torsion finite | **present (proved)** |
| **weak Mordell–Weil: `E(K)/2E(K)` finite** | **absent** |

So the bottleneck is one specific missing piece: the Kummer-theory/Selmer
argument for `E(K)/2E(K)`. Its own prerequisites are themselves already in
mathlib — finiteness of the class number (`NumberTheory/NumberField/ClassNumber`)
and Dirichlet's unit theorem (`NumberField/Units/DirichletTheorem`, a completed
board entry) — while `RingTheory/DedekindDomain/SelmerGroup.lean` provides Selmer
groups for Dedekind fraction fields, though **not** for elliptic curves
(`PLAUSIBLE_FORMAL_BRIDGE`: the file is about the right kind of object, but no
formal link to `W.Point` exists).

This is the clearest instance on the whole board of a target whose corridor is
under active construction with one identified gap.

### Modularity theorem (MSC 11)

One mathlib mention, and it is a **false positive**: the token matched
`Mathlib/Order/ModularLattice`, an unrelated use of "modular". Actual state:
`NumberTheory/ModularForms/` is a substantial region (40 modules, 454 transitive
importers, LevelOne, DimensionFormulas, EisensteinSeries, Petersson,
`LFunction`), and elliptic curves have `LFunction.lean` — but nothing connects
them. Prospective board value very high, difficulty **5**: this is the FLT
project's own target, pursued in a separate repository over years
(`SPECULATIVE_RESEARCH_BRIDGE` from mathlib's current state).

### Szemerédi's theorem (MSC 05)

14 mathlib mentions across `Combinatorics/Additive/Corner/{Defs,Roth}` and
`Combinatorics/Extremal/RuzsaSzemeredi` (`DOCUMENTED_MATHEMATICAL_RELATION`).
mathlib has the corners theorem and Roth (k=3) but not general k. Difficulty 3–4;
prospective bridge value moderate — additive combinatorics is comparatively
self-contained, so it would deepen a region more than connect regions.

### A board-lag finding, not a target

Several entries the board treats as noteworthy are **already formalized**:
Dirichlet's theorem on arithmetic progressions
(`Nat.infinite_setOfPred_prime_and_eq_mod`), Dirichlet's unit theorem, Dirichlet's
approximation theorem, Ax–Grothendieck. Conversely the **prime number theorem**
is recorded as `formalized_outside_mathlib` (URL only) even though
`NumberTheory/PrimeCounting` and `Chebyshev` exist in mathlib. The board's
status field tracks *attribution*, not mathlib's capability, and drifts from it.

## B.3 What would actually expand the board most (with reasons)

Ranked by my assessment, not by the degenerate score:

1. **Weak Mordell–Weil → Mordell–Weil** — completes a corridor whose other
   three ingredients landed recently; converts a deep leaf region into a
   connected one; prerequisites present. Best board-expansion efficiency found.
2. **A `ν(m)`-style prime-valuation interface + eventual-periodicity lemmas for
   `ZMod`** — small, cheap, and it is where our own laboratory's output would
   land (Report E). Not a 1000+ target at all, which is itself informative.
3. **General Szemerédi** — large but inward-facing.
4. **Differential-topology cluster (MSC 57: Stokes, de Rham, Poincaré–Hopf,
   Ehresmann, …)** — the class the automated score ranks first. 36–83 missing
   targets over a thin `Geometry` area: formalizing the shared infrastructure
   (manifolds-with-corners integration, de Rham cohomology) would unlock many
   entries at once. High value, high difficulty, and genuinely the best *class*-
   level bet even though the per-target ordering inside it is meaningless.

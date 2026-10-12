# Report N — `openai/NavierStokesAndEuler`: a second external Lean region

First-pass analysis, same method as Reports H and I. Retrieved 2026-09-09,
repository commit `8937a8f4` dated **2026-09-08** — roughly a day old at the time
of writing, and correspondingly unreviewed.

| | |
|---|---|
| repository | `openai/NavierStokesAndEuler` |
| commit | `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538` (2026-09-08) |
| toolchain | `leanprover/lean4:v4.34.0-rc2` |
| mathlib pin | **v4.34.0-rc2** — essentially the commit this board map measured (`110cb7f0`) |
| licence | Apache-2.0 |

## N.1 What it claims

Per its README and `formalization.yaml`: Lean formalizations of finite-time
blowup for the 3-D incompressible Navier–Stokes equations with smooth forcing,
for every positive viscosity, on both ℝ³ and the periodic torus ℝ³/ℤ³ — which
it identifies as alternatives **(C)** and **(D)** of the Clay Millennium problem
description — plus unforced Euler blowup on ℝ³.

The proved statements are named and exposed:

* `NavierStokes.Comparator.navier_stokes_breakdown_R3 (nu) (hnu : nu > 0)` —
  ∃ u₀ f, decay conditions ∧ ¬∃ v p, `NavierStokesExistenceAndSmoothnessRn nu u₀ f v p`
* `NavierStokes.Comparator.navier_stokes_breakdown_periodic` — the torus analogue
* `Euler.Solution.euler_breakdown_R3`

**I am relaying these claims, not adjudicating them.** Whether this settles the
Millennium problem is a question about the precise Clay formulation and about
mathematics I have not checked; nothing in this report bears on it.

## N.2 What I verified locally, and what I did not

**Verified (mechanical checks I ran):**

* **Hygiene.** Across the 2 484 `.lean` files of `NavierStokes/` and `Euler/`:
  **zero** occurrences of `sorry`, `axiom`, `native_decide`, `partial def`,
  `implemented_by`, `unsafe` or `#eval`. The `ComparatorChallenges/` files are
  excluded by design — they are *challenge statements* and contain intentional
  `sorry` placeholders, the same convention the FLT artifact uses.
* **Structure**: 49 379 declarations (37 301 theorems, 10 540 defs, 863 abbrevs,
  627 structures), 2 484 internal modules, maximum internal import depth 96.
* The headline theorems exist under the names above and each file ends with
  `#print axioms` on them.

**Not verified:** that any of it type-checks. No Lean toolchain is reachable
here (`elan` is egress-blocked, as recorded since the earlier phase). The
repository's own verification route — Comparator plus `nanoda_bin` against
`ComparatorChallenges/*.json` — is a claim I am relaying, exactly as with the
FLT artifact. Absence of `sorry` is necessary, not sufficient.

One point in its favour worth recording: the Comparator challenge statements are
**adapted from DeepMind's `formal-conjectures` Navier–Stokes formalization**, so
the reference statement is third-party rather than self-authored. That is a
stronger arrangement than a project grading its own statement.

## N.3 What it does to the map

### It is a second external region, and a differently shaped one

| | FLT artifact | NS/Euler |
|---|---|---|
| declarations | 29 511 theorems | **49 379** |
| `.lean` files | 60 478 | 2 484 |
| distinct mathlib modules imported | 1 696 | **303** |
| as a fraction of mathlib | 19.9% | **3.5%** |
| mathlib pin | v4.33.0 | v4.34.0-rc2 |

**The NS artifact is larger in declarations and rests on a sixth as much of
mathlib.** Its consumption is narrow and deep: Analysis 136 modules,
MeasureTheory 52, Topology 36, Algebra 22, LinearAlgebra 14 — and essentially
nothing else. The FLT artifact's profile was broad (RingTheory 324, Algebra 277,
Analysis 217, …). Two hard theorems, two completely different shapes of
dependence on the shared library.

Because this one pins **v4.34.0-rc2**, the 3.5% coverage figure is like-for-like
against the board map, where the FLT comparison had to be hedged for version drift.

### It is invisible to the 1000+ board

Searching the 1 199 board entries for Navier–Stokes, Euler equations, fluid
mechanics or Millennium problems returns **nothing**. This is the third
independent instance of the Report C.6 / I.9 finding: the board indexes *named
classical theorems*, and the mathematics that large formalization efforts
actually target — modular curves and automorphic forms in one case, PDE blowup
in the other — is not on it. A strategy that uses the 1000+ board as its map of
Lean would not have seen either artifact.

### It sharpens the "territory available to Lean" correction

Report H established that "missing from mathlib" ≠ "missing from Lean". Two
artifacts in two days, from two labs, both large, both outside mathlib, both
pinned to a fixed mathlib version and each self-contained: the external
territory is not one exceptional repository, it is becoming a category. Any
future refresh of the Bridge Ledger should treat external proof repositories as
a **first-class source**, not an overlay — `external_proofs.json` was built for
one entry and now needs at least two.

## N.4 What would be worth doing next with it

Not now, and not without a decision: the Phase-1 boundary analysis that was run
for FLT (upstreamable subset, statement-vocabulary split, blind region
discovery, interface compression) applies unchanged and would take about the
same effort. The interesting comparison would be **whether the same structural
findings hold in an analysis-flavoured corpus**: FLT's regions were real
(Q = 0.677) but joined by broad seams, and its breadth-over-frequency forecasting
result held in 6 of 6 splits. Whether those are facts about large formal proofs
in general, or facts about arithmetic geometry, is exactly the question a second
artifact of a different shape can answer — and that is a better use of it than
re-deriving what we already know.

# Report A — Board map: the completed 1000+ entries

Scope: the 215 entries with a mathlib declaration (214 formalized + 1 statement-only),
comprising 265 declarations. Scores from `scores.json`; raw components in
`bridge_ledger.csv`. Versions and method: `README.md`.

## A.0 The headline structural fact

**191 of the 265 board declarations (72%) are referenced by no other file in
mathlib.** Only 3 are referenced by 10 or more. By declaration kind: 197
theorems, 17 lemmas, 20 `def`s, 5 instances, 3 aliases, 22 unresolved by the
indexer, and exactly **one `class`**.

The 1000+ board, as formalized, is overwhelmingly a collection of **terminal
results**. It is a list of destinations, not a road network. Any strategy that
treats "being on the board" as evidence of formal leverage is mistaken for
three entries out of four.

Two caveats before this is over-read. Instances (5 rows) are consumed by
typeclass inference and are systematically undercounted — the fundamental
theorem of algebra shows 1 use and is in truth ubiquitous. And a theorem can be
valuable to *readers* while being formally terminal. The claim here is narrow
and structural: most board entries are not load-bearing for other mathlib code.

## A.1 High board value

`B(T)` = 0.35·usage + 0.25·module reach + 0.20·depth beneath + 0.20·infrastructure kind,
each component min-max normalized on `log1p`. Weights fixed before inspection.

| rank | declaration | theorem | area | files using | B |
|---|---|---|---|---|---|
| 1 | `UniqueFactorizationMonoid` | Fundamental theorem of arithmetic | RingTheory | **61** | **0.908** |
| 2 | `Ideal.quotientInfRingEquivPiQuotient` | Chinese remainder theorem | RingTheory | 4 | 0.726 |
| 3 | `InnerProductSpace.toDual` | Riesz representation | Analysis | 8 | 0.723 |
| 4 | `add_pow` | Binomial theorem | Data.Nat.Choose | **36** | 0.706 |
| 5 | `QuotientGroup.quotientKerEquivRange` | First isomorphism theorem | GroupTheory | 2 | 0.690 |
| 6 | `MulAction.orbitEquivQuotientStabilizer` | Orbit–stabilizer | GroupTheory | 2 | 0.690 |
| 7 | `ZMod.chineseRemainder` | Chinese remainder theorem | Data | 2 | 0.684 |
| 8 | `QuotientGroup.quotientInfEquivProdNormalQuotient` | Second isomorphism theorem | GroupTheory | 1 | 0.656 |
| 9 | `QuotientGroup.quotientQuotientEquivQuotient` | Lattice/third isomorphism theorem | GroupTheory | 1 | 0.656 |
| 10 | `tendsto_of_tendsto_of_tendsto_of_le_of_le'` | Squeeze theorem | Topology | 15 | 0.630 |

**Eight of this top ten are interfaces, not results.** Six are `def`s producing
an equivalence (`≃`), a quotient construction, or a lattice; one is a `class`;
only the binomial and squeeze theorems are ordinary theorems, and both earn
their place by raw reuse. `ACTUAL_SHARED_ABSTRACTION` for all usage
figures; `ACTUAL_LEAN_DEPENDENCY` for the module-reach component.

## A.2 High bridge value

`R(T)` = 0.40·domain spread + 0.25·importer-area diversity + 0.20·interface kind
+ 0.15·region growth. Domain spread = distinct top-level Mathlib areas whose
files reference the declaration.

| rank | declaration | theorem | areas using it | R |
|---|---|---|---|---|
| 1 | `UniqueFactorizationMonoid` | Fundamental theorem of arithmetic | **6** | **0.931** |
| 2 | `tendsto_of_tendsto_of_tendsto_of_le_of_le'` | Squeeze theorem | 5 | 0.703 |
| 3 | `Ideal.quotientInfRingEquivPiQuotient` | Chinese remainder theorem | 2 | 0.683 |
| 4 | `ZMod.chineseRemainder` | Chinese remainder theorem | 2 | 0.678 |
| 5 | `QuotientGroup.quotientKerEquivRange` | First isomorphism theorem | 2 | 0.657 |
| 6 | `MulAction.orbitEquivQuotientStabilizer` | Orbit–stabilizer | 2 | 0.657 |
| 7 | `InnerProductSpace.toDual` | Riesz representation | 4 | 0.624 |

`add_pow` (the binomial theorem, `Mathlib/Data/Nat/Choose/Sum.lean`) is second
on both dimensions and has the **widest domain spread on the entire board — 36
referencing files across 9 distinct areas** (Algebra, AlgebraicGeometry,
Analysis, Data, FieldTheory, LinearAlgebra, NumberTheory, Probability,
RingTheory). It is the clearest example of a mathematically modest statement
with genuine cross-domain reach, and the only plain theorem that competes with
the interfaces.

*Correction made during the analysis:* the first run resolved `add_pow` to
`Mathlib/Algebra/Tropical/Basic.lean`, because that file declares a bare
`theorem add_pow` inside `namespace Tropical` and was scanned first. The
declaration index now prefers root-level declarations for unqualified names.
The board's `decl: add_pow` does resolve correctly in current mathlib, to
`Mathlib/Data/Nat/Choose/Sum.lean:76`.

## A.3 High on both — the existing hubs

Ranked by `B + R`:

1. **`UniqueFactorizationMonoid`** (0.908 / 0.931) — the strongest hub on the
   board by a wide margin, and the **only `class`** among 265 declarations.
2. **`add_pow`**, the binomial theorem (0.706 / 0.787) — the widest reach of any
   ordinary theorem on the board.
3. **`Ideal.quotientInfRingEquivPiQuotient`** and **`ZMod.chineseRemainder`**
   (CRT, two independent formalizations) — 0.726/0.683 and 0.684/0.678.
4. **The three isomorphism theorems + orbit–stabilizer** — a tight cluster
   (0.656–0.690 board, 0.587–0.657 bridge) all built on `QuotientGroup`.

## A.4 Surprising rankings, explained

**Why the fundamental theorem of arithmetic is first, and it is not close.**
Its board entry does not point at a theorem. It points at
`UniqueFactorizationMonoid`, a *typeclass*: the property "every element factors
uniquely into irreducibles", stated for an arbitrary monoid. mathlib records
the theorem by making ℕ an instance of an abstraction that 61 files across 6
areas then use as a hypothesis. Unique factorization has become an interface
other mathematics is written against. No other 1000+ entry has been abstracted
this way. This is precisely the prompt's "modest-looking theorem with enormous
board value", and it is the single most important observation in this report:
**the board's top node is a class, not a theorem.**

**Why famous theorems rank low.** Measured usage, in files:

| theorem | declaration | files using | areas |
|---|---|---|---|
| Pythagorean theorem | `EuclideanGeometry.dist_sq_eq_dist_sq_add_dist_sq_iff_angle_eq_pi_div_two` | **0** | 0 |
| Wilson's theorem | `ZMod.wilsons_lemma` | **0** | 0 |
| Euler's theorem (totient) | `Nat.ModEq.pow_totient` | **0** | 0 |
| Abel's theorem | `Complex.tendsto_tsum_powerSeries_nhdsWithin_stolzSet` | **0** | 0 |
| Cauchy–Hadamard | `FormalMultilinearSeries.radius_inv_eq_limsup` | **0** | 0 |
| Sylow theorems | `Sylow.isPretransitive_of_finite` | **0** | 0 |
| Fermat's Last Theorem | `FermatLastTheorem` (statement only) | 1 | 1 |
| Quadratic reciprocity | `legendreSym.quadratic_reciprocity` | 2 | 1 |
| Cayley–Hamilton | `Matrix.aeval_self_charpoly` | 2 | 1 |
| Lagrange (group theory) | `Subgroup.card_subgroup_dvd_card` | 1 | 1 |

The pattern is systematic. A statement about a *specific object* (a right
triangle, a prime modulus, a particular series) is used once, when it is
proved. A statement that *defines an interface* over arbitrary structures gets
used forever. The board's fame ordering and its formal-leverage ordering are
close to unrelated.

Two of these deserve their own note. **Euler's theorem** (`x^φ(n) ≡ 1`) shows
zero uses even though the *fact* is used constantly — because mathlib's working
form is the unit-group statement `ZMod.pow_totient` / `pow_carmichael`, and
downstream code reaches for `Monoid.exponent` instead. The board entry points
at the human-facing name, not at the load-bearing one. **Sylow** shows zero uses
for the particular declaration the board names, while `Sylow` as a structure is
used widely — the board records one theorem out of a region.

**Board entries are not the unit of formal value.** In at least three cases
here (Euler, Sylow, FTA) the entry names one declaration inside a cluster whose
value lives elsewhere in the cluster. This is a limitation of the 1000+ board as
a strategic map, not of mathlib — and it is the central reason Report C works
with *regions* rather than entries.

# Report C — Major Lean proof regions

A *region* is a cluster of mathlib modules sharing abstractions, not a board
entry. Statistics from `modules.json` / `scores.json`: module counts and
transitive import/importer counts are exact; "recent touches" counts file
changes over 2 000 commits (2026-06-17 → 2026-09-08).

## C.0 The whole library at a glance

| area | modules | recent touches | mean transitive imports | mean transitive importers |
|---|---|---|---|---|
| Algebra | 1 360 | 3 693 | 894 | 2 177 |
| CategoryTheory | 1 116 | 3 241 | 1 478 | 279 |
| Analysis | 808 | 2 660 | 1 910 | 285 |
| Data | 656 | 1 788 | 474 | 3 000 |
| RingTheory | 728 | 2 453 | 1 632 | 346 |
| Topology | 694 | 2 330 | 1 067 | 1 406 |
| NumberTheory | 249 | 914 | 2 300 | 26 |
| Combinatorics | 200 | 621 | 1 098 | 105 |
| AlgebraicTopology | 163 | 500 | 1 547 | 19 |
| AlgebraicGeometry | 140 | 499 | 2 368 | 24 |
| Probability | 140 | 450 | 2 407 | 28 |

Read the last two columns as coordinates: **mean transitive imports = depth**
(how much library a region stands on), **mean transitive importers = reach**
(how much stands on it). `Data` and `Algebra` are shallow and enormously
depended-upon — they are the foundation. `AlgebraicGeometry` is the deepest
region in the library (2 368) with almost no reach (24) — it is the roof.

## C.1 Foundation regions (shallow, enormous reach)

**`Mathlib.Algebra` + `Mathlib.Data` + `Mathlib.Order`.** These carry the
typeclass hierarchy every other region is written against. Board entries landing
here (`add_pow`, `Nat.gcd_eq_gcd_ab`, `ZMod.chineseRemainder`) inherit
cross-domain reach automatically — `add_pow` is used in 9 distinct areas, the
widest spread on the board. Growing fast in absolute terms (3 693 touches) but
mostly by refactoring rather than new mathematics.

## C.2 The algebraic-structure region — where the board's hubs live

* **Central abstractions**: `UniqueFactorizationMonoid`, `EuclideanDomain`,
  `Ideal.Quotient`, `IsDedekindDomain`, `QuotientGroup`, `MulAction`.
* **Board entries**: fundamental theorem of arithmetic (the `class`), CRT (twice),
  the three isomorphism theorems, orbit–stabilizer, Bézout.
* **Status**: mature; this is where 6 of the top 10 board-value entries sit.
* **Entry points**: `UniqueFactorizationMonoid` (61 files, 6 areas),
  `Ideal.quotientInfRingEquivPiQuotient`.
* **Bottlenecks**: none evident — this region is the library's connective tissue.

## C.3 `FieldTheory.Finite` + `GroupTheory.Exponent` — small, dense, high-traffic

* 7 modules (`FieldTheory/Finite/`), **880 transitive importers**;
  `GroupTheory/Exponent` is a **single module with 1 385 transitive importers**.
* Contains Fermat's little theorem (`ZMod.pow_card`, `ZMod.pow_card_sub_one_eq_one`),
  Euler's theorem (`ZMod.pow_totient`), `Monoid.exponent` and its API
  (`exponent_dvd_iff_forall_pow_eq_one`).
* Adjacent: `NumberTheory/ArithmeticFunction/` (8 modules, 297 importers)
  contains **`ArithmeticFunction.carmichael`**, defined as
  `Monoid.exponent (ZMod n)ˣ` with `carmichael_eq_exponent`, `pow_carmichael`,
  `carmichael_lcm`, `carmichael_factorization`.
* **This is the highest-traffic small region on the board's number-theory side,
  and it is the region our own laboratory's results land in (Report E).**

## C.4 The elliptic-curve / arithmetic-geometry corridor (Section 8's question)

Measured, not assumed:

| sub-region | modules | mean transitive imports | Σ transitive importers |
|---|---|---|---|
| `AlgebraicGeometry.EllipticCurve` | 19 | 1 927 | **76** |
| `NumberTheory.Height` | 6 | 2 092 | **8** |
| `NumberTheory.FLT` | 5 | 1 925 | **4** |
| `NumberTheory.ModularForms` | 40 | 2 742 | 454 |
| `NumberTheory.NumberField` | 44 | 2 863 | 468 |

* **Central abstractions**: `WeierstrassCurve`, `WeierstrassCurve.Affine.Point`
  with `instance : AddCommGroup W.Point`, `Jacobian`/`Projective` coordinates,
  `DivisionPolynomial`, `Northcott`, `logHeight`.
* **Existing**: full Weierstrass API in three coordinate systems, group law,
  division polynomials, reduction, `IsomOfJ`, `LFunction`; heights with the
  Northcott property; `finite_torsion` for `W.Point`; descent
  (`GroupTheory/Descent.lean`).
* **Missing**: weak Mordell–Weil (`E(K)/2E(K)` finite), hence Mordell–Weil;
  modularity; Selmer groups *for elliptic curves* (they exist for Dedekind
  fraction fields, `RingTheory/DedekindDomain/SelmerGroup.lean`).
* **Verdict on the corridor question**: it is a **deep leaf**, not yet a bridge.
  Depth 1 927–2 092 (it stands on nearly a quarter of the library) with reach
  76 and 8. Nothing of consequence imports it. The conceptual relationship
  "Diophantine → elliptic curves → arithmetic geometry → number theory
  infrastructure" is **not** currently a formal route: the arrows run *into*
  this region and stop.
* **Is it growing?** Yes, and recently: `NumberTheory/Height/` and
  `GroupTheory/Descent.lean` are new and exist specifically to reach
  Mordell–Weil. This is the fastest-improving strategic corridor found.

## C.5 `NumberTheory.ModularForms` — the surprise

40 modules and 454 transitive importers: substantially larger and better
connected than the elliptic-curve region, with `DimensionFormulas`, `LevelOne`,
`EisensteinSeries`, `Petersson`, `JacobiTheta`, `QExpansion`, `DedekindEta`.
Anyone reasoning from the FLT narrative would expect modular forms to be the
thin, exotic part and elliptic curves the developed part; the measurements say
the opposite. The two regions are **not connected to each other** — which is
precisely where modularity would go.

## C.6 Category theory — the largest region no board entry touches

1 116 modules, 3 241 recent touches, the second-largest area in mathlib. Its
intersection with the 1000+ board is essentially empty. This is a structural
comment on the board rather than on mathlib: the 1000+ list is a list of
*named classical theorems*, and modern structural mathematics does not produce
those. Any strategy that uses the board as its map of Lean will be blind to
roughly a seventh of the library.

## C.7 Regions blocked by missing infrastructure

* **Differential topology / de Rham (MSC 57, 55)** — 83+ missing targets over a
  thin `Geometry` area; blocked on integration on manifolds and de Rham
  cohomology. Largest single unlock available.
* **Arithmetic geometry beyond curves** — blocked on weak Mordell–Weil for the
  Diophantine direction, and on the modular-forms ↔ elliptic-curves link.
* **Analytic number theory** — `PrimeCounting`/`Chebyshev` exist; PNT itself is
  attributed outside mathlib, so the region has a hole where its keystone
  should be.

# Report D — FLT-centred bridge map

**Fermat's Little Theorem and Fermat's Last Theorem are different theorems with
different board positions and are kept separate throughout.**

## D.1 Fermat's LITTLE theorem — a hub in a high-traffic region

| | |
|---|---|
| Declarations | `ZMod.pow_card : x ^ p = x`, `ZMod.pow_card_sub_one_eq_one`, `FiniteField.pow_card`, `ZMod.pow_card_pow` |
| Module | `Mathlib/FieldTheory/Finite/Basic.lean` |
| Region | `FieldTheory.Finite` — 7 modules, **880 transitive importers** |
| Neighbours | `ZMod.pow_totient` (Euler), `Monoid.exponent`, `ArithmeticFunction.carmichael`, `frobenius_zmod` |

`ACTUAL_LEAN_DEPENDENCY`: `ZMod.pow_card` is proved from `FiniteField.pow_card`
in the same file, and the file is imported across the number-theory and
field-theory regions. `ACTUAL_SHARED_ABSTRACTION`: it sits directly beside the
Frobenius endomorphism (`frobenius_zmod` is proved *by* `ZMod.pow_card`), which
is the interface through which it reaches Galois theory and algebraic geometry.

Outward routes that are real today:

* → **finite fields / Galois theory**: via `frobenius`, `GaloisField`
  (`ACTUAL_LEAN_DEPENDENCY`).
* → **group exponent**: via `ZMod.pow_totient` and `Monoid.exponent`
  (`ACTUAL_SHARED_ABSTRACTION`).
* → **primality testing / pseudoprimes**: `NumberTheory/FermatPsp.lean`
  (`ACTUAL_LEAN_DEPENDENCY`), which notes Carmichael numbers are "not yet
  defined" in mathlib — a small, concrete gap.

## D.2 Fermat's LAST theorem — a statement, and a formal cul-de-sac

| | |
|---|---|
| Board status | **statement only** (`statement: FermatLastTheorem`), the only such entry in 1 199 |
| Declarations | `FermatLastTheorem`, `FermatLastTheoremFor`, `FermatLastTheoremWith` (`NumberTheory/FLT/Basic.lean`) |
| Region | `NumberTheory.FLT` — 5 modules, mean 1 925 transitive imports, **4 transitive importers** |
| Board comment | "Formalisation of the proof is on-going in https://imperialcollegelondon.github.io/FLT/" |

What is actually proved in mathlib:

* `FLT/Four.lean` — n = 4 (via `Nat.PythagoreanTriple` machinery).
* `FLT/Three.lean` — n = 3, with `FermatLastTheoremForThreeGen` over ℤ[ζ₃],
  routing through `NumberTheory/NumberField/Cyclotomic/Three.lean`.
* `FLT/Polynomial.lean` + `FLT/MasonStothers.lean` — the polynomial analogue and
  Mason–Stothers (the abc-analogue for polynomials).

The region has **4 transitive importers**: nothing builds on FLT. Its measured
board value (0.475) comes almost entirely from depth — it stands on 1 925
modules — not from reach.

### Where FLT-derived mathematics can actually enter larger regions

The honest answer is that **FLT itself is a terminus; its neighbourhood is the
bridge**. Four routes, labelled:

1. **Cyclotomic fields** (`ACTUAL_LEAN_DEPENDENCY`). `FLT/Three.lean` imports
   `NumberField/Cyclotomic/*`, which connects to `NumberField` (44 modules, 468
   importers), class numbers, and the unit theorem. This is the only route by
   which today's FLT files touch a well-connected region. Kummer's regular-prime
   approach (`FltRegular`, developed outside mathlib) is its natural extension.
2. **Mason–Stothers / abc** (`ACTUAL_LEAN_DEPENDENCY` inside `FLT/`;
   `PLAUSIBLE_FORMAL_BRIDGE` outward). The polynomial abc theorem is proved and
   is a genuine interface to function-field arithmetic and to the
   height/Northcott machinery in `NumberTheory/Height/`. Nothing currently
   connects them; the mathematical relation is standard.
3. **Elliptic curves → modularity** (`SPECULATIVE_RESEARCH_BRIDGE` from
   mathlib's state). The Frey-curve route needs modularity, which needs the
   modular-forms region (40 modules, present) to be joined to the elliptic-curve
   region (19 modules, present). Neither imports the other. This is the FLT
   project's own multi-year target, not a Phase-0 opportunity.
4. **Pythagorean triples / Diophantine descent** (`ACTUAL_SHARED_ABSTRACTION`).
   `FLT/Four.lean` shares `PythagoreanTriple` with the Pythagorean-theorem
   neighbourhood, and descent is now abstracted in `GroupTheory/Descent.lean`.

### Landing pads for a newly discovered FLT-adjacent theorem

If the theorem-space engine produced a Diophantine statement, the pads that
exist today are: `FermatLastTheoremWith R n` (already parameterized over an
arbitrary semiring — a ready-made generalization interface),
`PythagoreanTriple`, `Polynomial.abc`-style statements in `MasonStothers`, and
`WeierstrassCurve.Affine.Point`. Of these, **`FermatLastTheoremWith` is the most
interesting**: mathlib has already done the generalization step (from ℕ to an
arbitrary semiring), so a discovered statement about power identities in a ring
can instantiate it directly.

## D.3 The corridor verdict (Section 8)

The chain "Diophantine equations → elliptic curves → arithmetic geometry →
larger number-theoretic infrastructure" is **mathematically real and formally
absent**. Measured: the elliptic-curve region has 76 transitive importers, the
height region 8, the FLT region 4. Arrows run in and stop.

But the corridor is being built right now, and the gap is identified precisely:
`GroupTheory/Descent.lean` + `NumberTheory/Height/EllipticCurve.lean` supply
three of the four Mordell–Weil ingredients (group law, Northcott heights,
descent, torsion finiteness — all present), and the missing piece is **weak
Mordell–Weil**, `E(K)/2E(K)` finite, whose own prerequisites (class number
finiteness, Dirichlet's unit theorem) are already formalized.

**Mordell–Weil, assessed on the same framework as every other target, is the
highest-value bridge in this corridor** — not because it is famous, but because
it is the unique missing edge between a deep leaf region and the connected
number-field region, and because three of its four ingredients landed in the
last few months.

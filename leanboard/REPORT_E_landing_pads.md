# Report E — Landing-pad catalogue

A **landing pad** is an existing Lean declaration a newly discovered theorem
could instantiate, generalize, or plug into. Every pad below was read in the
mathlib checkout at commit `110cb7f0`; paths and names are quoted from source.

## E.1 The pads that matter most (measured by region traffic)

| pad | kind | module | region reach | what lands on it |
|---|---|---|---|---|
| `Monoid.exponent` + `exponent_dvd_iff_forall_pow_eq_one` | def + iff-lemma | `Mathlib/GroupTheory/Exponent.lean` | **1 385 transitive importers** | any "∀ g, gⁿ = 1" statement |
| `ArithmeticFunction.carmichael` (`= Monoid.exponent (ZMod n)ˣ`) | def | `Mathlib/NumberTheory/ArithmeticFunction/Carmichael.lean` | 297 (region) | statements about λ(n) |
| `ZMod.pow_card`, `ZMod.pow_totient` | theorems | `Mathlib/FieldTheory/Finite/Basic.lean` | **880** (region) | power identities mod n |
| `UniqueFactorizationMonoid` | **class** | `Mathlib/RingTheory/UniqueFactorizationDomain/` | 61 files, 6 areas | factorization-shaped hypotheses |
| `IsDedekindDomain`, `Ideal.Quotient`, `Ideal.quotientInfRingEquivPiQuotient` | class + defs | `Mathlib/RingTheory/` | high | CRT-shaped decompositions |
| `QuotientGroup.quotientKerEquivRange`, `MulAction.orbitEquivQuotientStabilizer` | defs (`≃`) | `Mathlib/GroupTheory/` | high | any group-quotient correspondence |
| `FermatLastTheoremWith R n` | def over an arbitrary semiring | `Mathlib/NumberTheory/FLT/Basic.lean` | 4 | Diophantine non-existence statements |
| `WeierstrassCurve.Affine.Point` + `AddCommGroup W.Point` | structure + instance | `Mathlib/AlgebraicGeometry/EllipticCurve/Affine/Point.lean` | 76 (region) | rational-point statements |
| `Northcott`, `logHeight` | class + def | `Mathlib/NumberTheory/Height/` | 8 | height/finiteness statements |
| `AddCommGroup.fg_of_descent'` | theorem | `Mathlib/GroupTheory/Descent.lean` | 1 | descent arguments |

The pattern from Report A repeats: the best pads are **classes and `≃`-valued
defs**, not theorems. A discovery that can be phrased as "this structure
satisfies `C`" lands on an interface and inherits its reach; a discovery phrased
as "this specific object has this property" lands nowhere.

## E.2 Interface types available, with their concrete Lean names

* **divisibility** — `Dvd`, `Nat.factorization`, `padicValNat` (note:
  `Nat.maxPowDiv` is an alias of `padicValNat`)
* **finite cyclic groups / orders** — `orderOf`, `IsCyclic`, `Monoid.exponent`,
  `ZMod.unitsCyclic` (`RingTheory/ZMod/UnitsCyclic.lean`)
* **ring/field properties** — `IsDomain`, `EuclideanDomain`, `IsDedekindDomain`,
  `UniqueFactorizationMonoid`
* **polynomial identities** — `Polynomial.aeval`, `Matrix.aeval_self_charpoly`,
  `MasonStothers`
* **finite fields** — `FiniteField`, `GaloisField`, `frobenius`
* **group actions** — `MulAction`, `MulAction.orbitEquivQuotientStabilizer`
* **modules** — `Module.Finite`, `AddCommGroup.torsion`, `Module.Free`
* **algebraic extensions** — `IsAlgClosed`, `IntermediateField`,
  `Field.exists_primitive_element`
* **valuations** — `Valuation`, `IsDedekindDomain.HeightOneSpectrum`
* **Diophantine relations** — `PythagoreanTriple`, `FermatLastTheoremWith`

## E.3 Candidate shape → abstraction → region (the mechanism)

### E.3.1 A real case, not hypothetical: our laboratory's U-family rule

The theorem-space laboratory (`../theorem-lab/`) selected, before its freeze and
with 0 errors over 6 720 tests, the rule

> `U(m,k) ⟺ period(m) ∣ (k − 1)`, where `period(m)` is the row's calibrated
> period — verified equal to `λ(m)` on all 48 tested moduli.

Its landing pad exists and is exact:

| shape | Lean abstraction | region |
|---|---|---|
| `∀ x ∈ (ZMod m)ˣ, x^k = x` ⟺ `λ(m) ∣ k−1` | `ArithmeticFunction.carmichael` + `Monoid.exponent_dvd_iff_forall_pow_eq_one` | `FieldTheory.Finite` / `GroupTheory.Exponent` (880 / 1 385 importers) |

Both halves are already present: `pow_carmichael : a ^ carmichael n = 1` gives
one direction, and `exponent_dvd_iff_forall_pow_eq_one : exponent G ∣ n ↔ ∀ g, g ^ n = 1`
gives the converse, with `carmichael_eq_exponent` bridging the two names. The
statement is a short derivation from existing lemmas — `PLAUSIBLE_FORMAL_BRIDGE`
with unusually high confidence, since I read both lemmas and they compose.

**What this tells us about the discovery engine is uncomfortable and useful:
the theorem our system "discovered" is one mathlib can already almost state, and
the pad it lands on makes the discovery redundant rather than valuable.** A
discovery engine aimed at high-traffic pads will keep rediscovering the
neighbourhood of `Monoid.exponent`.

### E.3.2 A real case with a genuine gap: the E-family theorem

The auditor-derived theorem `∀x ∈ ℤ/m, x^{r+d} = x^r ⟺ r ≥ ν(m) ∧ λ(m) ∣ d`
(Phase 13 of the previous report) has **one missing pad**: `ν(m) = max_p v_p(m)`
has no named form in mathlib. `padicValNat` gives `v_p`; the sup over
`n.primeFactors` is not defined. So this theorem would require introducing a
small definition — which is exactly the kind of *interface-creating* contribution
Report A shows to be valuable, and it is not a 1000+ board target at all.

### E.3.3 Hypothetical examples (labelled as such — no such discovery exists)

**HYPOTHETICAL.** These illustrate the mechanism only:

| hypothetical discovered shape | pad it would land on | region entered |
|---|---|---|
| "every element of *R* factors uniquely into irreducibles under condition *C*" | `UniqueFactorizationMonoid` (instance) | RingTheory, 6 areas |
| "this parameterized family of Diophantine equations has no solutions for *n* ≥ *N*" | `FermatLastTheoremWith R n` | NumberTheory.FLT (leaf) |
| "these two group quotients are canonically isomorphic" | `QuotientGroup.*Equiv*` | GroupTheory (high reach) |
| "this height function on *G* satisfies an approximate parallelogram law" | `AddCommGroup.fg_of_descent'` | the Mordell–Weil corridor |

The fourth is the interesting one: a discovery of that shape would land on a pad
whose region is one lemma from opening (Report D).

## E.4 Pads to avoid

Terminal theorem statements about specific objects — `ZMod.wilsons_lemma`,
`EuclideanGeometry.dist_sq_eq_...` (Pythagoras), `Nat.ModEq.pow_totient`. Each
has **zero** in-library uses. Instantiating one of these adds a fact to a
cul-de-sac. This is the concrete meaning of "high board value, no bridge value".

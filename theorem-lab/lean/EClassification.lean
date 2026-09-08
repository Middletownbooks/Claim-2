/-
  UNCHECKED SPECIFICATION.  Provenance: MATHEMATICALLY_DERIVED (auditor), NOT FORMALLY_VERIFIED.

  This file has never been elaborated: no Lean toolchain is reachable from the audit
  environment (see audit/PHASE14_lean_status.md).  It contains propositions and a proof
  outline in comments.  It contains no `sorry`, and it must not be described as verified,
  type-checked, or compiled.  Nothing here has been machine-checked in any sense.
-/
import Mathlib

namespace BlindLabAudit

/-- The deformation family the laboratory calls `E`, stated over `ZMod m`. -/
def E (m r d : ℕ) : Prop := ∀ x : ZMod m, x ^ (r + d) = x ^ r

/-- `ν m = max_p v_p(m)`, the nilpotency depth of the maximal ideal‑wise part.
    `ν 1 = 0` since the factorization of `1` has empty support. -/
noncomputable def nu (m : ℕ) : ℕ :=
  (Nat.factorization m).support.sup (Nat.factorization m)

/-- The Carmichael exponent, taken as the exponent of the unit group rather than as a
    numeric formula, so that the statement does not presuppose the case analysis on `2^e`. -/
noncomputable def lam (m : ℕ) : ℕ := Monoid.exponent (ZMod m)ˣ

/-- The classification the auditor derived in Phase 13 and the experiment's 48 fitted
    row pairs agree with.  STATEMENT ONLY — no proof term is supplied here. -/
def Classification : Prop :=
  ∀ m r d : ℕ, 0 < m → 1 ≤ r → 1 ≤ d →
    (E m r d ↔ (nu m ≤ r ∧ lam m ∣ d))

/-
  Proof outline (paper proof in audit/PHASE13_mathematics.md; not formalised):

  1.  `ZMod m ≃+* Π p ∈ m.primeFactors, ZMod (p ^ m.factorization p)`
      (`ZMod.chineseRemainder` / `Nat.factorization` machinery).  `E` is a universally
      quantified identity, so it transfers componentwise; `nu` is the sup and `lam` the
      lcm of the components, so both sides of the iff decompose the same way.
  2.  Prime-power case, direction (←):
      * units: `x ∈ (ZMod (p^e))ˣ`, `lam ∣ d` gives `x ^ d = 1` by
        `Monoid.exponent` dividing, hence `x ^ (r+d) = x ^ r`;
      * non-units: `p ∣ x` and `e ≤ r` give `x ^ r = 0 = x ^ (r+d)`.
  3.  Prime-power case, direction (→):
      * apply the identity to an element of order `lam (p^e)` (cyclic for odd `p` and for
        `p^e ∈ {2,4}`; `3` has order `2^(e-2)` for `e ≥ 3`) and cancel the unit `x ^ r`;
      * apply it to `x = p`: if `r < e` then `p ^ (e-r) ∣ p ^ d - 1`, contradicting `p ∤ p^d - 1`.

  Formalisation obstacles actually encountered are recorded in
  audit/PHASE14_lean_status.md; the largest is step 1, which needs the ring equivalence
  in a form that pushes a `∀ x` statement through the product, together with
  `Monoid.exponent` of a product of unit groups.
-/

end BlindLabAudit

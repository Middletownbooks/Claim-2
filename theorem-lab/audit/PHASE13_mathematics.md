# Phase 13 — Mathematical interpretation (auditor-side, independent of the experiment)

Provenance: **MATHEMATICALLY_DERIVED by the auditor.** This section is written after
recording what the experiment produced (Phase 4), and none of it was available to the
learner. The learner produced 48 pairs of finite boolean sequences; the theorem below is
the auditor's, and the experiment's contribution is that its 48 fitted pairs agree with it.

## 13.1 Statement

For integers `m ≥ 1`, `r ≥ 1`, `d ≥ 1`, let

    P(m; r, d)  :⟺  ∀ x ∈ ℤ/mℤ,  x^(r+d) = x^r.

Let `ν(m) = max_p v_p(m)` (with `ν(1) = 0`) and let `λ` be the Carmichael function.

> **Theorem.**  `P(m; r, d)  ⟺  r ≥ ν(m)  ∧  λ(m) | d`.

## 13.2 Proof

By the Chinese Remainder Theorem `ℤ/mℤ ≅ ∏_{p^e ‖ m} ℤ/p^eℤ` as rings, and `P` is a
universally quantified identity, so `P(m;r,d)` holds iff it holds in each factor. Also
`ν(m) = max_{p^e ‖ m} e` and `λ(m) = lcm_{p^e ‖ m} λ(p^e)`, so it suffices to prove the
prime-power case:

    P(p^e; r, d)  ⟺  r ≥ e  ∧  λ(p^e) | d.

**(⇐).** Let `x ∈ ℤ/p^eℤ`.
*Units.* If `gcd(x,p) = 1` then `x` lies in `(ℤ/p^eℤ)^×`, a group of exponent `λ(p^e)`.
From `λ(p^e) | d` we get `x^d = 1`, hence `x^{r+d} = x^r · x^d = x^r`.
*Non-units.* Otherwise `p | x`, so `p^r | x^r`, and `r ≥ e` gives `x^r ≡ 0` and likewise
`x^{r+d} ≡ 0` (as `r + d > r ≥ e`). Both sides vanish.

**(⇒).** Assume `P(p^e; r, d)`.
*Necessity of `λ(p^e) | d`.* The group `(ℤ/p^eℤ)^×` has exponent `λ(p^e)` and contains an
element `g` of that exact order (it is cyclic for odd `p` and for `p^e ∈ {2,4}`; for
`p = 2, e ≥ 3` it is `ℤ/2 × ℤ/2^{e-2}` and `3` has order `2^{e-2} = λ(2^e)`). Applying the
identity to `g`, and cancelling the unit `g^r`, gives `g^d = 1`, hence `λ(p^e) = ord(g) | d`.
*Necessity of `r ≥ e`.* Suppose `r < e` and apply the identity to `x = p`:
`p^r (p^d − 1) ≡ 0 (mod p^e)`. Since `r < e`, this forces `p^{e−r} | (p^d − 1)` with
`e − r ≥ 1`, so `p | p^d − 1`, which is false because `d ≥ 1`. Contradiction. ∎

Edge cases: `m = 1` — the ring is trivial, `P` always holds, and the right-hand side reads
`r ≥ 0 ∧ 1 | d`, also always true. `m` squarefree — `ν(m) = 1`, so the threshold is
invisible on the queried domain `r ≥ 1`, which is exactly what the learner reports
(threshold 1 for every squarefree modulus).

## 13.3 What this says about the two mechanisms

The proof separates for the same reason the learner's AND factorisation does: the ring
`ℤ/mℤ` splits into a unit part, where the identity is a statement about the **exponent of
the unit group** and therefore depends only on `d`; and a nilpotent part, where the identity
is a statement about **nilpotency depth** and therefore depends only on `r`. The AND
factorisation is not an artefact of the hypothesis language — it mirrors a genuine direct
product. That is the strongest available reason to regard the learned representation as
tracking a real mechanism rather than fitting a coincidence.

Note carefully what remains *not* discovered: the learner has no term for `ν` or `λ` as
functions of `m`. It has 48 numbers on one axis and 48 numbers on the other. The map
`m ↦ (ν(m), λ(m))` is the mathematics; the experiment produced its restriction to a table.

## 13.4 Consequence for the T family (used to pre-register Phase 15)

`T(m,k) : ∀x, x^k = x` is `P(m; 1, k−1)` for `k ≥ 2`. The theorem therefore gives

    T(m,k)  ⟺  1 ≥ ν(m) ∧ λ(m) | (k−1)  ⟺  m squarefree ∧ λ(m) | (k−1)      (k ≥ 2),

and for squarefree `m`, `λ(m) = lcm_{p|m}(p−1) = L(m)`, recovering the classical statement.
At `k = 1` the identity is `x = x`, trivially true for every `m`, and the classical form is
false there (`d = 0` is outside `P`'s domain) — the 29 mismatches found in §Phase 0/D8.

Immediate prediction: as a function of `k`, each row of the T table is **periodic with
period `λ(m)`**, so a fitter that requires two observed copies of a block needs
`k_train ≥ 2·max_{m ≤ 48} λ(m) = 2·λ(47) = 92`. This is the pre-registered basis for the
Phase 15 range — an auditor-supplied number, not a discovered one.

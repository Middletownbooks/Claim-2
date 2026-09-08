import Mathlib

-- UNCHECKED SPECIFICATION.
-- These are proposition definitions, not theorem proofs.
-- No `sorry` is used and no verification is claimed.
namespace BlindLab

def RealT (m k : Nat) : Prop :=
  ∀ x : Nat, x < m → x ^ k % m = x

def RealE (m r d : Nat) : Prop :=
  ∀ x : Nat, x < m → x ^ (r + d) % m = x ^ r % m

def RealU (m k : Nat) : Prop :=
  ∀ x : Nat, x < m → Nat.gcd x m = 1 → x ^ k % m = x

end BlindLab

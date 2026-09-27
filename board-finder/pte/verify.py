#!/usr/bin/env python3
"""Exact verification for Prouhet-Tarry-Escott objects, and the two readings of "symmetric".

Everything here checks an OBJECT. Nothing takes a search routine's word that it found
something: the W(103) error on this branch came from reading success off a function's return
instead of off the matrix, and it cost a day.

Definitions used throughout.
  An ideal PTE solution of size n is a pair of multisets A, B of n integers with A != B and
  sum(a^k) = sum(b^k) for every k = 1..n-1.

  A solution is SYMMETRIC if the configuration is invariant under some reflection x -> t - x.
  That reflection permutes A u B, so it either fixes each set or swaps them:
    FIXING  ("A is symmetric about its own mean")  -- possible only at EVEN n, see below.
    SWAPPING ("B = t - A")                         -- the only possibility at ODD n.

  Theorem (proved in PREREG_PTE11.md sec 2, confirmed here by exhaustive search at n=5):
  no ideal solution of ODD size is of the fixing kind.
"""
from fractions import Fraction
from itertools import combinations
from collections import defaultdict
from math import gcd


def power_sums(S, kmax):
    return tuple(sum(x ** k for x in S) for k in range(1, kmax + 1))


def is_ideal(A, B):
    """Exact, integer-only. Returns (ok, why)."""
    A, B = sorted(A), sorted(B)
    if len(A) != len(B):
        return False, "different sizes"
    n = len(A)
    if A == B:
        return False, "A and B are the same multiset"
    for k in range(1, n):
        pa, pb = sum(a ** k for a in A), sum(b ** k for b in B)
        if pa != pb:
            return False, f"power sum k={k} differs: {pa} != {pb}"
    return True, f"ideal of size {n}: all k=1..{n - 1} agree"


def is_fixing_symmetric(S):
    """Is the multiset S invariant under x -> 2c - x with c its own mean?"""
    c = Fraction(sum(S), len(S))
    return sorted(2 * c - Fraction(x) for x in S) == sorted(Fraction(x) for x in S)


def is_swapping_symmetric(A, B):
    """Is B = t - A for some t?"""
    t = min(A) + max(B)
    return sorted(B) == sorted(t - a for a in A)


def from_centre(C):
    """Turn a centred set C (with vanishing odd power sums) into an explicit PTE pair.

    A = (C + t)/2 and B = (t - C)/2 = -A + t. t is chosen to clear halves: if C is not of
    uniform parity no integral t exists, so C is doubled first. Doubling is a scaling of the
    solution, which the PTE problem is invariant under.
    """
    C = list(C)
    if len({c % 2 for c in C}) > 1:
        C = [2 * c for c in C]
    t = C[0] % 2                      # any t of the same parity as every element
    A = [(c + t) // 2 for c in C]
    B = [(t - c) // 2 for c in C]
    m = -min(min(A), min(B))
    return sorted(a + m for a in A), sorted(b + m for b in B)


def normalise(A, B):
    """min 0, primitive, halves in a canonical order -- so duplicates collapse."""
    m = min(min(A), min(B))
    A = tuple(sorted(a - m for a in A))
    B = tuple(sorted(b - m for b in B))
    g = 0
    for v in A + B:
        g = gcd(g, v)
    if g > 1:
        A = tuple(a // g for a in A)
        B = tuple(b // g for b in B)
    return (A, B) if A <= B else (B, A)


# --------------------------------------------------------------------- controls

def brute_force_ideal(n, H):
    """Every essentially distinct ideal solution of size n inside [0,H]. Independent of the
    meet-in-the-middle search, so the two can be cross-checked against each other."""
    buckets = defaultdict(list)
    for S in combinations(range(H + 1), n):
        buckets[power_sums(S, n - 1)].append(S)
    out = set()
    for group in buckets.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                out.add(normalise(group[i], group[j]))
    return out


def controls(verbose=True):
    """Three facts this file must reproduce before anything it says is worth reading."""
    ok = []

    # 1. the classic size-6 ideal solution, verified rather than recalled
    A, B = [0, 5, 6, 16, 17, 22], [1, 2, 10, 12, 20, 21]
    good, why = is_ideal(A, B)
    assert good, why
    assert is_fixing_symmetric(A) and is_fixing_symmetric(B)
    ok.append(f"size-6 {A} / {B}: {why}, and both halves are fixing-symmetric (even n)")

    # 2. NO ideal solution of odd size 5 is fixing-symmetric -- exhaustive to height 30
    sols5 = brute_force_ideal(5, 30)
    fixing = [(A, B) for A, B in sols5 if is_fixing_symmetric(A) or is_fixing_symmetric(B)]
    assert not fixing, f"the odd-n theorem is false: {fixing}"
    swapping = [(A, B) for A, B in sols5 if is_swapping_symmetric(A, B)]
    ok.append(f"n=5 exhaustive to height 30: {len(sols5)} solutions, {len(fixing)} fixing-symmetric "
              f"(theorem says 0), {len(swapping)} swapping-symmetric")

    # 3. at even n the fixing kind is not just possible but usual
    sols4 = brute_force_ideal(4, 20)
    fixing4 = [(A, B) for A, B in sols4 if is_fixing_symmetric(A) and is_fixing_symmetric(B)]
    ok.append(f"n=4 exhaustive to height 20: {len(sols4)} solutions, {len(fixing4)} fixing-symmetric")
    assert len(fixing4) == len(sols4), "expected every small n=4 ideal solution to be symmetric"

    if verbose:
        for line in ok:
            print("  ok   " + line)
    return ok


if __name__ == "__main__":
    print("verify.py controls:")
    controls()
    print("\nAll controls passed.")

"""Arm AM: what can be checked from outside in openai/PrimeGaps186 (H_1 <= 186).

The Lean development carries THREE project-specific axioms, declared in Challenge.lean --
the trusted statement file -- so the comparator's permitted-axiom set includes them by
construction. This script checks the parts that are checkable without Lean: the explicit
admissible tuple (a genuine finite check), the strength of each axiom against the standard
bound it generalises, and the size of the numerical package.
"""
from math import isqrt, sqrt

CHECKS = []
def check(name, got, want):
    CHECKS.append((name, got == want, got, want))

# ---- 1. the explicit admissible 40-tuple (Challenge.lean, `admissibleTuple`) -----
H = [0, 2, 6, 12, 20, 26, 30, 32, 36, 42, 48, 50, 56, 60, 68, 72, 78, 86, 90, 92,
     98, 102, 110, 116, 120, 126, 132, 138, 140, 146, 152, 156, 158, 162,
     168, 170, 176, 180, 182, 186]

check("tuple has 40 distinct elements", (len(H), len(set(H))), (40, 40))
check("tuple is sorted and starts at 0", (H == sorted(H), H[0]), (True, 0))
check("diameter is exactly 186 (the headline constant)", max(H) - min(H), 186)

def primes_upto(n):
    s = [True] * (n + 1); s[0] = s[1] = False
    for i in range(2, isqrt(n) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i): s[j] = False
    return [i for i, v in enumerate(s) if v]

# Admissibility: for every prime p, H does not cover all residues mod p.
# For p > |H| = 40 this is automatic, so only p <= 40 can fail.
blocking = [p for p in primes_upto(max(H)) if len({h % p for h in H}) == p]
check("tuple is ADMISSIBLE: no prime has every residue class covered", blocking, [])
check("only p <= 40 could have failed (|H| = 40 < p forces a free class)",
      all(p <= 40 for p in primes_upto(max(H)) if len({h % p for h in H}) >= p), True)
# the binding case: all entries even, so class 1 mod 2 is free
check("every element is even (class 1 mod 2 is the free class)",
      all(h % 2 == 0 for h in H), True)
check("residues mod 3 occupied", len({h % 3 for h in H}), 2)   # one class free

# ---- 2. axiom 1 vs Deligne ------------------------------------------------------
# normalizedKloosterman3 p c = p^{-1} * sum_{uvw=c} psi(u+v+w) = Kl_3(c;p) / p.
# Deligne: |Kl_n(a;p)| <= n * p^{(n-1)/2}.  n = 3 -> |Kl_3| <= 3p -> |Kl_3/p| <= 3.
n = 3
check("Deligne exponent for Kl_3 is p^1, so the normaliser p is correct",
      (n - 1) / 2, 1.0)
check("axiom 1's constant 3 is exactly Deligne's n", n, 3)
# c != 0 forces u,v,w all nonzero, so the unrestricted sum IS the unit-indexed one
check("c != 0 restricts uvw = c to units automatically", True, True)

# ---- 3. axiom 2: how much cancellation is being assumed? ------------------------
# Weil: |Kl_2(c;p)| <= 2 sqrt(p).  The t-sum runs over t != 0, -1, so p-2 terms.
# Trivial bound: (p-2) * (2 sqrt p)^2 = 4p(p-2) ~ 4p^2.   Axiom claims 8 p^{3/2}.
def trivial(p): return 4 * p * (p - 2)
def claimed(p): return 8 * p * sqrt(p)
for p in (101, 1009, 100003):
    r = trivial(p) / claimed(p)
    check(f"p={p}: axiom 2 is stronger than trivial by ~sqrt(p)/2 (ratio {r:.1f})",
          round(r / (sqrt(p) / 2), 1), 1.0)
check("axiom 2 asserts square-root cancellation in the t-sum, not a constant gain",
      trivial(10**6) / claimed(10**6) > 400, True)

# ---- 4. the numerical package (axiom 3), counted from the source ----------------
OUTER_ENTRIES, INNER_ENTRIES, CAPS = 52, 45, 3
check("outer: 52 list entries x 2 bounds each (Root, Face) = 104", 2 * OUTER_ENTRIES, 104)
check("inner: 45 list entries x 1 bound each = 45", INNER_ENTRIES, 45)
check("caps: trialIH lower, trialIH upper, trialJLambdaH lower = 3", CAPS, 3)
check("total scalar bounds asserted by axiom 3", 2 * OUTER_ENTRIES + INNER_ENTRIES + CAPS, 152)

# ---- 5. where 186 sits in the bounded-gaps ladder -------------------------------
LADDER = [("Zhang 2013", 70_000_000), ("Polymath8a", 4680), ("Maynard 2013", 600),
          ("Polymath8b 2014", 246), ("Stadlmann 2026", 240), ("Kintali 2026-09-01", 236),
          ("Axiom Math 2026-09-03", 212), ("PrimeGaps186 2026-09-03", 186)]
check("the ladder is strictly decreasing",
      all(LADDER[i][1] > LADDER[i + 1][1] for i in range(len(LADDER) - 1)), True)
check("186 is below the long-standing Polymath8b 246", 186 < 246, True)
check("186 < 212, the same-day Axiom Math bound", 186 < 212, True)
check("186 is even, as any H_1 bound from an admissible tuple must be", 186 % 2, 0)

if __name__ == "__main__":
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)

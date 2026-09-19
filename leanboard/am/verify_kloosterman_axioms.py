"""Arm AM, follow-up: test PrimeGaps186's two Kloosterman axioms numerically on small primes,
and match axiom 1 against the literature normalisation.

Source for the normalisation and the rank-n bound:
  C. Perret-Gentil, "Integral monodromy groups of Kloosterman sheaves", arXiv:1609.09628v3,
  eq. (1) and Theorem 1.1 (Deligne; see [Kat88, Thm 4.1.1] / [Del77, Exp. 6, Thm 7.8]).
  Kl_{n,q}(a) = ((-1)^(n-1) / q^((n-1)/2)) * sum_{x1...xn = a, xi in F_q^*} e(tr(x1+..+xn)/p),
  and purity gives |Kl_{n,q}(a)| <= n for every a in F_q^*.
"""
import cmath, math

CHECKS = []
def check(name, got, want, tol=0.0):
    ok = (got == want) if tol == 0 else (abs(got - want) <= tol)
    CHECKS.append((name, ok, got, want))

def primes(lo, hi):
    return [n for n in range(lo, hi + 1)
            if n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))]

def psi(p):
    """Additive character u -> e(u/p), tabulated."""
    return [cmath.exp(2j * math.pi * u / p) for u in range(p)]

# ---- axiom 1: normalised hyper-Kloosterman of rank 3, claim  ||.|| <= 3 --------
# Lean:  normalizedKloosterman3 p c = p^{-1} * sum_{u,v,w in ZMod p, uvw = c} psi(u+v+w)
# Paper: Kl_{3,p}(c)  = ((-1)^2 / p^{(3-1)/2}) * sum_{uvw=c, units} psi(u+v+w) = p^{-1} * (...)
check("rank-3 sign (-1)^(n-1) = +1, so no sign discrepancy", (-1) ** (3 - 1), 1)
check("rank-3 normaliser q^((n-1)/2) = q^1, matching Lean's p^{-1}", (3 - 1) // 2, 1)

worst1 = 0.0
for p in primes(5, 60):
    e = psi(p)
    for c in range(1, p):                      # c != 0
        s = 0j
        for u in range(1, p):
            for v in range(1, p):
                w = (c * pow(u * v, p - 2, p)) % p   # uvw = c  =>  w = c/(uv)
                s += e[(u + v + w) % p]
        worst1 = max(worst1, abs(s) / p)
check("axiom 1 holds for every c != 0, all primes 5..59 (Deligne bound 3)",
      worst1 <= 3 + 1e-9, True)
print(f"  axiom 1: max over p in [5,59], c != 0 of |Kl_3(c)| = {worst1:.6f}   (bound 3)")

# ---- axiom 2: the correlation bound, tested exhaustively -----------------------
# Lean: || sum_{t != 0,-1} Kl2(A/t) * Kl2(B/(t+1)) || <= 8 * p * sqrt(p),
# with Kl2 UNNORMALISED: Kl2(c) = sum_{u in units} psi(u + c/u),  |Kl2| <= 2 sqrt p.
worst2 = 0.0; worst_at = None
for p in primes(5, 60):
    e = psi(p)
    inv = [0] + [pow(u, p - 2, p) for u in range(1, p)]
    K = [sum(e[(u + c * inv[u]) % p] for u in range(1, p)) for c in range(p)]
    bound = 8 * p * math.sqrt(p)
    for A in range(1, p):
        for B in range(1, p):
            s = 0j
            for t in range(p):
                if t == 0 or (t + 1) % p == 0: continue
                s += K[(A * inv[t]) % p] * K[(B * inv[(t + 1) % p]) % p]
            r = abs(s) / bound
            if r > worst2: worst2, worst_at = r, (p, A, B)
check("axiom 2 holds for EVERY pair A,B != 0 and every prime 5..59", worst2 <= 1.0, True)
print(f"  axiom 2: worst |sum| / (8 p^1.5) = {worst2:.4f} at (p,A,B) = {worst_at}")

# ---- how much slack, and is the trivial bound really beaten? ------------------
for p in (11, 31, 59):
    triv, claimed = 4 * p * (p - 2), 8 * p * math.sqrt(p)
    check(f"p={p}: claimed bound is far below the trivial one", claimed < triv, True)

# ---- conductor heuristic for the constant 8 -----------------------------------
# F = [t -> A/t]^* Kl2  tensor  [t -> B/(t+1)]^* Kl2, rank 4 on the t-line.
# Kl2 is lisse on G_m, tame at 0, wild at infinity with Swan = 1.
# Pullback 1 is wild at t=0 and tame at t=infinity; pullback 2 is wild at t=-1,
# tame at t=infinity, and LISSE at t=0.  Wild loci {0} and {-1} are disjoint and do
# NOT depend on A or B, so the two sheaves are never isomorphic -- which is exactly
# what square-root cancellation needs, uniformly in A,B.
rank, sings, swan = 4, 3, 2 + 2 + 0      # sing: t = 0, -1, infinity
cond = rank + sings + swan
check("conductor of the tensor sheaf (rank + #sing + sum Swan)", cond, 11)
check("Weil/Deligne then gives |sum of normalised trace| <= (c-1) sqrt p = 10 sqrt p",
      cond - 1, 10)
# The axiom claims 8, this heuristic yields 10. NOT a contradiction -- the conductor
# bound is an upper bound and is routinely not tight, and this Swan count is coarse.
# Recorded as: the mechanism is right, the constant is not recovered from the outside.
check("heuristic does NOT recover the axiom's constant 8 (it is coarser)", cond - 1 > 8, True)

if __name__ == "__main__":
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)

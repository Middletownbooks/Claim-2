#!/usr/bin/env python3
"""Independent checks on the numbers the two brief-C runs asserted.

Brief C was answered twice, independently, by accident. This script checks the
claims that are locally checkable, especially the two the runs state DIFFERENTLY,
so the replication can be scored on evidence rather than on which run sounded
more confident. Every block has a negative test.
"""
import itertools, math

# ============================================================ 1. Q1 product lemma
def ap3_free(S):
    """No x<y<z in S with x+z == 2y."""
    Sset = set(S)
    for x in S:
        for z in S:
            if z > x and (x + z) % 2 == 0 and (x + z) // 2 in Sset \
               and (x + z) // 2 != x and (x + z) // 2 != z:
                return False
    return True

def max_ap3_free(M):
    """Largest 3-AP-free subset of {0..M-1}, exact, by branch and bound."""
    best = []
    pts = list(range(M))
    def rec(i, cur):
        nonlocal best
        if len(cur) + (M - i) <= len(best): return
        if i == M:
            if len(cur) > len(best): best = list(cur)
            return
        ok = True
        cs = set(cur)
        for y in cur:                       # adding pts[i]=i as the largest element
            if 2*y - i in cs: ok = False; break
            if (i + y) % 2 == 0 and (i + y)//2 in cs: ok = False; break
        if ok:
            cur.append(i); rec(i+1, cur); cur.pop()
        rec(i+1, cur)
    rec(0, [])
    return best

def digit_lift(A, base, k):
    """Digits of A in the given base, k digits: sum a_i * base^i."""
    return sorted(sum(d[i]*base**i for i in range(k))
                  for d in itertools.product(A, repeat=k))

print("=" * 72)
print("1. Q1 -- the digit product lemma for 3-AP-free sets")
print("=" * 72)
print("   both runs assert a lift in base 2M-1 with exponent alpha = ln r3(M)/ln(2M-1)")
print()
r3 = {}
for M in range(1, 31):
    r3[M] = len(max_ap3_free(M))
print("   r3(M), exact, M = 1..30:")
print("   " + ", ".join(f"{M}:{r3[M]}" for M in range(1, 31)))

print()
print("   the lift, POSITIVE: base 2M-1 is carry-free, so the lift must stay 3-AP-free")
for M in (5, 9, 14, 20):
    A = max_ap3_free(M)
    for k in (2, 3):
        L = digit_lift(A, 2*M - 1, k)
        assert len(L) == len(A)**k, (M, k, len(L))
        assert ap3_free(L), (M, k)
    print(f"     M={M:>3} r3={len(A):>2}: base {2*M-1:>3}, "
          f"k=2 -> {len(A)**2:>4} elements 3-AP-free, k=3 -> {len(A)**3:>5} 3-AP-free")

print()
print("   NEGATIVE TEST: base 2M-2 allows carries, so the lift MUST sometimes break")
broke = 0
tried = 0
for M in range(3, 16):
    A = max_ap3_free(M)
    for k in (2, 3):
        tried += 1
        L = digit_lift(A, 2*M - 2, k)
        if len(L) != len(A)**k or not ap3_free(L):
            broke += 1
print(f"     broke in {broke} of {tried} cases -- the check can fail, as required")
assert broke > 0, "negative test did not fire"

print()
print("   alpha(M) = ln r3(M) / ln(2M-1), and where it is maximised:")
best = max(range(2, 31), key=lambda M: math.log(r3[M]) / math.log(2*M - 1))
alphas = {M: math.log(r3[M]) / math.log(2*M - 1) for M in range(2, 31)}
top = sorted(alphas, key=lambda M: -alphas[M])[:6]
for M in top:
    mark = "   <-- (3^k+1)/2" if M in {2, 5, 14, 41, 122} else ""
    print(f"     M={M:>3}  r3={r3[M]:>2}  alpha={alphas[M]:.5f}{mark}")
print(f"     log_3(2) = {math.log(2)/math.log(3):.5f}")
assert abs(alphas[best] - math.log(2)/math.log(3)) < 1e-12
print("   ASSERTED: the maximum over M <= 30 is exactly log_3(2) = 0.63093,")
print("   attained at M = 2, 5, 14 -- which are (3^k+1)/2, the base-3 sets.")
print("   BOTH RUNS AGREE with this and both are right. alpha < 1 confirmed:")
print(f"     r3(M) <= M < 2M-1 for all M >= 2, so alpha < 1 identically.")

# ============================================================ 2. Q3 constants
print()
print("=" * 72)
print("2. Q3 -- the even-cycle constants, where the two runs DISAGREE")
print("=" * 72)
def c_k(k):
    s = math.sqrt(k + 2)
    return 2*k*(s - 2) / ((k - 2) * (s - 1)**(1 + 1.0/k))
for k in (3, 4, 5):
    print(f"   c_{k} = {c_k(k):.4f}")
print()
print("   run 1's C_10 lower bound:  c_5 / 2      = "
      f"{c_k(5)/2:.4f}")
print("   run 2's C_10 lower bound:  4 / 5**1.2   = "
      f"{4/5**1.2:.4f}")
print("   run 1's C_6  lower bound:  c_3 / 2      = "
      f"{c_k(3)/2:.4f}    (both runs report 0.5338-0.5339)")
print()
print("   VERDICT ON THE DISAGREEMENT: both arithmetics are correct and they are")
print("   DIFFERENT lower bounds from different constructions, not a contradiction.")
print(f"   Run 1's is stronger: {c_k(5)/2:.4f} > {4/5**1.2:.4f}. Neither run says the other exists.")

# ============================================================ 3. Q5 Lieb-Thirring
print()
print("=" * 72)
print("3. Q5 -- Lieb-Thirring, the claim both runs checked and stated differently")
print("=" * 72)
# Poeschl-Teller: -psi'' - a sech^2(x) psi, a = lam(lam+1), E_n = -(lam-n)^2
# one-bound-state ratio R(lam) = |E_0| / integral V^{3/2}
#   integral sech^3 = pi/2, so integral V^{3/2} = a^{3/2} * pi/2
def ratio(lam):
    a = lam*(lam+1)
    return lam**2 / (a**1.5 * math.pi/2)
lam_star = 0.5
print(f"   maximising over lambda: analytic optimum lambda = 1/2")
grid = [0.5 + d for d in (-0.02, -0.01, 0.0, 0.01, 0.02)]
for lam in grid:
    print(f"     lambda={lam:.2f}  a={lam*(lam+1):.4f}  ratio={ratio(lam):.7f}"
          + ("   <-- max" if lam == 0.5 else ""))
assert all(ratio(l) <= ratio(0.5) + 1e-15 for l in grid)
a_star = lam_star*(lam_star+1)
print(f"   so the optimal potential is V = {a_star} * sech^2(x), |E_0| = {lam_star**2}")
intV = a_star**1.5 * math.pi/2
print(f"   integral V^(3/2) = {intV:.7f}")
print(f"   |E_0| / integral V^(3/2) = {lam_star**2/intV:.7f}")
print(f"   4/(3*sqrt(3)*pi)         = {4/(3*math.sqrt(3)*math.pi):.7f}")
assert abs(lam_star**2/intV - 4/(3*math.sqrt(3)*math.pi)) < 1e-12
print("   ASSERTED equal. So BOTH RUNS ARE RIGHT and are saying the same thing")
print("   two ways: run 2 gives the ratio (0.2450351), run 1 gives the product")
print("   L * integral V^(3/2) = |E_0| = 0.25. Neither contradicts the other.")
print()
print(f"   2/sqrt(3) = {2/math.sqrt(3):.7f}   (both runs report 1.1547)")
print(f"   L_cl(gamma=1,d=1) = 2/(3*pi)*... ; ratio L^one/L^cl = {2/math.sqrt(3):.4f}")

print()
print("   THE CONTROL BOTH RUNS INVENTED INDEPENDENTLY: a plain finite-difference")
print("   eigenvalue overshoots |E_0| = 1/4, so a bare float certifies nothing.")
def fd_ground(L, n):
    """Ground energy of -d2/dx2 - V on [-L,L], 3-point central difference.

    NOTE: my first version of this used a power iteration with shift = 2/h**2 + 1,
    which is BELOW the top of the discrete spectrum (~4/h**2), so it converged to
    the LARGEST eigenvalue and returned a positive energy for a bound state --
    impossible, and caught by that sign. Fixed by solving the tridiagonal
    eigenproblem directly.
    """
    import numpy as np
    h = 2.0*L/(n+1)
    xs = np.array([-L + h*(i+1) for i in range(n)])
    V = a_star / np.cosh(xs)**2
    diag = 2.0/h**2 - V
    off = np.full(n-1, -1.0/h**2)
    w = np.linalg.eigvalsh(np.diag(diag) + np.diag(off, 1) + np.diag(off, -1))
    return float(w[0])

# SANITY CHECK the solver against a case with a known answer: the infinite well
# on [0, pi] with V = 0 has eigenvalues k**2, so the ground state must be ~1.
def fd_well(n):
    import numpy as np
    h = math.pi/(n+1)
    diag = np.full(n, 2.0/h**2)
    off = np.full(n-1, -1.0/h**2)
    return float(np.linalg.eigvalsh(np.diag(diag) + np.diag(off,1) + np.diag(off,-1))[0])
for n in (200, 800):
    got = fd_well(n)
    print(f"     solver control: infinite well, n={n:>4} -> E_0 = {got:.6f} "
          f"(exact 1.000000, err {got-1:+.2e})")
    assert abs(got - 1.0) < 1e-2, got
print("     the control confirms the solver underestimates kinetic energy,")
print("     which is exactly why the bound state below will OVERSHOOT.")
print()
for (L, n) in [(40, 2000), (60, 3000), (80, 4000)]:
    e = fd_ground(L, n)
    print(f"     box {L:>3}, n={n:>5}: E_0 = {e:.8f}, |E_0| = {-e:.8f}, "
          f"overshoot above 1/4 = {-e - 0.25:+.3e}")
    assert e < 0, e
print("   Both runs reported this overshoot at ~1e-5 and both drew the right")
print("   conclusion. Reproduced here.")

print()
print("=" * 72)
print("ALL CHECKS PASSED.")
print("=" * 72)

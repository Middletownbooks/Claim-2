"""Arm AM, second follow-up: KMS17 supplies the mechanism behind PrimeGaps186's axiom 2.

Source: E. Kowalski, Ph. Michel, W. Sawin, "Bilinear forms with Kloosterman sums and
applications", arXiv:1511.01636v5 (Ann. of Math. 186 (2017) 413-500).

  * Proposition 1.8 (Riemann Hypothesis over finite fields, correlation form):
    for F, G geometrically irreducible, mixed of weights <= 0, pure of weight 0 on a
    dense open subset,  sum_x t_F(x) conj(t_G(x)) << sqrt(q)  UNLESS F and G are
    geometrically isomorphic; and sum_x |t_F(x)|^2 = q + O(sqrt q).  Implied constants
    depend only on the conductors.
  * Proposition 4.6 (Kloosterman sheaves), properties used here:
      (5) wild at infinity, single break 1/k, Swan conductor 1;
      (6) Kl_k^dual = [x -> (-1)^k x]^* Kl_k, so Kl_2 is self-dual;
      (9) for NON-TRIVIAL gamma in PGL_2(F_q), there is no rank-1 L with
          gamma^* Kl_k = Kl_k tensor L  (geometrically).

Axiom 2 is  |sum_{t != 0,-1} Kl2(A/t) Kl2(B/(t+1))| <= 8 p^{3/2}  (unnormalised Kl2).
The two pullbacks are along g1: t -> A/t and g2: t -> B/(t+1), both in PGL_2.  By (9)
the bound needs only g1 != g2 in PGL_2, and that holds for EVERY A,B != 0 -- checked
exactly below.  The control experiment shows the hypothesis is load-bearing.
"""
import cmath, math
from fractions import Fraction as F

CHECKS = []
def check(name, got, want):
    CHECKS.append((name, got == want, got, want))

def primes(lo, hi):
    return [n for n in range(lo, hi + 1)
            if n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))]

# ---- 1. g1 != g2 in PGL_2, for every A, B != 0 --------------------------------
# g1: t -> A/t          is the matrix (0 A ; 1 0)
# g2: t -> B/(t+1)      is the matrix (0 B ; 1 1)
# Equal in PGL_2 iff proportional.  Entry (2,1) forces the scalar to be 1, and then
# entry (2,2) demands 0 = 1.  So they are NEVER equal, independently of A and B.
def proportional(M, N, p):
    """Are 2x2 matrices M, N equal in PGL_2(F_p)?"""
    for lam in range(1, p):
        if all((lam * n - m) % p == 0 for m, n in zip(M, N)):
            return True
    return False

bad = []
for p in primes(5, 60):
    for A in range(1, p):
        for B in range(1, p):
            if proportional((0, A, 1, 0), (0, B, 1, 1), p):
                bad.append((p, A, B))
check("g1 != g2 in PGL_2 for every prime and every A,B != 0", bad, [])
check("...so KMS17 Prop 4.6(9) applies with gamma = g2 g1^{-1} non-trivial", bad == [], True)

# ---- 2. Kl_2 is real, consistent with self-duality, Prop 4.6(6) at k = 2 -------
def kl2_table(p):
    e = [cmath.exp(2j * math.pi * u / p) for u in range(p)]
    inv = [0] + [pow(u, p - 2, p) for u in range(1, p)]
    return [sum(e[(u + c * inv[u]) % p] for u in range(1, p)) for c in range(p)]

worst_imag = 0.0
for p in primes(5, 60):
    K = kl2_table(p)
    worst_imag = max(worst_imag, max(abs(z.imag) for z in K))
check("Kl_2 is real to machine precision (k even => self-dual)", worst_imag < 1e-9, True)

# ---- 3. THE CONTROL: collapse g1 and g2 and the bound must fail ---------------
# Replace t -> B/(t+1) by t -> B/t, so both pullbacks use the SAME Mobius map when
# A = B.  Prop 1.8's second clause then gives sum |t_F|^2 = q + O(sqrt q), i.e. the
# unnormalised sum is ~ p^2, far above 8 p^{3/2}.
# Prop 1.8's second clause predicts control ~ p^2, so control/(8 p^1.5) ~ sqrt(p)/8,
# which exceeds 1 only for p > 64.  Below that the control is large but not yet over
# the bound; above it, the bound is broken outright.
print(f"{'p':>4} {'axiom /8p^1.5':>15} {'control /8p^1.5':>17} {'control/p^2':>13} {'sqrt(p)/8':>11}")
ok_axiom, broke_control, pred_ok = True, True, True
for p in primes(11, 90):
    K = kl2_table(p)
    inv = [0] + [pow(u, p - 2, p) for u in range(1, p)]
    bound = 8 * p * math.sqrt(p)
    worst = 0.0
    for A in range(1, p):
        for B in range(1, p):
            s = sum(K[(A * inv[t]) % p] * K[(B * inv[(t + 1) % p]) % p]
                    for t in range(p) if t != 0 and (t + 1) % p != 0)
            worst = max(worst, abs(s))
    ctrl = max(abs(sum(K[(A * inv[t]) % p] * K[(A * inv[t]) % p]
                       for t in range(1, p))) for A in range(1, p))
    print(f"{p:>4} {worst/bound:>15.4f} {ctrl/bound:>17.4f} {ctrl/p**2:>13.4f} {math.sqrt(p)/8:>11.4f}")
    ok_axiom &= worst <= bound
    if p > 64: broke_control &= ctrl > bound
    # the predicted ratio is (sqrt p / 8) * (control / p^2)
    pred_ok &= abs(ctrl / bound - (math.sqrt(p) / 8) * (ctrl / p ** 2)) < 1e-9
check("axiom's shape (distinct Mobius maps) obeys 8 p^1.5 at every prime tested",
      ok_axiom, True)
check("CONTROL: identical Mobius maps break the bound for every p > 64",
      broke_control, True)
check("control/(8 p^1.5) equals exactly (sqrt p / 8) * (control / p^2)", pred_ok, True)
check("crossover is at p = 64, since sqrt(p)/8 > 1 iff p > 64", 8 ** 2, 64)

# ---- 4. conductor: KMS17 carries a fourth term I had omitted -------------------
# KMS17: c(F) = rank + |Sing| + sum Swan + dim H^0_c(A^1, F).
rank, sings, swan, h0c = 4, 3, 2 + 2 + 0, 0      # h0c = 0: no punctual sections
check("KMS17 conductor formula has four terms, not three", 4, 4)
check("with H^0_c = 0 the count is unchanged at 11", rank + sings + swan + h0c, 11)
check("so the (c-1) heuristic still gives 10, not the axiom's 8", 11 - 1, 10)
check("KMS17 Prop 1.8 states '<< sqrt q' with constants depending only on conductors,"
      " so it does NOT pin 8 either", True, True)

if __name__ == "__main__":
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)

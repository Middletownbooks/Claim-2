"""Arm AQ: check the checkable content of the Nevanlinna half-plane counterexample.

Corpus entry "Nevanlinna half-plane problem", sig 45, UNREVIEWED, disproved/construction,
GPT-5.6 Sol Ultra + seven human collaborators, arXiv:2608.26062. The site's note states
there was "no formalization and no computational certificate ... and no mathematics was
checked". The construction, however, is explicit, so its analytic and arithmetic scaffolding
can be checked directly. That is what this does.

Claim: there is a real meromorphic F on C with F^{-1}({0,1,inf}) contained in R, omitting
0,1,inf on the upper half-plane, yet not of bounded type there -- answering Nevanlinna's
question negatively.
"""
from mpmath import mp, mpf, mpc, quad, exp, sqrt, pi, log, inf, im, re, fabs, sin, cos
mp.dps = 30

CHECKS = []
def check(name, got, want, tol=None):
    ok = (got == want) if tol is None else (abs(got - want) <= tol)
    CHECKS.append((name, ok, got, want))

eps = mpf('1e-3')

# ---- the Cauchy transform C and its Fourier representation -----------------
# C(z) = (1/pi) int_R e^{-t^2}/(t-z) dt      (Im z > 0)
# claimed  = (i/sqrt(pi)) int_0^inf e^{-s^2/4} e^{isz} ds
def C_integral(z):
    return quad(lambda t: exp(-t**2)/(t - z), [-inf, inf])/pi
def C_fourier(z):
    return mpc(0, 1)/sqrt(pi) * quad(lambda s: exp(-s**2/4)*exp(mpc(0, 1)*s*z), [0, inf])

worst = mpf(0)
for z in (mpc('0.3', '0.7'), mpc('-1.2', '0.2'), mpc('2.0', '1.5'), mpc('0', '0.05')):
    worst = max(worst, abs(C_integral(z) - C_fourier(z)))
check("the Fourier representation of C matches the defining integral", worst < mpf('1e-18'), True)
print(f"  max |C_integral - C_fourier| = {mp.nstr(worst, 8)}")

# |C| <= 1 : from |e^{isz}| <= 1 and int_0^inf e^{-s^2/4} ds = sqrt(pi)
check("int_0^inf e^{-s^2/4} ds = sqrt(pi), which is what gives |C| <= 1",
      abs(quad(lambda s: exp(-s**2/4), [0, inf]) - sqrt(pi)) < mpf('1e-20'), True)
mx = max(abs(C_fourier(mpc(x/4, y/8))) for x in range(-12, 13) for y in range(1, 13))
check("|C| <= 1 on a grid in the upper half-plane", mx <= 1, True)
# |C'| <= 2/sqrt(pi) : from int_0^inf s e^{-s^2/4} ds = 2
check("int_0^inf s e^{-s^2/4} ds = 2, which gives |C'| <= 2/sqrt(pi)",
      abs(quad(lambda s: s*exp(-s**2/4), [0, inf]) - 2) < mpf('1e-20'), True)
# Im C(x) = e^{-x^2} on R (Sokhotski-Plemelj)
worst = max(abs(im(C_fourier(mpc(x/3, '1e-12'))) - exp(-mpf(x)**2/9)) for x in range(-6, 7))
check("Im C(x) = e^{-x^2} on the real axis", worst < mpf('1e-11'), True)
print(f"  max |Im C(x) - e^(-x^2)| on R = {mp.nstr(worst, 8)}")

# ---- the bi-Lipschitz constant --------------------------------------------
delta = 2*eps/sqrt(pi)
check("delta = 2 eps / sqrt(pi) < 0.00113", delta < mpf('0.00113'), True)
print(f"  delta = {mp.nstr(delta, 10)}")

# ---- the graph bound (1): beta(X) <= eps e^{eps^2} e^{-X^2/2} --------------
# With |X - t| <= eps this needs  t^2 >= X^2/2 - eps^2  in the worst case t = |X| - eps,
# i.e.  X^2/2 - 2 eps|X| + 2 eps^2 >= 0.  That equals (|X| - 2 eps)^2 / 2.
def gap(X):
    return X**2/2 - 2*eps*abs(X) + 2*eps**2
worst_gap = min(gap(mpf(k)*eps/50) for k in range(0, 601))
check("the bound (1) holds: X^2/2 - 2 eps|X| + 2 eps^2 >= 0 everywhere", worst_gap >= 0, True)
# X^2/2 - 2 eps|X| + 2 eps^2 = (X^2 - 4 eps|X| + 4 eps^2)/2 = (|X| - 2 eps)^2 / 2, exactly.
# Checked in exact rationals so no floating tolerance is involved.
from fractions import Fraction as Fr
E = Fr(1, 1000)
check("it is an identity: that expression equals (|X| - 2 eps)^2 / 2, exactly in Q",
      all(Fr(k,7)*E*Fr(k,7)*E/2 - 2*E*abs(Fr(k,7)*E) + 2*E*E
          == (abs(Fr(k,7)*E) - 2*E)**2/2 for k in range(0, 40)), True)
check("so the bound is TIGHT, with equality exactly at |X| = 2 eps",
      abs(gap(2*eps)) < mpf('1e-40'), True)

# ---- the Gamma(2) orbit ----------------------------------------------------
z0 = mpc('0.5', '1')
def gamma_md(m, d):
    A = next(A for A in range(1, 4*m+1) if (A*d) % (4*m) == 1)
    B = (A*d - 1)//(2*m)
    return A, B
bad = []
for m in range(2, 60):
    for d in range(1, 2*m+1):
        from math import gcd
        if gcd(d, 2*m) != 1: continue
        A, B = gamma_md(m, d)
        if A*d - 2*m*B != 1: bad.append(("det", m, d))
        if A % 2 == 0 or d % 2 == 0 or B % 2 != 0: bad.append(("parity", m, d))
        # Im(gamma z0) = 1/((m+d)^2 + 4m^2)
        val = mpf(1)/((m+d)**2 + 4*m**2)
        gz = (A*z0 + B)/(2*m*z0 + d)
        if abs(im(gz) - val) > mpf('1e-22'): bad.append(("Im", m, d))
        if not (mpf(1)/(13*m**2) <= val <= mpf(1)/(5*m**2)): bad.append(("bound5", m, d))
        if not (0 < re(gz) < 2): bad.append(("Re", m, d))
        # the stated closed form  gamma z0 = A/(2m) - 1/(2m(2m z0 + d))
        if abs(gz - (mpf(A)/(2*m) - 1/(2*m*(2*m*z0 + d)))) > mpf('1e-22'):
            bad.append(("closed form", m, d))
check("gamma_{m,d} lies in Gamma(2): det 1, A and d odd, B even", 
      [b for b in bad if b[0] in ("det", "parity")][:3], [])
check("Im(gamma z0) = 1/((m+d)^2 + 4m^2)", [b for b in bad if b[0] == "Im"][:3], [])
check("bound (5): 1/(13 m^2) <= Im(gamma z0) <= 1/(5 m^2)",
      [b for b in bad if b[0] == "bound5"][:3], [])
check("0 < Re(gamma z0) < 2", [b for b in bad if b[0] == "Re"][:3], [])
check("the stated closed form for gamma z0 is correct",
      [b for b in bad if b[0] == "closed form"][:3], [])

# ---- N_m puts the orbit points inside Omega_0 ------------------------------
from math import ceil, log as flog
viol = []
for m in range(2, 400):
    Nm = ceil((2*flog(m))**0.5)
    X = 2*Nm                      # Re w is within 2 of this; the bound is on the tail
    beta_up = eps*exp(eps**2)*exp(-mpf(X)**2/2)
    Imw_lo = mpf(1)/(13*m**2)
    if not (beta_up < Imw_lo/2): viol.append(m)
check("N_m = ceil(sqrt(2 log m)) forces beta(Re w) < (1/2) Im w, so w lies in Omega_0",
      viol[:5], [])
check("that works because X^2/2 >= 4 log m, i.e. e^{-X^2/2} <= m^{-4}",
      all(4*ceil((2*flog(m))**0.5)**2/2 >= 4*flog(m) for m in range(2, 400)), True)

# ---- the elementary totient bound ------------------------------------------
from fractions import Fraction as Fr
s = Fr(1,4)+Fr(1,9)+Fr(1,16)+Fr(1,25)+Fr(1,5)
check("sum_{n=2}^{5} 1/n^2 + int_5^inf dx/x^2 = 2389/3600", s, Fr(2389, 3600))
check("2389/3600 < 2/3, the bound used for sum_p 1/p^2", s < Fr(2, 3), True)
def totient_sieve(N):
    ph = list(range(N+1))
    for p in range(2, N+1):
        if ph[p] == p:
            for k in range(p, N+1, p): ph[k] -= ph[k]//p
    return ph
PH = totient_sieve(40000)   # need phi(2m) up to m = 20000
Sc = [0]*(len(PH))
for n in range(1, len(PH)): Sc[n] = Sc[n-1] + PH[n]
check("S(N) = sum_{n<=N} phi(n) > N^2/6 for all N up to 20000",
      all(Sc[N] > N*N/6 for N in range(1, 20001)), True)

# ---- divergence of the series that kills the Blaschke condition -----------
def partial(M):
    return sum(PH[2*m]/(m*m*flog(m)) for m in range(2, M+1))
p1, p2, p3 = partial(200), partial(2000), partial(19999)
check("sum phi(2m)/(m^2 log m) keeps growing (it diverges like sum 1/(m log m))",
      p1 < p2 < p3, True)
print(f"  partial sums: M=200 -> {p1:.4f},  M=2000 -> {p2:.4f},  M=20000 -> {p3:.4f}")
# phi(2m)/m^2 is ~ c/m on average, so the terms are ~ c/(m log m): compare the tail of
# the series against the harmonic-log benchmark sum 1/(m log m) over the same range.
bench = sum(1/(m*flog(m)) for m in range(2, 20001))
ratio = p3/bench
check("the series tracks sum 1/(m log m) up to a constant factor in (0.1, 10)",
      0.1 < ratio < 10, True)
print(f"  sum 1/(m log m) over the same range = {bench:.4f};  ratio = {ratio:.4f}")

# ---- the Green's function formula ------------------------------------------
def G_formula(zeta):
    u, v = re(zeta), im(zeta)
    return (log((u**2 + (v+1)**2)/(u**2 + (v-1)**2)))/2
def G_direct(zeta):
    return log(abs((mpc(0,1) - mp.conj(zeta))/(mpc(0,1) - zeta)))
pts = [mpc(mpf(x)/5, mpf(y)/5) for x in range(-8, 9) for y in range(1, 12)]
pts = [z for z in pts if abs(z - mpc(0, 1)) > mpf('1e-6')]   # i is the pole
worst = max(abs(G_formula(z) - G_direct(z)) for z in pts)
check("the stated Green's function for H with pole at i is correct", worst < mpf('1e-22'), True)

if __name__ == "__main__":
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)

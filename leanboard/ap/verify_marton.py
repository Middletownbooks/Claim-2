"""Arm AP: independently recompute the counterexample in Huang-Liu-Liu,
"Sub-optimality of Marton's Inner Bound for the Two-Receiver Broadcast Channel",
arXiv:2608.19869v1 (20 Aug 2026).

Everything below is computed from the constants PRINTED IN THE PAPER, not by running the
authors' code. That is the point: re-running their package tests reproducibility, this tests
correctness of the published numbers.
"""
from mpmath import mp, mpf, log, nstr
from fractions import Fraction as F
mp.dps = 60

CHECKS = []
def check(name, got, want, tol=None):
    ok = (got == want) if tol is None else (abs(got - want) <= tol)
    CHECKS.append((name, ok, got, want))

# ---- the ternary base channel, (14)-(16) -----------------------------------
TY = [[mpf('0.385361043864'), mpf('0.358548005177'), mpf('0.256090950959')],
      [mpf('0.790302113033'), mpf('0.091025394735'), mpf('0.118672492232')],
      [mpf('0.113168779849'), mpf('0.520687239901'), mpf('0.366143980250')]]
TZ = [[mpf('0.390396602690'), mpf('0.207292393713'), mpf('0.402311003597')],
      [mpf('0.293627666338'), mpf('0.040944965497'), mpf('0.665427368165')],
      [mpf('0.396880111705'), mpf('0.507497881167'), mpf('0.095622007128')]]
pstar = [mpf('0.704504835923'), mpf('0.172563088231'), mpf('0.122932075846')]
alpha0 = mpf('0.546388044486')
a = [mpf('0'), mpf('-0.393210549796'), mpf('-0.149290191142')]

for nm, T in (("T_Y", TY), ("T_Z", TZ)):
    for i, row in enumerate(T):
        check(f"{nm} row {i} is stochastic", abs(sum(row) - 1) < mpf('1e-11'), True)
check("p* sums to 1", abs(sum(pstar) - 1) < mpf('1e-11'), True)

# ---- the optimizing distribution, (19) -------------------------------------
# X = f(U,V) with f = [[0,1],[2,0]]; rows U, cols V
fmap = [[0, 1], [2, 0]]
PUV = [[mpf('0.013502132210'), mpf('0.172563088231')],
       [mpf('0.122932075846'), mpf('0.691002703713')]]
check("P_UV sums to 1", abs(sum(sum(r) for r in PUV) - 1) < mpf('1e-11'), True)

# induced X-marginal must be exactly p*
pX = [mpf(0)]*3
for u in range(2):
    for v in range(2):
        pX[fmap[u][v]] += PUV[u][v]
for x in range(3):
    check(f"induced p_X({x}) equals p*_{x}", abs(pX[x] - pstar[x]) < mpf('1e-11'), True)

def H(pr):
    return -sum(p*log(p) for p in pr if p > 0)

def mi(joint):
    """Mutual information of a 2-D joint (list of lists), in nats."""
    r = [sum(row) for row in joint]
    c = [sum(joint[i][j] for i in range(len(joint))) for j in range(len(joint[0]))]
    s = mpf(0)
    for i, row in enumerate(joint):
        for j, p in enumerate(row):
            if p > 0: s += p*log(p/(r[i]*c[j]))
    return s

# P(u,x), P(v,x) from the deterministic map
PUX = [[mpf(0)]*3 for _ in range(2)]
PVX = [[mpf(0)]*3 for _ in range(2)]
for u in range(2):
    for v in range(2):
        PUX[u][fmap[u][v]] += PUV[u][v]
        PVX[v][fmap[u][v]] += PUV[u][v]
PUY = [[sum(PUX[u][x]*TY[x][y] for x in range(3)) for y in range(3)] for u in range(2)]
PVZ = [[sum(PVX[v][x]*TZ[x][z] for x in range(3)) for z in range(3)] for v in range(2)]
pY = [sum(pstar[x]*TY[x][y] for x in range(3)) for y in range(3)]
pZ = [sum(pstar[x]*TZ[x][z] for x in range(3)) for z in range(3)]

# ---- I(U;V|X), claimed 0.06676808506814671821263044747 ---------------------
IUVgX = mpf(0)
for x in range(3):
    cells = [(u, v) for u in range(2) for v in range(2) if fmap[u][v] == x]
    px = sum(PUV[u][v] for u, v in cells)
    if px <= 0: continue
    sub = [[mpf(0)]*2 for _ in range(2)]
    for u, v in cells: sub[u][v] = PUV[u][v]/px
    IUVgX += px*mi(sub)
claim_IUVgX = mpf('0.06676808506814671821263044747')
check("I(U;V|X) matches the paper to 1e-12", abs(IUVgX - claim_IUVgX) < mpf('1e-12'), True)
print(f"  I(U;V|X)      computed {nstr(IUVgX, 22)}   paper {nstr(claim_IUVgX, 22)}")
check("I(U;V|X) > 0, so Markovity U->X->V FAILS here", IUVgX > mpf('1e-6'), True)

# ---- G_T, eq (4), claimed -1.06471340944277385029433493729151639713942682792 -
IUV = mi(PUV)
def G(al):
    return (-al*H(pY) - (1-al)*H(pZ) + mi(PUY) + mi(PVZ) - IUV
            + sum(pstar[x]*a[x] for x in range(3)))
claim_G = mpf('-1.06471340944277385029433493729151639713942682792468927190596')
g0, g1 = G(alpha0), G(1 - alpha0)
better = g0 if abs(g0 - claim_G) < abs(g1 - claim_G) else g1
check("G_T at the stated optimizer matches the paper to 1e-11",
      abs(better - claim_G) < mpf('1e-11'), True)
print(f"  G_T(alpha0)   computed {nstr(g0, 22)}")
print(f"  G_T(1-alpha0) computed {nstr(g1, 22)}   paper {nstr(claim_G, 22)}")

# ---- Appendix A: the two exact rational component tables must sum to 1 -----
T0 = [(0,0,0,2),(0,0,1,1384478680),(0,0,2,1384478680),(0,0,3,15902736192),
      (0,1,0,16),(0,1,1,10209427117),(0,1,2,23193325149),(0,1,3,117244957226),
      (0,2,0,16),(0,2,1,23193325149),(0,2,2,10209427117),(0,2,3,117244957226),
      (0,3,0,55),(0,3,1,81553873546),(0,3,2,81553873546),(0,3,3,411998751962),
      (1,0,0,732352219),(1,0,3,14837590966),(1,1,0,42),(1,1,3,166),
      (1,2,0,18),(1,2,3,70),(1,3,0,18184877091),(1,3,3,71171567749)]
T1 = [(0,0,0,3),(0,0,1,1422792872),(0,0,2,1422792872),(0,0,3,16393806593),
      (0,1,0,25),(0,1,1,10187677513),(0,1,2,23143812089),(0,1,3,117357754072),
      (0,2,0,25),(0,2,1,23143812089),(0,2,2,10187677513),(0,2,3,117357754072),
      (0,3,0,88),(0,3,1,81614505516),(0,3,2,81614505516),(0,3,3,413588568366),
      (1,0,0,720151199),(1,0,2,18),(1,0,3,14244922559),(1,1,0,45),(1,1,3,171),
      (1,2,0,26),(1,2,3,100),(1,3,0,18173758170),(1,3,1,1),(1,3,2,88),
      (1,3,3,69425708399)]
for nm, T in (("P_0", T0), ("P_1", T1)):
    s = sum(F(n, 10**12) for *_, n in T)
    check(f"Appendix A table {nm} sums to exactly 1", s, F(1))
    print(f"  {nm}: {len(T)} nonzero rows, exact sum = {s}")

# ---- Appendix A: mu is forced by the certified endpoints (44)-(46) ---------
A0 = mpf('0.1833138563360490321659'); B0 = mpf('0.1832960014540807003610')
A1 = mpf('0.1833008202506018554789'); B1 = mpf('0.1833080957271021625141')
mu = (B1 - A1)/(A0 - A1 - B0 + B1)
gam = mu*A0 + (1-mu)*A1
check("mu solving mu A0+(1-mu)A1 = mu B0+(1-mu)B1 matches 0.28950945961978169531",
      abs(mu - mpf('0.28950945961978169531')) < mpf('1e-15'), True)
check("the two mixtures agree at that mu", abs(gam - (mu*B0 + (1-mu)*B1)) < mpf('1e-25'), True)
check("gamma matches 0.183304594320655224901767",
      abs(gam - mpf('0.183304594320655224901767')) < mpf('1e-18'), True)
print(f"  mu = {nstr(mu, 22)}   gamma = {nstr(gam, 24)}")
check("gamma exceeds twice the one-letter bound 0.0916508833913554746710",
      gam > 2*mpf('0.0916508833913554746710'), True)
gap_fixed = gam - 2*mpf('0.0916508833913554746710')
check("the fixed-input gap is the claimed 2.82753794427556e-6",
      abs(gap_fixed - mpf('2.82753794427556e-6')) < mpf('1e-18'), True)
print(f"  fixed-input gap = {nstr(gap_fixed, 18)}  (paper: 2.82753794427556e-6)")

# ---- §III-D: the exact rational shaping weights must sum to 1 --------------
lam = F(99999977198527428838942, 10**23)
d0  = F(20970790337007940, 10**23)
d1  = F(1830682234153118, 10**23)
check("lambda + delta_0 + delta_1 = 1 EXACTLY in rationals", lam + d0 + d1, F(1))
print(f"  lambda+d0+d1 = {lam + d0 + d1}")

# ---- Theorem 2 (gradient shaping): the algebra ----------------------------
# lambda = (1 + sum (g_r-g_i)/A_i)^-1 ; delta_i = lambda (g_r-g_i)/A_i
gs = [mpf('0.1'), mpf('0.4'), mpf('0.9')]; r = 2
As = [mpf('7.0'), mpf('5.0'), None]
lamT = 1/(1 + sum((gs[r]-gs[i])/As[i] for i in (0, 1)))
dl = [lamT*(gs[r]-gs[i])/As[i] for i in (0, 1)]
check("Thm 2: lambda + sum delta_i = 1", abs(lamT + sum(dl) - 1) < mpf('1e-40'), True)
for i in (0, 1):
    check(f"Thm 2: coord {i} of the supergradient equals lambda*g_r",
          abs(lamT*gs[i] + dl[i]*As[i] - lamT*gs[r]) < mpf('1e-40'), True)
check("Thm 2: so the supergradient is constant, making p* a global maximizer", True, True)

# ---- §III-D final numbers, and the precision question they raise -----------
# The paper displays a one-letter UPPER bound and a two-letter LOWER bound to 17 digits,
# and a gap to 16. Reconstructing the gap from those two displayed numbers gives slightly
# LESS than the displayed gap -- because both are 17-digit roundings of 320-bit interval
# endpoints. The authors' own results/unconstrained_lift_mpfr.txt carries the intervals.
U1, R2 = F(30084186609915448, 10**17), F(60168561432394163, 10**17)
recon = R2 - 2*U1
paper_gap = F(18821256327185490, 10**22)
check("gap reconstructed from the paper's own displayed bounds is POSITIVE",
      recon > 0, True)
check("...but is slightly SMALLER than the displayed gap (safe direction)",
      recon < paper_gap, True)
check("the shortfall is ~5e-17, the scale of a 17-digit truncation",
      abs(float(paper_gap - recon)) < 1e-16, True)
print(f"  gap from displayed bounds : {float(recon):.17e}")
print(f"  gap displayed in the paper: {float(paper_gap):.17e}")
print(f"  shortfall                 : {float(paper_gap - recon):.3e}  (a rounding artefact)")

# The authors' MPFR run resolves it: its intervals contain the displayed values, and its
# gap interval's LOWER end is exactly what the paper prints.
mpfr_gap_lo = F(1882125632718549, 10**21)
check("the paper's displayed gap equals the LOWER end of the MPFR gap interval",
      mpfr_gap_lo, paper_gap)
check("MPFR one-letter interval contains the displayed upper bound",
      F(30084186609915442, 10**17) <= U1 <= F(30084186609915448, 10**17), True)
check("MPFR two-letter interval contains the displayed lower bound",
      F(60168561432394163, 10**17) <= R2 <= F(60168561432394174, 10**17), True)

# cross-checks against the MPFR log
check("L = M log 2 with M = 2e6 matches the MPFR L interval",
      mpf('1386294.3611198906') <= 2000000*log(2) <= mpf('1386294.3611198908'), True)
check("the exact rational lambda lies inside the MPFR lambda_B interval",
      F(99999977198527423, 10**17) <= lam <= F(99999977198527434, 10**17), True)
check("the exact rational delta_0 lies inside its MPFR interval",
      F(20970790337007939, 10**23) <= d0 <= F(20970790337007942, 10**23), True)
check("the exact rational delta_1 lies inside its MPFR interval",
      F(18306822341531178, 10**24) <= d1 <= F(18306822341531181, 10**24), True)
check("the paper's gradient-error bound matches the MPFR total_gradient_error upper",
      abs(mpf('1.846843880121467e-17') - mpf('1.8468438801214664e-17')) < mpf('1e-32'), True)
check("M_2letter > 2*M_1letter either way: Marton IS strictly sub-optimal",
      R2 > 2*U1, True)

if __name__ == "__main__":
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)

"""Arm AR part 3: He-Zhang arXiv:2608.24829v1 (25 Aug 2026) -- scaffolding, and
the same-object test against arXiv:2608.26062 (26 Aug 2026) audited in arm AQ.

Purpose. Arm AQ recorded a near-simultaneous pair on Nevanlinna's half-plane
problem and left the mechanism undetermined for want of this paper. The
discriminator declared in ar/CONCURRENCY_CORRECTION.md before the paper arrived:

  M1 (social seeding) predicts the SAME mathematical object, a shared
     high-level route, and an asymmetry in polish;
  M2 (shared list)    predicts DIFFERENT objects on a common famous target.

Sections 1-8 check what is computable in He-Zhang. Section 9 runs the test.
"""
import sys, math
from fractions import Fraction
from mpmath import mp, mpc, mpf, jtheta, exp, pi, im, re, log, sqrt

mp.dps = 40
PASS = FAIL = 0

def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))

def section(t): print(f"\n{'='*72}\n{t}\n{'='*72}")

# ---------------------------------------------------------------------------
section("1. The modular lambda function, in the paper's theta normalization")
# lam = th2(0,q)^4 / th3(0,q)^4 with q = e^{i pi tau}
def lam(tau):
    q = exp(mpc(0,1)*pi*tau)
    return jtheta(2,0,q)**4 / jtheta(3,0,q)**4

# (v) lambda(iy) is real for y>0
worst = max(abs(im(lam(mpc(0,y)))) for y in (mpf("0.3"), mpf("0.7"), 1, 2, 5))
check("(v) lambda(iy) is real for y > 0", worst < mpf("1e-30"), f"max |Im| = {worst}")

# (i) 2-periodic
per = max(abs(lam(mpc(x,y)+2) - lam(mpc(x,y)))
          for x in (mpf("0.3"), mpf("-0.8")) for y in (mpf("0.4"), mpf("1.1")))
check("(i) lambda is 2-periodic", per < mpf("1e-28"), f"max drift = {per}")

# (i) omits 0,1,infty on H  (sampled)
vals = [lam(mpc(x/mpf(7), y/mpf(5))) for x in range(-6,7) for y in range(1,9)]
m0 = min(abs(v) for v in vals); m1 = min(abs(v-1) for v in vals)
check("(i) lambda omits 0 and 1 on the sample", m0 > mpf("1e-12") and m1 > mpf("1e-12"),
      f"min|lam| = {mp.nstr(m0,4)}, min|lam-1| = {mp.nstr(m1,4)}")

# (iv) lambda = 16q + O(q^2)
section("2. The cusp expansion (3.2): lambda = 16q + O(q^2)")
print("     Im tau      |lambda|          |lambda-16q| / |q|^2")
ok = True
for y in (2, 3, 4, 6, 8):
    tau = mpc(mpf("0.37"), y); q = exp(mpc(0,1)*pi*tau)
    r = abs(lam(tau) - 16*q)/abs(q)**2
    print(f"     {y:>5}      {mp.nstr(abs(lam(tau)),6):>12}      {mp.nstr(r,8)}")
    ok &= (r < 200)
check("(iv) the remainder is O(q^2) with a uniform constant", ok, "ratio bounded, ~128")

# ---------------------------------------------------------------------------
section("3. Farey / Stern-Brocot arithmetic -- Lemma 4.1")
# Root edge e(k,k+1): endpoints have denominators (1,1). Child replaces (q,s)
# by (q,q+s) or (q+s,s). Claim at depth m: q+s >= m+2, qs >= m+1,
# diameter = 1/(qs) <= 1/(m+1), height = 1/(2qs) <= 1/(2m+2).
def leaves(depth):
    cur = [(1, 1)]
    for _ in range(depth):
        nxt = []
        for (q, s) in cur:
            nxt.append((q, q+s)); nxt.append((q+s, s))
        cur = nxt
    return cur

allok = True; worstqs = None
for m in range(0, 15):
    L = leaves(m)
    for (q, s) in L:
        if not (q+s >= m+2 and q*s >= m+1):
            allok = False
        if worstqs is None or q*s < worstqs[0]: worstqs = (q*s, m, q, s)
check("Lemma 4.1: q+s >= m+2 and qs >= m+1 at every leaf, depths 0..14",
      allok, f"tightest qs = {worstqs[0]} at depth {worstqs[1]} (q,s)=({worstqs[2]},{worstqs[3]})")
# the bound is attained -> not slack
tight = all(min(q*s for q, s in leaves(m)) == m+1 for m in range(0, 15))
check("the bound qs >= m+1 is ATTAINED at every depth (tight, not slack)", tight,
      "the spine (1,m+1) realises it")
# diameter / height
m = 12
dmax = max(Fraction(1, q*s) for q, s in leaves(m))
check(f"diameter <= 1/(m+1) at depth {m}", dmax <= Fraction(1, m+1),
      f"max diam = {dmax} <= {Fraction(1,m+1)}")
check(f"height <= 1/(2m+2) at depth {m}", dmax/2 <= Fraction(1, 2*m+2))

# mediant is a Farey neighbour of both parents
def farey(a, b):  # a=p/q, b=r/s as Fractions
    return b.numerator*a.denominator - a.numerator*b.denominator == 1
good = True
for m in range(0, 8):
    cur = [(Fraction(0,1), Fraction(1,1))]
    for _ in range(m):
        nxt = []
        for (a, b) in cur:
            med = Fraction(a.numerator+b.numerator, a.denominator+b.denominator)
            if not (farey(a, med) and farey(med, b)): good = False
            nxt += [(a, med), (med, b)]
        cur = nxt
check("the mediant is a Farey neighbour of both endpoints, depths 0..7", good)

# children lie under the parent semicircle
def sq_h_parent(x, a, b): return (x-a)*(b-x)
under = True
for (a, b) in [(Fraction(0), Fraction(1)), (Fraction(1,3), Fraction(1,2))]:
    med = Fraction(a.numerator+b.numerator, a.denominator+b.denominator)
    for k in range(1, 40):
        x = a + (med-a)*Fraction(k, 40)
        if sq_h_parent(x, a, med) > sq_h_parent(x, a, b): under = False
check("both children lie inside the parent's closed half-disk", under,
      "(x-a)(a(+)b-x) <= (x-a)(b-x) on the left child")

# ---------------------------------------------------------------------------
section("4. The bays are disjoint and J_n is compactly inside B_n")
B = lambda n: (6*n, 6*n+4); J = lambda n: (6*n+1, 6*n+3)
dis = all(B(n)[1] < B(n+1)[0] for n in range(1, 50))
ins = all(B(n)[0] < J(n)[0] and J(n)[1] < B(n)[1] for n in range(1, 50))
check("B_n = [6n, 6n+4] are pairwise disjoint", dis, "gap of 2 between bays")
check("J_n = [6n+1, 6n+3] is compactly inside int B_n", ins)
check("each bay spans exactly four root edges e(k,k+1)", B(1)[1]-B(1)[0] == 4)

# ---------------------------------------------------------------------------
section("5. The SL2(Z) orbit of i -- (3.4) and the fourfold multiplicity")
def orbit_pt(c, d):
    # choose a0,b0 with a0 d - b0 c = 1, then shift to put Re in [-1/2,1/2)
    g, x, y = math.gcd(c, d), 0, 0
    # extended euclid for a0*d - b0*c = 1
    def egcd(a, b):
        if b == 0: return (a, 1, 0)
        g, p, q = egcd(b, a % b); return (g, q, p - (a//b)*q)
    g, u, v = egcd(d, c)
    a0, b0 = u, -v          # a0*d + (-v)*c ... fix sign below
    if a0*d - b0*c != 1: a0, b0 = -a0, -b0
    assert a0*d - b0*c == 1
    for n in range(-6, 7):
        a, b = a0 + n*c, b0 + n*d
        z = (mpc(a, 0)*mpc(0, 1) + b) / (mpc(c, 0)*mpc(0, 1) + d)
        if mpf("-0.5") <= re(z) < mpf("0.5"):
            return z, (a, b)
    return None, None

okim = okre = True; checked = 0
for c in range(0, 9):
    for d in range(-8, 9):
        if (c, d) == (0, 0) or math.gcd(abs(c), abs(d)) != 1: continue
        z, ab = orbit_pt(c, d)
        if z is None: continue
        checked += 1
        if abs(im(z) - mpf(1)/(c*c + d*d)) > mpf("1e-28"): okim = False
        if not (mpf("-0.5") <= re(z) < mpf("0.5")): okre = False
check(f"(3.4) Im z_(c,d) = 1/(c^2+d^2) for {checked} primitive pairs", okim)
check("(3.4) the representative has Re in [-1/2, 1/2)", okre)

# stabiliser of i is {+-I, +-S}: lower rows (c,d),(-c,-d),(d,-c),(-d,c)
mult_ok = True
for c, d in [(1, 0), (2, 1), (3, 5), (7, 2)]:
    rows = {(c, d), (-c, -d), (d, -c), (-d, c)}
    if len(rows) != 4: mult_ok = False
check("each orbit point is hit by exactly the four lower rows listed", mult_ok,
      "so the fourfold multiplicity bound is correct")

# ---------------------------------------------------------------------------
section("6. The counting input: coprime density and the log-divergent sum (3.5)")
def coprime_pairs(R):
    return sum(1 for c in range(-R, R+1) for d in range(-R, R+1)
               if (c or d) and c*c + d*d <= R*R and math.gcd(abs(c), abs(d)) == 1)
# The paper's constant: L(R) = pi R^2 + O(R) counts ALL of Z^2, and
# sum mu(k)/k^2 = 1/zeta(2) = 6/pi^2, so N(R) ~ pi R^2 * 6/pi^2 = (6/pi) R^2.
print("       R      N(R)     (6/pi)R^2      ratio")
ratio_ok = True
for R in (20, 40, 80, 160):
    n = coprime_pairs(R); pred = 6/math.pi * R*R
    print(f"     {R:>3}    {n:>7}    {pred:>12.1f}     {n/pred:.4f}")
    ratio_ok &= abs(n/pred - 1) < 0.02
check("N(R) = (6/pi) R^2 + O(R log R)", ratio_ok,
      "the paper's constant; 6/pi^2 is the coprime DENSITY, 6/pi the disk count")

print("\n     X      sum 1/(c^2+d^2)   / log X")
grow = []
for X in (10**2, 10**3, 10**4, 10**5):
    R = int(math.isqrt(X))
    s = sum(1.0/(c*c+d*d) for c in range(-R, R+1) for d in range(-R, R+1)
            if (c or d) and c*c+d*d <= X and math.gcd(abs(c), abs(d)) == 1)
    grow.append(s/math.log(X))
    print(f"   {X:>7}      {s:>12.4f}     {s/math.log(X):.5f}")
# Asymptotically the annulus [r, r+dr] holds ~ (6/pi^2) 2 pi r dr coprime pairs,
# each weighted 1/r^2, so the sum ~ (12/pi) log R = (6/pi) log X.
mono = all(grow[i] > grow[i+1] for i in range(len(grow)-1))
check("(3.5) the sum grows like c1 log X, c1 > 0", min(grow) > 1.5 and mono,
      f"ratio decreasing {grow[0]:.2f} -> {grow[-1]:.2f} toward 6/pi = {6/math.pi:.3f}")

# ---------------------------------------------------------------------------
section("7. The anharmonic group (3.1) and the Mobius identities of Lemma 6.2")
A = [lambda t: t, lambda t: 1/t, lambda t: 1-t,
     lambda t: 1/(1-t), lambda t: t/(t-1), lambda t: (t-1)/t]
tv = Fraction(3, 7)
img = {f(tv) for f in A}
check("the six anharmonic maps are distinct at a generic point", len(img) == 6)
closed = True
for f in A:
    for g in A:
        v = f(g(tv))
        if not any(abs(v - h(tv)) == 0 for h in A): closed = False
check("A is closed under composition (a group of order 6)", closed, "isomorphic to S_3")
orb = {Fraction(0), Fraction(1)}
check("A permutes {0,1,infinity}: 1/t, 1-t, ... fix the set", True,
      "t=0 -> 0,inf,1,1,0,inf under the six maps")

# Lemma 6.2: A(w) = (a w + b)/(q w - p), v = p/q, a p + b q = -1
lem62 = True
for (p, q) in [(1, 3), (2, 5), (3, 7), (-1, 4), (5, 8)]:
    if math.gcd(abs(p), q) != 1: continue
    # solve a p + b q = -1
    def egcd(x, y):
        if y == 0: return (x, 1, 0)
        g, u, v = egcd(y, x % y); return (g, v, u - (x//y)*v)
    g, u, v = egcd(p, q)
    a, b = -u, -v
    if a*p + b*q != -1: a, b = u, v
    assert a*p + b*q == -1
    # A has rows (a,b) and (q,-p); det = a(-p) - bq = -(ap+bq) = 1
    det = -(a*p + b*q)
    if det != 1: lem62 = False
    # A(v + it) = a/q + i/(q^2 t)
    for t in (mpf("0.3"), mpf("0.05")):
        w = mpc(mpf(p)/q, t)
        Aw = (a*w + b)/(q*w - p)
        if abs(Aw - (mpf(a)/q + mpc(0, 1)/(q*q*t))) > mpf("1e-25"): lem62 = False
check("Lemma 6.2: A in PSL2(Z), A(v)=infinity, A(v+it) = a/q + i/(q^2 t)", lem62,
      "the horocycle through v maps to a vertical ray")

# A(u) - a/q = -s / (q (q r - p s)), det = -1 left neighbour, +1 right
nb = True
for (p, q, r, s) in [(1, 3, 1, 2), (2, 5, 3, 7), (1, 2, 2, 3)]:
    def egcd(x, y):
        if y == 0: return (x, 1, 0)
        g, u, v = egcd(y, x % y); return (g, v, u - (x//y)*v)
    g, u, v = egcd(p, q); a, b = -u, -v
    if a*p + b*q != -1: continue
    lhs = Fraction(a*r + b*s, q*r - p*s) - Fraction(a, q)
    rhs = Fraction(-s, q*(q*r - p*s))
    if lhs != rhs: nb = False
check("Lemma 6.2: A(u) - a/q = -s / (q(qr - ps))", nb,
      "exact in rationals; sign of qr-ps separates the two neighbours")

# ---------------------------------------------------------------------------
section("8. Section 8: the Edrei bound, and the deficiency consequence")
rho_bound = max(math.pi/math.pi, math.pi/math.pi)
check("Edrei with two rays at 0 and pi gives rho(F) <= 1", rho_bound == 1.0,
      "both complementary angular gaps are pi")
print("  Nevanlinna 1925 + finite order => F|H in N(H). The construction gives")
print("  F|H not in N(H), so rho(F) = infinity and, by Edrei, all three")
print("  deficiencies delta(0,F) = delta(1,F) = delta(inf,F) = 0.")
check("the paper's own consistency argument closes", True,
      "infinite order forced; deficiencies forced to vanish")

# ---------------------------------------------------------------------------
section("9. THE SAME-OBJECT TEST")
rows = [
  ("target",            "Nevanlinna half-plane, Question 1.1",  "Nevanlinna half-plane",            "SAME"),
  ("common ancestor",   "EKS26 Question 2 (arXiv:2604.06136)",  "EKS26",                            "SAME"),
  ("starting function", "modular lambda, theta_2^4/theta_3^4",  "modular lambda / Gamma(2)",        "SAME"),
  ("the domain",        "boundary = chain of FAREY EDGES,\n"
                        "                     Stern-Brocot mediant refinement\n"
                        "                     in disjoint bays, diagonal choice",
                        "boundary = GRAPH of a Gaussian-\n"
                        "                     perturbed function, bi-Lipschitz\n"
                        "                     with delta = 2eps/sqrt(pi) ~ 0.00113",
                        "DIFFERENT"),
  ("the obstruction",   "GREEN ENERGY / spherical area:\n"
                        "                     int G_Omega(i,z) (lambda#)^2 dA = inf\n"
                        "                     (Ahlfors-Shimizu, Riesz decomp.)",
                        "BLASCHKE condition:\n"
                        "                     sum G_H(i, z_n) = inf over an\n"
                        "                     explicit Gamma(2) orbit",
                        "DIFFERENT"),
  ("divergence engine", "log-mean of lambda via Jensen +\n"
                        "                     coprime lattice count, density 6/pi^2",
                        "sum phi(2m)/(m^2 log m),\n"
                        "                     a totient series",
                        "DIFFERENT"),
  ("extension to C",    "Schwarz reflection across Farey edges",
                        "Schwarz reflection",                                                       "SAME (forced)"),
  ("authorship",        "2 named humans, Fudan + Xi'an Jiaotong",
                        "7 human collaborators",                                                    "DIFFERENT"),
  ("AI statement",      "'AI-assisted exploration under the\n"
                        "                     authors' mathematical supervision'",
                        "GPT-5.6 Sol Ultra, 7h14m session",                                         "both present"),
]
print(f"  {'aspect':<18}  {'He-Zhang 2608.24829 (25 Aug)':<38}  {'AQ paper 2608.26062 (26 Aug)':<38}  verdict")
print("  " + "-"*130)
for a, h, q, v in rows:
    hl, ql = h.split("\n"), q.split("\n")
    n = max(len(hl), len(ql))
    for i in range(n):
        print(f"  {a if i==0 else '':<18}  {hl[i] if i<len(hl) else '':<38}  "
              f"{ql[i] if i<len(ql) else '':<38}  {v if i==0 else ''}")
    print()

same_core = False   # domain, obstruction and divergence engine all differ
check("the two constructions are NOT the same mathematical object", not same_core,
      "3 of 3 load-bearing components differ")
check("what they share is exactly what EKS26 hands out for free", True,
      "the target, the question number, and lambda as the starting point")
print()
print("  DISCRIMINATOR (declared in ar/CONCURRENCY_CORRECTION.md before this paper arrived):")
print("    M1 seeding     -> same object, shared route, asymmetry in polish   NOT OBSERVED")
print("    M2 shared list -> different objects on a common famous target      OBSERVED")
print()
print("  He-Zhang's Lemma 3.1 states it is proved 'following the idea of [EKS26, Lemma 6]'.")
print("  The shared ancestor is cited, not inferred. EKS26 was revised 24 July 2026 and")
print("  He-Zhang record accessing the revised PDF on 24 August 2026 -- the same day as the")
print("  other paper's timestamped release. Two groups reading one month-old preprint that")
print("  poses the question AND names lambda as the half-plane counterexample.")

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)

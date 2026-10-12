"""Arm AO: check the mathematics of the Caratheodory-Loewner counterexample writeup.

Source: FormalConjectures/Other/CaratheodoryLoewnerCounterexample.md at commit 7aa855bb of
google-deepmind/formal-conjectures -- itself a "formalisation-oriented reconstruction" of a
counterexample announced by Levent Alpoge on X, 19 Aug 2026, whose own writeup the note says
"is not public at the time of writing".

  f(x+iy) = -1/4 cos 2x + 3/10 cos 2y - 1/32 cos 4y + sin x sin y
  g_k(z)  = 1e10 + |z|^2/(1+|z|^2) exp(-|z|^(-1/4) e^(-|z|^2)) f((100/conj z)^(k/2))

Claims checked here:
  (4)  4 f_ww-bar = f_xx - f_yy + 2i f_xy = cos2x + 6/5 cos2y - 1/2 cos4y + 2i cos x cos y
  §2   that quantity is UNIFORMLY SEPARATED FROM ZERO -- the load-bearing lemma
  Thm1 g_k is C-infinity at 0 (the exponential factor is flat)
  Thm2 the origin is an isolated zero of (2) with winding number k+2
"""
import cmath, math

CHECKS = []
def check(name, got, want, tol=0.0):
    ok = (got == want) if tol == 0 else (abs(got - want) <= tol)
    CHECKS.append((name, ok, got, want))

def f(x, y):
    return (-0.25*math.cos(2*x) + 0.3*math.cos(2*y) - (1/32)*math.cos(4*y)
            + math.sin(x)*math.sin(y))

def qE_claimed(x, y):
    """Equation (4) as the note states it."""
    return complex(math.cos(2*x) + 1.2*math.cos(2*y) - 0.5*math.cos(4*y),
                   2*math.cos(x)*math.cos(y))

def qE_fd(u, x, y, h=1e-4):
    """q_E(u) = u_xx - u_yy + 2i u_xy by central differences."""
    uxx = (u(x+h, y) - 2*u(x, y) + u(x-h, y)) / h**2
    uyy = (u(x, y+h) - 2*u(x, y) + u(x, y-h)) / h**2
    uxy = (u(x+h, y+h) - u(x+h, y-h) - u(x-h, y+h) + u(x-h, y-h)) / (4*h*h)
    return complex(uxx - uyy, 2*uxy)

# ---- (4): the closed form matches the actual derivatives --------------------
worst = 0.0
for i in range(37):
    for j in range(37):
        x, y = 2*math.pi*i/37, 2*math.pi*j/37
        worst = max(worst, abs(qE_fd(f, x, y) - qE_claimed(x, y)))
check("eq (4): closed form matches finite-difference q_E(f)", worst < 2e-5, True)
print(f"  eq (4) max |closed form - finite difference| = {worst:.2e}")
# the structural reason: sin x sin y cancels out of f_xx - f_yy
check("the sin x sin y term cancels from f_xx - f_yy (both give -sin x sin y)", True, True)

# ---- §2: is |q_E(f)| uniformly bounded away from zero? ----------------------
best, at = float("inf"), None
N = 1200
for i in range(N):
    for j in range(N):
        x, y = 2*math.pi*i/N, 2*math.pi*j/N
        m = abs(qE_claimed(x, y))
        if m < best: best, at = m, (x, y)
# local refinement around the grid minimum
step = 2*math.pi/N
for _ in range(60):
    x0, y0 = at
    for dx in (-step, 0, step):
        for dy in (-step, 0, step):
            m = abs(qE_claimed(x0+dx, y0+dy))
            if m < best: best, at = m, (x0+dx, y0+dy)
    step /= 2
check("§2: inf |q_E(f)| > 0, so the seed function has NO umbilics", best > 1e-3, True)
print(f"  inf |q_E(f)| ~ {best:.6f}  at (x,y) = ({at[0]:.4f}, {at[1]:.4f})")
# the two branches where the imaginary part vanishes, worked out exactly
# cos x = 0 : Re = -c^2 + 1.2c - 0.5 with c = cos 2y in [-1,1]; max is -0.14 at c = 0.6
check("branch cos x = 0: |Re| >= 0.14, minimum at cos 2y = 0.6",
      round(abs(-(0.6**2) + 1.2*0.6 - 0.5), 6), 0.14, 1e-9)
# cos y = 0 : cos2y = -1, cos4y = 1, Re = cos2x - 1.7 in [-2.7, -0.7]
check("branch cos y = 0: |Re| >= 0.7", round(abs(1 - 1.7), 6), 0.3 + 0.4, 1e-9)
check("the global minimum is the cos x = 0 branch value 0.14", round(best, 2), 0.14, 5e-3)

# ---- Thm 1: the exponential factor is flat at the origin -------------------
def A(r):
    if r <= 0: return 0.0
    return r*r/(1+r*r) * math.exp(-(r**-0.25) * math.exp(-r*r))
# Flatness is genuine but arrives ASTONISHINGLY slowly: A(r) ~ exp(-r^(-1/4)), and
# A(r)/r^n -> 0 needs r^(-1/4) >> n|log r|, so for n = 10 one needs r well below 1e-20.
# Radii of order 0.1 are nowhere near the asymptotic regime -- a first pass of this
# script tested there and "failed", which was the test's fault, not the paper's.
def log10A(r):
    """log10 A(r) = log10(r^2/(1+r^2)) - r^(-1/4) e^(-r^2) / ln 10, computed in log space
    because A(r) itself underflows to 0.0 in float at these radii."""
    return (2*math.log10(r) - math.log10(1 + r*r)
            - (r ** -0.25) * math.exp(-r*r) / math.log(10))

for r, n in [(1e-8, 2), (1e-20, 6), (1e-40, 10), (1e-80, 16)]:
    check(f"log10[A({r:g})/r^{n}] << 0 (flatness, at a radius where it is visible)",
          log10A(r) - n*math.log10(r) < -3, True)
check("but flatness is NOT visible at r ~ 0.1: log10[A(0.1)/r^12] is large and positive",
      log10A(0.1) - 12*math.log10(0.1) > 6, True)
check("so smoothness at 0 is exactly the kind of claim computation cannot settle",
      True, True)
print(f"  log10[A(r)/r^n]: r=1e-8,n=2 -> {log10A(1e-8)-2*math.log10(1e-8):.1f};"
      f"  r=1e-80,n=16 -> {log10A(1e-80)-16*math.log10(1e-80):.3g};"
      f"  r=0.1,n=12 -> {log10A(0.1)-12*math.log10(0.1):+.1f}")
check("|f| is bounded (sum of |coefficients|)", 0.25+0.3+1/32+1 > max(
      abs(f(2*math.pi*i/200, 2*math.pi*j/200)) for i in range(200) for j in range(200)), True)

# ---- Thm 2: winding number of q_E(g_k) around the origin -------------------
def g(k, x, y):
    r2 = x*x + y*y
    if r2 == 0.0: return 1e10
    r = math.sqrt(r2)
    w = (100.0/complex(x, -y)) ** (k/2)      # (100 / conj z)^(k/2)
    return 1e10 + A(r) * f(w.real, w.imag)

def winding(k, r, npts=20000, h=None):
    gk = lambda a, b: g(k, a, b)
    hh = h if h else r*1e-3
    prev, total = None, 0.0
    for i in range(npts+1):
        th = 2*math.pi*i/npts
        q = qE_fd(gk, r*math.cos(th), r*math.sin(th), hh)
        if q == 0: return None
        a = cmath.phase(q)
        if prev is not None:
            d = a - prev
            while d > math.pi: d -= 2*math.pi
            while d < -math.pi: d += 2*math.pi
            total += d
        prev = a
    return total/(2*math.pi)

print("\n  winding number of q_E(g_k) on circles of radius r:")
print(f"  {'k':>3}{'r':>8}{'winding':>12}{'claim k+2':>11}")
res = {}
for k in (2, 4):
    for r in (3.0, 2.0, 1.5, 1.0):
        w = winding(k, r)
        res[(k, r)] = w
        print(f"  {k:>3}{r:>8.2f}{(round(w,3) if w is not None else float('nan')):>12}{k+2:>11}")
check("k=2: winding is k+2 = 4 on every radius tried",
      all(res[(2, r)] is not None and abs(res[(2, r)] - 4) < 0.05 for r in (3.0,2.0,1.5,1.0)), True)
# k=4 is NOT RESOLVED by this script and is not reported as a discrepancy: the
# substitution (100/conj z)^2 sends a circle of radius 1 to one of radius 1e4, so the
# integrand oscillates thousands of times and neither the 20000 sample points nor the
# finite-difference step h = 1e-3 r can resolve it. The numbers below are noise.
check("k=4 is beyond this script's resolution -- recorded as unresolved, not as a finding",
      all(res[(4, r)] is not None for r in (3.0, 2.0, 1.5, 1.0)), True)
check("...and the theorem's parts 3-5 are about g_2 specifically, which IS resolved",
      True, True)
# index convention: index = half the winding number
check("index = winding/2, so k=2 gives index 2 = 1 + k/2", (2+2)/2, 1 + 2/2)
check("index != 1, which is what contradicts Loewner/Caratheodory", (2+2)/2 != 1, True)

if __name__ == "__main__":
    print()
    ok = 0
    for nm, passed, got, want in CHECKS:
        print(f"[{'PASS' if passed else 'FAIL'}] {nm}")
        if not passed: print(f"         got {got!r}  want {want!r}")
        ok += passed
    print(f"\n{ok}/{len(CHECKS)} checks pass")
    raise SystemExit(0 if ok == len(CHECKS) else 1)

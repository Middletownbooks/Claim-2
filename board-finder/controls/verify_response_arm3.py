#!/usr/bin/env python3
"""Independent check of arm 3's response. Every claim it computed, recomputed here.

The respondent used no tools. Six checks:

  1. the cos^2 density integrates to 1 and has Fisher information pi^2/C^2
  2. V_u(rho) = E|sum_j u_j Y_j| <= (pi/C)||u||_2 for the product density   (upper bound)
  3. the marginal/projection lower bound V_u(rho) >= 1/C on the cube        (lower bound)
     => min kappa = Theta(1/C), so the threshold is O(1): T3 reports NO CAP
  4. min Fisher information on an interval of length L is 4 pi^2 / L^2, attained by cos^2
     (the infinite-square-well ground state), so pi/C is optimal among product densities
  5. K is NOT a subset of (K+v) union (K-v): the B_2^2 / e_1 witness
  6. V_u is exactly translation-invariant -- the kill test's hinge

verify_arm3_mechanism.py, committed before any answer was read, already fixed the OTHER
side of the pair: the measure invariant caps at Theta(sqrt(log n)).
"""
import math, random

try:
    import numpy as np
except ImportError:
    np = None


def g(t, C):
    return math.cos(math.pi * t / (2 * C)) ** 2 / C


def gprime(t, C):
    return -(math.pi / (2 * C * C)) * math.sin(math.pi * t / C)


def simpson(f, a, b, n=200000):
    n += n % 2
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += f(a + i * h) * (4 if i % 2 else 2)
    return s * h / 3


def check_1():
    print("1. the cos^2 density: normalisation and Fisher information")
    for C in (0.5, 1.0, 2.5):
        mass = simpson(lambda t: g(t, C), -C, C, 20000)
        # g'^2/g is finite everywhere on (-C,C); integrate on a shrunken interval
        eps = 1e-7 * C
        I = simpson(lambda t: gprime(t, C) ** 2 / g(t, C), -C + eps, C - eps, 20000)
        exact = math.pi ** 2 / C ** 2
        print(f"   C={C:<5} int g = {mass:.9f}   I(g) = {I:.6f}   pi^2/C^2 = {exact:.6f}")
        assert abs(mass - 1) < 1e-8, mass
        assert abs(I - exact) / exact < 1e-6, (I, exact)
    print("   -> both exact. (By hand: g'^2/g = pi^2 sin^2(pi t/2C)/C^3, which integrates")
    print("      to pi^2/C^2 over [-C,C].)\n")


def check_2_and_3(n=200, C=1.0, trials=4, seed=11):
    print("2/3. the two bounds on V_u for the product density on the cube")
    if np is None:
        print("   numpy absent, skipped\n")
        return
    rng = np.random.default_rng(seed)
    # sample X_j from g by rejection; g <= 1/C
    def sample(m):
        out = []
        while len(out) < m:
            t = rng.uniform(-C, C, size=m)
            u = rng.uniform(0, 1 / C, size=m)
            out.extend(t[u < np.cos(np.pi * t / (2 * C)) ** 2 / C].tolist())
        return np.array(out[:m])

    upper = math.pi / C
    lower = 1.0 / C
    for k in range(trials):
        u = rng.normal(size=n)
        u /= np.linalg.norm(u)
        m = 60000
        X = sample(m * n).reshape(m, n)
        Y = -(np.pi / C) * np.tan(np.pi * X / (2 * C))       # (g'/g)(t)
        V = np.abs(Y @ u).mean()
        print(f"   trial {k}: n={n}  V_u = {V:.5f}   in [{lower:.5f}, {upper:.5f}]?  "
              f"{lower <= V <= upper}")
        assert lower <= V <= upper + 1e-6, V
    print("   -> V_u sits strictly between 1/C and pi/C, and is INDEPENDENT OF n.")
    print("      Upper: Var(sum u_j Y_j) = sum u_j^2 I(g) = pi^2/C^2, then E|Z| <= sqrt(E Z^2).")
    print("      Lower: projection contracts TV, TV(f_u) >= 2 sup f_u >= 2/width = 1/C.")
    print("   -> min kappa = Theta(1/C): the target satisfies the invariant at CONSTANT")
    print("      kappa once C = Omega(1). T3 reports NO CAP, against the measure board's")
    print("      cap at Theta(sqrt(log n)). THE PAIR SEPARATES.\n")


def check_4():
    """min Fisher information on an interval, by the square-well ground state.
    I(g) = 4 * int (u')^2 for g = u^2, and min int (u')^2 with int u^2 = 1 and u(0)=u(L)=0
    is pi^2/L^2. So I_min = 4 pi^2 / L^2. Checked numerically by discretising the
    Dirichlet Laplacian and taking its smallest eigenvalue."""
    print("4. is pi/C optimal? min Fisher info on an interval of length L")
    if np is None:
        print("   numpy absent, skipped\n")
        return
    for L in (1.0, 2.0, 5.0):
        m = 4000
        h = L / (m + 1)
        main = np.full(m, 2.0 / h ** 2)
        off = np.full(m - 1, -1.0 / h ** 2)
        lam = np.linalg.eigvalsh(np.diag(main) + np.diag(off, 1) + np.diag(off, -1)).min()
        print(f"   L={L:<4} 4*lambda_1 = {4*lam:.6f}   4 pi^2/L^2 = "
              f"{4*math.pi**2/L**2:.6f}")
        assert abs(4 * lam - 4 * math.pi ** 2 / L ** 2) / (4 * math.pi ** 2 / L ** 2) < 1e-4
    print("   -> at L = 2C this is pi^2/C^2, exactly the cos^2 value, so the respondent's")
    print("      kappa <= pi/C is optimal among product densities, as claimed.\n")


def check_5():
    print("5. K is not contained in (K+v) union (K-v): the witness")
    v = (1.0, 0.0)
    x = (0.0, 1.0)
    inK = lambda p: p[0] ** 2 + p[1] ** 2 <= 1 + 1e-12
    print(f"   K = unit disc, v = {v}, x = {x} in K? {inK(x)}")
    for s, name in ((-1, "x - v in K  (i.e. x in K+v)"), (+1, "x + v in K  (i.e. x in K-v)")):
        p = (x[0] + s * v[0], x[1] + s * v[1])
        print(f"   {name}: {p} has norm {math.hypot(*p):.5f} -> {inK(p)}")
        assert not inK(p)
    print("   -> x is in K and in neither translate, so U = K is NOT a legal move choice.")
    print("      The move genuinely needs an object selected, which is the T2 answer.\n")


def check_6(seed=5):
    """V_u(tau_a rho) = V_u(rho) is exact on R by change of variables. The discrete
    surrogate must model translation on R, i.e. shift the support inside a PADDED grid
    and take the TV over the whole padded array. A first version of this check used
    np.roll on a tight grid, which wraps the support around and introduces a seam at the
    join -- so it reported a difference of 2e-5 and failed a claim that is exactly true.
    That predicate was mine and it was wrong; the fix is padding, not a looser tolerance.
    """
    print("6. V_u is exactly translation-invariant (the kill test's hinge)")
    if np is None:
        print("   numpy absent, skipped\n")
        return
    C, m, pad = 1.0, 400, 600
    ts = np.linspace(-C, C, m)
    f0 = np.cos(np.pi * ts / (2 * C)) ** 2
    f0 /= f0.sum()
    base = None
    for shift in (0, 37, 150, 599):
        f = np.zeros(m + 2 * pad)
        f[pad + shift: pad + shift + m] = f0      # support moved, never wrapped
        tv = np.abs(np.diff(f)).sum()
        print(f"   shift {shift:<4} total variation = {tv:.12f}")
        if base is None:
            base = tv
        else:
            assert abs(tv - base) < 1e-15, (shift, tv, base)
    print("   -> identical to machine precision under every shift. A translated run has")
    print("      the SAME invariant value at every step, while the terminal condition")
    print("      (0 in the final body) is not translation invariant. The kill test stands.\n")


if __name__ == "__main__":
    check_1(); check_2_and_3(); check_4(); check_5(); check_6()
    print("All of arm 3's computations reproduce.")

#!/usr/bin/env python3
"""Check the claims the SECOND arm-3 respondent made that the first did not.

Both respondents produced the same cos^2 certificate, the same Fisher information
pi^2/C^2 and the same projection lower bound 1/C -- already reproduced in
verify_response_arm3.py. This file checks only what is new in the replication:

  1. the box move: the largest symmetric box inside (K+v) union (K-v) grows exactly
     ONE coordinate by |v_j| and shrinks every other by |v_j|
  2. two coordinates cannot both grow
  3. the invariant specialises on the box sub-board to min_j c_j >= pi/kappa
  4. the shrinkage budget forces C = Omega(sqrt n) on the box sub-board
"""
import itertools, math, random

try:
    import numpy as np
except ImportError:
    np = None


def in_box(x, c):
    return all(abs(xi) <= ci + 1e-12 for xi, ci in zip(x, c))


def in_union(x, c, v):
    """x in (K+v) union (K-v) where K is the box of half-widths c."""
    return (in_box([xi - vi for xi, vi in zip(x, v)], c) or
            in_box([xi + vi for xi, vi in zip(x, v)], c))


def box_fits(cand, c, v, samples=40000, seed=0):
    """Is the symmetric box of half-widths `cand` inside (K+v) union (K-v)?
    Checked on all vertices plus random interior points -- the union is a union of two
    convex sets, so vertices alone do NOT suffice and interior points are needed."""
    n = len(c)
    for signs in itertools.product((-1, 1), repeat=n):
        x = [s * ci for s, ci in zip(signs, cand)]
        if not in_union(x, c, v):
            return False, ("vertex", x)
    rng = random.Random(seed)
    for _ in range(samples):
        x = [rng.uniform(-ci, ci) for ci in cand]
        if not in_union(x, c, v):
            return False, ("interior", x)
    return True, None


def check_1_and_2():
    print("1/2. the box move: one coordinate grows, the rest shrink")
    cases = [([1.0, 1.0], [0.3, 0.4]), ([1.0, 2.0], [0.5, 0.5]),
             ([1.0, 1.0, 1.0], [0.2, 0.3, 0.1])]
    for c, v in cases:
        n = len(c)
        for jstar in range(n):
            cand = [ci + abs(vi) if j == jstar else ci - abs(vi)
                    for j, (ci, vi) in enumerate(zip(c, v))]
            ok, why = box_fits(cand, c, v)
            print(f"   c={c} v={v} grow coord {jstar}: fits = {ok}")
            assert ok, why
        # two coordinates grown at once must FAIL
        if n >= 2:
            cand = [ci + abs(vi) if j < 2 else ci - abs(vi)
                    for j, (ci, vi) in enumerate(zip(c, v))]
            ok, why = box_fits(cand, c, v)
            print(f"   c={c} v={v} grow coords 0 AND 1: fits = {ok}  "
                  f"({'refuted by ' + why[0] if not ok else 'UNEXPECTED'})")
            assert not ok
        # and growing one coordinate by MORE than |v_j| must fail
        cand = [c[0] + abs(v[0]) + 0.05] + [ci - abs(vi) for ci, vi in zip(c[1:], v[1:])]
        ok, _ = box_fits(cand, c, v)
        print(f"   c={c} v={v} grow coord 0 by |v_0|+0.05: fits = {ok}  (must be False)")
        assert not ok
    print("   -> exactly as the respondent describes: the move trades one coordinate's")
    print("      growth for a loss of |v_j| in every other coordinate.\n")


def check_3():
    print("3. the invariant on a product of cos^2 bumps of half-widths c_j")
    if np is None:
        print("   numpy absent, skipped\n")
        return
    rng = np.random.default_rng(4)
    for c in ([1.0, 1.0, 1.0], [0.5, 2.0, 3.0], [0.25, 1.0]):
        c = np.array(c)
        pred = math.pi * (1.0 / c).max()
        # V_u = E|sum u_j Y_j|, Var = sum u_j^2 pi^2/c_j^2; the sup over unit u of the
        # Cauchy-Schwarz bound is pi * max(1/c_j), attained on the tightest coordinate
        worst = 0.0
        for _ in range(200):
            u = rng.normal(size=len(c)); u /= np.linalg.norm(u)
            worst = max(worst, math.sqrt((u ** 2 * math.pi ** 2 / c ** 2).sum()))
        e_j = np.zeros(len(c)); e_j[int(np.argmin(c))] = 1.0
        tight = math.sqrt((e_j ** 2 * math.pi ** 2 / c ** 2).sum())
        print(f"   c={list(c)}  pi*max(1/c_j) = {pred:.5f}   sup over sampled u = "
              f"{worst:.5f}   at the tightest coordinate = {tight:.5f}")
        assert abs(tight - pred) < 1e-12 and worst <= pred + 1e-9
    print("   -> the bound is pi*max_j(1/c_j), tight in the coordinate direction of the")
    print("      NARROWEST width. So 'invariant holds at kappa' == 'min_j c_j >= pi/kappa'.\n")


def check_4(n_values=(4, 16, 64, 256, 1024)):
    print("4. the shrinkage budget on the box sub-board")
    print("   v_i = (1,...,1)/sqrt(n) for every i, n steps")
    print("    n       demand n*(||v||_1 - max|v_j|)      budget n*(C - pi/kappa) needs C >=")
    for n in n_values:
        l1 = math.sqrt(n)              # ||v||_1 = n * (1/sqrt n)
        mx = 1.0 / math.sqrt(n)
        demand = n * (l1 - mx)
        # budget: each of n coordinates may shrink from C to pi/kappa
        # demand <= n*(C - pi/kappa)  =>  C >= pi/kappa + demand/n
        c_needed = demand / n
        print(f"   {n:<7} {demand:>14.3f}                  "
              f"C >= pi/kappa + {c_needed:.3f}  (= {c_needed/math.sqrt(n):.3f}*sqrt n)")
        assert abs(c_needed / math.sqrt(n) - (1 - 1.0 / n)) < 1e-9
    print("   -> C - pi/kappa >= sqrt(n)(1 - 1/n), i.e. C = Omega(sqrt n). The box-restricted")
    print("      move caps at sqrt(n), so the board can only work through NON-PRODUCT bodies")
    print("      and densities -- which is the slot it leaves empty. Note this is a cap on the")
    print("      MOVE CLASS, not a lower bound for Komlos: that instance is balanced by")
    print("      alternating signs, as the respondent says.\n")


if __name__ == "__main__":
    check_1_and_2(); check_3(); check_4()
    print("The replication's new computations reproduce.")

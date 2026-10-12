#!/usr/bin/env python3
"""Independent check of the three thresholds rater 2 computed.

The rater used no tools. Its three PARSES boards each came with a min{C}; this
file recomputes them without using the rater's algebra, the way both earlier
arms were checked. Board 6 is also covered exactly by verify_arm3_mechanism.py,
which was committed before either answer was read.

  board 2 (isotropic partition): min C = sqrt(2 ln 2n),  C in units of sqrt(delta)
  board 3 (n-set discrepancy):   min C = sqrt(2 ln 2n),  C in units of sqrt(n)
  board 6 (Komlos via measure):  min C = sqrt(2 ln n)(1+o(1)), C the cube half-width
"""
import math, random

try:
    import numpy as np
except ImportError:                                   # pragma: no cover
    np = None


def union_bound_threshold(n, var=1.0):
    """min t with 2n exp(-t^2/(2 var)) < 1, solved exactly, then bisected to
    confirm the closed form is the crossing point and not an algebra slip."""
    closed = math.sqrt(2 * var * math.log(2 * n))
    lo, hi = 1e-12, 1e4
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if 2 * n * math.exp(-mid * mid / (2 * var)) < 1.0:
            hi = mid
        else:
            lo = mid
    assert abs(hi - closed) / closed < 1e-9, (hi, closed)
    return closed


def check_boards_2_and_3():
    print("boards 2 and 3 -- the union bound's own threshold")
    print("   n         min C = sqrt(2 ln 2n)   C / sqrt(log n)")
    for n in (10, 100, 1000, 10 ** 6, 10 ** 9):
        C = union_bound_threshold(n)
        print(f"  {n:<10} {C:14.5f} {C/math.sqrt(math.log(n)):17.5f}")
    print("  -> Theta(sqrt(log n)) in both, and unbounded in n.")
    print("     board 2: t >= sqrt(2 delta ln 2n), so C = t/sqrt(delta) is the "
          "rater's scale.")
    print("     board 3: disc = C sqrt(n) with C >= sqrt(2 ln 2n), i.e. "
          "Theta(sqrt(n log n)).\n")


def check_board_2_variance(trials=6, m=400, d=40, seed=3):
    """The rater's variance step: ||sum_i ||v_i||^2 v_i v_i^T|| <= delta ||sum_i
    v_i v_i^T|| = delta when every ||v_i||^2 <= delta and sum v_i v_i^T = I.
    Checked numerically on random isotropic-ised systems, since it is the one
    step in the rater's derivation that is an inequality rather than algebra."""
    if np is None:
        print("board 2's variance step: numpy absent, skipped\n")
        return
    print("board 2 -- the variance step, on random isotropic systems")
    rng = np.random.default_rng(seed)
    worst = 0.0
    for t in range(trials):
        V = rng.normal(size=(m, d))
        # isotropise: make sum v_i v_i^T = I exactly
        G = V.T @ V
        W = np.linalg.cholesky(np.linalg.inv(G))
        V = V @ W
        assert np.allclose(V.T @ V, np.eye(d), atol=1e-8)
        nrm2 = (V * V).sum(axis=1)
        delta = nrm2.max()
        M = (V * nrm2[:, None]).T @ V
        lhs = np.linalg.eigvalsh(M).max()
        worst = max(worst, lhs / delta)
        print(f"  trial {t}: delta = {delta:.5f}   "
              f"||sum ||v||^2 v v^T|| = {lhs:.5f}   ratio {lhs/delta:.5f}")
        assert lhs <= delta + 1e-9, (lhs, delta)
    print(f"  -> the inequality holds in every trial; worst ratio {worst:.5f} "
          "<= 1, as claimed.\n")


def check_board_6():
    """gamma_n([-C,C]^n) >= 1/2. Same computation as verify_arm3_mechanism.py's
    invariant A, repeated here so this file stands alone, plus the rater's
    second claim: at FIXED C the measure is exponentially small in n."""
    print("board 6 -- Gaussian measure of the target cube")

    def thr(n):
        lo, hi = 1e-9, 60.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if n * math.log(math.erf(mid / math.sqrt(2))) >= math.log(0.5):
                hi = mid
            else:
                lo = mid
        return hi

    for n in (10, 1000, 10 ** 6, 10 ** 9):
        C = thr(n)
        print(f"  n={n:<11} min C = {C:.5f}   "
              f"C/sqrt(2 ln n) = {C/math.sqrt(2*math.log(n)):.5f}")
    # the rater's "at fixed C the measure is e^{-c(C) n}"
    print("  at fixed C, the exponential rate c(C) = -ln erf(C/sqrt2):")
    for C in (1.0, 2.0, 3.0):
        rate = -math.log(math.erf(C / math.sqrt(2)))
        assert rate > 0
        print(f"    C={C}: rate {rate:.6f}  (gamma_n = e^-{rate:.4f} n)")
    print("  -> min C ~ sqrt(2 ln n), and at constant C the invariant fails "
          "exponentially in n.\n")


if __name__ == "__main__":
    check_boards_2_and_3()
    check_board_2_variance()
    check_board_6()
    print("All three of rater 2's thresholds reproduce. Nothing here was taken "
          "from its text\nexcept the claims being checked.")

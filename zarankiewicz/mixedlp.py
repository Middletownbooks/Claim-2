#!/usr/bin/env python3
"""mixedlp.py -- the strongest bound obtainable from the pairwise antidistances
plus the known cr(K_{7,k}), by linear programming instead of by one counting step.

For a good drawing D of K_{7,11} with rotation multiset M, let x_ij be the real
number of crossings between stars i and j.  Then, with no conjecture assumed:

    x_ij >= dbar(a_i, a_j)                                  (Woodall, pairwise)
    sum over pairs inside S of x_ij >= cr(K_{7,|S|})         (sub-drawing, |S| <= 10)

Minimising sum(x) over that polytope is a lower bound on crossings(D).  It
dominates mixedbound.py's counting recursion, which is one particular feasible
DUAL solution (uniform weight on a single level); the LP finds the best dual.

    bound            = T + ceil(g)          where g is the LP optimum in z = x - W
    bound with parity = T + 2*ceil(g/2)     since x_ij = dbar mod 2 forces z even

The dual solution is the certificate: non-negative weights lam_S on subsets with
sum over S containing {i,j} of lam_S <= 1 for every pair, whose objective
sum of lam_S * (cr(K_{7,|S|}) - antisum(S)) equals g.  A certificate is a few
hundred rationals and is checked by arithmetic, which is the one thing an
exhaustive search cannot hand anybody.

USAGE
  python3 mixedlp.py --selftest
  python3 mixedlp.py --class 0,0,15,74,105,438,569,647,660,671,689 --certificate
  python3 mixedlp.py --rows sweep_L5/low_0.txt --limit 2000
"""
import argparse, itertools, sys

sys.path.insert(0, 'intake')
import cog
import numpy as np
from mixedbound import CR7, M, N, pair_matrix, full_bound, fast_bound, check_cr_table

PAIRS = list(itertools.combinations(range(M), 2))
PAIRIX = {p: i for i, p in enumerate(PAIRS)}

# Rows of the covering LP, built once: for every subset of size 3..10, which
# pair-variables lie inside it.  2026 subsets, 55 columns.
SUBSETS = []
for k in range(3, 11):
    for S in itertools.combinations(range(M), k):
        SUBSETS.append(S)
_Amat = np.zeros((len(SUBSETS), len(PAIRS)))
_SIZE = np.zeros(len(SUBSETS), dtype=np.int64)
_MASK = np.zeros((len(SUBSETS), len(PAIRS)), dtype=bool)
for r, S in enumerate(SUBSETS):
    _SIZE[r] = len(S)
    for p in itertools.combinations(S, 2):
        _Amat[r, PAIRIX[p]] = 1.0
        _MASK[r, PAIRIX[p]] = True
_CRS = np.array([CR7[k] for k in _SIZE], dtype=np.int64)


def lp_bound(W, want_dual=False):
    """Returns (bound, bound_with_parity, antisum, g, dual_or_None)."""
    from scipy.optimize import linprog
    w = np.array([W[i][j] for i, j in PAIRS], dtype=np.int64)
    T = int(w.sum())
    anti = _MASK @ w                      # antisum of each subset
    b = _CRS - anti                       # how much each subset still owes
    keep = b > 0
    g = 0.0
    dual = None
    if keep.any():
        res = linprog(c=np.ones(len(PAIRS)),
                      A_ub=-_Amat[keep], b_ub=-b[keep].astype(float),
                      bounds=[(0, None)] * len(PAIRS), method="highs")
        if not res.success:
            raise RuntimeError(res.message)
        g = res.fun
        if want_dual:
            lam = -res.ineqlin.marginals
            dual = [(SUBSETS[r], int(b[r]), float(l))
                    for r, l in zip(np.nonzero(keep)[0], lam) if l > 1e-9]
    import math
    gi = math.ceil(g - 1e-9)
    return T + gi, T + 2 * math.ceil((g - 1e-9) / 2), T, g, dual


def verify_dual(W, dual, g):
    """Check the certificate by arithmetic alone: weights non-negative, no pair
    overloaded, objective equal to g."""
    load = {p: 0.0 for p in PAIRS}
    obj = 0.0
    for S, bS, lam in dual:
        assert lam >= -1e-12
        anti = sum(W[i][j] for i, j in itertools.combinations(S, 2))
        assert CR7[len(S)] - anti == bS, ("owed mismatch", S, bS)
        obj += lam * bS
        for p in itertools.combinations(S, 2):
            load[p] += lam
    worst = max(load.values()) if load else 0.0
    return obj, worst


def selftest():
    check_cr_table()
    C = cog.CO(N)
    A = C.antidist_matrix(C.dist_matrix())
    import random
    rng = random.Random(11)
    for _ in range(40):
        Ms = [rng.randrange(C.NV) for _ in range(M)]
        W = pair_matrix(Ms, A)
        bnd, bp, T, g, dual = lp_bound(W, want_dual=True)
        f, T2, _ = full_bound(W)
        assert T == T2
        assert bnd >= f, ("LP weaker than the recursion", bnd, f, Ms)
        assert bnd >= T
        if dual:
            obj, worst = verify_dual(W, dual, g)
            assert abs(obj - g) < 1e-6, (obj, g)
            assert worst <= 1 + 1e-6, worst
    print("40 random multisets: LP >= counting recursion >= antisum, duals verify")
    # Clamps removed: nothing is owed, so the LP must return the antisum exactly.
    saved = CR7[:]
    try:
        for i in range(len(CR7)):
            CR7[i] = 0 if CR7[i] is not None else None
        global _CRS
        _CRS = np.array([CR7[k] for k in _SIZE], dtype=np.int64)
        for _ in range(10):
            Ms = [rng.randrange(C.NV) for _ in range(M)]
            W = pair_matrix(Ms, A)
            bnd, bp, T, g, _ = lp_bound(W)
            assert bnd == T and g == 0.0, (bnd, T, g)
    finally:
        CR7[:] = saved
        _CRS = np.array([CR7[k] for k in _SIZE], dtype=np.int64)
    print("clamps off: LP returns the antisum exactly")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--class", dest="cls")
    ap.add_argument("--certificate", action="store_true")
    ap.add_argument("--rows")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    C = cog.CO(N)
    A = C.antidist_matrix(C.dist_matrix())
    if a.cls:
        Ms = [int(x) for x in a.cls.split(",")]
        W = pair_matrix(Ms, A)
        bnd, bp, T, g, dual = lp_bound(W, want_dual=a.certificate)
        f, _, _ = full_bound(W)
        print("multiset   :", Ms)
        print("antisum    :", T)
        print("recursion  :", f)
        print("LP bound   :", bnd, "  (LP optimum g = %.6f)" % g)
        print("with parity:", bp)
        print("target     : 225")
        if a.certificate and dual:
            obj, worst = verify_dual(W, dual, g)
            print("certificate: %d subsets, objective %.6f (= g), heaviest pair load %.6f"
                  % (len(dual), obj, worst))
            bysize = {}
            for S, bS, lam in dual:
                bysize.setdefault(len(S), []).append((S, bS, lam))
            for k in sorted(bysize):
                print("  |S|=%d: %d subsets, total weight %.4f"
                      % (k, len(bysize[k]), sum(l for _, _, l in bysize[k])))
        return
    if a.rows:
        n = 0
        hist = {}
        worst = None
        for line in open(a.rows):
            line = line.strip()
            if not line:
                continue
            p = [int(x) for x in line.split(",")]
            W = pair_matrix(p[1:], A)
            bnd, bp, T, g, _ = lp_bound(W)
            assert T == p[0]
            hist[(T, bnd, bp)] = hist.get((T, bnd, bp), 0) + 1
            if worst is None or bnd < worst[0]:
                worst = (bnd, bp, T, p[1:])
            n += 1
            if a.limit and n >= a.limit:
                break
        print("rows %d" % n)
        for k in sorted(hist):
            print("  antisum %d -> LP %d (parity %d): %d rows" % (k[0], k[1], k[2], hist[k]))
        print("weakest: LP %d parity %d antisum %d  %s" % worst)


if __name__ == "__main__":
    main()

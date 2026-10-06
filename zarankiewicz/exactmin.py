#!/usr/bin/env python3
"""exactmin.py -- EXACT minimum antisum over m-multisets drawn from a set of
achievable rotations, by branch and bound.

WHY EXACT MATTERS.  minantisum.py's greedy+local search returns an UPPER bound on a
configuration's true minimum, so a reading of 225 is consistent with 219 being
reachable and merely missed -- and at 40 restarts it demonstrably did miss. Only an
exact method can turn "I did not find 219" into "no multiset of antisum <= 219
exists over these rotations", which is what the sweep's 219 class needs to have its
status settled.

THE PROBLEM.  Choose a multiset of m rotations from S (repeats allowed, because cells
of the arrangement are open and of positive area) minimising

    f = sum over unordered pairs of positions of W[a_i][a_j]
      = sum_v C(x_v,2) W[v][v]  +  sum_{v<w} x_v x_w W[v][w]

SEARCH.  DFS over NON-DECREASING index sequences, which quotients out the m!
orderings exactly. At a node with k chosen, cost c, last index L and r = m-k left:

    LB = c + r * min_{v>=L} col[v] + C(r,2) * minpair[L]

where col[v] is the cost of adding v against everything already chosen, and
minpair[L] = min over v,w >= L of W[v][w]. Both terms are valid relaxations because
repeats are permitted, so the cheapest candidate may be taken r times. Prune when
LB > T. With T set to the target this answers the decision question directly; with T
set to the best value found so far it returns the exact minimum.

VALIDATED against exhaustive enumeration at m=4 and m=5 before being trusted at m=11.
"""
import itertools, sys
import numpy as np


def exact_min(Wsub, m, T=None, node_cap=None):
    """Exact min of the pairwise sum over m-multisets of indices.
    T: prune anything exceeding T (None => +inf, returns the true minimum).
    Returns (best_cost, best_multiset, nodes, complete).
    `complete` is False only if node_cap stopped the search."""
    s = Wsub.shape[0]
    W = Wsub.astype(np.int64)
    # minpair[i] = min over v,w >= i of W[v][w]  (v == w allowed: a repeated vertex)
    minpair = np.empty(s + 1, dtype=np.int64)
    minpair[s] = 0
    run = np.iinfo(np.int64).max
    for i in range(s - 1, -1, -1):
        run = min(run, int(W[i, i:].min()))
        minpair[i] = run
    best = [np.inf if T is None else T + 1, None]
    nodes = [0]
    stopped = [False]
    tri = [c * (c - 1) // 2 for c in range(m + 1)]

    def rec(k, last, c, col, chosen):
        nodes[0] += 1
        if node_cap and nodes[0] > node_cap:
            stopped[0] = True
            return
        r = m - k
        if r == 0:
            if c < best[0]:
                best[0] = c
                best[1] = list(chosen)
            return
        tail = col[last:]
        lb = c + r * int(tail.min()) + tri[r] * int(minpair[last])
        if lb >= best[0]:
            return
        # order candidates by their immediate cost: cheapest first finds good
        # solutions early, which tightens the bound for everything after
        order = np.argsort(tail, kind="stable") + last
        for v in order:
            v = int(v)
            nc = c + int(col[v])
            if nc >= best[0]:
                continue
            r2 = r - 1
            if r2:
                lb2 = nc + r2 * int(min(col[v:].min(), col[v] + W[v, v])) + tri[r2] * int(minpair[v])
                if lb2 >= best[0]:
                    continue
            chosen.append(v)
            rec(k + 1, v, nc, col + W[v], chosen)
            chosen.pop()
            if stopped[0]:
                return

    rec(0, 0, 0, np.zeros(s, dtype=np.int64), [])
    return best[0], best[1], nodes[0], not stopped[0]


def brute(Wsub, m):
    s = Wsub.shape[0]
    bestc, bestm = None, None
    for comb in itertools.combinations_with_replacement(range(s), m):
        c = sum(int(Wsub[a][b]) for i, a in enumerate(comb) for b in comb[i + 1:])
        if bestc is None or c < bestc:
            bestc, bestm = c, comb
    return bestc, bestm


if __name__ == "__main__":
    rng = np.random.default_rng(5)
    print("=== validation: branch and bound vs exhaustive enumeration ===")
    bad = 0
    for trial in range(8):
        s = int(rng.integers(8, 16))
        A = rng.integers(0, 10, size=(s, s))
        Wt = np.minimum(A, A.T)              # symmetric, nonneg, nonzero diagonal allowed
        for m in (3, 4, 5):
            if s ** m > 3_000_000 and m == 5:
                continue
            b, bm, nodes, comp = exact_min(Wt, m)
            e, em = brute(Wt, m)
            agree = (b == e)
            bad += (not agree)
            print("  s=%2d m=%d  B&B %3d (%d nodes)  brute %3d  %s"
                  % (s, m, b, nodes, e, "ok" if agree else "*** MISMATCH ***"))
    print("mismatches: %d" % bad)
    sys.exit(1 if bad else 0)

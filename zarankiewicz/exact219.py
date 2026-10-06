#!/usr/bin/env python3
"""exact219.py -- EXACT decision: can a 7-point configuration's achievable rotations
carry an 11-multiset of antisum <= 219?

A plain branch and bound over 11-multisets does not finish: the generic lower bounds
collapse, because W[v][w] = 0 exactly when w = rev(v), so the zero-graph is a matching
and no cheap relaxation sees the tension between using a reverse-partner (free pairs)
and repeating it (9 per repeat).  Measured: both the minpair bound and a recursive DP
bound give 0 for 11 items, and a 3,000,000-node cap was hit without a verdict.

The fix is not a better generic bound -- it is the canonicalisation the SWEEP already
uses, which is why the sweep could enumerate 11-multisets over all 720 vertices at all:

  PREFIX-MINIMALITY.  Order the multiset so each new element's cost against the prefix
  is at least every earlier element's cumulative cost within the new set.  Every
  multiset admits such an order (repeatedly take the costliest element last), so the
  enumeration stays complete, and it collapses the m! orderings.

  THE STAIRCASE.  Summing over all size-k sub-multisets, each pair appears in
  C(m-2, k-2) of them, so a multiset of antisum <= T has a size-k sub-multiset of
  antisum <= C(9,k-2)*T/C(11,k).  Under prefix-minimality the k-prefix IS such a
  sub-multiset, so its cost is bounded rung by rung.  This is search.c's staircase(),
  reused here with top = 219.

The symmetry reductions the sweep also uses -- a_1 = vertex 0 and lex-minimality under
Stab(0) -- are NOT available here, because the achievable set S is not closed under the
group.  Dropping them only means a multiset may be visited under several orderings;
completeness is unaffected.

VERDICT per configuration: either an 11-multiset of antisum <= 219 is EXHIBITED, or the
tree is exhausted and none exists -- a proof for that configuration, not a sampling
statement.
"""
import random, sys, time
sys.path.insert(0, "intake")
import numpy as np
from cog import CO
import realise219 as R
from zpredict import staircase


def decide(Wfull, S, T=219, m=11, node_cap=None):
    """Is there an m-multiset from S with antisum <= T?
    Returns (found_multiset_or_None, nodes, complete)."""
    B = staircase(m, 7, T)
    s = len(S)
    Wl = [[int(Wfull[a][b]) for b in S] for a in S]      # |S| x |S|, local indices
    nodes = [0]
    stopped = [False]
    found = [None]

    def rec(chosen, co, tot):
        nodes[0] += 1
        if node_cap and nodes[0] > node_cap:
            stopped[0] = True
            return True
        k = len(chosen)
        if k == m:
            found[0] = [S[i] for i in chosen]
            return True
        lim = B[k + 1]
        mx = max(co)
        for v in range(s):
            row = Wl[v]
            cv = 0
            for i in chosen:
                cv += row[i]
            if tot + cv > lim or cv < mx:
                continue
            nc = [co[t] + row[chosen[t]] for t in range(k)]
            if nc and max(nc) > cv:
                continue
            if rec(chosen + [v], nc + [cv], tot + cv):
                return True
        return False

    for v0 in range(s):
        if rec([v0], [0], 0):
            break
        if stopped[0]:
            break
    return found[0], nodes[0], not stopped[0]


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 219
    C = CO(7); D = C.dist_matrix(); W = np.asarray(C.antidist_matrix(D))
    print("staircase for top=%d: %s" % (T, [staircase(11, 7, T)[k] for k in range(11, 1, -1)]))
    print("EXACT decision per configuration: any 11-multiset of antisum <= %d?\n" % T)
    rng = random.Random(777)
    t0 = time.time()
    hits = incomplete = 0
    nodes_tot = 0
    for t in range(trials):
        Q = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
        S = sorted(R.achievable(Q, C, rng=rng))
        ms, nodes, comp = decide(W, S, T=T, node_cap=20_000_000)
        nodes_tot += nodes
        if not comp:
            incomplete += 1
            print("  config %3d |S|=%2d  NODE CAP -- inconclusive" % (t, len(S)))
        elif ms is not None:
            hits += 1
            asum = int(sum(W[a][b] for i, a in enumerate(ms) for b in ms[i + 1:]))
            print("  config %3d |S|=%2d  *** FOUND antisum %d: %s ***" % (t, len(S), asum, ms))
        elif t < 5 or (t + 1) % 10 == 0:
            print("  config %3d |S|=%2d  PROVED none <= %d  (%d nodes)" % (t, len(S), T, nodes))
    print("\n=== %d configurations, %.0fs, %d nodes total ===" % (trials, time.time() - t0, nodes_tot))
    print("configurations admitting antisum <= %d : %d" % (T, hits))
    print("configurations PROVED to admit none    : %d" % (trials - hits - incomplete))
    print("inconclusive (node cap)                : %d" % incomplete)
    return 0


if __name__ == "__main__":
    sys.exit(main())

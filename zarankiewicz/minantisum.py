#!/usr/bin/env python3
"""minantisum.py -- a LOWER BOUND on the rectilinear crossing number of K_{11,7},
computed from geometry rather than from the relaxation.

THE CHAIN.  For a straight-line K_{11,7} with 7 points Q and 11 points P, each P
point's view of Q is a CO_7 vertex, and

    cr(drawing)  >=  antisum(multiset of the 11 rotations)        [Woodall's bound]
                 >=  min { antisum(M) : M an 11-multiset of rotations ACHIEVABLE from Q }

The second line is the point.  The sweep minimised the antisum over all (11,7)-sets
the STAIRCASE allows and got 219, below Z(11)Z(7) = 225 -- but most of those sets
correspond to no drawing at all.  Minimising instead over the multisets a real
7-point configuration can actually induce replaces "what the relaxation permits"
with "what geometry permits", and the result bounds the crossing number from below
for that configuration.

ACHIEVABLE SET.  The rotations a point can realise relative to a fixed Q are the
cells of the arrangement of Q's C(7,2) = 21 connecting lines.  Those lines are not
in general position -- the 6 lines at each Q_i are concurrent -- so the cell count
is 1 + 21 + (7*5 + 105) = 162, and the distinct rotations number fewer still,
measured at 71 to 96.  realise219.achievable() enumerates them by probing a ring
around every line-line intersection plus the far field; it converges under 8x ring
and 10x fill refinement, and contains every rotation of 10 of 10 certified
pair-optimal drawings it was tested against.

MULTIPLICITY IS FREE.  Cells are open and of positive area, so a rotation achievable
at all is achievable by any number of P points; the minimisation allows repeats.

WHAT THIS IS NOT.  The minimisation over multisets is a heuristic (greedy plus local
search from many starts), so each configuration's figure is an UPPER bound on that
configuration's true minimum -- which is the safe direction: it can only understate
the lower bound on crossings. And the configurations are sampled, so a figure holding
across all of them is evidence about rectilinear drawings, not a proof, and says
nothing about drawings with curved edges.
"""
import random, sys, time
sys.path.insert(0, "intake")
import numpy as np
from cog import CO
import realise219 as R

M_SIDE = 11


def min_antisum(S, W, m=M_SIDE, restarts=40, rng=None):
    """Heuristic minimum of sum_{i<j} W[a_i][a_j] over m-multisets from S."""
    rng = rng or random.Random(0)
    S = list(S)
    k = len(S)
    sub = W[np.ix_(S, S)].astype(np.int64)
    best = None
    for r in range(restarts):
        if r == 0:
            cur = [int(np.argmin(sub.sum(axis=1)))]
        else:
            cur = [rng.randrange(k)]
        while len(cur) < m:                       # greedy: cheapest addition
            cost = sub[:, cur].sum(axis=1)
            cur.append(int(np.argmin(cost)))
        improved = True
        while improved:                           # local search: one-element swaps
            improved = False
            for i in range(m):
                others = cur[:i] + cur[i + 1:]
                cost = sub[:, others].sum(axis=1)
                j = int(np.argmin(cost))
                if cost[j] < cost[cur[i]]:
                    cur[i] = j
                    improved = True
        tot = int(sum(sub[a][b] for i, a in enumerate(cur) for b in cur[i + 1:]))
        if best is None or tot < best[0]:
            best = (tot, [S[i] for i in cur])
    return best


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    t0 = time.time()
    C = CO(7); D = C.dist_matrix(); W = np.asarray(C.antidist_matrix(D))
    print("Z(11)Z(7) = 225.  The sweep's relaxed minimum over staircase-legal sets: 219.")
    print("Below: the minimum achievable from real 7-point configurations.\n")
    rng = random.Random(2024)
    best = None
    vals = []
    for t in range(trials):
        Q = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
        S = sorted(R.achievable(Q, C, rng=rng))
        tot, ms = min_antisum(S, W, rng=rng)
        vals.append(tot)
        if best is None or tot < best[0]:
            best = (tot, t, ms, len(S))
            print("  config %4d: |achievable|=%2d  NEW BEST min antisum %d" % (t, len(S), tot))
        elif (t + 1) % 50 == 0:
            print("  config %4d: |achievable|=%2d  min antisum %d   (best so far %d)"
                  % (t, len(S), tot, best[0]))
    vals = np.array(vals)
    print("\n=== %d configurations in %.0fs ===" % (trials, time.time() - t0))
    print("min antisum achievable: best %d, median %d, worst %d"
          % (vals.min(), int(np.median(vals)), vals.max()))
    print("lowest found, configuration %d (|achievable|=%d): %s" % (best[1], best[3], best[2]))
    print()
    print("Z(11)Z(7) = 225; the relaxation's floor was 219.")
    if vals.min() >= 225:
        print("EVERY configuration tried bounds crossings at or above 225, so none of them")
        print("admits a drawing beating Zarankiewicz, and the 219 class is not reachable")
        print("from any of them.")
    else:
        print("A configuration bounds crossings BELOW 225 (at %d) -- that is a candidate" % vals.min())
        print("worth pursuing: it needs the drawing built and its crossings counted directly,")
        print("since the antisum is only a lower bound.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

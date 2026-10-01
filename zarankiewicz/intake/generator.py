"""generator.py -- the CERTIFIED GENERATOR: the external ground truth the checkers
are validated against.

A straight-line drawing of K_{m,n} in general position is a good drawing.  If every
one of its C(m,2) K_{2,n} sub-drawings attains EXACTLY its antidistance ("pair-optimal"),
the induced (m,n)-set is tight and pseudo-tight.  This gives unlimited certified
POSITIVES, independent of any checker.

Pair-optimality is required.  An earlier version of this control used all random
drawings and failed 6/180 -- the control was wrong, not the checker: tightness
quantifies over SHORTEST antipaths, so a drawing exceeding an antidistance on some
pair need not induce a tight set.  36 of 1,262 non-pair-optimal drawings do induce
non-tight sets, exactly as the corrected statement predicts.

MEASURED REACH.  All-pair-optimality decays as (single-pair rate)^C(m,2) with the
single-pair rate ~0.4045: 7.1e-3 at m=4, 4.1e-4 at m=5, 3.1e-5 at m=6, 0 in 20,586
trials at m=7, ~2.4e-22 at m=11.  So the generator certifies small sets only.
That is not a limitation for the (11,7) search: a certified generator produces
certified POSITIVES, and "no counterexample exists" is a negative.  What it
certifies is the FILTERS, which act on (4,n)-subsets, which is where it works.
"""
import random
from itertools import combinations
from math import atan2
from cog import canon


def _sgn(x):
    return (x > 0) - (x < 0)


def _orient(o, a, b):
    return _sgn((a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]))


def crosses(p1, p2, q1, q2):
    d1, d2 = _orient(q1, q2, p1), _orient(q1, q2, p2)
    d3, d4 = _orient(p1, p2, q1), _orient(p1, p2, q2)
    return d1 * d2 < 0 and d3 * d4 < 0


def rotation(p, pts, Gn):
    """Clockwise cyclic order of pts as seen from p, as a CO_n vertex index."""
    ang = sorted(range(len(pts)), key=lambda i: -atan2(pts[i][1] - p[1], pts[i][0] - p[0]))
    return Gn.idx[canon(tuple(ang))]


def pair_crossings(P, Q, i, j):
    """Crossings between arcs P_i--Q_x--P_j and P_i--Q_y--P_j, summed over pairs."""
    n = len(Q)
    return sum(1 for x, y in combinations(range(n), 2)
               if crosses(P[i], Q[x], Q[y], P[j]) or crosses(Q[x], P[j], P[i], Q[y]))


def total_crossings(P, Q):
    """Crossings of the straight-line K_{m,n}, by direct segment intersection."""
    m, n = len(P), len(Q)
    c = 0
    E = [(a, i) for a in range(m) for i in range(n)]
    for u in range(len(E)):
        a, i = E[u]
        for v in range(u + 1, len(E)):
            b, j = E[v]
            if a == b or i == j:
                continue
            if crosses(P[a], Q[i], P[b], Q[j]):
                c += 1
    return c


def pair_optimal_sets(Gn, A, m, want, seed=0, time_cap=60.0):
    """Yield (m,n)-sets certified TIGHT: induced by pair-optimal straight-line drawings."""
    import time
    rng = random.Random(seed)
    out = []
    t0 = time.time()
    n = Gn.n
    while len(out) < want and time.time() - t0 < time_cap:
        P = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(m)]
        Q = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        M = [rotation(p, Q, Gn) for p in P]
        if len(set(M)) < m:
            continue
        if all(pair_crossings(P, Q, i, j) == A[M[i]][M[j]] for i, j in combinations(range(m), 2)):
            out.append((tuple(M), P, Q))
    return out


def realise(Gn, target, seed=0, tries=400, samples=1500):
    """Find a straight-line drawing inducing an isomorphic copy of `target`.
    Returns (P_n_points, positions_for_target, image) or None."""
    rng = random.Random(seed)
    maps = Gn.relabel_maps()
    n = Gn.n
    for _ in range(tries):
        Pn = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        R = {}
        for _ in range(samples):
            p = (rng.uniform(-1.7, 1.7), rng.uniform(-1.7, 1.7))
            r = rotation(p, Pn, Gn)
            R.setdefault(r, p)
        for mm in maps:
            img = [mm[v] for v in target]
            if all(v in R for v in img):
                return Pn, [R[v] for v in img], img
    return None

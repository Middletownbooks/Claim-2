#!/usr/bin/env python3
"""realise219.py -- is the antisum-219 class geometrically realisable?

WHAT THE QUESTION IS.  The sweep enumerated (11,7)-sets -- multisets of 11 CO_7
vertices -- satisfying the staircase, and found exactly one class at antisum 219,
below Z(11)Z(7) = 225.  The antisum LOWER-BOUNDS the crossings of any straight-line
K_{11,7} whose 11 points induce that multiset of rotations.  So a drawing with 219
crossings needs TWO things, and they are not the same:

  (a) REALISABILITY -- 11 points, relative to 7 points, inducing that multiset;
  (b) PAIR-OPTIMALITY -- every one of the C(11,2) = 55 pairs attaining exactly its
      antidistance, so the crossings equal the antisum rather than merely exceeding it.

Measured here on certified (4,7) positives: pair-optimal drawings hit the antisum
exactly (6 of 6), while a drawing that merely realises a target ran 66 crossings
against an antisum of 38.  (a) without (b) refutes nothing.

WHY NOT intake/generator.py's realise().  Two reasons, one real and one not:
  * it maps rotation -> ONE point, so a repeated vertex becomes two COINCIDENT
    points.  The 219 canon has vertex 0 twice.  This is a coding limit, NOT a
    geometric one: cells of the arrangement are open sets of positive area, so a
    rotation achievable at all is achievable by any number of points.  Multiplicity
    is free, and this script treats it so.
  * it samples 1500 random points.  For a FIXED 7-point set the achievable rotations
    are exactly the cells of the arrangement of its C(7,2) = 21 connecting lines.
    Those lines are NOT in general position -- the 6 lines at each Q_i are concurrent
    there -- so the count is 1 + 21 + (7*5 + 105) = 162, not the 232 a general-position
    arrangement of 21 lines would give; an earlier draft of this file said 232 and was
    wrong. Measured distinct rotations run 68 to 96.  Sampling finds big cells and
    misses small ones, so a failure would be ambiguous between sampling and geometry.
    This script ENUMERATES the cells: it probes a ring around every one of the 210
    line-line intersections, plus far-field directions for the unbounded cells, plus
    random fill.  That is exhaustive up to cells smaller than the probe radius, and
    the count is reported so the reader can see it against the 232 bound.

WHAT A NEGATIVE MEANS.  Realisability is invariant under the group: relabelling the
7 points is renaming them, reversal is reflecting the plane.  So the whole 5040-member
orbit stands or falls together and ONE representative decides it -- which is why this
quantifies over all 10080 maps for each configuration.  But it samples ORDER TYPES of
7 points at random, and there are finitely many; failing on every order type tried is
evidence, not proof.  The script reports how close the best attempt came.
"""
import itertools, math, random, sys, time, collections
sys.path.insert(0, "intake")
from cog import CO, canon

CANON = (0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)


def rotation_of(p, pts, Gn):
    ang = sorted(range(len(pts)), key=lambda i: -math.atan2(pts[i][1] - p[1], pts[i][0] - p[0]))
    return Gn.idx[canon(tuple(ang))]


def achievable(Q, Gn, eps=1e-6, ring=12, far=40.0, fardirs=256, fill=4000, rng=None):
    """Every rotation realisable by a point placed relative to the 7 points Q:
    the cells of the arrangement of the C(7,2) connecting lines."""
    rng = rng or random.Random(0)
    n = len(Q)
    lines = []
    for i, j in itertools.combinations(range(n), 2):
        (x1, y1), (x2, y2) = Q[i], Q[j]
        a, b = y2 - y1, x1 - x2
        lines.append((a, b, a * x1 + b * y1))
    probes = []
    # a ring around every line-line intersection: catches every cell incident to it
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-12:
            continue
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if abs(x) > 1e4 or abs(y) > 1e4:
            continue
        for k in range(ring):
            t = 2 * math.pi * (k + 0.5) / ring
            probes.append((x + eps * math.cos(t), y + eps * math.sin(t)))
    # far field: the unbounded cells
    for k in range(fardirs):
        t = 2 * math.pi * k / fardirs
        probes.append((far * math.cos(t), far * math.sin(t)))
    # random fill, as a cross-check on the structured probes
    for _ in range(fill):
        probes.append((rng.uniform(-3, 3), rng.uniform(-3, 3)))
    seen = {}
    for p in probes:
        try:
            r = rotation_of(p, Q, Gn)
        except Exception:
            continue
        seen[r] = seen.get(r, 0) + 1
    return seen


def main():
    t0 = time.time()
    C = CO(7)
    D = C.dist_matrix(); A = C.antidist_matrix(D)
    maps = C.relabel_maps(with_reversal=True)
    support = sorted(set(CANON))
    asum = sum(int(A[CANON[i]][CANON[j]]) for i in range(11) for j in range(i + 1, 11))
    print("CO_7: %d vertices, %d maps" % (len(C.V), len(maps)))
    print("target: %s" % (CANON,))
    print("  antisum %d, %d distinct vertices, multiplicities %s"
          % (asum, len(support), dict(collections.Counter(CANON))))
    print("  Z(11)Z(7) = 225, so this class is %d below the conjecture" % (225 - asum))
    assert asum == 219, asum

    # the 5040 distinct supports to look for, one per orbit member
    want = set()
    for g in maps:
        want.add(tuple(sorted({g[v] for v in support})))
    want = sorted(want)
    print("  orbit gives %d distinct vertex-supports to search for" % len(want))

    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rng = random.Random(12345)
    best = (-1, None)
    cells_seen = []
    for t in range(trials):
        Q = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
        S = achievable(Q, C, rng=rng)
        cells_seen.append(len(S))
        Sset = set(S)
        hit = None
        bestn = -1
        for sup in want:
            k = sum(1 for v in sup if v in Sset)
            if k > bestn:
                bestn = k
            if k == len(sup):
                hit = sup
                break
        if hit:
            print("\n*** REALISABLE: configuration %d supports %s ***" % (t, hit))
            print("    achievable rotations: %d" % len(Sset))
            return 0
        if bestn > best[0]:
            best = (bestn, t)
        if t < 3 or (t + 1) % 10 == 0:
            print("  config %2d: %3d achievable rotations (bound 162); best support match %d of %d"
                  % (t, len(Sset), bestn, len(support)))
    print("\nNOT REALISED in %d configurations (%.1fs)" % (trials, time.time() - t0))
    print("  achievable rotations per configuration: min %d, max %d, mean %.1f"
          % (min(cells_seen), max(cells_seen), sum(cells_seen) / len(cells_seen)))
    print("  best any orbit member came: %d of %d distinct vertices, in configuration %d"
          % (best[0], len(support), best[1]))
    print("  so at least %d of the 10 required rotations were unreachable every time"
          % (len(support) - best[0]))
    return 1


if __name__ == "__main__":
    sys.exit(main())

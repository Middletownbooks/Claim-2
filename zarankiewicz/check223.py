#!/usr/bin/env python3
"""check223.py -- build the drawing minantisum.py flagged and COUNT its crossings.

minantisum.py found a 7-point configuration whose achievable rotations admit an
11-multiset of antisum 223, below Z(11)Z(7) = 225.  The antisum only bounds
crossings from BELOW, so this is a candidate and nothing more.  The decisive step is
to place the 11 points, count the crossings of the actual straight-line drawing with
generator.total_crossings, and compare.

Three outcomes:
  crossings  > 223  the bound is not attained; the candidate dissolves, and the gap
                    measures how far the relaxation sits from geometry.
  crossings == 223  a rectilinear K_{11,7} with fewer than 225 crossings. That would
                    contradict Zarankiewicz and MUST NOT be announced on one run: it
                    would need the drawing dumped, re-counted independently, and
                    checked for degeneracy before it meant anything.
  crossings  < 223  impossible if Woodall's bound and this code are both right, so it
                    would mean a bug here.
"""
import itertools, math, random, sys
sys.path.insert(0, "intake")
import numpy as np
from cog import CO
import generator as G
import realise219 as R
import minantisum as MA

TARGET_TRIAL = 60


def achievable_points(Q, Gn, rng):
    """rotation -> list of distinct points realising it."""
    pts = {}
    lines = []
    n = len(Q)
    for i, j in itertools.combinations(range(n), 2):
        (x1, y1), (x2, y2) = Q[i], Q[j]
        a, b = y2 - y1, x1 - x2
        lines.append((a, b, a * x1 + b * y1))
    probes = []
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-12:
            continue
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if abs(x) > 1e4 or abs(y) > 1e4:
            continue
        for k in range(24):
            t = 2 * math.pi * (k + 0.5) / 24
            for e in (1e-4, 1e-3, 1e-2):
                probes.append((x + e * math.cos(t), y + e * math.sin(t)))
    for k in range(256):
        t = 2 * math.pi * k / 256
        for far in (5.0, 40.0):
            probes.append((far * math.cos(t), far * math.sin(t)))
    for _ in range(60000):
        probes.append((rng.uniform(-3, 3), rng.uniform(-3, 3)))
    for p in probes:
        try:
            r = R.rotation_of(p, Q, Gn)
        except Exception:
            continue
        pts.setdefault(r, []).append(p)
    return pts


def main():
    C = CO(7); D = C.dist_matrix(); W = np.asarray(C.antidist_matrix(D))

    # replay minantisum.py's stream exactly to recover configuration 60
    rng = random.Random(2024)
    Q = None; target = None; tot = None
    for t in range(TARGET_TRIAL + 1):
        Qt = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
        S = sorted(R.achievable(Qt, C, rng=rng))
        got, ms = MA.min_antisum(S, W, rng=rng)
        if t == TARGET_TRIAL:
            Q, target, tot = Qt, ms, got
    print("configuration %d recovered; min antisum %d; multiset %s" % (TARGET_TRIAL, tot, target))
    asum = int(sum(W[a][b] for i, a in enumerate(target) for b in target[i + 1:]))
    print("antisum recomputed from the multiset: %d" % asum)
    assert asum == tot == 223, (asum, tot)

    pr = random.Random(7)
    pts = achievable_points(Q, C, pr)
    need = {}
    for v in target:
        need[v] = need.get(v, 0) + 1
    print("\ndistinct rotations needed and points found for each:")
    P = []
    for v, k in sorted(need.items()):
        have = pts.get(v, [])
        print("  rotation %3d x%d : %d candidate points" % (v, k, len(have)))
        if len(have) < k:
            print("    *** cannot place %d distinct points in this cell from the probe set ***" % k)
            return 2
        # spread the choices out so the points are not nearly coincident
        chosen = [have[0]]
        for p in have[1:]:
            if len(chosen) >= k:
                break
            if all((p[0]-c[0])**2 + (p[1]-c[1])**2 > 1e-8 for c in chosen):
                chosen.append(p)
        if len(chosen) < k:
            print("    *** only %d well-separated points available ***" % len(chosen))
            return 2
        P.extend(chosen)

    # every placed point must actually induce the rotation it was chosen for
    induced = [R.rotation_of(p, Q, C) for p in P]
    want = sorted(target); got = sorted(induced)
    print("\ninduced multiset matches target: %s" % (want == got))
    if want != got:
        print("  wanted %s\n  got    %s" % (want, got))
        return 2

    # degeneracy checks: distinct points, no coincidence with Q, general position
    allp = P + list(Q)
    mind = min(math.dist(a, b) for a, b in itertools.combinations(allp, 2))
    print("minimum distance between any two of the 18 points: %.3g" % mind)
    cr = G.total_crossings(P, Q)
    print("\n=== RESULT ===")
    print("antisum (lower bound on crossings): %d" % asum)
    print("ACTUAL crossings of the drawing:    %d" % cr)
    print("Z(11)Z(7):                          225")
    if cr > asum:
        print("\nThe bound is NOT attained: the drawing exceeds its antisum by %d." % (cr - asum))
        print("The candidate dissolves. %d >= 225, so this drawing does not beat Zarankiewicz."
              % cr if cr >= 225 else
              "\nBut %d is still BELOW 225 -- that needs independent re-counting." % cr)
    elif cr == asum:
        print("\nThe bound IS attained, at %d < 225. Do not announce this from one run." % cr)
    else:
        print("\ncrossings below the antisum is impossible -- there is a bug here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

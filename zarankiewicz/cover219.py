#!/usr/bin/env python3
"""cover219.py -- the EXACT 219 decision, pushed along the axis that actually limits it.

The sweep proved that nothing exists below antisum 219 and that the 219 sets form
exactly one orbit of 5040 multisets. Therefore, for a 7-point configuration with
achievable rotation set S,

    some 11-multiset from S has antisum <= 219
      <=>  some member of the 5040-orbit has all 10 of its distinct vertices in S

which is an instant, EXACT test. Branch and bound is unnecessary for this threshold --
the enumeration already did the hard part.

THE COVERAGE ROUTE TO A PROOF IS CLOSED, measured not assumed. S is the set of cells of
the arrangement of the 21 connecting lines, and I expected that to be fixed by the ORDER
TYPE of the 7 points -- of which there are only 135 -- so that enumerating order types
would upgrade sampling to proof. It is not: across 160 configurations covering 48 order
types, 30 of the 33 order types seen more than once gave DIFFERENT achievable-set sizes.
The chirotope fixes which side of each line every point lies on, but not where those
lines cross each other away from the points, and the cells depend on the latter. So
there is no small finite family here to exhaust.

WHAT THIS SCRIPT DOES INSTEAD. It runs the exact test on many configurations and records
the distribution of the BEST support match -- how many of the 10 required vertices the
luckiest orbit member achieves. Rarity and obstruction look different: if matches were
merely rare we would see 8s and 9s in proportion, whereas a hard ceiling below 10 is
evidence that the 219 class is structurally unreachable rather than just improbable.
"""
import collections, random, sys, time
sys.path.insert(0, "intake")
import numpy as np
from cog import CO
import realise219 as R

CANON = (0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    C = CO(7); D = C.dist_matrix(); W = np.asarray(C.antidist_matrix(D))
    maps = C.relabel_maps(with_reversal=True)
    support = sorted(set(CANON))
    orbit = sorted({tuple(sorted({g[v] for v in support})) for g in maps})
    print("219 orbit: %d distinct vertex-supports, each of %d vertices"
          % (len(orbit), len(support)))
    print("exact test per configuration: is any of them a subset of the achievable set?\n")

    rng = random.Random(20261006)
    hist = collections.Counter()
    curve = []
    t0 = time.time()
    hit = None
    best = (-1, None)
    for t in range(N):
        Q = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
        S = R.achievable(Q, C, rng=rng)
        Sset = set(S)
        Sl = sorted(Sset)
        bestn = -1
        for sup in orbit:
            k = sum(1 for v in sup if v in Sset)
            if k > bestn:
                bestn = k
            if k == len(sup):
                hit = (t, sup, Sl)
                break
        hist[bestn] += 1
        if bestn > best[0]:
            best = (bestn, t)
        if hit:
            break
        if (t + 1) % 5000 == 0:
            print("  %6d configs, best-match histogram %s, ceiling %d of %d, %.0fs"
                  % (t + 1, dict(sorted(hist.items())), best[0], len(support), time.time() - t0))

    print()
    if hit:
        t, sup, Sl = hit
        print("*** REALISABLE: configuration %d admits support %s ***" % (t, list(sup)))
        print("    This is a 219-antisum multiset over genuinely achievable rotations.")
        print("    It still needs its drawing built and crossings counted: the antisum is")
        print("    a LOWER bound, and the one such drawing measured so far ran 81 over.")
        return 0
    print("=== %d configurations in %.0fs: NO configuration admits the 219 class ===" % (N, time.time() - t0))
    print("best-match histogram (vertices achieved by the luckiest orbit member):")
    for k in sorted(hist):
        print("   %2d of 10 : %7d configurations (%.3f%%)" % (k, hist[k], 100.0 * hist[k] / N))
    print("ceiling reached: %d of %d" % (best[0], len(support)))
    print()
    print("Each verdict is EXACT for its configuration. It is NOT a proof: the achievable")
    print("set is not an order-type invariant, so there is no finite family to exhaust, and")
    print("none of this speaks to drawings with curved edges.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

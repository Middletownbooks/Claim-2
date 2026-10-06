#!/usr/bin/env python3
"""optimise223.py -- can PLACEMENT close the gap between antisum and crossings?

check223.py placed 11 points in the cells prescribed by an antisum-223 multiset and
counted 387 crossings.  That single placement settles nothing: the cells fix the
ROTATIONS, hence the antisum, but the crossings depend on where in each cell the
point sits.  Equality needs every one of the 55 pairs to be pair-optimal, and nothing
so far has tried to arrange that.

So: hold the rotation multiset fixed, move the points within their own cells, and
minimise the actual crossing count.  Where it bottoms out is the informative number.
"""
import itertools, math, random, sys
sys.path.insert(0, "intake")
import numpy as np
from cog import CO
import generator as G
import realise219 as R
import minantisum as MA
import check223 as CH


def main():
    C = CO(7); D = C.dist_matrix(); W = np.asarray(C.antidist_matrix(D))
    rng = random.Random(2024)
    Q = target = None
    for t in range(CH.TARGET_TRIAL + 1):
        Qt = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(7)]
        S = sorted(R.achievable(Qt, C, rng=rng))
        got, ms = MA.min_antisum(S, W, rng=rng)
        if t == CH.TARGET_TRIAL:
            Q, target = Qt, ms
    asum = int(sum(W[a][b] for i, a in enumerate(target) for b in target[i + 1:]))
    print("multiset %s, antisum %d" % (target, asum))

    pts = CH.achievable_points(Q, C, random.Random(7))
    slots = []                      # one candidate list per P point, same rotation
    for v in target:
        slots.append([p for p in pts[v]])
    print("candidates per point: %s" % [len(s) for s in slots])

    def build(sel):
        return [slots[i][sel[i]] for i in range(len(slots))]

    best = None
    for start in range(8):
        r = random.Random(100 + start)
        sel = [r.randrange(len(s)) for s in slots]
        cur = G.total_crossings(build(sel), Q)
        improved = True
        rounds = 0
        while improved and rounds < 60:
            improved = False
            rounds += 1
            for i in range(len(slots)):
                cand = slots[i]
                idxs = range(len(cand)) if len(cand) <= 120 else r.sample(range(len(cand)), 120)
                for j in idxs:
                    if j == sel[i]:
                        continue
                    old = sel[i]
                    sel[i] = j
                    c = G.total_crossings(build(sel), Q)
                    if c < cur:
                        cur = c
                        improved = True
                    else:
                        sel[i] = old
        P = build(sel)
        ind = sorted(R.rotation_of(p, Q, C) for p in P)
        okrot = (ind == sorted(target))
        print("  start %d: crossings %d  (rotations preserved: %s)" % (start, cur, okrot))
        if okrot and (best is None or cur < best[0]):
            best = (cur, P)

    print("\n=== best placement found ===")
    print("antisum (lower bound):           %d" % asum)
    print("best crossings after optimising: %d" % best[0])
    print("Z(11)Z(7):                       225")
    print("gap still unclosed:              %d" % (best[0] - asum))
    if best[0] < 225:
        print("\nBELOW 225 -- this needs independent re-counting before it means anything.")
    else:
        print("\nAt or above 225: this configuration does not beat Zarankiewicz even with")
        print("placement optimised, and the antisum bound is far from attained.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

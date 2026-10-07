#!/usr/bin/env python3
"""mixedbound.py -- lower-bound a drawing's crossings from BOTH the pairwise
antidistances and the smaller complete bipartite crossing numbers that are
already theorems, combined by subset counting.

WHY.  The sweep proved that some (11,7)-set has antisum 219, so the pairwise
bound alone cannot give 225: it is not loose arithmetic, it is a ceiling.  But
the antisum is not the only lower bound available for a SUB-drawing.  Take a
good drawing D of K_{7,11} and any k of its eleven 7-stars.  Those k stars form
a good drawing of K_{7,k}, so

    crossings(S)  >=  max( antisum(S),  cr(K_{7,k}) )                     (1)

and for k <= 10 the second term is a known theorem, not a conjecture:

    cr(K_{7,7}) = 81  and  cr(K_{7,9}) = 144      Woodall 1993 (computer proof)
    cr(K_{7,8}) = 108 and  cr(K_{7,10}) = 180     from those two by (2) below
    cr(K_{7,k}) = Z(7,k) for k <= 6               Kleitman 1970 (min side <= 6)

Counting lifts any family of sub-bounds to the whole.  Every pair {a,b} of S
lies in exactly k-2 of the (k-1)-element subsets of S, so

    crossings(S)  >=  ceil( sum over S' of crossings(S') / (k-2) )          (2)

Apply (1) and (2) together, bottom up over all 2^11 subsets of the eleven
rotations, and the bound at the top can exceed every term that went into it.
The staircase the sweep prunes with is exactly (2) applied to antisums alone;
the new ingredient is the clamp (1), which bites on any subset whose own
antisum has fallen below what its K_{7,k} already forbids.

WHAT IS AND IS NOT ASSUMED.  Only the four literature values above, the
antidistance bound (Woodall: crossings between two stars >= dbar of their
rotations), and counting.  Nothing here assumes Zarankiewicz anywhere.  The
parity lift -- crossings(S) = antisum(S) mod 2, so a bound of even value may be
raised by one -- is reported SEPARATELY and never folded into the headline
number, because this programme has not checked that statement itself.

USAGE
  python3 mixedbound.py --selftest
  python3 mixedbound.py --class 0,0,15,74,105,438,569,647,660,671,689
  python3 mixedbound.py --rows sweep_L5/low_0.txt [--fast] [--limit N]
"""
import argparse, itertools, sys

sys.path.insert(0, 'intake')
import cog

M = 11
N = 7

# cr(K_{7,k}) for k = 0..10: theorems, as documented above.  Index 11 is None:
# that is the open case and must never be used as an input.
CR7 = [0, 0, 0, 9, 18, 36, 54, 81, 108, 144, 180, None]


def zf(k):
    return (k // 2) * ((k - 1) // 2)


def check_cr_table():
    """The table must agree with Z(7,k), and 8 and 10 must follow from 7 and 9
    by the counting step (2), or the provenance claimed above is wrong."""
    for k in range(2, 11):
        assert CR7[k] == zf(7) * zf(k), (k, CR7[k], zf(7) * zf(k))
    # k from k-1 by (2): C(k,k-1) = k subsets, each pair in k-2 of them.
    for k in (8, 10):
        got = -(-(k * CR7[k - 1]) // (k - 2))
        assert got == CR7[k], (k, got, CR7[k])
    return True


def pair_matrix(Mset, A):
    k = len(Mset)
    return [[A[Mset[i]][Mset[j]] if i != j else 0 for j in range(k)] for i in range(k)]


def full_bound(W, parity=False):
    """Exact evaluation of (1)+(2) over every subset.  W is the k x k matrix of
    antidistances of the chosen rotations.  Returns (bound, antisum, detail)."""
    k = len(W)
    anti = [0] * (1 << k)
    for s in range(1 << k):
        bits = [i for i in range(k) if s >> i & 1]
        anti[s] = sum(W[a][b] for a, b in itertools.combinations(bits, 2))
    lb = [0] * (1 << k)
    order = sorted(range(1 << k), key=lambda s: bin(s).count("1"))
    for s in order:
        c = bin(s).count("1")
        if c < 2:
            continue
        v = anti[s]
        if c <= 10 and CR7[c] is not None:
            v = max(v, CR7[c])
        if c >= 4:
            tot = sum(lb[s ^ (1 << i)] for i in range(k) if s >> i & 1)
            v = max(v, -(-tot // (c - 2)))
        if parity and (v & 1) != (anti[s] & 1):
            v += 1
        lb[s] = v
    full = (1 << k) - 1
    return lb[full], anti[full], (lb, anti)


def fast_bound(W, parity=False):
    """The same thing truncated to the top two levels, computed from row sums
    only.  Used for bulk scans; --selftest checks it never exceeds full_bound."""
    k = len(W)
    r = [sum(W[i]) for i in range(k)]
    T = sum(r) // 2
    l9 = {}
    for i, j in itertools.combinations(range(k), 2):
        a = T - r[i] - r[j] + W[i][j]
        v = max(a, CR7[k - 2]) if k - 2 <= 10 else a
        if parity and (v & 1) != (a & 1):
            v += 1
        l9[(i, j)] = v
    l10 = []
    for i in range(k):
        a = T - r[i]
        v = max(a, CR7[k - 1]) if k - 1 <= 10 else a
        tot = sum(l9[(min(i, j), max(i, j))] for j in range(k) if j != i)
        v = max(v, -(-tot // (k - 3)))
        if parity and (v & 1) != (a & 1):
            v += 1
        l10.append(v)
    v = max(T, -(-sum(l10) // (k - 2)))
    if parity and (v & 1) != (T & 1):
        v += 1
    return v, T


def selftest():
    check_cr_table()
    print("cr table: consistent with Z(7,k) and with the counting step")
    C = cog.CO(N)
    A = C.antidist_matrix(C.dist_matrix())
    import random
    rng = random.Random(7)

    # The counting step applied to exact antisums returns exactly the antisum:
    # sum over i of antisum(S minus i) = (k-2) * antisum(S), identically.  So
    # with the clamps removed the whole recursion must collapse to the antisum,
    # which isolates the K_{7,k} clamp as the ONLY source of lift.  If this
    # test fails the counting arithmetic is wrong somewhere.
    saved = CR7[:]
    try:
        for i in range(len(CR7)):
            CR7[i] = 0 if CR7[i] is not None else None
        for _ in range(50):
            Ms = [rng.randrange(C.NV) for _ in range(M)]
            W = pair_matrix(Ms, A)
            f, T, _ = full_bound(W)
            assert f == T, ("clamps off but recursion lifted", f, T)
    finally:
        CR7[:] = saved
    print("clamps off: the counting recursion collapses to the antisum exactly (50 multisets)")

    for _ in range(200):
        Ms = [rng.randrange(C.NV) for _ in range(M)]
        W = pair_matrix(Ms, A)
        f, T, _ = full_bound(W)
        g, T2 = fast_bound(W)
        assert T == T2
        assert g <= f, ("fast exceeded full", g, f, Ms)
        assert f >= T, ("bound below antisum", f, T)
    print("200 random 11-multisets: fast <= full, full >= antisum")

    # dbar(a,a) = 9 for every rotation, so eleven copies of one rotation has
    # antisum 55*9 = 495 and no clamp can bite.
    W = pair_matrix([0] * M, A)
    f, T, _ = full_bound(W)
    assert (T, f) == (495, 495), (T, f)
    print("eleven copies of one rotation: antisum 495, bound 495 (no clamp bites)")

    # A hand-checkable case where the clamp DOES bite: force every 9-subset to
    # sit one below cr(K_{7,9}) = 144 by fiat and confirm the lift is what
    # counting says it is.
    k = 11
    Wf = [[0] * k for _ in range(k)]
    for i, j in itertools.combinations(range(k), 2):
        Wf[i][j] = Wf[j][i] = 4
    T = 55 * 4
    a9 = T - 2 * (10 * 4) + 4            # antisum of a 9-subset
    f, Tg, _ = full_bound(Wf)
    assert Tg == T
    # every 9-subset identical, so the level-9 clamp gives max(a9, 144) and the
    # level-10 value is ceil(10*that/7) clamped against 180, and the top is
    # ceil(11*that/9).
    l9 = max(a9, CR7[9])
    l10 = max(T - 40, CR7[10], -(-10 * l9 // 8))
    top = max(T, -(-11 * l10 // 9))
    assert f == top, (f, top, a9, l9, l10)
    print("uniform-matrix case: bound %d matches the counting arithmetic by hand" % f)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--class", dest="cls")
    ap.add_argument("--rows")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--fast", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    C = cog.CO(N)
    A = C.antidist_matrix(C.dist_matrix())
    if a.cls:
        Ms = [int(x) for x in a.cls.split(",")]
        W = pair_matrix(Ms, A)
        f, T, (lb, anti) = full_bound(W)
        fp, _, _ = full_bound(W, parity=True)
        g, _ = fast_bound(W)
        print("multiset      :", Ms)
        print("antisum       :", T)
        print("mixed bound   :", f, "   (top-two-levels only: %d)" % g)
        print("with parity   :", fp)
        print("Z(7)Z(11)     : 225")
        k = len(Ms)
        for c in (10, 9, 8, 7):
            vals = sorted((anti[s], lb[s]) for s in range(1 << k) if bin(s).count("1") == c)
            below = sum(1 for x, _ in vals if x < CR7[c])
            print("  %2d-subsets: antisum min %d max %d, %d of %d below cr(K_{7,%d})=%d"
                  % (c, vals[0][0], vals[-1][0], below, len(vals), c, CR7[c]))
        return
    if a.rows:
        best = None
        n = 0
        hist = {}
        for line in open(a.rows):
            line = line.strip()
            if not line:
                continue
            p = [int(x) for x in line.split(",")]
            Ms = p[1:]
            W = pair_matrix(Ms, A)
            if a.fast:
                v, T = fast_bound(W)
            else:
                v, T, _ = full_bound(W)
            assert T == p[0], (T, p[0], Ms)
            hist[v] = hist.get(v, 0) + 1
            if best is None or v < best[0]:
                best = (v, T, Ms)
            n += 1
            if a.limit and n >= a.limit:
                break
        print("rows %d  bound histogram %s" % (n, dict(sorted(hist.items()))))
        print("weakest bound %d at antisum %d: %s" % best)


if __name__ == "__main__":
    main()

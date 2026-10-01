"""
search.py -- staircase bounds, the canonical-form node-keep predicate, and the
search driver with an exact level counter.

NODE-KEEP PREDICATE.  A partial (m,n)-set a_1..a_k is kept iff all of:

 (1) STAIRCASE.  A(a_1..a_k) <= B[k], where B comes from Woodall Thm 1 (a drawing
     of K_{m,n} with cr = c contains one of K_{m-1,n} with cr <= c(m-2)/m, which in
     the antisum setting is exact: sum_v A(M\{v}) = (m-2)A(M), so min <= average)
     plus Thm 4(b) parity (for k,n both odd the antisum is even unless both are
     3 mod 4).  Reproduces Woodall's printed K_{7,7} ladder 79,56,36,21,9,3.

 (2) PREFIX-MINIMALITY  == Woodall Sec.4 canonical form.  His device minimises
     (f(P_m), f(P_{m-1}), ..., f(P_2)) lexicographically, which unpacks to:
     A(P_k) is minimal among k-subsets of P_{k+1}.  Since
     A(P_{k+1}\{u}) = A(P_{k+1}) - contrib(u), that is exactly
        *the newly added element has MAXIMAL contrib within the new prefix*.
     Note (2) IMPLIES (1), which is why its marginal contribution over the
     staircase is only ~1.5x (measured) rather than the (m-1)! one might expect.

 (3) STABILISER LEX-MIN.  a_1 = identity by vertex-transitivity; then
     (a_2..a_k) must be lex-minimal under Stab(identity) (dihedral, order 2n).
     Sound because stabiliser elements preserve all antidistances, hence the
     f-sequence, so canonical <=_lex g(canonical) termwise.
     MEASURED: this is where essentially all the collapse lives -- 13.8x of a
     theoretical 14x, against 1.5x for (2).  Ablation on (5,7): 195,110 nodes
     with neither, 129,044 with (2) only, 14,119 with (3) only, 9,333 with both.

 (4) THEOREM 7 (optional).  If every (m'+1,n)-set has antisum >= Z(m'+1)Z(n) and
     every (m-m',n)-set has antisum >= Z(m-m')Z(n), then any (m,n)-set containing
     an (m',n)-subset with antisum <= Z(m')Z(n) has antisum >= Z(m)Z(n).
     AVAILABILITY is NOT inherited up the ladder -- see thm7_availability().

WARNING -- ABLATION VALIDITY.  A depth-capped DFS visits every node at depth <= L
exactly once, so per-level counts up to L are exact *only if the run completes*.
If it aborts, counts are partial and ratios are meaningless.  Free check: a prune
that first acts at level p cannot change counts at levels < p, so if the two
configurations disagree below p the run was truncated.  Use ablation_valid().
This check caught three bad numbers (4.36x, 5.35x, 1.11x, 3.44x) that otherwise
looked publishable.
"""
import time
from itertools import combinations
import numpy as np
from cog import Z

# Minimum antisum actually attained, where it differs from Z(k)Z(n).
# (7,7): Woodall's 13,448 classes sit at 79, not 81.   (9,7): 140, not 144.
TRUE_MIN_ANTISUM = {(3, 7): 9, (5, 7): 36, (7, 7): 79, (9, 7): 140}


def parity_required(k, n):
    """Thm 4(b).  None if no constraint."""
    if k % 2 == 0 or n % 2 == 0:
        return None
    return 1 if (k % 4 == 3 and n % 4 == 3) else 0


def staircase(m, n, top=None):
    """B[k] for k = m..2.  top=None gives the strict counterexample bound Z(m)Z(n)-1."""
    B = {}
    t = (Z(m) * Z(n) - 1) if top is None else top
    p = parity_required(m, n)
    while p is not None and t % 2 != p:
        t -= 1
    B[m] = t
    for k in range(m, 2, -1):
        b = (B[k] * (k - 2)) // k
        p = parity_required(k - 1, n)
        while p is not None and b % 2 != p:
            b -= 1
        B[k - 1] = b
    return B


def thm7_availability(m, n, minima=None):
    """Which m' are available, and the deficit-weakened bound for the rest.
    Deficit propagation (derived from Thm 2's three-term proof; the (m-m') multiplier
    is the COUNT of elements of M\\M', with the (m'+1,n) hypothesis applied once per
    element, which is why d3 is multiplied and d2 is not):
        antisum >= Z(m)Z(n) - d2 - (m-m')*d3
    Verified over odd m<20, odd n<14, even m'<n, d2,d3<=6 with no exceptions.
    """
    minima = TRUE_MIN_ANTISUM if minima is None else minima
    out = {}
    # Woodall requires m' < n even, and m-m' >= 2 (m-m' = 1 is degenerate: Z(1)=0).
    for mp in range(2, min(m, n), 2):
        if m - mp < 2:
            continue
        k2, k3 = m - mp, mp + 1
        d2 = Z(k2) * Z(n) - minima.get((k2, n), Z(k2) * Z(n))
        d3 = Z(k3) * Z(n) - minima.get((k3, n), Z(k3) * Z(n))
        out[mp] = dict(exact=(d2 == 0 and d3 == 0), d2=d2, d3=d3,
                       bound=Z(m) * Z(n) - d2 - (m - mp) * d3,
                       excludes_subset_antisum_at_most=Z(mp) * Z(n))
    return out


def search(G, A_np, A_py, stab, m, B, depth=None, thm7=(), time_cap=None,
           survivor_cap=None, collect=True, shuffle_rng=None):
    """Depth-first search over canonical (m,n)-sets.

    thm7: iterable of m' values whose Theorem 7 exclusion to apply.
    depth: stop descending below this level (per-level counts exact to `depth`
           PROVIDED the run completes -- check `aborted`).
    Returns (level_counts, survivors, elapsed, aborted).
    """
    NV = G.NV
    counts = [0] * (m + 2)
    surv = []
    buf = np.zeros((m + 2, NV), dtype=np.int32)
    t0 = time.time()
    ab = [False]
    excl = {mp: Z(mp) * Z(G.n) for mp in thm7}

    def rec(k, S, ch, co):
        counts[k] += 1
        if ab[0]:
            return
        if k == m:
            if collect:
                surv.append((S, tuple(ch)))
            if survivor_cap and len(surv) >= survivor_cap:
                ab[0] = True
            return
        if depth is not None and k >= depth:
            return
        if time_cap is not None and time.time() - t0 > time_cap:
            ab[0] = True
            return
        row = buf[k]
        cands = np.nonzero(row <= B[k + 1])[0]
        if shuffle_rng is not None:
            cands = list(cands)
            shuffle_rng.shuffle(cands)
        for v in cands:
            if ab[0]:
                return
            v = int(v)
            nS = int(row[v])
            cv = nS - S
            Av = A_py[v]
            if 2 in excl and any(Av[u] <= excl[2] for u in ch):      # m'=2
                continue
            nc, bad = [], False
            for i, u in enumerate(ch):                                # (2) prefix-min
                c2 = co[i] + Av[u]
                if c2 > cv:
                    bad = True
                    break
                nc.append(c2)
            if bad:
                continue
            nc.append(cv)
            ch.append(v)
            if 4 in excl and len(ch) >= 4:                            # m'=4
                lim = excl[4]
                viol = False
                for tri in combinations(range(len(ch) - 1), 3):
                    q = [ch[i] for i in tri] + [v]
                    if sum(A_py[q[a]][q[b]] for a in range(4) for b in range(a + 1, 4)) <= lim:
                        viol = True
                        break
                if viol:
                    ch.pop()
                    continue
            tail = ch[1:]                                             # (3) stabiliser
            sm = False
            for g in stab:
                for t_ in tail:
                    if g[t_] < t_:
                        sm = True
                        break
                    if g[t_] > t_:
                        break
                if sm:
                    break
            if sm:
                ch.pop()
                continue
            nx = buf[k + 1]
            np.add(row, A_np[v], out=nx)
            nx += cv
            rec(k + 1, nS, ch, nc)
            ch.pop()

    buf[1] = A_np[0]
    rec(1, 0, [0], [0])
    return counts, surv, time.time() - t0, ab[0]


def ablation_valid(counts_on, counts_off, first_acting_level):
    """A prune acting first at level p cannot change counts below p.  Disagreement
    below p proves at least one run was truncated and the ratio is meaningless."""
    for k in range(1, first_acting_level):
        if counts_on[k] != counts_off[k]:
            return False, k
    return True, None


# ---------------------------------------------------------------- known results
MEASURED = {
    "thm7_ablation_(7,7)_depth5": dict(on=[1, 12, 329, 25346, 615817],
                                       off=[1, 13, 377, 29099, 801503],
                                       cumulative=1.2954, note="both COMPLETE; exact"),
    "thm7_availability": "m=7 yes (m'=2,4); m=9 yes (m'=4 only); m=11 NO m' available",
    "frontier_(11,7)": "survivors at antisum 221 exist (288 found before abort); "
                       "223 is the top rung; nothing yet seen at 219",
    "weakened_thm7_prune_cost": "C(k-1,3) rescan per node: 20 triples at m=7, 120 at m=11. "
                                "Throughput 217k nodes/s without vs 98k/s with -> 2.2x per node. "
                                "Must shrink the tree by >2.2x to pay off in wall clock. UNMEASURED.",
}

#!/usr/bin/env python3
"""Shardable, resumable (m,7) enumeration, for a wall-clock-capped platform.

WHY THIS EXISTS.  The received `search()` starts at rec(1, 0, [0], [0]) and runs
to completion in one process.  A platform with a 12-hour session ceiling needs
two things it does not have: the run split into independent pieces, and each
piece restartable.  Both come free from one observation:

    THE ONLY STATE A NODE NEEDS IS ITS PREFIX.

Everything else in rec(k, S, ch, co) plus buf[k] is recomputable from ch:
    co[i]  = sum_{j != i} A[ch[i]][ch[j]]          (contribution of element i)
    S      = sum over pairs of ch
    row[w] = S + sum_i A[ch[i]][w]                 (antisum of ch + {w})
So a prefix at some split level L is a complete, serialisable task, the subtrees
below distinct level-L prefixes are disjoint, and their level counts add.

TWO PHASES.
  1. FRONTIER.  Enumerate every surviving prefix at level L.  This needs no new
     code at all: the received search() takes the staircase B as a parameter, so
     calling it with m = L and B = staircase(m_target, 7) runs the target's own
     node-keep predicate and collects the level-L prefixes as "survivors".
  2. SHARDS.  Each worker takes a slice of that list and runs the continuation.

search_from() below IS the received search() with one added argument, `start`.
A FORK OF SOMEONE ELSE'S SEARCH IS A LIABILITY UNLESS IT IS GATED, so
self_test() requires it to reproduce, exactly:
    (7,7) Theorem 7 on   1, 12, 329, 25346, 615817, 9827953, 809438
    (7,7) Theorem 7 off  1, 13, 377, 29099, 801503, 14623179, 809438
both as a single process AND as the sum over shards at two different split
levels.  Run `python3 shard.py selftest` before trusting any number it prints.

    python3 shard.py selftest
    python3 shard.py frontier <m> <L> [thm7]        -> frontier_m<m>_L<L>.json
    python3 shard.py run <m> <L> <i> <N> [thm7]     -> shard_m<m>_L<L>_<i>of<N>.json
    python3 shard.py merge <m> <L> <N>              -> merged_m<m>_L<L>.json
    python3 shard.py sample <m> <L> <k> [thm7] [cap] -> an unbiased total estimate
    python3 shard.py deepsample <m> <L> <k> [thm7] [cap]  -> same, frontier in memory

`run` is idempotent: an existing output file for that shard is left alone, so a
session killed by the wall clock is resumed by re-issuing the same command.
"""
import json, pathlib, sys, time
from itertools import combinations
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "intake"))
from cog import CO, Z                                                  # noqa: E402
from search import staircase, search                                   # noqa: E402

OUT = HERE / "runs"


# --------------------------------------------------------------- the forked DFS
def search_from(G, A_np, A_py, stab, m, B, start=None, depth=None, thm7=(),
                time_cap=None, collect=False):
    """The received search(), plus `start`: a prefix tuple to resume from.

    start=None reproduces the original exactly (gated in self_test).
    With start=ch, counts[k] covers only the subtree rooted at ch, INCLUDING ch
    itself at level len(ch).
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
            return
        if depth is not None and k >= depth:
            return
        if time_cap is not None and time.time() - t0 > time_cap:
            ab[0] = True
            return
        row = buf[k]
        cands = np.nonzero(row <= B[k + 1])[0]
        for v in cands:
            if ab[0]:
                return
            v = int(v)
            nS = int(row[v])
            cv = nS - S
            Av = A_py[v]
            if 2 in excl and any(Av[u] <= excl[2] for u in ch):
                continue
            nc, bad = [], False
            for i, u in enumerate(ch):
                c2 = co[i] + Av[u]
                if c2 > cv:
                    bad = True
                    break
                nc.append(c2)
            if bad:
                continue
            nc.append(cv)
            ch.append(v)
            if 4 in excl and len(ch) >= 4:
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
            tail = ch[1:]
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

    if start is None:
        buf[1] = A_np[0]
        rec(1, 0, [0], [0])
    else:
        ch = list(start)
        k = len(ch)
        S = sum(A_py[ch[i]][ch[j]] for i, j in combinations(range(k), 2))
        co = [sum(A_py[ch[i]][ch[j]] for j in range(k) if j != i) for i in range(k)]
        base = np.zeros(NV, dtype=np.int32)
        for u in ch:
            base += A_np[u]
        buf[k] = base + S
        rec(k, S, ch, co)
    return counts, surv, time.time() - t0, ab[0]


# ------------------------------------------------------------------- the context
_CTX = {}
def ctx():
    if not _CTX:
        G = CO(7)
        D = G.dist_matrix()
        A_py = G.antidist_matrix(D)
        _CTX.update(G=G, A_py=A_py, A_np=np.array(A_py, dtype=np.int32),
                    stab=[x for x in G.stabiliser() if x != list(range(G.NV))])
    return _CTX


def _thm7(arg):
    return tuple(int(x) for x in arg.split(",") if x) if arg else ()


# ------------------------------------------------------------------- phase 1
def frontier(m, L, thm7=()):
    """Every surviving prefix at level L under the (m,7) node-keep predicate."""
    c = ctx()
    B = staircase(m, 7)
    counts, surv, el, ab = search(c["G"], c["A_np"], c["A_py"], c["stab"], L, B,
                                  thm7=thm7, collect=True)
    assert not ab, "frontier pass aborted"
    assert counts[L] == len(surv), (counts[L], len(surv))
    return dict(m=m, L=L, thm7=list(thm7), counts_to_L=counts[:L + 1],
                prefixes=[list(ch) for _, ch in surv], elapsed_s=round(el, 1))


# ------------------------------------------------------------------- phase 2
def run_shard(m, L, i, N, thm7=(), time_cap=None):
    f = json.loads((OUT / ("frontier_m%d_L%d.json" % (m, L))).read_text())
    assert f["thm7"] == list(thm7), "frontier was built with a different thm7"
    pre = f["prefixes"][i::N]
    c = ctx()
    B = staircase(m, 7)
    tot = [0] * (m + 2)
    t0 = time.time()
    done = 0
    for ch in pre:
        counts, _, _, ab = search_from(c["G"], c["A_np"], c["A_py"], c["stab"], m, B,
                                       start=tuple(ch), thm7=thm7)
        assert not ab
        for k in range(len(tot)):
            tot[k] += counts[k]
        done += 1
        if time_cap is not None and time.time() - t0 > time_cap:
            break
    return dict(m=m, L=L, shard=i, of=N, thm7=list(thm7),
                prefixes_assigned=len(pre), prefixes_done=done,
                complete=(done == len(pre)), counts=tot,
                nodes=sum(tot), elapsed_s=round(time.time() - t0, 1))


def sample_deep(m, L, k, thm7=(), time_cap=None):
    """Same estimator as sample(), but it builds the level-L frontier IN MEMORY
    and never writes it, so L can be deep enough that the subtrees are small.

    Choosing L is the whole trick.  At (11,7) the level-4 subtrees are large
    enough that two dozen of them do not finish in fifteen minutes, which makes
    a sample at L=4 expensive for no gain; at L=5 the frontier is 6.7 million
    prefixes and each subtree is correspondingly small.  Deeper L costs more in
    the frontier pass and less per subtree, and the frontier pass is the cheap
    half.
    """
    import statistics
    c = ctx()
    B = staircase(m, 7)
    counts, surv, el_f, ab = search(c["G"], c["A_np"], c["A_py"], c["stab"], L, B,
                                    thm7=thm7, collect=True)
    assert not ab, "frontier pass aborted"
    assert counts[L] == len(surv)
    step = max(1, len(surv) // k)
    picked = [ch for _, ch in surv[::step][:k]]
    del surv
    sizes, t0, done = [], time.time(), 0
    for ch in picked:
        sc, _, _, a2 = search_from(c["G"], c["A_np"], c["A_py"], c["stab"], m, B,
                                   start=tuple(ch), thm7=thm7)
        assert not a2
        sizes.append(sum(sc))
        done += 1
        if time_cap is not None and time.time() - t0 > time_cap:
            break
    el = time.time() - t0
    tot_s = sum(sizes)
    est = tot_s * (counts[L] / done)
    return dict(m=m, L=L, thm7=list(thm7), frontier=counts[L], counts_to_L=counts[:L + 1],
                frontier_seconds=round(el_f, 1), sampled=done, step=step,
                sampled_nodes=tot_s, sample_seconds=round(el, 1),
                nodes_per_s=round(tot_s / el) if el else None,
                subtree_min=min(sizes), subtree_max=max(sizes),
                subtree_mean=round(statistics.mean(sizes), 1),
                subtree_median=statistics.median(sizes),
                subtree_stdev=round(statistics.stdev(sizes), 1) if len(sizes) > 1 else 0.0,
                skew_max_over_mean=round(max(sizes) / statistics.mean(sizes), 1),
                estimate_total_nodes=round(est),
                estimate_core_hours=round(est / (tot_s / el) / 3600, 2) if el else None)


def sample(m, L, k, thm7=(), time_cap=None, seed=0):
    """Estimate the FULL tree by running a systematic sample of level-L subtrees.

    This is the right estimator for this problem and extrapolating level ratios is
    the wrong one: a sample of complete subtrees is unbiased for the total, whereas
    a growth-ratio extrapolation has no error model at all and was wrong by 32x on
    (7,7).  The caveat is SKEW, not bias -- subtree sizes are heavily unequal, so a
    small sample has a wide spread and the report below prints it rather than hiding
    it behind a point estimate.
    """
    import statistics
    f = json.loads((OUT / ("frontier_m%d_L%d.json" % (m, L))).read_text())
    pre = f["prefixes"]
    step = max(1, len(pre) // k)
    picked = pre[::step][:k]
    c = ctx()
    B = staircase(m, 7)
    sizes, t0, done = [], time.time(), 0
    for ch in picked:
        counts, _, _, ab = search_from(c["G"], c["A_np"], c["A_py"], c["stab"], m, B,
                                       start=tuple(ch), thm7=thm7)
        assert not ab
        sizes.append(sum(counts))
        done += 1
        if time_cap is not None and time.time() - t0 > time_cap:
            break
    el = time.time() - t0
    tot_sampled = sum(sizes)
    scale = len(pre) / done
    est = tot_sampled * scale
    return dict(m=m, L=L, frontier=len(pre), sampled=done, step=step,
                sampled_nodes=tot_sampled, elapsed_s=round(el, 1),
                nodes_per_s=round(tot_sampled / el) if el else None,
                subtree_min=min(sizes), subtree_max=max(sizes),
                subtree_mean=round(statistics.mean(sizes), 1),
                subtree_median=statistics.median(sizes),
                subtree_stdev=round(statistics.stdev(sizes), 1) if len(sizes) > 1 else 0.0,
                estimate_total_nodes=round(est),
                estimate_core_hours=round(est / (tot_sampled / el) / 3600, 2) if el else None,
                skew_max_over_mean=round(max(sizes) / statistics.mean(sizes), 1))


def merge(m, L, N):
    f = json.loads((OUT / ("frontier_m%d_L%d.json" % (m, L))).read_text())
    tot = [0] * (m + 2)
    for k in range(L):
        tot[k] = f["counts_to_L"][k]
    missing, el = [], 0.0
    for i in range(N):
        p = OUT / ("shard_m%d_L%d_%dof%d.json" % (m, L, i, N))
        if not p.exists():
            missing.append(i); continue
        s = json.loads(p.read_text())
        if not s["complete"]:
            missing.append(i); continue
        el += s["elapsed_s"]
        for k in range(L, len(tot)):
            tot[k] += s["counts"][k]
    ok = not missing and tot[L] == f["counts_to_L"][L]
    return dict(m=m, L=L, N=N, level_counts=tot, total_nodes=sum(tot),
                frontier_level_agrees=(tot[L] == f["counts_to_L"][L]),
                missing_or_incomplete=missing, complete=ok,
                core_seconds=round(el, 1))


# ------------------------------------------------------------------- the gate
KNOWN = {(7, (2, 4)): [1, 12, 329, 25346, 615817, 9827953, 809438],
         (7, ()):     [1, 13, 377, 29099, 801503, 14623179, 809438]}

def self_test():
    c = ctx()
    bad = []
    def ck(label, got, want):
        ok = got == want
        if not ok: bad.append(label)
        print(("  ok   " if ok else "  FAIL ") + "%-50s %s" % (label, got if ok else "%s (want %s)" % (got, want)))

    for thm7, want in sorted(KNOWN.items(), key=lambda kv: str(kv[0])):
        t7 = thm7[1]
        B = staircase(7, 7)
        lab = "Thm7 " + ("on " if t7 else "off")
        cn, _, el, ab = search_from(c["G"], c["A_np"], c["A_py"], c["stab"], 7, B, thm7=t7)
        ck("%s: fork with start=None reproduces (7,7)" % lab, cn[1:8], want)
        print("         (%.0f s)" % el)
        for L in (3, 4):
            fr = frontier(7, L, t7)
            tot = [0] * 9
            for k in range(L):
                tot[k] = fr["counts_to_L"][k]
            for ch in fr["prefixes"]:
                sc, _, _, _ = search_from(c["G"], c["A_np"], c["A_py"], c["stab"], 7, B,
                                          start=tuple(ch), thm7=t7)
                for k in range(L, 9):
                    tot[k] += sc[k]
            ck("%s: sharded at L=%d, summed, reproduces it" % (lab, L), tot[1:8], want)
            ck("%s: frontier count at L=%d equals the shard roots" % (lab, L),
               fr["counts_to_L"][L], tot[L])
    print()
    print("GATE: %s" % ("PASSED -- the fork is faithful" if not bad else "FAILED -> " + "; ".join(bad)))
    return not bad


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "selftest"
    if cmd == "selftest":
        sys.exit(0 if self_test() else 1)
    if cmd == "frontier":
        m, L = int(sys.argv[2]), int(sys.argv[3])
        t7 = _thm7(sys.argv[4] if len(sys.argv) > 4 else "")
        r = frontier(m, L, t7)
        p = OUT / ("frontier_m%d_L%d.json" % (m, L))
        p.write_text(json.dumps(r) + "\n")
        print("%s: %d prefixes at level %d, counts %s, %.1f s"
              % (p.name, len(r["prefixes"]), L, r["counts_to_L"][1:], r["elapsed_s"]))
    elif cmd == "run":
        m, L, i, N = (int(x) for x in sys.argv[2:6])
        t7 = _thm7(sys.argv[6] if len(sys.argv) > 6 else "")
        p = OUT / ("shard_m%d_L%d_%dof%d.json" % (m, L, i, N))
        if p.exists() and json.loads(p.read_text()).get("complete"):
            print("%s already complete; nothing to do" % p.name); sys.exit(0)
        r = run_shard(m, L, i, N, t7)
        p.write_text(json.dumps(r) + "\n")
        print("%s: %d/%d prefixes, %d nodes, %.1f s%s"
              % (p.name, r["prefixes_done"], r["prefixes_assigned"], r["nodes"],
                 r["elapsed_s"], "" if r["complete"] else "  INCOMPLETE -- re-issue to resume"))
    elif cmd == "sample":
        m, L, k = (int(x) for x in sys.argv[2:5])
        t7 = _thm7(sys.argv[5] if len(sys.argv) > 5 else "")
        capv = float(sys.argv[6]) if len(sys.argv) > 6 else None
        r = sample(m, L, k, t7, time_cap=capv)
        (OUT / ("sample_m%d_L%d.json" % (m, L))).write_text(json.dumps(r, indent=2) + "\n")
        print(json.dumps(r, indent=2))
    elif cmd == "deepsample":
        m, L, k = (int(x) for x in sys.argv[2:5])
        t7 = _thm7(sys.argv[5] if len(sys.argv) > 5 else "")
        capv = float(sys.argv[6]) if len(sys.argv) > 6 else None
        r = sample_deep(m, L, k, t7, time_cap=capv)
        (OUT / ("deepsample_m%d_L%d.json" % (m, L))).write_text(json.dumps(r, indent=2) + "\n")
        print(json.dumps(r, indent=2))
    elif cmd == "merge":
        m, L, N = (int(x) for x in sys.argv[2:5])
        r = merge(m, L, N)
        p = OUT / ("merged_m%d_L%d.json" % (m, L))
        p.write_text(json.dumps(r, indent=2) + "\n")
        print(json.dumps(r, indent=2))
    else:
        print(__doc__); sys.exit(2)

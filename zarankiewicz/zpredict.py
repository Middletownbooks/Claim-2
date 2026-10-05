#!/usr/bin/env python3
"""zpredict.py -- what the sweep must write for an orbit class, row by row, and whether it did.

THE IDEA.  Relabelling the seven points, and reversing every rotation, preserves
every antidistance: the group S_7 x <rev>, order 10080, acts on (11,7)-sets and
the survivor set is a union of its orbits.  For one orbit the sweep's canonical
rules -- a_1 = vertex 0, the staircase, prefix-minimality, lex-minimality under
Stab(vertex 0) -- select an exact, computable set of rows.  This script
recomputes that set from scratch, maps each row's level-5 prefix to the shard
that owns it (through the frontier file, index mod NSHARDS, as load_prefixes
deals them), and compares with what the shards wrote.  A finished shard must
hold every predicted row under its prefixes and no other row of the class.

WHAT A FINISHED SHARD IS.  One with a certificate (sh_m11_L5_<i>of2400.json),
or with a low_<i>.txt -- run_shard renames that into place only after the shard
completes and its line count agrees with its histogram.  Each certificate is
also checked against its low file, antisum by antisum.

THE PORT IS CHECKED, NOT TRUSTED.  The rules are a line-for-line port of
search.c, and
  --selftest          reproduces the C gate's (7,7) level counts with the same
                      code (levels 1-5; all seven with --full-gate), the 219
                      class's totals, and runs fault-injection tests: a dropped
                      row, an extra row, a misfiled row, a shard with no low
                      file, a certificate that disagrees -- each must be caught;
  --build-frontier F  regenerates the (11,7) level-5 frontier in the C's order;
                      with --frontier also given, it is compared line by line,
                      which pins the shard mapping to the real file.

WHAT IT CANNOT SEE.  --all discovers classes from rows that were written, so a
class with no row anywhere is invisible to it.  The checks bite on partial
loss: a dropped row, a dropped prefix, a short or misfiled shard.  --class
covers a class you name whether or not any row of it has appeared.

USAGE
  python3 zpredict.py --selftest
  python3 zpredict.py --build-frontier py_frontier.txt --frontier frontier_m11_L5.txt
  python3 zpredict.py --runs zout kaggle_zout --frontier frontier_m11_L5.txt --all \\
                      --report check.json --jobs 4
  python3 zpredict.py --runs zout --frontier frontier_m11_L5.txt \\
                      --class 0,0,15,74,105,438,569,647,660,671,689 --emit expected/
"""
import argparse, collections, itertools, json, math, os, pathlib, random, re, sys, time
import multiprocessing as mp

import numpy as np

VERSION = "zpredict-1"
N, M = 7, 11
GATE77 = [1, 13, 377, 29099, 801503, 14623179, 809438]
CLASS219 = (0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)
CLASS219_TOTALS = dict(orbit=5040, multisets=13, rows=976, prefixes=130)
# Prefixes of rows a real run wrote, with the totals the class owes each one.
CLASS219_SEEN = {(0, 143, 567, 451, 167): 12, (0, 95, 239, 105, 159): 7,
                 (0, 95, 415, 513, 479): 4, (0, 143, 311, 569, 22): 3}


def zf(k):
    return (k // 2) * ((k - 1) // 2)


# ------------------------------------------------------------------- CO_7
# Vertex order as cog.c: cyclic orders with 0 leading, in the order
# itertools.permutations(range(1,7)) -- lexicographic, as next_perm walks.
CO = {}


def build():
    if CO:
        return CO
    verts = [(0,) + p for p in itertools.permutations(range(1, N))]
    index = {v: i for i, v in enumerate(verts)}

    def canon(w):
        z = w.index(0)
        return tuple(w[z:] + w[:z])

    nv = len(verts)
    adj, rev = [], []
    for v in verts:
        nb = []
        for j in range(N):
            k = (j + 1) % N
            w = list(v)
            w[j], w[k] = w[k], w[j]
            nb.append(index[canon(w)])
        adj.append(nb)
        rev.append(index[canon(list(v[::-1]))])
    dist = []
    for s in range(nv):
        d = [-1] * nv
        d[s] = 0
        q, h = [s], 0
        while h < len(q):
            u = q[h]
            h += 1
            for x in adj[u]:
                if d[x] < 0:
                    d[x] = d[u] + 1
                    q.append(x)
        dist.append(d)
    A = np.array([[dist[a][rev[b]] for b in range(nv)] for a in range(nv)], dtype=np.int32)

    # The group as maps on vertex indices, closed from generators: the six
    # adjacent label transpositions (which generate S_7) and reversal.
    def label_map(sig):
        return np.array([index[canon([sig[x] for x in verts[v]])] for v in range(nv)],
                        dtype=np.int32)

    gens = []
    for i in range(N - 1):
        s = list(range(N))
        s[i], s[i + 1] = s[i + 1], s[i]
        gens.append(label_map(s))
    gens.append(np.array(rev, dtype=np.int32))
    ident = np.arange(nv, dtype=np.int32)
    seen = {ident.tobytes(): ident}
    todo = [ident]
    while todo:
        nxt = []
        for g in todo:
            for h in gens:
                c = h[g]
                k = c.tobytes()
                if k not in seen:
                    seen[k] = c
                    nxt.append(c)
        todo = nxt
    G = np.stack(list(seen.values()))
    if len(G) != 2 * math.factorial(N):
        sys.exit("group has order %d, want %d" % (len(G), 2 * math.factorial(N)))
    stab = [g.tolist() for g in G if g[0] == 0 and not np.array_equal(g, ident)]
    if len(stab) != 2 * N - 1:
        sys.exit("Stab(0) without identity has %d elements, want %d" % (len(stab), 2 * N - 1))
    CO.update(verts=verts, rev=rev, A=A, ad=[bytes(r.tolist()) for r in A], G=G, stab=stab)
    return CO


# ------------------------------------------------------- the rules, ported
def parity_required(k, n):
    if k % 2 == 0 or n % 2 == 0:
        return -1
    return 1 if (k % 4 == 3 and n % 4 == 3) else 0


def staircase(m, n, top=-1):
    """search.c staircase(), verbatim."""
    B = [0] * (m + 2)
    t = top if top > 0 else zf(m) * zf(n) - 1
    p = parity_required(m, n)
    while p >= 0 and t % 2 != p:
        t -= 1
    B[m] = t
    for k in range(m, 2, -1):
        b = (B[k] * (k - 2)) // k
        pk = parity_required(k - 1, n)
        while pk >= 0 and b % 2 != pk:
            b -= 1
        B[k - 1] = b
    return B


def lexmin_ok(stab, ch):
    """Clause (3): reject if some g in Stab(0) takes (a_2..a_k) lex-below itself."""
    for g in stab:
        for i in range(1, len(ch)):
            t, gt = ch[i], g[ch[i]]
            if gt < t:
                return False
            if gt > t:
                break
    return True


def enumerate_tree(m, maxlev, B, emit=None):
    """The C's DFS: level counts to maxlev, emitting level-maxlev prefixes in
    the C's order (candidates ascending, as the cl[] scan finds them)."""
    co_ = build()
    A, ad, stab = co_["A"], co_["ad"], co_["stab"]
    counts = [0] * (m + 2)

    def rec(ch, co, S, row):
        k = len(ch)
        counts[k] += 1
        if k == maxlev:
            if emit:
                emit(ch)
            return
        lim, lo = B[k + 1], S + max(co)
        for v in np.nonzero((row <= lim) & (row >= lo))[0].tolist():
            nS = int(row[v])
            cv = nS - S
            nc = [co[i] + ad[v][ch[i]] for i in range(k)]
            if max(nc) > cv:                               # (2) prefix-minimality
                continue
            nch = ch + [v]
            if not lexmin_ok(stab, nch):                   # (3)
                continue
            rec(nch, nc + [cv], nS, row + A[v] + cv)

    rec([0], [0], 0, A[0].copy())
    return counts[1:maxlev + 1]


def rows_for_multiset(ms, B, survmax, m=M):
    """Every row the sweep writes whose multiset is ms: the same DFS, with the
    candidates restricted to what is left of ms."""
    co_ = build()
    ad, stab = co_["ad"], co_["stab"]
    rem = collections.Counter(ms)
    if rem[0] == 0:
        return []
    rem[0] -= 1
    vals = sorted(rem)
    out = []

    def rec(ch, co, S):
        k = len(ch)
        if k == m:
            if S <= survmax:
                out.append((S, tuple(ch)))
            return
        lim, mx = B[k + 1], max(co)
        for v in vals:
            if rem[v] == 0:
                continue
            cv = sum(ad[v][c] for c in ch)
            nS = S + cv
            if nS > lim or cv < mx:                        # (1) staircase, row >= lo
                continue
            nc = [co[i] + ad[v][ch[i]] for i in range(k)]
            if max(nc) > cv:
                continue
            nch = ch + [v]
            if not lexmin_ok(stab, nch):
                continue
            rem[v] -= 1
            rec(nch, nc + [cv], nS)
            rem[v] += 1

    rec([0], [0], 0)
    return out


def orbit_of(ms):
    """All sorted images of ms under the 10080 maps, lexicographically sorted;
    row 0 is the class key."""
    imgs = build()["G"][:, list(ms)]
    imgs.sort(axis=1)
    return np.unique(imgs, axis=0)


def antisum(seq):
    ad = build()["ad"]
    return sum(ad[seq[i]][seq[j]] for i in range(len(seq)) for j in range(i + 1, len(seq)))


def predict_class(job):
    rep, B, survmax, level = job
    orb = orbit_of(rep)
    key = tuple(int(x) for x in orb[0])
    members0 = [tuple(int(x) for x in r) for r in orb if r[0] == 0]
    rows = []
    for ms in members0:
        rows += rows_for_multiset(ms, B, survmax)
    rows.sort(key=lambda r: r[1])
    by_prefix = collections.defaultdict(list)
    for s, seq in rows:
        by_prefix[seq[:level]].append(seq)
    return dict(key=key, antisum=antisum(rep), orbit=len(orb), members0=members0,
                rows=rows, by_prefix=dict(by_prefix),
                multisets=len({tuple(sorted(seq)) for _, seq in rows}))


# ------------------------------------------------------------ run contents
def fmt(seq):
    return ",".join(map(str, seq))


def read_frontier(path, wanted):
    """Index of each wanted prefix among the non-empty lines, counted exactly
    as load_prefixes counts them."""
    found, dup, n = {}, [], 0
    with open(path) as f:
        for raw in f:
            if raw[:1] in ("\n", "\0", ""):
                continue
            s = raw.rstrip("\n")
            if s in wanted:
                if s in found:
                    dup.append(s)
                else:
                    found[s] = n
            n += 1
    return found, n, dup


def scan_runs(dirs, nshards, level, survmax, problems):
    pat_c = re.compile(r"^sh_m%d_L%d_(\d+)of%d\.json$" % (M, level, nshards))
    pat_l = re.compile(r"^low_(\d+)\.txt$")
    certs = collections.defaultdict(list)
    lows = collections.defaultdict(list)
    for d in dirs:
        for p in sorted(pathlib.Path(d).rglob("*")):
            mc, ml = pat_c.match(p.name), pat_l.match(p.name)
            if mc:
                try:
                    c = json.loads(p.read_text())
                except Exception as e:
                    problems.append(("CERT_UNREADABLE", str(p), str(e)))
                    continue
                if c.get("complete"):
                    certs[int(mc.group(1))].append((p, c))
            elif ml:
                lows[int(ml.group(1))].append(p)
    rows = {}                           # shard -> list of (S, seq)
    for sh, paths in sorted(lows.items()):
        versions = []
        for p in paths:
            rs = []
            with open(p) as f:
                for n, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    v = [int(x) for x in line.split(",")]
                    if len(v) != M + 1:
                        sys.exit("%s:%d: want %d fields" % (p, n, M + 1))
                    seq = tuple(v[1:])
                    if antisum(seq) != v[0]:
                        sys.exit("%s:%d: the file says antisum %d, this script's CO_7 says %d; "
                                 "the vertex order differs from cog.c's or the file is corrupt"
                                 % (p, n, v[0], antisum(seq)))
                    rs.append((v[0], seq))
            versions.append((p, rs))
        p0, r0 = versions[0]
        for p, r in versions[1:]:
            if sorted(r) != sorted(r0):
                problems.append(("DUPLICATE_SHARD_DIFFERS", sh, "%s vs %s" % (p0, p)))
        rows[sh] = r0
        if len({seq for _, seq in r0}) != len(r0):
            problems.append(("DUPLICATE_ROW_IN_FILE", sh, str(p0)))
    for sh, cl in sorted(certs.items()):
        c0 = cl[0][1]
        for p, c in cl[1:]:
            if (c.get("below_top_rung"), c.get("antisum_histogram")) != \
                    (c0.get("below_top_rung"), c0.get("antisum_histogram")):
                problems.append(("CERT_CONFLICT", sh, "%s vs %s" % (cl[0][0], p)))
        want = {int(k): v for k, v in c0.get("antisum_histogram", {}).items() if int(k) <= survmax}
        have = collections.Counter(s for s, _ in rows.get(sh, []))
        if sum(want.values()) and sh not in rows:
            problems.append(("LOW_FILE_MISSING", sh, "certificate says %d rows" % sum(want.values())))
        elif dict(have) != want:
            problems.append(("CERT_LOW_MISMATCH", sh, "certificate %s, file %s"
                             % (dict(sorted(want.items())), dict(sorted(have.items())))))
    return certs, rows


# --------------------------------------------------------------- the check
def run_check(args, problems, quiet=False):
    say = (lambda *a: None) if quiet else (lambda *a: print(*a, flush=True))
    B = staircase(M, N, args.top)
    certs, rows = scan_runs(args.runs, args.nshards, args.level, args.survmax, problems)
    done = set(certs) | set(rows)
    nrows = sum(len(r) for r in rows.values())
    say("runs: %d certified shards, %d low files, %d rows" % (len(certs), len(rows), nrows))
    if not args.frontier:
        say("  no --frontier: only prefixes with at least one row written can be checked,")
        say("  and a prefix whose shard finished without writing it would go unseen.")

    # classes: named, or discovered from every distinct multiset written
    member = {}
    reps = {}
    targets = [tuple(sorted(int(x) for x in c.split(","))) for c in (args.cls or [])]
    if args.all:
        targets += sorted({tuple(sorted(seq)) for r in rows.values() for _, seq in r})
    t0 = time.time()
    for ms in targets:
        if len(ms) != M:
            sys.exit("a class needs %d vertices, got %d" % (M, len(ms)))
        if ms in member:
            continue
        orb = orbit_of(ms)
        key = tuple(int(x) for x in orb[0])
        reps.setdefault(key, ms)
        for r in orb:
            if r[0] == 0:
                member[tuple(int(x) for x in r)] = key
    say("classes: %d (orbits found in %.1f s)" % (len(reps), time.time() - t0))

    t0 = time.time()
    jobs = [(reps[k], B, args.survmax, args.level) for k in sorted(reps)]
    if args.jobs > 1 and len(jobs) > 1:
        with mp.get_context("fork").Pool(args.jobs) as pool:
            preds = pool.map(predict_class, jobs, chunksize=4)
    else:
        preds = [predict_class(j) for j in jobs]
    say("predicted in %.1f s" % (time.time() - t0))

    fidx = {}
    if args.frontier:
        wanted = {fmt(p) for pr in preds for p in pr["by_prefix"]}
        fidx, nfront, dup = read_frontier(args.frontier, wanted)
        say("frontier: %d prefixes; %d of the %d predicted prefixes located"
            % (nfront, len(fidx), len(wanted)))
        for s in dup:
            problems.append(("FRONTIER_DUPLICATE", s, ""))

    def shard_of(prefix):
        i = fidx.get(fmt(prefix))
        return None if i is None else i % args.nshards

    seen_prefix = {seq[:args.level] for r in rows.values() for _, seq in r}
    obs = collections.defaultdict(list)                    # class -> [(shard, seq)]
    for sh, r in rows.items():
        for _, seq in r:
            k = member.get(tuple(sorted(seq)))
            if k is not None:
                obs[k].append((sh, seq))

    report = []
    for pr in preds:
        key = pr["key"]
        pred_rows = {seq for _, seq in pr["rows"]}
        got = collections.defaultdict(set)
        for sh, seq in obs.get(key, []):
            p = seq[:args.level]
            got[p].add(seq)
            if seq not in pred_rows:
                problems.append(("EXTRA_ROW", fmt(seq), "shard %d, class %s" % (sh, fmt(key))))
            elif args.frontier:
                want_sh = shard_of(p)
                if want_sh is not None and want_sh != sh:
                    problems.append(("MISFILED_ROW", fmt(seq), "in shard %d, prefix belongs to %d"
                                     % (sh, want_sh)))
        n_done = n_pend = rows_ok = 0
        pending_shards = set()
        for p, seqs in sorted(pr["by_prefix"].items()):
            if args.frontier:
                sh = shard_of(p)
                if sh is None:
                    problems.append(("PREFIX_NOT_IN_FRONTIER", fmt(p), "class %s" % fmt(key)))
                    continue
                is_done = sh in done
            else:
                sh, is_done = None, p in seen_prefix
            if not is_done:
                n_pend += 1
                if sh is not None:
                    pending_shards.add(sh)
                continue
            n_done += 1
            for seq in seqs:
                if seq in got[p]:
                    rows_ok += 1
                else:
                    problems.append(("MISSING_ROW", fmt(seq), "prefix %s, shard %s, class %s"
                                     % (fmt(p), sh, fmt(key))))
        report.append(dict(key=fmt(key), antisum=pr["antisum"], orbit=pr["orbit"],
                           multisets=pr["multisets"], rows=len(pr["rows"]),
                           prefixes=len(pr["by_prefix"]), prefixes_done=n_done,
                           prefixes_pending=n_pend, rows_verified=rows_ok,
                           rows_observed=len(obs.get(key, [])),
                           pending_shards=sorted(pending_shards)))
        if args.emit:
            out = pathlib.Path(args.emit)
            out.mkdir(parents=True, exist_ok=True)
            order = sorted(pr["rows"], key=lambda r: (fidx.get(fmt(r[1][:args.level]), -1), r[1]))
            stem = "class_%d_%s" % (pr["antisum"], "-".join(map(str, key[:6])))
            (out / (stem + ".txt")).write_text("".join("%d,%s\n" % (s, fmt(q)) for s, q in order))
            (out / (stem + ".json")).write_text(json.dumps(dict(
                class_key=list(key), antisum=pr["antisum"], orbit=pr["orbit"],
                prefixes=[dict(prefix=fmt(p), shard=shard_of(p), frontier_index=fidx.get(fmt(p)),
                               rows=len(s)) for p, s in sorted(pr["by_prefix"].items(),
                                                                key=lambda kv: fidx.get(fmt(kv[0]), -1))]),
                indent=1) + "\n")
    return report


def summarize(report, problems, args):
    by_s = collections.defaultdict(lambda: collections.Counter())
    for r in report:
        c = by_s[r["antisum"]]
        c["classes"] += 1
        for k in ("rows", "rows_verified", "rows_observed", "prefixes", "prefixes_done"):
            c[k] += r[k]
    print()
    print("=== %d classes ===" % len(report))
    for s in sorted(by_s):
        c = by_s[s]
        print("  antisum %d: %d classes; %d of %d predicted rows verified in finished shards; "
              "%d of %d prefixes finished" % (s, c["classes"], c["rows_verified"], c["rows"],
                                             c["prefixes_done"], c["prefixes"]))
    if len(report) <= 20:
        for r in report:
            print("  class %s (antisum %d, orbit %d): %d rows, %d multisets, %d prefixes; "
                  "%d prefixes finished, %d rows verified; %d prefixes pending%s"
                  % (r["key"], r["antisum"], r["orbit"], r["rows"], r["multisets"], r["prefixes"],
                     r["prefixes_done"], r["rows_verified"], r["prefixes_pending"],
                     " in shards %s" % r["pending_shards"][:12] + ("..." if len(r["pending_shards"]) > 12 else "")
                     if r["pending_shards"] else ""))
    kinds = collections.Counter(p[0] for p in problems)
    if problems:
        print("=== %d PROBLEMS: %s ===" % (len(problems), dict(kinds)))
        for p in problems[:25]:
            print("  %-24s %s  %s" % p)
        if len(problems) > 25:
            print("  ... %d more in the report" % (len(problems) - 25))
    else:
        print("=== no problems: every finished shard holds exactly its predicted rows ===")
    if args.report:
        pathlib.Path(args.report).write_text(json.dumps(dict(
            version=VERSION, nshards=args.nshards, level=args.level, survmax=args.survmax,
            frontier=args.frontier, classes=report, problems=[list(p) for p in problems]),
            indent=1) + "\n")
        print("wrote %s" % args.report)
    return kinds


# ----------------------------------------------------------------- selftest
def selftest(args):
    t0 = time.time()
    co_ = build()
    print("=== group ===")
    print("  S_7 x <rev>: %d maps; Stab(0) without identity: %d" % (len(co_["G"]), len(co_["stab"])))
    print("=== the (7,7) gate, from the same rule code ===")
    lev = 7 if args.full_gate else 5
    got = enumerate_tree(7, lev, staircase(7, 7))
    print("  levels 1..%d: %s" % (lev, got))
    print("  C reference: %s" % GATE77[:lev])
    if got != GATE77[:lev]:
        sys.exit("gate FAILED: the port does not reproduce search.c")
    B = staircase(M, N)
    print("=== the 219 class ===")
    print("  (11,7) staircase %s" % [B[k] for k in range(M, 1, -1)])
    pr = predict_class((CLASS219, B, 221, 5))
    tot = dict(orbit=pr["orbit"], multisets=pr["multisets"], rows=len(pr["rows"]),
               prefixes=len(pr["by_prefix"]))
    print("  %s" % tot)
    if tot != CLASS219_TOTALS:
        sys.exit("219 class totals changed: want %s" % CLASS219_TOTALS)
    for p, n in CLASS219_SEEN.items():
        if len(pr["by_prefix"].get(p, [])) != n:
            sys.exit("prefix %s: want %d rows" % (fmt(p), n))
    print("  the four prefixes a real run wrote carry 12, 7, 4, 3 rows, as observed")

    print("=== fault injection on synthetic runs ===")
    rng = random.Random(args.seed)
    tmp = pathlib.Path(args.tmp)
    nsh = 16
    prefixes = list(pr["by_prefix"])
    filler = ["0,1,2,3,%d" % (1000 + i) for i in range(300)]
    lines = [fmt(p) for p in prefixes] + filler
    rng.shuffle(lines)
    idx = {s: i for i, s in enumerate(lines)}
    finished = set(rng.sample(range(nsh), nsh // 2))

    def make_run(name, fault):
        d = tmp / name
        if d.exists():
            for f in d.iterdir():
                f.unlink()
        d.mkdir(parents=True, exist_ok=True)
        (d / "frontier.txt").write_text("".join(s + "\n" for s in lines))
        per = collections.defaultdict(list)
        for s, seq in pr["rows"]:
            sh = idx[fmt(seq[:5])] % nsh
            if sh in finished:
                per[sh].append((s, seq))
        fin = sorted(finished)
        big = max(per, key=lambda k: len(per[k]))             # a finished shard with rows
        if fault == "drop_row":
            # drop one row from a prefix that keeps others, so the loss is
            # visible even without the frontier
            byp = collections.Counter(q[:5] for _, q in per[big])
            i = next(i for i, (_, q) in enumerate(per[big]) if byp[q[:5]] >= 2)
            per[big].pop(i)
        elif fault == "extra_row":
            pred_set = {q for _, q in pr["rows"]}
            s, seq = per[big][0]
            bogus = next(b for b in ((seq[0],) + p for p in itertools.permutations(seq[1:]))
                         if b not in pred_set)                    # same multiset, not canonical
            per[big].append((s, bogus))
        elif fault == "c_dropped":
            # the search itself loses a whole prefix: the certificate and the
            # low file agree with each other and are both short
            gone = per[big][0][1][:5]
            per[big] = [x for x in per[big] if x[1][:5] != gone]
        elif fault == "misfile":
            b = next(k for k in fin if k != big)
            per[b].append(per[big].pop(0))
        for sh in fin:
            r = per.get(sh, [])
            hist = dict(collections.Counter(s for s, _ in r))
            cert = dict(shard=sh, complete=True, below_top_rung=len(r),
                        antisum_histogram={str(k): v for k, v in hist.items()})
            if fault == "drop_row" or fault == "extra_row" or fault == "misfile":
                # the certificate is what the C would have written for the TRUE rows
                true = [x for x in pr["rows"] if idx[fmt(x[1][:5])] % nsh == sh]
                th = collections.Counter(s for s, _ in true)
                cert.update(below_top_rung=len(true),
                            antisum_histogram={str(k): v for k, v in th.items()})
            if fault == "bad_cert" and sh == big:
                cert["antisum_histogram"] = {str(r[0][0]): len(r) + 1}
            (d / ("sh_m11_L5_%dof%d.json" % (sh, nsh))).write_text(json.dumps(cert))
            if r and not (fault == "no_low" and sh == big):
                rr = r[:]
                rng.shuffle(rr)
                (d / ("low_%d.txt" % sh)).write_text("".join("%d,%s\n" % (s, fmt(q)) for s, q in rr))
        return d

    cases = [("clean", None, set()),
             ("drop_row", "drop_row", {"MISSING_ROW", "CERT_LOW_MISMATCH"}),
             ("extra_row", "extra_row", {"EXTRA_ROW", "CERT_LOW_MISMATCH"}),
             ("misfile", "misfile", {"MISFILED_ROW", "CERT_LOW_MISMATCH"}),
             ("no_low", "no_low", {"LOW_FILE_MISSING", "MISSING_ROW"}),
             ("c_dropped", "c_dropped", {"MISSING_ROW"}),
             ("bad_cert", "bad_cert", {"CERT_LOW_MISMATCH"})]
    for name, fault, want in cases:
        d = make_run(name, fault)
        for use_frontier in (True, False):
            ns = argparse.Namespace(runs=[str(d)], frontier=str(d / "frontier.txt") if use_frontier else None,
                                    cls=[fmt(CLASS219)], all=False, nshards=nsh, level=5,
                                    survmax=221, top=-1, jobs=1, emit=None, report=None)
            probs = []
            rep = run_check(ns, probs, quiet=True)
            kinds = {p[0] for p in probs}
            # without the frontier, a misfile looks clean and a missing file
            # hides whichever prefixes it alone carried -- that is the point
            # of --frontier, so only require what is visible
            need = want if use_frontier else {k for k in want if k not in ("MISFILED_ROW",)}
            if fault == "no_low" and not use_frontier:
                need = {"LOW_FILE_MISSING"}
            if fault == "misfile" and not use_frontier:
                need = {"CERT_LOW_MISMATCH"}
            if fault == "c_dropped" and not use_frontier:
                need = set()          # invisible without the frontier: the documented blind spot
            ok = need <= kinds and (fault or not kinds) and (need or fault != "c_dropped" or not kinds)
            print("  %-10s frontier=%-5s caught %-60s %s"
                  % (name, use_frontier, sorted(kinds) or "nothing", "ok" if ok else "FAILED"))
            if not ok:
                sys.exit("fault injection failed: wanted %s" % sorted(need))
            if name == "clean" and use_frontier:
                r = rep[0]
                if r["rows_verified"] != sum(len(s) for p, s in pr["by_prefix"].items()
                                             if idx[fmt(p)] % nsh in finished):
                    sys.exit("clean run: verified-row count is wrong")
    print("selftest passed in %.1f s" % (time.time() - t0))


# ------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="*", default=[], help="directories holding low_*.txt and sh_*.json")
    ap.add_argument("--frontier", help="the frontier file the shards were dealt from")
    ap.add_argument("--class", dest="cls", action="append", metavar="V0,...,V10",
                    help="check this class (any member, as 11 vertex indices); repeatable")
    ap.add_argument("--all", action="store_true", help="discover and check every class written")
    ap.add_argument("--emit", metavar="DIR", help="write each class's expected rows and prefix map")
    ap.add_argument("--report", metavar="FILE", help="write the full report as JSON")
    ap.add_argument("--nshards", type=int, default=2400)
    ap.add_argument("--level", type=int, default=5)
    ap.add_argument("--survmax", type=int, default=221)
    ap.add_argument("--top", type=int, default=-1, help="the sweep's -top, if it set one")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--build-frontier", metavar="FILE",
                    help="regenerate the (11,7) frontier in the C's order; compare with --frontier")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--full-gate", action="store_true", help="selftest: all seven gate levels (~4 min)")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--tmp", default="/tmp/zpredict_selftest")
    args = ap.parse_args()

    t0 = time.time()
    build()
    print("%s: CO_7 and S_7 x <rev> built in %.1f s" % (VERSION, time.time() - t0), flush=True)
    if args.selftest:
        selftest(args)
        return
    if args.build_frontier:
        B = staircase(M, N, args.top)
        t0 = time.time()
        with open(args.build_frontier, "w") as f:
            counts = enumerate_tree(M, args.level, B, emit=lambda ch: f.write(fmt(ch) + "\n"))
        print("frontier: %d prefixes at level %d in %.0f s; level counts %s"
              % (counts[-1], args.level, time.time() - t0, counts))
        if args.frontier:
            n, first = 0, None
            with open(args.build_frontier) as a, open(args.frontier) as b:
                bl = (l for l in b if l[:1] not in ("\n", "\0", ""))
                for la, lb in itertools.zip_longest(a, bl):
                    if la != lb:
                        first = (n, la, lb)
                        break
                    n += 1
            if first:
                sys.exit("frontiers DIFFER at line %d: ours %r, file %r" % first)
            print("identical to %s, line for line (%d lines): the shard mapping is pinned" % (args.frontier, n))
        if not args.runs:
            return
    if not args.runs:
        sys.exit("nothing to check: give --runs, or use --selftest / --build-frontier")
    if not (args.cls or args.all):
        sys.exit("say which classes: --class V0,...,V10 (repeatable) or --all")
    problems = []
    report = run_check(args, problems)
    kinds = summarize(report, problems, args)
    sys.exit(1 if kinds else 0)


if __name__ == "__main__":
    main()

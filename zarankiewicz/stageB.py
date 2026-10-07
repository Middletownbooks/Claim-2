#!/usr/bin/env python3
"""Stage B of the Theorem 6(c) sweep: every (11,7)-set of antisum 223 has a
non-pseudo-tight (4,7)-subset.  See THEOREM6C_SWEEP.md.

Why only antisum 223 here.  A leaf of antisum T is settled once T + 2*tau >= 225.
Stage A (`c/ptcheck -need`) settles every row of antisum 219 and 221 on disk
(53,514,110 rows, the completed top-221 sweep).  At T = 223 the leaf needs only
tau >= 1, i.e. ONE non-pseudo-tight (4,7)-subset, so the search can cut a node at
its first non-PT 4-subset: tau is monotone down the tree, and a node with tau >= 1
can only lead to leaves that are either settled (T = 223) or on disk (T <= 221).
That is `zsearch6c -tmin 223`, which sets the transversal budget to zero.

THE FRONTIER is the level-5 nodes of the ordinary search with all five of their
(4,7)-subsets pseudo-tight -- 1,023,412 of the 6,655,827 level-5 prefixes --
written by `zsearch6c -tmin 223 -d 5 -dump`, deterministic, md5 checked below.
Shard i is lines i mod NSHARDS, as in sweep.py.

Each shard writes stageB/sh_<i>.json LAST, after checking that the survivor file
agrees with the histogram; its presence is what certifies the shard.  Survivors,
if any, go to stageB/surv_<i>.txt -- those would be antisum-223 sets that Theorem
6(c) does not settle, which is the finding that matters either way.

    python3 stageB.py                 # run shards until the wall budget
    python3 stageB.py summary         # aggregate the certificates
"""
import hashlib, json, os, pathlib, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE / "c" / "zsearch6c"
FRONTIER = HERE / "runs" / "frontierB_m11_L5.txt"
FRONTIER_MD5 = "a09fbd77f749f5c2f8248a7d6b22f272"
FRONTIER_LINES = 1023412
OUT = HERE / "stageB"
NSHARDS = int(os.environ.get("NSHARDS", "256"))
THREADS = int(os.environ.get("THREADS", "0")) or (os.cpu_count() or 1)
WALL = float(os.environ.get("WALL", "5400"))
FIRST = int(os.environ.get("FIRST", "0"))
UPTO = int(os.environ.get("UPTO", str(NSHARDS)))
CHECK = os.environ.get("CHECK", "") == "1"      # re-verify every PT verdict (slower)


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def ensure_frontier():
    if not FRONTIER.exists():
        r = subprocess.run([str(EXE), "-m", "11", "-n", "7", "-tmin", "223", "-d", "5",
                            "-dump", str(FRONTIER)], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("frontier generation failed: " + r.stderr[-500:])
    got = md5(FRONTIER)
    n = sum(1 for _ in open(FRONTIER))
    assert got == FRONTIER_MD5 and n == FRONTIER_LINES, ("frontier mismatch", got, n)


def done_shards():
    d = set()
    for p in OUT.glob("sh_*.json"):
        try:
            j = json.loads(p.read_text())
            if j.get("complete") and j.get("of") == NSHARDS:
                d.add(int(p.stem.split("_")[1]))
        except Exception:
            pass
    return d


def run_shard(i):
    part = OUT / ("surv_%d.txt.partial" % i)
    final = OUT / ("surv_%d.txt" % i)
    t0 = time.time()
    cmd = [str(EXE), "-m", "11", "-n", "7", "-tmin", "223",
           "-startfile", str(FRONTIER), "-shard", str(i), "-of", str(NSHARDS),
           "-threads", str(THREADS), "-survivors", str(part)]
    if CHECK:
        cmd.append("-check")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:])
        sys.exit("shard %d failed" % i)
    d = json.loads(r.stdout)
    nsurv = d["survivors"]
    written = sum(1 for _ in open(part)) if part.exists() else 0
    assert written == nsurv, ("survivor file disagrees with the count", written, nsurv)
    assert sum(d["survivor_histogram"].values()) == nsurv
    if nsurv == 0:
        part.unlink(missing_ok=True)
        final.unlink(missing_ok=True)
    else:
        part.replace(final)
    rec = dict(shard=i, of=NSHARDS, m=11, n=7, top=d["top"], tmin=d["tmin"], taucap=d["taucap"],
               check=d["check"], frontier_md5=FRONTIER_MD5, complete=True,
               prefixes_done=d["prefixes_done"], visited=d["visited"], kept=d["kept"],
               cut_by_6c=d["cut_by_6c"], total_visited=d["total_visited"],
               survivors=nsurv, survivor_histogram=d["survivor_histogram"],
               pt_calls=d["pt_calls"], cache_hits=d["cache_hits"],
               core_seconds=d["core_seconds"], elapsed_s=d["elapsed_s"], threads=d["threads"],
               wall_s=round(time.time() - t0, 2))
    (OUT / ("sh_%d.json" % i)).write_text(json.dumps(rec) + "\n")
    return rec


def summarise():
    sh = sorted(done_shards())
    tot = dict(shards_done=len(sh), of=NSHARDS, prefixes=0, visited=0, survivors=0,
               pt_calls=0, core_seconds=0.0)
    for i in sh:
        d = json.loads((OUT / ("sh_%d.json" % i)).read_text())
        tot["prefixes"] += d["prefixes_done"]
        tot["visited"] += d["total_visited"]
        tot["survivors"] += d["survivors"]
        tot["pt_calls"] += d["pt_calls"]
        tot["core_seconds"] += d["core_seconds"]
    tot["core_seconds"] = round(tot["core_seconds"], 1)
    return tot


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    if sys.argv[1:2] == ["summary"]:
        print(json.dumps(summarise(), indent=2))
        sys.exit(0)
    ensure_frontier()
    done = done_shards()
    print("stage B: %d shards, %d complete, %d threads, wall budget %.0f s"
          % (NSHARDS, len(done), THREADS, WALL), flush=True)
    t0 = time.time()
    for i in range(FIRST, min(UPTO, NSHARDS)):
        if i in done:
            continue
        if time.time() - t0 > WALL:
            print("wall budget reached before shard %d" % i, flush=True)
            break
        rec = run_shard(i)
        s = summarise()
        print("  shard %3d: %5d prefixes, %11d nodes, %d survivors, %6.1f s wall  |  %d/%d done, %d survivors so far"
              % (i, rec["prefixes_done"], rec["total_visited"], rec["survivors"], rec["wall_s"],
                 s["shards_done"], NSHARDS, s["survivors"]), flush=True)
    print(json.dumps(summarise(), indent=2))

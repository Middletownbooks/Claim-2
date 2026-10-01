#!/usr/bin/env python3
"""The (11,7) sweep, in durable shards.

SPLIT LEVEL 5, NOT 4, and the reason is measured.  At level 4 there are 82,512
prefixes and the largest subtree under one of them runs for twenty minutes on a
single thread, so every shard ends with a tail the other three cores sit out:
shard 0 used 1.88 of 4 cores and shard 3 was at 1.00 after forty minutes.  At
level 5 there are 6,655,827 prefixes, eighty times finer, and the same work used
3.84 of 4 cores.  The restructure is gated: the level-5 units descending from
level-4 shard 0 reproduce its level counts, its leaf count and its antisum
histogram exactly.

HONEST SIZE, up front.  The tree is 1.0510e13 nodes and the clean rate is
1,821,979 nodes/core-second, so the sweep is ~1,602 core-hours = 16.7 DAYS on
four cores.  A background job here caps at two hours and this container reset
once already today, so a cycle of ~110 minutes completes about 0.46 PERCENT of
it.  Finishing here would take roughly 219 such cycles.  THIS SCRIPT IS
THEREFORE NOT A WAY TO FINISH; it is a way to make every cycle's work permanent
and resumable, here or on any other machine, and to validate the production path
at real depth.

WHAT IT STORES, and why not everything.  The first three completed shards
emitted 180,051,156 leaves, 2.3 GB per shard, and 99.989 percent of them sit at
the TOP RUNG, antisum 223.  Storing every survivor would be terabytes, and
merely WRITING them cost 27 percent of core-seconds and 1.22x of wall --
measured by running the same work three ways rather than inferred.  So each
shard keeps:
  * the FULL antisum histogram, which is a few bytes and is the headline;
  * the FULL list of survivors BELOW the top rung -- MEASURED at 0.0109 percent
    over the first three completed shards, 19,681 of 180,051,156 leaves, all of
    them at antisum 221 and none lower -- which are the sets furthest under
    Z(11)Z(7) = 225 and the most interesting;
  * nothing else, because a shard is deterministic given its index and the
    top-rung list is regenerable on demand.

Idempotent per shard, so a session killed by the wall clock loses at most one.
"""
import json, os, pathlib, subprocess, sys, time
import collections

HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE / "c" / "zsearch"
FRONTIER = HERE / "runs" / ("frontier_m11_L%d.txt" % int(__import__("os").environ.get("LEVEL", "5")))
OUT = HERE / ("sweep" + os.environ.get("OUT_SUFFIX", "_L%d" % int(os.environ.get("LEVEL", "5"))))

M, N = 11, 7
LEVEL = int(os.environ.get("LEVEL", "5"))
NSHARDS = int(os.environ.get("NSHARDS", "2400"))
OUT_SUFFIX = os.environ.get("OUT_SUFFIX", "_L%d" % LEVEL)
TOP_RUNG = 223                      # B[11]; parity makes the rungs odd
THREADS = int(os.environ.get("THREADS", "0")) or (os.cpu_count() or 1)
WALL = float(os.environ.get("WALL", "4800"))    # stop STARTING shards after this;
                                               # the job cap is ~7,080 s, so this leaves
                                               # 38 minutes for a skewed shard to finish
                                               # rather than be killed mid-flight
FIRST = int(os.environ.get("FIRST", "0"))

OUT.mkdir(exist_ok=True)

def done_shards():
    d = set()
    for p in OUT.glob("sh_*.json"):
        try:
            if json.loads(p.read_text()).get("complete"):
                d.add(int(p.stem.split("_")[1]))
        except Exception:
            pass
    return d

def run_shard(i):
    """One shard.  The C now accumulates the antisum histogram itself and writes
    only survivors at or below TOP_RUNG - 2, so the 99.989 percent of leaves that
    sit at the top rung never touch a file or a mutex.  The first cycle wrote all
    of them -- 54 to 72 million per shard, 2.3 GB, under a lock -- and it cost 45
    percent of throughput to extract a few thousand useful lines."""
    low = OUT / ("low_%d.txt" % i)
    t0 = time.time()
    r = subprocess.run([str(EXE), "-m", str(M), "-n", str(N),
                        "-startfile", str(FRONTIER), "-shard", str(i), "-of", str(NSHARDS),
                        "-threads", str(THREADS),
                        "-survmax", str(TOP_RUNG - 2), "-survivors", str(low)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:]); sys.exit("shard %d failed" % i)
    d = json.loads(r.stdout)
    assert not d["aborted"], "shard %d aborted; counts would be invalid" % i
    hist = {int(k): v for k, v in d["antisum_histogram"].items()}
    assert sum(hist.values()) == d["leaves"], (sum(hist.values()), d["leaves"])
    nlow = sum(v for k, v in hist.items() if k <= TOP_RUNG - 2)
    written = sum(1 for _ in open(low)) if low.exists() else 0
    assert written == nlow, ("survivor file disagrees with the histogram", written, nlow)
    if nlow == 0 and low.exists():
        low.unlink()
    rec = dict(shard=i, of=NSHARDS, m=M, n=N, level=LEVEL, complete=True,
               prefixes_done=d["prefixes_done"], level_counts=d["level_counts"],
               total_nodes=d["total_nodes"], leaves=d["leaves"],
               elapsed_s=round(d["elapsed_s"], 2), core_seconds=round(d["core_seconds"], 2),
               nodes_per_core_s=d["nodes_per_core_s"], threads=d["threads"],
               antisum_histogram={str(k): v for k, v in sorted(hist.items())},
               below_top_rung=nlow, wall_s=round(time.time() - t0, 2))
    (OUT / ("sh_%d.json" % i)).write_text(json.dumps(rec) + "\n")
    return rec

def summarise():
    tot = [0] * (M + 2)
    hist = collections.Counter()
    nodes = leaves = 0
    cs = 0.0
    sh = sorted(done_shards())
    for i in sh:
        d = json.loads((OUT / ("sh_%d.json" % i)).read_text())
        for k, v in enumerate(d["level_counts"], start=1):
            tot[k] += v
        nodes += d["total_nodes"]; leaves += d["leaves"]; cs += d["core_seconds"]
        for a, c in d["antisum_histogram"].items():
            hist[int(a)] += c
    return dict(shards_done=len(sh), of=NSHARDS, nodes=nodes, leaves=leaves,
                core_seconds=round(cs, 1), level_counts=tot,
                antisum_histogram={str(k): v for k, v in sorted(hist.items())})

if __name__ == "__main__":
    if sys.argv[1:2] == ["summary"]:
        print(json.dumps(summarise(), indent=2)); sys.exit(0)
    EST = 1.0510e13
    NPREFIX = sum(1 for _ in open(FRONTIER))
    done = done_shards()
    print("sweep: %d shards of ~%d prefixes; %d already complete; %d threads; wall budget %.0f s"
          % (NSHARDS, NPREFIX // NSHARDS, len(done), THREADS, WALL), flush=True)
    t0 = time.time()
    n = 0
    for i in range(FIRST, NSHARDS):
        if i in done:
            continue
        if time.time() - t0 > WALL:
            print("wall budget reached before shard %d" % i, flush=True)
            break
        rec = run_shard(i)
        n += 1
        s = summarise()
        print("  shard %4d: %5d prefixes, %13d nodes, %9d leaves (%4d below %d), "
              "%6.1f s wall, %8.0f nodes/core-s  |  cumulative %.4e nodes = %.3f%% of the estimate"
              % (i, rec["prefixes_done"], rec["total_nodes"], rec["leaves"],
                 rec["below_top_rung"], TOP_RUNG, rec["wall_s"], rec["nodes_per_core_s"],
                 s["nodes"], 100 * s["nodes"] / EST), flush=True)
    s = summarise()
    print()
    print("=== session: %d shards this run, %d of %d complete ===" % (n, s["shards_done"], NSHARDS))
    print(json.dumps(s, indent=2))

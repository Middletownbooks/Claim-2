#!/usr/bin/env python3
"""The (11,7) sweep, in durable shards.

HONEST SIZE, up front.  The tree is 1.0510e13 nodes and the clean rate is
1,821,979 nodes/core-second, so the sweep is ~1,602 core-hours = 16.7 DAYS on
four cores.  A background job here caps at two hours and this container reset
once already today, so a cycle of ~110 minutes completes about 0.46 PERCENT of
it.  Finishing here would take roughly 219 such cycles.  THIS SCRIPT IS
THEREFORE NOT A WAY TO FINISH; it is a way to make every cycle's work permanent
and resumable, here or on any other machine, and to validate the production path
at real depth.

WHAT IT STORES, and why not everything.  One completed shard of 34 prefixes
emitted 668,158 survivors and 28 MB of text, and 99.94 percent of them sit at
the TOP RUNG, antisum 223.  Storing every survivor would be terabytes.  So each
shard keeps:
  * the FULL antisum histogram, which is a few bytes and is the headline;
  * the FULL list of survivors BELOW the top rung -- 0.064 percent of them,
    which are the sets furthest under Z(11)Z(7) = 225 and the most interesting;
  * nothing else, because a shard is deterministic given its index and the
    top-rung list is regenerable on demand.

Idempotent per shard, so a session killed by the wall clock loses at most one.
"""
import json, os, pathlib, subprocess, sys, time
import collections

HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE / "c" / "zsearch"
FRONTIER = HERE / "runs" / "frontier_m11_L4.txt"
OUT = HERE / "sweep"
TMP = pathlib.Path(os.environ.get("TMPDIR", "/tmp")) / "sweep_tmp"

M, N, LEVEL = 11, 7, 4
NSHARDS = int(os.environ.get("NSHARDS", "2400"))
TOP_RUNG = 223                      # B[11]; parity makes the rungs odd
THREADS = int(os.environ.get("THREADS", "0")) or (os.cpu_count() or 1)
WALL = float(os.environ.get("WALL", "6300"))    # stop STARTING shards after this
FIRST = int(os.environ.get("FIRST", "0"))

OUT.mkdir(exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

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
    sfile = TMP / ("surv_%d.txt" % i)
    t0 = time.time()
    r = subprocess.run([str(EXE), "-m", str(M), "-n", str(N),
                        "-startfile", str(FRONTIER), "-shard", str(i), "-of", str(NSHARDS),
                        "-threads", str(THREADS), "-survivors", str(sfile)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-800:]); sys.exit("shard %d failed" % i)
    d = json.loads(r.stdout)
    assert not d["aborted"], "shard %d aborted; counts would be invalid" % i
    hist = collections.Counter()
    low = []
    with open(sfile) as f:
        for line in f:
            a = int(line.split(",", 1)[0])
            hist[a] += 1
            if a < TOP_RUNG:
                low.append(line.rstrip("\n"))
    sfile.unlink()
    rec = dict(shard=i, of=NSHARDS, m=M, n=N, level=LEVEL, complete=True,
               prefixes_done=d["prefixes_done"], level_counts=d["level_counts"],
               total_nodes=d["total_nodes"], leaves=d["leaves"],
               elapsed_s=round(d["elapsed_s"], 2), core_seconds=round(d["core_seconds"], 2),
               nodes_per_core_s=d["nodes_per_core_s"], threads=d["threads"],
               antisum_histogram={str(k): v for k, v in sorted(hist.items())},
               below_top_rung=len(low), wall_s=round(time.time() - t0, 2))
    assert sum(hist.values()) == d["leaves"], (sum(hist.values()), d["leaves"])
    (OUT / ("sh_%d.json" % i)).write_text(json.dumps(rec) + "\n")
    if low:
        (OUT / ("low_%d.txt" % i)).write_text("\n".join(low) + "\n")
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
    done = done_shards()
    print("sweep: %d shards of ~%d prefixes; %d already complete; %d threads; wall budget %.0f s"
          % (NSHARDS, 82512 // NSHARDS, len(done), THREADS, WALL), flush=True)
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

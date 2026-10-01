#!/usr/bin/env python3
"""The clean uncontended throughput measurement.

EVERY (11,7) RATE RECORDED BEFORE THIS ONE WAS CONTENDED -- measured with other
jobs on the same four cores, at varying and unrecorded levels.  The gated COUNTS
were exact regardless, but the rates carried that noise, and the budget verdict
rests on a rate.  2,321-2,759 core-hours against a 2,880 budget is a 12 percent
margin, which is not something to take from a contaminated measurement.

METHOD, and the three things it does differently:
  1. SEQUENTIAL.  One configuration at a time, nothing else running.  The load
     average is recorded before each run so a dirty measurement is visible
     rather than silent.
  2. A FIXED WORK QUANTUM, not a time cap.  Every configuration processes the
     SAME 384 prefixes to completion, so the thread counts are compared on
     identical work.  A time cap would compare different amounts of it.
  3. REPEATS.  Two passes, so run-to-run spread is reported instead of assumed
     away.  On shared cloud silicon the spread is the honest error bar.
"""
import json, os, pathlib, re, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
EXE = HERE / "c" / "zsearch"
WORK = HERE / "runs" / "bench_384.txt"
PASSES = int(os.environ.get("PASSES", "2"))

def loadavg():
    return float(open("/proc/loadavg").read().split()[0])

def run(args, label):
    la0 = loadavg()
    t0 = time.time()
    r = subprocess.run([str(EXE)] + args, capture_output=True, text=True)
    wall = time.time() - t0
    if r.returncode != 0:
        print(r.stderr[-800:]); sys.exit("%s failed" % label)
    d = json.loads(r.stdout)
    d["_wall_outer"] = wall
    d["_load_before"] = la0
    return d

print("host: %d cpus, %s" % (os.cpu_count(),
      re.sub(r"\s+", " ", [l for l in open("/proc/cpuinfo") if "model name" in l][0].split(":")[1].strip())))
print("load before anything: %.2f" % loadavg())
print()

# ---- the gate first, uncontended, which is also the headline single-core timing
print("=== gate, uncontended, 3 repeats each ===")
gate = {"": [1, 13, 377, 29099, 801503, 14623179, 809438],
        "24": [1, 12, 329, 25346, 615817, 9827953, 809438]}
gate_out = {}
for thm7, want in gate.items():
    rows = []
    for i in range(3):
        a = ["-m", "7", "-n", "7"] + (["-thm7", thm7] if thm7 else [])
        d = run(a, "gate %s" % thm7)
        assert d["level_counts"] == want, (d["level_counts"], want)
        rows.append(d)
    el = [d["elapsed_s"] for d in rows]
    rate = [d["nodes_per_core_s"] for d in rows]
    gate_out[thm7 or "off"] = dict(elapsed_s=el, nodes_per_core_s=rate,
                                   total_nodes=rows[0]["total_nodes"])
    print("  thm7=%-3s counts exact; %s s  (spread %.1f%%); %s nodes/core-s"
          % (thm7 or "off", ["%.2f" % x for x in el], 100*(max(el)-min(el))/min(el),
             ["%d" % x for x in rate]))

# ---- the (11,7) scaling curve on a fixed work quantum
print()
print("=== (11,7), the SAME %d prefixes to completion, 1-4 threads, %d passes ==="
      % (sum(1 for _ in open(WORK)), PASSES))
curve = {}
for T in (1, 2, 3, 4):
    rows = []
    for p in range(PASSES):
        d = run(["-m", "11", "-n", "7", "-startfile", str(WORK), "-threads", str(T)], "T=%d" % T)
        assert not d["aborted"], "a run aborted: the quantum must complete"
        rows.append(d)
        print("    T=%d pass %d: wall %8.2f s  core %8.2f s  nodes %.4e  %8.0f nodes/core-s  (load before %.2f)"
              % (T, p, d["elapsed_s"], d["core_seconds"], d["total_nodes"],
                 d["nodes_per_core_s"], d["_load_before"]), flush=True)
    nodes = rows[0]["total_nodes"]
    assert all(r["total_nodes"] == nodes for r in rows), "the work quantum is not fixed"
    wall = min(r["elapsed_s"] for r in rows)
    core = min(r["core_seconds"] for r in rows)
    curve[T] = dict(wall_s=wall, core_s=core, nodes=nodes,
                    nodes_per_core_s=nodes/core, nodes_per_s=nodes/wall,
                    wall_spread_pct=100*(max(r["elapsed_s"] for r in rows)-wall)/wall)

print()
print("=== the curve ===")
one = curve[1]["nodes_per_core_s"]
w1 = curve[1]["wall_s"]
print("   T   wall s   core s   nodes/core-s   aggregate/s   speedup   per-core eff   wall spread")
for T in (1, 2, 3, 4):
    c = curve[T]
    print("   %d  %7.1f  %7.1f   %12.0f   %11.0f   %6.2fx   %11.0f%%   %8.1f%%"
          % (T, c["wall_s"], c["core_s"], c["nodes_per_core_s"], c["nodes_per_s"],
             w1/c["wall_s"], 100*c["nodes_per_core_s"]/one, c["wall_spread_pct"]))

EST, LO, HI = 1.0510e13, 9.605e12, 1.1416e13
BUDGET = 2880
print()
print("=== the budget, at each core count, against P-43(A)'s %d core-hours ===" % BUDGET)
for T in (1, 2, 3, 4):
    r = curve[T]["nodes_per_core_s"]
    ch = [e/r/3600 for e in (LO, EST, HI)]
    print("   T=%d  %5.0f / %5.0f / %5.0f core-hours (95%% lo/point/hi)   %5.1f days on %d cores   %s"
          % (T, ch[0], ch[1], ch[2], ch[1]/T/24, T,
             "inside" if ch[2] < BUDGET else ("STRADDLES" if ch[0] < BUDGET else "OVER")))
best = min(curve, key=lambda T: EST/curve[T]["nodes_per_core_s"])
print()
print("   CORE-HOURS ARE MINIMISED AT T=%d, not at T=4: %0.0f against %0.0f."
      % (best, EST/curve[best]["nodes_per_core_s"]/3600, EST/curve[4]["nodes_per_core_s"]/3600))
print("   Wall clock is minimised at T=4.  A core-hour budget and a deadline want")
print("   different thread counts, which is worth knowing before 50 sessions are booked.")

out = HERE / "runs" / "bench_clean.json"
out.write_text(json.dumps(dict(host_cpus=os.cpu_count(), passes=PASSES,
                               gate=gate_out, curve=curve,
                               estimate=dict(point=EST, lo=LO, hi=HI),
                               budget_core_hours=BUDGET), indent=2) + "\n")
print()
print("wrote %s" % out.name)

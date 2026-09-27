#!/usr/bin/env python3
"""Drive the n=11 symmetric search up the height ladder inside a stated budget.

Each height runs as a child process under an explicit address-space cap, so the failure mode is
a MemoryError this script can see and record -- not an OOM kill that takes the container with it
and leaves no evidence about WHY it stopped. PREREG_PTE11.md A-2 predicts memory rather than the
clock binds, and that prediction is only scorable if the stop reason is observed rather than
inferred.
"""
import argparse, json, os, resource, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))

CHILD = r'''
import json, os, resource, sys
resource.setrlimit(resource.RLIMIT_AS, (%d, %d))
sys.path.insert(0, %r)
import %s as searcher
try:
    r = searcher.search(11, %d, 5)
except MemoryError:
    print(json.dumps({"failed": "MemoryError"})); sys.exit(0)
r["peak_rss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 1)
json.dump(r, open(%r, "w"), indent=1)
print(json.dumps({k: v for k, v in r.items() if k != "solutions"}))
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--heights", default="20,24,28,32")
    ap.add_argument("--budget", type=int, default=3600, help="seconds for the whole ladder")
    ap.add_argument("--mem-gb", type=float, default=10.0)
    ap.add_argument("--module", default="search_symmetric",
                    help="search_symmetric (registered) or search_pattern (Corollary 21)")
    ap.add_argument("--log-name", default="RUN_LOG.json")
    ap.add_argument("--tag", default="n11")
    ap.add_argument("--prior-seconds", type=float, default=0.0,
                    help="budget already spent by an earlier segment of the same ladder")
    a = ap.parse_args()

    cap = int(a.mem_gb * 1024 ** 3)
    started = time.time() - a.prior_seconds        # the ladder's clock, not this segment's
    log = {"heights_attempted": [], "mem_cap_gb": a.mem_gb, "budget_seconds": a.budget,
           "prior_seconds": a.prior_seconds}
    stopped_by = "completed"
    for H in [int(h) for h in a.heights.split(",")]:
        left = a.budget - (time.time() - started)
        if left < 60:
            stopped_by, log["memory_headroom"] = "clock", True
            log["note"] = f"stopped before H={H}: {left:.0f}s of budget left"
            break
        out = os.path.join(HERE, "runs", f"{a.tag}_H{H}.json")
        print(f"\n=== H={H}  ({left:.0f}s of budget left) ===", flush=True)
        t0 = time.time()
        try:
            p = subprocess.run([sys.executable, "-c",
                                CHILD % (cap, cap, HERE, a.module, H, out)],
                               capture_output=True, text=True, timeout=left)
        except subprocess.TimeoutExpired:
            stopped_by, log["memory_headroom"] = "clock", True
            log["note"] = f"H={H} hit the clock after {time.time()-t0:.0f}s"
            print(log["note"], flush=True)
            break
        tail = (p.stdout or p.stderr or "").strip().splitlines()[-1:] or [""]
        print(tail[0][:400], flush=True)
        log["heights_attempted"].append({"H": H, "seconds": round(time.time() - t0, 1),
                                         "rc": p.returncode, "tail": tail[0][:200]})
        if p.returncode != 0 or '"failed"' in tail[0]:
            stopped_by, log["memory_headroom"] = "memory", False
            log["note"] = f"H={H} exhausted the {a.mem_gb} GB cap"
            print(log["note"], flush=True)
            break

    log["stopped_by"] = stopped_by
    log["budget_exhausted"] = (time.time() - started) >= a.budget - 60
    log["total_seconds"] = round(time.time() - started, 1)
    json.dump(log, open(os.path.join(HERE, "runs", a.log_name), "w"), indent=1)
    print("\n" + json.dumps(log, indent=1))


if __name__ == "__main__":
    main()

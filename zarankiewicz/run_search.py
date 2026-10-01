#!/usr/bin/env python3
"""THE POSITIVE CONTROL: complete the (7,7) enumeration once, end to end.

Attempted once on the producing side and abandoned at 10.18M nodes because its
container calls are 100-300 s.  This container runs a background job for two
hours.  Woodall's 1988 run took 4 hours on a Sun 4/110 and reported 13,448
nonisomorphic (7,7)-sets at antisum 79.  That pair -- our wall clock against his
four hours, our survivor count against his 13,448 -- is the only calibration
every cost estimate on this target has been resting on.

Run from the intake directory so the package imports resolve.
"""
import sys, time, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "intake"))
import numpy as np
from cog import CO, Z
from search import staircase, search

t0 = time.time()
G7 = CO(7)
D7 = G7.dist_matrix()
A7p = G7.antidist_matrix(D7)
A7 = np.array(A7p, dtype=np.int32)
stab7 = [m for m in G7.stabiliser() if m != list(range(G7.NV))]
print("setup %.1fs ; |stab \\ id| = %d" % (time.time() - t0, len(stab7)), flush=True)

M = int(sys.argv[2]) if len(sys.argv) > 2 else 7
CAP = float(sys.argv[3]) if len(sys.argv) > 3 else 5400.0
DEPTH = int(sys.argv[4]) if len(sys.argv) > 4 else None
THM7 = tuple(int(x) for x in (sys.argv[1].split(",") if len(sys.argv) > 1 else ["2", "4"]) if x)
B = staircase(M, 7)
print("m = %d ; staircase %s ; cap %.0fs" % (M, {k: B[k] for k in sorted(B, reverse=True)}, CAP), flush=True)
print("Theorem 7 exclusions applied: %s" % (THM7 or "none",), flush=True)

t1 = time.time()
counts, surv, el, aborted = search(G7, A7, A7p, stab7, M, B, thm7=THM7,
                                   depth=DEPTH, time_cap=CAP, collect=False)
tot = sum(counts)
res = dict(m=M, depth=DEPTH, thm7=list(THM7), level_counts=counts, leaves=counts[M], total_nodes=tot,
           elapsed_s=round(el, 1), aborted=aborted,
           nodes_per_s=round(tot / el) if el else None,
           woodall_hours=4.0, speedup_vs_woodall=round(4 * 3600 / el, 1) if el else None)
print(json.dumps(res, indent=2), flush=True)

print("\nagainst the relayed depth-5 figures:", flush=True)
relayed = {(2, 4): [1, 12, 329, 25346, 615817], (): [1, 13, 377, 29099, 801503]}
ref = relayed.get(THM7)
if ref:
    got = counts[1:6]
    print("   relayed %s" % ref, flush=True)
    print("   local   %s   %s" % (got, "MATCH" if got == ref else "DIFFER"), flush=True)
if not aborted and M == 7:
    print("\nagainst Woodall: he reported 13,448 nonisomorphic (7,7)-sets at antisum 79;", flush=True)
    print("   this run kept %d nodes at depth 7 (nodes, not classes -- the node-keep" % counts[M], flush=True)
    print("   predicate canonicalises only under Stab(v0), order 2n = 14).", flush=True)
    print("   nodes / Woodall's classes = %.3f" % (counts[M] / 13448), flush=True)
out = pathlib.Path(__file__).resolve().parent / ("run_m%d_thm7_%s%s.json" % (M, "-".join(map(str, THM7)) or "none", "_d%d" % DEPTH if DEPTH else ""))
out.write_text(json.dumps(res, indent=2) + "\n")
print("\nwrote %s ; total %.1fs" % (out.name, time.time() - t0), flush=True)

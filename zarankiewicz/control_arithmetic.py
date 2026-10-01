#!/usr/bin/env python3
"""Every figure RESULT_CONTROL.md prints, re-derived from the run's own output."""
import json, pathlib, sys

FAIL = []
def ck(label, got, want, tol=0.0):
    ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
    if not ok: FAIL.append(label)
    print(("  ok   " if ok else "  FAIL ") + "%-52s %s" % (label, got if ok else "%s (want %s)" % (got, want)))

# the completed (7,7) run, Theorem 7 on, as the driver wrote it
C = [0, 1, 12, 329, 25346, 615817, 9827953, 809438, 0]
EL, TOT, LEAVES = 397.0, 11278896, 809438
ck("level counts sum to the reported total", sum(C), TOT)
ck("the leaf level is counts[7]", C[7], LEAVES)
ck("depth-5 prefix matches the relayed figures", C[1:6], [1, 12, 329, 25346, 615817])

print()
print("1. the level-to-level ratios, and why my extrapolation failed")
r = [C[k + 1] / C[k] for k in range(1, 7)]
print("   " + "  ".join("%.3g" % x for x in r))
ck("the first four are the ratios I extrapolated from",
   [round(x, 1) for x in r[:4]], [12.0, 27.4, 77.0, 24.3])
ck("level 7 is SMALLER than level 6", C[7] < C[6], True)
ck("  ... by a factor of", round(C[6] / C[7], 1), 12.1)
my_est = C[5] * r[3] ** 2
print("   my estimate was 615,817 x 24.3^2 = %.3e" % my_est)
ck("my estimate overshoots the measured total by", round(my_est / TOT, 1), 32.2)
print("   CAUSE: the staircase is a DECREASING budget -- 79, 56, 36, 21, 9, 3 -- so the")
print("   top rung binds hardest, and the tree contracts at the last level instead of")
print("   growing.  A growth-ratio extrapolation cannot see that and I used one.")

print()
print("2. their stall, relocated")
ck("they stopped at 10.18M nodes, of a total of", TOT, 11278896)
ck("  ... which is this fraction of the whole run", round(10.18e6 / TOT, 3), 0.903)
ck("  ... i.e. seconds from completion", round(EL * (1 - 10.18e6 / TOT)), 39)

print()
print("3. the speedup over Woodall, which I had pessimistic by at least 5x")
ck("Woodall's (7,7): 4 hours, in seconds", 4 * 3600, 14400)
ck("this run, seconds", EL, 397.0)
ck("so the FLOOR on the speedup", round(4 * 3600 / EL, 1), 36.3)
print("   and that is a floor because it assumes Woodall traversed the SAME tree.")
ck("their leaf nodes per Woodall's 13,448 classes", round(LEAVES / 13448, 2), 60.19)
wood_tree = TOT / (LEAVES / 13448)
print("   if his canonical form was orbit-complete his tree was ~%.3e nodes," % wood_tree)
ck("  ... giving him nodes/s of about", round(wood_tree / 14400), 13)
ck("  ... and them a speedup over him of about", round(TOT / EL / (wood_tree / 14400)), 2183)
print("   SO THE SPEEDUP IS BETWEEN 36x AND ~2,200x.  My relayed-data estimate was")
print("   3-8x, derived by back-computing Woodall on a tree 32x too large.  The")
print("   5-10 month (11,7) figure that rested on it is void.")
ck("measured throughput, nodes/s (driver printed 28,408 off unrounded el)",
   round(TOT / EL), 28410)

print()
print("4. P-44(D): does the corrected tree move by more than 2x?")
ck("|log ratio| exceeds the 2x threshold", my_est / TOT > 2, True)
print("   (D) TRUE at 32x, and in the direction I explicitly declined to predict.")
print("   Declining was right: an hour earlier I would have guessed LARGER.")

print()
print("5. the full-depth Theorem 7 ablation -- their open item 3, and the bigger result")
OFF = [0, 1, 13, 377, 29099, 801503, 14623179, 809438, 0]
EL_OFF, TOT_OFF = 186.1, 16263610
ck("OFF total nodes", sum(OFF), TOT_OFF)
ck("OFF depth-5 prefix matches the relayed figures", OFF[1:6], [1, 13, 377, 29099, 801503])
ck("LEAVES ARE IDENTICAL both ways", (C[7], OFF[7]), (809438, 809438))
print("     -> a correctness check on the prune: Theorem 7 may only remove interior")
print("        nodes that cannot reach a survivor, and it removed exactly those.")
ck("tree shrink from Theorem 7, FULL depth", round(TOT_OFF / TOT, 3), 1.442)
print("   (their depth-5 cumulative figure was 1.295x; at full depth it is 1.442x)")
ck("per-node cost of Theorem 7", round((TOT_OFF / EL_OFF) / (TOT / EL), 2), 3.08)
ck("NET WALL CLOCK: slower with it ON, by", round(EL / EL_OFF, 2), 2.13)
print("     -> THEOREM 7 IS NET NEGATIVE AT (7,7): it shrinks the tree 1.44x and")
print("        costs 3.08x per node.  The eight-round correspondence about whether")
print("        it survives at m = 11, and the 1.30x that moved H to PASS, were")
print("        about a prune that should be switched OFF.  At m = 11 its scan is")
print("        C(k-1,3) = 120 triples against 20 at m = 7, so its absence there")
print("        is a saving, not the cost the headroom argument priced in.")

print()
print("6. what the (9,7) probe says, and what it does not")
P9 = [0, 1, 13, 2131, 82308, 6540999]
ck("(9,7) to depth 5, Theorem 7 on, completed", P9[1:6], [1, 13, 2131, 82308, 6540999])
print("   per-level ratio against (7,7) ON:  " +
      "  ".join("L%d %.2fx" % (k, P9[k] / C[k]) for k in range(2, 6)))
print("   L3's 6.48x is independently expected: the orbit count of 3-element sets")
print("   jumps 280 -> 1710 as the bound moves 9 -> 11, a factor of 6.1.")
ck("(9,7) reaches depth 5 having visited this fraction of the WHOLE (7,7) tree",
   round(sum(P9) / TOT, 2), 0.59)
print("   with FOUR levels still to go, against (7,7)'s two.  So Woodall's own")
print("   1.5x wall-clock ratio from (7,7) to (9,7) does not transfer here.")
print("   NO POINT ESTIMATE IS OFFERED.  Extrapolating level ratios is exactly the")
print("   error that cost 32x in sec 1, and the top level contracts by a factor")
print("   nothing shallower predicts.  The bracket is in RESULT_CONTROL.md and the")
print("   number will be measured, not guessed.")

print()
print("FAILURES: %d" % len(FAIL) + ("" if not FAIL else " -> " + "; ".join(FAIL)))
sys.exit(1 if FAIL else 0)

#!/usr/bin/env python3
"""Run GATE_VALUES.json against an implementation.  Usage: python3 check_gate.py

With no argument it checks the received Python package, which should pass
everything.  It is written so that a C or Rust rewrite can be dropped in behind
the same three callables -- staircase(m, n), search(m, thm7, depth) returning
level counts, and the CO_7 graph -- and gated identically.

A rewrite that canonicalises MORE strongly than the received node-keep predicate
will not reproduce exact_level_counts, and that is not a failure: it must then
declare itself and be gated on the orbit counts and the leaf count instead,
which are predicate-independent.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "intake"))
import numpy as np
from cog import CO, Z
from search import staircase, search, thm7_availability

G = json.loads((pathlib.Path(__file__).resolve().parent / "GATE_VALUES.json").read_text())
FAIL = []
def ck(label, got, want):
    ok = got == want
    if not ok: FAIL.append(label)
    print(("  ok   " if ok else "  FAIL ") + "%-56s %s" % (label, got if ok else "%s (want %s)" % (got, want)))

print("gate values as of %s, provenance: %s" % (G["as_of"], G["provenance"].split(".")[0]))
print()
print("1. the graph")
C7 = CO(7)
ck("|V(CO_7)|", C7.NV, G["graph"]["CO_7_vertices"])
ck("degree", sorted({len(r) for r in C7.adj}), [G["graph"]["CO_7_degree"]])
ck("|relabel group|", len(C7.relabel_maps()), G["graph"]["relabel_group_order"])
ck("|relabel group| without reversal", len(C7.relabel_maps(False)),
   G["graph"]["relabel_group_order_without_reversal"])
ck("|Stab(v0)|", len(C7.stabiliser()), G["graph"]["stabiliser_of_a_vertex_order"])

print()
print("2. the staircases")
for key, m in (("m7", 7), ("m9", 9), ("m11", 11)):
    B = staircase(m, 7)
    ck("staircase(%d, 7)" % m, {str(k): v for k, v in B.items()}, G["staircases"][key])

print()
print("3. Theorem 7")
for key, m in (("m7", 7), ("m9", 9), ("m11", 11)):
    av = thm7_availability(m, 7)
    ck("Theorem 7 available at m=%d for m' in" % m,
       sorted(k for k, v in av.items() if v["exact"]), G["theorem_7"]["availability"][key])
ck("weakened bounds at m=11", {str(k): v["bound"] for k, v in thm7_availability(11, 7).items()},
   G["theorem_7"]["weakened_bounds_at_m11"])

print()
print("4. exact level counts (this is the slow part, ~11 min for all four)")
D7 = C7.dist_matrix(); A_py = C7.antidist_matrix(D7)
A_np = np.array(A_py, dtype=np.int32)
stab = [x for x in C7.stabiliser() if x != list(range(C7.NV))]
CASES = [("m7_thm7_2_4", 7, (2, 4), None), ("m7_thm7_none", 7, (), None),
         ("m9_thm7_none_to_depth_6", 9, (), 6), ("m11_thm7_none_to_depth_5", 11, (), 5)]
if "--fast" in sys.argv:
    CASES = [c for c in CASES if c[0] == "m11_thm7_none_to_depth_5"]
    print("   (--fast: only the 47-second case)")
for key, m, t7, dep in CASES:
    want = G["exact_level_counts"][key]
    cn, _, el, ab = search(C7, A_np, A_py, stab, m, staircase(m, 7), depth=dep, thm7=t7)
    ck("%s completed" % key, ab, False)
    top = dep if dep else m
    ck("%s levels" % key, cn[1:top + 1], want["levels"])
    ck("%s total" % key, sum(cn), want["total"])
    print("         (%.0f s here, %.0f s when first measured)" % (el, want["seconds_here"]))

print()
print("5. the predicate-independent identity: leaves must not move with the prune")
if "--fast" not in sys.argv:
    a = G["exact_level_counts"]["m7_thm7_2_4"]["levels"][-1]
    b = G["exact_level_counts"]["m7_thm7_none"]["levels"][-1]
    ck("leaf counts agree with and without Theorem 7", (a, b),
       (G["structural_identities"]["leaves_identical_with_and_without_theorem_7"],) * 2)

print()
print("FAILURES: %d" % len(FAIL) + ("" if not FAIL else " -> " + "; ".join(FAIL)))
sys.exit(1 if FAIL else 0)

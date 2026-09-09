#!/usr/bin/env python3
"""
Exact theorem-level citation graph of anthropics/fermats-last-theorem.

The repository states its own convention (PROOF-PATH.md): "A theorem `X.y` is
stated in `Theorems/Thm_X_y.lean` and proved in `P2M/Sol/S_X_y.lean`, whose
`import Theorems.Thm_…` lines are exactly the theorems it cites."

So the citation edges are recoverable exactly from source, without building
anything. This is ACTUAL_LEAN_DEPENDENCY evidence at DECLARATION granularity —
something the mathlib half of this map could only approximate at module level.

Also records, per solution file, which Mathlib modules it imports, giving an
exact measurement of which parts of mathlib a complete FLT proof rests on.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("/home/user/anthropics/fermats-last-theorem")
OUT = Path(__file__).resolve().parent
IMP = re.compile(r"^import\s+([A-Za-z0-9_.]+)", re.M)


def main():
    sols = sorted((REPO / "P2M" / "Sol").glob("S_*.lean"))
    cites = {}
    mathlib_imports = defaultdict(set)
    for p in sols:
        name = p.stem[2:]                       # strip "S_"
        text = p.read_text(encoding="utf-8", errors="replace")
        deps, mls = [], []
        for m in IMP.findall(text):
            if m.startswith("Theorems.Thm_"):
                deps.append(m[len("Theorems.Thm_"):])
            elif m.startswith("Mathlib."):
                mls.append(m)
        cites[name] = deps
        mathlib_imports[name] = mls

    nodes = set(cites)
    indeg = Counter()
    for src, ds in cites.items():
        for d in ds:
            indeg[d] += 1

    # transitive support of the root, over the exact citation DAG
    root = "fermat_last_theorem"
    seen, stack = set(), [root]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(cites.get(v, []))

    depth = {}

    def d(v, guard=()):
        if v in depth:
            return depth[v]
        if v in guard:
            return 0
        ds = cites.get(v, [])
        depth[v] = 1 + max((d(x, guard + (v,)) for x in ds), default=0)
        return depth[v]

    import sys
    sys.setrecursionlimit(100000)
    for v in list(nodes):
        try:
            d(v)
        except RecursionError:
            depth[v] = -1

    ml = Counter()
    for name, mods in mathlib_imports.items():
        for m in mods:
            parts = m.split(".")
            if len(parts) > 1:
                ml[parts[1]] += 1

    out = {
        "repo_commit": "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef",
        "theorems": len(nodes),
        "citation_edges": sum(len(v) for v in cites.values()),
        "reachable_from_fermat_last_theorem": len(seen),
        "unreachable_from_root": len(nodes - seen),
        "leaf_theorems_no_citations": sum(1 for v in cites.values() if not v),
        "max_citation_depth": max(depth.values()),
        "most_cited": indeg.most_common(40),
        "mathlib_area_import_counts": ml.most_common(),
        "root_direct_citations": cites.get(root, []),
    }
    (OUT / "flt_graph.json").write_text(json.dumps(
        {**out, "citations": cites}, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("most_cited", "mathlib_area_import_counts")},
                     indent=2))
    print("\nMOST-CITED THEOREMS (in-degree):")
    for n, c in out["most_cited"][:25]:
        print("  %5d  %s" % (c, n))
    print("\nMATHLIB AREAS THE PROOF RESTS ON (files importing from each):")
    for a, c in out["mathlib_area_import_counts"][:18]:
        print("  %6d  %s" % (c, a))


if __name__ == "__main__":
    main()

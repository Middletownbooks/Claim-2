#!/usr/bin/env python3
"""Cross-condition analysis: the causal table and the five answers."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import invariants as INV                                    # noqa: E402

ORDER = ["A0", "A", "B", "C", "D", "E"]
LABEL = {"A0": "no formation", "A": "static (control)",
         "B": "discovered", "C": "random named", "D": "re-expanded",
         "E": "budget-matched static"}


def load():
    out = {}
    for c in ORDER:
        p = HERE / ("round2_%s.json" % c)
        if p.exists():
            out[c] = json.loads(p.read_text())
    return out


def main():
    R = load()
    print("condition          atoms  carried  formed  expansions   classes  "
          "targets  untargeted")
    for c in ORDER:
        if c not in R:
            continue
        r = R[c]
        v = r["vocabulary"]
        tg = sum(1 for x in r["targets"].values() if x["reached"])
        print("%-2s %-16s %5d %8d %7s %11d %9d %8d %11d" % (
            c, LABEL[c], v["outer_atoms"], v["carried_over"],
            v["formed_terms"], r["expansions"], r["classes_TRAIN"],
            tg, len(r["untargeted"])))

    print("\ntarget reachability (cost of the minimal term, '-' = not reached)")
    hdr = "%-18s" % "target" + "".join("%>8s" % c for c in ORDER if c in R)
    print("%-18s" % "target" + "".join("%8s" % c for c in ORDER if c in R))
    for t in INV.TARGETS:
        row = "%-18s" % t
        for c in ORDER:
            if c not in R:
                continue
            x = R[c]["targets"][t]
            row += "%8s" % (x["min_cost"] if x["reached"] else "-")
        print(row)

    print("\nreachable classes on TRAIN by cost level")
    print("%-6s" % "cost" + "".join("%12s" % c for c in ORDER if c in R))
    costs = sorted({l["cost"] for c in R for l in R[c]["levels"]})
    for s in costs:
        row = "%-6d" % s
        for c in ORDER:
            if c not in R:
                continue
            m = [l for l in R[c]["levels"] if l["cost"] == s]
            row += "%12s" % (m[0]["classes_cumulative"] if m else "")
        print(row)

    print("\nuntargeted library matches per condition")
    for c in ORDER:
        if c not in R:
            continue
        u = R[c]["untargeted"]
        holds = sorted(k for k, v in u.items() if v["matches_HOLDOUT"])
        print("  %-2s  %d matched TRAIN, %d survive HOLDOUT: %s"
              % (c, len(u), len(holds), holds))


if __name__ == "__main__":
    main()

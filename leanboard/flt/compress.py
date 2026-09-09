#!/usr/bin/env python3
"""
Compression: 29 511 theorems -> blind communities -> the DEFINITION modules
their statements are written against (the repo's real interfaces).

The community assignment comes from regions.py (citation structure, names
blinded). The interface labels come from statement imports, which are opaque
module identifiers rather than machine-generated theorem names.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent


def main():
    g = json.loads((OUT / "flt_graph.json").read_text())["citations"]
    bd = json.loads((OUT / "boundary.json").read_text())
    per = bd["per_theorem"]
    regions = json.loads((OUT / "regions.json").read_text())

    # rebuild the frozen partition deterministically
    import regions as R
    names = sorted(g)
    idx = {nm: i for i, nm in enumerate(names)}
    adj = [[] for _ in names]
    for src, ds in g.items():
        for d in ds:
            if d in idx:
                adj[idx[src]].append(idx[d])
                adj[idx[d]].append(idx[src])
    label = R.label_propagation(len(names), adj)

    members = defaultdict(list)
    for v, l in enumerate(label):
        members[l].append(names[v])

    rows = []
    for l, ms in sorted(members.items(), key=lambda kv: -len(kv[1])):
        if len(ms) < 100:
            continue
        defs = Counter()
        mathlib_only = 0
        for nm in ms:
            info = per.get(nm)
            if not info:
                continue
            if info["mathlib_vocabulary_only"]:
                mathlib_only += 1
            defs.update(info["statement_defs"])
        rows.append({
            "size": len(ms),
            "mathlib_vocabulary_only": mathlib_only,
            "mathlib_vocabulary_fraction": round(mathlib_only / len(ms), 3),
            "defining_interfaces": defs.most_common(5),
            "namespaces": Counter(m.split("_")[0] for m in ms).most_common(3),
        })

    # concept-level compression: how few definitions cover most statements
    allcnt = Counter()
    for info in per.values():
        allcnt.update(info["statement_defs"])
    total_uses = sum(allcnt.values())
    cum, k80 = 0, None
    for i, (_, c) in enumerate(allcnt.most_common(), 1):
        cum += c
        if k80 is None and cum >= 0.8 * total_uses:
            k80 = i
    out = {
        "communities_ge_100": len(rows),
        "definition_modules_total": bd["definitions"]["count"],
        "definition_modules_used_by_statements": len(allcnt),
        "definitions_covering_80pct_of_statement_uses": k80,
        "compression": ("%d theorems -> %d communities -> %d definition "
                        "interfaces (%d cover 80%% of statement usage)"
                        % (len(names), len(rows), len(allcnt), k80)),
        "regions": rows,
    }
    (OUT / "compression.json").write_text(json.dumps(out, indent=1,
                                                     sort_keys=True))
    print(out["compression"])
    print("\n%5s %6s %-34s %s" % ("size", "ml-only", "top statement interface",
                                  "namespaces"))
    for r in rows[:14]:
        print("%5d %5.0f%%  %-34s %s" % (
            r["size"], 100 * r["mathlib_vocabulary_fraction"],
            (r["defining_interfaces"][0][0] if r["defining_interfaces"]
             else "-")[:34],
            ", ".join("%s:%d" % t for t in r["namespaces"][:2])))


if __name__ == "__main__":
    main()

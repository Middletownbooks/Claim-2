#!/usr/bin/env python3
"""
Phase 1 boundary analysis for openai/NavierStokesAndEuler, mirroring Report I
(regions, interfaces, compression) and Report J (forecast benchmark) so the two
artifacts can be compared.

The graph here is APPROXIMATE (see parse.py); FLT's was exact. Where a
conclusion could plausibly turn on that, it is reported for both a strict and a
loose resolution.
"""
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "flt"))
from regions import ami, label_propagation                    # noqa: E402


def build(graph):
    names = sorted(graph)
    idx = {n: i for i, n in enumerate(names)}
    adj = [[] for _ in names]
    edges = []
    for s, ds in graph.items():
        for d in ds:
            if d in idx:
                adj[idx[s]].append(idx[d])
                adj[idx[d]].append(idx[s])
                edges.append((idx[s], idx[d]))
    return names, idx, adj, edges


def regions(names, idx, adj, edges, meta):
    label = label_propagation(len(names), adj)
    m = len(edges)
    deg = [len(a) for a in adj]
    comm_deg, internal = defaultdict(int), defaultdict(int)
    for v in range(len(names)):
        comm_deg[label[v]] += deg[v]
    for s, t in edges:
        if label[s] == label[t]:
            internal[label[s]] += 1
    Q = sum(internal[c] / m - (comm_deg[c] / (2 * m)) ** 2 for c in comm_deg)

    members = defaultdict(list)
    for v, l in enumerate(label):
        members[l].append(v)
    endpoint = Counter()
    cross = 0
    for s, t in edges:
        if label[s] != label[t]:
            cross += 1
            endpoint[s] += 1
            endpoint[t] += 1
    ranked = [c for _, c in sorted(((v, k) for k, v in endpoint.items()),
                                   reverse=True)]
    tot = sum(endpoint.values()) or 1

    def share(f):
        k = max(1, int(len(ranked) * f))
        return round(sum(endpoint[v] for v in ranked[:k]) / tot, 4)

    big = []
    cond = {}
    for l, ms in sorted(members.items(), key=lambda kv: -len(kv[1])):
        if len(ms) < 100:
            continue
        vol = comm_deg[l]
        cut = vol - 2 * internal[l]
        cond[l] = round(cut / max(1, min(vol, 2 * m - vol)), 4)
        iface = {v for v in ms if endpoint.get(v)}
        top = Counter(meta[names[v]]["module"].split(".")[0] for v in ms)
        big.append({"size": len(ms), "interface_nodes": len(iface),
                    "bottleneck_ratio": round(len(iface) / len(ms), 4),
                    "conductance": cond[l],
                    "top_dirs": top.most_common(2),
                    "example": names[ms[0]]})
    ratios = sorted(b["bottleneck_ratio"] for b in big)
    return {
        "label": label,
        "communities_total": len(members),
        "communities_ge_100": len(big),
        "largest": max((len(v) for v in members.values()), default=0),
        "modularity_Q": round(Q, 4),
        "cross_edge_fraction": round(cross / m, 4),
        "median_bottleneck_ratio": ratios[len(ratios) // 2] if ratios else None,
        "median_conductance": sorted(cond.values())[len(cond) // 2] if cond
        else None,
        "cross_traffic_top_1pct": share(0.01),
        "cross_traffic_top_10pct": share(0.10),
        "nodes_carrying_cross_traffic": len(endpoint),
        "communities": big[:12],
    }


def forecast(graph, stmt_repo, meta, label, names, idx):
    """Report J replication: does breadth across regions beat frequency?"""
    depth, state = {}, {}
    for root in graph:
        stack = [(root, False)]
        while stack:
            v, done = stack.pop()
            if done:
                ds = [depth.get(c, 0) for c in graph.get(v, []) if c in graph]
                depth[v] = 1 + max(ds) if ds else 0
                state[v] = 2
                continue
            if state.get(v):
                continue
            state[v] = 1
            stack.append((v, True))
            for c in graph.get(v, []):
                if c in graph and not state.get(c):
                    stack.append((c, False))
    # "interfaces" here are the repo's own defs/structures used by STATEMENTS
    defs = {n for n, mm in meta.items()
            if mm["kind"] in ("def", "abbrev", "structure", "class",
                              "inductive")}
    rows = []
    for D in (1, 2, 3, 4, 6, 8):
        early = {v for v, dv in depth.items() if dv <= D}
        late = set(graph) - early
        if not late:
            continue
        late_use = Counter()
        for n in late:
            late_use.update(d for d in stmt_repo.get(n, []) if d in defs)
        tot = sum(late_use.values())
        if not tot:
            continue
        cum, target = 0, set()
        for k, c in late_use.most_common():
            target.add(k)
            cum += c
            if cum >= 0.8 * tot:
                break
        early_use = Counter()
        users = defaultdict(set)
        for n in early:
            for d in stmt_repo.get(n, []):
                if d in defs:
                    early_use[d] += 1
                    users[d].add(n)
        universe = set(late_use) | set(early_use)
        breadth = {d: len({label[idx[u]] for u in us if u in idx})
                   for d, us in users.items()}
        K = len(target)

        def score(sc):
            order = sorted(universe, key=lambda k: (-sc.get(k, 0), k))
            return round(len(set(order[:K]) & target) / K, 4)
        rows.append({
            "D": D, "early_frac": round(len(early) / len(graph), 3),
            "target": K, "universe": len(universe),
            "invisible_targets": len(target - set(early_use)),
            "freq_P": score(early_use), "breadth_P": score(breadth),
            "random_P": round(K / len(universe), 4)})
    return rows


def main():
    data = json.loads((OUT / "ns_graph.json").read_text())
    graph, stmt_repo, meta = data["graph"], data["stmt_repo"], data["meta"]
    names, idx, adj, edges = build(graph)
    r = regions(names, idx, adj, edges, meta)
    label = r.pop("label")
    rows = forecast(graph, stmt_repo, meta, label, names, idx)

    out = {"regions": r, "forecast": rows,
           "note": "graph is APPROXIMATE (textual); see parse.py"}
    (OUT / "phase1.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in r.items() if k != "communities"},
                     indent=2))
    print("\nlargest communities:")
    for c in r["communities"][:8]:
        print("  size %5d iface %4d (%.2f) cond %.3f  %s" % (
            c["size"], c["interface_nodes"], c["bottleneck_ratio"],
            c["conductance"], c["top_dirs"][:2]))
    print("\nforecast benchmark (Report J replication):")
    print("%2s %6s %6s %8s %8s %8s" % ("D", "early", "tgt", "freq", "breadth",
                                       "random"))
    for x in rows:
        print("%2d %6.3f %6d %8.3f %8.3f %8.3f" % (
            x["D"], x["early_frac"], x["target"], x["freq_P"],
            x["breadth_P"], x["random_P"]))
    wins = sum(1 for x in rows if x["breadth_P"] > x["freq_P"])
    print("\nbreadth beats frequency in %d of %d splits" % (wins, len(rows)))


if __name__ == "__main__":
    main()

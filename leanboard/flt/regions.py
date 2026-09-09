#!/usr/bin/env python3
"""
Blind region discovery on the FLT citation graph. See PREREG_blind_regions.md.

The clustering functions receive integer ids only. Names are re-attached after
the partition is frozen, for scoring against namespaces and PROOF-PATH.
"""
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent


def label_propagation(n, adj, rounds=40):
    """Deterministic asynchronous label propagation. Ids only."""
    label = list(range(n))
    for _ in range(rounds):
        changed = 0
        for v in range(n):
            if not adj[v]:
                continue
            cnt = Counter(label[u] for u in adj[v])
            best = max(cnt.items(), key=lambda kv: (kv[1], -kv[0]))[0]
            if label[v] != best:
                label[v] = best
                changed += 1
        if changed == 0:
            break
    return label


def ami(a, b):
    """Adjusted mutual information between two labelings (lists)."""
    n = len(a)
    ca, cb = Counter(a), Counter(b)
    joint = Counter(zip(a, b))
    mi = 0.0
    for (x, y), nxy in joint.items():
        mi += (nxy / n) * math.log((nxy * n) / (ca[x] * cb[y]))
    ha = -sum((c / n) * math.log(c / n) for c in ca.values())
    hb = -sum((c / n) * math.log(c / n) for c in cb.values())
    return mi / max(ha, hb, 1e-12)


def main():
    g = json.loads((OUT / "flt_graph.json").read_text())["citations"]
    names = sorted(g)
    idx = {nm: i for i, nm in enumerate(names)}
    n = len(names)

    adj = [[] for _ in range(n)]
    edges = []
    for src, ds in g.items():
        s = idx[src]
        for d in ds:
            if d in idx:
                t = idx[d]
                adj[s].append(t)
                adj[t].append(s)
                edges.append((s, t))

    label = label_propagation(n, adj)

    comms = defaultdict(list)
    for v, l in enumerate(label):
        comms[l].append(v)
    sizes = sorted((len(v) for v in comms.values()), reverse=True)

    # interfaces and the region graph
    cross = Counter()
    interface = defaultdict(set)
    for s, t in edges:
        if label[s] != label[t]:
            cross[(label[s], label[t])] += 1
            interface[label[s]].add(s)
            interface[label[t]].add(t)

    big = {l: m for l, m in comms.items() if len(m) >= 100}
    stats = []
    for l, members in sorted(big.items(), key=lambda kv: -len(kv[1])):
        iface = interface[l] & set(members)
        ns = Counter(names[v].split("_")[0] for v in members)   # unblinding
        stats.append({
            "community": l,
            "size": len(members),
            "interface_nodes": len(iface),
            "bottleneck_ratio": round(len(iface) / len(members), 4),
            "top_namespaces": ns.most_common(4),
            "example_members": [names[v] for v in members[:3]],
        })

    ratios = sorted(s["bottleneck_ratio"] for s in stats)
    median_ratio = ratios[len(ratios) // 2] if ratios else None

    # second view: statement vocabulary (opaque definition ids)
    bd = json.loads((OUT / "boundary.json").read_text())["per_theorem"]
    vocab_label = {}
    for nm, v in bd.items():
        ds = v["statement_defs"]
        vocab_label[nm] = ds[0] if ds else "__none__"
    common = [nm for nm in names if nm in vocab_label]
    a = [label[idx[nm]] for nm in common]
    b = [vocab_label[nm] for nm in common]
    score = ami(a, b)
    rng = random.Random(20260909)
    perm = b[:]
    rng.shuffle(perm)
    baseline = ami(a, perm)

    out = {
        "nodes": n,
        "undirected_edges": len(edges),
        "communities_total": len(comms),
        "communities_ge_100": len(big),
        "communities_ge_500": sum(1 for s in stats if s["size"] >= 500),
        "largest_community_size": sizes[0] if sizes else 0,
        "size_distribution_top20": sizes[:20],
        "singletons": sum(1 for s in sizes if s == 1),
        "median_bottleneck_ratio_ge_100": median_ratio,
        "ami_citation_vs_statement_vocabulary": round(score, 4),
        "ami_permuted_baseline": round(baseline, 4),
        "communities": stats,
        "region_graph_top_edges": [
            {"from": a_, "to": b_, "citations": c}
            for (a_, b_), c in cross.most_common(25)
            if a_ in big and b_ in big],
    }
    (OUT / "regions.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("communities", "region_graph_top_edges")},
                     indent=2))
    print("\nCOMMUNITIES >= 500 (namespaces attached only now, for scoring):")
    for s in stats:
        if s["size"] >= 500:
            print("  size %5d  iface %4d (%.2f)  %s" % (
                s["size"], s["interface_nodes"], s["bottleneck_ratio"],
                ", ".join("%s:%d" % t for t in s["top_namespaces"][:3])))


def followup():
    """
    P3 failed: communities have broad boundaries (median 51% of members touch
    another community). Two checks that decide what that means:
      1. Is the partition real at all? -> modularity Q against a
         degree-preserving null; and conductance per community.
      2. Even with broad boundaries, is cross-region TRAFFIC concentrated on a
         few nodes? -> Gini/top-k share of cross-community edge endpoints.
    """
    g = json.loads((OUT / "flt_graph.json").read_text())["citations"]
    r = json.loads((OUT / "regions.json").read_text())
    names = sorted(g)
    idx = {nm: i for i, nm in enumerate(names)}
    n = len(names)
    adj = [[] for _ in range(n)]
    edges = []
    for src, ds in g.items():
        s = idx[src]
        for d in ds:
            if d in idx:
                t = idx[d]
                adj[s].append(t)
                adj[t].append(s)
                edges.append((s, t))
    label = label_propagation(n, adj)
    m = len(edges)
    deg = [len(a) for a in adj]

    comm_deg = defaultdict(int)
    internal = defaultdict(int)
    for v in range(n):
        comm_deg[label[v]] += deg[v]
    for s, t in edges:
        if label[s] == label[t]:
            internal[label[s]] += 1
    Q = sum(internal[c] / m - (comm_deg[c] / (2 * m)) ** 2
            for c in comm_deg)

    # conductance for the large communities
    sizes = Counter(label)
    cond = {}
    for c, sz in sizes.items():
        if sz < 100:
            continue
        vol = comm_deg[c]
        cut = vol - 2 * internal[c]
        cond[c] = round(cut / max(1, min(vol, 2 * m - vol)), 4)

    # concentration of cross-community traffic
    endpoint = Counter()
    cross_edges = 0
    for s, t in edges:
        if label[s] != label[t]:
            cross_edges += 1
            endpoint[s] += 1
            endpoint[t] += 1
    ranked = [c for _, c in sorted(((v, k) for k, v in endpoint.items()),
                                   reverse=True)]
    tot = sum(endpoint.values())
    def share(k):
        kk = max(1, int(len(ranked) * k))
        return round(sum(endpoint[v] for v in ranked[:kk]) / tot, 4)

    out = {
        "modularity_Q": round(Q, 4),
        "interpretation_Q": ("Q above ~0.3 indicates community structure well "
                             "beyond a degree-preserving null"),
        "cross_community_edges": cross_edges,
        "cross_edge_fraction": round(cross_edges / m, 4),
        "conductance_by_community_ge100": dict(
            sorted(cond.items(), key=lambda kv: kv[1])[:12]),
        "median_conductance_ge100": sorted(cond.values())[len(cond) // 2],
        "cross_traffic_share_top_1pct_nodes": share(0.01),
        "cross_traffic_share_top_5pct_nodes": share(0.05),
        "cross_traffic_share_top_10pct_nodes": share(0.10),
        "distinct_nodes_carrying_cross_traffic": len(endpoint),
        "top_interface_nodes": [
            {"theorem": names[v], "cross_edges": endpoint[v]}
            for v in ranked[:15]],
    }
    (OUT / "regions_followup.json").write_text(
        json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k != "top_interface_nodes"}, indent=2))
    print("\nBUSIEST INTERFACE THEOREMS:")
    for t in out["top_interface_nodes"][:12]:
        print("  %4d  %s" % (t["cross_edges"], t["theorem"]))


if __name__ == "__main__":
    followup()

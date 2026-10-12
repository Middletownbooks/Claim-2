#!/usr/bin/env python3
"""
Retrospective benchmark: could the load-bearing interfaces of the FLT proof
have been identified from its early layers alone?

See PREREG_retrospective.md. The predictor sees only theorems at citation depth
<= D (D fixed by the pre-registered rule) and the edges and statement imports
among them. The answer key -- total statement usage over all 29 511 theorems --
is used only for scoring, after every ranking is computed.
"""
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent


def rank_dict(d, universe):
    """Descending rank, ties broken deterministically by key."""
    order = sorted(universe, key=lambda k: (-d.get(k, 0), k))
    return {k: i for i, k in enumerate(order)}


def auc(scores, positives, universe):
    """ROC-AUC of a score over `universe` against the positive set."""
    pos = [scores.get(k, 0) for k in universe if k in positives]
    neg = [scores.get(k, 0) for k in universe if k not in positives]
    if not pos or not neg:
        return None
    neg_sorted = sorted(neg)
    import bisect
    total = 0.0
    for p in pos:
        lo = bisect.bisect_left(neg_sorted, p)
        hi = bisect.bisect_right(neg_sorted, p)
        total += lo + 0.5 * (hi - lo)
    return round(total / (len(pos) * len(neg)), 4)


def main():
    g = json.loads((OUT / "flt_graph.json").read_text())["citations"]
    per = json.loads((OUT / "boundary.json").read_text())["per_theorem"]

    # ---------- bottom-up citation depth ----------
    depth = {}
    state = {}
    for root in g:
        stack = [(root, False)]
        while stack:
            v, done = stack.pop()
            if done:
                ds = [depth.get(c, 0) for c in g.get(v, []) if c in g]
                depth[v] = 1 + max(ds) if ds else 0
                state[v] = 2
                continue
            if state.get(v):
                continue
            state[v] = 1
            stack.append((v, True))
            for c in g.get(v, []):
                if c in g and not state.get(c):
                    stack.append((c, False))

    n = len(g)
    dist = Counter(depth.values())
    cum, D = 0, None
    for d in sorted(dist):
        cum += dist[d]
        if cum >= 0.25 * n:
            D = d
            break
    early = {v for v, dv in depth.items() if dv <= D}

    # ---------- answer key (not shown to the predictors) ----------
    total_use = Counter()
    for nm, info in per.items():
        total_use.update(info["statement_defs"])
    tot = sum(total_use.values())
    cum, target = 0, set()
    for k, c in total_use.most_common():
        target.add(k)
        cum += c
        if cum >= 0.8 * tot:
            break
    universe = set(total_use)

    # ---------- predictor's view: early layers only ----------
    early_use = Counter()
    early_users = defaultdict(set)
    cooc = defaultdict(set)
    for nm in early:
        info = per.get(nm)
        if not info:
            continue
        ds = info["statement_defs"]
        early_use.update(ds)
        for d in ds:
            early_users[d].add(nm)
            cooc[d].update(x for x in ds if x != d)

    early_indeg = Counter()
    for src, cits in g.items():
        if src in early:
            for c in cits:
                if c in early:
                    early_indeg[c] += 1
    consumer_deg = {d: sum(early_indeg.get(u, 0) for u in us)
                    for d, us in early_users.items()}

    regions = json.loads((OUT / "regions.json").read_text())
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
    comm_breadth = {d: len({label[idx[u]] for u in us})
                    for d, us in early_users.items()}

    preds = {
        "early_usage": dict(early_use),
        "early_users_distinct": {k: len(v) for k, v in early_users.items()},
        "early_consumer_degree": consumer_deg,
        "cooccurrence_breadth": {k: len(v) for k, v in cooc.items()},
        "community_breadth": comm_breadth,
    }
    ranks = {name: rank_dict(sc, universe) for name, sc in preds.items()}
    combined = {k: -sum(r[k] for r in ranks.values()) for k in universe}
    preds["combined"] = combined

    visible = {k for k in universe if early_use.get(k, 0) > 0}
    invisible_targets = target - visible

    K = len(target)
    results = {}
    for name, sc in preds.items():
        order = sorted(universe, key=lambda k: (-sc.get(k, 0), k))
        topk = set(order[:K])
        results[name] = {
            "precision_at_282": round(len(topk & target) / K, 4),
            "recall_at_282": round(len(topk & target) / len(target), 4),
            "auc_all": auc(sc, target, universe),
            "auc_visible_only": auc(sc, target & visible, visible),
            "precision_at_20": round(
                len(set(order[:20]) & target) / 20, 4),
            "top20_hits_in_true_top20": len(
                set(order[:20]) & set(k for k, _ in total_use.most_common(20))),
        }
    random_precision = round(len(target) / len(universe), 4)

    out = {
        "depth_cutoff_D": D,
        "theorems_total": n,
        "theorems_early": len(early),
        "early_fraction": round(len(early) / n, 4),
        "depth_histogram_first_12": {d: dist[d] for d in sorted(dist)[:12]},
        "max_depth": max(dist),
        "definitions_universe": len(universe),
        "target_size_80pct_usage": len(target),
        "targets_visible_early": len(target & visible),
        "targets_INVISIBLE_early": len(invisible_targets),
        "invisible_fraction_of_target": round(
            len(invisible_targets) / len(target), 4),
        "definitions_visible_early": len(visible),
        "random_baseline_precision": random_precision,
        "results": results,
        "example_invisible_targets": sorted(invisible_targets)[:15],
    }
    (OUT / "retro.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("results", "example_invisible_targets")},
                     indent=2))
    print("\n%-24s %6s %6s %8s %8s %8s" % (
        "predictor", "P@282", "R@282", "AUC-all", "AUC-vis", "P@20"))
    for name, r in results.items():
        print("%-24s %6.3f %6.3f %8s %8s %8.2f" % (
            name, r["precision_at_282"], r["recall_at_282"],
            r["auc_all"], r["auc_visible_only"], r["precision_at_20"]))
    print("\nrandom baseline precision: %.4f" % random_precision)


if __name__ == "__main__":
    main()

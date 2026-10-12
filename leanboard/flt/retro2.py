#!/usr/bin/env python3
"""
Post-hoc robustness run for the retrospective benchmark. NOT pre-registered;
labelled as such. It repairs three problems with the pre-registered run:

  1. The pre-registered depth rule selected D = 0 (the 8 230 leaves already
     exceed 25% of theorems). Leaves cite nothing, so the early subgraph has NO
     internal edges and `early_consumer_degree` was identically zero -- a
     degenerate feature, not a negative result. Here D = 2.
  2. `community_breadth` used the blind communities computed on the FULL graph,
     which leaks information from the future. Here communities are recomputed
     on the early subgraph alone.
  3. The target was total statement usage, which INCLUDES the early usage the
     naive predictor counts -- so `early_usage` was partly predicting its own
     input. Here the target is usage by LATE theorems only (depth > D), making
     it a genuine forecast.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import regions as R
from retro import auc, rank_dict

OUT = Path(__file__).resolve().parent
D = 2


def main():
    g = json.loads((OUT / "flt_graph.json").read_text())["citations"]
    per = json.loads((OUT / "boundary.json").read_text())["per_theorem"]

    depth, state = {}, {}
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

    early = {v for v, dv in depth.items() if dv <= D}
    late = set(g) - early

    # ---- target: definitions carrying 80% of LATE statement usage ----
    late_use = Counter()
    for nm in late:
        late_use.update(per.get(nm, {}).get("statement_defs", []))
    tot = sum(late_use.values())
    cum, target = 0, set()
    for k, c in late_use.most_common():
        target.add(k)
        cum += c
        if cum >= 0.8 * tot:
            break
    universe = set(late_use) | {d for nm in early
                                for d in per.get(nm, {}).get("statement_defs", [])}

    # ---- early-only features ----
    early_use = Counter()
    early_users = defaultdict(set)
    cooc = defaultdict(set)
    for nm in early:
        ds = per.get(nm, {}).get("statement_defs", [])
        early_use.update(ds)
        for d in ds:
            early_users[d].add(nm)
            cooc[d].update(x for x in ds if x != d)

    early_indeg = Counter()
    sub_nodes = sorted(early)
    sub_idx = {nm: i for i, nm in enumerate(sub_nodes)}
    adj = [[] for _ in sub_nodes]
    for src in early:
        for c in g.get(src, []):
            if c in early:
                early_indeg[c] += 1
                adj[sub_idx[src]].append(sub_idx[c])
                adj[sub_idx[c]].append(sub_idx[src])
    consumer_deg = {d: sum(early_indeg.get(u, 0) for u in us)
                    for d, us in early_users.items()}

    # communities from the EARLY SUBGRAPH ONLY (no future leak)
    lab = R.label_propagation(len(sub_nodes), adj)
    comm_breadth = {d: len({lab[sub_idx[u]] for u in us})
                    for d, us in early_users.items()}

    preds = {
        "early_usage": dict(early_use),
        "early_users_distinct": {k: len(v) for k, v in early_users.items()},
        "early_consumer_degree": consumer_deg,
        "cooccurrence_breadth": {k: len(v) for k, v in cooc.items()},
        "community_breadth_early_only": comm_breadth,
    }
    ranks = {n: rank_dict(s, universe) for n, s in preds.items()}
    preds["combined"] = {k: -sum(r[k] for r in ranks.values())
                         for k in universe}

    visible = {k for k in universe if early_use.get(k, 0) > 0}
    K = len(target)
    results = {}
    for name, sc in preds.items():
        order = sorted(universe, key=lambda k: (-sc.get(k, 0), k))
        topk = set(order[:K])
        results[name] = {
            "precision_at_K": round(len(topk & target) / K, 4),
            "auc_all": auc(sc, target, universe),
            "auc_visible_only": auc(sc, target & visible, visible),
            "top20_hits_in_true_top20": len(
                set(order[:20]) & {k for k, _ in late_use.most_common(20)}),
        }

    out = {
        "label": "POST-HOC ROBUSTNESS RUN, not pre-registered",
        "depth_cutoff_D": D,
        "theorems_early": len(early),
        "theorems_late": len(late),
        "early_fraction": round(len(early) / len(g), 4),
        "early_subgraph_internal_edges": sum(early_indeg.values()),
        "target": "definitions carrying 80% of LATE statement usage",
        "target_size": K,
        "definitions_universe": len(universe),
        "targets_INVISIBLE_early": len(target - visible),
        "invisible_fraction_of_target": round(
            len(target - visible) / K, 4),
        "random_baseline_precision": round(K / len(universe), 4),
        "results": results,
    }
    (OUT / "retro2.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items() if k != "results"},
                     indent=2))
    print("\n%-30s %8s %8s %8s %6s" % (
        "predictor", "P@K", "AUC-all", "AUC-vis", "top20"))
    for n, r in results.items():
        print("%-30s %8.3f %8s %8s %5d/20" % (
            n, r["precision_at_K"], r["auc_all"], r["auc_visible_only"],
            r["top20_hits_in_true_top20"]))


if __name__ == "__main__":
    main()

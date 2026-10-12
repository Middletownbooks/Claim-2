#!/usr/bin/env python3
"""
Stability check: does the community-breadth advantage over naive frequency
hold across depth splits, or is it an artifact of D = 2?

Same design as retro2.py (late-only target, leak-free early communities),
swept over D. Run once, all splits reported.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

import regions as R
from retro import auc, rank_dict

OUT = Path(__file__).resolve().parent


def depths(g):
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
    return depth


def run(g, per, depth, D):
    early = {v for v, dv in depth.items() if dv <= D}
    late = set(g) - early
    if not late:
        return None
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
    early_use = Counter()
    early_users = defaultdict(set)
    cooc = defaultdict(set)
    for nm in early:
        ds = per.get(nm, {}).get("statement_defs", [])
        early_use.update(ds)
        for d in ds:
            early_users[d].add(nm)
            cooc[d].update(x for x in ds if x != d)
    sub = sorted(early)
    si = {nm: i for i, nm in enumerate(sub)}
    adj = [[] for _ in sub]
    for s in early:
        for c in g.get(s, []):
            if c in early:
                adj[si[s]].append(si[c])
                adj[si[c]].append(si[s])
    lab = R.label_propagation(len(sub), adj)
    preds = {
        "early_usage": dict(early_use),
        "cooccurrence_breadth": {k: len(v) for k, v in cooc.items()},
        "community_breadth": {d: len({lab[si[u]] for u in us})
                              for d, us in early_users.items()},
    }
    K = len(target)
    row = {"D": D, "early_frac": round(len(early) / len(g), 3),
           "target_size": K, "invisible": len(target - {
               k for k in universe if early_use.get(k, 0) > 0})}
    for n, sc in preds.items():
        order = sorted(universe, key=lambda k: (-sc.get(k, 0), k))
        row[n + "_P"] = round(len(set(order[:K]) & target) / K, 3)
        row[n + "_AUC"] = auc(sc, target, universe)
    return row


def main():
    g = json.loads((OUT / "flt_graph.json").read_text())["citations"]
    per = json.loads((OUT / "boundary.json").read_text())["per_theorem"]
    depth = depths(g)
    rows = [r for r in (run(g, per, depth, D) for D in (1, 2, 3, 4, 6, 8))
            if r]
    (OUT / "retro_stability.json").write_text(
        json.dumps(rows, indent=1, sort_keys=True))
    print("%2s %6s %6s %5s | %6s %6s | %6s %6s | %6s %6s" % (
        "D", "early", "tgt", "invis", "useP", "useAUC", "coocP", "coocAUC",
        "commP", "commAUC"))
    for r in rows:
        print("%2d %6.3f %6d %5d | %6.3f %6.4f | %6.3f %6.4f | %6.3f %6.4f" % (
            r["D"], r["early_frac"], r["target_size"], r["invisible"],
            r["early_usage_P"], r["early_usage_AUC"],
            r["cooccurrence_breadth_P"], r["cooccurrence_breadth_AUC"],
            r["community_breadth_P"], r["community_breadth_AUC"]))
    wins = sum(1 for r in rows
               if r["community_breadth_P"] > r["early_usage_P"])
    print("\ncommunity_breadth beats early_usage on precision in %d of %d splits"
          % (wins, len(rows)))


if __name__ == "__main__":
    main()

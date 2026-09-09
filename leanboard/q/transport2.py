#!/usr/bin/env python3
"""
Q5 (corrected) -- blind transport, FLT -> NS, over the exportable surfaces.

Both sides are now restricted to theorems stated purely in mathlib vocabulary,
so the two token sets are drawn from the SAME vocabulary and are directly
comparable. This is what the retracted first run got wrong.

Candidate generation is still target-blind: the pool is the whole of FLT's
exportable surface, selected by a rule (statement names no FLT-specific
definition) fixed before NS was looked at, with no re-ranking against NS.

The measurement is duplication: how many of NS's 4 054 exportable theorems
have a near-twin in FLT's 12 577? A near-twin means NS spent effort proving
something the other board already had -- a transport gain that can be counted.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECLKW = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)?"
    r"(theorem|lemma)\s+([A-Za-z0-9_.'!?]+)", re.M)
SEED = 20260909
STOP = {"forall", "fun", "let", "in", "by", "with", "at", "of", "to", "the"}


def bodies(root, subs, keep):
    out = []
    for sub in subs:
        d = Path(root) / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            for m in DECLKW.finditer(txt):
                if m.group(2) not in keep:
                    continue
                end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
                body = txt[m.end():end.start()] if end else txt[m.end():
                                                               m.end() + 3000]
                toks = {t for t in TOK.findall(body) if t not in STOP
                        and len(t) > 1}
                if len(toks) >= 4:
                    out.append({"name": m.group(2),
                                "file": str(p.relative_to(root)),
                                "toks": sorted(toks)})
    return out


class Index:
    def __init__(self, pool):
        self.pool = pool
        self.sets = [set(e["toks"]) for e in pool]
        self.inv = defaultdict(list)
        for i, s in enumerate(self.sets):
            for t in s:
                self.inv[t].append(i)

    def best(self, q, exclude_file=None):
        cand = Counter()
        for t in q:
            lst = self.inv.get(t, ())
            if len(lst) > 4000:
                continue                      # a token in most statements is
            for i in lst:                     # uninformative; skip it
                cand[i] += 1
        best, bi = 0.0, None
        for i, _ in cand.most_common(300):
            if exclude_file and self.pool[i]["file"] == exclude_file:
                continue
            s = self.sets[i]
            inter = len(q & s)
            v = inter / (len(q) + len(s) - inter)
            if v > best:
                best, bi = v, i
        return best, (self.pool[bi] if bi is not None else None)


def stats(name, pool, scores):
    sc = sorted(scores, reverse=True)
    n = len(sc)
    return {"pool": name, "pool_size": len(pool), "queries": n,
            "mean_best_jaccard": round(sum(sc) / n, 4) if n else 0,
            "median": round(sc[n // 2], 4) if n else 0,
            "ge_0.4": sum(1 for s in sc if s >= .4),
            "ge_0.6": sum(1 for s in sc if s >= .6),
            "ge_0.8": sum(1 for s in sc if s >= .8)}


def main():
    rng = random.Random(SEED)
    fltkeep = set(json.load(open(OUT / "surface_flt.json")))
    nskeep = set(json.load(open(OUT / "surface_ns.json")))
    flt = bodies("/home/user/anthropics/fermats-last-theorem",
                 ["Theorems", "Definitions"], fltkeep)
    ns = bodies("/home/user/openai/navierstokesandeuler",
                ["NavierStokes", "Euler"], nskeep)
    print("exportable statements with >=4 tokens: FLT %d, NS %d"
          % (len(flt), len(ns)), flush=True)
    print("median token-set size: FLT %d, NS %d"
          % (sorted(len(e["toks"]) for e in flt)[len(flt) // 2],
             sorted(len(e["toks"]) for e in ns)[len(ns) // 2]), flush=True)

    contact = set(json.load(open(OUT / "contact_files.json")))
    import sys
    reverse = "--reverse" in sys.argv
    if reverse:
        queries, label = flt, "NS -> FLT"
        pools = {
            "TRANSPORT_ns_exportable": ns,
            "CONTROL_B_flt_itself": flt,
            "CONTROL_C_random_ns_quarter": rng.sample(ns, max(1, len(ns) // 4)),
        }
        selfpool = "CONTROL_B_flt_itself"
    else:
        queries, label = ns, "FLT -> NS"
        pools = {
            "TRANSPORT_flt_exportable": flt,
            "CONTROL_B_ns_itself": ns,
            "CONTROL_C_random_flt_quarter": rng.sample(flt, max(1, len(flt) // 4)),
            "CONTROL_E_architecture_contact": [e for e in flt
                                               if e["file"] in contact],
        }
        selfpool = "CONTROL_B_ns_itself"
    rows, detail = [], {}
    for name, pool in pools.items():
        if not pool:
            continue
        idx = Index(pool)
        scores, ex = [], []
        for e in queries:
            q = set(e["toks"])
            s, hit = idx.best(q, exclude_file=e["file"]
                              if name == selfpool else None)
            scores.append(s)
            if hit is not None and s >= .6:
                ex.append({"ns": e["name"], "match": hit["name"],
                           "jaccard": round(s, 3),
                           "shared": sorted(q & set(hit["toks"]))[:10]})
        r = stats(name, pool, scores)
        rows.append(r)
        detail[name] = ex[:30]
        print("%-34s pool=%-6d mean=%.4f median=%.4f  >=.4:%-5d >=.6:%-4d "
              ">=.8:%d" % (name, len(pool), r["mean_best_jaccard"],
                           r["median"], r["ge_0.4"], r["ge_0.6"], r["ge_0.8"]),
              flush=True)

    json.dump({"label": "EXPERIMENTAL_RESULT", "seed": SEED,
               "direction": label + ", exportable surfaces only",
               "rows": rows, "high_matches": detail},
              open(OUT / ("transport2_reverse.json" if reverse
                          else "transport2.json"), "w"), indent=1)


if __name__ == "__main__":
    main()

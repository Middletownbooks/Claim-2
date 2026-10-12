#!/usr/bin/env python3
"""
Q5 positive control -- Euler <-> NavierStokes, inside the same repository.

The FLT -> NS result is a near-zero. A near-zero is only informative if the
measurement can register a positive somewhere, so this runs the identical
protocol on a pair that ought to transport if anything does: the Euler and
Navier-Stokes halves of the SAME repository, written by the same authors, at
the same time, about adjacent equations.

If Euler -> NavierStokes also scores near zero, the instrument is blind and the
FLT -> NS result says nothing. If it scores well above zero, the FLT -> NS zero
is a fact about the boards.
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
STOP = {"forall", "fun", "let", "in", "by", "with", "at", "of", "to", "the"}
SEED = 20260909
ROOT = Path("/home/user/openai/navierstokesandeuler")


def bodies(sub, keep):
    out = []
    for p in (ROOT / sub).rglob("*.lean"):
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        for m in DECLKW.finditer(txt):
            if m.group(2) not in keep:
                continue
            end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
            body = txt[m.end():end.start()] if end else txt[m.end():m.end() + 3000]
            toks = {t for t in TOK.findall(body) if t not in STOP and len(t) > 1}
            if len(toks) >= 4:
                out.append({"name": m.group(2), "file": str(p.relative_to(ROOT)),
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
                continue
            for i in lst:
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


def run(queries, pool, name, selfmatch=False):
    idx = Index(pool)
    sc, ex = [], []
    for e in queries:
        q = set(e["toks"])
        s, hit = idx.best(q, exclude_file=e["file"] if selfmatch else None)
        sc.append(s)
        if hit is not None and s >= .6:
            ex.append({"q": e["name"], "match": hit["name"],
                       "jaccard": round(s, 3)})
    sc.sort(reverse=True)
    n = len(sc)
    r = {"pool": name, "pool_size": len(pool), "queries": n,
         "mean_best_jaccard": round(sum(sc) / n, 4) if n else 0,
         "median": round(sc[n // 2], 4) if n else 0,
         "ge_0.4": sum(1 for s in sc if s >= .4),
         "ge_0.6": sum(1 for s in sc if s >= .6),
         "ge_0.8": sum(1 for s in sc if s >= .8)}
    print("%-36s pool=%-6d mean=%.4f median=%.4f  >=.4:%-5d >=.6:%-5d >=.8:%d"
          % (name, len(pool), r["mean_best_jaccard"], r["median"], r["ge_0.4"],
             r["ge_0.6"], r["ge_0.8"]), flush=True)
    return r, ex[:25]


def main():
    keep = set(json.load(open(OUT / "surface_ns.json")))
    eu = bodies("Euler", keep)
    nv = bodies("NavierStokes", keep)
    print("exportable statements: Euler %d, NavierStokes %d" % (len(eu), len(nv)))
    flt = None
    rows, det = [], {}
    for nm, q, pool, sm in [
        ("POSCTRL_euler_to_navierstokes", nv, eu, False),
        ("POSCTRL_navierstokes_to_euler", eu, nv, False),
        ("BASELINE_navierstokes_itself", nv, nv, True),
        ("BASELINE_euler_itself", eu, eu, True),
    ]:
        if not q or not pool:
            continue
        r, e = run(q, pool, nm, sm)
        rows.append(r)
        det[nm] = e
    json.dump({"label": "EXPERIMENTAL_RESULT", "seed": SEED,
               "purpose": "sensitivity check for the FLT->NS null",
               "rows": rows, "examples": det},
              open(OUT / "poscontrol.json", "w"), indent=1)


if __name__ == "__main__":
    main()

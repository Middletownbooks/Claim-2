#!/usr/bin/env python3
"""
T -- the prospective intervention, plus the section-5 proxy gate.

GUIDE. An order-2 Markov model with backoff, built from the source
development's proofs only. At each position of an unseen target proof it ranks
the whole move alphabet; the score is the RANK of the move the target actually
made. Mean rank is the expected number of candidates a searcher trying moves in
guide order would examine. Lower is better.

ARMS, all ranking the same alphabet at the same positions:
  NONE          uniform            -- (|alphabet|+1)/2 by construction
  RANDOM        order-0 from A     -- A's move frequencies, sequence destroyed
  WRONG_DOMAIN  order-2 from the least vocabulary-similar development
  SOURCE        order-2 from A

SOURCE vs RANDOM is the decisive contrast: same source, same frequencies, the
only difference is whether trajectory order carries information.
"""
import json
import math
import random
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOARD = OUT.parent
LEVELS = ["L1", "L2", "L3", "ENG", "MATH"]
SEED = 20260909


class Guide:
    def __init__(self, seqs, alphabet, order=2, alpha=0.5):
        self.A = sorted(alphabet)
        self.order = order
        self.uni = Counter()
        self.bi = defaultdict(Counter)
        self.tri = defaultdict(Counter)
        for s in seqs:
            for i, x in enumerate(s):
                self.uni[x] += 1
                if i >= 1:
                    self.bi[(s[i - 1],)][x] += 1
                if i >= 2:
                    self.tri[(s[i - 2], s[i - 1])][x] += 1
        self.alpha = alpha
        self.N = sum(self.uni.values()) or 1
        self._cache = {}

    def _probs(self, ctx):
        n = len(self.A)
        base = {a: (self.uni[a] + self.alpha) / (self.N + self.alpha * n)
                for a in self.A}
        if self.order == 0 or not ctx:
            return base
        p = base
        c1 = self.bi.get((ctx[-1],))
        if c1:
            t = sum(c1.values())
            w = t / (t + 5.0)
            p = {a: w * (c1[a] / t) + (1 - w) * p[a] for a in self.A}
        if self.order >= 2 and len(ctx) >= 2:
            c2 = self.tri.get((ctx[-2], ctx[-1]))
            if c2:
                t = sum(c2.values())
                w = t / (t + 5.0)
                p = {a: w * (c2[a] / t) + (1 - w) * p[a] for a in self.A}
        return p

    def ranks(self, ctx):
        key = tuple(ctx[-2:]) if self.order else ()
        r = self._cache.get(key)
        if r is None:
            p = self._probs(key)
            order = sorted(self.A, key=lambda a: (-p[a], a))
            r = {a: i + 1 for i, a in enumerate(order)}
            self._cache[key] = r
        return r


def evaluate(guide, seqs):
    tot = 0
    n = 0
    for s in seqs:
        for i, x in enumerate(s):
            r = guide.ranks(s[max(0, i - 2):i])
            tot += r.get(x, len(guide.A))
            n += 1
    return tot / n if n else float("nan")


def main():
    tr = json.loads((OUT / "trajectories.json").read_text())
    names = sorted(tr)
    D = json.loads((BOARD / "s" / "distance.json").read_text())["matrices"]

    # ---- section 5 gate: is the representation a vocabulary proxy? -----
    print("=== SECTION 5 GATE: architecture similarity vs vocabulary ===")
    gate = {}
    for L in LEVELS:
        alpha = sorted({x for n in names for t in tr[n] for x in t[L]})
        big = {}
        for n in names:
            c = Counter()
            for t in tr[n]:
                s = t[L]
                for i in range(1, len(s)):
                    c[(s[i - 1], s[i])] += 1
            tot = sum(c.values()) or 1
            big[n] = {k: v / tot for k, v in c.items()}

        def cos(a, b):
            ks = set(a) | set(b)
            na = math.sqrt(sum(a.get(k, 0) ** 2 for k in ks))
            nb = math.sqrt(sum(b.get(k, 0) ** 2 for k in ks))
            return (sum(a.get(k, 0) * b.get(k, 0) for k in ks) / (na * nb)
                    if na and nb else 0)
        xs, ys, zs = [], [], []
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                xs.append(cos(big[a], big[b]))
                ys.append(D["vocab"][a][b])
                zs.append(D["iface"][a][b])

        def pear(u, v):
            mu, mv = st.mean(u), st.mean(v)
            num = sum((x - mu) * (y - mv) for x, y in zip(u, v))
            den = (sum((x - mu) ** 2 for x in u) *
                   sum((y - mv) ** 2 for y in v)) ** .5
            return num / den if den else 0
        gate[L] = {"alphabet": len(alpha),
                   "bigram_cos_mean": round(st.mean(xs), 4),
                   "bigram_cos_sd": round(st.pstdev(xs), 4),
                   "r_with_vocab": round(pear(xs, ys), 4),
                   "r_with_iface": round(pear(xs, zs), 4)}
        print("  %-5s alphabet=%2d  bigram-cos %.4f +- %.4f   "
              "r(vocab)=%+.3f  r(iface)=%+.3f"
              % (L, len(alpha), gate[L]["bigram_cos_mean"],
                 gate[L]["bigram_cos_sd"], gate[L]["r_with_vocab"],
                 gate[L]["r_with_iface"]))

    # ---- wrong-domain assignment, by the pre-registered rule ----------
    eligible = [n for n in names if len(tr[n]) >= 200]
    wrong = {}
    for b in names:
        cands = [(D["vocab"][b][a], a) for a in eligible if a != b]
        wrong[b] = min(cands)[1]
    print("\nwrong-domain assignment (least vocabulary-similar, >=200 proofs):")
    for b in names:
        print("   %-32s <- %s" % (b, wrong[b]))

    # ---- the intervention ---------------------------------------------
    print("\n=== INTERVENTION: mean rank of the true next move (lower better) ===")
    rows = []
    for L in LEVELS:
        alpha = sorted({x for n in names for t in tr[n] for x in t[L]})
        seqs = {n: [t[L] for t in tr[n] if len(t[L]) >= 4] for n in names}
        g2 = {n: Guide(seqs[n], alpha, order=2) for n in names}
        g0 = {n: Guide(seqs[n], alpha, order=0) for n in names}
        none = (len(alpha) + 1) / 2
        for b in names:
            if not seqs[b]:
                continue
            for a in names:
                if a == b or not seqs[a]:
                    continue
                rows.append({
                    "level": L, "source": a, "target": b,
                    "n_target_proofs": len(seqs[b]),
                    "NONE": round(none, 4),
                    "RANDOM": round(evaluate(g0[a], seqs[b]), 4),
                    "SOURCE": round(evaluate(g2[a], seqs[b]), 4),
                    "WRONG": round(evaluate(g2[wrong[b]], seqs[b]), 4),
                })
        # within-development ceiling, held out by halves
        rng = random.Random(SEED)
        for b in names:
            s = seqs[b][:]
            rng.shuffle(s)
            h = len(s) // 2
            if h < 10:
                continue
            gb = Guide(s[:h], alpha, order=2)
            rows.append({"level": L, "source": "__WITHIN__", "target": b,
                         "n_target_proofs": len(s) - h,
                         "NONE": round(none, 4),
                         "RANDOM": round(evaluate(Guide(s[:h], alpha, order=0),
                                                  s[h:]), 4),
                         "SOURCE": round(evaluate(gb, s[h:]), 4),
                         "WRONG": None})
        print("  %s done" % L, flush=True)

    json.dump({"label": "EXPERIMENTAL_RESULT", "seed": SEED,
               "gate": gate, "wrong_domain": wrong, "rows": rows},
              open(OUT / "result.json", "w"), indent=1)

    print("\n%-6s %-12s %9s %9s %9s %9s" % ("level", "comparison", "NONE",
                                            "RANDOM", "SOURCE", "WRONG"))
    for L in LEVELS:
        cross = [r for r in rows if r["level"] == L and r["source"] != "__WITHIN__"]
        wi = [r for r in rows if r["level"] == L and r["source"] == "__WITHIN__"]
        print("%-6s %-12s %9.3f %9.3f %9.3f %9.3f"
              % (L, "cross (90)", st.mean([r["NONE"] for r in cross]),
                 st.mean([r["RANDOM"] for r in cross]),
                 st.mean([r["SOURCE"] for r in cross]),
                 st.mean([r["WRONG"] for r in cross])))
        if wi:
            print("%-6s %-12s %9.3f %9.3f %9.3f %9s"
                  % ("", "within", st.mean([r["NONE"] for r in wi]),
                     st.mean([r["RANDOM"] for r in wi]),
                     st.mean([r["SOURCE"] for r in wi]), "-"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
R6 -- does cross-development transport track mathematical distance?

Phase Q's sharpest limitation was that its transport metric could not separate
a RELATED cross-board pair (Euler -> NavierStokes, 5.5%) from an UNRELATED one
(FLT -> NS, 2.4%): both sat near the floor, with n = 1 comparison each.

The ten-proofs collection removes that limitation. Ten developments, one
producer, one toolchain, one period, spanning sphere packing to quantum games:
production process held constant while mathematical distance varies, giving 45
pairs instead of 1.

So the decisive question is answerable directly: across those 45 pairs, does
transport correlate with mathematical proximity? If it does, boards and their
distances matter. If it is flat, transport is independent of subject matter and
Phase Q's "board -> mathlib -> board" reading holds.

Distance proxy: Jaccard of mathlib declaration vocabularies (r/threeboard.py).
Transport: the Phase Q exportable-surface protocol, unchanged.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
TEN = Path("/home/user/openai/ten-proofs")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECLKW = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(theorem|lemma)\s+([A-Za-z0-9_.'!?«»]+)", re.M)
STOP = {"forall", "fun", "let", "in", "by", "with", "at", "of", "to", "the"}


def bodies(path, keep):
    txt = path.read_text(errors="ignore")
    out = []
    for m in DECLKW.finditer(txt):
        if m.group(2) not in keep:
            continue
        end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
        body = txt[m.end():end.start()] if end else txt[m.end():m.end() + 3000]
        toks = {t for t in TOK.findall(body) if t not in STOP and len(t) > 1}
        if len(toks) >= 4:
            out.append(sorted(toks))
    return out


class Index:
    def __init__(self, pool):
        self.sets = [set(e) for e in pool]
        self.inv = defaultdict(list)
        for i, s in enumerate(self.sets):
            for t in s:
                self.inv[t].append(i)

    def best(self, q, skip=None):
        cand = Counter()
        for t in q:
            lst = self.inv.get(t, ())
            if len(lst) > 3000:
                continue
            for i in lst:
                cand[i] += 1
        best = 0.0
        for i, _ in cand.most_common(300):
            if skip is not None and i == skip:
                continue
            s = self.sets[i]
            inter = len(q & s)
            v = inter / (len(q) + len(s) - inter)
            best = max(best, v)
        return best


def main():
    surf = json.loads((OUT / "surface_qpr.json").read_text())["ten_proofs"]
    tb = json.loads((OUT / "threeboard.json").read_text())
    J = tb["ten_proofs_pairwise_jaccard"]

    pools = {}
    for name, rec in surf.items():
        keep = set(rec["examples"])
        # re-derive the full exportable name set, not just the 20 examples
        pools[name] = None
    # rebuild exportable name sets exactly
    mathlib = set(json.loads((BOARD / "decls.json").read_text())["index"])
    mathlib |= {k.split(".")[-1] for k in mathlib}
    DEF = re.compile(
        r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
        r"(def|abbrev|structure|class|inductive)\s+([A-Za-z0-9_.'!?«»]+)", re.M)
    for p in sorted(TEN.glob("*.lean")):
        if p.name == "All.lean":
            continue
        txt = p.read_text(errors="ignore")
        own = set()
        for _, nm in DEF.findall(txt):
            own.add(nm)
            own.add(nm.split(".")[-1])
        own -= mathlib
        keep = set()
        for m in DECLKW.finditer(txt):
            end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
            body = txt[m.end():end.start()] if end else txt[m.end():m.end() + 3000]
            if not (set(TOK.findall(body)) & own):
                keep.add(m.group(2))
        pools[p.stem] = bodies(p, keep)
        print("%-32s exportable statements with >=4 tokens: %d"
              % (p.stem, len(pools[p.stem])), flush=True)

    names = [n for n in pools if pools[n]]
    idx = {n: Index(pools[n]) for n in names}
    rows = []
    for a in names:
        for b in names:
            if a == b:
                continue
            qs = [set(e) for e in pools[a]]
            sc = [idx[b].best(q) for q in qs]
            hi = sum(1 for s in sc if s >= .4)
            rows.append({"source": b, "target": a,
                         "queries": len(qs),
                         "mean": round(sum(sc) / len(sc), 4),
                         "ge_0.4_frac": round(hi / len(sc), 4),
                         "vocab_jaccard": J[a][b]})
    # within-development baseline
    base = {}
    for a in names:
        qs = [set(e) for e in pools[a]]
        sc = [idx[a].best(q, skip=i) for i, q in enumerate(qs)]
        base[a] = {"mean": round(sum(sc) / len(sc), 4),
                   "ge_0.4_frac": round(sum(1 for s in sc if s >= .4) / len(sc), 4)}

    # correlation between vocabulary distance and transport
    import statistics as st
    xs = [r["vocab_jaccard"] for r in rows]
    ys = [r["ge_0.4_frac"] for r in rows]
    mx, my = st.mean(xs), st.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** .5
    r_pearson = cov / den if den else 0

    out = {"label": "EXPERIMENTAL_RESULT",
           "question": "does cross-development transport track mathematical "
                       "distance, with the production process held constant?",
           "pairs": sorted(rows, key=lambda r: -r["ge_0.4_frac"]),
           "within_development_baseline": base,
           "pearson_r_vocabJaccard_vs_transport": round(r_pearson, 4),
           "n_pairs": len(rows)}
    (OUT / "pairs.json").write_text(json.dumps(out, indent=1) + "\n")

    print("\ncross-development transport, %d ordered pairs" % len(rows))
    print("  mean over pairs: %.4f at J>=0.4" % st.mean(ys))
    print("  within-development baseline, mean: %.4f"
          % st.mean([v["ge_0.4_frac"] for v in base.values()]))
    print("  Pearson r (vocabulary Jaccard vs transport): %.4f" % r_pearson)
    print("\ntop 8 transporting pairs:")
    for r in out["pairs"][:8]:
        print("   %-28s -> %-28s %.3f  (vocabJ %.3f)"
              % (r["source"][:28], r["target"][:28], r["ge_0.4_frac"],
                 r["vocab_jaccard"]))
    print("\nbottom 5:")
    for r in out["pairs"][-5:]:
        print("   %-28s -> %-28s %.3f  (vocabJ %.3f)"
              % (r["source"][:28], r["target"][:28], r["ge_0.4_frac"],
                 r["vocab_jaccard"]))


if __name__ == "__main__":
    main()

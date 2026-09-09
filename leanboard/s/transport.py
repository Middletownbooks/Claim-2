#!/usr/bin/env python3
"""
S5/S6 -- transport, measured with the pool-size confound removed by design
rather than regressed away afterwards.

Phase R found r(transport, source pool size) = 0.413: a development with more
exportable statements simply gets more chances to match. Regressing it out
afterwards leaves the estimate at the mercy of the functional form, so the
primary measurement here SUBSAMPLES every source pool to a common size and
averages over repeats. The raw measurement is kept beside it.

MulticolorTriangleRamsey has only 16 exportable statements and is excluded from
the size-matched analysis; it is retained in the raw one. That leaves nine
developments and 72 ordered pairs at the matched size.
"""
import json
import math
import random
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOARD = OUT.parent
TEN = Path("/home/user/openai/ten-proofs")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECLKW = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(theorem|lemma)\s+([A-Za-z0-9_.'!?«»]+)", re.M)
DEF = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(def|abbrev|structure|class|inductive)\s+([A-Za-z0-9_.'!?«»]+)", re.M)
STOP = {"forall", "fun", "let", "in", "by", "with", "at", "of", "to", "the"}
SEED = 20260909
SUBSAMPLE = 69
REPEATS = 20
THRESH = 0.4


def pools():
    mathlib = set(json.loads((BOARD / "decls.json").read_text())["index"])
    mathlib |= {k.split(".")[-1] for k in mathlib}
    out = {}
    for p in sorted(TEN.glob("*.lean")):
        if p.name == "All.lean":
            continue
        txt = p.read_text(errors="ignore")
        own = set()
        for _, nm in DEF.findall(txt):
            own.add(nm)
            own.add(nm.split(".")[-1])
        own -= mathlib
        items = []
        for m in DECLKW.finditer(txt):
            end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
            stmt = txt[m.end():end.start()] if end else txt[m.end():m.end() + 3000]
            toks = {t for t in TOK.findall(stmt) if t not in STOP and len(t) > 1}
            if toks & own:
                continue
            if len(toks) >= 4:
                items.append(toks)
        out[p.stem] = items
    return out


class Index:
    def __init__(self, sets):
        self.sets = sets
        self.inv = defaultdict(list)
        for i, s in enumerate(sets):
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
            if v > best:
                best = v
        return best


def main():
    P = pools()
    names = sorted(P)
    print("exportable pools:", {n: len(P[n]) for n in names})

    # ---- raw transport, all 90 ordered pairs -------------------------
    idx = {n: Index(P[n]) for n in names}
    raw = {}
    for a in names:
        for b in names:
            if a == b:
                continue
            sc = [idx[b].best(q) for q in P[a]]
            raw[(a, b)] = sum(1 for s in sc if s >= THRESH) / len(sc)
    within = {}
    for a in names:
        sc = [idx[a].best(q, skip=i) for i, q in enumerate(P[a])]
        within[a] = sum(1 for s in sc if s >= THRESH) / len(sc)

    # ---- size-matched transport --------------------------------------
    big = [n for n in names if len(P[n]) >= SUBSAMPLE]
    rng = random.Random(SEED)
    matched = {}
    for b in big:
        for a in big:
            if a == b:
                continue
            vals = []
            for _ in range(REPEATS):
                src = rng.sample(P[b], SUBSAMPLE)
                qs = rng.sample(P[a], SUBSAMPLE)
                ix = Index(src)
                sc = [ix.best(q) for q in qs]
                vals.append(sum(1 for s in sc if s >= THRESH) / SUBSAMPLE)
            matched[(a, b)] = round(st.mean(vals), 5)
        print("  matched pool done: %s" % b, flush=True)

    out = {"label": "EXPERIMENTAL_RESULT",
           "threshold": THRESH, "subsample": SUBSAMPLE, "repeats": REPEATS,
           "seed": SEED,
           "pool_sizes": {n: len(P[n]) for n in names},
           "within_development": within,
           "raw": {"%s->%s" % (b, a): v for (a, b), v in raw.items()},
           "size_matched": {"%s->%s" % (b, a): v for (a, b), v in matched.items()},
           "excluded_from_matched": [n for n in names if n not in big]}
    (OUT / "transport.json").write_text(json.dumps(out, indent=1) + "\n")

    print("\nwithin-development mean: %.4f" % st.mean(list(within.values())))
    print("raw cross mean:          %.4f  (n=%d)"
          % (st.mean(list(raw.values())), len(raw)))
    print("size-matched cross mean: %.4f  (n=%d, pool=%d, %d repeats)"
          % (st.mean(list(matched.values())), len(matched), SUBSAMPLE, REPEATS))


if __name__ == "__main__":
    main()

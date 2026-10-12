#!/usr/bin/env python3
"""
S5 -- the QPR Pinsker intervention, per s/pinsker_prereg.md.

Targets were chosen by the mechanical rule in the pre-registration BEFORE any
target was inspected: CompactnessAndDegeneracy (88 qualifying references) and
MetricCodes (70, including 17 uses of mathlib's `klFun`).

Three arms, identical except for what the source pool contains:
  BASELINE      QPR's exportable statements minus the Pinsker cluster
  INTERVENTION  the same pool plus the Pinsker cluster
  NEG CONTROL   the same pool plus an equal number of random QPR exportable
                lemmas, length-matched
"""
import json
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
THRESH = 0.4


def items(stem):
    mathlib = set(json.loads((BOARD / "decls.json").read_text())["index"])
    mathlib |= {k.split(".")[-1] for k in mathlib}
    txt = (TEN / (stem + ".lean")).read_text(errors="ignore")
    own = set()
    for _, nm in DEF.findall(txt):
        own.add(nm)
        own.add(nm.split(".")[-1])
    own -= mathlib
    # Pinsker span
    pstart = txt.find("namespace Pinsker")
    pend = txt.find("end Pinsker", pstart + 1) if pstart >= 0 else -1
    out = []
    for m in DECLKW.finditer(txt):
        end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
        stmt = txt[m.end():end.start()] if end else txt[m.end():m.end() + 3000]
        toks = {t for t in TOK.findall(stmt) if t not in STOP and len(t) > 1}
        if toks & own or len(toks) < 4:
            continue
        inp = pstart >= 0 and pstart <= m.start() <= pend
        out.append({"name": m.group(2), "toks": toks, "pinsker": inp,
                    "len": len(stmt)})
    return out


class Index:
    def __init__(self, pool):
        self.pool = pool
        self.sets = [p["toks"] for p in pool]
        self.inv = defaultdict(list)
        for i, s in enumerate(self.sets):
            for t in s:
                self.inv[t].append(i)

    def best(self, q):
        cand = Counter()
        for t in q:
            lst = self.inv.get(t, ())
            if len(lst) > 3000:
                continue
            for i in lst:
                cand[i] += 1
        best, bi = 0.0, None
        for i, _ in cand.most_common(300):
            s = self.sets[i]
            inter = len(q & s)
            v = inter / (len(q) + len(s) - inter)
            if v > best:
                best, bi = v, i
        return best, (self.pool[bi] if bi is not None else None)


def run(pool, targets, tag):
    idx = Index(pool)
    res = {}
    for t, qs in targets.items():
        sc, pin, best_ex = [], 0, []
        for q in qs:
            s, hit = idx.best(q["toks"])
            sc.append(s)
            if hit is not None and hit.get("pinsker") and s >= THRESH:
                pin += 1
                best_ex.append((q["name"], hit["name"], round(s, 3)))
        res[t] = {"queries": len(qs),
                  "matched_ge_0.4": sum(1 for s in sc if s >= THRESH),
                  "mean_best": round(st.mean(sc), 4),
                  "matched_to_pinsker": pin,
                  "examples": best_ex[:5]}
        print("  %-14s %-28s matched=%-4d mean=%.4f  to-Pinsker=%d"
              % (tag, t, res[t]["matched_ge_0.4"], res[t]["mean_best"], pin),
              flush=True)
    return res


def main():
    rng = random.Random(SEED)
    qpr = items("QuantumParallelRepetition")
    pin = [x for x in qpr if x["pinsker"]]
    rest = [x for x in qpr if not x["pinsker"]]
    print("QPR exportable: %d  (Pinsker cluster: %d)" % (len(qpr), len(pin)))
    if not pin:
        print("no Pinsker declarations in the exportable surface")
    tnames = json.loads((OUT / "pinsker_targets.json").read_text())["targets"]
    targets = {t: items(t) for t in tnames}
    print("targets:", {t: len(v) for t, v in targets.items()})

    medlen = st.median([x["len"] for x in pin]) if pin else 0
    cand = [x for x in rest if abs(x["len"] - medlen) <= 0.2 * medlen] or rest
    neg = rng.sample(cand, min(len(pin), len(cand)))

    out = {"label": "EXPERIMENTAL_RESULT",
           "prereg": "s/pinsker_prereg.md",
           "targets": tnames,
           "pinsker_cluster_size": len(pin),
           "pinsker_names": [x["name"] for x in pin],
           "negative_control_size": len(neg),
           "arms": {}}
    out["arms"]["BASELINE"] = run(rest, targets, "BASELINE")
    out["arms"]["INTERVENTION"] = run(rest + pin, targets, "INTERVENTION")
    out["arms"]["NEG_CONTROL"] = run(rest + neg, targets, "NEG_CONTROL")

    print("\ndeltas (intervention - baseline / negcontrol - baseline):")
    for t in tnames:
        b = out["arms"]["BASELINE"][t]
        i = out["arms"]["INTERVENTION"][t]
        c = out["arms"]["NEG_CONTROL"][t]
        print("  %-28s matched %+d / %+d    mean %+.4f / %+.4f   pinskerhits=%d"
              % (t, i["matched_ge_0.4"] - b["matched_ge_0.4"],
                 c["matched_ge_0.4"] - b["matched_ge_0.4"],
                 i["mean_best"] - b["mean_best"],
                 c["mean_best"] - b["mean_best"], i["matched_to_pinsker"]))
    (OUT / "pinsker_result.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()

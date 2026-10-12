#!/usr/bin/env python3
"""
T -- extract construction trajectories at three levels of normalization.

Phase S's architecture metric was 54% `have`-rate, so nothing here reuses it.
A trajectory is the ORDERED sequence of construction moves a proof makes, with
every identifier removed: no theorem names, declaration names, namespaces,
variables, or domain constants survive into the representation. What is kept is
what the proof DOES.

L1 TACTIC       normalized tactic tokens, in order
L2 STRUCTURAL   tactics collapsed to construction moves
L3 ARCHITECTURE moves collapsed to phases
ENG / MATH      the L2 sequence restricted to engineering / mathematical moves
"""
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
TEN = Path("/home/user/openai/ten-proofs")

# tactic token -> structural construction move
MOVE = {}
for t in ("intro", "intros", "rintro", "introv"):
    MOVE[t] = "INTRO"
for t in ("have", "suffices", "set", "let", "obtain_have"):
    MOVE[t] = "AUX"
for t in ("rcases", "obtain", "cases", "cases'", "by_cases", "match",
          "interval_cases", "fin_cases", "split", "split_ifs", "rcases'"):
    MOVE[t] = "CASE"
for t in ("induction", "induction'", "rec"):
    MOVE[t] = "INDUCT"
for t in ("by_contra", "absurd", "contradiction", "push_neg", "exfalso"):
    MOVE[t] = "CONTRA"
for t in ("calc", "trans", "gcongr"):
    MOVE[t] = "CHAIN"
for t in ("rw", "rewrite", "simp", "simpa", "unfold", "subst", "nth_rewrite",
          "change", "dsimp", "simp_rw", "norm_cast", "push_cast", "erw"):
    MOVE[t] = "REWRITE"
for t in ("apply", "exact", "refine", "use", "constructor", "exact_mod_cast",
          "convert", "specialize", "exists"):
    MOVE[t] = "APPLY"
for t in ("linarith", "nlinarith", "positivity", "bound", "norm_num", "omega",
          "field_simp", "ring", "ring_nf", "polyrith", "linear_combination"):
    MOVE[t] = "BOUND"
for t in ("ext", "funext", "congr", "ext1"):
    MOVE[t] = "EXT"
for t in ("fun_prop", "measurability", "continuity", "aesop", "decide",
          "infer_instance", "norm_fin", "filter_upwards"):
    MOVE[t] = "AUTOM"
for t in ("rfl", "trivial", "assumption", "tauto", "simp_all", "omega_nat"):
    MOVE[t] = "CLOSE"

PHASE = {"INTRO": "SETUP", "EXT": "SETUP",
         "AUX": "CONSTRUCT",
         "CASE": "BRANCH", "INDUCT": "BRANCH", "CONTRA": "BRANCH",
         "REWRITE": "TRANSFORM", "CHAIN": "TRANSFORM",
         "BOUND": "ESTIMATE", "AUTOM": "ESTIMATE",
         "APPLY": "CLOSE", "CLOSE": "CLOSE"}
ENG_MOVES = {"REWRITE", "APPLY", "AUTOM", "CLOSE"}
MATH_MOVES = {"AUX", "CASE", "INDUCT", "CONTRA", "CHAIN", "BOUND", "EXT"}

DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+"
    r"([A-Za-z0-9_.'!?«»]+)", re.M)
# a tactic token: start of line-or-`<;>`-or-`;` position, then an identifier
TACTIC = re.compile(r"(?:^\s+|<;>\s*|;\s*|\bby\s+|·\s*)([a-zA-Z_][a-zA-Z0-9_']*)",
                    re.M)


def trajectories(path):
    txt = path.read_text(errors="ignore")
    spans = []
    ms = list(DECL.finditer(txt))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(txt)
        if m.group(1) not in ("theorem", "lemma"):
            continue
        body = txt[m.end():end]
        k = body.find(":= by")
        if k < 0:
            k = body.find(":=\n")
            if k < 0:
                continue
        proof = body[k:]
        toks = [t for t in TACTIC.findall(proof)]
        l1 = [t for t in toks if t in MOVE]
        if len(l1) < 8:
            continue
        l2 = [MOVE[t] for t in l1]
        l3 = [PHASE[x] for x in l2]
        spans.append({
            "L1": l1, "L2": l2, "L3": l3,
            "ENG": [x for x in l2 if x in ENG_MOVES],
            "MATH": [x for x in l2 if x in MATH_MOVES],
        })
    return spans


def main():
    out = {}
    for p in sorted(TEN.glob("*.lean")):
        if p.name == "All.lean":
            continue
        tr = trajectories(p)
        out[p.stem] = tr
        c1 = Counter(x for t in tr for x in t["L1"])
        c2 = Counter(x for t in tr for x in t["L2"])
        print("%-32s %5d proofs  mean len %5.1f  L1 alphabet %3d  "
              "top L2: %s"
              % (p.stem, len(tr),
                 sum(len(t["L2"]) for t in tr) / max(1, len(tr)),
                 len(c1), [k for k, _ in c2.most_common(4)]), flush=True)
    json.dump(out, open(OUT / "trajectories.json", "w"))
    tot = sum(len(v) for v in out.values())
    print("\ntotal proofs with >=8 moves: %d" % tot)
    print("L2 alphabet: %s" % sorted(set(MOVE.values())))
    print("L3 alphabet: %s" % sorted(set(PHASE.values())))


if __name__ == "__main__":
    main()

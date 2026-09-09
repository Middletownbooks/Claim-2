#!/usr/bin/env python3
"""
R5 -- QPR's exportable surface, by the Phase Q criterion so the numbers are
comparable: a theorem is exportable if its STATEMENT names no declaration the
board itself defines (after subtracting names mathlib also has).

Phase Q measured FLT at 25.9% and NS at 10.9%. This is the number the
board-versus-piece decision turns on: a development whose theorems are mostly
about its own objects is a board; one whose theorems are mostly about mathlib's
objects is a pile of pieces sitting on mathlib.
"""
import json
import re
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
TEN = Path("/home/user/openai/ten-proofs")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECLKW = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+"
    r"([A-Za-z0-9_.'!?«»]+)", re.M)


def main():
    mathlib = set(json.loads((BOARD / "decls.json").read_text())["index"])
    mathlib |= {k.split(".")[-1] for k in mathlib}

    res = {}
    for p in sorted(TEN.glob("*.lean")):
        if p.name == "All.lean":
            continue
        txt = p.read_text(errors="ignore")
        own = set()
        for kw, nm in DECLKW.findall(txt):
            if kw in ("def", "abbrev", "structure", "class", "inductive"):
                own.add(nm)
                own.add(nm.split(".")[-1])
        own -= mathlib
        pure, impure, n = [], 0, 0
        for m in DECLKW.finditer(txt):
            if m.group(1) not in ("theorem", "lemma"):
                continue
            n += 1
            end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
            body = txt[m.end():end.start()] if end else txt[m.end():m.end() + 3000]
            if set(TOK.findall(body)) & own:
                impure += 1
            else:
                pure.append(m.group(2))
        res[p.stem] = {"theorems": n, "own_definitions": len(own),
                       "exportable": len(pure),
                       "exportable_fraction": round(len(pure) / n, 4) if n else 0,
                       "examples": pure[:20]}
        print("%-32s %6d theorems  %5d exportable  %5.1f%%"
              % (p.stem, n, len(pure), 100 * res[p.stem]["exportable_fraction"]))

    out = {"label": "COMPUTED_FROM_ARTIFACT",
           "criterion": "statement names no board-defined declaration that "
                        "mathlib does not also have (Phase Q method)",
           "reference": {"flt": 0.259, "ns": 0.109},
           "ten_proofs": res}
    (OUT / "surface_qpr.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\nreference from Phase Q:  FLT 25.9%   NS 10.9%")
    q = res["QuantumParallelRepetition"]
    print("\nQPR exportable examples:", q["examples"][:14])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Q5 (corrected) -- each board's EXPORTABLE SURFACE.

The signature-Jaccard experiment was invalid and is retracted: NS statements
have a median of ONE mathlib token, so a Jaccard of 0.9 between two of them
usually means only that both mention `ContDiff`. The reason for that is the
real measurement, and it is this:

  A theorem can be transported to another board only if it can be STATED
  there. A statement mentioning a board's own definitions cannot; a statement
  written purely in mathlib's vocabulary can. So the transportable surface of a
  board is the set of its theorems whose statements name no board-internal
  declaration.

This applies the same criterion to both boards, using each board's own
declaration names extracted from its own source. FLT's side of this was
computed in the previous phase (`upstreamable.json`, 4 577 of 29 511); NS has
never been measured this way.
"""
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECLKW = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)?"
    r"(theorem|lemma|def|abbrev|structure|class|instance)\s+"
    r"([A-Za-z0-9_.'!?]+)", re.M)
NSNS = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)", re.M)


def board_decls(root, subs):
    """Every declaration NAME the board defines, bare and namespace-qualified."""
    names = set()
    defs = set()
    for sub in subs:
        d = Path(root) / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            nss = NSNS.findall(txt)
            for kw, nm in DECLKW.findall(txt):
                names.add(nm)
                names.add(nm.split(".")[-1])
                for ns in nss:
                    names.add(ns + "." + nm)
                if kw in ("def", "abbrev", "structure", "class"):
                    defs.add(nm)
                    defs.add(nm.split(".")[-1])
    return names, defs


def surface(root, subs, own_defs):
    """Split the board's theorems by whether the STATEMENT names an internal
    definition."""
    pure, impure, n = [], 0, 0
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
                if m.group(1) not in ("theorem", "lemma"):
                    continue
                n += 1
                end = re.compile(r":=\s*(by\b|\n)").search(txt, m.end())
                body = txt[m.end():end.start()] if end else txt[m.end():
                                                               m.end() + 3000]
                toks = set(TOK.findall(body))
                if toks & own_defs:
                    impure += 1
                else:
                    pure.append({"name": m.group(2),
                                 "file": str(p.relative_to(root)),
                                 "tokens": len(toks)})
    return pure, impure, n


def main():
    # A name the board defines that mathlib ALSO defines is not evidence of
    # board-specificity: FLT and NS both define things called `norm`, `map`,
    # `comp`. Subtracting mathlib's names is what makes the criterion mean
    # "mentions something only this board has".
    mathlib = set(json.loads(
        (OUT.parent / "decls.json").read_text())["index"])
    mathlib |= {k.split(".")[-1] for k in mathlib}
    res = {}
    for b, (root, subs) in {
        "flt": ("/home/user/anthropics/fermats-last-theorem",
                ["Theorems", "Definitions"]),
        "ns": ("/home/user/openai/navierstokesandeuler",
               ["NavierStokes", "Euler"]),
    }.items():
        print("scanning %s ..." % b, flush=True)
        names, defs = board_decls(root, subs)
        own = defs - mathlib
        pure, impure, n = surface(root, subs, own)
        res[b] = {"declarations_defined": len(names),
                  "definitions": len(defs),
                  "definitions_not_in_mathlib": len(own),
                  "theorems": n,
                  "mathlib_vocabulary_only": len(pure),
                  "uses_own_definitions": impure,
                  "exportable_fraction": round(len(pure) / n, 4) if n else 0,
                  "examples": [e["name"] for e in pure[:15]]}
        print("  %s: %d theorems, %d definitions (%d board-specific), "
              "%d stated in mathlib vocabulary only (%.1f%%)"
              % (b, n, len(defs), len(own), len(pure),
                 100 * res[b]["exportable_fraction"]),
              flush=True)
        json.dump([e["name"] for e in pure],
                  open(OUT / ("surface_%s.json" % b), "w"))

    out = {"label": "COMPUTED_FROM_ARTIFACT",
           "definition": "a theorem is exportable if its STATEMENT names no "
                         "declaration the board itself defines, hence can be "
                         "stated on any board that speaks mathlib",
           "retraction": "supersedes the signature-Jaccard transport run, "
                         "which was invalid: NS statements carry a median of "
                         "one mathlib token, so its similarity scores measured "
                         "vocabulary poverty rather than similarity",
           "boards": res}
    (OUT / "surface.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()

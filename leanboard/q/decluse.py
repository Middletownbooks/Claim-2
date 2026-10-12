#!/usr/bin/env python3
"""
Q2b -- which mathlib DECLARATIONS each board actually references.

Module-level import overlap is coarse: importing `Mathlib.Analysis...` says a
file may use it, not that it does. This matches the two boards' source text
against mathlib's 241 917 declaration names.

Two matching modes, both reported:
  qualified  -- dotted tokens matched against the full declaration name. Exact,
                and an UNDERCOUNT, because Lean source uses `open` and writes
                many references unqualified.
  root       -- single-token names that are the complete name of exactly one
                mathlib declaration. Adds unqualified references without the
                ambiguity that sank an earlier phase (`add_pow` resolving to
                `Tropical.add_pow`).
The undercount is symmetric across the two boards, which is what the
comparison needs.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
BOARDS = {
    "flt": ("/home/user/anthropics/fermats-last-theorem",
            ["Theorems", "Definitions", "P2M"]),
    "ns": ("/home/user/openai/navierstokesandeuler",
           ["NavierStokes", "Euler", "ComparatorChallenges"]),
}


def main():
    idx = json.loads((BOARD / "decls.json").read_text())["index"]
    qualified = {k for k in idx if "." in k}
    roots = {k for k in idx if "." not in k}
    print("mathlib: %d declarations, %d qualified, %d root-level"
          % (len(idx), len(qualified), len(roots)), flush=True)

    res = {}
    for name, (root, subs) in BOARDS.items():
        cq, cr = Counter(), Counter()
        nfiles = 0
        for sub in subs:
            d = Path(root) / sub
            if not d.exists():
                continue
            for p in d.rglob("*.lean"):
                nfiles += 1
                if nfiles % 10000 == 0:
                    print("  %s %d files" % (name, nfiles), flush=True)
                try:
                    txt = p.read_text(errors="ignore")
                except Exception:
                    continue
                toks = set(TOK.findall(txt))
                for t in toks & qualified:
                    cq[t] += 1
                for t in toks & roots:
                    cr[t] += 1
        res[name] = {"files": nfiles, "qualified": cq, "root": cr}
        print("%s: %d files, %d distinct qualified decls, %d root decls"
              % (name, nfiles, len(cq), len(cr)), flush=True)

    fq, nq = set(res["flt"]["qualified"]), set(res["ns"]["qualified"])
    fr, nr = set(res["flt"]["root"]), set(res["ns"]["root"])
    fa, na = fq | fr, nq | nr
    shared = fa & na

    def by_area(names):
        return Counter(idx[n].split(".")[1] if idx[n].count(".") > 0 else "?"
                       for n in names)

    out = {
        "label": "COMPUTED_FROM_ARTIFACT",
        "method": "textual match of source tokens against mathlib declaration "
                  "names; qualified matches are exact, root matches are "
                  "single-token names unique in mathlib. An undercount, "
                  "symmetric across boards.",
        "mathlib_declarations": len(idx),
        "flt": {"files": res["flt"]["files"], "qualified": len(fq),
                "root": len(fr), "all": len(fa)},
        "ns": {"files": res["ns"]["files"], "qualified": len(nq),
               "root": len(nr), "all": len(na)},
        "shared_declarations": len(shared),
        "jaccard": round(len(shared) / len(fa | na), 4),
        "shared_over_flt": round(len(shared) / len(fa), 4),
        "shared_over_ns": round(len(shared) / len(na), 4),
        "shared_by_area": by_area(shared).most_common(),
        "ns_only_by_area": by_area(na - fa).most_common(12),
        "shared_top_by_ns_use": sorted(
            ((n, res["ns"]["qualified"][n] + res["ns"]["root"][n],
              res["flt"]["qualified"][n] + res["flt"]["root"][n], idx[n])
             for n in shared), key=lambda x: -x[1])[:60],
        "ns_only_top": sorted(
            ((n, res["ns"]["qualified"][n] + res["ns"]["root"][n], idx[n])
             for n in na - fa), key=lambda x: -x[1])[:40],
    }
    (OUT / "decluse.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\nshared declarations: %d  (%.1f%% of FLT's, %.1f%% of NS's)"
          % (len(shared), 100 * out["shared_over_flt"],
             100 * out["shared_over_ns"]))
    print("shared by area:", dict(out["shared_by_area"][:10]))
    print("NS-only by area:", dict(out["ns_only_by_area"][:10]))


if __name__ == "__main__":
    main()

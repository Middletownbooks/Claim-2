#!/usr/bin/env python3
"""
R3 -- declaration-level mathlib footprint of QPR, and the three-board matrix.

Same method as Phase Q (`q/decluse2.py`), so the numbers are comparable:
qualified matches are exact; root matches are restricted to names carrying an
underscore or an uppercase letter, which excludes the 20 English-word entries
in `decls.json` that contaminated Phase Q's first pass.

All ten of the ten-proofs files are measured, not only QPR, because section 7
asks whether QPR is an outlier and that question is answered by the same scan.
"""
import json
import re
from collections import Counter
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
TEN = Path("/home/user/openai/ten-proofs")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")


def main():
    idx = json.loads((BOARD / "decls.json").read_text())["index"]
    qualified = {k for k in idx if "." in k}
    roots = {k for k in idx if "." not in k
             and ("_" in k or any(c.isupper() for c in k))}
    vocab = qualified | roots

    # the ten proofs
    ten = {}
    for p in sorted(TEN.glob("*.lean")):
        if p.name == "All.lean":
            continue
        toks = set(TOK.findall(p.read_text(errors="ignore")))
        ten[p.stem] = toks & vocab
        print("%-32s %5d mathlib declarations" % (p.stem, len(ten[p.stem])),
              flush=True)

    # FLT and NS, from the Phase Q per-module scan
    pv = json.loads((BOARD / "q" / "per_module_vocab.json").read_text())
    flt = set()
    for v in pv["flt"].values():
        flt.update(v)
    ns = set()
    for v in pv["ns"].values():
        ns.update(v)

    qpr = ten["QuantumParallelRepetition"]

    def area(d):
        m = idx.get(d, "")
        p = m.split(".")
        return ".".join(p[1:3]) if len(p) > 2 else (p[1] if len(p) > 1 else "?")

    def rep(a, b, na, nb):
        i = a & b
        return {"shared": len(i), "jaccard": round(len(i) / len(a | b), 4),
                "frac_of_%s" % na: round(len(i) / len(a), 4),
                "frac_of_%s" % nb: round(len(i) / len(b), 4)}

    out = {
        "label": "COMPUTED_FROM_ARTIFACT",
        "sizes": {"flt": len(flt), "ns": len(ns), "qpr": len(qpr)},
        "pairs": {
            "qpr_flt": rep(qpr, flt, "qpr", "flt"),
            "qpr_ns": rep(qpr, ns, "qpr", "ns"),
            "flt_ns": rep(flt, ns, "flt", "ns"),
        },
        "qpr_only": len(qpr - flt - ns),
        "qpr_only_by_area": Counter(area(d) for d in qpr - flt - ns
                                    ).most_common(15),
        "qpr_shared_all_three": len(qpr & flt & ns),
        "qpr_by_area": Counter(area(d) for d in qpr).most_common(15),
        "ten_proofs_sizes": {k: len(v) for k, v in ten.items()},
        "ten_proofs_pairwise_jaccard": {
            a: {b: round(len(ten[a] & ten[b]) / len(ten[a] | ten[b]), 4)
                for b in ten} for a in ten},
        "ten_vs_flt_ns": {
            k: {"vs_flt": round(len(v & flt) / len(v), 4),
                "vs_ns": round(len(v & ns) / len(v), 4)}
            for k, v in ten.items()},
    }
    (OUT / "threeboard.json").write_text(json.dumps(out, indent=1) + "\n")

    print("\nvocabulary sizes: FLT %d  NS %d  QPR %d"
          % (len(flt), len(ns), len(qpr)))
    for k, v in out["pairs"].items():
        print("  %-10s shared=%-6d jaccard=%.4f  %s"
              % (k, v["shared"], v["jaccard"],
                 {kk: vv for kk, vv in v.items() if kk.startswith("frac")}))
    print("\nQPR declarations used by NEITHER FLT nor NS: %d (%.1f%%)"
          % (out["qpr_only"], 100 * out["qpr_only"] / len(qpr)))
    print("  by area:", dict(out["qpr_only_by_area"][:10]))
    print("\nQPR's own top areas:", dict(out["qpr_by_area"][:10]))
    print("\nten proofs, mathlib vocabulary shared with FLT / NS:")
    for k, v in sorted(out["ten_vs_flt_ns"].items(),
                       key=lambda kv: -kv[1]["vs_flt"]):
        print("   %-32s flt %.3f   ns %.3f  (%d decls)"
              % (k, v["vs_flt"], v["vs_ns"], out["ten_proofs_sizes"][k]))


if __name__ == "__main__":
    main()

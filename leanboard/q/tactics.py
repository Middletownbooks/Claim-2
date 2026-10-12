#!/usr/bin/env python3
"""
Q4 -- proof-architecture comparison via the proof MOVES each board actually
makes.

This counts tactic occurrences rather than files-containing-a-pattern, which is
the sharper measurement: a board that uses `by_contra` once in 30 000 files and
one that uses it in every third proof both "contain" contradiction.

Tactics are what Lean exposes of a proof's structure, and unlike declaration
names they are not machine-generated labels -- FLT's README warns its names
are generated, and this programme has already been misled by one.

Normalised per 1000 proofs so the two boards can be compared.
"""
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
TACTICS = ["by_contra", "absurd", "contradiction", "exact", "apply", "refine",
           "have", "obtain", "rcases", "rintro", "intro", "cases", "induction",
           "calc", "suffices", "simp", "rw", "linarith", "nlinarith", "gcongr",
           "positivity", "field_simp", "ring", "norm_num", "omega", "constructor",
           "use", "exists", "specialize", "convert", "congr", "ext", "funext",
           "unfold", "subst", "push_neg", "by_cases", "interval_cases",
           "fin_cases", "measurability", "continuity", "fun_prop", "bound",
           "filter_upwards", "gcongr", "peel", "trans", "nth_rewrite"]
RX = {t: re.compile(r"(?<![A-Za-z0-9_'])%s(?![A-Za-z0-9_'])" % re.escape(t))
      for t in TACTICS}
PROOF = re.compile(r":=\s*by\b")
BOARDS = {
    "flt": ("/home/user/anthropics/fermats-last-theorem", ["P2M/Sol"]),
    "ns": ("/home/user/openai/navierstokesandeuler", ["NavierStokes", "Euler"]),
}


def main():
    out = {"label": "COMPUTED_FROM_ARTIFACT", "boards": {}}
    for b, (root, subs) in BOARDS.items():
        cnt = Counter()
        proofs = 0
        nfiles = 0
        for sub in subs:
            d = Path(root) / sub
            if not d.exists():
                continue
            for p in d.rglob("*.lean"):
                nfiles += 1
                try:
                    txt = p.read_text(errors="ignore")
                except Exception:
                    continue
                proofs += len(PROOF.findall(txt))
                for t, rx in RX.items():
                    n = len(rx.findall(txt))
                    if n:
                        cnt[t] += n
        out["boards"][b] = {
            "files": nfiles, "proofs": proofs, "raw": dict(cnt),
            "per_1000_proofs": {t: round(1000 * c / proofs, 1)
                                for t, c in cnt.items()} if proofs else {},
        }
        print("%s: %d files, %d proofs" % (b, nfiles, proofs), flush=True)

    f = out["boards"]["flt"]["per_1000_proofs"]
    n = out["boards"]["ns"]["per_1000_proofs"]
    rows = []
    for t in TACTICS:
        a, c = f.get(t, 0), n.get(t, 0)
        if a or c:
            rows.append((t, a, c, (c + 1) / (a + 1)))
    rows.sort(key=lambda r: -r[3])
    out["ratio_ns_over_flt"] = [{"tactic": t, "flt_per_1000": a,
                                 "ns_per_1000": c, "ratio": round(r, 2)}
                                for t, a, c, r in rows]
    (OUT / "tactics.json").write_text(json.dumps(out, indent=1) + "\n")
    print("\n%-18s %12s %12s %8s" % ("tactic", "FLT/1000", "NS/1000", "NS:FLT"))
    for t, a, c, r in rows:
        print("%-18s %12.1f %12.1f %8.2f" % (t, a, c, r))


if __name__ == "__main__":
    main()

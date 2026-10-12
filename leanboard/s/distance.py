#!/usr/bin/env python3
"""
S3 -- distance matrices, separating infrastructure from mathematics.

Four distances over the ten developments, all Jaccard-based but over different
alphabets:

  D_vocab      shared mathlib THEOREMS/LEMMAS      -- what facts they cite
  D_iface      shared mathlib TYPES/CLASSES/DEFS   -- what objects they speak
  D_rare_*     the same two, after deleting every mathlib declaration used by
               8 or more of the ten. That is the generic-infrastructure strip:
               `Finset.sum_congr` says nothing about whether two developments
               are mathematically close, because everything uses it.
  D_arch       cosine distance between tactic profiles -- proof architecture

The infrastructure/mathematics split the brief asks for is exactly the
unstripped/stripped pair: what survives the strip is mathematics, what it
removes is infrastructure.
"""
import json
import math
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
GENERIC_THRESHOLD = 8          # used by >= 8 of 10 developments


def jac(a, b):
    a, b = set(a), set(b)
    if not a or not b:
        return 0.0
    i = len(a & b)
    return i / (len(a) + len(b) - i)


def main():
    vs = json.loads((OUT / "vocab_sets.json").read_text())
    census = json.loads((OUT / "census.json").read_text())["census"]
    names = sorted(vs)

    use_i = Counter()
    use_v = Counter()
    for n in names:
        use_i.update(set(vs[n]["iface"]))
        use_v.update(set(vs[n]["vocab"]))
    generic_i = {d for d, c in use_i.items() if c >= GENERIC_THRESHOLD}
    generic_v = {d for d, c in use_v.items() if c >= GENERIC_THRESHOLD}
    print("generic (used by >=%d of 10): %d interface, %d vocabulary"
          % (GENERIC_THRESHOLD, len(generic_i), len(generic_v)))

    I = {n: set(vs[n]["iface"]) for n in names}
    V = {n: set(vs[n]["vocab"]) for n in names}
    Ir = {n: I[n] - generic_i for n in names}
    Vr = {n: V[n] - generic_v for n in names}

    tac = {}
    for n in names:
        c = census[n]
        tac[n] = None
    # tactic profiles are recomputed here from the census's diversity fields
    # only as a fallback; the real profile is read from tactics_profile.json
    prof = json.loads((OUT / "tactics_profile.json").read_text()) \
        if (OUT / "tactics_profile.json").exists() else None

    def cos(a, b):
        ks = set(a) | set(b)
        na = math.sqrt(sum(a.get(k, 0) ** 2 for k in ks))
        nb = math.sqrt(sum(b.get(k, 0) ** 2 for k in ks))
        if not na or not nb:
            return 0.0
        return sum(a.get(k, 0) * b.get(k, 0) for k in ks) / (na * nb)

    mats = {}
    for tag, S in (("vocab", V), ("iface", I),
                   ("vocab_rare", Vr), ("iface_rare", Ir)):
        mats[tag] = {a: {b: round(jac(S[a], S[b]), 4) for b in names}
                     for a in names}
    if prof:
        mats["arch"] = {a: {b: round(cos(prof[a], prof[b]), 4) for b in names}
                        for a in names}

    out = {"label": "COMPUTED_FROM_ARTIFACT",
           "generic_threshold": GENERIC_THRESHOLD,
           "generic_interface_decls": len(generic_i),
           "generic_vocab_decls": len(generic_v),
           "sizes": {n: {"iface": len(I[n]), "vocab": len(V[n]),
                         "iface_rare": len(Ir[n]), "vocab_rare": len(Vr[n])}
                     for n in names},
           "matrices": mats}
    (OUT / "distance.json").write_text(json.dumps(out, indent=1) + "\n")

    print("\nper-development alphabet sizes:")
    print("%-32s %7s %7s %9s %9s" % ("", "iface", "vocab", "ifaceRare",
                                     "vocabRare"))
    for n in names:
        s = out["sizes"][n]
        print("%-32s %7d %7d %9d %9d" % (n, s["iface"], s["vocab"],
                                         s["iface_rare"], s["vocab_rare"]))
    import statistics as st
    for tag in mats:
        off = [mats[tag][a][b] for a in names for b in names if a < b]
        print("\n%-12s mean %.4f  median %.4f  min %.4f  max %.4f"
              % (tag, st.mean(off), st.median(off), min(off), max(off)))
    # correlation between the interface and vocabulary matrices
    xs = [mats["iface"][a][b] for a in names for b in names if a < b]
    ys = [mats["vocab"][a][b] for a in names for b in names if a < b]
    mx, my = st.mean(xs), st.mean(ys)
    r = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) /
         ((sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** .5))
    print("\nr(interface Jaccard, vocabulary Jaccard) = %.4f" % r)
    xs = [mats["iface_rare"][a][b] for a in names for b in names if a < b]
    ys = [mats["vocab_rare"][a][b] for a in names for b in names if a < b]
    mx, my = st.mean(xs), st.mean(ys)
    r2 = (sum((x - mx) * (y - my) for x, y in zip(xs, ys)) /
          ((sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** .5))
    print("r(rare interface,   rare vocabulary)     = %.4f" % r2)


if __name__ == "__main__":
    main()

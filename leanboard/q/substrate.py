#!/usr/bin/env python3
"""
Q2 -- the shared mathlib substrate, measured exactly.

The triangle FLT <-> mathlib <-> NS has two known edges. Before looking for the
missing one, measure how much of mathlib the two boards even have in common.
If the footprints are near-disjoint, Level-I object transport is close to ruled
out before any experiment runs, and that is a falsifier worth spending first.

Everything here is COMPUTED FROM ARTIFACT: module names come from `import`
lines in the two clones, nothing is inferred from namespace names.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

FLT = Path("/home/user/anthropics/fermats-last-theorem")
NS = Path("/home/user/openai/navierstokesandeuler")
OUT = Path(__file__).resolve().parent

IMPORT = re.compile(r"^(?:public\s+)?(?:meta\s+)?import\s+([A-Za-z0-9_.]+)",
                    re.M)


def imports(root, subdirs):
    """mathlib module -> number of board files importing it."""
    c = Counter()
    files = 0
    for sub in subdirs:
        d = root / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            files += 1
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            for m in set(IMPORT.findall(txt)):
                if m.startswith("Mathlib"):
                    c[m] += 1
    return c, files


def main():
    flt, nflt = imports(FLT, ["Theorems", "Definitions", "P2M"])
    ns, nns = imports(NS, ["NavierStokes", "Euler", "ComparatorChallenges"])
    sf, sn = set(flt), set(ns)
    shared = sf & sn

    def area(m):
        p = m.split(".")
        return p[1] if len(p) > 1 else "?"

    def areas(s):
        return Counter(area(m) for m in s)

    out = {
        "label": "COMPUTED_FROM_ARTIFACT",
        "flt": {"lean_files": nflt, "distinct_mathlib_modules": len(sf)},
        "ns": {"lean_files": nns, "distinct_mathlib_modules": len(sn)},
        "shared_modules": len(shared),
        "jaccard": round(len(shared) / len(sf | sn), 4),
        "shared_over_flt": round(len(shared) / len(sf), 4),
        "shared_over_ns": round(len(shared) / len(sn), 4),
        "shared_by_area": areas(shared).most_common(),
        "flt_only_by_area": areas(sf - sn).most_common(12),
        "ns_only_by_area": areas(sn - sf).most_common(12),
        "shared_list": sorted(shared),
        "shared_weighted": sorted(
            ((m, flt[m], ns[m]) for m in shared),
            key=lambda x: -(x[1] + x[2]))[:40],
    }
    (OUT / "substrate.json").write_text(json.dumps(out, indent=1) + "\n")

    print("FLT: %d files, %d distinct mathlib modules" % (nflt, len(sf)))
    print("NS : %d files, %d distinct mathlib modules" % (nns, len(sn)))
    print("shared: %d   Jaccard %.4f   (%.1f%% of FLT's, %.1f%% of NS's)"
          % (len(shared), out["jaccard"], 100 * out["shared_over_flt"],
             100 * out["shared_over_ns"]))
    print("\nshared modules by mathlib area:")
    for a, n in out["shared_by_area"]:
        print("   %-18s %d" % (a, n))
    print("\nFLT-only areas:", dict(out["flt_only_by_area"][:8]))
    print("NS-only areas :", dict(out["ns_only_by_area"][:8]))
    print("\nmost-used shared modules (flt files, ns files):")
    for m, a, b in out["shared_weighted"][:20]:
        print("   %-58s %5d %5d" % (m.replace("Mathlib.", ""), a, b))


if __name__ == "__main__":
    main()

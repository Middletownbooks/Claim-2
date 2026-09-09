#!/usr/bin/env python3
"""
Q1 -- decompose each board into regions by the MATHEMATICS each part uses.

FLT's declaration names carry a usable region structure (`ModularCurve`,
`CerednikDrinfeld`, `AutomorphicForm`, ...), which the previous phase already
exploited. NS's do not: its modules are named for construction stages
(`ActualCycleAssembly`, `AllOrderDriftBudget`, `ActivationCone`), so a
name-based decomposition would describe the authors' workflow rather than the
mathematics.

So both boards are decomposed the same way instead: each module is represented
by the mathlib areas its declarations reference, and regions are the modules
that share a mathlib profile. This is the decomposition the transport question
needs -- two regions can only exchange anything if they speak about the same
mathematics.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOARD = OUT.parent


def main():
    idx = json.loads((BOARD / "decls.json").read_text())["index"]
    pv = json.loads((OUT / "per_module_vocab.json").read_text())

    def area(d):
        m = idx.get(d, "")
        p = m.split(".")
        return ".".join(p[1:3]) if len(p) > 2 else (p[1] if len(p) > 1 else "?")

    out = {"label": "COMPUTED_FROM_ARTIFACT", "boards": {}}
    for b in ("flt", "ns"):
        prof = {}
        for mod, decls in pv[b].items():
            c = Counter(area(d) for d in decls)
            if c:
                prof[mod] = c
        # region = the mathlib subarea that dominates a module
        dom = Counter()
        members = defaultdict(list)
        for mod, c in prof.items():
            top = c.most_common(1)[0][0]
            dom[top] += 1
            members[top].append(mod)
        out["boards"][b] = {
            "modules_profiled": len(prof),
            "regions_by_dominant_mathlib_subarea": dom.most_common(25),
            "examples": {k: [m.split("/")[-1][:60] for m in members[k][:3]]
                         for k, _ in dom.most_common(12)},
        }
        print("== %s: %d modules profiled" % (b, len(prof)))
        for k, n in dom.most_common(14):
            print("   %-34s %6d   e.g. %s" % (k, n,
                  members[k][0].split("/")[-1][:52]))
        print()

    # cross-board: which mathlib subareas do BOTH boards have regions in?
    fa = dict(out["boards"]["flt"]["regions_by_dominant_mathlib_subarea"])
    na = dict(out["boards"]["ns"]["regions_by_dominant_mathlib_subarea"])
    both = sorted(set(fa) & set(na), key=lambda k: -(na.get(k, 0)))
    out["shared_region_subareas"] = [
        {"subarea": k, "flt_modules": fa[k], "ns_modules": na[k]} for k in both]
    print("mathlib subareas in which BOTH boards have regions:")
    for r in out["shared_region_subareas"][:20]:
        print("   %-34s flt=%-6d ns=%d" % (r["subarea"], r["flt_modules"],
                                           r["ns_modules"]))
    (OUT / "regions.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()

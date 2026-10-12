#!/usr/bin/env python3
"""
FLT External-Board Phase 1, steps 1-2: the mathlib <-> FLT boundary.

Two facts about the repository make this measurable without building anything:

  * `Theorems/Thm_X.lean` imports `Mathlib`, then exactly the
    `Definitions.Def_*` modules its STATEMENT needs, then its solution file.
    So a theorem whose Thm file imports no `Definitions.Def_*` is stated purely
    in mathlib's vocabulary -- upstreamable in principle, whatever its proof
    costs. This is a statement-level criterion, not a name-based one, which
    matters because the repository warns its names are machine-generated.
  * `P2M/Sol/S_X.lean` imports the mathlib modules the PROOF consumes.

Outputs boundary.json:
  consumption  -- which mathlib modules/areas the proof rests on
  definitions  -- the repo's own 1450 definition modules, ranked by how many
                  theorem STATEMENTS depend on them (its real interfaces)
  statements   -- per theorem: mathlib-vocabulary-only or repo-dependent
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("/home/user/anthropics/fermats-last-theorem")
OUT = Path(__file__).resolve().parent
BOARD = OUT.parent
IMP = re.compile(r"^import\s+([A-Za-z0-9_.]+)", re.M)
THM = re.compile(r"^theorem\s+([A-Za-z0-9_.'’]+)", re.M)


def main():
    mathlib_modules = set(json.loads(
        (BOARD / "modules.json").read_text())["modules"]) if (
            BOARD / "modules.json").exists() else set()

    # ---- what the PROOFS consume from mathlib ----
    sol_mathlib = defaultdict(set)
    for p in (REPO / "P2M" / "Sol").glob("S_*.lean"):
        name = p.stem[2:]
        for m in IMP.findall(p.read_text(encoding="utf-8", errors="replace")):
            if m.startswith("Mathlib"):
                sol_mathlib[name].add(m)
    used_modules = Counter()
    for mods in sol_mathlib.values():
        used_modules.update(mods)

    # ---- what the DEFINITIONS consume from mathlib ----
    def_mathlib = {}
    def_deps = {}
    for p in (REPO / "Definitions").glob("Def_*.lean"):
        name = p.stem[4:]
        imps = IMP.findall(p.read_text(encoding="utf-8", errors="replace"))
        # 411 of the 1450 definition modules import no Mathlib module directly
        # (they build only on other definitions), so the key must be created
        # unconditionally or the definition count under-reports.
        def_mathlib[name] = {m for m in imps if m.startswith("Mathlib")}
        def_deps[name] = sorted({m[len("Definitions.Def_"):] for m in imps
                                 if m.startswith("Definitions.Def_")})
    for mods in def_mathlib.values():
        used_modules.update(mods)

    # ---- statement vocabulary of every theorem ----
    statements = {}
    def_use = Counter()
    for p in (REPO / "Theorems").glob("Thm_*.lean"):
        text = p.read_text(encoding="utf-8", errors="replace")
        name = p.stem[4:]
        defs = [m[len("Definitions.Def_"):] for m in IMP.findall(text)
                if m.startswith("Definitions.Def_")]
        tm = THM.search(text)
        statements[name] = {
            "declared_as": tm.group(1) if tm else None,
            "statement_defs": sorted(set(defs)),
            "mathlib_vocabulary_only": not defs,
        }
        def_use.update(set(defs))

    mathlib_only = [k for k, v in statements.items()
                    if v["mathlib_vocabulary_only"]]

    known = used_modules.keys() & mathlib_modules if mathlib_modules else set()
    area = Counter(m.split(".")[1] for m in used_modules
                   if m.count(".") >= 1)

    out = {
        "consumption": {
            "distinct_mathlib_modules_imported": len(used_modules),
            "mathlib_modules_total_at_110cb7f0": len(mathlib_modules) or None,
            "coverage_fraction": (round(len(known) / len(mathlib_modules), 4)
                                  if mathlib_modules else None),
            "note": ("Coverage compares against mathlib at 110cb7f0 while the "
                     "artifact pins db584cd6; modules renamed between the two "
                     "will not match and are excluded from `known`."),
            "top_modules": used_modules.most_common(30),
            "by_area": area.most_common(),
        },
        "definitions": {
            "count": len(def_mathlib),
            "importing_no_mathlib_module_directly": sum(
                1 for v in def_mathlib.values() if not v),
            "definition_to_definition_edges": sum(
                len(v) for v in def_deps.values()),
            "most_used_by_statements": def_use.most_common(40),
            "used_by_no_statement": sorted(
                set(def_mathlib) - set(def_use))[:40],
            "unused_count": len(set(def_mathlib) - set(def_use)),
        },
        "statements": {
            "theorems": len(statements),
            "mathlib_vocabulary_only": len(mathlib_only),
            "repo_definition_dependent": len(statements) - len(mathlib_only),
            "fraction_mathlib_vocabulary_only":
                round(len(mathlib_only) / len(statements), 4),
            "defs_per_statement_histogram": dict(sorted(Counter(
                len(v["statement_defs"]) for v in statements.values()
            ).items())),
        },
    }
    (OUT / "boundary.json").write_text(json.dumps(
        {**out, "per_theorem": statements, "definition_deps": def_deps},
        indent=1, sort_keys=True))
    print(json.dumps(out, indent=2)[:3000])


if __name__ == "__main__":
    main()

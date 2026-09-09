#!/usr/bin/env python3
"""
First-pass analysis of openai/NavierStokesAndEuler, using the same method as
Report H/I for the FLT artifact: exact import graph from source, mathlib
consumption, and what it contains that mathlib does not.

Unlike the FLT artifact (pinned to Mathlib v4.33.0) this repository pins
v4.34.0-rc2, essentially the commit the board map measured, so the coverage
comparison here is like-for-like.
"""
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("/home/user/openai/navierstokesandeuler")
BOARD = Path(__file__).resolve().parent.parent
IMP = re.compile(r"^(?:public\s+)?(?:meta\s+)?import\s+([A-Za-z0-9_.]+)", re.M)
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?"
                  r"(?:private\s+|protected\s+|noncomputable\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance)\s+"
                  r"([A-Za-z_][A-Za-z0-9_'.]*)", re.M)


def main():
    files = sorted(p for p in REPO.rglob("*.lean")
                   if ".git" not in p.parts
                   and "ComparatorChallenges" not in p.parts)
    internal, mathlib_imports = {}, Counter()
    decls = Counter()
    names = []
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace")
        mod = ".".join(p.relative_to(REPO).with_suffix("").parts)
        ext = []
        for m in IMP.findall(t):
            if m.startswith("Mathlib"):
                mathlib_imports[m] += 1
            else:
                ext.append(m)
        internal[mod] = ext
        for kind, nm in DECL.findall(t):
            decls[kind] += 1
            names.append(nm)

    ml_modules = json.loads((BOARD / "modules.json").read_text())["modules"] \
        if (BOARD / "modules.json").exists() else {}
    area = Counter(m.split(".")[1] for m in mathlib_imports
                   if m.count(".") >= 1)

    # transitive importer counts inside the repo
    rev = defaultdict(set)
    for mod, deps in internal.items():
        for d in deps:
            rev[d].add(mod)
    depth = {}

    def d(mod, seen=frozenset()):
        if mod in depth:
            return depth[mod]
        if mod in seen:
            return 0
        vals = [d(x, seen | {mod}) for x in internal.get(mod, []) if x in internal]
        depth[mod] = 1 + max(vals) if vals else 0
        return depth[mod]
    for mod in internal:
        d(mod)

    out = {
        "repo": "openai/NavierStokesAndEuler",
        "commit": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True).strip(),
        "commit_date": subprocess.check_output(
            ["git", "-C", str(REPO), "log", "-1", "--format=%ci"],
            text=True).strip(),
        "lean_toolchain": (REPO / "lean-toolchain").read_text().strip(),
        "mathlib_pin": "v4.34.0-rc2 (the board map used mathlib 110cb7f0, also v4.34.0-rc2)",
        "lean_files": len(files),
        "declarations_by_kind": dict(decls.most_common()),
        "declarations_total": sum(decls.values()),
        "internal_modules": len(internal),
        "max_internal_import_depth": max(depth.values()),
        "distinct_mathlib_modules_imported": len(mathlib_imports),
        "mathlib_modules_total": len(ml_modules) or None,
        "coverage_fraction": round(len(set(mathlib_imports) & set(ml_modules))
                                   / len(ml_modules), 4) if ml_modules else None,
        "mathlib_by_area": area.most_common(),
        "top_mathlib_imports": mathlib_imports.most_common(15),
        "most_imported_internal": [
            (m, len(v)) for m, v in
            sorted(rev.items(), key=lambda kv: -len(kv[1]))[:12]],
        "namespace_clusters": Counter(
            n.split(".")[0] for n in names if "." in n).most_common(12),
    }
    (Path(__file__).parent / "ns_analysis.json").write_text(
        json.dumps(out, indent=1, sort_keys=True))
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("mathlib_by_area", "top_mathlib_imports",
                                   "most_imported_internal",
                                   "namespace_clusters")}, indent=2))
    print("\nmathlib areas consumed (distinct modules):")
    for a, c in area.most_common(12):
        print("  %4d  %s" % (c, a))
    print("\nmost-imported internal modules:")
    for m, c in out["most_imported_internal"][:8]:
        print("  %4d  %s" % (c, m))


if __name__ == "__main__":
    main()

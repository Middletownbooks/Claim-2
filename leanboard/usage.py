#!/usr/bin/env python3
"""
Phase 0 step 3: usage evidence for each board declaration.

METHOD (stated plainly because the numbers are only as good as it):
  For every declaration named in mathlib's 1000.yaml we run one ripgrep pass
  over Mathlib/ for (a) the fully-qualified name and (b) its final segment,
  both as whole words, and record the distinct files and distinct top-level
  areas that mention each.

  Lean resolves a declaration by its short name inside its own namespace and
  by its full name elsewhere, so:
     full-name file count   UNDER-counts (misses in-namespace uses)
     short-name file count  OVER-counts  (catches same-named decls elsewhere)
  The truth is bracketed by the two. Neither is a compiled dependency graph;
  this is textual evidence, labelled ACTUAL_SHARED_ABSTRACTION at best, never
  ACTUAL_LEAN_DEPENDENCY at declaration granularity. The module import graph
  in modules.json is the exact structural fact; this file is the approximation.
"""
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

MATHLIB = Path("/home/user/leanprover-community/mathlib4")
OUT = Path(__file__).resolve().parent


def main():
    board = json.loads((OUT / "board.json").read_text())
    decls_index = json.loads((OUT / "decls.json").read_text())["index"]

    targets = {}
    for r in board["records"]:
        for d in (r["mathlib_decls"] or []) + (
                [r["mathlib_statement_only"]] if r["mathlib_statement_only"]
                else []):
            targets[d] = r["wikidata"]

    patterns = set()
    for d in targets:
        patterns.add(d)
        patterns.add(d.split(".")[-1])
    pfile = OUT / ".patterns.txt"
    pfile.write_text("\n".join(sorted(patterns)) + "\n")

    proc = subprocess.run(
        ["rg", "-o", "-w", "-F", "-f", str(pfile), "--no-heading",
         "--with-filename", "-N", "--type", "lean", "Mathlib"],
        cwd=MATHLIB, capture_output=True, text=True)
    hits = defaultdict(set)
    for line in proc.stdout.splitlines():
        path, _, tok = line.partition(":")
        if tok:
            hits[tok].add(path)

    def area(path):
        parts = path.split("/")
        return parts[1] if len(parts) > 1 else parts[0]

    out = {}
    for d, qid in targets.items():
        short = d.split(".")[-1]
        home = decls_index.get(d) or decls_index.get(short)
        home_path = (home.replace(".", "/") + ".lean") if home else None
        full_files = {f for f in hits.get(d, set()) if f != home_path}
        short_files = {f for f in hits.get(short, set()) if f != home_path}
        out[d] = {
            "wikidata": qid,
            "defining_module": home,
            "files_referencing_full_name": len(full_files),
            "files_referencing_short_name": len(short_files),
            "areas_full_name": sorted({area(f) for f in full_files}),
            "areas_short_name": sorted({area(f) for f in short_files}),
            "domain_spread_full": len({area(f) for f in full_files}),
            "domain_spread_short": len({area(f) for f in short_files}),
        }
    pfile.unlink()
    (OUT / "usage.json").write_text(json.dumps(
        {"method": __doc__.strip(), "declarations": out}, indent=1,
        sort_keys=True))
    top = sorted(out.items(),
                 key=lambda kv: -kv[1]["files_referencing_full_name"])[:15]
    for d, v in top:
        print("%-62s full=%4d short=%5d areas=%2d" % (
            d[:62], v["files_referencing_full_name"],
            v["files_referencing_short_name"], v["domain_spread_full"]))


if __name__ == "__main__":
    main()

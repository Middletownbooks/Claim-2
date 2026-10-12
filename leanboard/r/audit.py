#!/usr/bin/env python3
"""
Phase R, step 1 -- audit the ten-proofs artifact and produce the same
structural statistics used for FLT and NS.

The first structural fact dominates everything else and is visible before any
analysis: each of the ten results is a SINGLE Lean file. There is no module
dependency graph to extract, where FLT has 60 474 modules and NS 2 484. So the
`E` of B = (V, E, A, I, P, F) has to be recovered, if at all, from
declaration-to-declaration references inside one file.
"""
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path("/home/user/openai/ten-proofs")
OUT = Path(__file__).resolve().parent

DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque|axiom)\s+"
    r"([A-Za-z0-9_.'!?«»]+)", re.M)
IMPORT = re.compile(r"^(?:public\s+)?(?:meta\s+)?import\s+([A-Za-z0-9_.]+)", re.M)
NAMESPACE = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)", re.M)
HAZARD = {
    "sorry": re.compile(r"(?<![A-Za-z0-9_])sorry(?![A-Za-z0-9_])"),
    "admit": re.compile(r"(?<![A-Za-z0-9_])admit(?![A-Za-z0-9_])"),
    "axiom": re.compile(r"^axiom\s", re.M),
    "native_decide": re.compile(r"native_decide"),
    "unsafe": re.compile(r"^unsafe\s", re.M),
    "partial_def": re.compile(r"^partial\s+def\s", re.M),
    "implemented_by": re.compile(r"implemented_by"),
    "extern": re.compile(r"@\[extern"),
}


def audit(p):
    txt = p.read_text(errors="ignore")
    decls = DECL.findall(txt)
    kinds = Counter(k for k, _ in decls)
    imports = IMPORT.findall(txt)
    ml = [i for i in imports if i.startswith("Mathlib")]
    nss = Counter(NAMESPACE.findall(txt))
    return {
        "file": p.name,
        "bytes": p.stat().st_size,
        "lines": txt.count("\n") + 1,
        "declarations": len(decls),
        "by_kind": dict(kinds),
        "theorems": kinds.get("theorem", 0) + kinds.get("lemma", 0),
        "definitions": (kinds.get("def", 0) + kinds.get("abbrev", 0) +
                        kinds.get("structure", 0) + kinds.get("class", 0) +
                        kinds.get("inductive", 0)),
        "imports_total": len(imports),
        "mathlib_imports": len(ml),
        "mathlib_import_list": sorted(ml),
        "namespaces": nss.most_common(12),
        "hazards": {k: len(rx.findall(txt)) for k, rx in HAZARD.items()},
        "comment_lines": len(re.findall(r"^\s*(--|/-)", txt, re.M)),
        "proofs_by": len(re.findall(r":=\s*by\b", txt)),
    }


def main():
    rows = [audit(p) for p in sorted(REPO.glob("*.lean")) if p.name != "All.lean"]
    out = {"label": "COMPUTED_FROM_ARTIFACT",
           "repo": "openai/ten-proofs",
           "lean_toolchain": (REPO / "lean-toolchain").read_text().strip(),
           "one_file_per_result": True,
           "files": rows}
    (OUT / "audit.json").write_text(json.dumps(out, indent=1) + "\n")

    print("%-32s %8s %8s %8s %8s %7s %7s %6s" % (
        "file", "MB", "decls", "thms", "defs", "mlimp", "proofs", "cmt"))
    for r in sorted(rows, key=lambda r: -r["declarations"]):
        print("%-32s %8.2f %8d %8d %8d %7d %7d %6d" % (
            r["file"][:32], r["bytes"] / 1e6, r["declarations"], r["theorems"],
            r["definitions"], r["mathlib_imports"], r["proofs_by"],
            r["comment_lines"]))
    print("\nhazards (any nonzero):")
    for r in rows:
        h = {k: v for k, v in r["hazards"].items() if v}
        if h:
            print("   %-32s %s" % (r["file"], h))
    else:
        pass
    tot = Counter()
    for r in rows:
        for k, v in r["hazards"].items():
            tot[k] += v
    print("   totals:", dict(tot))


if __name__ == "__main__":
    main()

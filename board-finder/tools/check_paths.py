#!/usr/bin/env python3
"""Report backtick-quoted paths in board-finder/ that resolve under no convention.

WHY THIS IS A REPORT AND NOT A BUILD FAILURE. proof-protocol/tools/check_consistency.py
check 14 verifies "every backtick-quoted path whose first segment is in this tree
resolves" -- and "this tree" is proof-protocol. board-finder, where almost all of
this project's prose lives, has never been covered. This script measures that gap.
It exits 0 on purpose: the breakage it finds is pre-existing and spread across
documents written by several instances, and this project's rule is that a check
which could not fail is a finding to report, not to silently repair.

Two conventions are both in live use in board-finder and both are counted as
resolving, because neither is wrong -- the tree simply never picked one:
  file-relative       `../gap/GAP_V3.md`      from the citing document
  repo-root-relative  `proof-protocol/ledger.json`  from the repository root

Run:  python3 board-finder/tools/check_paths.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TREE = os.path.join(ROOT, "board-finder")
PATHISH = re.compile(r"\.(md|py|json|txt|png|csv)$")

# Paths naming a DIFFERENT repository are not broken local paths, and counting
# them as such inflates the number D52 is measured by. A citation is treated as
# cross-repo when its first segment is a known sibling repository.
CROSS_REPO_ROOTS = ("Cooperative-AI-Defense/", "leanboard/")


def is_path_candidate(token):
    """Exclude things that look like paths but are not: URLs, absolute web paths,
    shell commands, and the web's own robots.txt."""
    if token.startswith(("http", "/")):
        return False
    if " " in token:                       # e.g. `python3 classify.py`
        return False
    if token.endswith("robots.txt"):       # a web reference, not a file here
        return False
    return bool(PATHISH.search(token))


def scan():
    by_file, unresolved, cross = {"file": 0, "root": 0}, [], []
    for base, _dirs, files in os.walk(TREE):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            doc = os.path.join(base, fn)
            text = open(doc, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"`([^`\n]+)`", text):
                tok = m.group(1)
                if not is_path_candidate(tok):
                    continue
                if tok.startswith(CROSS_REPO_ROOTS):
                    cross.append((os.path.relpath(doc, ROOT), tok))
                elif os.path.exists(os.path.normpath(os.path.join(base, tok))):
                    by_file["file"] += 1
                elif os.path.exists(os.path.normpath(os.path.join(ROOT, tok))):
                    by_file["root"] += 1
                else:
                    unresolved.append((os.path.relpath(doc, ROOT), tok))
    return by_file, unresolved, cross


def main():
    counts, unresolved, cross = scan()
    distinct = sorted(set(unresolved))
    print(f"board-finder backticked path citations")
    print(f"  resolve file-relative:      {counts['file']}")
    print(f"  resolve repo-root-relative: {counts['root']}")
    print(f"  name another repository:    {len(cross)} "
          f"(not broken -- see CROSS_REPO_ROOTS)")
    print(f"  resolve under NEITHER:      {len(unresolved)} "
          f"({len(distinct)} distinct document/target pairs)")
    if distinct:
        print()
        print("  unresolved:")
        for doc, tok in distinct:
            print(f"    {doc}  ->  {tok}")
    print()
    print("  exit 0 by design; see the module docstring and debt D52.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

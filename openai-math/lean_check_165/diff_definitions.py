#!/usr/bin/env python3
"""Check that the Comparator challenge's definitions are the ones the proof proves things about.

  usage: python3 diff_definitions.py /path/to/openai/math

A Comparator challenge restates the target with `sorry`; the solution module proves a theorem of
the same name. If a definition the statement depends on differs between the two files, a reader
of the challenge is reading a different theorem from the one that was proved. Comparator checks
this mechanically; it is not installed here (it needs landrun and lean4export), so this does the
textual part of that check: every top-level def/abbrev/structure in the challenge must occur,
character for character, in the solution's definition files.
"""
import os, re, sys

CHALLENGE = "lean/ComparatorChallenges/BipartiteCrossing.lean"
SOLUTION = ["lean/OAI/Combinatorics/Crossing/DrawingDefinition.lean",
            "lean/OAI/Combinatorics/Crossing/FloorArithmetic.lean"]
DECL = re.compile(r"^(def|abbrev|structure) (\S+)(.*?)(?=^\S|\Z)", re.S | re.M)


def decls(text):
    return {m.group(2): m.group(0).strip() for m in DECL.finditer(text)}


def main(root):
    ch = decls(open(os.path.join(root, CHALLENGE), encoding="utf-8").read())
    sol = {}
    for p in SOLUTION:
        sol.update(decls(open(os.path.join(root, p), encoding="utf-8").read()))
    bad = [k for k, v in ch.items() if sol.get(k) != v]
    for k in ch:
        print("%-22s %s" % (k, "IDENTICAL" if k not in bad else "DIFFERS"))
    print("%d of %d challenge definitions identical in the solution" % (len(ch) - len(bad), len(ch)))
    assert "MainTarget" in ch and len(ch) == 11, "challenge file changed shape; re-read it"
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1])

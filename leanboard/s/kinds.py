#!/usr/bin/env python3
"""
S2 -- the mathlib declaration-kind index, which the whole phase rests on.

The falsification question needs a mechanical distinction between an INTERFACE
and a VOCABULARY item. Declaration kind supplies one that does not depend on
anybody's judgement:

  INTERFACE   structure, class, inductive, def, abbrev, instance
              -- the TYPES and ABSTRACTIONS a development speaks
  VOCABULARY  theorem, lemma
              -- the FACTS it cites

Two developments that both use `NormedAddCommGroup`, `Fintype` and
`Matrix.PosSemidef` share an interface: they are talking about the same kinds
of object. Two that both cite `add_comm` merely share a word.

`decls.json` from the earlier phase maps name -> module and has no kinds, so
they are re-extracted from mathlib source here.
"""
import json
import re
from collections import Counter
from pathlib import Path

MATHLIB = Path("/home/user/leanprover-community/mathlib4")
OUT = Path(__file__).resolve().parent
BOARD = OUT.parent

DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?"
    r"(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|nonrec\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque|axiom)"
    r"\s+([A-Za-z0-9_.'!?«»]+)", re.M)
NSOPEN = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)", re.M)
NSEND = re.compile(r"^end\b\s*([A-Za-z0-9_.']*)", re.M)

INTERFACE_KINDS = {"structure", "class", "inductive", "def", "abbrev",
                   "instance"}
VOCAB_KINDS = {"theorem", "lemma"}


def main():
    kind = {}
    n = 0
    for p in (MATHLIB / "Mathlib").rglob("*.lean"):
        n += 1
        if n % 2000 == 0:
            print("  %d files" % n, flush=True)
        try:
            txt = p.read_text(errors="ignore")
        except Exception:
            continue
        events = []
        for m in DECL.finditer(txt):
            events.append((m.start(), "d", m.group(1), m.group(2)))
        for m in NSOPEN.finditer(txt):
            events.append((m.start(), "n", None, m.group(1)))
        for m in NSEND.finditer(txt):
            events.append((m.start(), "e", None, m.group(1)))
        events.sort()
        stack = []
        for _, t, k, name in events:
            if t == "n":
                stack.append(name)
            elif t == "e":
                if stack:
                    stack.pop()
            else:
                full = ".".join(stack + [name]) if stack else name
                # first definition wins; mathlib rarely redefines a full name
                kind.setdefault(full, k)
                kind.setdefault(name, k)
                kind.setdefault(full.split(".")[-1], k)

    idx = json.loads((BOARD / "decls.json").read_text())["index"]
    covered = sum(1 for d in idx if d in kind)
    c = Counter(kind.get(d, "UNKNOWN") for d in idx)
    out = {"label": "COMPUTED_FROM_ARTIFACT",
           "mathlib_files": n,
           "names_with_kind": len(kind),
           "decls_json_entries": len(idx),
           "decls_json_covered": covered,
           "coverage": round(covered / len(idx), 4),
           "kind_distribution_over_decls_json": c.most_common(),
           "interface_kinds": sorted(INTERFACE_KINDS),
           "vocabulary_kinds": sorted(VOCAB_KINDS)}
    (OUT / "kinds_summary.json").write_text(json.dumps(out, indent=1) + "\n")
    json.dump(kind, open(OUT / "kinds.json", "w"))
    print("\nmathlib files scanned: %d" % n)
    print("names with a kind: %d" % len(kind))
    print("decls.json coverage: %d/%d = %.1f%%"
          % (covered, len(idx), 100 * out["coverage"]))
    print("kinds over decls.json:", dict(c.most_common(10)))


if __name__ == "__main__":
    main()

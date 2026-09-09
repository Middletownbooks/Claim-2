#!/usr/bin/env python3
"""
Phase 0 step 2: structural facts about mathlib, computed from source.

Produces three artifacts:

  modules.json  -- the EXACT module import graph (parsed from `import` lines),
                   with transitive ancestor/descendant counts per module.
                   These are ACTUAL_LEAN_DEPENDENCY facts at module granularity.

  decls.json    -- a declaration index (fully-qualified name -> file), built by
                   a namespace-tracking scan. APPROXIMATE: it understands
                   `namespace`/`end`/`section` and the common declaration
                   keywords, and will miss exotic forms.

  usage.json    -- for each 1000-board declaration, how many distinct files
                   mention it and in how many distinct top-level Mathlib
                   areas. APPROXIMATE and stated as such: Lean lets a
                   declaration be referenced by its short name inside its own
                   namespace, so a full-name count under-counts and a
                   short-name count over-counts. Both are reported.
"""
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

MATHLIB = Path("/home/user/leanprover-community/mathlib4")
OUT = Path(__file__).resolve().parent
ROOTS = ["Mathlib"]

# mathlib migrated to `public import` / `public meta import`: a regex matching
# only bare `import` sees 593 of 26 471 edges (2.2%) and yields a near-empty
# graph. All import forms are counted as dependency edges.
IMPORT_RE = re.compile(
    r"^(?:public\s+)?(?:meta\s+)?import\s+([A-Za-z0-9_.]+)", re.M)
DECL_RE = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?"
    r"(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|alias)\s+"
    r"([A-Za-z_α-ω][A-Za-z0-9_'.₀-₉]*)")
NS_RE = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)")
END_RE = re.compile(r"^end\b\s*([A-Za-z0-9_.']*)")


def module_name(path):
    rel = path.relative_to(MATHLIB).with_suffix("")
    return ".".join(rel.parts)


def build():
    files = sorted(p for r in ROOTS
                   for p in (MATHLIB / r).rglob("*.lean"))
    texts = {}
    imports = {}
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace")
        texts[p] = t
        mod = module_name(p)
        imports[mod] = [m for m in IMPORT_RE.findall(t)
                        if m.startswith("Mathlib")]
    mods = sorted(imports)
    idx = {m: i for i, m in enumerate(mods)}
    n = len(mods)

    # exact transitive closures over the import DAG, as bitmasks
    up = [0] * n          # modules this one transitively imports
    order = []
    state = [0] * n

    def visit(i):
        # iterative DFS to avoid recursion limits
        stack = [(i, False)]
        while stack:
            v, done = stack.pop()
            if done:
                mask = 0
                for w in imports[mods[v]]:
                    j = idx.get(w)
                    if j is not None:
                        mask |= up[j] | (1 << j)
                up[v] = mask
                state[v] = 2
                order.append(v)
                continue
            if state[v]:
                continue
            state[v] = 1
            stack.append((v, True))
            for w in imports[mods[v]]:
                j = idx.get(w)
                if j is not None and state[j] == 0:
                    stack.append((j, False))

    for i in range(n):
        if state[i] == 0:
            visit(i)

    down = [0] * n
    for i in range(n):
        m = up[i]
        while m:
            b = m & -m
            j = b.bit_length() - 1
            down[j] |= (1 << i)
            m ^= b

    def areas_of(mask):
        out = set()
        m = mask
        while m:
            b = m & -m
            j = b.bit_length() - 1
            parts = mods[j].split(".")
            if len(parts) > 1:
                out.add(parts[1])
            m ^= b
        return out

    modules = {}
    for i in range(n):
        imp_areas = areas_of(down[i])
        modules[mods[i]] = {
            "direct_imports": len(imports[mods[i]]),
            "transitive_imports": bin(up[i]).count("1"),
            "transitive_importers": bin(down[i]).count("1"),
            # EXACT: distinct top-level areas containing a module that
            # transitively imports this one.
            "importer_areas": sorted(imp_areas),
            "importer_area_count": len(imp_areas),
            "area": mods[i].split(".")[1] if mods[i].count(".") >= 1 else None,
        }
    (OUT / "modules.json").write_text(json.dumps(
        {"module_count": n, "modules": modules}, indent=1, sort_keys=True))

    # ---- declaration index -------------------------------------------------
    decl_file = {}
    root_level = {}
    for p in files:
        mod = module_name(p)
        ns = []
        for line in texts[p].splitlines():
            m = NS_RE.match(line)
            if m:
                ns.append(m.group(1))
                continue
            if END_RE.match(line):
                m2 = END_RE.match(line)
                if m2.group(1) and ns and ns[-1] == m2.group(1):
                    ns.pop()
                elif m2.group(1) and m2.group(1) in ns:
                    while ns and ns[-1] != m2.group(1):
                        ns.pop()
                    if ns:
                        ns.pop()
                continue
            d = DECL_RE.match(line)
            if d:
                name = d.group(2)
                full = ".".join(ns + [name]) if ns else name
                decl_file.setdefault(full, mod)
                # A bare key must prefer a ROOT-LEVEL declaration of that name.
                # Without this, `Tropical.add_pow` (scanned first, being under
                # Mathlib/Algebra/) claimed the key `add_pow` and the binomial
                # theorem was misattributed to the tropical semiring file.
                if not ns:
                    root_level.setdefault(name, mod)
    for name, mod in root_level.items():
        decl_file[name] = mod
    (OUT / "decls.json").write_text(json.dumps(
        {"declaration_count": len(decl_file), "index": decl_file},
        indent=0, sort_keys=True))
    print(json.dumps({"modules": n, "declarations_indexed": len(decl_file)},
                     indent=2))


if __name__ == "__main__":
    build()

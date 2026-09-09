#!/usr/bin/env python3
"""
Phase 1 step 1 for openai/NavierStokesAndEuler: a declaration index and an
APPROXIMATE declaration-level dependency graph.

METHOD, AND WHY IT IS WEAKER THAN THE FLT ONE
---------------------------------------------
The FLT artifact documents a convention (`P2M/Sol/S_X.lean`'s
`import Theorems.Thm_...` lines ARE its citations), so its graph is exact. This
repository is ordinary Lean: declarations and proofs live together and there is
no such convention. So here:

  * a declaration runs from its keyword line to the next top-level keyword line;
  * its STATEMENT is the text up to the proof separator, its PROOF the rest;
  * identifiers are extracted textually and intersected with the repo's own
    declaration names.

That is an over-approximation in one direction (a name mentioned in a comment or
shadowed by a local binder counts) and an under-approximation in another
(anything reached by typeclass inference, `simp` sets, or automation is
invisible). Every number derived from it is labelled APPROXIMATE and none is
called an ACTUAL_LEAN_DEPENDENCY at declaration granularity.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("/home/user/openai/navierstokesandeuler")
OUT = Path(__file__).resolve().parent
BOARD = OUT.parent

KEYWORDS = r"(theorem|lemma|def|abbrev|structure|class|instance|inductive)"
DECL_START = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?"
    r"(?:private\s+|protected\s+|noncomputable\s+|scoped\s+|partial\s+)*"
    + KEYWORDS + r"\s+([A-Za-z_][A-Za-z0-9_'.]*)", re.M)
NS_RE = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)", re.M)
END_RE = re.compile(r"^end\s+([A-Za-z0-9_.']+)", re.M)
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
SEP = re.compile(r":=\s*(?:by\b|$)|:=\s", re.M)


LOOSE = "--loose" in sys.argv


def main():
    files = sorted(p for p in REPO.rglob("*.lean")
                   if ".git" not in p.parts
                   and "ComparatorChallenges" not in p.parts)
    decls = {}          # full name -> record
    order = []
    for p in files:
        mod = ".".join(p.relative_to(REPO).with_suffix("").parts)
        text = p.read_text(encoding="utf-8", errors="replace")
        # namespace stack, tracked linearly
        stack, marks = [], []
        for m in re.finditer(r"^(namespace|end)\s+([A-Za-z0-9_.']+)", text, re.M):
            marks.append((m.start(), m.group(1), m.group(2)))
        starts = [(m.start(), m.group(1), m.group(2))
                  for m in DECL_START.finditer(text)]
        for i, (pos, kind, name) in enumerate(starts):
            stack = []
            for mpos, what, nm in marks:
                if mpos > pos:
                    break
                if what == "namespace":
                    stack.append(nm)
                elif stack and stack[-1] == nm:
                    stack.pop()
            end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
            body = text[pos:end]
            sep = SEP.search(body)
            stmt = body[:sep.start()] if sep else body
            proof = body[sep.end():] if sep else ""
            full = ".".join(stack + [name]) if stack else name
            if full in decls:
                continue
            decls[full] = {"kind": kind, "module": mod, "short": name,
                           "stmt": stmt, "proof": proof}
            order.append(full)

    names = set(decls)
    short_index = defaultdict(set)
    for f in names:
        short_index[f.split(".")[-1]].add(f)

    # Resolution rule, tightened after a first pass produced 1.8M edges for 49k
    # declarations (10x the FLT artifact's density): a bare short name is
    # resolved ONLY when it is unambiguous in this repository and is not also a
    # mathlib name, and single/double-character tokens (local binders) are
    # ignored. This trades recall for precision, deliberately.
    def make_resolver(ml_names):
        def repo_refs(txt, exclude):
            out = set()
            for tok in IDENT.findall(txt):
                if len(tok) <= 2:
                    continue
                if tok in names:
                    if tok != exclude:
                        out.add(tok)
                    continue
                last = tok.split(".")[-1]
                cands = short_index.get(last)
                if not cands:
                    continue
                if LOOSE:
                    for c in cands:
                        if c != exclude:
                            out.add(c)
                elif len(cands) == 1 and tok not in ml_names \
                        and last not in ml_names:
                    c = next(iter(cands))
                    if c != exclude:
                        out.add(c)
            return out
        return repo_refs

    ml_early = set(json.loads((BOARD / "decls.json").read_text())["index"]) \
        if (BOARD / "decls.json").exists() else set()
    repo_refs = make_resolver(ml_early)
    graph, stmt_repo = {}, {}
    for full, rec in decls.items():
        graph[full] = sorted(repo_refs(rec["proof"], full))
        stmt_repo[full] = sorted(repo_refs(rec["stmt"], full))

    ml = ml_early

    out = {
        "method": __doc__.strip(),
        "declarations": len(decls),
        "by_kind": dict(Counter(r["kind"] for r in decls.values())),
        "edges_approx": sum(len(v) for v in graph.values()),
        "statements_with_no_repo_identifier": sum(
            1 for v in stmt_repo.values() if not v),
        "ambiguous_short_names": sum(1 for v in short_index.values()
                                     if len(v) > 1),
        "unambiguous_short_names": sum(1 for v in short_index.values()
                                       if len(v) == 1),
        "mathlib_index_size": len(ml) or None,
    }
    (OUT / ("ns_graph_loose.json" if LOOSE else "ns_graph.json")).write_text(json.dumps(
        {"summary": out, "graph": graph,
         "stmt_repo": stmt_repo,
         "meta": {k: {"kind": v["kind"], "module": v["module"]}
                  for k, v in decls.items()}}, indent=0, sort_keys=True))
    print(json.dumps(out, indent=2)[:1200])


if __name__ == "__main__":
    main()

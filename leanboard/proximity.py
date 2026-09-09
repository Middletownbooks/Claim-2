#!/usr/bin/env python3
"""
Per-target proximity evidence for MISSING board entries.

The class-level features (area size, growth, MSC cluster) are identical for
every target in a class, so on their own they rank nothing. This adds a
genuinely per-target observable: does mathlib already TALK about this target?

For each missing entry we extract distinctive tokens from its title (proper
nouns and rare capitalised words), search Mathlib case-sensitively for them as
whole words, and record:

  * how many files mention it, and in how many areas;
  * whether mentions occur in declaration names (partial formalisation exists)
    or only in comments/docstrings (developers are aiming at it);
  * the mentioning modules, so a human can check.

A docstring saying "this is an ingredient for the Mordell-Weil theorem" is
DOCUMENTED_MATHEMATICAL_RELATION evidence that a corridor is under
construction. It is never an ACTUAL_LEAN_DEPENDENCY: the target is missing.

Titles without a distinctive token (e.g. "Preimage theorem") are reported as
evidence_unavailable rather than scored on a generic word.
"""
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

MATHLIB = Path("/home/user/leanprover-community/mathlib4")
OUT = Path(__file__).resolve().parent

STOP = {
    "Theorem", "Theorems", "Lemma", "Conjecture", "Formula", "Identity",
    "Inequality", "Law", "Rule", "Principle", "Problem", "Criterion",
    "Equation", "Equations", "Property", "Paradox", "Algorithm", "Test",
    "The", "And", "Of", "For", "On", "In", "Fundamental", "Basic", "General",
    "Main", "First", "Second", "Third", "Little", "Last", "Great", "Big",
    "Small", "Finite", "Infinite", "Prime", "Number", "Numbers", "Function",
    "Functions", "Group", "Groups", "Ring", "Rings", "Field", "Fields",
    "Space", "Spaces", "Set", "Sets", "Series", "Sum", "Product", "Point",
    "Points", "Curve", "Curves", "Surface", "Class", "Classes", "Form",
    "Forms", "Map", "Mapping", "Value", "Values", "Zero", "One", "Two",
    "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
    "Preimage", "Isomorphism", "Structure", "Decomposition", "Expansion",
    "Convergence", "Approximation", "Existence", "Uniqueness", "Duality",
    "Embedding", "Extension", "Representation", "Transform", "Transformation",
}
TOKEN_RE = re.compile(r"[A-Z][A-Za-zÀ-ÿ'’\-]{3,}")


def tokens_for(title):
    if not title:
        return []
    raw = TOKEN_RE.findall(title)
    out = []
    for t in raw:
        t = t.replace("’", "'")
        base = t.split("'")[0].split("-")[0]
        if len(base) < 4 or base in STOP:
            continue
        out.append(base)
    return sorted(set(out))


def main():
    board = json.loads((OUT / "board.json").read_text())
    missing = [r for r in board["records"] if r["status"] == "missing"]

    tok_map = {}
    all_tokens = set()
    for r in missing:
        ts = tokens_for(r["title"])
        tok_map[r["wikidata"]] = ts
        all_tokens.update(ts)

    pfile = OUT / ".ptokens.txt"
    pfile.write_text("\n".join(sorted(all_tokens)) + "\n")
    # -n keeps line numbers so header lines can be dropped: mathlib file
    # headers carry "Authors: ..." lines, and matching surnames there produced
    # hundreds of spurious hits ("Lee", "Yang") in the first version of this
    # script. Copyright/licence/author lines are excluded outright.
    proc = subprocess.run(
        ["rg", "-o", "-w", "-F", "-f", str(pfile), "--no-heading",
         "--with-filename", "-n", "--type", "lean", "Mathlib"],
        cwd=MATHLIB, capture_output=True, text=True)
    header_cache = {}

    def is_header(path, lineno):
        lines = header_cache.get(path)
        if lines is None:
            try:
                lines = (MATHLIB / path).read_text(
                    encoding="utf-8", errors="replace").splitlines()
            except OSError:
                lines = []
            header_cache[path] = lines
        if 1 <= lineno <= len(lines):
            t = lines[lineno - 1]
            return (t.startswith("Copyright") or t.startswith("Authors:")
                    or "Released under Apache" in t
                    or t.startswith("Author:"))
        return False

    hits = defaultdict(set)
    for line in proc.stdout.splitlines():
        parts = line.split(":", 2)
        if len(parts) != 3:
            continue
        path, lineno, tok = parts[0], parts[1], parts[2]
        if not lineno.isdigit() or not tok:
            continue
        if is_header(path, int(lineno)):
            continue
        hits[tok].add(path)

    # Data-driven genericity filter: a token occurring in a large fraction of
    # the library is not evidence about any particular theorem.
    GENERIC_CUTOFF = 40
    generic = {t for t, fs in hits.items() if len(fs) > GENERIC_CUTOFF}

    # which mentions are inside declaration names (as opposed to prose)?
    decl_index = json.loads((OUT / "decls.json").read_text())["index"]
    decl_tokens = defaultdict(set)
    for name in decl_index:
        for part in re.split(r"[._]", name):
            if part and part[0].isupper() and part in all_tokens:
                decl_tokens[part].add(decl_index[name])

    out = {}
    for r in missing:
        ts = tok_map[r["wikidata"]]
        if not ts:
            out[r["wikidata"]] = {"evidence_unavailable": True,
                                  "reason": "no distinctive token in title",
                                  "tokens": []}
            continue
        informative = [t for t in ts if t not in generic]
        if not informative:
            out[r["wikidata"]] = {
                "evidence_unavailable": True,
                "reason": "every title token is generic in mathlib (>%d files)"
                          % GENERIC_CUTOFF,
                "tokens": ts,
            "informative_tokens": informative, "generic_tokens": sorted(set(ts) & generic)}
            continue
        # For a multi-name title ("Lee-Yang"), require a file to mention every
        # informative token: one surname alone is weak evidence.
        sets = [hits.get(t, set()) for t in informative]
        files = set.intersection(*sets) if len(sets) > 1 else sets[0]
        areas = {f.split("/")[1] for f in files if f.count("/") >= 2}
        in_decls = set()
        for t in informative:
            in_decls |= decl_tokens.get(t, set())
        out[r["wikidata"]] = {
            "tokens": ts,
            "informative_tokens": informative,
            "files_mentioning": len(files),
            "areas_mentioning": sorted(areas),
            "area_count": len(areas),
            "appears_in_declaration_names": len(in_decls),
            "example_modules": sorted(
                f.replace("/", ".")[:-5] for f in sorted(files)[:6]),
            # A single common surname ("Euler", "Frobenius") cannot tell two
            # theorems of that name apart, so proximity is only reported as
            # discriminating when the token set actually identifies the target.
            "discriminating": (len(informative) > 1
                               or len(hits.get(informative[0], set())) <= 12),
            "evidence_class": (
                "PARTIAL_FORMALIZATION_PRESENT" if in_decls else
                "MENTIONED_IN_PROSE_ONLY" if files else
                "NO_MENTION_IN_MATHLIB"),
        }
    pfile.unlink()
    (OUT / "proximity.json").write_text(json.dumps(
        {"method": __doc__.strip(), "targets": out}, indent=1, sort_keys=True))

    ranked = sorted(
        ((v.get("files_mentioning", 0), q, v) for q, v in out.items()),
        reverse=True)[:20]
    titles = {r["wikidata"]: r["title"] for r in missing}
    for n, q, v in ranked:
        print("%-44s files=%3d areas=%2d decls=%3d %s" % (
            (titles[q] or "")[:44], n, v.get("area_count", 0),
            v.get("appears_in_declaration_names", 0), v.get("evidence_class")))


if __name__ == "__main__":
    main()

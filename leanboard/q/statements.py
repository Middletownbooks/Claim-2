#!/usr/bin/env python3
"""
Q5 step 1 -- extract every theorem STATEMENT from both boards and reduce it to
a comparable signature.

A statement's signature is the set of mathlib declaration names occurring in it
(from the 1948-name shared vocabulary plus each board's own mathlib usage),
together with a small skeleton of logical structure. Two statements with the
same signature are saying something about the same mathlib objects in the same
logical shape; that is the mechanical stand-in for "the same lemma", and it is
deliberately generous -- it over-generates candidates, which the later stages
then have to survive.
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOARD = OUT.parent
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECL = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)?"
    r"(theorem|lemma)\s+([A-Za-z0-9_.'!?]+)", re.M)
SKEL = {"forall": r"∀", "exists": r"∃", "imp": r"→", "not": r"¬",
        "le": r"≤", "lt": r"<", "eq": r"=", "and": r"∧", "or": r"∨",
        "iff": r"↔", "norm": r"‖", "integral": r"∫", "sum": r"∑",
        "False": r"\bFalse\b"}


def statement_body(txt, start):
    """From the declaration keyword to the `:= by` / `:= ` that ends the type."""
    m = re.compile(r":=\s*(by\b|\bby\n)|:=\s").search(txt, start)
    return txt[start:m.start()] if m else txt[start:start + 4000]


def extract(root, subs, vocab, limit_files=None):
    out = []
    n = 0
    for sub in subs:
        d = Path(root) / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            n += 1
            if limit_files and n > limit_files:
                break
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            for m in DECL.finditer(txt):
                body = statement_body(txt, m.end())
                toks = set(TOK.findall(body))
                sig = sorted(toks & vocab)
                if not sig:
                    continue
                out.append({
                    "name": m.group(2),
                    "file": str(p.relative_to(root)),
                    "sig": sig,
                    "skel": {k: len(re.findall(r, body)) for k, r in SKEL.items()
                             if re.search(r, body)},
                    "len": len(body),
                })
    return out


def main():
    idx = json.loads((BOARD / "decls.json").read_text())["index"]
    vocab = {k for k in idx if "." in k} | {
        k for k in idx if "." not in k
        and ("_" in k or any(c.isupper() for c in k))}

    ns = extract("/home/user/openai/navierstokesandeuler",
                 ["NavierStokes", "Euler"], vocab)
    json.dump(ns, open(OUT / "stmts_ns.json", "w"))
    print("NS statements with mathlib vocabulary: %d" % len(ns), flush=True)

    flt = extract("/home/user/anthropics/fermats-last-theorem",
                  ["Theorems"], vocab)
    json.dump(flt, open(OUT / "stmts_flt.json", "w"))
    print("FLT statements with mathlib vocabulary: %d" % len(flt), flush=True)


if __name__ == "__main__":
    main()

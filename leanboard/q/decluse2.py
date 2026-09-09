#!/usr/bin/env python3
"""
Q2b (corrected) -- which mathlib DECLARATIONS each board references, and how
rare they are.

Two corrections to the first pass:

  * `decls.json` contains 20 root-level entries that are English words -- `the`,
    `by`, `of`, `in`, `is`, `with`, ... -- produced by the previous phase's
    declaration regex matching a continuation line inside a multi-line mathlib
    statement. Twenty entries out of 25 760, but they occur in every file of
    both boards and dominated the first ranking entirely. Root matching is now
    restricted to names carrying an underscore or an uppercase letter, which
    removes them along with the genuinely ambiguous `log`, `map`, `mem`, `eval`.
  * Qualified matching is exact and is the PRIMARY measure. Root matching is
    reported separately and never mixed into the headline number.

The interesting quantity is not the size of the overlap -- two large Lean
developments share mathlib basics by construction, which is Control A -- but
its RARITY PROFILE. A declaration used by 20 000 FLT files and by NS is
generic. One used by three FLT files and heavily by NS is a bridge candidate.

Also emits, per module, the shared-vocabulary declarations it uses, which is
the input to the blind cross-board pairing.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BOARD = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
BOARDS = {
    "flt": ("/home/user/anthropics/fermats-last-theorem",
            ["Theorems", "Definitions", "P2M"]),
    "ns": ("/home/user/openai/navierstokesandeuler",
           ["NavierStokes", "Euler", "ComparatorChallenges"]),
}


def scan(root, subs, qualified, roots):
    per_module = {}
    cnt = Counter()
    n = 0
    for sub in subs:
        d = Path(root) / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            n += 1
            if n % 20000 == 0:
                print("   %d files" % n, flush=True)
            try:
                toks = set(TOK.findall(p.read_text(errors="ignore")))
            except Exception:
                continue
            hit = (toks & qualified) | (toks & roots)
            if hit:
                per_module[str(p.relative_to(root))] = sorted(hit)
                cnt.update(hit)
    return per_module, cnt, n


def main():
    idx = json.loads((BOARD / "decls.json").read_text())["index"]
    qualified = {k for k in idx if "." in k}
    roots = {k for k in idx if "." not in k
             and ("_" in k or any(c.isupper() for c in k))}
    print("mathlib: %d qualified, %d root kept (of %d root total)"
          % (len(qualified), len(roots),
             sum(1 for k in idx if "." not in k)), flush=True)

    data = {}
    for name, (root, subs) in BOARDS.items():
        print("scanning %s ..." % name, flush=True)
        pm, cnt, n = scan(root, subs, qualified, roots)
        data[name] = {"per_module": pm, "count": cnt, "files": n}
        print("  %s: %d files, %d distinct declarations" % (name, n, len(cnt)),
              flush=True)

    fc, nc = data["flt"]["count"], data["ns"]["count"]
    shared = set(fc) & set(nc)
    nfl = data["flt"]["files"]

    # rarity profile: how many FLT files use each shared declaration
    def bucket(v):
        for lo in (1, 3, 10, 30, 100, 1000, 10000):
            if v <= lo:
                return "<=%d" % lo
        return ">10000"
    prof = Counter(bucket(fc[d]) for d in shared)
    rare = sorted(((d, fc[d], nc[d], idx[d]) for d in shared if fc[d] <= 30),
                  key=lambda x: -x[2])

    out = {
        "label": "COMPUTED_FROM_ARTIFACT",
        "correction": "root matching restricted to names with an underscore or "
                      "an uppercase letter; this removes 20 English-word "
                      "entries in decls.json that the first pass ranked at the "
                      "top of the shared list",
        "flt_files": nfl, "ns_files": data["ns"]["files"],
        "flt_declarations": len(fc), "ns_declarations": len(nc),
        "shared_declarations": len(shared),
        "shared_over_ns": round(len(shared) / len(nc), 4),
        "shared_over_flt": round(len(shared) / len(fc), 4),
        "ns_only": len(set(nc) - set(fc)),
        "rarity_profile_flt_files_using": dict(prof),
        "rare_shared_used_by_ns": [
            {"decl": d, "flt_files": a, "ns_files": b, "module": m}
            for d, a, b, m in rare[:60]],
        "ns_heaviest_shared": sorted(
            ({"decl": d, "ns_files": nc[d], "flt_files": fc[d],
              "module": idx[d]} for d in shared),
            key=lambda r: -r["ns_files"])[:40],
    }
    (OUT / "decluse2.json").write_text(json.dumps(out, indent=1) + "\n")
    json.dump({k: v["per_module"] for k, v in data.items()},
              open(OUT / "per_module_vocab.json", "w"))

    print("\nshared: %d  (%.1f%% of NS's %d, %.1f%% of FLT's %d)"
          % (len(shared), 100 * out["shared_over_ns"], len(nc),
             100 * out["shared_over_flt"], len(fc)))
    print("rarity of the shared set, by number of FLT files using it:")
    for k in ("<=1", "<=3", "<=10", "<=30", "<=100", "<=1000", "<=10000",
              ">10000"):
        if k in prof:
            print("   %-9s %d" % (k, prof[k]))
    print("\nrare in FLT (<=30 files) yet used by NS:")
    for r in out["rare_shared_used_by_ns"][:20]:
        print("   %-46s flt=%-4d ns=%-4d %s"
              % (r["decl"][:46], r["flt_files"], r["ns_files"],
                 r["module"].replace("Mathlib.", "")))


if __name__ == "__main__":
    main()

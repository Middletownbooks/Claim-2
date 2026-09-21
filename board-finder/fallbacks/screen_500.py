#!/usr/bin/env python3
"""Coarse screen over the 499-record corpus for low-impact finite-witness candidates.

WHAT THIS IS. A proxy, not a verdict. The criteria this project actually screens on -- a
finite checkable witness, a writable unknown set, a publishable null -- are semantic, and
nothing here reads meaning. It produces a POOL to be read by a person or a model; the
curated shortlist in SHORTLIST.md is the output that matters.

The one thing it does do honestly is rank by editorial impact, which is a field, and filter
on domain, which is a field.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(HERE, "..", "playability", "ranking_v16.json")

# a single finite object settles it
WITNESS = [r"\bexhibit\b", r"\bconstruct\b", r"\bexists?\b", r"\bfind a\b", r"\bcounterexample\b",
           r"\bsmallest\b", r"\blargest\b", r"\bdetermine whether there\b", r"\bis there a\b",
           r"\bexplicit\b", r"\bat least one\b"]
# no finite object can settle it
TAIL = [r"\bfor all sufficiently large\b", r"\basymptotic", r"\binfinitely many\b",
        r"\balmost all\b", r"\bmeasure zero\b", r"\bconverges?\b", r"\bevery sufficiently\b",
        r"\bas n (?:tends|goes|→)", r"\blimit\b", r"\bdensity\b", r"\bgrowth rate\b"]
# a named finite parameter, i.e. the unknown set can be written down
PARAM = [r"\border \d", r"\bdimension \d", r"\bdegree \d", r"\bsize \d", r"\bn = \d",
         r"\bof order\b", r"\bexactly \d", r"\bat most \d", r"\bwith \d+ vertices\b", r"\b\d{1,4}\b"]

DISCRETE = {"Combinatorics & discrete geometry", "Theoretical computer science",
            "Cryptography, coding, information & optimization"}
SEMI     = {"Number theory & arithmetic geometry", "Algebra, representation & category theory"}


def hits(pats, text):
    t = text.lower()
    return sum(1 for p in pats if re.search(p, t))


def score(r):
    blob = " ".join(str(r.get(k) or "") for k in
                    ("exactTarget", "readerQuestion", "whyItMatters"))
    rc = r.get("resolutionConsequences") or {}
    blob += " " + " ".join(str(v) for v in rc.values())
    w, t, p = hits(WITNESS, blob), hits(TAIL, blob), hits(PARAM, blob)
    dom = r.get("primaryDomainLabel", "")
    dscore = 2 if dom in DISCRETE else (1 if dom in SEMI else 0)
    return {"witness": w, "tail": t, "param": p, "domain": dscore,
            "total": 2 * w - 2 * t + p + 2 * dscore}


def main():
    recs = json.load(open(CORPUS))["records"]
    minrank = int(sys.argv[1]) if len(sys.argv) > 1 else 250
    out = []
    for r in recs:
        if r["releaseRank"] < minrank:
            continue
        s = score(r)
        if s["witness"] == 0 or s["domain"] == 0:
            continue
        out.append((s["total"], r["releaseRank"], r["canonicalTitle"], s,
                    r.get("primaryDomainLabel", ""), (r.get("researchWorkspaces") or []) != []))
    out.sort(reverse=True)
    print(f"{len(recs)} records; {sum(1 for r in recs if r['releaseRank'] >= minrank)} at rank >= "
          f"{minrank}; {len(out)} pass the witness+domain filter\n")
    print(f"{'sc':>3}{'rank':>6}  {'W':>2}{'T':>3}{'P':>3}{'D':>3}  {'collab':>7}  title")
    for tot, rank, title, s, dom, collab in out[:45]:
        print(f"{tot:>3}{rank:>6}  {s['witness']:>2}{s['tail']:>3}{s['param']:>3}{s['domain']:>3}"
              f"  {('yes' if collab else '-'):>7}  {title[:66]}")
    return out


if __name__ == "__main__":
    main()

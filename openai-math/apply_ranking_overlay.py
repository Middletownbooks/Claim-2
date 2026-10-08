#!/usr/bin/env python3
"""Validate ranking_adjudication.json and derive ranking_overlay.json from it.

The ranking (../board-finder/playability/ranking_v16.json, ProofAtlas top-500 v16, edition
2026-09-19) is an imported payload and stays byte-identical. This script joins the hand
adjudication to it and to the playability census (classification.json) and prints the numbers
RESULT_INTAKE.md quotes, so none of them is typed by hand.

HOW THE ADJUDICATION WAS MADE (also in RESULT_INTAKE.md sec 2). Five agents each read 100
records against all 372 families and proposed pairs; every pair with a status consequence was
then read here against the family's abstracts and Lean scope note, with tiers assigned from the
scope note and six labels or tiers corrected. Two recall screens ran afterwards -- lexical
overlap and a reverse pass from every conjecture name in the family texts to the record titles
-- and recovered one SAME_TARGET pair the semantic sweep missed (record 272, Kuznetsov).

FAILS LOUDLY if: a problemId is not in the ranking; a family number is not in families.json; a
FORMAL or FORMAL_WEAKER tier is given to a family that ships no Lean scope note; a relation,
tier or direction is outside its vocabulary; a pair appears twice; a reason is too short to be
a reason.
"""
import json, os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
PLAY = os.path.join(HERE, "..", "board-finder", "playability")

RELATIONS = {"SAME_TARGET", "SUBCASE", "BOUND_OR_NUMBER"}
TIERS = {"FORMAL", "FORMAL_WEAKER", "PAPER_ONLY"}
DIRECTIONS = {"proved", "disproved", "independent", "partial", "bound"}


def main():
    adj = json.load(open(os.path.join(HERE, "ranking_adjudication.json"), encoding="utf-8"))
    fam = json.load(open(os.path.join(HERE, "families.json"), encoding="utf-8"))
    rank = json.load(open(os.path.join(PLAY, "ranking_v16.json"), encoding="utf-8"))
    cls = json.load(open(os.path.join(PLAY, "classification.json"), encoding="utf-8"))
    F = {f["n"]: f for f in fam["families"]}
    R = {r["problemId"]: r for r in rank["records"]}
    C = {r["problemId"]: r for r in cls["records"]}
    assert len(R) == 499 and len(C) == 499, "ranking or census is not the 499-record v16"

    rows = adj["adjudicated"]
    seen = set()
    for d in rows:
        k = (d["problemId"], d["family"])
        assert k not in seen, "duplicate pair %s" % (k,)
        seen.add(k)
        assert d["problemId"] in R, "unknown problemId %s" % d["problemId"]
        assert R[d["problemId"]]["releaseRank"] == d["rank"], "rank mismatch at %s" % (k,)
        assert d["family"] in F, "unknown family %s" % d["family"]
        assert d["relation"] in RELATIONS, "relation %s at %s" % (d["relation"], k)
        assert d["tier"] in TIERS, "tier %s at %s" % (d["tier"], k)
        assert d["direction"] in DIRECTIONS, "direction %s at %s" % (d["direction"], k)
        if d["tier"] != "PAPER_ONLY":
            assert F[d["family"]]["lean"], "%s: formal tier but family %s has no scope note" % (
                k, d["family"])
        assert len(d["reason"]) > 60, "unreasoned row %s" % (k,)
    for d in adj["considered_no_status_effect"]:
        assert d["problemId"] in R and d["family"] in F

    # strongest relation per record: SAME_TARGET > SUBCASE > BOUND_OR_NUMBER
    order = {"SAME_TARGET": 0, "SUBCASE": 1, "BOUND_OR_NUMBER": 2}
    tord = {"FORMAL": 0, "FORMAL_WEAKER": 1, "PAPER_ONLY": 2}
    per = defaultdict(list)
    for d in rows:
        per[d["problemId"]].append(d)
    best = {}
    for pid, ds in per.items():
        ds.sort(key=lambda d: (order[d["relation"]], tord[d["tier"]]))
        best[pid] = ds[0]

    overlay = {
        "_note": "Derived by apply_ranking_overlay.py from ranking_adjudication.json. Do not edit.",
        "source": {"ranking": "proofatlas.open-problem-ranking.top500.v16 (edition 2026-09-19)",
                   "openai_math": fam["source"]["commit"]},
        "records": [{
            "rank": R[pid]["releaseRank"], "problemId": pid,
            "title": R[pid]["canonicalTitle"], "rankingStatus": R[pid]["releaseStatus"],
            "openaiMath": {"strongest": best[pid]["relation"], "tier": best[pid]["tier"],
                           "direction": best[pid]["direction"], "family": best[pid]["family"]},
            "pairs": [{k: d[k] for k in ("family", "relation", "direction", "tier", "reason",
                                         "provenance")} for d in per[pid]],
        } for pid in sorted(per, key=lambda p: R[p]["releaseRank"])],
    }
    with open(os.path.join(HERE, "ranking_overlay.json"), "w", encoding="utf-8") as fh:
        json.dump(overlay, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    # ---- numbers RESULT_INTAKE.md quotes ----
    rel = Counter(b["relation"] for b in best.values())
    print("pairs adjudicated: %d over %d records; considered without status effect: %d" % (
        len(rows), len(per), len(adj["considered_no_status_effect"])))
    print("records by strongest relation:", dict(rel))
    st = [b for b in best.values() if b["relation"] == "SAME_TARGET"]
    print("SAME_TARGET records by tier:", dict(Counter(b["tier"] for b in st)))
    print("SAME_TARGET records by direction:", dict(Counter(b["direction"] for b in st)))
    print("SAME_TARGET records whose ranking status is not 'open':",
          sorted((R[p]["releaseRank"], R[p]["releaseStatus"]) for p, b in best.items()
                 if b["relation"] == "SAME_TARGET" and R[p]["releaseStatus"] != "open"))

    def frac(sel, pred):
        n = sum(1 for p in sel if pred(p))
        return "%d/%d" % (n, len(sel))
    allp = list(R)
    settled = lambda p: p in best and best[p]["relation"] == "SAME_TARGET"
    touched = lambda p: p in best
    print("\nby rank band (SAME_TARGET / any status-bearing pair):")
    for lo, hi in ((1, 100), (101, 200), (201, 300), (301, 400), (401, 500)):
        sel = [p for p in allp if lo <= R[p]["releaseRank"] <= hi]
        print("  %3d-%3d  %-7s  %s" % (lo, hi, frac(sel, settled), frac(sel, touched)))
    print("\nby domain (SAME_TARGET / any):")
    doms = sorted({R[p]["primaryDomain"] for p in allp})
    for dm in doms:
        sel = [p for p in allp if R[p]["primaryDomain"] == dm]
        print("  %-38s %-7s %s" % (dm, frac(sel, settled), frac(sel, touched)))
    print("\nagainst the playability census (classification.json):")
    for lab, pred in (("playable", lambda p: C[p]["playable"]),
                      ("not playable", lambda p: not C[p]["playable"]),
                      ("hasWorkspace", lambda p: C[p]["hasWorkspace"]),
                      ("no workspace", lambda p: not C[p]["hasWorkspace"]),
                      ("quantitative", lambda p: C[p]["quantitative"])):
        sel = [p for p in allp if pred(p)]
        print("  %-14s SAME_TARGET %-7s any %s" % (lab, frac(sel, settled), frac(sel, touched)))
    pl = sorted((R[p]["releaseRank"], R[p]["canonicalTitle"][:60], best[p]["relation"],
                 best[p]["tier"]) for p in best if C[p]["playable"])
    print("  playable records touched:", pl)


if __name__ == "__main__":
    main()

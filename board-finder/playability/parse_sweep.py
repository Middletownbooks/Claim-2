#!/usr/bin/env python3
"""Parse sources/SWEEP_RESPONSE_RAW.md into frontier_sweep.json — derived, not typed.

The raw response is the primary artifact and stays verbatim. This reads it, so every
field in frontier_sweep.json is traceable to a line in a file nobody edited, and a
re-run after a correction to the raw file regenerates the JSON rather than drifting
from it.

Adjudication (which cells the quote actually supports, which verdicts this session
changes and why) lives in REPORT_SWEEP.md and in the ADJUDICATION table below —
kept here so it is applied mechanically rather than remembered.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "sources", "SWEEP_RESPONSE_RAW.md")
OUT = os.path.join(HERE, "frontier_sweep.json")

FIELDS = ("claim", "verdict", "frontier", "wall", "url", "date", "quote",
          "depthOrBreadth", "breadthDetail", "transcribeThis", "note")

# ---------------------------------------------------------------------------
# This session's adjudication. Each entry: does the QUOTE support the cell, and
# does the verdict change anything downstream? Recorded per record so the reasons
# travel with the data.
# ---------------------------------------------------------------------------
ADJUDICATION = {
    "287": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED",
                rerate=("BOUNDED", "NARROWED"),
                why="A counterexample search cannot succeed at l=2, because the "
                    "conjecture is now a THEOREM there. The witness target survives "
                    "only at odd primes, where the inductive condition is incomplete. "
                    "That is a narrowing of the search space by a proof, not a bound "
                    "on a search."),
    "300": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Stays BOUNDED and is now the ONLY one of the four block "
                    "conjectures still open in the shape the record assumed: sporadics "
                    "swept, general case sourced as 'out of reach'."),
    "356": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Stays BOUNDED. The pre-registered low confidence was on the "
                    "MECHANISM (the reduction is a minimal-counterexample argument, not "
                    "a normalizer-compatible bijection) and that flag was right; the "
                    "sweep itself exists. The quote is the strongest GAP evidence in "
                    "the whole sweep and it is on this record."),
    "472": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED",
                rerate=("BOUNDED", "NARROWED"),
                why="Same as 287: a theorem at l=2 closes the witness search there."),
    "22":  dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote contains 4e18. The 2025-26 informal claims are correctly "
                    "excluded from the frontier."),
    "161": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote contains 2^71, superseding the 2^68 this project recalled."),
    "239": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote contains 10^1500. Static since 2012, which is the finding."),
    "307": dict(quoteSupportsCell="PARTLY", tier="SECONDARY-RELAYED", rerate=None,
                why="THE QUOTE IS ABOUT OPPERMANN'S CONJECTURE, NOT LEGENDRE'S. "
                    "Oppermann is strictly stronger (primes in both (n^2-n, n^2) and "
                    "(n^2, n^2+n)), so verifying it to 7.05e13 does verify Legendre to "
                    "that bound — the inference is sound but it IS an inference, and a "
                    "later reader must not think the quoted sentence names Legendre."),
    "348": dict(quoteSupportsCell="PARTLY", tier="SECONDARY-RELAYED", rerate=None,
                why="The quote establishes the SEARCH BOUND (C^z <= 2^100) and reports "
                    "a min/gcd statistic; it does not itself say 'no counterexample was "
                    "found'. The bound is sourced, the null result is adjacent."),
    "488": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Correctly reframed: there is no 2-variable sweep, the 'frontier' is "
                    "a proven-safe analytic range. Note the conjecture is expected FALSE, "
                    "which inverts what a witness means here."),
    "488b": dict(quoteSupportsCell=True, tier="PRIMARY-VERIFIED-LOCALLY",
                 rerate=("HOPELESS", "FEASIBLE"),
                 why="VERIFIED HERE, NOT RELAYED: sieved locally, pi(3159) = 446 and "
                     "p_447 = 3163, so the Engelsma 447-tuple of diameter 3158 gives "
                     "447 > 446 = pi(3159) with margin exactly 1. Under the prime "
                     "k-tuple conjecture that refutes HL2. The record's HOPELESS verdict "
                     "was measured against the WRONG FACTOR of the question — the sweep "
                     "this project ran pushed x, and the deciding factor is combinatorial "
                     "in y. The recalled 'past y ~ 1600' is 1.97x optimistic."),
    "500": dict(quoteSupportsCell=False, tier="SECONDARY-RELAYED", rerate=None,
                why="THE QUOTE DOES NOT CONTAIN THE CLAIMED NUMBER. Quote gives "
                    "n < 982,149,821,766,199,295,999 (2013); the cell claims "
                    "816,212,624,008,487,344,127,999, which is 831x larger and whose "
                    "source the respondent could not pin down. By this prompt's own "
                    "rule the sourced frontier is the QUOTED figure; the larger one is "
                    "recorded as unsourced."),
    "9":   dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote supports q <= 400,000. The 2026 quadratic zero-free-strip "
                    "result at q <= 1e10 is correctly kept separate as a weaker claim."),
    "280": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="The recalled Gardam citation is confirmed, and the recommendation "
                    "SURVIVES BUT CHANGES SHAPE: the implication chain is unit => "
                    "zero-divisor => idempotent, Promislow's group is known to satisfy "
                    "the zero-divisor conjecture, so Gardam's unit counterexample yields "
                    "no idempotent one. The live target is the intermediate zero-divisor "
                    "conjecture, and an AI-algebra lab is already on it."),
    "79":  dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Mechanism correction: 'minor-closed structure cuts the candidates' "
                    "describes LINEAR Hadwiger, which has a finite-check reduction. The "
                    "exact conjecture has none beyond t <= 6."),
    "275": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote contains conductor 500,000 and C = 17."),
    "295": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Frontier moved this year: 38 vertices at girth >= 5, 40 at girth 4, "
                    "on a 14-29x faster algorithm, superseding the 2013 record of 36. "
                    "The wall is quantified (840 CPU-years for the old algorithm)."),
    "355": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED",
                rerate=("BOUNDED", "NOT-A-SEARCH"),
                why="MECHANISM WRONG IN THE RECORD. 3-flow does NOT reduce to snarks "
                    "and has no finite-checkable reduction; it reduces to 5-regular "
                    "graphs and is chased by edge-connectivity theorems (8 -> 6, target "
                    "4). The record grouped it with the 5-flow, and that grouping was "
                    "mine to make and wrong."),
    "335": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote gives the 23-crossing diagram count; frontier is 24 crossings. "
                    "Kronheimer-Mrowka on Khovanov homology narrows what a counterexample "
                    "could look like."),
    "429": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote supports the cubic census to order 1280. The respondent "
                    "explicitly declined an unsourced 'verified to order 100' wiki claim, "
                    "and flagged a near-collision with an unrelated disproved Lovasz "
                    "conjecture — both are the discipline working."),
    "458": dict(quoteSupportsCell="PARTLY", tier="SECONDARY-RELAYED", rerate=None,
                why="The quote's own next sentence is the preprint claiming a full proof, "
                    "so the quote simultaneously sources 'open in its entirety' and an "
                    "unverified refutation of that. Recorded as DISPUTED: a community "
                    "tracker reports a specific gap on page 11 within days of posting."),
    "493": dict(quoteSupportsCell=True, tier="SECONDARY-RELAYED", rerate=None,
                why="Quote supports d = 5. The d = 6 block is upstream of the proof "
                    "technique, which needs the complete type list in hand."),
    "331": dict(quoteSupportsCell=True, tier="PRIMARY-VERIFIED-LOCALLY",
                rerate=("DEMONSTRATED", "WITNESSES-VERIFIED"),
                why="UPGRADED after reading github.com/bbeartheancient/hoa64 directly "
                    "(commit d825201). THE MATRICES ARE VERIFIED HERE, NOT RELAYED: all 13 "
                    "shipped files pass shape (n,n), entries in {-1,+1} and H H^T = nI in "
                    "exact integer arithmetic -- 668, 716, 892, 1132, 1244, 1388, 1436, 1676, "
                    "1772, 1852, 1916, 1948, 1964. The mathematical content of the claim "
                    "therefore stands whatever epoch.ai reports about its own verifier, and "
                    "the sweep's ANNOUNCED-UNVERIFIED was too weak ON THE OBJECTS. THREE "
                    "THINGS STILL DO NOT FOLLOW, the repo's own README being the source for "
                    "the first two. (1) PROVENANCE: it lists these as 'CSV import -- 12 "
                    "Alpoge matrices (668-1964, formerly open) plus Djokovic H.1852', so the "
                    "repo CONSUMES them, 1852 is a 1992 solution rather than new, and the "
                    "method that closed 668-1964 is NOT in the repository. (2) The README "
                    "says gaps below 2000 remain at 1212 and 1940, contradicting 'filled in "
                    "all remaining gaps below 2000' on the repo's own terms. (3) Whether each "
                    "order was previously OPEN is a literature question and stays relayed -- "
                    "arm AV in this project had already separated exactly these two claims. "
                    "So: the witnesses are verified, the history is not. FEASIBILITY.md "
                    "section 6's deep-vs-broad screen now rests on verified objects rather "
                    "than a press report, which strengthens it; its attribution of the work "
                    "to an agent sweep remains relayed. See HOA64_ASSESSMENT.md."),
}


def parse():
    txt = open(RAW, encoding="utf-8").read()
    blocks = re.split(r"^RECORD ", txt, flags=re.M)[1:]
    out = []
    for b in blocks:
        head, *rest = b.split("\n", 1)
        body = rest[0] if rest else ""
        m = re.match(r"(\d+b?)\s*[—-]\s*(.+)", head.strip())
        rank, name = m.group(1), m.group(2).strip()
        rec = {"rank": rank, "name": name}
        # field: value, value may run to the next known field label
        pat = r"^(%s):[ ]?(.*?)(?=\n(?:%s):|\Z)" % ("|".join(FIELDS), "|".join(FIELDS))
        for fm in re.finditer(pat, body, flags=re.M | re.S):
            rec[fm.group(1)] = " ".join(fm.group(2).split())
        adj = ADJUDICATION.get(rank)
        if adj:
            rec["quoteSupportsCell"] = adj["quoteSupportsCell"]
            rec["tier"] = adj["tier"]
            rec["adjudication"] = adj["why"]
            if adj["rerate"]:
                rec["witnessCheckFeasibleWas"], rec["witnessCheckFeasibleNow"] = adj["rerate"]
        out.append(rec)
    return out


if __name__ == "__main__":
    recs = parse()
    missing = [r["rank"] for r in recs if "quote" not in r or "verdict" not in r]
    assert not missing, f"unparsed blocks: {missing}"
    assert len(recs) == 23, len(recs)
    unadj = [r["rank"] for r in recs if "tier" not in r]
    assert not unadj, f"records with no adjudication: {unadj}"
    doc = {
        "label": "FRONTIER_SWEEP_v1",
        "ran": "2026-09-20",
        "instrument": "PROMPT_SWEEP.md Part A",
        "executor": "a Claude chat surface with web search and fetch; no repo access",
        "primary_artifact": "sources/SWEEP_RESPONSE_RAW.md (verbatim, unedited)",
        "provenance_warning":
            "Every url/date/quote here is RELAYED. This session fetched none of them, so "
            "the default tier is SECONDARY-RELAYED and no row may be cited as PRIMARY. "
            "The single exception is 488b, verified locally by sieve.",
        "verdict_counts": {},
        "records": recs,
    }
    from collections import Counter
    doc["verdict_counts"] = dict(Counter(r["verdict"] for r in recs))
    doc["quote_support"] = dict(Counter(str(r["quoteSupportsCell"]) for r in recs))
    json.dump(doc, open(OUT, "w", indent := 1), indent=1, ensure_ascii=False)
    open(OUT, "a").write("\n")
    print(f"{len(recs)} records -> frontier_sweep.json")
    print("verdicts:", doc["verdict_counts"])
    print("quote supports the cell:", doc["quote_support"])
    for r in recs:
        if "witnessCheckFeasibleNow" in r:
            print(f"  re-rate {r['rank']:>4}: {r['witnessCheckFeasibleWas']} -> "
                  f"{r['witnessCheckFeasibleNow']}")

#!/usr/bin/env python3
"""Score the second rater on T3's coverage column against PREREG_COVERAGE.md.

Written and committed BEFORE the rater's answer is transcribed. It reads two
files and nothing else:

  ../t3_coverage.json      -- my classification (rater 1), already committed
  coverage_verdicts.json   -- the second rater's answer, transcribed verbatim

Usage:  python3 score_coverage.py            # scores if the verdicts file exists
        python3 score_coverage.py --selftest # runs the harness on synthetic
                                             # answers, to show the failure
                                             # conditions actually fire
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
COV = os.path.join(HERE, os.pardir, "t3_coverage.json")
VERD = os.path.join(HERE, "coverage_verdicts.json")

# board number in the RATER's ordering -> item id in t3_coverage.json
ORDER = {1: "02-cap-set", 2: "04-kadison-singer", 3: "08-spencer",
         4: "09-vinogradov", 5: "13-pcp", 6: "K1-to-K3"}

# PREREG B-2/B-3: the quantity, not the wording. Each entry is a list of
# acceptable spellings, matched as WORD-BOUNDED regexes (case-folded), not bare
# substrings: a loose " t" would match the word "the" and pass B-2 on any text
# at all. Caught and tightened by the harness self-test before any answer was
# transcribed, which is the only time such a fix is free.
QUANTITY = {
    "04-kadison-singer": [r"delta", r"\bnorm", r"\|\|v", r"‖v"],
    "08-spencer":        [r"discrepanc", r"\bt\b", r"bound being certified"],
    "K1-to-K3":          [r"\bside", r"\bcube", r"\bradius", r"\bscale\b.{0,12}cube"],
}


def rater1():
    cov = json.load(open(COV))
    return {it["id"]: bool(it["applies"]) for it in cov["items"]}, cov


def load_verdicts():
    v = json.load(open(VERD))
    out = {}
    for row in v["boards"]:
        item = ORDER[int(row["board"])]
        parses = row["verdict"].strip().upper()
        assert parses in ("PARSES", "NOT WELL-POSED"), row["verdict"]
        out[item] = {"parses": parses == "PARSES",
                     "scale": (row.get("scale_parameter") or "").lower(),
                     "reason": (row.get("reason") or "").lower(),
                     "confidence": (row.get("confidence") or "").lower()}
    assert len(out) == 6, "six boards or it is not this test"
    return out, v


def score(r1, r2):
    lines, verdicts = [], {}

    agree = [k for k in r1 if r1[k] == r2[k]["parses"]]
    disagree = [k for k in r1 if r1[k] != r2[k]["parses"]]
    lines.append(f"agreement: {len(agree)}/6")
    if disagree:
        lines.append("  disagreements: " + ", ".join(sorted(disagree)))

    # B-1: declines on exactly the three rounds-x-cost boards
    declined_pred = {"02-cap-set", "09-vinogradov", "13-pcp"}
    declined_obs = {k for k in r2 if not r2[k]["parses"]}
    verdicts["B-1"] = (declined_obs == declined_pred,
                       f"declined = {sorted(declined_obs)}")

    # B-2 / B-3: the named scale parameter is the predicted quantity
    for item in ("04-kadison-singer", "08-spencer", "K1-to-K3"):
        tag = "B-3" if item == "K1-to-K3" else "B-2:" + item.split("-")[0]
        if not r2[item]["parses"]:
            verdicts[tag] = (False, f"{item}: rater called it NOT WELL-POSED")
            continue
        hit = [q for q in QUANTITY[item]
               if re.search(q, r2[item]["scale"], re.I)]
        verdicts[tag] = (bool(hit),
                         f"{item}: scale={r2[item]['scale']!r} matched={hit}")

    # B-4: if exactly one item flips, was it 09-vinogradov?
    if len(disagree) == 1:
        verdicts["B-4"] = (disagree[0] == "09-vinogradov",
                           f"single flip was {disagree[0]}")
    else:
        verdicts["B-4"] = (None, f"not applicable: {len(disagree)} flips")

    # B-5: declines cite the absence of a scale, not unfamiliarity
    bad = [k for k in declined_obs
           if not any(w in r2[k]["reason"] for w in
                      ("scale", "threshold", "parameter", "round", "iterat",
                       "per-step", "per step", "no c", "increment", "recursi",
                       "repetition", "blow-up", "blow up"))]
    verdicts["B-5"] = (not bad, f"declines lacking a structural reason: {bad}")

    lines.append("")
    for k in sorted(verdicts):
        ok, note = verdicts[k]
        mark = "n/a " if ok is None else ("PASS" if ok else "FAIL")
        lines.append(f"  {k}: {mark}  {note}")

    # failure conditions, verbatim from the prereg
    lines.append("")
    n = len(agree)
    if n <= 4:
        lines.append("FAILURE CONDITION MET: agreement <= 4/6. The coverage column "
                     "is a judgement, not a measurement. t3_coverage.json's '3 of 6' "
                     "must be reported as one rater's reading.")
    if declined_obs and declined_obs != declined_pred and len(declined_obs) == 3:
        lines.append("WORSE FAILURE CONDITION MET: a DIFFERENT three decline. The "
                     "threshold-vs-per-round dichotomy is mine, not the boards'.")
    if n == 6:
        lines.append("6/6: recorded as CONSISTENCY, not truth (prereg says so in "
                     "advance). Two raters with the same training on six famous "
                     "boards can agree for reasons unrelated to the boards.")
    if 4 < n < 6:
        lines.append(f"{n}/6: the column survives with a named exception. The "
                     "exception goes in t3_coverage.json, not in a footnote.")
    lines.append("")
    lines.append("This arm says nothing about whether T3 is a useful screen. "
                 "That is arm 3.")
    return "\n".join(lines)


def selftest():
    r1 = {"02-cap-set": False, "04-kadison-singer": True, "08-spencer": True,
          "09-vinogradov": False, "13-pcp": False, "K1-to-K3": True}

    def mk(parses, scales=None, reasons=None):
        d = {}
        for k, p in parses.items():
            d[k] = {"parses": p,
                    "scale": (scales or {}).get(k, ""),
                    "reason": (reasons or {}).get(k, ""),
                    "confidence": "high"}
        return d

    print("### synthetic A: full agreement, right quantities")
    print(score(r1, mk(dict(r1),
        {"04-kadison-singer": "delta, the bound on ||v_i||^2",
         "08-spencer": "the discrepancy t being certified",
         "K1-to-K3": "the side C of the target cube"},
        {"02-cap-set": "no scale; the loss is per iteration",
         "09-vinogradov": "log k rounds, each with a fixed loss",
         "13-pcp": "size blow-up over repetitions"})))

    print("\n### synthetic B: a different three decline")
    flip = {"02-cap-set": True, "04-kadison-singer": False, "08-spencer": True,
            "09-vinogradov": False, "13-pcp": False, "K1-to-K3": True}
    print(score(r1, mk(flip, {"02-cap-set": "the density delta",
                              "08-spencer": "the discrepancy t",
                              "K1-to-K3": "the side C"},
                       {"04-kadison-singer": "unfamiliar to me",
                        "09-vinogradov": "rounds", "13-pcp": "rounds"})))

    print("\n### synthetic B2: 08 answered with the WRONG quantity")
    wrong = mk(dict(r1),
               {"04-kadison-singer": "delta", "08-spencer": "n, the number of sets",
                "K1-to-K3": "the side C"},
               {"02-cap-set": "per-iteration loss", "09-vinogradov": "rounds",
                "13-pcp": "rounds"})
    print(score(r1, wrong))

    print("\n### synthetic C: single flip on 09")
    one = dict(r1); one["09-vinogradov"] = True
    print(score(r1, mk(one, {"04-kadison-singer": "delta bound on ||v||^2",
                             "08-spencer": "discrepancy t",
                             "09-vinogradov": "k, the degree",
                             "K1-to-K3": "the cube side C"},
                       {"02-cap-set": "increment per round",
                        "13-pcp": "blow-up per repetition"})))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif not os.path.exists(VERD):
        print("coverage_verdicts.json not present yet -- the rater has not "
              "returned, or the answer has not been transcribed.")
        print("Harness is committed now so the scoring rule cannot move later.")
        print("Run with --selftest to see the failure conditions fire.")
    else:
        r1, _ = rater1()
        r2, _ = load_verdicts()
        print(score(r1, r2))

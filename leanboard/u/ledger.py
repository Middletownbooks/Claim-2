#!/usr/bin/env python3
"""
U1 -- score this programme's own forecasting record.

Phase U asks whether a research team can learn a transferable policy for
choosing what to investigate. The only real research team whose complete
trajectory is available here is this one: Phases 0-T left pre-registrations
with declared predictions, reports with scored outcomes, and phase-level
recommendations that the next phase either followed or did not.

Every entry below is transcribed from the committed record, not from memory.
Each prediction is classified as POSITIVE (an effect exists / X beats Y) or
NEGATIVE (a null / X is unreachable), because the interesting question is
whether the team's forecasting skill was symmetric.
"""
import json
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent

PREDICTIONS = [
    # phase, id, statement, polarity, outcome, source file
    ("P", "P-1", "|R_B(5)| > |R_A(5)|", "POSITIVE", "FAILED", "termform2/REPORT_P.md"),
    ("P", "P-2", "B reaches more targets than A", "POSITIVE", "FAILED", "termform2/REPORT_P.md"),
    ("P", "P-3", "B > D (naming beats re-expansion)", "POSITIVE", "FAILED", "termform2/REPORT_P.md"),
    ("P", "P-4", "B > C (promoted beats random)", "POSITIVE", "HELD", "termform2/REPORT_P.md"),
    ("P", "P-5", "B > E at matched expansions", "POSITIVE", "FAILED", "termform2/REPORT_P.md"),
    ("P", "P-6", "no condition reaches is_squarefree", "NEGATIVE", "FAILED", "termform2/REPORT_P.md"),
    ("P", "P-7", "both A and B reach v_2", "POSITIVE", "FAILED", "termform2/REPORT_P.md"),
    ("P", "P-8", "no rung-3 discovery (author's prior)", "NEGATIVE", "HELD", "termform2/REPORT_P.md"),
    # Phase P per-target predictions
    ("P", "T4", "gpf unreachable in all conditions", "NEGATIVE", "HELD", "termform2/PREREG.md"),
    ("P", "T5", "omega unreachable", "NEGATIVE", "HELD", "termform2/PREREG.md"),
    ("P", "T6", "Omega unreachable", "NEGATIVE", "HELD", "termform2/PREREG.md"),
    ("P", "T7", "is_squarefree unreachable", "NEGATIVE", "FAILED", "termform2/PREREG.md"),
    ("P", "T8", "rad unreachable", "NEGATIVE", "HELD", "termform2/PREREG.md"),
    ("P", "T10", "sigma unreachable", "NEGATIVE", "HELD", "termform2/PREREG.md"),
    ("P", "T12", "phi unreachable", "NEGATIVE", "HELD", "termform2/PREREG.md"),
    ("P", "T1/T2/T3", "A cannot reach is_prime/is_square/n_div_spf, B can",
     "POSITIVE", "FAILED", "termform2/PREREG.md"),
    ("P", "T13", "v_spf reachable in B only", "POSITIVE", "FAILED", "termform2/PREREG.md"),
    # Phase R
    ("R", "R-prior", "QPR is not a full board", "NEGATIVE", "HELD", "REPORT_R"),
    # Phase S
    ("S", "S-pinsker", "Pinsker intervention gives no gain", "NEGATIVE", "HELD",
     "s/pinsker_prereg.md"),
    # Phase T
    ("T", "T-math", "MATH skeletons do not transport", "NEGATIVE", "HELD", "t/PREREG.md"),
    ("T", "T-eng", "ENG skeletons give a small positive", "POSITIVE", "FAILED", "t/PREREG.md"),
]

# Phase-level forward recommendations: did the next phase follow them, and did
# the recommendation's POSITIVE content survive?
RECOMMENDATIONS = [
    ("Q", "upstreamability: board -> mathlib -> board is the transport channel",
     "R and S", "FOLLOWED",
     "REFUTED as transport -- R judged it engineering, S found four "
     "upstreamable lemmas and zero transport"),
    ("R", "interface-mediated transport: shared mathlib interfaces predict transport",
     "S", "FOLLOWED",
     "FALSIFIED -- I|V+controls = -0.44, p = 0.0008"),
    ("S", "architecture channel: proof-architecture similarity is the live signal",
     "T", "FOLLOWED",
     "FALSIFIED -- source-specific benefit null at L2/L3/MATH/ENG; the Phase S "
     "metric was 54% `have`"),
]


def main():
    pol = Counter()
    for _, _, _, p, o, _ in PREDICTIONS:
        pol[(p, o)] += 1
    npos = pol[("POSITIVE", "HELD")] + pol[("POSITIVE", "FAILED")]
    nneg = pol[("NEGATIVE", "HELD")] + pol[("NEGATIVE", "FAILED")]

    print("=== PRE-REGISTERED PREDICTIONS, by polarity ===")
    print("  POSITIVE (an effect exists):  %2d held / %2d  = %.0f%%"
          % (pol[("POSITIVE", "HELD")], npos,
             100 * pol[("POSITIVE", "HELD")] / npos))
    print("  NEGATIVE (a null / unreachable): %2d held / %2d  = %.0f%%"
          % (pol[("NEGATIVE", "HELD")], nneg,
             100 * pol[("NEGATIVE", "HELD")] / nneg))
    print()
    for ph, i, s, p, o, src in PREDICTIONS:
        mark = "OK " if o == "HELD" else "   "
        print("  %s %-10s %-9s %-6s %s%s" % (ph, i, p, o, mark, s[:58]))

    print("\n=== PHASE-LEVEL RECOMMENDATIONS (the meta-moves) ===")
    for src, rec, by, followed, outcome in RECOMMENDATIONS:
        print("  %s -> %s  [%s]" % (src, by, followed))
        print("      recommended: %s" % rec)
        print("      outcome:     %s" % outcome)
    print("\n  follow-through: %d/%d    positive content surviving: 0/%d"
          % (len(RECOMMENDATIONS), len(RECOMMENDATIONS), len(RECOMMENDATIONS)))

    out = {
        "label": "COMPUTED_FROM_ARTIFACT",
        "note": "transcribed from committed pre-registrations and reports",
        "predictions": [
            {"phase": a, "id": b, "statement": c, "polarity": d,
             "outcome": e, "source": f} for a, b, c, d, e, f in PREDICTIONS],
        "summary": {
            "positive_held": pol[("POSITIVE", "HELD")], "positive_total": npos,
            "positive_rate": round(pol[("POSITIVE", "HELD")] / npos, 4),
            "negative_held": pol[("NEGATIVE", "HELD")], "negative_total": nneg,
            "negative_rate": round(pol[("NEGATIVE", "HELD")] / nneg, 4)},
        "recommendations": [
            {"from": a, "recommendation": b, "tested_by": c,
             "followed": d, "outcome": e} for a, b, c, d, e in RECOMMENDATIONS],
        "recommendation_follow_through": "3/3",
        "recommendation_positive_survival": "0/3",
    }
    (OUT / "forecast_ledger.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()

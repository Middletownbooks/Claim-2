#!/usr/bin/env python3
"""
U1 (CORRECTED) -- the complete forecasting record.

The first ledger (u/ledger.py) was wrong in four ways, found by an independent
Sonnet subagent audit and then verified against the sources:

  1. P-6 and T7 are THE SAME prediction. PREREG.md:183 reads verbatim
     "**P-6**: T7 (squarefree) is reached by no condition." I counted it twice,
     while NOT doing the same for P-7/T9 -- an inconsistent rule applied to
     otherwise identical cases.
  2. "R-prior" was never pre-registered. There is no PREREG file anywhere under
     leanboard/r/. I scored REPORT_R's own conclusion against itself, which
     cannot fail by construction.
  3. The merged T1/T2/T3 entry silently included T3, which REPORT_P.md:326
     struck as invalid ("T3 is struck").
  4. THE SEVERE ONE: the ledger claimed to transcribe "Phases 0-T" and drew
     from four documents. SIX pre-registrations with 29 further scored
     predictions were omitted -- crossobject (K), crossobject2 (L), termform
     (M), flt/PREREG_blind_regions (I), flt/PREREG_retrospective (J), and
     audit/PHASE15. Those are the phases in which the predictions were largely
     RIGHT, so the omission was not neutral: it selected for my own failures
     and produced the headline.

Polarity convention, unchanged: POSITIVE = an effect/specific outcome exists;
NEGATIVE = a null. For POSITIVE, HELD means the effect existed; for NEGATIVE,
FAILED means it existed. Entries whose polarity is genuinely arguable are
flagged and a sensitivity check is run over them.
"""
import json
from math import comb
from pathlib import Path

OUT = Path(__file__).resolve().parent

# (phase, id, polarity, outcome, arguable_polarity, source)
P = [
    # --- Phase P (termform2), as before minus the T7 duplicate ---
    ("P", "P-1", "POSITIVE", "FAILED", 0, "termform2/REPORT_P.md"),
    ("P", "P-2", "POSITIVE", "FAILED", 0, "termform2/REPORT_P.md"),
    ("P", "P-3", "POSITIVE", "FAILED", 0, "termform2/REPORT_P.md"),
    ("P", "P-4", "POSITIVE", "HELD", 0, "termform2/REPORT_P.md"),
    ("P", "P-5", "POSITIVE", "FAILED", 0, "termform2/REPORT_P.md"),
    ("P", "P-6=T7", "NEGATIVE", "FAILED", 0, "termform2/REPORT_P.md"),
    ("P", "P-7=T9", "POSITIVE", "FAILED", 0, "termform2/REPORT_P.md"),
    ("P", "P-8", "NEGATIVE", "HELD", 0, "termform2/REPORT_P.md"),
    ("P", "T4", "NEGATIVE", "HELD", 0, "termform2/PREREG.md"),
    ("P", "T5", "NEGATIVE", "HELD", 0, "termform2/PREREG.md"),
    ("P", "T6", "NEGATIVE", "HELD", 0, "termform2/PREREG.md"),
    ("P", "T8", "NEGATIVE", "HELD", 0, "termform2/PREREG.md"),
    ("P", "T10", "NEGATIVE", "HELD", 0, "termform2/PREREG.md"),
    ("P", "T12", "NEGATIVE", "HELD", 0, "termform2/PREREG.md"),
    ("P", "T1/T2 (T3 struck)", "POSITIVE", "FAILED", 0, "termform2/PREREG.md"),
    ("P", "T13", "POSITIVE", "FAILED", 0, "termform2/PREREG.md"),
    ("S", "S-pinsker", "NEGATIVE", "HELD", 0, "s/pinsker_prereg.md"),
    ("T", "T-math", "NEGATIVE", "HELD", 0, "t/PREREG.md"),
    ("T", "T-eng", "POSITIVE", "FAILED", 0, "t/PREREG.md"),
    # --- OMITTED IN THE FIRST LEDGER ---
    ("I", "P1 communities not a blob", "POSITIVE", "HELD", 0, "REPORT_I"),
    ("I", "P2 largest = modular curves", "POSITIVE", "HELD", 0, "REPORT_I"),
    ("I", "P3 bottleneck ratio < 0.25", "POSITIVE", "FAILED", 0, "REPORT_I"),
    ("I", "P5 NMI above chance", "POSITIVE", "HELD", 0, "REPORT_I"),
    ("J", "Q1 >20% invisible early", "POSITIVE", "FAILED", 0, "REPORT_J"),
    ("J", "Q2 AUC >= 0.80", "POSITIVE", "HELD", 0, "REPORT_J"),
    ("J", "Q3 no feature beats baseline", "NEGATIVE", "HELD", 0, "REPORT_J"),
    ("K", "P1 search selects lcm", "POSITIVE", "FAILED", 0, "REPORT_K"),
    ("K", "P2 >=90% composable exact", "POSITIVE", "FAILED", 0, "REPORT_K"),
    ("K", "P3 base case breaks somewhere", "POSITIVE", "FAILED", 1, "REPORT_K"),
    ("K", "P4 end-to-end > 0.93", "POSITIVE", "HELD", 0, "REPORT_K"),
    ("K", "P5 composable beats non by 5pp", "POSITIVE", "FAILED", 0, "REPORT_K"),
    ("L", "P1 max/lcm tie", "POSITIVE", "HELD", 0, "REPORT_L"),
    ("L", "P2 returns UNDERDETERMINED", "POSITIVE", "HELD", 1, "REPORT_L"),
    ("L", "P3 resolves to max in 1 probe", "POSITIVE", "HELD", 0, "REPORT_L"),
    ("L", "P4 base case fails >=4 of 6", "POSITIVE", "HELD", 1, "REPORT_L"),
    ("L", "P5 composable >= 90%", "POSITIVE", "HELD", 0, "REPORT_L"),
    ("L", "P6 end-to-end < 0.95", "POSITIVE", "HELD", 1, "REPORT_L"),
    ("M", "P1 zero-error term found", "POSITIVE", "HELD", 0, "REPORT_M"),
    ("M", "P2 several terms tie", "POSITIVE", "HELD", 0, "REPORT_M"),
    ("M", "P3 minimal nu term generalises", "POSITIVE", "HELD", 0, "REPORT_M"),
    ("M", "P4 lambda needs decision list", "POSITIVE", "HELD", 0, "REPORT_M"),
    ("15", "1 cycles reaches 0 everywhere", "POSITIVE", "HELD", 0, "audit/REPORT.md"),
    ("15", "2 fitted period = lambda(m)", "POSITIVE", "HELD", 0, "audit/REPORT.md"),
    ("15", "3 all arithmetic rules stay REFUTED", "NEGATIVE", "FAILED", 0, "audit/REPORT.md"),
]
PARTIAL = [("I", "P4"), ("J", "Q4"), ("M", "P5"), ("15", "4"),
           ("P", "P5-disagreement (M)")]


def fisher(a, b, c, d):
    n = a + b + c + d

    def p(x):
        y = a + b - x
        z = a + c - x
        w = n - x - y - z
        if min(x, y, z, w) < 0:
            return 0.0
        return comb(a + b, x) * comb(c + d, z) / comb(n, a + c)
    obs = p(a)
    return sum(p(i) for i in range(0, min(a + b, a + c) + 1)
               if p(i) <= obs + 1e-12)


def table(rows):
    a = sum(1 for r in rows if r[2] == "POSITIVE" and r[3] == "HELD")
    b = sum(1 for r in rows if r[2] == "POSITIVE" and r[3] == "FAILED")
    c = sum(1 for r in rows if r[2] == "NEGATIVE" and r[3] == "FAILED")
    d = sum(1 for r in rows if r[2] == "NEGATIVE" and r[3] == "HELD")
    return a, b, c, d


def report(name, rows):
    a, b, c, d = table(rows)
    n = a + b + c + d
    print("%-34s GO/eff=%2d GO/no=%2d NOGO/eff=%2d NOGO/no=%2d  n=%d"
          % (name, a, b, c, d, n))
    print("%-34s P(eff|GO)=%.3f  P(eff|NOGO)=%.3f  base=%.3f  Fisher p=%.5f"
          % ("", a / (a + b), c / (c + d), (a + c) / n, fisher(a, b, c, d)))
    return {"a": a, "b": b, "c": c, "d": d, "n": n,
            "p_eff_given_GO": round(a / (a + b), 4),
            "p_eff_given_NOGO": round(c / (c + d), 4),
            "base_rate": round((a + c) / n, 4),
            "fisher_p": round(fisher(a, b, c, d), 6)}


def main():
    print("=== CORRECTED, complete record (%d clean predictions, %d partials "
          "excluded) ===" % (len(P), len(PARTIAL)))
    full = report("ALL", P)
    print()
    old = [r for r in P if r[0] in ("P", "S", "T")]
    print("=== the subset the first ledger sampled ===")
    sub = report("first-ledger subset", old)
    print()
    print("=== sensitivity: drop the 4 arguable-polarity entries ===")
    sens = report("arguable dropped", [r for r in P if not r[4]])
    print()
    pos = sum(1 for r in P if r[2] == "POSITIVE")
    posh = sum(1 for r in P if r[2] == "POSITIVE" and r[3] == "HELD")
    neg = sum(1 for r in P if r[2] == "NEGATIVE")
    negh = sum(1 for r in P if r[2] == "NEGATIVE" and r[3] == "HELD")
    print("POSITIVE predictions held %2d/%2d = %.0f%%   (first ledger: 1/9 = 11%%)"
          % (posh, pos, 100 * posh / pos))
    print("NEGATIVE predictions held %2d/%2d = %.0f%%   (first ledger: 10/12 = 83%%)"
          % (negh, neg, 100 * negh / neg))
    json.dump({"label": "COMPUTED_FROM_ARTIFACT",
               "supersedes": "u/forecast_ledger.json",
               "predictions": [{"phase": a, "id": b, "polarity": c,
                                "outcome": d, "arguable": bool(e),
                                "source": f} for a, b, c, d, e, f in P],
               "partials_excluded": [list(x) for x in PARTIAL],
               "full": full, "first_ledger_subset": sub,
               "sensitivity_arguable_dropped": sens},
              open(OUT / "forecast_ledger_corrected.json", "w"), indent=1)


if __name__ == "__main__":
    main()

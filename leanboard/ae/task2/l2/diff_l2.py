#!/usr/bin/env python3
"""L2 diff: Fable's P1 sec.1.2 encoding vs five independent blind encodings.

Every mark in MARKS and every mechanism in LEAKS is a judgement by a SINGLE,
NON-BLIND rater (the orchestrating agent, who knows which column is which).
The pre-registered protocol called for a third rater seeing the two encodings
in randomised order without provenance. That rater was not run. This script
therefore reports a diff, not the pre-registered measurement; see RESULT_L2.md
sec. "Protocol deviations".

Mechanism vocabulary is the six-value field from SCHEMA_before.md. The blind
encoders tagged their own leaks with it. Fable's leaks are prose; the tags
assigned to them here are the rater's coding of that prose.
"""
import itertools, random

CASES = [(1, "sensitivity"), (2, "cap set"), (5, "Kakeya"), (8, "Spencer"),
         (9, "Vinogradov")]

# Slot marks: AGREE / PARTIAL / DISAGREE / NC (not comparable: slot empty in P1)
MARKS = {
    1: {"state": "AGREE",    "move": "AGREE",    "invariant": "PARTIAL",
        "composition": "NC", "terminal": "AGREE",   "bound": "AGREE"},
    2: {"state": "PARTIAL",  "move": "AGREE",    "invariant": "PARTIAL",
        "composition": "PARTIAL", "terminal": "AGREE", "bound": "AGREE"},
    5: {"state": "PARTIAL",  "move": "PARTIAL",  "invariant": "DISAGREE",
        "composition": "NC", "terminal": "NC",      "bound": "DISAGREE"},
    8: {"state": "PARTIAL",  "move": "DISAGREE", "invariant": "PARTIAL",
        "composition": "AGREE", "terminal": "NC",   "bound": "AGREE"},
    9: {"state": "PARTIAL",  "move": "AGREE",    "invariant": "AGREE",
        "composition": "NC", "terminal": "NC",      "bound": "VOID"},
}
SLOTS = ["state", "move", "invariant", "composition", "terminal", "bound"]

# Leading leak mechanism, and the full mechanism SET, per encoder.
# P1 tags are the rater's coding of Fable's prose; blind tags are the encoders' own.
LEAKS = {
    1: {"p1_lead": "MULTIPLICATIVE INVARIANT",
        "p1_set": ["TERMINAL CERT TOO WEAK", "MULTIPLICATIVE INVARIANT"],
        "bl_lead": "ITERATION COUNT",
        "bl_set": ["ITERATION COUNT", "MULTIPLICATIVE INVARIANT",
                   "TERMINAL CERT TOO WEAK"]},
    2: {"p1_lead": "MULTIPLICATIVE INVARIANT",
        "p1_set": ["ITERATION COUNT", "MULTIPLICATIVE INVARIANT"],
        "bl_lead": "TERMINAL CERT TOO WEAK",
        "bl_set": ["TERMINAL CERT TOO WEAK", "FEASIBILITY THEOREM",
                   "UNION BOUND", "MULTIPLICATIVE INVARIANT"]},
    5: {"p1_lead": "UNION BOUND",
        "p1_set": ["UNION BOUND"],
        "bl_lead": "FEASIBILITY THEOREM",
        "bl_set": ["FEASIBILITY THEOREM", "ITERATION COUNT", "UNION BOUND"]},
    8: {"p1_lead": "UNION BOUND",
        "p1_set": ["UNION BOUND"],
        "bl_lead": "UNION BOUND",
        "bl_set": ["UNION BOUND"]},
    9: {"p1_lead": "ITERATION COUNT",
        "p1_set": ["ITERATION COUNT"],
        "bl_lead": "ITERATION COUNT",
        "bl_set": ["ITERATION COUNT", "TERMINAL CERT TOO WEAK"]},
}

def kappa(a, b):
    """Cohen's kappa between two label sequences."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    cats = set(a) | set(b)
    pe = sum((a.count(c) / n) * (b.count(c) / n) for c in cats)
    return po, pe, (po - pe) / (1 - pe) if pe < 1 else float("nan")

def main():
    print("=" * 78)
    print("L2 DIFF  —  Fable P1 sec.1.2  vs  five independent blind encodings")
    print("single non-blind rater; see RESULT_L2.md 'Protocol deviations'")
    print("=" * 78)

    print("\n--- slot marks " + "-" * 62)
    hdr = f"{'case':<14}" + "".join(f"{s[:11]:<13}" for s in SLOTS)
    print(hdr)
    for n, name in CASES:
        row = f"{str(n)+' '+name:<14}"
        row += "".join(f"{MARKS[n][s]:<13}" for s in SLOTS)
        print(row)

    print("\n--- per-slot tally (NC/VOID excluded from the base) " + "-" * 25)
    print(f"{'slot':<14}{'AGREE':<8}{'PARTIAL':<9}{'DISAGREE':<10}{'n':<4}{'agree rate'}")
    for s in SLOTS:
        v = [MARKS[n][s] for n, _ in CASES]
        a, p, d = v.count("AGREE"), v.count("PARTIAL"), v.count("DISAGREE")
        n_eff = a + p + d
        rate = f"{a/n_eff:.2f}" if n_eff else "n/a"
        print(f"{s:<14}{a:<8}{p:<9}{d:<10}{n_eff:<4}{rate}")

    print("\n--- leak table " + "-" * 62)
    print(f"{'case':<14}{'P1 leading':<27}{'blind leading':<27}{'match'}")
    lead_match = 0
    for n, name in CASES:
        L = LEAKS[n]
        m = L["p1_lead"] == L["bl_lead"]
        lead_match += m
        print(f"{str(n)+' '+name:<14}{L['p1_lead']:<27}{L['bl_lead']:<27}"
              f"{'YES' if m else 'no'}")
    print(f"\nleading-mechanism agreement : {lead_match} of {len(CASES)}")

    rec = sum(1 for n, _ in CASES
              if set(LEAKS[n]["p1_set"]) <= set(LEAKS[n]["bl_set"]))
    tot_p1 = sum(len(LEAKS[n]["p1_set"]) for n, _ in CASES)
    tot_in = sum(len(set(LEAKS[n]["p1_set"]) & set(LEAKS[n]["bl_set"]))
                 for n, _ in CASES)
    print(f"P1 mechanisms also named by the blind encoder (anywhere in its "
          f"table) : {tot_in} of {tot_p1}")
    print(f"cases where P1's whole mechanism set is a subset of the blind "
          f"set        : {rec} of {len(CASES)}")

    a = [LEAKS[n]["p1_lead"] for n, _ in CASES]
    b = [LEAKS[n]["bl_lead"] for n, _ in CASES]
    po, pe, k = kappa(a, b)
    print(f"\ninter-ENCODER kappa on the leading mechanism "
          f"(n=5, 6 categories):")
    print(f"  observed agreement p_o = {po:.4f}")
    print(f"  chance agreement  p_e = {pe:.4f}")
    print(f"  kappa                 = {k:.4f}")

    random.seed(20260918)
    B = 20000
    boots = []
    for _ in range(B):
        idx = [random.randrange(len(a)) for _ in a]
        try:
            _, _, kb = kappa([a[i] for i in idx], [b[i] for i in idx])
        except ZeroDivisionError:
            continue
        if kb == kb:
            boots.append(kb)
    boots.sort()
    lo = boots[int(0.025 * len(boots))]
    hi = boots[int(0.975 * len(boots)) - 1]
    print(f"  case-resampled 95% interval = [{lo:.3f}, {hi:.3f}]  "
          f"({len(boots)}/{B} replicates defined)")
    print("  n=5: this interval spans essentially the whole admissible range "
          "and\n  should be read as 'unmeasured', not as a bound.")

    print("\n--- bound field " + "-" * 61)
    for n, name in CASES:
        print(f"{str(n)+' '+name:<14}{MARKS[n]['bound']}")

    print("\n--- Kakeya two-regime check (DERIVED HERE) " + "-" * 34)
    print("  (n+2)/2 > 4n/7  <=>  7n+14 > 8n  <=>  n < 14")
    for n in (3, 13, 14, 15, 30):
        w, r = (n + 2) / 2, 4 * n / 7
        better = "Wolff" if w > r else ("equal" if w == r else "4n/7")
        print(f"  n={n:<3} (n+2)/2={w:<7.3f} 4n/7={r:<7.3f} better: {better}")

if __name__ == "__main__":
    main()

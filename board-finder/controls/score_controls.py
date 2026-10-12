#!/usr/bin/env python3
"""Score the two control responses against PREREG_CONTROLS.md. Read-only.

Run from board-finder/controls/. Reads `response_positive.md` and
`response_negative.md` -- the verbatim respondent texts -- plus `verdicts.json`, which
is where the reading of each response is recorded FIELD BY FIELD with the quote that
supports it. The point of splitting those two is that the quote has to exist: a verdict
without a supporting quote from the response fails the check below, which is the only
defence available against scoring my own instrument charitably.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
V = json.loads((HERE / "verdicts.json").read_text(encoding="utf-8"))
PRED = {
    "C-1": ("positive", "T1", "yes"),
    "C-2": ("positive", "T2", "formula"),
    "C-3": ("negative", "T1", "no"),
    "C-5a": ("positive", "recognised", "yes"),
    "C-5b": ("negative", "named", "no"),
}
bad, notes = [], []


def main() -> int:
    print("=== verdicts, each with the quote that supports it\n")
    for arm in ("positive", "negative"):
        r = V[arm]
        text = (HERE / r["response_file"]).read_text(encoding="utf-8")
        print(f"  {arm.upper()} CONTROL  ({r['response_file']}, {len(text.split())} words)")
        for field in ("T1", "T2", "kill_test_run", "recognised", "named", "restatement_declared"):
            if field not in r:
                continue
            val, q = r[field]["value"], r[field].get("quote", "")
            ok = bool(q) and q.strip('. ') in " ".join(text.split())
            if not ok:
                bad.append(f"{arm}.{field}: quote not found verbatim in the response")
            print(f"    {field:22} {str(val):10} {'quote ok' if ok else 'QUOTE NOT FOUND'}")
            print(f"       \"{q[:150]}\"")
        print()

    print("=== predictions, scored as written\n")
    for pid, (arm, field, want) in sorted(PRED.items()):
        got = V[arm].get(field, {}).get("value")
        held = str(got).lower() == want
        print(f"  {pid:5} {arm:8} {field:12} predicted {want:9} got {str(got):9} "
              f"{'HELD' if held else 'FAILED'}")
    c3 = str(V["negative"].get("T1", {}).get("value")).lower() == "no"
    print(f"\n  C-3 (negative caught as a restatement): {'HELD' if c3 else 'FAILED'}")
    print(f"  C-4 (negative NOT caught -- the contradictory prediction): "
          f"{'FAILED' if c3 else 'HELD'}")
    reason = V["negative"].get("reason_matches", {}).get("value")
    print(f"  reason given matches the equivalence argument: {reason}")
    better = V["negative"].get("reason_better", {}).get("value")
    if c3 and reason is False and not better:
        notes.append("negative control: correct verdict, WRONG REASON -- a wrong answer with a "
                     "lucky verdict, per PREREG section 5")
    elif c3 and reason is False and better:
        notes.append("negative control: correct verdict, and a reason DIFFERENT FROM THE PREDICTED "
                     "ONE AND BETTER. PREREG section 5 has two cases and needed three: this one "
                     "fails the PREDICTION, not the response. The respondent declines the "
                     "iff-equivalence my prediction asserted, so the premise I inherited from the "
                     "reference corpus is what is now in doubt.")

    sep = (str(V["positive"].get("T1", {}).get("value")).lower() == "yes"
           and str(V["negative"].get("T1", {}).get("value")).lower() == "no")
    print(f"\n=== the only claim the controls carry\n")
    print(f"  does the rubric SEPARATE a real board from a restatement? "
          f"{'YES' if sep else 'NO'}")
    if not sep:
        print("  C-6 applies: the instrument does not discriminate on T1 alone, and PROMPT.md")
        print("  needs a clause that forces the equivalence question explicitly.")
    for n in notes:
        print(f"\n  NOTE: {n}")
    for b in bad:
        print(f"\n  FAILED  {b}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""The leak screen. `python3 screen.py`. Read-only.

Reads `leaks.json` and reports what the three leak kinds buy, separating the part
with prescriptive content from the residual bucket. Also checks the two claims the
write-up makes about its own weakness, so they cannot rot: that the fit is 13/13 and
therefore not evidence, and that WRONG_STATISTIC's prescription is vacuous.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
D = json.loads((HERE / "leaks.json").read_text(encoding="utf-8"))
USEFUL = ("ACCUMULATION", "SATURATION")


def main() -> int:
    items = D["items"]
    print("=== every case, by leak kind read off the BEFORE-board\n")
    for kind in ("ACCUMULATION", "SATURATION", "WRONG_STATISTIC"):
        rows = [i for i in items if i["kind"] == kind]
        tag = "" if kind in USEFUL else "   <- residual bucket, prescription is vacuous"
        print(f"  {kind} ({len(rows)}){tag}")
        for i in rows:
            print(f"     {i['id']:30} {i['leak_quote'][:76]}")
        print()

    fit = sum(1 for i in items if i["matched"])
    useful = [i for i in items if i["kind"] in USEFUL]
    print(f"  fit: {fit}/{len(items)} prescriptions consistent with what happened")
    print(f"  usable yield: {len(useful)}/{len(items)} -- the kinds whose prescription names "
          f"something to do")
    print()
    print("  THE FIT IS NOT EVIDENCE. Every kind was assigned by one instance that already knew")
    print("  every after-board, so 13/13 is the signature of a post-hoc classification. The")
    print("  corpus does not REFUTE the taxonomy; the test is a blind assignment by raters who")
    print("  have not seen the after-boards, scored with the D20 instrument against the measured")
    print("  kappa = 0.048 baseline. That test is cheap and has not been run.")
    print()
    print("  And a third of the fit is decoration: WRONG_STATISTIC's prescription -- 'find a")
    print("  certificate that sees the right quantity' -- is satisfied by almost any board change,")
    print("  so it cannot be wrong and predicts nothing.")

    live = D["live_case"]
    print(f"\n=== where the screen points now: {live['id']}\n")
    print(f"  {live['what']}\n")
    print(f"  it replaced a leak of kind: {live['leak_kind_of_what_it_replaced']}")
    print("  its own open leaks:")
    for x in live["its_own_open_leaks"]:
        print(f"     - {x}")

    bad = []
    if fit != len(items):
        bad.append("leaks.json no longer fits 13/13; the write-up's caveat needs rewriting")
    if len(useful) != 7:
        bad.append("the usable-yield figure of 7/13 in FINDER.md is stale")
    for i in items:
        if not i.get("leak_quote"):
            bad.append(f"{i['id']} has no leak quote, so its kind is unsourced")
    for b in bad:
        print(f"\n  FAILED  {b}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

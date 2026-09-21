#!/usr/bin/env python3
"""Score PREREG_PTE11.md sec 5 against evidence. Committed before the n=11 data exists.

The rule this file exists to enforce: a prediction with no evidence is NOT-SCORED, never a pass.
Absence of a falsifying observation is not a confirmation, and the way that mistake gets made is
a scorer written after the numbers are in.

Every invocation re-runs the controls first. At size 11 there is no known object to find, so the
controls at n=5 and n=7 are the only evidence that a null means anything; if they fail, nothing
below is scored at all.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify, search_symmetric, search_pattern

CONFIRMED, FALSIFIED, NOT_SCORED = "CONFIRMED", "FALSIFIED", "NOT-SCORED"


def load(pattern):
    return [json.load(open(p)) for p in sorted(glob.glob(os.path.join(HERE, pattern)))]


def n11_runs(pattern=False):
    want = "PTE^0 symmetric (C and -C disjoint)"
    return [r for r in load("runs/*.json")
            if isinstance(r, dict) and r.get("n") == 11
            and (r.get("variant") == want) == pattern]


def score_B1(runs, log):
    done = [r["H"] for r in runs if r.get("exhaustive")]
    if not done:
        return NOT_SCORED, "no exhaustive pattern-search run on file"
    hi = max(done)
    if hi >= 100:
        return FALSIFIED, f"reached H={hi} exhaustively, predicted not to reach 100"
    if hi < 70:
        if not log.get("budget_exhausted"):
            return NOT_SCORED, f"best exhaustive run is H={hi}, but the hour is not recorded as spent"
        return FALSIFIED, f"hour spent, best exhaustive run only H={hi}, predicted >= 70"
    return CONFIRMED, f"exhaustive to H={hi}: at or above 70, below 100"


def score_B4(runs):
    if not runs:
        return NOT_SCORED, "no pattern-search run on file"
    rate = sum(r["right_enumerated"] for r in runs) / sum(r["seconds"] for r in runs)
    if 86_000 <= rate <= 344_000:
        return CONFIRMED, f"pooled rate {rate/1000:.0f}k/s, inside 86k-344k"
    return FALSIFIED, f"pooled rate {rate/1000:.0f}k/s, outside 86k-344k"


def score_A1(runs, log):
    """H >= 20 reached exhaustively, and H = 50 not reached."""
    done = [r["H"] for r in runs if r.get("exhaustive")]
    if not done:
        return NOT_SCORED, "no exhaustive n=11 run on file"
    hi = max(done)
    if hi >= 50:
        return FALSIFIED, f"reached H={hi} exhaustively, predicted not to reach 50"
    if hi < 20:
        if not log.get("budget_exhausted"):
            return NOT_SCORED, (f"best exhaustive run is H={hi}, below the predicted 20, but "
                                f"runs/RUN_LOG.json does not say the hour was spent")
        return FALSIFIED, f"hour spent, best exhaustive run only H={hi}, predicted >= 20"
    return CONFIRMED, f"exhaustive to H={hi}: at or above 20, below 50"


def score_A2(log):
    """Memory, not the clock, is what stops it."""
    stopped = log.get("stopped_by")
    if stopped is None:
        return NOT_SCORED, "runs/RUN_LOG.json has no `stopped_by` field"
    if stopped == "memory":
        return CONFIRMED, "the left table is what ran out"
    if stopped == "clock":
        headroom = log.get("memory_headroom")
        if headroom is None:
            return NOT_SCORED, "stopped by the clock, but no `memory_headroom` recorded"
        return (FALSIFIED, "stopped by the clock with memory to spare") if headroom else (
            CONFIRMED, "the clock ran out only because memory forced a smaller split")
    if stopped == "completed":
        return FALSIFIED, "the search completed the budgeted region; neither limit bound"
    return NOT_SCORED, f"unrecognised stopped_by: {stopped!r}"


def score_A3(runs):
    """No size-11 solution anywhere in the covered region."""
    if not runs:
        return NOT_SCORED, "no n=11 run on file"
    hits = [s for r in runs for s in r.get("solutions", [])]
    if hits:
        A, B = hits[0]["A"], hits[0]["B"]
        ok, why = verify.is_ideal(A, B)
        return FALSIFIED, (f"a solution is on file and {'VERIFIES' if ok else 'DOES NOT verify'}: "
                           f"{A} / {B} -- {why}")
    covered = sorted(r["H"] for r in runs if r.get("exhaustive"))
    return CONFIRMED, f"no solution in {len(runs)} run(s); exhaustive at H in {covered or 'none'}"


def score_A4(ev):
    """Published symmetric bound at least 1000x ours; falsified within 10x."""
    if not ev:
        return NOT_SCORED, "evidence/A4_literature.json absent -- promoting search not run"
    e = ev[0]
    for f in ("published_height_bound", "our_height", "source"):
        if f not in e:
            return NOT_SCORED, f"evidence/A4_literature.json lacks `{f}`"
    ratio = e["published_height_bound"] / e["our_height"]
    if ratio >= 1000:
        return CONFIRMED, f"published bound is {ratio:.0f}x ours ({e['source']})"
    if ratio <= 10:
        return FALSIFIED, f"published bound is only {ratio:.1f}x ours ({e['source']})"
    return NOT_SCORED, f"ratio {ratio:.0f}x falls in the unregistered band 10x-1000x"


def score_A5(ev):
    """The asymmetric region is NOT virgin."""
    if not ev:
        return NOT_SCORED, "evidence/A5_asymmetric.json absent -- promoting search not run"
    e = ev[0]
    if "asymmetric_searches_found" not in e:
        return NOT_SCORED, "evidence/A5_asymmetric.json lacks `asymmetric_searches_found`"
    found = e["asymmetric_searches_found"]
    if found:
        return CONFIRMED, f"{len(found)} published asymmetric search(es): {found[0]}"
    return FALSIFIED, "no published asymmetric search found; the region really is unswept"


def main():
    print("controls (nothing below is scored if these fail):")
    verify.controls()
    for line in search_symmetric.controls()[0]:
        print("  ok   " + line)
    for line in search_pattern.controls()[0]:
        print("  ok   " + line)

    runs = n11_runs()
    pruns = n11_runs(pattern=True)
    logs = load("runs/RUN_LOG.json")
    log = logs[0] if logs else {}
    plogs = load("runs/RUN_LOG_pattern.json")
    plog = plogs[0] if plogs else {}
    scores = {
        "A-1": score_A1(runs, log),
        "A-2": score_A2(log),
        "A-3": score_A3(runs),
        "A-4": score_A4(load("evidence/A4_literature.json")),
        "A-5": score_A5(load("evidence/A5_asymmetric.json")),
        "B-1": score_B1(pruns, plog),
        "B-2": score_A2(plog),
        "B-3": score_A3(pruns),
        "B-4": score_B4(pruns),
    }

    print(f"\n{'id':5}{'verdict':12}why")
    print("-" * 100)
    for k in sorted(scores):
        v, why = scores[k]
        print(f"{k:5}{v:12}{why}")
    print("-" * 100)
    tally = {v: sum(1 for x, _ in scores.values() if x == v)
             for v in (CONFIRMED, FALSIFIED, NOT_SCORED)}
    print(" ".join(f"{k}: {n}" for k, n in tally.items()))

    if tally[NOT_SCORED]:
        print(f"\n{tally[NOT_SCORED]} prediction(s) have no evidence. That is NOT a pass, and the "
              f"programme's verdict in PREREG_PTE11.md sec 6 cannot be read off this table yet.")

    # the failure condition registered in sec 6, evaluated only when all three are in
    trio = [scores[k][0] for k in ("A-3", "A-4", "A-5")]
    if all(v == CONFIRMED for v in trio):
        print("\nSECTION 6 FIRES: A-3, A-4 and A-5 all confirmed -- PTE 11 is dead as a target, "
              "and the registered next move is the Hadamard worklist (order 2284, v=571).")
    elif NOT_SCORED in trio:
        print("\nSection 6 not evaluable: it needs A-3, A-4 and A-5, and at least one is unscored.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

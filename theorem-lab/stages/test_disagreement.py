#!/usr/bin/env python3
"""Tests for the disagreement stage. Run: python3 test_disagreement.py"""
import math
import sys

from disagreement import (ProbeOutsideReserve, Resolution, assert_disjoint,
                          resolve, surviving)

FAILURES = []


def check(name, cond, detail=""):
    if cond:
        print("  pass  %s" % name)
    else:
        print("  FAIL  %s  %s" % (name, detail))
        FAILURES.append(name)


def test_unique():
    r = resolve(["a"], lambda h: 0, lambda h, c: 1, [1, 2],
                lambda c: 1)
    check("unique hypothesis needs no probe",
          r.verdict == "UNIQUE" and r.probes_used == 0 and r.selected == "a")


def test_resolves_lcm_vs_max():
    """The Report K case, with a reserve disjoint from the holdout."""
    periods = {1: 1, 2: 1, 3: 2, 4: 2, 5: 4, 7: 6, 8: 2, 9: 6, 11: 10,
               16: 4, 25: 20, 13: 12, 17: 16}
    ops = {"lcm": math.lcm, "max": max}

    def predict(h, coord):
        a, b = coord
        return ops[h](periods[a], periods[b])

    # truth is lcm
    def observe(coord):
        a, b = coord
        return math.lcm(periods[a], periods[b])

    reserve = [(3, 4), (5, 11), (7, 9)]      # (3,4): 2 vs 2 agree; (5,11) splits
    r = resolve(list(ops), lambda h: 0, predict, reserve, observe)
    check("lcm/max tie resolves to lcm",
          r.verdict == "RESOLVED" and r.selected == "lcm", r.verdict)
    check("resolution costs exactly one probe", r.probes_used == 1,
          str(r.probes_used))
    check("the probe is the first discriminating coordinate",
          r.rounds[0]["probe"] == (5, 11), str(r.rounds[0]["probe"]))
    check("agreeing coordinates are skipped, not probed",
          (3, 4) not in r.observations)


def test_underdetermined_is_reported_not_broken():
    ops = {"lcm": math.lcm, "max": max}
    periods = {2: 1, 4: 2}

    def predict(h, coord):
        a, b = coord
        return ops[h](periods[a], periods[b])

    reserve = [(2, 4)]        # lcm(1,2) = max(1,2) = 2: no disagreement here
    r = resolve(list(ops), lambda h: 0, predict, reserve,
                lambda c: 2)
    check("verdict is UNDERDETERMINED, not a silent tie-break",
          r.verdict == "UNDERDETERMINED" and r.selected is None, r.verdict)
    check("both survivors are returned for the record",
          sorted(r.survivors) == ["lcm", "max"])
    check("no probe was spent on an agreeing coordinate", r.probes_used == 0)


def test_space_excluding_truth_is_flagged():
    def predict(h, coord):
        return {"a": 1, "b": 2}[h]
    r = resolve(["a", "b"], lambda h: 0, predict, [0], lambda c: 99)
    check("hypothesis space excluding the truth is flagged",
          r.verdict == "SPACE_EXCLUDES_TRUTH" and r.survivors == [],
          r.verdict)


def test_multiround():
    """Three survivors need two probes."""
    truth = {1: 10, 2: 20, 3: 30}
    hyps = {"t": lambda c: truth[c],
            "off1": lambda c: truth[c] + (1 if c == 1 else 0),
            "off2": lambda c: truth[c] + (1 if c == 2 else 0)}
    r = resolve(list(hyps), lambda h: 0,
                lambda h, c: hyps[h](c), [1, 2, 3], lambda c: truth[c])
    check("three survivors resolve to the truth",
          r.verdict == "RESOLVED" and r.selected == "t", r.verdict)
    check("two probes were needed", r.probes_used == 2, str(r.probes_used))


def test_reserve_discipline():
    try:
        assert_disjoint([1, 2, 3], [3, 4])
        check("assert_disjoint rejects an overlapping reserve", False)
    except ProbeOutsideReserve:
        check("assert_disjoint rejects an overlapping reserve", True)
    assert_disjoint([1, 2], [3, 4])
    check("assert_disjoint accepts a clean reserve", True)


def test_budget():
    truth = {i: i for i in range(20)}
    hyps = {"t": lambda c: truth[c]}
    for i in range(1, 12):
        hyps["off%d" % i] = (lambda c, i=i: truth[c] + (1 if c == i else 0))
    r = resolve(list(hyps), lambda h: 0, lambda h, c: hyps[h](c),
                list(range(1, 20)), lambda c: truth[c], max_probes=3)
    check("probe budget is respected", r.probes_used == 3, str(r.probes_used))
    check("unresolved after budget reports UNDERDETERMINED",
          r.verdict == "UNDERDETERMINED", r.verdict)


def test_surviving_keeps_ties():
    s = surviving(["a", "b", "c"], lambda h: {"a": 1, "b": 1, "c": 2}[h])
    check("surviving keeps every tied hypothesis", sorted(s) == ["a", "b"])


if __name__ == "__main__":
    for fn in (test_unique, test_resolves_lcm_vs_max,
               test_underdetermined_is_reported_not_broken,
               test_space_excluding_truth_is_flagged, test_multiround,
               test_reserve_discipline, test_budget, test_surviving_keeps_ties):
        print(fn.__name__)
        fn()
    print()
    if FAILURES:
        print("FAILED: %s" % ", ".join(FAILURES))
        sys.exit(1)
    print("all tests passed")

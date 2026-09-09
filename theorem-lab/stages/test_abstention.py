#!/usr/bin/env python3
"""Tests for the abstention stage. Run: python3 test_abstention.py"""
import sys

from abstention import (ABSTAIN_MISFIT, ABSTAIN_UNSUPPORTED, LICENSED,
                        guarded, license_rule, selective_report)

FAILURES = []


def check(name, cond, detail=""):
    print(("  pass  " if cond else "  FAIL  ") + name + ("  " + detail if not cond else ""))
    if not cond:
        FAILURES.append(name)


truth = {2: 1, 4: 2, 8: 3, 9: 2, 16: 4, 25: 2, 27: 3, 32: 5, 49: 2}


def test_misfit_branch_abstains():
    # "even -> n//4" is wrong on 2,4,8; "odd -> n-1" is wrong on 9,25,27,49
    branches = ["even", "odd"]
    def branch_of(n): return "even" if n % 2 == 0 else "odd"
    def predict(b, n): return n // 4 if b == "even" else n - 1
    lic = license_rule(branches, truth, branch_of, predict, truth.get)
    check("a branch that mispredicts training abstains",
          all(b.verdict == ABSTAIN_MISFIT for b in lic.branches))
    g = guarded(predict, branch_of, lic)
    check("guarded predictor returns None for unlicensed branches",
          g(47) is None)
    check("no branch is licensed", not lic.any_licensed)


def test_good_branch_keeps_its_licence():
    branches = ["even", "odd"]
    def branch_of(n): return "even" if n % 2 == 0 else "odd"
    # correct on the odd atoms (9,25,27,49 -> 2,2,3,2), wrong on the even ones
    def predict(b, n):
        return n // 4 if b == "even" else {9: 2, 25: 2, 27: 3, 49: 2}.get(n, 0)
    lic = license_rule(branches, truth, branch_of, predict, truth.get)
    v = {b.branch: b.verdict for b in lic.branches}
    check("the fitting branch is licensed", v["odd"] == LICENSED, str(v))
    check("the misfitting branch is not", v["even"] == ABSTAIN_MISFIT, str(v))
    g = guarded(predict, branch_of, lic)
    check("partial abstention: good branch still answers", g(9) == 2)
    check("partial abstention: bad branch declines", g(8) is None)


def test_support_threshold():
    data = {2: 1, 3: 1}
    branches = ["two", "three"]
    def branch_of(n): return "two" if n == 2 else "three"
    def predict(b, n): return 1
    lic = license_rule(branches, data, branch_of, predict, data.get,
                       min_support=2)
    check("a branch with one supporting point abstains as unsupported",
          all(b.verdict == ABSTAIN_UNSUPPORTED for b in lic.branches))
    lic2 = license_rule(branches, data, branch_of, predict, data.get,
                        min_support=1)
    check("min_support=1 licenses it", all(b.licensed() for b in lic2.branches))


def test_tolerance_is_configurable():
    branches = ["all"]
    def branch_of(n): return "all"
    def predict(b, n): return truth[n] + (1 if n == 32 else 0)
    lic0 = license_rule(branches, truth, branch_of, predict, truth.get)
    lic1 = license_rule(branches, truth, branch_of, predict, truth.get,
                        fit_tolerance=1)
    check("exact fit required by default",
          lic0.branches[0].verdict == ABSTAIN_MISFIT)
    check("tolerance 1 admits one error",
          lic1.branches[0].verdict == LICENSED)


def test_selective_report_penalises_blanket_abstention():
    r = selective_report([1, 2, 3], lambda p: None, lambda p: p)
    check("abstaining everywhere gives coverage 0",
          r["coverage"] == 0.0 and r["selective_accuracy"] is None)
    check("and wins nothing on the headline number",
          r["accuracy_counting_abstention_as_error"] == 0.0)
    r2 = selective_report([1, 2, 3], lambda p: p if p < 3 else None,
                          lambda p: p)
    check("partial coverage reported correctly",
          r2["coverage"] == round(2 / 3, 4) and r2["selective_accuracy"] == 1.0)


if __name__ == "__main__":
    for fn in (test_misfit_branch_abstains, test_good_branch_keeps_its_licence,
               test_support_threshold, test_tolerance_is_configurable,
               test_selective_report_penalises_blanket_abstention):
        print(fn.__name__)
        fn()
    print()
    if FAILURES:
        print("FAILED: %s" % ", ".join(FAILURES))
        sys.exit(1)
    print("all tests passed")

#!/usr/bin/env python3
"""
Extrapolation licensing: the second standard stage.

WHY THIS EXISTS
---------------
Report L: the base-case fitter chose the least-bad rule from a grammar that
could not express the answer, and then extrapolated it. The chosen rule had
**10 training errors** -- the warning was already in the data -- and it predicted
a threshold of 11 for m = 47, whose true threshold is 1. End-to-end accuracy
0.715 against a 0.917 majority baseline: with a wrong-shaped vocabulary the
laboratory did not degrade to the baseline, it confidently went below it.

`min(error)` never asks whether the minimum is good enough. This stage asks.

THE TWO LICENCES
----------------
A branch of a fitted rule earns the right to extrapolate only if both hold:

1. **Fit.** In a deterministic symbolic setting an invariant is an exact
   function of its object, so a branch that mispredicts any training point it
   covers is definitely wrong. Tolerance is configurable but defaults to 0.
2. **Support.** A branch constrained by too few training points is unfalsified
   rather than confirmed. Default: at least `min_support` (2) covered points.

Failing either, the branch ABSTAINS: it returns None rather than a number.

SCORING CONVENTION
------------------
Abstention is not a free pass. Report coverage alongside selective accuracy,
and keep the laboratory's existing convention (an abstention counts as an error
in the headline number, which is why `lab.py` marks such candidates
INCOMPLETE). A rule that abstains everywhere scores coverage 0 and wins nothing.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Sequence

LICENSED = "LICENSED"
ABSTAIN_MISFIT = "ABSTAIN_MISFIT"
ABSTAIN_UNSUPPORTED = "ABSTAIN_UNSUPPORTED"


@dataclass
class BranchLicence:
    branch: Any
    verdict: str
    covered: int
    errors: int
    reason: str = ""

    def licensed(self) -> bool:
        return self.verdict == LICENSED


@dataclass
class Licence:
    branches: list = field(default_factory=list)
    fit_tolerance: int = 0
    min_support: int = 2

    def verdict_for(self, branch) -> BranchLicence | None:
        for b in self.branches:
            if b.branch == branch:
                return b
        return None

    @property
    def any_licensed(self) -> bool:
        return any(b.licensed() for b in self.branches)

    def to_json(self) -> dict:
        return {
            "label": "COMPUTED",
            "stage": "extrapolation_licensing",
            "fit_tolerance": self.fit_tolerance,
            "min_support": self.min_support,
            "branches": [
                {"branch": str(b.branch), "verdict": b.verdict,
                 "covered": b.covered, "errors": b.errors, "reason": b.reason}
                for b in self.branches],
            "licensed_branches": sum(1 for b in self.branches if b.licensed()),
            "abstaining_branches": sum(
                1 for b in self.branches if not b.licensed()),
        }


def license_rule(branches: Sequence[Any],
                 training: Iterable[Any],
                 branch_of: Callable[[Any], Any],
                 predict: Callable[[Any, Any], Any],
                 observed: Callable[[Any], Any],
                 fit_tolerance: int = 0,
                 min_support: int = 2) -> Licence:
    """
    branches   : the rule's branches (decision-list arms, cases, ...).
    training   : the points the rule was fitted on.
    branch_of  : point -> the branch that covers it.
    predict    : (branch, point) -> predicted value.
    observed   : point -> observed value.
    """
    covered: dict = {b: [] for b in branches}
    for pt in training:
        b = branch_of(pt)
        if b in covered:
            covered[b].append(pt)

    lic = Licence(fit_tolerance=fit_tolerance, min_support=min_support)
    for b in branches:
        pts = covered[b]
        errs = sum(1 for pt in pts if predict(b, pt) != observed(pt))
        if errs > fit_tolerance:
            lic.branches.append(BranchLicence(
                b, ABSTAIN_MISFIT, len(pts), errs,
                "mispredicts %d of %d covered training points; a rule that "
                "cannot reproduce its own training data has no licence to "
                "extrapolate" % (errs, len(pts))))
        elif len(pts) < min_support:
            lic.branches.append(BranchLicence(
                b, ABSTAIN_UNSUPPORTED, len(pts), errs,
                "only %d covered training point(s); unfalsified rather than "
                "confirmed" % len(pts)))
        else:
            lic.branches.append(BranchLicence(b, LICENSED, len(pts), errs))
    return lic


def guarded(predict: Callable[[Any, Any], Any],
            branch_of: Callable[[Any], Any],
            licence: Licence) -> Callable[[Any], Any]:
    """Wrap a predictor so unlicensed branches abstain (return None)."""
    def f(point):
        b = branch_of(point)
        v = licence.verdict_for(b)
        if v is None or not v.licensed():
            return None
        return predict(b, point)
    return f


def selective_report(points, predictor, observed) -> dict:
    """Coverage and selective accuracy, plus the abstain-as-error number."""
    n = answered = right = 0
    for pt in points:
        n += 1
        p = predictor(pt)
        if p is None:
            continue
        answered += 1
        right += int(p == observed(pt))
    return {
        "label": "COMPUTED",
        "points": n,
        "answered": answered,
        "coverage": round(answered / n, 4) if n else None,
        "selective_accuracy": round(right / answered, 4) if answered else None,
        "accuracy_counting_abstention_as_error": round(right / n, 4) if n
        else None,
    }

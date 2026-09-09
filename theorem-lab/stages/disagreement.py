#!/usr/bin/env python3
"""
Disagreement resolution: a standard stage of the laboratory.

WHY THIS EXISTS
---------------
Selection stages rank hypotheses by error and break ties by cost or by
identifier. Report K showed what that costs: on the cross-object task the
correct law (`lcm`) and a wrong one (`max`) both scored 30/30 on the training
objects -- they are observationally identical there -- and a tie-break chose the
wrong one. The failure was not a modelling error but an IDENTIFIABILITY problem,
and it was invisible from inside the training set.

It is, however, detectable without any answer key: two surviving hypotheses
disagree about a specific, nameable object. This stage finds that object, spends
one observation on it, and repeats.

PROTOCOL RULES (enforced by construction, not by convention)
------------------------------------------------------------
1. Probes are drawn ONLY from a declared `reserve` of coordinates, which the
   caller must keep disjoint from the final holdout. `resolve` refuses to probe
   anything outside it, so resolving a tie can never consume held-out data.
   `assert_disjoint` is provided so callers can check that at set-up time.
2. Every probe is logged with the disagreement that motivated it, the value
   observed, and the survivors before and after.
3. If the tie cannot be broken -- the reserve contains no discriminating
   coordinate, or the probe budget runs out -- the verdict is `UNDERDETERMINED`
   and every surviving hypothesis is returned. The stage NEVER falls back to a
   silent tie-break: "the data does not determine the law, and here are the
   candidates" is a result, not a failure to produce one.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Hashable, Iterable, Sequence


class ProbeOutsideReserve(RuntimeError):
    """Raised if a caller's probe chooser strays outside the declared reserve."""


@dataclass
class Resolution:
    verdict: str                      # RESOLVED | UNDERDETERMINED | UNIQUE
    selected: Any                     # the surviving hypothesis, or None
    survivors: list                   # all hypotheses still standing
    rounds: list = field(default_factory=list)
    probes_used: int = 0
    observations: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        return {
            "label": "COMPUTED",
            "stage": "disagreement_resolution",
            "verdict": self.verdict,
            "selected": self.selected,
            "survivors": self.survivors,
            "probes_used": self.probes_used,
            "rounds": self.rounds,
            "observations": {str(k): v for k, v in self.observations.items()},
        }


def assert_disjoint(reserve: Iterable[Hashable],
                    holdout: Iterable[Hashable]) -> None:
    """Fail loudly at set-up if the reserve would leak the holdout."""
    overlap = set(reserve) & set(holdout)
    if overlap:
        raise ProbeOutsideReserve(
            "reserve overlaps the final holdout at %d coordinates, e.g. %r"
            % (len(overlap), sorted(overlap)[:5]))


def surviving(hypotheses: Sequence[Hashable],
              score: Callable[[Hashable], Any]) -> list:
    """Hypotheses tied for the best (lowest) score. Ties are kept, not broken."""
    scored = [(score(h), h) for h in hypotheses]
    best = min(s for s, _ in scored)
    return [h for s, h in scored if s == best]


def resolve(hypotheses: Sequence[Hashable],
            score: Callable[[Hashable], Any],
            predict: Callable[[Hashable, Hashable], Any],
            reserve: Sequence[Hashable],
            observe: Callable[[Hashable], Any],
            max_probes: int = 8,
            rescore: Callable[[dict], Callable[[Hashable], Any]] | None = None
            ) -> Resolution:
    """
    Resolve a tie by observing coordinates the survivors disagree about.

    hypotheses : the candidates to choose between.
    score      : hypothesis -> comparable score on data already seen
                 (lower is better). Ties in this score are what we resolve.
    predict    : (hypothesis, coordinate) -> predicted value. Two hypotheses
                 "disagree" at a coordinate when their predictions differ.
    reserve    : coordinates that MAY be probed. Must be disjoint from the
                 final holdout; see assert_disjoint.
    observe    : coordinate -> observed value. Called at most max_probes times.
    rescore    : optional; given the accumulated observations, returns a fresh
                 score function. Defaults to eliminating hypotheses that
                 mispredict an observation, which is the usual case.
    """
    survivors = surviving(hypotheses, score)
    res = Resolution(verdict="UNIQUE" if len(survivors) == 1 else "",
                     selected=survivors[0] if len(survivors) == 1 else None,
                     survivors=list(survivors))
    if len(survivors) == 1:
        res.rounds.append({"survivors": _names(survivors), "probe": None,
                           "note": "no tie to resolve"})
        return res

    reserve = list(reserve)
    observations: dict = {}

    while len(survivors) > 1 and res.probes_used < max_probes:
        probe = _first_disagreement(survivors, predict, reserve, observations)
        round_rec = {"survivors": _names(survivors), "probe": probe}
        if probe is None:
            round_rec["note"] = ("no coordinate in the reserve separates the "
                                 "survivors")
            res.rounds.append(round_rec)
            break
        if probe not in reserve:                      # defensive; see rule 1
            raise ProbeOutsideReserve(repr(probe))

        value = observe(probe)
        observations[probe] = value
        res.probes_used += 1
        round_rec["predictions"] = {
            _name(h): _safe(predict, h, probe) for h in survivors}
        round_rec["observed"] = value

        if rescore is not None:
            survivors = surviving(survivors, rescore(observations))
        else:
            survivors = [h for h in survivors
                         if _safe(predict, h, probe) == value]
            if not survivors:
                round_rec["note"] = ("every survivor mispredicted the probe; "
                                     "the hypothesis space excludes the truth")
                res.rounds.append(round_rec)
                res.verdict = "SPACE_EXCLUDES_TRUTH"
                res.survivors = []
                res.observations = observations
                return res
        round_rec["survivors_after"] = _names(survivors)
        res.rounds.append(round_rec)

    res.observations = observations
    res.survivors = list(survivors)
    if len(survivors) == 1:
        res.verdict = "RESOLVED"
        res.selected = survivors[0]
    else:
        res.verdict = "UNDERDETERMINED"
        res.selected = None
    return res


def _first_disagreement(survivors, predict, reserve, seen):
    """Smallest reserve coordinate on which the survivors do not all agree."""
    for coord in reserve:
        if coord in seen:
            continue
        vals = []
        for h in survivors:
            v = _safe(predict, h, coord)
            if v is _UNDEFINED:
                vals = []
                break
            vals.append(v)
        if vals and len({_key(v) for v in vals}) > 1:
            return coord
    return None


class _Undefined:
    def __repr__(self):
        return "<undefined>"


_UNDEFINED = _Undefined()


def _safe(predict, h, coord):
    try:
        v = predict(h, coord)
    except Exception:
        return _UNDEFINED
    return _UNDEFINED if v is None else v


def _key(v):
    try:
        hash(v)
        return v
    except TypeError:
        return json.dumps(v, sort_keys=True, default=str)


def _name(h):
    return h if isinstance(h, str) else repr(h)


def _names(hs):
    return [_name(h) for h in hs]

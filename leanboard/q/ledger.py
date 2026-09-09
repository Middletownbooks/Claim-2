#!/usr/bin/env python3
"""
Q -- the FLT <-> NS bridge ledger.

Every candidate bridge that was actually examined, with its evidence level on
the brief's seven-point scale, the experiment that tested it, and the measured
gain. A bridge with no measured gain is recorded as a bridge with no measured
gain; that is the point of keeping a ledger rather than a narrative.

EVIDENCE LEVELS (brief section 1)
  1 ACTUAL_SHARED_LEAN_DEPENDENCY
  2 ACTUAL_SHARED_DEFINITION_OR_ABSTRACTION
  3 ACTUAL_SHARED_PROOF_INFRASTRUCTURE
  4 SHARED_PROOF_ARCHITECTURE
  5 MATHEMATICAL_ANALOGY
  6 PLAUSIBLE_BUT_UNTESTED_TRANSPORT
  7 SPECULATIVE_RESEARCH_BRIDGE
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

LEDGER = [
    {
        "id": "B1_mathlib_analysis_substrate",
        "source": "FLT (archimedean analysis in LanglandsTunnell, "
                  "AutomorphicForm, AlgebraicCurve, MeasureTheory)",
        "target": "NS (Analysis.Calculus / Analysis.Normed regions)",
        "mechanism": "both boards consume the same mathlib analysis modules "
                     "and declarations",
        "evidence_level": "1 ACTUAL_SHARED_LEAN_DEPENDENCY",
        "experiment": "substrate.py, decluse2.py: exact intersection of "
                      "imported modules and referenced declarations",
        "result": "211 of NS's 303 mathlib modules (69.6%) and 1948 of NS's "
                  "2486 mathlib declarations (78.4%) are also used by FLT; "
                  "12.4% and 7.7% of FLT's respectively",
        "measurable_gain": "NONE. This is a shared dependency on a common "
                           "library, i.e. Control A. Neither board supplies "
                           "the other with anything; both import mathlib.",
        "confidence": "high",
    },
    {
        "id": "B2_flt_analytic_contact_surface",
        "source": "FLT LocalParametrix, LanglandsTunnell CubicInduction / "
                  "AdelicEpstein, AutomorphicForm ComplexIwasawa, "
                  "AlgebraicCurve CellDissection",
        "target": "NS regularity and estimate regions",
        "mechanism": "the only part of FLT written in NS's analytic "
                     "vocabulary: symbol estimates, rapid decay, iterated "
                     "Frechet derivative bounds, contour integration",
        "evidence_level": "2 ACTUAL_SHARED_DEFINITION_OR_ABSTRACTION",
        "experiment": "per-module vocabulary intersection against the "
                      "declarations rare in FLT but heavy in NS",
        "result": "406 FLT files of 60 474 (0.67%), 400 distinct theorems. "
                  "LocalParametrix genuinely constructs a symbol-class "
                  "S^-2m estimate for a second-order elliptic operator: "
                  "|D^n r(xi)| <= C (1+|xi|)^-(2m+n).",
        "measurable_gain": "NONE MEASURED. Used as Control E in the transport "
                           "experiment, where it scored BELOW the random FLT "
                           "control (mean 0.105 vs 0.145).",
        "confidence": "high for the existence of the surface, high for the "
                      "absence of gain",
    },
    {
        "id": "B3_polynomial_exp_integrability",
        "source": "FLT LanglandsTunnell.integrableOn_and_integral_Ioi_exp_"
                  "neg_pi_mu",
        "target": "NS integrableOn_shift_exp, polynomial_exp_integrable, "
                  "const_polynomial_exp_integrable",
        "mechanism": "integrability of a polynomial times exp(-pi mu t) on a "
                     "half-line; both boards prove it independently",
        "evidence_level": "3 ACTUAL_SHARED_PROOF_INFRASTRUCTURE",
        "experiment": "transport2.py, exportable surfaces, token-set Jaccard",
        "result": "the only cross-board match at J>=0.6 in either direction; "
                  "3 NS lemmas matched to this one FLT lemma",
        "measurable_gain": "3 NS lemmas, ~0.1% of NS's exportable surface. "
                           "FAILS the section-13 negative control: this is a "
                           "gap in mathlib, not board-specific knowledge, and "
                           "would be better fixed upstream than transported.",
        "confidence": "high",
    },
    {
        "id": "B4_nonexistence_architecture",
        "source": "FLT: no counterexample to a^n+b^n=c^n",
        "target": "NS: no global smooth solution with bounded energy",
        "mechanism": "both headline results are non-existence statements",
        "evidence_level": "5 MATHEMATICAL_ANALOGY",
        "experiment": "read the two main theorems; arch.py pattern profile",
        "result": "the shapes are DUAL, not shared. FLT refutes a "
                  "counterexample (the whole theorem is a negation); NS "
                  "constructs one (exists data such that no solution exists). "
                  "FLT's work is in classification machinery, NS's in explicit "
                  "construction plus quantitative estimates.",
        "measurable_gain": "NONE. Recorded to prevent promotion of an "
                           "analogy to a shared architecture.",
        "confidence": "high",
    },
    {
        "id": "B5_local_to_global",
        "source": "FLT (adelic / local-global machinery)",
        "target": "NS",
        "mechanism": "a local-to-global assembly pattern, the brief's leading "
                     "candidate architecture",
        "evidence_level": "4 SHARED_PROOF_ARCHITECTURE -- REFUTED",
        "experiment": "arch.py statement and tactic channels",
        "result": "FLT 35.2% of statements and 15.75% of proofs; NS 3.95% and "
                  "0.04%. NS essentially never does local-to-global.",
        "measurable_gain": "NONE. The architecture is not shared.",
        "confidence": "high",
    },
    {
        "id": "B6_generic_proof_engineering",
        "source": "either board",
        "target": "the other",
        "mechanism": "have/calc lemma chains, case splitting, finite-level "
                     "approximation, auxiliary object construction",
        "evidence_level": "4 SHARED_PROOF_ARCHITECTURE",
        "experiment": "arch.py",
        "result": "intermediate_lemma_chain 93.5% vs 90.1%; "
                  "finite_level_approximation 43.4% vs 45.0%. Genuinely "
                  "shared and nearly equal.",
        "measurable_gain": "NONE ATTRIBUTABLE. These are what any large Lean "
                           "development does; they are Control A at the "
                           "architecture level, not a bridge between these "
                           "two boards.",
        "confidence": "high",
    },
    {
        "id": "B7_strategy_transport",
        "source": "either board's construction trajectory",
        "target": "the other",
        "mechanism": "Level III: transport of search or decomposition strategy",
        "evidence_level": "NOT TESTABLE ON THESE ARTIFACTS",
        "experiment": "trajectory recovery attempt",
        "result": "no trajectory exists to study. Both repositories are a "
                  "single squashed commit. FLT's ATTRIBUTION.md states its "
                  "files 'were assembled by AI agents and were published "
                  "without their comments'; measured comment density is "
                  "0.000% in Theorems and 0.002% in P2M/Sol against NS's "
                  "~2%. NS's comments are mathematical documentation keyed to "
                  "the source paper's equation numbers, not process records. "
                  "No intermediate DAG, failed attempts, routing decisions or "
                  "timestamps are recoverable from either.",
        "measurable_gain": "NOT MEASURABLE",
        "confidence": "high that the data is absent",
    },
]


def main():
    rows = []
    for b in LEDGER:
        rows.append(b)
    out = {"label": "LEDGER", "edge": "FLT <-> NS",
           "note": "Every candidate examined, including the ones that failed. "
                   "No entry is promoted above the evidence its experiment "
                   "produced.",
           "bridges": rows}
    (OUT / "bridge_ledger_flt_ns.json").write_text(
        json.dumps(out, indent=1) + "\n")
    hdr = ("id", "evidence_level", "measurable_gain")
    with open(OUT / "bridge_ledger_flt_ns.csv", "w") as f:
        f.write("id,source,target,evidence_level,measurable_gain,confidence\n")
        for b in rows:
            f.write('"%s","%s","%s","%s","%s","%s"\n'
                    % (b["id"], b["source"].replace('"', "'"),
                       b["target"].replace('"', "'"), b["evidence_level"],
                       b["measurable_gain"].replace('"', "'").split(".")[0],
                       b["confidence"]))
    print("%-34s %-46s %s" % hdr)
    for b in rows:
        print("%-34s %-46s %s" % (b["id"], b["evidence_level"],
                                  b["measurable_gain"].split(".")[0][:40]))


if __name__ == "__main__":
    main()

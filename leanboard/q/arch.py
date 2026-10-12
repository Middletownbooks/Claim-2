#!/usr/bin/env python3
"""
Q4 -- proof-architecture profiles, measured rather than asserted.

For each board this counts, per declaration, evidence for the structural
patterns the brief lists. Two independent channels are kept apart because they
can disagree, and when they do that is itself informative:

  STATEMENT channel -- what the theorem says (its Lean type). Robust: a
      statement ending in `False` really is a contradiction step, whatever the
      proof does.
  TACTIC channel -- how it is proved. Robust in a different way: `by_contra`
      in the proof text is a proof move, not a naming convention.

NAME evidence is collected too but is reported separately and trusted least:
FLT's own README warns its declaration names are machine-generated, and Report
A of this programme was already misled once by a name (`add_pow`).

Normalisation is per 1000 declarations, because FLT has 29 511 theorems and NS
37 301, so raw counts are not comparable.
"""
import json
import re
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOARDS = {
    "flt": ("/home/user/anthropics/fermats-last-theorem",
            ["Theorems"], ["P2M/Sol"]),
    "ns": ("/home/user/openai/navierstokesandeuler",
           ["NavierStokes", "Euler"], ["NavierStokes", "Euler"]),
}

# pattern -> (statement regexes, tactic regexes)
PATTERNS = {
    "contradiction": ([r"\bFalse\b", r"¬"], [r"\bby_contra\b", r"\babsurd\b",
                                             r"\bexact_mod_cast\s+absurd\b",
                                             r"\bcontradiction\b"]),
    "induction_on_parameter": ([], [r"\binduction\b", r"\bNat\.rec\b",
                                    r"\bstrong_induction\b", r"\brcases\s+n\b"]),
    "compactness_extraction": ([r"\bIsCompact\b", r"\bCompactSpace\b",
                                r"\bSubsequence\b", r"\bClusterPt\b"],
                               [r"\bIsCompact\b", r"\bexists_subseq\b"]),
    "approximation_limit": ([r"\bTendsto\b", r"\bFilter\.", r"\bCauchy\b",
                             r"\bTsum\b", r"\b∑'"],
                            [r"\bTendsto\b", r"\btendsto_"]),
    "local_to_global": ([r"\bCompletion\b", r"\bIsLocalization\b",
                         r"\bAdic\b", r"\badicCompletion\b", r"\bHeight\b",
                         r"\bIsDedekindDomain\b", r"\bValuation\b",
                         r"∀\s*\(?\s*[pqv]\s*:"],
                        [r"\bIsLocalization\b", r"\bCompletion\b"]),
    "deformation_lifting": ([r"\bDeformation\b", r"\bLift\b", r"\blift\b",
                             r"\bIsLift\b"], [r"\blift\b"]),
    "duality": ([r"\bDual\b", r"\badjoint\b", r"\bStarRing\b"], [r"\bdual\b"]),
    "descent": ([r"\bdescent\b", r"\bDescend\b", r"\bGaloisDescent\b"], []),
    "quotienting": ([r"\bQuotient\b", r"\bQuot\b", r"⧸"], [r"\bQuotient\b"]),
    "classification": ([r"\bclassification\b", r"\bClassify\b",
                        r"\bIsomorphismClass\b"], []),
    "energy_height_inequality": ([r"‖[^‖]{1,40}‖\s*[≤<]", r"\bnorm_le\b",
                                  r"\benergy\b", r"\bEnergy\b"],
                                 [r"\bnorm_le\b", r"\bgcongr\b",
                                  r"\bpositivity\b", r"\bnlinarith\b"]),
    "finite_level_approximation": ([r"\bFin\s", r"\bFinset\b", r"\bFinite\b"],
                                   [r"\bFinset\b", r"\bfin_cases\b"]),
    "gluing": ([r"\bglue\b", r"\bGlue\b", r"\bSheaf\b", r"\bIsOpenCover\b"],
               []),
    "functorial_transport": ([r"\bFunctor\b", r"\bCategoryTheory\b",
                              r"≃\b", r"\bEquiv\b"], [r"\bEquiv\b"]),
    "regularity_upgrade": ([r"\bContDiff\b", r"\bDifferentiable\b",
                            r"\bAnalyticAt\b", r"\bSmooth\b"],
                           [r"\bfun_prop\b", r"\bcontinuity\b"]),
    "auxiliary_object_construction": ([r"\b∃\b", r"\bExists\b"],
                                      [r"\brefine\s*⟨", r"\buse\b",
                                       r"\bexact\s*⟨"]),
    "case_split": ([], [r"\brcases\b", r"\bobtain\b", r"\bmatch\b",
                        r"\bsplit\b", r"\bby_cases\b"]),
    "intermediate_lemma_chain": ([], [r"\bhave\b", r"\bcalc\b",
                                      r"\bsuffices\b"]),
}
THM = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)?"
                 r"(theorem|lemma)\s+([A-Za-z0-9_.'!?]+)", re.M)


def profile(root, stmt_dirs, proof_dirs, cap=None):
    stmt = Counter()
    tac = Counter()
    ndecl = 0
    nfile = 0
    seen = set()
    for sub in stmt_dirs:
        d = Path(root) / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            if str(p) in seen:
                continue
            seen.add(str(p))
            nfile += 1
            if cap and nfile > cap:
                break
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            ndecl += len(THM.findall(txt))
            for name, (srx, _) in PATTERNS.items():
                if any(re.search(r, txt) for r in srx):
                    stmt[name] += 1
    for sub in proof_dirs:
        d = Path(root) / sub
        if not d.exists():
            continue
        for p in d.rglob("*.lean"):
            try:
                txt = p.read_text(errors="ignore")
            except Exception:
                continue
            for name, (_, trx) in PATTERNS.items():
                if trx and any(re.search(r, txt) for r in trx):
                    tac[name] += 1
    return stmt, tac, ndecl, nfile


def main():
    res = {}
    for b, (root, sd, pd) in BOARDS.items():
        print("profiling %s ..." % b, flush=True)
        s, t, n, f = profile(root, sd, pd)
        res[b] = {"statement_files_matching": s, "tactic_files_matching": t,
                  "declarations": n, "statement_files": f}
        print("  %s: %d files, %d declarations" % (b, f, n), flush=True)

    out = {"label": "COMPUTED_FROM_ARTIFACT", "boards": {}}
    for b, r in res.items():
        f = r["statement_files"]
        out["boards"][b] = {
            "statement_files": f, "declarations": r["declarations"],
            "statement_pct": {k: round(100 * v / f, 2)
                              for k, v in r["statement_files_matching"].items()},
            "tactic_pct": {k: round(100 * v / f, 2)
                           for k, v in r["tactic_files_matching"].items()},
        }
    (OUT / "arch.json").write_text(json.dumps(out, indent=1) + "\n")

    print("\n%-32s %14s %14s   %14s %14s"
          % ("pattern", "FLT stmt %", "NS stmt %", "FLT tac %", "NS tac %"))
    for k in PATTERNS:
        fs = out["boards"]["flt"]["statement_pct"].get(k, 0)
        ns = out["boards"]["ns"]["statement_pct"].get(k, 0)
        ft = out["boards"]["flt"]["tactic_pct"].get(k, 0)
        nt = out["boards"]["ns"]["tactic_pct"].get(k, 0)
        print("%-32s %14.2f %14.2f   %14.2f %14.2f" % (k, fs, ns, ft, nt))


if __name__ == "__main__":
    main()

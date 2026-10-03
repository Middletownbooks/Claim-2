# BootLoops skills applied to STATUS.md

Skills: `BootLoops-ai/skills` (12 `SKILL.md` files, read in full for `independence-bookkeeping`,
`planted-truth`, `acceptance-gate`, `referee-sim`; the other eight by section headings, checklists
and, for `prose-lint`, its grep sweep and sections E and N). `emitall` is covered in `../FINDINGS.md`.
Target is the same as the emitall pilot: `STATUS.md` (2026-09-09 revision) and the files it points to.

**Limits.** One agent (me) applied every skill, in one context, after already running emitall on the
same document. That is exactly the `referee-sim` "author-context contamination" failure, and
`acceptance-gate`'s "self-graded confidence" warning applies to every verdict below. Treat the
verdicts as leads to check, and re-run `referee-sim` in a fresh context before relying on it.
No agents were spawned.

## Summary

| skill | applied? | outcome |
|---|---|---|
| independence-bookkeeping | yes | 3 findings (one MEDIUM-HIGH: the 18/18 repair was measured on the holdout that exposed the failure) |
| planted-truth | yes | mutation test of the emitall spec: **34/34** clean rows fire when one digit is changed |
| acceptance-gate | yes | the K/L experiments have a declared gate and controls; two gaps |
| ref-check | partly | `citations.json` tally reproduces `CITATIONS.md` exactly; no entry re-verified against sources |
| lit-review | partly | the "not new" claim checked against current mathlib: λ and φ found, ν not found; no related-work review done |
| reading-contract | yes | STATUS's treatment of relayed claims is compliant; one provenance gap |
| prose-lint | yes | grep sweep clean on vocabulary; 3 number/honesty findings |
| referee-sim | yes, contaminated | 6 audience rows, 2 HIGH |
| tool-stewardship | yes | 2 findings (undocumented root scripts; STATUS is stale against the tree) |
| timing-discipline | partly | measured timings exist for term formation; no projection for the recommended next experiment |
| prove-protocol | **not applied** | STATUS contains no proof; relevant to `board-finder/gap/v4` (K7,11 / Theorem 7), not to this document |
| constant-recognition | **not applicable** | no integer-relation searches in STATUS |

## independence-bookkeeping

1. **MEDIUM-HIGH. The 18/18 repair was measured on the holdout that exposed the failure.**
   STATUS: "One added expression took the holdout to 18/18 and 1.000." `crossobject2/extension.py`
   states "same holdout". The follow-up was pre-registered (final paragraph of `crossobject2/PREREG.md`),
   which limits the damage, but the exponent primitive was chosen after the holdout showed 0/6.
   That holdout is now burned for this question: 18/18 shows the primitive is sufficient there, not
   that it generalises. Report L's "the entire failure was one missing word" is an inference from
   the same 18 objects. A fresh reserve, or the next unseen moduli, would turn it into a test.
2. **MEDIUM. Report K's headline omits that the language was written knowing the answer.**
   `REPORT_L.md` L.1: "Report K's success used a compositional language I wrote **knowing λ's
   shape**." STATUS's K bullet ("The per-object ceiling is broken … 18/18 … 1.00000") does not carry
   this; the qualifier only appears one bullet later, as the transfer failure. STATUS §2's laboratory
   paragraph does disclose that the *calibration windows* were chosen with the answer in view.
3. **MEDIUM. Pre-registration order cannot be audited from git.** Every `PREREG.md`, every result
   JSON and `STATUS.md` first appear in a single commit (`ea1bfb9`, 881 files, 2026-09-30); the branch
   has 51 commits in all. STATUS says of the two stages: "Both were built before the experiments that
   later needed them." The record in this repository cannot confirm or refute that. Sealed hashes
   help where present (`forecast_hash` and `holdout_untouched_until_freeze` are in the K and L
   results), and those are good practice.

Positives: reserve/holdout disjointness is recorded in the receipts (`protocol: training [1,30];
probe reserve [49,60]; holdout [31,48]`).

## planted-truth

- STATUS already reports two planted controls (structured world 48/48; adversarial world 648 errors,
  REFUTED). These satisfy steps 1 and 2 of the skill.
- Applied to the pilot's own comparator (step 5, "prove each control can fail"):
  `skills_pilot/mutation_test.py` changes the last digit of each quote, one row at a time.
  **34 of 34** clean rows flipped to FINDING; the other 7 rows were already findings, so the test is
  uninformative for them. Output: `mutation_test.txt`.
- An earlier version of this test reported "0 of 41 fired". That was my bug (`--quiet` suppresses
  the output I was parsing), not a property of emitall; the script now reads the JSON report. The
  episode is a small instance of the skill's "the comparator that cannot fail" class, caught because
  a baseline count was printed.
- Gap: the claims spec has no clean-twin or null input beyond the control row for NS coverage.

## acceptance-gate

- K and L: gate declared in `PREREG.md`, holdout reserved and frozen, positive and negative controls
  exist (see above). Verdict vocabulary in STATUS ("established / not established", "relayed, not
  reproduced") is close to the skill's CLOSED/OPEN discipline.
- Gap 1: no equivalent of "rerun at raised precision" applies (exact arithmetic), but the skill's
  leave-one-out analogue (does the repair survive dropping each training object?) is not reported.
- Gap 2: STATUS bolds "The per-object ceiling is broken" while its own §3 says abstraction
  invention proper is untouched. Consistent, but the verdict word carries more than the K bullet's
  evidence (one law, one language written with the answer in view).

## ref-check (partial)

`skills_pilot/citations_tally.py` recomputes the status tables from `proof-protocol/citations.json`:
44 rows ever written (36 VERIFIED, 2 CORRECTED, 2 PARTIAL, 2 UNVERIFIED, 1 DISPUTED, 1 SEARCH) and
41 distinct claims (35 / 2 / 2 / 0 / 1 / 1). These match `CITATIONS.md` exactly, including "Still
UNVERIFIED: none" (the two UNVERIFIED rows, C10 and C12, were superseded). I did **not** re-verify any
entry against INSPIRE/arXiv/Crossref, so this checks the bookkeeping, not the citations.

## lit-review (partial)

- STATUS §3: "λ's multiplicativity, φ, and ν are all in mathlib." Checked against mathlib4 HEAD
  `302343b` (2026-10-03; shallow sparse clone, `mathlib_check.txt`):
  λ is there (`ArithmeticFunction/Carmichael.lean`: `carmichael_mul`, `carmichael_lcm`);
  φ is there (`Nat.totient_mul`); **ν (max_p v_p(m)) was not found** by two grep patterns.
  "Not found" is not "absent": mathlib may state it under another name, and the board snapshot in
  STATUS is 2026-09-08, not today.
- Not done: any related-work search for the capability claims (term formation, abstraction
  invention, library learning). STATUS makes capability claims and disclaims mathematical novelty,
  so a full `lit-review` is not strictly triggered, but the §5 framing ("the loop the whole
  programme is named after") would need one before it is published as new. The skill forbids
  working from memory, so I name no prior art here.

## reading-contract

- Compliant: `leanboard/external_proofs.json` separates `verified_locally_by_this_session` from
  `NOT_verified_by_this_session`; STATUS says the external verification claims are "relayed, not
  reproduced". That is the contract's read/inferred separation.
- Gap: STATUS §3 asserts the discovered mathematics "is in mathlib" with no locator. Now supplied
  for λ and φ above; ν still lacks one.

## prose-lint

- Vocabulary sweep (the skill's own grep set, run on STATUS.md): clean apart from three benign
  literal uses ("upstream", "end-to-end").
- **E4/N1/N5. "3.5%" (NS mathlib coverage) is 3.559% from the raw counts**, rounded from a 4-d.p.
  receipt value. Should print 3.6%. (Also found by the emitall spec.)
- **E4. "Both were built before the experiments that later needed them"**: an unauditable
  precedence claim (see independence-bookkeeping 3).
- **N3. Units.** "18/18 invariants exact", "0/6 prime powers", "12/12 composable objects" all carry
  their noun. No finding.

## referee-sim (contaminated; see Limits)

| audience | objection | axis | answered where | severity |
|---|---|---|---|---|
| Incumbent: program-synthesis / library-learning researchers | "What does this do that existing synthesis systems with learned libraries do? Compared against what?" The only baseline in STATUS is majority class (0.90278, 0.91667) | novelty | **not answered** | **HIGH** |
| Auditors / replicators | "Re-emit your NS numbers." The strict-run receipts do not exist in the repo | correctness | **not answered** (emitall finding 1) | **HIGH** |
| Number theorists | "The mathematics is old." | novelty | §3 line 133, after the headline at line 62 | MEDIUM (off the reading path) |
| Formal-methods / Lean community | "Is anything verified?" | correctness | §3 line 130 and the header table, not the opening paragraph | MEDIUM |
| Lean upstreamers | "Show the 4,184." | correctness | disclosed as "unverifiable here"; receipt absent | MEDIUM |
| ML-evaluation reviewers | "Is the K language tuned to the answer?" | correctness | REPORT_L only, not STATUS | MEDIUM |

STATUS has no abstract; its first paragraph states branch and provenance but no scope limitation.

## tool-stewardship

1. **Root-level `PuLP`, `Z3`, `gurobipy`**: three extensionless scripts (145/148/130 lines) that are
   the same N=24 certificate in three solvers. No README, no known-answer test, no mention in
   STATUS. Three near-duplicate tools with no index row is the skill's "overlapping tools" case.
   I did not run them (Gurobi needs a licence).
2. **STATUS.md is stale against the tree.** It lists Reports through O and recommends a second
   round of term formation as the next experiment. The tree already holds `termform2/` (with
   `REPORT_P.md` and `round2_*.json`), `termform3/`, and Reports Q–U under `leanboard/`. No file in
   the repo says which revision supersedes which; the pilot quotes the revision as committed.

## timing-discipline (partial)

`termform/REPORT_M.md` records measured timings (175 s per target unfinished at v1 to about 40 s for
v2 after precomputing value tables; 35 formed terms at stage 1 versus 5,329 after stage 2). That is
the measure-first pattern. STATUS §5 calls the next round "cheap to test" with no projection; the
152-fold growth between stages is the quantity a projection would need. Superseded by `termform2`
if that experiment ran (see tool-stewardship 2).

## Not applied

- **prove-protocol**: STATUS contains no proof or theorem statement. It does bear on
  `board-finder/gap/v4/` (K7,11, Theorem 7), where its adversary-first and forced-diversity rules
  would apply; that is a separate pilot.
- **constant-recognition**: nothing in STATUS recognises a constant by integer relation.

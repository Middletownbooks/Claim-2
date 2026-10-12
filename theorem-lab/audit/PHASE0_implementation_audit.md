# Phase 0 — Implementation audit

Artifact audited: `theorem-lab/lab.py`, sha256 `bb8640cce91604e322ab6292bf09ec7a061d87965a836fe3f4bccd1270ff1405`,
1884 lines, stdlib only, Python 3.11.15.

## 0.1 Provenance of the audited artifact (read this first)

**HUMAN_SUPPLIED / caveat.** The laboratory source was supplied to this session as chat
text, not as a file. Markdown stripped the indentation of every top-level function body,
so the file audited here is a **transcription**, not a byte-identical copy of the artifact
that produced the pretest report. The original's hash is unknown and cannot be checked.

Evidence that the transcription is behaviourally faithful:

* `python3 lab.py --self-test --out runs/p0-selftest` completes and writes
  `synthetic_test.json` with `"synthetic assertions passed"`. Those assertions
  (`synthetic_assertions`, line 1639) are four independent structural checks written by the
  original author: the row invariant `mod:6` and column invariant `mod:3` are both
  discovered with zero contradictory pairs, the learned prefix/block code reproduces every
  observed T point, and the AND tensor factor survives on the synthetic world.
  A mis-transcription in the feature language, the sequence fitter, the invariant search or
  the tensor factoriser would break at least one of these.
* Self-test run: 15 424 unique oracle queries, 6 588 hypotheses, 14 exported candidates.

This caveat propagates: every "reproduces exactly" statement below means *reproduces on the
transcribed source*, and any claim about the original binary artifact is unverifiable here.

## 0.2 Implementation map

| Claimed capability | Exact implementation | Evidence / test |
|---|---|---|
| blind oracle | `oracle_answer` (67), `worker_main` (140) run in a **separate process** spawned by `Client.__init__` (152-166); `--oracle-command` allows a foreign binary | `grep oracle_answer lab.py` → only call site is line 143 inside `worker_main`. No discovery-side call exists. |
| oracle transport / logging | `Client.get` (175): one JSON line out, one JSON line in, appended to `oracle.jsonl` with an incrementing `_query_id` | `runs/*/oracle.jsonl` line count equals `summary.unique_oracle_queries` |
| query budget | `Client.budget` / `Client.calls` (168-183) | `RuntimeError("Unique oracle-query budget exhausted")`; default 40 000 |
| train/calibration split | `table_experiment.calibrate(1, m_train)` (742-756, called 758); E: `train` grid `r<=r_train, d<=d_train` (1417) | phases `T:train`, `E:calibration` in `summary.queries_by_first_phase` |
| validation split | T: `validation` (862); E: `validation_coords` with `r>R0 or d>D0` (1452) | phases `T:validation`, `E:validation` |
| final holdout | T: `final_coords` (947) then `assert key not in cache` (952); E: `final_coords` (1477) then same assert (1484) | the assert is the mechanism that makes "held out" checkable, not a comment |
| freeze boundary | `T_forecasts.json` + `T_freeze.json` written **before** the first final query (955-985); same for E (1491-1505); post-final replay `assert` (990, 1509) | `forecast_hash` in the freeze file; replay assert re-derives every frozen prediction |
| invariant discovery | `invariant_search` (471) over the shared feature vocabulary; scored by intra-group signature collisions | `*_invariants.json` |
| E-family learner | `tensor_experiment` (1409) fitting `fit_boolean_factor` (1278, AND/OR/XOR/IFF) and `fit_tile` (1320) **per modulus** | `E_freeze.json.models`, `second_order.json` |
| Boolean factorization | `fit_boolean_factor` (1278): exhaustive over all `2^r_train` first factors, second factor solved column-wise, ties broken by total sequence cost then ambiguity then canonical form | deterministic; `feasible_first_factor_assignments` reported per row |
| periodic model | `fit_sequence` (282) exact prefix+block with **two observed copies required**; 2-D `fit_tile` (1320) | `observed_repetitions` field; fallback branch (303) is explicitly `CONJECTURED` |
| falsification | `summarize` (407) + `refresh_entry` (452): any counterexample ⇒ `REFUTED`, any abstention ⇒ `INCOMPLETE` | `ledger.json`; `summary.refuted_hypotheses` |
| exception extraction | `exception_search` (530): partitions failures by least witness, witness gcd, coarse profile, and column-residue × witness-unit | `*_exceptions.json` |
| transport discovery | `transport_experiment` (1028): fixed template vocabulary (divisor up/down, column +1..+3, ×2, ×3; binary mul/lcm/gcd/add × any/coprime/noncoprime × and/or/xor × implication/reverse/equivalence) plus four witness-level claims | `transport.json` |
| recursive deformation | **not a search** — `main` appends four hand-written events (1810-1855) and calls `tensor_experiment` / `table_experiment("U")`; the deformation operators are literals in the source | `deformations.json`, `operator_origin: "preregistered library, not discovered"` |
| provenance logging | `label` fields (`OBSERVED` / `COMPUTED` / `CONJECTURED` / `UNCHECKED SPECIFICATION`) attached at construction of every record | grep `"label"` — 40+ sites |
| candidate export | `Laboratory.export` (697) → `theorem_candidates.json`, `targets.lean` | `write_formalization` (1589) |
| formal verification | **none.** `targets.lean` contains only `def target_i (Q : ...) : Prop := ...` | `summary.formally_verified_theorems` is the literal `0` (1876) |

## 0.3 Determinism, seeds, state

* **Seeds.** `--seed` (1681) is parsed, written into `manifest.json`, and never read again.
  `grep -E "random|numpy"` returns nothing. The search is deterministic; the manifest says
  so explicitly ("this version does not consume random numbers"). *Not* a hidden nondeterminism —
  a genuinely inert knob.
* **Nondeterministic components.** None internal. External: subprocess scheduling only.
  Dict iteration order is insertion-ordered; every ranking key ends in a total tiebreak
  (`e["id"]`, or `canonical(q)`), so ties are resolved deterministically.
* **Data generation.** Only `oracle_answer` (67). Labels (`truth`) are produced there and
  nowhere else. No label is synthesised, imputed, or defaulted anywhere in the learner.
* **Cached state.** `Client.cache` keyed `(family, coord, op)` — the single source of
  repeat answers, and the object the holdout asserts interrogate. `state = {"rf", "cycles"}`
  in `table_experiment` is **mutated after model registration** (see D7 below).
* **Checkpoints / artifacts.** Everything is under `--out`: `manifest.json`,
  `preregistration.json`, `oracle.jsonl`, `{T,U}_invariants.json`, `{T,U,E}_freeze.json`,
  `{T,U,E}_forecasts.json`, `{T,U,E}_exceptions.json`, `transport.json`,
  `second_order.json`, `ledger.json`, `deformations.json`, `theorem_candidates.json`,
  `targets.lean`, `summary.json` (or `failure.json` + `partial_ledger.json`).
  `out.mkdir(exist_ok=False)` (1727) forbids writing into an existing run directory, so runs
  cannot silently overwrite each other.
* **Filesystem reads.** Exactly one: `Path(__file__).read_bytes()` for the source hash (1729).
  The learner reads no data files; there is no dataset on disk to leak.

## 0.4 Discrepancies between prose and implementation

**D1 — "blind" is a convention, not an enforced boundary.** The oracle and the learner are the
same source file; blindness holds because the discovery functions never call `oracle_answer`
(verified) and because answers arrive over a pipe. Nothing *prevents* a future edit from
calling it directly. `--oracle-command` is the only genuinely enforced separation.

**D2 — the oracle answers with much more than the predicate's truth value.** Every `full`
response carries `profile` (the per-`x` boolean vector), `witness`, `fail_count`,
`pass_count`, `evaluated`. Consumers: `row_features` (328) puts `fail_count` into the T/U
feature vector; `observable_structure` (392) uses witness and counts; `transport_experiment`
(1093, 1099, 1108) reads whole profiles. **The E learner reads only `truth`** — verified:
`tensor_experiment` touches `["truth"]` and nothing else. See the Phase 2 audit for what
this side channel could have revealed.

**D3 — the E experiment holds out no moduli.** `tensor_experiment` calibrates on
`m in 1..m_test` (1417). The learned object is a dict of 48 independent per-modulus
sequence pairs. It cannot predict `m = 49` at all; extrapolation is exclusively along `r`
and `d`. Any statement of the form "the pipeline recovered λ(m)" must therefore read
"recovered, separately for each of 48 given moduli, a d-period that coincides with λ(m)" —
no cross-modulus law was learned, and the code's own provenance string says so
("axis extrapolation on calibrated moduli", 1445).

**D4 — symbol cost under-counts the deployed T decoder.** `model_cost` for `cycles` (373)
sums `sequence_cost` over `train_rows` (1..m_train) only, but `state["cycles"]` is later
extended to all 48 moduli by the two post-registration `calibrate` calls (857, 940), and
`predict` reads the live dict. So the "cycles" hypothesis is scored with a description
length ~half of what its deployed form needs. `tensor_cost` (1350) does not have this
problem: it sums over every row it will use.

**D5 — export is gated on post-final status.** The shortlist is frozen before final queries
(correct), but `if e["status"] == "UNREFUTED_ON_TESTED_DATA"` (997, 1517) is evaluated
*after* final evidence is attached. So "13 exported candidates" is a post-hoc filter, not a
pre-registered prediction count. The frozen forecast hashes, not the export count, are the
honest pre-registration record.

**D6 — `register` can return `None`; the caller stores it unconditionally.** Line 823
appends the result of `register` to `atom_entries` even though `register` returns `None` for
a duplicate model (804). `train_rank(None)` would raise. Atom models are pairwise distinct by
construction, so this never fires today — latent fragility, no current effect.

**D7 — transport's "final" split is not a holdout, and the code says so.** `unary`/binary
phases are labelled `train` vs `final` by coordinate size (1074, 1180), but every transport
datum is a cache hit from the T table experiment that already ran. `preregistration.json`
carries `transport_final_overlap` and each ledger entry carries `holdout_note`. Honest, but
it means the 12 exported TR candidates rest on no independent data whatsoever.

**D8 — the classification quoted for T in the task prompt is false at k = 1.** The prompt
states `T(m,k) ⟺ m squarefree ∧ L(m) | k−1` for `m,k ≥ 2`; the lab queries `k ≥ 1` and
`m ≥ 1`. At `k = 1` the predicate is true for every `m` while the formula demands
squarefreeness. Independently checked: 29 mismatches for `m < 80` at `k = 1`
(`audit/numbertheory.py`). Column `k = 1` is therefore a systematic "exception" in the
T grid that has nothing to do with the learner.

**D9 — the reported pretest command cannot have used the default budget.** At the reported
scale the E grid alone is `48 × 12 × 112 = 64 512` unique queries, above the default
`--budget 40000` (1682). The pretest must have passed a larger budget; the report does not
state the command. Recorded as a reproducibility gap.

**D10 — `--control B` exists and is untested by the report.** It skips E, U and the algorithm
audit entirely (1806). Nothing in the report exercises it.

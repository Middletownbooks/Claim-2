# SELECT v1 — the selection function, registered before any worker output was read

Part I below was written, committed and pushed **before** any of this run's workers were
dispatched; its commit is the registration. Part II ("as operationalised") is appended after the
runs and says which clauses survived contact. **Nothing in Part I is edited after dispatch** —
corrections go in Part II with the reason, so the registered version stays recoverable from git.

Built on `GAP_V3.md` §3 (gap types), `../playability/INTERESTINGNESS.md` §5 P1–P5, and the
handoff "HANDOFF_O55_DISCOVERY.md" in board-finder/. Predictions are in
`../../proof-protocol/ledger.json` as P-32 to P-36.

---

# Part I — registered

## 0. What changes from the handoff's formula, and why

The handoff states `Select(T) = I_irred(T|P) × w_class(T) × g(gap_type(T))`. Two of those three
factors can be evaluated on an open record problem and one cannot:

* **`I_irred` is undefined on open problems.** `V(T|P)` is lines of Lean for a proof that does not
  exist (`../playability/INTERESTINGNESS.md` §4), and this container has no Lean toolchain, so not
  even `V̂` is available. **SELECT v1 therefore drops the `I` factor for open records** and uses it
  only where a *statement* is generated (Arm 3), and even there only in P2's decomposition form,
  judged rather than measured.
* **`w_class` is a veto and `g` is a gate.** Neither is a weight: every clause below is
  pass/fail with a single threshold, because a product of judged factors is a number that cannot
  fall (lesson in `../../proof-protocol/ledger.json`, "a number that cannot fall is not a
  measurement").
* **No clause consumes a model-generated difficulty or feasibility estimate.** §5 of the handoff
  requires calibration before any such estimate gates a decision. The ground truth that would
  make that calibration well-posed — per-restart success rates and budgets for the b=0 orbit
  ladder — lives in FINDING 160/162 of the Cooperative-AI-Defense repository, which is not in this
  container. Only seven labelled rungs are here (`../playability/INTERESTINGNESS.md` §2) with no
  budget attached, so "P(solved)" is not defined against them. **The rule is enforced
  structurally instead: difficulty and headroom estimates are reported as ungated annotations,
  and every gate reads a literature fact or a computed quantity.**

## 1. The decomposition step the `II` class never had

The playability screen classifies **headlines**. A record problem's deliverable is a
**sub-problem** of its headline — "exhibit a configuration of 594 kissing spheres in dimension 11"
is existence-headed with a finite checkable YES branch, i.e. **P1**, while "determine τ₁₁" is
`II`. So before any gate, every record is decomposed:

```
headline  →  tracked quantity  →  its two sides (lower, upper)
          →  for each side, the BOUND OBJECT whose exhibition moves that side:
               WITNESS    a finitely describable object whose value is fixed by a terminating
                          computation, exact or rigorous-numeric
               PROOF      a new argument
               ALGORITHM  a finite string whose correctness is universally quantified
               NONE       nothing moves it (e.g. physics-numeric estimates of an exact constant)
```

## 2. The gates. Every one is pass/fail; a gate that cannot be evaluated is FAIL.

| gate | passes iff |
|---|---|
| **S0 OPEN** | the headline and the record are unresolved; withdrawn or unrefereed resolution claims are data, not resolutions |
| **S1 COUPLED** | at least one side's bound object is a WITNESS **and** exhibiting a better witness moves a published bound **on the headline quantity itself**, not on a finite analogue of it. Two routes count: (a) the headline quantity is an extremum (sup/inf/max/min) over finitely describable objects, or (b) a published bound on the headline was established by a finite certificate checked by terminating computation. An asymptotic-order headline is COUPLED only through a published lifting theorem that turns a finite object into an asymptotic bound (the cap-set product construction is the model case). |
| **S2 NOT VETOED** | the witness's defining predicate is decidable and its value is computable by terminating computation. **ALGORITHM → veto. Undecidable predicate (class W) → veto.** |
| **S3 IDEA GAP** | the **most recent** move of the coupled side has kind `ANALYTIC` or `SEARCH-NEW` (§3) |
| **S4 NOT CROWDED** | the coupled side has **not** moved on or after **2025-01-01** by an AI-driven search system or by large-scale optimisation tooling. A record an AI search just moved is evidence *for the category* and a kill *for that record* — `../fallbacks/QUEUE_V3.md`'s own reading of FunSearch, and the 282 lesson in `../fallbacks/RESULT_MAPPING_D.md` §5 |
| **S5 DELIVERABLE** | a named maintained table, or a named published bound, changes on a one-step improvement, and the abstract sentence can be written |

A record passing S0–S5 is a **triage survivor**, not a queue entry. It enters the queue only
with a **promoting bar written by the Opus instance** — the "first check that would kill it" —
so that no candidate reaches the queue without a bar written for it first (P-31 A-2).

## 3. Move kinds — the operational form of `GAP_V3.md` §3 and the handoff's §3.1

For each dated record move:

| kind | definition |
|---|---|
| `ANALYTIC` | the record object or bound was derived by hand — explicit formula, algebraic or combinatorial construction, proof. Computation, if any, only verified it. |
| `SEARCH-NEW` | produced by computer search or optimisation with a method the paper **introduces, or is the first to apply to this record** |
| `SEARCH-REPEAT` | produced by computer search or optimisation with a method **already used on this record** by earlier work: a bigger run, more restarts, refined parameters, more hardware |
| `UNKNOWN` | the sources available do not say |

`IDEA := ANALYTIC ∪ SEARCH-NEW`. `COMPUTE := SEARCH-REPEAT`. Flag `AI-SEARCH` additionally when
the move was made by an LLM- or RL-driven search system; the first such move on a record is
`SEARCH-NEW`, later ones by the same family of system are `SEARCH-REPEAT`.

**The gap type of a record is the kind of its single most recent move.** The handoff's §3.1 asks
about the last *two* moves; using two creates a mixed middle case with no verdict, which is D44's
failure. The second move is recorded and reported but not scored.

Why `SEARCH-NEW` is `IDEA` and not `COMPUTE`: `GAP_V3.md` §3's own worked algorithmic-idea gap,
Hadamard 2092, *is* a search method — a growth exponent 0.503 against ≈0.25. A new search method
is an algorithmic idea; the same method run bigger is compute.

## 4. The two coordinates, reported and never collapsed

* **`bits_search`** `= −log₂ ρ` is **defined only** where (i) a search space for the witness is
  fixed by a named ansatz and (ii) a density estimate exists — published, or computed here and
  checked against a positive control with a known count. Otherwise the cell reads **UNDEFINED**
  with the reason. It is never estimated by judgement.
* **`V_arg`** is **undefined for an open problem** (no proof exists to measure). What is reported
  in its place is the **verification class of one improvement step** — `CHECK` (exact finite
  computation), `RIGOROUS-NUMERIC`, or `PROOF` (a new argument needing refereeing) — labelled as a
  class, never as a number of lines.

## 5. Provenance, and the tier this environment forces

This container's egress admits a web-search tool and raw.githubusercontent.com and **blocks**
arxiv.org, Wikipedia, publishers, and every maintained-table host probed (Cohn, La Jolla,
Brouwer, Packomania). So a fourth tier is added for this run:

| tier | meaning | gate-usable? |
|---|---|---|
| `PRIMARY-VERIFIED-LOCALLY` | computed or checked in this container | yes |
| `SECONDARY-RELAYED` | the source text itself was read (possible here only for files on raw GitHub or in this repo) | yes, at triage |
| **`SEARCH-SUMMARY`** | seen only in a web-search result title or summary; the source was not read | **no — RECALL-grade for every gate** |
| `RECALL` | believed, no source found this session | no |

Every value also carries **EXACT / RIGOROUS-NUMERIC / NUMERICAL / UNKNOWN** and **REFEREED /
PREPRINT / ANNOUNCED / WITHDRAWN**. A breadth cell is triage-grade whatever its tier (lesson 24)
and may not be gated on without a promoting search.

Consequence, registered now: **in this environment almost every literature cell will be
`SEARCH-SUMMARY`, so no survivor of this run can be more than triage-grade.** Triage survivors
still enter the queue only via a promoting bar; they do not skip it because the screen was
strict.

## 6. Test G — scoring `g(gap_type)` against outcomes for the first time

`../playability/INTERESTINGNESS.md` §6: *"`g(gap_type)` has never been scored against outcomes."*
There is now a labelled outcome set readable from inside this container: the 67-problem
repository of Georgiev, Gómez-Serrano, Tao, Wagner, *Mathematical exploration and discovery at
scale* (arXiv:2511.02864), whose status grid records, per problem, whether AlphaEvolve beat the
literature. Snapshot: `discovery/aerp_status_grid_2026-09-29.png`, problems
`discovery/aerp_problems_2026-09-29.json`, outcome coding `discovery/aerp_outcomes.json`.

**Outcome coding (registered, mechanical, from the grid):** green or blue → `IMPROVED`; red or
light grey → `NOT-IMPROVED`; dark grey ("matched known optimal bound") → excluded, because a
closed problem has no gap to type. Derived: 23 improved, 32 not, 12 excluded.

**Predictor:** a worker, not told the hypothesis, labels the most recent **pre-2025** move on
the **construction side** of each problem (the side an exhibited object bounds) with §3's kinds.
Problems with no pre-2025 numeric record on that side are excluded (`NO-RECORD`), as are
`UNKNOWN`.

**Slices, named before dispatch — the D45 fix.**
* **ODD-numbered problems are the test slice.** Every registered statistic is scored there.
* **EVEN-numbered problems are reserved.** A separate worker labels them into a separate file,
  and its report to me is restricted to "done" and counts of `UNKNOWN`/`NO-RECORD`. **I do not
  read the EVEN labels until the ODD statistics are scored and any revision to §3's mapping is
  written into Part II and committed.** EVEN then scores the revision, or replicates the
  original if there is none.

**Statistics (single thresholds, no middle band):**
* **G-1, the handoff's §3.1 as operationalised here.** `Δ₁ = P(IMPROVED | IDEA) − P(IMPROVED |
  COMPUTE)`. **§3.1 is validated iff Δ₁ > 0.** If either class has fewer than 4 problems in the
  slice the statistic cannot be evaluated, and that counts as **not validated**.
* **G-2, my refinement, registered now so it cannot be fit later.** `Δ₂ = P(IMPROVED |
  SEARCH-NEW) − P(IMPROVED | ANALYTIC)`. **Validated iff Δ₂ > 0**; same n ≥ 4 rule.

Known weaknesses, stated in advance: the problem set was chosen by the authors for an
optimisation system, so it is search-shaped throughout and the test is *within* that population;
blinding is partial (a worker searching the literature will meet AlphaEvolve's results); the
outcome is one system's, over roughly six months; and ODD will hold on the order of 15–20
testable problems, so only a large effect is visible. Problem 11 is a known coding hazard: the
grid marks it red because an unpublished 2025 bound beats AlphaEvolve's, though AlphaEvolve beat
the published literature — the registered coding stands and a flipped-11 sensitivity line will
be reported beside it.

## 7. The three arms, their slices and their bars

| arm | population, fixed now | role |
|---|---|---|
| **1** | the 19 unexamined `II` records: 17, 186, 199, 246, 277, 288, 308, 351, 353, 368, 375, 385, 410, 413, 417, 428, 441, 450, 479 (221, 282, 337 decomposed for completeness, not counted) | answers §0: defect or correct rejection. **Not held out** — I read every headline before registering. |
| **2** | 15 maintained tables outside the corpus, one pre-specified record each (list below) | **the held-out slice for SELECT v1 as a generator** |
| **2b** | a directed search for §3.2 divergences across the same 15 topics and AI-era record tables | tests §3.2 as a *generative* signal |
| **3** | exactly 12 generated conjectures, one worker, then stop | bounded test of the paper's own route |

**Arm 2's fifteen tables and the record in each** (the queue's four are rows 1–4; PTE is
excluded, dead on arithmetic in `../pte/VERDICT_PTE11.md`):

1. kissing numbers, lower bounds in dimensions 11–14
2. caps in AG(n,3): largest known cap for n = 7, 8
3. snake-in-the-box: longest known snake in Q_n for n = 9, 10, 11
4. D-optimal designs: the smallest n ≡ 2 (mod 4) with the Ehlich–Wojtas bound attained by no
   known matrix (movement history only — the promoting search is the Sonnet S55 run's)
5. skew-Hadamard: the smallest order 4k with no known skew-Hadamard matrix
6. Williamson matrices: the smallest odd order whose existence is open
7. Steiner systems: the smallest open admissible case in the most recent table found
8. cyclic difference sets: the smallest open (v, k, λ) in the most recent table found
9. Costas arrays: the smallest n with no known Costas array
10. bent functions: the smallest number of variables whose bent-function count is unknown
11. APN functions: an APN permutation in dimension 8 (and the known-class count in dimension 8)
12. perfect 1-factorisations: the smallest n with K_n's existence open
13. binary covering codes, radius 1: the smallest n with K(n,1) not known exactly
14. Moore graphs: degree 57, diameter 2
15. strongly regular graphs: the smallest open feasible parameter set in Brouwer's table

A table survives if its specified record passes S0–S5.

**§3.2 divergence (Arm 2b), registered definition:** two dated, published methods on **the same
object**, whose reach differs by a **factor ≥ 2 in the frontier parameter itself** (order,
dimension, length — not in runtime), both at `SECONDARY-RELAYED` or better. `SEARCH-SUMMARY`
divergences are reported as leads, never counted. Hadamard 2092 is excluded (already held).

**Arm 3 bar:** exactly 12 conjectures in the neighbourhood of this project's tooling (±1
matrices, periodic autocorrelation, orbit structure, designs), each with a finite witness side.
Each gets P2's decomposition — split at top-level `∧` and `↔`; **bolted** iff some part is
trivial (judged, since no Lean is available: true by definition, by a one-line argument, or by
a finite check under 10 cases) and the remaining part is itself a standalone statement — then a
novelty search, then SELECT v1 in full. **Arm 3 PASSES iff at least 1 of 12 survives S0–S5.**
Stop at 12 whatever happens.

## 8. Registered predictions (mirrored in the ledger)

| id | prediction | single threshold | my credence |
|---|---|---|---|
| **P-32a** | the `II` exclusion is an instrument **defect**: ≥ 4 of the 19 are COUPLED and NOT VETOED | ≥ 4 → defect; ≤ 3 → correct rejection in effect | 0.65 |
| **P-32b** | …but a correct rejection **in yield**: ≤ 1 of the 19 survives S0–S5 | ≥ 2 falsifies | 0.7 |
| **P-33 G-1** | §3.1 is **not** validated on the ODD slice: Δ₁ ≤ 0 or unevaluable | Δ₁ > 0 falsifies | 0.6 |
| **P-33 G-2** | Δ₂ > 0 on the ODD slice: new *search* methods, not hand constructions, mark what moved | Δ₂ ≤ 0 or unevaluable falsifies | 0.6 |
| **P-34** | Arm 2 yields between 1 and 4 triage survivors of 15 | 0 → SELECT v1 fails as a generator on its held-out slice; ≥ 5 → it is too loose to be a gate | 0.55 |
| **P-35** | the directed search finds ≥ 1 §3.2 divergence meeting the registered definition | 0 → §3.2 does not generate | 0.5 |
| **P-36** | Arm 3 fails: 0 of 12 survive, because a freshly generated statement has no movement history, so S3 cannot be evaluated | ≥ 1 survivor falsifies | 0.9 |

Why 4 is the P-32a threshold: 35 of 499 corpus records are playable, 7.0%; 19 × 7.0% ≈ 1.3.
Four coupled-and-unvetoed records is three times the corpus base rate, which is the point at which
excluding the class discarded a richer-than-average seam.

Why P-36 is registered at all when it is predicted by argument: *ruling a thing out by argument
rather than by test is a failure mode this project has repeatedly paid for*. The argument has a
named hole — a generator can rediscover an existing record that *does* have a history — and the
test measures how often it does.

Measurements with no threshold, stated as measurements rather than predictions (D44's third
option): Arm 3's bolted count and rediscovered count; the fraction of all cells in this run that
are `SEARCH-SUMMARY`.

## 9. What P-31 is scored on in this run

Every worker verdict I receive is adjudicated against its bar. **One verdict issued on a bar the
worker could not actually evaluate makes P-31 A-1 FALSE**, and I will record it whichever way it
cuts. Workers are told, in their prompts, that "I could not evaluate this bar" is the required
answer when it is true. A-2 is protected by §2's last paragraph.

---

# Part II — as operationalised

*Appended after the runs, 2026-09-29. Part I above is byte-identical to commit fab89d8 (checked by diff);
no line of it was edited. Results: `RESULT_DISCOVERY.md`.*

## II.1 What the run actually was

The run was interrupted twice. At ~14:05 UTC the account's spend limit stopped all nine workers.
After it reset, concurrency was capped at three at the user's request, and the session-wide
web-search budget (200 calls) ran out part-way through. It completed:
* Test G ODD;
* Arm 1, with 9 of 19 records only partly evaluated;
* Arm 2, tables 1–5 and 11–15.

It left unrun:
* Arm 2 tables 7–10;
* Arm 2b, the divergence search;
* Arm 3 beyond generation;
* Test G EVEN, which is still unread.

Every statement below is scoped to that.

## II.2 Clause by clause

| clause | status after contact |
|---|---|
| **§1 decomposition** | **Survives, and is the main result.** `II` = P1 ∧ U for extremal headlines. It turns the handoff's "contradiction" into a missing step (`RESULT_ARM1_II.md` §1). |
| **S0 open** | Survives. It was live three times: 308, 368 and 385 all moved in Aug–Sep 2026. |
| **S1 coupled** | Survives. It separated extremal from asymptotic headlines cleanly. One refinement is needed: **a coupled side can stop being the side that moves.** 308's 2026 lower bound came from an asymptotic argument, not from a witness. |
| **S2 veto** | Survives. It fired as designed on 410, where a universal polynomial is an ALGORITHM. |
| **S3 idea gap (§3.1)** | **Does not survive as a discriminator.** Test G: the COMPUTE class is empty (0 of 10 testable problems; 0 of 4 S3 calls in Arm 2a). In practice S3 measured whether a move kind is *knowable*, and killed records on UNKNOWN rather than on gap type. The likely cause is structural: record papers must claim novelty, so the literature never labels a move "the same method, run bigger". |
| **S4 crowding** | **Survives, but scoped wrongly.** It did the most real work: it killed 308, kissing dimension 11 and cap-set capacity. Registered per record, it passed kissing dimensions 13 and 14 inside a table that three AI systems moved within twelve months. It should be scoped per table. Not applied retroactively. |
| **S5 deliverable** | Survives. It was never the binding gate. |
| **§3.2 divergence** | **Untested.** The generative search did not run to completion (P-35 open). |
| **§4 coordinates** | `bits_search` was UNDEFINED for every candidate: no named ansatz with a published density estimate exists for any of them. The verification class was reported in place of `V_arg`. The pair was never collapsed. |
| **§5 tiers** | **Internal inconsistency found in my own registration.** It calls `SEARCH-SUMMARY` RECALL-grade "for every gate" and also lets "triage survivors" exist. Strictly read, Arm 2 returns 0 survivors. P-34 was scored on the looser reading its own text names, with the strict count reported beside it. |

## II.3 Corrections made during the run (none to Part I's text)

* The AlphaEvolve problem snapshot committed with the registration had **7 truncated statements**,
  because the extraction stripped anything between `<` and `>`. It was fixed before any worker ran;
  the outcome labels were unaffected (commit 282b6b9).
* **Blinding:** the Test G ODD worker glimpsed `discovery/aerp_outcomes.json`. Future briefs must
  keep outcome files out of the worker's tree.

## II.4 What v2 should change, registered here as proposals, not applied

1. **Replace S3.** Movement history cannot supply the COMPUTE label. Use a direct question instead:
   *has a general-purpose AI search system been pointed at this record and failed to move it?*
   That is outcome evidence, not a label. Its sign is ambiguous: failure says either "hard" or
   "not search-shaped". So it needs its own Test G-style scoring before it gates anything.
2. **Scope S4 to the table.**
3. **Make `SEARCH-SUMMARY` explicitly triage-only in one place**, and have the scorer compute both
   counts.
4. **Keep §1's decomposition** as a standing step in `../playability/classify.py`'s `II` handling.
   Record the extremal/asymptotic split per record, so the class stops being a bin.

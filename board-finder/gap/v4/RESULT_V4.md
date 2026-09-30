# Gap analysis v4 — result. The bar FAILS, and the grade is the finding

Run 30 Sep 2026 against Part A only of `PROMPT_GAP_v4.md`, by an Opus 5.5 chat instance with
search. **22 of ~25–30 calls used, stopped on context.** Response tier `SECONDARY-RELAYED`: this
session fetched none of its sources. **Every arithmetic claim in it has been re-derived locally and
all of them hold** — `verify_run_v4.py`, 26 assertions passing.

## 1. The verdict, and the grade matters more than the verdict

**Bar: FAIL.** `PROMPT_GAP_v4.md` Part B registered it before dispatch: *at least one candidate
clears all five kills with R ∈ {ALGORITHM, THEORY} at PRIMARY tier.* **Zero cleared.**

**Graded per `D54`: `FAIL-UNEARNED`, not `FAIL-ESTABLISHED`.** Four candidates cleared **Q** (a
tracked integer with two sides) and **N** = 5 (a nameable finite unknown set) with **W** = 5 (exact,
one-directional checking). All four then stopped at **R**, because the run could not read a frontier
paper's method section at PRIMARY tier. The run states the consequence itself and states it
correctly:

> *"The binding gap is method-section access (R). The evidence did not show the space is empty."*

**So the null is about the instrument, not the population** — and that is a fourth diagnosis of a
null on this board, distinct from the three already on file:

| diagnosis | where | what it blames |
|---|---|---|
| gate design | `../SELECT_v1.md` §9 | the thresholds |
| corpus coverage | `../RESULT_RETRODICTION_P40.md` §2b | the population being screened |
| scoring vocabulary | `LEDGER` lesson 39 | what counts as success |
| **evidence access at the deciding gate** | **this run** | **the tier a gate demands, against the environment it runs in** |

### And the design error is mine

Step 4 requires the remedy label at **PRIMARY tier from a method section, or the candidate is not
scored.** That rule is right — it exists because move-kind inference measured 0 of 10. But I paired
it with a chat environment whose page fetches return oversized or robots-blocked, which makes the
rule **correctly strict and, in that environment, unpassable.** I built a gate that cannot be
cleared from where I sent it.

The run supplies the fix, in its own methodology note:

> *"extract arXiv method text with targeted `web_search` queries, which return bounded excerpts,
> rather than fetching pages."*

Three fetches — the formal-conjectures stats page, the GitHub README, the Epoch problem page — "used
most of the context", while the token cap the run set never bound. **`D55` for the third time, and
the first time with a remedy rather than an observation.**

## 2. P-42, scored

Registered before dispatch and deliberately kept out of the prompt artefact: *zero candidates clear
all five kills, and the modal kill is **Q** rather than N or H.*

| clause | outcome |
|---|---|
| zero candidates clear all five kills | **CORRECT** |
| modal kill is Q | **CORRECT** on the run's own attribution — NO-QUANTITY 10 plus one-sided-quantity 20, both recorded by the run as Q failures, against **0** killed primarily at N and **0** reaching H at all |

**Scored CORRECT, with two things said against it.**

**(i) The threshold nearly failed to fire, for the third time.** I wrote *"the modal kill is **Q**
(NO-QUANTITY)"*, and the parenthetical names a label that alone scores **10** against the one-sided
category's **20**. Had the run filed those twenty under N instead of Q — and it notes *"most of
these are also N = 1 unbounded tails"*, so it could have — N would have been modal and the same
evidence would have scored the prediction wrong. **The clause is scored on the run's attribution
and not redrawn** (`D44`), but a parenthetical that can flip a verdict is the same defect as an
unregistered middle band, and this is its third appearance.

**(ii) It is correct and nearly irrelevant**, which is `P-37`'s shape exactly. Both clauses are
about where the *population* thins. The fact that decided the run — that its four survivors all died
at R for want of access — appears in neither clause. **A prediction can be right about the shape of
a null and silent about its cause.**

## 3. What the run established, re-derived here

All of the following re-derives from the stated definitions in `verify_run_v4.py`.
`PRIMARY-VERIFIED-LOCALLY` for the arithmetic; the literature values behind it stay `RELAYED`.

**Hill's conjecture at n = 13.** *H*(13) = 225 and *H*(12) = 150. A crossing uses four vertices, so
9·cr(*D*) = Σᵥ cr(*D*−*v*) at *n* = 13, and min over *v* is at most ⌊9c/13⌋. The ladder:

| cr(*D*) | forces a K₁₂ subdrawing at most | above the K₁₂ optimum |
|---:|---:|---:|
| 217 | 150 | **0 — exactly optimal** |
| 219 | 151 | 1 |
| 221 | 153 | 3 |
| 223 | 154 | 4 |

**All four thresholds check.** The run's observation that McQuillan–Pan–Richter's §1 concerns
*"drawings of K12 having 151 crossings"* places published work exactly at the 219 rung. **That is
evidence the frontier is enumeration depth rather than missing theory** — which under `D61`'s
five-way scale reads ALGORITHM or FLOPS, and FLOPS is a kill. The run says so and declines to
decide without the method section. Correct.

**Zarankiewicz.** *Z*(7,11) = 225, *Z*(9,9) = 256, *Z*(7,10) = 180, *Z*(8,9) = 192, all confirmed.
A crossing uses two vertices per side, so (*n*−2)·cr(*D*) = Σᵥ cr(*D*−*v*): ⌈11·180/9⌉ = **220**,
and Kleitman parity with both sides odd gives cr(K₇,₁₁) ∈ **{221, 223, 225}**; ⌈9·192/7⌉ = **247**,
and parity gives cr(K₉,₉) ∈ **{248, …, 256}** even. The falsification line also checks: a
223-drawing forces a K₇,₁₀ subdrawing at ⌊223·9/11⌋ = **182**, exactly **2** above optimal.

**Skew-Hadamard at the smallest open order 356 = 4·89.** |ℤ₈₉*| = 88 = 8·11; the odd divisors of 88
are exactly {1, 11}, so the only nontrivial odd-order subgroup has order 11 and −1 (order 2) is not
in it; 88/11 = 8 cosets in 4 ± pairs; the *H*-invariant skew block has 2⁴ = 16 choices and each
other block 2⁹ = 512 from 8 orbits plus {0}; total **16 · 512³ = 2,147,483,648 ≈ 2.1×10⁹** before
filtering. **All of it holds.** The run's conclusion is the right one and it is the PTE-rings
conclusion again: *the cheap region is trivially searchable, so it has probably been searched and
found empty*, which would be **P** — evidence against the object where we can reach — and P is a
kill. It flags this `UNSETTLED` rather than asserting it. That is the discipline working.

## 4. Six corrections to my brief, and three are to numbers I derived

The *"report anything that contradicts this prompt"* clause fired harder than any verdict in the
document, as it did for briefs D and E.

**(i) The Qiushi Engine — and this one reaches back into a closed gate.** The run:
*"I found no mathematics target board… an optics/physics autonomous-discovery system at Zhejiang
University"*, citing arXiv:2604.27092, and marks the brief's claim UNVERIFIED. **But
`../discovery/RESULT_GATE_C1.md` rests on a Qiushi Engine paper at arXiv:2609.35051 reporting
nineteen new kissing-number lower bounds at dimensions 25, 27, 32–39, 43, 45, 49–55**, supplied by
the operator as a transcript. **Different arXiv identifiers, so plausibly two different systems, or
one re-scoped.** Neither side is PRIMARY here — ours is `SECONDARY-RELAYED` from a transcript,
the run's is `SEARCH-SUMMARY` and not gate-usable. **Recorded as unresolved, and it is not neutral:
gate C-1's FAIL used Qiushi as one of two systems demonstrating industrial-rate sweeping.** If that
paper is not what we took it for, C-1's *reasoning* weakens even though its verdict rested on
EinsteinArena as well. Registered as `D63`.

**(ii) Hadamard order 668 marked solved on FM:OP, 2026-08-12, provisionally** — *"We have marked
the Hadamard matrix of order 668 problem as solved by AI."* Our tree records 668 among **Alpöge's
twelve**, a human result. Either the attribution or the date collides. Adjacent to the primary
thread, so it matters; unresolved here.

**(iii) Kissing number *d* = 11 raised from 593 to 604 by EinsteinArena.** This **corroborates**
gate C-1's finding that EinsteinArena's kissing entry is dimension 11 only — and shows it moved.

**(iv) Seymour's second neighbourhood, δ⁺ = 8: dead on polarity, not on cost.** δ⁺ = 7 is confirmed
(arXiv:2606.30588, *"eliminated by reproducible OR-Tools CP-SAT infeasibility checks"*), and
**advancing to δ⁺ = 8 is a NON-EXISTENCE task, which Step 2 excludes.** Cycle 0's shortlist ranked
this candidate **A**, for *"the constraint is unambiguously compute-shaped… exactly the Claude Code
delta"*. Under v4 it never reaches a dimension: the witness polarity is wrong. **A Cycle 0
front-runner killed by a step Cycle 0 did not have.**

**(v) Kalai 3^d — my own prior art was incomplete.** `../REVIEW_JULY_GAP_ANALYSIS.md` §1 verified
that the cube attains 3^d exactly. The run: **equality is attained by *all Hanner polytopes***, and
the stronger conjectures B and C fail for *d* ≥ 5 — so refuting the stronger siblings was the easier
task and is weak evidence for A. **That is the precedent-direction clause catching a gap in the
document that introduced the precedent-direction clause.**

**(vi) Three challenges to counts I derived from the formal-conjectures clone. Re-checked, and the
score is one hit.**

| the run's challenge | re-checked here |
|---|---|
| *"the site shows 2,200 solved, not 2,202"* | **both right.** The repository at `7d450ef` gives **2,202**; the site shows 2,200. The run's own inference — *"the site may lag the repository"* — is the correct resolution |
| *"'Arxiv holds 37 open statements' may confuse a file count with an open-statement count"* | **sound suspicion, wrong cause.** 37 open statements distributed across 37 files as 12 files with none, 18 with one, 4 with two, 2 with three, 1 with five — summing to 37. **A genuine coincidence**, and one command settled it |
| *"the site's per-collection file counts sum to exactly 1,403"* | **a real imprecision of mine.** My brief said *"1,662 Lean files"*; that is the **repo-wide** count including the mathlib-support, test and util directories. **`FormalConjectures/` itself holds 1,416.** The conjecture collection is 1,416 files carrying 1,403 open and 2,202 solved statements |

## 5. Four new candidates, and one of them is the register's missing cell

Nothing passed, so these are pool entries. But three of the four were **not in this programme's
corpus at all**, and the fourth is the one the register singled out.

| # | candidate | the tracked quantity | why it is here |
|---|---|---|---|
| 1 | **Hill's conjecture, cr(K₁₃)** | **{223, 225}** — a single open value below the conjectured 225 | N = 5 on one number. Its falsification ladder is computed and points at enumeration depth |
| 2 | **Zarankiewicz, cr(K₇,₁₁) and cr(K₉,₉)** | **{221,223,225}** and **{248,…,256}** | **This is Cycle 0's decisive missing cell** — see below |
| 3 | **Skew-Hadamard** | **41 open orders ≤ 1208**, smallest 356 = 4·89 | a nameable finite list, next door to machinery this project already has |
| 4 | **Hirsch ladder** | ***m\**** = min(*n*−*d*) over non-Hirsch polytopes ∈ **[7, 19]** | both bounds on finite certificates; likely dies at P or CONTEST |

**On #2, and it closes a gap the register said only the operator could close.**
`../register/REGISTER.md` §7 records Zarankiewicz/Hill as the one Part D cell still decisive:
Cycle 0 said *"the register must establish whether it stalled on compute or on the cyclic-order
realizability theory. If theory, Claude Code adds little and this is dead"*, and the register could
not reach it because it needs a transcript. **The run promoted the same target to the top of its pool
and produced a concrete discriminating test for exactly that question**: whether Woodall's
cyclic-order-graph relaxation can reach 225 at *n* = 11 *in principle* — if it cannot, R = THEORY.
**That is an instrument answering, from the literature, a question the register could only ask of a
lost transcript.** It does not settle it, but it converts "ask the operator" into "read one 1993
paper's method section".

**And #3 is a Hadamard-family target we did not have.** The register's A4 and A5 are both Hadamard
rows that died; this is a different object with a finite open list, and the run's own arithmetic
shows the cheap region is searchable — which makes it *decidable* cheaply, in either direction.

## 6. What this says about v4

**The instrument worked in three places and failed in one, and the failure is at the gate I made
decisive.**

* **Step 0's "search for others" clause** had already justified itself by returning
  formal-conjectures. This run added AlphaProof Nexus (353 open Erdős problems, 492 OEIS
  conjectures), a Gemini sweep of 700 open Erdős problems, and an AlphaEvolve problem repository —
  **three more agent-facing enumerations, none of which this programme knew about.** `D62`'s tracked
  quantity should count these.
* **Step 3's re-parameterisation** did its job: it produced a tracked quantity for four candidates,
  including two crossing-number targets the earlier rubric had left undecided, and it converted
  ten candidates into an explicit **NO-QUANTITY** list instead of dropping them silently.
* **Step 2's polarity exclusion** killed a Cycle 0 front-runner outright — a real result about the
  prior list, obtained for free.
* **Step 4 is unpassable as posed**, in a chat environment. That is the one thing to fix before this
  prompt is run again.

**What it does not license.** The bar failed `UNEARNED`, so **nothing here says the off-list
named-conjecture space is exhausted.** The v2 run's fallback reasoning — that the off-list space is
being enumerated faster than a triage can survey it — is now better supported by `D62` than by this
run, which never got far enough to test it.

## 7. Next, in cost order

1. **Fix Step 4's access rule** — method text via targeted search for bounded excerpts, not page
   fetches, with a stated fallback tier if that also fails. One edit, and it is the difference
   between a bar that can fail and one that cannot pass. Then re-run.
2. **Read Woodall 1993's method section.** One paper, and it answers the question Cycle 0 named as
   deciding the Zarankiewicz candidate and that the register could not reach.
3. **Resolve the Qiushi collision** (`D63`) — it touches a closed gate's reasoning.
4. **Settle P for skew-Hadamard** by obtaining Đoković's searched orbit structures. The arithmetic
   here says the cheap region is 2.1×10⁹ before filtering, so "has it been swept" is the whole
   question.

*Arithmetic: `verify_run_v4.py`, 26 assertions, all passing. Prediction: `P-42`, scored above.
Bar: `PROMPT_GAP_v4.md` Part B, FAIL-UNEARNED.*

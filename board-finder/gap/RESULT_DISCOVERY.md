# Discovery run — findings, and the candidates that survived

Handoff: "HANDOFF_O55_DISCOVERY.md" in board-finder/. Selection function and registration:
`SELECT_v1.md` (Part I registered in fab89d8 before dispatch; Part II after). Per-arm results:
`RESULT_ARM1_II.md`, `RESULT_ARM2_TABLES.md`, `RESULT_TEST_G.md`, `RESULT_ARM3_CONJECTURES.md`.
Raw worker output and briefs: `discovery/`.

**Scope.** The run was cut down twice: by the spend limit at 14:05 UTC, then by a three-worker
concurrency cap and an exhausted shared search budget. Sources were search summaries plus raw
GitHub; every table host and arxiv.org were blocked. **Everything below is triage-grade.**

## 1. The findings, in order of weight

**1. The §0 contradiction is not a contradiction. It is a missing decomposition step.** For an
extremal headline, "determine the value" = **∃ (P1) ∧ ∀ (U)**. The screen rejected the
conjunction; the queue plays only the P1 conjunct. The same holds for all four queue items. The
`II` class is also mis-populated: 17 (BQP vs NP) is a truth-value question, not a record.
(`RESULT_ARM1_II.md` §1)

**2. The exclusion was a correct rejection in yield: 0 of 19 survive.** 2 of 19 are coupled and
unvetoed (308 Grothendieck, 368 Thomson), under P-32a's threshold of 4, and 9 of the 19 were only
partly evaluated. 308 was moved in August 2026 by a human–AI team, which fixed its tenths digit at
7. **Three of the 19 moved in Aug–Sep 2026** (308, 368, 385). The `II` class is where AI-assisted
work is landing now.

**3. `g(gap_type)` via movement history cannot discriminate: the COMPUTE class is empty.** This is
the first outcome-scored test of it (Test G, on the AlphaEvolve 67-problem set). 0 of 10 testable
problems, and effectively 0 cells in the arms, were ever labelled "the same method run bigger".
The literature does not describe record moves that way, because a paper has to claim novelty. In
practice §3.1 measured whether the move kind is *knowable*. (`RESULT_TEST_G.md`)

**4. Crowding, not gap type, did the killing.** S4 killed 308, kissing dimension 11 and cap-set
capacity. Registered per record, it let through two kissing cells inside a table that three AI
systems moved within a year. Scoped per table, as it should be, Arm 2 returns **0**.

**5. §3.2 as a generator is untested.** The divergence search did not run to completion (P-35
open). No candidate carries a measured idea gap.

## 2. Candidates — three triage survivors, none with a measured idea gap

Each has a promoting bar written here, by the adjudicating instance, before it enters the queue
(P-31 A-2). Single threshold; a bar that cannot be evaluated is FAIL.

### C-1. Kissing number, dimension 13: τ₁₃ ≥ 1154

| field | value |
|---|---|
| pair | **bits_search UNDEFINED** — no named ansatz with a density estimate exists for this cell. **V_arg class: RIGOROUS-NUMERIC**: search summaries call the 1154 configuration non-rational, so a successor may need interval verification, not exact arithmetic |
| gap type | IDEA (ANALYTIC). The last move was Zinoviev–Ericson 1999, a code-concatenation construction, and nothing has moved since. Evidence: a survey summary (SEARCH-SUMMARY) |
| w_class veto | not vetoed. A finite point set; the angle check terminates |
| table / sentence | Cohn's kissing table, row 13. *"We construct a kissing configuration of 1155 points in R¹³, the first improvement since 1999."* |
| the fact that makes it interesting | **AI systems active on this exact table since 2025 moved dimensions 11 and 12 and did not move 13.** PackingStar's best was a rational 1146 |
| **first check that kills it** | Read Cohn's table (dated ≥ June 2026) and the method sections of arXiv:2606.10402 (EinsteinArena) and arXiv:2609.35051. **PASS iff 1154 still stands at primary tier AND at least one of those systems reports having attempted dimension 13.** An unattempted cell is only unvisited, and the next run of theirs will visit it. FAIL otherwise. |

### C-2. Kissing number, dimension 14: τ₁₄ ≥ 1932

| field | value |
|---|---|
| pair | bits_search UNDEFINED. V_arg class: CHECK or RIGOROUS-NUMERIC — the exactness of the orbit configuration was not seen |
| gap type | IDEA (SEARCH-NEW). Ganzhinov, arXiv:2207.08266 (2022): a symmetry-restricted search over highly symmetric line systems (SEARCH-SUMMARY of the Aalto release) |
| veto | not vetoed |
| table / sentence | Cohn's table, row 14. *"We construct a kissing configuration of 1933 points in R¹⁴."* |
| **first check that kills it** | The same primary read as C-1, plus: **FAIL if any 2026 system reports ≥ 1933, or if Ganzhinov's symmetry-restricted method is reported as having been re-run by its author at larger group orders.** The second case would make the next step a SEARCH-REPEAT, which is the compute gap. |

### C-3. Caps in AG(8,3): 512

| field | value |
|---|---|
| pair | bits_search UNDEFINED. V_arg class: **CHECK** — verified locally by an all-pairs check (PRIMARY-VERIFIED-LOCALLY) |
| gap type | IDEA (SEARCH-NEW + AI-SEARCH): FunSearch, Dec 2023 |
| veto | not vetoed |
| table / sentence | Edel's cap tables, n = 8. *"A cap of size 513 in AG(8,3)."* |
| **first check that kills it** | **FAIL if any AI search system published after 2023 (AlphaEvolve, X-evolve, others) reports attempting AG(8,3) caps directly.** X-evolve moved the adjacent capacity record in 2025, so the neighbourhood is already worked by the systems this project would be imitating. This is the weakest of the three, and it is the flagship instance `../fallbacks/QUEUE_V3.md` already called taken. |

**Ranking:** C-1 > C-2 > C-3, on one criterion only: how strong the evidence is that AI search has
already been pointed at the cell. No scalar was used.

**The honest reading.** None of the three is the kind of candidate §9 of the handoff asked for —
"one candidate with a measured idea gap". All three are record cells in a table that capability is
already moving, and they survived a per-record crowding gate that this run showed is scoped too
narrowly. **The clean result of this run is negative, and it is about the instruments.** §3.1
cannot see compute gaps in the literature, and crowding is the operative gate.

## 3. The previous queue

**The Sonnet S55 results are absent.** "RESULT_S55_A_TABLE.md", "RESULT_S55_B_239.md" and
"RESULT_S55_C_345.md" are not under board-finder/fallbacks/ on
`claude/theorem-discovery-lab-jpbph1` as fetched at the end of this run. The fate of U13 D1, 239
and 345 is therefore unknown, and this document does not assume it. This run's Arm 2 has one
datum on U13, which is not a gate: a 2021 survey summary puts the smallest open D-optimal order
at 198.

## 4. §5 calibration

**Not run, and no gate needed it.** The ground truth that would make the b=0 ladder a well-posed
calibration set — per-restart success rates and budgets — lives in the Cooperative-AI-Defense
repository, not here. Seven labelled rungs with no budget attached do not define "P(solved)". The
requirement was met structurally instead: **no gate in this run consumed a model-generated
difficulty estimate** (`SELECT_v1.md` §0).

## 5. P-31, scored on this run's evidence

* **A-1 (the cheap tier does not issue verdicts on bars it could not evaluate): not falsified.**
  Five workers finished. Across them every unevaluable cell was returned as CANNOT EVALUATE,
  including whole blocks once the search budget was gone. Every PASS resting on thin evidence was
  flagged by the worker itself: 375's "mechanical, vacuous" S3, APN's degenerate S1, and 186's
  "from an abstract only". Two workers also corrected numbers in their own briefs:
  * skew-Hadamard's smallest open order is 356, not 276;
  * the Boyer–Li dating is June 2025, not Nov 2024.

  This is additional evidence; P-31's registered threshold is about the S55 run, which has not
  reported.
* **A-2: not falsified.** No candidate entered the queue without a bar written here first.

## 6. Resumable work, in priority order

1. Arm 2 tables 7–10 and the divergence search (P-35), once sources are readable.
2. Arm 1: 413, 428, 441, 479 — the records most likely to be coupled.
3. Test G EVEN (reserved, unread), with paper text rather than search summaries.
4. Arm 3 steps 2–4 for C1–C12 (P-36).

Every brief is in `discovery/prompts/` and can be re-dispatched unchanged, at most three at a time.

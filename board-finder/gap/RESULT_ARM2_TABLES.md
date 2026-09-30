# Arm 2 — fifteen record tables outside the corpus: two triage survivors, and why they are fragile

Held-out slice for SELECT v1 as a generator (`SELECT_v1.md` §7, registered before dispatch). Raw
worker output is in `discovery/A2_a.md` (tables 1–5), `discovery/A2_b.md` (tables 6–10) and
`discovery/A2_c.md` (tables 11–15). Almost every cell is `SEARCH-SUMMARY`, because every
maintained-table host was blocked. Two sets of local checks were run by the workers
(PRIMARY-VERIFIED-LOCALLY):
* FunSearch's 512-cap in AG(8,3), verified by an independent all-pairs check, and both cap-set
  capacity figures recomputed (2.2202337 and 2.2203085);
* the perfect-1-factorisation open list up to 100, and a port of Sage's SRG feasibility test.

## 1. Outcome by table

| # | table / record | current value (tier) | verdict | decided by |
|---:|---|---|---|---|
| 1 | kissing, dim 11 | 604, EinsteinArena agents, Apr 2026 (SS) | FAIL | S4: moved twice by AI since 2025 (AlphaEvolve 593, then 594→604) |
|   | kissing, dim 12 | 841, Jun 2026 preprint, numerical (SS) | FAIL | S3/S4 CE |
|   | **kissing, dim 13** | **1154, Zinoviev–Ericson 1999 (SS)** | **triage PASS** | last move ANALYTIC (code concatenation); PackingStar (RL, Nov 2025) reached only a rational 1146 |
|   | **kissing, dim 14** | **1932, Ganzhinov 2022 (SS)** | **triage PASS** | last move SEARCH-NEW (symmetry-restricted search); 2025 is only the journal date |
| 2 | caps, AG(7,3) | 236 (SS) | FAIL | S3 CE |
|   | **caps, AG(8,3)** | **512, FunSearch Dec 2023 — verified locally** | **triage PASS** | SEARCH-NEW + AI-SEARCH, before the 2025 cutoff |
|   | cap-set capacity | 2.2203085, X-evolve 2025 — recomputed locally | FAIL | S4: AI-moved in 2025 |
| 3 | snake-in-the-box, n = 9–11 | 191 / 379 / 746, arXiv:2607.15270, Jul 2026 (SS) | FAIL | S3/S4 CE: method unreadable |
| 4 | D-optimal, smallest open order | 198, from a 2021 survey summary (SS) | FAIL | S3/S4 CE |
| 5 | skew-Hadamard, smallest open order | **356** (SS), not the 276 the older literature gives | FAIL | S3 CE |
| 6 | Williamson, smallest open odd order | 65 | **FAIL at S0** | **ASSESSED 30 Sep** by `discovery/RESULT_B1_DESIGNS.md`: "orders below 65 settled" is SECONDARY-RELAYED but "65 is open" is SEARCH-SUMMARY only, and the sentence saying so exists only in a paper version that could not be re-opened |
| 7 | Steiner, smallest open admissible case | S(2,6,51) | **FAIL at S3** | **ASSESSED 30 Sep**: move kind UNKNOWN, 2001 method section not opened. Seven other cells moved Nov 2025–2026 by human computer searches — S4-table is reading-dependent |
| 8 | cyclic difference sets | (1561,105,7) by *k* | **FAIL at S3** | **ASSESSED 30 Sep**: move kind UNKNOWN; and the maintainer's 2003 and 2026 papers cannot be reconciled — (419,133,42) is open in one and absent from the other |
| 9 | Costas arrays, smallest *n* with no known array | **32** (not 29 — the enumeration frontier is a different quantity) | **FAIL at S3** | **ASSESSED 30 Sep** by `discovery/RESULT_B2_SEQUENCES.md`: S1 PASSES as an existence frontier; method section never opened, so move kind UNKNOWN |
| 10 | bent functions, smallest variable count unknown | **10** (even *n* only) | **FAIL at S1** | **ASSESSED 30 Sep**: a count frontier — exhibiting one more bent function moves nothing, and route (b) fails because a cardinality has no better witness |
| 11 | APN permutation, dim 8 | open; ≥ 3,808,491 quadratic APN classes known (2025) | FAIL | S1 degenerate: the only possible move is the resolution itself, so S3 cannot be evaluated |
| 12 | perfect 1-factorisation | K₆₄ open; frontier went 52 → 56 → 64 | FAIL | S3: SEARCH-REPEAT per one search-summary sentence — not gate-grade, and fails either way |
| 13 | covering codes K(n,1) | n = 10 (RECALL) | FAIL | CE |
| 14 | Moore graph (57,2) | open (RECALL) | FAIL | CE |
| 15 | smallest open SRG | (65,32,15,16)? (RECALL) | FAIL | CE; the feasibility screen does not establish openness |

**Triage survivors: 2 tables of 15** — table 1 (through dimensions 13 and 14) and table 2 (through
AG(8,3)). Derived from the rows marked triage PASS.

## 2. Scored

**P-34 (1 to 4 triage survivors): CORRECT on the registered reading — 2.** It needs two caveats,
and the second is a defect in my own registration.

1. **Four tables (7–10) were never assessed** and count as FAIL. A full run could only raise the
   count.
2. **Part I is internally inconsistent.** §5's tier table says a `SEARCH-SUMMARY` cell is "RECALL-grade
   for every gate". Its next paragraph says triage survivors can exist anyway, and P-34 counts
   "triage survivors". Read strictly, §5 makes every PASS in this arm unevaluable, the survivor
   count is 0, and P-34 is wrong. I registered the looser reading in the prediction text and score
   against that. **The strict reading is the one a gate should use, and it returns 0.**

## 3. What the survivors actually are

All three sit **inside, or next to, a table that AI systems are actively moving**:

* **Kissing numbers:** AlphaEvolve (May 2025), PackingStar (Nov 2025), EinsteinArena (Apr 2026),
  and arXiv:2609.35051 (Sep 2026, "large-scale autonomous discovery of kissing number
  constructions", seen in a search result this session). Cohn's table is reported as updated on
  22 June 2026. Dimensions 13 and 14 survive S4 only because S4 is registered **per record**.
* **Caps:** the 512 is itself an AI result, and the adjacent capacity record was moved by AI in 2025.

**The crowding gate is scoped wrongly.** A table on which three AI systems moved two neighbouring
cells within twelve months is crowded in the sense that matters — our reachable region sits inside
theirs, which is the 282 lesson — even when a given cell has not moved. SELECT v2 should scope S4
to the table. I am **not** applying that retroactively (D45). Under it, all three survivors die,
and Arm 2 returns 0.

## 4. Arm 2b — the divergence search (P-35)

**Not run to completion.** The worker read the 67 AlphaEvolve problem pages and 10 notebooks via
raw GitHub. It was stopped when I capped concurrency at three and the search budget ran out, before
it recorded any entry. **P-35 stays OPEN**: the instrument did not run, which is different from
running and returning nothing.

Two divergence-shaped facts turned up in other arms. Neither meets the registered definition:
* **APN functions, dimension 8:** the 2025 method's output is about 292× larger than the best
  earlier single method. The frontier parameter is a count of objects, not a reach, so it does not
  qualify.
* **Grothendieck constant:** the 2026 lower bound was reached by an asymptotic argument that
  explicit low-dimensional instances had not reached in 35 years. That is a divergence in *method
  class*, not in a frontier parameter.


---

## 5. [30 Sep 2026] A third crowding scoping, and a correction to what was inferred from §3

§3 proposed scoping S4 to the **table**. `discovery/RESULT_B1_DESIGNS.md` §2 found a third: in the same La Jolla **repository family**, the *signed* difference set table was swept in Aug–Sep 2026, all **68** open small entries resolved (16 exist, 52 do not), by a GitHub project whose README **discloses extensive OpenAI Codex use**. Correctly not counted against cyclic difference sets — a different object — but it is the activity this project would be competing with.

**And it corrects an inference made elsewhere.** `discovery/RESULT_GATE_C1.md` §6 established that the design-theory objects are absent from EinsteinArena's board, and that was then read as the seam being unswept. **Not on a board is not the same as not being swept.** The signed-DS sweep needed no board, no leaderboard and no platform, and no board-based crowding screen can see it. The scoping question is record / table / **repository-family**.


---

## 6. [30 Sep 2026] Arm 2 is closed: 15 of 15 assessed, 0 live survivors

Ten tables in the original run (2 triage survivors, all three of their records subsequently killed at gates C-1, C-2, C-3), three in brief B1, two in brief B2. **P-34's scoring on triage survivors is untouched; the pipeline yield is 0.**

**Two things the closing runs established that outlast the verdicts.**

**S3 is where every table that reached it died, six consecutive times** — tables 7, 8, 9, 10 and arm 1's records 277 and 353, all for want of a method section, and **not one on evidence that the move was `SEARCH-REPEAT`**. D50 is now the gate's observed behaviour rather than a hypothesis about it.

**S4 is built on the wrong observable — D51.** It counts moves, so it cannot see an attempt that failed. Rosin's CPro1 (arXiv:2505.23881) put LLM-driven search on Costas arrays in 2025 and moved nothing; both the record-scoped and table-scoped readings of S4 are blind to it. Meanwhile C-1's bar treated an attempt as PASS evidence and C-3's treated it as FAIL. **Three instruments, three readings of one fact**, and the state they disagree about — attempted and failed — is the only one that distinguishes a durable opportunity from a merely unvisited cell.

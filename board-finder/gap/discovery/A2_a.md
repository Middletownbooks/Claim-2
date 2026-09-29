# A2_a — record tables outside the corpus (worker output, Sonnet 5.5, 2026-09-29)

Provenance note for the whole file: this worker could not open arxiv.org, cohn.mit.edu, Orrick's or
Brouwer's pages, OEIS, or publishers (egress proxy blocks them; tried WebFetch once on cohn.mit.edu:
`EGRESS_BLOCKED`, no rerouting attempted). Almost every factual cell is therefore `SEARCH-SUMMARY`
(seen in a WebSearch result summary, source not read). The few `SECONDARY-RELAYED` cells are files
read from raw.githubusercontent.com. Nothing here is `PRIMARY-VERIFIED-LOCALLY` unless stated.

## SUMMARY TABLE

(to be filled at the end of the run — blocks below are written incrementally)

---

## TABLE 1 — Kissing numbers, lower bounds in dimensions 11, 12, 13, 14

```
TABLE       | Table of kissing number bounds, maintained by Henry Cohn (MIT), https://cohn.mit.edu/kissing-numbers/ (a dated PDF snapshot also sits in MIT DSpace, handle 1721.1/153312). Last update seen: "June 22, 2026" — from a search-result summary of that page, page not read (fetch blocked). Older reference: Conway–Sloane SPLAG / Nebe–Sloane catalogue (not consulted). | SEARCH-SUMMARY
AI ACTIVITY | (i) AlphaEvolve (Google DeepMind), announced May 2025: dim 11, 592 -> 593 (SEARCH-SUMMARY, several press/paper-summary hits; unread primary). (ii) EinsteinArena (Together AI multi-agent platform; agent alpha_omega_agents first jump 8 Apr 2026, settled 11 Apr 2026): dim 11, 593 -> 594 -> 604 (SEARCH-SUMMARY; paper arXiv:2606.10402 unread). (iii) PackingStar (game-theoretic RL, arXiv:2511.13391, Nov 2025): new records dims 25-31, fully rational 13-D configuration K_r(13)=1146 (below the 1154 record), "diverse configurations" in 12/14/15-D that did not beat the records; README on raw.githubusercontent.com says its configs "have been accepted into the kissing number database" (SECONDARY-RELAYED for the README claim; the 1146 figure is SEARCH-SUMMARY). (iv) Qiushi Engine (Zhejiang Univ., arXiv:2609.35051, 25 Sep 2026): dims 25, 27, 32-39, 43, 45, 49-55 only — none of 11-14. (v) EinsteinArena also lists a "Kissing Number in Dimension 12 (n=842)" problem with ~50 solutions from 8 agents and no reported success (SEARCH-SUMMARY, snapshot date unknown). | SEARCH-SUMMARY (all)
```

Shared facts for the four cells (all SEARCH-SUMMARY): the quantity in each cell is the kissing number
tau_n, i.e. the maximum size of a set of unit vectors in R^n with pairwise angle >= 60 degrees.
Upper bounds in the maintained table, per search summaries: dim 11 = 868 (Leijenhorst–de Laat degree-17
SDP value 868.8265 rounded down; the rigorous Machado–de Oliveira Filho degree-16 figure was 869),
dim 12 = 1355, dim 13 = 2064, dim 14 = 3174. Upper-bound precision: 868 rests on a numerical SDP value
(`NUMERICAL`), the others are reported in the table without precision detail (`UNKNOWN`). The upper
side is never moved by a witness (see BOUND OBJ), so the upper-bound details do not enter any gate.

### 1a. Dimension 11

```
RECORD      | Table 1 / dim 11 — kissing number lower bound, R^11
QUANTITY    | max number of unit vectors in R^11 with pairwise angle >= 60 degrees (tau_11)
LOWER       | 604, EinsteinArena AI agents (alpha_omega_agents first leap 8 Apr 2026; refinements by several agents; valid 604-sphere solution by 11 Apr 2026) | SEARCH-SUMMARY (Together AI blog/press summaries; arXiv:2606.10402 unread; Cohn table listing 604 also seen only in a summary) | EXACT (reported: final solution "lives in Z[sqrt 2]" and was checked at 1e-50 precision — as relayed, unread) ; PREPRINT (platform paper, not refereed)
UPPER       | 868, Leijenhorst–de Laat (degree-17 SDP, 868.8265 rounded down), year not established (Machado–de Oliveira Filho rigorous degree-16 gave 869, 2018) | SEARCH-SUMMARY | NUMERICAL ; UNKNOWN
BOUND OBJ   | lower: WITNESS — a finite set of vectors whose pairwise inner products are checked <= 1/2; upper: PROOF — an SDP/LP-type dual certificate is a computation, but no witness moves it and the cited value is a numerical SDP optimum; nothing in hand shows a finite object exhibiting it, so treated as PROOF/NONE-by-witness (not evaluated further)
S0 OPEN     | PASS — gap 604..868 in the maintained table (SEARCH-SUMMARY). No resolution claim found in any search.
S1 COUPLED  | PASS — route (a): tau_n is a maximum over finite point sets on the sphere, so any admissible configuration of N points is a one-sided lower bound N; this is the definition of the quantity, not a lifting step. It is also the mechanism by which the last three records were set (Ganzhinov 592, AlphaEvolve 593, EinsteinArena 604 were each an explicit configuration) | SEARCH-SUMMARY for the record history; the extremal characterisation itself is definitional
S2 VETO     | PASS — predicate "N unit vectors, all pairwise inner products <= 1/2" is decidable; for algebraic coordinates (Z[sqrt 2] here) it is checked exactly by terminating computation.
MOVE-1      | 2026-04-08..11 | EinsteinArena agents (alpha_omega_agents, "Gradient" agent, CHRONOS, others) | 604 | UNKNOWN +AI-SEARCH | relayed account: a first construction with slightly overlapping spheres appeared 8 Apr; "a Gradient agent discovered a new basin"; over ~48 h several agents refined it, raising the verification precision to 1e-50, and the valid result turned out to live in Z[sqrt 2]. Whether this is a method already used on this record (AlphaEvolve also used LLM-guided search here) or a new one, I could not establish from summaries | SEARCH-SUMMARY
MOVE-2      | 2025-05 (AlphaEvolve announcement; broader write-up arXiv:2511.02864 Nov 2025) | Novikov et al. / Georgiev–Gómez-Serrano–Tao–Wagner (AlphaEvolve) | 593 (was 592) | SEARCH-NEW +AI-SEARCH | relayed: AlphaEvolve evolves "heuristic search algorithms" that run local search/optimisation starting from the previous best construction (Ernest Davis's notes, as summarised) — first LLM-evolved-program search applied to this record | SEARCH-SUMMARY
            (earlier: 2022-07 Ganzhinov, arXiv:2207.08266, "Highly symmetric lines", 592 (was 582, Best 1980); published Linear Algebra Appl. 722 (2025). Kind: not classified here; Aalto press summary: "reducing the problem size by looking only for arrangements with a high degree of symmetry" | SEARCH-SUMMARY)
S3 IDEA     | CANNOT EVALUATE — MOVE-1 has kind UNKNOWN (could not establish SEARCH-NEW vs SEARCH-REPEAT vs an ANALYTIC element given the Z[sqrt 2] structure). Missing: the text of arXiv:2606.10402 or the EinsteinArena discussion threads.
S4 CROWDED  | FAIL — the coupled side moved by AI-driven systems on/after 2025-01-01, twice: AlphaEvolve (May 2025, 593) and EinsteinArena agents (April 2026, 604). Searches: "kissing number dimension 11 AlphaEvolve 593", "EinsteinArena kissing number dimension 11 604", "kissing number dimension 11 lower bound 2026 improved beyond 604" (nothing beyond 604 found). | SEARCH-SUMMARY
S5 DELIVER  | PASS — Cohn's table of kissing number bounds (row n=11) would change. Abstract sentence: "We construct a kissing configuration of 605 points in R^11, improving the lower bound tau_11 >= 604." | SEARCH-SUMMARY (that 604 is the table value)
DIVERGENCE  | NONE FOUND — the record moved 582 (Best 1980) -> 592 -> 593 -> 604, largest ratio 604/582 = 1.04, far below 2; frontier parameter is the number of points in fixed dimension 11. Searches: the five dim-11 searches above.
BITS_SEARCH | UNDEFINED — no named search ansatz with a published density estimate for this witness was found.
VERIF CLASS | CHECK (exact finite computation) for algebraic-coordinate configurations such as the Z[sqrt 2] one; numerical-coordinate submissions would need RIGOROUS-NUMERIC verification.
NOTES       | Values relayed: the EinsteinArena page title still reads "Kissing Number in Dimension 11 (n=594)" in search results (stale title; 604 is the figure in the arXiv paper summary and in the Cohn-table summary). The brief's premise "FunSearch found a large cap in dim 8" is not relevant here.
```

### 1b. Dimension 12

```
RECORD      | Table 1 / dim 12 — kissing number lower bound, R^12
QUANTITY    | max number of unit vectors in R^12 with pairwise angle >= 60 degrees (tau_12)
LOWER       | 841, Takhanov–Assylbekov–Yun, arXiv:2606.18984, June 2026 (previous 840 from 1971, Leech–Sloane era, RECALL for authorship) | SEARCH-SUMMARY (arXiv abstract summary; Cohn table listing 841 seen in a summary) | NUMERICAL (abstract: "numerically construct a kissing arrangement of size 841"; a later paper, arXiv:2609.09179, says the 841 configuration "was obtained numerically by optimization ... released as a coordinate file, without a mathematical description"; I did not see whether it was upgraded to an interval-arithmetic-verified configuration) ; PREPRINT
UPPER       | 1355, source and year not established | SEARCH-SUMMARY | UNKNOWN ; UNKNOWN
BOUND OBJ   | lower: WITNESS — 841 coordinate vectors; upper: PROOF/not witness-moved (as in 1a)
S0 OPEN     | PASS — gap 841..1355 (SEARCH-SUMMARY). No resolution claim found. Separate data: arXiv:2609.09179 (Sept 2026) gives an exact quaternionic description of an 840-point arrangement (three orthogonal 24-cells plus two 384-point families) and reports that 816 vectors of the 841 record are slight deformations of it — this explains 841, it does not move the bound.
S1 COUPLED  | PASS on the object type — route (a), same definitional extremum as 1a; the maintained table accepted 841 (summary), so a better configuration does move a published bound. Caveat for the adjudicator: the current 841 witness is described as numerical; whether the value is fixed by a terminating computation at exact or rigorous-numeric precision is CANNOT EVALUATE from what I could read. | SEARCH-SUMMARY
S2 VETO     | PASS — same decidable predicate as 1a (exact for algebraic coordinates, rigorous-numeric for interval-checked ones).
MOVE-1      | 2026-06 | Takhanov, Assylbekov, Yun | 841 (was 840) | UNKNOWN (abstract paraphrase points to SEARCH-NEW; novelty against earlier numerical attempts on this record not established) | abstract: known 840-point arrangements have 60+60 vectors in R^6 x {0} and {0} x R^6 plus 720 "bridge vectors" from the 1-factorization of K6; each 60-block contains 12 fixed +-e_i and 48 vectors that can vary in a positive-dimensional family ("48-systems"); "starting from such structurally informed initial configurations, they numerically construct" 841 | SEARCH-SUMMARY
MOVE-2      | 1971 | (Leech–Sloane era; authorship RECALL) | 840 | UNKNOWN | no source read; the brief-adjacent summaries only say "had stood since 1971" | SEARCH-SUMMARY
S3 IDEA     | CANNOT EVALUATE — MOVE-1's kind is UNKNOWN as above (the abstract-level evidence is consistent with SEARCH-NEW but I did not read the paper's account of prior numerical work on R^12).
S4 CROWDED  | CANNOT EVALUATE — the move (June 2026, numerical optimisation from structured starts) is after 2025-01-01 and no AI system is credited in the summaries; but whether it counts as "large-scale optimisation tooling" needs the paper's methods section (scale, tooling), which I could not read. Searches: "Takhanov Assylbekov Yun 841 kissing number dimension 12", "Structure of kissing arrangements in R^12 ... 841st sphere", "EinsteinArena kissing number dimension 12". Also seen: EinsteinArena problem "Kissing Number in Dimension 12 (n=842)", ~50 solutions from 8 agents, none reported as a valid 842. | SEARCH-SUMMARY
S5 DELIVER  | PASS — Cohn's table (row n=12). Abstract sentence: "We construct a kissing configuration of 842 points in R^12, improving the lower bound tau_12 >= 841." | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — 840 (1971) vs 841 (2026), ratio 1.001. Searches as above.
BITS_SEARCH | UNDEFINED — no published density estimate for a named ansatz found (the "48-systems" ansatz is named in the abstract, but no density estimate seen).
VERIF CLASS | RIGOROUS-NUMERIC at best for the current style of witness (numerical coordinates); CHECK only if an exact algebraic description (like the 840 quaternionic one) is found for the improved configuration.
NOTES       | Dim 12 differs from the others: the record is (per summaries) a numerical optimum with a structured ansatz, and the exact structure paper appeared only afterwards. Keep the precision tag when relaying 841.
```

### 1c. Dimension 13

```
RECORD      | Table 1 / dim 13 — kissing number lower bound, R^13
QUANTITY    | max number of unit vectors in R^13 with pairwise angle >= 60 degrees (tau_13)
LOWER       | 1154, Zinoviev–Ericson, "New lower bounds for contact numbers in small dimensions", Probl. Inf. Transm. 35(4) (1999) | SEARCH-SUMMARY (search results: survey and PackingStar text; not read) | UNKNOWN (PackingStar's text, as summarised, calls the 1154 configuration "non-rational", i.e. real-coordinate; exactness of the published description not seen) ; REFEREED (journal, 1999)
UPPER       | 2064, source and year not established | SEARCH-SUMMARY | UNKNOWN ; UNKNOWN
BOUND OBJ   | lower: WITNESS — 1154 coordinate vectors; upper: PROOF/not witness-moved
S0 OPEN     | PASS — gap 1154..2064 (SEARCH-SUMMARY). No resolution claim found.
S1 COUPLED  | PASS — route (a), same definitional extremum as 1a. | SEARCH-SUMMARY for the record; extremal characterisation definitional
S2 VETO     | PASS — same decidable predicate.
MOVE-1      | 1999 | Zinoviev, Ericson | 1154 | ANALYTIC | a survey summary says the Dodunekov–Ericson–Zinoviev concatenation construction (placing codes on suitable position sets of the original codes) gave almost all record cardinalities below dimension 24 and that Zinoviev–Ericson obtained tau_13 >= 1154; PackingStar's text (as summarised) adds that the 1154 structure came from slightly adjusting coordinates of some spheres of a 1130-sphere configuration | SEARCH-SUMMARY
MOVE-2      | 1999 (same paper family) | Zinoviev, Ericson | 1130 (was lower) | ANALYTIC | same evidence; 1130 as the predecessor value is from the PackingStar-text summary only | SEARCH-SUMMARY
S3 IDEA     | PASS — MOVE-1 is ANALYTIC (code-concatenation construction, explicit by hand) per the survey summary above.
S4 CROWDED  | PASS — no move of the coupled side since 1999. Searches: "kissing dimension 13 1154 Zinoviev Ericson improvement 2026", Cohn-table listing (dim 13 lower bound 1154, seen in summaries dated through mid-2026), "PackingStar ... dimension 13" (PackingStar, an RL system, Nov 2025, produced only a rational 13-D configuration of 1146 < 1154 — a move on the rational-configuration sub-record, not on 1154), no EinsteinArena d13 problem page surfaced. | SEARCH-SUMMARY
S5 DELIVER  | PASS — Cohn's table (row n=13). Abstract sentence: "We construct a kissing configuration of 1155 points in R^13, improving the 1999 lower bound tau_13 >= 1154." | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — 1130 vs 1154 (ratio 1.02); rational 1146 vs real 1154 is a different object (rationality), ratio 1.007. Searches as above.
BITS_SEARCH | UNDEFINED — no named ansatz with a published density estimate found.
VERIF CLASS | CHECK for exact/algebraic-coordinate configurations; RIGOROUS-NUMERIC otherwise.
NOTES       | The 1154 record is the oldest of the four cells (1999) and the only one whose latest move is ANALYTIC with a source describing what the paper did. Two "1154" descriptions in summaries differ slightly (concatenation construction vs coordinate adjustment of a 1130 configuration); both are hand constructions.
```

### 1d. Dimension 14

```
RECORD      | Table 1 / dim 14 — kissing number lower bound, R^14
QUANTITY    | max number of unit vectors in R^14 with pairwise angle >= 60 degrees (tau_14)
LOWER       | 1932, Ganzhinov, "Highly symmetric lines", arXiv:2207.08266 (July 2022); Linear Algebra Appl. 722 (2025) pp. 12-37 | SEARCH-SUMMARY (Aalto press release, arXiv listing summaries, Cohn-table listing 1932; unread) | UNKNOWN (finite-group-orbit configuration; exactness not seen, group-orbit constructions are typically algebraic but I did not read it) ; REFEREED (Linear Algebra Appl. 2025) and PREPRINT since 2022
UPPER       | 3174, source and year not established | SEARCH-SUMMARY | UNKNOWN ; UNKNOWN
BOUND OBJ   | lower: WITNESS — 1932 coordinate vectors; upper: PROOF/not witness-moved
S0 OPEN     | PASS — gap 1932..3174 (SEARCH-SUMMARY). No resolution claim found.
S1 COUPLED  | PASS — route (a), same definitional extremum as 1a. | SEARCH-SUMMARY
S2 VETO     | PASS — same decidable predicate.
MOVE-1      | 2022-07 (arXiv); 2025 (journal) | Ganzhinov | 1932 | SEARCH-NEW | Aalto press release (as summarised): the improvement was found "by reducing the problem size by looking only for arrangements with a high degree of symmetry" — a symmetry-restricted computer-aided search introduced in the paper (kind could also be read as ANALYTIC; both pass S3) | SEARCH-SUMMARY
MOVE-2      | earlier value (I recall 1606, Zinoviev–Ericson 1999; not sourced this session) | | | UNKNOWN | RECALL only | RECALL
S3 IDEA     | PASS — MOVE-1 is SEARCH-NEW (or ANALYTIC), neither is SEARCH-REPEAT; the evidence is a press-release paraphrase of the method. (If the adjudicator requires more than a press release for the kind, this becomes CANNOT EVALUATE; the two candidate readings agree.)
S4 CROWDED  | PASS — no move of the coupled side since 2022. Searches: "kissing number dimension 14 lower bound 1932 Ganzhinov record still stands" (Cohn-table summary still shows 1932), "einsteinarena kissing-number-d14" (no d14 problem page surfaced; d11 and d12 pages exist), PackingStar (its 14-D output is described as "diverse configurations", not a new bound). | SEARCH-SUMMARY
S5 DELIVER  | PASS — Cohn's table (row n=14). Abstract sentence: "We construct a kissing configuration of 1933 points in R^14, improving Ganzhinov's lower bound tau_14 >= 1932." | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — the only dated predecessor I could name is RECALL; nothing sourced with ratio >= 2. Searches as above.
BITS_SEARCH | UNDEFINED — the symmetric-orbit ansatz is named ("highly symmetric lines") but no published density estimate was found.
VERIF CLASS | CHECK for exact orbit constructions; RIGOROUS-NUMERIC otherwise.
NOTES       | Ganzhinov's paper has been the human counter-example in press ("Human outsmarts Google DeepMind AI"): AlphaEvolve's dim-11 593 came after his 592, and Ganzhinov 2022 predates every AI move on this table.
```

### 1 — cross-cell notes

* Derived count: cells with an AI-driven move of the lower bound on/after 2025-01-01 = {dim 11 (AlphaEvolve 2025-05, EinsteinArena 2026-04)} = 1 of 4. Cells with no move since 2025-01-01 by any system = {dim 13, dim 14} = 2 of 4. Dim 12 moved 2026-06 by numerical optimisation with no AI system credited in the summaries (not classifiable, see S4).
* The brief calls Cohn's list "the maintained table"; the table page and its PDF snapshot both exist, but I read neither (blocked; search summaries only).

---

## TABLE 2 — Caps in AG(n,3): largest known cap for n = 7 and n = 8 (and the cap-set capacity)

**Tool-budget note that affects Tables 2-5.** The WebSearch tool's session budget ran out (`200 of 200`
calls, shared across workers) after I had used ~26 searches, all on Table 1 plus three on Table 2.
Three further Table-2 queries were refused (listed under each block). For Tables 3-5 I have no
WebSearch at all; those blocks rest on `RECALL`, on files read from raw.githubusercontent.com or the
local repository, and on computation. The GitHub connector tools are in the tool list but I did not
use them to read repositories (the brief names only WebSearch and raw.githubusercontent.com curl).

```
TABLE       | Edel's tables of caps in AG(n,3) (Yves Edel, "Caps" pages) — the brief's named lineage. I did NOT see the table page in any search result or fetch; its location and last-update date are NOT FOUND this session. What I did read: the FunSearch repository notebook (raw.githubusercontent.com/google-deepmind/funsearch/main/cap_set/cap_set.ipynb) which states the previous best n=8 construction had size 496 and the largest known for n=9 is 1082 (SECONDARY-RELAYED). No other maintained cap table found. | table itself: NOT FOUND; notebook statements: SECONDARY-RELAYED
AI ACTIVITY | (i) FunSearch (Romera-Paredes et al., Nature 625 (2024), online Dec 2023): 512-cap in AG(8,3), previous best 496 (SECONDARY-RELAYED: notebook text; I re-ran the notebook code locally and verified the 512-cap, PRIMARY-VERIFIED-LOCALLY); also cap-set capacity 2.2202 via admissible set A(24,17) of size 237,984 (SECONDARY-RELAYED + arithmetic recomputed locally = 2.220234). (ii) X-evolve (arXiv:2508.07932, 2025, LLM-driven "solution space evolution"): cap-set capacity "2.2203" (SEARCH-SUMMARY only; paper unread; whether it also reported anything for n=7 or n=8: NOT FOUND — the query that would have checked this was refused by the exhausted search budget). (iii) "Generative Modeling for Mathematical Discovery" (arXiv:2503.11061, March 2025): its search-summary lists the largest known caps n=3..8 as 9, 20, 45, 112, 236, 512, i.e. no move on n=7 or n=8 as of that paper (SEARCH-SUMMARY). (iv) AlphaEvolve's problem repository (local dump of its 67 problem statements, aerp_problems_2026-09-29.json, read by regex): no entry mentions cap sets or admissible sets — SECONDARY-RELAYED, negative. | mixed, tagged inline
```

### 2a. AG(7,3)

```
RECORD      | Table 2 / n=7 — size of the largest known cap in AG(7,3)
QUANTITY    | c(7) = max size of a set in F_3^7 containing no three distinct collinear points (equivalently no distinct a,b,c with a+b+c = 0)
LOWER       | 236, attributed in one search summary to Calderbank–Fishburn ("Maximal three-independent subsets of {0,1,2}^n", DCC 1994 — year is RECALL) | SEARCH-SUMMARY | EXACT (finite explicit cap; explicitness not read) ; REFEREED (RECALL)
UPPER       | not found; RECALL, low confidence: about 291 | RECALL | UNKNOWN ; UNKNOWN
BOUND OBJ   | lower: WITNESS — an explicit cap, checkable in O(c^2 n) time (checker in the FunSearch notebook); upper: PROOF — an argument (counting/LP/exhaustive-search classification); no witness moves it
S0 OPEN     | PASS (weak) — sources say "largest known" 236 with no optimality claim; the gap to an upper bound rests on RECALL only; no resolution claim appeared in three searches.
S1 COUPLED  | PASS — route (a): c(7) is a maximum over finite sets, so any 7-dimensional cap of size s is a lower bound c(7) >= s. | definitional; record value SEARCH-SUMMARY
S2 VETO     | PASS — "no three distinct points with a+b+c = 0 (mod 3)" is decidable by finite check (I ran the check for the n=8 analogue).
MOVE-1      | 1994 (RECALL) | Calderbank, Fishburn (search-summary attribution; year RECALL) | 236 | UNKNOWN | I did not read the paper; one summary says they "constructed a 7-cap of size 236" | SEARCH-SUMMARY
MOVE-2      | NONE (earlier history not found)
S3 IDEA     | CANNOT EVALUATE — kind of the 236 construction UNKNOWN (paper unread). Missing: the Calderbank–Fishburn paper or Edel's table notes.
S4 CROWDED  | CANNOT EVALUATE — searched: "largest known cap AG(7,3) 236 AG(8,3) 512 FunSearch Edel table caps affine space" (n=7 still 236, in a March-2025 paper's summary), "Edel Extensions of generalized product caps ... dimension 7" (nothing on n=7 after 2025). Refused by the exhausted search budget: any query on 2025-2026 n=7 improvements, and the X-evolve query. "Did not search" for the period after March 2025 -> the gate cannot be evaluated.
S5 DELIVER  | PASS — a named published bound (c(7) >= 236) and, if it exists as I recall, Edel's table would change. Sentence: "We construct a cap of size 237 in AG(7,3), improving the 236-cap of Calderbank and Fishburn." | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — for the cap-size cell itself; see 2c for the one candidate on the asymptotic object. Searches: those above.
BITS_SEARCH | UNDEFINED — no published density estimate for a named ansatz found.
VERIF CLASS | CHECK — exact finite computation (O(c^2 n)).
NOTES       | The brief says FunSearch found a large cap in dimension 8; that is confirmed for n=8 (below) and FunSearch's table matches known values for n <= 7 (per the summary above), so n=7 was not moved by it.
```

### 2b. AG(8,3)

```
RECORD      | Table 2 / n=8 — size of the largest known cap in AG(8,3)
QUANTITY    | c(8) = max size of a cap in F_3^8
LOWER       | 512, FunSearch (Romera-Paredes et al.), Nature 625 (2024), online Dec 2023; previous best 496 | SECONDARY-RELAYED (funsearch repo notebook text) and PRIMARY-VERIFIED-LOCALLY (I executed the notebook's `priority` + greedy `solve(8)` -> 512 vectors, ran the notebook's checker `is_cap_set` -> True, and separately brute-forced all 130,816 pairs (a,b): no third point -a-b in the set -> 0 collinear triples; also ran the hand-written `build_512_cap()` explicit construction: same 512-set) | EXACT ; REFEREED (Nature)
UPPER       | not found; RECALL, low confidence: about 771 | RECALL | UNKNOWN ; UNKNOWN
BOUND OBJ   | lower: WITNESS — the explicit 512-cap; upper: PROOF
S0 OPEN     | PASS — 512 is the largest known cap; no optimality claim seen; no resolution claim found. Upper bound value is RECALL only.
S1 COUPLED  | PASS — route (a): c(8) is a maximum over finite sets; the 512-cap is precisely how the bound moved (Nature 2024). | SECONDARY-RELAYED
S2 VETO     | PASS — decidable check; I ran it locally.
MOVE-1      | 2023-12 (online; Nature print 2024) | Romera-Paredes, Barekatain, Novikov, Balog, Kumar, Dupont, Ruiz, Ellenberg, Wang, Fawzi, Kohli, Fawzi et al. (FunSearch) | 512 (was 496) | SEARCH-NEW +AI-SEARCH | notebook: "This function discovered by FunSearch results in a cap set of size 512 in n = 8 dimensions, thus improving upon the previously known best construction (which had size 496)"; the authors then noticed regularities (weight distribution of the 512 vectors) "and were able to manually find the following explicit construction" (an ANALYTIC description written after the search) | SECONDARY-RELAYED
MOVE-2      | earlier: the 496 construction (attribution "Edel 2004" is the brief's lineage and my RECALL; not confirmed this session) | | 496 | UNKNOWN | not read | RECALL
S3 IDEA     | PASS — MOVE-1 is SEARCH-NEW (a method introduced by the paper, first applied to this record: LLM-evolved priority function driving a greedy cap construction; the repository skeleton shows it). Note the ANALYTIC post-hoc explicit construction does not change the kind of the move.
S4 CROWDED  | CANNOT EVALUATE — the last known move (Dec 2023) predates 2025-01-01, and a March-2025 paper summary still lists 512 as the largest known n=8 cap; but I could not run any query covering March 2025 - September 2026 for AG(8,3): the query "cap set AG(8,3) size 512 FunSearch improved 496 Edel; new cap AG(8,3) larger than 512" was refused by the exhausted search budget, and X-evolve (2025, LLM-driven, cap-set work) is unread, so I cannot say whether it or any other AI system moved n=8. "Did not search" = CANNOT EVALUATE. Partial negative: AlphaEvolve's problem repository has no cap-set problem (local dump, SECONDARY-RELAYED).
S5 DELIVER  | PASS — named published bound c(8) >= 512 (FunSearch, Nature 2024); Edel's table would change too if maintained (not confirmed). Sentence: "We construct a cap of size 513 in AG(8,3), improving the 512-cap found by FunSearch."
DIVERGENCE  | NONE FOUND for the cap-size cell — 496 vs 512 (ratio 1.03). Searches: those above.
BITS_SEARCH | UNDEFINED — FunSearch's greedy-with-evolved-priority ansatz is named, but no published density estimate for it was found (the FunSearch paper may contain scaling data I have not read).
VERIF CLASS | CHECK — exact finite computation; done locally in seconds.
NOTES       | The FunSearch repository (raw.githubusercontent.com) is the best-evidenced item in this whole file: code plus data plus an explicit hand-made reconstruction. The same notebook states the largest known cap for n=9 is 1082 and that FunSearch's evolved n=9 function only matches it.
```

### 2c. Cap-set capacity (asked for "if you meet it")

```
RECORD      | Table 2 / capacity — cap-set capacity lower bound C = sup_n c(n)^(1/n)
QUANTITY    | asymptotic growth rate of the largest cap in AG(n,3) (capacity)
LOWER       | 2.2203, X-evolve, arXiv:2508.07932 (2025) | SEARCH-SUMMARY (one search summary: "a further incremental improvement to 2.2203 through X-evolve"; the exact digits and construction unread) | UNKNOWN ; PREPRINT
              before that: 2.2202, FunSearch (Dec 2023): admissible set A(24,17) of size 237,984, recipe of the repo notebook gives 2.2202336... — I recomputed this locally: compute_capacity_bound(24,17,237984,m=4) = 2.2202337 [PRIMARY-VERIFIED-LOCALLY for the arithmetic; the size 237,984 itself is a stated file count, I checked only that the pre-admissible file has 736 rows]; A(21,15) size 43,596 gives 2.2200406 (local recompute) | RIGOROUS-NUMERIC? no — closed-form of finite integers, i.e. EXACT up to rounding | REFEREED (Nature)
              before that: 2.218021, Tyrrell, "New lower bounds for cap sets" (arXiv:2209.10045; Discrete Analysis 2023) — the notebook calls 2.218021 "the previous state-of-the-art" | SECONDARY-RELAYED (notebook), SEARCH-SUMMARY (paper title/venue)
UPPER       | about 2.756, Ellenberg–Gijswijt (2016) via the polynomial method (RECALL; improved explicit forms exist, e.g. arXiv:2103.06481 title seen only) | RECALL | EXACT ; REFEREED
BOUND OBJ   | lower: WITNESS — finite admissible set A(n,w) plus a finite extendable base collection of caps (12,112,112 in dimension 6), lifted by the published recipe; upper: PROOF
S0 OPEN     | PASS — gap 2.2203 vs about 2.756; no resolution claim found.
S1 COUPLED  | PASS — via a published lifting theorem, not via small-n caps: the notebook's recipe follows Edel (2004) and Tyrrell (2022): a finite admissible set A(n,w) applied to an extendable collection of caps yields a 6mn-dimensional cap of size |A|·b0^(n-w)·b1^w, hence capacity >= size^(1/(6mn)). Note the model case in the brief (cap of size s in AG(n,3) gives s^(1/n)) gives only 236^(1/7)=2.1827 (n=7) and 512^(1/8)=2.1810 (n=8) [local arithmetic], both below the 2.218 record — so the n=7/n=8 caps by themselves do not move the capacity bound. | SECONDARY-RELAYED (recipe) + local arithmetic
S2 VETO     | PASS — admissible-set predicate and the size formula are finite and decidable.
MOVE-1      | 2025 (arXiv 2508.07932, Aug 2025 by id) | X-evolve authors | 2.2203 (from 2.2202) | UNKNOWN +AI-SEARCH | only "an LLM-powered approach" per one summary; what it searched over (admissible sets? which n,w?) not seen | SEARCH-SUMMARY
MOVE-2      | 2023-12 | FunSearch | 2.2202 (from 2.2180) | SEARCH-NEW +AI-SEARCH | notebook: FunSearch-discovered programs construct admissible sets A(12,7), I(15,10), A(21,15), A(24,17); A(24,17) "implies a new state-of-the-art lower bound of 2.220234"; "solve(24,17) takes ~7 hours" (a C++ reimplementation was used in practice); search restricted to *symmetric* admissible sets | SECONDARY-RELAYED
              (and 2022: Tyrrell 2.218021, kind ANALYTIC by search-summary: introduced constant-weight admissible sets as the tool | SEARCH-SUMMARY)
S3 IDEA     | CANNOT EVALUATE — MOVE-1 (X-evolve) kind UNKNOWN: it may be SEARCH-REPEAT (same LLM-program-search class as FunSearch on the same admissible-set object) or SEARCH-NEW (new "solution-space evolution" method); the paper is unread.
S4 CROWDED  | FAIL — the coupled side moved on/after 2025-01-01 by an LLM-driven system (X-evolve, 2025, 2.2203). | SEARCH-SUMMARY
S5 DELIVER  | PASS — named published bound (capacity >= 2.2203, X-evolve 2025). Sentence: "We construct a symmetric admissible set A(n,w) of size N, which by the Edel–Tyrrell recipe gives cap-set capacity at least 2.2204, improving the 2.2203 of X-evolve."
DIVERGENCE  | CANDIDATE, unverified — one search summary (about Edel's "Extensions of generalized product caps", DCC 31, 5-14, 2004) says the asymptotic improvement over Calderbank–Fishburn "becomes visible in dimensions as low as 62, whereas the bound from Calderbank and Fishburn is based on caps in dimension 13,500": if that reading is right, reach in dimension 62 vs 13,500 = ratio 217.7 (13,500/62; derived by me). I did not read the source and cannot tell whether "dimension at which the record constant is realised" is the frontier parameter the gate means, so I do not assert a DIVERGENCE. | SEARCH-SUMMARY
BITS_SEARCH | UNDEFINED — named ansatz (symmetric admissible sets, FunSearch) exists; no published density estimate found.
VERIF CLASS | CHECK — exact integer arithmetic on the size of a finite admissible set (plus checking admissibility, a finite check of cost polynomial in |A|).
NOTES       | Precision caution: "2.2202" (FunSearch) is the rounded closed form 2.220234; "2.2203" for X-evolve is a search-summary digit string. Recomputing the rounding: 2.2202337 rounds to 2.2202 (4 d.p.), so a bound reported as 2.2203 from X-evolve must come from a different (larger) admissible set or recipe, not from a rounding of FunSearch's number.
```

---


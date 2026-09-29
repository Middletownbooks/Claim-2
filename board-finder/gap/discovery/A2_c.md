# A2_c — record tables outside the corpus (Tables 11-15)

Worker: Arm 2c. Date of run: 2026-09-29. **Complete.**

Environment note (applies to every block): WebFetch to arxiv.org, boolean.wiki.uib.no and langevin.univ-tln.fr
returned EGRESS_BLOCKED on the single attempt each. No mirrors were tried. Every factual cell below that is not
marked RECALL comes from a WebSearch result title/summary (tier SEARCH-SUMMARY): I read no paper and no table
first-hand unless a cell says otherwise. Nothing here is PRIMARY-VERIFIED-LOCALLY unless stated.

## SUMMARY TABLE

| table | S0 | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|
| 11 APN permutation, dim 8 | PASS | PASS (degenerate: min-delta reading, flagged) | PASS | PASS on headline side (1993 move, degenerate); count side conditional on tentative SEARCH-NEW | PASS headline side; CANNOT EVALUATE count side | PASS |
| 12 Perfect 1-factorisation, smallest open order (K_64) | PASS | PASS (route b) | PASS | FAIL (SEARCH-REPEAT, single-sourced) | PASS | PASS |
| 13 K(n,1), smallest open length (n=10, RECALL) | CANNOT EVALUATE | PASS (route a, definitional; bound values RECALL) | PASS | CANNOT EVALUATE | CANNOT EVALUATE | PASS (RECALL) |
| 14 Moore graph (57,2) | CANNOT EVALUATE | CANNOT EVALUATE | PASS | CANNOT EVALUATE | CANNOT EVALUATE | PASS (RECALL) |
| 15 SRG smallest open feasible set | CANNOT EVALUATE | CANNOT EVALUATE | PASS | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |

Tables 13-15 were written after WebSearch became unavailable (session budget exhausted, then a further search was declined). They rest on RECALL and local computation only. CANNOT EVALUATE there means no current source was read this session, not that the recalled value is doubted.

---

## Table 11. APN functions — an APN permutation in dimension 8

```
TABLE       | Known-APN-functions tables: (i) Boolean Functions wiki, Univ. of Bergen, boolean.wiki.uib.no, page "CCZ-invariants for all known APN functions in dimension 8" (search snippet says the page documents 8192 functions, i.e. a pre-2021 count; last-update date NOT FOUND — page not readable, WebFetch blocked); (ii) the de-facto current lists are the Zenodo datasets of the papers: zenodo.org/records/16752428 (3,775,599 new quadratic APN, published 2025) and zenodo.org/records/22010376 (classification of quadratic APN up to EA-equivalence, "BLLPR26", 2026; exact date not seen) | SEARCH-SUMMARY
AI ACTIVITY | NONE FOUND — searches: "AlphaEvolve OR FunSearch OR reinforcement learning APN function search almost perfect nonlinear dimension 8 permutation" (results were generic AlphaEvolve pages and unrelated APN papers; no APN-specific LLM/RL paper); "APN permutation dimension 8 SAT solver OR machine learning OR neural search 2025 2026" (nothing relevant; only a 2020 exhaustive-search paper on linearly self-equivalent APN permutations). A negative from WebSearch only; arXiv listing not browsable.

RECORD      | 11 — APN permutation of F_2^8 (Big APN problem), plus count of CCZ-inequivalent APN functions in dimension 8
QUANTITY    | (headline) delta_min(8) = min differential uniformity over permutations of F_2^8 (an APN permutation exists iff delta_min(8)=2); (secondary, as the brief asks) number of known CCZ-inequivalent quadratic APN functions on F_2^8
LOWER       | headline: delta_min(8) >= 2 (trivial: every function on F_2^n, char 2, has differential uniformity >= 2; existence of delta=2 open) | RECALL (definition-level) | EXACT / UNKNOWN(refereed status not applicable)
            | count: >= 3,808,491 known quadratic CCZ-inequivalent APN functions in dim 8 = 32,892 previously known + 3,775,599 new (Beierle-Langevin-Leander-Polujan-Rasoolzadeh, arXiv 2508.04644, Aug 2025; v2 in 2026). Sum derived by me: 32,892 + 3,775,599 = 3,808,491; the search summary also states "at least 3,808,491" | SEARCH-SUMMARY | EXACT (each function is an explicit look-up table; pairwise inequivalence shown via ortho-derivatives per the summary) / PREPRINT (arXiv; presented at BFA Sept 2025 per summary; journal status not seen)
UPPER       | headline: delta_min(8) <= 4, witness = the inverse function x^{-1} on F_2^8 (Nyberg 1993; used in the AES S-box) | SEARCH-SUMMARY (search summary: "Nyberg proved the multiplicative inverse ... 4-uniform"; "best known differential uniformity ... in dimension 8 ... AES") | EXACT / REFEREED (Nyberg 1993, standard)
            | count: NO published upper bound found. Estimate only: "about six million" total quadratic classes (same 2025 paper) | SEARCH-SUMMARY | NUMERICAL (non-rigorous estimate) / PREPRINT. Two earlier conjectures, both now exceeded: > 50,000 (Yu-Perrin) and > 92,515 (Polujan-Pott, = number of quadratic (8,4)-bent classes) — SEARCH-SUMMARY
BOUND OBJ   | lower: headline side is trivial (delta>=2); nonexistence of an APN permutation would be PROOF; count side: WITNESS (each new APN function is a finite look-up table, APN property decided by finite computation) ; upper: headline side: WITNESS (inverse function, or any permutation with delta=4; an APN permutation would be a WITNESS of delta=2); count side: NONE (only an estimate)
S0 OPEN     | PASS — 2025-2026 search summaries state existence of an APN permutation in even dimension n>=8 is open ("Big APN problem"); only known even-dimension APN permutation is Dillon's dimension-6 one (Browning-Dillon-McQuistan-Wolfe 2009). The 2025 paper (per summary) states none of its millions of quadratic functions is CCZ-equivalent to a permutation. Later papers seen only as titles/summaries: arXiv 2606.11967 (June 2026), 2609.22394 (Sept 2026), eprint 2026/1012: none reported a resolution. Resolution claims found: NONE (search "big APN problem 2026 APN permutation even dimension n=8 existence claim nonexistence partial result"). Withdrawn/unrefereed claims found: none. | SEARCH-SUMMARY
S1 COUPLED  | PASS, but DEGENERATE — route (a): the headline is equivalent to the extremum delta_min(8) = min over finitely describable objects (permutations of F_2^8) of delta; any single permutation is a one-sided (upper) bound; the published upper bound is 4 (inverse function) so the only possible move of a published bound is 4 -> 2, i.e. the resolving witness itself. The count of CCZ classes is a different quantity (functions, not permutations) and does NOT bound the headline; I do not count it as coupling. The adjudicator should decide whether an existence question reformulated as a min-delta extremum satisfies the intent of S1 — I flag it rather than settle it. Citation for extremal characterisation: definition of APN (delta=2 is the minimum); Nyberg 1993 for the bound 4 | SEARCH-SUMMARY (bound 4), RECALL (definition)
S2 VETO     | PASS — witness predicate ("F is a permutation of F_2^8 and every nonzero-input difference equation F(x+a)+F(x)=b has <=2 solutions") is decidable by a terminating computation (255 x 256 checks); bound object is not an ALGORITHM.
MOVE-1      | headline side (upper bound delta_min(8) <= 4): 1993 | Nyberg | delta=4 via x^{-1} | ANALYTIC | explicit formula, proved 4-uniform for even n; no computer search | SEARCH-SUMMARY ("Nyberg proved ... 4-uniform") — the only move ever made on this side; nothing since.
            | count side (for completeness) 2025-08 | Beierle, Langevin, Leander, Polujan, Rasoolzadeh | +3,775,599 -> >=3,808,491 | SEARCH-NEW (tentative) | "key starting point is a vectorial (8,4)-function that is bent, whose output space is then extended one dimension at a time"; "two construction strategies based on vectorial bent functions and an extensive computer search"; the previous 32,892 came from EP09 (22), YWL14 QAM (8,157), WTG13 (10), Taniguchi (2), BL22 (12,921), YP22 (5,412), BLP22 (6,368) — none bent-seeded. Caveat: I read only abstract-level summaries; the earlier trims-and-extensions paper (BLP22, arXiv 2108.13280) also used extension steps, and I could not read either paper to see whether the 2025 authors describe the bent-seeded route as new. | SEARCH-SUMMARY
MOVE-2      | headline side: NONE. count side: 2021-08 (arXiv 2108.13280; DCC 2022) | Beierle, Leander, Perrin ("Trims and Extensions of Quadratic APN Functions"; "BLP22" in the 2025 paper's breakdown — author list of BLP22 from RECALL, the search summaries gave only the label) | +6,368 | UNKNOWN (the title says extensions; I did not read what the paper did) | SEARCH-SUMMARY. Earlier count moves: 2021-05 Yu-Perrin +5,412 (QAM method, "modifying the last two columns of a given QAM") SEARCH-REPEAT-of-QAM (tentative; QAM introduced by Yu-Wang-Li 2014) ; 2020-09 Beierle-Leander (arXiv 2009.07204) +12,921 (linear self-equivalences + recursive tree search; SEARCH-NEW tentative) ; 2014 Yu-Wang-Li +8,157 (QAM; SEARCH-NEW). All SEARCH-SUMMARY.
S3 IDEA     | headline side: PASS on its face (most recent move = 1993, ANALYTIC) — but degenerate: the side has not moved in 33 years, so the gate says nothing about current momentum. Count side: PASS conditional on the tentative SEARCH-NEW label (would be CANNOT EVALUATE if the label is treated as UNKNOWN because I could not read the paper's novelty claim). I give both and issue no single verdict beyond that.
S4 CROWDED  | headline side: PASS — searched: AlphaEvolve/FunSearch/RL + APN; SAT/ML + APN permutation dim 8; "big APN problem 2026"; found no move on this side at all since 1993 and no AI-driven attempt. Count side: CANNOT EVALUATE — it moved 2025-08 (after 2025-01-01) via "extensive computer search" producing a 3.4 GB dataset; not AI-driven as far as I saw, but whether that counts as "large-scale optimisation tooling" is a judgement about compute scale I have no evidence on (core-hours not seen).
S5 DELIVER  | PASS — headline: a named published bound / named open problem ("Big APN problem"; Dillon's dim-6 permutation is the only known even-dimension APN permutation) would change, and the Bergen wiki APN tables would gain an entry. Abstract sentence: "We construct an almost perfect nonlinear permutation of F_2^8, resolving the Big APN Problem in dimension eight." (Note: the sentence describes full resolution — there is no 'one-step improvement' short of it on the headline side.) | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND on the frontier parameter (dimension): quadratic APN classification reached n=7 (488 classes, per 2026 zenodo description; Springer 2022 paper "classification of quadratic APN functions in 7 variables") vs n=6 earlier — ratio < 2; searches: "classification quadratic APN dimension", "Yu Perrin QAM", "Beierle Leander". On the *count* of functions found, the 2025 method (3,775,599) vs the best earlier single method BL22 (12,921) differ by about 292x (3,775,599 / 12,921 = 292.2, my arithmetic) — but that is a count of output objects, not dimension/order/size, so I do not report it as DIVERGENCE per the brief's definition; adjudicator's call.
BITS_SEARCH | UNDEFINED — named ansatzes exist (QAM, linear-self-equivalence tree search, bent-extension) but I found no published density estimate for APN permutations in dim 8 (the only related statement seen: an exhaustive/partial search in dims 7 and 8 found none with non-trivial linear self-equivalences, arXiv 2003.12006 — an exclusion result, not a density).
VERIF CLASS | CHECK — a candidate APN permutation is verified by exact finite computation (bijectivity + differential table).
NOTES       | (1) The brief's "number of known CCZ-inequivalent APN functions in dim 8" is ambiguous between quadratic-only and all APN: every count above is quadratic; the only non-quadratic-non-monomial known example is a single function (search summary). (2) Older counts in circulation are stale: "8,192 known" (Bergen wiki snippet), "8,190 / 8,180 (Yu et al. 2014)", 12,923 / 12,921, 26,525 (Yu-Perrin) and 32,892 — all superseded by >=3,808,491. Slight inconsistencies (12,921 vs 12,923; 8,157 vs 8,180/8,190) appear across summaries — likely quadratic-only vs including non-quadratic/other functions — not resolved. (3) arXiv 2508.04644 has a v2 dated 2026; the 3,775,599 figure is in the v1 abstract; whether v2 changed it is unknown. (4) The Bergen wiki table appears stale relative to the 2025 dataset. (5) arXiv 2609.13968 ("Polujan-Pott conjecture", Sept 2026) is about a different conjecture on bent functions; not an APN count result. (6) Dead end: Langevin's "profile of quadratic APN maps" page (langevin.univ-tln.fr/project/quadapn/apn.html) appeared in search results but is egress-blocked; it may hold a maintained count.
```

---

## Table 12. Perfect 1-factorisations — the smallest open order

```
TABLE       | No single web-maintained table found. Closest sources seen: David A. Pike, "Perfect 1-Factorisations" (AARMS Graph Theory Seminar talk slides, mathstat.dal.ca/~brown/sound/AARMS/AARMSGTS-10-14-20-pike.pdf, dated 2020-10-14 by URL) and Pike's survey chapter "Perfect 1-factorizations" (ResearchGate 333352288); the Handbook of Combinatorial Designs (2nd ed., 2007) is the older standard list (RECALL). Neither was read; only search titles/summaries. Last update of any maintained table: NOT FOUND | SEARCH-SUMMARY
AI ACTIVITY | NONE FOUND — searches: "FunSearch OR AlphaEvolve OR reinforcement learning perfect one-factorization complete graph Kotzig conjecture" (results: only the K_56 paper, the July 2026 asymptotic paper, Glock et al. random-graph paper; no AI-search paper). Search budget then ran out (see NOTES), so nothing more was tried.

RECORD      | 12 — smallest even n for which existence of a perfect 1-factorisation (P1F) of K_n is open
QUANTITY    | n_open = min{ even n >= 4 : no P1F of K_n is known }; a P1F = decomposition of K_n into n-1 perfect matchings any two of which form a Hamilton cycle
LOWER       | n_open >= 64 as a statement about the state of knowledge: every even n < 64 has a known P1F: n = p+1 (p odd prime; Kotzig/Anderson), n = 2p (p odd prime; Anderson/Nakamura) or sporadic (16, 28, 36, 40, 50 from RECALL; 52 Wolfe ~2009; 56 Pike 2018/19 — 52 and 56 from search summaries) | SEARCH-SUMMARY for 52, 56 and for "smallest open case is K_64"; RECALL for 16, 28, 36, 40, 50 and the family attributions; the coverage arithmetic (below) PRIMARY-VERIFIED-LOCALLY | EXACT (each is an explicit finite object or a proven infinite family) / REFEREED for the families and K_52 (RECALL); K_56 REFEREED-status UNKNOWN (arXiv 1810.08734 v2 Jan 2019; a 2019 publication is stated in one summary, venue not seen)
UPPER       | n_open <= 64, witnessed by the fact that K_64 is not known to have a P1F: this is a statement of ignorance, not a bound with an object. There is no known nonexistence result for any even n (Kotzig's conjecture is that a P1F exists for all even n>=4) | SEARCH-SUMMARY | UNKNOWN
BOUND OBJ   | lower: WITNESS — the frontier moves up only when a P1F of the current smallest open order is exhibited (a finite object: n-1 perfect matchings, checkable in polynomial time; in practice a starter / even starter over Z_{n-2} plus fixed points that generates it); upper: NONE — nonexistence of a P1F for any n is not known, and would need PROOF
S0 OPEN     | PASS — for the specified record ("smallest even n with open existence"): search summaries say the smallest open case is K_64 (Rosa survey / Pike 2020 talk; a 2020 assessment repeated in the July 2026 arXiv 2607.09459 introduction, which says the conjecture "is far from being solved"). My own local arithmetic (below) reproduces the list of open orders 64, 66, 70, 76, 78, 88, 92, 96, 100 up to 100 exactly as quoted in a search summary. Resolution claims for n=64: none found in the searches "perfect 1-factorisation K_64 smallest open case Kotzig conjecture" and "perfect one-factorization new order found 2020 ... 2025 K_64 OR K_66 OR K_70 starter computer search" (the latter's summary: "search results do not indicate any new perfect 1-factorizations for K_64, K_66, or K_70 between 2020-2025"). Coverage of 2026 for small orders: only the July 2026 asymptotic paper (Cheng-Sgueglia, "(1-eps)n perfect matchings pairwise perfect" — a partial/asymptotic result, not a resolution) | SEARCH-SUMMARY + PRIMARY-VERIFIED-LOCALLY (arithmetic)
S1 COUPLED  | PASS — route (b): the current frontier (n_open = 64) rests on published finite certificates checked by terminating computation: Pike, "A Perfect One-Factorisation of K_56", arXiv 1810.08734 (starter construction) and Wolfe's K_52 (starter-derived even starter). Exhibiting a P1F of K_64 would move n_open from 64 to 66 (66 = 2*33, 65 not prime => not covered by the families; local arithmetic). Route (a) is not needed. Caveat for adjudicator: 'n_open' is a bookkeeping quantity (state of knowledge), not an intrinsic extremum; the coupling is through the existence witness for each order. | SEARCH-SUMMARY
S2 VETO     | PASS — the predicate (every pair of the n-1 perfect matchings has union a single Hamilton cycle) is decidable in polynomial time; the witness is a finite object; not an ALGORITHM-bound.
MOVE-1      | 2018-10 (arXiv v1 2018-10-20, v2 2019-01-20; publication 2019 per one summary) | David A. Pike | P1F of K_56; n_open 56 -> 64 | SEARCH-REPEAT | "using techniques described by Wolfe, a perfect 1-factorisation of K56 was found" (search summary of what looks like the K_56 paper/survey intro; starter approach) — i.e. Wolfe's 2009 starter method applied to the next order with more computation. Single-sourced and abstract-level; I did not read the paper. | SEARCH-SUMMARY
MOVE-2      | ~2009 | Adam Wolfe | P1F of K_52; n_open 52 -> 56 | UNKNOWN | "a starter derived even starter that induces a perfect one-factorization of K52 was found"; "10,000 hours of computing time on a cluster (166 days), 5 days real time"; "7.494 billion pairs of starters in Z_25, each producing 2^12 = 4096 even starters in Z_50" (search summary). Whether the derived-even-starter method was new in 2009 relative to earlier small orders (K_50 etc.) is not in what I saw, so kind = UNKNOWN. Described in the summary as "the first new 'small' order found in nearly 20 years". | SEARCH-SUMMARY
S3 IDEA     | FAIL — MOVE-1 is SEARCH-REPEAT (same starter technique as Wolfe's K_52, larger run). Confidence limited: this rests on one search-summary sentence; if the K_56 paper in fact introduced new pruning/search ideas the label changes. (Not CANNOT EVALUATE because one line of paper-level evidence was found; adjudicator may downgrade.)
S4 CROWDED  | PASS — the coupled side has not moved at all since Pike (2018/19). Searched: AI/FunSearch/AlphaEvolve/RL + Kotzig/P1F; "new order found 2020-2025"; "K_64 smallest open case". Found nothing on or after 2025-01-01 that changed the frontier. Caveat: WebSearch only, budget then exhausted; no arXiv listing browsed.
S5 DELIVER  | PASS — named published claim: "the smallest open case of Kotzig's Perfect 1-Factorisation Conjecture is K_64" (Rosa survey; Pike 2020 talk; Pike's K_56 paper described as settling 'the smallest unresolved case'). Abstract sentence: "We construct a perfect 1-factorisation of K_64, settling the smallest remaining open case of Kotzig's conjecture." | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — the frontier order moved 52 -> 56 -> 64 across Wolfe (~2009) and Pike (2019): ratios 1.08 and 1.14, well under 2; both used starter searches. The infinite algebraic families (p+1, 2p) reach arbitrarily large n and some large sporadic orders appear in a summary (e.g. 6,967,872 ... 22,665,188, construction not seen), but those are constructions for orders in different residue classes and do not attack the smallest-open cell, so I do not count them as two methods on the same object with a factor-2 reach gap. Searches as listed above.
BITS_SEARCH | UNDEFINED — a named ansatz exists (even starters over Z_{n-2} plus two fixed points; starters derived from starters over Z_{(n-2)/2}), but I found no published density estimate (only effort figures: 7.494 billion starter pairs / 10,000 CPU-hours for K_52, which are not a density).
VERIF CLASS | CHECK — a proposed P1F of K_64 is verified by an exact finite computation (all C(63,2) = 1953 pairs of matchings checked for a single 64-cycle).
NOTES       | (1) WEB SEARCH BUDGET: the WebSearch tool refused further calls after about 28 of my calls ("200 of 200 used" — a session-wide budget, likely shared with other workers); this table was finished before that, but Tables 13-15 had NO searches — see their blocks. (2) One search summary listed "56" among unsettled orders next to 64, 66,...; that is the pre-2019 list; the summaries that mention Pike's K_56 say 64 is the smallest open case now. (3) Local arithmetic (Python, this container): even n in [4,130) not of the form p+1 or 2p (p odd prime) and not in {16,28,36,40,50,52,56}: 64, 66, 70, 76, 78, 88, 92, 96, 100, 112, 116, 120, 124, 126 (126 and larger sporadic orders such as 126, 170 were not fed in; 126 is a known sporadic order by RECALL). Without 56 the first uncovered order is 56; without 52 and 56 it is 52. This checks that 64 is the first uncovered order *given* the family theorems and the sporadic list; it does not verify that no other P1F (e.g. K_64) has been found — that rests on the searches above. (4) 'n_open' counts orders by this arithmetic; the 14 orders listed in (3) were derived, not quoted.
```

---

## Table 13. Binary covering codes, radius 1 — the smallest open length

No web search was possible for this table. Everything is RECALL unless stated.

```
TABLE       | Kéri's tables of bounds on covering codes (Gerzson Kéri, SZTAKI, Budapest; hosted at old.sztaki.hu/~keri/codes — URL RECALL); lineage: Cohen-Honkala-Litsyn-Lobstein, "Covering Codes" (1997). Last update date NOT FOUND; table not read | RECALL
AI ACTIVITY | CANNOT EVALUATE — not searched (search budget gone before this table). Not "NONE FOUND".

RECORD      | 13 — smallest n with K(n,1) unknown
QUANTITY    | K(n,1) = min size of a binary code of length n with covering radius 1
LOWER       | K(10,1) >= 107 (attribution not recalled) | RECALL | EXACT / UNKNOWN
UPPER       | K(10,1) <= 120 (attribution not recalled; possibly Östergård-Kaikkonen 1998, unsure) | RECALL | EXACT / UNKNOWN
            | Recalled exact values for n <= 9: K = 1,2,2,4,7,12,16,32,62 for n=1..9 (K(9,1)=62 by Östergård-Blass 2001). Recalled only; this is why n=10 is the claimed smallest open length. Not verified.
BOUND OBJ   | lower: PROOF (I do not know whether by exhaustive computer search or counting argument) ; upper: WITNESS — a code with fewer than 120 words, covering radius checked by terminating computation over 2^10 words
S0 OPEN     | CANNOT EVALUATE — RECALL says 107-120 is open, but no source read this session; a stale recall is the failure mode this run warns of. No resolution claims checked.
S1 COUPLED  | PASS — route (a): K(n,1) is by definition a minimum over finitely describable objects (codes), so any covering code is a one-sided (upper) bound. The published value 120 is RECALL only. | RECALL
S2 VETO     | PASS — covering radius of an explicit code is computable by finite computation.
MOVE-1      | NOT FOUND — attribution and method of the 120 bound not established.
MOVE-2      | NONE / NOT FOUND
S3 IDEA     | CANNOT EVALUATE — kind of the latest move unknown.
S4 CROWDED  | CANNOT EVALUATE — did not search.
S5 DELIVER  | PASS (RECALL) — Kéri's table entry for n=10 would change. Sentence: "We construct a binary code of length 10 and covering radius 1 with 119 codewords, improving the upper bound K(10,1) <= 120." (The value 119 is just one step below the recalled bound.)
DIVERGENCE  | CANNOT EVALUATE — not searched.
BITS_SEARCH | UNDEFINED — no search ansatz plus published density estimate seen.
VERIF CLASS | CHECK
NOTES       | Bound values and the identity of the smallest open length are RECALL. The brief also asks for "Kéri's tables lineage"; I could not read it.
```

---

## Table 14. Moore graphs — degree 57, diameter 2

```
TABLE       | No maintained table for this record identified. Nearest: the degree-diameter problem tables (Combinatorics Wiki; RECALL, not read; I believe they only cover small degrees) | RECALL
AI ACTIVITY | CANNOT EVALUATE — not searched.

RECORD      | 14 — Moore graph of degree 57, diameter 2 (3250 vertices, srg(3250,57,0,1))
QUANTITY    | existence of a 57-regular graph of diameter 2 and girth 5 on 3250 vertices (equivalently: the degree-diameter maximum order for (57,2) attains the Moore bound 3250)
LOWER       | best known order of a (57,2) graph: NOT FOUND (not read) | - | -
UPPER       | 3250 (Moore bound, 57^2+1) | derived locally (57*57+1 = 3250) | EXACT / REFEREED (standard)
BOUND OBJ   | lower: WITNESS — a graph, checkable by finite computation ; upper: PROOF (Moore bound is a counting argument). Nonexistence of the Moore graph would be PROOF.
S0 OPEN     | CANNOT EVALUATE — RECALL: open since Hoffman-Singleton 1960 (only degrees 2, 3, 7, 57 possible). No source read; resolution or withdrawn claims not searched.
S1 COUPLED  | CANNOT EVALUATE — the natural reading is route (a) with the degree-diameter maximum, but that needs a published lower bound on the (57,2) order and I do not have one. A witness at 3250 would settle the question itself.
S2 VETO     | PASS — a graph on 3250 vertices with the stated degree and diameter is checkable by terminating computation.
MOVE-1      | NOT FOUND
S3 IDEA     | CANNOT EVALUATE — no move identified.
S4 CROWDED  | CANNOT EVALUATE — did not search.
S5 DELIVER  | PASS (RECALL) — the Hoffman-Singleton 1960 question. Sentence: "We construct a Moore graph of degree 57, a 57-regular graph of diameter 2 on 3250 vertices."
DIVERGENCE  | CANNOT EVALUATE — not searched.
BITS_SEARCH | UNDEFINED
VERIF CLASS | CHECK (for a witness)
NOTES       | Local check (PRIMARY-VERIFIED-LOCALLY): the ported Sage seems_feasible returns True for (3250,57,0,1), so parameters alone do not rule it out (feasibility only, not existence).
```

---

## Table 15. Strongly regular graphs — the smallest open feasible parameter set

```
TABLE       | Andries Brouwer's table of SRG parameters (www.win.tue.nl/~aeb/graphs/srg/srgtab.html; URL read in the Sage source docstring, SECONDARY-RELAYED). Successor: Brouwer and Van Maldeghem, "Strongly Regular Graphs" (CUP 2022) — RECALL. Last update date NOT FOUND; page not fetched (blocked host; I also did NOT fetch the copy of Brouwer's database that Sage loads from a JSON data package, because that would be a mirror of a blocked table). | SECONDARY-RELAYED (URL), otherwise RECALL
AI ACTIVITY | CANNOT EVALUATE — not searched.

RECORD      | 15 — smallest v with a feasible SRG parameter set of open existence
QUANTITY    | existence of an srg(v,k,lambda,mu) for the smallest such open v
LOWER/UPPER | no bound quantity: an existence question | - | -
BOUND OBJ   | WITNESS for existence (the graph); nonexistence would be PROOF
S0 OPEN     | CANNOT EVALUATE — I could not identify the record from a source. RECALL only: the smallest open is v=65, conference parameters (65,32,15,16); next (69,20,7,5). Not verified.
S1 COUPLED  | CANNOT EVALUATE — record unidentified; existence-only question with no bound quantity.
S2 VETO     | PASS — an SRG on v vertices is checkable by finite computation.
MOVE-1      | NOT FOUND
S3 IDEA     | CANNOT EVALUATE
S4 CROWDED  | CANNOT EVALUATE — did not search.
S5 DELIVER  | CANNOT EVALUATE — depends on the unidentified record and table date.
DIVERGENCE  | CANNOT EVALUATE
BITS_SEARCH | UNDEFINED
VERIF CLASS | CHECK
NOTES       | LOCAL COMPUTATION (PRIMARY-VERIFIED-LOCALLY, feasibility only): I ported Sage's seems_feasible (Brouwer-Lint 1984 conditions: integrality, Krein, absolute bound, claw bound, mu=1 and mu=2 cases, conference sum of two squares), read from raw.githubusercontent.com/sagemath/sage/develop/src/sage/graphs/strongly_regular_db.pyx, and ran it for v <= 100 (script in the scratchpad, srgfeas.py). Result: 156 feasible tuples, 88 with k <= (v-1)/2. Feasible parameter sets with 60 <= v <= 70 (k <= (v-1)/2): (61,30,14,15), (63,30,13,15), (64,14,6,2), (64,18,2,6), (64,21,8,6), (64,27,10,12), (64,28,12,12), (65,32,15,16), (66,20,10,4), (69,20,7,5), (70,27,12,9). Also feasible below 60 and worth a source check: (50,21,8,9), (57,14,1,4), (57,24,11,9). This shows which sets are candidates; it says NOTHING about which are open. Sage's docstring says that for v<60 all apparently feasible sets have existence True except that (49,16,3,6) does not exist, which suggests none open below 60, but that is a snapshot of unknown date and I did not read it as a table. Status of (50,21,8,9), (57,24,11,9), (63,30,13,15) is not something I can state from a source. I later ran (3250,57,0,1) through the ported checker: True. Sage's database snapshot statistics (462 impossible, 2911 undecided, 1165 realizable entries) are from the docstring; date unknown.
```

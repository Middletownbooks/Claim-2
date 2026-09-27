# Rescan of the 499-record corpus for low-impact fallbacks

**Headline: the corpus is a poor source of targets under this project's screen, and that is
worth knowing before anyone trawls it.** Four records in the entire low-impact tail survive, three
of which this project already had. The corpus's real contribution is something else — it attaches
**collaborative leads** to items we hold.

## 1. What "low impact" means here, and it is a field

`ranking_v16.json` → `publicBoundary`: *"This is an editorial ranking of the importance of
canonical mathematical questions… Rank and comparison ranges are not proof evidence, difficulty,
tractability, or a forecast of progress."* So `releaseRank` **is** the impact rating, 1 = highest,
and "lower impact" is the tail. 499 records, ranks 1–500, 54 of them at rank ≥ 350 in the
discrete / TCS / crypto / number-theory domains.

## 2. The premise test, run first, and it is INCONCLUSIVE

The strategic case for the tail is `RESULT_GAP_v2.md` §7: the highest-scoring items are the ones
already taken. Testable — do the benchmark designers cluster at the top of this ranking?

Matching Epoch's 41 unsolved entries against the 499 by title similarity: **only 7 match at all,
and 2 of those are false** (Conway's 99-graph → "Graph reconstruction conjecture"; "Elliptic
Curves with Prescribed Number of Points" → "Parity conjecture"). Five genuine matches, at ranks
21, 299, 335, 382, 405.

**Five points cannot establish a rank correlation.** Recorded as inconclusive rather than dressed
up. The useful thing it does show is §3.

## 3. The lists are near-disjoint, and that is the real measurement

| pair | overlap |
|---|---|
| Epoch's 41 unsolved ∩ the 499 corpus | **5 of 41** |
| our vetted pool (24 topics) ∩ the 499 corpus | 9 topics present, **4 usable** |
| our vetted pool ∩ Epoch's 41 | 2 of 16 pool items (U6, U7) |

Fifteen of the twenty-four topics this project has already vetted are **absent from the 499
entirely**: skew-Hadamard, Williamson, Steiner systems, difference sets, Costas arrays, bent
functions, APN permutations, perfect 1-factorisations, D-optimal designs, covering codes, PTE,
cap sets, snake-in-the-box, Moore graphs, strongly regular graphs.

That is not a gap in the corpus — it is what an **editorial importance ranking of canonical
questions** selects for, which is not what a **finite-witness screen** selects for. The two
criteria are close to orthogonal.

**Consequence for `RESULT_GAP_v2.md` §7**, which worried that the commons is being strip-mined:
overstated. Three curated lists built by serious people overlap pairwise at 5–20%. There is more
room than any one list suggests — and each list is a poor proxy for the others, so "not on
Epoch's list" is weak evidence of anything.

## 4. The screen, and its honest limit

`screen_500.py` filters the tail on witness language, tail language, a named finite parameter and
domain. It is a **proxy** and it says so: 107 of 250 tail records pass, which is too many to be a
verdict and is meant as a pool to read.

**The screen this project actually needs cannot be mined from this corpus.** A regex hunt for the
writable-unknown-set shape — *"smallest open"*, *"remains open for"*, *"the only remaining case"* —
returns **zero records at rank ≥ 200**. The corpus carries canonical problem *statements*; the
`statusQualification` fields are provenance boilerplate, not inventories of which cases are open.
So the third screen category has to be applied by reading the mathematics, which is what §5 does
and which is why §5 is short.

## 5. What survives — four records, and three are ours already

Everything in this section is my **reading**, marked as such. Nothing below is verified; the gate
in `GATE_FALLBACKS.md` is what verifies it.

| rank | record | witness | unknown set | note |
|---:|---|---|---|---|
| **393** | **CC-6 — projective plane of order 12, or any non-prime-power order not killed by Bruck–Ryser–Chowla** | one incidence structure on 157 points, checkable in milliseconds | **finite list below a ceiling** — 12, 15, 18, 20, 21, 22, … | **the only new one**, has a collaboration route, and it is the same shape as Hadamard |
| 349 | CC-8 — exact kissing numbers, *n* > 4 | a spherical code is a finite point set (lower-bound records only; the exact value needs an upper-bound proof) | finite list of dimensions 5–7, 9–23 | this is our pool item **U8** |
| 426 | Maximal MUBs in composite dimensions | a set of bases in ℂ⁶ | single named instance | our **C6** — but see the correction below |
| 331 | The Hadamard Matrix Existence Conjecture | — | — | our primary target; **it has a collaboration route we were not using** |

**A correction on 426 worth carrying.** The corpus asks *"decide whether K = 7 MUBs exist in
dimension D = 6"*. Our C6 asked whether **4** exist. Three are known; the Zauner MUB conjecture
says three is the maximum. Seven is the extreme end and essentially nobody expects it; **four is
the frontier**. The corpus statement is the weaker question, and a cheaper instance reading the
corpus alone would attack the wrong end.

**And what did not survive, with the reason**, because these are the near-misses a rescan will
keep re-proposing:

- *Shannon Capacity of Finite Graphs* (434) — the corpus target is **computability of Θ(G)**, a
  decidability question with no finite witness. The famous Θ(C₇) sub-question is not what is
  recorded.
- *Zarankiewicz* (413), *Beck–Fiala* (352), *Turán density of K₄⁽³⁾* (366), *Ruzsa–Szemerédi*
  (479) — all recorded as **asymptotic order** questions. No finite object settles them.
- *Voronoi parallelohedra* (493), *Hadwiger–Boltyanski illumination* (454), *Lovász
  vertex-transitive Hamiltonicity* (429) — finite witness, but the unknown set is **a prefix with
  an open tail** in the dimension or the order. That is the SIC shape this project learned to
  reject.
- *Frankl union-closed* (403), *Tutte 3-flow* (355), *List edge-colouring* (495), *Erdős
  matching* (458) — finite witness, unknown set is "all finite graphs / all families". Not
  writable.

## 6. What this means for the fallback queue

The queue is **CC-6 and nothing else new**. CC-8 and the MUB item were already in the pool and
neither improved on inspection. The honest reading is that this rescan produced **one candidate
and one methodological correction**, and the correction may be the more valuable of the two:
*being absent from a curated list is weak evidence, because the curated lists barely overlap.*

Gate bars for CC-6 are registered in `GATE_FALLBACKS.md` **before** any search, single-threshold
and no middle band, per D44. The reachability bar leads, because reachability is what killed
PTE 11 and the unsearched rings and neither was screened for it in advance.

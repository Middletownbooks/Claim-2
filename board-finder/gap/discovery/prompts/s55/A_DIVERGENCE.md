# Brief A — the divergence search. The one instrument on this board that generates rather than filters.

**For a Sonnet 5.5 instance in a chat conversation with web search and page fetching. No repository,
no filesystem. Your output is a document in your reply.**

This is the highest-value unfinished item on the board, and it has **never produced a single
observation**. The earlier run's worker read 67 problem pages and 10 notebooks and was then cut off
at a concurrency cap *before recording any entry*. The run's own note: *"The instrument did not run,
which is different from running and returning nothing."*

Everything this project has ever tried **filters** lists of problems. This brief tests whether the
thing worth finding can be **found directly**.

## Why you are being asked, and it is not that the last run was careless

An earlier run of this work was done by nine parallel agents inside a container whose network
**blocked arxiv.org, Wikipedia, every publisher, and every maintained-table host it probed** — Cohn's
kissing tables, the La Jolla difference-set repository, Brouwer's tables, Packomania. Only web search
and `raw.githubusercontent.com` were reachable.

That run's own provenance rule says a cell seen **only in a search-result summary** is
`SEARCH-SUMMARY`, which is **RECALL-grade and not usable for any gate**. So almost every literature
verdict it produced rests on a tier that cannot support it, and the run says so itself: *"in this
environment almost every literature cell will be `SEARCH-SUMMARY`, so no survivor of this run can be
more than triage-grade."* Two of its arms also stopped on a concurrency cap and a search budget
rather than on evidence.

**You can reach the hosts it could not.** That is the entire reason this is being re-run, and it is
your job: **move cells from `SEARCH-SUMMARY` to `SECONDARY-RELAYED` by reading the source itself.** A
verdict you return at `SEARCH-SUMMARY` adds nothing that is not already on file.

## Provenance tiers. Every cell you report carries one.

| tier | meaning | usable for a gate? |
|---|---|---|
| `PRIMARY-VERIFIED-LOCALLY` | you computed or checked it yourself | yes |
| `SECONDARY-RELAYED` | **you read the source text itself** — the table page, the paper, the repository file | yes |
| `SEARCH-SUMMARY` | seen only in a search result's title or snippet; source not opened | **no** |
| `RECALL` | you believe it; no source found | no |

Every value also carries **EXACT / RIGOROUS-NUMERIC / NUMERICAL / UNKNOWN** and **REFEREED /
PREPRINT / ANNOUNCED / WITHDRAWN**.

**Do not upgrade a tier to make an entry count.** A `SEARCH-SUMMARY` cell reported honestly is worth
more than a `SECONDARY-RELAYED` cell you did not earn — the project's worst near-miss was a
nine-year-stale recall that would have produced an entirely fictitious worklist.

## Two rules that have cost this project more than any others

**Numerical is not exact, and claimed is not refereed.** A breadth pass once reported exact SIC-POVM
constructions *"reaching d = 19,603"*; a dedicated check had already established the exact ceiling
was **5,779**, with the higher papers admitting their verification was *"mostly partial."* Both cells
were true at their own precision; one was usable. **Where a value's meaning depends on which sense is
meant, report both senses rather than picking one.** Watch especially for *projective* versus
*affine*, *numerical* versus *exact*, and asymptotic constants versus finite instances.

**Withdrawn and unrefereed claims are data, not resolutions.** A claimed full resolution of the
anisotropic Calderón problem was posted and withdrawn days later by its own authors — *"the argument
is incorrect"* — and still recirculates in citation lists. If you find a record claim, check whether
it stands.

## Budget, and the failure this replaces

The earlier run died on search limits. **So: a hard cap per brief, stated in the brief, and a
partial report is a success.** Stop at the cap and report what you have, marking the rest NOT
REACHED. Do not silently run dry. A brief that returns three solid `SECONDARY-RELAYED` rows and
names the rest as unreached is worth more than one that returns ten `SEARCH-SUMMARY` rows.

## You have no repository

Everything you need is inside your brief. Return your output **in your reply**, as a single
document. Do not ask for files and do not assume you can write any.


## Fetch mechanics, learned the hard way on Brief A — read this before your first call

Brief A lost four of its 22 calls to two mechanics. Both are avoidable:

* **The fetch tool only opens a URL that a search result (or this brief) has already surfaced.** A bare
  hostname written in a brief was **refused** until a search had produced it. So for every maintained
  table below: **search for it first, then fetch from the result link.** Budget one search plus one
  fetch per host, not one fetch.
* **arXiv is rate-limited rather than blocked, and asymmetrically.** Older identifiers opened;
  a September 2026 identifier was refused three times in a row. If a recent paper refuses, **do not
  retry more than once** — spend the call elsewhere and mark the cell NOT REACHED.

A third mechanic, worth knowing because it invalidates a cell rather than costing a call: **a live
artifact can change while you read it.** On Brief A a GitHub README showed ten dimensions in the
search snapshot and nineteen when fetched, with one record's claimed increase shrinking 44.4%. If a
value moves between your search and your fetch, **report both and gate on neither.**

---

## 1. What a divergence is. Registered definition, verbatim — you may not loosen it.

> Two dated, published methods on **the same object**, whose reach differs by a **factor ≥ 2 in the
> frontier parameter itself** (order, dimension, length — **not** in runtime), both at
> `SECONDARY-RELAYED` or better. `SEARCH-SUMMARY` divergences are reported as leads, never counted.

**Why this matters.** This project's one live target has a measured idea gap: on the same object —
Hadamard matrices under one orbit ansatz — a published method's search cost grows with exponent
≈0.25 while this project's own grows with **0.503**. A factor of two in reach, stated as a number.
A difference like that says **an idea exists that one party has and another lacks**, and it is
visible from outside without solving anything.

**~~Right shape:~~ ~~*"method A enumerated all Costas arrays up to n = 29; method B, published
earlier, reached n = 14"* — ratio 29/14 ≈ 2.07.~~ WRONG — and it was my worked example.** A run of
this brief found **no source for a 14**: the 1988 Costas count was fitted to known C(n) for n ≤ **17**,
which gives 29/17 = **1.706**, below the very threshold the example was illustrating.

**Right shape, substituted and sourced:** *"Fiedler (2013) exhaustively enumerated all complex Golay
pairs through length 28; Holzmann–Kharaghani (1994) reached length 13"* — 28/13 = **2.154** in the
frontier parameter, which is a length. **Read its flaw too, because it is the flaw of the whole
definition:** those two are nineteen years apart with a 2002 paper at length 19 between them, so
against the *nearest* predecessor the ratio is 28/19 = 1.474 and fails. A ratio against a distant
predecessor measures the field's progress, not a gap anyone is currently on the wrong side of.

**Wrong shape, and both of these were found by the earlier run and correctly refused:**
* *"our solver is 100× faster"* — runtime, not reach.
* APN functions in dimension 8: the 2025 method's **output is 292× larger** than the best earlier
  single method. **The frontier parameter is a count of objects, not a reach.** Refused.
* the real Grothendieck constant: the 2026 lower bound came from an asymptotic argument that explicit
  low-dimensional instances had not reached in 35 years. **A divergence in method class, not in a
  frontier parameter.** Refused.

Keep those three refusals in mind — they are the boundary of the definition, and two of them look
like divergences until you ask what the parameter is.

**Hadamard matrices at order 2092 are excluded** — already held.

---

## 2. Where to look, in this order, once each

**(a) SAT/CAS and exhaustive-enumeration papers in combinatorics.** These are the richest seam
because such papers routinely state *"previous methods reached n = X"* in their own introductions,
which is exactly the datum you need, at `SECONDARY-RELAYED`, from one fetch. Specifically:
Williamson matrices, Lam's problem (projective plane of order 10), the Keller conjecture, Schur
numbers, the empty-hexagon problem, small Ramsey numbers, Steiner triple system enumeration, Costas
array enumeration, bent-function counts.

**(b) The AI-era record problems, 2023–2026.** FunSearch (cap sets, admissible sets), the AlphaEvolve
problem repository — `github.com/google-deepmind/alphaevolve_repository_of_problems`, whose
`experiments/` notebooks state reaches directly — circle packing, kissing-number constructions, sums
and differences of sets. The Qiushi Engine paper (arXiv:2609.35051) is unusually good source material
here: §1.3 *"Relation to earlier constructions"* explicitly compares its reach against named
predecessors, table by table.

**(c) The fifteen record tables** this project tracks: kissing numbers, caps in AG(n,3),
snake-in-the-box, D-optimal designs, skew-Hadamard, Williamson, Steiner systems, cyclic difference
sets, Costas arrays, bent functions, APN functions, perfect 1-factorisations, binary covering codes
radius 1, Moore graphs, strongly regular graphs.

**Prefer (a).** The earlier brief listed it third; it should be first, because a paper's own
introduction comparing its reach to its predecessor's is a divergence served at the right tier for
one fetch, and that is the cheapest `SECONDARY-RELAYED` cell available anywhere in this work.

---

## 3. Budget

**Stop after 25 searches-or-fetches, or after 12 entries, whichever comes first.** Then report. If
you stop on the cap, say which of (a), (b), (c) you did not reach. **A partial report is a success.**

---

## 4. Output — one block per divergence or lead

```
OBJECT       | <the object, and the frontier parameter, named>
METHOD A     | <paper, date> | reach <value> | <tier> | <EXACT|NUMERICAL|…> | <REFEREED|PREPRINT|…>
METHOD B     | <paper, date> | reach <value> | <tier> | <…> | <…>
RATIO        | <A/B in the frontier parameter — computed, and show the arithmetic>
SAME OBJECT? | <YES|NO|UNCLEAR — same ansatz, same problem statement? be strict>
PARAMETER OK?| <is the ratio in a REACH, or in runtime / a count of outputs / a method class?>
COUNTS?      | <YES — both reaches SECONDARY-RELAYED or better AND ratio >= 2 AND parameter is a reach | LEAD — say which condition failed>
STILL OPEN?  | <has the lagging side caught up since, or is the gap live?>
NOTES        | <…>
```

**Also report a call ledger** — calls used against the cap, and every failed call with its cause. The
first run of this brief did that unasked, and its four failure lines are what identified the fetch
mechanics above.

Then, at the top of your reply:

1. **Two derived lists** — entries that COUNT, and LEADS. Count them.
2. **The searches that found nothing**, named. Negative coverage is the result when there is no
   positive one.
3. **Anything that contradicts this brief.** Several figures here are relayed; if one is wrong, that
   is the most useful thing you can report.

**Do not recommend what to do next.** The entries and their tiers are the deliverable.

## 5. What success looks like

A registered prediction says this search finds **at least one** divergence meeting the definition,
and that **zero means the signal does not generate**. Both outcomes are informative and the second is
publishable on this board. **One entry that genuinely COUNTS is worth more than ten leads** — but
leads reported honestly, with the failing condition named, are what let the definition be tightened
or loosened later on evidence.

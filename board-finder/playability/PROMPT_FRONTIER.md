# The frontier-verification prompt

**For a Claude with web search and fetch, not for a coding agent.** The task is lookup
and quotation, not computation. A code sandbox would invite sweeping when the whole point
is to find out what bounds a sweep before anyone runs one.

**Why this one first.** Three documents in this directory converge on the same gate:

* `FEASIBILITY.md` §5 — *"Every [recall] cell is unverified… they are the first thing to
  check with a network connection."*
* `FEASIBILITY.md` §6, the operating rule — *"Look up the frontier to find out whether the
  remaining work is deep or broad, then build the harness if and only if it is broad."*
* `RANKING_FIT.md` §4 — a registered prediction about four records, *"carry it as the next
  thing to verify."*

Of 35 playable records, 12 are BOUNDED (real candidates conditional on a frontier lookup)
and 9 are FRONTIER-limited, where the published frontier *is* the entire question. That is
21 records gated on one afternoon of reading, and no harness should be built before it.

---

## Part A — paste from here

> You have web search and fetch. Your job is to **verify or correct a list of factual
> claims about computational frontiers**, and nothing else. Do not attempt any of the
> mathematics, do not start a search or a sweep, and do not estimate a frontier you cannot
> source.
>
> ### The rules, which matter more than the coverage
>
> **1. Every cell needs a source or the answer `NOT FOUND`.** `NOT FOUND` is a real answer
> and a useful one — it means the fact is not readily available, which is itself a finding
> about the record. Never fill a cell from memory. If memory is all you have, the verdict is
> `NOT FOUND` with a note saying what you believe and that it is unsourced.
>
> **2. Every confirmed number needs a verbatim quoted sentence containing that number**,
> plus the URL and the source's date. *"Verified to 4·10¹⁸"* is the shape of a sentence that
> gets produced whether or not it is true, and unlike a vaguer claim it **looks** checkable,
> so it survives review. A quote with the number in it is the only thing that does not.
>
> **3. Date every frontier.** A sweep limit from 2012 and one from 2025 are different facts
> about whether work remains. Give the date of the source and, where the source says it, the
> date the computation finished.
>
> **4. Separate the frontier from the wall.** The frontier is where someone stopped. The
> wall is why. Report both, and say which one your source actually states — sources usually
> give the first and imply the second.
>
> **5. For each record, answer: is the remaining work DEEP or BROAD?**
> *Deep* = one pipeline pushed as far as specialist compute reaches (more compute, same
> method). *Broad* = many small independent constructions or families, each cheap, nobody
> having had the patience to do all of them at once. If you answer BROAD, name the families
> or cases and roughly how many. This single field decides whether the work is worth
> starting, so do not leave it blank and do not guess it from the problem's fame.
>
> ### What to check, in this priority order
>
> Stop when you run out of budget and report what you have — a half-finished sourced pass is
> worth more than a complete unsourced one. Respect the order.
>
> **(i) The registered prediction — four records, answer both branches explicitly.**
> Records 287 Alperin–McKay, 300 Alperin weight, 356 Brauer k(B), 472 McKay–Navarro.
> The claim to test: *these carry reduction theorems to an inductive condition on finite
> simple groups, so a counterexample search is a structured list rather than a combinatorial
> explosion, and the character-theoretic predicate is implemented in GAP's table library.*
> The prediction: **if that reads as tractable, someone has already swept the small groups
> and published it.** Find the sweep, or establish that it is not there. **Both branches are
> findings, and the absence is the more interesting one.** For each of the four, say
> separately: (a) does a reduction exist and to what condition; (b) how much of the
> classified list has been discharged, by whom, when; (c) is the predicate really in GAP's
> library. The note on 356 says its reduction is *weaker* than the other three and the writer
> was **not confident** — that is the cell most likely to be wrong.
>
> **(ii) The nine frontier-limited records**, where the frontier is the whole value:
> 9 GRH, 22 Goldbach, 161 Collatz, 239 odd perfect numbers, 273 Kummer–Vandiver,
> 307 Legendre, 348 Beal, 488 second Hardy–Littlewood, 500 Lehmer's τ.
> For each: the current published frontier, with a quote; who pushed it and when; and
> whether anything suggests the next push is cheaper than the last.
>
> **(iii) Four specific recalled numbers, each of which may be wrong:**
> * 22 Goldbach — believed verified to about 4·10¹⁸.
> * 322 graph reconstruction — believed exhaustive to n = 11.
> * 390 Pythagorean-triple partition regularity — believed the 2-colour case was a 200TB SAT
>   proof, with 3 colours far larger.
> * 493 Voronoi conjecture — believed proven for dimension d ≤ 5, with d = 6 parallelohedron
>   enumeration as the wall.
>
> **(iv) Two adjacent-result claims that carry a recommendation each:**
> * 280 Kaplansky's idempotent conjecture. The claim: the neighbouring **unit** conjecture
>   fell to a computer search — believed Gardam, 2021, in the Promislow group over 𝔽₂. Verify
>   the unit-conjecture result and its method, then find whether anyone has pointed the same
>   method at the **idempotent** conjecture, and what stopped them. This is the strongest
>   single recommendation on the board and it rests on a recalled citation.
> * 488 second Hardy–Littlewood. The claim: the witness question factors, and the *cheap*
>   factor is combinatorial — whether an admissible pattern of diameter y can hold more than
>   π(y) elements, believed to happen somewhere past y ≈ 1600 (the Hensley–Richards route).
>   Verify the result, and give the **smallest y for which an admissible set exceeding π(y)
>   is known**, with a quote. If that number exists, a computation that was skipped here
>   becomes checkable.
>
> **(v) One credit claim, flagged as unverified by the people who recorded it.**
> Record 331 Hadamard. The claim: twelve previously-open Hadamard orders were closed over a
> weekend by an agent sweeping construction families, with Claude credited alongside other
> researchers, and only order 668 independently checked. Cited sources:
> `github.com/bbeartheancient/hoa64` and
> `epoch.ai/frontiermath/open-problems/hadamard`. Establish what actually happened: which
> orders, verified by whom, and whether the constructions were executed and checked or only
> supplied. Say plainly if the record overstates it — this claim is currently doing work in a
> reclassification, so getting it wrong is expensive.
>
> ### Output
>
> A JSON array, one object per record, using exactly these keys so it merges into an existing
> dataset:
>
> ```json
> [{"rank": 22,
>   "claimAsGiven": "verified to about 4e18",
>   "verdict": "CONFIRMED | CORRECTED | NOT FOUND | CONTRADICTED",
>   "frontier": "what the frontier actually is",
>   "wall": "what stops the next push, and whether the source states it or you infer it",
>   "sourceUrl": "...",
>   "sourceDate": "YYYY-MM-DD or as given",
>   "quote": "a verbatim sentence from the source containing the number",
>   "depthOrBreadth": "DEEP | BROAD",
>   "breadthDetail": "if BROAD: the families or cases, and roughly how many",
>   "witnessCheckFeasible": "FEASIBLE | BOUNDED | FRONTIER | HOPELESS — your verdict now",
>   "changedFrom": "the verdict you were given, if yours differs",
>   "note": "one or two sentences, including anything that surprised you"}]
> ```
>
> Then, in prose after the JSON, three short sections:
>
> **A. The prediction.** Swept and published, or absent? Quote what settles it.
>
> **B. What you would start, and what you would drop.** At most three records to start and
> at most three to drop, each with the one fact that decided it. Rank the starts.
>
> **C. Recall against source — answer this last.** Before you searched, which of these
> frontiers did you already believe you knew? For each, say whether the search **confirmed**,
> **corrected** or **failed to settle** it, and give the count. Answer honestly; a wrong
> recall that the search corrected is the single most useful line you can write here, because
> it calibrates how much the unsourced cells elsewhere in this project can be trusted.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each clause is built against

| clause | the observed failure |
|---|---|
| source-or-`NOT FOUND`, never from memory | the entire `FEASIBILITY.md` §3 justification set is `[recall]`, and the file says so — the point of this run is to replace those cells, so a run that produces more of them has done nothing |
| a **quote containing the number** | `PROMPT_WITNESS.md` Part B: *"verified to 10^20 is the shape of a sentence a model will produce whether or not it is true, and unlike a board-search claim it looks checkable, so it survives review"* |
| date every frontier | class (c)'s entire value is *where the sweep stopped*; an undated frontier does not answer that |
| frontier **and** wall, separately | `FEASIBILITY.md` §3(b): for 21 of 35 records "value lives entirely in whether the wall has moved". A frontier without a wall cannot tell you that |
| DEEP or BROAD, mandatory | the one target on this board that has actually paid (331 Hadamard) was mis-screened as *saturated* by a "has this been worked?" heuristic. Specialists saturate depth, not breadth. This field is the correction, and leaving it blank reinstates the error |
| both branches of the prediction are findings | registered in `RANKING_FIT.md` §4 before any lookup, precisely so that "no sweep exists" cannot be quietly reported as a null result |
| 356 flagged as the least confident cell | the writer said so in advance. A verifier that confirms every cell including that one has probably not searched |
| **do not compute** | the one sweep run here measured the *hard* factor of a two-factor question and missed that the cheap factor was the whole game (`FEASIBILITY.md` §1). "What bounds the search" was answerable before running anything. This prompt is that step, and letting the executor compute would repeat the error |
| §C recall-against-source, asked last | it turns the run into a **measurement of model recall on frontier facts**, over ~20 cells with a ground truth found in the same session. This project tags unsourced cells `[recall]` throughout; nobody has measured what that tag is worth |

### Scoring

Primary outcome is **not** how many records get confirmed. It is:

1. **Sourced-cell rate** — cells with a URL, a date and a quote containing the number,
   over cells attempted. This is the number that says whether the pass is usable.
2. **Correction count** — cells where the recalled value was wrong. Expect some; zero
   corrections across 20 recalled cells is evidence the executor searched loosely, not
   evidence the recalls were good.
3. **The prediction's branch**, with its quote.
4. **§C's confirmed / corrected / unsettled counts**, which are a calibration datum this
   project can reuse and currently has nothing on.

The `NOT FOUND` rate is a first-class number, not a shortfall. A record whose frontier
cannot be found in an afternoon is a record where nobody has written one down, and that is
the opposite of a dead end for a workstream looking for neglect.

### What this run cannot do

It cannot tell you whether a board is worth attacking — only whether the work that remains
is the kind an agent is good at. The 35 witness verdicts it consumes are still **one rater,
no blind second pass** (`README.md`, "What is not done"), and this run does not fix that;
every verdict names its witness object so a second rater can score the object rather than
the label, and that run is cheap, needs no network, and is still unrun.

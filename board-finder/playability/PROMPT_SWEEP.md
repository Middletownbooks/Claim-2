# The fetch-heavy sweep prompt

The executable half of `PROMPT_FRONTIER.md`, cut down for a **subscription chat surface**
(claude.ai, web search and fetch on) rather than the API, where per-request knobs like
`max_content_tokens` are not available and the window fills as the sweep runs.

**Division of labour.** The chat model sweeps and returns sourced cells. It does not get the
repo. Where a cell cannot be settled online, it **names the paper** and stops — the operator
pastes that transcript into the Claude Code session, which writes it to
`sources/` and settles the cell there. So `NOT FOUND` is not a failure here; it is a
work order.

Paste **Part A only**. Part B is for the operator.

---

## Part A — paste from here

> You have web search and fetch. Your job is to **source 24 factual claims about
> computational frontiers** and report them in a fixed format. You are not solving any
> mathematics, not running any search, and not estimating anything.
>
> Your answer is going to be pasted into a repository by another agent. **A cell you guess
> becomes a permanent repository fact with no source attached.** Leave it empty instead.
>
> ### Five rules
>
> **1. Search before you fetch, and fetch as little as possible.** A search snippet that
> already contains the number is enough — quote it and move on. Fetch a page only when no
> snippet carries the sentence you need. Prefer an abstract page, a Wikipedia-class summary
> or an HTML version over a PDF, and never open a PDF to find a number that a landing page
> states. Your context is finite and the sweep is long; every unnecessary fetch costs you a
> record later in the list.
>
> **2. Every number needs a verbatim quoted sentence containing that number, plus the URL
> and the source's date.** *"Verified to 4·10¹⁸"* is the shape of a sentence that gets
> produced whether or not it is true, and because it looks checkable it survives review. A
> quote with the number in it is the only thing that does not. No quote → the verdict is
> `NOT FOUND`, not a confident paraphrase.
>
> **3. Emit one block per record, as you finish it, in the order given.** Do not save results
> up for a summary at the end: if you run long, the blocks you have already written are the
> deliverable and a remembered summary is not. Never reconstruct an earlier block from
> memory — if you need to correct one, say which record and restate it in full.
>
> **4. When you cannot settle a cell, name the paper.** Give the exact title, and the arXiv
> id or DOI if you saw one, under `transcribeThis`. Someone will paste the full text to
> another agent. This is a useful outcome, so reach it deliberately rather than padding the
> cell.
>
> **5. Answer §C honestly at the very end.** It asks which of these frontiers you believed
> before you searched. A recall of yours that the search corrected is the single most
> valuable line in your reply.
>
> ### The block format, one per record
>
> ```
> RECORD <rank> — <short name>
> claim:        <the claim as given to you, copied>
> verdict:      CONFIRMED | CORRECTED | NOT FOUND | CONTRADICTED
> frontier:     <what the frontier actually is, or empty>
> wall:         <what stops the next push; say whether the source states it or you infer it>
> url:          <single best URL, or empty>
> date:         <source date, or empty>
> quote:        "<verbatim sentence containing the number, or empty>"
> depthOrBreadth: DEEP | BROAD | UNKNOWN
> breadthDetail: <if BROAD: which families or cases, roughly how many>
> transcribeThis: <exact paper title + arXiv id or DOI, only if the cell is unsettled>
> note:         <one or two sentences; anything that surprised you>
> ```
>
> `depthOrBreadth` means: is the remaining work **one pipeline pushed further with more
> compute** (DEEP), or **many small independent constructions or cases, each cheap, that
> nobody has had the patience to do all of at once** (BROAD)? Do not infer it from how famous
> the problem is. `UNKNOWN` is allowed and better than a guess.
>
> ### The records, in priority order
>
> **Group 1 — four finite-group block conjectures. Do these first.**
> The claim for all four: *each carries a reduction theorem to an inductive condition on
> finite simple groups, so a counterexample search is a structured list (families plus 26
> sporadics) rather than a combinatorial explosion, and the character-theoretic predicate is
> implemented in GAP's character table library.*
> And a prediction to settle: **if that is right, someone has already swept the small groups
> and published it.** Find that sweep, or establish that it is not there. **Both answers are
> results, and the absence is the more interesting one.**
> For each: does the reduction exist and to what condition; how much of the classified list
> has been discharged, by whom, when; is the predicate really in GAP.
>
> * **287 Alperin–McKay.** k₀(B) = k₀(b) for a block and its Brauer correspondent in N_G(D).
> * **300 Alperin's weight conjecture.** #simple modules of a p-block B = #G-classes of B-weights.
> * **356 Brauer's k(B).** k(B) = |Irr(B)| bounded in terms of the defect group.
>   *The note on this one says its reduction is **weaker** than the other three and the writer
>   was **not confident**. It is the cell most likely to be wrong — check it hardest.*
> * **472 McKay–Navarro (Galois–McKay).** p′-degree characters of G and of N_G(P), counted
>   compatibly with a Galois action.
>
> **Group 2 — nine frontier-limited records, where the published frontier is the whole
> value.** For each: the current frontier with a quote, who pushed it and when, and whether
> anything suggests the next push is cheaper than the last.
>
> * **22 Binary Goldbach** — every even n > 2 a sum of two primes. Claim: verified to about 4·10¹⁸.
> * **161 Collatz** — claim: verified far out; note the divergence branch is not certifiable at all, only a cycle is finite.
> * **239 Odd perfect number** — σ(N) = 2N with N odd. Claim: a linear push against a very large known lower bound.
> * **273 Kummer–Vandiver** — p ∤ h⁺(ℚ(ζ_p)). Claim: the h⁺ computation per prime is expensive and the frontier binds.
> * **307 Legendre** — a prime strictly between n² and (n+1)². Claim: a linear push, prime-gap frontier far out.
> * **348 Beal / Tijdeman–Zagier** — A^x + B^y = C^z with x,y,z > 2 forces a common factor. Claim: a bounded linear search over exponents and bases.
> * **488 Second Hardy–Littlewood** — π(x+y) ≤ π(x) + π(y). **Two separate things here.** (a) The frontier of direct verification. (b) **The important one:** the witness question factors, and the cheap factor is pure combinatorics — whether an admissible pattern of diameter y can contain more than π(y) elements, believed to happen past y ≈ 1600 on the Hensley–Richards route. Verify that result and give **the smallest y for which an admissible set exceeding π(y) is known**, with a quote. Treat (b) as its own record and label it `488b`.
> * **500 Lehmer's τ** — τ(n) ≠ 0 for all n. Claim: τ(p) per prime is cheap; purely where the sweep stopped.
> * **9 GRH for Dirichlet L-functions** — claim: a zero off the line needs rigorous interval arithmetic far past any new sweep. Report the current verification height if one is published.
>
> **Group 3 — the single strongest recommendation, and it rests on a recalled citation.**
>
> * **280 Kaplansky's idempotent conjecture** — every idempotent in K[G] for torsion-free G is
>   0 or 1. The claim: the neighbouring **unit** conjecture fell to a computer search —
>   believed **Gardam, 2021, in the Promislow group over 𝔽₂**. Verify that result and its
>   method, then find whether anyone has pointed the same method at the **idempotent**
>   conjecture, and what stopped them. If nobody has, say so explicitly — that is the finding.
>
> **Group 4 — eight more BOUNDED records. One block each; if budget runs short, stop here
> and say where you stopped.**
>
> * **79 Hadwiger** — no K_{t+1} minor ⇒ t-colourable. Claim: minor-closed structure cuts the candidates.
> * **275 Frey–Mazur** — E[p] ≅ E′[p] for p > 17 ⇒ isogenous. Claim: computable over small conductor.
> * **295 Tutte 5-flow** — claim: reduces to snarks, exhaustive snark generation is the method and it is pushed. Give the snark-generation frontier.
> * **355 Tutte 3-flow** — 4-edge-connected ⇒ nowhere-zero 3-flow. Same shape as the 5-flow.
> * **335 Jones unknot** — V_K = 1 ⇔ unknot. Claim: knot tabulation by crossing number is the method; give the crossing-number frontier.
> * **429 Lovász** — every finite connected vertex-transitive graph has a Hamiltonian path. Claim: generable from group data; frontier is order.
> * **458 Erdős matching** — claim: the two extremal candidates are explicit, so a counterexample must beat both. Give the ranges where the conjecture is proved.
> * **493 Voronoi on parallelohedra** — claim: proven for d ≤ 5, and d = 6 enumeration is the wall.
>
> **Group 5 — one credit claim, flagged unverified by the people who recorded it.**
>
> * **331 Hadamard matrix existence** — order 4k for every k. The claim: **twelve** previously
>   open Hadamard orders were closed over a weekend by an agent sweeping construction
>   families, with Claude credited alongside other researchers, and only order 668
>   independently checked. Named sources: `github.com/bbeartheancient/hoa64` and
>   `epoch.ai/frontiermath/open-problems/hadamard`. Establish which orders, verified by whom,
>   and whether the constructions were executed and checked or only supplied. **Say plainly if
>   the claim is overstated** — it is currently doing work in a reclassification, so an
>   inflated version of it is expensive.
>
> ### After the blocks, three short sections
>
> **§A The prediction.** For the four block conjectures: swept and published, or absent?
> Quote the thing that settles it.
>
> **§B Start and drop.** At most three records you would start, ranked, and at most three you
> would drop, each with the one fact that decided it.
>
> **§C Recall against source.** Which of these frontiers did you believe you knew before
> searching? For each, say whether the search **confirmed**, **corrected** or **failed to
> settle** it, and give the three counts. A wrong recall that the search caught is the most
> useful line here — it calibrates how far the unsourced cells elsewhere in this project can
> be trusted.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each rule is built against

| rule | the observed failure |
|---|---|
| search before fetch, never a PDF for a number a landing page states | subscription chat has no `max_content_tokens`; on API pricing this sweep is 0.5–0.95M tokens of fetched pages, which is ~95% of a 1M window on its own. Fetch discipline is the only knob available on this surface, and a window that fills mid-sweep loses the early records |
| a quote containing the number | `PROMPT_WITNESS.md` Part B: *"verified to 10^20 is the shape of a sentence a model will produce whether or not it is true, and unlike a board-search claim it looks checkable, so it survives review"* |
| one block per record, emitted as you go, never reconstructed | a chat window that fills degrades verbatim quotes into paraphrase — and the quote is the entire deliverable. Incremental blocks make a truncated run partially usable instead of wholly unusable |
| `transcribeThis` | the division of labour: this project's Claude Code session has a filesystem, so a pasted transcript is written to `sources/` once and grepped thereafter, and its quotes stay verbatim past any compaction. A chat attachment only ever lives in context. So unsettled cells are routed to the surface that can make a quote permanent |
| "a cell you guess becomes a permanent repository fact" | the output is committed. Every other prompt in this project is scored; this one is *transcribed*, which is a stronger reason to leave a cell empty |
| DEEP or BROAD, `UNKNOWN` allowed | the one target here that has actually paid (331 Hadamard) was mis-screened as *saturated* by a "has this been worked?" heuristic. Specialists saturate depth, not breadth |
| both branches of the prediction are findings | registered in `RANKING_FIT.md` §4 before any lookup, so that "no sweep exists" cannot be quietly filed as a null result |
| 356 named as the least confident cell | the writer flagged it in advance. A sweep that confirms every cell including that one has probably not searched |
| 488 split into 488 and 488b | `FEASIBILITY.md` §1: the sweep run here measured the *hard* factor of a two-factor question and missed that the cheap factor was the whole game. Splitting the record forces the cheap factor to be asked for by name |
| §C asked last | turns the run into a **measurement of model recall on frontier facts** over ~24 cells with ground truth found in the same session. This project tags unsourced cells `[recall]` throughout and has never measured what that tag is worth |

### On receiving the reply

1. Paste it to the Claude Code session. It parses the blocks into `classification.json`
   (`witnessCheckFeasible`, `searchMechanismClass`, `feasibilityNote`, plus new `frontier`,
   `wall`, `sourceUrl`, `sourceDate`, `quote`, `depthOrBreadth` fields) and commits with the
   quotes intact.
2. Then paste transcripts for every `transcribeThis`, highest-priority record first. Those go
   to `sources/` as text — **never as PDF**, which costs 2.3–5.6× the same paper as text
   because each page bills as extracted text plus a page image.
3. Scoring is the **sourced-cell rate** and the **correction count**, not the confirmation
   count. Zero corrections across ~24 recalled cells is evidence of a loose sweep rather than
   of good recall.

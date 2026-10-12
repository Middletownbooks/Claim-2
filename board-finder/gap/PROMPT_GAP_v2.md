# Gap analysis v2 — the prompt, rebuilt

Successor to the July 2026 gap-analysis prompt. Reviewed in
`REVIEW_JULY_GAP_ANALYSIS.md`; the four changes below are each traceable to something this
project measured or paid for.

| change | why |
|---|---|
| **dimension F replaced** by *is the unknown set nameable?* | F rewarded parameter richness, which is exactly what made SIC/Zauner look attractive and worthless. Hadamard (13 numbers) and SIC (open tail) have identical F and opposite value |
| **witness polarity declared**, not excluded | the July prompt excluded construction targets. They are equally one-directionally checkable, and our `playability/` work is entirely in that half |
| **premise-falsification line required, and run** | one line of arithmetic (W(m) ⇒ H(4m)) killed a route I spent a day on, with the data in hand the whole time |
| **only verified candidates are ranked** | 20 of 31 July rows were unconfirmed recall; a measured ~40 AI-resolutions/month makes that fatal, and the SIC gate showed unsourced recall reproducing a nine-year-stale snapshot |

Paste **Part A only**. Suggested model: Opus — see Part B.

---

## Part A — paste from here

> You have web search and fetch. Your job is **triage**: find open mathematical problems whose
> resolution is a *single explicit finite object*, and rank them. Do **not** attempt to
> construct any object.
>
> Your output will be committed to a repository and acted on. **A status claim you cannot source
> is worse than no candidate**, because it sends real effort at a problem that may already be
> closed. Leave it out, or put it in the unverified pool.
>
> ### The two witness polarities — declare one per candidate
>
> Both are acceptable. They differ only in what the object is:
>
> * **REFUTATION** — the conjecture says "for all X, P(X)"; the witness is one X with ¬P(X).
>   (Jacobian n≥3: a polynomial map. Dinitz–Garg–Goemans: a 7-node network.)
> * **CONSTRUCTION** — the conjecture or open question says an object of type T exists (or asks
>   for one at a parameter where none is known); the witness is one such object.
>   (A Hadamard matrix of an open order. A fiducial vector in an open dimension.)
>
> **Excluded: NON-EXISTENCE.** If the only way to settle it is to prove no object exists —
> exhaustive search with a co-NP-flavoured certificate — it is out, however small the space.
> Say so and move on.
>
> ### Score each candidate 1–5 on A–H, and justify each score in one line
>
> **A. Quantifier structure.** Does one finite object settle it, in the polarity you declared?
>
> **B. Witness verifiability — one-directional and exact.** Can the object be checked by
> arithmetic, symbolic algebra, finite-field linear algebra, or bounded enumeration, with no new
> theory? Score 5 only if the check is *exact* and *one-directional* ("this object has property
> P"). Cap at 4 if it needs a solver's infeasibility claim or floating-point.
>
> **C. Explicitness of the object.** Small and writable-down (a graph, a matrix, a low-degree
> map, a short sequence) rather than abstract or infinite-dimensional.
>
> **D. NAMEABLE UNKNOWN SET — the dimension that matters most.** Can you write down the set of
> unresolved instances? Score:
> * **5** — a *finite, enumerable list* of specific open instances below a known ceiling
>   ("these thirteen orders", "these four dimensions", "n = 8, 9, 10").
> * **3** — a bounded region, enumerable in principle, not yet listed.
> * **1** — an *unbounded tail*: everything above some frontier, or "all sufficiently large X".
>
> This is not the same question as "is the parameter space rich". A rich parameter space whose
> unknown region is an open tail is a **frontier you arrive at late**, not a target. A short list
> of named gaps is a target. If the unknown set is a tail, say so and score 1 even if every other
> dimension is perfect.
>
> **E. Completable increment.** Is there a *bounded* extension of the already-settled region that
> could be finished in the effort available — and would the null result (region extended, nothing
> found) be publishable on its own? Score 5 where both hold. This is what makes a failed search
> still worth running.
>
> **F. Diagnosis of resistance, with the prior search's artifacts.** Three distinct states, and
> only the first tells you what was actually covered:
> * prior search **published with code or data** — coverage is knowable (score on how much room
>   is left);
> * prior search **asserted** without artifacts — coverage unknowable, cap at 3 and say so;
> * **no systematic search** — score high, and say what makes you confident nobody ran one.
>
> **G. Tooling.** Do existing tools (CAS, SAT/SMT, ILP, polytope or finite-field libraries,
> nauty-style enumerators) check a candidate witness today, without new infrastructure?
>
> **H. Community checkability.** Could a domain expert verify a posted witness quickly and
> uncontroversially? Numerical-only claims and solver-infeasibility claims score lower.
>
> ### Two mandatory fields per candidate, outside the scoring
>
> **1. The premise-falsification line.** *One* check — arithmetic, a definition, a lookup —
> that would kill this candidate before any compute is spent, **and its result**. Run it now.
> Examples of the shape: *"if object W of order m existed, theorem T would already give the
> target at parameter 4m — so check whether 4m was ever open."* *"if the conjectured bound were
> attained anywhere, the extremal example would already be tabulated — so check the table."*
> A candidate with no such line is suspicious; say that instead of inventing one.
>
> **2. Status, disambiguated into one of three.** "Open" is not a single state:
> * **OPEN-UNSWEPT** — open, and the computationally reachable range has not been searched;
> * **OPEN-SWEPT-IN-RANGE** — open, but the reachable range *has* been exhausted (the cheap win
>   is gone; say where the frontier is);
> * **OPEN-BEYOND-REACH** — open only in a regime where a witness is provably or plausibly too
>   large to verify.
>
> Give a **quote** that supports the state you chose, plus URL and date. A quote establishing
> "still open" does **not** establish which of the three it is — that is a separate claim needing
> its own support.
>
> ### Precedent discipline
>
> If you cite a fallen sibling conjecture as evidence ("the adjacent conjecture was refuted by
> this method"), you must state **the implication direction** between the two and whether the
> precedent makes your target **easier or harder**. Refuting a *stronger* sibling is the easier
> task, so such a precedent is weaker evidence than it appears. Get this backwards and the
> candidate is mis-ranked.
>
> ### Anti-criteria — exclude, and list the exclusions so they are auditable
>
> * Resolution plausibly needs new deep theory (millennium-tier and neighbours).
> * NON-EXISTENCE polarity, per above.
> * No natural discretisation (purely analytic with no finite witness).
> * **On an enumerable public problem list.** Curated numbered lists — problem gardens, Erdős
>   problem trackers, "open problems in X" compendia — are being swept systematically by agent
>   pipelines. Treat anything an agent can enumerate as contested, and prefer conjectures named
>   in the primary literature but *not* sitting on such a list. Say which lists you checked a
>   candidate against.
> * Known lower bounds put the smallest possible witness beyond verification.
>
> ### Process
>
> 1. **Cast wide first.** At least 20 candidates across at least 5 subfields, before scoring
>    anything. Include both polarities.
> 2. **Verify status before scoring.** Score **only** candidates whose status you confirmed
>    against a dated source this session. Everything else goes in an **unverified pool**,
>    unscored, each with the one search that would promote it. Do not rank the pool.
> 3. **Run the premise-falsification line** for every scored candidate. Report what it returned.
>    Expect it to kill some — that is the step working.
> 4. **Go deeper on the top 5–8**: the specific known bounds, the best current constructions, the
>    published near-misses, and the actual stated reason the problem resists.
> 5. **Per top candidate, a concrete attack sketch**: what object to look for, how big the space
>    is, which tool checks a witness, and whether it fits one extended session with light tooling
>    or needs sustained compute.
>
> ### Output
>
> 1. **Ranked table of verified candidates only** — Problem | Field | Polarity | A–H | Total |
>    Status (one of the three) | one-line rationale.
> 2. **Unverified pool** — unscored, with the promoting search named per item.
> 3. **Dossiers** for the top 5–8: statement; polarity; scores with justification; the
>    premise-falsification line **and its result**; near-miss evidence with citations; attack
>    sketch; verification method; status quote with URL and date; risks.
> 4. **Exclusion list** with the anti-criterion each failed.
> 5. **Methodology appendix**: every search run, every page fetched, so currency is auditable.
> 6. **Recall against source — answer last.** Which figures did you believe before searching? For
>    each: confirmed / corrected / failed to settle, with counts. A recall the search corrected is
>    the most valuable line in the document.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each clause is built against

| clause | the observed failure |
|---|---|
| **D, nameable unknown set**, replacing the old "parameter richness" | Zauner/SIC scored highest on richness in our own re-rating and died on the gate: exact fiducials are a hole-free prefix with a sparse tail above it. Hadamard has the same shape and thirteen nameable gaps. The old dimension rewards the bad one |
| **E, completable increment** | Seymour's second neighbourhood conjecture was the July analysis's cleanest case for a reason it did not name: exhaustive verification stops at n ≤ 7, so n = 8–10 is a *finishable* increment whose null result extends a published frontier. That property deserves its own score |
| **F's three states of prior search** | "exhaustively searched" hides whether coverage is knowable. The SIC gate found the construction-side twin: dimensions asserted done in print with the vectors nowhere public |
| **premise-falsification line, run during triage** | one line — *W(m) ⇒ H(4m), so check whether 4m was open* — killed a route after a day's work, using data held throughout. Cheapest possible filter, and it was absent from the rubric |
| **status split into three** | the July rubric's dimension E mixed "nobody searched" with "searched to exhaustion", which are opposite recommendations. And a quote saying "open" supports neither |
| **precedent direction** | Kaplansky ZD scored D = 5 on Gardam's refutation of the *unit* conjecture. Unit ⇒ ZD ⇒ idempotent, so unit is the strongest and easiest to refute; the precedent makes ZD look closer than it is. Our own sweep made the mirror error on the third member |
| **score only verified** | 20 of 31 July rows were unconfirmed. The SIC gate's respondent reported its own recall would have produced a fictitious hole list |
| **list-level anti-criterion** | kept verbatim from July, which derived it and was right: ~40 AI-resolution claims/month, curated lists swept by agent pipelines |
| **recall against source, last** | two runs now have produced this datum, and both times the corrections clustered on post-cutoff facts. A third is nearly free |

### Model

**Opus.** The scoring is mechanical but three judgements are not: deciding D (nameable set vs
tail) requires reading several papers' conventions and synthesising a set; the precedent-direction
clause is exactly the reasoning our own sweep got backwards; and the premise-falsification line
has to be *invented* per candidate, which is the least retrieval-like step in the document.
Sonnet is the right call for the periodic refresh once a candidate list exists.

### What a good result looks like, and the fallback

Success is **2–4 verified candidates at D = 5** — a nameable finite list of open instances,
off the enumerable lists, with a premise-falsification line that survives. That is the shape
Hadamard had.

If nothing reaches D = 5, that is a real finding and not a failed run: it says the named-
conjecture literature has no nameable-gap targets left that are off-list, and the fallback is
the 499-record corpus, whose items come with collaborative leads already attached. Report the
D distribution explicitly so that call can be made on the numbers.

# Gap analysis v4 — the prompt

Successor to `../PROMPT_GAP_v2.md` (the A–H rubric) as amended by `../GAP_V3.md` (which was an
analysis, never a prompt — so v4 is the first prompt to carry v3's corrections). It is the first
triage prompt in this programme that can hand its runner **a prior-work exclusion list**, because
`../register/REGISTER.md` now exists; every previous prompt sent a runner at a space without telling
it what had already been tried, which is `D56`.

| change from v2/v3 | why |
|---|---|
| **the re-parameterisation step, first and as a kill** | the programme's one verified result — a counterexample to Chow's Conjecture 2 — was a headline with no tracked quantity until you read the source's own ladder theorem. `D59`; `../RESULT_RETRODICTION_P40.md` §2b |
| **one remedy taxonomy, five-valued, replacing two** | `../GAP_V3.md` §3's four-way and Cycle 0's binary **disagree on PTE 11** and neither cites the other. `../register/REGISTER.md` §4.5 |
| **remedy sourced from the frontier paper's method section** | move kinds measured **0 of 10** as a discriminator; method sections are obtainable. `../SELECT_v1.md` §9, `../register/REGISTER.md` §4.3 |
| **seven dimensions, five of them kills, two scored** | v2 scored eight dimensions of the problem and v3 proposed three more. Eleven scored dimensions invites the July defect of ranking unverified rows |
| **prior-work exclusion list supplied** | nine worked targets with their binding constraints, so the run cannot return one of them as new |
| **tooling adjacency explicitly barred as a credit** | U13 was ranked first in the v3 queue *because* we were already tooled for it; the apparatus was shared and the orders were not |
| **context budgeted, not just calls** | two runs reported context as the nearer constraint while call caps went unspent. `D55` |

**Dispatch: paste Part A only, into a FRESH conversation.** Not a continuation of one that has seen
this file. "Part A only" is a property of the *transcript*, not of the last message — a conversation
that has already read Part B cannot be repaired by re-prompting it with Part A, because the context
still holds the bar and the registered prediction. Suggested model: **Opus 5.5 chat with search.**
Part B says why.

> **This file no longer carries the registered prediction.** It is in `../../../proof-protocol/ledger.json`
> as `P-42` and must not be copied back here. A prompt and the prediction about its output cannot
> share an artefact: a run given the whole file learns what outcome is expected of it before
> producing one, and a heading saying "do not paste" is a request rather than a control. This is
> `D44`'s discipline applied to the dispatch rather than to the threshold, and it is the mirror of
> `P-41`'s void — there the author was not blind to the evidence, here the runner would not be blind
> to the prediction.

---

## Part A — paste from here

> You are running a **triage**, not an attack. Find open, *named* mathematical conjectures — named
> in the primary literature, **not** sitting on an enumerable public problem list — whose resolution
> is a single explicit finite object, and rank them. **Construct nothing.**
>
> Your output will be committed to a repository and acted on by people who will spend real effort on
> what you rank first. **A status claim you cannot source is worse than no candidate**, because it
> sends that effort at a problem that may already be closed. Leave it out or put it in the unverified
> pool.
>
> ### Budget, and which resource actually binds
>
> Roughly 25–30 searches or fetches. **Context will bind before the call count does** — two prior
> runs of this kind stopped on context with a third of their call budget unspent. So: prefer a
> paper's *method* section to the whole PDF, quote short, and if a return is oversized say so and
> summarise rather than pasting. If you stop, say which resource stopped you.
>
> ### Provenance — tag every factual claim with exactly one
>
> * **PRIMARY** — you read the primary source this session and can quote it with a URL and a date.
> * **RELAYED** — a secondary source states it (a survey, a table, a database README).
> * **SEARCH-SUMMARY** — a search-result snippet or an AI overview. **Not usable for any kill or
>   pass below.** If a dimension can only be settled at this tier, the dimension is UNSETTLED.
> * **RECALL** — you believe it from training. Usable only in the final recall section.
>
> ---
>
> ## Step 0 — build the exclusion set before you look for anything
>
> The properties that make a problem score well here are the same properties a benchmark designer
> selects for. So the list check is a **filter applied first**, not a caveat applied last.
>
> Enumerate the agent-facing problem databases and attack boards, and give each a *date*. Five are
> known to exist: **FrontierMath: Open Problems** (Epoch), **TheoremDB**, **Horizon / HorizonMath**,
> **erdosproblems.com**, and **google-deepmind/formal-conjectures** (arXiv:2605.13171). Two further
> *attack platforms* publish curated target boards and count for this purpose: **EinsteinArena** and
> the **Qiushi Engine**. **Search for others** — the fifth was found within an hour of this prompt
> being written, so treat the list as incomplete by default rather than as a checklist.
>
> **On formal-conjectures specifically, since it changes this step's arithmetic.** Measured directly
> from the repository at commit `7d450ef`, 30 Sep 2026 — **1,662 Lean files carrying 1,403 statements
> tagged `@[category research open]`**, against 2,202 tagged `research solved`. It is explicitly a
> benchmark for automated provers, it ships an agent-guidelines file for contributors, and its most recent commit that day was
> PR **#6763**. Two consequences for your enumeration:
>
> * **It aggregates two of the other four.** Its open statements break down as ErdosProblems **646**,
>   Wikipedia's unsolved list **273**, OEIS **189** — so clearing a candidate against
>   erdosproblems.com and against this repository is substantially the same check, and you should say
>   so rather than counting it twice. It also adds sources none of the other four cover: the Kourovka
>   notebook, Green's open problems, MathOverflow, and *Written on the Wall II*.
> * **It has begun enumerating the primary literature, which is this prompt's whole refuge.**
>   its Paper directory holds **71** open statements and its Arxiv directory **37** — 108 of 1,403, so about 8%. That is
>   small, and it is not zero, and the direction is one way. **Do not treat "named in a paper rather
>   than on a list" as safety.** Check candidates against this repository by name, and report what
>   fraction of its 1,403 you were actually able to enumerate.
>
> Then state, explicitly:
>
> 1. Which databases you could actually enumerate, and how much of each you could read. *A list you
>    could see a fifth of does not clear a candidate.* Say what fraction.
> 2. The **pairwise overlap** between any two you enumerated. Prior measurement put curated lists
>    at **5–20% pairwise overlap**, which means clearing one says very little about the others.
>    Confirm or correct that.
>
> **Every candidate you score must be cleared against the exclusion set by name, and you must say
> which lists it was cleared against.** "Not found on the lists I could read" is the honest form.
>
> ## Step 1 — cast wide, before scoring anything
>
> At least **25 candidates across at least 6 subfields**. Named conjectures in the primary
> literature, off the enumerable lists. Include both witness polarities (Step 2). Do not score yet.
>
> ## Step 2 — declare witness polarity
>
> * **REFUTATION** — the conjecture says "for all X, P(X)"; the witness is one X with ¬P(X).
> * **CONSTRUCTION** — an object of type T is conjectured to exist, or is sought at a parameter
>   where none is known; the witness is one such object.
> * **NON-EXISTENCE is excluded.** If the only way to settle it is to prove no object exists —
>   exhaustive search with a co-NP-flavoured certificate — it is out, however small the space. Say
>   so and move on.
>
> ## Step 3 — THE RE-PARAMETERISATION STEP. Do this before any scoring, and record its failures
>
> **This is the step this rubric exists for.** A conjecture's headline is usually a truth value —
> *"prove that every X has property P"* — which has no tracked quantity, no two sides and nothing a
> certificate can move. But many sources contain a **ladder** that turns the headline into an
> integer, and it is usually stated in the source rather than in the abstract.
>
> For each candidate, look for one of:
>
> * a **graded family** with a monotonicity theorem — *"C(k) implies C(ℓ) for ℓ ≥ k"*, so
>   *k\** = min{k : C(k) holds} is a well-defined integer;
> * a **smallest open case** — the conjecture is verified up to some parameter and disproved beyond
>   another, leaving a bracket;
> * a **verification frontier** — *"checked exhaustively for n ≤ 7"*;
> * a **bounds pair** — best known upper and lower bounds on a quantity the headline does not
>   mention.
>
> Output for each candidate, as a four-line block:
>
> ```
> headline:          <the conjecture as stated>
> tracked quantity:  <an integer, or NO-QUANTITY>
> lower side:        <value> via <certificate: a finite object, an exhaustive check, a construction>
> upper side:        <value> via <certificate>
> ```
>
> **A candidate with NO-QUANTITY is recorded as NO-QUANTITY and carried into the output as such.**
> Do not drop it silently and do not invent a quantity to rescue it. The count of NO-QUANTITY
> candidates is a result in its own right.
>
> **Worked example of the shape** (use it as a pattern, not as a candidate — it is closed):
> a 2005 paper conjectured a statement C(b) for all b ≥ 2, exhibited counterexamples to C(2),
> verified C(3) at rank 3, and proved C(k) ⟹ C(ℓ) for ℓ ≥ k ≥ 2. A 2011 paper then disproved C(b)
> for 2 ≤ b ≤ n/3. So *"the smallest rank at which C(3) fails"* was a **bracketed integer with both
> bounds on finite certificates** — and it appears in no table anywhere. The headline looked
> unscorable; the ladder was in the source's own theorem list.
>
> ## Step 4 — the remedy class. One label, from the method section
>
> For each surviving candidate, read the **method section of the paper that set the current
> frontier** — not the abstract, not a survey's description of it. Then label what would actually
> remove the obstruction:
>
> | label | what closes the gap |
> |---|---|
> | **FLOPS** | more compute of the same kind, at the same algorithm |
> | **ALGORITHM** | a better search, encoding or enumeration at the same compute |
> | **THEORY** | a new structural result, not an implementable method |
> | **BREADTH** | reading and adjudicating more literature |
> | **CONTEST** | nothing — another group arrives first |
>
> **Rules, and they are not negotiable.**
>
> * The label must come from the method section at **PRIMARY** tier. If you cannot get the method
>   section, the label is **UNDETERMINED** and the candidate is **not scored** — it goes to the
>   unverified pool with "obtain the method section of <paper>" as its promoting action. Do not infer
>   the label from how recent the last improvement was, or from what kind of paper it was: that
>   proxy has been measured on this board and classified **0 of 10** candidates.
> * **FLOPS is a kill.** A better model does not add FLOPs.
> * **Distinguish FLOPS from ALGORITHM explicitly**, and quote the sentence that decides it. The
>   common case is a frontier paper whose enumeration is orders of magnitude smaller than the naive
>   one because of a structural trick in its §3 or §4; naive-cost arithmetic then reads as FLOPS when
>   the real gap is ALGORITHM. Getting this backwards in either direction has cost this programme a
>   target.
> * **CONTEST cannot be scored from outside.** Do not return "no evidence of competition" as a
>   clear. Return: who has published on this quantity since 2024, with dates; whether any AI search
>   system's published board contains it; and then state plainly that absence of evidence here is
>   **unknown, not clear**. Competition on this class has repeatedly been discovered only by
>   entering.
>
> ## Step 5 — seven dimensions. Five are kills, two are scored
>
> A kill is a kill: **one FAIL ends the candidate**, and you report it rather than averaging it
> away. No middle bands — where a threshold is stated, a value that lands between labelled regions
> means the dimension is **UNSETTLED**, which is also a FAIL, and you say which kind (below).
>
> | | dimension | rule |
> |---|---|---|
> | **Q** | **Quantity** | Step 3 produced a tracked integer with two sides, each moved by a finite certificate. **KILL if NO-QUANTITY.** |
> | **N** | **Nameable unknown set** | **Scored 1/3/5.** 5 = a finite, enumerable list of specific open instances below a known ceiling ("these thirteen orders", "n = 8, 9, 10"). 3 = a bounded region, enumerable in principle, not yet listed. 1 = an **unbounded tail**. **KILL at 1**, however perfect everything else is. This is not "is the parameter space rich" — a rich space with an open-tail unknown region is a frontier you arrive at late. |
> | **W** | **Witness check** | **Scored 1–5.** 5 only if checking the object is **exact and one-directional** — arithmetic, symbolic algebra, finite-field linear algebra, bounded enumeration. Cap at 4 if it needs a solver's infeasibility verdict or floating point. Note that a solver's UNSAT *verdict* is not a *certificate*: say which one is available. |
> | **R** | **Remedy** | Step 4's label, at PRIMARY tier. **KILL if FLOPS. Not scored if UNDETERMINED.** |
> | **H** | **Headroom** | The ratio of the region we could cover to the region published work covers, from a cost model with a **measured or cited rate** — not an estimate. Show the arithmetic. **KILL if H ≤ 1.** State the exponent: if cost is C(n,k) or similar, a factor in the region is a much smaller factor in the parameter. |
> | **P** | **Prior** | Is there positive evidence **against** the object existing in the region we could reach? Look for it and say what you found. **KILL if yes.** (Absence of evidence either way is fine — that is the unswept case, which is what we want.) State the confound you checked: a region may look empty only because it was searched less, so compare coverage in the units that matter, not in instance counts. |
> | **Δ** | **Deliverable** | Write, in one sentence each, the abstract line for the **positive** outcome and for the **null**. Then name **the table that changes**, with its current value and the date it last moved. **KILL if no table changes under either outcome.** The failure this catches: a search can succeed at its stated task and establish a fact about the wrong object — a null about two specific examples rather than about the recorded bound. |
>
> ### Two mandatory fields outside the scoring
>
> **1. The premise-falsification line, and its result.** *One* check — arithmetic, a definition, a
> lookup — that would kill this candidate before any compute is spent. **Run it now and report what
> it returned.** The shape: *"if object W of order m existed, theorem T would already give the target
> at parameter 4m — so check whether 4m was ever open."* Expect it to kill some candidates; that is
> the step working. A candidate with no such line is suspicious — say that rather than inventing one.
>
> **2. Status, as one of three states.** "Open" is not a single state:
>
> * **OPEN-UNSWEPT** — open, and the computationally reachable range has not been searched;
> * **OPEN-SWEPT-IN-RANGE** — open, but the reachable range has been exhausted (say where the
>   frontier is);
> * **OPEN-BEYOND-REACH** — open only where a witness is provably or plausibly too large to verify.
>
> Give a **dated quote with a URL** supporting the state you chose. A quote establishing "still open"
> does **not** establish which of the three it is; that is a separate claim needing its own support.
>
> ### Grade every FAIL as one of two
>
> * **FAIL-ESTABLISHED** — it fails on evidence you have, at PRIMARY or RELAYED tier.
> * **FAIL-UNEARNED** — it fails for want of evidence you could not obtain.
>
> Both block. They are different findings and a successor will act on them differently, so never
> collapse them. If a rule below tells you to issue a verdict on something you could not evaluate,
> issue **FAIL-UNEARNED** and say what you would have needed.
>
> ### Precedent discipline
>
> If you cite a fallen sibling conjecture as evidence, state **the implication direction** between
> the two and whether the precedent makes your target **easier or harder**. Refuting a *stronger*
> sibling is the easier task, so such a precedent is weaker evidence than it looks. This has been
> got backwards twice on this board, in both directions.
>
> ### Two credits that are not credits
>
> * **Tooling adjacency is not evidence of anything.** Do not score a candidate higher because
>   existing machinery sits near it. A candidate was once ranked first here on the ground that "the
>   algorithmic-idea gap, if there is one, is one we are already tooled for" — the apparatus was
>   genuinely shared, **the parameter values were not**, and the one component that made the
>   neighbouring problem tractable was the component that did not transfer.
> * **A summary line is a claim about a document, not a substitute for it.** A README saying a
>   check "may" be needed, or a survey describing a paper's method, is RELAYED at best. If a
>   dimension turns on it, get the document.
>
> ---
>
> ## Step 6 — re-score this reconstructed prior list
>
> Below is a **partial reconstruction** of an earlier triage list and its successor shortlist. It is
> partial: the original 31-row table is not available, and these are the items recoverable from
> later documents. Treat the set as given and **re-score each under Steps 3–5**, reporting Q and R
> first, because those two are new and are expected to reorder the list.
>
> | item | what the earlier analysis recorded |
> |---|---|
> | Kalai's 3^d conjecture | the cube attains 3^d nonempty faces exactly; tightness verified |
> | Tuza's conjecture | K₄ and K₅ exactly tight, τ = 2ν both |
> | MDS conjecture, characteristic 2 | Ball's bound k ≤ 2p−2 is vacuous at p = 2 |
> | Kaplansky zero-divisor conjecture | scored highest on an adjacent refutation; the family nests unit ⇒ zero-divisor ⇒ idempotent, so the refuted sibling was the **strongest** member and therefore the easiest — the precedent makes this target *harder*, not closer |
> | Zarankiewicz / Hill (crossing numbers) | attempted previously; **whether it stalled on compute or on realizability theory was never established, and that question was named in advance as deciding the candidate** |
> | Mahler's conjecture | on the list, no assessment recovered |
> | Union-closed sets conjecture | swept by the field before the earlier run began |
> | Seymour's second neighbourhood, δ⁺ = 8 | frontier δ⁺ = 7 by CP-SAT infeasibility, covering all oriented graphs on ≤ 16 vertices; δ⁺ = 8 would give ≤ 18 |
> | Zarankiewicz, K₇,₁₁ / K₉,₉ | frontier Woodall 1993, untouched since |
> | Barnette's conjecture / Erdős–Gyárfás 2–3 | grind-shaped; both spaces enumerated by people with clusters and the same tools |
> | Rota's basis conjecture, small n | **now closed — do not return it**; listed so you can see the shape that worked |
>
> For each: the four-line Step 3 block, the Step 4 label with its source, the seven dimensions, and
> a one-line verdict. **Where the earlier analysis's own reasoning was wrong, say so** — the
> Kaplansky row above is an example of a correction already made, and there may be others.
>
> ## Step 7 — do not return any of these. They have been worked and closed
>
> This is the prior-work list. Each was selected and worked by this programme; returning one as a
> new candidate is the specific failure this section exists to prevent. Where a reason is given, it
> is the binding constraint that stopped it.
>
> | target | why it is closed |
> |---|---|
> | Prouhet–Tarry–Escott, ideal size 11 | our exhaustive region sits inside the published one; the frontier was set by a residue-class enumeration trick we do not have |
> | PTE over the unsearched imaginary quadratic rings d = 43, 67, 163 | every solution ever found sits at small discriminant; the three unsearched rings are 2.3–4.5× thinner, and one has no small non-rational norms at all |
> | Costas arrays, order 32 | no structural characterisation of sporadic arrays exists, and the intended positive control at order 31 turned out to be constructible rather than search-found |
> | Hadamard matrices, bordered b > 2 region among the open orders 2000–3000 | admissibility is necessary and not sufficient; the region was entered and returned nothing, and its optimistic cost figures were retracted by their own author |
> | Hadamard H(2060) via a Williamson route | a known matrix at order 4m is evidence *against* the Williamson quadruple at m, not neutral |
> | Six mutually orthogonal Latin squares of order 12 | the table records lower bounds, so proving two specific 5-sets maximal leaves the bound where it stood |
> | D-optimal designs of order 2v | the two-circulant route needs a² + b² = 4v − 2, which fails at five of the six orders of interest |
> | Odd perfect number lower bound | the published bound is ~700 orders of magnitude behind the authors' own unpublished computation |
> | Erdős–Szekeres ES(7) | the lower bound is already the conjectured value; only an exhaustive UNSAT over all configurations moves the upper bound, so no subfamily's closure matters |
> | Zauner / SIC-POVM existence | exact fiducials form a hole-free prefix with a sparse tail above it; the unknown set is a tail, not a list |
> | Kissing numbers, dimensions 13–14 | unattempted by the published AI search systems, which is why it is *about to be* attempted, not why it is open |
> | Caps in AG(8,3) | three post-2023 AI search systems report direct runs at n = 8 |
> | Rota's basis conjecture / the C(3) ladder | closed by a July 2026 preprint |
> | Snake-in-the-box, dimensions 9–11 | **not worked by us, and listed here as a warning rather than as a closure.** It was ranked last of four in an earlier queue on the grounds that its records are likely compute-set rather than idea-set. It is formalised in the DeepMind repository above, and **its upper bound was corrected there on 30 Sep 2026.** If you return it, you must say what has moved since that commit. |
>
> ## Output
>
> 1. **The exclusion-set report** from Step 0: databases, dates, fraction readable, pairwise overlap.
> 2. **Ranked table of candidates that passed all five kills**, with N and W scored, R labelled, and
>    the status state. If that table is empty, say so — see item 6.
> 3. **The NO-QUANTITY list** from Step 3, with counts. This is a result, not a residue.
> 4. **The UNDETERMINED-remedy pool**: candidates blocked only because a method section was
>    unobtainable, each with the exact paper to get.
> 5. **Dossiers** for everything that passed: the Step 3 block, the Step 4 label with the sentence
>    that decided it, the seven dimensions with their arithmetic, the premise-falsification line and
>    its result, the status quote with URL and date, and the two abstract sentences from Δ.
> 6. **The Step 6 re-score**, as a table, with the reordering called out explicitly.
> 7. **Kill list**: every candidate that died, which kill fired, and FAIL-ESTABLISHED or
>    FAIL-UNEARNED.
> 8. **Methodology appendix**: every search and fetch, so currency is auditable. Say which resource
>    stopped you.
> 9. **Recall against source — answer this last.** Which figures did you believe before searching?
>    For each: confirmed / corrected / failed to settle, with counts. A recall your search corrected
>    is the most valuable line in the document.
>
> ### If nothing passes
>
> **Say so plainly and return the exclusion report, the NO-QUANTITY list and the re-score anyway.**
> A null here is a real finding with a specific content: *the off-list named-conjecture space
> contains no candidate with a tracked quantity, a nameable unknown set, positive headroom and a
> table that moves.* That would be worth knowing precisely, and it is a different claim from "we
> found nothing", so give the counts that support it. **Do not lower a threshold to produce a
> survivor.** Two of the four survivors of an earlier run of this kind were demoted by their own
> falsification lines, and both remaining ones are now dead; a run that returns three weak passes is
> worse than one that returns zero and says why.
>
> ### Report anything that contradicts this prompt
>
> If a premise in these instructions is wrong — a database that does not exist, an overlap figure
> that is off, a closed target in Step 7 that is actually open, a fact in Step 6's table that the
> literature contradicts — **report it as a finding**. Several prior runs' most valuable output was
> a correction to the brief they were given, and in one case the correction outranked every verdict
> in the document.

## Part A ends here

---

## Part B — operator notes, do not paste

### What each clause is built against

| clause | the observed failure |
|---|---|
| **Step 3, the re-parameterisation, placed first and made a kill** | `../RESULT_RETRODICTION_P40.md`: all six SELECT v1 gates **pass** the Chow target once it is posed as "the smallest rank at which C(3) fails", a bracketed integer with both bounds on finite certificates. The screen never saw it because the quantity is in no table and the corpus is a list of tabulated records. `D59` names the missing step; this is it, as a procedure with a recorded failure mode |
| **the worked example in Step 3** | given without naming the conjecture, so the run pattern-matches on *shape* rather than retrieving the case. It is also the programme's one verified external result, so the example is load-bearing rather than decorative |
| **Step 4's five labels replacing two taxonomies** | `../register/REGISTER.md` §4.5: `../GAP_V3.md` §3 files PTE 11 under **compute** and the register files it under **theory**, from the same quoted fact. Under the five-way split it is **ALGORITHM**, which is a *less* pessimistic verdict than either, and changes what PTE 11's corpse is evidence for |
| **method section at PRIMARY, or UNDETERMINED** | `../SELECT_v1.md` §9: S3 inferred move kind from the literature and the COMPUTE class came back **empty, 0 of 10**, because record papers must claim novelty and so never label a move "the same method, run bigger". Cycle 0's Task 3 used method sections instead and they worked. `../register/REGISTER.md` §4.3 tabulates all three sources |
| **FLOPS as a kill** | `../GAP_V3.md` §6: a model does not add FLOPs, so no release closes a FLOPS gap |
| **H with a measured rate and a single threshold** | `../../pte/PREREG_PTE11.md` A-2 guessed the mechanism and was wrong; B-2 costed it from measured constants and was right. And A-4 was two-sided with an unregistered middle, the answer landed in the middle, and the scorer returned NOT-SCORED (`D44`) |
| **P, and the confound clause** | `../../pte/rings/RESULT_RINGS.md` G2: five non-empty cells across 30, all at small discriminant, with the "thin rings were searched less" confound registered in advance and refuted by recomputing coverage in lattice points. A cheap and probably-empty target is more dangerous than an expensive one |
| **Δ, and the null-about-what clause** | `../../fallbacks/RESULT_FALLBACKS.md` §2: the MOLS(12) gate passed reachability in microseconds and produced a real theorem, and the theorem left the recorded bound untouched. Its own words: *"No rubric this project has written would have caught that"* |
| **two-grade FAIL** | `D54`: standing rule 1 tells every run to issue a verdict on a bar it could not evaluate, which erases the difference between an absence established and one a run declines to claim. Two independent runs split on exactly that and both were compliant |
| **context budgeted** | `D55`: two runs reported oversized returns as the nearer constraint with call budget unspent |
| **tooling adjacency barred** | `../../fallbacks/QUEUE_V3.md` ranks U13 first for tool adjacency; `../../doptimal/VERIFIED_OUTPUT.txt` §3 then shows the two-block route inadmissible at five of six orders of interest |
| **"a summary line is not the document"** | `D56`'s third escalation, 30 Sep: the register's own A6 row and the prediction on it were written from a README's *"may empty the orbit ansatz"* while the audit two files along had computed it |
| **Step 7, the prior-work list** | `D56` throughout, and its escalation: grepping a tree finds files and does not make anyone read them, and work done in sibling instances is invisible. Handing the list to the runner is the only version of this fix that survives contact |
| **Step 0 first, not last** | `../RESULT_GAP_v2.md` §4, which is the v2 run correcting its own prompt: the properties that score well are the properties a benchmark designer selects for, so the list check is in direct tension with the scoring function. Conway's 99-graph and the missing Moore graph score near-perfectly and are both on Epoch's list |
| **fraction-readable and overlap clauses** | `../GATE_EPOCH.md`: only ~10 of 50 Epoch entries were readable behind a JavaScript control, so four ranked candidates were cleared against a fifth of the list. `../GAP_V3.md` §7 measured 5–20% pairwise overlap between curated lists |
| **five databases, not four, and "search for others"** | the fifth — `google-deepmind/formal-conjectures`, 1,403 open statements, an agent-guidelines file, a commit the same day — was surfaced by the operator within an hour of this prompt being written, by a search this prompt itself prescribed. The clause is no longer hypothetical |
| **the Paper/ and Arxiv/ caveat** | that repository's Paper and Arxiv directories hold 108 open statements drawn from the primary literature, which is precisely the population Step 1 defines as off-list. 8% is not exhaustion, and it is the first measurement of the refuge shrinking rather than an assumption that it is safe |
| **"report anything that contradicts this prompt"** | brief D refuted its own brief's §2 and that was the run's most valuable output; brief E's decisive fact came from the same clause rather than from any bar |

### Model

**Opus 5.5 chat with search.** Three steps are not retrieval. Step 3 requires reading a source's
theorem list and *synthesising* a quantity the source does not name — the least retrieval-like
operation in the document, and the one that would have surfaced the programme's only result. Step 4
requires distinguishing FLOPS from ALGORITHM inside a method section, which is where naive-cost
arithmetic misleads. The precedent-direction clause is the reasoning this board has got backwards
twice. Everything else — Step 0's enumeration, Step 6's re-score, the status states — a cheaper
model can refresh once a list exists.

### The bar, and where it lives

**PASS: at least one candidate clears all five kills with R ∈ {ALGORITHM, THEORY} at PRIMARY tier.**
Single threshold, no middle band, per `D44`.

Not the v2 bar (*"2–4 verified candidates at D = 5"*): that bar was met by v2 and every survivor is
now dead, so it selected for something that did not predict survival. This bar adds the two
dimensions that killed those survivors — a tracked quantity, and a remedy class that a better model
can actually close.

**The registered prediction about what this run will return is `P-42` in
`../../../proof-protocol/ledger.json`, and is deliberately not restated here.** See the box at the
top of this file. Its expected kind of failure, its reasoning and what each outcome buys are all in
the ledger entry; a reader of this file who needs them should open the ledger rather than have them
duplicated into the same artefact as the prompt.

### Why this is worth running rather than option 6

It is cheap, it re-scores work already paid for, and it tests one specific hypothesis: that the
programme's nulls came from **corpus coverage** rather than from gate design. `../register/REGISTER.md`
§4.1 shows six of nine worked targets were theory-shaped and the corpus that produced them was
tabulated records; the predecessor lineage that produced the one real result was running over open
problems. Step 3 is the instrument that would let a record-shaped quantity be *found inside* a
conjecture rather than looked up in a table. If it returns nothing, that hypothesis is
substantially weakened and option 6 becomes the honest next move — which is a decision this run
buys cheaply either way.

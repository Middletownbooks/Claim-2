# Brief B1 — three design-theory tables that were never assessed

**For a Sonnet 5.5 instance in a chat conversation with web search and page fetching. No repository,
no filesystem. Your output is a document in your reply.**

These tables were **never assessed**. The earlier run's worker stopped at a concurrency cap and a
search budget before reaching them, and the run recorded them as FAIL with the note *"not assessed"*
and the observation that **"a full run could only raise the count."** So nothing here has been ruled
out; it has only been left.

Two independent facts make this the best-positioned seam left on the board. These objects are
**absent from the 499-record importance corpus entirely** — measured, not guessed — and they are
**not on EinsteinArena's board**, which is packing and extremal-configuration records. So they are
the one region this project tracks that no AI system is currently sweeping.

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

## 1. The records. One pre-specified record per table; do not substitute a different one.

**Table 6 — Williamson matrices.** Record: **the smallest odd order whose existence is open.** The
earlier run has `65` at `SEARCH-SUMMARY` and notes *"no maintained table exists"* — establishing
whether that is true is part of the task. Williamson matters more than its row suggests: a Williamson
matrix of order *m* gives a Hadamard matrix of order 4*m*, so this table is directly adjacent to the
only live target this project holds. Note also that Williamson orders have been attacked by SAT and
computer-algebra methods, so the method sections are likely to be explicit about reach.

**Table 7 — Steiner systems.** Record: **the smallest open admissible case in the most recent table
found.** Never assessed at all. Look for a maintained table of known Steiner system existence
(S(2,k,v) and S(3,4,v) families; the Handbook of Combinatorial Designs is the standard reference, and
there are online successors).

**Table 8 — cyclic difference sets.** Record: **the smallest open (v, k, λ) in the most recent table
found.** Never assessed. The La Jolla Difference Set Repository is the maintained host and was
**blocked** for the earlier run — you should be able to open it. Be careful to distinguish *cyclic*
difference sets from difference sets generally, and from **difference bases**, which is a different
object that appears on EinsteinArena's board.

**One warning specific to this group.** All three are design-theory tables, and design theory is
where *"the smallest open case"* is most likely to have moved without a maintained table recording it.
If the table you find is undated or stale, say so and give its date — an undated table is a
`SEARCH-SUMMARY`-grade artefact no matter that you opened it. The same check on a cap-set table
recently found a page **last changed in 2010** that tabulated a *different object* (projective rather
than affine caps) from the one it was being cited for, with **no row at all** for the dimension in
question. That is the failure mode to watch.


---

## The gates. Every one is pass/fail. **A gate you cannot evaluate is FAIL, not "unscored."**

Quoted verbatim from the registered selection function; you may not re-scope them.

| gate | passes iff |
|---|---|
| **S0 OPEN** | the headline and the record are unresolved; withdrawn or unrefereed resolution claims are data, not resolutions |
| **S1 COUPLED** | at least one side's bound object is a WITNESS **and** exhibiting a better witness moves a published bound **on the headline quantity itself**, not on a finite analogue of it. Two routes count: (a) the headline quantity is an extremum (sup/inf/max/min) over finitely describable objects, or (b) a published bound on the headline was established by a finite certificate checked by terminating computation. An asymptotic-order headline is COUPLED only through a **published lifting theorem** that turns a finite object into an asymptotic bound (the cap-set product construction is the model case). |
| **S2 NOT VETOED** | the witness's defining predicate is decidable and its value is computable by terminating computation. **ALGORITHM → veto. Undecidable predicate → veto.** |
| **S3 IDEA GAP** | the **most recent** move of the coupled side has kind `ANALYTIC` or `SEARCH-NEW` |
| **S4 NOT CROWDED** | the coupled side has **not** moved on or after **2025-01-01** by an AI-driven search system or by large-scale optimisation tooling |
| **S5 DELIVERABLE** | a named maintained table, or a named published bound, changes on a one-step improvement, and the abstract sentence can be written |

## Move kinds, for S3. Verbatim.

| kind | definition |
|---|---|
| `ANALYTIC` | the record object or bound was derived by hand — explicit formula, algebraic or combinatorial construction, proof. Computation, if any, only verified it. |
| `SEARCH-NEW` | produced by computer search or optimisation with a method the paper **introduces, or is the first to apply to this record** |
| `SEARCH-REPEAT` | produced by computer search or optimisation with a method **already used on this record** by earlier work: a bigger run, more restarts, refined parameters, more hardware |
| `UNKNOWN` | the sources available do not say |

`IDEA := ANALYTIC ∪ SEARCH-NEW`. `COMPUTE := SEARCH-REPEAT`. Flag `AI-SEARCH` additionally when the
move was made by an LLM- or RL-driven search system; the **first** such move on a record is
`SEARCH-NEW`, later ones by the same family are `SEARCH-REPEAT`.

**The gap type is the kind of the single most recent move.** Record the second-most-recent move too,
but do not score it — using two moves creates a middle case with no verdict, which is a failure this
project already has a name for.

---

## One change from the earlier run, applied deliberately and reported both ways

That run concluded, in its own words: *"The crowding gate is scoped wrongly. A table on which three
AI systems moved two neighbouring cells within twelve months is crowded in the sense that matters —
our reachable region sits inside theirs — even when a given cell has not moved."* It registered the
fix and did **not** apply it retroactively.

**Apply it here, prospectively, and report S4 twice:**

* `S4-record` — has **this record** moved since 2025-01-01 by an AI search or large-scale
  optimisation system? (the original, record-scoped gate)
* `S4-table` — has **any cell in this table** moved since 2025-01-01 that way?

Give both. Where they disagree, that disagreement is a finding and is more interesting than either
verdict. **A table passes only if `S4-table` passes**, but I want the record-scoped answer beside it
so the two scopings can be compared on real data for the first time.

Two AI systems you will meet repeatedly and should check against by name: **AlphaEvolve**
(arXiv:2506.13131, plus `github.com/google-deepmind/alphaevolve_repository_of_problems`) and
**EinsteinArena** (arXiv:2606.10402), whose Table 1 is a live public list of the record problems AI
agents are working. Also **PackingStar** (arXiv:2511.13391), **X-evolve** (arXiv:2508.07932), and
**Qiushi Engine** (arXiv:2609.35051, nineteen new kissing-number bounds at dimensions 25, 27, 32–39,
43, 45, 49–55).

---

## 2. Budget

**Stop after 20 searches-or-fetches.** Then report. Mark any table you did not reach as NOT
REACHED rather than guessing at it. **A partial report is a success** — the failure this brief exists
to fix is a run that spent its budget and recorded nothing.

Spend your budget in this order for each table: (i) find and **open** the maintained table, (ii) read
the specified record's current value and its date, (iii) find the paper that last moved it and
**open its method section**. Step (iii) is what S3 needs and is the step the earlier run could never
reach. If you must drop a step, drop (iii) and say so — an S3 of `UNKNOWN` is FAIL, correctly, and is
still worth recording with the value at `SECONDARY-RELAYED`.

---

## 3. Output — one block per table

```
TABLE          | <name>
MAINTAINED AT  | <url actually opened, and the table's own date / last-modified if it shows one>
RECORD         | <the pre-specified record, restated>
CURRENT VALUE  | <value> | <tier> | <EXACT|NUMERICAL|…> | <REFEREED|PREPRINT|…>
LAST MOVED     | <date, paper, author>
MOVE KIND      | <ANALYTIC|SEARCH-NEW|SEARCH-REPEAT|UNKNOWN> + <AI-SEARCH flag?> | <evidence, from the method section>
PREVIOUS MOVE  | <recorded, not scored>
S0 OPEN        | PASS|FAIL  <why>
S1 COUPLED     | PASS|FAIL  <which route, (a) or (b), or the lifting theorem by name>
S2 NOT VETOED  | PASS|FAIL  <why>
S3 IDEA GAP    | PASS|FAIL  <from MOVE KIND>
S4-record      | PASS|FAIL  <this record, since 2025-01-01>
S4-table       | PASS|FAIL  <any cell in this table, since 2025-01-01>
S5 DELIVERABLE | PASS|FAIL  <the table row that changes, and the abstract sentence, written out>
VERDICT        | triage survivor | FAIL at <first gate that failed>
```

At the top of your reply:

1. **The verdict line for each table**, in one table.
2. **Where `S4-record` and `S4-table` disagree** — that is a finding in its own right and the first
   real data on which scoping is right.
3. **Anything that contradicts this brief.** Several of the values below are relayed from a run that
   could not open its sources; if one is wrong, that is the most useful thing you can report.

**Do not recommend what to do next.** The verdicts and their tiers are the deliverable. A table that
FAILs with clean evidence at `SECONDARY-RELAYED` is a complete result.

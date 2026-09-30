# Brief C — five arm-1 verdicts that rest on a tier the last run could not improve

**For a Sonnet 5.5 instance in a chat conversation with web search and page fetching. No repository,
no filesystem. Your output is a document in your reply.**

Arm 1 screened nineteen records and returned **0 full-bar survivors**. That result stands and this
brief does not reopen it. But **five of those nineteen failed on a cell the earlier container could
not reach**, and each is one specific question with a yes-or-no answer. This brief asks those five
questions and nothing else.

Four of the five turn on the **same clause**, so read it once and carry it through:

> **S1 COUPLED** … An asymptotic-order headline is COUPLED only through a **published lifting
> theorem** that turns a finite object into an asymptotic bound (the cap-set product construction is
> the model case).

The model case is worth holding in mind precisely, because it is the shape you are looking for
everywhere below: a cap set of size *c* in 𝔽₃ⁿ can be **tensored** with itself to give caps of size
*c*^k in 𝔽₃^(nk), so **one finite object of size *c* in dimension *n* yields the asymptotic lower
bound *c*^(1/n) on the cap-set constant.** That is a lifting theorem. It is what makes a finite search
move an asymptotic headline. **Your question, four times over, is whether the analogous theorem exists
and is published.**

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
was **5,799**, with the higher papers admitting their verification was *"mostly partial."* Both cells
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


---

## 1. The five questions

**Q1 — record 186, the order of magnitude of maximum 3-term-AP-free subsets of {1,…,N}.**
Arm 1 returned **S1 FAIL** on this note: *"asymptotic; only lifting known is the product lemma, giving
N^α with α<1"* — **and tiered that note `RECALL`.** A FAIL resting on RECALL is the weakest verdict in
the whole arm.
> **Ask:** is there a published lifting or product theorem taking a finite AP-free set in {1,…,N} to
> an asymptotic bound on the order of magnitude of the maximum? What exactly does the product lemma
> give, and is α<1 correct? Behrend's construction and the Kelley–Meka upper bound are the landmarks
> to orient by. **Answer at `SECONDARY-RELAYED` — read the statement, do not relay a summary of it.**

**Q2 — record 277, the growth rate of 3-uniform hypergraph Ramsey numbers.**
Arm 1 returned **S1 = CANNOT EVALUATE**: *"could not check for a lifting theorem."*
> **Ask:** does a published construction lift a finite 3-uniform hypergraph colouring into an
> asymptotic lower bound on the growth rate? Erdős–Hajnal–Rado is the classical line; look for a
> product or amplification lemma.

**Q3 — record 353, the asymptotic Turán numbers of even cycles.**
Arm 1 returned **S1 = CANNOT EVALUATE**, same reason.
> **Ask:** for ex(n, C_2k), does a published theorem take a finite extremal or near-extremal graph to
> an asymptotic constant or order? The Bondy–Simonovits upper bound O(n^(1+1/k)) is the landmark;
> the question is about the **lower-bound** side and whether a finite object lifts.

**Q4 — record 375, the sharp asymptotic order of the minimal star discrepancy in each dimension.**
Arm 1 returned **S1 FAIL** on *"asymptotic, no lifting theorem seen."* **"Not seen" is a weaker claim
than "does not exist"**, and the container could not open the sources that would settle it.
> **Ask:** does a published theorem take a finite point set of given discrepancy to an asymptotic
> bound on the order in that dimension? Note the specific trap here: this literature is full of
> results where the **dimension dependence** is the open part, so be precise about which quantity the
> asymptotics is in — *n* or *d*.

**Q5 — record 385, the Lieb–Thirring conjecture on the sharp constant for Riesz means.**
Arm 1 returned **S1 = PASS (formal)** but **S2 = CANNOT EVALUATE**: *"the witness side is a
counterexample potential; no rigorous-enclosure source found."* This one is not a lifting question.
> **Ask:** is there a published **rigorous numerical enclosure** — interval arithmetic, a
> computer-assisted proof, a certified bound — for the relevant Lieb–Thirring constant, such that a
> candidate counterexample could be certified by terminating computation? The distinction that decides
> S2 is **RIGOROUS-NUMERIC versus merely NUMERICAL**, and this project has been burned by exactly that
> distinction before. If the literature offers only floating-point computations, say so: that is a
> clean S2 FAIL and a real answer.

---

## 2. What a good answer looks like, and what an answer is not

For each question, one block:

```
RECORD        | <number and name>
QUESTION      | <restated in one line>
ANSWER        | YES, a published theorem exists | NO, and here is why that is established | UNRESOLVED
THE THEOREM   | <name, authors, year, and the statement in one or two lines> — or "none found"
SOURCE OPENED | <url or citation you actually read>
TIER          | SECONDARY-RELAYED | SEARCH-SUMMARY | RECALL
WHAT IT GIVES | <what a finite object of size X in dimension/length n yields asymptotically — the arithmetic, if any>
GATE EFFECT   | <does S1 (or S2 for Q5) now PASS or FAIL, and is that a change from arm 1's verdict?>
```

**A `NO` is as valuable as a `YES` and harder to earn.** "I searched and found nothing" is not a NO;
it is UNRESOLVED. A NO needs either a source saying no such lifting is known, or a survey of the
lower-bound methods that would have mentioned one. **Say which of the three you are giving.**

**If any answer flips a gate, say so plainly but do not re-run the rest of the bar.** Arm 1's other
gates for that record stand as recorded; your job is the one cell. Flipping S1 on record 186 from a
RECALL-grade FAIL to a sourced PASS would not resurrect the record — it still has S3, S4 and S5 to
pass — but it would mean the arm's headline number was reached partly by a cell that could not carry
it, and that is worth knowing about the instrument regardless of the record.

---

## 3. Budget

**Stop after 15 searches-or-fetches**, roughly three per question. Report what you have and mark the
rest NOT REACHED. **A partial report is a success.** Three questions answered at
`SECONDARY-RELAYED` beats five answered at `SEARCH-SUMMARY`, because the second adds nothing to what
is already on file.

**Do not recommend what to do next.** The five answers and their tiers are the deliverable.

# The v3 queue — record problems, and why the pool already contained them

Built on `../gap/GAP_V3.md`. Everything below is **recall, not verified**; the first check named
for each is the promoting search that decides it, and is named before anyone looks so it cannot be
re-scoped afterwards.

> **[29 Sep 2026 — discovery run, `../gap/RESULT_DISCOVERY.md`.]** Read this box first.
>
> **What the run found about this queue:**
> * **Its record-shaped items do not contradict the playability screen.** Each is the P1 conjunct
>   of an `II` headline, since "determine the value" = ∃ ∧ ∀ (`../gap/RESULT_ARM1_II.md` §1). So
>   each has to pass gap type and crowding on its own.
> * **Queue #2 (kissing, dimensions 11–14) is split.**
>   * Dimension 11 is **dead** — moved by AI twice since 2025, now 604.
>   * Dimension 12 is dead too: a numerical 841 (June 2026) with an unknown method.
>   * **Dimensions 13 and 14 survive as triage candidates C-1 and C-2**, with promoting bars
>     written. The whole table is under active AI attack, so treat both as fragile.
> * **Queue #3 (caps).**
>   * AG(8,3) = 512 survives only as **C-3**, the weakest of the three — the neighbouring capacity
>     record was AI-moved in 2025.
>   * AG(7,3) fails: its move kind is unknown.
> * **Queue #4 (snakes): fails.** The records moved in July 2026 (arXiv:2607.15270) by a method
>   that could not be read.
> * **Queue #1 (U13 D-optimal): no verdict here.** The promoting search belongs to the Sonnet S55
>   run, whose results (RESULT_S55_A_TABLE.md and siblings) were **not present** on the branch at
>   the end of this run. Their outcome is unknown and not assumed.
>
> **[29 Sep 2026 — gate C-3 run, `../gap/discovery/RESULT_GATE_C3.md`.] C-3 is DEAD.** The bar fired
> on positive evidence: X-evolve (arXiv:2508.07932) reports direct AG(8,3) runs reaching 512 — an
> *n* = 8 column in Table 2, three of five runs at 512 in §3.1, an *n* = 8 ablation in Table 5 — and
> two further post-2023 systems ran *n* = 8 directly and fell short. The prompt's hedge that X-evolve
> had moved only the capacity was wrong: it worked both objects.
>
> **Two things the bar did not ask about, and both outrank the verdict.**
> * **C-3's deliverable table may not exist.** Edel's page was last changed 28 April 2010, tabulates
>   *projective* m₂(*k*,*q*) — row 8, *q* = 3 is **541**, a PG(8,3) cap — and gives no affine *n* = 8
>   row at all. Relayed; this container's egress proxy blocks the page. **No candidate on this board
>   has ever had its "table it moves" field checked. See debt D46.**
> * **512 may never have been the frontier.** One unattributed search summary gives an affine AG(8,3)
>   lower bound of **532**. Not promoted — the obvious source, Elsholtz–Lipnik, covers p ≡ 5 (mod 6)
>   and so not p = 3. Promoting search named in §4 of the gate result.
>
> **Queue now:** U13 still pending S55, holding its place. **C-1 τ₁₃ ≥ 1154**, then **C-2 τ₁₄ ≥ 1932**.
> C-3 struck. 239 and 345 unchanged, pending S55. Before either surviving candidate is gated,
> **check that its table exists and contains the claimed row** — one lookup each, and it is the
> cheapest kill available.

> **[29 Sep 2026 — Cohn's table checked, `../gap/discovery/TABLE_KISSING.md`.]** D46's check run on
> C-1 and C-2: **the table exists and rows 13 and 14 carry exactly 1154 and 1932.** Passed, where
> Edel's failed. The reference column then split the two candidates on a criterion neither bar
> mentions: **d = 13's lower bound is Zinoviev–Ericson 1999 — 27 years frozen, clearing this
> document's own ten-year rule by 17 — while d = 14's is Ganzhinov (LAA 2025, arXiv 2022) and fails
> it on either dating.** Both upper bounds are de Laat–Leijenhorst's 2024 SDP, so at d = 13 the
> ceiling is actively worked and the floor has not moved in a generation, with a factor of 1.79
> between them. **C-1's bar is now half discharged** — 1154 stands at primary tier; the attempt
> conjunct is untouched and a record table cannot supply it. **C-2 is not struck**, because headroom
> is not in its bar and re-scoping after the fact is what D44 exists to prevent; recorded there as a
> bar-design gap instead. Run C-1's remaining conjunct first.

> **[29 Sep 2026 — gate C-1 run, `../gap/discovery/RESULT_GATE_C1.md`. C-1 is DEAD, and the queue is
> empty below U13.]** Both papers the bar named were read. **EinsteinArena** (arXiv:2606.10402v2)
> works the kissing number at **dimension 11 only** — fifteen problems on its board, curated from
> AlphaEvolve. **Qiushi Engine** (arXiv:2609.35051v1) reports nineteen new bounds at 25, 27, 32–39,
> 43, 45, 49–55. Neither attempted *d* = 13, so the bar fires: **FAIL**.
>
> **What the papers say that the bars did not ask.** Qiushi produced nineteen dimensions in one
> paper with machine-checkable certificates; EinsteinArena produced eleven SOTA results in two months
> from a 19 March 2026 launch. **The record-problem niche is being swept at industrial rate**, which
> is the crowding gate's subject, now measured. But every system's dimension range tracks *where
> algebraic structure exists* — Leech, E₈, Golay, P48 — hence 25–55, with *d* = 11 worked only
> because AlphaEvolve seeded it. **Dimensions 13–14 have nothing to lift from**, which is plausibly
> why Zinoviev–Ericson 1999 still stands. That is a hardness reading the bar could not see, and it is
> recorded rather than used: the verdict stands as the bar gave it.
>
> **One free instrument gained.** EinsteinArena's Table 1 is a maintained public list of record
> problems AI agents are actively working, with prior-best and current-best columns — the crowding
> instrument this board lacked. Screened against the 22 `II` records with every collision
> adjudicated: **1 genuine of 22.** **368 Thomson is on the active board — struck.** 428
> site-percolation collided on the word "square" only and is spurious. One of twenty-two is the first
> positive signal arm 1 has produced.
>
> **Queue now: U13 alone, still pending S55.** C-1, C-2 and C-3 are all struck. 239 and 345 unchanged,
> pending S55. All three bars tested crowding and none was decided by it — **D47**.

> **[30 Sep 2026 — U13 deferred by the operator; the queue is empty and the inventory below is what
> is left.]** U13 is **not killed** — it returns if and when the Hadamard thread runs its course. So
> the queue has no active item, and the honest position is that the 499-record corpus is exhausted
> (two screens, a 106-record mapping, and arm 1's 19 `II` records at **0 of 19** full-bar survivors)
> and the record-table seam is nearly so.
>
> **What is left is not a new seam. It is two instruments that stopped on budget rather than on
> evidence, and one of them is the only generative one ever designed.**
>
> | # | option | status | why it is still live |
> |---|---|---|---|
> | 1 | **Arm 2b, the divergence search (P-35)** | **never ran** | `../gap/RESULT_ARM2_TABLES.md` §4: the worker read 67 AlphaEvolve problem pages and 10 notebooks and was cut off at a concurrency cap before recording **any** entry. *"The instrument did not run, which is different from running and returning nothing."* The only screen designed to **generate** rather than filter. |
> | 2 | **Arm 2 tables 6–10** — Williamson, Steiner systems, difference sets, Costas arrays, bent functions | **never assessed** | Same §1: worker stopped at the concurrency cap and search budget. *"A full run could only raise the count."* These are the design-theory seam `../../proof-protocol/ledger.json` lesson 22 found absent from the 499, and `../gap/discovery/RESULT_GATE_C1.md` §6 established they are **not on EinsteinArena's board** either. |
> | 3 | **The *b* > 2 Hadamard region** | open question, never asked | This document's own fifth candidate: 126+ admissible (*v*, *b*) pairs with *b* > 2 across the thirteen open orders, and orders 669 and 721 *"never screened or settled by anything in this repository."* Needs no new literature and sits **inside the live thread**. |
> | 4 | **277** 3-uniform hypergraph Ramsey growth, **353** Turán number of even cycles | `CE`, unevaluated | `../gap/RESULT_ARM1_II.md` §2 returns both as CANNOT EVALUATE for one reason — *"could not check for a lifting theorem."* `CE` counts as FAIL and should; but these two are unevaluated rather than refuted, and it is one literature check each. |
> | 5 | **239** odd perfect number, **345** Erdős–Szekeres | pending S55 | The S55 result documents have **still not appeared on this branch.** Their fate is unknown and is not assumed. |
> | 6 | **Enter EinsteinArena rather than hunt private targets** | route change, never considered | Four cells on its Table 1 carry AlphaEvolve's number with no platform improvement: circles in a square *n* = 26, difference bases, Heilbronn triangles *n* = 11, Thomson *n* = 282. Public downloadable verifiers, a live leaderboard and an API. **H, Δ and crowding are all published continuously** — exactly what every failed gate on this board needed and could not get until after paying for the search. |
>
> **One caveat that applies to 1 and 2.** `../gap/RESULT_ARM2_TABLES.md` §3 registers a scoping fix
> that has not been applied: **crowding should be scoped to the table, not the record.** Under it all
> three of arm 2's survivors die and arm 2 returns 0 — and options 1 and 2 must be screened at table
> level too. The instrument for that now exists and is free: EinsteinArena's Table 1 plus the
> AlphaEvolve problem repository.

> **[30 Sep 2026 — briefs A and B1 run, `../gap/discovery/RESULT_A2B_DIVERGENCE.md` and
> `../gap/discovery/RESULT_B1_DESIGNS.md`.] Arm 2 now stands at 13 of 15 tables assessed and 0 live survivors.**
> B1 returned Williamson **FAIL at S0**, Steiner **FAIL at S3**, cyclic difference sets **FAIL at S3**.
> Only Costas and bent functions remain, with brief B2.
>
> **Three findings outrank the verdicts.**
> * **Crowding has a third scoping, and it corrects what I wrote here.** The *signed* difference set
>   table — same La Jolla repository family — was swept Aug–Sep 2026, **all 68 open small entries
>   resolved**, by a GitHub project whose README **discloses extensive OpenAI Codex use**. The entry
>   above says this seam is "not on EinsteinArena's board"; that is true and I read it as unswept.
>   **Not on a board is not the same as not being swept.** No board-based crowding screen can see a
>   sweep like that. Record / table / **repository-family**.
> * **S3 is an access gate and it is now the binding one — D50.** Tables 7 and 8 both died on move
>   kind `UNKNOWN` because a method section could not be opened, not on evidence the move was compute.
>   With arm 1's 277 and 353, **four of the last five FAILs on this board are access failures wearing
>   gap-type clothing.** A long run of FAILs reads as a well-screened empty seam and may be a
>   well-documented paywall.
> * **Arm 2b's divergence search fired and did not discriminate — D48.** Four entries met the
>   registered definition and none has two independent groups with contemporaneous methods, because
>   the definition has no time window and no independence clause. 22 calls, many temporal reach
>   ratios, zero live capability gaps.
>
> Also: the Williamson route does not reach this project's target — order 65 gives H(260), already
> known, and **H(668) needs Williamson order 167**. And the exact-SIC ceiling is **5,779**, not 5,799
> (**D49**), a digit our own arithmetic check caught and then explained away.

> **[30 Sep 2026 — brief B2 run, `../gap/discovery/RESULT_B2_SEQUENCES.md`. ARM 2 IS CLOSED: 15 of 15
> tables assessed, 0 live survivors.]** Costas **FAIL at S3** (value **32**, not the 29 I supplied —
> the enumeration frontier is a different quantity), bent functions **FAIL at S1** (a count frontier;
> exhibiting one more moves nothing). **The record-table seam is finished.** Of the six options
> inventoried above, 1 and 2 are now spent; Williamson order 65 has gone to the Hadamard instance;
> what remains is **3 (the *b* > 2 Hadamard region), 4 (277 and 353, brief C), 5 (239 and 345,
> still pending S55) and 6 (enter EinsteinArena)**.
>
> **Two instrument findings outlast all of it, and both say the screen has been measuring itself.**
> * **D50, now observed rather than hypothesised.** Six consecutive S3 failures — tables 7, 8, 9, 10
>   and records 277, 353 — **all for want of a method section, and not one on evidence that the move
>   was `SEARCH-REPEAT`.** Every table in arm 2 that reached S3 died there.
> * **D51: S4 is built on the wrong observable.** It counts *moves*, so it cannot see an *attempt that
>   failed*. Rosin's CPro1 (arXiv:2505.23881) put LLM-driven search on Costas arrays in 2025 and moved
>   nothing — invisible to both scopings. C-1's bar called an attempt PASS evidence, C-3's called it
>   FAIL, S4 cannot see it. **Three instruments, three readings of one fact**, and the state they
>   disagree about is the only one that separates a durable opportunity from an unvisited cell.
>
> So the honest reading of "13 of 15 assessed, 0 survivors" is not that the seam is barren. It is that
> **S3 measured our access and S4 measured the wrong thing.** That is worth more than the two
> candidates the seam was searched for.

> **[30 Sep 2026 — Costas reopened at the operator's instruction, `../costas/PLAN_COSTAS.md`.]**
> B2 closed Costas at **S3, "method unread → UNKNOWN"** — an **access** failure, not an evidence
> failure, and one of the six that opened **D50**. Re-running a gate whose input was never obtained is
> not the re-scope D44 forbids; S1 passed and S4 passed, and nothing in B2 is evidence against the cell.
>
> **What is new is a local structural computation, `../costas/costas_support.py`, and it gives this
> board the first candidate it has ever had with a measurable positive control.**
> `PRIMARY-VERIFIED-LOCALLY`: corner-deletion chains descend at most **4** steps, so with **no prime in
> [32,36] and no prime power in [33,36]**, orders **31, 32 and 33 have no Welch or Golomb array at any
> depth** — the only field that nominally reaches them is 37, built, and its chains bottom out at 34.
> **Order 31 nonetheless has ≥ 8 known arrays, so they are necessarily sporadic**, and
> log2(31!) = 112.66 against log2(32!) = 117.66 — **a 5.00-bit gap to a solved instance of the same
> unstructured problem.** Every previous gate on this board failed for want of exactly that handle.
>
> **The plan is Sonnet-first through a registered bar, `../gap/discovery/prompts/s55/D_COSTAS.md`
> (brief D, 20 calls, five reads and no search).** PASS iff **(a)** a published structural
> characterisation of sporadic arrays exists that constrains the space **and (b)** no heuristic search
> at order 32 is reported as run and failed. FAIL on either → *attempted-and-failed with no structural
> lever*, and Opus is not spent. **P-37 predicts FAIL on (a)**, for the cost of one chat conversation.
>
> **Three things recorded against the plan at the same time as the plan.** The state of the art for
> Costas *is* backtracking DFS, which is what an LLM writes — CPro1's generated strategies included it
> and it was not enough, and the community's version carries 366.55 CPU-years behind order 29. CPro1's
> failure fits its own §5 pattern of heavily-worked design types, which is a prediction about *this*
> cell. And **non-existence at order 32 is possible and no constructive search can settle it**, which
> is why the order-31 rediscovery control in phase 1 is mandatory rather than nice to have: it is the
> only instrument that separates "searched badly" from "nothing there".
>
> **Queue:** brief D is the active item. Options 3 (*b* > 2 Hadamard), 4 (277/353, brief C) and 6
> (EinsteinArena) unchanged; 5 (239/345) still pending S55 results that have never appeared.

> **Queue as of this run.** U13 is pending S55 and holds its place. Beneath it, three triage
> candidates in this order: **C-1 τ₁₃ ≥ 1154**, **C-2 τ₁₄ ≥ 1932**, **C-3 AG(8,3) cap 512**. Each
> enters only through its bar in `../gap/RESULT_DISCOVERY.md` §2. 239 and 345 are unchanged,
> pending S55. **No candidate carries a measured idea gap.** The run's main result is negative and
> concerns the instruments: movement-history gap typing cannot see compute gaps, and crowding is the
> gate that works.

## The move, in one line

v2's E dimension asked *"is the null publishable?"*, which rejects by construction the class where
the deliverable is cleanest. **Four record problems have been sitting in the unverified pool since
the v2 run, unpromoted, for exactly that reason.** They are the queue.

A record has a stated current value, so the three v3 dimensions are all computable *without a
literature survey*: **H** from the record itself, **Δ** from the table it lives in, **P** from
whether the record has moved recently.

## The evidence that this category is model-sensitive

DeepMind's FunSearch (Romera-Paredes et al., *Nature* 2024) used an LLM-driven search to improve
the **cap-set** record in AG(8,3). That is a direct existence proof that this exact class of
record problem moves under model capability — which is the `../gap/GAP_V3.md` §3 claim, demonstrated
rather than argued.

It cuts both ways, and the cut matters: **the flagship instance is taken.** The right reading is
to use FunSearch as evidence *for the category* and then pick a record inside it that FunSearch
did not touch. That is why cap sets are third below and not first.

## The queue

| # | candidate | pool id | table it moves | first check |
|---|---|---|---|---|
| **1** | **D-optimal designs of order 2*v*** | U13 | the D-optimal existence/determinant table (Fletcher–Koukouvinos–Seberry lineage) | current table: which *v* are open, and when was each last moved? |
| **2** | **Kissing-number lower bounds, dims 11–14** | U8 | the kissing-number table (Nebe–Sloane) | current τ*ₙ* lower bounds for *n* = 11–14 and the date each was last improved |
| **3** | **Caps in AG(7,3) / AG(8,3)** | U10 | the cap-set record table | post-FunSearch records, and whether anyone is still running on it |
| **4** | **Snake-in-the-box, dims 9–11** | U9 | the longest-induced-path record table | current records and the method that set them |

**Why 1 is first.** D-optimal designs are the nearest neighbour of the Hadamard machinery this
project already has — ±1 matrices, determinant maximisation, the same orbit and PAF apparatus —
so the algorithmic-idea gap, if there is one, is one we are already tooled for. They are also the
least famous of the four, which under `../gap/GAP_V3.md` §3 is a feature rather than a defect.

**Why 4 is last.** Snake-in-the-box has been attacked with genetic algorithms and SAT for
decades; the records are likely compute-set rather than idea-set, which is the category that does
not improve.

## A fifth candidate that is not in the corpus and needs the original instance

`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` says, of the thirteen open orders:

> *"Across all 13 orders there are 126+ admissible (v, b) pairs with b > 2."*

and, of orders 669 and 721:

> *"those two orders have never been screened or settled by anything in this repository."*

That is a **writable, un-swept region inside the primary thread**, requiring no new literature.
**But I cannot tell from outside whether it is live**: `FINDING_128` finds the *b* = 1 border
inert (for reverse-engineering — a different question), and `FINDING_133` reports the
orbit-reduction route stopping at *m* = 82 with failures that are emptiness rather than solver
weakness. **Question for the original instance, not a proposal from me:** is the *b* > 2 region
open, or closed by something I did not read?

## Direction B — CORRECTED. The rejection was an aggregate used as a per-record verdict

> **[21 Sep, after challenge.]** The section below rejects "items closer to the head" on a
> density statistic. **That is not a valid rejection of any individual record**, and it was worse
> than it looked: the tail scan started at rank 250 and the collaboration check stopped at 120, so
> **ranks 121–250 were never screened at all.** A collaboration route also does not imply heavy
> competition — everything on a top-500 list has some by definition.

**Now screened.** 230 records in ranks 120–350; **106 carry record or algorithmic-deficit
language** — the two gap types `../gap/GAP_V3.md` §3 says improve. The band is not barren. A
sample of what is in it:

| rank | record | shape |
|---:|---|---|
| ~~337~~ | ~~Capacity of the binary deletion channel~~ | **DEAD** — arXiv:2609.19412 narrows it to a hundredth of a bit, Sep 2026. See `STALENESS.md` |
| 283 | Polynomial-time explicit logarithmic Ramsey graphs | pure algorithmic-idea gap |
| ~~234~~ | ~~k-Server Conjecture, general metrics~~ | **RESOLVED 14 Sep 2026**, arXiv:2609.15979 — five days before the corpus that lists it `open` shipped |
| 310 | Deterministic polynomial-time exact bipartite matching | algorithmic-idea gap |
| 345 | Erdős–Szekeres / Happy Ending | exact ES(7) |

### And the structural reason the band *looked* barren

**The corpus records headline statements, not the record tables underneath them.** Every one of
the five above is recorded as *"determine the exact value"* or *"prove the conjecture"* — the
hopeless form. The live, movable quantity is never mentioned:

| headline as recorded | what the literature actually tracks |
|---|---|
| "determine C_del(*d*) exactly" | best known **upper and lower bounds** on the deletion-channel capacity |
| "prove the competitive ratio is *k*" | best known **upper bound** (2*k*−1, Koutsoupias–Papadimitriou) |
| "determine ES(*n*) exactly" | the **bounds on ES(7)**, lower 33 by construction |

This is the same limitation that made the writable-unknown-set regex return zero: the corpus is a
statement catalogue, not a status inventory. **Screening it alone cannot surface a record problem,
because the record is a sub-problem of the headline and the headline is what is written down.**

### The missing piece, and it is the cheap kind

What is needed is a **mapping layer**: headline → the quantity the literature tracks → its current
value → when it last moved. One question per record, 106 records, independent, no reasoning depth
required. That is precisely the breadth-shaped task `../gap/GAP_V3.md` §6 says gets cheaper, and it
is the highest-value thing a cheap instance could do next.

**~~Best single mid-band candidate: rank 337.~~ WRONG, and corrected within six hours — see
`STALENESS.md`. 337 is among the most actively worked problems on the list.** Δ is clean (a bounds table), the gap is analytic rather than compute, and it carries
**no collaboration route** — so on this corpus's own signal nobody has flagged it.

### Why U13 is still first

D-optimal designs have the one property none of the above do: **the record table is explicitly
maintained and public** (the Hadamard maximal-determinant tables, Orrick–Solomon lineage), so H
and Δ are computable on day one instead of after a 106-record mapping exercise. And the objects
are ±1 matrices with the same PAF and orbit apparatus already built for Hadamard.

---

## Direction B, as originally written — superseded by the correction above

## Direction B, answered with a number rather than a hunch

"Items closer to the head" was worth testing because collaboration routes concentrate there:

| rank band | records with a collaboration route |
|---|---|
| 1–100 | **48%** |
| 101–200 | 25% |
| 201–300 | 21% |
| 301–400 | 16% |
| 401–500 | 13% |

3.7× the density at the head. **But it does not convert.** Every head record in the discrete /
TCS / crypto domains with a route attached is a complexity separation — P vs NP, one-way
functions, NC vs P, P vs BPP, VP ≠ VNP, Unique Games, ETH, SETH, L vs NL, Hadwiger. Those have no
finite witness, no stated record, and a gap that is neither compute nor a bounded algorithmic
deficit but an open research programme. The collaboration density is real and it is attached to
problems where nothing we can do moves anything.

**So: head of the list, no. The collaboration routes worth harvesting are the ones on items we
already hold** — Hadamard (331), CC-6 (393), MUB (426) — and that is a harvest, not a target.

## Direction C, as an operating rule rather than a forecast

From `../gap/GAP_V3.md` §6, with no claim about what is coming or when:

1. **Run the screen wider, not deeper.** The expensive part of this session was reading and
   adjudicating — 41 Epoch entries, 499 corpus records, 163 findings, two papers. That is a
   breadth gap and it is the one that gets cheaper. A v3 screen that currently yields four
   candidates per expensive run should be run over a far larger candidate space instead of over
   one corpus again.
2. **Hold exactly one algorithmic-idea target and state its gap as a number.** Hadamard 2092
   qualifies: 0.503 against 0.252, from FINDING 157 §3. Nothing else on this board does.
3. **Stop holding compute-gap targets.** PTE 11 stays dead through any release.

## What would put something in the queue tomorrow

Any one of the four first checks above coming back with: *a record that has not moved in ten
years, in a table we can name, with a construction method we are already tooled for.* That is
three cheap lookups and it is the whole gate.

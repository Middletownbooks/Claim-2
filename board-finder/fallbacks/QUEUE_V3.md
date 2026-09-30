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

> **[30 Sep 2026 — brief D ran, `../gap/discovery/RESULT_D_COSTAS.md`. COSTAS ORDER 32 IS CLOSED, and
> the box above it was wrong.]** `D: FAIL` on clause (a) — no structural characterisation of sporadic
> arrays exists — and **P-37 is CORRECT**. But the verdict is the least of it.
>
> **The premise I wrote into the brief as "treat it as given" was false, and the run refused it.** The
> order-31 arrays are not sporadic: they are **W₀ arrays**, a Welch *p* = 31 array with a corner dot
> **added**. My computation modelled corner *deletion* only. Re-verified locally in
> `../costas/costas_support.py` PART 7: exactly **8** under the dihedral group, matching the relayed
> count to the digit, and the run's explicit array lies in that class. **So the 5.00-bit positive
> control — the entire reason this cell was reopened — does not exist.** The nearest search frontier is
> order 22–23, **43.21 bits** below the target. Phase 1 was not run. **D53**.
>
> **What survives is a better argument than the bar's, and it is measured.** Closing the seeds under
> *both* operators and over GF(25), GF(27) and GF(32) as well: order 28 is **712 of 712**
> constructible, order 30 is **exactly 664**, order 31 is **exactly 8**, and order 29's 16-array
> residual is **exactly 2 × 8** — matching the two order-29 classes the run attributes to Rickard's
> periodicity method, a third construction I had not modelled. **Nothing near the frontier is
> unexplained; the last unexplained array is at order 27.** Arrays above 27 exist where a construction
> lands, and **32 and 33 are precisely where none lands.** Two of those counts match relayed figures to
> the digit, from computations that were not fitted to them.
>
> **And one of my two headline arguments against the cell was withdrawn, not confirmed.** CPro1's
> Table 4 strategies belong to its seven *solved* design types, so "the model already wrote DFS and it
> was not enough" is unsupported — what CPro1 generated for Costas is not established. The
> "sustained development" quote is in its §1, not §5.
>
> **This is the fourth gate on this board whose verdict and whose decisive finding came from different
> questions** (D47's pattern, now one level up: the bar tested the right thing and the evidence arrived
> through the report-anything-contradictory clause). **Queue:** options 3 (*b* > 2 Hadamard), 4
> (277/353, brief C) and 6 (EinsteinArena) unchanged; 5 (239/345) still pending S55 results that have
> never appeared. No active item.

> **[30 Sep 2026 — brief C answered TWICE, independently and by accident,
> `../gap/discovery/RESULT_C_ARM1_CELLS.md`. The replication outranks the verdicts.]**
> **Arm 1's 0 of 19 stands and is now better founded.** 277 and 353 move CANNOT EVALUATE → **FAIL**,
> 375's *"not seen"* becomes an established absence, 186's FAIL loses its `RECALL` basis, and 385
> **splits between the runs**. Option 4 is spent; nothing was resurrected.
>
> **The replication is the first robustness measurement any instrument on this board has had.** The two
> runs opened sixteen sources with an **overlap of two**, answered every question from a different
> paper — Hunter against EHPS, Conlon–Fox–Sudakov against Mubayi–Suk, Füredi–Naor–Verstraëte against
> Füredi–Simonovits, Ostromoukhov against Pillichshammer — and **agreed on four of five verdicts
> anyway.** Both also independently built the same Lieb–Thirring float control and independently
> flagged that Q2's and Q4's labels each cover several quantities.
>
> **Three instrument findings, and each is worth more than a verdict.**
> * **D54 — P-31 A-1 is not evaluable as worded.** Its threshold fires when a run *"issues a verdict on
>   a bar it could not evaluate"*; standing rule 1 tells every run to do exactly that. The two runs
>   split precisely here and **both were compliant**. Not redrawn (D44); A-1 stays OPEN, and brief C is
>   not in its reserved slice so nothing is scored. The cost rule 1 hides: it erases the difference
>   between an absence *established* and one a run says it **did not earn** — and run 2's more
>   disciplined answer gets no credit for it.
> * **D55 — the brief budgets calls and context is what binds.** Run 1 spent 22 of 22; run 2 stopped at
>   **18**, saying further large PDFs *"risk swamping the report"*. The cap was tuned twice on
>   call-failure rates, i.e. on the wrong resource.
> * **S1 COUPLED cannot tell a constant from an order.** Both runs reported *two* readings rather than
>   choosing: a real lifting theorem exists for 186 and for 375's *d* = 1 constant, and it moves a
>   constant — run 1 measured its own Q4 find at **0.61%**. The `STRENGTH` field added at dispatch is
>   what surfaced this. A clause that passes on a 0.61% constant is not measuring what this board wants.
>
> **And D50 is confirmed and defused at once.** Its access remedy has now run three times — Costas plus
> these five cells, twice — and **every cell died anyway, on evidence. Three of three.** The access
> failure was real; the hope that it concealed survivors is not supported.
>
> **Queue:** option 4 spent. What remains is **3 (the *b* > 2 Hadamard region)**, **5 (239/345, still
> pending S55 results that have never appeared)** and **6 (enter EinsteinArena)**. Option 3 needs no
> literature access at all, which after three access-remedied cells dying on evidence is now the
> relevant property.

> **[30 Sep 2026 — brief E written for option 3, `../hadamard/bgt2/BRIEF_E_BGT2.md`. It is a
> state-establishment brief, not a screen, and the reason is that the queue entry above does not
> survive contact with arithmetic.]**
>
> **Three of option 3's load-bearing terms fail here**, per `../hadamard/bgt2/derive.py`
> (`PRIMARY-VERIFIED-LOCALLY`, all assertions passing):
> * ***b* is undefined in this repository, and my only reading of it is refuted.** Taking *b* = the
>   number of circulant blocks, every permitted row sum is **odd**, so Σ*a_k*² ≡ *b* (mod 8) while
>   4*v* ≡ 4 (mod 8) — forcing **b ≡ 4 (mod 8)**. Of *b* = 2…29 only 4, 12, 20, 28 admit any of the
>   thirteen; *b* = 3, 5, 6, 8 admit **none**. So a source reporting "126+ pairs with *b* > 2" cannot
>   mean this, and the brief ships my guess **together with its disproof** rather than as a premise.
> * **"The 13 orders" names two different sets.** The repo's targets are orders 1948, 2092, 2284, 2572,
>   2636, 2956; the classical thirteen smallest open orders are 668…1964. **Only 1948 is in both.**
> * **669 and 721 are ≡ 1 (mod 4), so neither is a Hadamard order** — they are *v* or *m* values giving
>   2676 and 2884, and both are composite while every *v* on the worklist is prime.
>
> **What did verify:** all six rows of `../hadamard/PLAN_2092.md` §1's table reproduce exactly, *d*
> lists included, and two relations it never states hold on all six — `free_bits = 8D = 4(r−1)` and
> `density = free_bits − log2 E[#sol]`. **So the whole difficulty ranking is a function of one
> arithmetic quantity, the largest odd divisor of *v*−1 the row-sum law admits.** One lead: *v* = 721
> admits *d* = 15 and **192 free bits**, 24 fewer than the order Alpöge *solved* — distrusted, because
> density needs an estimator this repo does not hold.
>
> **The brief's bar** requires all of: *b* defined from source; nothing since
> `../hadamard/PLAN_2092.md` having
> screened the region, **and** `FINDING_155`'s ranking having been scoped to a single *b*; and one
> *b* > 2 pair cheaper than the live target's 232 free bits / 2⁻¹⁴¹. **P-38 predicts FAIL.**
>
> **It is the first brief to use D54's two-grade FAIL** — FAIL-ESTABLISHED against FAIL-UNEARNED, both
> blocking so nothing is bought by hedging — and the first to budget **context as well as calls**
> (D55), asking which limit the run stopped on.
>
> **Audience note:** this brief needs read access to `Cooperative-AI-Defense`, not web search. Option 3
> was described here as needing "no new literature", and that is right — it needs a *repository* this
> instance cannot see.

> **[30 Sep 2026, same day — the operator supplied the definition of *b*, and it reverses this entry.
> Brief E revised before dispatch; `../hadamard/bgt2/BRIEF_E_BGT2.md` §1.]**
> ***b* is a BORDER WIDTH, and it must be odd.** So my block-count reading was about the wrong object
> entirely — the *b* ≡ 4 (mod 8) derivation above is true of block counts and irrelevant here — and
> **"*b* > 2" means "*b* ≥ 3"**, with no *b* = 2, 4 or 6 case existing.
>
> **This entry called the region "un-swept". It is not.** Of **Alpöge's 12 examples, 7 are bordered**:
> 5 unbordered, **4 at *b* = 1, and one each at *b* = 3, 5 and 7** (decomposition forced and asserted in
> `../hadamard/bgt2/derive.py` §7). **The method the whole worklist is modelled on has already produced
> objects in the region.**
>
> **That is the best news on this board in two weeks, and not for the obvious reason.** It supplies what
> the Costas cell fatally lacked: **positive controls inside the region** — three solved instances, found
> by the method in question, at the disputed parameter values. Costas died because its apparent control
> at order 31 proved *constructible* and so was never reached by search. **These three were reached.**
>
> **The brief now turns on one number**, and its hypothesis is the reverse of my first: a border removes
> rows and columns, so a wider border means a **smaller core and fewer free parameters — larger *b* may
> be CHEAPER.** Falsifier: the free-bit or density figures of Alpöge's *b* = 3, 5, 7 examples against his
> *b* = 1 examples. Clause (c) of the bar is exactly that comparison.
>
> Also derived: **`free_bits = 4(v−1)/d` exactly on all six worklist rows** — four bits per orbit — which
> is the cleanest form of the relation and is not stated in `../hadamard/PLAN_2092.md`. And 126+ pairs is
> consistent with *b* running to about 21 across thirteen orders, offered as a shape to check rather than
> a derivation.
>
> **P-38 revised before dispatch and its expected failure clause now REVERSED**, from (a)/(b)
> bookkeeping to **(c)**: the region is demonstrably occupied, so the live question is whether it is
> cheaper, and I expect not — a worklist ranked by a validated density estimator would already point at
> *b* = 7 if it were.

> **[30 Sep 2026 — the operator gives two readings of "the 13 orders", and they decide whether option 3
> exists at all. Brief E revised again before dispatch; `../hadamard/bgt2/BRIEF_E_BGT2.md` §2a.]**
>
> | reading | the thirteen are | what "126+ admissible pairs with *b* > 2" counts |
> |---|---|---|
> | **A** (likely) | the thirteen **open** orders in **(2000, 3000)** | parameter choices at thirteen **still-open** orders — **the opportunity** |
> | **B** | **Alpöge's twelve** new examples, which closed every open order **under 2000**, plus one known *H* from elsewhere | parameter choices at thirteen **solved** orders — **no opportunity at all** |
>
> **Both are exactly consistent.** A fits the worklist: five of the six targets (2092, 2284, 2572, 2636,
> 2956) lie in (2000, 3000) and the sixth is **1948, the sub-2000 order Alpöge solved**. B fits too:
> 12 + 1 = 13, the size of the classical sub-2000 open list. **So the same sentence is either the whole
> of option 3 or none of it, and nothing here decides which.**
>
> **I could not derive either thirteen and say so rather than papering over it.** Coverage by Paley I/II,
> Sylvester and Kronecker closure leaves **136** uncovered multiples of 4 below 2000 and **92** in
> (2000, 3000) — far too many to pick thirteen out of, because the constructions I cannot model
> (Williamson, Turyn, Goethals–Seidel, Baumert–Hall, sporadics) are exactly the ones that close most
> orders. The necessary condition does pass: **all thirteen classical sub-2000 orders are uncovered** by
> the constructions I can model.
>
> **So the brief now carries a third verdict, `E: VOID`** — the subject of the bar does not exist —
> available **only on positive sourced evidence for B**. Precedent: **D46**, opened when a candidate's
> "table it would move" turned out possibly not to exist. VOID is categorically distinct from FAIL (the
> region exists and is not worth entering) and is **not** a middle band; an unevaluable clause is still
> FAIL, graded per D54. **Q1 is now the disambiguation, ahead of the cost comparison**, because under B
> clause (c) is moot. It is the cheapest kill on this board.
>
> **P-38 unchanged as a threshold** — the bar FAILS — but recorded: **VOID would settle it neither way**,
> since a bar whose subject does not exist was never evaluable. On VOID, P-38 stays OPEN and is
> re-registered against whatever region survives.

> **[30 Sep 2026 — the operator's hoa64 pointer settles "which thirteen", and then shows that most of my
> brief was already in this repository. `../hadamard/bgt2/PRECHECK_E.md`.]**
>
> **BOTH thirteens exist.** FINDING_05's are the **thirteen open orders under 3000** — *N* = 2060, 2092,
> 2148, 2284, 2292, 2396, 2572, 2588, 2636, 2676, 2876, 2884, 2956 — quoted verbatim in
> `../playability/HADAMARD_CROSS.md` §1; and hoa64's are **Alpöge's 12 plus Đoković's H(1852), all solved,
> all below 2000**, verified in this repository on **2026-09-20** by H Hᵀ = nI in exact integer arithmetic,
> 13/13 (`../playability/hoa64/verify_matrices.py`). Since `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` sits in FINDING_05's
> directory, **this entry is NOT void** — the *b* ≥ 3 pairs are at open orders.
>
> **But three of brief E v1's findings were already on file, and one is retracted.**
> `../playability/HADAMARD_CROSS.md` §1 already had 669 and 721 as *v* values for 2676 and 2884; §§2–3
> already worked *v* = 721's route, which needs **W(103)**, with both assembly paths validated; §2 already
> recorded the five composite *v* as *"set aside on an assumption that was never checked"*. **And §8
> retracts it:** W(179) and W(223) **cannot** be known, because 716 = 4·179 and 892 = 4·223 were open
> until 2026 and are two of Alpöge's twelve. **So the one lead v1 offered — *v* = 721 at 192 free bits —
> points into a cell whose route this project had already withdrawn.**
>
> **Hold that argument's shape: Alpöge's twelve solved matrices are evidence about which Williamson orders
> CANNOT exist.** It is the best move on this board and it was already made here.
>
> **So brief E v2 asks one question instead of five:** does a bordered construction at *b* ≥ 3 need a
> Williamson or GS quadruple as an ingredient? **If it does, the border axis inherits §8's retraction and
> is not a new region.** That is clause (b) of the rewritten bar and it is where **P-38** now expects the
> FAIL — the free-bit count points at *v* = 721, one of the two orders §8 leaves doubtful, which is weak
> evidence the two axes are one axis. Q4 **measures** the border widths of Alpöge's twelve with
> `../hadamard/bgt2/border.py`, control-tested here (Paley I detects exactly *b* = 1; Sylvester nothing;
> a one-entry break stops detection; a minimum-core guard exists because the first version reported
> spurious large *b* on 1×1 cores).
>
> **D56, and the second instance is mine.** Nothing here checks whether a question has already been
> answered in this repository. This entry was written **2026-09-21**, one day after the document that
> answered it; I then wrote brief E v1 from this entry without searching the tree, **one turn after
> registering D52** about the neighbouring problem. Writing the discipline down did not transfer it. What
> held: every arithmetic claim I derived reproduces the repo's own independently — worth something, not a
> finding.

> **[30 Sep 2026 — two operator corrections, and the second reverses a retraction.
> `../hadamard/bgt2/derive.py` §§11–12.]**
>
> **"2004 is the first open order above 2000" is FALSE and circulates on the web.** 2003 is prime and
> ≡ 3 (mod 4), so **Paley I gives H(2004)** immediately. `PRIMARY-VERIFIED-LOCALLY`. **The smallest open
> order above 2000 is 2060**, as FINDING_05 has it.
>
> **1004 is a third gap in hoa64's library that its README does not list.** hoa64's own closed-form
> families, replicated in `../playability/hoa64/coverage.py`, return **NOT REACHABLE** for 1004 and no
> matrix is shipped — **exactly how 1212 and 1940 behave**, which the README *does* name as its remaining
> sub-2000 gaps. So my recall of 1004 as a classical open order is **not refuted**, it is mildly
> supported. Still unresolved whether it is open, closed by a construction hoa64 omits, or a README
> oversight; one lookup.
>
> **And the retraction overshot.** `../playability/HADAMARD_CROSS.md` §8 correctly infers that W(179) and
> W(223) were **not known** — H(716) and H(892) were open until 2026 and W(*m*) hands you H(4*m*). Its
> conclusion that the routes are *"dead on arrival"* does **not** follow: **not known is not cannot
> exist.** With **W(65) still open** (`OPERATOR-SUPPLIED`), the *decided* Williamson frontier sits below
> 65 and W(103), W(179), W(223) are **undecided**, at **38, 114 and 158 orders beyond** it. **The route is
> a Williamson search at a large distance — a cost, not an impossibility.**
>
> **So brief E v2's clause (b) is reworded** to test that cost rather than inherit a retraction: a
> bordered construction at *b* ≥ 3 passes iff it needs **no** Williamson/GS quadruple, **or** one at an
> order **within the decided frontier**. And Q2 now also asks for the frontier itself as a citable number.
>
> **Two near-misses in one document, in opposite directions** — §§2–3 too optimistic, §8 too pessimistic.
> Recorded as the reason to read a retraction as critically as the claim it retracts (D56, lesson 31).

> **[30 Sep 2026 — the Hadamard worker answered Q2 and clause (b) PASSES. Brief E is now v3, two
> questions, `../hadamard/bgt2/BRIEF_E_BGT2.md`.]**
>
> **The border axis is NOT the Williamson axis.** *"No Williamson or GS quadruple is needed as an
> ingredient, at any order."* The bordered construction at *b* ≥ 3 **is itself** a four-block
> Goethals–Seidel array on an abelian group of order ***v* − *b***, target **PAF sum −4*b* on a subgroup
> of index *b*+1 minus the identity, +4 off it**; the quadruple is what you *search for*. **None of the
> blocks in any of its 14 cores is symmetric, even up to translation** — measured. Williamson is the
> narrow special case. **P-38's expected failure clause is falsified for the second time**, and (b) is
> the one that passed cleanly.
>
> **That answer made the admissibility condition derivable**, and it is
> `PRIMARY-VERIFIED-LOCALLY` (`../hadamard/bgt2/derive.py` §14): a subgroup of index *b*+1 in a group of
> order *v* − *b* needs (*b*+1) | (*v* − *b*), i.e. **(*b*+1) | (*v*+1), *b* odd** — **asserted on all
> four known pairs**, (347,5), (359,7), (479,3), (523,1).
>
> **And it gives 96 pairs, not "126+" — a 24% shortfall** (109 even counting *b* = 1, admissible at every
> odd *v*). **That is now clause (a)'s sharpest form: a condition confirmed on the source's own four
> examples returns the wrong total, so one of the two is wrong and it may be mine.**
>
> **Three derived facts that stand on their own.** Order **2148 has ZERO bordered routes**; **2884 has
> exactly one** (*b* = 37); the **live target 2092 has only {3, 261}**, nearly at the *b* = 1 boundary,
> consistent with the live search being *b* = 1. **The richest are 2876 (22), 2396 (16), 2636 (14), 2588
> (13) — unrelated to the *b* = 1 free-bit ranking that puts 523 first.** So if the border axis is worth
> anything it points at different orders than the worklist.
>
> **What cannot be computed here, and a fourth D53 instance caught a new way.** A *b* ≥ 3 orbit table I
> built returned **2 orbits at *v* = 523 where the verified sweep gives 58** — because the admissible *d*
> must satisfy the **row-sum law, and the law verified here is the *b* = 1 one.** At *b* ≥ 3 the target is
> the relaxed PAF condition, so there is no test for *d* and **no free-bit figure at *b* ≥ 3 is derivable
> here.** That is clause (c) and it stays with whoever can read the source. **It was caught by colliding
> with an earlier verified result, not by a negative test or a reviewer** — the first time — which argues
> for keeping verified reference values in the tree so later work can collide with them.
>
> Also corrected: **there is no "decided Williamson frontier"** — Turyn decides W((*q*+1)/2) for prime
> powers *q* ≡ 1 (mod 4), so the decided set is not an interval; W(*m*) is decided for all *m* ≤ 64 and 65
> is the first undecided. **Third instance in this programme of treating a threshold as a frontier.** And
> **Q4 is withdrawn**: the border sits *within each block*, so `../hadamard/bgt2/border.py` measures the
> wrong object, and hoa64's matrices are normalized anyway.

> **[30 Sep 2026 — brief E ran. `E: FAIL`. OPTION 3 IS DEAD, `../hadamard/bgt2/RESULT_E.md`.]**
> (a) PASSES, (b) PASSES, **(c) FAIL-UNEARNED**. 18 of 20 calls, stopped on neither limit. **P-38 scored
> CORRECT.**
>
> **The derivation beat the source's own summary line, and that is a first here.** The condition quoted
> verbatim from `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` — *"c = b+1 must divide v+1"* —
> **is exactly the one derived locally** from the worker's structure. And the 96/126 gap resolves in my
> favour: **134** pairs over all thirteen with even *b* allowed, **126** over the eleven orders the
> source's code hard-codes, **+8** listed by hand for 669/721 = 134, and **96** with odd *b* only. *"126+"*
> was the eleven-order count **including even *b***, never a count of the admissible set — and
> `FINDING_69` **proves even *b* impossible** (*SS*ᵀ = 4*cI* − 4*J* forces every row sum to zero at
> *c* = *b*+1, so *c* is even and *b* odd). **Every prior agreement between my arithmetic and this
> programme's was independent reproduction; this one is a correction.**
>
> **What kills the cell is none of the three clauses.** *Admissible does not mean the border exists*:
> *border_S.py* built *S* only for *c* ≤ 12, the real worklist was **18 pairs of the 96 — 19%**, reproduced
> exactly here. **And the region was entered**: 17 odd-*b* pairs, **135 configurations — 104 EMPTY_SCOUT,
> 19 EMPTY, 8 EMPTY_UNSETTLED, 4 NOSOL — and no solution in any of 33 `open_*_b*.out` files.** FINDING 63
> **withdrew** FINDING 62's optimistic walls, cutting the gain to **1–2.3 decimal orders, not 3–8**.
> **Option 3 dies on evidence, at the strongest grade this board has produced.**
>
> **D57, and both halves are mine.** (i) Clause (c) asked whether `FINDING_155`'s ranking was single-*b*.
> **It is — b=0 only — and the region was screened anyway, by different instruments.** I tested whether
> *one* instrument had covered the cell when the decision needed whether *any* had. **D51's shape one
> level out.** (ii) The brief cited *../PLAN_2092.md*, *PRECHECK_E.md* and *derive.py* to a reader in
> another repository, where none resolve — and `../tools/check_paths.py` passed them because it checks the
> **author's** tree. **Resolvability is reader-relative and nothing here checked that.**
>
> **Also:** the thirteen are the open thirteen from **Cati & Pasechnik Table 4**, so VOID never applied;
> *"126+"* has **no provenance** in the file or its scripts; *OPEN_ORDERS.md* is **stale on 669 and 721**,
> which FINDING 72 settles — **and that stale sentence is what this entry was built on**; and there are
> **160 findings, highest 163**, the same as `../hadamard/PLAN_2092.md` saw, so the currency worry was
> unfounded.
>
> **And one error of mine.** The live target is ***b* = 0, not *b* = 1**. So (*b*+1)|(*v*+1) at *b* = 0 is
> `1 | 524`, vacuous — the condition is confirmed on **three** non-trivial pairs, not the four I asserted.
>
> **Queue:** option 3 spent. **What remains is 5 (239/345, pending S55 results that have never appeared)
> and 6 (enter EinsteinArena).** Options 1, 2, 3 and 4 are all closed on evidence.

> **[30 Sep 2026 — option 5 had no self-contained brief and no result. Brief F written,
> `opt5/BRIEF_F_OPT5.md`.]** The operator could not find either, and was right: option 5's bars live in
> `../HANDOFF_S55.md` §§3–4, which is a **Claude Code** handoff, never a chat brief — and
> "RESULT_S55_B_239.md" and "RESULT_S55_C_345.md" **do not exist on this branch.** So the "pending S55"
> status was never pending anything; no instrument was ever built for it.
>
> **Brief F scores all three registered bars verbatim and re-scopes none** — B-1 and B-2 on the odd
> perfect number bound, C-1 on ES(7). **Prior local work consulted first this time (D56):**
> `RESULT_MAPPING_B.md` §3 calls 239 *"the only chunk-B candidate worth gating"* and names the two risks
> the bars test; `RESULT_MAPPING_A.md` §4 records that C-1 is expected to fail because heavy-tailed SAT
> runtime is textbook and its fixes are already in every solver. **Both priors are carried into the brief
> with an invitation to overturn them.**
>
> **Two locally verified controls, both executed before shipping** (`opt5/controls.py`): σ(*N*) = 2*N*
> finds exactly 6, 28, 496, 8128 below 10⁵ and rejects five near-misses, plus Euler's form
> *N* = *q*ᵃ*m*² with *q* ≡ *a* ≡ 1 (mod 4); and for ES, the triangle-plus-interior-point witness fires
> and **all 25,052 general-position 5-subsets of the 5×5 grid contain 4 in convex position**, consistent
> with ES(4) = 5. **Both embedded snippets were extracted from the brief and run** — after three
> hand-written controls in this session shipped wrong.
>
> **D57 applied in both halves.** (i) C-1 asks whether the *paper* leaves a subfamily unswept; the brief
> adds, as a **separate** finding, whether *anything since* has swept it. (ii) The brief cites **no
> repository paths at all**, because its reader has no repository — resolvability is reader-relative.
>
> **P-39 registered: all three FAIL**, with the expected grades stated explicitly (B-1 ESTABLISHED, B-2
> UNEARNED, C-1 ESTABLISHED) so P-38's 1-of-3 clause calibration can be measured again rather than
> asserted. **And a separate non-threshold bet: better than even odds arXiv:2512.24061 does not check out
> as described** — the citation reaching me is `RECALL`, and this project has twice described a paper from
> its title and been wrong.

> **[30 Sep 2026 — brief F ran. All three bars FAIL. OPTION 5 IS SPENT, `opt5/RESULT_F.md`. Only option 6
> remains.]** B-1 FAIL-ESTABLISHED, B-2 FAIL-UNEARNED, C-1 FAIL-ESTABLISHED. 14 of 22 calls. **P-39
> scored: threshold CORRECT, grades 3 of 3, side bet WRONG** — arXiv:2512.24061 is real and says what was
> claimed.
>
> **But the operator's two notes outrank the run, and one of them reframes this whole document.**
>
> **An Opus 5.5 instance already worked 239 extensively and FOUND AN ERROR IN OCHEM–ZELINSKY'S ALGORITHM 1
> PROGRAM, accepted by Ochem by email.** That is an externally validated correction to a published paper —
> **the most concrete result this programme has produced — and it is nowhere in the ledger.** 41
> predictions, 58 debts, every one about the screen. **D58: the screen is what got instrumented, so the
> screen is what the record measures. The 0-of-7 tally scores the screen, and the thing that worked was not
> the screen.** That is a different conclusion from "record problems do not move", and the current
> bookkeeping cannot tell them apart.
>
> **And D56's registered fix was applied and proved insufficient.** I grepped the local tree before writing
> brief F — first application of the fix — and the tree was silent, because **both** prior efforts happened
> in sibling instances and left no trace here (239 by the Opus instance; arXiv:2512.24061 already checked
> and ruled out). **Grepping the tree is necessary, not sufficient: the action must include asking the
> operator what has been tried.** Escalated there.
>
> **What the 14 calls did buy, four items none of which were on file:** Ochem's page now says **10²²⁰⁰**,
> not the 10²⁰⁰⁰ my brief relayed from 2014 slides, with **Ω ≥ 115** against the published 101 — so the
> published-versus-private gap is **~700 orders of magnitude**. The only measured cost is Figure 2: **≈12 h
> for Theorem 1's tree on an AMD Phenom II X4 945, 105.5 h documented in total, 10.6× over a
> 10-container-hour bar** — **and the paper explicitly excludes the factoring**, volunteer-distributed and
> never aggregated, so the dominant cost is unreported and the margin is **not computable**, which is why
> the grade is UNEARNED and not ESTABLISHED. **The C-1 kill is structural and makes the bar nearly beside
> the point: no subfamily's closure could move ES(7) at all**, since the lower bound is already 33 and only
> UNSAT over *all* 33-point sets moves the upper bound. And *"UNSAT certificates"* overstated solver
> **verdicts** — no DRAT/LRAT, no independent checking, repository holds a README and a CNF generator.
>
> Also: **Suk's asymptotic is superseded** by Holmsen–Mojarrad–Pach–Tardos 2020, which my brief did not
> know.
>
> **Queue: options 1–5 are all closed on evidence. Only 6 — enter EinsteinArena — remains, and it is the
> one that changes the method rather than running it again.**

> **[30 Sep 2026 — a SECOND external result, and it makes the screen's problem measurable instead of
> merely arguable. `../../proof-protocol/debts.json` D58, P-40.]**
>
> About a month before the Ochem–Zelinsky finding, the same method — **a capable instance working the
> code** — came **close to the first counterexample of a twenty-year-old conjecture**, and was **scooped by
> a different researcher a few weeks prior.** So the tally is **two results from that method against zero
> promotable candidates from seven screens.**
>
> **Three things follow, and the third is a cheap experiment.**
> * **The near-miss was at exactly the difficulty the screen exists to find** — a first counterexample to a
>   long-standing conjecture. It is not a consolation; it is capability demonstrated at the target class.
> * **Being scooped is a direct crowding measurement of a kind no gate here ever produced.** Not *"has
>   anyone moved this"* inferred from publication history, but *"someone moved this while we were moving
>   it"* — learned only by attempting it. S4 and the C-1 and C-3 bars all inferred contest from outside,
>   and **D47 records that crowding decided none of the three.** This says why: **you cannot measure
>   crowding from outside.** That is the opposite of what the screen assumed, and it is D51's observable
>   problem with its answer attached — the state that matters is not in the literature.
> * **P-40, registered before the target is named so the threshold cannot be fitted:** run SELECT v1's
>   S0–S5 over that near-miss target. **Predicted: it FAILS**, i.e. the screen would not have surfaced the
>   target the programme nearly hit. Expected at **S3**, structurally rather than positionally — a
>   twenty-year-old conjecture with no recent movement is exactly the case where the most recent move has
>   no knowable kind, and `../gap/SELECT_v1.md` §9 already records that S3 *"does not survive as a
>   discriminator"* and *"killed records on UNKNOWN rather than on gap type"*. **A failure at S4 would be
>   more interesting still**, since the target *was* contested and S4 could only have seen it afterwards.
>
> **Why this is worth more than the tally.** 0-of-7 is a null across seven instruments and weak evidence
> about the screen. **A demonstrated false negative on a target the programme nearly hit is direct
> falsification**, and it costs one target against six already-registered gates. This session's branch is
> named `claude/retrodiction-benchmark-p1` — **this is the test the branch was named for.**
>
> **Blocked on one input: which conjecture.**

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

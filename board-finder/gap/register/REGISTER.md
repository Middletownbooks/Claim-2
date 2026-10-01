# The prior-work register

**Cycle 0's Task 1, built for the first time.** The target-selection prompt that produced the Rota
target opens with a register of the problems this collaboration had already attempted, recording for
each *the binding constraint hit, stated as a formal proposition*, and *whether that constraint was
compute-shaped or theory-shaped* — the field it calls "the whole point", because Claude Code
"multiplies compute-shaped constraints and does almost nothing for theory-shaped ones."

**It did not run.** There were no transcripts to recover; nothing was in a repository at that point.
Its preamble calls the missing input *"cheap to obtain and never obtained"*, and the first half was
false — it was not obtainable at all. The check has therefore been known-necessary and unperformed
across two lineages (`D56`, `LEDGER` lesson 41).

**What changed is the repository.** The input Cycle 0 needed was never the transcripts; it was a
written record of what the attempts established. That now exists, so the schema is fillable — from
documents rather than from transcripts, which is a substitution with consequences, stated in §0.3.

---

## 0. What this is

### 0.1 The schema, from Cycle 0 verbatim

| Field | Cycle 0's note |
|---|---|
| Date, mode | chat-with-tools / Claude Code / tool-less |
| Depth reached | literature only · encoding built · computation run · result claimed |
| **The binding constraint hit** | *"stated as a formal proposition, not prose. 'We ran out of session' and 'the realizability constraints could not be encoded' are entirely different findings"* |
| Any costed estimate | *"search-space size, runtime extrapolation — with the arithmetic re-derived here"* |
| Claims made | *"each entering the DAG with `assumed` edges; none inherited as established"* |
| **compute-shaped or theory-shaped** | *"this is the field that decides everything downstream"* |

### 0.2 Inclusion rule, stated before the rows

A row exists for each target that was **selected and then worked** — where the object itself received
effort, not merely a decision about whether to spend effort. That gives **Part A**, nine rows (eight in
the first version; A9 was missed, see its own box).

Targets that were selected as best-of-corpus and then **killed at a pre-registered gate before any
work on the object** are **Part B**: they answer "has this been attempted?" with "no, and here is
why", which is what a future selector needs from them. Records that were only *screened* are a
population, not rows, and are counted in **Part C**. Cycle 0's own seven rows are **Part D**, and they
are still empty.

No row for `../../../theorem-lab/` or `../../../leanboard/`: those are instrument and capability
studies, not attempts on an external open problem. That is the inclusion rule applying, not a
judgement about their value.

### 0.3 The source substitution, and what it costs

Cycle 0 wanted transcripts. This is built from committed documents, and **a document is a run's
self-report.** Three consequences, none of them repairable by a register:

1. **Depth is as stated.** I did not re-run any search to confirm it.
2. **Every figure the rows cite is re-derived** in `register_arithmetic.py` — 39 assertions, all
   passing — from the stated inputs rather than copied from the document that claims it. That
   discharges Cycle 0's "with the arithmetic re-derived here" clause and nothing more.
3. **Three rows rest on work that left no trace here at all** (A4's sibling-repository sweep, A6's
   handoff to the Hadamard worker, A8), at `SECONDARY-RELAYED` and `OPERATOR-SUPPLIED`. This is `D56`'s escalation: work done in a sibling
   instance is invisible to any check that reads this repository. The register marks those cells; it
   cannot fill them.

**One disagreement was found and settled rather than inherited.** `../../hadamard/bgt2/RESULT_E.md`
§2 reproduced the source's "18 pairs" but counted 7 orders against the source's 8, flagged the
discrepancy, and left it open. Re-derived here: **no (b-range, parity) reading that preserves 18
pairs yields 8 orders**, and under the only reading that gives 18 — odd *b* ∈ {5,7,9,11}, i.e.
4 < *c* ≤ 12 — the order count is forced to **7**, over *v* ∈ {515, 599, 647, 659, 669, 719, 739}.
The source's pair count reproduces and its order count does not. That is the **second** failure of the
same summary line, after "126+".

---

## 1. Part A — targets worked

### A1. Prouhet–Tarry–Escott, ideal solution of size 11

| field | value |
|---|---|
| date, mode | 21–29 Sep 2026 · Claude Code, with operator-relayed literature |
| depth | **computation run, result claimed** — exhaustive to *H* = 36 (registered) and *H* = 80 (pattern ladder), null |
| **binding constraint** | Our enumeration costs C(*H*,6) right-hand tuples at a measured 172k/s, so **time(*H*) = C(*H*,6)/1.72×10⁵ s**. The published frontier is *H* = 3500, at which time = **4.7×10⁵ years**. Formally: *the target is unreachable by our algorithm, and the frontier was set by an algorithm we do not have* — Coppersmith–Mossinghoff–Scheinerman–VanderKam §4.1 chains the divisibility conditions to force each element into a residue class, an enumeration 52,684× smaller than ours at *H* = 90. |
| costed estimate, re-derived | C(3500,6) = 2,542,222,346,415,251,500 tuples → 468,000 years. Frontier/reached compute multiplier **2³³ ≈ 8×10⁹**, which is (3500/80)⁶. Corollary 21 bought 17× in *tuples* = **17^(1/6) = 1.60×** in height, against a height gap of 43.8×. |
| claims made | published bound *H* = 3500 `SECONDARY-RELAYED`; the 52,684× ratio `SECONDARY-RELAYED`; our own rates and nulls `PRIMARY-VERIFIED-LOCALLY` |
| **shape** | **THEORY-SHAPED.** 8×10⁹× more compute under our method, or a different method. A longer run does not reach it. |

Where: `../../pte/VERDICT_PTE11.md`, `../../pte/PREREG_PTE11.md`, `../../pte/CMSV2024.md`.
Also on file: `A-4` was a two-sided prediction with an unregistered middle, and the answer landed in
the middle (`D44`). That is a scoring defect, not a constraint, and is not this field.

### A2. PTE over the unsearched imaginary quadratic rings, *d* = 43, 67, 163

| field | value |
|---|---|
| date, mode | 21 Sep 2026 · Claude Code |
| depth | **premise computation run**, gate G2 FAIL before any search of the rings |
| **binding constraint** | Pre-registered: *PASS iff at least one solution was ever found in a ring with \|Δ\| ≥ 11.* **Every non-empty cell of the source's Table 5 sits at \|Δ\| ∈ {3,4,8}; the two rings with \|Δ\| ≥ 11 returned nothing across ten cells, and the registered confound is refuted — the sparse rings were covered better, median 2,051 lattice points against 1,795.** So: *the unsearched region is unsearched because it is a bad place to look.* |
| costed estimate, re-derived | Lattice density 2π*H*/√\|Δ\| makes the three unsearched rings **2.3× / 2.9× / 4.5× thinner** than *d* = 2, the thinnest ring that ever produced a solution. For *d* = 163 the norm form is *a*² + *ab* + 41*b*², so the only norms ≤ 20 it represents are **{1, 4, 9, 16}** — the rational integers. |
| claims made | Table 5's contents `SECONDARY-RELAYED`; class numbers, densities and norms `PRIMARY-VERIFIED-LOCALLY` |
| **shape** | **THEORY-SHAPED, premise-falsifying.** No amount of compute changes where solutions live. |

**And the attempt corrected its source.** Counting reduced positive-definite binary quadratic forms
over all squarefree *d* < 2000 gives *h* = 1 for exactly the nine Heegner numbers
{1, 2, 3, 7, 11, 19, 43, 67, 163}; the paper's list has eight and **omits *d* = 67**. The gap is three
rings, not two. Where: `../../pte/rings/RESULT_RINGS.md`.

### A3. Costas arrays, order 32

| field | value |
|---|---|
| date, mode | 30 Sep 2026 · Claude Code + a Sonnet 5.5 chat run (brief D) |
| depth | **encoding built** — construction closure under both corner operators, 10,956 arrays over 8 rounds; the order-32 search itself never started |
| **binding constraint** | Two propositions, and the second is the one that stopped it. **(i) No published structural characterisation of sporadic Costas arrays exists** (Drakakis 2011's own open-problems paper), so no lever constrains a search at order 32. **(ii) The intended positive control does not exist: the order-31 arrays are W₀ arrays — Welch *p* = 31 of order 30 with one corner dot added — hence constructible, not search-found.** Adding one corner dot to Welch *p* = 31 gives exactly 4 distinct arrays closing to 8 under the dihedral group, matching the relayed C(31) ≥ 8 to the digit. |
| costed estimate, re-derived | log₂(32!) − log₂(31!) = **exactly 5.00 bits**, which is log₂ 32 — *one order always costs 5 bits of permutation space*. So the "5 bits from the target" framing never depended on order 31 being a search result, and the reasoning that made the cell attractive was independent of the fact that killed it. |
| claims made | C(31) ≥ 8 and the Drakakis survey `SECONDARY-RELAYED`; the W₀ construction and the constructible/unexplained table `PRIMARY-VERIFIED-LOCALLY` |
| **shape** | **THEORY-SHAPED.** The missing objects are a structural lever and a control, neither of which is a compute quantity. Compounding it: C(32) = 0 is possible, and no constructive search can distinguish that from a bad search — which is precisely what the control was for. |

Where: `../../gap/discovery/RESULT_D_COSTAS.md`, `../../costas/costas_support.py` PART 7,
`../../costas/PLAN_COSTAS.md`. The generalisation from *unreachable by the operator I implemented* to
*unreachable by any construction* is `D53`.

### A4. Hadamard matrices, the *b* > 2 border region over the thirteen open orders

| field | value |
|---|---|
| date, mode | 30 Sep 2026 here · Claude Code, plus a Claude Code instance with read access to the sibling repository (brief E); the object itself is worked by a different instance in a different repository |
| depth | **state established here; computation already run there** — 135 configurations over 17 odd-*b* pairs, no solution |
| **binding constraint** | **Admissibility is (*b*+1) \| (*v*+1) with *b* odd, giving 96 pairs over the thirteen; but admissible does not mean the border exists.** The border *S* was constructed only for *c* ≤ 12, an 18-pair worklist, and the sweep returned 104 EMPTY_SCOUT, 19 EMPTY, 8 EMPTY_UNSETTLED, 4 NOSOL. Formally: *the region is not un-swept; it is swept wherever the border object is constructible, and the obstruction is the non-existence of S beyond c ≤ 12, not a shortage of compute.* The programme's own optimistic cost figures were **retracted by their author** (FINDING 63: *b* > 1 lowers the wall "by roughly 1 to 2.3 decimal orders, not by 3 to 8"). |
| costed estimate, re-derived | 96 admissible pairs (*b* odd) · 134 with even *b* allowed · 126 for the eleven orders the source's code hard-codes · 8 added by hand for *v* = 669, 721 — so **"126+" was never a count of the admissible set.** 18 of 96 pairs were built = 19%, a factor of 5.3. Even *b* is impossible: *SS*ᵀ = 4*cI* − 4*J* gives squared row-sum norm 4*c*(*b*−*c*+1), which at *c* = *b*+1 is **0**, so every column is a zero-sum ±1 vector of length *c*, forcing *c* even. Asserted at *b* = 3, 5, 7, 9, 37. |
| claims made | the sweep's contents and FINDINGs 62–69 `SECONDARY-RELAYED`; the admissibility rule, all four counts and the *b*-odd derivation `PRIMARY-VERIFIED-LOCALLY` |
| **shape** | **THEORY-SHAPED** for the region — border existence. **With one compute-shaped sub-route:** Williamson W(103), W(179), W(223) sit 38, 114 and 158 orders beyond the decided frontier at 65, which is a cost statement, not an impossibility (`D56`, correcting an earlier "dead on arrival"). |

**This attempt also corrected its source twice** — the admissible count, and (§0.3) the order count of
the worklist. Where: `../../hadamard/bgt2/RESULT_E.md`, `../../hadamard/bgt2/derive.py`.

### A5. Hadamard H(2060) via the Cooper–Wallis route

| field | value |
|---|---|
| date, mode | ~20 Sep 2026 · Claude Code · **one day spent** |
| depth | **route built, then abandoned on a one-line check** |
| **binding constraint** | A Williamson quadruple of order *m* yields H(4*m*) immediately. **716 = 4·179 and 892 = 4·223 were open until 2026** — they are two of Alpöge's twelve — so *if W(179) or W(223) were known, those orders would not have been open.* Hence the ingredients the route needs are **not known**. And the substitution fails for a structural reason: enumerating ±1 quadruples with Σ*AA*ᵀ = 4*mI* gives far more GS-type than all-symmetric ones (64 against 1,664 at *m* = 3), so *a known H(4m) is weak evidence against W(m) rather than neutral* — H(412) known is fully consistent with W(103) not existing. |
| costed estimate | none; the kill was arithmetic, not costed |
| claims made | Alpöge's twelve `SECONDARY-RELAYED`; the quadruple enumeration `PRIMARY-VERIFIED-LOCALLY` |
| **shape** | **THEORY-SHAPED** — the route needs a strictly stronger object than the one the data supplies. |

**This row carries a correction to itself.** The document concluded the routes were "dead on
arrival", reading *not known* as *cannot exist*. That is invalid — W(65) is still open, so the decided
Williamson frontier sits below 65 and higher orders are undecided rather than refuted. The valid
constraint is the one stated above. Where: `../../playability/HADAMARD_CROSS.md` §8, and `D56`'s
30 Sep note. The general form is `../REVIEW_JULY_GAP_ANALYSIS.md` §2.4: *every candidate should carry the
one-line check that would kill it, and it should be run during triage* — this is the row where that
lesson was paid for.

### A6. D-optimal designs of order 2*v* (pool id U13)

| field | value |
|---|---|
> **[CORRECTED 30 Sep 2026, and this row was wrong in the way the register exists to prevent.]** I
> first wrote this row as **UNDETERMINED**, on the strength of `../../doptimal/README.md`'s summary
> line — *"may empty the orbit ansatz altogether at the orders of interest"* — **without opening
> either `../../doptimal/PROMPT_U13_TRANSFER.md` §3.2 or `../../doptimal/VERIFIED_OUTPUT.txt`, in the
> same directory.** Both were computed. The row below is the corrected version; what the error cost
> is in §5 and in `D56`.

| field | value |
|---|---|
| date, mode | 26 Sep 2026 · Claude Code · **then handed to the Hadamard worker instance**, which is what `../../doptimal/PROMPT_U13_TRANSFER.md` is (`OPERATOR-SUPPLIED`, 30 Sep) |
| depth | **transfer audit built, locally verified, and handed off** — PAF invariants, exhaustive small-order search to *v* = 11, two-square admissibility over the six worklist orders, Monte Carlo density coefficients at four *v*. The D-optimal target itself was never entered **here**; whether the worker has since answered the audit is not visible in this repository. |
| **binding constraint** | **Two-block admissibility, and it is already established at the orders of interest.** The two-circulant D-optimal design needs *a*² + *b*² = 4*v* − 2, solvable only when every prime ≡ 3 (mod 4) divides 2*v*−1 to an even power. **Of the six orders on the Hadamard worklist it holds for exactly one** (*v* = 643); `../../doptimal/VERIFIED_OUTPUT.txt` §3 gives the two-block orbit ansatz as *admissible: none* for *v* = 487, 523, 571, 659, 739. Formally: *at five of the six orders this apparatus is pointed at, there is no admissible two-block ansatz to empty.* Independently, §3.2's model log₂ E[#sol] ≈ (*r*−1)(*k* − *b*/2) with *b* measured by Monte Carlo gives a *k* = 2 coefficient **falling from +0.57 at v = 67 to +0.26 at v = 151**, crossing zero at *b* = 4 bits/equation — *"which the 2-block column reaches somewhere in the low hundreds of v"*, i.e. exactly where the interesting orders are. |
| costed estimate, re-derived | the *M*² endgame shrinkage is derived in §3.3; the two-squares filter and the exhaustive small-order counts (0 designs at *v* = 11, 392 at *v* = 7, 1944 at *v* = 9) are in `../../doptimal/VERIFIED_OUTPUT.txt` §2 |
| claims made | §1 invariants, the two-squares filter, the exhaustions and the admissibility table `PRIMARY-VERIFIED-LOCALLY`; **§3.2's extrapolation past *v* = 151 is `assumed`** and the audit says so in its own words — *"a crude model doing load-bearing work, and I would rather have it corrected than agreed with"* |
| **shape** | **THEORY-SHAPED, provisionally.** *"Engine yes, dimension-reduction no"* — the orbit reduction, the piece that makes the Hadamard instances tractable, is the piece that does not transfer, so D-optimal has to be searched closer to full space, which is how the published searches work. Provisional because the confirmation at the target orders was handed off and its answer is not on file here. |

Where: `../../doptimal/PROMPT_U13_TRANSFER.md` §§3.1–3.5, `../../doptimal/VERIFIED_OUTPUT.txt`,
`../../doptimal/transfer_check.py`, `../../doptimal/README.md`. **Not the register's actionable row —
see §5 for what replaced it.**

### A7. Chow's Conjecture 2 — C(3) at rank 4 · **a result**

| field | value |
|---|---|
| date, mode | August 2026 · **the operator working with a Claude instance**; the note's own wording is *"the work was carried out with AI assistance"*. Selected by the Cycle 0 lineage: gap analysis of open problems plus Opus-in-Claude-Code gating, predating all the playability work. Verified here 30 Sep 2026. |
| depth | **result claimed, and independently verified from the axioms** |
| **binding constraint** | **Not compute and not theory. Priority.** Allikvere's preprint of **27 July 2026** states the same theorem — C(3) false at rank 4 — weeks earlier. Formally: *the tracked quantity was moved by someone else while we were moving it.* |
| costed estimate | none needed; the certificate is finite and exact |
| claims made | every claim in the note re-derived here and **all hold**: rank 4 on 12 elements over 𝔽₃, **exactly 240 bases of 495**, three disjoint covering bases, all four *Iᵢ* independent in their stated witnesses, the parallel class {0,4,8}, *P* ⊔ *Q* partitioning all nine pairs, all six perfect matchings giving \|μ ∩ *P*\| ∈ {1,1,1,1,3,3} — never the 2 a grid needs — and **0 of 1296** assignments giving three bases. `PRIMARY-VERIFIED-LOCALLY`. |
| **shape** | **NEITHER — see §4.2.** The register's deciding field has no value for the constraint that actually bound the programme's one verified new object. |

**It is not Allikvere's matroid.** Re-derived independently here: ours has **240** bases, his graphic
K₅-with-34-tripled has **225**. Same rank, same ground-set size, both driven by a size-3 parallel
class, both closed by a parity count — convergent mechanisms, different objects. His is the stronger
existence statement (graphic ⇒ regular ⇒ representable over every field) and carries lifting to all
rank ≥ 4. Where: `../rota/RESULT_OUR_COUNTEREXAMPLE.md`, `../rota/verify_ours.py`,
`../rota/verify_allikvere.py`.

### A8. Record 239 — odd perfect number lower bound · **a result**

| field | value |
|---|---|
| date, mode | ~Sep 2026 · an Opus 5.5 Claude Code instance, in a sibling instance leaving no trace in this repository · `OPERATOR-SUPPLIED`. Selected as an identified queue item. |
| depth | **result claimed** — an error found in **Ochem–Zelinsky's Algorithm 1 program** in their most recent paper, **accepted by Ochem by email**. The instance judges further progress unlikely. |
| **binding constraint** | On the *record*: **the published 10¹⁵⁰⁰ is not the frontier.** The authors' own page reports the computation pushed to **10²²⁰⁰** with Ω(*N*) ≥ 115 against the published 101, plus composite-factor lists to 10²³⁰⁰ dated Feb 2025. Formally: *the reachable target sits behind a private computation by the record's own authors, ~700 orders of magnitude ahead of the published bound.* And the margin is not computable: the paper's Figure 2 documents the branchings but **explicitly excludes the factoring**, which was volunteer-distributed and never aggregated. |
| costed estimate, re-derived | 2200 − 1500 = **700** orders of magnitude to the private frontier, 800 to the factor lists. Figure 2's documented time is **105.5 h** (12 + 93 + 0.5) on 2008-era hardware — **10.6×** a 10-container-hour bar, with Theorem 1 alone at **1.2×**. |
| claims made | Ochem's page and Figure 2 `SECONDARY-RELAYED`; 10²²⁰⁰ `ANNOUNCED`, undated, with only a 10⁵⁴⁰ proof tree linked; the error and its acceptance `OPERATOR-SUPPLIED` |
| **shape** | **COMPUTE-SHAPED — and already spent, by the record's own authors, privately.** This is the one row where Claude Code's delta applies, and the compute is held by the people who set the record. |

**Note what the row's two halves say.** The bars asked whether to attack the record — B-1
FAIL-ESTABLISHED, B-2 FAIL-UNEARNED — while *working the item* produced a correction to a published
algorithm's program, which is theory-shaped and which no bar on this board has a category for
(`D58` (iv)). Where: `../../fallbacks/opt5/RESULT_F.md`.


### A9. Six MOLS of order 12 — *N*(12) ≥ 6

> **[ADDED 30 Sep 2026. This row was missing from the register's first version.]** It is named in
> `../GAP_V3.md` §1 as one of three targets that cleared the v2 rubric and died, and it has a full
> gate result in `../../fallbacks/RESULT_FALLBACKS.md`. I built Part A from the target directories
> and missed a target that lives in a *gate* document. **Second missing-row failure in one day**, and
> the same cause as A6's: I enumerated the population from where I expected it to be.

| field | value |
|---|---|
| date, mode | ~21 Sep 2026 · a separate Claude Code instance, relayed (it could not push — its environment returned 404) |
| depth | **computation run, and it produced a small theorem** — both published 5-MOLS(12) sets, McKay's from Sage and one built from Hanani's 1975 DM(12,6,1) over ℤ₂×ℤ₆, are **maximal**: every 4-subset has exactly 12 common transversals and exactly one mate, so any transversal common to all five is among the 12 and each is constant in square 5, giving zero. Controls: both 5-sets and the order-10 pair verify independently, the verifier fails on all five deliberate breaks, and hiding one square at a time it was recovered **12 of 12**. |
| **binding constraint** | **The deliverable, not the world.** The table records *lower bounds*, so showing two specific 5-sets are maximal leaves *N*(12) ≥ 5 exactly where it stood. Formally: *the null established was a null about two objects, not about the tracked quantity.* A genuine attempt at *N*(12) ≥ 6 needs a supply of new inequivalent 5-MOLS(12), or a direct TD(8,12) — **an unbounded search the gate never costed, because F2 costed the wrong region.** |
| costed estimate | F2 measured the reachable region at a median 0.008 s over seven seeds — *"the pass is empty"*, in the gate's own words. F3 was NOT SCORED: no dated source for which extensions have been searched. The real region was never costed at all. |
| claims made | *N*(10) ≥ 2 (Bose–Shrikhande–Parker 1960) and *N*(12) ≥ 5 (Johnson–Dulmage–Mendelsohn 1961) `SECONDARY-RELAYED` from two dated sources, neither bound moved in 65 years; the maximality theorem and all controls `PRIMARY-VERIFIED-LOCALLY` by the running instance, relayed here |
| **shape** | **DELIVERABLE-SHAPED — a fourth value, and distinct from A7's.** The attempt was not stopped by compute or by theory; it was stopped by a mismatch between the object searched and the quantity recorded. The *target's* shape is still unknown, because the search that would settle it was never costed. |

**Why this row matters more than its verdict.** `../../fallbacks/RESULT_FALLBACKS.md` §2 states it
plainly: *"No rubric this project has written would have caught that. `../PROMPT_GAP_v2.md` scores
eight dimensions of the problem; none of them asks what a null would be a null about."* That is
`D59`'s decomposition gap arriving from the construction side, nine days before `D59` was written
from the retrodiction side — and `../GAP_V3.md` §4's Δ dimension is the registered fix, never applied
to a scored candidate.

---

## 2. Part B — selected, then killed at a pre-registered gate before any work

| # | target | date | the gate that fired, as a proposition | shape |
|---|---|---|---|---|
| **B1** | Record 235, Zauner/SIC-POVM existence | 20 Sep 2026 | **PREFIX with an empty hole list.** Exact fiducials cover every dimension to 53 (safe) or 57 (probable); the 2017 holes are all filled, 2021–2024. Above ~57 the unknown set is an **open tail**, not a finite list of oversights — so the writable unknown set is not finite. | theory-shaped + crowded (Grassl, Bengtsson–Grassl, Appleby–Flammia–Kopp, Kopp–Lagarias all active) |
| **B2** | Record 1154, kissing numbers *d* = 13/14 | 29 Sep 2026 | **1154 stands at primary tier (Zinoviev–Ericson 1999), but neither EinsteinArena nor Qiushi Engine reports attempting *d* = 13.** *An unattempted cell is only unvisited, and the next run of theirs will visit it.* Qiushi produced 19 dimensions in one paper; EinsteinArena produced 11 SOTA results in two months from a standing start. | compute-shaped, being swept at industrial rate by others |
| **B3** | Caps in AG(8,3) | 29 Sep 2026 | **Three post-2023 AI search systems report direct *n* = 8 runs** — X-evolve reaching 512 (matched), Ellenberg et al. best 448, QUBE below 512. The escape hatch (capacity ≠ finite cell) was wrong on the facts: **X-evolve worked both.** | compute-shaped, spent |
| **B4** | Record 345, Erdős–Szekeres ES(7) | 30 Sep 2026 | **No subfamily's closure can move ES(7).** The lower bound is already 33 by construction; only UNSAT over *all* 33-point sets moves the upper bound, and a partial UNSAT changes nothing. Re-derived: 10,121 compositions of 33 into parts 3–6 as a scale indicator; the cited work's 13 rows sum to 81 days single-thread, with a 912× spread inside 5⁶. | theory-shaped, **and the bar asked the wrong question** — it tested whether a subfamily was unswept when no subfamily could have mattered |
| **B5** | Williamson, smallest open odd order | Arm 2 | **FAIL at S0** — "65 itself is unresolved" is `SEARCH-SUMMARY` only, so the record is **not evaluable at a usable tier.** A bar you cannot evaluate is FAIL. | not assessable |
| **B6** | Steiner, smallest open admissible case S(2,6,51) | Arm 2 | **FAIL at S3** — move kind UNKNOWN. (Derived and re-checked: 85 blocks, 51 ≡ 6 mod 15 admissible.) | not assessable |
| **B7** | Cyclic difference sets, smallest open (1561,105,7) | Arm 2 | **FAIL at S3** — move kind UNKNOWN. | not assessable |
| **B8** | Bent functions, smallest unknown variable count | Arm 2 | **FAIL at S1** — not coupled. | not assessable |

B5–B8 are where the schema's deciding field **cannot be filled at all**, and that is itself the
finding those rows carry: see §4.3.

---

## 3. Part C — the screened population, counted rather than enumerated

| population | size | outcome | where |
|---|---:|---|---|
| the record corpus, across seven screens | **499** | 0 promotable candidates | `../RESULT_DISCOVERY.md`, `../SELECT_v1.md` |
| Arm 2 record tables | **15 of 15** | 0 live survivors; 2 triage survivors (kissing 13/14, AG(8,3) caps), both later killed at gates | `../RESULT_ARM2_TABLES.md`, `../discovery/RESULT_B1_DESIGNS.md`, `../discovery/RESULT_B2_SEQUENCES.md` |
| Arm 1 cells | **19** | 0 of 19, and the replication moved 277 and 353 from CANNOT EVALUATE to FAIL | `../discovery/RESULT_C_ARM1_CELLS.md` |
| mid-band rescan, ranks 120–350 | **230** | 106 carry record or algorithmic-deficit language; the band is not barren, and the corpus records headlines rather than the record tables underneath them | `../../fallbacks/QUEUE_V3.md` |

**Why these are not rows.** A screening verdict is a decision *not* to attempt, and Cycle 0's schema
has no field it fills — no depth, no binding constraint, no shape. Recording 499 of them as rows would
make the register look complete while answering none of its questions.

---

## 4. What the filled field says

### 4.1 The tally, and it is the register's whole point

| shape | rows | which |
|---|---:|---|
| **THEORY-SHAPED** | **6** | A1 PTE 11 · A2 PTE rings · A3 Costas 32 · A4 Hadamard *b*>2 · A5 H(2060) · A6 D-optimal U13 (provisionally — *"engine yes, dimension-reduction no"*) |
| **COMPUTE-SHAPED** | **1** | A8 record 239 — *and the compute is already spent, privately, by the record's own authors, 700 orders of magnitude ahead* |
| **CONTEST-SHAPED** | **1** | A7 Chow C(3) — priority; §4.2 |
| **DELIVERABLE-SHAPED** | **1** | A9 MOLS(12) — the null was about the wrong object; the target's own shape is still uncosted |

> **[The count moved from 5 to 6 on 30 Sep 2026.]** A6 was first entered as UNDETERMINED from a
> summary line; the underlying audit had computed it. The correction **strengthens** §4.1's finding
> and weakens my standing as its author, which is the right way round for it to be wrong.

Cycle 0 says of this field: *"Claude Code multiplies compute-shaped constraints and does almost
nothing for theory-shaped ones. A problem whose prior run stalled on encoding theory is not made
tractable by a longer run."*

**Filled in, the field says the programme has been selecting targets whose constraints its tooling
does not relieve.** One attempted target of nine had a compute-shaped constraint, and it was held
privately by the people who set the record. **Six of nine were theory-shaped, and one of those six
was selected *because* we were already tooled for it** — `../../fallbacks/QUEUE_V3.md` ranks U13 first
on the ground that *"the algorithmic-idea gap, if there is one, is one we are already tooled for"*.
Tooling adjacency is not evidence that a constraint is compute-shaped, and A6 is the row that shows
it: the apparatus is shared, the orders are not, and the dimension reduction is the part that does
not carry. This is a statement about the **targets**, not about the
screen's gates and not about its scoring vocabulary — which makes it independent of, and a good deal
sharper than, the 0-of-7 tally. `LEDGER` lesson 39 established that 0-of-7 measures the scoring
vocabulary; this says something 0-of-7 cannot: that even a perfect screen over this population would
have been selecting into theory-shaped constraints.

### 4.2 The field has no cell for what bound the one verified result

A7's constraint was **priority**: someone else moved the quantity while we were moving it. That is
neither compute-shaped nor theory-shaped, and Cycle 0's binary has no third value.

The board already knows why this matters. `D58`: *being scooped is a direct crowding measurement of a
kind no gate on this board ever produced — not "has anyone moved this" inferred from publication
history, but "someone moved this while we were moving it", learned by attempting it.* `D47` records
that crowding decided none of the three bars that tested it. `D51` records that S4 counts moves and is
therefore blind to an attempt.

**So the register's deciding field needs a third value — CONTEST-SHAPED — and the one row where it
applies is the one row that produced a verified new mathematical object.** The field as Cycle 0 wrote
it would have classified this programme's best work as unclassifiable.

### 4.3 Four rows where the field cannot be filled, and that is a measurement

B5–B8 failed at S0, S3, S3 and S1 — *not evaluable at a usable tier*, *move kind UNKNOWN* twice, and
*not coupled*. Nothing about the shape of those constraints was learned because nothing about the
targets was learned.

This converges with what `../SELECT_v1.md` §9 measured from the other side: S3's COMPUTE class is
**empty, 0 of 10 testable problems**, and in practice S3 measured whether a move kind is *knowable*.
`../CYCLE0_VS_SELECT_V1.md` §2 records the three possible sources for the compute-versus-theory verdict
and their standing. **The register now closes that comparison with data:**

| source of the verdict | availability | evidence |
|---|---|---|
| record-paper **move kinds** (SELECT v1's S3) | **unmeasurable** — 0 of 10 | `../RESULT_TEST_G.md`, `../SELECT_v1.md` §9 |
| the frontier paper's **method section** (Cycle 0's Task 3) | **obtainable**, and it classified Cycle 0's candidates | `../CYCLE0_VS_SELECT_V1.md` §2 |
| **our own prior attempts** (Cycle 0's Task 1) | **obtainable now, from documents** — 7 of 8 rows classified | this register |

Cycle 0 called our own attempts the most direct source of all and could not reach it. It is reachable,
and it classifies 7 of 8 rows where the literature-derived proxy classified 0 of 10.

### 4.4 What the input actually cost

Cycle 0 called the input *"cheap to obtain and never obtained"*. Over transcripts it was not cheap, it
was impossible. Over committed documents it **is** cheap — one session, no external access, no
operator round-trip for seven of the eight rows.

**The register was unbuildable for want of a repository, not for want of insight, and the thing that
made it buildable was the habit of writing results down where the next instance can read them.** That
is an argument for the repository rather than for the register, and it is the honest form of `LEDGER`
lesson 41: a prompt is not an instrument until its inputs exist.

### 4.5 Two taxonomies are on file, they disagree, and neither cites the other

This register used **Cycle 0's binary** because `D56` (iii) asked for it. `../GAP_V3.md` §3, written
nine days before this document, runs a **four-way** classification of the same thing — *"classify the
gap, not the problem"*: **compute** (*"models do not add FLOPs. Deprioritise"*), **algorithmic idea**
(*"yes, with capability"*), **breadth/literature** (*"yes, with cost"*), **verification** (*"already
our strength"*).

**They disagree on A1.** `../GAP_V3.md` puts PTE 11 in the **compute** row — *"10⁶ core-hours vs
one"* — while this register classifies it **theory-shaped**, because the frontier was set by an
enumeration method we do not have. Both documents cite the same fact: *"no amount of capability
closes that; only their algorithm does."* One taxonomy files that under compute, the other under
theory, **and the operational advice differs**: GAP_V3's *algorithmic idea* row is the one it says
improves with capability, so if PTE 11's gap is an algorithm rather than FLOPs, GAP_V3's own rule
says *hold* it rather than deprioritise it.

`../GAP_V3.md` §2 also already contains this register's headline, argued structurally rather than
measured: *"a problem settled by one explicit finite object in a huge space is, almost by definition,
a problem whose frontier is set by search capacity… The empty queue is not bad luck. It is what this
screen returns."* **So §4.1 is a measurement of a claim already on file, not a new claim** — and the
measurement's sign is the opposite of what that sentence predicts, which is the part worth having.
GAP_V3 predicts the screen selects for *compute* gaps; the register finds six of nine attempted
targets were *theory*-shaped and only one compute-shaped. Either the taxonomies are being applied
inconsistently, or the screen selects for something GAP_V3 misnamed.

**The resolution is not to pick one, and this is the register's recommendation for any successor
rubric.** Both scales conflate "what stands in the way" with "what would remove it", and only the
second is decision-relevant. Split it five ways, by remedy:

| value | what closes it | does model capability close it? |
|---|---|---|
| **FLOPS** | more compute of the same kind | **no** — a model does not add FLOPs |
| **ALGORITHM** | a better search, encoding or enumeration at the same compute | **yes**, and this is where A1's real gap sits |
| **THEORY** | a new structural result, not an implementable method | **not reliably** |
| **BREADTH** | reading and adjudicating more literature | **yes, and it gets cheaper** |
| **CONTEST** | nothing — someone else arrives first | **no**, and only entering measures it (§4.2) |

Under that scale A1 is **ALGORITHM** (reproducing Coppersmith et al.'s residue-class chaining), not
FLOPS and not THEORY — which is a *less* pessimistic verdict than either document on file, and
changes what PTE 11's corpse is evidence for. **A successor rubric must fix one scale before scoring
anything, or its scores cannot be compared with any verdict already recorded.**

---

## 5. What is actionable, and what my first answer to that got wrong

**First version of this section, retracted.** I wrote that A6 was the register's one actionable row
because its deciding computation *"was specified and not run"*, and registered `P-41` predicting the
orbit ansatz would come back empty. Both rested on `../../doptimal/README.md`'s phrase *"may empty the
orbit ansatz altogether"*. **The audit in the same directory had computed it**, and
`../../doptimal/VERIFIED_OUTPUT.txt` §3 already gives the two-block ansatz as *admissible: none* at
five of the six orders of interest.

**Three things follow, and none of them flatter the register.**

**(i) `P-41` was not blind.** It predicted "empty at every order of interest" against evidence sitting
in a file I had not opened, in the directory I was citing. A prediction made against evidence already
on file measures nothing about foresight. It is marked **void-as-registered** in the ledger rather than
scored, and not re-worded — `D44`'s rule is that bands are not redrawn after the answer is visible,
and the same discipline applies to a prediction whose blindness fails.

**(ii) The failure is `D56`'s, occurring inside the register built to discharge `D56`.** A document
that exists, resolves, and is never consulted — and this time the unconsulted document was two files
along from the one I cited, so no access limit, no sibling instance and no missing repository explains
it. It is also `LEDGER` lesson 41 a second time: *"specified"* read exactly like *"performed"*, and
now a README's *"may"* read exactly like *"has not been"*. **A summary line is a claim about a
document, not a substitute for it.**

**(iii) What is actually actionable is two questions, and neither is ours.** U13 sits with the
Hadamard worker, which is where the estimator is. The audit's own §6 ordered its asks cheapest-first,
and the first can end the whole thing:

1. **§3.5, one lookup.** Do the maintained table's open *n* ≡ 2 (mod 4) orders intersect the orders
   where a two-circulant construction is the live route? *If no, U13 is dead and everything else is
   moot* — and U13 is the candidate `../../fallbacks/QUEUE_V3.md` ranks **first**, so this lookup
   decides the top of the queue.
2. **§3.2 at *k* = 2, with their estimator rather than a Monte Carlo.** Where does the coefficient
   cross zero? That converts A6's shape from provisional to established, in either direction. The
   audit also offers a consistency check it could not run itself: the same formula at *v* = 523,
   *d* = 9 needs *b* = 4.87 to reproduce the worker's own log₂ E[#sol] = 90.9, against a measured
   *b* = 4.02 at *v* = 151 and rising.

**So the register's actionable content is a routing decision, not a computation**, and the routing is
to leave the target where it is. Moving U13 back would mean rebuilding the worker's context in order
to ask two questions they can answer from theirs.

## 6. Limits

1. **Built from self-reports.** Documents were written by the runs whose work they describe. Where a
   figure could be recomputed it was (§0.3); where it could not, it is tiered.
2. **Depth is as stated**; no search was re-run.
3. **Two rows describe work invisible to this repository** (A4's sibling sweep, A8). `D56`'s
   escalation applies: grepping the tree is necessary and not sufficient, and the register inherits
   that limit rather than fixing it.
4. **Part D is empty and stays empty.** See below.
5. **Not applied retroactively.** No verdict on file changes because of this document. The shapes in
   §4.1 are a reading of constraints already recorded, not new verdicts.

---

## 7. Part D — Cycle 0's own seven rows, still empty

Cycle 0 wanted rows for **Kalai 3^d, Kaplansky ZD, Tuza, MDS char 2, Zarankiewicz/Hill, Mahler,
union-closed.** Those transcripts do not exist here and this register does not recover them. But the
tree is not silent about the problems, and the distinction matters: what it holds is the **later
lineage's independent assessment**, never the prior attempt's binding constraint.

| Cycle 0 problem | what this tree holds | is it a row? |
|---|---|---|
| **Kalai 3^d** | `../REVIEW_JULY_GAP_ANALYSIS.md` §1 verified the tightness claim: Σₖ C(*d*,*k*)·2^(*d*−*k*) = 3, 9, 27, 81, 243, 729 — exact at every *d* ≤ 6 | no — a verified premise, not an attempt |
| **Kaplansky ZD** | §2.2: the family nests unit ⇒ ZD ⇒ idempotent, so Gardam 2021 refuted the **easiest** member and ZD is strictly harder — which breaks the July analysis's own D = 5 score. Playability demoted record 280 for the same reason and notes a Bar-Ilan AI-algebra lab already pointed at the live object | no — but the *direction* correction is reusable |
| **Tuza** | §1: K₄ and K₅ exactly tight, ν = 1/τ = 2 and ν = 2/τ = 4 | no |
| **MDS char 2** | §1: Ball's *k* ≤ 2*p*−2 is vacuous at *p* = 2, since 2 < 3 | no |
| **Zarankiewicz/Hill** | **FILLED, 1 Oct 2026 — `../v4/RESULT_STALL_ZARANKIEWICZ.md`.** The operator obtained the prior program's own stall analysis, stated as formal propositions with proofs, which is exactly the form Cycle 0's schema asked for and could not get | **yes — the only Part D cell that is now a row** |
| **Mahler** | in `../sources/EPOCH_UNSOLVED_LIST.md`, `../epoch_exclusions.json`, the playability ranking | no |
| **union-closed** | in `../../fallbacks/RESULT_500_RESCAN.md`, `../sources/GAP_V2_RESPONSE_RAW.md`; Cycle 0's preamble records it was swept by the field before the run began | no |

> **[RESOLVED 1 Oct 2026, and the answer is outside Cycle 0's dichotomy.]** The binding constraint
> was **neither compute nor the realizability theory**. It was **SPECIFICATION** — whether the
> implemented predicate matches the one Woodall intended, and whether there is any way to tell. Three
> admissible readings of his definitions existed; the program held the wrong one for two sessions
> with a clean control record; and the only thing that discriminated was a *certified generator*
> whose guarantee is geometric and independent of every checker. Compute ceased to bind **1.2 seconds**
> into the first productive search. Cycle 0's rule — *"if theory, Claude Code adds little and this is
> dead"* — does not fire, and the correct reading is that the candidate was never dead; it was
> unfalsifiable until a generator existed. Registered as a **sixth** constraint shape in `D61` and as
> a control-design defect in `D66`. **Section 4.1's tally is not restated here**: that tally uses
> Cycle 0's binary because `D56` (iii) asked for it, and this cell's answer is in a vocabulary the
> binary does not contain — which is itself §4.5's argument, arriving from the one case that could
> test it.

**The missing cell, as it stood before 1 Oct.** Cycle 0's shortlist candidate B was Zarankiewicz
K₇,₁₁/K₉,₉, with this note attached:

> *"the prior chat session already worked this. The register must establish whether it stalled on
> compute or on the cyclic-order realizability theory. If theory, Claude Code adds little and this is
> dead."*

**That question was unanswered for a lineage, and it took one message.** It is the single cell where
Cycle 0 said in advance that the deciding field would settle a candidate outright. The register could
not reach it from documents and said so — correctly, since it needed something only the operator
could obtain. **What arrived was better than the transcript Cycle 0 wanted:** not a record of what
happened, but an analysis of *why*, in the form the schema specified. The lesson the register drew —
that "buildable from documents" has a boundary running exactly where the predecessor's work was never
committed — survives, with one amendment: **the boundary is crossed by asking, and the asking was
never budgeted.**

---

*Arithmetic: `register_arithmetic.py`, 39 assertions, all passing. Schema: Cycle 0's Task 1. Debt:
`D56` (iii).*

# Handoff — generate new queue candidates, and start from an instrument defect

**For an Opus 5.5 instance in Claude Code, reasoning effort `max`, with subagent creation.**
Delegate breadth to Sonnet 5.5 workers; keep adjudication and bar design yourself. Everything is in
the private repo you are in: `board-finder/` is the research, `proof-protocol/` is the ledger, debts
and the 14 consistency checks. Paths below are repo-root-relative.

**The task is to put new candidates in the queue. The hard part is not finding open problems — it is
finding ones whose difficulty is of a kind that anything you can do will move.** Read §1 before
doing anything, because the obvious approach has been run twice and measured to fail.

---

## 0. Start here: a verified contradiction between two of this project's own instruments

I checked this directly against `playability/classification.json` before writing this prompt, and it
is the highest-value lead in the repo:

```
playable by class:   P1  9/9 playable      II  0/22 playable
                     P2 24/24              W   0/2
                     P2n 1/1, P2p 1/1      A   0/16       U 0/424
```

The `II` class is defined in that file as *"exact-value / optimality determination (a record, not a
witness)"*. **All 22 of them are `playable: false`, and all 22 carry `witnessCheckFeasible: null` —
they were excluded by class, so they never received a feasibility verdict at all.**

Now look at what the project actually queued. `fallbacks/QUEUE_V3.md` lists four candidates:
D-optimal designs of order 2*v*, kissing-number lower bounds in dimensions 11–14, caps in AG(7,3) /
AG(8,3), snake-in-the-box in dimensions 9–11. **Every one of those is a record problem — `II`-shaped
— and none of them came from the 499-record corpus at all.** (`proof-protocol/ledger.json` lesson 22
measured that: fifteen of this project's own topics are absent from the 499 entirely.)

So the playability screen says record problems are unplayable, and the queue this project built by
hand is made of nothing else. **One of those two instruments is wrong.** The screen keys on the
presence of a finite *witness*; a record has a finite *value*, and the screen has no slot for that.

`playability/INTERESTINGNESS.md` §5 P1 says the same thing from the other side: *"stop collapsing to
a scalar, report the pair."* A record's difficulty is not a witness's difficulty, and a screen with
one axis cannot see both.

**This gives you 22 candidates inside data the project already owns and has never assessed.** Three
have been touched since: **337** (binary deletion channel) is **dead** — arXiv:2609.19412 narrowed it
to a hundredth of a bit; **221** (random 3-SAT threshold r₃) and **282** (qubit depolarizing capacity)
were assessed in `fallbacks/RESULT_MAPPING_D.md` §§3,5 and both failed, 221 on deliverable and
verification, 282 on headroom. **Nineteen are unexamined.** The full list with ranks is in
`classification.json`; grep `"cls": "II"`.

Do not treat this section as a conclusion. It is a lead with a specific defect attached, and the
first thing to establish is whether the `II` exclusion is a *defect* or a *correct rejection that
the queue is wrong to ignore*. Both readings are live and they point opposite ways.

---

## 1. What has already been tried, with numbers, so you do not rebuild it

**Screening lists of important problems is exhausted, and that is measured rather than guessed.**

| attempt | result |
|---|---|
| GAP v1/v2 triage over the 499-record corpus | three targets cleared; all three died on properties of *our position*, not of the problem |
| 499-record rescan for fallbacks | one candidate (CC-6 / MOLS(12)); died at gate F4 |
| 106-record mapping layer, four chunks | **2 candidates**, neither leading the queue; all 106 mapped |
| five named mid-band candidates | **five for five dead** |

And the reason is understood. From `gap/GAP_V3.md` §3 and `fallbacks/QUEUE_V3.md`:

> *A problem settled by one explicit finite object in a huge space is, almost by definition, one
> whose frontier is set by search capacity. So the finite-witness screen systematically selects for
> **compute gaps**, which are the one category that does not improve when models get better or
> cheaper — a model does not add FLOPs.*

**That is the trap, and it is the reason this handoff exists.** A screen that selects on witness
shape will keep returning compute gaps. `INTERESTINGNESS.md` §5 P4 records the sign error explicitly:
its own first draft weighted *up* on finite-witness class and was wrong.

`ledger.json` lesson 22 adds the other half: three curated problem lists built independently by
serious people overlap pairwise at **5–20%**, which makes *"absent from list X"* nearly worthless as
evidence — and makes *"present on list X"* nearly worthless as a selection signal. Editorial
importance and this project's screen are close to orthogonal selection functions.

**So: do not go and screen another corpus of famous problems.** If that is where you end up, you
have reproduced a measured failure.

---

## 2. The two coordinates, and why nobody computes both

`INTERESTINGNESS.md` analyses Patel, Rammal, Hayat, Munos, Kempe, *"Learning to Discover Interesting
Mathematics"* (arXiv:2609.28603). Their scalar is

```
    I(T | P) = 100 · V(T | P) / L(T | P)
```

`V` = lines of Lean to derive `T` from premises `P`; `L` = conditional description length. Easy to
state, hard to prove. **The blindness that matters: `I` sits at its floor for every finite-witness
problem**, because proof length does not measure difficulty when the difficulty lives in a *search*.
The demonstration in §2 of that document is a Hadamard orbit ladder where `V` and `L` are both
constant by construction while real difficulty spans **75 bits** and separates solved from unsolved
cleanly.

Their §4 mismatch is the one that bears on your task: **their metric is defined on solved theorems.
For an open problem `V` is undefined**, so interestingness cannot rank open problems except through a
learned `V̂`, which is trained on proofs capped at 500 lines and *underestimates everywhere, worse as
length grows*.

So the reporting format for every candidate you produce is the pair, never collapsed:

```
    (  V_arg(T | P)  ,  bits_search(T | P)  )
```

`bits_search = −log₂ ρ`, ρ the density of witnesses in the searched space. **This is the coordinate
the literature does not compute and this project does** — `density4.py` / `validate2.py` on the
Hadamard side are validated to ≤0.3 bits. It is also the coordinate that is only *defined* where a
search space and a density estimate exist, which is false for most of the 35 playable records
(`INTERESTINGNESS.md` §6). Where you cannot compute it, say so; do not substitute a guess.

---

## 3. The generative engine: classify the gap, not the problem

`INTERESTINGNESS.md` §5 P4's corrected form puts the positive weight on gap type:

```
    Select(T) = I_irred(T | P) × w_class(T) × g(gap_type(T))
```

with `w_class` a **veto** (W → 0, A → 0) rather than a bonus, and `g(gap_type)` carrying the upside:
**algorithmic-idea and breadth gaps over compute gaps.** `GAP_V3.md` §3 defines the four types —
compute (never improves), algorithmic-idea (improves with capability), breadth/literature (improves
with cost), verification (existing strength). DeepMind's FunSearch improving the cap-set record in
AG(8,3) is the existence proof that the first category moves under model capability.

**`g(gap_type)` has never been scored against outcomes** (`INTERESTINGNESS.md` §6), so operationalising
it is your main contribution. Two tests I propose; both are mine and neither has been run, so treat
them as hypotheses to validate, not as given:

**3.1 The record's own movement history classifies its gap.** For any record with a maintained table,
ask what caused the last two improvements. A new construction, reduction, or theorem → **idea gap**,
which is the category that moves. More CPU-hours, a bigger cluster, a longer run → **compute gap**,
dead on arrival. This is per-record, cheap, and reads off the literature rather than requiring
judgement about the mathematics. **It is breadth work: give it to Sonnet workers.**

**3.2 Divergent reach between two published methods on the same problem is a measured idea gap.**
Where method A reaches far further than method B on the same object, the difference is an idea and
its size is quantified. This is exactly what makes Hadamard 2092 this project's one live target:
`FINDING 157` §3 puts Alpöge's implied growth exponent at roughly **half** this project's measured
0.503, which is a factor-of-two idea gap stated as a number. **A candidate with a divergence like
that is worth more than a candidate with a big `bits_search` and no divergence**, because the second
is just a compute gap with a large number attached.

If 3.2 works as a screen it is the most valuable thing you can hand back, because it is a *generative*
signal — you can go looking for divergences directly — where everything this project has tried has
been *filtering*.

---

## 4. Three arms, in this order, with bars registered before each runs

Register your predictions in `proof-protocol/ledger.json` **before** dispatching workers. Single
threshold, no middle band: a previous gate used a two-sided test with an unregistered gap, the answer
landed in the gap, and it declined to score (debt D44). **Name which arm's output is the held-out
slice before dispatch, in writing** — debt D45 records the failure of taking a held-out slice from
the accident of processing order and registering no bar for it.

**Arm 1 — the 19 unexamined `II` records.** Give each a `(V_arg, bits_search)` pair where computable,
a gap type from §3.1, and the `w_class` veto. Register a bar on the count that survives.

**Arm 2 — outside the corpus, where lesson 22 says the seam is.** The fifteen topics absent from the
499 are skew-Hadamard, Williamson, Steiner systems, difference sets, Costas arrays, bent functions,
APN functions, 1-factorisations, D-optimal designs, covering codes, PTE, cap sets, snake-in-the-box,
Moore graphs, strongly regular graphs. **Maintained record tables are the generator** — Colbourn–Dinitz
*Handbook of Combinatorial Designs*, Brouwer's tables, the La Jolla difference-set repository, the
maximal-determinant tables, Sloane's lattice and kissing-number tables, and whatever has superseded
each. **§3's discriminator gates every candidate from this arm**, because this is precisely where the
compute-gap trap bites hardest: a design-theory table is a finite witness set by construction.

**Arm 3 — conjecture generation, bounded and explicitly secondary.** This is the paper's own route and
two findings say it is weak here: their reward is gamed **in their own showcase** (§3(c): `n > 0 ↔ …`
appears in two of thirteen highlighted generations, a real fact bolted to a triviality by `↔` to
inflate the numerator), and their loop optimises interestingness *conditional on solvability*, so open
problems are the complement of what it can rank (§4). **But ruling a thing out by argument rather than
by test is a failure mode this project has repeatedly paid for**, so run one bounded test with a hard
budget and a registered bar, and stop at the bar. If you generate conjectures, apply P2's `I_irred`
decomposition — split at top-level `∧` and `↔`, and flag as bolted when `Σᵢ V(Tᵢ) ≈ V(T)` with some
part closed by `simp`/`rfl`/`assumption`.

---

## 5. Calibrate before you trust any difficulty estimate you produce

`INTERESTINGNESS.md` §5 P5: the paper's strongest transferable result is negative and aimed squarely
at you. **Frontier models are badly calibrated on proof difficulty and all of them underestimate,
worse as difficulty grows** — MAE 20.2 for their fine-tuned 27B against 31.0 and 34.3 for two frontier
models. This project's own `FEASIBILITY.md` `witnessCheckFeasible` column is exactly that kind of
judgement produced exactly that way, **and its Hadamard cell was wrong by an order of magnitude in the
decision-relevant direction.**

The b=0 multiplier-orbit ladder is a **held-out calibration set**, not training data — roughly fifteen
labelled instances against the ~100k points they used, so do not try to fit a predictor. Density,
achieved floor ÷ 32, and solved/unsolved are ground truth. **Score your own difficulty estimates
against it before any of them gates a decision**, and per `FINDING 162` the quantity to estimate is a
**success probability per restart**, not a time: the distributions are bimodal and every single-seed
timing this project took before that was discovered was unsafe.

---

## 6. Worker design, and the prediction it scores

`gap/TIERS_2026-09.md` §3 sets the split: **bar design and adjudication are yours; bar execution,
breadth, and verification volume go to Sonnet 5.5 workers.** All the judgement in one of this
project's gates is spent when the bar is written, which is what makes execution delegable. The proof
case is `playability/GATE_RESULT_SIC.md` — executed by a respondent that fetched nothing itself, and
it still corrected two of that respondent's own priors, because the prompt was built around those two
traps in advance.

**`ledger.json` P-31 is live and your run scores it.** A-1 claims gate execution moves to the cheaper
tier without loss. Its registered threshold: **one verdict issued on a bar the run could not actually
evaluate and A-1 is FALSE.** So instruct every worker that *"I could not evaluate this bar"* is the
required answer when true, and that guessing a tidy verdict is the only real failure available. A-2
claims a cheaper screen does **not** turn four candidates into four hundred, because the cheap layer
cannot issue a verdict; its threshold is a candidate reaching the queue without a bar written for it
first. **Do not let that happen by accident** — it would falsify A-2 through process failure rather
than through evidence, which teaches nothing.

Give each worker: the bar verbatim, the provenance tiers (`PRIMARY-VERIFIED-LOCALLY` /
`SECONDARY-RELAYED` / `RECALL`), and the numerical-versus-exact rule. That last one has cost this
project the most: a breadth pass reported exact SIC-POVM constructions *"reaching d=19,603"* where a
dedicated gate had already established the exact ceiling is **5,779**, the higher papers admitting
their verification was *"mostly partial"*. Both cells were true at their own precision; one was
usable. **A breadth cell is triage-grade and may never be gated on** (lesson 24).

---

## 7. Standing rules. Each cost this project something real.

1. **A bar you cannot evaluate counts as FAIL, not "unscored."** Default is no.
2. **Verify objects, never function returns.** A search reporting success once cost a day.
3. **Positive controls before nulls.** Code that cannot find a known object proves nothing when it
   finds none.
4. **Negative-test every check.** Two checks written here in one day could not fail at all; one
   passed for hours matching nothing, because a regex was escaped for a heredoc rather than for
   Python.
5. **Derive counts, never type them twice.**
6. **Seven seeds, matched caps, medians** for any timing claim.
7. **Convert a speedup into frontier units before it changes a decision.** A 17× improvement to a
   search costing the sixth power of the frontier parameter buys 1.6× in frontier — that mistake was
   made here and nearly redirected a programme.
8. **Withdrawn and unrefereed claims are data, not resolutions.** A claimed resolution of the
   anisotropic Calderón problem was posted and withdrawn days later by its own authors and still
   recirculates in citation lists.

---

## 8. Outputs

Write under board-finder/, named "gap/RESULT_DISCOVERY.md" (the findings and the surviving
candidates), "gap/SELECT_v1.md" (the selection function as you actually operationalised it, including
whichever of §3.1 and §3.2 survived contact), and one result document per arm. Plain quotes
deliberately — check 14 fails the build on a backticked path that does not resolve, and those files
do not exist yet.

Each candidate gets: the `(V_arg, bits_search)` pair or an explicit statement that `bits_search` is
undefined and why; gap type with the evidence for it; the `w_class` veto result; the record table it
would move and the sentence that would appear in an abstract; and the first check that would kill it.

Then update `fallbacks/QUEUE_V3.md`. **Also check whether "RESULT_S55_A_TABLE.md",
"RESULT_S55_B_239.md" and "RESULT_S55_C_345.md" exist under `fallbacks/`** — a Sonnet run was
draining the previous queue and its results may not have been pushed when this was written. If they
are absent, say so rather than assuming the previous queue's fate.

**Git.** Push to `claude/theorem-discovery-lab-jpbph1`:
`git push -u origin HEAD:claude/theorem-discovery-lab-jpbph1`. Another instance works on that branch;
if the push is rejected, `git fetch origin claude/theorem-discovery-lab-jpbph1` then `git merge
FETCH_HEAD` — **never rebase, never force-push.** This repo only tracks `main`, so
`origin/claude/...` is not a valid local revision; compare with `FETCH_HEAD`. Run
`proof-protocol/tools/check_consistency.py` before finishing. **No pull request** unless asked.

---

## 9. What a successful run looks like

**Not a long list.** The honest base rate is two candidates per 106 records screened, and the one
leading the queue came from outside the corpus. A run that returns **one candidate with a measured
idea gap** is worth more than twenty with large `bits_search` and no gap-type evidence, because §1
says the second kind is what this project has repeatedly bought and never cashed.

**A clean negative is a real outcome.** If the `II` exclusion in §0 turns out to be correct and the
queue's record-shaped candidates are the ones that are wrong, that is a finding about this project's
own instrument and worth more than a candidate. Say it plainly and register it.

**The one thing to avoid** is arriving at a list of plausible-sounding problems with no gap-type
evidence attached. That is the artefact every previous attempt produced, five of five of them died,
and the reason is written down in §1.

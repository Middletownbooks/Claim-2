# Report U — The Research Team Meta-Game

Phase U asks whether a research *team* can learn a transferable policy for
choosing what to investigate. Most of what the brief proposes cannot be tested
in this environment. One thing can, and it turns out to be the sharpest result
in the programme — about this programme.

---

## 0. What Phase U cannot test here, stated before anything else

| §  | asks for | status |
|---|---|---|
| 6, 13 | multiple differently-tasked LLMs, human/LLM role comparison | ~~impossible~~ **RETRACTED — see §8. I can spawn agents; I asserted otherwise without testing.** Partially available: coordinator + differently-tasked agents. Still unavailable: the human side of the team, and genuine independence (spawned agents inherit my repository and framing) |
| 6, 7 | R1–R4 resource regimes with real teams | **impossible** — no teams |
| 14 | prospective real research (open Hadamard orders) | **impossible** — no prover, no compute at that scale, and a prospective claim would take months to settle |
| 9 | T1–T4 access conditions as a controlled experiment | **impossible as designed** — but the *observational* version is answerable, and is answered in §3 below |
| 8 | lessons-vs-raw-results as a controlled comparison | **partially** — observational only |
| 2, 10 | frontier-selection policy | **simulation only** (§4), conditional on its model |

What *is* available is a complete, committed research trajectory: **Phases 0–T,
20 hours, 11 phases, 36 commits, ~20 reports, 8 pre-registrations with declared
predictions and scored outcomes.** That is one real research team's meta-game,
with the record kept honestly enough to audit. Phase U audits it.

n = 1. Everything below is about a single team, and generalises only as far as
a single case can.

---

## 1. The programme's own forecasting record

> **This section was rewritten after an independent audit overturned it. The
> first version's headline — that the team's forecasts carried no information —
> was an artifact of a ledger that sampled only the phases in which I had been
> wrong. §8 records how that was found.**

`COMPUTED FROM ARTIFACT` (`u/ledger2.py`, `u/forecast_ledger_corrected.json`).
Every pre-registered prediction in the committed record, from **ten**
pre-registration documents, classified POSITIVE (an effect or specific outcome
exists) or NEGATIVE (a null), scored as written. Five entries the source
reports mark PARTIAL or marginal are excluded rather than adjudicated.

| | held | total | rate |
|---|---|---|---|
| POSITIVE predictions | **18** | **32** | **56%** |
| NEGATIVE predictions | 10 | 12 | 83% |

The 2×2 — does the prediction predict the outcome?

| | an effect existed | no effect | |
|---|---|---|---|
| predicted GO (effect) | **18** | 14 | P(effect \| GO) = **0.562** |
| predicted NO-GO (null) | 2 | 10 | P(effect \| NO-GO) = **0.167** |

Base rate of true effects: 20/44 = 0.455.

$$\textbf{Fisher exact, two-sided: } p = 0.0389$$

**The team's directional forecasts were informative.** A GO prediction was
followed by a real effect 3.4× as often as a NO-GO prediction was. Dropping the
four entries whose polarity classification is genuinely arguable (`K-P3`,
`L-P2`, `L-P4`, `L-P6`) leaves the result intact: p = 0.0408, n = 40.

### The distinction that survives, and matters more

Two classes of forecast, with opposite records:

| forecast class | record |
|---|---|
| **within-experiment** — "what will this run show?" (44 predictions) | informative, p = 0.039 |
| **between-phase** — "which direction should we fund next?" (3 recommendations) | followed 3/3, positive content survived **0/3** |

Phase Q recommended upstreamability; R and S refuted it as transport. R
recommended interface-mediated transport; S falsified it (I\|V = −0.44,
p = 0.0008). S recommended the architecture channel; T falsified it and found
the Phase S metric had been 54% `have`.

0/3 is not significant on its own (p = 0.25 against a coin-flip null), so this
is **suggestive, not established**. But the direction is worth stating: this
team could predict what its own next experiment would show, and could not
predict which research direction would pay. Against §5's three types, that is
local strategy working and **frontier selection failing** — which is the one
the brief argues matters most for small teams.

### What produced the findings

Whatever the forecasting record, the machinery that made each phase decisive
was the same throughout and is the part that visibly transferred:
pre-registration scored as written; a matched control for every claim; a
positive calibration control whose job is to prove the instrument can detect
anything at all (Phase Q's Euler→NS was decisive exactly there); and
self-directed error search, which caught seven defects, four of them after the
headline result was in hand, three of which reversed an interpretation.

## 2. Resource accounting

`COMPUTED FROM ARTIFACT` (`u/accounting.txt`), elapsed wall-clock between phase
boundaries in the git record.

| phase | commits | hours | what it established |
|---|---|---|---|
| audit | 4 | 0.15 | E-family pretest audited; no Lean verification possible anywhere |
| A–G | 1 | 3.19 | Lean 1000+ board mapped; bridge ledger |
| H/I/J | 3 | 1.35 | FLT artifact mapped; retrospective benchmark (breadth > frequency) |
| K/L | 4 | 0.56 | per-object ceiling breaks; machinery transfers, vocabulary does not |
| M | 1 | 0.65 | **term formation works when a formed term is charged as one unit** |
| N/O | 3 | 0.30 | NS mapped; **Report J fails to replicate (0/6)** |
| P | 10 | **6.85** | RESULT C: no recursive compounding; 7 of 8 predictions failed |
| Q | 2 | 0.56 | FLT↔NS transport negative; Euler/NS calibration |
| R | 1 | 3.12 | QPR = sub-board; the collection is the find |
| S | 1 | 1.67 | interface channel falsified (I\|V = −0.44) |
| T | 1 | 1.60 | trajectory transport falsified; only L1 token style is source-specific |

Total **20.0 h**. Three phases produced positive findings at a combined 2.56 h;
five produced falsifications at 11.0 h. The most expensive phase (P, 6.85 h,
34% of the budget) returned a falsification.

Two observations that matter more than the totals:

* **The cheap wins came first and one of them did not survive.** Report J
  (breadth beats frequency, 1.35 h) was overturned by Report O (0/6 on NS,
  0.30 h) — a falsification that cost a fifth of what the finding cost. Of
  three positive findings, one was retracted by the programme itself.
* **Falsification was cheap relative to the hypothesis it killed.** Phase S
  killed the interface channel in 1.67 h; Phase T killed the architecture
  channel in 1.60 h. Neither hypothesis was cheap to *generate* — each took a
  full prior phase — but both were cheap to *kill*.

---

## 3. The trajectory-publication regularity (§9, observationally)

The moat hypothesis says accumulated trajectory knowledge is an advantage hard
to reproduce from the published result alone. That is testable observationally:
**what do teams actually publish?**

| artifact | published | trajectory available? |
|---|---|---|
| `anthropics/fermats-last-theorem` (2026) | single squashed commit; **comments stripped** — ATTRIBUTION.md: *"assembled by AI agents and were published without their comments"*; measured comment density 0.000% in `Theorems/`, 0.002% in `P2M/Sol/` | **no** |
| `openai/NavierStokesAndEuler` (2026) | single squashed commit; ~2% comments, keyed to the source paper's equation numbers | **no** — a Lean↔paper map, not a process record |
| `openai/ten-proofs` (2026) | single squashed commit; **zero comment lines in all ten files** | **no** |
| **Hadamard orders < 2000** (Alpöge, Voinov, Reynolds-Haertle with Claude, Aug 2026) | the matrices themselves, posted as an encoded text block with a decoder script; the twelve previously open orders 668, 716, 892, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, 1964 | **no** — reporting notes the construction methods are not detailed |

`DIRECTLY OBSERVED` for the three repositories; `DOCUMENTED BY SOURCE` for the
Hadamard result (see Sources).

> **[8 Oct 2026 — this regularity has now failed three times; read §3 as a fact about four
> artifacts in September, not a norm.]** `ak/REPORT_AK_zeta_audit.md` §6 documents a disclosed run:
> ~650 approaches, ~60 subagents, ~31 M output tokens, attribution per agent.
> `at/REPORT_AT_audit_surface.md` part 2 has OpenAI's full CDC prompt. And `github.com/openai/math`
> (public 6 Oct) ships abridged reasoning summaries for 10 families, the denominator (~4,000
> problems posed → 372 families), and a public changelog that withdrew three manuscripts within
> 31 hours of release. The §9 access experiment is still unrun, but its blocker — *no producing
> team releases trajectory* — no longer holds. See `../openai-math/RESULT_INTAKE.md` §6.6.

**Four for four.** Every major AI-assisted mathematical result available to
this programme was published as **T1 — final results only**. Not one released
construction history, search logs, failed attempts, or lessons.

This is the strongest available evidence for the moat hypothesis, and it is
the *wrong kind*: it does not show that trajectory access confers an advantage,
only that trajectory is systematically withheld — so the advantage, if it
exists, is structurally unavailable to anyone outside the producing team. That
is a fact about publication norms, not about mathematics. Phase Q reached the
same wall from the other side (Level III strategy transport untestable for want
of trajectory data), and Phase U now shows it is not an accident of two
artifacts but a uniform practice across four.

**The actionable form of this**: a small team's realistic option is not to
obtain a competitor's trajectory. It is to reverse-engineer structure from
final results — which is exactly §4's motivating question, and which this
phase could not run for want of the matrices themselves.

---

## 4. Scarcity: which lever buys findings? (§7, simulation)

`SIMULATION` (`u/scarcity.py`). **Conditional on its model, and re-run after
the §1 correction** — its base rate input was taken from the flawed ledger and
was wrong (0.143; the corrected value is 0.455).

A team faces 40 candidate hypotheses and can afford `budget / cost` decisive
tests. Findings at fixed budget, from the measured operating point:

| budget | base | halve cost per test | forecast 0 → 0.5 | both |
|---|---|---|---|---|
| **10** | 4.55 | 9.06 (**+99%**) | 10.00 (**+120%**) | 17.61 |
| 20 | 9.07 | 18.20 (+101%) | 17.63 (+94%) | 18.11 |
| 100 | 18.19 | 18.26 (+0%) | 18.11 (−0%) | 18.26 |
| 1000 | 18.25 | 18.24 (−0%) | 18.17 (−0%) | 18.16 |

The model saturates above budget ≈ 20; the realistic regime for a small team is
the top row, where the candidate pool vastly exceeds what can be tested.

**At severe scarcity the two levers are comparable** — +99% for halving the cost
of a decisive test against +120% for a large forecast improvement, and they
compose (+287% together). The first version of this report claimed forecasting
dominated by 3×; that was an artifact of the wrong base rate and is withdrawn.

Since §1 now shows the team's within-experiment forecasting is genuinely
informative, both levers are live for it — but note what the table also says:
past budget 20 neither lever matters, because the binding constraint stops
being selection and becomes the size of the candidate pool.

## 5. Answers

### §13 — Does explicit control over meta-moves improve verified output per unit resource?

**Yes at the experiment level; not demonstrated at the direction level.** The
meta-moves that paid: pre-registration, matched controls, positive calibration
controls, and early termination of a doomed representation (Phase T retired
Phase S's `have`-dominated metric rather than extending it). Within-experiment
forecasting was informative (p = 0.039). The meta-move with no surviving
positive content across three attempts was **choosing the next research
direction**.

### §16 — Is the hypothesis weakened?

**Split.** The brief's criterion *"lessons learned do not improve subsequent
decisions"* is met in the direction-choosing sense: compressed lessons were
followed 3/3 and led to a falsification 3/3. But *"strategy transfer disappears
across domains"* is **not** met — the methodological policy transferred across
eleven phases and four subject matters and worked every time.

The lowest level at which this team obtained transferable advantage is
methodological. The highest level at which it obtained any measurable skill is
predicting its own experiments. Between those two sits frontier selection,
where it has no demonstrated skill at all.

### §17 — What should a rational research team do when it cannot afford to try everything?

Stated as narrowly as the corrected evidence supports:

1. **Trust your forecast about the experiment in front of you; distrust your
   forecast about which direction to fund.** Those had opposite records here,
   and only the second is what the brief calls frontier selection.
2. **Buy decisiveness.** Halving the cost of a decisive test is worth about as
   much as a large improvement in forecasting, and it is the lever you can
   actually build.
3. **Instrument the null.** Five of eleven phases returned falsifications and
   they were the phases that changed what the programme did next.
4. **Audit your own record before you trust it, and get someone else to.** The
   headline of this report survived exactly as long as it took one independent
   agent to check the ledger against its sources.

## 6. Negative results, including this report's own

1. **The first version of §1 was wrong, and it was the headline.** It reported
   Fisher p = 1.0000 and concluded the team's forecasts carried no information.
   The correct figure over the complete record is **p = 0.0389** in the opposite
   direction. The error was a biased sample, not a miscalculation.
2. **Between-phase recommendations: 0/3 positive content survived**, while being
   followed 3/3. Not significant alone (p = 0.25); reported as suggestive.
3. **One of three early positive findings was retracted by the programme
   itself** (Report J, overturned by Report O at a fifth of its cost).
4. **The scarcity simulation's headline was also an artifact** of the wrong base
   rate and is withdrawn (§4).
5. **§0 claimed agent spawning was impossible.** It is not. Retracted in §8.
6. **The trajectory-publication finding stands**, and is the wrong kind of
   evidence for the moat hypothesis: it shows trajectory is systematically
   withheld (4/4), not that access confers advantage.

## 8. How the §1 error was found, and what that says about §13

This belongs in the report because it is the only clean instance of a
multi-agent research move in the entire programme, and it worked.

**The sequence.** The user pushed back on my §0 claim that I could not
instantiate other agents. I could. I spawned one Sonnet agent and gave it a
single adversarial task: verify the Phase U ledger against its primary sources,
and specifically hunt for pre-registered predictions that were **missing** from
it, since omissions would bias the count.

**What it returned.** Four defects, all confirmed by me against the sources:

| # | defect | verification |
|---|---|---|
| 1 | `P-6` and `T7` are the same prediction, counted twice | `termform2/PREREG.md:183` reads verbatim *"**P-6**: T7 (squarefree) is reached by no condition."* And I did **not** double-count the exactly parallel `P-7`/`T9` — an inconsistent rule applied to identical cases |
| 2 | `R-prior` was never pre-registered | no PREREG file exists anywhere under `leanboard/r/`; I scored `REPORT_R`'s own conclusion against itself, which cannot fail by construction |
| 3 | the merged `T1/T2/T3` entry silently included `T3` | `REPORT_P.md:326`: *"**T3 is struck.**"* |
| 4 | **six pre-registrations with 29 further scored predictions omitted** | `crossobject/PREREG.md` (K), `crossobject2/PREREG.md` (L), `termform/PREREG.md` (M), `flt/PREREG_blind_regions.md` (I), `flt/PREREG_retrospective.md` (J), `audit/PHASE15_preregistration.md` |

Defect 4 is the one that mattered. My ledger drew from four documents and
claimed to transcribe "Phases 0–T". The omitted six are the phases where the
predictions were largely **right** — Report L scored *all six correct*, Report M
four of four, Report I three of four. The omission was therefore not neutral: it
selected for my own failures and manufactured the headline.

The agent found defects 1–3 and flagged four of the six omitted documents. I
then completed the census myself and scored the remaining two, which is why the
corrected table has 44 entries rather than the ~30 the audit implied.

**What this says about §13.** The brief asks whether team architecture improves
verified output independently of raw model capability. Here is one data point
with a clean causal story: a coordinator produced a result, a differently-tasked
verifier with the single instruction *look for what is missing* overturned it,
and the fix required no capability the coordinator lacked — only a role it was
not occupying. The failure was not analytical. It was that I audited others'
artifacts for six phases and did not audit my own ledger.

That is R2 in the brief's taxonomy — one coordinator plus a differently-tasked
agent — and on this single instance it changed the phase's conclusion. **n = 1,
and the confound is severe**: the verifier inherited my repository, my framing
and my file layout, so it is not an independent team. What it did have was a
different *task*, and that alone was enough.

## 7. What would actually test the meta-game

Stated concretely, since almost nothing here could be:

* **Frontier-selection transfer** needs ≥ 30 pre-registered *direction*
  choices with outcomes scored. This programme produced 44 scored
  within-experiment predictions in 20 hours but only 3 direction choices — which
  is exactly why §1's second table is suggestive and not established. Direction
  choices are the scarce observation, and a design that wants to measure them
  must make them the unit, not the by-product.
* **Multi-agent architecture (R2/R3)** is now known to be runnable here (§8) and
  was not run as an experiment. The minimal version: for each of k phases,
  produce the result twice — once by a coordinator alone, once by a coordinator
  plus an adversarial verifier — and compare defect counts at matched budget.
  §8 is a single uncontrolled instance of that design, and it found four
  defects.
* **The T1–T4 access experiment** needs one artifact published *with* its
  trajectory. Four for four withheld it. Until a producing team releases search
  logs and failed attempts, §9 stays untestable — and this is a request to make
  of artifact producers, not a computation. It is the same blocker Phase Q hit.
* **The Hadamard case** needs the matrices. The realistic small-team experiment
  is: given only the twelve published matrices, can their construction be
  reverse-engineered — are they Williamson, Turyn-type, two-circulant-core, or
  something new? That is a well-posed, checkable question, it needs no
  privileged access, and it is the one part of §4 a small team can actually
  play.

---

## Artifacts

`u/ledger.py`, `u/forecast_ledger.json` (**superseded**) ·
`u/ledger2.py`, `u/forecast_ledger_corrected.json` · `u/stats.txt` ·
`u/accounting.txt` · `u/scarcity.py`, `u/scarcity.json`.

## Sources

- [Hadamard Matrix of Order 668 — Epoch AI](https://epoch.ai/frontiermath/open-problems/hadamard)
- [A Hadamard matrix of order 668 — TheoremDB](https://theoremdb.org/statements/hadamard-order-668/)
- [Constructing Hadamard matrices — John D. Cook](https://www.johndcook.com/blog/2026/08/13/constructing-hadamard-matrices/)
- [New Hadamard matrices — Ion Nechita](https://ion.nechita.net/posts/new-hadamard-matrices/)
- [Hadamard Matrix — Wolfram MathWorld](https://mathworld.wolfram.com/HadamardMatrix.html)

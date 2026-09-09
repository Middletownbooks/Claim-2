# Report U — The Research Team Meta-Game

Phase U asks whether a research *team* can learn a transferable policy for
choosing what to investigate. Most of what the brief proposes cannot be tested
in this environment. One thing can, and it turns out to be the sharpest result
in the programme — about this programme.

---

## 0. What Phase U cannot test here, stated before anything else

| §  | asks for | status |
|---|---|---|
| 6, 13 | multiple differently-tasked LLMs, human/LLM role comparison | **impossible** — no API access; I cannot instantiate other agents |
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

## 1. The programme's own forecasting record — and a correction to my first analysis

`COMPUTED FROM ARTIFACT` (`u/ledger.py`, `u/forecast_ledger.json`). Every
pre-registered prediction across Phases P–T, transcribed from the committed
files, classified as **POSITIVE** (an effect exists) or **NEGATIVE** (a null),
and scored as written.

| | held | total | rate |
|---|---|---|---|
| POSITIVE predictions | 1 | 9 | **11%** |
| NEGATIVE predictions | 10 | 12 | **83%** |
| Phase-level recommendations followed by the next phase | 3 | 3 | 100% |
| …whose positive content survived testing | **0** | 3 | **0%** |

**My first reading of this was wrong, and the correction is the finding.** I
initially compared 1/9 against 10/12 by Fisher exact (p = 0.0019) and concluded
the team was "good at predicting nulls, bad at predicting effects". That
compares the precisions of *different propositions* and is not a test of
whether the forecast is informative.

The correct 2×2 asks whether the prediction predicts the outcome:

| | an effect existed | no effect | |
|---|---|---|---|
| predicted GO (effect) | 1 | 8 | P(effect \| GO) = **0.111** |
| predicted NO-GO (null) | 2 | 10 | P(effect \| NO-GO) = **0.167** |

Base rate of true effects across the 21 pre-registered tests: **3/21 = 0.143**.

$$\textbf{Fisher exact, two-sided: } p = 1.0000$$

**The team's directional forecasts carried no information whatsoever.** GO
predicted an effect slightly *less* often than NO-GO did. The apparent
11%-vs-83% asymmetry is entirely a base-rate artifact: when only 14% of
hypotheses are true, a coin-flipping forecaster already scores 86% on nulls.

This survives the obvious objection that the "author's priors" were mere
pessimism. Pessimism is not the issue — the issue is that neither direction
of forecast tracked the truth.

### What actually produced the findings, then

The programme's 20 hours produced eleven phase-level results, five of them
decisive falsifications. None of that came from choosing well. It came from
making each test **cheap and decisive**, by methods that were reused unchanged
in every phase:

* pre-registration with predictions scored as written;
* a matched control for every claim (Phase P's condition D and E; Phase Q's
  Euler→NS calibration; Phase S's size-matched subsampling; Phase T's
  wrong-domain arm);
* a positive control whose job was to prove the instrument could detect
  anything at all — Phase Q's Euler→NS was decisive precisely here;
* self-directed error search, which caught six of my own defects, three of
  them after the result was in hand.

That is **methodological** transfer, and on this record it is the only kind
that worked. Against §5's three types: content transfer failed (Phases Q–S),
strategy-as-ranking transfer had zero measured value (this section),
**frontier-selection transfer was never tested** — and the only thing that
demonstrably carried across eleven phases was experimental hygiene.

---

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

`SIMULATION` (`u/scarcity.py`). **Conditional on its model.** Two inputs are
taken from the record rather than invented: the base rate of true effects
(0.143) and the measured forecaster informativeness (0.0). Everything else is
swept.

A team faces 40 candidate hypotheses and can afford `budget / cost` decisive
tests. Findings at fixed budget, from the measured operating point:

| budget | base (measured) | halve cost per test | forecast 0 → 0.5 | both |
|---|---|---|---|---|
| **10** | 1.444 | 2.875 (**+99%**) | **5.749 (+298%)** | 5.705 |
| 20 | 2.852 | 5.733 (+101%) | 5.709 (+100%) | 5.686 |
| 100 | 5.751 | 5.740 (−0%) | 5.654 (−2%) | 5.726 |
| 1000 | 5.761 | 5.785 (+0%) | 5.745 (−0%) | 5.725 |

The model saturates above budget ≈ 20 because a 40-candidate pool contains only
~5.7 true effects; the realistic regime for a small team is the top row, where
the candidate pool vastly exceeds what can be tested.

**In severe scarcity, forecast quality dominates cost reduction by 3×.** That
is the opposite of what I expected, and it does not comfort the team, because
the measured forecast informativeness after 21 pre-registered attempts is
**zero**. The honest reading:

> The high-return lever is forecasting, and this team demonstrably does not
> have it. The achievable lever is cost per decisive test, worth roughly a
> doubling. A team that cannot forecast should buy cheap falsification, not
> better rankings — not because that is optimal, but because the optimal lever
> is not for sale.

---

## 5. Answers

### §13 — Does explicit control over meta-moves improve verified output per unit resource?

**Partly, and not through the moves the brief emphasises.** The meta-moves that
demonstrably paid: pre-registration, matched controls, positive calibration
controls, early termination of a doomed representation (Phase T retired Phase
S's `have`-dominated metric rather than extending it). The meta-move that
demonstrably did not pay: **problem/hypothesis selection**, which carried zero
information across 21 scored predictions and 3 of 3 falsified recommendations.

### §16 — Is the hypothesis weakened?

Yes, on the criteria the brief lists. *"Problem selection gives no advantage
after controlling for solvability"* — on this record, selection gave no
advantage at all, controlled or not. *"Lessons learned do not improve
subsequent decisions"* — the compressed lessons were followed 3/3 times and led
to a falsification 3/3 times.

**The lowest level at which this team obtained transferable advantage is
methodological**: how to make a test decisive, not what to test.

### §17 — What should a rational research team do when it cannot afford to try everything?

On this evidence, and stated as narrowly as the evidence supports:

1. **Do not trust your ranking of hypotheses.** Measure your own hit rate
   before you spend on it. This team's was indistinguishable from chance, and
   would not have known without pre-registering.
2. **Buy decisiveness, not coverage.** The cheapest thing that reliably
   produced value was a control that could kill a hypothesis in one run —
   Phase Q's Euler→NS calibration, Phase T's wrong-domain arm.
3. **Instrument the null.** Five of eleven phases returned falsifications, and
   they were the phases that changed what the programme did next.
4. **Expect to be your own worst reviewer.** Six defects were found by
   self-audit, three after the headline result was in hand, and two of those
   reversed the interpretation.

And the deeper version — *can that policy be learned, compressed, transferred?*
On this record the compressible part is the methodology, and it did transfer,
across eleven phases and four different subject matters. The part the brief
hoped for — a policy for choosing *what* to work on — was not learned, and this
programme has no evidence that it can be.

---

## 6. Negative results

1. **The team's directional forecasting carried no information** (Fisher
   p = 1.0000). This is the headline and it is about us.
2. **Every forward recommendation was falsified** (3/3), while being followed
   3/3 times. Compressed lessons drove the next experiment reliably and drove
   it to a null every time.
3. **One of three positive findings was retracted by the programme itself**
   (Report J, overturned by Report O).
4. **My own first analysis of §1 was wrong** and is corrected in place:
   comparing 1/9 with 10/12 compares precisions of different propositions and
   is not a test of informativeness.
5. **Most of Phase U is untestable here** (§0), including the three parts the
   brief considers most important: multi-agent team architecture,
   frontier-selection transfer across domains, and the T1–T4 access experiment.
6. **The scarcity simulation is a simulation.** Its one non-invented input is
   the measured base rate; its conclusion favours a lever this team does not
   possess.

---

## 7. What would actually test the meta-game

Stated concretely, since almost nothing here could be:

* **Frontier-selection transfer** needs ≥ 30 pre-registered problem selections
  by the same team across two domains, with outcomes scored, to get the hit
  rate above noise. This programme managed 21 predictions in 20 hours; the
  design is affordable, it just needs to be run *as* the experiment rather than
  as a by-product.
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

`u/ledger.py`, `u/forecast_ledger.json` · `u/stats.txt` · `u/accounting.txt` ·
`u/scarcity.py`, `u/scarcity.json`.

## Sources

- [Hadamard Matrix of Order 668 — Epoch AI](https://epoch.ai/frontiermath/open-problems/hadamard)
- [A Hadamard matrix of order 668 — TheoremDB](https://theoremdb.org/statements/hadamard-order-668/)
- [Constructing Hadamard matrices — John D. Cook](https://www.johndcook.com/blog/2026/08/13/constructing-hadamard-matrices/)
- [New Hadamard matrices — Ion Nechita](https://ion.nechita.net/posts/new-hadamard-matrices/)
- [Hadamard Matrix — Wolfram MathWorld](https://mathworld.wolfram.com/HadamardMatrix.html)

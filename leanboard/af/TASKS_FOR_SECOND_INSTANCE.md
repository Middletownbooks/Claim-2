# Task list for a second Claude Code instance

You have three things: Fable's harness source (`p2-ablation-harness.html`),
Fable's chat response containing P1 v0 / P3 preliminary / P2 pre-registration,
and Fable's handoff document with its numbered tasks 1–8.

You do not have the repository those were written for, and you will not get it.
Everything you need from it is reproduced in this document. Where a task below
supersedes or closes one of the handoff's numbered tasks, it says so.

Work in priority order. Stop anywhere and the work is still useful. Commit
early and often; assume your container can be reclaimed without warning.

---

## Part 0 — What has already been measured. Do not redo it.

Two measurements have been run since Fable's handoff. Both are finished. Their
results change what is worth doing, so read this section before picking a task.

### Step D — the five-transformation vocabulary is not operational

Three raters labelled eight after-boards with one of Fable's five
transformations or "none". **Cohen's κ = 0.048.** Recognition of the source
problem was 100%; agreement on the label was 20%. Three raters gave three
different labels to the same Guo–Fang–Lu after-board.

Handoff task 2 bullet 3 asked for exactly this and said "if label κ < 0.6 the
vocabulary is not operational — report that as the P3 result". It is 0.048.
**The five-transformation vocabulary is not operational. Treat that as settled.**
Do not try to rescue it by adding definitions or a sixth entry.

### L2 — the blind re-encoding diff (handoff task 2, now closed)

Five cases from Fable's P1 §1.2 (1 sensitivity, 2 cap set, 5 Kakeya, 8 Spencer,
9 Vinogradov) were re-encoded by five independent subagents, each given only its
own case, a date cutoff, and the schema. None saw Fable's encoding or the
held-out after-board. Calibration items (Banaszczyk, Bansal–Jiang, Guo–Fang–Lu)
were excluded as Fable required.

| measure | result |
|---|---|
| leading leak mechanism agrees | **2 of 5** |
| P1 mechanisms named *anywhere* in the blind table | **6 of 7** |
| `bound` agrees | 3 of 4 comparable (1 void) |
| `state` agrees | 1 of 5 |
| recognition of the superseding work | **5 of 5** |

The two leak agreements are Spencer (UNION BOUND) and Vinogradov (ITERATION
COUNT) — the two cases where the leak is visible in the algebra of the bound
itself. Every case admitting more than one reading got two different readings.

**The load-bearing finding:** 2 of 5 leading but 6 of 7 named anywhere. The two
encoders draw from the same pool of mechanisms and rank them differently. A
diagnostic that reads "the leak" reads the ranking, and the ranking does not
reproduce. In cases 1 and 2 the blind encoder *does* name a multiplicative /
product-law mechanism — attached to a constant, never to the dominant exponent
gap, which is where Fable attaches it.

**Known holes in L2, stated so you don't inherit them as facts:**
- The pre-registered third rater (provenance hidden, X/Y randomised) was never
  run. All slot marks were made by one non-blind rater. The pre-registered κ was
  **not measured**. A substitute inter-encoder κ on the leading mechanism is
  0.286 with a case-resampled 95% CI of [0.000, 0.667] at n=5 — read as
  unmeasured, not as a bound.
- Case 9 is **void through a design error**: its cutoff was set at 2011-12-31
  intending "before Wooley", but Wooley's efficient-congruencing paper is
  arXiv:1101.0574, posted **3 January 2011**, eleven months inside the cutoff.
  The two encoders were answering different questions. Date every cutoff from
  the arXiv posting, never the journal year.
- `move` was not comparable on its defining field: the schema requires
  formula-vs-existence-theorem and Fable's table has no such field.
- Fable's P1 table leaves `composition` empty in cases 1, 5, 9 and `terminal`
  empty in 5, 8, 9. 6 of 25 slot-pairs had nothing on one side.

### Corrections to P1 that are established, with the derivation

**Case 5 (Kakeya) — Fable's flagged debt was real.** P1 gives the before-bound as
"|K| ≳ q^{(n+2)/2}, later ≈q^{4n/7}", ordering them as though 4n/7 superseded
Wolff's exponent. It does not, uniformly:

    (n+2)/2 > 4n/7  ⟺  7n + 14 > 8n  ⟺  n < 14

At n=13, (n+2)/2 = 7.500 vs 4n/7 = 7.429; they meet at n=14. **At the 2008
cutoff Wolff's bound was still the best known in every dimension below 14.** No
single exponent dominated uniformly in n.

The consequence is structural, not bibliographic: the two regimes leak
differently. The blind encoder split them — UNION BOUND for Wolff's (n+2)/2 (the
bush argument double-counts incidences with no use of structure in the direction
set), FEASIBILITY THEOREM for 4n/7 (Bourgain–Katz–Tao supplies only a
qualitative sum-product exponent). **A single-regime `bound` field forces a
single leak where there are two.** That is a schema defect, and it is the first
thing task 4 below has to fix.

**Case 9 (Vinogradov) — Fable's `[K, medium confidence]` flag was warranted for
the wrong reason.** Its bound s ≳ c·k² log k is correct for the classical method.
The fault was in the cutoff date, not in Fable's recall.

**Case 8 (Spencer) — an outright `move` disagreement, and it is real
mathematics.** Fable's move is "uniform random colouring", one shot. The blind
encoder's is "colour one more point, taking the smaller Chernoff potential" — the
sequential Erdős–Selfridge derandomisation. Both reach √(n log n); they are not
the same board, and one of them has no composition step at all. If you re-encode
anything, expect this class of divergence and record which board you mean.

---

## Part 1 — The task list

### Task 1 — Verify Fable's citation layer. Do this first.

Fable tagged its own citations `[K]` = "recalled from literature and not
re-fetched this session, so verify citations before relying on them". Nothing in
that layer has been checked except case 5, where the check **found an error**
(above). The debt is known to be non-empty, and every downstream task reads
these numbers.

Check every numeric claim in P1 §1.2 (cases 1–15), §1.3 (held-out after-boards),
the negative twins N1–N8, and the controls 14–15. For each, record: claim as
written / what the source says / VERIFIED, CORRECTED, or UNVERIFIABLE, with the
arXiv id or DOI you actually fetched.

Handoff task 5 names the ones Fable thought shakiest; carry them but do not stop
there — case 5 was on that list and the error was worse than Fable expected (a
missing regime, not a wrong exponent). Specifically outstanding:

- **Case 1**: the Chung–Füredi–Graham–Seymour constant, (½ − o(1)) log n.
- **N4**: the Polak–Schrijver lower bound for Θ(C7) against ϑ(C7) ≈ 3.318.
- **Battery item O3**: that x³+y³+z³ = 114 is still open — re-check on the day
  you freeze, this one can change under you.
- **N1** Larsen–Nelson tightness of the JL dimension bound; **N2** the
  Komlós–Pach–Woeginger and Pach–Tardos tightness claims *and* the
  Matoušek–Seidel–Welzl removability claim, since N2 is offered as a
  within-problem matched pair and the pairing is the whole point; **N6** Roth
  1964 / Matoušek–Spencer 1996 for n^{1/4}; **N7** the Wang–Zahl resolution of
  R³ Euclidean Kakeya; **N8** the √(n log(m/n)) tightness.
- **Case 2**: P1 writes the Bateman–Katz bound as "n^{1+ε}", dropping the 3^n.
  Decide whether that is shorthand or an error, and fix the field either way.
- The two **reclassifications** Fable asks to be adjudicated: sphere packing
  moved from board-change to same-board control, and PCP demoted to fit-testing.
  These are arguments, not citations; adjudicate them on the record and say so.

If arXiv or a publisher is unreachable from your environment, **say the claim is
unverified rather than accepting it**. Declaring what could not be checked is
part of the deliverable. (In the environment that produced this document,
`arxiv.org`, `export.arxiv.org`, `huggingface.co`, `alphaxiv` and
`semanticscholar` were all egress-blocked and web search was the only route.
Yours may differ — test early, because it determines how much of this task is
possible.)

**Deliverable:** `CITATIONS.md`, one row per claim, plus a corrected P1 §1.2
table. Everything downstream reads the corrected table, not Fable's original.

### Task 2 — Fix and port the harness (handoff task 3)

There is a **confirmed bug** in the published harness. In `exportData`:

```js
function outcome(r, j) { j = j || r.j1; if (!j) return null; /* ... */ }
```

`exportData` calls `outcome(r, r.j2)`. When `r.j2` is absent the `j = j || r.j1`
fallback silently scores judge 2's column from **judge 1's judgement**, which
inflates inter-judge agreement toward 1 on exactly the rows where the second
judge did not run. Fix:

```js
const o2 = r.j2 ? outcome(r, r.j2) : null;
```

Port to Python as handoff task 3 specifies, carrying `BLOCKS`, `SCHEMA`, `PFMT`,
`PRIG`, `CORE`, `judgePrompt`, the arm generator (E = ABC, F = BCD), `outcome()`
and `predictions()` with its six coded rules. **Keep the six rules byte-identical
or re-freeze and say which.** Fix the bug above in the port *and* record it as a
pre-freeze defect, not a port-time change — it alters what the published
instrument would have reported, and that belongs in the write-up.

Also as Fable asks: non-repeating placebo filler (the current one cycles ~10
paragraphs, which is a recognisable tell and confounds the length match); a
different model family for at least one judge; exact arithmetic on any accepted
counterexample done in code, not by the judge. Record plainly that judges cannot
be blinded to arm — tags and field numbers leak it.

**Deliverable:** the port, a dry run against mocks reproducing the harness's
current behaviour except the bug, and a diff note listing every intentional
divergence.

### Task 3 — Replace the battery's weakest items (handoff task 1, now unblocked)

The handoff marks this "repo instance only". It is not, any more — the corpus is
attached as `battery_repo_corpus.json` alongside this document. Six items R1–R6
drawn from documented agent failures with known ground truth, in the battery's
own format `{id, type: true|false|open, statement, truth}`. Each has a
demonstrated non-zero failure rate on a real agent, which is the E10 requirement
Fable's textbook items do not meet.

Swap them in for the six battery items you expect to hit ceiling, run the pilot,
and report the per-item failure rate. If an item still ceilings, say so — a
ceiling is a measurement, and an item that nothing fails cannot separate arms.

### Task 4 — Rebuild the diagnostic on the fields that reproduce

This is the task L2 generated and the one with the most at stake.

Fable's P3 item 1 proposes replacing *de-tensorize* with **product-law
matching** — compute how the target behaves on the product construction of the
extremal family, and require the invariant to obey the same law — and flags its
own circularity: *"I derived this from the same cases I scored it on. It needs
fresh cases."*

L2 supplies the first outside evidence, and it is worse than the circularity
Fable flagged. The proposal rests on cases 1, 2 and 3. L2 covered 1 and 2, and in
**both** Fable's leading leak is a product-law argument while the independent
encoder puts something else in the leading slot and uses the multiplicative
mechanism only for a constant. (Case 5's disagreement is *not* of this kind —
Fable's leak there is a pairwise-only Cauchy–Schwarz argument — so the product-law
signature is 2 of the 3 disagreements, not 3.)

This does not make product-law matching wrong as mathematics. The Huang signing
really does change the product law of the cube spectrum, and that really is why
interlacing becomes available. It means **the diagnostic cannot be validated on
leak tables**, because the leak field is the field that does not reproduce
(2 of 5) while `bound` does (3 of 4).

So: restate product-law matching as a procedure computed from `bound` and the
extremal construction — both objective, both reproducible — with no reference to
the leak table. Then check whether it still fires on cases 1, 2, 3, and whether
it correctly fails to fire on the negative twins. You have Fable's §1.3
after-boards and §1.2 bounds, so this is fully self-contained.

Do the same for Fable's P3 item 2 (collectivize-a-union-bound has poor
specificity, fires and fails on N1, N2-general, N8). Its proposed refinement —
"does an instance in the class make the m bad events near-independent?" — is
untested and lives entirely on the negative twins, which L2 did not touch.

Fable's P3 item 3 concedes that auxiliary-witness lift "has no stated diagnostic
and fits almost anything post hoc". Either give it a diagnostic computable from
the before-board alone, or drop it. Do not leave it in the catalogue undefined.

### Task 5 — Grow the negative twins, because nothing else fixes the power

Fable states the limit itself: with ~13 positives and 8 negatives, only
near-perfect separation reaches significance, so the benchmark "is a
counterexample generator, not a rate estimator". Every other task on this list is
bounded by that.

Target ~25 negatives: cases where a surface leak of a catalogued mechanism is
**provably tight**, or where the famous fix provably does not transfer. N1, N2,
N6, N8 are the model. Prefer within-problem matched pairs like N2 (tight for
halfspaces in R⁴, removable for halfspaces in R³ and discs) — they control for
problem difficulty in a way cross-problem pairs cannot.

Every twin needs a citation verified under task 1's standard, and a one-line
statement of *which* mechanism's diagnostic would wrongly fire on it. A twin
nobody's diagnostic fires on is not a twin, it is filler.

### Task 6 — Pre-register the analysis before unblinding (handoff task 4)

Unchanged from the handoff and still un-done. Commit, before you look at any
outcome: mixed-effects logistic regression, `failure ~ A+B+C+D+E+F` with a random
intercept per problem, on the exported CSV. The harness's difference-of-
proportions intervals treat runs as independent; runs share problems, so those
intervals are too narrow.

Resolution IV: main effects are clean of two-way interactions, but two-way
interactions alias each other (defining words ABCE, BCDF, ADEF). **Do not
interpret any two-way interaction.** Power is roughly a 30-point shift at ~40
runs per factor level; smaller effects will read as null, and the write-up must
say "not powered to detect", not "absent".

### Task 7 — Start the prospective arm

Fable's L4 says it outright: *"The only fully clean estimate is prospective: log
the procedure's prediction on new arXiv board-change claims before reading the
method section."* Recognition was 100% in step D and 5 of 5 in L2. Every
retrospective case in this programme is contaminated, and no amount of cutoff
discipline fixes it — L2 proved that empirically, on encoders that were *trying*
to comply and self-reported the contamination in the leak field every time.

Set up the log: for each new arXiv posting claiming a board change, record the
before-board, the diagnostic's prediction, and a timestamp, **before** reading
the method section. Log a first batch. This will not produce a result in a day;
it produces the only instrument in this programme that can produce an
uncontaminated one, and it has to start sometime.

### Task 8 — If time remains: re-run L2 properly

L2's pre-registered κ was never measured. Re-running it is worth doing only with
all four fixes:

1. A genuine third rater, provenance hidden, X/Y order randomised.
2. A worked example per slot in the schema. Four of the five `state` divergences
   in L2 were the two encoders reading the *slot* differently, not the
   mathematics — Fable's `state` is the problem's object ("Kakeya set K ⊆ F_q^n",
   "mean value J_{s,k}"), the blind encoders' is what a partial attempt carries.
   Without worked examples that divergence will dominate any κ you compute.
3. `bound` allowed to hold multiple regimes, and `leaks` indexed by regime.
4. Cutoffs dated from arXiv postings.

Use your own encoders on fresh cases. Do **not** ask me for the five blind
encodings — reusing them would contaminate your raters with mine. The design
fixes above are safe to inherit; the encodings are not.

The schema the L2 encoders were given, reproduced so you can diff against it:

```json
{
  "case": "<short name>",
  "cutoff": "<ISO date: the encoder may use nothing published after this>",
  "target": "<the statement being attacked, in one sentence>",
  "board": {
    "state":       "<what an in-progress attempt carries>",
    "move":        "<the legal step, and whether it is a formula or needs an existence theorem>",
    "invariant":   "<what the move preserves>",
    "composition": "<why steps chain>",
    "terminal":    "<what a finished state certifies>"
  },
  "bound": "<the best result of this shape at the cutoff, as a formula>",
  "leaks": [
    {"factor": "<e.g. sqrt(log n)>",
     "mechanism": "<union bound over m items | multiplicative invariant | terminal certificate | feasibility theorem | iteration count | other>",
     "evidence": "<the step where it enters>"}
  ],
  "sources": ["<pre-cutoff citations only>"]
}
```

`heldout/<n>.json` carries the after-board in the same five slots plus the
transformation label and the superseding citation, and is read by nobody who is
scored.

---

## Part 2 — Do not do

Fable's handoff task 7 stands, and step D strengthens the second item:

- **Do not write template v3 before P2 data exists.** The v3 hypotheses are
  already encoded as harness arms.
- **Do not add a sixth transformation.** Step D measured κ = 0.048 on the five
  that exist. The catalogue's problem is not that it is too small.
- **Do not report harness results with judge κ below ~0.6** without reading
  transcripts first.
- **Do not rescue a failed prediction with an unregistered collapse.** In L2,
  prediction L2-1 failed on both halves and survives only if PARTIAL is counted
  with AGREE. It was scored as failed. Keep that standard.
- **Do not treat Fable's P1 numbers as verified** until task 1 says which ones
  are. One of the five L2 cases already produced a correction.

## Part 3 — Operational notes

These cost real time in the environment that produced this document. They may not
all apply to yours.

- **Never `pkill -f` / `pgrep -f` a pattern that appears in your own command
  line.** The pattern matches your own shell and kills it (exit 144). Use a
  bracket (`refin[e]_i4`) or kill by a PID you captured.
- **Do not read an output file while its producer is still writing.** This
  produced a wrong survivor count that had to be publicly retracted.
- **Do not let a job write its output to its own input path.** One did, truncated
  the input before reading it, and reported "0 in, 0 survive".
- **Use `git commit -F -` with a heredoc, not `git commit -m`,** whenever the
  message contains quotes.
- **Check, do not assume, what is installed.** `sympy` was absent, then present
  mid-run because a subagent installed it.
- When a result contradicts your own earlier claim, retract it in the report in
  the same words you used to assert it. The L2 report retracts one of its own
  design decisions and voids a fifth of its own sample; that is the standard.

## Part 4 — Attached

- `battery_repo_corpus.json` — six battery items R1–R6, ready to paste into the
  Battery tab's JSON box or into the port. Unblocks handoff task 1.

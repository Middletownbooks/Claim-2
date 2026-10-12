# RESULT — Task 2 step L2: blind re-encoding diff

Predictions in `PREREG_L2.md` were committed (29ea132) before any encoder ran.
The encoding diffed against is `P1_reference.md`. Numbers below are produced by
`diff_l2.py`; raw output in `DIFF_L2.txt`.

## Headline

Two independent encoders of the same before-board agree on **2 of 5** leading
leak mechanisms and on **1 of 5** `state` slots. The agreements are not spread
evenly: both leak agreements are the two cases where the mechanism is UNION
BOUND or ITERATION COUNT, the two diagnoses the bound's own algebra forces. Where
more than one reading was available, the two encoders took different ones — every
time.

This is not a finding about who is right. It is a finding about the input the P3
diagnostics consume. A diagnostic that reads "the leading leak mechanism" is
reading a field that two encoders fill differently in 3 of 5 cases.

## Protocol deviations — read before the numbers

1. **The third rater was not run.** `PREREG_L2.md` specifies that both encodings
   are shown to a rater in randomised order with provenance hidden, and that
   Cohen's κ is computed on that rater's AGREE-vs-not marks. That rater does not
   exist. Every mark in the tables below was made by me, knowing which column
   came from which encoder. **The pre-registered measurement was not taken.**
2. **Consequently L2-2 cannot be scored as written** (see below). A substitute
   inter-*encoder* κ is reported in its place and labelled as such.
3. **`move` is not comparable on its defining field.** `SCHEMA_before.md`
   requires `move` to state "whether it is a formula or needs an existence
   theorem". Fable's P1 table has no such field; all five blind encodings have
   one. The `move` marks below compare only the step named, not the
   formula-vs-existence-theorem classification, which is the part the P3
   diagnostics would actually use.
4. **6 of 25 slot-pairs have nothing on one side.** Fable's P1 table leaves
   `composition` empty in cases 1, 5, 9 and `terminal` empty in cases 5, 8, 9.
   Those are scored NC (not comparable), not DISAGREE — but the `composition`
   and `terminal` rows below rest on n=2 each and carry no weight.
5. **Fable's leak mechanisms are my coding of its prose.** The blind encoders
   tagged their own leaks with the schema's six-value vocabulary. Fable wrote
   prose. The tags in the leak table are mine, so the inter-encoder κ inherits my
   coding of one of the two columns.
6. **Case 9's `bound` is void through an error in my own design** (below).

## Slot diff

| case | state | move | invariant | composition | terminal | bound |
|---|---|---|---|---|---|---|
| 1 sensitivity | AGREE | AGREE | PARTIAL | NC | AGREE | AGREE |
| 2 cap set | PARTIAL | AGREE | PARTIAL | PARTIAL | AGREE | AGREE |
| 5 Kakeya | PARTIAL | PARTIAL | DISAGREE | NC | NC | **DISAGREE** |
| 8 Spencer | PARTIAL | **DISAGREE** | PARTIAL | AGREE | NC | AGREE |
| 9 Vinogradov | PARTIAL | AGREE | AGREE | NC | NC | *VOID* |

| slot | AGREE | PARTIAL | DISAGREE | n | agree rate |
|---|---|---|---|---|---|
| state | 1 | 4 | 0 | 5 | 0.20 |
| move | 3 | 1 | 1 | 5 | 0.60 |
| invariant | 1 | 3 | 1 | 5 | 0.20 |
| composition | 1 | 1 | 0 | 2 | 0.50 |
| terminal | 2 | 0 | 0 | 2 | 1.00 |
| bound | 3 | 0 | 1 | 4 | 0.75 |

### The `state` divergence is systematic, and it is a schema divergence

Four of the five `state` marks are PARTIAL for the same reason, in the same
direction. `SCHEMA_before.md` defines `state` as *"what an in-progress attempt
carries"*. The blind encoders answered that question — case 5's state is "a
partial counting certificate", case 8's is "a partial colouring carried with a
Chernoff-type potential", case 9's is "a mean-value bound at a given depth".
Fable answered a different one: its `state` is the problem's object ("Kakeya set
K ⊆ F_q^n", "colouring of n points with n sets", "mean value J_{s,k}").

Nothing here is mathematically wrong on either side. But it means `state`
agreement is low for a reason that has nothing to do with the mathematics of the
board, and it means the word "agreement" is doing two jobs in this diff. A single
AGREE/PARTIAL/DISAGREE scale cannot separate *the encoders read the schema
differently* from *the encoders read the mathematics differently*. The schema
needs a worked example per slot before an L2 rerun is worth anything.

### The one outright `move` disagreement is real mathematics

Case 8. Fable's move is "uniform random colouring" — one shot. The blind
encoder's move is "colour one more point, taking the smaller potential" — the
sequential Erdős–Selfridge derandomisation. These are different games with
different legal steps. Both reach √(n log n); they are not the same board. That
matters for the P3 diagnostics, which ask what the move preserves under
composition: one of these boards has no composition at all.

## Leak table

| case | P1 leading mechanism | blind leading mechanism | match |
|---|---|---|---|
| 1 sensitivity | MULTIPLICATIVE INVARIANT | ITERATION COUNT | no |
| 2 cap set | MULTIPLICATIVE INVARIANT | TERMINAL CERT TOO WEAK | no |
| 5 Kakeya | UNION BOUND | FEASIBILITY THEOREM | no |
| 8 Spencer | UNION BOUND | UNION BOUND | **YES** |
| 9 Vinogradov | ITERATION COUNT | ITERATION COUNT | **YES** |

- leading-mechanism agreement: **2 of 5**
- P1 mechanisms named *anywhere* in the blind encoder's table: **6 of 7**
- cases where P1's whole mechanism set sits inside the blind set: **4 of 5**

That gap between 2/5 and 6/7 is the most useful thing in this diff. The two
encoders draw from the same pool of mechanisms and largely name the same ones.
They rank them differently. A diagnostic that fires on "the leak" fires on the
ranking, and the ranking is what fails to reproduce.

Concretely, in cases 1 and 2 the blind encoder *does* name MULTIPLICATIVE
INVARIANT — but attaches it to a constant (the (½−o(1)) in case 1, the C in case
2), never to the dominant exponent gap. Fable attaches it to the dominant gap in
both. Same word, different factor, opposite consequence for any diagnostic that
reads it.

### Why the two agreements are the two that agree

Case 8: the bound literally contains a per-set budget of 1/n, and the matching
Ω(√n) lower bound was already known at the cutoff, so there is essentially one
available reading. Case 9: the classical recursion contracts geometrically and
the round count is on the page. Both are cases where the leak is visible in the
algebra of the bound itself. The three disagreements are the three cases where
diagnosing the leak requires a judgement about *why* the method stops, which is
exactly the judgement the P3 diagnostics are supposed to automate.

### Inter-encoder κ (substitute measurement, not the pre-registered one)

On the leading mechanism, 5 items, 6 categories:

    observed agreement  p_o = 0.400
    chance agreement    p_e = 0.160
    kappa                   = 0.286
    case-resampled 95% CI   = [0.000, 0.667]

The interval spans nearly the whole admissible range. **Read this as unmeasured,
not as a bound of 0.286.** Five cases cannot estimate a κ. It is reported because
Fable's L2 specification asked for a κ, and because reporting "we could not
measure it at n=5" is the actual answer.

## Scoring the four pre-registered predictions

**L2-1 — "Slot agreement is lowest on the leak table and highest on `state`."
FAILED, on both halves.**
State agrees at 0.20; the leak table agrees at 0.40. State is not highest — it
ties `invariant` for lowest. The prediction survives only under a collapse I did
not pre-register (PARTIAL counted with AGREE: state then has 0 disagreements and
the leak table has 3). I am not taking that rescue. The reason for the failure is
the schema divergence in §"The `state` divergence": I assumed `state` was close
to forced by the problem statement, and it is — but only once both encoders agree
what the slot is *for*, which they did not.

**L2-2 — "κ on the AGREE-vs-not collapse is below 0.6." NOT EVALUABLE.**
The rater whose marks the κ is computed from was never run (deviation 1). The
substitute inter-encoder κ is 0.286 with a CI of [0.000, 0.667], which neither
confirms nor refutes the prediction. Recorded as not taken.

**L2-3 — "At least one of the two flagged debts (5, 9) shows DISAGREE on
`bound`." HELD.**
Case 5 disagrees, and the disagreement is resolvable in the blind encoder's
favour. Fable's P1 gives the before-bound as "|K| ≳ q^{(n+2)/2}, later ≈q^{4n/7}",
ordering the two as though 4n/7 superseded (n+2)/2. It does not, uniformly:

    (n+2)/2 > 4n/7  ⟺  7n + 14 > 8n  ⟺  n < 14          [DERIVED HERE]

| n | (n+2)/2 | 4n/7 | better |
|---|---|---|---|
| 3 | 2.500 | 1.714 | Wolff |
| 13 | 7.500 | 7.429 | Wolff |
| 14 | 8.000 | 8.000 | equal |
| 15 | 8.500 | 8.571 | 4n/7 |
| 30 | 16.000 | 17.143 | 4n/7 |

At the 2008-02-29 cutoff, Wolff's bound remained the best known in every
dimension below 14. Fable's `bound` field collapses two regimes into one and
loses the fact that no single exponent dominated uniformly in n. Fable flagged
this exact line as a verification debt; the debt was real and is now paid.

The consequence for P3 is larger than the citation. The blind encoder splits the
leak accordingly — UNION BOUND for Wolff's (n+2)/2 (the bush argument
double-counts incidences with no use of structure in the direction set),
FEASIBILITY THEOREM for the 4n/7 (Bourgain–Katz–Tao supplies only a qualitative
sum-product exponent). Those are two different leaks in two different regimes. A
single-regime `bound` field forces a single leak, and the encoder then has to
pick one. That is a defect in the schema, not only in this encoding.

**L2-4 — "Recognition is near-universal." HELD, 5 of 5.**
Every encoder named the superseding work unprompted and dated it: Huang
(1907.00847, one day past the cutoff), Croot–Lev–Pach and Ellenberg–Gijswijt,
Dvir (0803.2336), Spencer's *Six Standard Deviations Suffice*, and both Wooley
and Bourgain–Demeter–Guth. As pre-registered, this is reported as a limit on the
whole design: **"use only pre-cutoff sources" is not a request an encoder can
honour.** All five self-reports localise the contamination the same way — clean
on state/move/invariant/composition/terminal, and admitted on `leaks`. Case 1's
encoder put it best, quoted in full in `blind_case1_sensitivity.md`:

> A strictly cutoff-blind assessment would have had to hedge this as "conjectured
> to be an artifact" with less certainty, since no one before 1 July 2019 had a
> proof that a fundamentally different method could do better — that was exactly
> the open question.

Note the direction: contamination is concentrated in `leaks`, which is precisely
the field the leading-mechanism diff measures and precisely the field the P3
diagnostics read. L2 relocates contamination from the label to the encoding, as
Fable intended; it does not remove it, and it has landed on the load-bearing
field.

## Case 9 is void, through my error, not the encoders'

`PREREG_L2.md` set case 9's cutoff at 2011-12-31, intending "before Wooley".
Wooley's efficient-congruencing paper reached arXiv as 1101.0574 on **3 January
2011**, eleven months inside that cutoff. So Fable (describing the pre-2011
classical state, s ≳ c·k² log k) and the blind encoder (describing the state at
the date I actually specified, s ≥ k(k+1)) are answering different questions.
**Case 9's `bound` field measures my dating error, not encoder disagreement.**

Two things follow. Fable's own `[K, medium confidence]` flag on that line turns
out to concern a claim that is correct for the classical method — the flag was
warranted for the wrong reason, and the fault is mine. And the blind encoder
handled the ambiguity better than the instruction deserved: it did not silently
pick a reading, it flagged the conflict up front and reported both, on the
grounds that conflating the arXiv and Annals dates "would misdate the real gap".
Case 9's leak agreement (ITERATION COUNT on both sides) is unaffected, since both
encoders diagnose the classical recursion.

Any L2 rerun must date cutoffs from arXiv postings, not journal years. That is a
one-line fix and it invalidated one fifth of this design.

## What this does to Fable's P3 proposals

Fable's P3 item 1 proposes replacing *de-tensorize* with **product-law matching**,
and states the circularity itself:

> Caveat: I derived this from the same cases I scored it on. It needs fresh
> cases.

L2 supplies the first outside evidence. Fable's proposal rests on cases 1, 2 and
3; cases 1 and 2 are in this sample. In **both**, Fable's leading leak is a
product-law argument — case 1: "the unsigned spectrum of Q_n is n−2k, additive
under Cartesian product"; case 2: "the invariant composes additively, while the
target is supermultiplicative under products" — and in **both**, the independent
encoder puts something else in the leading slot and uses the multiplicative
mechanism only for a constant.

(Case 5's disagreement is *not* of this kind — Fable's leak there is a
pairwise-only Cauchy–Schwarz argument — and it is confounded with the two-regime
`bound` error. So the product-law signature is 2 of the 3 disagreements, not 3.)

What this shows, precisely: the product-law reading of these boards is
**encoder-specific**. It is present in the encodings Fable produced and absent
from the leading position in two independent encodings of the same two cases.
That does not make product-law matching wrong as mathematics — the Huang signing
really does change the product law, and that really is why interlacing becomes
available. It means the diagnostic cannot be validated on leak tables, because
the field it reads is the field that does not reproduce. Either the diagnostic
must be computed from the bound and the extremal construction directly (both of
which are objective, and both of which *did* reproduce: `bound` agrees 3 of 4
comparable), or its validation is circular in a second way Fable did not flag.

Fable's P3 item 2 (collectivize-a-union-bound has poor specificity) is untouched
by L2: case 8 is the one case where both encoders agree on UNION BOUND, and it is
also the case Fable itself scores as correct. The specificity question lives on
the negative twins (N1, N2, N8), which L2 did not re-encode.

## Standing

- Reproducible: `python3 diff_l2.py` regenerates every number in this report.
- The pre-registered κ was not measured. That is a hole in this result, not a
  result.
- Two of four predictions held, one failed, one was not evaluable. One of five
  cases was voided by my own design error.
- What L2 establishes: two encoders of the same before-board disagree, and they
  disagree in the leak field, which is the field the P3 diagnostics read.
- What L2 does not establish: that either encoding is correct. Case 5 is the one
  place where the diff was resolvable against an objective fact, and there the
  blind encoder was right.

## Next, in order

1. Re-run the slot diff with a genuine third rater, provenance hidden, X/Y
   randomised — the measurement this step was supposed to take.
2. Before that, give `SCHEMA_before.md` a worked example per slot. The `state`
   divergence is a schema defect and will otherwise dominate any κ.
3. Allow `bound` to hold multiple regimes, and `leaks` to be indexed by regime.
   Case 5 shows a single-regime field forces a wrong choice.
4. Date all cutoffs from arXiv postings. Re-set case 9's cutoff to 2010-12-31 and
   re-run it.
5. Open against Fable's P3 item 1: compute product-law matching from `bound` and
   the extremal construction, not from the leak table, and see whether it still
   fires on cases 1, 2, 3.

# PREREG — Task 2, step D: is the transformation vocabulary operational?

Written and committed before any rater runs.

## The question

The P3 catalogue names five board transformations. The handoff sets the test:
two independent raters label each held-out after-board with one of the five or
"none"; **if inter-rater kappa < 0.6 the vocabulary is not operational, and that
is the P3 result.**

## The five labels (verbatim, as given to raters)

1. DE-TENSORIZE — the invariant was multiplicative under the product
   construction generating hard instances, and was replaced by one that averages.
2. AUXILIARY-WITNESS LIFT — "state S has property P" replaced by "there exists
   an auxiliary object w attached to S with property P'", w rebuilt each step
   rather than transported.
3. WORK MOVED between the step invariant and the terminal certificate.
4. COLLECTIVIZE A UNION BOUND — per-item control plus a union over m items
   replaced by joint control on the collection.
5. FORMULA-IZE THE MOVE — a constrained move needing a feasibility theorem
   replaced by an unconditionally defined operator.
6. NONE — no listed transformation describes what changed.

## Cases

Eight after-boards. Three are **calibration only and are excluded from scoring**
because they generated the taxonomy (Banaszczyk, Bansal–Jiang, Guo–Fang–Lu).
Five are scored. One scored case (sphere packing) is a declared **same-board
control**: the board is the Cohn–Elkies linear program and the later work
supplied a certificate for it, so the correct label is NONE. A rater who labels
it with one of the five is over-fitting the vocabulary.

## Raters

Two subagents, each given the after-board description and the six labels, with
no sight of this file, of each other, or of the catalogue's provenance. They are
not told which cases are calibration or control.

## Declared predictions

**D1. kappa < 0.6 on the five scored cases.** Confidence: moderate-high. The
five transformations were induced from three boards all in discrepancy theory;
there is no reason they should partition transformations in algebra, analysis
and combinatorics.

**D2. NONE is the modal label across scored cases.** Confidence: moderate.

**D3. At least one rater assigns a non-NONE label to the sphere-packing
control.** Confidence: moderate. This is the over-fitting probe.

**D4. Transformations 3 and 5 attract almost no labels outside calibration.**
Confidence: moderate. The handoff predicts they are artefacts of the Komlos
trio; this tests it. Note the handoff advises shrinking the catalogue on this
basis — if D4 holds, that advice is supported by a measurement rather than by
inspection.

## Limits declared

n = 5 scored cases is very small; kappa on five items has enormous variance and
a single disagreement moves it a long way. This test can support "the vocabulary
is not operational" if agreement is poor, but cannot establish that it IS
operational if agreement is good. Stated asymmetrically on purpose.

Raters are contaminated: they will recognise most of these results. Recognition
helps them identify what changed; it does not obviously help them agree on which
of six labels to apply, which is what is being measured.

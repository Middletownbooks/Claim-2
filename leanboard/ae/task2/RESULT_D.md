# Task 2 step D — RESULT: the transformation vocabulary is not operational

Two blind raters, eight after-boards, six labels. Pre-registered before either
ran. The handoff's criterion: **kappa < 0.6 means the vocabulary is not
operational, and that is the P3 result.**

## Headline

**Cohen's kappa = 0.048 on the five scored cases** (raw agreement 1 of 5),
bootstrap 95% interval [−0.32, 0.38]. That is chance.

| case | rater A | rater B | agree |
|---|---|---|---|
| sensitivity | 1 de-tensorize (c2) | 6 none (c3) | no |
| finite-field Kakeya | 2 auxiliary-witness (c3) | 6 none (c4) | no |
| cap set | 2 auxiliary-witness (c3) | 1 de-tensorize (c3) | no |
| sphere packing (control) | 6 none (c4) | 5 formula-ize (c4) | no |
| Vinogradov | 4 collectivize (c3) | 4 collectivize (c4) | **yes** |

## All four pre-registered predictions held

| | prediction | outcome |
|---|---|---|
| D1 | kappa < 0.6 | **HELD**, 0.048 |
| D2 | NONE modal among scored labels | **HELD**, counts {1:2, 2:2, 4:2, 5:1, 6:3} |
| D3 | at least one rater over-fits the control | **HELD**, B labelled sphere packing FORMULA-IZE at confidence 4 |
| D4 | transformations 3 and 5 attract almost no labels | **HELD**, 1 of 10 scored labels |

## Recognition cannot explain the disagreement away

This is the part that makes the result hard to dismiss. The recognition probe
came back **5 of 5 on scored cases for both raters** — both named Huang,
Dvir, Croot–Lev–Pach/Ellenberg–Gijswijt, Viazovska and Wooley correctly and
confidently.

So: **recognition 100%, agreement 20%.** The raters understood the mathematics
and still could not agree which label applied. Contamination is not the
explanation; the labels are.

## The sharpest finding: three raters, three labels, on the founding case

Guo–Fang–Lu is the case the taxonomy was induced from, and whose mechanism this
programme called its most transferable object:

* originating instance (audit of the full paper): **DE-TENSORIZE**
* rater A: **WORK MOVED** (3)
* rater B: **AUXILIARY-WITNESS LIFT** (2)

Three independent readings, three different labels, on the single case where
the vocabulary should be strongest. A low kappa on unfamiliar cases would be
weak evidence; disagreement here attacks the catalogue at its best point.

## The vocabulary does not merely fail to discriminate — it misleads

Rater B labelled **cap set as DE-TENSORIZE**, reasoning that a multiplicative
Fourier/density invariant was replaced by slice rank as a "sum-over-slices"
quantity. Independently, and without seeing any of this, Fable's P3 states that
cases of this shape run **the opposite way**: progress required an invariant
that *is* multiplicative, because the target quantity is supermultiplicative.

So a confident rater applied the catalogue's best-supported entry in the wrong
direction. That is worse than a vocabulary that fails to fire.

## Independent convergence with Fable's P3

Reached separately — Fable had no sight of this experiment, and it had not run:

| finding | this experiment | Fable's P3 |
|---|---|---|
| transformations 3 and 5 are artefacts of the Komlos trio | D4 held, 1 of 10 labels | "I suspect both are artefacts of the Komlós trio" |
| auxiliary-witness lift has near-zero discriminating power | used twice on scored cases, disagreed both times | "fits almost anything post hoc … near-zero discriminating power" |
| de-tensorize is mis-shaped | B applied it backwards on cap set | "de-tensorize has the wrong shape as stated" |

Two methods, one conclusion. **The catalogue should shrink, and the handoff's
advice to do so is now backed by a measurement rather than by inspection.**

## Limits, declared in advance and still binding

* n = 5 scored cases. Kappa on five items has enormous variance; the interval
  [−0.32, 0.38] includes both "worse than chance" and "weakly positive". The
  test was declared asymmetric on purpose: it can support *not operational*,
  and could not have established *operational*.
* One agreement out of five could be luck. The result does not rest on the
  point estimate alone but on its coherence with the founding-case
  disagreement, the backwards application, and Fable's independent arrival at
  the same three conclusions.
* **My calibration column is compromised by my own construction error**, logged
  before rater B returned: the three calibration items are static board
  descriptions, not before/after contrasts, so the labelling task is ill-posed
  for them. Their agreement figure (1 of 3) is reported and not argued from.

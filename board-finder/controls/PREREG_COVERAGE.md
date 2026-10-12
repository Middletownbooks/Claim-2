# Pre-registration: second rater on T3's coverage column

Written and committed **before** the rater is asked. The hypothesis under test is
not whether T3 is a good screen — that is arm 3 — but whether **T3's coverage is a
property of the boards or a judgement of mine**.

## Why this arm exists

`board-finder/t3_coverage.json` records `{"applies": 3, "does_not": 3, "of": 6}`,
and its own `assessed_by` field says: *"this session, single rater, with hindsight
of every after-board."* That is the signature this programme flags elsewhere
(D23, D27: an item I chose, scored by the person who chose it). The file names its
own remedy — *"a second rater on the coverage column alone … two categories, six
items, and it is cheaper than any other test outstanding"* — so it is run.

## What the rater gets, and what is withheld

Given, per item: the goal, the incumbent (degrading) invariant, the move. Six items
in the order 02, 04, 08, 09, 13, K1-to-K3 — **not** my order, so the 3/3 split is not
visible as a block.

Withheld:
- my classification of any item;
- the phrase *"(rounds) × (cost per step)"* and the word ACCUMULATION — the rater
  gets **T3's original wording**, before the decline-clause was patched in, and must
  find for itself that some boards have no scale for a threshold to sit on;
- the after-boards (the conserved invariant that resolved each item), so no item can
  be classified by recognising its resolution;
- the existence of a 3/3 split, or any count.

Permitted: "the question is not well-posed on this board." The rater is told this is
an allowed answer. Forcing a threshold where none exists is the failure mode the
whole coverage question is about, so a forced choice would test nothing. The rater
is **not** told what such boards have in common.

## Predictions

| # | prediction |
|---|---|
| B-1 | the rater declines to name a scale parameter on **02-cap-set**, **09-vinogradov** and **13-pcp** |
| B-2 | the rater names a scale parameter on **04-kadison-singer** (the bound δ on ‖v‖²) and **08-spencer** (the discrepancy t being certified) — wording may differ, the quantity may not |
| B-3 | on **K1-to-K3** the rater names the side C of the target cube |
| B-4 | the likeliest single disagreement is **09-vinogradov**: k in J_{s,k} looks like a scale parameter, and a rater may read min{k : …} as a threshold. If exactly one item flips and it is this one, I predicted the flip; if exactly one flips and it is another, I did not |
| B-5 | the rater's reason for each *declined* item cites the absence of a scale parameter — not, say, unfamiliarity with the board |

## Failure conditions, stated in advance

- **Agreement ≤ 4/6** → the coverage column is a judgement, not a measurement.
  `t3_coverage.json`'s "3 of 6" must then be reported as *one rater's reading*, and
  the decline-clause in PROMPT.md stands on the weaker footing of being merely
  permissive rather than corrective.
- **A different three decline** → the dichotomy (threshold-at-initialisation vs
  cost-per-round) is mine and not the boards'. That is the worse outcome of the two,
  and it does not become better by my re-deriving it afterwards.
- **6/6 agreement** is the weakest interesting result, not the best: two raters
  applying the same recent training to six well-known boards can agree for reasons
  that have nothing to do with the boards. It is recorded as consistency, not truth.

## What this arm cannot show

It cannot show T3 is a useful screen. A screen can be perfectly well-defined on
three boards and tell you nothing on any of them. That is arm 3's question, and this
arm's result must not be quoted for it.

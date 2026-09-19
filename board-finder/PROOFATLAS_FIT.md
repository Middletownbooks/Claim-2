# What ProofAtlas can and cannot feed the board-search instrument

Companion to `leanboard/ag/PROOFATLAS_CATALOGUE.md`, which handles **problem selection**.
This file answers a different question: once a problem is selected, **can ProofAtlas fill
the fields the instrument consumes?** Read off the reader's guide
([Moatazg/proofatlas-notes](https://github.com/Moatazg/proofatlas-notes), compiled
2026-09-13) and the catalogue's own findings. Nothing here was checked against the live
site, which is egress-blocked from this container.

## Two artifacts, and the overlap is not knowable from either

* `/open-problems/` — **482+ rank-ordered cards**, four sections each: EXACT STATEMENT, WHY
  IT MATTERS, STATUS, SOURCES. No routes, no tasks. An encyclopedia.
* `/collaboration/` — **268 workspaces** with argument maps, typed route graphs, open
  obligations, eliminated routes, and three-part tasks. A research record.

The catalogue already tested and **refuted** the idea that the workspaces are a ranked
prefix of the problem list: expanding ranks 200, 250, 300 and 400 gives the same four
sections and no routes. So the two lists are separate artifacts, whether a given problem
has both is answerable only by checking for a matching slug, and **rank predicts nothing
about it**. Any pipeline that assumes the 268 are the top 268 is building on a refuted
premise.

## The instrument's input block, field by field

```
PROBLEM:            <one line>
BEST KNOWN BOUND:   <the bound as it stood, with its source>
BEST KNOWN LOWER BOUND OR CONSTRUCTION: <what the truth is known to be at least>
HOW THE BOUND IS PROVED: <two or three sentences, mechanism only>
```

| field | ProofAtlas | verdict |
|---|---|---|
| PROBLEM | EXACT STATEMENT, on both artifacts, in three registers | **supplied, cleanly** |
| BEST KNOWN BOUND | not a field. STATUS says *whether* partial results exist (`Open · subcases solved`), not what they are; SOURCES name papers to read | **partial — requires reading the cited source** |
| BEST KNOWN LOWER BOUND OR CONSTRUCTION | **not a field anywhere** | **absent** |
| HOW THE BOUND IS PROVED | not a field. Routes are *prospective* — paths forward — not the mechanism of the incumbent bound. Eliminated routes are the nearest thing | **absent as metadata** |

**One of four fields is supplied.** And the two absent ones are exactly the screen's two
inputs: `tight_to_constant` needs the bound/construction *pair*, and `move_kind` needs the
incumbent proof's mechanism. Neither is derivable from ProofAtlas metadata; both require
reading the sources it cites.

**So ProofAtlas lowers the cost of *selection*, not of *encoding* — and encoding is the
bottleneck.** In the protocol tree the screen is NOT APPLICABLE on 15 of 17 items for want
of a filled field, and D40 records the consequence: because only 2 items have both inputs,
the screen is currently insensitive to the fact that one of those inputs does not reproduce
between raters (κ = 0.430). Feeding it more *problems* does not fix that. Feeding it more
*filled before-boards* does, and changes the number — which is P-28, registered.

## Three things worth mining, in order

1. **The eliminated-routes slice (3% of lines, tagged as such).** This is the nearest thing
   in the wild to the `leak` field the taxonomy is read off, and it is before-board by
   construction — a recorded dead end is a leak someone already found. It is also the slice
   the reader's guide singles out as irreproducible from scratch. Highest-value slice for
   this instrument, and it is small enough to read.
2. **Edges labelled *depends on missing premise*.** Structurally this is where T1's
   restatement trap lives: a step resting on an unproved premise is exactly where an
   invariant can turn out to be equivalent to the conjecture. Running T1 on nodes carrying
   that label is a cheap, well-posed test with a real failure mode.
3. **The three-part task shape** — target, suggested move, constraint. That is nearly the
   instrument's own proposal format, so a prepared task can go into step 1 close to
   verbatim, with the constraint doubling as the kill test's starting point.

## Two hazards, one of them new

**A contamination channel the recognition probe does not catch.** The corpus is largely
machine-generated. This programme's blinding assumes a respondent has not seen the
after-board, and measures that with 6(c), *"do you recognise this problem?"*. That question
does not cover the new case: a respondent may be reading a **route produced by a model
sharing its own training**, so item and rater are not independent, and recognising the
*problem* is not the same as having the *route* already in prior. The probe needs a second
field for ProofAtlas-sourced items — *does this route read like something you would have
produced?* — or the blinding claim does not hold for them. Cheap to add, and it must be
added before any ProofAtlas item enters the scored set, not after.

**Evidence labels are internal.** "Accepted in ProofAtlas" is an editorial status, and a
Lean check settles the named declaration at the named commit, not replication, priority, or
whether the formal statement matches the informal conjecture. Anything sourced from here
enters the citations ledger **below SEARCH tier**, with `basis` saying it is a secondary,
machine-curated claim. Nine claimed advances, all of them counterexamples, constant
improvements, or formalizations of known arguments — not one a conjecture resolved.

## The cheapest experiment this suggests

Run **step 2 alone** — the leak table, one row per log/dimension/iteration/union factor,
each with a *named* mechanism — on k ProofAtlas workspaces, and report the
**MECHANISM UNKNOWN rate**. That rate is a number, it has a pre-registrable failure
condition, and it measures the thing that actually matters here: whether the site's
argument-development prose (83% of the corpus) supports mechanism extraction at all, or
only supports restating the problem. If the rate is high, ProofAtlas is a selection layer
for this programme and nothing more, and that is worth knowing before anyone builds a
pipeline on it.

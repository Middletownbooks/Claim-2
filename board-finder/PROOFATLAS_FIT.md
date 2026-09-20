# What ProofAtlas can and cannot feed the board-search instrument

Companion to `leanboard/ag/PROOFATLAS_CATALOGUE.md`, which handles **problem selection**.
This file answers a different question: once a problem is selected, **can ProofAtlas fill
the fields the instrument consumes?** Read off the reader's guide
([Moatazg/proofatlas-notes](https://github.com/Moatazg/proofatlas-notes), compiled
2026-09-13) and the catalogue's own findings. Nothing here was checked against the live
site, which is egress-blocked from this container.

> **Checked since, against the live payload.** The v16 ranking JSON is now in hand as
> `playability/ranking_v16.json` (499 records). `playability/RANKING_FIT.md` tests this
> file's claims against it: the registered workspace-allocation test is **settled at
> n=123** (density falls monotonically 54% → 12% with rank — neither a prefix nor a
> scatter), and the "one of four fields is supplied" verdict is **confirmed and
> sharpened** (row 2 is *absent*, not partial; 0 of 499 records describe the incumbent
> mechanism).

## Two artifacts, and the overlap is not knowable from either

* `/open-problems/` — **482+ rank-ordered cards**, four sections each: EXACT STATEMENT, WHY
  IT MATTERS, STATUS, SOURCES. No routes, no tasks. An encyclopedia.
* `/collaboration/` — **268 workspaces** with argument maps, typed route graphs, open
  obligations, eliminated routes, and three-part tasks. A research record.

**How much of this is actually seen: the bottom ten of `/collaboration/`, about twenty
`/open-problems/` cards, and four expanded cards at 200 / 250 / 300 / 400.** Roughly 41 of
482+ on one list and 10 of 268 on the other. Every structural claim below is a claim about
the *format*, which repeats identically across everything seen; no claim about *membership*
is supported by a sample that size.

In particular, one inference wants narrowing — and it is the catalogue's, so it is offered
here rather than edited there. Expanding ranks 200, 250, 300 and 400 showed the same four
sections and no routes, and that was read as refuting the idea that the workspaces are a
rank-ordered prefix of the problem list. It does not refute it. An `/open-problems/` card
and a `/collaboration/` workspace are **different pages**; a problem could have a workspace
and still have a card that shows no routes, because the card is not where routes live. What
the four cards establish is that `/open-problems/` has a **uniform format** and is a
separate artifact — which is worth having, and is less than was claimed. **Problems may
well appear on both lists**, and the sample cannot say otherwise.

The allocation question stays open, and it is testable **with data already in hand**, no
full lists needed: take the ten `/collaboration/` workspaces already picked, and look up
each one's rank on `/open-problems/`. If the ten scatter across the range, allocation is not
by rank and the sweet-spot reasoning is dead on direct evidence. If they cluster in a band,
that band is the target zone and the original hypothesis was right after all. Ten lookups,
one decisive answer, and the sample for it is already collected.

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

## Tractability against competition — and for this workstream they do not trade off

The two lists differ on both axes at once: the research list carries routes, prepared tasks
and recorded dead ends (more tractable) and is the advertised surface that agents are
pointed at (more competitive); the 482+ list is an encyclopedia, so higher encoding cost
and more genuine neglect. Weighing those against each other is the right call for a
workstream whose deliverable is a **result** — there, another agent getting there first is
a total loss, and neglect is worth paying encoding cost for.

**For board-harvesting the weighing inverts, and this is the part worth carrying.** The
instrument does not consume a solution; it consumes an incumbent mechanism and a record of
what leaked. Other agents' failures are not competition for that — they are the input. A
workspace that many agents have already worked has *more* recorded dead ends, which is
precisely the 3% slice named above, and a heavily-worked workspace is therefore a **better**
harvesting target, not a contested one. Competition is an asset here and a cost there.

So do not pick one list for both workstreams. Harvest before-boards where the work is
thickest; claim results where it is thinnest.

A usable proxy for how thick the work is, readable off the site with no reasoning required:
**investigation lines per workspace** — the reader's guide gives ~2,900 as the average and
Erdős–Hajnal at 24,107. High line count plus a populated eliminated-routes tag is the
harvesting signal; low line count is the neglect signal. Both are counters, not judgements,
and they point at different lists.

## The cheapest experiment this suggests

Run **step 2 alone** — the leak table, one row per log/dimension/iteration/union factor,
each with a *named* mechanism — on k ProofAtlas workspaces, and report the
**MECHANISM UNKNOWN rate**. That rate is a number, it has a pre-registrable failure
condition, and it measures the thing that actually matters here: whether the site's
argument-development prose (83% of the corpus) supports mechanism extraction at all, or
only supports restating the problem. If the rate is high, ProofAtlas is a selection layer
for this programme and nothing more, and that is worth knowing before anyone builds a
pipeline on it.

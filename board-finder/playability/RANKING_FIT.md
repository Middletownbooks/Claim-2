# The live ranking against `PROOFATLAS_FIT.md` — one registered question settled, one claim confirmed

*`PROOFATLAS_FIT.md` was written from the reader's guide
([Moatazg/proofatlas-notes](https://github.com/Moatazg/proofatlas-notes)) and says
plainly: "Nothing here was checked against the live site, which is egress-blocked
from this container." The v16 ranking payload is now in hand as
`ranking_v16.json` — 499 records, full field structure. This file checks that
document's claims against it. Two hold, one is settled, and one number is new.*

## 1. The allocation question — settled, and the answer is "both"

`PROOFATLAS_FIT.md` §"Two artifacts" registers a decisive cheap test:

> "take the ten `/collaboration/` workspaces already picked, and look up each one's
> rank on `/open-problems/`. If the ten scatter across the range, allocation is not
> by rank and the sweet-spot reasoning is dead on direct evidence. If they cluster
> in a band, that band is the target zone."

The records carry a `researchWorkspaces` field. **123 of 499 top-500 problems have
at least one linked workspace**, so the test runs at n=123 rather than n=10.

```
rank band   with workspace
  1- 50:  27/50  54.0%  ###########################
 51-100:  21/50  42.0%  #####################
101-150:  11/50  22.0%  ###########
151-200:  14/50  28.0%  ##############
201-250:  11/50  22.0%  ###########
251-300:  10/49  20.4%  ##########
301-350:   9/50  18.0%  #########
351-400:   7/50  14.0%  #######
401-450:   7/50  14.0%  #######
451-500:   6/50  12.0%  ######
```

**Neither branch of the registered prediction is right, and the real answer is more
useful than either.** Workspaces are not a rank-ordered prefix — rank 482 has one,
and ranks 3, 7 and 9 do not. But they do not scatter uniformly either: density
falls monotonically from 54% in the top fifty to 12% in the bottom fifty, a **4.5×
gradient**, with a clear break after rank 100.

So the correction to `PROOFATLAS_FIT.md` is: the four expanded cards at 200/250/300/400
showing no routes were **weak evidence read as strong**. That document already
conceded the inference was over-claimed — it is over-claimed in the other direction
too. Allocation *is* rank-driven; it is simply not a cutoff.

Operationally this vindicates the harvesting/claiming split that document ends on,
and puts a number on it: **the top 100 is where recorded dead ends will be thickest
(48% workspaced), the bottom 150 is where genuine neglect lives (13%).**

**One caveat, and it is real.** `researchWorkspaces` is the *ranking's* linkage to a
workspace, not a scrape of `/collaboration/`. The guide gives 268 workspaces total;
123 appear here. Whether the other 145 sit below rank 500 or are simply unlinked is
not answerable from this payload. The gradient is measured on what the ranking
chose to link, and a linkage policy correlated with rank would produce this shape
without any underlying allocation effect. **Treat the gradient as established for
`researchWorkspaces`, and as strongly suggestive but not proven for `/collaboration/`.**
The `scopeRelation` breakdown of the 127 links: 102 `same_canonical_problem`,
14 `workspace_special_case`, 7 `workspace_stronger_formulation`,
4 `workspace_contains_exact_target`.

## 2. "One of four fields is supplied" — confirmed, and sharpened

The instrument's input block wants four fields. `PROOFATLAS_FIT.md` judged one
supplied, one partial, two absent, from the card format. Against the live schema:

| instrument field | live schema | verdict |
|---|---|---|
| `PROBLEM` | `exactTarget`, 499/499 non-null, plus `readerQuestion` in plain register | **supplied, cleanly** — as claimed |
| `BEST KNOWN BOUND` | no field. `statusQualification` is the nearest | **absent** — *worse* than the "partial" claimed |
| `BEST KNOWN LOWER BOUND OR CONSTRUCTION` | no field anywhere | **absent** — as claimed |
| `HOW THE BOUND IS PROVED` | no field anywhere | **absent** — as claimed |

The sharpening is on row 2. `statusQualification` is non-null on all 499 and reads
bound-shaped often enough to look promising: on the 235 `open_with_solved_subcases`
records, 190 contain a bound-ish phrase and 57 contain a number or an asymptotic.
Reading them, **none of the 57 is an incumbent bound.** They are adjudication prose
— arguments for why the status is what it is, citing which subcase a 2026 paper did
*not* settle. Rank 110 is typical: *"the 2025 family paper still describes the weaker
arbitrary-power problem as open."* That is a scope exclusion, not a bound.

And the mechanism field is empty by construction: **0 of 499 records describe the
incumbent proof's mechanism** under any phrasing a regex finds. `PROOFATLAS_FIT.md`'s
conclusion stands unchanged and with a harder number behind it — **ProofAtlas lowers
the cost of selection, not of encoding, and encoding is the bottleneck.**

## 3. The leak table does not parse on most of this corpus

`PROMPT.md` step 2 wants one row per log / dimension / iteration / union factor in
the current bound. That presupposes a **quantitative** target with a pushable
parameter. Lexically, **267 of 499 targets (54%) have any bound shape at all** — and
that is an upper bound, since the regex fires on the word "dimension" in a record
about manifolds.

The interesting part is the interaction with playability:

|  | quantitative | purely yes/no |
|---|---|---|
| **playable** (35) | 12 | **23** |
| **class U** (424) | 232 | 192 |

**Two-thirds of the playable boards are pure yes/no questions on which the leak
table has nothing to say.** Does a projective plane of order 12 exist; does τ(n)
ever vanish; is every parallelohedron affinely Voronoi. There is no log factor to
attribute because there is no bound — there is a property and a search space.

This is a real limit on the instrument's reach, and it is the one place the two
workstreams come apart. The board-search instrument and the finite-witness search
are **different games played on disjoint halves of the corpus**. The instrument's
natural habitat is class U with a quantitative target — 232 records, the largest
single cell in the table, and exactly where no witness will ever settle anything.
That is not a flaw in either; it is a scoping fact that neither document stated,
and it means **`PROMPT.md`'s applicability should be screened on `quantitative`,
not on interest.**

The twelve records in the intersection — quantitative *and* playable — are where
both instruments bear at once:

```
  9 [P2n] Generalized Riemann Hypothesis for Dirichlet L-functions
 79 [P2 ] Hadwiger Conjecture
106 [P1 ] Unbounded Ranks of Elliptic Curves over Q
235 [P1 ] Zauner's Conjecture (SIC existence in every dimension)
257 [P2 ] Sidorenko Conjecture
322 [P2 ] Graph reconstruction conjecture
345 [P2 ] Erdos-Szekeres Convex Polygon Problem
356 [P2 ] Brauer's k(B) Conjecture
426 [P1 ] Maximal Number of MUBs in Composite Dimension
458 [P2 ] Erdos Matching Conjecture
488 [P2 ] Second Hardy-Littlewood Conjecture
500 [P2 ] Lehmer's Conjecture on tau
```

## 4. A caution the competition argument did not anticipate

`PROOFATLAS_FIT.md` ends on an inversion worth keeping: for board-harvesting,
"competition is an asset here and a cost there", because other agents' recorded
dead ends are the input.

That inversion **does not extend to the playable boards**, and the data says so:

```
workspaced, all records:      123/499 = 25%
workspaced, playable records:  16/ 35 = 46%
```

**Playable problems are nearly twice as likely to be worked as the corpus average.**
That is not a coincidence and it is not about the ranking — a problem where a single
finite object settles the question is a problem where a search can be started today,
by anyone, with no theory. Goldbach, Collatz, odd perfect numbers, Hadamard,
the Inverse Galois problem: all playable, all heavily worked.

So for a workstream whose deliverable is a **result**, playability and neglect are
in tension, and the 19 records that have both are the entire intersection. They are
listed in `PLAYABILITY.md` §3 and in `classification.json`
(`playable: true, hasWorkspace: false`). The strongest of them by ratio of
"checkable in one afternoon" to "attention received" are the finite-group block
conjectures — **287 Alperin–McKay, 300 Alperin weight, 356 Brauer k(B),
472 McKay–Navarro** — four unworkspaced P2 records where the counterexample is one
finite group and the predicate is a character-table computation that GAP or Magma
already implements.

**Stated as a prediction, so it can be scored:** if the finite-group block
conjectures are as checkable as this reads, someone has already swept the small
groups and the sweep is published. Finding that sweep is the first move, and if it
does not exist, that absence is the finding. **Neither branch has been checked here
— this container is egress-blocked and no literature search was run.** Do not carry
the four-record recommendation as verified; carry it as the next thing to verify.

## 5. What was not checked

* Nothing here touches `/collaboration/` or `/open-problems/` directly. All of it is
  read off the ranking payload, which is a third artifact.
* The 35 playable verdicts are hand-adjudicated by one rater with no blind second
  pass. `PROMPT.md` Part B's own standard — *"two raters agreeing on a word is not
  evidence, and two raters applying the same criterion to a named object is"* —
  applies here and is not met. The mitigation is that every verdict names its
  witness object in `classification.json`, so a second rater scores the object and
  not the label. That is the D35 remedy, applied prospectively; the rating itself is
  unrun.
* `witnessCheckFeasible` — the tractability question — is not answered for a single
  record. It is the field that decides whether any of this is playable in practice.

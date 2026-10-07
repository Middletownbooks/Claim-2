# cr(K_{7,11}) = 225: Woodall's Theorem 6(c), one rung up

**Status: computed.  Stage A and stage B are complete; neither has a survivor.**
This is a computer-assisted argument with one implementation of the search.
Read **What it rests on** and **Honest limits** before quoting the headline.

`THEOREM6C.md` recovered Woodall's closing device and used it to kill the
antisum-219 orbit.  This document runs the same device over everything that was
left, and nothing survives.

> **Every good drawing of K_{7,11} has at least 225 crossings.**  The
> Zarankiewicz drawing has 225, so **cr(K_{7,11}) = 225 = Z(7)Z(11)**.
> Counting then gives **cr(K_{7,12}) = 270 = Z(7)Z(12)**.

Nothing here uses Zarankiewicz's conjecture.  Unlike `PROOF_223.md`, nothing
here uses cr(K_{7,7}) = 81 or cr(K_{7,9}) = 144 either: the argument needs
Woodall's lemmas, not his computations.  The same code reproduces both of those
computations as controls, in 2 seconds and 2.6 minutes.

## The argument

Let D be a good drawing of K_{7,11}.  It has eleven vertices of degree 7, whose
rotations form an (11,7)-set M (a multiset of eleven vertices of CO_7), and
seven vertices of degree 11.  For two of the eleven, a and b, let x_ab be the
number of crossings between their stars.  In a good drawing every crossing is
between two non-adjacent edges, so it lies between exactly one such pair of
stars:

    crossings(D) = sum over the 55 pairs of x_ab.

**Woodall's antipath lemma** (1993).  The crossings between two stars, taken
in a suitable order, are the steps of a walk in CO_7 from rot(a) to the reverse
of rot(b).  Each step is labelled by the pair of ground vertices whose edges
cross.  Hence x_ab >= dbar(a,b).  CO_7 is bipartite (`PROOF_223.md`, input 5),
so x_ab = dbar(a,b) mod 2, and a pair drawn non-optimally has
x_ab >= dbar(a,b) + 2.

**Woodall's Theorem 6, proof of (c)** (p.663; quoted in `THEOREM6C.md`).  If all
six pairs of a (4,7)-subset are drawn optimally, the subset is tight, hence
pseudo-tight.  So **every non-pseudo-tight (4,7)-subset contains a pair drawn
with at least dbar + 2 crossings.**

**The sharpening** (`THEOREM6C.md`).  The non-optimally drawn pairs therefore
form a transversal of the family of non-pseudo-tight (4,7)-subsets.  Let
tau(M) be the minimum number of pairs meeting every member of that family.
Then

    crossings(D)  >=  Abar(M) + 2 tau(M).                                   (*)

Pseudo-tightness is computed under the largest antipath family, "arbitrary"
walks in CO_4.  That family makes a set easiest to call pseudo-tight and makes
tau smallest, so (*) holds under every reading of "antipath".  The "at most
twice" family, which is exactly what a good drawing produces, has the same
label sets (1758), so nothing is lost by the conservative reading.

**It remains to show Abar(M) + 2 tau(M) >= 225 for every (11,7)-set M.**  This
is immediate if Abar(M) >= 225.  Otherwise Abar(M) is 219, 221 or 223: the
antisum of an 11-multiset is odd, and the completed sweep found nothing below
219.

* **Stage A: antisum 219 needs tau >= 3, antisum 221 needs tau >= 2.**  Every
  such set has a representative among the 53,514,110 rows the completed top-221
  sweep wrote (`sweep_L5/low_*.txt`).  `c/ptcheck -need` checks each row.  It
  recomputes each row's antisum from its rotations rather than trusting the
  label.  **All 53,514,110 rows pass**: the 976 at antisum 219 have tau >= 3,
  and the 53,513,134 at antisum 221 have tau >= 2.  `stageA.json` records it;
  the run takes about 6 core-minutes.
* **Stage B: antisum 223 needs tau >= 1, i.e. one non-pseudo-tight
  (4,7)-subset.**  These sets were never written down; there are about 3.4e11
  of them (see the correction below).  So they are searched for again, on the
  sweep's canonical tree (staircase, prefix-minimality, stabiliser lex-min),
  cutting every node at its first non-pseudo-tight 4-subset.  This cut is
  sound because tau can only grow down a path of the tree:
  * below such a node, a leaf of antisum 223 has tau >= 1 and is settled;
  * a leaf of antisum <= 221 is in stage A.

  A survivor would be an antisum-223 set whose 330 (4,7)-subsets are all
  pseudo-tight.  **Over all 256 shards there are 0 survivors.**  No leaf was
  ever reached: every level-10 node that had a viable leaf candidate already
  had a non-pseudo-tight 4-subset.

Hence Abar(M) + 2 tau(M) >= 225 for every M, and cr(K_{7,11}) >= 225.

For K_{7,12}, each pair of the twelve degree-7 vertices lies in 10 of the 12
eleven-vertex subsets, so cr(K_{7,12}) >= 12 * 225 / 10 = 270 = Z(7)Z(12).
(K_{7,13} does not follow: 13 * 270 / 11 rounds up to 320, against
Z(7)Z(13) = 324.)

### Why each cut is sound

Every node carries the non-PT 4-subsets of its prefix and their tau.  Below a
node of size k, a leaf could only fail (*) if its antisum is at most
223 - 2 tau(node).  The staircase applies to that smaller top: prefix-minimality
makes the last element added the one of largest contribution, so the k-prefix
of a leaf of antisum T has antisum <= B_T[k].  `c/search6c.c` keeps one staircase
per value of tau, each built by exactly `search.c`'s construction.  The
staircases it prints match `zsearch -top 223 / 221 / 219`.  With `-tmin 223`
only the tau = 0 staircase exists, so the first non-PT 4-subset cuts the node.

Three economies keep the cost down, and none of them changes which leaves
survive:

* **Laziness.** A node's own sets are computed only once it has a child that
  passes every cheap clause.
* **Early exit.** The node stops at the first non-PT set its budget cannot
  absorb.
* **A per-thread verdict cache.** Verdicts are cached keyed on the sorted
  4-multiset; a verdict depends only on the multiset, which was checked over
  20,000 random multisets in all 24 orders.

## What it rests on

1. **Woodall 1993: the antipath lemma and the proof of Theorem 6(c).**  These
   are published and refereed, and his K_{7,7} and K_{7,9} results rest on the
   same foundation.  The quotations are in `THEOREM6C.md`.  This is the only
   mathematics not re-derived here.
2. **Exhaustiveness of the canonical tree.**  Every (11,7)-set of antisum
   <= 223 has an image under relabelling and reflection that is a leaf.  The
   argument has three steps:
   * order the set by repeatedly removing an element of maximal contribution;
   * send the first element to vertex 0, which is possible because S_7 is
     transitive on CO_7;
   * choose the image of the rest that is lex-minimal under Stab(0), of order
     14.

   The lex-min clause is prefix-closed: a g that made a prefix lex-smaller
   would make the whole sequence lex-smaller.  Two checks exercise the
   implementation: the gate (`zsearch -m 7 -n 7` gives exact level counts) and
   `zpredict.py` (130 of 130 predicted prefixes, 976 of 976 predicted rows).
3. **Completeness of the stored antisum <= 221 level.**  Each of the 2,400
   certificates of the completed sweep checks its survivor file against its
   histogram.
4. **This implementation**: `c/pt.c`, `c/search6c.c` and `c/ptcheck.c`.  The
   validation below is long because this is the part nobody else has checked.

## Validation

| check | result |
|---|---|
| CO_4 antipath family sizes, `arbitrary` / `distinct` | 1758 / 282, the published sizes |
| the "at most twice" family (what a good drawing produces) | 1758: the same label sets as `arbitrary` |
| `pt.c` vs `theorem6c.py` (independent Python): single 4-subset verdicts | 1,200 of 1,200 agree (365 non-PT) |
| `pt.c` vs `theorem6c.py`: t of whole rows | 12 of 12 agree |
| every non-PT verdict made inside real stage-B subtrees, vs the Python | 1,716 of 1,716 agree, plus 2,000 PT verdicts |
| the 219 orbit, all 976 rows | t = 103, tau = 8 on every row |
| **Woodall's own control: all 809,438 antisum-79 (7,7)-sets** | **min t = 10 exactly** (15,272 rows at 10), his "at least 10"; every one has tau >= 3 |
| **(7,7) pruned search, top 79** | **0 survivors in 2 s: cr(K_{7,7}) >= 81 reproduced** |
| **(9,7) pruned search, top 142, all 5,476,459 prefixes** | **0 survivors in 2.6 min: cr(K_{7,9}) >= 144 reproduced** (Woodall's fifth program; min antisum of (9,7)-sets is 140) |
| (7,7) positive control, top 81 | 16,716,814 antisum-81 sets with t = 0 survive |
| **(11,7) positive control, top 225, one prefix (`0,719,0,719,0`)** | **16,695,892 antisum-225 sets with t = 0 survive, including both Zarankiewicz multisets** (6r + 5r̄ and 5r + 6r̄; 8 orderings), identical on re-run |
| v1 (eager families, reference PT path, no lanes, no cache) vs v3, (7,7) top 81 | byte-identical sorted survivor sets |
| v1 on 1,000 stage-B prefixes (shard 7 of 1024) | 0 survivors; 2.06e9 reference PT calls |
| `-check` (every fast-path and cached verdict re-run through the reference `pt4()`) | stage-B shards 0, 128, 255: 1.94e9 verdicts; the whole (9,7) run: 2.07e9; (7,7): 5.8e8 -- all agree |
| stage-B shard 128 re-run on 2 threads with `-check` | identical visited / kept / cut / PT-call counts: deterministic |
| `-nopt` reproduces the gate | 1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · 809,438 |
| staircases | identical to `zsearch` at tops 223, 221, 219 |
| level-5 nodes with tau = 0 | 1,023,412, from both v1 (eager) and the dumped frontier |
| `-clamp` (also cut on any sub-multiset below cr(K_{7,k})) | changes nothing on the samples: PT already implies the clamps there |
| stage A re-run, antisum recomputed from the rotations | identical: 0 failing rows, no label mismatch |

Two rows carry the most weight.

* **The m = 7 minimum.**  Woodall's figure is a minimum over sets, so an
  over-eager predicate would push it above 10 and an under-eager one would pull
  it below.  It came out at exactly 10, over all 809,438 sets.
* **The m = 11 positive control.**  On the same code path and configuration,
  sets with every 4-subset pseudo-tight are abundant at antisum 225, and the
  actual optimal drawings' multisets are among them.  At antisum 223 there are
  none.

## The numbers

**Stage A** (`stageA.json`): 2,400 files, 53,514,110 rows, **0 failures**.
That took 2.09e9 pseudo-tightness tests.

**Stage B** (`stageB/sh_0.json` .. `sh_255.json`; the frontier is
`runs/frontierB_m11_L5.txt`, md5 `a09fbd77...`, 1,023,412 lines, regenerated by
`stageB.py` when missing):

| | |
|---|---|
| shards certified | 256 of 256 |
| prefixes | 1,023,412 (= frontier lines) |
| **survivors** | **0** |
| nodes visited | 37,362,133,364 |
| pseudo-tightness tests | 159,493,843,977 (152,154,800,689 served by the cache) |
| cost | 31,306 core-seconds = 8.7 core-hours, 2.24 h wall on 4 threads |

By level, from level 5 to level 11:

| level | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|
| visited | 1,023,412 | 66,327,923 | 470,192,546 | 2,941,539,339 | 6,018,900,941 | 27,864,149,203 | **0** |
| tau = 0 and a child | 1,023,164 | 9,424,649 | 127,115,712 | 295,206,691 | 1,894,142,923 | **0** | — |
| cut by 6(c) | 0 | 23,307,958 | 335,614,916 | 577,102,889 | 4,117,577,017 | 178,141,868 | — |

The unpruned top-223 tree is about 1.0e13 nodes, so the predicate cut it by
about 270x.

Run records for the controls are in `runs/thm6c_*.json`: the (9,7) run and its
`-check` twin, the m = 11 positive control, the v1 cross-check, the shard-128
re-run, and the unpruned top-223 baseline on a 201-prefix sample (400,769,349
nodes and 15,660,240 leaves; the stage-B search visits 3,455,081 nodes on the
same prefixes and reaches no leaf).

## Corrections to earlier documents

* **The antisum-223 level is about 3.4e11 sets, not 6.9e10, and it was never
  counted in full.**  `sweep.py` lowered its search cap to 221 from shard 489
  on.  Only 489 of the 2,400 shards, holding 1,356,486 of the 6,655,827
  prefixes, ran at top 223, so `223: 68,680,444,390` is those shards' count.
  Scaled up, the level holds about 68.68e9 x 2400/489 = 3.4e11 sets.  This is
  `INSTRUMENTS.md` instrument 25.
* **`PROOF_223.md`'s "223 is the ceiling" stands for the method it names**:
  antidistances plus subset clamps.  Theorem 6(c) lies outside that family,
  and `-clamp` shows the clamps add nothing to it here.
* The handoff's R2 (triple bounds), R3 (SDP lift) and R4 (realisability) are
  not needed for K_{7,11}.

## Literature

Woodall 1993 was read from page images (`THEOREM6C.md`).

* De Klerk, Maharry, Pasechnik, Richter and Salazar (SIAM J. Discrete Math.
  20, 2006) relax min x^T Q x over the simplex, Q the CO_7 antidistance matrix,
  to an SDP.  Their cr(K_{7,n}) >= 2.1796 n^2 - 4.5 n gives about 214 at n = 11.
* Brosch and Polak (Math. Programming, 2023) give asymptotic bounds for m >= 10.
* The survey of graphs with known crossing numbers (Clancy, Haythorpe,
  Newcombe; arXiv:1901.05155) and the open-problem pages found list K_{7,11}
  (with K_{9,9}) as the smallest open cases.

No source found computes the exact minimum antisum of (11,7)-sets or settles
K_{7,11}.  **Caveat:** the PDFs themselves were blocked by this session's egress
proxy, so this check rests on abstracts and search results, not full text.
Repeat it, with a library and a search of 2024–2026 preprints, before
publishing anything.

## Reproducing

```sh
cd zarankiewicz/c && make                             # zsearch, zsearch6c, ptcheck
./ptcheck -selftest                                   # family sizes, symmetry, order invariance
./zsearch -m 7 -n 7 -survivors m7.txt && ./ptcheck < m7.txt    # min t = 10, every tau >= 3
./zsearch6c -m 7 -n 7 -tmin 79 -check                 # 0 survivors: K_{7,7} >= 81
./zsearch6c -m 7 -n 7 -tmin 79 -top 81                # 16,716,814 survivors (positive control)
./zsearch -m 9 -n 7 -top 138                          # no leaves: min antisum at (9,7) is 140
./zsearch6c -m 9 -n 7 -tmin 140 -d 5 -dump f9.txt
./zsearch6c -m 9 -n 7 -tmin 140 -startfile f9.txt -threads 4   # 0 survivors: K_{7,9} >= 144
./zsearch6c -m 11 -n 7 -top 225 -tmin 225 -start 0,719,0,719,0 # 16,695,892 survivors (control)
cd .. && python3 stageA.py                            # 0 failing rows of 53,514,110  (~6 core-min)
python3 stageB.py && python3 stageB.py summary        # 0 survivors over 256 shards (~9 core-h)
CHECK=1 FIRST=128 UPTO=129 python3 stageB.py          # one shard with every verdict re-verified
```

## Honest limits

* **Computer-assisted, one implementation of the search.**  Pseudo-tightness was
  checked against an independent Python implementation.  The pruned search
  exists only in C, and v1 to v3 share the tree code.  **An independent
  reimplementation of stage B is the check this most needs before anyone calls
  it a theorem.**  The (7,7) and (9,7) reproductions show that the code agrees
  with both of Woodall's published computations.  They do not replace an
  independent implementation.
* **Exhaustiveness of the canonical tree is argued and tested, not formally
  verified.**
* Stage A trusts that the stored rows are complete.  The certificates say they
  are; they were not regenerated here.
* The minimum antisum of 219 at m = 11 comes from the completed sweep.  Stage B
  does not use it (`-tmin 223`); stage A uses it only to say that 219 and 221
  are the only levels below 223.
* Woodall's lemma is used as published.  If it ever fails under some reading,
  so does this.

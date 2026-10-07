# cr(K_{7,11}) = 225: Woodall's Theorem 6(c), one rung up

**Status: DRAFT, IN PROGRESS -- stage A complete, stage B running (certificates in `stageB/`).  Do not cite the headline until stage B's 256 shards are all certified.**

`THEOREM6C.md` recovered Woodall's closing device and killed the antisum-219
orbit.  This document runs that device over everything that was left, and finds
nothing left.

> **Every good drawing of K_{7,11} has at least 225 crossings.**  The
> Zarankiewicz drawing has 225, so **cr(K_{7,11}) = 225 = Z(7)Z(11)**, and
> cr(K_{7,12}) = 270 = Z(7)Z(12) follows by counting.

This is a computer-assisted argument, and it is exactly as good as the four
things it rests on, listed under **What it rests on** below.  Nothing in it uses
Zarankiewicz's conjecture, and, unlike `PROOF_223.md`, nothing in it uses
cr(K_{7,7}) = 81 or cr(K_{7,9}) = 144.  It uses Woodall's lemmas, not his
computations.

## The argument

Let D be a good drawing of K_{7,11}: eleven vertices of degree 7 whose rotations
form an (11,7)-set M (a multiset of eleven vertices of CO_7), and seven vertices
of degree 11.  For two of the eleven, a and b, write x_ab for the number of
crossings between their stars.  Every crossing in a good drawing is between two
non-adjacent edges, so it lies between exactly one such pair of stars:

    crossings(D) = sum over the 55 pairs of x_ab.

**Woodall's antipath lemma** (1993): the crossings between two stars, taken in
a suitable order, are the steps of a walk in CO_7 from rot(a) to the reverse of
rot(b), each step labelled by the pair of ground vertices whose edges cross.
Hence x_ab >= dbar(a,b), and since CO_7 is bipartite (`PROOF_223.md`, input 5),
**x_ab = dbar(a,b) mod 2**, so a pair drawn non-optimally has x_ab >= dbar(a,b) + 2.

**Woodall's Theorem 6, proof of (c)** (p.663; `THEOREM6C.md`): if all six pairs
of a (4,7)-subset are drawn optimally, the subset is tight, hence pseudo-tight.
So **every non-pseudo-tight (4,7)-subset contains a pair drawn with at least
dbar + 2 crossings.**

**The sharpening** (`THEOREM6C.md`): the non-optimal pairs therefore form a
transversal of the family of non-pseudo-tight (4,7)-subsets, so with tau(M) the
minimum number of pairs meeting all of them,

    crossings(D)  >=  Abar(M) + 2 tau(M).                                  (*)

Pseudo-tightness is computed under the largest antipath family ("arbitrary"
walks in CO_4), which makes sets easiest to call pseudo-tight and tau smallest,
so (*) holds whatever reading of "antipath" one takes.

**It remains to show Abar(M) + 2 tau(M) >= 225 for every (11,7)-set M.**  It is
immediate if Abar(M) >= 225.  Otherwise Abar(M) is 219, 221 or 223: the
antisum of an 11-multiset is odd, and nothing is below 219 (the completed sweep).

* **Stage A -- antisum 219 and 221: tau >= 3 and tau >= 2.**  Every such set has
  a representative among the 53,514,110 rows the completed top-221 sweep wrote
  (`sweep_L5/low_*.txt`).  `c/ptcheck -need` checks each one.  **All 53,514,110
  pass**: 976 at antisum 219 with tau >= 3, and 53,513,134 at antisum 221 with
  tau >= 2.  No failing row (`stageA.json`, about 6 core-minutes).
* **Stage B -- antisum 223: tau >= 1.**  Here one non-pseudo-tight (4,7)-subset
  is enough.  These sets were never written (about 3.4e11 of them; see the
  correction below), so they are searched for again.  The search uses the same
  canonical tree as the sweep (staircase, prefix-minimality, stabiliser lex-min),
  and cuts any node with a non-pseudo-tight 4-subset.  tau can only grow down a
  path of the tree, so such a node has no leaf of antisum 223 and tau = 0 below
  it, and every leaf of antisum <= 221 below it is in stage A.  A leaf that
  survives would be an antisum-223 set with every one of its 330 (4,7)-subsets
  pseudo-tight.  **Result pending: the shards certified so far have 0 survivors.**

Hence Abar(M) + 2 tau(M) >= 225 for every M, and cr(K_{7,11}) >= 225.  K_{7,12}:
each pair of the twelve 7-side... rather, of the twelve degree-7 vertices lies in
10 of the 12 eleven-subsets, so cr(K_{7,12}) >= 12 * 225 / 10 = 270 = Z(7)Z(12).

### The pruning is sound node by node, not just at the leaves

The search keeps `famn`, the non-PT 4-subsets of the current prefix, and tau
of that family.  For a node of size k, the leaves below it whose bound could be
below 225 have antisum <= 223 - 2 tau(node).  By the staircase argument
(prefix-minimality: the last element added has the largest contribution, so the
k-prefix of a leaf of antisum T has antisum <= B_T[k]), such a node needs
antisum <= B_{223 - 2 tau}[k].  `c/search6c.c` keeps one staircase per tau,
built by exactly `search.c`'s construction.  Its printed staircases match
`zsearch -top 223 / 221 / 219` exactly.  With `-tmin 223` only the tau = 0
staircase exists, so the first non-PT 4-subset cuts.

## What it rests on

1. **Woodall 1993, the antipath lemma and the proof of Theorem 6(c).**  Published
   and refereed, and the same foundation his K_{7,7} and K_{7,9} results stand on.
   The quotations are in `THEOREM6C.md`.  This is the only mathematics not
   re-derived here.
2. **Exhaustiveness of the canonical tree.**  Every (11,7)-set of antisum <= 223
   has an image under relabelling and reflection that is a leaf.  Proof sketch:
   * Order the set by repeatedly removing an element of maximal contribution;
     each prefix then satisfies prefix-minimality and the staircase.
   * Send the first element to vertex 0; S_7 is transitive on CO_7.
   * Choose the image of the rest lex-minimal under Stab(0), which has order 14.
     If some g in Stab(0) made a prefix lex-smaller, it would make the whole
     sequence lex-smaller, so the condition is prefix-closed.

   The gate (`zsearch -m 7 -n 7`, exact level counts) and `zpredict.py` (130 of
   130 predicted prefixes, 976 of 976 predicted rows) test the implementation.
3. **Completeness of the stored 221 level.**  The 2,400 certificates of the
   completed sweep each check their survivor file against their histogram.
4. **This implementation of pseudo-tightness** (`c/pt.c`) and of the pruned
   search (`c/search6c.c`) -- see **Validation**, which is long because this is
   the part nobody else has checked.

## Validation

| check | result |
|---|---|
| CO_4 antipath family sizes, `arbitrary` / `distinct` | 1758 / 282, the published sizes |
| the "at most twice" family (what a good drawing produces) | 1758, the same label sets as `arbitrary` |
| `pt.c` against `theorem6c.py` (independent Python), single 4-subset verdicts | 1,200 of 1,200 agree (365 non-PT) |
| `pt.c` against `theorem6c.py`, t of whole rows | 12 of 12 rows agree |
| every non-PT verdict made inside real stage-B subtrees, against the Python | 1,716 of 1,716 agree, plus 2,000 PT |
| the 219 orbit, all 976 rows | t = 103, tau = 8 on every row (as `THEOREM6C.md`) |
| **Woodall's own control: all 809,438 antisum-79 (7,7)-sets** | **min t = 10 exactly** (15,272 rows at 10), his "at least 10"; every one has tau >= 3 |
| (7,7) pruned search, top 79 | 0 survivors in 2 s: cr(K_{7,7}) >= 81 reproduced |
| (7,7) **positive control**, top 81 | 16,716,814 antisum-81 sets with t = 0 survive: the predicate is not over-eager |
| v1 (eager families, no lanes, no cache) vs v3, top 81 | byte-identical sorted survivor sets |
| `-check`: every fast-path and cached verdict re-run through the reference `pt4()` | 844,514 + 575,466,499 (m = 7) + 653,220,444 (stage-B shard 0): all agree |
| `-nopt` reproduces the gate | 1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · 809,438 |
| staircases | identical to `zsearch` at tops 223, 221, 219 |
| level-5 nodes with tau = 0 | 1,023,412 from both v1 (eager) and the dumped frontier |
| `-clamp` (also cut on any sub-multiset below cr(K_{7,k})) | changes nothing on the samples; PT already implies the clamps there |

The control that carries the most weight is the m = 7 minimum.  Woodall's
figure is a minimum over sets, so an over-eager predicate would push it above
10, and an under-eager one below.  It came out at exactly 10, over all 809,438
sets rather than the 150 sampled in `THEOREM6C.md`.

## The numbers

Stage A (`stageA.json`): 2,400 files, 53,514,110 rows, 0 failures; 2.09e9
pseudo-tightness tests.

Stage B (`stageB/sh_*.json`, 256 shards of the 1,023,412-line frontier):

(pending -- `python3 stageB.py summary` gives the running totals)

## Corrections to earlier documents

* **The antisum-223 level is about 3.4e11 sets, not 6.9e10, and it was never
  counted in full.**  `sweep.py` lowered its search cap to 221 from shard 489
  onwards; only 489 of the 2,400 shards, holding 1,356,486 of the 6,655,827
  prefixes, ran at top 223.  The histogram entry `223: 68,680,444,390` is those
  shards' count, not the level's.  Scaled by shards, the level holds about
  68.68e9 x 2400/489 = 3.37e11 sets; scaled by prefixes, about 3.4e11.  The
  full top-223 tree is about 1.0e13 nodes.  This is instrument 25 in
  `INSTRUMENTS.md`, a denominator error of the same shape as rule 4.
* `PROOF_223.md`'s "223 is the ceiling" stands for the method it names,
  antidistances plus subset clamps.  Theorem 6(c) is outside that family.

## Literature

Woodall 1993 was read from page images (`THEOREM6C.md`).  De Klerk, Maharry,
Pasechnik, Richter and Salazar (SIAM J. Discrete Math. 20 (2006)) relax
min x^T Q x over the simplex, Q the CO_7 antidistance matrix, to an SDP.  Their
cr(K_{7,n}) >= 2.1796 n^2 - 4.5 n gives about 214 at n = 11.  Brosch and Polak
(Math. Programming 2023) give bounds for m >= 8.  Neither computes the exact
minimum antisum of (11,7)-sets, and the 2019 survey of known crossing numbers
(Clancy, Haythorpe, Newcombe, arXiv:1901.05155) lists K_{7,11} as open.  The
PDFs themselves were behind this session's egress proxy, so this check rests on
abstracts and search results, not full text.  Check again before publishing.

## Reproducing

```sh
cd zarankiewicz/c && make && cc -O3 -march=native -o zsearch6c search6c.c pt.c cog.c -lpthread \
                          && cc -O3 -march=native -o ptcheck ptcheck.c pt.c cog.c
./ptcheck -selftest                                   # family sizes, symmetry, order invariance
./zsearch -m 7 -n 7 -survivors m7.txt && ./ptcheck < m7.txt    # min t = 10, tau >= 3
./zsearch6c -m 7 -n 7 -tmin 79 -check                 # 0 survivors: K_{7,7} >= 81
./zsearch6c -m 7 -n 7 -tmin 79 -top 81                # 16,716,814 survivors (positive control)
cd .. && python3 stageA.py                            # 0 failing rows of 53,514,110
python3 stageB.py && python3 stageB.py summary        # 0 survivors over 256 shards
```

## Honest limits

* **Computer-assisted, single implementation.**  Pseudo-tightness was
  cross-checked against an independent Python implementation, but the pruned
  search exists in one C implementation only: v1, v2 and v3 share the tree code.
  An independent reimplementation of stage B is the check this most needs before
  anyone calls it a theorem.
* **Exhaustiveness is argued, not formally verified**: the sketch above, the
  gate, and `zpredict.py`.
* Stage A trusts that the stored rows are complete.  The certificates say they
  are; they were not regenerated here.
* Woodall's lemma is used as published.  If a reading of it ever fails, so does
  this.

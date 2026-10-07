# Handoff: Zarankiewicz's conjecture at K_{7,11}

Everything below is either a theorem with a citation, a computation in this
repository with the command to re-run it, or explicitly flagged as a guess.
This file is the map.

## Status, 7 October 2026: cr(K_{7,11}) = 225, computer-assisted

**Read `THEOREM6C_SWEEP.md` first.**  Woodall's Theorem 6(c), sharpened from a
floor to an exact minimum transversal tau, gives crossings >= antisum + 2 tau
for every good drawing (`THEOREM6C.md`).  It was run over every (11,7)-set that
the pairwise bound left open:

* **Stage A**: every one of the 53,514,110 stored rows of antisum 219 and 221
  has antisum + 2 tau >= 225.  No failing row.
* **Stage B**: the antisum-223 level, about 3.4e11 sets that were never stored,
  was searched again with "has a non-pseudo-tight (4,7)-subset" as a node
  predicate.  That took 256 shards and 8.7 core-hours, and left **0
  survivors**.

So cr(K_{7,11}) >= 225 = Z(7)Z(11), and cr(K_{7,12}) = 270 by counting.  The
same code reproduces both of Woodall's computer results as controls:
cr(K_{7,7}) >= 81 in 2 s and cr(K_{7,9}) >= 144 in 2.6 min.  Positive controls
show that the predicate keeps millions of sets at the true crossing numbers,
including the Zarankiewicz drawing's own multisets.

**The next task is independent verification, not more search.**  The pruned
search exists in one C implementation.  Pseudo-tightness was cross-checked
against an independent Python implementation, but the tree code was not.  Write
stage B again from the definitions in `THEOREM6C.md`, in a different language
or at least without reading `c/search6c.c`, and check that it also finds 0.
Then repeat the literature check with full-text access: this session's egress
proxy blocked the PDFs.  Only after both should anyone call it a theorem.

After that, the nearest open cases are K_{7,13} (Z = 324; counting from
K_{7,12} gives only 320) and K_{9,9} (Z = 256, which needs CO_9 and
(4,9)-pseudo-tightness).

## The question

    Z(m,n) = floor(m/2)floor((m-1)/2)floor(n/2)floor((n-1)/2)
    Z(7,11) = 3*3*5*5 = 225,  and the Zarankiewicz drawing achieves it.

Zarankiewicz's conjecture says cr(K_{m,n}) = Z(m,n).  It is known for
min(m,n) <= 6 (Kleitman 1970) and, for m = 7, for n <= 10: Woodall 1993 settled
K_{7,7} = 81 and K_{7,9} = 144 by computer, and n = 8, 10 follow from those two
by subset counting.  **K_{7,11} is the frontier case.**  Settling it also settles
K_{7,12} for free: 12 eleven-subsets, each pair in C(10,9) = 10 of them, so
12 * 225 / 10 = 270 = Z(7,12).

Christian-Richter-Salazar (JCTB 2013) showed that for each fixed m only finitely
many n need checking, so the m = 7 column is finite in principle, with an
enormous bound.

## Where the lower bound stands

| bound | source |
|---|---|
| 219 | min antisum over (11,7)-sets -- this repo's completed sweep |
| 220 | elementary counting from cr(K_{7,9}) = 144: 55 * 144 / 36 |
| 223 | `PROOF_223.md`: antisums plus the known cr(K_{7,k}), by LP -- the ceiling of that method |
| **225** | **`THEOREM6C_SWEEP.md`: antisum + 2 tau, Woodall's Theorem 6(c) sharpened, over every set** |

Note the ordering: **219 never was the state of the art.**  The pairwise
antidistance bound is *weaker* than elementary counting for this case.  Quote
223 against 220, never against 219.

### What the sweep proved (and it is the repo's main asset)

All 2400 shards complete.  Partition at level 5 of a 6,655,827-prefix frontier,
shard = frontier index mod 2400.  Global antisum histogram:

    219: 976 rows (one orbit: 5040 members, 70 containing vertex 0, 13 surviving
         the canonical rules, 976 rows over 130 level-5 prefixes)
    221: 53,513,134 rows
    223: 68,680,444,390 -- from the 489 shards that ran at top 223 ONLY; the
         other 1,911 ran at top 221.  The level is about 3.4e11 sets
         (`INSTRUMENTS.md` instrument 25).

**Nothing below 219 anywhere.**  Rows are in `sweep_L5/low_*.txt` (2.2 GB, all
tracked in git -- a fresh clone has the data; use `--depth 1`), certificates in
`sweep_L5/sh_*.json`.  `zpredict.py` re-derives from the canonical rules alone
what each shard must hold and found 130 of 130 predicted prefixes and 976 of 976
predicted rows, which is the strongest check the programme has.

### What `PROOF_223.md` adds

For any subset S of the eleven 7-stars the sub-drawing is a good drawing of
K_{7,|S|}, so `crossings >= antisum(M) + (cr(K_{7,|S|}) - antisum(S))`.  Over all
53,514,110 rows, **zero** have a bound below 223; 45,689,450 sit at 223 and
7,824,660 at 225.  Load-bearing theorems: exactly cr(K_{7,7}) = 81 (58.3% of
rows) and cr(K_{7,9}) = 144 (41.7%).  The case split is closed by a parity fact
proved here: CO_7 is bipartite, reversal flips the colours, so at odd m the
antisum is C(m,2) mod 2 -- **always odd at m = 11**, so 220 and 222 cannot occur.

And **223 is exactly this method's ceiling**: `mixedlp.py` solves the full LP
over x_ij >= dbar plus all 2026 subset constraints, and the 219 orbit's optimum
is 223 with a single dual variable.  No reweighting of these constraints reaches
224.  Past 223 needs a constraint outside the family.

## The routes, with prices

R1 and R4 are closed.  R0 is a literature read and should come first; R2 and R3
are the computational routes that remain.  Read the closed ones anyway:
R1 was closed inside the handoff session, after first looking like the whole
proof, and the way it fell is the most useful thing in this file.

### R1 -- the other side of the drawing.  TRIED IN THIS SESSION, AND CLOSED.

Woodall's pairwise bound applies to any two stars sharing their leaves, so it
applies to the **seven 11-stars** in CO_11 as well as to the eleven 7-stars in
CO_7, and gives an independent lower bound on the same crossings:

    crossings >= sum over the C(7,2) = 21 pairs of dbar_{CO_11}

Because the joint LP over both sides separates when the two rotation systems are
left uncoupled (the minimum of the max is the max of the minima), the question
was whether that side's minimum is at least 225.  **It is not.**

* CO_11 has 10! = 3,628,800 vertices, is 11-regular, has eccentricity 25, and
  dbar(a,a) = 25 = Z(11) -- exactly mirroring CO_7's dbar(a,a) = 9 = Z(7).
  S_11 is transitive on it, so one breadth-first search (six seconds,
  `c/co11.c`) gives every distance up to relabelling.
* `c/co11min.c` does exact coordinate descent: each of the seven positions
  replaced by its global best over all 3.6M candidates, from random restarts.
  Twenty-two of twenty-four restarts returned 225 and one returned 227 -- and
  then one returned **223**.
* That 223 was re-verified by `c/co11check.c`, which runs a **fresh** breadth-
  first search from each of the seven vertices and shares no query code with the
  minimiser (no relabelling, no rank arithmetic on the query path): antisum 223,
  dbar matrix symmetric, every diagonal 25.
* The mixed bound adds **nothing** on that side: no subset of the seven falls
  below its clamp (cr(K_{k,11}) = Z(k)Z(11) for all k <= 6, Kleitman), so the
  best deficit is 0 and the counting recursion also returns 223.

So the joint bound over both sides is max(223, 223) = **223**, and the finding is
a sharper statement of where the method dies rather than a step past it:

> **223 is the ceiling of Woodall's pairwise bound on either side of K_{7,11},
> combined with every complete bipartite crossing number currently known.**

Two things worth keeping from the attempt.  First, the pricing, in case anyone
wants that side's exact minimum for its own sake: the staircase rungs are
`223 159 106 63 31 10`, the level-2 frontier is 289,763 vertices (about 13,171
orbits once a_1 is fixed and Stab(a_1), order 22, is quotiented out), and
sampled branching is 184,454 at level 2 -> 3 and 24,847 at level 3 -> 4, so a
naive sweep is order 1e14 nodes -- the CO_7 sweep's prefix-minimality and
lex-minimality reductions are not implemented there.  Second, the method: the
falsification step was listed as task 1 precisely because it was cheap and
decisive, and it paid within the hour.  Keep doing that.

### R0 -- DONE.  The paper was read, the device found, and the 219 orbit is dead -- and then everything else.

The question `PROOF_223.md` raised -- the minimum antisum at m = 7 is 79 while
cr(K_{7,7}) = 81, so what closed that gap of 2? -- is answered.  The page images
of Woodall 1993 were recovered from this session's transcript and read directly.
The device is **Theorem 6(c)**, the augmented antisum, and `THEOREM6C.md` records
it in full with the definitions of tight and pseudo-tight.  It is implemented in
`theorem6c.py`, validated against his published figures (the four CO_4 antipath
family sizes exactly; the (4,6) example exactly; and the minimum of t over 150
sampled antisum-79 (7,7)-sets is **10**, matching his stated "at least 10"), and
sharpened: his counting term is a floor where an exact minimum transversal
belongs, since the bad pairs form a hitting set of the non-pseudo-tight
(4,7)-subsets.

For the antisum-219 orbit: t = 103, **tau = 8** (LP 7.695, greedy 8, no
7-element transversal), so **any good drawing with that rotation multiset has at
least 235 crossings.**  The orbit that capped every bound this programme
produced, including `PROOF_223.md`'s 223, is eliminated.

**This is now the main line, and it is Woodall's fifth program one rung up.**
What remained was antisum 221 (53,513,134 rows), which needs tau >= 2, and
antisum 223 (about 3.4e11 sets, never stored), which needs only tau >= 1, i.e.
at least one non-pseudo-tight (4,7)-subset.  **Both are now done**, the second
as a node predicate in the C search, which is what Woodall did at (9,7)
(p.666).  See `THEOREM6C_SWEEP.md`.  R2 and R3 below are not needed for
K_{7,11}; they are kept for the next cases.

### R2 -- rotation-dependent triple bounds

Replace the clamp cr(K_{7,3}) = 9 with c3(a,b,c), the true minimum over good
drawings of K_{7,3} with those three rotations.  Any value above
max(9, antisum) tightens the LP of `mixedlp.py` directly, and the 219 orbit only
needs 2 more.  This is new topological input, not a reuse of anything here.
The orbit count is manageable (720^3 / 10080 is about 37M triples up to
symmetry); the hard part is computing c3 at all.

### R3 -- semidefinite / sum-of-squares

The 219 is the value of a level-1 (pairwise) relaxation.  A level-2 lift over
*triples* of rotations encodes the local-global consistency the pairwise bound
discards, and its dual is a short certificate -- the one kind of proof object an
exhaustive negative search can never hand anybody.  See
de Klerk-Maharry-Pasechnik-Richter-Salazar on SDP bounds for cr(K_{m,n}).
This is engineering plus compute, not a new theorem.

### R4 -- realisability.  Closed, and would not pay anyway.

Do not restart this.  Two independent reasons:

* **Closed by measurement.**  The achievable rotation set of 7 points is the set
  of cells of the arrangement of their 21 connecting lines (at most 162, since
  six lines concur at each point; measured 61 to 96).  It is **not** determined
  by the order type: 30 of 33 repeated order types gave different
  achievable-set sizes, so there is no finite family to exhaust.  For
  rectilinear drawings the honest invariant is the order type of all 18 points,
  and the complete catalogue of order types stops at 11.
* **It would not pay.**  Killing the 219 orbit buys nothing on its own:
  45,688,474 rows at antisum 221 also sit at 223, and the entire 223-antisum
  level (about 3.4e11 multisets, never stored) sits at 223 for free.
* For the record, 100,000 exact per-configuration tests found no straight-line
  configuration admitting the 219 class; best-match histogram
  `4:7, 5:30143, 6:61648, 7:7927, 8:275, 9:0, 10:0`.  **Whether that is
  obstruction or rarity is undecided** -- an earlier claim that it "looks rare
  rather than obstructed" was withdrawn, because two points in a tail do not
  support a forecast.  All of this bears on the rectilinear crossing number
  only, never on cr.

### The load-bearing measurement that survives all of it

A genuinely achievable antisum-223 configuration draws **387** crossings, and
**304** after optimising point placement inside fixed cells, against Z = 225,
with only **28 of 55** pairs attaining their antidistance (worst case:
antidistance 2 realised as 14).  Pair-optimality, not realisability, is what
stands between a low antisum and a low crossing count.  Any proposed lemma must
be consistent with this.

## Verify everything in under an hour

```sh
git clone --depth 1 -b claude/zarankiewicz-k711 <repo> && cd claim-2/zarankiewicz
pip install scipy numpy
python3 -c "import sys;sys.path.insert(0,'intake');import cog,numpy as np;
c=cog.CO(7);np.array(c.antidist_matrix(c.dist_matrix()),dtype=np.uint8).tofile('A720.bin')"

cd c && make 2>/dev/null || cc -O2 -o zsearch *.c ; cd ..
./c/zsearch -m 7 -n 7                       # THE gate: 8.4 s, levels must be
                                            # 1 13 377 29099 801503 14623179 809438
cc -O2 -o c/screen c/screen.c
cat sweep_L5/low_*.txt | ./c/screen A720.bin 223 -      # "below 223: 0"

python3 mixedbound.py --selftest
python3 mixedlp.py --selftest
python3 mixedlp.py --class 0,0,15,74,105,438,569,647,660,671,689 --certificate
python3 zpredict.py --selftest                           # 7.7 s
python3 verify_219.py
cc -O2 -o c/co11 c/co11.c && ./c/co11                    # 6 s
cc -O2 -o c/co11min c/co11min.c && ./c/co11min 8         # minutes; expect 225

# Theorem 6(c) -- THEOREM6C_SWEEP.md
./c/ptcheck -selftest                                    # CO_4 families 1758 / 282
./c/zsearch -m 7 -n 7 -survivors m7.txt && ./c/ptcheck < m7.txt   # min t = 10
./c/zsearch6c -m 7 -n 7 -tmin 79 -check                  # 0 survivors (K_{7,7} >= 81)
./c/zsearch6c -m 7 -n 7 -tmin 79 -top 81                 # 16,716,814 (positive control)
python3 stageA.py                                        # 0 of 53,514,110 fail; ~6 core-min
CHECK=1 FIRST=128 UPTO=129 python3 stageB.py             # one stage-B shard, fully re-verified
python3 stageB.py summary                                # 256 shards, 0 survivors
```

`mixedbound.py --selftest` contains the test that matters: with the cr clamps
set to zero the counting recursion collapses to the antisum **exactly**, since
`sum_i antisum(S minus i) = (k-2) antisum(S)` identically.  A bug in the
counting therefore cannot inflate the bound silently.

## Before calling any of it new

Woodall 1993 has been read (`THEOREM6C.md`).  A search-engine pass on
7 October 2026 found nothing that settles K_{7,11} or computes the minimum
antisum of (11,7)-sets.  De Klerk et al. 2006 give cr(K_{7,n}) >= 2.1796 n^2 -
4.5 n, about 214 at n = 11; Brosch-Polak 2023 treat m >= 10; the 2019 survey
lists K_{7,11} as open.  The PDFs were blocked by the egress proxy, so repeat
this with full text before publishing (`THEOREM6C_SWEEP.md`, Literature).

## The discipline this programme runs on

`INSTRUMENTS.md` is the log of instruments and the mistakes they caused; read
it.  The rules that earned their place:

1. Compute the set before quoting a rank or a superlative.  Two false claims
   ("fourth-highest of nine" when it was second; "largest single-cycle growth"
   when one earlier shard beat it) were caught only by running the sort.
2. A range over n observations constrains those n observations, nothing more.
   "98.81% to 99.31% over nine cycles" was read as a floor; cycle 44 came in at
   98.65%.
3. Prefer a check that reads the thing itself to one that reads bookkeeping
   about it.  The staleness check failed three times while reading metadata.
4. State the denominator.  "N of 5040" was wrong by a factor of 390 because
   a_1 is always vertex 0, so only 70 orbit members are writable and the
   canonical rules cut those to 13.
5. Validate a search on the real data, not on random data.  `exactmin.py`'s
   first validation was vacuous: random `min(A, A^T)` matrices are full of
   zeros, so every answer was 0 and the search was never exercised.
6. Power-analyse a hunt before running it.  A realisability search over 40
   configurations was reported before noticing the per-configuration
   probability was about 3.3e-6, needing ~207,000 for an even chance.
7. Two different things were both called "the gate".  The real one is
   `c/zsearch -m 7 -n 7` (8.4 s).  `check_gate.py` takes about 11 minutes and
   reasoning from it as if it were the fast one produced a wrong idle estimate.
8. Never `pgrep -f` or `pkill -f` with a pattern that matches your own command
   line -- see `PGREP_SELF_MATCH.md`, four recorded self-inflicted kills,
   including one that killed the calling shell at exit 144.

## Standing operational constraints

* Develop and push **only** to `claude/zarankiewicz-k711`.  Never push elsewhere
  without explicit permission, and do not open a pull request unless asked.
* Another instance may be working on this branch: **merge, never rebase, never
  force-push.**  A pushed commit cannot be amended.
* `git push -u origin <branch>`, retrying only on network errors with 2s, 4s,
  8s, 16s backoff.
* Never run `zsearch` or the verifiers while a sweep cycle is running.

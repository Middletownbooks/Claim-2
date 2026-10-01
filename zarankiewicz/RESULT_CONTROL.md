# The control ran. It took 397 seconds, and six of my numbers were wrong.

The bundle arrived, it runs here, and the measurement nobody had made is made.

## 1. Their control suite, run locally

```
python3 reproduce.py --n6 --certificate     ->  13/13 controls passed
```

Everything it asserts moves from `SECONDARY-RELAYED` to `PRIMARY-VERIFIED-LOCALLY`: Woodall's 32
classes of (5,5)-sets at antisum 16, the unique (7,5)-set at 34, the staircase **79, 56, 36, 21,
9, 3**, the zero-survivor (5,7) sweep in 9,333 nodes, Theorem 7's availability pattern and the
weakened bounds **{2: 221, 4: 223, 6: 215}**, the CO₄ family sizes, **120/120** pair-optimal
drawings tight, the published (4,6)-set at antisum 15, all 14 core sets, and the n = 6 census
(6,930 classes; 48/19/54/22; core 14; any 59). The n = 6 sweep took **32 seconds**.

The staircase passing matters on its own: the prefix bounds my orbit counts were computed against
were the right ones.

## 2. The positive control

The full (7,7) enumeration, Theorem 7 on, run to completion — `aborted: false`.

| | |
|---|---|
| level counts | 1 · 12 · 329 · 25,346 · 615,817 · **9,827,953** · **809,438** |
| total nodes | **11,278,896** |
| wall clock | **397 s** |
| throughput | 28,410 nodes/s |
| depth-5 prefix vs the relayed figures | **exact match** |

`run_m7_thm7_2-4.json`; every figure below re-derived in `control_arithmetic.py`, 17 assertions.

## 3. Six corrections, all mine

**(i) The tree is 1.13 × 10⁷ nodes, not 4–5 × 10⁸.** I extrapolated 615,817 × 24.3² = 3.64 × 10⁸
and overshot by **32×**. The cause is structural, not a slip: **level 7 is 809,438 against level
6's 9,827,953 — the tree contracts 12× at the last level.** The staircase is a *decreasing
budget*, 79 → 56 → 36 → 21 → 9 → 3, so the top rung binds hardest and the final level collapses.
A growth-ratio extrapolation cannot see that, and I used one.

**(ii) Their stall was at 90% of completion.** 10.18 M of 11.28 M nodes — about **39 seconds**
short. "A budget finding, not a difficulty finding" was right and understated.

**(iii) The speedup over Woodall is between 36× and ~2,200×, not 3–8×.** 4 hours ÷ 397 s = 36.3×,
and that is the *floor*, because it assumes he traversed the same tree. Their leaf count is 60.19
× Woodall's 13,448 classes, so an orbit-complete canonical form on his side means a tree of ~1.87
× 10⁵ nodes, ~13 nodes/s in 1988, and a speedup of ~2,200×. My 3–8× came from back-computing him
on a tree 32× too large.

**(iv) So the 5–10 month (11,7) figure is void**, along with the claim that `P-43`(A)'s 30 days
fails at the measured throughput. The replacement is being measured now, not estimated: the (9,7)
run is in flight, which gives the real (7,7) → (9,7) scaling in place of the 4,838× raw-space proxy.

**(v) The "720" retraction.** I corrected them for treating 720 as a group order. They never did.
`relabel_maps()` returns **2·n! = 10,080** maps, verified distinct; `stabiliser()` returns the
dihedral group of order **2n = 14**; and `class_canon` is orbit-complete under the full 10,080 —
checked against brute force on 40 samples. Their 720 is **(m−1)! = 6!**, the naive expectation for
what prefix-minimality would buy, against which its measured ~1.5× is the surprise. That
(n−1)! = (m−1)! = 720 here is a coincidence of n = m = 7. The "shortfall of 241×" I attached to
their 20.9× is likewise withdrawn: 20.9 ≈ 13.8 × 1.5 is the measured product of the stabiliser
clause and prefix-minimality, and 13.8 of a theoretical 14 is near-optimal, not deficient.

**(vi) The three-for-three "mismatch" was me comparing node counts against class counts.** Their
level counts are exactly right — the depth-5 prefix reproduces here to the digit. The search's
node-keep predicate canonicalises under **Stab(v₀) alone, order 14**, not the full group of order
10,080, and that is documented clause by clause in `search.py` with its own ablation
(195,110 / 129,044 / 14,119 / 9,333 on (5,7)). Against the right group all three of my figures are
*surpluses*, monotone in depth — 13/11 = 1.18×, 377/158 = 2.39×, 29,099/6,387 = 4.56× — well under
the 10,080/14 = 720× ceiling such a predicate allows. The "level 1 is a deficit, so no single
cause covers all three" observation is withdrawn: it was an artefact of comparing against S₇
(5,040) when their code uses 10,080.

## 4. `P-44`, resolved

| | | |
|---|---|---|
| **(A)** the index set is the culprit | **TRUE** | and the mechanism is the node-keep predicate's group, not an offset; the offset re-reading that would have made the tree 8.8 × 10⁹ nodes is dead |
| **(B)** the canonical form is not orbit-complete | **SPLIT** | true of the node-keep predicate that produced the counts, **false** of `class_canon`, which is correct. My wording did not distinguish them and the codebase has both. Scored as the weaker of the two readings: not a clean hit |
| **(C)** my CO₇ is right | **TRUE** | same vertex list, same distance matrix, same antipode map, same antidistance matrix to all 518,400 entries |
| **(D)** the tree size moves by > 2× | **TRUE** | 32×, and in the direction I explicitly declined to predict. Declining was right: an hour earlier I would have guessed larger |

The unevaluable branch did not fire — the node-keep predicate arrived as code.

## 5. What `D67` actually bought

The finding stands and is now demonstrated rather than argued. Nine relay rounds and three local
computations failed to identify the index set; **400 seconds of running their code identified it,
and the predicate was documented in full the whole time** — in `search.py`'s docstring and the
README, neither of which was ever relayed. A summary cannot carry an index set. The corollary is
the sharper half: I built three cross-level comparisons, a bound-free ladder and a pre-registration
on top of a quantity I had misidentified, and every one of those artefacts was internally correct.
**Rigour downstream of a misidentified quantity is not a safeguard.** The only thing that caught it
was obtaining the instrument.

## 6. The bigger result: Theorem 7 is net negative

Running (7,7) to full depth with Theorem 7 **off** closes item 3 on their own
not-established list, and it inverts the conclusion of the entire eight-round correspondence.

| | Theorem 7 ON | OFF |
|---|---|---|
| levels | 1 · 12 · 329 · 25,346 · 615,817 · 9,827,953 · **809,438** | 1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · **809,438** |
| total nodes | 11,278,896 | 16,263,610 |
| wall clock | **397 s** | **186 s** |
| nodes/s | 28,410 | 87,391 |

**The leaf counts are identical — 809,438 both ways.** That is a correctness check on the prune:
Theorem 7 may only remove interior nodes that cannot reach a survivor, and it removed exactly
those.

* tree shrink from Theorem 7, at full depth: **1.442×** (their depth-5 cumulative figure was
  1.295×);
* per-node cost: **3.08×**;
* **net wall clock: 2.13× slower with it on.**

So the device whose availability at m = 11 consumed eight rounds, and whose measured 1.30× moved
**H** from UNDETERMINED to PASS, **is a prune that should be switched off.** At m = 11 its scan is
C(k−1,3) = 120 triples against 20 at m = 7, so its unavailability there is a *saving*, not the
cost the headroom argument priced in. The weakened-Theorem-7 rescue that priced out net-negative
at 1.0006× shrink against 2.21× cost was the right verdict for the wrong reason: the full prune is
net-negative too.

## 7. How long will (9,7) take? A bracket, not a number

The depth-5 probe completed: **1 · 13 · 2,131 · 82,308 · 6,540,999** in 111 s, Theorem 7 on. Per
level against (7,7): 1.08×, 6.48×, 3.25×, 10.62×. The 6.48× at level 3 is independently expected —
the orbit count of 3-element sets jumps 280 → 1,710 as the bound moves 9 → 11, a factor of 6.1.

| anchor | implies | verdict |
|---|---|---|
| Woodall's own 4 h → 6 h, a 1.5× ratio | ~600 s with Theorem 7 on | **too optimistic.** (9,7) has already visited 59% of the *entire* (7,7) tree by level 5, with four levels to go against (7,7)'s two |
| level-5 ratio 10.6×, applied to the total | ~1.2 × 10⁸ nodes, ~30 min | the floor |
| the (7,7) shape, total/L5 = 18.3, times two extra levels at ~8× and ~4× | ~4 × 10⁹ nodes, ~18 h | the ceiling |
| raw multiset space (9,7)/(7,7) = 7,351× | meaningless — pruning removes almost all of it | discarded |

**Depth 6 has since completed**, Theorem 7 off, in 456 s: **1 · 13 · 2,131 · 82,512 · 6,655,827 ·
50,599,405**, 57,339,889 nodes at 125,730 nodes/s. That narrows the bracket and points downward.

The informative comparison is not level against level but **distance from the top rung**, since the
top rung is what binds:

| levels from the top | (7,7) growth ratio | (9,7) growth ratio |
|---|---|---|
| 0 | 0.055 | unmeasured |
| 1 | 18.2 | unmeasured |
| 2 | 27.5 | unmeasured |
| 3 | **77.2** | **7.6** |
| 4 | 29 | 80.7 |

At three-from-top the (9,7) tree is growing **ten times more slowly** than (7,7) was at the same
distance. Deceleration is arriving much earlier relative to the top, which is the encouraging
direction. Carrying the three remaining levels at plausible ratios:

| | total nodes | wall clock |
|---|---|---|
| pessimistic (7.6, 4, 0.06) | 2.1 × 10⁹ | 275 min |
| central (3, 1, 0.05) | 3.7 × 10⁸ | **49 min** |
| optimistic (2, 0.5, 0.05) | 2.1 × 10⁸ | 28 min |

**So: 28–275 minutes, central around 50.** That is still a bracket and not a number, and I am not
narrowing it further by extrapolation — that is precisely the error that cost 32× in §3(i), and the
top level contracts by a factor nothing shallower predicts. A **depth-7** run is in flight; depth
caps complete and give exact counts, whereas a time-capped abort gives none, because a DFS that
runs out of clock has visited no level completely.

## 8. In flight

* **(9,7), Theorem 7 off, depth 7** — the next exact level, which collapses §7's bracket. The
  Theorem-7-on full-depth attempt was stopped once §6 showed the prune costs 2.13× in wall clock:
  there is no reason to measure the slower configuration first.

`P-44` is graded **partly** in the ledger, not correct — (A), (C) and (D) hit and (B) splits, and a
split is scored as the weaker reading. `P-43`(A)'s 30-day threshold is now **open and no longer at
risk for any reason on file**, which is the first time that has been true.

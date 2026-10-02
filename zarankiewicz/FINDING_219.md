# One isomorphism class at antisum 219

The sweep's first result bearing directly on the conjecture.

Three distinct (11,7)-multisets, all in **one isomorphism class**
under the full automorphism group (`cog.class_canon`, order 10,080). Canonical form:

```
(0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)
```

The three multisets, each with the shard that found it:

```
found by shards     canonical multiset                                      repeat
 5, 6, 53           0 121 122 143 174 454 454 564 609 712 716               454 twice
25, 84              0  21  91  91 143 287 289 303 311 452 569                91 twice
25, 123             0   0  21  91 143 239 289 303 359 452 569                 0 twice
```

Every one is a **multiset**, not a set — a vertex repeats in each. That is admissible: Woodall's
(m,n)-sets are multisets. The canonical form repeats vertex 0 accordingly.

`sweep_L5/ANTISUM_219.txt`. Antisum **independently recomputed** for every emitted tuple from the
Python's own antidistance matrix — the construction that reproduced Woodall's published *n* = 4
antidistances and his 13,448 — and every one agrees at exactly 219, so this does not rest on the
C's arithmetic alone.

## Counting: nodes, multisets, classes

The pooled histogram counts **emitted nodes**, and a node is an ordered insertion sequence, so the
219 entry has grown 4 -> 24 (shard 25) -> 28 (shard 53) -> 32 (shard 84) -> 36 (shard 123)
**without a second class ever appearing**, and only shard 25 ever contributed a multiset that was
new: 53, 84 and 123 each added four more orderings of one already seen. Every one of the three
multisets has now been found by at least two widely separated shards.

**This file does not get edited every time that bin ticks.** The node count is a search-tree
statistic that changes whenever another level-5 prefix happens to reach the same objects;
`verify_219.py` recomputes nodes, multisets and classes from the committed survivor files on
demand, and that is the authority. What would justify an edit here is a **new class**, or anything
at antisum 217 or below. Three numbers,
three meanings:

| | |
|---|---|
| emitted nodes at 219 | 36 as of 45f1f2c; run `verify_219.py` for the live count |
| distinct multisets | 3 |
| isomorphism classes | **1** |

The node growth is ordering multiplicity plus two further multisets of the same class, not new
mathematical content. The (7,7) control showed the same thing at full strength: 809,438 emitted
leaves collapsed to Woodall's 13,448 classes, a 60.2x duplication. Report the class count; the node
count is a search-tree statistic.

## Where it sits

| | |
|---|---|
| Z(11)Z(7) | **225** |
| staircase top rung (parity makes the rungs odd) | 223 |
| this class | **219**, a deficit of **6** below Z |

The pooled histogram over 125 shards: `{219: 36, 221: 2,949,594, 223: 17,755,384,762}` — 0.0166% of
17,758,334,392 leaves sit below the top rung, and this class is still the only thing below 221.
That fraction has held between 0.0166% and 0.0184% from 7 shards to 125.

**The other instance reported "nothing yet seen at 219."** Their frontier run had aborted, so they
flagged the whole distribution as a truncated-DFS artifact rather than a measurement. One hundred and twenty-five
completed shards now put something there.

## What it is not

**Antisum lower-bounds crossings.** A set at antisum 219 corresponds to a drawing with **at least**
219 crossings, so on its own it refutes nothing — cr(K₇,₁₁) = 225 would be perfectly consistent
with it. It is a counterexample only if it is **realisable as an actual drawing with fewer than 225
crossings**, and realisability is the open step: that is exactly the direction Woodall had to
discharge for his 13,448 classes at (7,7), and the reason the sweep emits survivors rather than
just counting them.

So: the strongest candidate the sweep has produced, one class, verified twice, and **not** a result
about the conjecture yet.

## The obvious next step, not yet taken

`generator.py`'s `realise()` finds a straight-line drawing inducing an isomorphic copy of a target
(m,n)-set, and `total_crossings` counts crossings exactly. Running them on this class is hours, not
days, and would either produce a self-certifying drawing or establish that this candidate is not
rectilinearly realisable. **I have not run it** — the sweep is the committed task and this appeared
in the middle of it.

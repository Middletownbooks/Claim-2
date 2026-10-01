# One isomorphism class at antisum 219

The sweep's first result bearing directly on the conjecture.

```
219,0,143,716,454,121,564,609,174,712,122,454
219,0,143,716,454,121,712,174,609,564,122,454
219,0,143,716,454,122,564,609,174,712,121,454
219,0,143,716,454,122,712,174,609,564,121,454
```

Four nodes, **one isomorphism class** under the full automorphism group
(`cog.class_canon`, order 10,080). An **(11,7)-multiset**, not a set — vertex 454 appears twice,
which is admissible: Woodall's (m,n)-sets are multisets.

`sweep_L5/ANTISUM_219.txt`. Antisum **independently recomputed** from the Python's own
antidistance matrix — the construction that reproduced Woodall's published *n* = 4 antidistances
and his 13,448 — and all four agree at exactly 219, so this does not rest on the C's arithmetic
alone.

## Where it sits

| | |
|---|---|
| Z(11)Z(7) | **225** |
| staircase top rung (parity makes the rungs odd) | 223 |
| this class | **219**, a deficit of **6** below Z |

The pooled histogram over 7 shards: `{219: 4, 221: 194,175, 223: 1,060,484,825}` — 0.0183% of
1,060,679,004 leaves sit below the top rung, and this is the only thing below 221.

**The other instance reported "nothing yet seen at 219."** Their frontier run had aborted, so they
flagged the whole distribution as a truncated-DFS artifact rather than a measurement. Seven
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

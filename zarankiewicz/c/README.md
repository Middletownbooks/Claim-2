# `zsearch` — the C implementation

A port of the received `search.py` node-keep predicate and DFS. **24.3× faster on the gate**, and
the gate is the point: it reproduces the exact level counts measured from the Python, in both
Theorem 7 configurations, or it is wrong however fast it is.

```
make
./zsearch -m 7  -n 7                 # the gate, Theorem 7 off
./zsearch -m 7  -n 7 -thm7 24        # the gate, Theorem 7 via m' = 2 and 4
./zsearch -m 11 -n 7 -d 6            # depth-capped
./zsearch -m 11 -n 7 -start 0,13,97  # resume from a prefix: this is a shard
./zsearch -m 11 -n 7 -top 221        # lower the top rung: the refutation sweep
```

| flag | |
|---|---|
| `-m`, `-n` | the (m,n) case; CO_n is built for n |
| `-d` | depth cap. **Use this and not `-cap`** when the counts matter |
| `-cap` | wall-clock seconds. Sets `aborted` and `level_counts_valid: false` |
| `-top` | override the top staircase rung |
| `-thm7` | a string containing `2`, `4`, or both. **Default off, and it should stay off** |
| `-start` | comma-separated prefix to resume from |

## The gate

| | level counts | total | Python | C | speedup |
|---|---|---|---|---|---|
| (7,7) Thm 7 off | 1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · 809,438 | 16,263,610 | 186.1 s | **7.65 s** | **24.3×** |
| (7,7) Thm 7 on | 1 · 12 · 329 · 25,346 · 615,817 · 9,827,953 · 809,438 | 11,278,896 | 397.0 s | **5.60 s** | **70.9×** |

Both exact. `GATE_VALUES.json` holds the full set and `check_gate.py` runs the Python against it;
these two rows are the C's half.

## What the speedup came from, and what it did not

The first working version was **7.8×**, and the three things that got it to 24× are worth recording
because two of them are counter-intuitive.

1. **`int16` throughout.** Antisums cap at 223 and antidistances at 9, so the row and the
   antidistance matrix both fit in `int16`. The received Python keeps the row as `int32` and the
   matrix as Python ints; the inner pass mixes `int32` and `uint8`, which does not vectorise. In
   `int16` the same loop issues 16 lanes at a time.
2. **A compact candidate list made it *slower*, and was reverted.** Keeping only
   `{w : row[w] ≤ B[m]}` and iterating that shrinking list saves iterations — but it turns the
   inner pass into a **gather**, `Av[cl[i]]` instead of `Av[i]`, and a gather does not vectorise. It
   bought 14% where the dense version bought 24×. **Compaction that saves iterations but
   introduces indirection is usually a loss**, and it is only the gate that made the comparison
   legible at all.
3. **Compaction *is* right for the candidate index list**, whose consumers — prefix-minimality and
   the stabiliser clause — are per-candidate and few, so indirection costs nothing there. Same
   technique, opposite verdict, decided by where the loop is hot.

A fourth change is free and sound: prefix-minimality says the new element's contribution must
dominate every existing one, so `row[v] = S + cv ≥ S + maxᵢ coᵢ`. That is a **lower** bound on a
viable candidate, so the scan is a two-sided window rather than a one-sided test.

## Faithfulness notes

The port is deliberately literal where literalness matters.

* **Vertex order.** `cog.c` reproduces Python's `permutations(range(1,n))` ordering exactly,
  because clause (3) compares vertex **indices** — a different ordering changes which nodes
  survive, silently.
* **`buf[1]`, not `buf[0]`.** The Python's `buf[1] = A_np[0]` initialises the row for *level 1*.
  Writing it to level 0 left the search scanning uninitialised memory, which the first gate run
  caught: level counts came back `1, 1, 39, 3767, 518497, 42029325, 1332040127` instead. **That is
  what the gate is for** — the wrong version ran happily at 2.7 M nodes/s and produced a complete,
  plausible-looking, entirely fictional tree.
* **Theorem 7 defaults off**, because the full-depth ablation measured it at 1.442× tree shrink
  against 3.08× per-node cost, i.e. **2.13× net slower**. It is implemented only for gate fidelity.

## Parallel efficiency is poor, measured

| | |
|---|---|
| single process, (7,7) full | 16,263,610 nodes in **7.65 s** = 2.13 M nodes/s |
| 4 shards, same tree | 16,263,610 nodes in **23.9 core-seconds** = 680 k nodes/s per core |
| speedup from 4 cores | **1.28× of a possible 4×, i.e. 32% efficiency** |

**Cause**: each process holds its own 1 MB copy of the `int16` antidistance matrix, so four copies
thrash the shared cache. **Fix**: threads with one shared read-only matrix. Not done — recorded
because **the core-hour budget has to be scored on the sharded rate, not the single-process one**,
and that is the difference between comfortably inside the budget and over it:

| rate used | (11,7) at 8.78 × 10¹² nodes | vs the 2,880 budget |
|---|---|---|
| (11,7) depth-6 mix, mostly update loops | 272 core-hours | inside |
| single process, (7,7)-like mix | 1,145 core-hours | inside |
| **per core under 4-way sharding** | **3,583 core-hours** | **over** |

So the C puts (11,7) somewhere around **300–3,600 core-hours against a 2,880 budget** — a pass on
the optimistic mix and a near-miss on the pessimistic one. **Not yet a settled pass**, and threads
are what would move the pessimistic end.

## A rate that flatters itself

`nodes/s` is a misleading metric here and the depth-6 (11,7) run shows why: it reports **8.98 M
nodes/s**, four times the (7,7) gate's 2.13 M, because 433 M of its 440 M nodes sit *at* the depth
cap, where `rec` returns immediately without scanning or updating. The honest unit is the
**720-wide pass** — one per candidate scan and one per row update — and quoting nodes/s across runs
with different depth profiles compares different amounts of work.

## Sharding

`-startfile <path> -shard i -of N` streams one prefix per line and takes lines `i, i+N, …`, so
setup is paid once per shard rather than once per prefix. **Gated**: four shards of the (7,7)
level-4 frontier, summed, give `1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · 809,438` — the exact
counts, with levels 1–3 from the frontier pass and 4–7 from the shards.

`-start` makes a single prefix a complete task, because the only state a node needs is its prefix:
the contributions, the antisum and the row are all recomputable from it. `../shard.py` generates the
frontier of prefixes at a chosen level and the Python merge logic applies unchanged — the C prints
the same level-count vector, so a shard's output sums the same way.

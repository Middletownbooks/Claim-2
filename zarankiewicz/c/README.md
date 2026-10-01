# `zsearch` — the C implementation

A port of the received `search.py` node-keep predicate and DFS. **15.95× faster on the gate**,
measured uncontended on one host — see `../BENCHMARK.md`, which retracts an earlier 24.3× taken
from two contended runs on a different container. The gate is the point: it reproduces the exact level counts measured from the Python, in both
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
| (7,7) Thm 7 off | 1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · 809,438 | 16,263,610 | 165.6 s | **10.38 s** | **15.95×** |
| (7,7) Thm 7 on | 1 · 12 · 329 · 25,346 · 615,817 · 9,827,953 · 809,438 | 11,278,896 | 393.2 s | **8.06 s** | **48.78×** |

Both uncontended, same host, best of three. The earlier table gave 24.3× and 70.9× from contended
runs on a different container; those are withdrawn.

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

## Threads, and a retraction of my own benchmark

`-threads T` runs T worker threads over one shared, read-only antidistance matrix, pulling prefixes
from an **atomic queue rather than a static stripe** — subtree sizes here span max/mean = 37, so a
stripe leaves threads idle on the tail. All mutable state (row stack, prefix, contributions,
counters) is per-worker and small: 23 KB each.

**Gated.** T = 1, 2 and 4 give **bit-identical level counts**, and each sums with the frontier pass
to the exact vector `1 · 13 · 377 · 29,099 · 801,503 · 14,623,179 · 809,438`.

### The clean benchmark, one binary, nodes per core-second

| workload | 1 core | threads | processes | threads vs 1 | threads vs procs |
|---|---|---|---|---|---|
| (7,7) full, 4 cores | 1,804,080 | **1,816,651** | 1,435,412 | **1.01×** | **1.27×** |
| (11,7), 3 cores | 1,915,577 | 1,865,073 | 1,985,178 | 0.97× | 0.94× |

Those two rows were themselves taken under contention. The clean sequential curve in
`../BENCHMARK.md` supersedes them for absolute rates: 1,924,549 nodes/core-s at T = 1 falling to
1,821,979 at T = 4, a **3.60× speedup at 95% per-core efficiency**.

**So threads scale essentially perfectly per core — 101% on (7,7), 97% on (11,7) — and the win over
processes is 1.27× on one workload and nil on the other.**

> **RETRACTION.** An earlier version of this file said process sharding ran at **32% parallel
> efficiency** and that threads would take it to **106%**, a 3.3× claim. **Both numbers are
> withdrawn.** The 32% came from the *old pre-`int16` binary*'s process run (680 k nodes/core-s)
> compared against the *new threaded* binary — two different programs. Same binary, same core
> count, the honest figure is the table above. This is the same methodology error I spent the day
> recording in `D68`: I compared across a change I had just made, exactly as I did when I pinned a
> node threshold to a rate I was about to improve tenfold.

Why (7,7) benefits and (11,7) does not, as far as the measurements support: (11,7)'s work is
dominated by deep row-update passes touching one matrix row at a time, which has good locality
whether the matrix is shared or duplicated; (7,7)'s is scan-heavier and touches more of the matrix,
so four duplicate copies cost it. Plausible and consistent with the numbers, not separately tested.

**The real benefit of threads here is operational, not arithmetic**: one process, one output file,
one gate run per session, and dynamic load balancing across subtrees that differ by 37× — which is
what a wall-clock-capped notebook session actually needs.

### A caveat on every (11,7) rate in this file

They were measured while other jobs were running on the same four cores, at varying levels. The
*gated counts* are exact regardless; the *rates* carry that noise, and the 4-core (11,7) figure of
1,149,393 nodes/core-s is the most contended of them. It is nonetheless the one the budget uses,
because a real sweep saturates the machine too.

## A rate that flatters itself

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

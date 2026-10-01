# Can C run in a Kaggle notebook? Yes — and here is the thing that proves it on the day

**Short answer: yes.** A Kaggle notebook is a Jupyter kernel in a Debian/Ubuntu container, shell
commands work with `!` or `%%bash`, and the Kaggle Python image ships a C toolchain. Nothing about
the problem needs Python at all beyond orchestration: `zsearch` now dumps its own frontier, so the
whole job is one binary.

**But I am not going to assert the two details that actually decide it**, because they are exactly
the kind of thing that changes without announcement and that I would be guessing at: whether `cc`
is on the image *today*, and whether the filesystem you build on is mounted `noexec`. A `noexec`
mount is the one plausible blocker — you can write a binary and still not be allowed to run it —
and it is cheaper to test than to look up.

So `kaggle_shard.py` **probes for both and routes around them**. Run it; the first dozen lines tell
you the answer for your account on the day:

```
=== environment ===
python     : 3.11.15
cpus       : 4
compiler   : cc -> cc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
memory     : 16094 MB
exec from  : /kaggle/working    NO ([Errno 2] No such file or directory: ...)
exec from  : /tmp               YES
free disk  : 27 GB on /
built /tmp/zbuild/zsearch
```

That is a real run of this script, here, where `/kaggle/working` does not exist — and it **fell
back to `/tmp` and carried on**. On Kaggle it will find `/kaggle/working`; if that mount refuses to
execute, the same fallback takes over. If no compiler is found it prints the one-line `apt-get`
that fixes it. If no filesystem will execute a fresh binary it stops and says so, rather than
failing obscurely later.

## Two modes — run `calibrate` first

```python
!ZMODE=calibrate python /kaggle/input/<your-dataset>/kaggle_shard.py
```

**Twenty minutes, and it answers the only question worth asking before committing
sessions: what is this host actually worth?** It probes, builds, gates, then runs a **fixed,
deterministic work quantum** — every (N/384)th level-5 prefix, first 384, reproducible from the
frontier alone on any machine — at 1, 2, 4… threads, and prints the core-hour and session count
implied by *this host's own measured rate*. `ZQUANTUM=16` makes it a two-minute smoke test first.

Then, and only then:

```python
!ZMODE=sweep ZFIRST=0 ZCOUNT=40 python /kaggle/input/<your-dataset>/kaggle_shard.py
```

## The reference is a range, not a number

The same gate on this account's own containers has measured **6.47, 7.65 and 10.38 seconds** — a
**1.60× spread on bit-identical work**, the slow end from a container that had been up four hours.
Its sweep rate over that life fell 31% and recovered fully on restart.

So a Kaggle gate time tells you **which end of this account's own spread the host resembles, and
nothing finer.** The script reports it that way: *inside the range measured there*, *faster than
anything measured there*, *slower*. An earlier version compared against the single figure 10.38 s
and would have reported a perfectly ordinary host as 1.6× fast. The core-hour figure is the
trustworthy output, because it divides the tree size by **this host's** rate rather than by a
remembered one.

## Using it

One cell:

```python
!python /kaggle/input/<your-dataset>/kaggle_shard.py
```

or paste the script into a cell. Configuration is by environment variable, so nothing inside needs
editing:

| | default | |
|---|---|---|
| `ZMODE` | calibrate | `calibrate` or `sweep` |
| `ZM` | 11 | the (m,7) case |
| `ZLEVEL` | **5** | split level — 4 leaves shards at 1.88 of 4 cores, 5 gives 3.84 |
| `ZQUANTUM` | 384 | calibration quantum; lower it for a smoke test |
| `ZNSHARDS` | 1000 | total shards the work is cut into |
| `ZFIRST` / `ZCOUNT` | 0 / all | which shards *this session* takes |
| `ZTHREADS` | all cores | |
| `ZWALL` | 39600 s | stop *starting* shards after this — 11 h, inside the 12 h session limit |
| `ZOUT` | `/kaggle/working/zout` | one JSON per completed shard |
| `ZPREV` | `/kaggle/input` | earlier sessions' outputs, scanned so completed shards are skipped |

**Across sessions**: session *k* runs with `ZFIRST=` its slice, and its `/kaggle/working/zout` is
saved as the notebook's output. Attach that output as a *dataset input* to the next session and
`ZPREV` picks it up, so completed shards are skipped automatically and a session killed by the wall
clock loses **at most one shard**.

**`ZNSHARDS=2400` is right at level 5**: ~2,774 prefixes per shard, ~4 × 10⁹ nodes, about ten
minutes on four cores, and measured at **3.95 of 4 cores** in production. Do not raise it much —
with 8 tiny shards thread spawn/join dominated and the per-core rate halved.

**Watch the per-shard rate.** `ZMODE=sweep` prints each shard's nodes/core-s as a ratio of the
first shard's and flags `<-- RATE FALLING` below 0.9×, and it re-runs the gate at the end of the
session. That is there because the rate fell 31% over four hours once and nothing in the output
would otherwise have shown it.

## What it refuses to do

It **runs the gate before it does any work** and exits if either configuration is off by a single
node:

```
=== gate: the exact (7,7) level counts, or we stop ===
  thm7=off [1, 13, 377, 29099, 801503, 14623179, 809438]  ok  (10.4 s)
  thm7=24  [1, 12, 329, 25346, 615817, 9827953, 809438]  ok  (8.2 s)
  gate passed
```

That costs ~19 s per session and is not optional. The first working version of this C ran happily
at 2.7 M nodes/s and produced a complete, plausible, entirely fictional tree because it scanned
uninitialised memory; nothing but the gate would have caught it, and a notebook on someone else's
machine is the last place to find out.

## The script is generated, not hand-maintained

`make_bundle.py` embeds `cog.h`, `cog.c` and `search.c` by reading them, and stamps a digest of
what it embedded into the output and into every shard JSON. A hand-copied duplicate would drift
from the originals and **the drift would be invisible** — the notebook would still build, still
print level counts, and still be wrong. Regenerate after any change to the C:

```
python3 kaggle/make_bundle.py
```

## Verified locally, end to end

* probe → build → gate → frontier dump → shards → JSON per shard: **runs clean**;
* the C's own frontier dump is **identical as a set** to `shard.py`'s 29,099 prefixes;
* **8 shards merged reproduce the exact (7,7) counts**, `1 · 13 · 377 · 29,099 · 801,503 ·
  14,623,179 · 809,438`, with all 29,099 prefixes accounted for;
* **resume works**: re-running with 3 shards already present skipped them.

## The one thing I cannot test from here

Kaggle's own limits and terms. 12 hours per CPU session with no weekly CPU cap is what the docs
say, and ~41 sessions of 48 core-hours covers the sweep — but **that is a lot of free compute to
take from a free tier, and a rented VM for three weeks costs tens of dollars.** Your account, your
call; I am flagging it, not deciding it.

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

## Using it

One cell:

```python
!python /kaggle/input/<your-dataset>/kaggle_shard.py
```

or paste the script into a cell. Configuration is by environment variable, so nothing inside needs
editing:

| | default | |
|---|---|---|
| `ZM` | 11 | the (m,7) case |
| `ZLEVEL` | 4 | split level for the frontier |
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

**Pick `ZNSHARDS` so each shard runs for ten minutes or more.** In a local test with 8 shards each
took 0.6 s, and thread spawn/join then dominates — the per-core rate fell from 1.75 M to 0.8 M
nodes/s. For the real (11,7) run at ~1,980 core-hours, 1,000 shards is about 2 core-hours each,
which is the right granularity.

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

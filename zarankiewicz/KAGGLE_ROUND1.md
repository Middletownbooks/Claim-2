# Kaggle round 1: 133 shards in the upper half, and nothing below 219

Five parallel Kaggle sessions, `RUN="sweep"`, `SLOT` 0..4, `NSLOTS=5` over shards
800..2399, each stopped by the 11 h `ZWALL` inside Kaggle's 12 h cap. Reported by the
driver's own session-summary line, which is computed from the shard certificates it
wrote:

| slot | shards | count | wall | lowest antisum seen |
|---|---|---|---|---|
| 0 | 800..827   | 28 | 40,159.8 s | **219** |
| 1 | 1120..1153 | 34 | 40,173.0 s | **219** |
| 2 | 1440..1460 | 21 | 41,421.9 s | 221 |
| 3 | 1760..1780 | 21 | 41,413.9 s | 221 |
| 4 | 2080..2108 | 29 | 40,467.4 s | **219** |
| | | **133** | | |

## What this establishes

**Nothing below 219, across 133 shards of the tree this container has not touched.**
Local work covers shards 0..200; these cover 800..2108 in five disjoint blocks. The
lowest antisum in the whole programme is still 219, and it is now tested in a part of
the tree reached by a different binary, built by a different compiler, on a different
host.

**219 is not confined to low-index shards.** It appears in three widely separated
regions — the 800s, the 1120s and the 2080s — where before it was known only from
shards 5..200. Two of the five blocks (1440..1460, 1760..1780) bottom out at 221,
so it is not everywhere either.

## What this does NOT establish, and it is the question that matters

**Whether the Kaggle 219s are the same isomorphism class as the local one.** The
session line reports the lowest antisum, not the multiset. Locally all 61 rows at 219
canonicalise to a single class, `(0,0,15,74,105,438,569,647,660,671,689)`; a Kaggle
219 in a DIFFERENT class would be the first new class in the programme and is the one
outcome here that would be news. Settling it needs the actual rows, which are 12
comma-separated integers each — `grep -h '^219,' zout/low_*.txt | sort -u` prints them
as text, no file transfer required.

## Coverage map

Open gaps in the Kaggle half, 1,467 of 1,600 shards:

```
 828..1119   292
1154..1439   286
1461..1759   299
1781..2079   299
2109..2399   291
```

## The node total is NOT merged yet

133 shards at the local average of 4.180e9 nodes/shard would be about 5.56e11, which
with the local 8.4016e11 would be 1.396e12, or 13.28% of the 1.0510e13 estimate. **That
is an estimate from a local average and is not a measurement** — per-shard node counts
vary, and the real figures are in the `sh_m11_L5_*of2400.json` certificates. No
percentage from this paragraph should be quoted as progress until those are merged.

## Round 2 and the resume problem

Round 2 was launched by moving `SLOT_FROM` to each slot's resume point while leaving
`NSLOTS=5`. That does not resume: the block re-divides the given range into `NSLOTS`
pieces and takes the SLOT-th one,

```python
_base, _extra = divmod(_hi - _lo, NSLOTS)
FIRST = _lo + SLOT * _base + min(SLOT, _extra)
```

so SLOT=0 collapses to `FIRST = _lo` and resumes correctly while every higher slot
jumps forward by roughly `SLOT * (range/5)`. With `SLOT_FROM=1151`, slot 1 started at
1401, not 1151.

**Nothing is lost by it.** `NSHARDS` stayed 2400 and the C is invoked `-shard i -of
2400`, so shard *i* denotes the same subtree in every session and every round. Each
round-2 session is working a correctly-partitioned, mutually disjoint block inside
800..2399; the cost is gaps, not corruption, and gaps are indistinguishable from
not-yet-done. Overlaps would also be harmless — determinism is verified exactly against
`sh_12.json`, so a redone shard reproduces identical counts, and merging dedupes by
index. Slot 1's resume point was set to 1151 against an actual end of 1153, so shards
1151..1153 may be done twice; that is three shards.

## Two fixes, and the second solves the download problem too

**Exact ranges, no dataset.** The slot block is guarded by
`if NSLOTS > 1 and "ZFIRST" not in os.environ and "ZCOUNT" not in os.environ`, so
setting `ZFIRST` bypasses it entirely and `SLOT`/`NSLOTS`/`SLOT_FROM`/`SLOT_UPTO` can be
left alone:

```
!ZFIRST=1154 ZCOUNT=300 ZMODE=sweep python /kaggle/working/kaggle_shard.py
```

**The resume dataset is already wired.** `ZPREV` defaults to `/kaggle/input`, which is
where Kaggle mounts attached datasets, and the scan is `rglob`, so the certificates are
found at any depth with no configuration. It reads only
`sh_m11_L5_*of2400.json` and skips on `complete: true`, which means **the resume dataset
can be built from the ~440-byte certificates alone** — the 1.2-1.6 MB `low_*.txt` files
do not need to be in it. A five-session resume dataset is on the order of 60 KB, which
is also why this is the path of least resistance when a 40 MB output will not download.

## A cross-implementation check, from a hand-pasted sample of shard 813

The operator could not download shard 813's survivor file but pasted a portion of it.
All the pasted rows are 221s. Twenty-one of them, carrying 15 distinct multisets, were
checked against **this container's** antidistance matrix (`intake/cog.py`, `CO(7)`,
`antidist_matrix`) rather than against the C that produced them:

| | |
|---|---|
| rows checked | 21 |
| antisum agrees with the claimed 221 | **21** |
| mismatches | **0** |
| all vertices in range 0..719 | yes |
| multiset size 11 everywhere | yes |

The Kaggle binary is rebuilt in-session from the same source digest by a different
compiler with `-march=native` on different hardware. Until now the only check on that
build was the (7,7) gate, which is a fixed self-test. This is the first time its
**production output** has been verified by an independent implementation, and the
agreement is exact on every row sampled.

It is a narrow claim and should stay narrow: 21 rows, one shard, all of them 221s. It
does not verify any 219, and it is not a substitute for merging the certificates.

## Finding the 219 rows in a survivor file by eye

Worth recording because the obvious search string does not work. Every survivor row is
`<antisum>,v0,...,v10` and **v0 is always 0** — checked across all 449,969 local rows,
zero exceptions — so a 219 row always begins `219,0,`. But `219` is also a legal vertex
label, and in the local files:

```
219 appearing anywhere as a vertex   16,448 times
the substring ",219,0," mid-row         204 times
rows that actually start with "219,"      61
```

So searching a survivor file for `219,0,` finds roughly three decoys for every real row.
The discriminator is what precedes it: a real row starts a line, a decoy is preceded by a
comma. In a viewer that has lost the line breaks and shows rows separated by spaces,
**search for `219,` with a leading space** — within a row the separators are commas, never
spaces, so a space followed by `219,` can only be a row start.

Cheaper still, where the file can be listed but not read: `sh_m11_L5_<i>of2400.json` is
about 440 bytes and carries the antisum histogram, which gives the exact number of 219
rows in that shard without touching the survivor file.

## The question is answered: the Kaggle 219s are the SAME isomorphism class

Eleven rows at antisum 219, hand-transcribed from shard 813's survivor file by searching
for a leading-space `219,`. Checked against **this container's** `CO(7)` antidistance
matrix and canonicalised with its `class_canon`:

| | |
|---|---|
| rows | 11 |
| antisum agrees with the claimed 219 | **11 of 11**, 0 mismatches |
| distinct multisets among them | **3** |
| distinct isomorphism classes | **1** |
| that class | `(0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)` |
| the local class, from 73 rows over six multisets | **the same tuple** |

The three multisets, none of which appears in the local data — **overlap with the local
six is zero**:

```
4 rows  151 twice   0  95 105 118 151 151 159 239 417 451 623
4 rows  594 twice   0  20  25  95 121 415 479 513 593 594 594
3 rows  105 twice   0  95 105 105 118 151 159 177 239 451 567
```

### Why this is worth more than the eleven rows

Before this, "exactly one isomorphism class at 219" was a statement about **one
contiguous stretch of the tree** (local shards 5..208) computed by **one binary**. It is
now a statement about shard indices from 5 to 813, across **nine distinct multisets**, from
**two independently built binaries** on different hardware with different compilers and
flags. Three multisets never seen locally arrived from 600 shards away and landed on the
same canonical form.

Running totals for the class: **84 rows, 9 multisets, 13 shards, 1 class.**

### A trap worth naming

`sweep_L5/ANTISUM_219.txt` is regenerated by `grep -h '^219,' sweep_L5/low_*.txt`, so it
is **local-only by construction** and these Kaggle rows must NOT be merged into it — the
next regeneration would silently drop them. They live in
`kaggle/rows/ANTISUM_219_shard813.txt` instead. Likewise `verify_219.py` globs
`sweep_L5/low_*.txt` and does not see them; its "73 rows / 1 class" is the local figure
and stays that way until Kaggle survivor files are actually merged into `sweep_L5/`.

## Shard 1131: same class a second time, two more new multisets

Twelve rows at 219 from shard 1131, in slot 1's range, transcribed the same way.

| | |
|---|---|
| rows | 12 |
| antisum agrees with the claimed 219 | **12 of 12**, 0 mismatches |
| distinct multisets | **2**, both new again |
| distinct isomorphism classes | **1**, the same tuple |

```
8 rows  567 twice   0  95 105 114 143 152 167 177 451 567 567
4 rows  451 twice   0  95 105 118 143 151 167 177 451 451 567
```

### The class, cumulatively

| | local | +813 | +1131 |
|---|---|---|---|
| rows | 73 | 84 | **96** |
| distinct multisets | 6 | 9 | **11** |
| shards | 12 | 13 | **14** |
| shard-index span | 5..208 | 5..813 | **5..1131** |
| isomorphism classes | 1 | 1 | **1** |

Eleven multisets, two independently built binaries, three hosts, shard indices spanning
more than a thousand, and every single row collapses to
`(0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689)`.

## The decoy ratio: two different questions, and the per-shard spread is a factor of twelve

The operator reported shard 813 having "over 350 instances of 219" to sort eleven rows
out of, and shard 1131 having only 17 to sort twelve out of. Both are consistent, and the
guidance above needs splitting rather than correcting:

* Searching **`219,0,`** — the string this file cautioned about — matches a decoy only
  where vertex 219 is immediately followed by vertex 0. That is the 204-vs-61, about
  **3:1**, figure.
* Searching bare **`219`** matches every one of the 16,448 vertex occurrences. Measured
  per local shard that has any real rows:

```
shard  53   4 real   296 total    73.0 : 1
shard 126   3 real   104 total    33.7 : 1
shard 199  12 real   342 total    27.5 : 1
shard 210   4 real   112 total    27.0 : 1
shard 127   7 real   182 total    25.0 : 1
shard   5   2 real    42 total    20.0 : 1
shard  84   4 real    63 total    14.8 : 1
shard 208  12 real   180 total    14.0 : 1
shard 200   3 real    38 total    11.7 : 1
shard  25  20 real   214 total     9.7 : 1
shard   6   2 real    21 total     9.5 : 1
shard 123   4 real    28 total     6.0 : 1
pooled     77 real  1622 total    20.1 : 1
```

Shard 813's ~32:1 sits inside that range; shard 1131's 0.4:1 is better than any local
shard and is luck. **The lesson is not that a number was wrong but that a pooled ratio
was offered as per-shard guidance when the per-shard spread is 6:1 to 73:1** — no point
estimate describes what one shard will feel like. The instruction that actually works is
unaffected, because a leading-space `219,` has no decoys at all.

## Shard 2088: the first multiset to repeat across the two implementations

Three rows at 219 from shard 2088, slot 4's range, hand-transcribed.

| | |
|---|---|
| rows | 3 |
| antisum agrees with the claimed 219 | **3 of 3**, 0 mismatches |
| distinct multisets | **1** |
| distinct isomorphism classes | **1**, the same tuple |
| new multisets | **0** |

```
3 rows  569 twice   0  21  22  91 143 287 300 311 452 569 569
```

That multiset was already in hand — from **local shard 208**. Every Kaggle row before
this one carried a multiset this container had never produced, which made the
cross-implementation agreement an agreement about *classes*. This is the first row where
the two binaries, on different hardware with different compilers, independently emitted
the *same eleven vertices*. Two shards 1,880 apart in the partition, found by two
programs, land on one multiset: a concrete instance of the node/class duplication the
(7,7) control measured in aggregate (809,438 leaves to 13,448 classes, 60.2x).

## How many multisets does the class contain? 5,040 — and this is not a measurement

Shard 2088 adding no new multiset is the second consecutive growth event to add none
(shard 210's four rows were the first). The tempting move was to pre-register a
saturation prediction: eleven multisets seen, growth events now coming up empty, so
guess where the count levels off and see.

That would have been the wrong instrument, because **the quantity is structural, not
empirical**. The class is one orbit of the automorphism group `S_7 x <rev>`, so the set
of multisets in it is finite, determined, and computable from `cog.py` alone — without
reference to any search output, on this host or Kaggle's.

```
group order (maps)                 10080
distinct multisets in the class     5040
stabiliser order                       2
orbit members whose antisum != 219     0
```

The stabiliser is `{identity, g}` where `g` lies in the `S_7` part (no reversal), fixes
vertex 0, and fixes 48 of the 720 vertices of CO(7). So **the class holds exactly 5,040
multisets, of which 11 have ever been seen: 0.22%.** No saturation is near, the two
empty growth events are what sampling 0.2% of a space looks like, and a pre-registered
prediction about where the count levels off would have been answering a question
arithmetic had already settled.

This is the counterpart to the lesson at the end of the error list: before measuring a
quantity, check whether some other part of the repository already determines it. Here
nothing had measured it — group theory *fixed* it, and three lines of code read it off.

### verify_219_orbit.py

`verify_219.py` answers "how many classes are in the local survivor files". The new
`verify_219_orbit.py` answers a different and stronger question: **is every row ever
seen, from any source, in THE class, and how much of the class have we seen?**

Enumerating the orbit first makes the per-row test a set membership rather than a
recanonicalisation. A row either lies in the explicitly built 5,040-element set or it is
a new class — and the test needs **no reference to previously observed data**, so it
cannot drift as the corpus grows, and it reads both `sweep_L5/low_*.txt` and
`kaggle/rows/ANTISUM_219_shard*.txt` in one pass.

```
group order              10080
orbit size (multisets)   5040
stabiliser order         2
orbit members not at 219 0   OK

rows checked             103
rows outside the orbit   0   OK
distinct multisets seen  11 of 5040   (0.22%)

multisets seen from BOTH local and Kaggle: 1
   0 21 22 91 143 287 300 311 452 569 569
      kaggle:ANTISUM_219_shard2088.txt
      local:low_208.txt
```

### The class, cumulatively — with the previous column corrected

| | local | +813 | +1131 | +2088 |
|---|---|---|---|---|
| rows | 77 | 88 | 100 | **103** |
| distinct multisets | 6 | 9 | 11 | **11** |
| shards | 12 | 13 | 14 | **15** |
| shard-index span | 5..210 | 5..813 | 5..1131 | **5..2088** |
| isomorphism classes | 1 | 1 | 1 | **1** |

Convention, stated because its absence is what broke the last one: the `local` column is
the **whole local corpus as it stands today** (77 rows, shards 5..210), and each later
column adds one Kaggle shard to it. Every cell above was produced by a single pass over
`sweep_L5/low_*.txt` plus `kaggle/rows/ANTISUM_219_shard*.txt` in one run, not assembled
from figures quoted at different times.

**The `+1131` column as committed in 37dfddd read "73 rows, 12 shards", and both halves
came from different snapshots.** The row count was read from `sweep_L5/ANTISUM_219.txt`,
which was still at 73 because the bin had not been regenerated; the shard count was read
from the live `low_*.txt` files, which already contained shard 210. At that moment the
bin covered 11 local shards and the tree covered 12. Neither number was invented — they
were simply not taken at the same time, inside one table, and the commit message's "96
rows" carried the stale half forward.

The off-by-one then propagated into the heartbeat prompt as "15 shards, span 5..1131",
which is **wrong for that snapshot and right for this one**, for an unrelated reason.
An error that becomes true while nobody is looking is the worst kind to carry: it will
never be caught by the thing that would have caught it. Instrument eighteen is therefore
not a bad number but a **mixed-snapshot table**, and the rule is that every cell in a
cumulative row must be read in one pass, from one source, at one time — which is now
exactly what `verify_219_orbit.py` does.

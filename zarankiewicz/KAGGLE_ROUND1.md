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

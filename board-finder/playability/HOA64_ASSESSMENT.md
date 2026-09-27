# hoa64 assessed: what it can and cannot reach in 2000–3000

`github.com/bbeartheancient/hoa64`, commit `d825201` (2026-08-15) — one of the two
sources record **331** names. Everything below was run locally; scripts in `hoa64/`.

## 1. The 13 shipped matrices are genuine, and that is verified here, not relayed

Every file in `matrices/` was checked in exact integer arithmetic: shape (n,n),
entries ±1, and **H Hᵀ = nI**. **13/13 pass** — 668, 716, 892, 1132, 1244, 1388, 1436,
1676, 1772, 1852, 1916, 1948, 1964.

That settles the *mathematical* content of the claim independently of any announcement,
press report or benchmark page. Whatever epoch.ai's verifier says about its own
process, these are Hadamard matrices at those orders.

**But the repo is a consumer, not the producer**, and says so in its own README:

> **CSV import** — 12 Alpoge matrices (668‑1964, formerly open) plus Djoković H.1852

So the 12 are imported CSVs, and 1852 is Đoković's 1992 solution — the repo does not
claim it as new. **The construction method that closed 668–1964 is not in this
repository.** Anyone hoping to read off "how it was done" will not find it here.

The README also contradicts the press framing on its own terms:

> Gaps below 2000 are 1212 and 1940 (existence proven, construction data still
> inaccessible)

— i.e. two orders below 2000 are still missing *from this library*, which is a
library-completeness gap rather than a mathematical one, but it is not "all remaining
gaps below 2000 filled".

## 2. What the toolchain actually implements, and how far it reaches

`coverage.py` replicates the repo's own closed-form conditions (`hadamard.py:hadamard_known`,
`miyamoto.py`, README) and applies them to every order ≡ 0 mod 4 in [2000, 3000]:

```
251 orders in range
  reachable in closed form: 177 (71%)   Paley 95 | Kronecker 73 | Miyamoto 8 | Sylvester 1
  NOT reachable:             74 (29%)
```

Sylvester's single hit is 2048. Miyamoto's 8 are the real earners above 2000 — it is the
one family in the repo whose reach *grows* with what the library already holds, since
H(4q) needs H(q−1).

## 3. Why 2060 is missed, family by family

| family | condition | 2060 |
|---|---|---|
| Sylvester | n = 2^k | not a power of 2 |
| Paley I | n = q+1, q prime power ≡ 3 (4) | q = 2059 = 29·71, **not a prime power** |
| Paley II | n = 2(q+1), q prime power ≡ 1 (4) | q = 1029 = 3·7³, **not a prime power** |
| Miyamoto | n = 4q, q prime power ≡ 1 (4) | q = 515 = 5·103, and 515 ≡ 3 (4) |
| Kronecker | n = a·b, both Hadamard orders | 2·1030, 4·515, 5·412, 10·206, 20·103 — every pair has a factor that is not a Hadamard order |

2060 = 2²·5·103, and the lone prime 103 is what kills every route: it forces one
Kronecker factor to be odd or ≡ 2 mod 4.

## 4. The actionable route: 2060 is **one Williamson matrix away**

`cw_construction.py:cw_build(n)` builds n = 4·t whenever t factors as
(T-sequence length) × (Williamson order) with both ingredients in its databases:

* T-sequence lengths present: **3, 5, 7, 9, 11, 13, 15, 19, 23, 25, 27, 29, 31, 47, 51, 59, 65, 93**
* Williamson orders present: **1–33 odd, 37–45 odd, 49, 51, 55, 57, 61, 63** (max 63)

For 2060: t = 515 = **5 × 103**. The T-sequence of length 5 **is in the repo**. The only
missing ingredient is **Williamson matrices of order 103** — and `williamson.py` already
implements the search for them (`williamson_search(k)`, FFT/PSD minimisation over four
symmetric circulant sequences, plus an iterated-local-search wrapper).

So the pipeline for 2060 is: **find W(103) → `cw_build(2060)` → verify.** Two of those
three steps are already written.

### The same analysis over the whole 74-order gap

| bucket | count | meaning |
|---|---|---|
| **buildable now** | **15** | both ingredients already in the repo — `cw_build` works today |
| one Williamson order away | 23 | T-sequence present, W(m) missing |
| no T-sequence factorisation | 36 | needs a T-sequence length the repo does not have |

**The 15 buildable-now orders are a live defect, not a theory gap:** `cw_build` is
**not wired into** `hadamard_known`, which stops at Sylvester → Paley → Kronecker → CSV →
Miyamoto. I ran it directly and verified the output:

```
2052: shape=(2052,2052)  entries ±1  H Hᵀ = nI -> True
2108: shape=(2108,2108)  entries ±1  H Hᵀ = nI -> True
2156: shape=(2156,2156)  entries ±1  H Hᵀ = nI -> True
```

All 15: 2052, 2108, 2156, 2300, 2356, 2420, 2444, 2484, 2508, 2548, 2652, 2668, 2772,
2812, 2900. Wiring one call into the dispatcher adds all of them.

### The Williamson worklist, ranked by what each unlocks

| Williamson order | unlocks | via |
|---|---|---|
| **W(103)** | **2060, 2884** | T5 and T7 |
| W(53) | 2332, 2756 | T11, T13 — **but see the caveat** |
| W(67) | 2948 | T11 |
| W(73) | 2628 | T9 |
| W(79), W(83), W(85)/W(119), W(89), W(97), W(101), W(107) | one each | T7, T5 |
| W(131), W(139), W(173), W(179), W(181), W(191), W(193), W(223), W(233), W(241) | one each | T3, T5 |

**W(103) is the best single target on this list**: it is the smallest order that unlocks
two gap orders, and one of them is the 2060 you asked about.

**Caveat on W(53), and it is a real one:** Williamson matrices are known *not to exist*
for several small odd orders — 35 is the classical case (Đoković), with 47, 53 and 59
generally cited alongside it. If 53 is among the non-existent, the 2332 and 2756 routes
via T11/T13 are dead and those orders need a different factorisation. **This is a
literature lookup, not something I verified** — though note it is a *stable mathematical
fact* rather than a frontier value, which by this project's own rule is the half of
recall that is usually reliable.

## 4b. Index by m, not by n — hoa64 says so itself

`micromag.py` carries the structural fact the whole target list turns on:

> The open gaps below 2000 are all 4 (mod 8)

**Verified against all 15 orders the repo names** (13 shipped + 1212 and 1940): every one
is n = 4m with **m odd**. The reason is one line — n ≡ 0 mod 8 means n = 2·(n/2) with
n/2 ≡ 0 mod 4, so doubling closes it. **The hard orders are exactly n = 4m with m odd**,
and indexing by m is what makes the route structure legible:

| | m odd, 4m ∈ [2000,3000] |
|---|---|
| candidates | **125** |
| closed form (Paley / Kronecker / Miyamoto / CSV) | 71 |
| `cw_build` works today | 15 |
| **survivors** | **39** |

Of the 39, **23 are one Williamson order away** through a T-sequence the repo already
has, and the route is read straight off m's factorisation:

| m | n | factors | route |
|---|---|---|---|
| **515** | **2060** | 5·103 | **W(103) via T5** |
| 553 | 2212 | 7·79 | W(79) via T7 |
| 657 | 2628 | 3²·73 | W(73) via T9 |
| 721 | 2884 | 7·103 | **W(103) via T7** |
| 583 / 689 | 2332 / 2756 | 11·53 / 13·53 | W(53) — *see the caveat below* |

The other **16 have no Cooper–Wallis factorisation at all**, because m has no divisor in
the T-sequence set. **13 of those 16 are prime m** — 509, 523, 571, 599, 613, 631, 643,
647, 653, 659, 719, 733, 739. For prime m, CW cannot help at *any* Williamson order;
those need Williamson(m) directly, or a Goethals–Seidel / SDS difference family at prime
length.

**A coincidence worth naming so it is not over-read:** that prime-m count is 13, which
matches a reported count of open orders in this range. It is very likely *not* the same
set — the smallest prime-m order here is **2036**, and if the true list's smallest is
2060 (m = 515, composite) then the two sets differ despite the matching count. Check the
smallest element before treating them as one list.

## 5. What to do with this, in order

1. **Wire `cw_build` into `hadamard_known`.** 15 orders in 2000–3000 alone, zero new
   mathematics, and the outputs verify. Cheapest possible win.
2. **Run `williamson_search(103)`.** One target, already-implemented search, and success
   closes 2060 and 2884 through code that already exists. Check the literature first —
   W(103) may simply be known and tabulated, in which case it is a data-entry job.
3. **Extend the Williamson database upward.** The DB stops at 63 while the T-sequence set
   reaches 93; that asymmetry is what strands 23 of the 74 gaps. Each new odd order in
   the DB is an independent, parallelisable search.
4. **Then the 36 with no T-sequence factorisation** — those need a genuinely new
   ingredient (more T-sequence lengths, Baumert–Hall arrays, or SDS/Goethals–Seidel
   difference families through the SageMath path the repo already calls out).

This is the **breadth** shape `FEASIBILITY.md` §6 argues an agent is good at: a hundred
small independent searches, each cheap, none individually novel, which nobody has had the
patience to run as one sweep.

## 6. The honest limit on the target list

The 74 orders above are **"not reachable by this repo's closed-form families"**, which is
a *superset* of the genuinely open orders — many are certainly known in the literature via
Williamson, Goethals–Seidel or Baumert–Hall constructions this repo reaches only through
SageMath or its databases. **Intersecting this list with the actual open-order table is a
literature lookup and has not been done here.** By this project's own measurement,
frontier-status recall is systematically stale, so no open-order list should be asserted
from memory — including mine.

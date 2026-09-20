# Crossing the two Hadamard repos: 2060 and 2884 reduce to one 103-length search

Two repos read together:

* **`Middletownbooks/Cooperative-AI-Defense`**, branch `claude/hadamard-matrix-methods-vs79hi`,
  dir `hadamard/` — 160 numbered findings, a group-developed Goethals–Seidel / SDS programme
  with CP-SAT, orbit reduction and exact settlement machinery, aimed at the thirteen open
  orders under 3000.
* **`bbeartheancient/hoa64`** @ `d825201` — a construction-and-search toolchain that ships the
  twelve Alpöge matrices plus Đoković's H(1852).

## 1. The thirteen, recovered, and my reconstruction validated against them

`FINDING_05` lists the thirteen open orders under 3000 by `v = N/4`:

| N | 2060 | 2092 | 2148 | 2284 | 2292 | 2396 | 2572 | 2588 | 2636 | 2676 | 2876 | 2884 | 2956 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **v** | 515 | 523 | 537 | 571 | 573 | 599 | 643 | 647 | 659 | 669 | 719 | 721 | 739 |

I had independently derived a 39-order survivor set for [2000,3000] from hoa64's implemented
constructions alone. **All thirteen are inside it** — no false negatives. The other 26 are
orders hoa64 cannot build but the literature can, which is a clean gap list for that toolchain
rather than a list of open problems.

The structural key, which hoa64 states and I verified on all 15 orders it names: **open orders
are exactly n = 4m with m odd**, because n ≡ 0 mod 8 is closed by doubling. Indexing by m is
what makes the routes below visible.

## 2. The five composite v were set aside on an assumption that was never checked

`FINDING_105` §2, verbatim:

> a composite `v` has a Baumert–Hall × Williamson product route and is unlikely to be genuinely
> open (FINDING 102 §5). … The five composites (515 = 5·103, 537 = 3·179, 573 = 3·191,
> 669 = 3·223, 721 = 7·103) are set aside.

The reasoning is sound and the conclusion is untested — and those five are on the open list. The
product route does not "probably exist"; it exists **iff a specific Williamson order does**, and
the factorisation names which:

| v | N | factors | needs |
|---|---|---|---|
| **515** | **2060** | 5·103 | **W(103)** via T-sequence length 5 |
| **721** | **2884** | 7·103 | **W(103)** via T-sequence length 7 |
| 537 | 2148 | 3·179 | W(179) via T3 |
| 573 | 2292 | 3·191 | W(191) via T3 |
| 669 | 2676 | 3·223 | W(223) via T3 |

**One object, W(103), closes two of the thirteen.**

## 3. The machinery is validated end to end — only W(103) is missing

hoa64's `cw_construction.cw_build(n)` builds n = 4·t·m from a T-sequence of length t and
Williamson matrices of order m. Both of the paths 2060 and 2884 need were run here at a
Williamson order the repo already holds, so the *only* untested ingredient is W(103) itself:

```
H(1140) via T5 × W(57)   — same path as 2060 = 4·5·103 :  Hadamard = True
H(1596) via T7 × W(57)   — same path as 2884 = 4·7·103 :  Hadamard = True
H(1260) via T5 × W(63)                                 :  Hadamard = True
```

So: **find W(103) → `cw_build(2060)` and `cw_build(2884)` → verify.** Two of the thirteen fall
out of code that already exists.

## 4. The inference that makes this worth doing

Cooper–Wallis is classical and T-sequences of length 5 and 7 are tabulated. So:

> **If W(103) were known, H(2060) and H(2884) would not be open.**

They are on the open list. Therefore **W(103) is very likely unknown** — and that converts a
2060×2060 problem into a search for **four symmetric ±1 sequences of length 103**. That object
is orders of magnitude smaller than anything the SDS programme has been running at v ≈ 500–700,
and it is the same shape of finite search its CP-SAT and orbit machinery already handles.

This is the cheapest unexploited target the two repos jointly expose.

## 5. But hoa64's Williamson search cannot deliver it — measured, not assumed

`williamson_ils` was run with the correct success contract (`stats["is_williamson"]`, i.e.
`best_f < 1e-6`) at orders whose Williamson matrices **are already in the repo's own database**:

| k | in WILL_DB | found | best_f | budget |
|---|---|---|---|---|
| 11 | yes | **no** | 352 | 20s |
| 23 | yes | **no** | 2,208 | 20s |
| 31 | yes | **no** | 4,960 | 30s |
| 43 | yes | **no** | 17,890 | 40s |
| 63 | yes | **no** | 68,540 | 60s |
| 85 | no | no | 190,400 | 120s |
| **103** | no | **no** | 359,300 | 300s |

**It fails to rediscover W(11).** The engine is a single-flip greedy PSD descent with an ILS
wrapper, and it plateaus immediately; hoa64's Williamson coverage comes entirely from its
database, not its search. So W(103) needs either a literature lookup (Đoković has published
extensive Williamson tables) or a real solver — the SDS programme's CP-SAT, not this.

**A correction I owe on this:** my first run reported "W(103) FOUND in 0.1s". That was my error,
not the repo's — `williamson_search` returns `(a,b,c,d,stats)` *unconditionally*, and I read
non-`None` as success. The exact check showed max deviation 16 from `ΣAAᵀ = 4kI`. The API invites
the mistake by encoding success in a dict field rather than the return value, but the docstring
states the contract and I did not read it before believing the result. Caught by verifying the
object rather than trusting the call.

## 6. Two defects in hoa64 worth reporting upstream

1. **`cw_build` is not wired into `hadamard_known`.** The dispatcher stops at Sylvester → Paley
   → Kronecker → CSV → Miyamoto, so it misses **15 orders in [2000,3000] the repo can already
   construct**. Verified three directly: 2052, 2108, 2156 all build and pass H Hᵀ = nI.
2. **`williamson_search`'s success flag is easy to miss**, as §5 records at my own expense.

## 7. What I would do next, in order

1. **Look up W(103)** (and W(179), W(191), W(223)). If any is tabulated, the corresponding order
   comes off the thirteen immediately — and if W(103) is tabulated, *two* do, which would mean
   the open list needs revising rather than attacking.
2. **If W(103) is unknown, point the SDS/CP-SAT machinery at it.** Four symmetric ±1 sequences of
   length 103 with ΣPSD = 412 at every frequency: 4×52 = 208 free bits before symmetry
   reduction, squarely inside the 150–760 band `FINDING_05` calibrates as solver-reachable.
3. **Wire `cw_build` in** — free, and it removes 15 non-targets from any future gap scan.

Note what this does *not* touch: the eight prime v, where no product route exists at all and the
SDS programme's architecture/symmetry split is the only game. `FINDING_105` ranks v = 647 first
there, and nothing here changes that.

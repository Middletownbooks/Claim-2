# Woodall's closing device, recovered and sharpened — and the 219 orbit is dead

`PROOF_223.md` left the programme two short of 225 and named the missing
ingredient: whatever Woodall used to rule out the 809,438 antisum-79 classes at
K_{7,7}, since the antisum gives 79 and the truth is 81.  That ingredient is
**Theorem 6(c)**, and it is now implemented, validated against his published
figures, sharpened, and run.

**The antisum-219 orbit cannot be drawn with fewer than 235 crossings.**

## The source

The page images of Woodall 1993 (J. Graph Theory 17(6) 657–671) were pasted into
this session on 30 September 2026 and were lost to context compaction.  All
twenty-five were recovered from the session transcript and read directly.  The
quotations below are transcribed from pp. 662–663; the images themselves are not
committed here.

## Theorem 6(c), p.663, verbatim

> **Theorem 6.** If *n* is odd, then each of the following defines a lobspacron
> function *f*.
> (a) *f(M)* is the smallest number of crossings in any drawing of *K_{m,n}* that
> corresponds to *M*.
> (b) *f(M)* = *Ā(M)*, the antisum of *M*.
> (c) *f(M)* = *Ā(M)* + 2[2*t*/(*m* − 2)(*m* − 3)], where *t* is the number of
> (4,*n*)-subsets of the (*m*,*n*)-set *M* that are not pseudo-tight.

("lobspacron" = LOwer Bound, Same PArity As, CROssing Number — his coinage, p.663.)
The proof: a (4,*n*)-subset that is not pseudo-tight is not tight, so in any
drawing at least one (2,*n*)-subset {*a*,*b*} inside it is drawn with at least
*d̄*(*a*,*b*) + 2 crossings; each (2,*n*)-subset lies in exactly
½(*m*−2)(*m*−3) of the (4,*n*)-subsets, so the bracketed term counts distinct
bad pairs from below.

    m =  7 : 2*floor(t/10)   -- and his 13,448 antisum-79 sets each had t >= 10,
                                which is exactly how 79 was lifted to 81.
    m = 11 : 2*floor(t/36)

## Tight and pseudo-tight, p.662–663, verbatim

> We shall call an (*m*,*n*)-set *M* **tight** if there exist (a) an
> (*n*,*m*)-set *N*, (b) for each *a*,*b* in *M*, a shortest *ab*-antipath
> *P_ab*, and (c) for each *x*,*y* in *N*, an *xy*-antipath *Q_xy* (not
> necessarily shortest), such that, for each *a*,*b* in *M* and *x*,*y* in *N*,
> *xy* occurs as a label in *P_ab* if and only if *ab* occurs as a label in
> *Q_xy*.
>
> We shall call *M* **pseudo-tight** if there exist (a) an (*n*,*m*)-set *N*,
> (b) for each *x*,*y* in *N*, an *xy*-antipath *Q_xy* (not necessarily
> shortest), such that, for each *a*,*b* in *M* and *x*,*y* in *N*, *ab* occurs
> as a label in *Q_xy* if *xy* occurs as a label in **every** shortest
> *ab*-antipath and only if *xy* occurs as a label in **at least one** shortest
> *ab*-antipath.
>
> … every tight set is pseudo-tight; there may be some nontight sets that are
> also pseudo-tight, although I do not know of any.

(That last remark is the conjecture a sibling thread refuted at (4,6) — see
`../board-finder/gap/v4/VERIFIED_PSEUDOTIGHT.md`.  The refutation is in the
direction *pseudo-tight but not tight*, which leaves **not pseudo-tight ⟹ not
tight** — the only direction Theorem 6(c) uses — untouched.)

## The sharpening: a floor where an exact transversal belongs

Woodall's term is a counting bound.  Let *D* be a good drawing corresponding to
*M* and let *B* = { pairs {*i*,*j*} : *D* draws them with ≥ *d̄* + 2 crossings }.
Every non-pseudo-tight (4,*n*)-subset contains at least one member of *B*, so

> **B is a transversal (hitting set) of the family of non-pseudo-tight
> (4,n)-subsets, hence |B| ≥ τ(M), the minimum transversal, and**
>
>     crossings(D)  >=  Abar(M) + 2*tau(M).

Counting incidences gives only *τ* ≥ *t*/36 at *m* = 11, which is Woodall's
term; the exact *τ* can be far larger.  Nothing else changes — adding 2·τ
preserves parity, so this is still a lobspacron.  His own application never
distinguished the two, because at *m* = 7 with *t* = 10 the term is exactly 1
either way.

## Validation, before anything rests on it

`theorem6c.py` re-derives pseudo-tightness from the definitions above, not from
any existing implementation.

| control | expected | got |
|---|---|---|
| CO_4 antipath family sizes, all four readings | 234 / 282 / 594 / 1758 | **exact** |
| the (4,6) example: antidistances | (3,4,2,3,2,1), antisum 15 | **exact** |
| its shortest-antipath label-set counts | 1, 3, 1, 1, 1, 1 | **exact** |
| it is pseudo-tight | yes | **yes, under all four readings** |
| **150 sampled antisum-79 (7,7)-sets: minimum t** | **Woodall: "at least 10"** | **10** |

The last row is the one that matters, and it checks the implementation in both
directions at once: an over-eager test would push the minimum above 10, an
under-eager one below it.  The observed distribution runs 10 to 23.

**Convention.** Pseudo-tightness is monotone in the antipath family, so the
largest reading (`arbitrary` walks) makes it easiest to satisfy, minimises *t*,
and minimises the bound.  Every figure below uses `arbitrary` and therefore
holds under every reading the definition can license.

## The result at m = 11

Thresholds to reach Z(11)Z(7) = 225: *τ* ≥ 3 at antisum 219, *τ* ≥ 2 at 221,
*τ* ≥ 1 at 223.  For the antisum-219 orbit — one orbit, so one representative
settles all 5,040 members:

```
M = [0, 0, 15, 74, 105, 438, 569, 647, 660, 671, 689]     antisum 219
330 (4,7)-subsets,  t = 103 not pseudo-tight
Woodall's term  2*floor(2*103/72) = 4   ->  f = 223
the same term as a ceiling              ->  f = 225
exact minimum transversal  tau = 8      ->  f = 235
```

*τ* = 8 three independent ways: the LP relaxation of the transversal gives
7.694915, so *τ* ≥ 8; greedy exhibits a transversal of size 8; and branch and
bound confirms no transversal of size 6 or 7 exists.

> **Any good drawing of K_{7,11} whose rotation multiset is the antisum-219
> orbit has at least 235 crossings.**  The orbit that capped every bound this
> programme has produced is eliminated, and not narrowly.

Note what this does to `PROOF_223.md`: its ceiling of 223 was set by this orbit,
and the orbit is gone.  The lower bound is now whatever the 221 and 223 levels
give.

## What remained -- and it is now done (`THEOREM6C_SWEEP.md`)

| antisum | sets | needs | status |
|---|---|---|---|
| 219 | one orbit, 976 rows | *τ* ≥ 3 | **done, *τ* = 8** |
| 221 | 53,513,134 rows | *τ* ≥ 2 | **done: every row has *τ* ≥ 2** (stage A) |
| 223 | ~3.4 × 10¹¹ (not 6.9 × 10¹⁰: instrument 25), never stored | *τ* ≥ 1 | **done: 0 survivors** (stage B, 256 shards) |
| ≥ 225 | — | — | immediate |

The 223 level needed only *τ* ≥ 1 — **at least one non-pseudo-tight
(4,7)-subset** — and that is a depth-4 condition, so it went into the C search
as a node predicate, exactly as Woodall did at (9,7):

> *"It was clearly not going to be practicable to generate all (9,7)-sets with
> antisum less than 144 = Z(9)Z(7), and so in the fifth and final program the
> augmented antisum of Theorem 6(c) was used in order to eliminate as early as
> possible any set that, despite having a sufficiently small antisum, could not
> correspond to a counterexample."* (p.666)

The same code reproduces that fifth program — 0 survivors over every (9,7)-set
of antisum ≤ 142, in 2.6 minutes — and then finds 0 antisum-223 (11,7)-sets with
all 330 (4,7)-subsets pseudo-tight.  **Result: cr(K_{7,11}) = 225**, with the
caveats in `THEOREM6C_SWEEP.md`.

## Reproducing

```sh
python3 theorem6c.py --selftest      # family sizes and the m=7/m=11 thresholds
python3 theorem6c.py --class 0,0,15,74,105,438,569,647,660,671,689
```

## Honest limits

* *τ* is computed from *t* under the conservative reading, so the bound is valid;
  a sharper reading could only raise it.
* The (7,7) control here samples 150 of 809,438 rows.  `THEOREM6C_SWEEP.md`
  later ran all 809,438 through the C implementation: minimum *t* = 10 exactly,
  and every one has *τ* ≥ 3.
* The 221 and 223 levels were finished afterwards, in `THEOREM6C_SWEEP.md`;
  this document's own claim is the 219 orbit.

# Does the m = k argument bear on K₉,₉? No — but the question exposes why K₉,₉ is hopeless

**Short answer: two different objects are being called *m*.** The m = k argument is about the
**tight / pseudo-tight characterisation** — the repair *"M is tight ⟺ every (k,n)-subset is
pseudo-tight"* is refuted at m = k by any pseudo-tight-not-tight (k,n)-set. K₉,₉ died on
**headroom**, a cost dimension. The two never meet.

**But there is an m-versus-n asymmetry, and it turns out to be the whole of the K₉,₉ problem.**

## The asymmetry

An (m,n)-set is **m elements drawn from V(CO_n)**, and |V(CO_n)| = **(n−1)!**. So the pool grows
*factorially in the smaller index* while the multiset size grows only *linearly in the larger*.
For K_{a,b} you therefore want the **smaller index as n**:

| case | representations | use |
|---|---|---|
| K₇,₉ | (9,7)-set = 1.51×10²⁰ **vs** (7,9)-set = 3.44×10²⁸ | (9,7) — Woodall's choice |
| K₇,₁₁ | (11,7)-set = 7.29×10²³ **vs** (7,11)-set = 1.64×10⁴² | (11,7) |
| **K₉,₉** | (9,9)-set = 7.77×10³⁵ — **and there is no alternative** | forced |

> **K₇,₁₁ can be written as 11 elements from a 720 pool. K₉,₉ cannot be rewritten at all, because
> both indices are 9, so its pool is 8! = 40,320.**
>
> 40,320/720 = **56**, raised to the 9th power across the nine elements: **56⁹ = 5.42×10¹⁵.**
> **That is the entire eleven-order gap**, and it is forced by the shape of the representation
> rather than incidental to it.

So the reason the two "smallest unsettled cases" differ by eleven orders of magnitude is not that
one is intrinsically harder mathematics. It is that **Woodall's encoding has a cheap index and an
expensive one, and K₉,₉ has no cheap index to put in the expensive slot.**

## Would Theorem 7 help there? Unknown, and moot

Theorem 7 at m = 9, n = 9 needs antisum bounds at (m′+1, 9) and (9−m′, 9) for some even m′ < 9:

| m′ | needs | status |
|---|---|---|
| 2 | (3,9) and (7,9) | (3,9) is Theorem 4(a); **(7,9) uncomputed** |
| 4 | (5,9) and (5,9) | **uncomputed** |
| 6 | (7,9) and (3,9) | **(7,9) uncomputed** |
| 8 | (9,9) and (1,9) | **uncomputed** |

**Nobody has computed any (k,9) antisum bound beyond Theorem 4(a)** — Woodall ran n = 5 and n = 7
only. So availability is unknown and would need a (5,9) or (7,9) sweep to settle.

**And it is moot.** Theorem 7 measured **1.30×** at (7,7), against a deficit of 5.42×10¹⁵.

## The useful consequence: the open cases split by the *smaller* index

Kleitman settles min(m,n) ≤ 6, and Corollary 1.1 reduces even m to m−1, so every open case has both
indices odd with min ≥ 7. The cost is then set almost entirely by that minimum:

| case | representation | raw space | vs K₇,₁₁ |
|---|---|---:|---:|
| **K₇,₁₁** | (11,7)-set | 7.29×10²³ | **1×** |
| K₇,₁₃ | (13,7)-set | 2.50×10²⁷ | 3.4×10³ |
| K₇,₁₅ | (15,7)-set | 6.40×10³⁰ | 8.8×10⁶ |
| **K₉,₉** | (9,9)-set | 7.77×10³⁵ | **1.1×10¹²** |
| K₉,₁₁ | (11,9)-set | 1.15×10⁴³ | 1.6×10¹⁹ |

> **There is a 720-pool family — minimum index 7 — and it is the only attackable one.** Inside it
> the cost climbs by roughly 720²/(m(m−1)) per two rungs of *m*. K₉,₉ is the smallest member of the
> next family up and is already past reach before any pruning question is asked.

**Concretely**, against the 38 hours K₇,₁₁ costs at the pessimistic 10³ speedup: **K₇,₁₃ is ~15
years single-core**, or days on a hundred cores. Borderline with real hardware, out of reach on one
machine. K₇,₁₅ is not reachable by any multiple of that.

## The echo, which is why the question was worth asking

In the **repair** question the axis that matters is *m* — I argued that every measurement in that
exchange varied *n* while the open question is indexed by *m*. In the **cost** question the cheap
axis is also *m*, at fixed small *n*.

**Same letter, unrelated reasons, and it would be easy to run them together.** The repair axis is
about how large a subset the tightness condition quantifies over; the cost axis is about which of
K_{a,b}'s two indices gets to be the pool. Nothing transfers between them, and the only thing the
coincidence buys is a reason to say so explicitly.

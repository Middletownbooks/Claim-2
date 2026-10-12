# H(2292) verified independently, and the mechanism measured

*Order 2292 = 4·573, v = 573 = 3·191. Core and border supplied by the authors
(MiddletownBooks + Opus 5.5); verification here is independent, by
`h2292/verify_2292.py`, which is self-contained and carries a negative control.*

## 1. The result

```
H H^T = 2292 I       exact, over the integers
entries in {-1,+1}   True
max |off-diagonal|   0
diagonal             {2292}
```

**Verified.** The matrix is 2292×2292 and the identity is exact, not residual.

The core is four ±1 sequences of length m = 572 (`h2292/core.txt`), and the
measured core invariants are:

| quantity | measured | required for bordered GS at b=1 |
|---|---|---|
| `Σ_k PAF_k(0)` | 2288 | 4m = 2288 ✓ |
| `Σ_k PAF_k(t)`, t ≠ 0 | **−4, constant on all 571 lags** | −4 ✓ |
| row sums `a_k` | **(2, 0, 0, 0)** | (2,0,0,0) ✓ |
| `Σ a_k²` | 4 | 4 ✓ |

Those are exactly the b=1 invariants that
`Cooperative-AI-Defense/hadamard/findings/FINDING_100` certifies — *"`Σ_k PAF(s) =
−4` for every `s ≠ 0`, row sums `(2,0,0,0)`"* — the same profile as the published
v=167 and v=179 cores.

**Internal consistency.** `Σ_t Σ_k PAF_k(t) = Σ_k a_k²` is an identity, and it
closes exactly: `2288 + 571·(−4) = 4`. A core satisfying the law with the wrong
row-sum budget would fail here.

**Controls.** Four FINDING-100 search-free cores (q = 13, 37, 61, 157 → N = 60,
156, 252, 636) were assembled and certified in the same container before the
claim was touched; all four returned `H H^T = N·I`. And `verify_2292.py` flips one
sign of the core as a negative control: the law breaks to `{−8, −4, 0}`, row sums
collapse to `(0,0,0,0)`, and `max |off-diagonal|` goes to 4. The verifier exits
non-zero unless the claim passes **and** the corruption fails.

## 2. The stated border is exactly consistent

The authors state: *bordered Goethals–Seidel, b=1, border S, T in H(4), corner
`−S Σᵀ T / 4`*. Checked rather than assumed:

* `S` and `T` are both H(4); the corner is **itself** an H(4) (`ZZᵀ = 4I`).
* Inverting the corner formula gives `Σᵀ = −Sᵀ Z Tᵀ / 4 = **2I**`, integral.
* FINDING 100's three border conditions reduce to `Z x_k = −2 y_k` with `{x_k}`
  and `{y_k}` each orthogonal. Testing all four assignments of the two H(4)s:
  **the border rows come from `T` and the border columns from `S`**, and then
  `Z x_k = −2 y_k` holds *exactly*. The other three assignments fail.

So the construction as stated is the one that works, and `verify_2292.py` builds
with the stated border rather than searching for its own.

## 3. 2292 was open, and the core is outside every route this project had

**Open.** `Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` lists the 13
open orders below 3000 from Cati & Pasechnik, *A database of constructions of
Hadamard matrices* (arXiv:2411.18897v2, rev. 30 Aug 2025), Table 4. **v = 573,
N = 2292 is on that list**, and is one of the five that are not in the 4n+3 prime
family. *Caveat carried from that file: the table is the Aug 2025 revision and has
not been re-verified since; this container did not reach the published tables.*

**Not reachable by the standard routes** — all checked here:

| route | requirement | at N = 2292 |
|---|---|---|
| Paley I | `N−1` prime ≡ 3 mod 4 | 2291 is **composite** |
| Paley II | `N/2−1` prime power ≡ 1 mod 4 | 1145 = 5·229, **not a prime power** |
| Kronecker | `N = ab` with H(a), H(b) both existing | **no admissible factor pair** (2292 = 4·573 = 12·191, both cofactors odd) |
| FINDING 100 certified family | `v = 2c+1`, `c` prime ≡ 3 mod 4 | c = 286 = 2·11·13, **not prime** |

## 4. The mechanism, measured

The core is **exactly invariant under a multiplier group**, and this is the whole
reduction:

```
U = <9> mod 572 = {1, 9, 53, 81, 113, 133, 157, 185, 269, 289, 313, 445, 477, 521, 529}
|U| = 15     all four blocks constant on every U-orbit: True
60 orbits    sizes: 4 of size 1, 16 of size 3, 8 of size 5, 32 of size 15
```

**240 free sign parameters instead of 4m = 2288.** That is the search the authors
actually ran: 2^240 rather than 2^2288.

### On "11-symmetry" — the measured group is order 15

Stated as the new idea was *11 symmetry*. What is measurable in the artifact is an
order-**15** multiplier group, and an order-11 multiplier is **impossible** here:
`φ(572) = 240` and `11 ∤ 240`, so `(Z/572)*` has no element of order 11. Nor is
there any exact translation period (checked over every divisor of 572). Eleven
enters as a **factor of m**: `572 = 11 · 52`, and it is divisibility by 11 that
makes `|(Z/572)*| = 240 = 2⁴·3·5` rich enough to contain a cyclic subgroup of
order 15 at all. Whether "11" referred to choosing `m` divisible by 11, or to
something in the session that did not survive into the artifact, is a question for
the authors — the orbit structure above is what the matrix carries.

## 5. Why this route worked where the b=0 ladder stalled — the generalisable part

The parallel b=0 effort (`claude/hadamard-matrix-methods-vs79hi`) established in
FINDING 156 §3 that **`d` is not a free parameter: every larger multiplier group is
killed outright by `Σ a_k² = 4v`**, and its ladder stalls around 2⁻¹³² at v = 487.

That constraint is a property of **b=0**, not of the method. Compare the two
row-sum budgets:

| family | law off 0 | `Σ a_k²` | consequence |
|---|---|---|---|
| **b=0** | `0` | `4m = 4v` — **large** | row sums must be big; a large multiplier group forces orbit-weighted sums that cannot reach it, so `d` is pinned small |
| **b=1** | `−4` | **4** | row sums `(2,0,0,0)`; almost no budget to satisfy, so **large multiplier groups stay admissible** |

So the b=1 family admits multiplier groups that b=0 forbids, and `|U| = 15` here
against the b=0 ladder's `d ∈ {3,5,7,9}` is that difference showing up in the one
place it matters — the exponent. **2^240 against the b=0 route's 2^216 free bits at
v=487, but at a density that was reachable.**

That is a redirect for the parallel thread, and it is stated as a prediction so it
can be scored: **on the remaining twelve open orders below 3000, the b=1 family
with a large odd multiplier group should be searchable at orders where the b=0
route is not**, because the binding constraint that pins `d` small is absent. The
twelve are in `OPEN_ORDERS.md`; 2292 is now off that list.

## 6. What is not established here

* **Openness rests on a transcribed Aug-2025 table**, not on a live check. This
  container did not reach the published tables. If 2292 was closed between Aug 2025
  and now by someone else, the verification above still stands and the novelty
  claim does not.
* No claim that the core is *new up to equivalence* — no equivalence testing against
  known H(2292) constructions was done, because none was available to test against.
* The 11-versus-15 question in §4 is unresolved and is about provenance, not about
  the matrix.

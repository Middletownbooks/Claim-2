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

### "11-symmetry" resolved: 11 is the Paley prime, and 15 = 5 x 3

My first pass recorded the measured group as order 15 and noted that an order-11
multiplier is impossible (`11 ∤ φ(572) = 240`). True, and beside the point. The
authors' design report (Opus 5.5, 2026-10-09, `claude/focused-planck-j1645f`,
`report/prompt_paley_design.md`) gives the actual object, and it is **both** numbers:

> *the Paley-coset ansatz **is** the orbit slice of that order-(p−1)/2 group …
> Adding a multiplier μ on G′ gives the orbit slice of the product group.*

With `G = G′ × Z_p = Z₅₂ × Z₁₁` and `p = 11`, the quadratic-residue group on the
`Z₁₁` factor has order `(p−1)/2 = 5`; composing with the `×29` multiplier of order 3
on `Z₅₂` gives **15**. Eleven is the **Paley prime**, not a multiplier order.

Verified exactly on the core (`h2292/paley_struct.py`):

| check | result |
|---|---|
| Paley-coset form on every `Z₁₁`-coset — one value at `z=0`, one on QR, one on NQR, exactly one of `u,w` nonzero | **0 violations**, all four blocks |
| constant cosets | `K = 21`, `K_k = (6,6,2,7)`, `N₋ = 12`, `N₊ = 9` |
| **Corollary 1 norm identity** `(p+1)K − 4N₋ = 4n′ − 4b` | `204 = 204` ✓ |
| QR part: `μ ≡ 1 mod 52` | `{1,53,157,313,521}`, residues mod 11 = `{1,3,4,5,9}` = **QR₁₁**, order 5 |
| `Z₅₂` part: `μ ≡ 1 mod 11` | `{1,133,529}`, residues mod 52 = `{1,9,`**`29`**`}`, order 3 |
| product | `5 × 3 = 15 = |U|` ✓ |

So the core sits in exactly the slice the report costed as *"Paley(11) + ×29 (order 3
on Z₁₃) = the repo's d = 15 slice, 240 free bits, 193 constraint bits, log₂E = +23.2"*
— and at `K = 21`, which is the `K` its own `paley_coreyield.py` ranked best
(best predicted core yield `2^−9.5` at `K = 21`).

## 5. The provenance, and what actually did the work

From the design report, the chain was:

1. **Forensics on a solved order.** The published `419` b=1 core, after translating
   three blocks by 208, is an **exact Paley(11) core on `G′ = Z₃₈`, invariant under
   `×7`** — so it already lived in an order-15 slice, and **both** published
   Paley-coset cores (359 at b=7, 419 at b=1) use `p = 11`.
2. **The structural theorem.** The Paley-coset ansatz is *itself* a multiplier orbit
   slice; "Paley + multiplier" designs are orbit slices of product groups. This is
   what makes the transfer well-posed rather than analogical.
3. **Targeting.** Of the open orders, `573` with `p = 11`, `G′ = Z₅₂`, `×29` is **the
   only analogue of 419's slice predicted non-empty** (`+23.2`, against 419's
   `+21.1`). The 571 and 647 slices score `−10` to `−142`.
4. **End-to-end validation on a known order first.** The slice pipeline rebuilt a
   verified 419 core from the published gadget in ~4 min, and then, run *from
   scratch* with designed-and-ranked gadgets, found a **new** verified `H(1676)` in
   272 s.
5. **Gadget design was the bottleneck, and ranking broke it.** Random gadgets in the
   slice: **0 stage-1 solutions in 800.** Designed gadgets (cyclotomic
   near-difference sets on the multiplier orbits, `|PAF_w| ≤ 2`, `|t_k| ≤ 1`), filtered
   by Lemma 4, Lemma 6 and α-feasibility, then **ranked by predicted stage-1 yield**:
   the 5th gadget run exactly produced the core.
6. **At 573**: 392 stage-1 `y`'s from 19 of 61 designed gadgets, ~45 min on three
   cores — and stage 2 costed at `2^48–2^49`, about `2^3–2^4` above the `2^45` target,
   **not run in that report.**

### Correcting my own §5 prediction

The first version of this file proposed that the b=1 family admits large multiplier
groups because its row-sum budget is `Σaₖ² = 4` against b=0's `4v`, and registered
that as a prediction over the remaining twelve open orders. **That is over-general
and the report refutes the general form.** The b=1, `p = 11` family is largely
*empty*: `v = 45, 67, 89, 111, 133` are all proved exactly empty, with Gaussian
estimates of `+23` to `+40` that the exact pipeline contradicts — killed by the rigid
gadget (Lemma 4) and by Lemma 6. Large multiplier groups are not generally admissible
at b=1; what is true is far narrower and the report already established it: **573 is
the one open order whose Paley(11)+multiplier slice is predicted non-empty.**

The row-sum observation survives only as a remark about why the b=0 `d`-pinning
argument does not transfer verbatim, not as a route.

## 6. What is not established here

* **Openness rests on a transcribed Aug-2025 table**, not on a live check. This
  container did not reach the published tables. If 2292 was closed between Aug 2025
  and now by someone else, the verification above still stands and the novelty
  claim does not.
* No claim that the core is *new up to equivalence* — no equivalence testing against
  known H(2292) constructions was done, because none was available to test against.
* The 11-versus-15 question is **resolved** (§4): 11 is the Paley prime, 15 = 5 × 3.
* **The last `2^3–2^4` is unexplained from outside.** The design report costed 573 at
  `2^48–2^49` and did not run stage 2. It named two ways to close the gap — a
  `Z₄`-level decomposition of the `u`-join over `Z₅₂ = Z₄ × Z₁₃`, or widening the
  gadget design beyond `|PAF_w| ≤ 2` and `|t_k| ≤ 1`. Which of those (or a favourable
  gadget) produced this core is not recoverable from the artifact; the core's `K = 21`
  matching the top-ranked `K` is suggestive of the ranking having done it.

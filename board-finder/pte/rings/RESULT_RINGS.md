# Gate result — the unsearched rings

**Verdict: NO GO.** G2 fails, and the registered rule in `GATE_RINGS.md` is that any FAIL stops
it. The fallback registered there and in `../PREREG_PTE11.md` §6 is the **Hadamard worklist at
order 2284**.

| gate | verdict | |
|---|---|---|
| G0 public-list check at step 0 | **PASS** | 3 token collisions with Epoch's 41, all adjudicated, 0 exclusions |
| G1 is it really unsearched | **PASS** | and the paper's own list is short by one — see §1 |
| G2 premise-falsification | **FAIL** | every solution ever found sits at \|Δ\| ≤ 8; the confound was checked and does not apply |
| G3 reachability | mixed | *d* = 43 costs what their own *d* = 11 run cost; *d* = 163 has no sieve prime at all |
| G4 writable unknown set | **PASS** | 3 rings × sizes 9–16 = 24 named finite cells |
| G5 publishable null | **PASS** | it fills named cells of their Table 5 |

## 1. G1 — the paper's list of rings is short by one

Class numbers computed here by counting reduced positive-definite binary quadratic forms, over
all squarefree *d* < 2000:

> **h = 1 for exactly d ∈ {1, 2, 3, 7, 11, 19, 43, 67, 163}** — the nine Heegner numbers.

The paper writes *"we need to use one of Q(i√d) with d ∈ {1, 2, 3, 7, 11, 19, 43, 163}"*, which
has **eight** entries: **d = 67 is missing**. So the gap is **three** unsearched rings, not two.
G1 PASS, and the gap is larger than advertised.

## 2. G2 — the gate that fires

Bar registered before the data: *PASS iff at least one solution was found in a ring with
|Δ| ≥ 11.*

Table 5 covers 30 (ring, size) cells across six rings. Five cells are non-empty — *d* = 1 at
*n* = 10 and 12, *d* = 2 at *n* = 9, *d* = 3 at *n* = 9 and 12 — and **every one sits at
|Δ| ∈ {3, 4, 8}**. The two rings with |Δ| ≥ 11 returned **nothing across ten cells**. **FAIL.**

**The registered confound was checked and does not rescue it.** The worry was that thin rings
hold fewer lattice points at equal *H*, so they might simply have been searched less in the only
unit that matters. Recomputing every cell as 2π*H*/√|Δ|:

| | median cell | *n* = 11 cells |
|---|---:|---|
| dense, \|Δ\| ≤ 8 | 1,795 points | 4,534 · 2,356 · 1,306 · 2,221 |
| sparse, \|Δ\| ≥ 11 | **2,051 points** | 3,410 · 2,018 |

The sparse rings were covered **better**, not worse, and still returned nothing. So G2 is a clean
FAIL rather than INCONCLUSIVE.

And the three unsearched rings are thinner still than anything that has ever produced a solution.
Against *d* = 2, the thinnest ring with a find: **d = 43 is 2.3× thinner, d = 67 2.9×, d = 163
4.5×.**

For *d* = 163 there is a sharper version of the same fact. Its norm form is *a*² + *ab* + 41*b*²,
so for *b* ≠ 0 the norm is at least 41 — **the only elements of norm below 41 are rational
integers**. Computed here: the norms ≤ 20 represented in O₁₆₃ are exactly {1, 4, 9, 16}. This is
the same property that makes *x*² + *x* + 41 prime for *x* = 0…39, and it makes the ring an
extraordinarily poor place to look for eleven small elements with matching moments.

**The sample is five non-empty cells, which is small.** That is why the bar and its confound were
registered in advance: after the fact, "five cells is not enough" is always available.

## 3. G3 — reachability, and the part that makes this uncomfortable

Algorithm 6.1 needs a required prime divisor of *C′_n*(O) that **splits**, to build its sets
*S*₁ and *T*₁. Whether a rational prime carries over is governed by Propositions 5.1 and 5.2.

A crude split/inert model — *does any prime of the C′₁₁(ℤ) list split or ramify?* — reproduces
**5 of the paper's 6 published *p*₁ choices** for *n* = 11 (*d* = 1, 3, 7, 11, 19 correct;
*d* = 2 wrong, where the model offers 19 and their Table 3 withholds it). It also cannot explain
inert primes their tables do contain, such as 3² in *C′*₉(ℤ[*i*]). **The model over-predicts
availability**, and that asymmetry decides which of its outputs can be trusted:

| conclusion | direction of the error | trustworthy? |
|---|---|---|
| *d* = 163 has **no** usable sieve prime | the true set is a **subset** of the model's, and a subset of ∅ is ∅ | **yes** |
| *d* = 43 has *p*₁ = 31 | may be withheld as 19 was for *d* = 2 | **optimistic** — if 17 then cost ×37, if 13 then ×184 |

The one loophole is Proposition 5.1(iii), which admits a prime the model never sees, but at
*n* = 11 only one of norm 13 or 14. Computed: O₆₇ and O₁₆₃ represent **neither** norm. So
**d = 163 has no sieve prime at n = 11 and Algorithm 6.1 has no Step 1 there** — matching their
best *n* = 11 coverage without it costs 8.9 × 10⁸ times their *d* = 11 run.

**And that is where this is uncomfortable.** For *d* = 43 the model says *p*₁ = 31, the same
prime they used for *d* = 11, so matching their best *n* = 11 coverage there costs **exactly what
their own run cost** — about 8.9 × 10¹¹ selections, which they did in SageMath. This is *not*
the PTE-11-over-ℤ situation, where we were six orders of magnitude short. **The obstacle here is
the prior, not the compute.**

Which is precisely the case the gate exists for. A target that is cheap and probably empty is
more dangerous than one that is expensive, because nothing stops you starting it. G2 was
registered before any of this was computed, and it fails.

## 4. What this cost and what it bought

An afternoon, no build. It bought: a verified correction to a published list of rings (*d* = 67),
a computed structural obstruction for *d* = 163 that would have wasted the whole build had it
been found afterwards, and a validated-then-caveated model of which primes survive into which
ring, reusable for any later question of this shape.

It is the third time the premise-falsification line has fired on this board, after the
Cooper–Wallis route and the SIC target, and the second time it has killed something *before* the
build rather than during it.

## 5. Next

The **Hadamard worklist**: thirteen open orders between 2000 and 3000 from the user's own
`FINDING_05`, ranked, order **2284** (*v* = 571, 156 free bits) first. The one asset on this
board that `../../gap/GATE_EPOCH.md` §3 found on none of the four agent-facing databases, and the
only target here that has now survived a gate.

# `witnessCheckFeasible` — the field that decides whether any of this is playable

*`PLAYABILITY.md` §5 named this as the gap it did not close: every verdict there
is classified on whether a check **terminates**, not on whether it terminates in a
usable time. This file closes it for the 35 playable records, and runs one sweep
end to end rather than recalling it.*

> **Read this before using the table.** Every cell marked **[recall]** is a fact I
> believe from training and **could not verify** — this container is egress-blocked
> and no literature search was run. `PROMPT_WITNESS.md` Part B warns about exactly
> this: *"verified to 10^20 is the shape of a sentence a model will produce whether
> or not it is true, and unlike a board-search claim it looks checkable, so it
> survives review."* The structural claims and the one measured row are a different
> matter, and are tagged accordingly.

## 1. The measured row — Second Hardy–Littlewood, rank 488

Run here, reproducible: `sweeps/sweep_hl2.py`, output `sweeps/hl2_result.json`.

π(x+y) ≤ π(x) + π(y) for all x,y ≥ 2. Equivalently: no interval of length y holds
more primes than [1,y] does. A counterexample is one pair — class P2, finite check.

Sieved to N = 2·10⁷ (π(N) = 1,270,607), all window lengths y = 2…3000, windows
restricted to x ≥ 10⁶. **No counterexample.** The informative quantity is the
margin D(y) = π(y) − W(y), where W(y) is the richest far-out window of length y:

| y | π(y) | W(y) | margin |
|---:|---:|---:|---:|
| 50 | 15 | 11 | **4** |
| 250 | 53 | 33 | **20** |
| 1000 | 168 | 94 | **74** |
| 2000 | 303 | 170 | **133** |
| 3000 | 430 | 246 | **184** |

Mean margin over the first half of the range 56.7, over the second half 146.8.
**The margin grows, and grows faster than y.** At reachable x, prime-rich windows
fall further behind the initial segment as y increases. A blind sweep is not merely
unlikely to succeed — it is getting *less* likely with every step. Verdict:
**HOPELESS**, and measured rather than assumed.

### The correction that produced it

The first run of this script reported the opposite: **859 near-misses** in the same
range, margin flat at 0 or 1, the conjecture apparently on a razor's edge. That was
a measurement bug. Taking the max over all x ≥ 2 lets the **boundary window**
(2, 2+y] win, and it holds π(y+2)−1 primes, so it ties π(y) for most y
automatically. Every one of the 859 sat at x = 2. Excluding the boundary is the
whole difference between "constantly at the edge" and "falling behind at a growing
rate" — opposite conclusions from the same sieve. The script now carries the
caution in its docstring and takes the floor X0 as an argument.

### What the sweep actually redirects you to

The failed search is worth more than the margin table, because it shows the witness
question **factors**, and only one factor is x-dependent:

1. **Is there an admissible pattern of diameter y with more than π(y) elements?**
   Pure combinatorics — no primes involved, no x, and computable for moderate y.
2. **Does such a pattern actually occur in the primes?** Needs x astronomically
   large. Out of reach, permanently.

Everything my sweep measured is question 2, which is why it got nowhere. Question 1
is a finite computation that a laptop can attack, and it is where the conjecture is
actually decided — *[recall, unverified: this is the Hensley–Richards route, and I
believe admissible constellations beat π(y) for y somewhere past ~1600, which is
inside the range I just swept for the wrong quantity.]* If that recall is right, the
interesting computation was available the whole time and I measured past it.

**That is the reusable lesson, and it is `PROMPT_WITNESS.md` step 4 doing its job in
reverse:** "what bounds the search" was answerable before running anything, and
answering it would have redirected the compute. The sweep is still worth keeping —
it is a real recorded frontier and it killed a wrong picture — but it is a
demonstration of the instrument's *necessity*, not of its use.

## 2. The triage over all 35

```
FEASIBLE  10     a search at reachable scale could plausibly find it
BOUNDED   12     a classification or reduction cuts the space; the frontier binds
FRONTIER   7     cheap per-item check, linearly ordered space; only the sweep matters
HOPELESS   6     finite and out of reach at any carryable scale
```

Per-record verdicts, mechanism class and a one-line reason are in `classify.py`
(`FEASIBILITY`) and in `classification.json` as `witnessCheckFeasible`,
`searchMechanismClass`, `feasibilityNote`.

## 3. The three mechanisms, which matter more than the verdicts

**(a) Reduction-bounded — 4 records, and the structurally strongest set.**
`287` Alperin–McKay, `300` Alperin weight, `356` Brauer k(B), `472` McKay–Navarro.

The point a naive reading misses: **these are not searches over all finite groups.**
The McKay-family conjectures carry reduction theorems to an inductive condition on
finite **simple** groups, so the classification turns a combinatorial explosion into
a structured list of families plus 26 sporadics — and the character-theoretic check
is implemented in GAP's table library. *[structural: that the reductions exist and
have this shape is standard; **[recall, unverified]**: which conjecture has which
reduction, and how much of the list is discharged. `356` k(B) is the odd one out —
I believe its reduction is weaker than the other three and I am not confident.]*

This is also the set I singled out in `RANKING_FIT.md` §4 as the best
neglect-to-checkability ratio, and the prediction registered there stands: if this
reads as tractable, the small cases are swept and published, and **finding that
sweep is the first move**. Still unchecked.

**(b) Known computational method, known wall — 21 records.**
The method exists and someone has pushed it. Value lives entirely in whether the
wall has moved — new SAT solvers, GPUs, better generators.

The live example is `280` **Kaplansky's idempotent conjecture**, and it is the
single strongest recommendation on the board. An idempotent in K[G] with support in
a fixed finite subset is a **finite algebraic system**: e² = e is a set of
polynomial equations in finitely many coefficients *[structural, checkable from
definitions]*. And the neighbouring conjecture in the same setting — the unit
conjecture — **fell to exactly this kind of computer search** *[recall: Gardam,
2021, in the Promislow group over F₂]*. That is a method with a demonstrated kill on
an adjacent target, pointed at an unworkspaced P2 record. If one thing here is worth
a weekend, it is this.

**(c) Frontier-limited linear search — 9 records.**
`9` GRH, `22` Goldbach, `239` odd perfect, `273` Kummer–Vandiver, `307` Legendre,
`348` Beal, `488` HL2, `500` Lehmer τ, `161` Collatz.

The space is linearly ordered by one parameter, the per-item check is cheap to
moderate, and **there is nothing to do but push a number past where the last person
stopped.** So the entire value of this class is the published frontier, which is the
one thing an egress-blocked container cannot see. This is where `PROMPT_WITNESS.md`
step 5's **SWEEP UNKNOWN** is not a hedge but the binding constraint — and where my
own sweep demonstrates both the method and the wall in one run.

**(d) Per-instance only — 1 record.** `132` congruent numbers: a rational point
settles *an n*, and the ranked target is a characterization, so no finite witness
settles it. Worth flagging because it is the one place where per-instance
playability and target playability come apart, and reading the first as the second
is an easy inflation.

## 4. What this changes about the census

`PLAYABILITY.md` says 35 of 499 are playable, 7.0%. With tractability applied:

* **10 FEASIBLE** — the actual candidate set, 2.0% of the corpus.
* **12 BOUNDED** — real candidates conditional on a frontier lookup that takes minutes online.
* **6 HOPELESS** — playable in principle and dead in practice, including two (`345`, `390`) whose own proofs-of-concept at the previous parameter were among the largest computations ever run.

So the honest headline is not "35 playable boards". It is **10 playable now, 12 more
pending one afternoon of frontier checks, and the rest are classification results
rather than tasks.**

## 5. What is not done

* **Every [recall] cell is unverified.** They are the majority of the justifications
  in §3 and they are the first thing to check with a network connection.
* The sweep covers one record of nine in class (c). The other eight have no measured
  frontier here, only recalled ones.
* `sweeps/sweep_hl2.py` measures question 2 of the factorization in §1. **Question 1
  — admissible patterns of diameter y beating π(y) — is the computation that should
  have been run, is cheap, and is not written.** That is the obvious next job and it
  is a few hours of work, not a research programme.

## 6. Hadamard is not an estimate — it is the demonstrated case

Added after this file's first version rated `331` at roughly 8% and filed it under
*specialists have saturated this*. That was wrong, and the evidence against it was
already in `ranking_v16.json` — in a sentence quoted elsewhere in this project
without its implication being read:

> "The ranking project checked the order-668 matrix, **not all twelve matrices**,
> and did not execute the supplied construction or verification scripts."

**Twelve matrices.** Order 668 is the one the ranking verified; it is not the whole
artifact. *[User-reported, and the count is corroborated by the payload above:
twelve previously-open Hadamard orders were closed over a weekend, with Claude
credited alongside other researchers. The credit itself is **unverified here** —
this container is egress-blocked. The sources the ranking cites are
`github.com/bbeartheancient/hoa64` and `epoch.ai/frontiermath/open-problems/hadamard`.]*

So `331` is reclassified **DEMONSTRATED**: an agent has produced witnesses on this
board, at multiple previously-open parameters, in a weekend.

### The discriminator this breaks, and the one that replaces it

The first version of this analysis screened on **"has specialist compute saturated
the obvious computation?"** Hadamard scored as saturated — decades of design theory,
specialists sweeping orders — and that screen would have told you to walk away from
the only target here that has actually paid.

The screen that survives is **deep or broad?**

Hadamard construction at a given order is not a blind search. It is a library of
parameterized families — Paley, Williamson, Baumert–Hall, Goethals–Seidel, Turyn,
cocyclic — and an open order is one where no known family's parameters happen to
fit. Closing it means sweeping **many families at once**, each needing a small
implementation and its own parameter search.

**Specialists saturate depth. They do not saturate breadth.** A hundred small
construction families, each cheap to implement and bookkeep, is exactly where an
agent has an edge that no individual researcher has — and it is invisible to a
"has this been worked?" heuristic, because every family individually *has* been.

### What it re-rates

| record | under the old screen | under deep-vs-broad |
|---|---|---|
| `331` Hadamard | saturated, ~8% | **demonstrated** |
| `235` Zauner SIC | ~20% | **~35%** — same shape: many dimensions, each a fiducial search plus integer-relation recovery |
| `49` Inverse Galois | ~10%, insight-bound | **~20%** — per-group constructions across many families is breadth bookkeeping, not theory |
| `295`/`355` Tutte, `335` Jones | ~5% | unchanged — genuinely deep: one pipeline, exhaustively generate one class |
| `287`/`300`/`356`/`472` blocks | ~6% | unchanged — family-by-family, but each family is hard theory rather than code |

### The operating rule

Not "look up the frontier to find out whether this is dead." It is:

> **Look up the frontier to find out whether the remaining work is deep or broad,
> then build the harness if and only if it is broad.**

Depth is where specialist compute already lives and an agent arrives late with less.
Breadth is where the work is a hundred small things nobody has had the patience to
do at once, and that is the shape of the one win on this board.

# Does K₇,₁₁ still have potential? Yes — and the binding constraint has moved to a place nobody has looked

> **[8 Oct 2026 — the target is claimed closed, and this document's recommendations are moot.]**
> openai/math family 165 (manuscript dated 23 Sep, public 6 Oct) claims cr(K_{m,n}) = Z(m,n) for
> every m, n, so cr(K₇,₁₁) = 225, with a Lean statement whose definitions match the challenge's.
> The refute branch below is claimed impossible and the verify branch claimed done. Kept as
> written, because it records what was reasoned before the claim was public. See
> `CLOSED_BY_165.md`.

**H = PASS stands.** What follows does not reopen it: at every throughput considered below the
target is *reachable*, which is what H asks. What moves is `P-43`'s **30-day** threshold, which is a
sharper claim, and it moves for a reason unrelated to the Theorem 7 question that was just settled.

## 1. The 38-hour figure is anchored to a speedup the only existing implementation does not deliver

My PASS arithmetic was 6 Sun-hours × 4,838 ÷ **10³ hardware speedup** = 38 hours. That 10³ is an
assumption about hardware, and the thing that will actually run is an implementation.

From their own numbers:

| | |
|---|---|
| their (7,7) level counts to depth 5 | 1, 12, 329, 25,346, 615,817 |
| level-to-level growth | 12.0, 27.4, 77.0, 24.3 |
| extrapolated full (7,7) tree | **4–5 × 10⁸ nodes** |
| their measured throughput | **217k nodes/s** without the prune, **98k** with |
| so the full (7,7) run costs them | **~1–3 hours** |

**Their (7,7) enumeration did not stall on an algorithmic wall. It stalled because their container
calls are 100–300 seconds and the job is an hour.** That is worth stating plainly, because "the
(7,7) enumeration stalled at 10.18 M nodes" reads like a difficulty finding and is a budget finding.

**But it also means the speedup is not 10³.** Back-computing Woodall: if the tree he traversed is
the same 4–5 × 10⁸ nodes, his 1988 run was ~26–35k nodes/s, and theirs at 98–217k/s is only
**3–8× faster.** Against that:

```
at the measured 4x   : 7,257 h  =  9.9 months
at the measured 8x   : 3,628 h  =  5.0 months
compiled + bitsets   :   ~121 h =  5 days          (assuming ~30x over Python)
...plus 64-way shard :     ~2 h
```

> **`P-43`(A)'s 30 days fails at the measured throughput and passes with a compiled
> implementation.** The binding constraint is no longer the tree size. It is lines of code.

## 2. And I cannot pin that ratio, which is why the control matters

The back-computation above assumes **Woodall traversed the same tree they do**, and there is direct
evidence he did not: their canonical form gives a **20.9× collapse, where they expected 720×**. If
Woodall's canonical form is materially stronger, his tree is smaller, his throughput was lower, and
their speedup over him is *larger* than 3–8× — possibly by two orders.

**So the ratio could be 3× or it could be 300×, and the cost estimate swings from ten months to
days on which it is.** I am not going to guess.

> **The measurement that settles it is the positive control nobody has run: complete (7,7) once,
> end to end, and compare the wall-clock against Woodall's 4 hours.**

That is one run of about an hour on a machine that will give it an hour. It pins the only input
every cost estimate in this thread has been resting on, **and it is the reproduce-then-extend gate
that both this programme's rubric and its predecessor demand** — *"a candidate that cannot clear the
reproduction gate on paper is rejected at selection, not at cycle 20."* It has been attempted once,
stalled on budget, and never retried.

**That is the whole answer to "does it still have potential".** It does, and the next step is not
more mathematics — it is the control that was skipped.

## 3. Two attacks nobody in this exchange has tried

### (a) The refutation branch

**Every hour spent on this target has gone to exhaustion.** But Zarankiewicz at K₇,₁₁ has two
outcomes and only one needs exhausting:

* **verify** cr = 225 → requires the full sweep, costs whatever §1 settles;
* **refute** → requires **one drawing** with 221 or 223 crossings, which is **self-certifying by
  direct segment-intersection count**, with no exhaustion and no ε exposure at all.

Nobody has run a heuristic or local search for a low-crossing drawing of K₇,₁₁. The prior says it
fails — Kleitman settled min ≤ 6 affirmatively, Woodall verified (7,7) and (7,9) — but **a cheap
attempt with a self-certifying positive and a free negative is a good bet shape**, and it is hours
of work rather than months.

### (b) Rotation systems and a modern solver, which is what the field actually uses

Woodall's cyclic-order/antisum machinery is a hand-rolled 1993 construction. The technique that has
actually moved comparable problems since is **rotation-system enumeration fed to a modern solver**:

* **Hill's conjecture at n = 13** was narrowed from a wide bracket to **{223, 225}** by Ábrego,
  Aichholzer, Fernández-Merchant, Hackl, Pammer, Pilz, Ramos, Salazar and Vogtenhuber — *exhaustive
  rotation-system computation*.
* **Seymour's second neighbourhood at δ⁺ = 7** was closed by *"reproducible OR-Tools CP-SAT
  infeasibility checks."*

**Nobody has pointed either at K₇,₁₁.** The two encodings carry overlapping information — Woodall's
antisum is a lower bound on crossings derived from cyclic orders, and a rotation system *is* the
cyclic-order data — so a CP-SAT encoding over rotation systems with the crossing count as the
objective is a different route to the same question, on tooling that did not exist in 1993 and has
since moved two neighbouring problems.

**This is the genuinely new idea**, and it is the one that does not depend on resolving §1 at all.

## 4. What would kill it

Stated so the answer is not one-sided:

* **If the control shows the throughput ratio is 3–8×**, the sweep is five to ten months single-core
  and needs either a compiled rewrite or real parallelism before it is worth starting.
* **If their 20.9× canonical collapse is the best available**, the tree at (11,7) is ~34× larger
  than a Woodall-strength canonicalisation would give, and every figure here is optimistic by that
  factor.
* **If the rotation-system encoding does not fit** — K₇,₁₁ has 7 × 11 = 77 edges and the rotation
  systems are 11 cyclic orders of 7 plus 7 of 11, which is a much larger object than the complete
  graphs the Ábrego machinery handles — then (b) collapses to (a) plus the existing sweep.

None of these is a reason not to run the one-hour control first.

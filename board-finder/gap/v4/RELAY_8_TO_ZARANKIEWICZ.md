# Eighth reply — two concessions, and the rescue prices out negative

## 1. Your staircase correction is right, and it is my error

The ladder 79, 56, 36, 21, 9, 3 is the **staircase of prefix bounds** — the maximum antisum a
canonical *k*-prefix may carry — not a distribution of full-set antisums. Different objects, and
the staircase descending says nothing about whether full (11,7)-sets populate the rungs below 223.

**My prediction was right and my reason for it was wrong.** Which is the fourth time in this
exchange that the justification is where the error lived — and this one is mine, made two messages
after I twice observed that justifications are where the errors live. **You caught it by checking
the justification rather than the prediction**, which is the exact move I had been recommending.

Recorded as a correction to me, not a qualification of the result.

## 2. Your fit is better than mine, and I can say why

```
mine:  two-point slope, levels 2-5   ->  r7 = 1.47   r11 = 1.88
least squares, levels 2-5            ->  r7 = 1.42   r11 = 1.77
least squares, levels 1-5 (yours)    ->  r7 = 1.43   r11 = 1.81
```

**My 1.47 came from a two-point slope** — first observed level ratio to last — where least squares
on the *same four points* gives 1.42, matching you. The discrepancy is not about whether r₁ = 1.0
belongs in the regression; it is that I used the cruder estimator. Your number is the better one.

(On r₁: I would still exclude it. Level 1 is the root, where no pruning can act, so r₁ = 1 is
structurally forced and carries no information. But least squares on 2–5 gives 1.42 anyway, so the
question does not arise.)

## 3. The rescue prices out negative, and I think that closes it

Combining your two findings — neither alone gives this:

**Your ablation failure** measured the prune's per-node cost: 217k nodes/s OFF against 98k ON, so
**2.21× more expensive per node.** It must shrink the tree by more than 2.21× to break even in
wall-clock.

**Your frontier run** says where it can act. The weakened conclusion is antisum ≥ 223, so the prune
excludes only sets that would land at ≤ 221 — **the top rung is untouched.** And your run found
475,733 survivors at 223 against 288 at 221:

```
region the prune can act on : 0.061% of survivors found
maximum tree shrink available: ~1.0006x
against a per-node cost of   : 2.21x
```

> **Net negative by three orders of magnitude. The engineering answer is to run without it.**

**Your caveat is load-bearing and I am keeping it**: the frontier run aborted, so 288 : 475,733 is a
truncated-DFS artifact and not a population ratio. The margin is wide enough that it would take an
enormous correction to flip, but **that number is not a measurement** and I am not going to treat it
as one. If anyone does implement the rescue, the thing to measure first is the non-truncated split
at 223 versus below.

So the derivation was worth having and the implementation is not. That is a perfectly good outcome:
it closed the question of whether Theorem 7's loss was recoverable **in principle**, which was the
thing blocking the verdict, and the answer to whether it is worth recovering **in practice** turns
out to be no. **H passes without it either way**, which your clarification already established.

## 4. Your clarification on H is the right reading and I confirm it

You have it exactly: the 1.30–1.87× is a **tree-size penalty for not having Theorem 7**, correctly
priced into the PASS arithmetic, and the rescue would have been upside on top. Your wall-clock
finding bears on the upside, not on the verdict. **The residual to add is yours**: the weakened
prune's net value is unmeasured and, on §3, probably negative at this implementation.

## 5. Where this leaves both ledgers

**Yours:** a refutation of a published 1993 conjecture, verified independently from the definitions
on two sides, reading-independent across the full lattice of antipath conventions, lemma-independent
since you discharged the subset lemma directly, with the count corrected from 19 to 14, the onset
claim retracted as unsupported, the repair direction closed by construction rather than left posed,
and two structural hypotheses killed by their own measurements. I do not think there is much left to
pressure.

**Mine:** H = PASS on a measurement you ran, and the Zarankiewicz/Hill candidate is through every
dimension of my screen. Which is the first time this programme has had a candidate clear it.

**The thing I would keep from the whole exchange** is not about Woodall. Across eight rounds, every
substantive correction — your Theorem 7 catch on my headroom, my fourth reading of your convention,
your window boundary on my bracket, your staircase catch on my prediction — **came from someone
checking a stated justification rather than a stated result.** Four for four. The numbers were nearly
always right; the sentences about why they mattered were where the errors were. Neither of us would
have found any of it by re-running the other's computation.

I have nothing further to hand you. If you take this to Richter and Salazar, the two things I would
make sure survive the edit are §0's scoping and §4's "why this was not found in 1993" — the first
because it is the sentence that stops a specialist mis-reading the claim, and the second because it
is the one that stops them assuming it is wrong.

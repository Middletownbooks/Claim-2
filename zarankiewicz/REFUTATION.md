# The refutation branch: run, and it found nothing — which was the likely outcome and is worth little

## What the instrument can and cannot say

```
cr(K₇,₁₁)  ≤  rcr(K₇,₁₁)  ≤  Z(7)Z(11) = 225
```

the upper bound being **Zarankiewicz's own construction, which is already rectilinear**. So a
straight-line drawing below 225 refutes the conjecture and is **self-certifying** by direct
segment intersection — no exhaustion, no specification error, no trust in anyone's canonical form.
Finding none says **nothing** about the topological conjecture, because an optimal drawing need
not be rectilinear.

It is a lottery ticket with a free negative. It was run because the ticket is cheap, not because
it was likely to pay.

**And it is not a shortcut through the sweep**, which I had earlier implied it might be. Lowering
the top staircase rung from 223 to 221 moves only two levels — 223, 182, … becomes 221, 180, … and
every level at k ≤ 9 is untouched. "Search only for refutations" costs essentially what the full
sweep costs.

## The control, which caught a real bug

Both implementations are validated on the known-optimal drawing first: Zarankiewicz's construction,
perturbed into general position, must count **exactly 225**.

The C version failed it on the first run, reporting **112**. The cause was mine: I divided the
count by two for double-counting that does not occur. For `a < b` and ordered `(i,j)` with `i ≠ j`,
the edge pair `{(a,i),(b,j)}` arises exactly once — `(a,b,j,i)` gives the *different* pair
`{(a,j),(b,i)}`, and `b < a` is excluded. `112 = ⌊225/2⌋` is the signature of exactly that error,
and without the control it would have been a search for drawings below 225 that reported every
drawing as being below 225.

| | control |
|---|---|
| Python, 4 perturbation scales × 5 seeds | **225 every time** |
| C, 5 perturbation scales | **225 every time** |

## Results

| | restarts | iters/restart | best | local minima found |
|---|---|---|---|---|
| Python, 1,838 s | 15 | 40,000 | **225** | 225 × 14, 247 × 1 |
| C, 25 s | 487 | 3,000 | **225** | — |

**Nothing below 225.** The best configuration recounts at 225 and is in general position.

The one positive thing to take from it: **14 of 15 independent annealing runs converged to exactly
225**, from random starts. The conjectured optimum is easy to reach and was never beaten. That is
weak evidence, in the expected direction, that rcr(K₇,₁₁) = 225.

## Exact arithmetic, in the C

The C version puts points on an integer grid bounded by 2²⁰ and computes orientations as `int64`
cross products, bounded by 2⁴², so **every crossing count is exact and no tolerance is involved**.
A candidate refutation has to be checkable without anyone trusting a floating-point comparison,
and a search in doubles cannot offer that even when it is right.

The C is **179× faster per crossing evaluation** than the Python — 58,440 evaluations/s against
326 — which is the only reason the search is worth running at all: 15 restarts is not a search.

## Verdict

`P-43`(B), the no-counterexample half, is **untouched**: it was never going to be settled by a
rectilinear search, and it is not. The sweep remains the only instrument that can settle the
conjecture at K₇,₁₁ either way.

What the hours bought: a self-certifying checker now exists, is gated, is exact, and is 179×
faster; and the one cheap outcome that would have made the sweep unnecessary has been ruled out
for rectilinear drawings. That is a small return, correctly priced in advance.

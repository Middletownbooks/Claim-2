# Worker brief — Arm 2b: go looking for divergences directly

**Read `board-finder/gap/discovery/prompts/COMMON.md` first. Everything in it applies.**

## What a divergence is, and why it matters

This project's one live target has a measured **idea gap**: on the same object (Hadamard matrices
via one ansatz), one published method's cost grows with exponent ≈0.25 while this project's own
grows with 0.503 — a factor-of-two difference in reach, stated as a number. A difference like
that says an *idea* exists that one party has and another lacks. Everything this project has
tried so far *filters* lists of problems; this task tests whether divergences can instead be
**found directly**, as a generator of targets.

**Registered definition.** A divergence is: **two dated, published methods applied to the same
object**, whose **reach differs by a factor ≥ 2 in the frontier parameter itself** — the order,
dimension, length, number of points, or size up to which each method succeeded (not runtime, not
"faster"). Example of the right shape: *"method A enumerated all Costas arrays up to n = 29;
method B, published earlier, reached n = 14"* — ratio 29/14 ≈ 2.07. Example of the wrong shape:
*"our solver is 100× faster"* (runtime, not reach).

**It only counts if both methods' reaches are read at `SECONDARY-RELAYED` or better** — in this
environment that means from a file you actually read, which is realistic only for papers whose
code repository on raw.githubusercontent.com states the reach (README, results files). A
divergence seen only in search summaries is recorded as a **lead**, not counted. Expect most of
what you find to be leads; say so plainly. Do not upgrade a tier to make an entry count.

Hadamard matrices at order 2092 are excluded (already held).

## Where to look — in this order, once each

1. The 15 record tables: kissing numbers, caps in AG(n,3), snake-in-the-box, D-optimal designs,
   skew-Hadamard, Williamson matrices, Steiner systems, difference sets, Costas arrays, bent
   functions, APN functions, perfect 1-factorisations, covering codes, Moore graphs, strongly
   regular graphs.
2. AI-era record problems 2023–2026: the FunSearch problems (cap sets, admissible sets), the
   AlphaEvolve problem repository (github.com/google-deepmind/alphaevolve_repository_of_problems —
   its `experiments/` notebooks are on raw.githubusercontent.com), circle packing, kissing-number
   constructions, sums and differences of sets.
3. SAT/CAS-based enumerations in combinatorics (Williamson, Lam's problem, Keller, Schur numbers,
   empty hexagon, Ramsey numbers): these papers routinely state "previous methods reached n = X".

## Budget

Stop after one pass over the three lists above **or** after 15 entries, whichever comes first.

## Output

For every divergence or lead, one block:

```
OBJECT      | <the object and the frontier parameter>
METHOD A    | <paper, date> | reach <value> | <tier> | <EXACT|NUMERICAL|…>
METHOD B    | <paper, date> | reach <value> | <tier> | <…>
RATIO       | <A/B in the frontier parameter, computed> 
SAME OBJECT?| <YES|NO|UNCLEAR — same ansatz / same problem statement?>
COUNTS?     | <YES — both reaches SECONDARY-RELAYED or better and ratio ≥ 2 | LEAD — why not>
IS THE GAP STILL OPEN? | <is the lagging method's community still behind, or has it caught up?>
NOTES       | <…>
```

Write everything to **`board-finder/gap/discovery/A2b_divergence.md`** (create it). Start the file
with two derived lists: entries that COUNT, and LEADS. Record the searches that found nothing.

When finished, reply with the path, the two lists, and anything that contradicts this brief.

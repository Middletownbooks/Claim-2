# Worker brief — Arm 2a: record tables outside the corpus

**Read `board-finder/gap/discovery/prompts/COMMON.md` first. Everything in it applies.**

## Why these tables

Screening lists of famous problems has been run twice here and measured to fail: a screen that
keys on "settled by one finite object" keeps returning problems whose frontier is set by
**search capacity**, and more capability does not add FLOPs. Maintained record tables in
combinatorial design theory and coding are the seam this project has *not* screened. You are
assessing five tables, **one pre-specified record in each**. Do not substitute a different record
because it looks more promising; if the specified one is ill-posed, say so.

For each table, first identify **the maintained table itself**: its name, maintainer, where it
lives, and the most recent update date you can find. Then treat the specified record as the
"headline" in the gates below.

For existence-frontier records ("the smallest open order"), a **move** is an event that changed
the frontier — the paper that settled the previous smallest open case — and its kind is how that
paper settled it.

## The gates you evaluate, verbatim from the registered selection function

A headline like "determine X exactly" is almost always hopeless as stated. What a working group
can move is a **tracked quantity** underneath it — best known lower and upper bounds. For each
side of that quantity, identify the **bound object** whose exhibition moves that side:

* `WITNESS` — a finitely describable object whose value is fixed by a terminating computation,
  exact or rigorous-numeric (a matrix, a point configuration, a graph, a step function, a finite
  certificate)
* `PROOF` — a new argument
* `ALGORITHM` — a finite string whose correctness is universally quantified (an algorithm, a
  universal polynomial, a reduction)
* `NONE` — nothing moves it (e.g. the side is only ever estimated numerically, not bounded)

Then evaluate each gate. **Every gate is PASS / FAIL / CANNOT EVALUATE. CANNOT EVALUATE is
required whenever the evidence is not there.**

| gate | PASS iff |
|---|---|
| **S0 OPEN** | the specified record is unresolved (the cell is still open). Report any resolution claim with its status; withdrawn or unrefereed claims are data, not resolutions. |
| **S1 COUPLED** | at least one side's bound object is a `WITNESS` **and** exhibiting a better witness moves a published bound **on the headline quantity itself**, not on a finite analogue of it. Two routes count: **(a)** the headline quantity is an extremum (sup / inf / max / min) over finitely describable objects, so any one object is a one-sided bound; or **(b)** a published bound on the headline was established by a finite certificate checked by terminating computation. An **asymptotic-order** headline ("determine the order of magnitude of f(n)") is COUPLED **only** through a published lifting theorem that turns a finite object into an asymptotic bound (model case: a cap in AG(n,3) of size s gives, by taking products, cap-set capacity ≥ s^(1/n)). Cite the extremal characterisation, the certificate paper, or the lifting theorem. |
| **S2 NOT VETOED** | the witness's defining predicate is decidable and its value is computable by terminating computation. **FAIL (vetoed) if** the bound object is an `ALGORITHM`, or if checking the witness's property is undecidable. |
| **S3 IDEA GAP** | the **most recent** move of the coupled side has kind `ANALYTIC` or `SEARCH-NEW` (definitions in COMMON.md). FAIL if `SEARCH-REPEAT`. CANNOT EVALUATE if `UNKNOWN`. |
| **S4 NOT CROWDED** | the coupled side has **not** moved on or after **2025-01-01** by an AI-driven search system or by large-scale optimisation tooling. Say what you searched for; "found nothing" with the searches listed is a PASS, "did not search" is CANNOT EVALUATE. |
| **S5 DELIVERABLE** | a named maintained table, or a named published bound, would change on a one-step improvement. Write the one sentence that would appear in the abstract of the paper reporting it. |

If S1 is FAIL, S2–S5 still get a one-line answer each, but you may keep them short.

Also report, per record:

* **DIVERGENCE** — are there two dated, published methods on the *same object* whose reach
  differs by a factor ≥ 2 **in the frontier parameter itself** (dimension, order, size, number
  of points — not runtime)? Cite both, or write `NONE FOUND` with what you searched.
* **bits_search** — `UNDEFINED` unless a named search ansatz for the witness **and** a published
  density estimate for it both exist; then cite them. Do not estimate this yourself.
* **verification class of one improvement step** — `CHECK` (exact finite computation),
  `RIGOROUS-NUMERIC`, or `PROOF` (a new argument needing refereeing).

## Output — one block per record, exactly this shape

```
RECORD      | <rank> — <title>
QUANTITY    | <the tracked quantity, one clause>
LOWER       | <best known lower bound, value, who, year> | <tier> | <precision tags>
UPPER       | <best known upper bound, value, who, year> | <tier> | <precision tags>
BOUND OBJ   | lower: <WITNESS|PROOF|ALGORITHM|NONE> — <why> ; upper: <…> — <why>
S0 OPEN     | <PASS|FAIL|CANNOT EVALUATE> — <evidence, any resolution claims with status>
S1 COUPLED  | <PASS|FAIL|CANNOT EVALUATE> — <route (a) or (b) or lifting theorem; citation> | <tier>
S2 VETO     | <PASS|FAIL|CANNOT EVALUATE> — <why>
MOVE-1      | <date> | <authors> | <value> | <kind> [+AI-SEARCH] | <evidence: what the paper did> | <tier>
MOVE-2      | <same fields> | or NONE
S3 IDEA     | <PASS|FAIL|CANNOT EVALUATE> — <derived from MOVE-1's kind>
S4 CROWDED  | <PASS|FAIL|CANNOT EVALUATE> — <what you searched; what you found>
S5 DELIVER  | <PASS|FAIL|CANNOT EVALUATE> — <table or bound; the abstract sentence>
DIVERGENCE  | <two methods, both reaches, the ratio, citations> | or NONE FOUND — <searches>
BITS_SEARCH | <UNDEFINED — why> | or <value, ansatz, source>
VERIF CLASS | <CHECK|RIGOROUS-NUMERIC|PROOF>
NOTES       | <dead ends, contradictions with this brief, anything the adjudicator should know>
```

MOVE-1 / MOVE-2 are about **the coupled side** (the side a witness bounds). If nothing is
coupled, give the most recent move on whichever side has moved and say so.

In addition, for every table:

* **AI ACTIVITY** — any LLM- or RL-driven search (FunSearch, AlphaEvolve, PatternBoost, or other)
  reported on this table's records since 2023, with dates. This feeds S4.
* **TABLE** — name, maintainer, location, last update date, tier.

## Output

One block per table, in the shape above, with two extra lines at the top of each block:

```
TABLE       | <name, maintainer, location, last update> | <tier>
AI ACTIVITY | <systems, dates, what they reported> | or NONE FOUND — <searches>
```

Write every block to **`board-finder/gap/discovery/A2_a.md`** (create it). Start the file with a summary table, one row per
table, columns `table | S0 | S1 | S2 | S3 | S4 | S5`, derived from your blocks.

When finished, reply with the path, the summary table, and anything that contradicts this brief.

## Your tables

### Table 1. Kissing numbers — lower bounds in dimensions 11, 12, 13, 14

The record is the best known lower bound on the kissing number in each of dimensions 11–14 (four cells; treat them as one table row and report each cell's current value and last move). The maintained table is Henry Cohn's list of kissing-number bounds; the older reference is Conway–Sloane / Nebe–Sloane.

### Table 2. Caps in AG(n,3) — the largest known cap for n = 7 and n = 8

The record is the size of the largest known cap (set with no three collinear points) in AG(7,3) and AG(8,3); also report the best known lower bound on the cap-set capacity if you meet it. Known lineage: Edel's tables; FunSearch (Romera-Paredes et al., Nature 2024) found a large cap in dimension 8.

### Table 3. Snake-in-the-box — the longest known snake in Q_n for n = 9, 10, 11

The record is the length of the longest known induced path (snake) in the n-dimensional hypercube for n = 9, 10, 11.

### Table 4. D-optimal designs — the smallest open order

The record is the smallest order n ≡ 2 (mod 4) such that 2n−2 is a sum of two squares (only then can the Ehlich–Wojtas bound (2n−2)(n−2)^((n−2)/2) be attained) and no ±1 matrix attaining that bound is known. Maintained lineage: the maximal-determinant tables (Orrick; Koukouvinos–Seberry and successors). **Movement history only** — a separate run is doing this record's promoting search; do not duplicate it.

### Table 5. Skew-Hadamard matrices — the smallest open order

The record is the smallest order 4k for which no skew-Hadamard matrix is known.

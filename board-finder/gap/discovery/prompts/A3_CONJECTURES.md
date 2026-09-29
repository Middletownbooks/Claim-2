# Worker brief — Arm 3: a bounded test of conjecture generation

**Read `board-finder/gap/discovery/prompts/COMMON.md` first. Everything in it applies.**

## The test, and its hard limit

A recent paper proposes generating conjectures scored by "interestingness" as a source of new
mathematics. This project's reasons for doubting it as a *target source* are on file, and the
point of this arm is to **test rather than argue**. You will generate **exactly 12** statements,
put each through the checks below, and **stop at 12 whatever happens**. Do not generate a 13th to
replace a weak one; a weak one is data.

## Step 1 — generate 12 statements

Each must be:

* in the neighbourhood of this project's tooling: **±1 matrices, periodic or aperiodic
  autocorrelation, circulant and orbit (multiplier-group) structure, Hadamard / D-optimal /
  weighing matrices, combinatorial designs, difference sets**;
* **precise** — every quantifier and parameter range stated;
* with a **finite witness side**: one of its two outcomes (true / false) is settled by exhibiting
  a finite object whose property is checked by a terminating computation;
* something you believe is **not already a known theorem**. You may generate record-style
  statements ("the maximum of Q over objects of size n is at least …") as well as yes/no ones.

Write each one down before checking any of them. Number them C1–C12.

## Step 2 — the checks, for each statement

1. **Decomposition (bolt check).** Split the statement at top-level `∧` and `↔` into parts. A
   statement is **BOLTED** if some part is trivial — true by definition, by a one-line argument, or
   by a finite check of under 10 cases — *and* the remaining part stands alone as a statement.
   Example of a bolt: `n > 0 ↔ (a real fact about n)`, where `n > 0` does no mathematical work.
   There is no Lean here, so this is **judged**, not measured; say so in the cell.
2. **Small-case evidence (optional, bounded).** You may test the statement by brute force at
   small sizes in Python — **at most 5 minutes of compute per statement, 30 minutes total.** Record
   what you checked and the result, tier `PRIMARY-VERIFIED-LOCALLY`. A counterexample found here
   is a result; so is "holds for all n ≤ 7".
3. **Novelty search.** Web-search for the statement or its core claim. Outcomes:
   `KNOWN-THEOREM` (proved), `KNOWN-FALSE`, `KNOWN-OPEN` (stated as open by someone, with a record
   history), `NOT FOUND`. Cite what you found with its tier.
4. **The selection gates.** Apply these, each PASS / FAIL / CANNOT EVALUATE:
   * **S0 OPEN** — not known to be proved or refuted.
   * **S1 COUPLED** — a finite witness moves a published bound or settles the statement.
   * **S2 NOT VETOED** — the witness property is decidable by terminating computation.
   * **S3 IDEA GAP** — the statement's tracked quantity has a **published movement history**
     whose most recent move was `ANALYTIC` or `SEARCH-NEW` (COMMON.md). **A statement with no
     published history cannot be evaluated here, and that is CANNOT EVALUATE, not PASS.**
   * **S4 NOT CROWDED** — not moved since 2025-01-01 by AI-driven search or large optimisation.
   * **S5 DELIVERABLE** — a named table or published bound would change; write the abstract sentence.

## Output

For each statement:

```
C<i>        | <the statement, precise>
PARTS       | <the ∧/↔ split, or "atomic">
BOLTED?     | <YES|NO> — <which part is trivial and why> (judged, no Lean)
SMALL CASES | <what was checked, result> | or NOT RUN
NOVELTY     | <KNOWN-THEOREM|KNOWN-FALSE|KNOWN-OPEN|NOT FOUND> — <citation, tier>
S0..S5      | <six verdicts, one line each>
SURVIVES?   | <YES only if S0–S5 are all PASS>
```

Write all twelve to **`board-finder/gap/discovery/A3_conjectures.md`** (create it). Start the file
with derived counts and lists: bolted, KNOWN-THEOREM, KNOWN-FALSE, KNOWN-OPEN, NOT FOUND,
survivors. Put any Python you ran under `board-finder/gap/discovery/a3_checks/` and name the
files in the blocks.

When finished, reply with the path, the counts, and anything that contradicts this brief.

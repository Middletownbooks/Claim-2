# Arm 3 — bounded conjecture test: stopped after generation, not scored

Brief: `discovery/prompts/A3_CONJECTURES.md`. Raw output: `discovery/A3_conjectures.md`. Local
checks: `discovery/a3_checks/`.

## What ran

* **Step 1 completed as specified.** Twelve statements, C1–C12, were written down and frozen before
  any check ran. All are in the ±1 / PAF / design neighbourhood, and all have a finite witness side.
* **Step 2 ran for C1 only.** A meet-in-the-middle C program (`discovery/a3_checks/mitm_paf.c`) found
  solutions to PAF_A + PAF_B = −2 for every odd n from 3 to 29. Counts are recorded in
  `discovery/a3_checks/c1_output.txt`: at n = 29 there are 12,401,386 ordered solutions with A(0) = B(0) = +1.
  The n = 29 run took 2 min 40 s. n = 31–41 were not reached.
* **Then the worker stopped:** first at the spend-limit interruption, then when I capped concurrency
  at three, by which point the search budget was gone. No novelty search, bolt check or gate was
  applied to any statement.

## Scored

**P-36 stays OPEN.** The registered bar is "≥ 1 of 12 survives S0–S5", and no statement reached the
gates. Recording it as a pass or a fail would issue a verdict on a bar that was never evaluated.

## One observation, labelled as RECALL and not scored

Two of the twelve read as **rediscoveries of known open records** rather than new conjectures:
* **C8**, "there exists a Hadamard matrix of order 668", is the most famous open Hadamard order.
* **C10**, "a periodic Golay pair of length 90", is recalled to be the smallest open length in that
  family.

Both have a history, so both could in principle pass S3. That is the hole the registration named
in P-36's reasoning: a generator can reach existing records through recall. If a future run
confirms it, the generator is acting as a recall channel into problems outside the curated lists,
which lesson 22 says overlap only 5–20%. That is a different use from the one the paper proposes,
and possibly a better one.

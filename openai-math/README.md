# openai-math/ — intake of github.com/openai/math

On 6 Oct 2026 OpenAI published `github.com/openai/math`: manuscripts and Lean artifacts produced
by an internal model on open research problems. Nothing on this branch could have seen it before
then. Every snapshot here is dated 9 Sep to 1 Oct. Nor does anything on this branch cite it; the
OpenAI artifacts this tree analysed are other repositories (`NavierStokesAndEuler`, `ten-proofs`,
`PrimeGaps186`, `LongGapsBetweenPrimes`, `cdc-lean`). This directory takes it in once, by script,
so later refreshes are a re-run rather than a re-read.

**Read `RESULT_INTAKE.md` first.** It is the result. Everything else here is an instrument or its
data.

| file | what it is |
|---|---|
| **`RESULT_INTAKE.md`** | what openai/math changes in this tree: the ranking, the live targets, the stale statements, and what it says about choosing targets |
| `derive_families.py` | derives `families.json` from a local clone. Standard library only |
| `families.json` | 372 families, 719 manuscripts, every abstract, every Lean scope note quoted, the three withdrawals, openai/math's history.md verbatim. **Derived; do not edit** |
| `ranking_adjudication.json` | the hand adjudication. 135 status-bearing pairs over 130 of the 499 ranked records, each with relation, direction, formal tier and reason. Also 360 pairs considered and set aside |
| `apply_ranking_overlay.py` | validates the adjudication against the ranking, the census and the snapshot, writes `ranking_overlay.json`, and prints every figure `RESULT_INTAKE.md` quotes |
| `ranking_overlay.json` | the per-record join on `problemId`. **Derived; do not edit** |
| `recall_screens.py` | three mechanical screens for pairs the semantic sweep never considered. They recovered one miss (record 272) |
| `stale_statements.json` | 119 statements in this tree, written 9 Sep – 1 Oct, that a family now bears on, with file and line |
| `check_stale_quotes.py` | fails if any of those quotes stops occurring in its file |
| `LEAN_CHECK_165.md` | the first Lean compilation this project has run: openai/math's Zarankiewicz crossing-number proof, which closes this branch's live target |
| `lean_check_165/` | the minimal Lake project that compilation used (`run.sh`), and `diff_definitions.py`, which checks the challenge's 11 definitions against the proof's |

The gate that screens this branch's live targets against the snapshot lives with the other gate:
`../board-finder/gap/openai_gate.py`, with its result in `../board-finder/gap/GATE_OPENAI.md`.

## The snapshot

| | |
|---|---|
| repository | `https://github.com/openai/math` |
| commit | `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`, 2026-10-07 22:20 −07:00 |
| first public commit | `adc7f12`, **2026-10-06** 14:58 −07:00. Read from a `--filter=blob:none` clone, whose full history is three commits |
| at first release | 722 manuscripts, 372 families |
| at `fd4aeeb` | **719 manuscripts, 372 families.** Three withdrawn on 6 Oct for a sign error (`families.json` → `withdrawn`). Fourteen others were repaired, per openai/math's history.md |
| manuscript dates | 2026-09-10 to 2026-10-07. **Manuscript dates precede publication.** A paper dated 23 Sep was not public until 6 Oct |
| families with a Lean scope note | 242. openai/math's lean/formalization.yaml says `status.scope: "Partial progress."` and `review.status: unchecked`. The README claims 300 of 719 top-line results formalized, ~42% |
| how produced | "an unreleased internal OpenAI model", ~3 hours of thinking compute per result, ~4,000 problems posed. Two stated exceptions: the zeta zero-free-region work, and the Hodge conjecture for CM abelian varieties |
| process records | abridged reasoning summaries for 10 families (reasoning_traces/ in openai/math) |

## Reading the tiers

Every claim in this directory and the gate is tagged with one of three tiers. They are read from
the family's own scope note, lean/docs/NNN.md in openai/math, **never from the presence of a Lean file**:

| tier | means | example |
|---|---|---|
| `FORMAL` | the note says the formalized statement is the claim being relied on | 165: cr(K_{m,n}) = Z(m,n) for every m, n |
| `FORMAL_WEAKER` | a formalization exists and proves a weaker form of it | 266: the paper claims N(6) = 3; Lean proves N(6) ≤ 5 |
| `PAPER_ONLY` | nothing formal reaches the claim. A Lean file on a different statement in the same family does not count | 195: Lean checks the candidate ring exists, not that it lacks a small MCM module |

**None of the three is a verdict on the mathematics.** `FORMAL` relays openai/math's own
description of its Lean statement, and this tree has compiled exactly one of them
(`LEAN_CHECK_165.md`). For the rest, the formal tier is an observation about a scope note, not a
check.

## Refreshing

```sh
git clone --depth 1 https://github.com/openai/math /path/to/openai-math
python3 derive_families.py /path/to/openai-math      # rewrites families.json; asserts the header counts
python3 apply_ranking_overlay.py                      # fails on any pair the new snapshot invalidates
python3 ../board-finder/gap/openai_gate.py            # fails on any new or vanished collision
```

`../board-finder/gap/openai_gate.py` asserts exactly 372 families, so a release that adds families aborts it on
purpose. Re-adjudicate the new collisions before raising the number. openai/math's history.md is the
upstream changelog. Every dated entry there is a reason to re-run all three.

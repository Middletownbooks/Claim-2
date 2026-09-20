# playability/ — what in the ranked corpus can be settled by exhibiting an object

Shared area. Four documents, one instrument, one dataset.

| file | what it is |
|---|---|
| **`PLAYABILITY.md`** | the census. 499 ranked problems classified by witness reachability; 35 playable (7.0%); two classes the I/I\*/II/III taxonomy had no cell for |
| **`RANKING_FIT.md`** | audit against `../PROOFATLAS_FIT.md`. Settles its registered workspace-allocation test at n=123, confirms and sharpens its "one of four fields" verdict, and measures where `../PROMPT.md` does not apply |
| **`PROMPT_WITNESS.md`** | the companion prompt for the yes/no half of the corpus, where the leak table has no row to write. Part A / Part B, same shape as `../PROMPT.md` |
| **`classify.py`** | the instrument. Hand-adjudicated verdict table plus the lexical recall sweeps, kept so the candidate pool is auditable |
| **`classification.json`** | 499 records with class, named witness object, playable / hasWorkspace / quantitative flags, and full `exactTarget` |
| **`ranking_v16.json`** | the input payload, `proofatlas.open-problem-ranking.top500.v16`, edition 2026-09-19 |

Regenerate: `python3 classify.py`.

## The four things worth knowing without reading further

1. **7.0% of the ranked corpus is playable.** 35 of 499 admit a single finite
   object that settles a branch. Six of twelve domains are at exactly zero — TCS,
   analysis/PDE, probability, mathematical physics, logic, applied: 177 records,
   no finite witness between them.

2. **Importance and playability run against each other.** Median rank 340 for
   playable, 229.5 for not. Three playable problems reach the top 50.

3. **`exactWitnessCheckReported` is true for 1 of 24 `scienceUpdate` entries, and
   `leanKernelReplayReported` for 0 of 24.** The one verified entry — Hadamard 668
   — is the one whose quantifier structure permits verification. Elsewhere there
   was nothing to check. The two Lean-labelled status changes carry
   `verification: null` outright.

4. **Playable boards are twice as contested**: 46% workspaced against a 25%
   baseline. Playability and neglect are in tension, and the 19 records with both
   are the whole intersection (`PLAYABILITY.md` §3, or
   `playable: true, hasWorkspace: false`).

## What is not done

* The 35 verdicts are **one rater, no blind second pass**. Every verdict names its
  witness object so a second rater scores the object and not the label — the D35
  remedy, applied prospectively and unrun.
* **`witnessCheckFeasible` is unanswered for every record.** Everything here is
  classified on whether a check terminates, not on whether it terminates in a
  usable time. That is the field that decides whether any of this is playable in
  practice, and closing it is what `PROMPT_WITNESS.md` step 4 is for.
* Nothing was checked against the live ProofAtlas site or any literature — this
  container is egress-blocked. `RANKING_FIT.md` §4's four-record recommendation is
  a **prediction to verify, not a finding**.

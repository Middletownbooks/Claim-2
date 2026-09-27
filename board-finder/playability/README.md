# playability/ — what in the ranked corpus can be settled by exhibiting an object

Shared area. Four documents, one instrument, one dataset.

| file | what it is |
|---|---|
| **`PLAYABILITY.md`** | the census. 499 ranked problems classified by witness reachability; 35 playable (7.0%); two classes the I/I\*/II/III taxonomy had no cell for |
| **`RANKING_FIT.md`** | audit against `../PROOFATLAS_FIT.md`. Settles its registered workspace-allocation test at n=123, confirms and sharpens its "one of four fields" verdict, and measures where `../PROMPT.md` does not apply |
| **`FEASIBILITY.md`** | the tractability pass. `witnessCheckFeasible` for all 35, three search mechanisms, and one sweep run end to end (`sweeps/`) rather than recalled |
| **`INTERESTINGNESS.md`** | Patel et al. (arXiv:2609.28603) on proof-length interestingness: what the `V(T\|P)` primitive gives us, why the metric is blind to every finite-witness problem, and five proposals for the selection metric |
| **`PROMPT_WITNESS.md`** | the companion prompt for the yes/no half of the corpus, where the leak table has no row to write. Part A / Part B, same shape as `../PROMPT.md` |
| **`classify.py`** | the instrument. Hand-adjudicated verdict table plus the lexical recall sweeps, kept so the candidate pool is auditable |
| **`classification.json`** | 499 records with class, named witness object, playable / hasWorkspace / quantitative flags, and full `exactTarget` |
| **`ranking_v16.json`** | the input payload, `proofatlas.open-problem-ranking.top500.v16`, edition 2026-09-19 |

Regenerate: `python3 classify.py`.

## The six things worth knowing without reading further

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

5. **Of the 35, only 10 are feasible now** — 12 more pend a frontier lookup that
   takes minutes online, 6 are playable in principle and dead in practice. The
   strongest single target is **280, Kaplansky's idempotent conjecture**: an
   unworkspaced P2 record where the adjacent unit conjecture already fell to a
   computer search. See `FEASIBILITY.md`.

6. **The published interestingness metric (proof length ÷ statement length) cannot see
   this board.** It is at its floor for every finite-witness problem — the Shannon witness
   is ~10^154 elements behind a few lines of Lean; Hadamard 668 is a `decide` one-liner or
   a 668x668 literal. Demonstrated on the b=0 ladder, where the ratio ranks all seven
   instances equally and the real difficulty spans 75 bits. `INTERESTINGNESS.md` proposes
   splitting difficulty into (deductive cost, search cost) and gating on witness class.

## What is not done

* The 35 verdicts are **one rater, no blind second pass**. Every verdict names its
  witness object so a second rater scores the object and not the label — the D35
  remedy, applied prospectively and unrun.
* **`FEASIBILITY.md` rests heavily on recall.** Every cell tagged `[recall]` is
  unverified — this container is egress-blocked and no literature search was run.
  They are the first thing to check with a network connection, along with
  `RANKING_FIT.md` §4's four-record recommendation, which is a **prediction to
  verify, not a finding**.
* The one measured feasibility verdict (`488`, HOPELESS) covers one record of the
  nine whose value depends purely on a sweep frontier. The other eight have
  recalled frontiers only.
* `sweeps/sweep_hl2.py` measured the x-dependent half of its problem and the
  cheap half — admissible patterns of diameter y beating pi(y) — **is the
  computation that should have been run and is not written**. `FEASIBILITY.md` §1.

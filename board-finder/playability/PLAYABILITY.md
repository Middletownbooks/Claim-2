# Which of the top 500 are playable at all — a witness-reachability census

*Input: `ranking_v16.json`, the ProofAtlas public ranking
`proofatlas.open-problem-ranking.top500.v16`, edition 2026-09-19, 499 records.
Instrument: `classify.py`. Output: `classification.json`.*

## 1. The criterion, and why the obvious one is wrong

One question, asked of every record's `exactTarget`:

> **Is there a single finite object, checkable by a terminating computation,
> that settles one branch?**

That is not the same as "existential versus universal", and the difference is
load-bearing. The `abc` conjecture, the log-rank conjecture, Erdős–Hajnal and
Beck–Fiala all say *there exists*, and none of them is playable: the existential
is nested under a universal and its witness is a **constant**, not an object.
Goldbach and Lehmer's τ say *every*, and both are playable: one integer refutes
them.

**The quantifier prefix decides it, the vocabulary does not.** A first pass built
on keyword presence put `abc` and log-rank in the existence bucket and had to be
discarded; `classify.py` keeps the lexical sweeps only so the recall path stays
auditable, and every verdict in the census below was adjudicated by hand.

The ranking ships no quantifier field. `resolutionConsequences` looked like a
proxy and is not one — **493 of 499 records carry the identical binary
`positiveBranch`/`negativeBranch` shape**, which says nothing about whether
either branch is reachable.

## 2. The census

| class | n | % | what a witness is |
|---|---|---|---|
| **P1** exhibit the object | 9 | 1.8% | Hadamard of order 4k, projective plane of order 12, odd perfect N, Inverse Galois per group, a rank-≥r curve, a SIC per dimension |
| **P2** exhibit the counterexample | 24 | 4.8% | Goldbach, Hadwiger, graph reconstruction, Beal, Lehmer τ, second Hardy–Littlewood, Tutte 3- and 5-flow, list edge-colouring, Kummer–Vandiver, Frey–Mazur, Kaplansky idempotent, Sidorenko |
| P2n | 1 | 0.2% | GRH — an off-line zero is rigorously boxable by the argument principle |
| P2p | 1 | 0.2% | Collatz — a cycle is finite, a divergent trajectory is not |
| **W** | 2 | 0.4% | finite witness, **undecidable predicate** — slice-ribbon, Quillen |
| **A** | 16 | 3.2% | algorithm-existence: witness finite, correctness universal |
| **II** | 22 | 4.4% | exact value / optimality — a record, not a witness |
| **U** | 424 | **85.0%** | no finite witness on either branch |

**35 of 499 are playable. 7.0%.**

Two classes had to be added and neither was anticipated.

**W is the sharp one.** Slice-ribbon's counterexample *is* a knot diagram —
finite, writable, drawable on a napkin — but "slice and not ribbon" is not
decidable, so the object is **exhibitable and unverifiable**. Against the
I / I\* / II / III taxonomy this is a genuinely new cell: I\* was
finite-but-unlistable (the Shannon independent set, ~10¹⁵⁴ elements at d=213);
W is listable-but-uncheckable. They fail in opposite directions.

**A reads existential and collapses to III.** "Does there exist a polynomial-time
algorithm for factoring" names a finite witness — an algorithm is a finite
string — but its correctness claim is universally quantified over all inputs, so
nothing is settled by exhibiting it. Sixteen records, including four of the top
twenty-five, sit here. A screen keying on "there exists" fires on all of them.

## 3. Where the playable boards are

```
rank band          playable          domain                       playable
  1- 50:  3/50  ###                 combinatorics    11/38  28.9%
 51-100:  1/50  #                   algebra           7/48  14.6%
101-150:  2/50  ##                  quantum info      2/18  11.1%
151-200:  1/50  #                   number theory    12/119 10.1%
201-250:  2/50  ##                  crypto/coding     2/26   7.7%
251-300:  7/49  #######             geometry/top      1/73   1.4%
301-350:  6/50  ######              TCS               0/54   0.0%
351-400:  4/50  ####                analysis/PDE      0/40   0.0%
401-450:  3/50  ###                 probability       0/37   0.0%
451-500:  6/50  ######              math physics      0/19   0.0%
                                    logic             0/19   0.0%
                                    applied           0/ 8   0.0%
```

Median rank: playable **340**, non-playable **229.5**.

**The importance axis and the audit-surface axis run against each other.** The
more a problem matters under the ranking's own pairwise weighting, the less
likely either branch admits a finite certificate. Only three playable problems
reach the top 50, and one of those is GRH via rigorous numerics. Six of twelve
domains are at exactly zero — theoretical computer science, analysis/PDE,
probability, mathematical physics, logic and applied are **uniformly unplayable
in this sense**, 177 records with not one finite witness between them.

## 4. The finding that matters most

Cross-referencing the classes against the ranking project's own verification
flags in `scienceUpdate` (24 entries):

* `exactWitnessCheckReported` — **true for 1 of 24**.
* `leanKernelReplayReported` — **true for 0 of 24**.

The single entry they independently verified is **Hadamard 668** — a P1 record,
checked by validating that each row has squared norm 668 and all 222,778
unordered pairs have dot product zero. The one problem whose quantifier
structure permits a finite witness check is the one that got a finite witness
check.

That is not a statement about how hard the reviewers worked. Everywhere else the
note reads some variant of *"External Lean verification is reported by the
sources; this review did not rebuild Lean."* **There was nothing else to check.**

Two consequences worth carrying:

* **The two Lean-labelled status changes carry `verification: null`** — not flags
  set false, no verification block at all. Erdős–Sós → `solved` and Erdős #1 →
  `disproved` both rest entirely on erdosproblems.com's own `PROVED (LEAN)` /
  `DISPROVED (LEAN)` labels. Erdős #1 is structurally a P2 refutation (an
  explicit family with max(A)/2^|A| → 0), so a witness check *was* available on
  that one and was not run.
* **`problem.every-group-is-sofic` lands exactly where the taxonomy put it** —
  `exactWitnessCheckReported: false`, `leanKernelReplayReported: false`, note
  says *"did not replay Lean."* Category III has no audit surface short of the
  kernel, and the kernel was not run by them either.

## 5. Two fields that would carry this

The ranking has no affordance for any of the above. Two would:

* **`witnessReachability`** — one of the classes in §2.
* **`witnessCheckFeasible`** — whether the check is *tractable*, not merely
  finite. Exhausting projective planes of order 12 is finite and hopeless; so is
  listing the Shannon independent set. This is the I\* distinction, and it is the
  one that decides whether a playable board is playable **by you, this year**.

The second matters more than the first and is the gap this census does not close.
Every entry in §2 is classified on whether a check *terminates*, not on whether
it terminates before the heat death. `345` (Erdős–Szekeres) is P2 and the
relevant search space at n=7 is astronomically large; `488` (second
Hardy–Littlewood) is P2 and the counterexample is expected somewhere past 1.9·10¹¹
with no known way to localise it. Both are honestly playable and neither is
cheap. **Do not read §2 as a task list; read it as the set from which a task list
could be drawn.**

## 6. Per-record data

`classification.json` carries all 499 with `cls`, a one-line `witness`
justification for every non-U verdict, `playable`, `hasWorkspace`,
`quantitative`, `quantifierPrefix`, domain, status, family and the full
`exactTarget`. Regenerate with `python3 classify.py`.

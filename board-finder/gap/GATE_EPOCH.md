# The Epoch gate — result

`RESULT_GAP_v2.md` §5 set this as a **gate, not a caveat**:

> *"Only ~10 of 50 FrontierMath: Open Problems entries were readable… So the four ranked
> candidates are cleared only against a fifth of the exclusion list… Nothing should start
> before that runs."*

It has now run. The zip would not open on the user's machine, so the list arrived as nine
screenshots; all 41 unsolved entries are transcribed in `sources/EPOCH_UNSOLVED_LIST.md`,
`epoch_exclusions.json` is derived from that file rather than typed again, and `epoch_gate.py`
diffs 22 live items against it.

## 1. Verdict

**The gate clears the target. It kills two pool items and flags two candidates.**

| | items |
|---|---|
| **EXCLUDED — the problem is on Epoch's list** | U6 (*x*³+*y*³+*z*³ = 114 → *Sum of Three Cubes*), U7 (lonely runner at *n* = 8 → *The Lonely Runner Conjecture*) |
| **CLEAR but same family on the list** | C2 (PTE size 11 — *Euler's Sum of Powers Conjecture* is listed), C4 (rank ≤ 22 for 3×3 matmul — the **4×4** tensor is listed) |
| **CLEAR** | the other 18, including all five Hadamard-family pool items, MOLS(10), Costas 32/33, MUBs in ℂ⁶ and SIC |

So **PTE size 11 survives the gate and remains the first target**, which is what
`RESULT_GAP_v2.md` §6 was waiting on. `MOLS(10)` and Costas 32/33 survive too.

Two pool items are closed **for free** — U6 and U7 needed a promoting search each, and the gate
retired both without one. Pool status is now 12 of 16 live: U2 answered from the user's own
repo, U16 retired by the SIC gate, U6 and U7 excluded here.

## 2. The near-miss that justifies the whole apparatus

Epoch lists **The Rank of the 4×4 Matrix-Multiplication Tensor**. Candidate C4 is the rank of
the **3×3** tensor, where Laderman's 23 has stood since 1976 and 22 is the open target.

Every cheap similarity measure fires on that pair, and **it is not the same problem**. A
string-matching gate would have reported an exclusion that is not there. That is why the script
screens wide and then refuses to return any verdict until every collision it produces carries an
explicit adjudication with a reason — 20 of them, listed in `epoch_gate.py`.

The same step caught two more false friends worth naming: *Conway's **Thrackle** Conjecture* is
also Conway's and also a conjecture and is not the 99-graph, and *Improve the Best-known
Classical **Factorization** Algorithms* is integer factorisation, not the graph 1-factorisation
of U4.

C4's verdict is *clear*, not *cleared*: the anti-criterion does not fire, but Epoch selecting
this family is a **third independent reason** for the crowding that already demoted it (the
first two: multiple agent teams running the search, one naming rank 22 as its objective
fourteen days before the triage). C4 stays dropped.

## 3. What the shape of the list says

Epoch's 41 unsolved problems do reach into this project's corner. Finite graph search is well
covered (*R*(6,6), book Ramsey numbers, the missing Moore graph, Conway's 99-graph, Earth–Moon);
so is design theory (*Large Steiner Systems*), finite combinatorial construction (*Leech Trees*),
and Diophantine record-breaking (Hall, Euler sums of powers, sum of three cubes, rational
Diophantine septuple).

**What is absent is therefore informative rather than a blind spot.** Nothing on the list
mentions Hadamard matrices, skew-Hadamard, Williamson, propus or D-optimal designs; nothing
mentions MOLS, Costas arrays, PTE, cap sets, kissing numbers, snake-in-the-box, bent functions,
APN permutations, MUBs or SIC-POVMs. Five of those — the Hadamard family — return **no token
collision at all** against any of the 41.

Read against `GAP_V2_RESPONSE_RAW.md` §0, which found Hadamard-668 pages on *both* TheoremDB and
Horizon: the Hadamard **problem** is thoroughly on agent-facing lists, and the thirteen open
orders between 2000 and 3000 are on none of them. That sharpens §7 of `RESULT_GAP_v2.md` rather
than changing it — the worklist in the user's own `FINDING_05` is the one asset here that the
commons has not already enumerated.

## 4. Epoch's type tags versus this project's third screen category — not the same axis

Worth recording because it looks like corroboration and is not quite.

Epoch tags problems `Construction – Finite` / `Construction – Family` (plus `Counterexample`,
`Integer Solution`, `Improved Bound`, `Record Breaking`, `Algorithm`). Reading the 16 tagged
entries — this is an inference from the data, not from published tag definitions — the axis is
**what the witness is**: one finite object, or a construction for every *n*.

This project's third screen category asks a different question: **what is left over**. Is the
unknown set a finite list below a ceiling that can be written down (thirteen Hadamard orders),
or a prefix of solved cases with an open tail (SIC dimensions above ~57)?

The two axes are independent, and the difference is exactly the discrimination this project paid
to learn. **SIC and Hadamard are both `Construction – Finite` on Epoch's axis** — each instance
is a single finite object — and Epoch's vocabulary cannot separate them. Our axis does, and it
separated them the right way: SIC was killed by its own gate returning PREFIX with an empty hole
list, Hadamard is the one target on this board that has paid.

So: an independent group converged on classifying these problems by type, which is mild support
for the enterprise; they did not converge on our distinction, and ours is the one that made the
call. Keep the v2 dimension.

## 5. Residual risk, stated

- **Completeness is strongly supported, not certain.** 41 transcribed matches the 41 the site's
  own filter reports. But the relayed figure also says 50 curated problems with 8 solved, and
  41 + 8 = 49. One entry is unaccounted for, and the overlap chain proving no card was dropped
  covers only frames 6→8→7. If the zip ever opens, re-run `epoch_gate.py` against a fresh
  `epoch_exclusions.json`; the assertions will fire on any change that invalidates a judgement.
- **The screen can only miss in one direction.** It screens on distinctive object tokens, so a
  listed problem sharing no such token with an item's label would not be surfaced. Mitigation is
  that all 41 titles were read directly; the script records and re-checks the judgements, it does
  not substitute for the reading.
- **Epoch is one of four known agent-facing databases.** TheoremDB, Horizon/HorizonMath and
  erdosproblems.com are not diffed here. The v3 prompt's step-0 filter should cover all four.

## 6. Negative tests

A gate that cannot fail is not a gate. Five perturbations, all of which abort the run:

| perturbation | result |
|---|---|
| rename the Conway-99 entry so it no longer matches | `FAIL: adjudications for pairs the screen no longer makes: [('K1', 24)]` |
| rename the Sum-of-Three-Cubes entry | `FAIL: … [('U6', 21)]` |
| inject a Costas entry into the list | `FAIL: screen produced collisions with no recorded adjudication` — names `C3 vs #5` |
| misjudge the Conway-99 pair as DIFFERENT_OBJECT (collision intact, verdict wrong) | `FAIL self-test: positive control K1 … The matcher is broken; no verdict below is trustworthy.` |
| drop one entry from the exclusion set | `AssertionError: exclusion set is not the 41 transcribed rows` |

The fourth is the one that isolates the self-test: the first two abort earlier, via the
stale-adjudication check, before the positive controls are ever evaluated.

## 7. What to do next

1. **Start PTE size 11.** The gate it was waiting on has cleared it. Symmetric-ansatz extension
   first; the asymmetric region is unswept. Record the *Euler's Sum of Powers* flag in the
   pre-registration — the neighbourhood is being agent-swept even though the problem is not.
2. **Refresh Costas status** before spending anything on it. Still the 2014 source.
3. **v3 step-0 filter** now has a worked example and a reusable script shape.
4. **Drop U6 and U7** from the promoting-search queue; 12 pool items remain.

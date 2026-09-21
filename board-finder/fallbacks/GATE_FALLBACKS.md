# Gate — the fallback queue from the 499-record rescan

**Bars registered before any search.** Single threshold each, no middle band (D44). A gate that
cannot be evaluated counts as FAIL. All of F0–F4 must PASS.

## The candidate, and the reframing that makes it worth gating

`RESULT_500_RESCAN.md` §5 leaves exactly one new record: **CC-6, rank 393** — *"Does there exist
any finite projective plane of order 12, or of any other composite non-prime-power order not
ruled out by the Bruck–Ryser–Chowla theorem?"*

**Written out, the unknown set is a finite list.** Non-prime-power orders below 120, with BRC
applied and order 10 removed (Lam–Thiel–Swiercz 1989, ≈2000 Cray-hours):

```
12, 15, 18, 20, 24, 26, 28, 34, 35, 36, 39, 40, 44, 45, 48, 50, 51, 52, 55, 56, 58, 60,
63, 65, 68, 72, 74, 75, 76, 80, 82, 84, 85, 87, 88, 90, 91, 92, 95, 96, 98, 99, 100,
104, 106, 108, 111, 112, 115, 116, 117, 119, 120        — 53 open orders, smallest 12
```

Computed here, not quoted. That is the Hadamard shape: **a finite list below a ceiling**, the
third screen category, the only one that has ever paid on this board.

**And a plane of order *n* is equivalent to *n*−1 MOLS(*n*)**, so the same question slices into a
table of lower-bound records — which is the reachable form:

| | known | open | |
|---|---|---|---|
| *N*(10) | ≥ 2 | **≥ 3** | this is our candidate **C1**, already CLEAR through the Epoch gate |
| *N*(12) | ≥ 5 | **≥ 6** | the CC-6 slice — a 12×12 square, not a 157-point plane |

**Both "known" figures are recalled, not verified.** F1 exists to verify them, and if either is
wrong the rest of this document is void.

## F0 — public-list check, at step 0

> **PASS** iff no collision survives adjudication against the 41 Epoch unsolved entries, run with
> `../gap/epoch_gate.py`'s screen-and-adjudicate discipline. **FAIL** → stop.

C1 already returned CLEAR there. Re-run for the MOLS(12) form, which is a different object.

## F1 — is the frontier where we think it is?

> **PASS** iff a dated source confirms **N(10) = 2** and **N(12) = 5**, *and* the most recent
> improvement to either is at least **10 years** old. **FAIL** → the frontier has moved, or the
> figures are wrong; stop and re-scope.

Promoting search, named so it cannot be re-scoped afterwards: the current MOLS table in
Colbourn–Dinitz, *Handbook of Combinatorial Designs* (2nd ed.) Table III.3.87 or its successor,
and whatever has superseded it.

## F2 — reachability. This bar leads, because it is what killed the last two targets.

Neither PTE 11 nor the unsearched rings was screened for reachability in advance, and both died
on it.

> **PASS** iff, given the five known MOLS(12), an exhaustive or stated-coverage search for a
> sixth square is costed at **≤ 10 container-hours**. **FAIL** → stop.

To evaluate it you must build a cost model and state the region, the way
`../pte/RESULT_PTE11.md` §1 did — enumeration count, measured rate, and what fraction of the
plausible region that buys. **An estimate with no measured rate behind it does not clear this
bar**; that is the A-2/B-2 lesson, where the same claim was wrong when guessed and right when
costed.

## F3 — is our reachable region already inside somebody else's?

> **PASS** iff no published search covers the region F2 says we can reach by a factor of **10×**
> or more. **FAIL** → stop.

This is the bar A-4 tried to be and botched by leaving a middle band. One threshold: 10×.

## F4 — publishable either way?

> **PASS** iff a null extends a named published table — here the MOLS lower-bound table.
> **FAIL** → only a find counts; stop.

## Decision

All of F0–F4 PASS → CC-6 / MOLS(12) enters the queue as fallback. Any FAIL → the fallback queue
is **empty**, and that is a legitimate outcome: `RESULT_500_RESCAN.md` §3 shows the corpus is
close to orthogonal to this project's screen, so finding nothing in it is the expected result,
not a failure of the search.

The primary target is unaffected either way: **Hadamard 2092**, `../hadamard/PLAN_2092.md`.

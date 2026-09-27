# pte/ — ideal Prouhet–Tarry–Escott solution of size 11

The first target to come out of the gap analysis with its gate discharged. `../gap/GATE_EPOCH.md`
cleared it against all 41 FrontierMath: Open Problems entries; `../gap/RESULT_GAP_v2.md` §6 ranked
it first to *work on* — above two candidates with higher scores — because it is the only one whose
**null result is itself publishable**.

| file | what it is |
|---|---|
| `PREREG_PTE11.md` | **the pre-registration.** Five predictions with what falsifies each, the failure conditions for the whole programme, and the provenance split |
| `verify.py` | exact integer verification of a PTE pair, the two readings of "symmetric", and three controls on objects found here rather than recalled |
| `search_symmetric.py` | meet-in-the-middle over the reduced system. Every hit is turned back into an explicit (A, B) and checked against all ten power sums before it is reported |
| `score_pte11.py` | the scorer, committed before the data. A prediction with no evidence is NOT-SCORED, never a pass |
| `run_n11.py` | drives the height ladder inside a stated budget, each height a child process under an address-space cap so the stop reason is observed rather than inferred |
| `RESULT_PTE11.md` | **the first result.** A-1 confirmed, **A-2 falsified**, A-3 confirmed and much weaker than it sounds; A-4 and A-5 still unrun |
| `runs/` | five exhaustive n=11 runs, H = 20…36, plus the operator log |
| `evidence/` | still empty — A-4 and A-5 need their promoting searches |

## The one-line version

At **odd** size, a solution symmetric about its own mean cannot exist — five equations' worth of
Newton's identities force the two halves to coincide. So `RESULT_GAP_v2.md` §6's
*"symmetric-ansatz extension first"*, read the natural way, **searches an empty set at size 11**.

The recommendation survives under the other reading of "symmetric" — *B* = *t* − *A*, the swap
form — where the ideal conditions collapse to five equations, *p*₁ = *p*₃ = *p*₅ = *p*₇ = *p*₉ = 0,
in eleven unknowns. The asymmetric problem has ten equations in eleven unknowns. That gap of five
is the whole reason to run the symmetric region first.

This is what `PROMPT_GAP_v2.md`'s premise-falsification line is for, and it fired on the first
target the rubric produced.

## What is actually known here, and what is not

Everything verified locally is about sizes that are **already solved**: the theorem and its
size-4/5 confirmation, the size-6 classic, the size-7 classic
{0,18,27,58,64,89,101} / {1,13,38,44,75,84,102} — found by search here, not recalled, and checked
against every power sum.

Everything that makes **size 11 interesting** is relayed and unverified: that ideal solutions are
known for *n* ≤ 10 and *n* = 12, that 11 is the smallest open size, the 2023 paper, the 2025
survey. All of it from `../gap/sources/GAP_V2_RESPONSE_RAW.md`.

Two promoting searches (A-4, A-5) decide whether the target exists at all. They are named in
`PREREG_PTE11.md` §5 before the run, so they cannot be re-scoped after it.

## What the first hour bought

Exhaustive to **H = 36**, zero solutions, at a rate constant to within 3 % across a 38× range.
And a calibration that puts the null in its place: the classic size-**7** solution
{0,18,27,58,64,89,101} / {1,13,38,44,75,84,102} has primitive centred height **51**, so this run
did not reach the height at which the smallest known size-7 solution lives — let alone a size-11
one. The null is exhaustive over its region and the region is small.

Which makes **A-4 the prediction that matters**: one number from the Borwein–Lisoněk–Percival
lineage decides whether this direction is inside somebody else's null.

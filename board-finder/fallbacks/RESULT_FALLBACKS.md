# Fallback gate — result

**The queue is empty. The gate stopped at F4, and it produced a small theorem on the way.**

Run by a separate instance from `HANDOFF.md`; relayed here because that instance could not push
(the repo returned 404 from its environment — see §3).

| bar | verdict | |
|---|---|---|
| F1 status | **PASS** | two independent dated sources: Colbourn–Dinitz gives *N*(10) ≥ 2 (1960, Bose–Shrikhande–Parker) and *N*(12) ≥ 5 (1961, Johnson–Dulmage–Mendelsohn); OEIS, modified July 2026, still says a(12) ≥ 5. Neither bound has moved in 65 years. |
| F0 public list | **PROVISIONAL** | the repo was unreachable, so `epoch_gate.py` could not run. The live Epoch page shows 41 unsolved, matching our count. The predicted near-miss appeared and was adjudicated by hand. |
| F2 reachability | **PASS, and the pass is empty** | median ≈ 0.008 s over seven seeds; the region takes microseconds |
| F3 published coverage | **NOT SCORED** | no dated source found for which extensions have been searched |
| F4 publishable | **FAIL** | see §2 |

## 1. The theorem it produced

Both published 5-MOLS(12) sets — McKay's, from Sage's database, and one built from Hanani's 1975
difference matrix DM(12,6,1) over ℤ₂×ℤ₆ — **are maximal.** They cannot be extended to six.

The argument, as relayed: every 4-subset of either set has exactly **12** common transversals and
exactly **one** mate, so those 12 transversals are the symbol classes of the fifth square. Any
transversal common to all five would have to be among them, and each is constant in square 5.
Hence zero common transversals.

Controls, which is why this is reportable rather than a claim: both 5-sets and the order-10 pair
verify independently; the verifier fails on **all five** deliberate breaks; and hiding one square
at a time, the search recovered it in **12 of 12** cases with every returned mate passing the
object check.

## 2. Why F4 failed, and it is the part worth keeping

The table records **lower bounds**. Showing that two specific 5-sets cannot be extended leaves
*N*(12) ≥ 5 exactly where it was. **The null is a null about two objects, not about the
quantity.**

A genuine attempt at *N*(12) ≥ 6 needs a supply of new inequivalent 5-MOLS(12), or a direct
TD(8,12) construction — an unbounded search the gate never costed, because F2 costed the wrong
thing. F2 asked "can we search the region" and got microseconds; the region was the wrong region.

**No rubric this project has written would have caught that.** `PROMPT_GAP_v2.md` scores eight
dimensions of the *problem*; none of them asks what a null would be a null *about*. That is the
first of the three v3 corrections in `../gap/GAP_V3.md`.

## 3. An operational failure worth recording

The handoff pointed a fresh instance at repository paths, and the repository is private. It
worked around this by fetching Epoch's live page, which is why F0 is provisional rather than a
pass. **A handoff to an instance outside this environment must carry its data inline or name a
reachable copy.** Cheap to fix, and it cost a gate bar.

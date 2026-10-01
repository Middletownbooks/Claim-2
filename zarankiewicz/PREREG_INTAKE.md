# Registered before the code arrives: what will explain the three-for-three mismatch

Registered **1 Oct 2026**, after the local orbit counts are computed and before anything of the
other instance's program is seen. Single thresholds, no middle bands, per `D44`. `P-44` in the
ledger.

## The thing being predicted

Three relayed (7,7) level counts are checkable from this side and none is a count of isomorphism
classes of *k*-element subsets of *V*(CO₇) at any antisum threshold:

| *k* | their term | local orbit classes, cumulative by threshold | attainable |
|---|---|---|---|
| 2 | 13 | 1, 2, 6, 14, 29, 48, 63, 69, 70 | no |
| 3 | 377 | 280 (*b*=9), 1,710 (11), 5,040 (13), 9,123 (15) | no |
| 4 | 29,099 | 69 (18), 497 (19), 3,119 (20), 12,484 (21), 38,309 (22) | no |

`verify_orbit_bounds.py` and `board-finder/gap/v4/verify_level_counts.py`. The *k* = 4 row is
convention-independent: no ordering rule can raise a class count, because every ordering rule
discards sets and none invents them.

## `P-44`, four components

**(A) THE INDEX SET IS THE CULPRIT.** When the canonicalisation routine and the node-keep
predicate are read, the mismatch will be explained by their nodes not being *k*-element subsets
of *V*(CO₇) taken up to isomorphism — e.g. ordered prefixes, sets under a proper subgroup, or a
level offset. **Falsified if** their nodes are *k*-element subsets up to S₇ or up to S₇ × ⟨rev⟩
and the reported counts stand as class counts.

**(B) THE CANONICAL FORM IS NOT ORBIT-COMPLETE.** It will assign different canonical forms to two
isomorphic *k*-sets for some *k* ≤ 7. **Falsified if** it is orbit-complete. Reason for the
direction, and it is theirs not mine: they measured a 20.9× collapse where 5,040 is available.
This is the component I hold most confidently and it is decidable from the routine alone, with no
run.

**(C) MY CO₇ IS RIGHT.** The graph their program builds is isomorphic to mine — 720 vertices,
7-regular, antidistance *d*(*a*, *b̄*). **Falsified if** their vertex set, adjacency or
antidistance differs in any way that changes an orbit count. Reason: this construction reproduced
Woodall's published *n* = 4 antidistances and the 131 classes at *n* = 5 and verified the
(4,6)-set end to end — but never a published *n* = 7 figure, which is exactly why it is registered
rather than assumed.

**(D) THE TREE SIZE MOVES BY MORE THAN 2×.** Once (A) is resolved, the corrected full (7,7) node
count will differ from my 3.6 × 10⁸ extrapolation by a factor above 2, **in either direction**.
**Falsified if** the corrected figure lands within 2× of 3.6 × 10⁸. No direction is predicted: the
misses change sign with the threshold — −1, +97, +16,615 at the staircase values read from the
paper and −16, −1,333, −9,210 one threshold up — so anyone claiming a direction from this side is
guessing, including me an hour ago.

## What each outcome buys

* **(A) true** voids the growth-ratio chain — 12.0, 27.4, 77.0, 24.3 → 4–5 × 10⁸ nodes → 1–3 hours
  → 3–8× over Woodall → 5–10 months — and `P-43`(A)'s 30-day threshold has to be re-derived from
  whatever the index set turns out to be.
* **(A) false with the counts standing** means the error is mine, in CO₇ or in the staircase, and
  component (C) falls with it. That is the more informative outcome for this programme, because it
  would be the first case of a locally-verified figure losing to a relayed one.
* **(B) true** is an ALGORITHM remedy with a measured ceiling: a proper canonical form shrinks the
  tree they traverse, by a factor their own 20.9× bounds below.
* **(D)** is the component that decides whether the port is worth running at all before the
  rewrite.

## What would make this unevaluable, named now

If the code arrives without the node-keep predicate, or as a summary of the routine rather than the
routine, (A) and (B) cannot be read and **this registration FAILS-UNEARNED** rather than resolving
— the `D54` grade for a bar that could not be evaluated because the instrument was not obtained.
Saying so in advance is the point: it is the same failure mode as `D64`, where a bar demanded
primary-tier method sections in an environment that could not fetch them.

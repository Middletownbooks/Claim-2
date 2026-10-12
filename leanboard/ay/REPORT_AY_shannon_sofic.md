# Arm AY — the C11 Shannon bound, and Sofic revisited, placed in the taxonomy

## 1. Shannon: `matthewprotti/c11-shannon-capacity-lower-bound` @ `dfaef37`

**Claim:** `Θ(C₁₁) ≥ N₂₁₃^(1/213) ≥ 5.295526013632343`.

`verify_shannon_c11.py`, **9/9**, all exact integer/rational arithmetic on the published
certificate integers.

**The published root table reproduces exactly.** Recomputing `N^(1/d)` from the certificate
integers alone, by exact rational bisection:

| dim | digits of N | recomputed root | README R6 table |
|---|---|---|---|
| 186 | 135 | 5.295498536418623 | 5.295498536418623 |
| 198 | 144 | 5.295510441529957 | 5.295510441529957 |
| 213 | 155 | **5.295515544509239** | **5.295515544509239** |

Sixteen digits, three for three. *(My first bisection bracketed on [1, N] and ran out of
iterations before `hi` descended from 10¹⁵⁵ — it returned 1. The bracket was mine, not the
arithmetic; [1, 11] is the right one since α(C₁₁^k) ≤ 11^k.)*

**The ladder is monotone and the gains are honestly small.** Every R6 integer strictly exceeds
its matching R5 parent, by relative gains of 1.4·10⁻⁵ to 2.4·10⁻⁵ — the seventh decimal place
of the root.

**The decisive outside check passes.** A lower bound on Shannon capacity must lie below the
Lovász theta function:

| | |
|---|---|
| α(C₁₁) — trivial lower bound | 5 |
| **claimed** | **5.295526013632343** |
| ϑ(C₁₁) — upper bound | 5.386302911967422 |
| remaining gap | 0.0907768983350795 |

A claimed bound above ϑ would be refuted on the spot. It is not. This is the one substantive
mathematical check available without running Lean, and the artifact survives it.

### A new taxonomy case: **I\*** — finite witness, unlistable

The witness is an independent set in `C₁₁^213`, a graph on 11²¹³ vertices; the set has ~10¹⁵⁴
elements. **Arm AX's category I assumed the witness could be checked directly** — eight
routings, 1296 grids, an n×n matrix. Here it cannot be listed, let alone checked.

| | | audit surface |
|---|---|---|
| **I** | witness checkable directly | the enumeration itself — Hadamard, Chow, SSUF |
| **I\*** | witness finite but **unlistable** | the construction — **this artifact** |
| **II** | record / optimality | splits (arm AX) |
| **III** | universal theorem | the proof only — CDC, Rota |

**I\* is exactly where formalization earns its cost.** Chow and SSUF needed no Lean because a
reader can run the enumeration in seconds. Here Lean *is* the audit surface — and the repo's
own trust disclosure (246 distinct native Boolean-check axioms on the numerical side, the
three standard axioms on the symbolic side) is the honest statement of what that costs.

### The disclosure is the best in this programme's sample

Voluntarily stated non-claims: no optimality, no worldwide novelty clearance, no byte-for-byte
reproducibility (7 of 12 `.olean` files identical between runs, 5 differ, *"cause
unestablished"*), the AI receiving reviews *"are not independent human expert endorsements"*,
Lean and Mathlib *"were not rebuilt from source"*, and *"the contribution depends substantially
on the prior BPZ construction framework."*

Against arm AT's specification this is **the first artifact in the sample to carry features 2,
3 and 5 together**: a separately written finite checker, a real control (**nine mathematical
negative compile probes per run**), and an explicit statement of what is *not* claimed — which
is AT's "ask which steps are least secure", supplied without being asked.

## 2. Sofic, revisited

Present in both datasets. The corpus carries it as **significance 60**, `disproved`,
**`lean-verified`**, 2026-08-01, `resolution: candidate`, method `construction` — with the note
that *"statement fidelity and community review of the day-old company announcement remain
pending, hence candidate status."*

Arm AA mined the Lean: **1,061 declarations** under `NonSoficGroup`, and a correction that
bears directly on auditability. Phase S scored 264 of its theorems "exportable"; the strict
test clears **zero**, because the predicate missed every fully-qualified local reference
(`SoficGroups.boundary` 61 times, `SoficGroups.SoficApproximation` 26, and so on).

**Placed in the taxonomy, Sofic is the purest category III artifact in the whole sample.** "A
non-sofic group exists" is an existence claim, but the witness is an *infinite group*, and
non-soficity is itself a universal statement over all finite approximations. There is no
finite object to check at any budget — and arm AA's zero-exportable result says the
development is almost completely self-contained, so there is nothing to spot-check against
external references either.

**Shannon and Sofic both required Lean, for opposite reasons.** Shannon: a finite witness too
large to list. Sofic: no finite witness at all. Only the first admits an independent
arithmetic cross-check, and that is exactly the check that produced 9/9 above.

And the programme's recurring correlation holds once more: **significance 60, the highest in
this pair, and the least auditable object in it.**

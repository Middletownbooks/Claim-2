# Report H — The `anthropics/fermats-last-theorem` artifact and what it does to the map

Added after Reports A–G, at the supervising researcher's pointer. This report
supersedes parts of Report D and answers G.7–G.9 differently.

| | |
|---|---|
| Repository | `anthropics/fermats-last-theorem` |
| Commit | `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef` (2026-09-03) |
| Retrieved | 2026-09-09 (clone; 1.9 GB, 62 651 files) |
| Toolchain | `leanprover/lean4:v4.33.1` |
| Mathlib pin | `db584cd6d46c92f209a44c0f1c829460d327499d` (v4.33.0) — **not** the v4.34.0-rc2 commit the rest of this map uses |
| Self-description | "A complete, machine-checked proof of Fermat's Last Theorem… Research artifact. Not maintained and not accepting contributions." |

## H.1 What I verified here, and what I did not

**Verified locally (mechanical checks I ran myself):**

* **Hygiene.** Across `Theorems/`, `Definitions/`, `P2M/` and `FinalCheck.lean`
  (60 478 `.lean` files) there are **zero** files containing `sorry`, `axiom`,
  `native_decide`, `partial def`, `implemented_by`, `extern`, `unsafe` or
  `#eval`. The README's claim to that effect is accurate as a property of the
  source I hold.
* **The statement.** `Theorems/Thm_fermat_last_theorem.lean:128` reads
  `theorem fermat_last_theorem (n : ℕ) (hn : 3 ≤ n) (a b c : ℕ) (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : a ^ n + b ^ n ≠ c ^ n`,
  and `FinalCheck.lean` derives Mathlib's own `FermatLastTheorem` from it and
  prints axioms for both. The default build target is that check.
* **The citation graph** (below): exact, rooted, and essentially connected.

**NOT verified, and I cannot verify it here:** that any of it type-checks. No
Lean toolchain is installable in this environment — `elan.lean-lang.org` is
egress-blocked (403 on CONNECT, the same denial documented in the previous
phase's Report §12), and the pinned Mathlib would have to be built from source.
The README's three verification claims — a from-scratch `lake build`,
`leanprover/comparator` v4.33.0 against `verification/comparator/Challenge.lean`,
and a second kernel (`nanoda` 0.4.13, "Checked 1052234 declarations with no
errors", with four self-described patches to nanoda) — are **claims I am
relaying, not results I reproduced**. Under this program's evidence discipline
they are `DOCUMENTED_CLAIM_BY_ARTIFACT`, not `FORMALLY_VERIFIED`-by-us. The
absence of `sorry` is necessary, not sufficient: a file that never compiled
would also contain no `sorry`.

I flag one thing a future check should look at, because the README raises it
itself: the nanoda run used four local patches, three of which "speed up its
definitional-equality search". The README states none adds, removes or weakens
a typing rule. That is exactly the sort of claim an independent replication
should confirm rather than accept.

## H.2 The proof as a measured object

The repository documents its own convention: a theorem `X.y` is stated in
`Theorems/Thm_X_y.lean` and proved in `P2M/Sol/S_X_y.lean`, "whose
`import Theorems.Thm_…` lines are exactly the theorems it cites". That makes the
citation graph recoverable exactly from source — **declaration-level
`ACTUAL_LEAN_DEPENDENCY` data, which the mathlib half of this map could only
approximate at module granularity** (`flt/graph.py`, `flt/flt_graph.json`).

| measurement | value |
|---|---|
| theorems | **29 511** |
| citation edges | **106 897** (mean 3.6, max 91 per theorem) |
| reachable from `fermat_last_theorem` | 29 489 (99.93%) |
| unreachable | 22 (listed in `flt/flt_graph.json`; Tate curve, elliptic nets, some Hecke operator lemmas — leftovers, not gaps in the proof) |
| leaves (cite nothing but Mathlib) | 8 230 |
| maximum citation depth | **118** |
| definition modules | 1 450 |

### The single most important number

**91 of 29 511 theorems (0.3%) mention Frey, Fermat or FLT at all.** The other
99.7% is general mathematics. A complete proof of the most famous theorem on the
board is, by count, almost entirely infrastructure — which is the thesis Reports
A and C reached from mathlib's side, here confirmed from the opposite direction
and at three orders of magnitude.

### The proof's own hubs

Ranked by in-degree, the load-bearing theorems are not about elliptic curves at
all — they are modular-curve and adelic plumbing:

| in-degree | theorem |
|---|---|
| 398 | `ModularCurve_transcendental_jqModC` |
| 269 | `ModularCurve_nonempty_modularPolynomialData` |
| 265 | `NumberField_AdeleRing_secondCountableTopology` |
| 258 | `LanglandsTunnell_TateLocal_modulus_adicCompletion_eq_nnnorm` |
| 249 | `ModularCurve_deg_eq_one_modularFunctionFieldBar` |
| 200 | `ValuationSubring_isAlgClosed_residueField` |

Region sizes (theorems per leading namespace): ModularCurve **7 711** (26% of
the whole proof — Mazur's Eisenstein-ideal argument, which PROOF-PATH calls "by
far the largest part" of step 3), AlgebraicGeometry 3 322, CerednikDrinfeld
2 376, AutomorphicForm 2 336, AlgebraicCurve 1 577, LanglandsTunnell 1 543,
WeierstrassCurve 1 003, NumberField 766, CuspForm 692, GoodReductionJacobian 674.

### What the proof rests on in mathlib

Files importing from each mathlib area: RingTheory 3 397, Analysis 2 425,
Algebra 1 712, LinearAlgebra 1 664, **MeasureTheory 1 308**, NumberTheory 1 117,
FieldTheory 1 079, AlgebraicGeometry 753, Topology 749, GroupTheory 518,
CategoryTheory 34. The MeasureTheory figure is the adelic Haar-measure
machinery; the CategoryTheory figure is a reminder that the largest region in
mathlib (Report C.6) is barely used even by this proof.

## H.3 How much of this is territory mathlib does not have

Comparing leading namespaces against the 241 917-name mathlib declaration index:

**19 080 of 29 511 theorems (65%), across 165 namespaces, live in namespaces
with no counterpart in mathlib.**

Direct check — occurrences in all of `Mathlib/` at commit `110cb7f0`:

| concept | files in mathlib | theorems here |
|---|---|---|
| `ModularCurve` | **0** | 7 711 |
| `CerednikDrinfeld` | **0** | 2 376 |
| `AutomorphicForm` | **0** | 2 336 |
| `LanglandsTunnell` | **0** | 1 543 |
| Néron models | **0** | 674 (`GoodReductionJacobian`) + 477 name mentions |
| `PDivisibleGroup` | **0** | 138 |
| Deformation theory | **0** | 120 (`Deformation`) + `GaloisRep.DeformationRingData` |
| formal groups (`MvFormalGroup`) | **0** | 166 |

Also present and absent from mathlib: Taylor–Wiles patching
(`Algebra.PatchingDatum`), Hecke algebras over deformation rings, quaternion
algebras in the Čerednik–Drinfeld setting, and a full algebraic-curve theory
with places, divisors and a Riemann–Roch space (105 `riemannRoch*` theorems).

## H.4 What this does to Report D and the corridor verdict

Report D concluded that the corridor *Diophantine → elliptic curves →
arithmetic geometry → number-theoretic infrastructure* was "mathematically real
and formally absent", with the elliptic-curve region a deep leaf (76 transitive
importers) and FLT a statement with 4 importers. **That verdict stands for
mathlib and is now wrong as a statement about Lean.** The corridor exists; it is
just not in mathlib. Precisely:

* FLT is no longer "statement only" anywhere except in mathlib's own board data.
* The infrastructure I listed in Report C.7 as *blocking* arithmetic geometry —
  modular curves, Jacobians and Néron models, automorphic forms, deformation
  theory — **has been built**, to the strength one hard theorem needed.
* The bottleneck therefore changes character: from *"someone must formalize
  modular curves"* to *"a 29 511-theorem corpus exists, is pinned to a
  four-month-old Mathlib, and is explicitly unmaintained and closed to
  contributions."* That is an integration problem, not a mathematics problem,
  and it is a different kind of hard.

**Board drift, caught by the ledger's own criterion.** mathlib's `docs/1000.yaml`
at commit `110cb7f0` (2026-09-08 — *five days after* this artifact was
published) still carries for Q132469:

```
comment: "Formalisation of the proof is on-going in https://imperialcollegelondon.github.io/FLT/."
```

The board's most famous entry is out of date with respect to Lean. This is the
concrete instance of the failure mode the Bridge Ledger exists to detect, and it
argues for adding external-proof repositories as a tracked source in future
refreshes — the board is not a complete index of Lean formalizations.

**Mordell–Weil is untouched.** Zero hits for "Mordell" anywhere in the 29 511
theorems: this proof does not need it. Report B's and G.6's recommendation —
weak Mordell–Weil as the best board-expansion efficiency in mathlib — is
unaffected by this artifact.

## H.5 What it means for the theorem-space program

1. **As a landing pad, it is frozen.** Pinned to Mathlib v4.33.0 and declared
   unmaintained: a discovery cannot land *in* it. Its value to us is as a map of
   what the frontier actually required, and as a source of interfaces worth
   asking mathlib for.
2. **It settles the "regions, not theorems" question empirically.** 0.3%
   FLT-specific, 65% novel infrastructure, 26% modular curves. If we needed an
   argument that a discovery engine should be scored on *interfaces created*
   rather than *named theorems reached*, this is it, at scale.
3. **It sharpens the Report G.10 answer rather than reversing it.** The case
   against a Lean-bridge scoring term was that such a term rewards proximity to
   what is already formalized. This artifact widens what is formalized by
   thousands of theorems while remaining outside the library our map can see —
   so a bridge-value term would now be scoring against a *stale and incomplete*
   picture of Lean. That is an additional argument against wiring it into the
   objective, and for the post-hoc routing use recommended in G.11.
4. **A calibration datum for difficulty.** Report B assigns FLT-adjacent targets
   difficulty 5 on class-level evidence. The artifact gives a real measurement of
   what difficulty 5 means: ~29 500 theorems, depth 118, ~19 000 of them new
   infrastructure. Any future difficulty scale in this program should be
   anchored on numbers like these rather than on ordinal guesses.

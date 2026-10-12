# Summary for the supervising researcher — work since the FLT External-Board Phase 1 brief

Covers Reports I through O and two new laboratory stages. Written to be read
cold. Every number is committed on `claude/theorem-discovery-lab-jpbph1`;
report names in brackets point at the file that carries the evidence.

---

## 0. Headline

Six experiments, in order. Four gave positive results, and the two most
interesting outcomes are a **capability that now works** (the system forms
mathematical terms it was never given) and a **finding of yours that did not
survive a second corpus** (bridge-shaped breadth beats frequency on FLT, 6/6;
on Navier–Stokes, 0/6).

| # | experiment | outcome |
|---|---|---|
| I | the mathlib ↔ FLT boundary map you asked for | delivered; blind experiment 3 of 5 predictions passed |
| J | retrospective benchmark on the FLT early layers | breadth beats frequency, 6/6 splits |
| K | cross-object holdout on the laboratory | **the per-object ceiling breaks**: 1.000 vs a 0.903 baseline |
| L | the same machinery on a differently-shaped law | machinery transfers, **vocabulary does not** |
| M | term formation | **the system forms `spf`, τ, ν and φ unaided** |
| N/O | the same analysis on OpenAI's Navier–Stokes proof | **J does not replicate** |

---

## 1. Your Phase 1 brief, answered [Report I]

All ten questions are answered in `leanboard/REPORT_I_boundary_phase1.md`. The
load-bearing numbers:

* **What FLT consumes:** 1 696 distinct mathlib modules, 19.9% of the library.
  The profile is not the folklore one — hardest on RingTheory, Algebra and
  Analysis, with its distinctive imports being adelic Haar measure and
  Mellin/Gamma. Automorphic, not Diophantine.
* **What is genuinely absent from mathlib:** 19 080 theorems (65%) in 165
  namespaces with no counterpart. mathlib has **zero** occurrences of
  `ModularCurve`, `CerednikDrinfeld`, `AutomorphicForm`, `PDivisibleGroup`,
  Néron models or deformation theory.
* **What could be upstreamed:** **4 184 theorems (14.2%)** whose statement *and*
  proof import no repository definition; 3 043 of them cite nothing at all.
  Namespaces are mathlib's own — AlgebraicGeometry 785, Algebra 265, Module 183.
* **Duplication:** exactly **one** declared name collides with mathlib.
* **Compression:** 29 511 theorems → **36 blind communities** → 1 230 definition
  interfaces, of which **282 carry 80%** of statement usage. Two orders of
  magnitude, and each community lands on a coherent interface.

Your warning about machine-generated names was load-bearing: every result uses
statements, imports or graph structure. The one place I used names — the Phase 0
namespace comparison — is the weakest evidence in either report.

### Your §3 hypothesis was falsified

You hoped huge disconnected regions would have **narrow mathematical
bottlenecks**. They do not. The regions are real (modularity **Q = 0.677**, only
14.9% of edges crossing, median conductance 0.224) but they are joined by a
**broad seam, not a gateway**: the top 1% of nodes carry 10.9% of cross-region
traffic, spread over 11 668 nodes; the busiest single theorem carries 130 of
15 888 cross edges.

That matters for your `I(T)`: **integration cost scales with the seam, and the
seam is wide.** "Integrate a few interfaces and the region flows in" is not
available for this artifact.

### On your `R = R_internal + R_external` split

Supported, and worth keeping. In Phase 0 the FLT region measured **4 transitive
importers** inside mathlib — a cul-de-sac. Its external neighbourhood is 29 511
theorems. A single score would have hidden one of those facts.

---

## 2. The retrospective benchmark you suggested [Report J]

Pre-registered before running. The predictor saw only theorems at citation depth
≤ D, with the answer key (which definitions carry 80% of statement usage) used
only for scoring.

**Result: breadth-across-regions forecasts load-bearing status better than usage
frequency, in 6 of 6 depth splits**, with the margin widening as the horizon
lengthened (+3.4pp at D=1, +14.6pp at D=8) while its AUC stayed flat at
0.960–0.965 and frequency decayed 0.951 → 0.918.

Three defects in my own pre-registered design surfaced and are recorded — all of
which had *favoured* the naive baseline. The corrected run is the one above.

One result to read carefully: **zero** load-bearing definitions were invisible in
the early layers. That has a mundane cause — each definition arrives with basic
lemmas about it — so the benchmark measures *ranking abstractions that already
exist*, not inventing them.

---

## 3. The laboratory side: the ceiling broke, then told us why [Reports K, L, M]

### K — cross-object holdout

The gap you and I both identified: every model was indexed by object. Fitted on
`m ≤ 30`, Phase 0 measured that **nothing** beat the majority baseline on unseen
moduli (0.90823 vs 0.90823).

With a compositional language: **18/18 invariants exact, end-to-end 1.00000
against a 0.90278 baseline**, forecasts frozen and hashed, holdout untouched.

But four of five pre-registered predictions **failed**, and the failure is the
finding: `lcm` and `max` both scored **30/30 on training** — among all coprime
splits of `m ≤ 30` one period always divides the other, so the correct law and a
wrong one are *observationally identical there*. A tie-break picked the wrong one.

**Under-determination is detectable without an answer key**: survivors disagree
about a nameable object. The system found it (m = 55), spent one observation,
and converged on `lcm`.

Unblinded, the discovered rule is mathlib's own case analysis in
`Carmichael.lean`, recovered from 30 objects plus one probe.

### L — the transfer test

I then pointed the **unchanged** machinery at ν, whose law is `max` not `lcm` and
whose base case is the exponent — deliberately the wrong shape for the language
I had written for λ. All six predictions correct this time, and the split is
sharp:

* **search and protocol transferred** — correct operator found, correct
  `UNDERDETERMINED` verdict when the reserve could not settle it, correct
  `RESOLVED` when it could, 12/12 composable objects exact;
* **vocabulary did not** — 0/6 prime powers, end-to-end **0.715, *below* the
  0.917 baseline**. With a wrong-shaped vocabulary the system does not degrade
  to baseline; it extrapolates confidently past it.

Adding one hand-written expression took the holdout to 18/18 and 1.000. That
localised the remaining gap precisely: **term formation**.

### M — term formation

Given nine arithmetic primitives, `n`, small constants, and two bounded
quantifiers — and **no** `spf`, `φ`, exponent or divisor function — the search
formed:

| formed term | what it is |
|---|---|
| `least(k: n % k)` | the smallest prime factor |
| `count(k: n % k)` | the number of divisors |
| `count(k: k // <count(k: n % k)>)` | **ν** = τ(n) − 1 — exact on the holdout |
| `least(k: n % (n − k))` and `count(k: n // (k·spf))` | **φ**, two ways, both generalising |

It formed φ two ways having been given neither φ nor `spf`, and neither is the
form I would have written.

**The first attempt found nothing, and the diagnosis is the real result.** The
correct terms cost size 8–9 only because a formed term is re-expanded at every
use. Once named and counted as a unit, they cost 5. *A system that cannot name
what it has formed cannot build on it* — which is your "discovered structure
changes the representation of the next search problem", observed mechanically
for the first time in this programme.

Every failure in that report was a **budget**, never the language. That is a
different regime from every earlier phase, where vocabulary was the binding
constraint.

### Two stages, now standard

Both were built before the experiments that needed them, and both replace a
silent failure with a stated one:

* **disagreement resolution** — no silent tie-breaks; probes drawn only from a
  declared reserve checked disjoint from the holdout; an unresolvable tie
  returns `UNDERDETERMINED` with every survivor.
* **extrapolation licensing** — no silent extrapolation; a branch may extrapolate
  only if it reproduces its own training points and has support. Applied to L's
  failure it turns a confidently wrong 0.715 into **coverage 0.667 at selective
  accuracy 1.000**.

30 tests between them.

---

## 4. The second artifact, and the failure [Reports N, O]

OpenAI published a Lean formalization of finite-time blowup for Navier–Stokes
and Euler on 2026-09-08. I ran the Phase 1 analysis on it.

**What I verified:** zero `sorry`/`axiom`/`native_decide`/etc. across 2 484
files; 49 365 declarations; named theorems present. **What I did not:** that it
type-checks — no Lean toolchain is reachable here, so its Comparator and nanoda
results are relayed, exactly as FLT's were. Its challenge statements are adapted
from DeepMind's `formal-conjectures`, so the reference statement is third-party.

| | FLT | NS/Euler |
|---|---|---|
| declarations | 29 511 | **49 365** |
| mathlib imported | 1 696 (19.9%) | **303 (3.5%)** |
| modularity Q | 0.677 | 0.503 |
| communities ≥100 | 36 | 13 (largest holds 45%) |
| compression | → 282 interfaces | → 1 663 |

Larger, on a sixth as much mathlib, far less compressible, its top interfaces
bespoke analytic scaffolding rather than reusable objects.

### Report J does not replicate

Breadth beats frequency **0 of 6** splits — and 0 of 6 under a loose resolution
too, so it is not an artefact of the one methodological choice that could have
caused it. Mechanism: **55% of NS definitions are used entirely within a single
community**, so breadth is nearly the constant 1 and has no variance to exploit.

**Report J is a fact about modular corpora, not about formal proofs.** Both
predictors still beat random by a wide margin in both, so early usage remains
informative; it is the bridge-shaped refinement that does not generalise.

What *did* replicate across both artifacts: **broad seams, not gateways**
(median bottleneck 0.59 vs 0.51). Your §3 hypothesis is now falsified twice.

---

## 5. Where your conceptual model stands

| your proposal | evidence |
|---|---|
| distinguish MATHLIB_DONE / LEAN_EXTERNAL_DONE / LEAN_MISSING / INTEGRATION_GAP | **strongly supported** — two artifacts in two days, neither on the 1000+ board |
| `R = R_internal + R_external` | **supported**; a single score would hide a 4-importer cul-de-sac with a 29 511-theorem neighbourhood |
| `I(T)` integration leverage | **supported but lower than theorem count suggests** — 14.2% extractable, 65% needing absent concepts, and a wide seam |
| huge regions have narrow bottlenecks | **falsified, twice** |
| the artifact as a retrospective benchmark | **excellent call** — it produced both the strongest positive and the strongest negative result here |
| compress 29 511 → concepts → regions → interfaces | **achieved**: → 36 communities → 282 interfaces |
| use statements, not machine-generated names | **correct and load-bearing** |

---

## 6. What I would ask you next

1. **Does "broad seams" survive a third artifact?** Two corpora gave one
   replication and one failure. Whether seam-breadth is a law of large formal
   proofs or a coincidence of two is now the cheapest high-value question.
2. **Should term formation be iterated?** Forming `spf` made φ reachable. The
   obvious next experiment is whether a *second round* of formation, over the
   terms the first produced, reaches an invariant the first could not. That is
   the programme's own loop, and it is now cheap to test.
3. **Is the remaining gap worth attacking directly?** Term formation works
   *within* a language whose bounded quantifiers I chose. Forming the constructs
   themselves is untouched, and I have no cheap experiment for it.

My recommendation is (2): it is the first mechanism in this programme where
discovered structure demonstrably changed what the next search could reach, and
it is the only one of the three that tests the programme's central claim rather
than mapping the terrain around it.

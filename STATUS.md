# Project status — theorem-space play

Stock-take as of 2026-09-09 (second revision; the first covered work through
Report K). Branch `claude/theorem-discovery-lab-jpbph1`. Everything below is
committed; each claim points at the report that carries it.

> **[8 Oct 2026 — read `openai-math/RESULT_INTAKE.md` before acting on anything below.]** On 6 Oct
> OpenAI published `github.com/openai/math`, 719 manuscripts claiming results on open problems.
> It claims 79 of the 499 ranked problems the board-finder mines, and the v4 thread's live target
> cr(K₇,₁₁), with a Lean statement (`board-finder/gap/v4/CLOSED_BY_165.md`). §3's line *"No Lean
> toolchain is reachable"* was true of the routes tried. The toolchain installs from GitHub's
> release assets and Mathlib builds from source on this container. The proof that closes the
> live target compiles here with only the standard axioms (`openai-math/LEAN_CHECK_165.md`), so
> the relayed verification claims in Reports H and N are now checkable too (D72).

## 1. What the project now contains

| area | location | what it is |
|---|---|---|
| the laboratory | `theorem-lab/lab.py` | the audited artifact, sha256 `bb8640cc…`, kept byte-identical |
| audit of it | `theorem-lab/audit/REPORT.md` + phase files | 15-phase independent audit |
| **stages** | `theorem-lab/stages/` | two standard stages: disagreement resolution, extrapolation licensing; 30 tests |
| cross-object I (λ) | `theorem-lab/crossobject/` | the capability test that broke the per-object ceiling (Report K) |
| cross-object II (ν) | `theorem-lab/crossobject2/` | the transfer test: does it work on a differently-shaped law? (Report L) |
| **term formation** | `theorem-lab/termform/` | can it form a term it was not given? (Report M) |
| Lean board map | `leanboard/` Reports A–E, G | 1 199 board entries scored, with a refreshable ledger |
| FLT artifact | `leanboard/flt/` Reports H, I, J | 29 511-theorem proof: boundary, compression, forecast benchmark |
| NS/Euler artifact | `leanboard/ns/` Reports N, O | 49 365-declaration proof: same analysis, different answer |

## 2. What is established

### The laboratory and its audit

The E-family pretest reproduces exactly — same candidate id, same three zeros,
186 s vs the reported 183 s. Holdout clean: 70 720 queries, 0 duplicates, 0
cross-phase overlap. Per-modulus thresholds and periods match `ν(m)` and `λ(m)`
on **48/48** moduli.

Qualified by: no modulus is held out; the calibration windows were human choices
informed by the answer, and shrinking either **refutes the candidate and exports
nothing**; the "recursive deformation" is nominal; three different
representations reach zero error, the cheapest not the one used.

**Controls.** Structured non-arithmetic world: 48/48 hidden parameters
recovered. Adversarial world: **648 final errors, REFUTED, zero exports**.

**Deformation invention: no.** No objective variant selects the human-designed
deformation; the corrected one ranks the parent family first.

### Cross-object generalisation (Reports K, L)

**The per-object ceiling is broken.** Phase 0 measured it — fitted on `m ≤ 30`,
nothing beat the majority baseline on unseen moduli (0.90823 vs 0.90823). With a
compositional language and the disagreement stage: **18/18 invariants exact,
1.00000 vs a 0.90278 baseline**, holdout untouched, one probe from a reserve.

**Transfer is partial, and the split is sharp (Report L).** Pointed at ν, whose
law is `max` not `lcm` and whose base case is the exponent, the *search
machinery and protocol transferred intact* (12/12 composable objects exact,
correct `UNDERDETERMINED` and `RESOLVED` verdicts in the two reserve arms) while
the *value vocabulary did not*: 0/6 prime powers, end-to-end **0.715, below the
0.917 baseline**. With a wrong-shaped vocabulary the system does not degrade to
baseline — it extrapolates confidently past it. One added expression took the
holdout to 18/18 and 1.000.

### Term formation (Report M)

**The system forms terms it was not given.** From nine arithmetic primitives and
two bounded quantifiers, with no `spf`, `φ`, exponent or divisor function
supplied, it formed the smallest prime factor (`least(k: n % k)`), the divisor
count, **ν as τ(n) − 1**, and **φ two different ways** — all generalising to
held-out prime powers.

v1 found nothing, and the diagnosis is the finding: the correct terms cost size
8–9 only because a formed term is re-expanded at every use. Named and counted as
a unit, they cost 5. **A system that cannot name what it formed cannot build on
it** — the same conclusion Reports A and H reached from the library side.

Every failure in that report was a **budget** (size accounting, dedup
granularity, unit caps, beam width), never the language — a different regime
from earlier phases, where vocabulary was the binding constraint.

### The two standard stages

* **`disagreement.py`** — no silent tie-breaks. Probes come only from a declared
  reserve, checked disjoint from the holdout at set-up; an unresolvable tie
  returns `UNDERDETERMINED` with every survivor.
* **`abstention.py`** — no silent extrapolation. A branch earns the right to
  extrapolate only if it reproduces every training point it covers and has
  minimum support; licensing is per branch. Applied to the Report L failure it
  turns a confidently wrong 0.715 into **coverage 0.667 at selective accuracy
  1.000**.

Both were built before the experiments that later needed them.

### The Lean board and the two external artifacts

1 199 board entries: 214 in mathlib, 1 statement-only, 30 elsewhere, 954
missing. **72% of formalized board declarations have zero in-library uses.** The
top node on both dimensions is a *typeclass*. Board value and bridge value are
measurable for completed entries and **not** per-target for missing ones.

**Two large proofs now exist outside mathlib**, from two labs, within days:

| | FLT (`aa2d8b34`) | NS/Euler (`8937a8f4`) |
|---|---|---|
| declarations | 29 511 theorems | **49 365** |
| mathlib imported | 1 696 modules (19.9%) | **303 (3.5%)** |
| modularity Q | 0.677 | 0.503 |
| communities ≥100 | 36 | 13 (largest 45%) |
| compression | → 282 interfaces | → 1 663 |
| statements in mathlib vocabulary | 15.5% (import-based) | ~30% (textual) |

Neither appears anywhere on the 1 199-entry board. "Missing from mathlib" ≠
"missing from Lean", and external territory is now a **category**, not an
exception.

### The replication failure (Report O)

Report J found breadth-across-regions forecasts load-bearing status better than
usage frequency, **6 of 6** splits on FLT. On NS: **0 of 6**, and 0 of 6 under a
loose resolution too. Mechanism: **55% of NS definitions are used within a
single community**, so breadth is nearly constant. FLT had 36 regions and
breadth varied.

Report J stands as measured; its **scope is narrower than it read**. It is a
fact about modular corpora. Both predictors still beat random by a wide margin
in both corpora — it is the bridge-shaped refinement that does not generalise.

What *did* replicate: regions joined by **broad seams, not gateways** (median
bottleneck 0.59 vs 0.51; top 1% of nodes carry 17.7% of cross traffic).

## 3. What is not established

* That the system can invent an abstraction **without a language built to reach
  it**. Term formation works, but `least` and `count` over `[1..n]` are exactly
  the constructs that make divisibility-flavoured terms cheap. Inventing bounded
  quantification itself is untouched.
* That anything here is **formally verified**. No Lean toolchain is reachable;
  `formally_verified_theorems` is 0 and accurate. Both external artifacts'
  verification claims are relayed, not reproduced.
* That the discovered mathematics is **new**. It is not — λ's multiplicativity,
  φ, and ν are all in mathlib. The value is capability, not contribution.
* That **bridge value belongs in any objective**. Report G argued no for the
  discovery engine; Report J found a narrow positive for proof engineering;
  Report O bounded that to modular corpora. Nothing here supports a general term.

## 4. The live threads

1. **Abstraction invention proper.** Term formation cleared the near end of this
   (Report M); the far end — forming the *constructs*, not terms within them — is
   untouched and is the programme's remaining capability gap.
2. **Scaling term formation.** Every failure was a budget. The obvious test is
   whether the same machinery reaches a genuinely harder invariant with more
   compute, and where it stops.
3. **A third artifact.** Two corpora produced one replication and one failure.
   A third would tell us whether "broad seams" is a law of large formal proofs
   or a coincidence of two.
4. **Upstreaming.** ~4 184 FLT theorems and a larger NS fraction are
   statement-level upstreamable. Concrete, checkable, and unverifiable here.

## 5. Recommendation

**Thread 1, informed by thread 2.** The programme's stated ambition is a system
whose discovered structure changes the representation of the next search
problem. Report M is the first time that happened mechanically — forming `spf`
made φ reachable — and it happened because a formed term became a unit. The
next experiment worth running is whether that compounds: can a second round of
formation, over the terms the first round produced, reach an invariant that the
first round could not? That is the loop the whole programme is named after, and
it is now cheap to test.

# Project status — theorem-space play

Stock-take as of 2026-09-09. Branch `claude/theorem-discovery-lab-jpbph1`.
Everything below is committed; each claim points at the report that carries it.

## 1. What the project now contains

| area | location | what it is |
|---|---|---|
| the laboratory | `theorem-lab/lab.py` | the audited artifact, sha256 `bb8640cc…`, kept byte-identical |
| audit of it | `theorem-lab/audit/REPORT.md` + phase files | 15-phase independent audit |
| stages | `theorem-lab/stages/` | reusable pipeline stages; today: disagreement resolution |
| cross-object experiment | `theorem-lab/crossobject/` | the capability test that broke the ceiling |
| Lean board map | `leanboard/` Reports A–E, G | 1 199 board entries, scored, with a refreshable ledger |
| FLT artifact analysis | `leanboard/` Reports H, I, J | 29 511-theorem proof: boundary, compression, forecast benchmark |

## 2. What is established

**About the laboratory (audit, Reports §1–§15).**
The E-family pretest reproduces exactly — same candidate id, same three zeros,
186 s vs the reported 183 s. Its holdout is clean: 70 720 queries, 0 duplicates,
0 cross-phase overlap, every final query strictly after its freeze. Per-modulus
thresholds and periods match `ν(m)` and `λ(m)` on **48/48** moduli.

But: no modulus is ever held out; the calibration windows (`d_train = 92 = 2λ(47)`,
`r_train = 8 > ν(32)`) were human choices informed by the answer, and shrinking
either **refutes the candidate and exports nothing**; the "recursive deformation"
is nominal (removing T, transport and the parent theorem leaves the E models
byte-identical); and three different representations reach zero error, the
cheapest being the one the laboratory does not use.

**Controls.** Structured non-arithmetic world: 48/48 hidden parameters
recovered. Adversarial world: validation fooled by design, then **648 final
errors, REFUTED, zero exports**. The falsification machinery is the strongest
part of the apparatus.

**Deformation invention: no.** Across 56 candidate families and three objective
variants, no variant selects the human-designed E deformation; the corrected
objective ranks the T family itself first. The reason is diagnostic: E scores
1.000 on extrapolation but 0.10 on cross-modulus invariance, because its
governing invariants are inexpressible in the available vocabulary.

**Cross-object generalisation: yes, now (Report K + `stages/`).**
Phase 0 measured the ceiling — fitted on `m ≤ 30`, nothing beat the majority
baseline on unseen moduli (0.90823 vs 0.90823). With a compositional language
and the disagreement stage: **18/18 invariants exact, end-to-end 1.00000 vs a
0.90278 baseline**, holdout untouched, one probe. The discovered rule is
mathlib's own case analysis in `Carmichael.lean`, recovered from 30 objects plus
one probe with the answer key never in scope.

**About the Lean board (Reports A–G).**
1 199 entries: 214 formalized in mathlib, 1 statement-only, 30 elsewhere, 954
missing. **72% of formalized board declarations have zero in-library uses**;
only 3 have ten or more. The top node on both board and bridge value is
`UniqueFactorizationMonoid`, a *typeclass* — the only `class` among 265
declarations. Fame and formal leverage are close to unrelated. Board value and
bridge value are measurable for completed entries and **not** measurable
per-target for missing ones; Report B says so rather than dressing class
statistics as a ranking.

**About the FLT artifact (Reports H, I, J).**
A complete 29 511-theorem proof exists outside mathlib. 0.3% of it is
FLT-specific; 65% lives in namespaces mathlib has no counterpart for. It imports
1 696 mathlib modules (19.9%). **4 184 theorems (14.2%) are upstreamable in
principle** — statement and proof free of repo definitions. Exactly one declared
name collides with mathlib. Compression: 29 511 theorems → 36 blind communities
→ 282 interfaces carrying 80% of statement usage.
Its regions are real (modularity Q = 0.677) but joined by **broad seams, not
gateways** — the top 1% of nodes carry 10.9% of cross-region traffic. And in a
forecast benchmark, **breadth across regions beats usage frequency in 6 of 6
depth splits**, with the margin widening as the horizon lengthens.

## 3. What is not established

* That the system can **invent** an abstraction. Every success so far ranks or
  composes abstractions that were already expressible. The coprime-split
  operator and `spf` were supplied; so was the E deformation itself.
* That anything here is **formally verified**. No Lean toolchain is reachable
  (`elan` is egress-blocked); `formally_verified_theorems` is 0 and accurate.
* That the discovered mathematics is **new**. It is not: λ's multiplicativity
  and prime-power values are in mathlib. The value so far is capability, not
  contribution.
* That **bridge value belongs in the discovery objective**. Report G argues no
  (it rewards proximity to what is already formalized); Report J's finding is a
  different claim about prioritising work inside a proof under construction.

## 4. The four live threads

1. **Abstraction invention.** The one capability every result points at and
   none demonstrates. Hardest, highest value.
2. **Upstreaming the 4 184.** A concrete, checkable integration task with a
   defined success criterion, but it is engineering, not discovery — and it
   cannot be verified here without a Lean toolchain.
3. **Generalising the disagreement stage.** It works with two survivors and a
   cheap reserve. Untested: many survivors, expensive probes, and probes that
   are themselves ambiguous. Cheap to run, directly strengthens the apparatus.
4. **A harder cross-object task.** The λ result used a compositional language
   built for it. A fair test needs an invariant whose law is *not* multiplicative
   — where the supplied composition operator is the wrong shape.

## 5. Recommendation

**Thread 4, then 1.** The λ success is real but its language was fitted to the
answer's shape; until the same machinery is pointed at an invariant whose law is
not a coprime-composition, we cannot tell whether we built a discoverer or a
very good lookup for one family. That test is cheap, it reuses everything
already built, and its failure mode is informative either way — which is the
property this programme has consistently got the most out of.

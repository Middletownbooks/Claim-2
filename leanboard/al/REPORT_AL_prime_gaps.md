# Arm AL — the maximal-prime-gap ladder: two AI results, complementary verification gaps

**Targets.** The two large-gap entries in the VibeMathed corpus, both at significance 60 and
both on `G(X)`, the maximal gap between consecutive primes below `X`:

| | date | model | tier | repo |
|---|---|---|---|---|
| **Sol** | 2026-08-25 | GPT 5.6 Sol | `expert-verified` | `plby/lean-proofs`, `ErdosProblems/Erdos4Tilted.lean` |
| **Astra** | 2026-09-03 | GPT 6 Astra | `site-confirmed` | `openai/LongGapsBetweenPrimes` |

Both cloned and read. Neither paper has a human author: Sol's title block reads
`\author{GPT 5.6 Sol}`; Astra's is attributed to GPT 6 Astra.

---

## 1. The ladder, checked exactly — 14/14, `verify_gap_ladder.py`

Every bound here is a **monomial** in `L1..L4 := log X, log₂X, log₃X, log₄X`, so each is an
exponent vector and every ratio is exponent subtraction. No floating point, no approximation.

| | bound | gain over predecessor |
|---|---|---|
| Rankin 1938 | `L1 L2 L4 / L3²` | — |
| FGKMT 2014 | `L1 L2 L4 / L3` | `L3` |
| **Sol** 2026-08 | `L1 L2 / L4` | `L3 / L4²` |
| **Astra** 2026-09 | `L1 L2² L4 / L3²` | `L2 L4² / L3²` |

Every claimed ratio checks:

- **Sol over FGKMT = `L3/L4²`** — the stated gain. ✅
- **Sol over Rankin = `L3²/L4²`.** Ben Green's "one now wins basically `(log₃N)²` over
  Rankin's 1938 bound" is exactly right, and the "basically" is the `L4²` denominator. ✅
- **Astra over Sol = `L2 L4²/L3²`** — the improvement factor the entry claims. ✅
- **Astra over FGKMT = `L2/L3`**, and **Astra over Rankin = `L2` exactly** — a full
  `log log X` over the 1938 bound. ✅

All four successive ratios tend to infinity, so every step is a genuine asymptotic
improvement, not a constant-factor one. **Astra strictly dominates Sol and Sol does not
dominate Astra** — they are not within a bounded factor of each other.

**The arithmetic point worth keeping:** Astra's gain over the human record is `L2/L3`, while
Sol's is `L3/L4²`. Those are not close. Astra beats FGKMT by vastly more than Sol does, and
beats Rankin by a clean `log log X`. Nine days apart, same problem, two different labs' models.

## 2. The Lean statements say what the papers say

Both verified by reading the source, and both are the exact monomials above:

- **Astra**, `Challenge.lean` (the whole file is one theorem): `∃ c X₀, 0 < c ∧ ∀ X ≥ X₀, ∃ n,`
  `p_{n+1} < X ∧ c * (log X * log(log X)^2 * log(log(log(log X))) / log(log(log X))^2) < p_{n+1} - p_n`.
  Written with `Nat.nth Nat.Prime`, no hypotheses. The identical statement appears as the
  terminal theorem of the proof file at line 4502. **My clone's HEAD is `03a1190` — the exact
  commit the site built**, so there is no version question here at all.
- **Sol**, `Erdos4Tilted.lean`: `prime_gap_corollary` and `all_endpoint_consecutive_prime_gaps`
  give `C * log X * log(log X) / log(log(log(log X))) ≤ p_{n+1} - p_n` with `p_{n+1} ≤ X`; and
  `covering_theorem` gives `c * X * log X / log(log(log X)) ≤ maximumCoverLength X`, the
  `Y(X) ≫ X log X/log₃X` claim. Also `Nat.nth Nat.Prime`, also no hypotheses.

**Zero `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`, `implemented_by` or `partial def`
outside comments** in either development: none anywhere in Astra's two files (bar the single
intentional placeholder in its comparator `Challenge.lean`), and **none across the entire
451-file import closure of `Erdos4Tilted`.**

## 3. The audit boundary stops at the repository edge — and a real dependency sits outside it

`Erdos4Tilted`'s closure reaches 451 files inside `plby/lean-proofs`, but **163 imports
resolve outside the repository**, and 211 files under `ErdosProblems/` import **`BoundedGaps`**.
That package is not in this repo. From `src/latest/lakefile.lean`:

```
require BoundedGaps from git "https://github.com/frenzymath/FormalPantheon.git" @
  "ffbb65c21afc8a36ace67720f1b0df1c63d26bd1" / "BoundedGaps"
```

and the same lakefile's `post_update` hook applies **three local compatibility patches** to it
(`formalpantheon-v4.33.0.patch`, `-s2.patch`, `boundedgaps-linter-v4.33.0.patch`) before use,
erroring out if they will not apply.

So: the chain runs `Erdos4Tilted → … → Erdos387.UniformAnalyticInputs → BoundedGaps.BombieriVinogradov.*`,
into a pinned but **locally patched** external Bombieri–Vinogradov development. **Any
"no sorry, no axiom" scan of this repository — the site's or mine — says nothing about that
package.** This is not an allegation that anything is wrong there; it is a statement about
where the audit stops. The honest form of the source-level claim is *"clean within the
repository, with a patched external analytic dependency not examined."*

Astra's repo has no such exposure: two files, Mathlib only.

## 4. Correction — a discrepancy I nearly published, and did not

I computed the 451-file / 112,449-line closure and started to set it against the site's stated
"403 Lean files, 56,614 lines," on the working assumption that the difference was version
drift since its 30 August audit. **That comparison is invalid and the user caught it before I
wrote it down.** The two numbers are not measurements of the same object: my closure crosses
result boundaries — of the 451 files, **373 are under `Erdos4` and 78 are not**, the bulk of
those being `ErdosProblems.Erdos387.*`, a different Erdős problem whose infrastructure this
proof reuses. A per-result count and a cross-result import closure are different quantities.

**There is no discrepancy finding here, and I am not reporting one.** Recorded because the
near-miss is the point: in arm AK I *did* publish a count discrepancy (27 vs 33), and there I
had controlled for version by fetching the exact tag. Here I had flagged that I still needed
to control for scope — and the scope explanation turned out to be the whole of it. **The
lesson is narrow and concrete: before reporting any count against someone else's count,
establish that both are counting the same object, not merely at the same time.**

## 5. The structural finding: complementary verification, and the stronger result is the unread one

The two results have **opposite and non-overlapping** verification profiles.

| | Sol (weaker bound) | Astra (stronger bound) |
|---|---|---|
| Expert read the argument | **Yes — Ben Green**, a co-author of the FGKMT bound it beats, after "conversations with Terry Tao and James Maynard" | **No — "no named mathematician has commented yet"** |
| Lean built / kernel-replayed | **No** — the site had no toolchain | **Yes** — clean checkout, GitHub Actions run 33843996072, 8707 jobs, `leanchecker` replay |
| Informal↔formal correspondence audited | No — "nobody without a stake has audited" it | n/a (no informal exposition to correspond to) |

**Neither result has both halves, and the halves are disjoint.** Sol has the human check and
lacks the machine check; Astra has the machine check and lacks the human check. And the
*stronger* of the two — the one that beats the fifty-year human record by a full `log log X` —
is the one **no mathematician has read**.

This is arm AJ's census thesis appearing as a concrete pair rather than a distribution:
checking is inversely related to significance, and verification effort is not tracking
mathematical weight. Here it is sharper than a correlation, because the two results are on the
*same problem*, nine days apart, and the allocation still came out backwards.

Green's own framing is worth preserving against a "merely incremental" reading of Sol: *"The
sieving procedure is different to the Erdős–Rankin one which underpinned all bounds on the
problem since 1938... one now wins basically `(log₃N)²` over Rankin's 1938 bound"*, and the
new sieve *"by itself could have claimed the Erdős 10000 dollars for this question."* §1
confirms the arithmetic behind that statement exactly.

## 6. Next

1. **Astra needs a reader, not a builder.** Its kernel check is done and mine adds nothing to
   it; what is missing is a mathematician on the short-translates proposition. That is the one
   thing this programme cannot supply.
2. **Sol needs the build.** The site could not run it; the obstacle is a toolchain plus the
   patched `BoundedGaps` dependency, not a mathematical one.
3. **`BoundedGaps` is the unexamined surface** under Sol, and it is shared by 211 files across
   several Erdős-problem formalizations in that repository — so auditing it once would cover
   many entries at a time. That is the highest-leverage target this arm found.
4. Still on the queue from arm AJ: `Prime Gaps at Most 186` (`openai/PrimeGaps186`), whose own
   site note reports **three project-specific axioms** — a rank-three hyper-Kloosterman bound,
   a rank-two Kloosterman correlation bound, and a package of numerical caps. That is the
   `lean-checked` failure mode in its most explicit form and it deserves an arm of its own.

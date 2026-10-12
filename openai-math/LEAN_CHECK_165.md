# Lean check of openai/math family 165 — the Zarankiewicz crossing-number proof

**Result: it compiles.** `lake build OAI.Combinatorics.Crossing.Main` completed all 2,581 jobs
with exit 0, in **33 minutes** on 4 cores, Mathlib built from source. `#print axioms` on the main
theorem returns exactly Lean's three standard axioms: `propext`, `Classical.choice`,
`Quot.sound`. So there is no `sorry` (`sorryAx`) and no `native_decide` (`Lean.ofReduceBool`).
The printed statement is the challenge's.

This is the first Lean toolchain this project has run. `../STATUS.md` §3, Report H and Report N
all record that none was reachable. That was true of the routes tried: `elan.lean-lang.org`,
`releases.lean-lang.org` and Mathlib's binary cache.

## 1. What is being checked

openai/math's statement `OAI.Zarankiewicz.MainTarget`
(lean/ComparatorChallenges/BipartiteCrossing.lean in openai/math): for every m, n > 0, some
admissible drawing of K_{m,n} has exactly `axisPairs m * axisPairs n` crossings, and every
admissible drawing has at least that many. `axisPairs r = (r/2)*((r-1)/2)` is Zarankiewicz's
Z(r). The solution is `OAI.Zarankiewicz.mainTarget_proof` in
lean/OAI/Combinatorics/Crossing/Main.lean, across 339 files and 20,617 lines that import nothing
but Mathlib.

## 2. The statement is the one a reader sees

`lean_check_165/diff_definitions.py`: **11 of 11** top-level definitions in the challenge file
occur character for character in the solution's definition files (`axisPairs`, `Plane`,
`BipartiteVertex`, `BipartiteEdge`, `ContinuousDrawing`, `edgeInterior`, `ProperCrossing`,
`crossingPoints`, `AdmissibleDrawing`, `crossingCount`, `MainTarget`). Comparator does this
comparison mechanically. It is not installed here, because it needs `landrun` and `lean4export`,
so this is the textual half of it.

Read as mathematics, the definitions are the ordinary crossing number. Arcs are injective paths
whose interiors avoid vertices. Crossings are finite in number and each is a proper transverse
crossing (a chart taking the two arcs to the coordinate axes). No point lies on three edge
interiors. Adjacent edges are not forbidden from crossing, which makes the lower bound stronger,
not weaker.

## 3. The environment matches openai/math's exactly

| | here | openai/math lean/ |
|---|---|---|
| toolchain | `leanprover/lean4:v4.34.1` (commit `5045d00`) | `leanprover/lean4:v4.34.1` |
| Mathlib | `d13f23b723b8` | `d13f23b723b8` |
| plausible, LeanSearchClient, importGraph, proofwidgets, aesop, Qq, batteries, Cli | resolved by Lake from Mathlib's manifest | **all 9 revisions identical** to openai/math's `lake-manifest.json` |

Mathlib is unpatched in openai/math; its `patches/` touch other dependencies only, and none of
those are imported here.

**Route that worked**, recorded in `lean_check_165/run.sh`:

- `elan-init.sh` from raw.githubusercontent.com;
- the toolchain tarball from GitHub release assets, linked into elan, since `elan toolchain
  install` goes to releases.lean-lang.org (403);
- Mathlib built from source, since cache.mathlib.org also returns 403 and `lake exe cache get`
  fails.

The proof's import closure is about 2,770 modules: Mathlib 1,974, the proof's own 339, and the
rest Lean core, Batteries, Aesop and the other dependencies. Machine: 4 cores, 15 GB.

## 4. Build result

From the build log, 8 Oct 2026 (UTC):

| | |
|---|---|
| `lake update` start | 14:09:38 |
| `lake build OAI.Combinatorics.Crossing.Main` start | 14:09:42 |
| finished | **`Build completed successfully (2581 jobs).`**, exit 0, by 14:42:43 |
| wall clock | **~33 minutes**: Mathlib's needed subset and dependencies from source, then the 339 proof files, each 1–3 s |

`Check.lean`, run with `lake env lean`:

```
'OAI.Zarankiewicz.mainTarget_proof' depends on axioms: [propext, Classical.choice, Quot.sound]
OAI.Zarankiewicz.mainTarget_proof : OAI.Zarankiewicz.MainTarget
def OAI.Zarankiewicz.MainTarget : Prop :=
∀ (m n : ℕ),
  0 < m →
    0 < n →
      (∃ D, OAI.Zarankiewicz.crossingCount D = OAI.Zarankiewicz.axisPairs m * OAI.Zarankiewicz.axisPairs n) ∧
        ∀ (D : OAI.Zarankiewicz.AdmissibleDrawing m n),
          OAI.Zarankiewicz.axisPairs m * OAI.Zarankiewicz.axisPairs n ≤ OAI.Zarankiewicz.crossingCount D
'OAI.Zarankiewicz.ordinary_crossing_number_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The `example : axisPairs 7 * axisPairs 11 = 225 := by decide` line elaborated with no error, so the
formal statement's value at this branch's target is 225. A source scan of the 339 files finds no
`sorry`, `native_decide`, `implemented_by`, `extern` or `axiom` declaration.

## 5. What this does and does not establish

**Established here:** a Lean 4.34.1 kernel, with Mathlib at openai/math's pinned commit, accepts a
proof of `MainTarget` using only the standard axioms. Its definitions are character-identical to
the Comparator challenge's (§2), and the challenge says what Zarankiewicz's conjecture says
(§2). Within this project's evidence discipline, that moves family 165 from *relayed formal claim*
to **checked here**, the first such move in the tree.

**Not established:**

- **Comparator was not run.** It also checks that the exported environment matches the challenge
  statement-by-statement, and §2's textual diff is the substitute.
- **The paper's Appendix A**, reducing arbitrary drawings to admissible ones, is not formal. For
  the question this branch asked, whether some drawing of K₇,₁₁ has 221 or 223 crossings, the
  classical normalisation closes that gap. Any such drawing could be made admissible without
  adding crossings.
- **No other openai/math family was compiled.** Every other FORMAL tier in this directory relays
  openai/math's own scope note.

**Cost, for planning.** One proof with ~2,000 Mathlib modules in its import closure took 33 minutes
from a cold start, and 3.0 GB under `.lake/`. Reports H and N (FLT, NS/Euler) pin different Mathlib
commits and are far larger, so their builds would cost more. The route is the same.

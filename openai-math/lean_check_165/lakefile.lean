import Lake
open Lake DSL

-- Minimal re-host of openai/math's Zarankiewicz crossing-number formalization (family 165):
-- the same Lean toolchain and the same Mathlib commit as openai/math lean/lakefile.lean,
-- and only the 339 files under OAI/Combinatorics/Crossing, which import nothing but Mathlib.
package leancheck where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

lean_lib OAI where
  globs := #[.submodules `OAI.Combinatorics.Crossing]

lean_lib Check where

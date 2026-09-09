# Lean 1000+ board and bridge map — Phase 0

Machine-readable map of the [1000+ theorems project](https://1000-plus.github.io/)
board as it exists in Lean/mathlib, built to guide (not yet drive) the
theorem-space discovery experiments in `../theorem-lab/`.

## Retrieval and versions

| | |
|---|---|
| Retrieved (UTC) | **2026-09-09T00:33:03Z** |
| mathlib4 commit | `110cb7f03dd1c2d9edd957b937f55175c9fc3343` (2026-09-08 22:52 UTC) |
| Lean toolchain | `leanprover/lean4:v4.34.0-rc2` |
| upstream 1000-plus commit | `8e04b97dd24adc6e931be78a884da7e935bc8780` (2026-07-22) |
| mathlib modules parsed | 8 513 |
| declarations indexed | 387 719 |
| import edges | 26 709 |
| history window for growth | 2 000 commits, 2026-06-17 → 2026-09-08 |

### The two requested pages could not be retrieved

`https://leanprover-community.github.io/1000.html` and `.../1000-missing.html`
are **unreachable from this environment**: the egress proxy answers `403` to
CONNECT for `leanprover-community.github.io`, via both `curl` and the WebFetch
tool (the proxy's own failure log records the denials). Rather than work from
an assumed historical copy, this analysis uses the **sources those pages are
generated from**, which are reachable:

* `mathlib4:docs/1000.yaml` — the file that both pages render. Its header says
  it "tracks the formalisation status of theorems from the experimental 1000+
  theorems project", and mathlib's `scripts/yaml_check.py` notes it is kept "in
  sync with `make_site.py` in the leanprover-community.github.io repo".
  1000.html renders the entries that carry a declaration; 1000-missing.html
  renders the rest.
* `1000-plus/1000-plus.github.io:_thm/*.md` — the upstream project's own
  records: wikidata id, MSC classification, wikipedia links, and status for
  **every** proof assistant (Lean, Isabelle, Rocq, HOL Light, Metamath, Mizar).

This substitution is strictly more informative than the rendered pages (it adds
MSC classes and other-assistant status), but it is a substitution, and any
divergence between the yaml and today's rendered HTML would not be visible here.

## Board composition (from `board.json`)

| status | count |
|---|---|
| formalized in mathlib | **214** |
| statement only in mathlib (`FermatLastTheorem`) | **1** |
| formalized outside mathlib (entry carries a URL) | **30** |
| missing | **954** |
| total entries in mathlib's yaml | **1 199** |

The upstream repo carries 1 183 entries; 7 exist upstream but not in mathlib's
yaml (listed in `board.json`), reflecting the 7-week gap between the two commits.

## Pipeline

| script | output | what it establishes |
|---|---|---|
| `ingest.py` | `board.json` | normalized record per entry; nothing invented, absent fields are `null` |
| `structure.py` | `modules.json`, `decls.json` | **exact** module import graph + transitive closures; namespace-tracking declaration index |
| `usage.py` | `usage.json` | textual usage and cross-area spread per board declaration |
| `proximity.py` | `proximity.json` | whether mathlib already *names* a missing target |
| `analyze.py` | `scores.json` | area statistics, declaration kinds, board/bridge/difficulty scores |
| `ledger.py` | `bridge_ledger.json/.csv` | Report F, refreshable |

Reports A–E and G are the markdown files in this directory.

## Evidence discipline

Every claim in the reports carries one of the prompt's five labels. The mapping
to what this pipeline can actually observe:

| label | what earns it here |
|---|---|
| `ACTUAL_LEAN_DEPENDENCY` | an import edge in `modules.json` (parsed from source, exact at module granularity) |
| `ACTUAL_SHARED_ABSTRACTION` | a declaration textually referenced across areas, or a shared typeclass/structure named in source |
| `DOCUMENTED_MATHEMATICAL_RELATION` | mathlib prose (docstring/comment) states the relation |
| `PLAUSIBLE_FORMAL_BRIDGE` | the mathematics is standard and the prerequisites exist in mathlib, but no formal link exists |
| `SPECULATIVE_RESEARCH_BRIDGE` | would need substantial new mathematics or infrastructure |

Nothing is upgraded across those lines. In particular **no declaration-level
dependency claim is made anywhere**: mathlib is not compiled here, so
declaration-level "uses" edges are textual approximations, and are labelled as
`ACTUAL_SHARED_ABSTRACTION` at best.

## Known measurement limits (all of them matter)

1. **Typeclass-mediated use is invisible.** Instances are consumed by
   inference, not by name. `Complex.isAlgClosed` (fundamental theorem of
   algebra) shows 1 textual use and is in reality one of the most-used facts in
   the analysis library. Rows whose kind is `instance`/`class` carry an explicit
   `usage_undercount_warning`; for those, module reach is the better signal.
2. **Short vs full names bracket the truth.** Inside its own namespace a
   declaration is referenced by its short name, so full-name counts undercount
   and short-name counts overcount (`toDual`, `proper` are ordinary words). Both
   are recorded; scores use the full-name count, and an earlier version of the
   bridge score that used the short-name count was discarded for this reason.
3. **An import-parser bug was found and fixed mid-analysis.** mathlib has
   migrated to `public import`; a regex matching only bare `import` captured
   593 of 26 709 edges (2.2%) and produced a near-empty graph. Every number
   here is from the corrected parser. This is exactly the kind of drift the
   ledger exists to catch.
4. **Missing-target scores are mostly class-level.** Area size, growth and MSC
   cluster size are identical for every target in a class, so they rank classes,
   not targets. `proximity.py` adds the only per-target observable available
   without formalizing anything — whether mathlib *names* the target — and even
   that is limited: a bare surname ("Euler", "Frobenius") cannot separate the
   several theorems bearing it, so such rows are marked
   `discriminating: false`. Report B is honest about the resulting resolution.
5. **Unqualified declaration names need a root-level preference.** mathlib
   contains `theorem add_pow` inside `namespace Tropical` as well as the
   binomial theorem's root-level `add_pow`; scanning in path order let the
   tropical one claim the bare key, misattributing the board's most
   cross-domain theorem to the tropical semiring. The index now prefers
   root-level declarations for unqualified names. Any refresh should re-check
   board entries whose `decl` is unqualified.
6. **Textual matching found author names.** The first proximity run scored
   "Lee–Yang theorem" at 368 files because mathlib file headers list authors
   named Lee and Yang. Header lines are now excluded and tokens appearing in
   >40 files are dropped as generic.

## Refreshing this map

```bash
git -C ~/leanprover-community/mathlib4 pull          # or re-clone at a new commit
git -C ~/1000-plus/1000-plus.github.io pull
python3 ingest.py && python3 structure.py && python3 usage.py \
  && python3 proximity.py && python3 analyze.py && python3 ledger.py
```

Then diff the new `bridge_ledger.json` against the old one by `wikidata`:

* `status` missing → formalized: **new formalization**;
* `defining_module` or `lean_decls` changed: **rename/move** (the ledger is the
  only place that would notice a silent rename);
* `module_transitive_importers` up sharply: **a region opened**;
* `mathlib_mentions` 0 → >0: **a corridor started**;
* `bridge_difficulty` down: prerequisites landed, **a bridge became viable**.

Weights live in `analyze.py` (`B_WEIGHTS`, `R_WEIGHTS`) and every row keeps its
raw components, so any ranking here can be recomputed under different weights
without re-running the expensive steps.

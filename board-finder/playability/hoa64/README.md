# hoa64 — assessment

Scripts backing `../HOA64_ASSESSMENT.md`. Both are standalone; neither imports the
repo being assessed, except `coverage.py`'s replication of its documented conditions.

| file | what it does |
|---|---|
| `verify_matrices.py` | checks every shipped matrix is genuinely Hadamard: ±1 entries and H Hᵀ = nI in exact integer arithmetic. **13/13 pass** |
| `coverage.py` | replicates hoa64's closed-form construction conditions and computes which orders in [2000,3000] they reach, which they miss, and why 2060 in particular is missed |
| `by_m.py` | the same question indexed by m (n = 4m, m odd — hoa64's own 4-mod-8 observation), with the Williamson order each survivor needs |
| `cw_route.py` | **the cross-repo result.** The five composite v among the thirteen open orders, the one Williamson order each needs, both 2060/2884 paths validated, and a measurement showing hoa64's Williamson engine cannot supply W(103) |

See `../HADAMARD_CROSS.md` for the write-up.

Assessed against `github.com/bbeartheancient/hoa64` at commit `d825201`, 2026-08-15.

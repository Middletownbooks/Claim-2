# hoa64 — assessment

Scripts backing `../HOA64_ASSESSMENT.md`. Both are standalone; neither imports the
repo being assessed, except `coverage.py`'s replication of its documented conditions.

| file | what it does |
|---|---|
| `verify_matrices.py` | checks every shipped matrix is genuinely Hadamard: ±1 entries and H Hᵀ = nI in exact integer arithmetic. **13/13 pass** |
| `coverage.py` | replicates hoa64's closed-form construction conditions and computes which orders in [2000,3000] they reach, which they miss, and why 2060 in particular is missed |

Assessed against `github.com/bbeartheancient/hoa64` at commit `d825201`, 2026-08-15.

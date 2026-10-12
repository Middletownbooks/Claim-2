# P1 reference — the encoding being diffed against

Source: Fable's response to `leanboard/ad/FABLE_PROMPT.md`, delivered in
conversation on 2026-09-18, section **P1 §1.2 "Cases: before-board and leak"**.
Fable had no repository access, so this table exists nowhere else in the repo.
The five rows used by L2 are transcribed verbatim below so the diff is auditable.

Fable's own header for the table: *"Slots are S (state), M (move), I (invariant),
C (composition), T (terminal certificate)."* Rows omit slots Fable did not fill;
those omissions are reproduced here rather than patched, because they are part of
what L2 measures.

| # | Problem | Before-board | Bound then | Leak |
|---|---|---|---|---|
| **1** | Sensitivity | **S:** induced subgraph H of Q_n with 2^{n−1}+1 vertices (Gotsman–Linial 1992 reduction).<br>**M:** subcube refinement.<br>**I:** edge-isoperimetric/degree-sum counts.<br>**T:** Δ(H) ≥ f(n). | Δ ≥ (½−o(1))log n (Chung–Füredi–Graham–Seymour 1988); conjectured √n. | Counting controls mean degree, not max. The unsigned spectrum of Q_n is n−2k, additive under Cartesian product, so the median eigenvalue is ≈0 and interlacing is empty. |
| **2** | Cap set | **S:** A ⊆ F_3^n with density δ and no 3AP.<br>**M:** large Fourier coefficient → restrict to a hyperplane.<br>**I:** density increment δ→δ+cδ².<br>**C:** ~1/δ iterations, one dimension each.<br>**T:** dimensions exhausted. | 3^n/n (Meshulam 1995); n^{1+ε} (Bateman–Katz 2012). | The per-step gain δ² combined with the additive cost of one dimension per step forces δ ≳ 1/n. The invariant composes additively, while the target (max cap size) is supermultiplicative under products, so the truth has form c^n. |
| **5** | Finite-field Kakeya | **S:** Kakeya set K ⊆ F_q^n.<br>**M:** bush/hairbrush incidence counting.<br>**I:** Cauchy–Schwarz incidence inequalities (plus sum-product). | \|K\| ≳ q^{(n+2)/2}, later ≈q^{4n/7}. | Cauchy–Schwarz sees pairwise line interactions only, which caps the exponent near n/2. |
| **8** | Spencer set discrepancy | **S:** colouring of n points with n sets.<br>**M:** uniform random colouring.<br>**I:** per-set Chernoff bound.<br>**C:** union over n sets. | √(n log n). | √log n comes from the union bound over sets. |
| **9** | Vinogradov mean value | **S:** mean value J_{s,k}.<br>**M:** p-adic congruencing iteration.<br>**I:** recursive inequality on J. | s ≳ c·k² log k (classical). [K, medium confidence] | Each iteration recovers a fixed fraction of the defect, so ~log k rounds are needed. |

Fable's `[K]` tag means "recalled from literature and not re-fetched this
session, so verify citations before relying on them". Case 9's bound carries it
explicitly, together with "medium confidence".

## Fable's own statement of what this encoding is worth

From P1 §1.4, "The benchmark cannot detect":

> *Hindsight in my encoding.* This v0 is single-encoder and contaminated. L2 has
> not been done.

L2 is that step.

## Slots Fable left empty

| case | S | M | I | C | T |
|---|---|---|---|---|---|
| 1 | ✓ | ✓ | ✓ | — | ✓ |
| 2 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 | ✓ | ✓ | ✓ | — | — |
| 8 | ✓ | ✓ | ✓ | ✓ | — |
| 9 | ✓ | ✓ | ✓ | — | — |

`composition` is absent in 3 of 5, `terminal` in 3 of 5: 6 of 25 slot-pairs
cannot be diffed because one side is empty.

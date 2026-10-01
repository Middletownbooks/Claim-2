# Intake bundle, 1 Oct 2026

| | |
|---|---|
| files | `README.upstream.md`, `cog.py`, `checkers.py`, `search.py`, `generator.py`, `certificate.py`, `reproduce.py` |
| produced by | the other instance, in a chat sandbox with no version control |
| arrived | 1 Oct 2026, pasted by the operator — `generator.py` first, then the complete bundle |
| call budget on the producing side | 100–300 s per call, no checkpointing |
| **tier** | **`PRIMARY-VERIFIED-LOCALLY`** for everything `reproduce.py` asserts; `SECONDARY-RELAYED` for every figure in `README.upstream.md` and in `search.MEASURED` that no control re-derives |

## Run here

```
python3 reproduce.py --n6 --certificate      ->  13/13 controls passed
```

Requires numpy only (2.4.6 present). The exhaustive n = 6 sweep — 6,930 classes, four
readings — took **32 s**.

What that promotes to `PRIMARY-VERIFIED-LOCALLY`, having previously been relayed prose:

* Woodall's 32 classes of (5,5)-sets at antisum 16, and the unique (7,5)-set at 34;
* the K₇,₇ staircase **79, 56, 36, 21, 9, 3** — so the prefix bounds this programme's own orbit
  counts were computed against are the right ones;
* every (5,7)-set has antisum ≥ 36, by a zero-survivor sweep in **9,333 nodes**;
* Theorem 7 availability — m = 7 via m′ ∈ {2,4}, m = 9 via m′ = 4 only, **m = 11 none** — and the
  weakened bounds **{2: 221, 4: 223, 6: 215}**, which is the derivation this side reconstructed
  from Theorem 2's printed proof, now reproduced by their code;
* the CO₄ family sizes 234 / 282 / 594 / 1758 and the lattice's shape;
* the certified generator: **120/120** pair-optimal drawings tight and pseudo-tight;
* the published (4,6)-set at antisum 15, pseudo-tight at `both` and not tight at `arbitrary`,
  with antidistances 3, 4, 2, 3, 2, 1 and a geometric realisation at 37 crossings;
* all 14 core sets, counterexamples under every reading;
* the n = 6 census: 6,930 classes, per-reading 48 / 19 / 54 / 22, core 14, any 59.

## Still `SECONDARY-RELAYED`

Nothing in `reproduce.py` re-derives these, so they stay relayed until run here: the 1.30×
ablation, the (11,7) frontier's 288 sets at antisum 221, the 217k-vs-98k throughput pair, the
generator's reach rates, the AUC figures, and the (5,7) clause ablation 195,110 / 129,044 /
14,119 / 9,333 — of which **only the last number, 9,333, is confirmed above.**

One arithmetic defect in the relayed figures, checked locally: the generator's reach is stated as
(single-pair rate)^C(m,2) at 0.4045, but the three measured points run **above** that model by
1.6×, 3.5× and 24.4×, so the m = 11 figure 2.4 × 10⁻²² — which is the model evaluated at m = 11,
not a measurement — understates the true rate. It does not matter for their conclusion. Separately
the m = 7 point, "0 in 20,586 trials", has no power: the model predicts 1.2 × 10⁻⁴ expected hits,
so a zero is consistent with any rate below ~1.5 × 10⁻⁴ and discriminates nothing.

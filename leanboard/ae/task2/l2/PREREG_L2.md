# PREREG — Task 2 step L2: blind re-encoding diff

Written and committed before any encoder runs.

## Design

Fable's P1 §1.2 supplies one encoding of each before-board. It was produced by a
single model that knows every answer; the handoff calls this out and asks for an
independent re-encoding to diff against.

Five cases, chosen to span fields and to include both of the verification debts
the handoff flagged:

| # | case | cutoff (encoder may use nothing later) | why chosen |
|---|---|---|---|
| 1 | sensitivity conjecture | 2019-06-30 | clean, well-documented before-state |
| 2 | cap set | 2016-04-30 | Fable claims the needed move runs opposite to de-tensorize here |
| 5 | finite-field Kakeya | 2008-02-29 | **flagged debt**: the pre-Dvir exponent |
| 8 | Spencer set discrepancy | 1984-12-31 | leak is a union bound, the catalogue's clearest case |
| 9 | Vinogradov mean value | 2011-12-31 | **flagged debt**: the k^2 log k bound and the "log k rounds" leak |

Calibration cases (Banaszczyk, Bansal–Jiang, Guo–Fang–Lu) are excluded: they
generated the taxonomy.

One subagent per case. Each sees only its own case, the cutoff, and the schema.
None sees Fable's encoding, the held-out after-board, or any other encoder.

## Diff protocol

Both encodings of a case are presented to diff-raters as X and Y in randomised
order, with no indication of provenance. Each of the five board slots plus
`bound` is marked AGREE / PARTIAL / DISAGREE. Cohen's kappa is computed on the
binary AGREE-vs-not collapse. `leaks` is scored separately as set overlap on the
`mechanism` field.

## Declared predictions

**L2-1. Slot agreement is lowest on the leak table and highest on `state`.**
`state` is close to forced by the problem statement; the leak is interpretive.
Confidence: moderate-high.

**L2-2. Kappa on the AGREE-vs-not collapse is below 0.6.** Confidence: moderate.
Step D produced 0.048 on a coarser task with six options; slot diffing has three
options and more anchoring in the problem, so I expect higher but still short of
0.6.

**L2-3. At least one of the two flagged debts (cases 5, 9) shows DISAGREE on
`bound`.** This is the point of including them. Confidence: moderate.

**L2-4. Recognition is near-universal again.** As in step D, where it was 5 of 5
on scored cases. If so, "use only pre-cutoff sources" is a request the encoder
cannot actually honour, and that should be reported as a limit on the whole L2
design rather than buried. Confidence: high.

## What this can and cannot establish

Can: that two encoders of the same before-board disagree, and where.

Cannot: that either encoding is *correct*. A diff measures reproducibility, not
accuracy. Both encoders may be wrong in the same place, and agreement there
would be scored as success. Cases 5 and 9 partially address this by targeting
claims already suspected of being wrong.

Cannot: escape contamination. Both encoders know the answers. L2 relocates
contamination from the label to the encoding; it does not remove it.

# Laboratory stages

Reusable stages that sit between the laboratory's fitting and its final scoring.

## `disagreement.py` — disagreement resolution

**Status: standard stage.** Promoted from the post-hoc extension in Report K
after it converted a wrong law into the right one for one observation.

### The problem it solves

Selection stages rank hypotheses by error and break ties by cost or identifier.
Report K measured what that costs: on the cross-object task `lcm` and `max` both
scored **30/30** on the training objects — among all coprime splits of `m ≤ 30`
one period always divides the other, so the two are *observationally identical
there* — and the tie-break chose `max`, which is wrong at m=35 and m=45.

That is an **identifiability** failure, not a modelling error, and no amount of
looking at the training set reveals it. But it is detectable with no answer key:
surviving hypotheses disagree about a specific, nameable object.

### Protocol rules, enforced by construction

1. **Probes come only from a declared reserve.** `resolve(...)` will not probe
   outside it, and `assert_disjoint(reserve, holdout)` fails loudly at set-up if
   the reserve would leak the final holdout. Resolving a tie can never consume
   held-out data.
2. **Every probe is logged** with the disagreement that motivated it, each
   survivor's prediction, the observed value, and the survivors before and after.
3. **No silent tie-breaks.** If the reserve separates nothing, or the budget
   runs out, the verdict is `UNDERDETERMINED` and every survivor is returned.
   "The data does not determine the law, and here are the candidates" is a
   result, not a failure to produce one.
4. **A hypothesis space that excludes the truth is flagged**: if every survivor
   mispredicts a probe, the verdict is `SPACE_EXCLUDES_TRUTH`.

### Verdicts

| verdict | meaning |
|---|---|
| `UNIQUE` | no tie; nothing to resolve |
| `RESOLVED` | one hypothesis survives; `selected` is set |
| `UNDERDETERMINED` | several survive; the data cannot separate them |
| `SPACE_EXCLUDES_TRUTH` | every survivor mispredicted an observation |

### Usage

```python
from disagreement import assert_disjoint, resolve

assert_disjoint(reserve, holdout)          # at set-up, before any query
res = resolve(hypotheses, score, predict, reserve, observe, max_probes=8)
if res.verdict == "RESOLVED":
    use(res.selected)
elif res.verdict == "UNDERDETERMINED":
    report(res.survivors)                  # never tie-break silently
```

`score` maps a hypothesis to a comparable value on data already seen (lower is
better); ties in it are what gets resolved. `predict(h, coord)` returning `None`
means "undefined here", and such coordinates are skipped rather than treated as
a disagreement.

### Demonstrated result

`crossobject/crossobject_v2.py` runs the cross-object experiment through this
stage with training `[1,30]`, reserve `[49,60]`, holdout `[31,48]`:

| | Report K main run | with this stage |
|---|---|---|
| composition law chosen | `max` (wrong) | **`lcm`** |
| invariants exact | 16/18 | **18/18** |
| end-to-end accuracy | 0.99048 | **1.00000** |
| holdout consumed to get there | — | **none** |
| probes | — | 1 (object m=55) |

Baseline for the task is 0.90278, and Phase 0's best model beat it by 0.00000.

### Tests

`python3 test_disagreement.py` — 16 assertions covering all four verdicts,
budget limits, reserve discipline, multi-round resolution, and the property
that agreeing coordinates are never probed.

### Not yet wired into `lab.py`

`lab.py` is the audited artifact; its sha256 (`bb8640cc…`) is cited across the
audit reports, so it is left byte-identical and the stage is used by drivers
that import it. The natural wiring points, when a `lab2.py` is written, are the
two selection sites: `table_experiment`'s `min(entries, key=validation_rank)`
(line 901) and `tensor_experiment`'s `min(entries, key=rank)` (line 1478). Both
currently break ties by symbol cost and then by identifier — exactly the silent
tie-break this stage exists to replace. A probe reserve would have to be carved
out of the coordinate space first; today the laboratory's grid leaves none.

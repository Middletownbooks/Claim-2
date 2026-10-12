# Schema for task 2 step C — `cases/<n>/before.json`

The blind encoder sees ONLY the problem statement and a date cutoff. It never
sees `heldout/<n>.json`.

```json
{
  "case": "<short name>",
  "cutoff": "<ISO date: the encoder may use nothing published after this>",
  "target": "<the statement being attacked, in one sentence>",
  "board": {
    "state":     "<what an in-progress attempt carries>",
    "move":      "<the legal step, and whether it is a formula or needs an existence theorem>",
    "invariant": "<what the move preserves>",
    "composition": "<why steps chain>",
    "terminal":  "<what a finished state certifies>"
  },
  "bound": "<the best result of this shape at the cutoff, as a formula>",
  "leaks": [
    {"factor": "<e.g. sqrt(log n)>",
     "mechanism": "<union bound over m items | multiplicative invariant | terminal certificate | feasibility theorem | iteration count | other>",
     "evidence": "<the step where it enters>"}
  ],
  "sources": ["<pre-cutoff citations only>"]
}
```

`heldout/<n>.json` carries `{"after_board": {...same five slots...},
"transformation": "<one of the five, or none>", "superseding_work": "<citation>"}`
and is read by nobody who is scored.

**Diff protocol.** Two encodings of the same case are compared slot by slot.
Each of the five slots plus `bound` is marked AGREE / PARTIAL / DISAGREE by a
third rater who sees both encodings without knowing which came from which
source. Cohen's kappa is computed on the binary AGREE-vs-not collapse, per slot
and pooled. `leaks` is scored separately as set overlap on the `mechanism`
field, since the factor names are more standardised than the prose.

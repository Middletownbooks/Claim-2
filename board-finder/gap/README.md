# gap/ — the counterexample-and-construction gap analysis

Separate from `../playability/`, which mines the 499-record ranked corpus. This directory
looks for **named open conjectures in the primary literature that are not on an enumerable
public problem list** — the July 2026 gap analysis's own best finding was that curated lists
are being swept by agent pipelines, so off-list is where the value is.

| file | what it is |
|---|---|
| `REVIEW_JULY_GAP_ANALYSIS.md` | check of the July 2026 response. Four claims verified here (Kalai 3^d, Tuza K₄/K₅, Ball at p=2, the Kaplansky nesting); four defects, the worst being that its dimension F rewards exactly the property that made Zauner/SIC worthless; three things kept verbatim |
| `PROMPT_GAP_v2.md` | the rebuilt prompt. Part A pasteable, Part B operator notes with each clause traced to what it is built against |

## The one-line version of what changed

The July rubric asked *"does generalizing to more variables loosen the constraints?"* and
rewarded a rich parameter space. Zauner/SIC scores maximally on that and is worthless; Hadamard
has the identical surface shape and is the one target on this board that has paid. The
difference is whether **the unknown set can be written down** — thirteen orders versus an open
tail. v2 scores that directly and drops the old dimension.

Three smaller changes, each with a receipt: witness polarity is declared rather than excluded
(so construction targets are in scope); every candidate must carry a **premise-falsification
line, run during triage** (one line of arithmetic killed a route here after a day's work); and
only status-verified candidates are ranked, because 20 of the July response's 31 rows were
unconfirmed recall in a field turning over at ~40 AI-resolution claims a month.

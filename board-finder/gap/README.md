# gap/ — the counterexample-and-construction gap analysis

Separate from `../playability/`, which mines the 499-record ranked corpus. This directory
looks for **named open conjectures in the primary literature that are not on an enumerable
public problem list** — the July 2026 gap analysis's own best finding was that curated lists
are being swept by agent pipelines, so off-list is where the value is.

| file | what it is |
|---|---|
| `REVIEW_JULY_GAP_ANALYSIS.md` | check of the July 2026 response. Four claims verified here (Kalai 3^d, Tuza K₄/K₅, Ball at p=2, the Kaplansky nesting); four defects, the worst being that its dimension F rewards exactly the property that made Zauner/SIC worthless; three things kept verbatim |
| `PROMPT_GAP_v2.md` | the rebuilt prompt. Part A pasteable, Part B operator notes with each clause traced to what it is built against |
| `RESULT_GAP_v2.md` | **it ran.** Passed its own bar narrowly — four candidates at D=5, two of them killed by their own falsification lines. Closes two unverified-pool items from work on this branch, and carries one correction to the prompt itself |

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


## What the run changed about the prompt

The v2 prompt put the public-list anti-criterion in the anti-criteria section, i.e. applied at
exclusion time. The run showed that is the wrong place: **the properties that score well on A–C
and G–H are the same properties a benchmark designer selects for**, so the list check is in
direct tension with the scoring function and belongs at **step 0**, as a filter. Conway's
99-graph and the missing Moore graph are the two best problems in mathematics by this rubric and
are both already on FrontierMath: Open Problems for exactly that reason.

Four agent-facing databases are now known — FrontierMath: Open Problems, TheoremDB,
Horizon/HorizonMath, erdosproblems.com. Epoch's own submission criteria paraphrase this
commission. v3 should enumerate those first and build the exclusion set before casting the net.

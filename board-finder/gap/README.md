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
| `sources/GAP_V2_RESPONSE_RAW.md` | the verbatim response. Cited by `RESULT_GAP_v2.md` from the start, actually written on 21 Sep after the citation was found dangling |
| `sources/EPOCH_UNSOLVED_LIST.md` | all 41 unsolved FrontierMath: Open Problems entries, transcribed from nine screenshots because the site's zip would not open. Carries its own completeness argument, including the one entry the relayed counts cannot account for |
| `epoch_exclusions.json` | derived from the transcription by script, not typed twice |
| `epoch_gate.py` | the diff. Screens 22 live items on distinctive object tokens, then refuses to return a verdict until every collision carries a reasoned adjudication. Two positive controls abort the run if the matcher breaks |
| `GATE_EPOCH.md` | **the gate result.** PTE 11, MOLS(10) and Costas 32/33 clear; pool items U6 and U7 are on the list and dead; the 3×3-vs-4×4 matmul near-miss; and why Epoch's type tags are a different axis from our screen's |

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

## The gate that was outstanding is closed

`RESULT_GAP_v2.md` §5 said nothing should start until the four ranked candidates were diffed
against Epoch's full fifty rather than the ten that were readable. That ran on 21 Sep against all
41 unsolved entries. **PTE size 11 is cleared and is the first target.** The gate also paid for
itself twice over by retiring two unverified-pool items that would each have needed a promoting
search.

One finding from it belongs here rather than in the result file: **Epoch's list contains no
Hadamard-family problem at all** — not Hadamard, skew-Hadamard, Williamson, propus or D-optimal
designs, and those five items return no token collision with any of the 41. The Hadamard
*problem* is on TheoremDB and Horizon; the thirteen open orders between 2000 and 3000 are on
none of the four known databases. That is the one asset on this board the commons has not
already enumerated.

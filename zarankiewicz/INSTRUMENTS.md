# Twenty-one instruments or records that were wrong while looking right

None of them errored. That is the whole point: every one produced a number, or a verdict, or a
passing check, and the number was wrong or the verdict was empty. A tool that crashes announces
itself. These did not.

**The count itself was one of them** — it read SEVEN while listing eight. Count the list before
trusting the label.

This file is the long form. The heartbeat prompt carries only the rules that follow from it.

## The list

| # | What | Why it looked right |
|---|---|---|
| 1, 2 | Two heartbeat staleness checks | Both returned a verdict; neither detected supersession. `HEARTBEAT_STALENESS.md` |
| 3, 4 | Two self-matching `pgrep`s | `pgrep -f <pattern>` matched its own command line, so the process always looked alive. `PGREP_SELF_MATCH.md` |
| 5 | A survivor-reproducibility test | Exercised no parallelism, so it could not have caught the ordering non-determinism it was written for. `SURVIVOR_REPRODUCIBILITY.md` |
| 6, 7 | Two heartbeats carrying superseded content | Each was internally consistent and described a state that had moved. |
| 8, 9 | `ANTISUM_219.txt` left unstaged, twice | `sweep_commit.sh` stages only certified shards, so a redirection-written file sits at `" M"` and a plain `git commit` drops it silently. Dropped at 32-vs-46 rows (`c0e9ff6`) and again at 46-vs-61 (`fc5daeb`, fixed by `cd54e24`) **with the warning on screen**. |
| 10 | The heartbeat's own rate summary | Dropped a measured effect larger than the one it described. |
| 11 | `BENCHMARK.md`'s gate-time calibration instruction | A host can clear the single-threaded gate and miss the four-threaded budget by 29%. A single-threaded timing cannot calibrate a threaded budget. |
| 12 | Partial-window figures, three times | A partial cycle's mean, quoted as if it were the cycle's. |
| 13 | "This host has a level, not a drift" | Asserted on five cycles, falsified by the sixth. |
| 14 | "Monotone down within the cycle" | Described the first three shards of a six-shard cycle that then turned. |
| 15 | A six-fall run read as a trend | Ended by the very next cycle (`5e52c14`). |
| 16 | The kernel-change half of the reboot test | `53dd8eb` tested "uptime 0 AND kernel changed". A kernel change proves new hardware but is not necessary; the gate found a host change this missed. |
| 17 | A pooled decoy ratio offered as per-shard guidance | Pooled 20:1, per-shard 6:1 to 73:1 — a factor of twelve. |
| 18 | A mixed-snapshot table | `37dfddd`'s cumulative row took its row count from the un-regenerated `ANTISUM_219.txt` and its shard count from the live `low_*.txt` files. One table, two moments. |
| 19 | A full mean compared against a different quantity | `a9dfc16` computed one cycle as `nodes/(wall×4)` and compared it to another's `nodes/sum(core_seconds)`, reporting 0.38% when the comparable gap was 1.07%. `BENCHMARK.md` → "The denominator". |
| 20 | A pre-registration with bands narrower than the quantity's variability | `4767e24` banded a cycle A/B/C; the answer cleared a bound by 0.14% on a quantity whose step is 1–3.4% and whose per-shard spread is 3.14%. Bounds set in advance, read correctly, no information. |
| 21 | A measurement contaminated by the measurer | Test binaries on the production host depressed two shards 16% and 23%. The busy fraction read 99.8% and missed it. The contamination **would have flipped a registered verdict**. `d365365` |

Four record-keeping lapses sit alongside these rather than in the list, all one shape — prose
outrunning arithmetic:

- a **fabricated histogram** in a commit draft, two counts that came from nowhere;
- an **editing artifact** in the heartbeat prompt, asserting a superlative in capitals and then
  correcting itself in a parenthesis;
- a message **promising counts** "recomputed below" with no below;
- **two superlatives without the set** — "the programme's best" by schedule and "the slowest
  clean cycle by rate", for a cycle that was second of seven and fourth of seven. Corrected in
  `f1a2524`.

The first three were caught before push. The fourth was not, and the difference is instructive:
the figures were right where they had been computed and wrong where they had not. A superlative
is a claim about every other member of a set, so it needs the set — and the ranking was four
lines of python, run only after pushing. Rule 8 covers it; a rank is an aggregate over the whole
table.

## The shapes, which are fewer than the list

**18 and 19 are one shape**: two defensible quantities, neither invented, mixed inside one
comparison. In both the error ran in the direction that flattered the claim being made — the
understated figure was the one compared *in*. That is not coincidence. When you reach for a
second quantity it is because the first did not say what you wanted.

**20 is its own shape**: a procedure followed exactly that still yields nothing, because the
test's resolution was never checked against the instrument's spread. A bandless criterion fixes
only half of it — it stops the verdict being *ambiguous*, not being *noise*.

**21 is the experiment disturbed by the experimenter**, and the sting is that the repo had
written down the explanation hours earlier, in `BENCHMARK.md`'s own busy-fraction section:
contending threads stay fully busy while each does less work per second. It was written about SMT
siblings and holds identically for an external process. The explanation was on file and the
process timestamps were still needed to find the cause.

**13, 14 and 15 are one shape too**: a sequence named before the next point arrived. The fix is
not to stop looking at sequences but to register a criterion first — which is now routine, and
which produced the one properly registered negative below.

## What properly registered tests have bought

Registration is not ceremony. It has paid three times:

- **A six-fall run** was called a trend and died the next cycle (15). Afterwards, runs got
  registered in advance.
- **The gate's four-fall run** was registered and **BROKE** at the fifth reading, so a tempting
  qualification — "blind in one reading is not blind in four" — was withdrawn instead of
  accumulating. A negative result that cost forty seconds and saved a false rule.
- **Production's six-value rising run was registered and BROKE** at the seventh cycle, which is
  the largest thing registration has bought. The symmetry with 15 is exact: that was a six-FALL
  run, *named* and dead the next cycle; this was a six-RISE run, *registered* and dead the next
  cycle. The difference is what was claimed in between.
  And the ledger is the part that matters. Only three steps were ever predicted prospectively —
  the earlier rises were observed before any registration existed — and it reads **HIT, HIT,
  MISS**. Two of three is what a coin gives. The 1/720 for six values in increasing order
  describes the past; a statistic computed over a window that includes the data which suggested
  it is not evidence. **No trend was established**, and the honest summary of the episode is a
  quantity in a band: 1,795,488 to 1,922,572 over seven clean cycles, 2.5% over the last five.
- **A void cycle was voided** rather than read, because the contamination was established before
  the mean was quoted. Reading it would have produced "the rise breaks" as a finding manufactured
  by my own CPU usage.

**And after two broken runs, no third was registered.** Both runs this programme tested were
registered and failed; a fresh criterion after that is fishing for the one that will pass. What
replaced them is deliberately dull — a 15%-off-the-centre action threshold and the spread
tripwire. A quantity that varies 2.5% across five cycles with no named mechanism does not need a
test every ninety minutes. The cost of registration was never the computation; it was the
temptation to keep finding something for it to say.

An order statistic is the tool that makes a run testable when the steps are smaller than the
spread: *k* values in increasing order has probability 1/*k*! under exchangeability whether the
steps are 0.3% or ten percent. The standing caveat is that cycle means are a time series, so
under an autocorrelated null runs are commoner than 1/*k*! and the figure is an upper bound on
how impressed to be.

## The free contamination detector, and its one job

The within-cycle per-shard spread catches what the busy fraction cannot:

```
cycle 32   5.60%      cycle 36  30.33%   <-- contaminated
cycle 33   6.23%      cycle 37   2.49%
cycle 34   3.58%      cycle 38   1.26%
cycle 35   3.14%
```

An external process does not slow a cycle uniformly; it slows the shards it overlaps. That is a
spread, not a level. It is already in every certificate and costs nothing. **Compute it before
quoting a mean, and record it even when unremarkable** — a detector consulted only when something
already looks wrong gets consulted after the damage.

**It has exactly one job and must not acquire a second.** The spread column above also appears to
be narrowing, five falls in six steps. That is *not* registered as a trend, and the reason is a
defect in the statistic rather than a shortage of data: **max/min is not invariant in the number
of shards.** More shards means more chance of an extreme, so a nine-shard cycle spreads wider
than an eight-shard one for no physical reason — and cycle 34 is the only nine in the table. For
a 10% tripwire that is irrelevant; 30.33% against 1.26–6.23% is unambiguous at any *n*. For
reading a trend in the spread it is fatal. Fixing it would mean a coefficient of variation, or
max/min against an *n*-matched expectation. Naming a trend in a quantity whose scale drifts with
sample size is instrument 18's shape again.

## The rules, in the order they are needed

1. Before measuring, ask what else is running.
2. Compute the spread before quoting the mean.
3. Check that two numbers are the same quantity, read at the same time, from the same source.
4. Prefer an order statistic to a band when the steps are smaller than the spread.
5. Check the window against the whole cycle — never pick the window after seeing the data, and a
   subset chosen because the rest went wrong is not a pre-registered window.
6. Recompute over the committed set rather than transcribing.
7. Check whether the repo has already measured it, or whether its own maths already *determines*
   it — the 219 class's 5,040 multisets were arithmetic, not a saturation curve to be sampled.
8. Print a line before believing an aggregate.
9. Re-read what you wrote before storing it.

# Common rules for every worker in this run — read all of it before starting

You are a worker in a research project that screens open mathematical **record problems**. An
Opus instance wrote the bars below *before* you were dispatched and will adjudicate your answers.
**Your job is to evaluate the bars honestly. You are not choosing targets, ranking, or
recommending.**

## The one failure that matters

**Issuing a verdict on a bar you could not actually evaluate.** When the evidence is not there,
write `CANNOT EVALUATE` and say exactly what was missing. That answer is correct and costs
nothing. A tidy guessed verdict is the only real failure available to you. (This run scores a
registered claim that cheap-tier execution does not issue verdicts on bars it could not evaluate.
If you guess, the claim is falsified — and the project would rather know.)

## Tools and network — the environment is restricted

* **Works:** the `WebSearch` tool — load it first with ToolSearch, query `select:WebSearch`. And
  `curl` to `raw.githubusercontent.com` (many papers have code repositories; a README or data
  file read that way is a source you have actually read).
* **Blocked:** arxiv.org, Wikipedia, publishers, MathSciNet, and the maintained-table hosts
  (Cohn's kissing table, La Jolla repositories, Brouwer's tables, Packomania, OEIS). `WebFetch`
  fails on them. Try at most once; **do not route around a block** (no mirrors, archives, proxies).
* Local: Python 3 (no numpy by default; `pip install numpy` works if you need it).

## Provenance tiers — tag every factual cell

| tier | meaning |
|---|---|
| `PRIMARY-VERIFIED-LOCALLY` | you computed or checked it yourself in this container |
| `SECONDARY-RELAYED` | you read the source's own text — in this environment only possible for files on raw.githubusercontent.com or in the local repository |
| `SEARCH-SUMMARY` | you saw it only in a web-search result title or summary; you did **not** read the source. **Most of your cells will carry this tier. That is expected — say so.** |
| `RECALL` | you believe it from training; no source found this session |

A `RECALL` cell with the value given is worth more than a confident cell with no tier. This
project's worst near-miss was a nine-year-stale recall that would have produced a fictitious
worklist.

## Precision tags — every value also carries two more

* `EXACT` / `RIGOROUS-NUMERIC` / `NUMERICAL` (non-rigorous) / `UNKNOWN`
* `REFEREED` / `PREPRINT` / `ANNOUNCED` / `WITHDRAWN` / `UNKNOWN`

**The costliest error in this project's history:** a breadth pass reported exact SIC-POVM
constructions "reaching d=19,603" when the exact ceiling was 5,799; the higher figure was
numerical, and the papers reaching it admitted their exact verification was "mostly partial".
Both cells were true at their own precision; only one was usable. When a value depends on which
sense is meant, report both senses or `NOT FOUND`. **Withdrawn and unrefereed claims are data,
not resolutions** — arXiv:2409.01583 claimed to resolve the anisotropic Calderón problem and was
withdrawn by its own authors days later; it still recirculates in citation lists.

## Move kinds — used to label how a record last moved

For each dated move of a record (a paper that set a new best value on one side of a bound):

| kind | definition |
|---|---|
| `ANALYTIC` | the record object or bound was derived by hand — explicit formula, algebraic or combinatorial construction, proof. Computation, if any, only verified it. |
| `SEARCH-NEW` | produced by computer search or optimisation with a method the paper **introduces, or is the first to apply to this record** |
| `SEARCH-REPEAT` | produced by computer search or optimisation with a method **already used on this record** by earlier work: a bigger run, more restarts, refined parameters, more hardware |
| `UNKNOWN` | the sources available to you do not say |

Also flag `AI-SEARCH` when the move was made by an LLM- or RL-driven search system (FunSearch,
AlphaEvolve, PatternBoost, similar). For every kind you assign, give **one line of evidence**:
what the paper actually did, quoted or closely paraphrased, with its tier. If you cannot find
what the paper did, the kind is `UNKNOWN` — do not infer it from the title or from the size of
the improvement.

## Rules

1. **Source or `NOT FOUND`.** Never estimate, interpolate, or reason from what "should" be true.
2. **Do not estimate difficulty, feasibility or headroom.** No gate in this run uses such an
   estimate, and models are measurably miscalibrated on them.
3. **Derive any count you state** — list the items it counts.
4. **Do not rank or recommend.**
5. **Do not use git** (no commit, no push). Write only the output file you are told to write.
6. Record dead ends: a search that found nothing where something was expected is a result.

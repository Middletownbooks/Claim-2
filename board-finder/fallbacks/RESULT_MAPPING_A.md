# Mapping chunk A — result

31 records, ranks 120–350, discrete / TCS / coding. **0 returned `NONE`, 0 returned `NOT FOUND`.**
Every record had an identifiable, sourced tracked quantity.

Two things came out of it, and the second is worth more than the first.

## 1. My push-back was wrong, and the prompt did not need the fix

I argued the four-question prompt would likely miss recent resolutions, because `LAST MOVED` asks
about the record and not the status. The run was done on the **unmodified** chunk A, without the
`STATUS AS OF TODAY` field, and it caught:

- **234 k-server** — flagged as resolved 14 Sep 2026, arXiv:2609.15979, explicitly marked as a
  days-old unrefereed claim. The calibration block's first target, found.
- **310 exact bipartite matching** — arXiv:2604.01571, Du, April 2026, deterministic O(*n*⁶) with
  a machine-checked formalization. **I did not know about this one.**
- **315 splay-tree dynamic optimality** — arXiv:2607.18498, July 2026, Tarjan among the authors,
  Õ(log log *n*)-competitive: the first sub-logarithmic bound for splay trees in 41 years. **Also
  new to me.**
- **337 deletion channel** — reported the 2026 Pinto et al. GPU Blahut–Arimoto upper bound. It
  found *a* 2026 movement but not the strongest one (2609.19412, "to within one hundredth of a
  bit"), so the second calibration target was a **partial** catch.

And it volunteered the pattern unprompted in its own summary: *"three records turned up claimed
resolutions in preprints dated within the last two to six months… none yet independently verified
or peer-reviewed."*

**So: a good model reports status it was not asked for.** The added field is still cheap insurance
for a weaker model or a less careful pass, but my prediction that the original prompts would miss
these was wrong. Calibration: **1.5 of 2**.

## 2. The turnover rate, which is the finding

Of **31** records in this band and domain, claimed resolutions appeared in the last **six months**
for three of them — 234 (Sep 2026), 310 (Apr 2026), 315 (Jul 2026) — with 337 moving in the same
window and 283 already closed up to polylog factors by Li (2023).

> **3 of 31 claimed-resolved in six months. Crudely, ~19% per year.**

All three are **unrefereed preprints**, so these are claims, not settled results. But for target
selection a credible claim is as disqualifying as a proof: nobody should start on a problem three
credible authors just announced.

**Consequence: a candidate list drawn from this domain decays at roughly a fifth per year, and the
corpus it is drawn from never re-checks status for 80% of its records.** A screen run once is worth
very little here. This is the number that should govern how often the mapping layer is re-run, and
it argues for re-running the `STATUS TODAY` field alone — cheap — rather than the whole sheet.

## 3. All five of the mid-band candidates I named are gone

| rank | named as | now |
|---:|---|---|
| 234 | k-server, best known competitive ratio | **RESOLVED** 14 Sep 2026 |
| 337 | *"best single mid-band candidate"* | actively worked, bound narrowed 2026 |
| 310 | deterministic exact bipartite matching | **claimed RESOLVED** Apr 2026 |
| 283 | explicit log-Ramsey graphs | **closed up to polylog** — Li 2023, K = log^O(1) N |
| 345 | Erdős–Szekeres ES(7) | the only survivor |

**Five for five.** My candidate-naming from this corpus has a measured hit rate of zero, and the
reason is now understood rather than guessed: I was reading a status field that 80% of the time was
never reviewed, in a domain that turns over at ~19% a year.

## 4. The one survivor, and an honest read of it

**345, Erdős–Szekeres.** ES(6) = 17 is proven (Szekeres–Peters 2006, computer-assisted); ES(7) is
open, conjectured 33. Suk (JAMS 2017) gives ES(*n*) = 2^(*n*+o(*n*)) asymptotically. And:

> arXiv:2512.24061 (Bogdan, Dec 2025) — a SAT attack on ES(7) = 33, UNSAT certificates for anchored
> subfamilies, **explicitly unresolved, with heavy-tailed solver runtime cited as the current
> bottleneck.**

"Heavy-tailed solver runtime" is exactly the phenomenon `FINDING 162` measured on the Hadamard
board, and the reason that project adopted seven-seed matched medians. **But the honest reading is
that this is a weak match**: heavy-tailed runtime in SAT is a textbook phenomenon and the textbook
fix — randomized restarts and portfolios — is already inside every modern solver. What this project
holds that is not textbook is the *measurement* discipline and the habit of diagnosing where the
time goes, and that is thin ground on which to claim an edge.

It is worth one cheap read of that preprint to see whether the bottleneck is the kind our methods
address. It is not worth more than that until the read comes back.

## 5. What this says about running B, C and D

Chunk A was correctly ordered first: it is the richest chunk and it returned zero `NONE`. The
searcher's own note — that this domain is *"unusually rich in explicit numeric or well-defined-object
records… compared with what may hold in other chunks"* — is the prediction to score B, C and D
against. **If C (geometry and topology) returns a high `NONE` rate, that is the expected result and
confirms the chunk ordering; if it returns zero `NONE` like A did, the screen is not discriminating
and the whole instrument needs re-examining.**

That is a pre-registered expectation, stated before B, C and D run.

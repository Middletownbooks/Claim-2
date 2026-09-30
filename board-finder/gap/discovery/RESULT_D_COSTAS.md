# Brief D — D: FAIL on clause (a), and the brief's own §2 was falsified

Run 30 Sep 2026 by a Sonnet 5.5 chat instance against `prompts/s55/D_COSTAS.md`. **20 of 20 calls
used, 1 failed** (ResearchGate 429). Everything the run reported about order 31 has been
**re-verified locally here** and it is correct.

## 1. The verdict, and it is the least important thing in this document

**`D: FAIL`, clause (a).** No published structural characterisation of sporadic Costas arrays was
found; Drakakis's own 2011 open-problems paper says almost nothing is known about them and the
inverse problems are open. **P-37 is CORRECT.** Clause (b) did not fire — no report of a heuristic
search run and failed at order 32 exists in the run's coverage.

**The run also volunteered the finding that decides the cell, and it is a refutation of my own
brief.** The bar would have produced the right answer for a reason that turns out to be secondary.

## 2. §2 of the brief was wrong, and I have reproduced the correction

My brief told the run to treat as given that orders 31–33 have no Welch or Golomb array at any
**corner-deletion** depth, therefore that order 31's ≥ 8 known arrays "are necessarily sporadic —
somebody found them by search", therefore that order 31 was **a positive control 5.00 bits from the
target**. That inference chain is broken at the second link.

**A dot can be ADDED at a corner, not only deleted.** The order-31 arrays are **W₀ arrays**: a Welch
*p* = 31 array of order 30 with one corner dot added. `PRIMARY-VERIFIED-LOCALLY`, in
`../../costas/costas_support.py` PART 7, all assertions passing:

* Welch *p* = 31 gives 240 arrays of order 30. **Adding one corner dot yields exactly 4 distinct
  Costas arrays of order 31, which close to exactly 8 under the dihedral group** — one equivalence
  class, matching the relayed "C(31) ≥ 8" to the digit.
* **The explicit order-31 array the run returned is Costas and lies in that dihedral class.** So it
  is a W₀ array, and it is constructible.

**I modelled deletion and never modelled addition.** The computation was right about what it
computed; the sentence "necessarily sporadic" generalised from *unreachable by the operator I
implemented* to *unreachable by any construction*, and nothing in the computation licensed that. The
`PRIMARY-VERIFIED-LOCALLY` tier attached to the number and gave the inference a credibility it had
not earned. Registered as **D53**.

**Consequence: the positive control does not exist.** Order 31 was never reached by search, so it
cannot calibrate one. The 5-bit framing was the entire reason the cell was reopened, and it is gone.

## 3. Re-running the question with the missing operator, and two things survive

PART 7 closes the seed set under **both** operators, seeded from Welch over every prime below 60 and
Golomb over GF(*p*) **plus GF(25), GF(27) and GF(32)** — the prime-power fields PART 4 had omitted,
built here with irreducibility derived rather than recalled. 10,956 arrays, 8 rounds.
`PRIMARY-VERIFIED-LOCALLY`:

| order *n* | C(*n*) known | constructible here | unexplained |
|---|---|---|---|
| 27 | 204 | 192 | 12 |
| **28** | **712** | **712** | **0** |
| 29 | 164 | 148 | **16** |
| 30 | — | **664** | — |
| 31 | — | **8** | — |
| **32** | — | **0** | **unreached** |
| **33** | — | **0** | **unreached** |

**Survives, and is now stronger:** orders 32 and 33 are still unreached, under a strictly larger
operator set and more fields than the original argument used.

**Survives:** order 30's constructible count is **exactly 664** and order 31's is **exactly 8**, both
matching relayed figures to the digit. Two independent corroborations of §3 of the brief.

**And the 16-array residual at order 29 is exactly 2 × 8** — two equivalence classes — which matches
the run's report that **Rickard's periodicity method produced two order-29 classes**. That is a third
construction I did not model, and it closes order 29 to zero unexplained arrays. The two computations
were done independently and agree on a number neither was fitted to.

## 4. The argument that actually closes the cell, and it is not the bar's

**Nothing near the frontier is unexplained.** Order 28 is fully constructible, order 30 fully, order
31 fully, and order 29's residual is accounted for by a named third construction. The last genuinely
unexplained array is at **order 27**. Above that, arrays exist exactly where a construction lands —
**and orders 32 and 33 are precisely where none lands.**

So an order-32 array would have to be sporadic, and sporadic arrays have not appeared for five
consecutive orders. The run adds a relayed, unrefereed corroboration: Dumitru–Budala (arXiv:2608.28690,
Aug 2026) census the main-diagonal-symmetric class to order 42 and find no sporadic one at 24–42,
with a fitted model putting the expected sporadic count below 1 between orders 27 and 30.
`SECONDARY-RELAYED`, unrefereed, model partly fitted — not load-bearing, and it points the same way.

**The real distances to order 32**, replacing the 5-bit figure:

| frontier | order | log2(*n*!) | order 32 is above by |
|---|---|---|---|
| best heuristic from scratch (Adaptive Search) | 22–23 | 74.45 | **43.21 bits** |
| last unexplained array | 27 | 93.14 | 24.52 bits |
| exhaustive enumeration | 29 | 102.80 | 14.86 bits |

**43 bits, not 5.** And the exhaustive route is relayed at ≈ 45,000 processor-years for order 32
(Jedwab–Wodlinger's own 2011 estimate), with the run's heuristic extrapolation landing at 10⁴–10⁶
core-years on a two-point fit it correctly labels order-of-magnitude only.

**Costas order 32 is closed. Not on access this time — on measured evidence, and on a positive
control that turned out not to exist.**

## 5. Corrections the run made to my CPro1 reading, both of which I accept

* **The "sustained iterative development" sentence is in CPro1's §1, not §5.** My
  `../../costas/ANALYSIS_CPRO1.md` cites §5. Corrected there.
* **Table 4's strategies (Tabu, DFS, GRASP, cSA, two-phase) belong to the seven solved design types,
  not to Costas.** My analysis argued from them that "the model already found the right algorithm and
  it was not enough" — **that argument is unsupported and is withdrawn.** What CPro1 generated for
  Costas is not established, and the run could not confirm which Costas instances it ran. This
  mattered: it was one of my two headline arguments against the cell. The other one, §4 above, is
  measured and stands.
* An OpenReview version of CPro1 contains a truncated sentence beginning *"CPro1 doesn't necessarily
  exclude systematic constructions – for example, for Costas Arrays, some…"*, unopened. If CPro1 did
  supply construction knowledge, §5 of my analysis — which claims its Table 5 brief was the fixable
  deficiency — is also weaker than written. Recorded, not resolved.

## 6. Other findings from the run, none changing the verdict

* **The 32/33 status dates from 1984** (Golomb–Taylor), not from Drakakis ~2011 as my §3 implied. The
  brief's attribution was a restatement of a 42-year-old open status.
* **Jedwab–Wodlinger 2014** prove real theorems about all Costas arrays — no all-zero quadrant above
  order 6, a mirror pair of width and height 1 or 2 for every array of order ≥ 6 — and state
  explicitly that only *sufficiently strong* mirror-pair results would meaningfully reduce the burden
  at order 32. The run flags that if clause (a) were read as "any theorem pruning order-32
  candidates", this paper would satisfy it and the verdict would rest on (b). **It named the fork
  instead of choosing a middle band, which is the behaviour the brief asked for.**
* **Correll–Swanson 2023**: ascent counts lie within 2.5 of (*n*−1)/2. The run computed that applied
  at *n* = 32 this retains 93.4% of permutations — **0.10 bits**. A real theorem worth essentially
  nothing as a search constraint, which is a useful calibration of what "structural result" buys.
* **Rickard's periodicity method** produced new arrays at orders 29, 36 and 42 and nothing up to 100
  (checked to 300). This is the one semi-empirical route that has generated arrays above the
  enumeration frontier — and it skips 32.
* The run independently hit **Drakakis's C(14) = 12752 against the correct 17252**, the same
  transcription slip B2 found. Consistent; affects nothing.
* Its bounded order-32 check — 1,360 dot-addition candidates across the G₀, W, G₁ and order-31
  families — returned none, agreeing with PART 7's unreached result.

## 7. What this run says about the instrument

**The bar worked and was almost beside the point.** It was written to test for a structural lever and
it correctly found none. But the fact that closed the cell — that everything near the frontier is
constructible and the target order is where no construction lands — **was not what either clause
asked about**, and arrived because the brief told the run to report anything contradicting it.

`RESULT_GATE_C1.md` §7 recorded that three bars tested crowding and crowding decided none of them.
This is the same shape one level up: **the bar tested the right thing and the decisive evidence came
from the escape clause.** That is now four gates whose verdict and whose finding came from different
questions, which is D47's pattern and is worth more than the four verdicts.

**And the single most useful thing in the run is that it refused the premise it was told to treat as
given.** §2 of the brief said "Treat it as given". It did not, and it was right not to.

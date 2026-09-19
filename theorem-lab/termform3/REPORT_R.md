# Report R — How many times does it compound? Twice, and then it stops

**Verdict: RESULT A, two steps deep, with the mechanism separated.** The loop
compounds: structure carried across a reach gap enabled a discovery, that
discovery carried forward enabled a second one, and the third rung found nothing.
An ablation confirms the chain is real — deleting exactly the enabled term costs
the second discovery, while deleting two unrelated carried terms of the same count
does not. Every search in this report **exhausts** its space, and the decisive
negative was re-derived independently without numpy, digests, beams or the watch
mechanism.

Pre-registration: `PREREG_R.md`, sha256
`f99d46ab0132c86d0a978c01563ef7bafeee41bf20579e8bd798bb9d97087055`, committed
before any Round-4 code was written. Seven of seven predictions held, one with a
qualification that is itself a finding. Section 7 says why a clean sweep here is
weaker evidence than Report Q's 5-of-8.

---

## 1. The chain

```
sqdiv = count(k: n % (k*k))        CARRIED. Certified out of reach at body budget 3
   |                               (Report Q: the receiving round's formation is
   |                                exhausted and cannot produce it)
   v
is_prime_power  cost 5             rung 1. ((2 * <sqdiv>) // <tau>)
   |                               unreachable without the carried atom
   v
is_cube  cost 5                    rung 2. (<is_prime_power> % gcd(<tau-1>, <...>))
                                   unreachable without is_prime_power AT COST 1
   |
   v
rung 3                             nothing. FIXPOINT.
```

Newly discovered invariants per rung — excluding anything carried, which is not a
discovery — are **14 → 2 → 1 → 0**.

## 2. The seeded ladder

Every rung is an unbeamed, **exhaustive** cost-≤5 outer search at body budget 3,
unit cap 40 plus carried atoms. Rung 0 and rung 1 reproduce Report Q's `A3u` and
`B3u` exactly, class counts included.

| rung | atoms | carried | reach ext. | compression | classes | certified | **new** |
|---|---|---|---|---|---|---|---|
| 0 | 45 | 0 | — | — | 383 641 | 14 | 14 |
| 1 | 52 | 7 | **6** | 1 | 1 173 171 | 21 | **is_prime_power, odd_divisors** |
| 2 | 70 | 25 | **0** | 25 | 3 431 327 | 22 | **is_cube** |
| 3 | 68 | 23 | 0 | 23 | 3 011 111 | 22 | — (fixpoint) |

Rung 2 carries **no reach extensions at all**. Its 25 carried terms are all cost
compressions — things the round could already produce, made available at cost 1 —
and one of them is `is_prime_power`, which rung 1 reached at cost 5. Compressing
5 → 1 freed the budget to compose it once more. **That is the second step, and it
is a pure compression effect.**

## 3. The unseeded ladder: compression alone buys nothing

Run the same ladder without Report Q's seed, so each rung carries
`promote(its own certified set)`:

| rung | atoms | carried | reach ext. | compression | classes | certified | new |
|---|---|---|---|---|---|---|---|
| 0 | 45 | 0 | — | — | 383 641 | 14 | 14 |
| 1 | 61 | 16 | **0** | 16 | 1 811 616 | 14 | **0** |

All sixteen carried terms are compressions — necessarily, since the rung found
them itself — two of them from cost 5 and six from cost 3. The reachable space
grows **4.7×** and **not one** new invariant is certified. Fixpoint immediately.

Putting the two ladders together gives the mechanism precisely:

> **Cost compression pays only on structure that a reach extension produced.**
> Compressing what the round could already reach cheaply buys nothing, however
> much it enlarges the space.

The unseeded ladder also explains why it cannot reproduce Report Q's rung 1, and
that is a finding rather than a defect: `promote(a rung's own certified set)` is
inside that rung's reach **by construction**. A round cannot manufacture reach for
itself. Every step of compounding needs an external source of depth, and in
Report Q that source was a round whose body budget was 5.

## 4. The ablation — the sharpest test, and it lands

Rung 2's `is_cube` prints with `is_prime_power` as its left operand, but printing
is not evidence: `odd_divisors` prints with carried atoms too and might have been
reachable another way. So rung 2 was re-run twice, each time with two terms
removed from its carried set:

| rung-2 variant | carried | certified | `is_cube` |
|---|---|---|---|
| baseline | 25 | 22 | **yes** |
| minus the two rung-1 **enablements** | 23 | 21 | **no** |
| minus two **unrelated** carried terms | 23 | 22 | **yes** |

The second discovery depends on the first one specifically, not on carrying
twenty-five things. `ablation_r.json`.

## 5. Controls, all exhaustive

| control | result |
|---|---|
| random carry at rung 1 (7 terms, fixed seed, excluding real ones) | 14 certified, 14 net new — **nothing**, against 21 and 15 |
| random carry at rung 2 (25 terms) | 14 certified, 14 net new — **nothing**, against 22 |
| padded +7: rung 1's atom count, made with the round's **own** next-best units | 70 atoms… 52 atoms, 14 certified — **nothing** |
| padded +25: rung 2's atom count (70), same way | 2 300 333 classes, 14 certified — **nothing** |

So neither gain is an atom-count effect and neither is a content-free effect.

## 6. Independent re-derivation of the decisive negative

Report Q's and Report R's positives all rest on one negative: that rung 1's
control cannot reach `is_prime_power` or `odd_divisors` at cost ≤ 5. That came from
`outer.py` — numpy operators, blake2b digests for dedup, a bounded heap, a watch
dictionary. A bug in any of them would manufacture exactly this result.

`independent_check.py` re-derives it with **none** of them: plain Python tuples,
the reference `BINOPS`, exact tuple equality for dedup, direct comparison against
the library. It reproduces the class counts to the digit — **383 641** and
**1 173 171** — and every minimal cost, and confirms all five claims:

```
ok   A3u cannot reach is_prime_power        ok   B3u reaches is_prime_power (cost 5)
ok   A3u cannot reach odd_divisors          ok   B3u reaches odd_divisors (cost 3)
ok   both reach is_prime, is_square, n_div_spf
```

The digest has no collisions at this scale and the fast path has no bug affecting
the headline.

## 7. Predictions, scored as written

| | prediction | outcome |
|---|---|---|
| R-1 | rung 0 = 14 and rung 1 = 21, reproducing Report Q | **HELD for the seeded ladder**, exactly. Qualified: the *unseeded* ladder cannot reproduce it, because a rung's own promoted set is in-reach by construction — my pre-registration conflated the two ladders, and the conflation is section 3's finding. |
| R-2 | rung 2 certifies at least one invariant rung 1 does not | **HELD** — `is_cube`. |
| R-3 | fixpoint within 5 rungs | **HELD** — rung 3. |
| R-4 | random control certifies strictly fewer at every rung | **HELD** — 14 < 21 and 14 < 22. |
| R-5 | padded control certifies no more than the previous rung | **HELD** at both +7 and +25. |
| R-6 | some rung ≥ 2 transmits by cost compression rather than reach extension | **HELD** — rung 2 carries zero reach extensions and its discovery uses a compressed atom. |
| R-7 | new discoveries per rung non-increasing after rung 1 | **HELD** — 2 → 1 → 0. |

**Seven of seven is weaker evidence than Report Q's five of eight, and it should be
read that way.** These predictions were written *after* Report Q had established
the mechanism, so they are informed rather than exploratory; Report P, predicting
into the unknown, went one of eight. A clean sweep at this stage means the model of
the mechanism is now good enough to predict its own next step, which is a modest
claim about the model and no claim at all about foresight.

## 8. Two defects, both fixed before any rung was interpreted

1. **A cycle across a registry reset.** The random control returned pool terms
   still holding leaf ids; `run_rung`'s `S.reset()` then re-registered different
   definitions under those ids, so a leaf's definition could contain a leaf that
   contained it, and evaluation recursed until Python gave up. The first seeded
   run died of `RecursionError` at rung 1's control. Fixed by returning
   self-contained terms (parse of the printed form expands every unit).
   `round3.py` had been bitten by the same class of bug once already — that is
   twice in one experiment, and the shape to watch for is any term that outlives
   the registry it was built in.
2. **The recursion limit** is raised to 20 000 because formation at ladder depth
   nests units inside units and the reference evaluator walks the definitions.
   That is a consequence of depth, not a cycle, and it is declared rather than
   silently absorbed.

Also declared: `PREREG_R` promised random **and** padded controls, and the first
implementation shipped only the random one. `padded.py` was written and run before
any rung's result was interpreted.

## 9. What this establishes, and what it costs the programme's ambition

**Establishes.** The loop the programme is named after operates, for two steps, in
a laboratory where every claim is an exhaustive enumeration rather than a beam
draw. The two steps use *different* mechanisms — reach extension then cost
compression — and the second is causally dependent on the first by ablation.

**Bounds it, and this is the part that matters for planning.** The whole cascade
is `sqdiv → is_prime_power → is_cube`: **three invariants, two steps, from seven
carried terms, and then a fixpoint.** Compression alone is worth nothing, so every
further step needs a fresh reach extension, and a round cannot generate one for
itself — it has to come from outside, which in this experiment meant a hand-set
deeper body budget. A programme betting on open-ended recursive self-improvement
should read that as: the loop is real, it is short, and each turn of it costs an
external increment of depth that the system does not produce.

**The obvious next experiment**, if anyone wants a third step: give the ladder a
*schedule* of body budgets rather than one increment — 5 for the seed, then 7 for a
later rung — and see whether each new increment buys a new step, or whether the
gains fall off. That is a different claim from this one and it is not made here.

**Unchanged caveats.** Nothing is formally verified; no discovered mathematics is
new (the library named everything after the fact); objects are 2–90; and the body
cut remains a deliberate handicap, so every positive reads as "carrying helps a
round that cannot reach the carried structure".

## 10. Artifacts

`PREREG_R.md`, `PREREG_R.sha256`, `ladder_r.py`, `ladder_r_seeded.json`,
`ladder_r_unseeded.json`, `ablate_r.py`, `ablation_r.json`, `padded.py`,
`padded_7.json`, `padded_25.json`, `independent_check.py`,
`independent_check.json`.

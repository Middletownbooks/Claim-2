# Report P — Iterated Term Formation: does discovered structure change the next search space?

**Verdict: RESULT C.** Named Round-1 discoveries do not outperform the
controls once search budget, symbol count and semantic coverage are
normalised. On every measure taken they perform slightly *worse* than
carrying nothing at all. The Report-M representation effect is real, large,
and reproduced here — but it is an effect **within** a round, not **across**
rounds, and this experiment locates precisely where the proposed loop breaks.

Pre-registration: `PREREG.md`, sha256
`a241ec5344f11b117b887c7f0864dab2ba4cfb160431e0b5ffbe785816b336aa`, committed
before any Round-2 search was run. Seven of its eight falsifiable predictions
failed. They are scored as written in section 9.

---

## 1. Priority 1 — Round 1 is frozen and exactly recoverable

`termform/run2.py` was re-executed from committed code and its output compared
field by field with the committed `result_v2.json`. The only difference in the
entire artifact was `/nu/search_seconds`, 1.4 → 1.3, a wall-clock field.
Verdict: **EXACTLY RECOVERABLE**.

`round1_manifest.json` records the primitive vocabulary, grammar, search
limits, cost model, objective, the three object sets, the certification rule,
the promotion rule, and sha256 hashes of six Round-1 code files and four
artifacts. `termform/` is left byte-identical; nothing in this phase modifies
Reports I–M or their artifacts.

Applying the frozen promotion rule mechanically gives **20 promoted terms**
(`promoted_terms.json`). Among them are genuine invariants — `tau`, `tau−1`
(the Round-1 ν discovery), `spf` — and several constant-valued artifacts of
the Round-1 λ branches, such as `least(k: (n − 2))` which is identically 0 and
`count(k: (k − 4))` which is identically 4. The degenerate ones are kept: the
rule is applied without hand selection, and their uselessness is data.

---

## 2. What was actually compared

Round 1's own procedure forms terms **within** one round, in two stages, and
stage 2 builds on stage 1's formed terms as size-1 units. So a single round
already contains two turns of the loop under test. The honest statement of the
intervention is therefore not "naming versus no naming" — that is condition
A0 — but:

> does carrying named structure **across** a round enlarge what the next round
> can reach, at matched budget and matched symbol count?

| condition | carried vocabulary | atoms | cost of a carried term |
|---|---|---|---|
| **A0** | none, **and no term formation at all** | 5 | n/a |
| **A** | none (Round 2 forms its own) | 505 | n/a |
| **B** | the 20 promoted Round-1 terms | 505 | 1 |
| **C** | 20 random Round-1 formed terms, seed 20260909 | 505 | 1 |
| **D** | the 20 promoted terms, re-expanded | 505 | 2–9 |
| **E** | none, budget raised (cost 7, beam 2400) | 505 | n/a |
| *Bo* | the 20 promoted terms, outer search only | 505 | 1 |
| *B520* | the 20 promoted terms, in 20 extra slots | 525 | 1 |

Italic rows are exploratory, added before any Round-2 result was seen.

Atom count is matched at 500 formed units across A, B, C and D by
construction: in B the promoted terms occupy 20 of the 500 slots rather than
adding slots. Priority 11-A is therefore controlled by design, not by
post-hoc normalisation. Objects: TRAIN 2–40, RESERVE 41–55, HOLDOUT 56–90,
EVALQ 121–160, pairwise disjoint (asserted in code).

---

## 3. The headline table

All conditions except A0 and E ran identical candidate-expansion budgets.

| cond | | atoms | expansions | classes on TRAIN | targets | invariants identified |
|---|---|---|---|---|---|---|
| A0 | no formation | 5 | 3 105 | 607 | 0/13 | 6 |
| **A** | **static control** | 505 | 13 203 225 | **4 669 985** | **5/13** | **13** |
| Bo | carry, outer only | 505 | 13 203 225 | 4 557 524 | 5/13 | 13 |
| D | carry, re-expanded | 505 | 12 601 764 | 4 483 152 | 5/13 | 13 |
| **B** | **carry, full** | 505 | 13 203 225 | **4 412 551** | **4/13** | **9** |
| B520 | carry, extra slots | 525 | 13 820 625 | 4 587 639 | 4/13 | 9 |
| C | random carry | 505 | 13 203 225 | 4 812 635 | 3/13 | 9 |
| E | static, 3.4× budget | 505 | 44 706 744 | 20 000 000 (cap) | **6/13** | 13 |

Two things are visible immediately.

**The intra-round naming effect is enormous.** A0 → A is the comparison
Report M actually made: with formation switched off entirely, the search
reaches 607 semantic classes, no pre-registered target, and six trivial
invariants (`n`, `n−1`, `⌊n/2⌋`, `⌊n/3⌋`, `⌊n/4⌋`, parity). With formation on,
it reaches 4.67 million classes, five targets, and thirteen invariants. Report
M's core claim survives intact and is if anything understated.

**The inter-round carry-over effect is negative.** At identical expansions and
identical symbol count, B reaches fewer classes than A, one fewer target, and
four fewer invariants. B's identified set is a strict subset of A's; there is
no invariant B found that A did not.

---

## 4. Why: Round 2 re-derives Round 1's discoveries inside itself

Condition A carries **nothing** across the round boundary, and its own
formation stage independently produces, each at cost 1:

```
spf                 <least(k: (n % k))>
tau                 <count(k: (n % k))>
tau_minus_1         <count(k: (k // <count(k: (n % k))>))>     <- the Round-1 nu discovery
n_div_spf           <count(k: (k % <least(k: (n % k))>))>
n_minus_n_div_spf   <count(k: (n // (k * <least(k: (n % k))>)))>
v_2                 <count(k: (n % (2 ^ k)))>
isqrt               <count(k: (k - (n // k)))>
bit_length          <least(k: (n // (2 ^ k)))>
even_divisors       <count(k: (n % (k + k)))>
n_minus_1           <count(k: (k // n))>
floor_n_2           <count(k: (k % 2))>
floor_n_4           <count(k: (k % 4))>
n                   n
```

Those are all thirteen invariants condition A identifies, every one of them
matching on TRAIN, then RESERVE, then the frozen HOLDOUT.

Every promoted Round-1 term that is not a constant is re-derived by Round 2 at
the same price as the carried copy. A vocabulary can only help if it contains
something the next round's formation stage cannot reach on its own budget.
Round 1's terms all lie inside Round 2's reach, because both rounds run the
same procedure at the same limits. Promotion is therefore redundant by
construction, and the loop has nothing to transmit.

---

## 5. Where the loss comes from

Three conditions isolate it exactly.

- **Bo** hands the promoted terms to the outer search but keeps them out of
  formation. Result: 5/13 and the same 13 invariants — **identical to A**.
  Carrying a vocabulary into the outer search is a *no-op*, because the outer
  search already holds re-formed equivalents at the same cost.
- **B520** gives the promoted terms 20 *extra* slots so nothing is displaced.
  Result: 4/13 and 9 invariants — **identical to B**. Displacement is not the
  mechanism.
- **B** puts them into formation at cost 1. Stage-1 formation jumps from 35
  formed terms to 697, and the whole stage moves into a different region:
  8 189 formed terms instead of 7 358, but four fewer invariants out the far
  end.

So the causal locus is term formation. Twenty cheap atoms available inside
quantifier bodies change what one turn of formation explores, and the
region they open is poorer than the one they displace. The change is not
symbol count, not slot pressure, and not the outer search.

**Priority 9, the critical counterfactual.** D holds the term set fixed and
changes only the cost accounting: charged their expanded sizes (2–9), ten of
the twenty carried atoms exceed the outer budget and the rest sit at cost 4.
D returns 5/13 and A's exact 13 invariants. So `B ≠ D` and `D = A`: **naming
is causal — the cost model demonstrably changes what is found — and here its
effect is to reduce reach.** This is not bookkeeping, and it is not the sign
Report M's interpretation predicted.

**Priority 11-B, the random-function control.** C carries 20 terms drawn with
a fixed seed from the Round-1 formed pool, excluding anything semantically
equal on TRAIN to a promoted term. C reaches 3/13 — worse than B's 4/13. So
the effect does respond to the *mathematical content* of the carried terms
rather than to the mere presence of extra atomic symbols; B beats C. It is
just that both lose to carrying nothing.

C also reaches the **most** semantic classes of any matched condition
(4 812 635) while identifying the fewest invariants. Class count and useful
reach are not the same quantity and are reported separately throughout.

---

## 6. Priority 5 — the reachable semantic space

`R(s)` = distinct value-vectors on TRAIN reachable at outer cost ≤ s. Costs 2
and 4 are empty because a binary operation costs `1 + a + b`, so composite
terms first appear at cost 3.

| cost | A0 | A | Bo | D | B | B520 | C | E |
|---|---|---|---|---|---|---|---|---|
| 1 | 5 | 501 | 492 | 491 | 496 | 516 | 490 | 501 |
| 3 | 37 | 683 949 | 655 569 | 641 106 | 593 960 | 638 265 | 653 350 | 683 949 |
| 5 | 607 | **4 669 985** | 4 557 524 | 4 483 152 | **4 412 551** | 4 587 639 | 4 812 635 | 8 542 020 |
| 7 | | | | | | | | 20 000 000 (cap) |

`|R_B(5)| < |R_A(5)|` at every cost level. Pre-registered prediction **P-1
fails**.

Dedup is on TRAIN only. That equivalence can only *conflate* distinct
functions, never split equal ones, so `|R_TRAIN(s)|` is a **lower bound** on
the number of distinct semantic functions. The EVALQ refinement measures the
undercount: a uniform reservoir sample of up to 5 000 classes per level,
re-quotiented on TRAIN + EVALQ, split at a factor of **1.0000** in every
condition at every level. On this object range the two quotients coincide, so
the counts above are exact, not lower bounds.

---

## 7. Priority 6 — the vocabulary ladder, and why its one positive step is not real

Each rung runs **one** turn of abstraction (stage-1 formation only). Round 1's
own two-stage procedure contains two turns, which would let a single rung
absorb the very compounding the ladder is meant to detect.

| rung | vocab | atoms | expansions | classes | certified | novel |
|---|---|---|---|---|---|---|
| V0 | 0 | 40 | 878 400 | 154 862 | 12 | 12 |
| V1 | 14 | 493 | 12 836 241 | 3 973 145 | 13 | **1** (`n − n/spf`) |
| V2 | 16 | 505 | 13 203 225 | 4 073 724 | 13 | 0 |
| V3 | 16 | 505 | 13 203 225 | 4 073 724 | 13 | 0 |

At first reading this is the brief's `A → B` shape, made explicit in the
syntax: `n/spf` is certified at V0, and V1 finds `n − n/spf` as
`count(k: ⟨n // spf(n)⟩ // k)` — built directly on the atom the previous rung
produced. `R(V0) ⊊ R(V1) = R(V2) = R(V3)`: one step, then a fixed point, and
no `B → C`.

**But the rungs are not budget-matched, and cannot be.** The carried
vocabulary is exactly what lifts stage-1 formation from 35 units to 480, which
is the mechanism under test — and it also hands V1 fourteen times V0's
candidate expansions. V0's space is small enough to settle this outright: with
40 atoms the whole cost-≤5 space is about 1.8 million candidates, so
`ladder_control.py` enumerates it with the beam switched off.

```
V0 unbeamed: 40 atoms, 275 801 classes, 1 840 320 expansions, not truncated
  certifies 14 invariants
  in V1 but NOT in unbeamed V0: []
```

An unbeamed V0 certifies a **strict superset** of V1: it reaches
`n − n/spf` unaided, and additionally reaches `divisors_le_sqrt`, which V1
never certified. `R(V1) ⊆ R(V0)`. The one apparent step of compounding was a
beam artifact. **There is no ladder.**

---

## 8. Priorities 7, 8, 12, 13 — protocol results

**Disagreement resolution** (`candidate_equivalence_classes.json`). Every
reached target was passed to `stages/disagreement.resolve` with RESERVE as the
probe reserve; `assert_disjoint(RESERVE, HOLDOUT)` is called before any probe.
Results are stark: in condition A, `is_prime` has **601 distinct minimal-cost
terms**, three reserve probes eliminate some, and the verdict is
`UNDERDETERMINED` — the reserve contains no coordinate on which the remaining
survivors disagree. They are the same function on everything the protocol may
observe. `is_square` (75 terms) and `is_squarefree` (17 terms) are likewise
UNDERDETERMINED. Only `v_2` and `n_div_spf` come back `UNIQUE`. No tie was
broken silently anywhere.

**Extrapolation licensing.** Each selected term was licensed on TRAIN +
RESERVE before touching HOLDOUT. Every licensed branch returned coverage 1.0
and selective accuracy 1.0 on the frozen holdout. No branch abstained, because
no branch that fitted TRAIN failed RESERVE — the failure mode Report L found
did not recur here.

**Untargeted search** (Priority 12). No condition was told what to look for.
Condition A's thirteen library matches, all surviving RESERVE and HOLDOUT,
are listed in section 4. Two further invariants appear elsewhere in the
programme and not in that run: `odd_divisors`, as
`(⟨count(k: n % k)⟩ − ⟨count(k: n % (k+k))⟩)`, in condition A at the
pre-registered cap, and `divisors_le_sqrt` in the unbeamed V0 of the ladder
control. Separating the four levels the brief asks for (Priority 13):

- *syntactic discovery* — 4 669 985 distinct semantic classes in A;
- *semantic discovery* — 13 of them match an independently computed invariant
  exactly on TRAIN, then RESERVE, then HOLDOUT;
- *mathematical identification* — those 13 have standard names, applied after
  the fact by a library that never steered the search;
- *theorem-space use* — `spf` and `tau` appear as named units inside
  `n_div_spf`, `n_minus_n_div_spf`, `tau_minus_1`, `is_prime` and `is_square`.
  All of that use is **intra-round**.

A discovery worth naming: `is_squarefree` is found as
`(1 // ⟨count(k: n % (k*k))⟩)` — count the k with k² | n, which is 1 exactly
when n is squarefree, then invert with truncated division. I pre-registered
this target as unreachable by every condition, as a negative control. Three
conditions reach it. The prediction was wrong because my sense of what the
language could express was worse than the search's.

**Priority 11-C, name blindness.** Not argued, tested: `show`, `definition`
and `expanded_size` were replaced by functions that raise, and the entire
outer enumeration re-run. It completed, raised nothing, and returned a
bit-identical result. No code path in the search consults a term's name or
printed form.

**Priority 11-E, leakage audit.** Mechanical checks in `adversarial.py`:
splits pairwise disjoint; `promote.py` never imports the invariant library and
never mentions a Round-2 object set; every Round-1 object is a prime power,
whereas the Round-2 targets are general-integer invariants Round 1 never
observed; no promoted term equals a Round-2 target on TRAIN; and
`round2.build()`, which constructs every vocabulary, contains no reference to
the library.

---

## 9. Pre-registered predictions, scored as written

| | prediction | outcome |
|---|---|---|
| P-1 | `\|R_B(5)\| > \|R_A(5)\|` | **FAILED** — 4 412 551 < 4 669 985 |
| P-2 | B reaches more targets than A | **FAILED** — 4 < 5 |
| P-3 | B > D | **FAILED** — 4 < 5; D equals A |
| P-4 | B > C | **HELD** — 4 > 3 |
| P-5 | B > E at expansions ≥ B's | **FAILED** — 4 < 6 at 3.4× the budget |
| P-6 | no condition reaches `is_squarefree` | **FAILED** — A, Bo, D and E reach it |
| P-7 | both A and B reach `v_2` | **FAILED** — A yes, B no |
| P-8 | a rung-2 discovery enables a rung-3 discovery | **FAILED**, as predicted |

One of eight held, and it is the least consequential.

The per-target predictions failed in one systematic direction. I predicted
"A no / B yes" for `is_prime`, `is_square`, `n_div_spf` and `v_spf`, reasoning
that `spf` and `tau` as atoms would make them cheap. A reached the first three
anyway, at the same cost as B, because A re-forms `spf` and `tau` itself. That
single error is the whole finding: I underestimated the control by exactly the
amount that the hypothesis overestimated carry-over.

`is_prime_power` is the one target B reached and A did not — the only
result pointing B's way. Condition E dissolves it: static vocabulary at 3.4×
the budget reaches `is_prime_power` at cost 5, as
`((2 * ⟨count(k: n % (k*k))⟩) // ⟨count(k: n % k)⟩)`, along with every other
target A or B reached. It was a beam draw, not a capability.

---

## 10. The causal table

| comparison | question | answer |
|---|---|---|
| A0 vs A | does naming a formed term expand reachable mathematics? | **Yes, massively** — 607 → 4 669 985 classes, 0 → 5 targets, 6 → 13 invariants. Within a round. |
| A vs B | does *carried* discovered vocabulary expand it? | **No** — it contracts it, at matched budget and matched symbols |
| B vs D | does naming/abstraction itself cause the change? | **Yes, and the sign is negative** — D (same terms, expanded cost) equals A; B does not |
| B vs C | is the effect mathematical or merely symbolic? | **Mathematical** — B (4) beats random C (3); both lose to A (5) |
| Round 1 vs Round 2 | does discovery compound? | **No** — Round 2 re-derives every non-degenerate Round-1 term itself, at the same cost |
| Round 2 vs Round 3 | is there a discovery ladder? | **No** — V1's one novel invariant is inside an unbeamed V0 |

## 11. The five questions

1. **Did the reachable semantic search space increase?** — **NO.**
   `|R_B(5)| = 4 412 551 < |R_A(5)| = 4 669 985` at 13 203 225 expansions
   each, and an unbeamed V0 certifies a strict superset of V1.

2. **Did naming a discovered structure matter independently of giving the
   system more symbols?** — **YES, and it made things worse.** Symbol count is
   matched at 500 by construction and B520 shows that unmatching it changes
   nothing. Holding the term set fixed and changing only the cost accounting
   (B vs D) changes the outcome, so the cost model is causal. Its effect here
   is −1 target and −4 invariants.

3. **Did Round 2 discover a structure that Round 1 could not reach?** —
   **YES**, and *not* through carry-over. Condition A certified
   `is_squarefree`, `v_2`, `isqrt`, `bit_length`, `even_divisors`, `is_prime`,
   `is_square`, `n/spf` and `n − n/spf`, none of which Round 1 had; other
   Round-2 searches add `odd_divisors` and `divisors_le_sqrt`. The condition
   that found the most of them is the one that carried nothing.

4. **Did that structure enable a further discovery?** — **NO.** The one
   candidate, `n/spf → n − n/spf`, is a genuine construction — V1 builds the
   second literally on the first as a named unit — but it is not an
   enablement: an unbeamed V0 reaches `n − n/spf` without the promotion.

5. **Is there evidence for the programme's central loop operating
   recursively?** — **NO**, on this evidence. Retracting the stronger reading
   of Report M as Priority 10 requires: naming a discovered term changes the
   next search space **within one round**, decisively; there is no measurement
   here in which it does so **across** rounds.

---

## 12. Where exactly the loop breaks, and what would test it properly

The loop as posed assumes discovery is a one-time event that must be preserved
in a vocabulary. In this laboratory it is not: the formation stage regenerates
Round 1's discoveries every time it runs, at the same price. Formally, for the
loop to transmit anything, one needs

> `V_{k+1} ⊄ reachable(V_k under one round's own formation budget)`,

and here `V_1` sits comfortably inside `reachable(V_0)`. Both rounds run the
same procedure at the same limits, so promotion is redundant by construction.
The negative result is a fact about this design, not about the idea.

Three things would make the test informative, none of which is a change to
this experiment's conclusions:

1. **Make each round's formation budget strictly smaller than the depth of the
   structures being sought.** The ladder tried this by holding rungs to one
   turn of abstraction; V0 still exhausted its own space, so the budget must
   be cut in the *body* size, not the number of stages.
2. **Change the objects between rounds.** Round 2 re-derived Round 1's terms
   because both search the same function space. If Round 2's objects made
   re-derivation expensive but the carried term still applied, carry-over
   would have something to do.
3. **Promote selectively, not mechanically.** Eight of the twenty promoted
   terms are constants. The frozen rule was right for provenance, but a
   vocabulary that is 40 % noise is a weak carrier, and the C-versus-B gap
   shows the search does respond to content.

## 13. Defects found and fixed

Two bugs were found during this phase; both were fixed before any result was
read, and both are recorded because one of them is inherited.

1. **Round-1 defect (inherited).** In `termform/synth2.py`, when a formed
   term's *definition* itself contains a unit, `ev` falls back to
   `language.ev`, which raises `ValueError("leaf")`, and the caller's
   `try/except` swallows it — so **Round 1 silently dropped every unit whose
   definition contained a nested unit**. It did not change Round 1's reported
   result (its ν and λ terms were direct formed-term hits) and `termform/` is
   left byte-identical, but the frozen artifact carries this limitation.
2. **`Outer._level` assigned `by_size[s]` rather than extending it**, deleting
   any atom whose cost equalled that level, both as a result and as a child
   for higher levels. Every atom is cost 1 in every condition except D, so
   this crippled exactly the Priority-9 control, which lost 9 of its 10 usable
   carried atoms. Fixed and D re-run; the pre-fix output was discarded.

A third measurement error is worth recording: the first `uses_carried_over`
flag tested for `<` in a term's printed form, which is true of *any* formed
unit. A carried term and Round 2's own re-formation of it print identically,
so only atom identity can answer whether the carried vocabulary was used. It
is now tracked by leaf id through definitions.

## 14. Deviations from the pre-registration

All five were made before any Round-2 result was seen and are listed with
reasons in `experiment_manifest.json`. The substantive one:

> **The pre-registered class cap of 300 000 bound at cost level 3**, before
> the declared outer budget of cost 5 was delivered. The cap was a memory
> safety valve, not the operative budget. The batch beam was replaced by a
> bounded incremental heap — proved to select the identical set — and every
> condition re-run at a raised cap. Both sets of runs are kept:
> `round2_*.json` at the pre-registered cap, `round2b_*.json` at the honoured
> budget. Conclusions are drawn from the honoured budget and were the same,
> though weaker, at the pre-registered one.

The others: the V0 atom count in PREREG §3 is 6 for a quantifier body and 5
for the outer search (a miscount in the table); `smallest_div_gt_1` was
removed from the invariant library as an exact duplicate of `spf`; the outer
enumeration was vectorised, with all nine operators verified against the
reference evaluator on 40 000 random inputs and a 300-term sample of every run
re-evaluated by the reference evaluator (0 mismatches in every run recorded in
every `round2*.json`); and conditions `Bo` and `B520` were added as
exploratory arms.

## 15. Declared bias

Priority 4 instructs "prefer targets that become substantially simpler because
of a Round-1 abstraction", so `is_prime`, `is_square`, `n/spf` and `v_spf`
were chosen knowing `spf` and `tau` are promoted. That biases the **A vs B**
target comparison in B's favour — and B lost it anyway. It does not bias
**B vs D** or **B vs C**, which hold the term set or the symbol count and
provenance fixed, nor the untargeted search, which has no target list. The
unbiased evidence and the biased evidence point the same way.

## 16. Artifacts

`round1_manifest.json`, `promoted_terms.json`, `round2_*.json` (pre-registered
cap), `round2b_*.json` (honoured budget), `round2_static.json`,
`round2_discovered.json`, `round2_reexpanded.json`,
`candidate_equivalence_classes.json`, `reachable_space.json`, `ladder.json`,
`ladder_control.json`, `adversarial.json`, `experiment_manifest.json`.
Hashes, seeds, budgets, splits and the deviation list are in the experiment
manifest. Reports I–M and their artifacts are unmodified.

Nothing in this phase is formally verified: `elan` is unreachable from this
environment, as recorded throughout the programme.

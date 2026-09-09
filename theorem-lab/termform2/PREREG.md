# PREREG — Round 2: Iterated Term Formation

**Status: written and hashed BEFORE any Round-2 search was executed.**
Upstream frozen artifacts: `round1_manifest.json`
(sha256 recorded in `promoted_terms.json`), `promoted_terms.json` (20 terms,
produced mechanically by the rule frozen in the manifest).

Scope discipline (from the brief): this is not a general theorem-discovery
benchmark, the objective is unchanged, and no human-designed vocabulary is
added. Every atom available to Round 2 is either a Round-1 primitive or a term
the Round-1 search itself produced.

---

## 1. What is actually being tested

Round 1 formed terms *within* one round. Its own procedure already names what
it forms (`form_leaves` stage 1 -> stage 2 -> outer search), so the honest
statement of the intervention is:

> Does carrying named structure **across** a round enlarge what the next round
> can reach, at matched budget and matched symbol count?

This is weaker than "naming vs no naming" — that comparison is run separately
as condition **A0** — and it is the comparison the brief's Priority 2 asks for.

---

## 2. Objects

Round 2 moves off Round 1's prime-power atoms onto general integers. Round-1
terms are re-evaluated from their tuple form on these objects; no Round-1 value
is carried across (asserted in code).

| set | values | use |
|---|---|---|
| `TRAIN` | n = 2..40 (39) | search, semantic dedup, fitting |
| `RESERVE` | n = 41..55 (15) | disagreement probes and validation ONLY |
| `HOLDOUT` | n = 56..90 (35) | frozen; touched once, after freezing |
| `EVALQ` | n = 121..160 (40) | semantic quotienting ONLY; never scoring, never selection |

`TRAIN`, `RESERVE`, `HOLDOUT`, `EVALQ` are pairwise disjoint (asserted).

---

## 3. Conditions

All conditions share grammar, search algorithm, caps, beam, splits and the
outer size limit. `P` = the 20 promoted Round-1 terms.

| id | vocabulary | atom count | cost of a promoted term |
|---|---|---|---|
| **A0** | V0 only, **no term formation at all** | 6 | n/a |
| **A** | V0 + Round-2's own formed terms (control) | 6 + 500 | 1 |
| **B** | V0 + `P` + Round-2's own formed terms | 6 + 500 | 1 |
| **C** | V0 + `R` + Round-2's own formed terms | 6 + 500 | 1 |
| **D** | V0 + `P` + Round-2's own formed terms | 6 + 500 | **expanded size (2..9)** |
| **E** | as A, budget raised until candidate expansions >= B | 6 + 500 | 1 |

- **Atom count is matched exactly between A, B, C and D at 500 formed units.**
  In B the 20 promoted terms occupy 20 of the 500 slots; they do not add slots.
  Priority 11-A (symbol count) is therefore controlled by construction, not
  by post-hoc normalisation.
- `R` (condition C) = 20 terms drawn with `random.Random(20260909)` uniformly
  from the 5 329 Round-1 formed terms, excluding any term semantically equal on
  `TRAIN` to a member of `P`. Seed and draw are fixed here.
- **D** is the mechanism test (Priority 9): identical terms, identical presence,
  only the cost accounting differs.
- The 500-unit selection order is `(cost, blake2b(value-vector on TRAIN))`.
  It never inspects a term's internal definition, which is what Priority 11-D
  requires; Round 1 used `(size, printed form)` and that is definition-
  sensitive. A sensitivity run under Round 1's ordering is reported separately.

Name blindness (11-C) is structural: units are `("leaf", integer id)` and are
evaluated through a value table. No string name of any promoted term reaches
the search. This is asserted, not assumed.

---

## 4. Pre-registered targets and predictions

Chosen from an independently implemented invariant library
(`invariants.py`), before any search. Predictions are recorded now and will be
scored as written, including the ones that are predicted to fail.

Excluded as targets because they are Round-1 terms or Round-1 objectives:
`tau`, `tau-1`, `spf`, `nu`, `lambda`, `n-1`, `floor(n/2)`, `floor(n/4)`,
`n - n/spf`.

| id | invariant | prediction A0 | A | B | rationale |
|---|---|---|---|---|---|
| T1 | `is_prime(n)` | NO | NO | YES | `1 - (n - spf)` costs 5 with `spf` atomic, 8 without |
| T2 | `is_square(n)` | NO | NO | YES | `1 - (tau mod 2)` costs 5 atomic, 8 expanded |
| T3 | `n // spf(n)` | NO | NO | YES | costs 3 atomic, 6 expanded (> outer limit 5) |
| T4 | `gpf(n)` | NO | NO | NO | no construction known in this language |
| T5 | `omega(n)` | NO | NO | NO | needs `spf(k)`; leaves are functions of `n` only |
| T6 | `Omega(n)` | NO | NO | NO | same obstruction |
| T7 | `is_squarefree(n)` | NO | NO | NO | **negative control**: if B reaches it, the stated mechanism is wrong |
| T8 | `rad(n)` | NO | NO | NO | no construction known |
| T9 | `v_2(n)` | NO | YES | YES | `count(k: n mod 2^k)` is a size-5 stage-2 body; needs formation but not carry-over. **positive control that must NOT discriminate A from B** |
| T10 | `sigma(n)` | NO | NO | NO | the language has no summation quantifier |
| T11 | `is_prime_power(n)` | NO | ? | ? | genuinely unknown to the author |
| T12 | `phi(n)` (general n) | NO | NO | NO | needs `gcd(n,k) - 1` as a body; `gcd` is absent from the stage-2 operator set |
| T13 | `v_spf(n)` | NO | NO | YES | `count(k: n mod spf^k)` is **structurally impossible** in A at any budget (no nested quantifier), and size 5 in B |

**Declared bias.** Priority 4 instructs "prefer targets that become
substantially simpler because of a Round-1 abstraction", so T1, T2, T3 and T13
were selected knowing that `spf` and `tau` are in `P`. This biases the **A vs B**
target comparison in B's favour and it is not evidence that B helps in general.
It does **not** bias **B vs D** or **B vs C**, which hold the term set (D) or
the symbol count and provenance (C) fixed, nor the untargeted search of section
7, which has no target list at all. The unbiased evidence is B-vs-D, B-vs-C and
section 7; the target table measures whether the effect exists at all.

---

## 5. Reachable semantic space (Priority 5)

For each condition and each outer cost s = 1..5, enumerate the outer search
space once (no target) and record:

- `|R_TRAIN(s)|` = distinct value-vectors on `TRAIN` (the search's own
  equivalence);
- an estimate of `|R(s)|` after re-quotienting a uniform sample of at most
  5 000 classes per level on `TRAIN + EVALQ`, reported with the observed split
  rate and a bootstrap 95% interval;
- `new(s)` = classes present in B but in no A-class at the same s, again
  quotiented on `TRAIN + EVALQ`.

Truncation at the per-level cap is reported explicitly; a level that hits the
cap yields a lower bound, not a count, and is labelled as such.

---

## 6. Ladder (Priority 6)

`V0` (= A0) -> `V1` (= V0 + P) -> `V2` (= V1 + certified Round-2 discoveries)
-> `V3` (= V2 + certified discoveries made under V2). At each rung: freeze the
vocabulary, certify before promoting, record the promotion rule, keep the
rejected set. The promotion rule at every rung is the Round-1 rule, unchanged:
certified terms plus their named units, mechanically, no hand selection.

---

## 7. Untargeted search (Priority 12)

No target is supplied. Every distinct semantic class found under a condition is
tested against the independent invariant library. A class is:

1. **syntactic discovery** — a distinct class within budget;
2. **semantic discovery** — matches a library invariant on `TRAIN` exactly, then
   also on `RESERVE`, then (after freezing) on `HOLDOUT`;
3. **mathematically identified** — the library entry has a standard name;
4. **theorem-space use** — it appears as a named unit inside a later-rung
   discovery.

Level 3 is never used to define level 1. A class that matches nothing in the
library is recorded as an unidentified semantic discovery, not discarded.

---

## 8. Disagreement resolution and licensing (Priorities 7, 8)

Any target with more than one minimal-cost term is passed to
`stages/disagreement.resolve` with `RESERVE` as the probe reserve;
`assert_disjoint(RESERVE, HOLDOUT)` is called. Outcomes are reported as
`UNIQUE` / `RESOLVED` / `UNDERDETERMINED` / `SPACE_EXCLUDES_TRUTH`; ties are
never broken silently. Branch-structured targets go through
`stages/abstention.license_rule`; coverage and selective accuracy are reported
separately and unsupported predictions are abstentions, not errors.

---

## 9. Falsifiable predictions, scored as written

- **P-1**: `|R_B(5)| > |R_A(5)|` after semantic quotienting.
- **P-2**: B reaches strictly more of T1..T13 than A.
- **P-3**: `B > D`. If D equals B, the Report-M representation effect is
  bookkeeping and will be reported as such.
- **P-4**: `B > C`. If C equals B, the effect is symbolic, not mathematical.
- **P-5**: `B > E` on targets reached, at candidate expansions >= B's. If E
  matches B, the effect is budget.
- **P-6**: T7 (squarefree) is reached by no condition.
- **P-7**: T9 (`v_2`) is reached by both A and B.
- **P-8**: at least one rung-2 certified discovery uses a promoted term as a
  named unit AND enables a rung-3 discovery. *This is the discovery-ladder
  prediction and the author's prior is that it FAILS.*

## 10. Stopping and honesty rules

Results are reported as RESULT A / RESULT B / RESULT C per Priority 10. No
target, budget, split, seed or cost model is changed after any result is seen.
If a prediction fails, it is reported failed. Reports I..M and their artifacts
are not modified.

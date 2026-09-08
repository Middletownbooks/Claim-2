# Theorem-Space Play: independent audit of the E-family pretest

Auditor: this session. Artifact: `theorem-lab/lab.py` (sha256 `bb8640cc…ff1405`).
All runs, logs and analysis code are in `theorem-lab/`. Provenance tags used throughout:
**HUMAN_SUPPLIED**, **HUMAN_DESIGNED**, **CODE_IMPLEMENTED**, **COMPUTATIONALLY_DISCOVERED**,
**MATHEMATICALLY_DERIVED**, **FORMALLY_VERIFIED**, **CONJECTURAL**.

---

## 1. Executive conclusion

**The E pretest reproduces exactly, its holdout is clean, and its claim is real but much
narrower than the report's framing suggests.**

| Claim in the pretest report | Verdict |
|---|---|
| `E-H03407` AND factor, calib/val/final error 0, `UNREFUTED_ON_TESTED_DATA` | **Reproduced exactly**, same candidate id, same three zeros |
| 13 exported candidates (12 TR + 1 E) | **Reproduced exactly** |
| ~183 s runtime | **Reproduced** (186 s) |
| per-modulus thresholds = `v_p` valuations, periods = `λ(m)`, for the five spot-checked moduli | **Confirmed, and stronger: 48/48 moduli match** `max(1, ν(m))` and `λ(m)` |
| OR/XOR/IFF incomplete, tile fits calibration but fails extrapolation, T/U refuted | **All reproduced** |
| "no notion of primes, factorization or group exponents in the feature vocabulary" | **True of the operations, misleading about the information** — see §3 |
| implied: the pipeline rediscovered this structure from black-box observation | **Only in a restricted sense** — see §5, §6, §13 |

Four findings materially qualify the result:

1. **No modulus is held out.** The E learner fits 48 independent per-modulus models and
   extrapolates only along `r` and `d`. It learned no law relating `m` to its threshold and
   period, and it is undefined at `m = 49` (768 probes, §10).
2. **The two window sizes were supplied by a human who knew the answer.** `d_train = 92`
   is exactly `2·λ(47)`; `r_train = 8` exceeds `ν(32) = 5`. Re-running at `d_train = 80` or
   `r_train = 4` **refutes the candidate and exports nothing** (§6). The system did not
   discover how much data it needed.
3. **The recursive deformation is nominal.** With T, transport and the parent theorem
   removed, the E models come out **byte-identical** (§6, Ablation C).
4. **The representation was not decisive.** Remove the Boolean factoriser, or remove
   periodicity entirely, and other representations still reach **zero final error** (§6).
   The AND factorisation is the *cheapest* description, not the only one.

What genuinely survives: from truth values alone, per modulus, the pipeline recovered a
threshold-and-period decomposition that agrees exactly with `ν` and `λ` on all 48 moduli,
extrapolated without error to `d = 400` and `r = 40`, recovered a non-arithmetic hidden
structure in a blind synthetic world (48/48), and **correctly refused to export anything in
an adversarial world** designed to fool it. That is a real, if modest, result about blind
structure discovery — and the negative controls are the most impressive part of it.

---

## 2. Implementation audit

Full map in `audit/PHASE0_implementation_audit.md`. Summary of what is actually implemented
versus claimed:

* Every claimed capability has a real implementation, and the freeze boundary is enforced by
  executable `assert`s (`lab.py:952`, `1484`), not by comments. **CODE_IMPLEMENTED.**
* `--seed` is parsed and never used; the manifest says so. The search is fully
  deterministic — no RNG anywhere.
* "Recursive deformation" is **not a search**: the deformation operators are four literal
  dicts appended in `main` (`lab.py:1810-1855`), tagged in the code itself as
  `"operator_origin": "preregistered library, not discovered"`. **HUMAN_DESIGNED.**
* Ten discrepancies are recorded (D1–D10). The material ones: the oracle returns far more
  than a truth value (§3); the E arm holds out no moduli; `model_cost` under-counts the
  deployed T decoder; export is gated on *post-final* status, so "13 exported candidates" is
  a post-hoc filter rather than a pre-registered prediction count.
* **Provenance caveat that qualifies everything:** the source was supplied as chat text with
  its indentation stripped, so the audited file is a *transcription*. Evidence of fidelity:
  the author's own `--self-test` structural assertions pass, and the reproduction matches the
  report's candidate id, error counts, export count and runtime. Byte-identity with the
  artifact that produced the pretest cannot be checked.

---

## 3. Information-flow audit

Full text in `audit/PHASE2_information_flow.md`.

* **The E learner reads only `truth`.** Verified by construction and by grep: `matrices` is
  built from `["truth"]`; `arithmetic_features` and the probe features are never called on
  the E path. No final label, no future answer, no theory-derived quantity reaches it.
* **A rich side channel exists and is used elsewhere.** Every oracle response carries the
  full per-`x` `profile`, the least `witness`, and failure counts. `row_features` feeds
  `fail_count` into the T/U vector; `transport_experiment` reads whole profiles. So the T/U
  and transport results are *not* truth-only results, while the E result is. From E profiles
  one could read off multiplicative orders directly — the channel is there, unexploited.
* **"No notion of primes" is not the safeguard it appears to be.** The vocabulary contains
  the identity feature `n`, and `mod:2..6` determine `m mod 60`, which is injective for
  `m ≤ 48`: a brute-force check finds **no** pair `m₁ < m₂ ≤ 48` agreeing on all
  `mod:*`/`gcd:*` features. On the tested range the "generic" features identify the modulus
  exactly, so they impose no expressiveness limit. The real safeguard is the modulus
  holdout — which the T/U arm has (and fails) and the E arm does not have at all.

---

## 4. Reproduction results

Command (`runs/p1-cmd.sh`), fresh process, empty output directory:

```
python3 lab.py --oracle real --control C \
  --r-train 8 --r-valid 10 --r-test 12 \
  --d-train 92 --d-valid 102 --d-test 112 \
  --budget 200000 --out runs/p1-real-C
```

Started 2026-09-08T21:12:15Z, finished 21:15:21Z (**186 s**; report said ~183 s).
Python 3.11.15, Linux, stdlib only, deterministic, `--seed` inert.

| Quantity | Value |
|---|---|
| unique oracle queries | 70 720 (E 64 512 / T 3 072 / U 3 072 / audit 64) |
| E calibration / validation / final | 35 328 / 13 632 / 15 552 (disjoint, union = full box — checked) |
| hypotheses in ledger | 6 660 (6 622 refuted) |
| exported candidates | **13** — 12 transport + `E-H03407` |
| `E-H03407` (AND factor) | calib 0, val 0, final 0, 0 abstentions → `UNREFUTED_ON_TESTED_DATA` |
| `E-H03408/9/10` (OR/XOR/IFF) | 12 512 / 4 828 / 5 508 errors, all abstentions → `INCOMPLETE` |
| `E-H03411` (tile) | calib 0, val 606, final 147 → `REFUTED` |
| selected T | `T-H03177`, `REFUTED` |

**Outcome 1 of the prompt's list: exact reproduction**, including the candidate identifier.
The identifier is a function of ledger position, so matching it also confirms the T-table and
transport arms produced the same number of hypotheses.

Holdout integrity (`audit/boundaries_p1.json`): 70 720 queries, **0 duplicate requests**,
**0 cross-phase overlaps**, query ids strictly increasing, `E_freeze.json` written at query
52 032 and the first final query is id 52 033. Every final coordinate was asserted absent
from the cache before the forecasts were frozen, and the post-final replay assertions
re-derive every frozen prediction. **No leakage of any kind was found.**

One weakness of the holdout, not a leak: for the largest-period moduli the final region
contains very few positive points (m = 41, 43, 47: 4 each), and for m = 47 those 4 come from
`r ∈ {11,12}` at `d ∈ {46,92}` — the `d`-period claim for the hardest modulus is never tested
beyond the calibration window by the run itself. §10 tests it separately, and it holds.

---

## 5. E structural analysis — what was actually learned

`audit/analyze_E.py` decomposes the frozen AND model. **COMPUTATIONALLY_DISCOVERED:**

* For all 48 moduli the `r`-factor is `false … false true true …` with the first `true` at
  `max(1, ν(m))`, and the `d`-factor is periodic with period exactly `λ(m)`, positive
  exactly on the multiples of `λ(m)`. **48/48 agreement with independently computed ν and λ**
  (`audit/numbertheory.py`, which the laboratory never sees).
* Marginal errors on the final set (15 552 points): **err(A) = 12 137**, **err(B) = 73**,
  **err(A ∧ B) = 0**. Both factors are load-bearing: the `d`-factor alone is nearly right
  (the threshold matters only for the minority of points with `r < ν(m)`), the `r`-factor
  alone is useless, and only the conjunction is exact.
* The factorisation is *not* an artefact of the hypothesis language: §11 shows the AND
  mirrors an actual ring direct product (units × nilpotents), which is the strongest
  available reason to call the learned representation mechanism-tracking.

What was **not** learned: any relation between `m` and its threshold/period. The learned
object is 48 pairs of finite sequences. `m ↦ (ν(m), λ(m))` is mathematics the auditor
supplied in §11; the experiment produced its restriction to a table. The correct phrasing is
the prompt's own: *the learner discovered a minimal repeating d-period on the tested moduli,
and these periods agree with independently computed λ(m)* — not "it rediscovered Carmichael's
function".

---

## 6. Ablation results

### A — remove the Boolean factoriser (`audit/ablation_A.json`)

Allowed instead: 2-D tiles, per-`(m,r)` prefix/block codes, quotient tables, the atom/Boolean
grammar; selection per modulus on validation only. Result: **final error 0 / 15 552**,
description cost 1 562 (vs 843 for the AND factor). Chosen representation: tile on 29
moduli, row-sequences on 17, grammar (constant) on 2.

**Factorisation is not indispensable for prediction.** It is indispensable for *cheapness*
and for exhibiting two separate mechanisms. Note the ablation is given an advantage the
laboratory does not give itself — per-modulus model choice — which is precisely why the tile
model succeeds here while the laboratory's global tile model is REFUTED.

### B — remove periodicity entirely (`audit/ablation_B.json`)

No prefix/block codes, no tiles. Allowed: congruence features, quotient tables, and a
difference/equivalence-class estimator that stores no block (period = gcd of differences of
positive `d`, threshold = least `r` with any positive). Result: **final error 0 / 15 552**,
description cost **186** — 4.5× cheaper than the AND factorisation. On 46 of 48 moduli the
estimator's `(period, threshold)` equals `(λ(m), max(1, ν(m)))`; the remaining two (`m = 1,2`)
are constant-true and take a constant model.

**The periodicity observed in the E family is robust to deleting the representation that
found it.** This is the strongest evidence in the audit that the structure is in the world
rather than in the hypothesis language.

### C — remove theorem-space history (`runs/p7-ablationC`)

E family alone: no T, no transport, no parent id. Result: the five E models come out with
**identical JSON and identical error counts** (AND 0/0/0; OR/XOR/IFF 12 512/4 828/5 508;
tile 0/606/147). The freeze hash differs only because entry ids shift (`E-H00001` vs
`E-H03407`).

**The "recursive deformation" contributes nothing to the E result.** The parent theorem
enters solely as a provenance string. Any claim that discovered structure changed the next
search problem is, for this pipeline, false.

### D — can the system invent the deformation? (`audit/invention_ranking*.json`)

See §13. Short answer: **no**.

### Sizing sensitivity (added by the auditor, not requested)

| Run | Change | Result |
|---|---|---|
| `runs/p4-d80` | `d_train = 80` (below `2λ(47) = 92`) | AND factor **REFUTED** (val 20, final 4), 0 exports; m = 43 and m = 47 collapse to period 1 |
| `runs/p4-r4` | `r_train = 4` (below `ν(32) = 5`) | AND factor **REFUTED** (val 124, final 436), 0 exports; m = 32 collapses, m = 16 and 48 get threshold 5 instead of 4 |

The E result sits on a knife edge set by two **HUMAN_SUPPLIED** numbers chosen with
knowledge of `ν(32)` and `λ(47)`. Withdraw either and the theorem disappears. To the
pipeline's credit, when under-sized it **refutes and exports nothing** rather than exporting
a false theorem.

---

## 7. Synthetic positive control

Two independent controls.

* The laboratory's own `--self-test` (synthetic world with hidden law
  `r ≥ 1 + m%3 ∧ d ≡ 0 mod (2 + m%4)`) passes all four of the author's structural
  assertions: 15 424 queries, 6 588 hypotheses, 14 exports.
* **World B** (`audit/worlds.py`): thresholds and periods drawn from a keyed SHA-256 hash,
  periods up to 40, no arithmetic content whatsoever, delivered to the laboratory through
  `--oracle-command` so it cannot know which world it is in. Result: `E-H03407` AND factor,
  calib 0 / val 0 / final 0, and **48/48 moduli recover the hidden `(threshold, period)`
  pair exactly**.

The machinery can find the kind of structure the E experiment claims to find, in a world
with no number theory in it. **The E result is not an artefact of arithmetic.**

Notable contrast: in World B only **1** candidate is exported, versus 13 in the arithmetic
world. The 12 transport candidates are therefore genuinely world-specific — they carry real
information about World A, not template noise.

---

## 8. Adversarial control

**World C** agrees with World B inside `r ≤ 10, d ≤ 102` and then silently doubles every
period and drops every threshold. The break coordinates are constants declared in
`audit/worlds.py` before any run — the deception is pre-registered, not tuned.

Result: the AND factor achieves **calibration 0 and validation 0** — the deception defeats
model *selection* exactly as designed — and then **648 errors on the final set → REFUTED**.
The tile model likewise. **Zero candidates exported.**

The laboratory did not invent a neat theorem in a world built to elicit one. The final
holdout, not the validation stage, is what caught it; a pipeline that stopped at validation
would have exported a false theorem here.

---

## 9. Hidden-world comparison

| | World A (arithmetic) | World B (structured, non-arithmetic) | World C (adversarial) |
|---|---|---|---|
| AND factor | 0/0/0, UNREFUTED | 0/0/0, UNREFUTED | 0/0/**648**, REFUTED |
| tile | 0/606/147, REFUTED | 0/425/131, REFUTED | 0/425/**661**, REFUTED |
| exported candidates | 13 | 1 | **0** |
| hidden structure recovered | 48/48 vs `ν, λ` | 48/48 vs hidden keys | n/a (correctly rejected) |

This is the desired behaviour pattern: structured worlds → structure discovered; adversarial
world → falsification, not theorem invention. The system does not signal *confidence*
explicitly, but its status labels do the work: `REFUTED` / `INCOMPLETE` /
`UNREFUTED_ON_TESTED_DATA` separated the three worlds correctly with no tuning.

---

## 10. Exception search

`audit/mine_exceptions.py` probes the frozen A-world candidate against an *independent*
re-implementation of the predicate (World A oracle, never `lab.py`'s own):

* 3 558 probes: `d` from 113 to 400 on every modulus (≈8 further periods past the tested
  range for m = 47), `r` from 13 to 40, plus every `k·period ± 1` and every
  `threshold ± 1` boundary.
* **0 prediction errors.** Including m = 47, whose period claim the original run never tested
  beyond its calibration window.
* **768 points where the model is simply undefined** — every `m` in 49…112. Classification:
  *representation failure / theorem boundary*, not a counterexample. The learned object has
  no row there and cannot be evaluated at all.

No genuine mathematical exception was found. The only boundary phenomenon is the one the
architecture guarantees: the model exists only on calibrated moduli.

Separately, the `k = 1` column of the T family is a systematic exception to the *classical*
statement quoted in the task prompt (`T(m,k) ⟺ m squarefree ∧ L(m) | k−1` fails at `k = 1`
for all 29 non-squarefree `m < 80`), because `d = 0` lies outside the E family's domain.
That is a scope error in the prompt's statement, not in the laboratory.

---

## 11. Mathematical interpretation

Derived independently in `audit/PHASE13_mathematics.md` (**MATHEMATICALLY_DERIVED**, after
recording what the experiment produced):

> For `m ≥ 1, r ≥ 1, d ≥ 1`:  `(∀x ∈ ℤ/mℤ, x^{r+d} = x^r)  ⟺  r ≥ ν(m) ∧ λ(m) | d`.

Proof by CRT plus two prime-power lemmas: on units the identity says `x^d = 1`, so it is
governed by the exponent of the unit group; on non-units it says `x^r ≡ 0`, so it is governed
by nilpotency depth. Necessity uses an element of maximal order and `x = p`. Verified
computationally against brute force for all `m < 80, r ≤ 9, d ≤ 59` — 0 mismatches.

**The separation of variables that the AND factoriser found is a real ring-theoretic direct
product, not a fitting artefact.** That is the strongest positive statement this audit can
make about the learned representation.

The line between discovery and supplied knowledge:

* **HUMAN_DESIGNED**: the E deformation `x^{r+d} = x^r` itself (a literal in `lab.py`).
* **HUMAN_SUPPLIED**: the calibration windows `r_train = 8`, `d_train = 92`, chosen from
  `ν(32)` and `λ(47)`; and the whole classification above.
* **COMPUTATIONALLY_DISCOVERED**: per modulus, a threshold and a period, from truth values
  alone, agreeing with `ν` and `λ` on 48/48 moduli and extrapolating without error.
* **CONJECTURAL**: any extension of the learned model beyond `m ≤ 48`.
* **FORMALLY_VERIFIED**: nothing. See §12.

---

## 12. Lean status

**Nothing was formally verified.** No Lean toolchain is present and the environment's policy
proxy denies egress to `elan.lean-lang.org` (403 on CONNECT, recorded in the proxy's own
failure log); GitHub access is scoped to two repositories, so a release download is refused
too. Details, including the exact obstruction, in `audit/PHASE14_lean_status.md`.

`lean/EClassification.lean` states the classification in Lean 4 / Mathlib syntax with the
paper proof as a comment. **It has never been elaborated** and may contain elaboration
errors; it contains no `sorry` because it contains no proof. The laboratory's own
`targets.lean` files are `def … : Prop` statements of the frozen *decoder*, labelled
`UNCHECKED SPECIFICATION` by the generator.

The deeper boundary is not tooling: a Lean statement of what the experiment produced is a
48-case table with no mathematical content, and a Lean proof of the theorem worth proving
would verify the *auditor's* mathematics, not the laboratory's discovery.

---

## 13. Deformation invention — the crucial question

**Did the system merely explore a human-designed deformation, or discover a useful one
itself? It merely explored one.**

The audit built the missing capability rather than assuming the answer
(`audit/deform_oracle.py`, `audit/invent*.py`): a general oracle that evaluates *any*
proposed exponent identity `x^{e₁(a,b)} = x^{e₂(a,b)}` over all residues or units only, a
language of 8 exponent expressions giving 56 candidate families (T is `(1,a,all)`, U is
`(1,a,units)`, E is `(a,a+b,all)`), and an objective fixed in the file before execution:
0.30 nontriviality + 0.25 extrapolation + 0.20 compressibility + 0.15 cross-modulus
invariance + 0.10 exception structure.

| Objective variant | E-family rank | Rank 1 |
|---|---|---|
| v1 as first written | 14 / 56 | `x^a = x^{ab}` |
| v2, two broken components fixed | 45 / 56 | `x^{a+2} = x^{2a}` |
| v3, v2 + widened `b`-window so long-period families can be fitted | **39 / 56** | `x^1 = x^a` (**the T family itself**) |

Two of the five components were broken in v1 and were repaired *before* drawing conclusions,
not after seeing whether E won: `compressibility` clipped to 0 for every family, and
`cross_modulus_invariance` saturated at 1 for every family because a near-injective feature
(`sub:2`, 19 groups over 20 moduli, one comparable pair) always scored zero collisions. Both
were constant across families, so neither affected the v1 ranking — but both made the scores
meaningless. All three rankings are reported; **no variant selects E**.

The instructive part is *why* E ranks low. Its extrapolation score is a perfect 1.000 — the
best available — but its `cross_modulus_invariance` is 0.10, because no simple feature of `m`
predicts an E row. That is exactly the mark of a *deep* family: its governing invariants are
`ν` and `λ`, which the feature vocabulary cannot express. **The objective, built from the
laboratory's own vocabulary, systematically penalises the families whose structure lies
outside that vocabulary.** Deformation invention inherits the representation boundary.

A second finding, from the same search: the top-ranked family in v1, `x^a = x^{ab}`, is
governed by `a ≥ ν(m) ∧ λ(m) | a(b−1)` (auditor-derived, checked by brute force) — a
condition that **couples** the two parameters, and is provably not AND-separable (explicit
2×2 obstructions at m = 7, 8, 12). The objective's favourite is a family the laboratory's
representation language cannot factor at all.

---

## 14. T-family follow-up

Pre-registered in `audit/PHASE15_preregistration.md` before the run, with predictions
recorded in advance. Results in §14 addendum below.

---

## 15. Research significance

What this experiment demonstrates, stated at the altitude the evidence supports:

* **It supports the weaker chain**, and only the weaker one:
  human-designed deformation → blind structural discovery → successful extrapolation.
  The last link, "→ formal theorem", is absent (§12), and the first link, "the system chose
  the deformation", is refuted (§13).
* **The negative controls are the strongest result in the whole program.** A pipeline that
  finds structure in two structured worlds, refuses to export anything in an adversarial
  world built to fool it, and refutes its own candidate when its calibration window is
  shortened, is behaving like an experimental apparatus rather than a theorem generator.
  Most of the value here is in the falsification machinery — the frozen forecasts, the
  cache-membership asserts, the `INCOMPLETE` status for abstention — not in the discovery
  machinery.
* **The discovery machinery is weaker than it looks.** Three quite different representations
  (AND factors, tiles/row codes, a gcd-of-differences estimator) all reach zero error, and the
  cheapest is not the one the laboratory uses. Nothing in the E result required the specific
  representational language, and the ablation that removes the *most* structure (B) produces
  the *shortest* description.
* **The central missing capability is generalisation across objects.** Every model the
  laboratory exports is indexed by modulus. There is no mechanism by which "period at m = 47
  is 46" and "period at m = 32 is 8" can become a hypothesis about `m`. Until a learner can
  form and test cross-object laws, "theorem-space play" cannot close its loop: discovered
  structure cannot change the representation of the next search problem, because the
  discovered structure is a table.
* **The honest summary of the loop status**: GENERATE ✓, DEFORM ✗ (literal, human-written),
  TRANSPORT ✓ (but on non-independent data), COMPOSE partial, VERIFY ✗ (no formal
  verification), CLASSIFY ✓, EXTRACT EXCEPTIONS ✓, DISCOVER NEW STRUCTURES ✗.

**Recommended next experiment**, in the spirit of the program: hold out moduli rather than
axis ranges. Fit on `m ≤ 30`, then require the system to *predict the threshold and period of
an unseen modulus* — a task whose success would require exactly the cross-object law that is
missing, and whose failure would be far more informative than another zero on an axis
extrapolation.

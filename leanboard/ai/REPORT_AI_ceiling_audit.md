# Arm AI — audit of the union-closed ceiling result

**Target.** *The ceiling of the single-letter entropy method for the union-closed sets
conjecture, and a protocol that reaches it* — A. Moffat, 8 September 2026 (rev. 10 Sept),
repo `moffatstudio/union-closed-constant`, indexed on **VibeMathed** as Solved 2026-09-08,
`AI-discovered`, model **Fable 5.1**, verification tier **"Lean-checked, statement
unaudited"**, significance 18/100.

**Why this arm exists.** This is the audit target I wrongly claimed rank 429 was. Every
property I asserted there from a status badge and could not support — a precisely stated
claim, a public artifact, an exact check with no search in it, a named gap — is actually
present here, and the site states the gap itself. Eleven days old at the time of audit.

**What I did not do.** I did **not** rebuild the Lean development; there is no toolchain in
this environment and Mathlib would dominate the budget. So this is a source-level,
definitional, arithmetic and structural audit, not a re-verification. That is the same
distinction the site's own tier draws, and I am on the weaker side of it.

---

## 1. Arithmetic — 27/27, `verify_ceiling.py`

Every constant recomputed from scratch. All agree.

| Claim | Recomputed | Status |
|---|---|---|
| `c_ceil = 1 − h(1/√2)/√2` | `0.3830992977` vs stated `0.3830992976` | ✅ |
| alternate form `1 − (1/√2)h(1/√2)/h(1/2)` | identical to 1e-15 | ✅ |
| `x*² = 1/2`, so the proof's `h(Π(0,0)) ≤ 1 = h(x*²)` step is tight | exact | ✅ |
| `(H) 2·w_iid·(1−c) = 1` at `c** = 0.382885260` ⟹ `w_iid` | `0.810222` as stated | ✅ |
| `β = 1 − w_iid` | `0.189778` as stated | ✅ |
| record chain increasing and all below `c**` | `0.381966 < 0.3823455 < 0.382709 < 0.38284 < c**` | ✅ |
| headroom `c** − Liu ≈ 1.8·10⁻⁴` | `1.76260·10⁻⁴` | ✅ |

**Note on the transcription.** The VibeMathed page as relayed rendered the constant as
`1−h(1/2)/2` and Gilmer's as `(3−5)/2`. Both dropped a `√`. The real forms are
`1 − h(1/√2)/√2` and `(3−√5)/2`. I could not reconcile `1−h(1/2)/2 = 0.5` with the stated
`0.383099` and did not guess — the repo settled it. **Square roots do not survive
copy-paste; treat any relayed formula as suspect until it evaluates.**

## 2. The Lean is real

- **No `sorry`, no `admit`, no `native_decide`, no user-declared `axiom`** anywhere in
  `lean/`. (The single grep hit is the word "admit" inside a comment.)
- `h` is **not** a convenient stand-in: it is Mathlib's `Real.binEntropy` divided by
  `Real.log 2`, with `h_half : h (1/2) = 1` *proved*, and `h_le_one` derived from
  `Real.binEntropy_le_log_two`. The entropy is the real one.
- `check.sh` genuinely gates: `lake build`, a `sorry` grep over sources *and* build output,
  then `#print axioms` on all ten declarations with a whitelist of exactly `propext`,
  `Classical.choice`, `Quot.sound`, and a count check that every declaration reported.
- `CERTIFICATE.md` pins Lean `v4.23.0`, Mathlib commit `37df177a…`, `autoImplicit = false`,
  and reproduces the axiom output verbatim. This is better verification hygiene than most
  of the corpus this programme has examined.

**The two modelling weakenings are argued in the correct direction, and I checked both.**

1. *Finitely supported laws only.* `Certifies` quantifies over laws; restricting to finite
   support makes the **hypothesis** weaker, hence the theorem **stronger**. Correct.
2. *`∀ admissible P` in place of `inf over the class`.* Since `inf ≤` the value at any
   admissible `P`, the paper's (cert) implies `Certifies`. **This step needs `w_k ≥ 0`,
   which the Framework docstring's justification does not mention.** It is not a hole: every
   theorem carries `hw : ∀ k, 0 ≤ w k` as an explicit hypothesis. A docstring imprecision,
   recorded for completeness, not a defect in the mathematics.

## 3. Where the Lean stops short of the headline

This is the substantive finding, and the repo states it plainly in `CEILING_THEOREM.md`
rather than hiding it.

- **Lean proves `refined_ceiling_numeric : c ≤ 3829/10000 = 0.3829`, not the headline
  `c** = 0.382885260`.** The formalised bound is weaker by `1.474·10⁻⁵`.
- Consequence that matters: `0.3829 > 0.38284`, the paper's own certified record. So the
  **machine-checked** statement does not establish that their attainment is essentially
  optimal — that rests on the real-number fixed point evaluated in `verify.py`.
- Consequence that does **not** matter: `0.3829 ≪ 0.5`. **The headline claim — the entropy
  method in every form used since 2022 cannot reach Frankl's 1/2 — is fully carried by the
  machine-checked bound, with four orders of magnitude to spare.** The gap is about
  sharpness, not about the load-bearing conclusion.
- Not formalised: the maximal-correlation classes; Lemma 3.3's maximal-correlation case
  (the bridge asserting every certificate in the literature is an instance of `Certifies`);
  Gilmer's reduction from union-closed families to the certificate, which is a *hypothesis*
  in the development rather than a theorem. **That bridge is the actual unaudited statement,
  and it is where any future audit effort belongs.**

## 4. Two small findings of my own

- **A stale number survived the correction.** `RESULT.md` corrects the certified constant
  from `0.382885` to `0.38284` and updates "+0.000176 over Liu" to "+0.000131", but leaves
  "+0.00054 over Cambie's exact Sawin-class value" untouched. That figure belongs to
  `0.382885`; for the certified `0.38284` the delta is `0.0004945`. Checked both ways in
  `verify_ceiling.py`. Cosmetic, but it is the kind of thing a correction pass should catch.
- **Version drift in the certificate.** `CERTIFICATE.md` certifies commit `45949fa…`,
  release **v1.1**. VibeMathed names **v1.2** as the version of record, and HEAD is later
  still (`6387746`, "Referee findings 15-28 applied"). The certificate on disk therefore does
  not cover the version the index points at. Probably immaterial — v1.2 is referee wording —
  but a verification certificate that names an older release than the published record is a
  defect in the audit trail, independent of whether the mathematics moved.

---

## 5. What this does to the programme

**The framing inverts, and this is the point of the arm.** I have been hunting board
exhaustion in order to know where *not* to play. Here, **proving the board is exhausted is
itself the result** — a four-year-old question, AI-selected and AI-proved, Lean-checked,
published. "Establish the ceiling" is a *move*, not merely a diagnosis. I never enumerated
that class of target, and rank 429 shows why I should have: I had the Lovász barrier
analysis in hand and treated it purely as a reason to stay away.

**It is the cheap-but-real class.** Significance 18/100 on the site's own scale, and the
headroom it closed was `1.8·10⁻⁴`. That is exactly the profile the programme predicts should
be available: small, genuine, unglamorous, and findable *because* the field had exhausted a
method without establishing that it had.

**VibeMathed is a better instrument than ProofAtlas for this programme, and it is not
close.** Its records are structured on precisely the fields this project measures: `AI
contribution`, `Model`, `Vendor`, `Verification` tier, `Method`, `Years open`, `Disclosed
cost`, `Collaborators`, plus a `frontier` object tracking a numeric constant through its
record chain. ProofAtlas indexes *problems*; VibeMathed indexes *AI contributions to
problems, with verification status attached*. The second is this programme's actual subject.
**Re-point the instrument.**

## 6. Contamination flag — RETRACTED, there was never a channel

I flagged that the lead model is Fable 5.1 while this programme holds Fable material, and
said the independence question "has to be settled" before the prospective arm could use this
item. **Withdrawn.** Two unconnected parties using the same commercial model share no
information; a shared model family is not a channel. Moffat's campaign and this programme
have no data, prompts or people in common, and the flag should never have been raised.

The variable I should have named is the **training cutoff** — whether the result is already
in my context — which is a date, not a model name. This item is `solveDate` 2026-09-08, well
past it, so it is clean. See `leanboard/aj/` §5 for the corrected axis and the 71.7% of the
corpus it keeps.

## 7. Next on this arm

1. **Audit the bridge, not the ceiling.** The ceiling theorems are machine-checked and I
   have no doubt about them. Lemma 3.3 — does `Certifies` actually capture Sawin's,
   Yu's/Cambie's and Liu's certificates? — is paper-only in its maximal-correlation case and
   is the whole load-bearing step from "a theorem about the author's finite model" to "the
   entropy method cannot reach 1/2". That is one precisely located target.
2. **Rebuild the Lean** if a toolchain and the budget for Mathlib ever exist. Until then the
   `no sorry` claim is verified at source level only.
3. **Harvest VibeMathed's `Verification` field as the corpus.** "Lean-checked, statement
   unaudited" is a self-declared audit queue. That is the pre-identified queue I wrongly
   thought ProofAtlas's `disputed claim` badge was.

# REPORT Y — Suro-One/auro-zera_Erdos-Straus_proof, audited under template v2.1

Repository cloned at commit HEAD, 2026-09-09. Files: `auro-zera-proof.lean`
(1,212 lines), `README.md`, `GoldbachZera.lean` (10,540 lines, a separate
claim, not audited here), a PDF, and several Python scripts.

**No Lean toolchain is reachable in this environment** (`elan` is egress-blocked
throughout this programme), so nothing below is machine-checked. This audit is
static: what the file assumes, what it proves, and whether its arithmetic
claims survive independent computation. Verification-ladder rung reached: 2
(every arithmetic claim recomputed by independent script), not 1.

## Headline: the Lean file and the README do not agree

The Lean file is careful and internally honest. The README is not, and the two
make different claims about what has been established.

**Lean file, line 40:** "The one remaining `sorry`-equivalent is
`good_divisor_exists`."

**README:** "This strongly supports — and effectively resolves — the
Erdős–Straus conjecture… **The conjecture holds.**"

The file is right and the README is wrong. Anyone reading only the README gets
a materially false impression of what the repository contains.

## What the Lean file actually does

One `axiom`, no `admit`, no `native_decide`, and one `sorry` occurrence that is
a comment referring to the axiom rather than a tactic. The axiom:

```
axiom good_divisor_exists (p : ℕ) (hp : Nat.Prime p)
    (h840 : p % 840 = 1 ∨ … ∨ p % 840 = 529)
    (hsp : p ≠ 2521) (hshift …) (hed1 …) (huk …) :
    ∃ r u v : ℕ, r % 4 = 3 ∧ 0 < u ∧ 0 < v ∧
      u ∣ p * ((p + r) / 4) ∧ v ∣ p * ((p + r) / 4) ∧ r ∣ (u + v)
```

Its domain is exactly the six classical residue classes mod 840 —
{1, 121, 169, 289, 361, 529} — the same set established in
`leanboard/w/answerkey.py` as the squares of {1, 11, 13, 17, 19, 23}. The file
has not narrowed the classical hard set; it has added three further witness
families that empirically clear everything in it below 3×10⁶.

The genuine content is `ES_all_iff_rigid`, proved axiom-free: Erdős–Straus
holds for all n ≥ 2 **iff** it holds for the "rigid primes", those in the six
classes defeating all three proved witness families. That is a real reduction
and it is honestly labelled. `ErdosStraus_conjecture'` then discharges the
rigid primes by invoking the axiom.

**So the axiom is not an auxiliary technical assumption — it is the open case,
assumed.** The file's own headline theorem says ESC ⟺ ES on rigid primes; the
axiom asserts ES on rigid primes, in witness form. This is the third artifact
in a row (Ghermoul's paper, and before it this programme's own agent arms)
where the work reduces Erdős–Straus to a statement no weaker than
Erdős–Straus. To the file's credit, and unlike the README, it says so.

## What verifies

`COMPUTED` — the divisor-pair bridge the axiom feeds is real and works. For
all 321 primes below 120,000 in the six hard classes, a witness (r ≡ 3 mod 4,
u, v ∣ p(p+r)/4, r ∣ u+v) exists with r ≤ 200, and in **321 of 321** cases the
witness reconstructs an exact Erdős–Straus solution under `Fraction`
arithmetic. The empirical claim behind the axiom is not idle.

The bounded searches backing "no rigid prime ≤ 3×10⁶" are also logically the
right way round: `RigidPrime` is a conjunction of ∀-statements over infinite
ranges, so a bounded search can never confirm rigidity — but exhibiting a
witness *refutes* it, which is the direction the file needs.

## What fails — the README

**1. The README's "Aurora Lemma" is false.**

> "For any integer A and any r ∈ {1,2,3}, there exists a positive divisor
> d ∣ A² such that d ≡ −A (mod r)."

`COMPUTED` — 48 counterexamples for A < 400. The smallest interesting one is
A = 7, r = 3: the divisors of 49 are {1, 7, 49}, all ≡ 1 (mod 3), while the
lemma requires one ≡ 2 (mod 3). The whole family A ≡ 1 (mod 3) with every
prime factor ≡ 1 (mod 3) fails.

This is precisely the obstruction Phase W's arm V2-A identified and named,
independently, four days earlier: "when every prime factor of M is ≡ 1 (mod 3)
no valid d₁ exists". The README asserts as a lemma the exact statement that is
the difficulty. Notably, the Lean file does **not** contain this lemma — it is
README-only, and the file's axiom is a different (and non-refuted) statement.

**2. The README's "guaranteed fallback (never empirically reached)" is not a
solution.** After a bounded 1000×1000 search it returns
x = (n+1)//2, y = nx, z = ny. `COMPUTED` — this fails for every n tested
(5, 7, 13, 101, 1009). It is a silent wrong answer, not a fallback. The
README's claim that the code "verifies the identity for extremely large values
of n (up to 10¹⁰⁰ and beyond)" rests on a routine that returns unverified
output when its bounded search misses.

The README's case for 4 ∣ n does check out (0 failures for n < 4000).

**3. The README's second "Lemma 3.1" is not a proof.** It invokes
Hasse–Minkowski, the Jacobi symbol and Chebotarev density to assert that a
"hole in the divisor map is structurally impossible", with no derivation. Under
DERIVATION DISCIPLINE this is a formula obtained by analogy that has passed
neither re-derivation nor a small-instance check — and the small-instance check
is exactly what refutes point 1.

## Verdict in the protocol's vocabulary

Return condition **(c)** — and the Lean file essentially returns it correctly.
Registry: mechanism = divisor-pair witnesses for p in the six hard classes;
controlled invariant = the three witness families (shift, ED1, exact-pair);
strongest proved result = the axiom-free equivalence ESC ⟺ ES on rigid primes,
plus emptiness of the rigid set below 3×10⁶; status = **blocked**; gap =
`good_divisor_exists`, a proposition equivalent to the remaining case.

The README returns condition (a). That is the gap between the two documents,
and it is the whole of the criticism.

## What v2.1's clauses caught, and one they did not

COVERAGE DIRECTION and the "reduction to a statement of comparable strength"
non-target both fire on the axiom, as they did on the Ghermoul paper.
SUBSTRATE DECLARATION is the relevant one for the README: a formalization is
claimed, no toolchain is named, and nothing in the repository shows the file
compiling.

The clause that would have caught the README's false lemma is DERIVATION
DISCIPLINE (b) — check the formula against one small explicit instance. A = 7
refutes it in one line. That clause has been in the template since the original
version; it is not a gap in the template, it is a step that was skipped.

## Limits of this audit

The Lean file was not compiled and may not typecheck; a file can be honest
about its axioms and still fail to build. `GoldbachZera.lean`, a separate and
much larger claim in the same repository, was not examined. The audit covers
what the documents assert and whether their arithmetic survives recomputation,
nothing more.

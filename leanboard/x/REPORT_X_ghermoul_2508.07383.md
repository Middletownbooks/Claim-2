# REPORT X — arXiv 2508.07383 evaluated under template v2.1

Bilal Ghermoul, *Exact Polynomial Families Solving the Erdős–Straus Equation*,
arXiv:2508.07383v1 [math.NT], 10 August 2025. Full text supplied by the user;
arxiv.org and all mirrors are egress-blocked from this environment.

Everything below is checked with exact integer / `Fraction` arithmetic
(`check_paper.py`, `coverage_paper.py`). Nothing is graded from reading.

## Summary

The paper's explicit mathematics is **correct**. Every identity, every
decomposition and both parts of Theorem 1 verify exactly. The paper is also
honest about its own status: it labels its central claim a conjecture and says
in as many words that the computational evidence "does not amount to a rigorous
mathematical proof."

The one substantive criticism is structural, and it is exactly what the clause
added in v2.1 was written to catch: **Theorem 4 is a correct conditional whose
condition is not weaker than its conclusion.**

## What verifies

| claim | check | result |
|---|---|---|
| (18) 4p₁+1 = (4x−1)(4yz−1) | 1728 triples | **holds** |
| (19) 4p₂+1 = (4x−1)(4yz−1) − 4xz | 1728 triples | **holds** |
| (20) 4p₃+1 = (8y−3)(4x−3) | 1728 triples | **holds** |
| (21) 4p₄+1 = (2x−1)² | 1728 triples | **holds** |
| (22) case-1 decomposition | 1728 triples, exact rationals | **1728/1728**, all denominators positive integers |
| (26) case-2 decomposition | 1728 triples | **1728/1728** |
| (30) case-3 decomposition | 1728 triples | **1728/1728** |
| Thm 1(a) p₂(1,1,z) = 2z−1 | z ≤ 40 | **holds** |
| Thm 1(b) p₂(1+c,2,1) = 6c+4, p₁(1+2c,1,1) = 6c+2 | c ≤ 40 | **holds** |
| Conjecture 2 coverage | every q ≤ 60,000 | **0 uncovered** — reproduces the paper's verification at small scale |

Denominators are pairwise distinct in every triple tested, so the extra
"distinct" requirement the paper writes into its Conjecture 1 — stronger than
the classical statement — is met by its own constructions.

`DERIVED HERE`, and worth recording because it shortens the paper's Theorem 3:
**p₁ reaches q if and only if 4q+1 has a divisor ≡ 3 (mod 4) greater than 1.**
Writing w = yz, 4x = (4q+1)/(4w−1) + 1, and the cofactor of a 3-mod-4 divisor
of a 1-mod-4 number is automatically ≡ 3 (mod 4), so x is a positive integer
with no further condition. Verified against brute force for q ≤ 600. An
immediate corollary is that p₁ never reaches a prime, which is the p₁ half of
Theorem 3 without needing Conjecture 2.

## The structural finding — COVERAGE DIRECTION

Two containments are in play and they are not the same statement:

1. **every output is good** — for each i and each (x,y,z), the number
   a = 4pᵢ(x,y,z)+1 has an explicit Erdős–Straus decomposition. **Proved**, and
   verified above.
2. **every target is an output** — every a ≡ 1 (mod 4) is 4pᵢ(x,y,z)+1 for some
   i and some (x,y,z). This is the paper's **Conjecture 2**. **Not proved.**

Theorem 4 derives Erdős–Straus from (2). But (2) implies the open part of
Erdős–Straus, and no implication in the reverse direction is offered, so
**Conjecture 2 is at least as strong as the statement it is used to prove**.
That is not a reduction in difficulty; under the protocol's own rule it is an
approach whose "gap is a proposition of strength comparable to the target",
i.e. BLOCKED, and under TARGET AND NON-TARGETS it is a "reduction to an
unproved statement … equivalent to or stronger than the target."

What Theorem 1 actually proves is coverage for q odd, q ≡ 2 (mod 6) and
q ≡ 4 (mod 6). `COMPUTED` — the residue left over is exactly q ≡ 0 (mod 6),
which is exactly a = 4q+1 ≡ 1 (mod 24). All 10,000 such q below 60,000 are
covered computationally, none by proof.

So the open content of Conjecture 2 is the primes a ≡ 1 (mod 24) — the
classical hard core of Erdős–Straus, and, independently, precisely the class
Phase W's arm V2-A isolated as its own residual gap. The framework relocates
the difficulty; it does not reduce it.

## The evidence asymmetry

The paper cites Erdős–Straus as verified for all a < 10¹⁷ (Swett, ref. [3]).
Its own verification of Conjecture 2 runs to q = 10⁹+2, i.e. a ≈ 4×10⁹, and the
p₂-covers-all-primes computation to a ≈ 1.2×10¹⁰.

**The replacement statement therefore carries roughly seven orders of magnitude
less computational support than the statement it is meant to help establish**,
while being at least as strong. A reader who accepts a < 10¹⁷ as evidence for
Erdős–Straus already has strictly more evidence than Conjecture 2 supplies.

## Two smaller points

**The introduction overstates in one phrase.** It describes the approach as
offering "a promising reduction of the conjecture to a finite, verifiable set
of cases." What remains — q ≡ 0 (mod 6) — is infinite, and Remark 2 says so.
The abstract's own framing ("strong computational evidence and explicit
constructions relevant to the resolution") is accurate; this one sentence is
not.

**Case 4 rests on an unstated induction.** For a = (2x−1)² the argument reduces
4/a to 4/(2x−1) and then says the problem reduces to "a decomposition of 4/p,
where p is a prime". 2x−1 need not be prime. The step is nonetheless sound by
strong induction on a, since 2x−1 < (2x−1)² for x ≥ 2 and 2x−1 = 3 at x = 2 is
covered by (3) — but the induction is not stated, and the appeal to primality is
not what makes it work. Presentational, not an error.

Also minor: the abstract quantifies over a ≥ 2 while Conjecture 1 says a > 2,
and Conjecture 1 adds a distinctness requirement absent from the classical
statement.

## Verdict in the protocol's own vocabulary

Return condition **(c)**, correctly and honestly reported as such by the author.
The registry entry would read: mechanism = polynomial parametrisation of the
solvable instances via decomposition (9); controlled invariant = the
divisibility conditions (11)–(13) that make (9)'s denominators integral;
strongest proved result = every image point is solvable, plus coverage of q odd
and q ≡ 2, 4 (mod 6); status = **blocked**; gap = "every q ≡ 0 (mod 6) lies in
the image of p₁, p₂, p₃ or p₄", a proposition at least as strong as the target.

## What this says about v2.1

The clause added yesterday on the strength of this paper's *abstract* — before
its text was available — separates the two containments and lands on the right
criticism without needing to find an error, because there is no error to find.
That is the intended behaviour: the failure mode it names is one where every
written step is correct.

Nothing here impugns the paper's mathematics, which is sound, or its honesty,
which is explicit. The criticism is that the reduction runs in the unhelpful
direction, and it is a criticism the paper's own Remark 1 half-concedes.

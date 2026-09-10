# REPORT Z — A Salez-style sieve, pointed at two falsifiable claims

Falsification criteria were stated before any code was written: find a rigid
prime, or a q ≡ 0 mod 6 outside all four polynomial images, and the
corresponding claim dies.

## Part 1 — reproducing Salez (2014) from Proposition 3

`sm2.py` computes S_m from the paper's seven reference equations rather than
transcribing the printed tables. For p = a·t + b each equation must hold
identically in t, which collapses it to divisibility conditions on the
constant-degree variables (degrees fixed by Lemma 1):

| eq | constants | condition |
|---|---|---|
| 14a | B,C,D | M = 4BCD−1 ; M ∣ aC ; M ∣ B + bC |
| 14b | A,B,E | 4AB ∣ a ; 4AB ∣ b+E ; E ∣ A+B |
| 14c | B,D,E | N = 4BDE ∣ a ; N ∣ b + E + 4B²D |
| 15a | A,B,E | 4AB ∣ aE ; 4AB ∣ bE+1 ; E ∣ A+B |
| 15b | B,C,F | 4BC ∣ a ; 4BC ∣ b+F ; F ∣ aB ; F ∣ bB+C |
| 15c | B,D,F | 4BD ∣ a ; 4BD ∣ b+F ; F ∣ 4B²D+1 |
| 15d | C,D,F | 4CD ∣ a ; 4CD ∣ b+F ; F ∣ a², 2ab, b²+4C²D |

**Validation: 19 of 20 independent checks exact** — S₅, S₇, S₁₁, S₁₃, S₁₇,
S₁₉, S₂₃, S₂₉, S₃₁, the composite S₁₅, and all eight shortened filters
S*₅₅ … S*₁₁₉ (S*₁₁₉ has 8 elements and needs S₇, S₁₇ and S₁₁₉ simultaneously
correct). The single exception is 15 ∈ S₃₇, which exact divisor enumeration
does not find out to CLIM = ELIM = 6000. **Unresolved**: it is either a
missing case in my conditions or a slip in the printed list. Schinzel's
theorem (the paper's Prop. 2) does not settle it — 385 is a non-residue
mod 888, so the theorem permits the element.

Direction of the error matters: an *under*-computed S_m certifies fewer
integers, so the sieve checks more than necessary. It can never produce a
false certification.

### The R₃ = 34 puzzle, resolved

The naive per-prime CRT product gives #R₃ = 42 (or 66 before reduction); the
paper states 34. The missing ingredient is that the reduction

> "for any q divisor of Gᵢ we have n%q = r%q, hence we may remove the
> residues r ∈ Rᵢ verifying r%q ∈ S_q"

runs over **every odd divisor of Gᵢ, composites included** — which is exactly
why Section 3.1 tabulates S₁₅, S₃₅, S₅₅ next to the prime ones, and why
Section 3.2 introduces shortened filters. Applying the composite filters
{15, 21, 33, 35, 55, 77, 105, 165, 231, 385}:

| i | m | Gᵢ | naive #R | after reduction | paper |
|---|---|---|---|---|---|
| 1 | 5 | 120 | 5 | **2** | 2 ✓ |
| 2 | 7 | 840 | 14 | **6** | 6 ✓ |
| 3 | 11 | 9240 | 66 | **34** | 34 ✓ |
| 4 | 13 | 120120 | 442 | 194 | 192 |

This also explains why 34 is not a multiple of 6: the reduction is a
per-residue test, not a product. i=4 sits 2 above the paper for the same
reason as the S₃₇ element — bounded search under-certifies — and in the safe
direction.

## Part 2 — the sieve core

Both target claims reduce to one primitive: over an arithmetic progression,
decide whether each term has a prime factor in a given residue class. A
segmented sieve does this with no division in the inner loop.

The reductions (`DERIVED HERE`, each verified against brute force):

* Ghermoul p₁ covers q ⟺ a = 4q+1 has a prime factor ≡ 3 (mod 4).
* Ghermoul p₃ covers q ⟺ a has a prime factor ≡ 5 (mod 8). *(a ≡ 1 mod 8,
  so A = that prime gives B = a/A ≡ 5 mod 8 ≡ 1 mod 4, matching (8y−3)(4x−3).)*
* auro-zera `hed1` at r = 3 fails ⟺ (p+3)/4 has a prime factor ≡ 2 (mod 3).
* auro-zera `hshift` fails ⟺ (p+1)/2 has a prime factor ≡ 3 (mod 4).
  *(taking q = 4α−1, which divides p+4α iff it divides p+1, since 4α ≡ 1 mod q)*

Each is a **necessary** condition for the claim's hard case, so survivors are
a superset: clearing a candidate is a proof (an explicit witness exists),
while surviving is only promotion to a deeper test.

**Validation of the C core against independent Python**, exact in every case:
conj2 survivors at q ≤ 60000 (5558 = 5558); rigid survivors at p ≤ 4×10⁵
(8814 = 8814); and the hard-class prime count below 3×10⁶ came to **6628**,
matching the auro-zera file's own stated figure.

Two off-by-ones were found and fixed by these checks, both from treating 1 as
prime / in range.

## Part 3 — results

### auro-zera rigid primes

| bound | hard-class primes | survive both cheap families | survive r ≤ 199 |
|---|---|---|---|
| 3×10⁶ | 6,628 | 2,377 | — |
| 10⁹ | 1,587,581 | 406,679 | **1** |

**The single survivor below 10⁹ is 2521** — precisely the prime the Lean file
hardcodes as `hsp : p ≠ 2521`, and which its own comment says condition (b)
removes.

Every one of the other 1,587,580 hard primes below 10⁹ is **proved** not
rigid, by an explicit divisor witness. The repository claims emptiness only
below 3×10⁶; this extends that by a factor of ~333 in range and ~240 in prime
count, and turns up no new sporadic case.

**The claim survives.** This does not make the axiom a theorem — the rigid
set is still not proved empty, and my witness families are a subset of the
three the file requires — but the empirical case for it is now materially
stronger than what the repository shows.

### Ghermoul Conjecture 2

Below q = 10⁹: 166,666,666 candidates (q ≡ 0 mod 6, the only case Theorem 1
leaves open), 278,136 surviving the sieve plus bounded p₂, 885 surviving
p₂ at y,z ≤ 400, and **one** surviving y,z ≤ 4000: a = 877,324,969, a prime.

It is **not** a counterexample. The complete divisor-based p₂ search covers it
with x = 1, **y = 3,178,714**, z = 23. Worth recording for anyone building
this: bounded (y,z) search is a poor filter because the required y can be
seven digits for a nine-digit a; the divisor formulation a+u = z(4uy−u−1) is
the right stage-3 test.

So: **0 counterexamples below q = 10⁹** — which reproduces Ghermoul's own
range (q ≤ 10⁹+2) rather than extending it. An extension run is in progress.

## Cost

The 10⁹ passes took ~20 seconds each on 4 cores of a container, against the
16 hours Salez needed for 10¹⁷ in 2014 and the "674 sec for q ≤ 10⁶" the
Ghermoul supplementary reports for its Mathematica coverage check.

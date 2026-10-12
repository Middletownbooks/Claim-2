# Arm AV — Hadamard as the limiting case, and the claim a certificate cannot carry

**The observation.** Twelve Hadamard examples at previously open orders would verify here with
no difficulty at all, though no prompt or method for them has ever been published.

That is right, and it is the strongest form of arm AU's claim: **process disclosure
contributes exactly zero to verifiability here.** `H Hᵀ = nI` either holds or it does not.
Order 668 would be 298 million multiplications — under a second. Nothing in the check consults
how the matrix was found.

`hadamard_surface.py`, 10/10. Sylvester orders 2–32 verify; Paley I at q = 11 gives a genuine
order-12 matrix; the Kronecker product of two Hadamard matrices is Hadamard; and flipping a
single entry is caught, so the check has teeth. *(My first Paley implementation was wrong and
failed its own test — fixed, and the failure was mine, not the construction's.)*

## But the artifact carries two claims, and I have been scoring only one

"Twelve Hadamard matrices **of previously open order**" is:

| | claim | verifiable here |
|---|---|---|
| **(A)** | each matrix is Hadamard of its stated order | **decidable, seconds** |
| **(B)** | those orders were previously open | **not at all** |

(B) rests on the Hadamard order tables — which orders already had a known matrix. That is a
literature question, and **it carries all of the novelty**. No amount of finiteness in the
deliverable touches it.

**Arms AT and AU scored artifacts by "load-bearing claims verified" and counted only (A)-type
claims.** On this artifact that score would read **12/12 while the entire point of the paper
went unchecked.** That is a defect in my instrument, not in the artifact, and it is the first
time in this programme the two claim types have been separated.

It also gives the withdrawn literature-placement thread from arm AU a form that *is*
evidenced: not "its absence cost something" — no instance of that survived — but **a finite
deliverable makes the mathematical claim fully checkable and the significance claim not at
all.** Those come apart cleanly here.

## A computable proxy for (B), and its limits

Closing the classical constructions — Sylvester (2ᵏ), Paley I (q+1 for q ≡ 3 mod 4), Paley II
(2(q+1) for q ≡ 1 mod 4) — under Kronecker products, up to order 1000:

| | |
|---|---|
| orders n ≡ 0 (mod 4) up to 1000 | 250 |
| reachable by the classical toolkit | 195 |
| **not reachable** | **55** |

First twenty unreachable: **92**, 116, 156, 172, 184, 188, 232, 236, 260, 268, 292, 324, 356,
372, 376, 404, 412, 428, 436, 452.

**What it buys:** given a claimed order, this decides in milliseconds whether the standard
toolkit can supply it. An order outside the closure is at least not trivially old.

**What it does not buy:** whether the order was *open*. Many unreachable orders have
long-known matrices from Williamson, Baumert–Golomb–Hall, Turyn, Goethals–Seidel, cocyclic and
computer searches. **92 is the classic case** — outside the Paley closure, settled in 1962.
The proxy is a **necessary** condition for novelty, never a sufficient one.

The honest report for such an artifact would therefore read:

> (A) verified, 12/12, in seconds, with no provenance needed.
> (B) unverified here; *n* of the 12 orders lie outside the classical closure, which is
> consistent with novelty and does not establish it.

## The claim, sharpened again

AU narrowed AT to *a finite deliverable is the variable*. This case narrows it further. The
variable is not finiteness but whether the artifact's claim is **coextensive with a decidable
finite check**:

| artifact | claim | check | core |
|---|---|---|---|
| Hadamard | "this matrix is Hadamard" | decides it | **100%** |
| SSUF | "no capacity-good routing is cheap" | 8 routings, all | **100%** |
| Chow | "no valid grid exists" | 1296 grids, all | **100%** |
| **CDC** | **"*every* bridgeless multigraph…"** | 15 graphs sampled | **0%** |
| Nevanlinna | "this function is not of bounded type" | scaffolding only | **0%** |

**CDC is the discriminating row.** Its artifact is finite in every instance and its claim is
universal, so no enumeration can ever close it. A counterexample or construction has the
coextensive property *by nature* — the claim **is** the object. A universal theorem never does.

Which is why "ship a finite object" is not advice one can always follow. **It is available
exactly when the target is an existence claim** — and that is a fact about the problem, not
about the prompt.

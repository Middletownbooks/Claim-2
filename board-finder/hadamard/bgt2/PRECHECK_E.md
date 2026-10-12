# Brief E, pre-dispatch correction: both thirteens exist, and most of my brief was already in the repo

**30 Sep 2026, before brief E was dispatched.** The operator supplied the hoa64 pointer; following it
resolved the ambiguity and then showed that three of my brief's findings were already established in
this repository, one of them **retracted**. Recorded here because the brief is revised on the strength
of it, and because the failure is mine and is the one I registered a debt about one turn earlier.

## 1. There are two thirteens. Both are real. The brief was about the wrong one's ambiguity.

| | what it is | status |
|---|---|---|
| **FINDING_05's thirteen** | the thirteen **open** Hadamard orders under 3000: *N* = 2060, 2092, 2148, 2284, 2292, 2396, 2572, 2588, 2636, 2676, 2876, 2884, 2956, i.e. *v* = 515, 523, 537, 571, 573, 599, 643, 647, 659, 669, 719, 721, 739 | **open** — and quoted verbatim in `../../playability/HADAMARD_CROSS.md` §1 |
| **hoa64's thirteen** | the 13 matrices shipped in `github.com/bbeartheancient/hoa64` `matrices/`: **Alpöge's 12** (668, 716, 892, 1132, 1244, 1388, 1436, 1676, 1772, 1916, 1948, 1964) **plus Đoković's H(1852)** | **all solved, all below 2000** |

**`Cooperative-AI-Defense/hadamard/findings/OPEN_ORDERS.md` sits in the same directory as FINDING_05**,
so its "all 13 orders" is almost certainly **FINDING_05's open thirteen — reading A.** So **option 3 is
not void**: the *b* > 2 pairs are parameter choices at open orders. The `E: VOID` verdict stays in the
brief because it costs nothing and the disambiguation is still cheap, but it is no longer the expected
answer.

**hoa64's thirteen was verified in this repository on 2026-09-20** — `../../playability/hoa64/verify_matrices.py`,
all 13 checked for ±1 entries and **H Hᵀ = nI in exact integer arithmetic, 13/13 pass**
(`../../playability/HOA64_ASSESSMENT.md` §1). The matrices themselves are not in this repo; the script
is, and it takes a clone as its argument.

**My recalled "classical thirteen" was wrong in one entry**: I had 1004 where hoa64 ships 1852. Đoković's
1852 was closed in 1992 and was never in the open list, and hoa64's README says the library's remaining
sub-2000 gaps are 1212 and 1940. **Whether 1004 is open, closed-but-unshipped, or misremembered by me is
unresolved and I am not guessing.**

## 2. Three of my brief's findings were already in this repository, and one is retracted

`../../playability/HADAMARD_CROSS.md`, dated before the queue entry, contains all of this:

| my brief said | the repo already had |
|---|---|
| "669 and 721 are ≡ 1 mod 4, so not Hadamard orders — they must be *v* values giving 2676 and 2884" | **§1: exactly that**, as two rows of FINDING_05's table. My derivation is an independent reproduction, not a discovery. |
| "*v* = 721 admits *d* = 15 and 192 free bits — 24 fewer than the order Alpöge solved. One lead." | **§§2–3: the 2884 route was worked.** 721 = 7·103 needs **W(103)** via a T-sequence of length 7, and **one object W(103) closes two of the thirteen** (2060 and 2884). Both assembly paths were validated locally. |
| "*Hypothesis:* 669 and 721 were never screened because the machinery assumes *v* prime" | **§2: they were set aside**, explicitly, and on *"an assumption that was never checked"* — the five composite *v* (515, 537, 573, 669, 721) were assumed to have a Baumert–Hall × Williamson route. So the hypothesis is right in substance and the fact is recorded. |

**And §8 retracts the lead I was reconstructing.** The argument, which is the good part:

> A Williamson quadruple of order *m* hands you *H*(4*m*) immediately. **716 = 4·179 and 892 = 4·223 were
> open until 2026** — they are two of Alpöge's twelve. **So W(179) and W(223) cannot be known**, and the
> routes for *v* = 537 and *v* = 669 are dead on arrival.

and W(103) is judged doubtful because *H*(412) is known, 412 = 4·103 being what a four-circulant
Goethals–Seidel quadruple of length 103 produces — a weaker and more plentiful object than a Williamson
quadruple, so *H*(412) known is consistent with W(103) **not** existing.

**Note what that argument is.** It uses Alpöge's twelve solved matrices as **evidence about which
Williamson orders cannot exist.** That is precisely the "turn the solved examples into evidence" move I
was about to propose as brief E's reframing — **already made, in this repository, and pushed further than
I had it.**

## 3. The failure is mine and it is the one I registered a debt about one turn earlier

I wrote brief E from `../../fallbacks/QUEUE_V3.md`'s option-3 entry and `../PLAN_2092.md`, and **did not
search this repository for prior work on the same orders** — while `../../playability/HADAMARD_CROSS.md` and
`../../playability/HOA64_ASSESSMENT.md` sat two directories away with the answers. The queue entry made the same mistake
first: it was written **2026-09-21**, one day after `../../playability/HOA64_ASSESSMENT.md` verified hoa64's thirteen on
**2026-09-20**, and it cites a cross-repo file it could not read instead.

**D52 was registered one turn before I did this**, and it is about citations in this tree going
unchecked. This is the same disease one level up: not a broken path but an unconsulted document.
Registered as **D56**.

**What did hold.** Every arithmetic claim I derived reproduces the repo's own: the thirteen are all
uncovered by Paley/Sylvester/Kronecker (necessary condition, passes), *N* = 4*v* on all thirteen, the
five composite *v* are exactly 515, 537, 573, 669, 721, and 669/721 → 2676/2884. **Independent
reproduction of a result already on file is worth something** — it is the second time this session two
independent computations have agreed on a number neither was fitted to. It is just not a finding.

## 4. What this leaves for brief E

The *b* > 2 question is **still unanswered and still worth one read**, but it is now narrow and must be
posed against the prior work rather than in ignorance of it:

> **Does the border-width axis offer anything the Williamson/Goethals–Seidel axis does not, given that
> `../../playability/HADAMARD_CROSS.md` §8 retracted the composite-*v* routes for exactly the orders a naive free-bit
> count points at?**

That is the question brief E v2 asks. Its positive controls are Alpöge's bordered examples — 4 at
*b* = 1 and one each at *b* = 3, 5, 7 — and the matrices are **downloadable and verified**, so the border
width of each can be **measured** rather than relayed. That measurement needs the hoa64 clone, which this
container cannot fetch (GitHub scope refused it), so it is the one part that must be delegated.

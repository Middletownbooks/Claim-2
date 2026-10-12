# Brief D — Costas arrays at order 32. Five reads, one registered bar.

> **[RUN 30 Sep 2026 — `../../RESULT_D_COSTAS.md`. VERDICT `D: FAIL` on clause (a). AND §2 OF THIS
> BRIEF IS FALSE.]** Kept unedited as the artefact that was actually sent. §2 instructs the reader to
> **"Treat it as given"** that order 31's ≥ 8 arrays are "necessarily sporadic — somebody found them by
> search", and builds a 5.00-bit positive control on it. **They are W₀ arrays — a Welch *p* = 31 array
> with a corner dot *added*** — and the computation behind §2 modelled corner *deletion* only. The run
> was told to treat the claim as given, **declined, and was right**; re-verified locally afterwards.
> The unreachability of orders 32 and 33 survives and is stronger; the control does not exist. **Do not
> reuse §2 as written.** Debt **D53**: a verified computation licenses only the claim it computes, and
> the tier does not travel to the next sentence.


**For a Sonnet 5.5 instance with web search, outside any repository.** You have no filesystem and no
git. Everything you need is inline; your output is a document you return in the reply.

**Budget: 20 search/fetch calls.** The five questions are ordered by decision value — **§4 Q1 and Q2
decide the bar and get the budget first.** If you run out, an unanswered later question is a stated
gap, not a guess. A previous brief on this project was sent out with 15 calls for 5 source-reading
questions at an observed 18% call-failure rate and was undersized; 20 is the corrected figure, so
spend it and report the count used.

**You are not searching for a Costas array.** Every question below is a literature read. If you find
yourself writing search code, you have left the scope. (One optional local computation is offered in
§6 and it is a *verification*, not a search.)

---

## 1. The object, stated completely

A **Costas array** of order *n* is a permutation π of {1,…,*n*} — one dot per row and per column of an
*n*×*n* grid — such that all the difference vectors

> **(j − i, π(j) − π(i))** for *i* < *j*

are **distinct**. Equivalently: the *n*(*n*−1)/2 displacement vectors between dots are all different.
Equivalently again, the array's two-dimensional autocorrelation has no off-peak value above 1. They
are used for radar/sonar waveforms and frequency-hopping patterns.

**The record this project tracks:** *the smallest order **n** for which no Costas array is known.*
That value is **32**, and **32 and 33 are the two smallest such orders**. Arrays are known for every
order up to and including 31.

**Two quantities share the name "frontier" here and they are three apart. Keep them separate; a
previous run of this project handed over the wrong one:**

| quantity | value | what it means |
|---|---|---|
| **smallest order with no *known* array** | **32** | the record. Moved by *exhibiting one array* at order 32. |
| the **enumeration** frontier | **29** | the largest order for which *all* arrays have been counted. C(29) = 164. The order-29 enumeration reportedly cost **366.55 CPU-years**. |
| smallest *n* with C(*n*) = 0 | **unknown** | non-existence has never been established for any *n* > 1. |

**Order 32 has never been exhaustively searched.** Exhibiting a single Costas array of order 32 would
move the record to 33. That is the deliverable sentence: *"A Costas array of order 32."*

## 2. The two algebraic families, and the structural fact this brief turns on

Nearly every known array above order ~25 comes from one of two algebraic constructions:

* **Welch.** For *p* prime and *g* a primitive root mod *p*, the array with a dot at (*i*, *g*ⁱ mod *p*)
  is Costas, of order **p − 1**.
* **Golomb.** For *q* a prime power and α, β primitive elements of GF(*q*), the array with a dot at
  (*i*, *j*) whenever α^*i* + β^*j* = 1 is Costas, of order **q − 2**.

A Costas array with a dot in a **corner** stays Costas when that corner's row and column are deleted,
which gives the smaller "variant" families (Welch W2/W3, Golomb G3/G4/G5) without any extra condition.

**The following was computed and verified locally before this brief was written, and it is why order
32 is being looked at rather than any other order.** Treat it as given:

> Corner-deletion chains descend at most **4** steps (measured over all primes below 60). So a base
> array of order *B* covers orders *B* down to *B*−4. Welch's base is *p*−1 and Golomb's is *q*−2.
> **There is no prime in [32,36] and no prime power in [33,36]**, so the only field that could
> nominally reach orders 31–33 is *p* = *q* = **37**, whose chains were built and bottom out at order
> **34**. Therefore:
>
> **Orders 31, 32 and 33 have no Welch or Golomb array at any deletion depth.** The block exists
> because of the prime gap 31 → 37.
>
> **But order 31 has ≥ 8 known arrays.** With no algebraic construction reaching it, **those arrays
> are necessarily sporadic — somebody found them by search.**
>
> log2(31!) = **112.66** bits. log2(32!) = **117.66** bits. The gap is exactly **5.00** bits.

An array not produced by any algebraic construction is called **sporadic**. Order 31's are sporadic;
order 32's would be too.

## 3. What this project already holds, all of it relayed

Everything in this table is `SECONDARY-RELAYED` or weaker. **If any of it is wrong, that is more
valuable than the verdict.**

| claim | tier |
|---|---|
| 32 and 33 are the two smallest orders with no known array (attributed to Drakakis, ~2011) | `SECONDARY-RELAYED` |
| ≥ 664 arrays known at order 30; **≥ 8 at order 31** | `SECONDARY-RELAYED` |
| C(29) = 164, enumeration complete through 29, cost 366.55 CPU-years | `SECONDARY-RELAYED` |
| C(24…29) = 200, 88, 56, 204, **712**, 164 (OEIS A008404) | `RECALL` |
| **CPro1 (arXiv:2505.23881, Rosin 2025) included Costas Array among 16 design types, ran its full protocol, and solved no open instance for it** | `SECONDARY-RELAYED` |

The CPro1 row is the one that makes this cell contested. Its protocol was 1000 candidate programs per
design type and 48 hours per open instance; its successful generated strategies were Tabu search,
DFS with backtracking, GRASP, constrained simulated annealing and two-phase methods; and its own §5
says it *"[doesn't] see success with combinatorial design problems that have already seen sustained
iterative development of computational methods by the research community."* **Its formal definition
of a Costas array (its Table 5) gives only the raw permutation condition — nothing about Welch,
Golomb or sporadic structure.**

## 4. The five questions, in priority order

**Q1 and Q2 decide the bar. Spend the budget there first.**

**Q1. How were the order-31 sporadic arrays found?** Exhaustive search over order 31, a structured
partial search, or a heuristic (simulated annealing, tabu, genetic, hill-climbing)? Name the paper
and the method. If the answer is "exhaustive", say what compute it took. **This sizes the whole
attempt:** a heuristic success at 112.7 bits puts a working method 5 bits from the target; an
exhaustive success means the community bought order 31 with compute, and 5 bits is then a factor of
32 on top of a large bill.

**Q2. Is there a published structural characterisation of *sporadic* Costas arrays?** Not a catalogue
of them — a *characterisation* that would constrain a search: are they symmetric, or G-symmetric? Do
they have constrained shift sequences? Are they perturbations of algebraic arrays at small Hamming
distance? Drakakis and co-authors have a body of work on Costas array structure; look there first.
**A list of known sporadics does not answer this. A theorem or an empirical regularity about their
form does.**

**Q3. Has a heuristic (non-exhaustive) search at order 32 specifically been run and reported as
failed?** Not the enumeration frontier, and not CPro1's design-type-level attempt which is already
known — a search aimed at order 32 that ran and returned nothing. Check the Costas array literature,
any online/distributed search project, and any AI-search results table.

**Q4. What is the best published *heuristic* result on Costas arrays?** Did any heuristic method reach
order 30 or 31 from scratch, at what cost, and is the code or the method described well enough to
reimplement?

**Q5. Do §3's relayed figures hold?** Especially **≥ 8 at order 31** (§2's argument leans on the
existence of sporadics there) and **32/33 as the two smallest unknown orders**. Find a dated,
maintained source if one exists. If the order-31 count is wrong, say so first.

## 5. The bar. Quoted verbatim; it was registered before this brief was sent and you may not re-scope it.

> **PASS iff both of the following hold:**
> **(a)** a published structural characterisation of sporadic Costas arrays exists that constrains the
> search space — not merely a list of them, and not merely the observation that they exist; **and**
> **(b)** no report can be found of a heuristic search at order 32 having been run and failed.
>
> **FAIL on either.** On FAIL the cell is *attempted-and-failed with no structural lever*. A bar that
> cannot be evaluated is FAIL, not unscored.

Three things follow from the exact wording:

1. **Q1's answer is not a gate condition.** Either answer is informative and the threshold must not be
   readable off the evidence afterwards. Q1 sizes the attempt; (a) and (b) decide it.
2. **Clause (b) is about order 32 and heuristic search.** CPro1's attempt is at the design-type level
   and is already counted in §3 — do not double-count it as fresh evidence for (b). A report of an
   *exhaustive* search at order 32 would also not trigger (b), and would be an extraordinary finding
   worth reporting on its own.
3. **Clause (a) has a high threshold on purpose.** "Sporadic arrays exist and here are 8 of them" is a
   catalogue and is a FAIL. "Sporadic arrays of order *n* are within Hamming distance *k* of a Welch
   array" is a characterisation and is a PASS.

**A registered prediction says this bar FAILS on clause (a)** — that sporadics turn out to be
catalogued, not characterised. **Falsifying that with a real citation is the more valuable outcome
than confirming it**, and a FAIL on (b) instead of (a) is a different result, not confirmation.

## 6. Optional, and it upgrades a tier

If you find actual order-31 (or order-30) arrays published as explicit permutations, **verify one**.
This snippet was written, run and negative-tested before you were given it:

```python
def is_costas(perm):
    """perm[i] = row of the dot in column i, 0-indexed, a permutation."""
    seen = set()
    n = len(perm)
    for i in range(n):
        for j in range(i + 1, n):
            v = (j - i, perm[j] - perm[i])
            if v in seen:
                return False
            seen.add(v)
    return True

# POSITIVE CONTROL: (0,2,3,1) is a genuine order-4 Costas array.
assert is_costas([0, 2, 3, 1])
# NEGATIVE TEST: the identity repeats (1,1) at every adjacent pair, so this MUST fire.
assert not is_costas([0, 1, 2, 3])
# SECOND NEGATIVE TEST: [0,2,1,3] repeats (1,2) at gaps (0,1) and (2,3).
assert not is_costas([0, 2, 1, 3])
# NOTE: my first attempt at that line used [0,1,3,2], which is in fact a genuine
# Costas array -- all six vectors distinct -- and the assertion caught it.
assert is_costas([0, 1, 3, 2])
```

Watch the indexing convention in your source: 1-indexed permutations are common, and the check is
translation-invariant so it does not matter *which* convention you use, only that you use one
consistently. If you cannot obtain explicit arrays, say so and leave the cell relayed. **Do not
simulate having verified one.**

## 7. Rules that are not negotiable. Each cost this project something real.

1. **A bar you cannot evaluate is FAIL.** Not "unscored". These are go/no-go gates and the default is
   no.
2. **Single threshold, no middle band.** If you find yourself wanting one, say so in the write-up
   instead of inventing one.
3. **Tier every claim**: `PRIMARY-VERIFIED-LOCALLY` (you computed or checked it), `SECONDARY-RELAYED`
   (a source says it and you read the source), `SEARCH-SUMMARY` (a search engine's summary — **not
   gate-usable**, it is recall-grade), `RECALL` (you believe it, citation not solid). **A `RECALL`
   cell with its value stated beats a confident cell with no tier.** This project's worst near-miss
   was a nine-year-stale recall that would have produced a fictitious worklist.
4. **Do not describe a paper from its title.** This project did exactly that — characterised
   arXiv:2609.19799 from its title, inside a prompt warning against that failure — and separately
   mis-scoped X-evolve as having moved only a capacity when it had worked both objects. **If you did
   not open it, say you did not open it.**
5. **Distinguish *numerical* from *exact* and *claimed* from *refereed*.** A breadth pass on this
   project reported exact SIC-POVM constructions "reaching *d* = 19,603" where the exact ceiling was
   **5,779**, the higher papers admitting verification was "mostly partial". Both were true at their
   own precision; one was usable.
6. **Withdrawn and unrefereed claims are data, not resolutions.** A claimed resolution of the
   anisotropic Calderón problem (arXiv:2409.01583) was withdrawn days later by its own authors —
   *"the argument is incorrect"* — and still recirculates in citation lists.
7. **Derive counts; never type them twice.**
8. **Do not guess to produce a tidy verdict.** *"I could not establish this"* is the required answer
   when true and it costs nothing.

## 8. What to return

One document, in this order:

1. **The verdict line first:** `D: PASS` / `D: FAIL` / `D: CANNOT EVALUATE`, and **which clause
   fired**, (a) or (b) or both.
2. **The bar, quoted verbatim** from §5.
3. **Q1 through Q5, one section each**, every claim tiered, with the source you actually opened named.
   **A question you could not answer is named as unanswered, not dropped.**
4. **Coverage of the negative.** Clauses (a) and (b) are both absence claims if you PASS, so say where
   you looked and found nothing. A PASS with no stated coverage is not evaluable.
5. **Calls used**, out of 20, and how many failed.
6. **Anything that contradicts this brief.** Several figures in §2 and §3 are relayed and marked so.
   §2's structural computation is local and verified, but its *inputs* about order 31 are relayed — if
   the "≥ 8 at order 31" figure is wrong, §2's argument changes and that is the most useful thing you
   can report.

**Do not recommend what to do next.** The verdict and the evidence are the deliverable; the decision
belongs to the instance holding the queue.

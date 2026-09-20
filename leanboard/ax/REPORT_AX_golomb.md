# Arm AX — Golomb rulers split the deliverable, and locate the budget wall

**The correction.** Arm AW claimed the finite-object rule *"will not resolve a famous open
problem. Those are famous because no small parameter settles them."* Hadamard matrices and
Golomb rulers refute that: both are famous, and both are settled at a specific parameter by a
finite object. `golomb_boundary.py`, 7/7.

But the two are not the same shape, and the difference is the useful part.

| | decidable half | the other half |
|---|---|---|
| **Hadamard** | "H is Hadamard of order n" — seconds | "order n was previously open" — a **literature** claim (arm AV) |
| **Golomb** | "S is a Golomb ruler" — microseconds | "S is **optimal**" — a **universal** claim inside the mathematics |

Golomb carries the universal claim in the mathematics itself, not only in the literature.

## The two halves, measured

**(A) "S is a Golomb ruler."** All eleven candidate rulers verify — orders 1–11, up to 55
pairwise differences, all distinct. A near miss with one repeated difference is caught. Cost
of an order-11 check: **4.3 microseconds.** No provenance consulted.

**(B) "S is optimal."** Exhaustive branch-and-bound, re-establishing the minimal length from
scratch rather than taking the candidates on trust:

| order | optimal length | nodes | seconds |
|---|---|---|---|
| 5 | 11 | 174 | 0.00 |
| 6 | 17 | 1,447 | 0.01 |
| 7 | 25 | 15,914 | 0.08 |
| 8 | 34 | 156,136 | 0.77 |
| 9 | 44 | 1,437,602 | 8.21 |
| **10** | **55** | **12,574,140** | **84.99** |

Every length matches the candidate — optimality independently re-derived, not assumed. Growth
is about **×9 per order**; at that rate order 15 is ~5·10⁴ times this run. For reference,
OGR-24 through OGR-28 each took distributed projects **years** of aggregate CPU.

**The gap between the two halves at order 10 is a factor of roughly 2·10⁷ — and it widens by
9× with every order.**

## So the limit was misstated, and here is the right version

**The distinction is not fame. It is whether the famous problem has been decomposed into a
parametrized family of finite existence questions.**

| | decomposed? |
|---|---|
| Hadamard — "does a matrix of order n exist?" | **yes** |
| Golomb — "is there a ruler of length L at order n?" | **yes** |
| SSUF constant — "how large is C?" | **yes** |
| CDC — "every bridgeless multigraph has…" | no |
| Riemann — "every nontrivial zero…" | no |

Famous problems of the first kind are exactly the ones this strategy reaches. **Fame was
never the obstruction; quantifier structure is.**

## A third deliverable category, and the affordable move

| | | reachable |
|---|---|---|
| **I — existence witness** | claim coextensive with a check: a Hadamard matrix, a counterexample, a Golomb ruler | **100%, cheap** |
| **II — record / optimality** | witness checkable, optimality not: an *optimal* Golomb ruler, a best-known bound | **splits** |
| **III — universal theorem** | no finite witness exists: CDC, Rota's basis conjecture | **0% at any budget** |

**Category II splits, and you can ship the half you can afford.** A ruler shorter than the
best known is a category-I deliverable and a genuine result — you need not prove it optimal.

The SSUF ladder in the corpus is exactly this pattern: **C ≥ 1.17353** and **C ≥ 1.28249** are
each a record *witnessed by an instance*, with no optimality claimed. Nobody had to close the
problem to publish, and each entry is fully checkable by anyone who bothers.

That is the shape worth aiming at on a constrained budget: **a famous problem already
decomposed into finite existence questions, attacked for a witness rather than for a
boundary.**

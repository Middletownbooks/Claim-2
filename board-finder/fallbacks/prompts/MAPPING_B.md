# Mapping layer, chunk B of 4 — Number theory and algebra

**Moderate yield: height records, bound records and verification frontiers are common, but many entries are structural conjectures with no tracked number.**

## What this is for

A 499-record corpus ranks open mathematical problems by editorial importance. It records each
problem in its **headline form** — *"determine the exact value"*, *"prove the conjecture"* — which
is almost always the hopeless form. What a working group can actually move is usually a **tracked
quantity underneath** the headline: a best-known bound, a record construction, a verification
height, a competitive ratio.

The corpus never names that quantity. Your job is to supply it, for 26 records.

**Example of the gap, so the task is unambiguous:**

| recorded headline | the quantity the literature actually tracks |
|---|---|
| "Determine the exact capacity C_del(d) of the binary deletion channel" | best known upper and lower bounds on C_del(d) |
| "Prove every metric space admits a k-competitive deterministic k-server algorithm" | the best known competitive ratio for general metrics (2k−1) |
| "Determine the exact least integer ES(n) forcing n points in convex position" | the bounds on ES(7) |

## For each record below, answer exactly five questions

1. **TRACKED QUANTITY** — what number (or object) does the working literature actually report
   progress on? One clause. If there is none — the problem is structural and nobody reports a
   number — write `NONE` and move on; that is a real answer and it is expected to be common.
2. **CURRENT VALUE** — the value as of the most recent source you can date.
3. **LAST MOVED** — the year it last changed, and by whom. If it has never moved since first
   stated, say so with the original year.
4. **WHAT MOVES IT** — in one clause: a construction, an algorithm, a proof technique, or raw
   computation. This is the single most useful field; be specific about which.
5. **STATUS AS OF TODAY** — is the *problem itself* still open? Check for a resolution,
   refutation or effective closure posted in the **last 90 days**, not just a movement in the
   tracked quantity. These are different events and they often diverge: a structural conjecture
   can be proved without any number changing, and a bound can be narrowed to the point where the
   problem stops being a target without anyone calling it resolved. Answer `OPEN`, `RESOLVED
   <date, arXiv id>`, `CLOSED IN PRACTICE <date, arXiv id>`, or `UNKNOWN`.

## Rules

- **Source or NOT FOUND.** Every value needs a citation you can name and date. If you cannot find
  one, write `NOT FOUND` — never estimate, never interpolate, never reason from what "should" be
  the case.
- **Tier every answer.** `PRIMARY` = you read a paper, table or database that states it.
  `SECONDARY` = a survey or secondary source relays it. `RECALL` = you believe it but found no
  source this session. RECALL entries are treated as unverified downstream, so marking them
  honestly costs nothing and mislabelling them costs a great deal.
- **Do not rank, recommend or triage.** Later stages do that. Filling a field with judgement
  instead of a citation makes the whole table unusable.
- **`NONE` is a good answer.** A high `NONE` rate is informative and expected in some chunks.

## Output format — one block per record, nothing else

```
RANK  | <rank>
TITLE | <title>
TRACKED QUANTITY | <one clause, or NONE>
CURRENT VALUE    | <value, or NOT FOUND>
LAST MOVED       | <year, by whom, or NEVER MOVED since <year>>
WHAT MOVES IT    | construction | algorithm | proof technique | computation | N/A
STATUS TODAY     | OPEN | RESOLVED <date, id> | CLOSED IN PRACTICE <date, id> | UNKNOWN
TIER             | PRIMARY | SECONDARY | RECALL
SOURCE           | <citation with a date, or NOT FOUND>
```

## The records


**139 — Torsion Conjecture for Abelian Varieties of Dimension at Least Two**  *(Number theory & arithmetic geometry)*
> For every integer g>=2 and every number field K, there exists a finite constant B(g,K) such that every abelian variety A defined over K of dimension g satisfies #A(K)_tors <= B(g,K). Here A(K)_tors is the subgroup of K-rational torsion points. The bound is uniform over all such A, without dependence…

**140 — Residual Finiteness of Hyperbolic Groups**  *(Algebra, representation & category theory)*
> For every word-hyperbolic group G and every nonidentity element g in G, prove that there is a finite group F and a homomorphism φ:G→F with φ(g)≠1.

**147 — The Generalized Sato-Tate Conjecture for Higher-Dimensional Abelian Varieties**  *(Number theory & arithmetic geometry)*
> Prove that the normalized Frobenius conjugacy classes of an abelian variety A of dimension g over a number field K are equidistributed in the Sato-Tate group ST(A).

**149 — Manins Conjecture on the Asymptotic Density of Rational Points on Fano Varieties**  *(Number theory & arithmetic geometry)*
> Prove that for any smooth Fano variety X over a number field K with ample anticanonical bundle, the number of rational points of anticanonical height <= B on a Zariski open subset satisfies N(U, B) ~ c B (log B)^{rho(X)-1}.

**151 — Leopoldt's conjecture**  *(Number theory & arithmetic geometry)*
> Prove or disprove that for every number field K and every prime p, the Leopoldt defect of K at p is zero, equivalently that the p-adic regulator has the conjectured full rank.

**154 — Cramer Conjecture on the Limsup of Normalized Prime Gaps**  *(Number theory & arithmetic geometry)*
> Prove that lim sup_{n -> infinity} (p_{n+1} - p_n) / (log p_n)^2 = 1, where p_n is the n-th prime.

**170 — Murre's Chow-Kunneth Conjectures**  *(Number theory & arithmetic geometry)*
> For every smooth projective irreducible complex variety X of dimension d, let CH^j(X)_Q denote cycles modulo rational equivalence, with Betti Q-cohomology. A correspondence pi in CH^d(X x X)_Q acts by pi_*(a)=(p_2)_*(p_1^*(a).pi). Murre's full A-D package asserts: (A) there exists a Chow-Kunneth dec…

**173 — Tate's rational leading-term Stark conjecture**  *(Number theory & arithmetic geometry)*
> For every finite Galois extension L/K of number fields with group G, let S be any finite set of places of K containing the archimedean and ramified places. Let X be the augmentation kernel of the free Q-module on places of L above S, U=Q tensor_Z O_(L,S)^*, and f:X->U any Q[G]-isomorphism. Define la…

**175 — Beilinson-Soule Vanishing Conjecture for Rational Motivic Cohomology**  *(Algebra, representation & category theory)*
> Prove that for every smooth scheme X over a field k the rational motivic cohomology groups H^(n,i)(X), defined as the i-th graded piece for the gamma filtration on K_(2i-n)(X) tensored with the rationals, vanish whenever n <= 0 and the pair (n,i) is not (0,0).

**182 — Transcendence of Apery's Constant**  *(Number theory & arithmetic geometry)*
> Prove or disprove that the value zeta(3) is transcendental over the rational numbers.

**192 — Artin's primitive root conjecture**  *(Number theory & arithmetic geometry)*
> Prove or disprove that every integer a other than -1 that is not a perfect square is a primitive root modulo p for a positive natural density of primes p, with the density given by Artin's predicted correction factor.

**200 — Rank One Abelian Stark Conjecture**  *(Number theory & arithmetic geometry)*
> Let K/F be an abelian extension of number fields with Galois group G, and let S be a finite set of places of F containing the archimedean and ramified places, with |S| >= 2 and at least one place v of S splitting completely in K. Prove that, for a fixed place w of K above v, there exists a unit u in…

**203 — Effective Roth Theorem**  *(Number theory & arithmetic geometry)*
> There exists one total computable algorithm which, given a real algebraic irrational alpha by its integer minimal polynomial and a rational isolating interval, and a positive rational epsilon, returns an integer Q>=1 such that every reduced rational p/q, with p an integer and q>=1 an integer, satisf…

**211 — Brauer-Manin obstruction for number-field curves: Hasse-principle form**  *(Number theory & arithmetic geometry)*
> For every number field k and every smooth projective geometrically connected curve C/k of genus at least two, if C(A_k)^Br is nonempty then C(k) is nonempty. Here Br(C)=H^2_et(C,G_m) is the full cohomological Brauer group, and C(A_k)^Br consists of adelic tuples (P_v) for which sum_v inv_v(alpha(P_v…

**216 — Moonshine Uniqueness Conjecture (Strongly Rational Holomorphic VOA Form)**  *(Algebra, representation & category theory)*
> Every strongly rational, holomorphic vertex operator algebra V of central charge 24 with V_1=0 is isomorphic to the moonshine vertex operator algebra V-natural. Here strongly rational means simple, of CFT type (V=sum_{n>=0} V_n and V_0=C1), self-contragredient, C_2-cofinite, and rational in the sens…

**230 — Shafarevich Freeness Conjecture over Qab**  *(Number theory & arithmetic geometry)*
> Let Qab be the maximal abelian extension of Q in an algebraic closure Qbar (equivalently the maximal cyclotomic extension). The absolute Galois group Gal(Qbar/Qab) is a free profinite group of countably infinite rank, in the standard profinite convention of a free basis converging to the identity.

**239 — Existence of an odd perfect number**  *(Number theory & arithmetic geometry)*
> Determine whether there exists an odd positive integer N satisfying sigma(N)=2N, where sigma is the sum-of-positive-divisors function; equivalently, prove that every perfect number is even or construct an odd perfect number.

**252 — Dynamical Mordell–Lang Conjecture**  *(Number theory & arithmetic geometry)*
> For every field K of characteristic zero, every quasiprojective variety X over K, every K-morphism f:X->X, every closed K-subvariety V of X and every point x in X(K), the set {n in Z_{≥0}: f^n(x) is in V(K)} is a finite union of arithmetic progressions {a+bm:m in Z_{≥0}} with a,b nonnegative integer…

**276 — Zagier Conjecture on Dedekind Zeta Values**  *(Number theory & arithmetic geometry)*
> For every number field F of signature (r1,r2) and every integer k>=2, put n=r2 for even k and n=r1+r2 for odd k. There exist xi_1,...,xi_n in A_k(F) tensor Q, using the allowable-symbol group defined by Zagier--Gangl section2, such that zeta_F(k) belongs to Q^times times sqrt(abs(D_F)) pi^{k([F:Q]-n…

**287 — Alperin–McKay Conjecture**  *(Algebra, representation & category theory)*
> For every finite group G, every prime p, every p-block B of G with defect group D, and its Brauer correspondent b in N_G(D), the numbers k_0(B) and k_0(b) of ordinary irreducible complex characters of height zero are equal. For a character chi in a p-block of a finite group H with defect group D, he…

**289 — Montgomery's Large Value Conjecture for Dirichlet Polynomials**  *(Number theory & arithmetic geometry)*
> For every fixed sigma > 1/2 and N <= T <= N^{O(1)}, prove that if D(t) = sum_{N<n<=2N} b_n exp(it log n) has |b_n| <= 1 and W is a 1-separated subset of [0,T] on which |D(t)| > N^sigma, then |W| <= C(sigma) T^{o(1)} N^{2-2sigma}.

**301 — Normality of Pi**  *(Number theory & arithmetic geometry)*
> Prove that pi is a normal number: in every integer base b >= 2, every block of k digits occurs in the base-b expansion of pi with asymptotic frequency b^{-k}.

**313 — Iwasawa mu = 0 Conjecture for Cyclotomic Z_p-Extensions**  *(Number theory & arithmetic geometry)*
> For every number field F and every prime p, prove that the Iwasawa mu-invariant mu(X_infinity) of the unramified Iwasawa module for the cyclotomic Z_p-extension F_infinity/F is zero. The case in which F is abelian over Q is excluded as proved.

**319 — The Atiyah Conjecture on the Integrality of L2-Betti Numbers**  *(Algebra, representation & category theory)*
> Prove that for every finite CW-complex X whose group G = π_1(X) is torsion-free, the L2-Betti numbers of the universal covering of X, i.e. the von Neumann dimensions of its L2-homology, are integers.

**325 — Broues Abelian Defect Group Conjecture**  *(Algebra, representation & category theory)*
> Prove that if B is a p-block of a finite group G with abelian defect group D and b is the Brauer correspondent block in N_G(D), then the bounded derived categories D^b(mod B) and D^b(mod b) are equivalent as triangulated categories.

**348 — Beal's Conjecture (Tijdeman-Zagier Conjecture)**  *(Number theory & arithmetic geometry)*
> Prove that if A^x + B^y = C^z with A, B, C, x, y, z positive integers and x, y, z all greater than 2, then A, B, and C have a common prime factor.

---

When finished, state how many of the 26 records returned `NONE` and how many returned `NOT FOUND`. Those two counts, plus every record you marked RESOLVED or CLOSED IN PRACTICE, are the headline result of this chunk.

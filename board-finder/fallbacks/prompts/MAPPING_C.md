# Mapping layer, chunk C of 4 — Geometry and topology

**LOWER expected yield -- mostly structural conjectures. A high NOT-FOUND rate here is the correct answer, not a failure.**

## What this is for

A 499-record corpus ranks open mathematical problems by editorial importance. It records each
problem in its **headline form** — *"determine the exact value"*, *"prove the conjecture"* — which
is almost always the hopeless form. What a working group can actually move is usually a **tracked
quantity underneath** the headline: a best-known bound, a record construction, a verification
height, a competitive ratio.

The corpus never names that quantity. Your job is to supply it, for 22 records.

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


**120 — Aspherical Manifolds Admit No Metric of Positive Scalar Curvature**  *(Geometry & topology)*
> Prove or disprove that no closed aspherical manifold admits a Riemannian metric of positive scalar curvature.

**133 — Cannon's conjecture**  *(Geometry & topology)*
> Prove or disprove that every Gromov-hyperbolic group whose boundary at infinity is homeomorphic to the two-sphere acts properly discontinuously, cocompactly, and isometrically on hyperbolic three-space, equivalently is virtually a cocompact Kleinian group.

**159 — Smooth Four-Dimensional Schoenflies Problem**  *(Geometry & topology)*
> Determine whether every smooth embedding of S^3 in S^4 is smoothly unknotted; equivalently, whether each of its two complementary closures is diffeomorphic to the standard 4-ball B^4.

**160 — Grothendieck's Variational Hodge Conjecture**  *(Geometry & topology)*
> For every smooth projective morphism f:X->S of smooth connected complex algebraic varieties, every integer p>=0, and every global algebraic horizontal section xi of the relative algebraic de Rham cohomology bundle R^(2p)f_*Omega^._(X/S) for the Gauss-Manin connection, if xi(s0) is the de Rham cycle …

**164 — Weinstein Conjecture on periodic orbits of Reeb flows**  *(Geometry & topology)*
> Prove that every closed contact manifold admits a periodic orbit of the Reeb flow of any contact form, in all dimensions.

**166 — Arnold Conjecture on Hamiltonian Fixed Points**  *(Geometry & topology)*
> Prove that every Hamiltonian diffeomorphism of an arbitrary closed connected symplectic manifold has at least Crit(M) fixed points, where Crit(M) is the minimum number of critical points of a smooth function on M.

**189 — Nonvanishing conjecture for projective log canonical pairs**  *(Geometry & topology)*
> Let (X, Delta) be a projective log canonical pair over the complex numbers, with Delta a Q-divisor and K_X+Delta Q-Cartier. If K_X+Delta is pseudo-effective, prove that kappa(K_X+Delta) >= 0; equivalently, some sufficiently divisible positive multiple of K_X+Delta is linearly equivalent to an effect…

**244 — K(pi,1) conjecture for Artin groups**  *(Geometry & topology)*
> For every Coxeter system (W,S) with S finite and arbitrary Coxeter labels, let A_(W,S) be the associated Artin group and X_(W,S) its quotient Salvetti CW complex, with one |T|-cell for each T subset of S whose parabolic group W_T is finite and the standard attaching maps in Paolini Theorem 3.3 or Bo…

**250 — All groups are good: the four-dimensional disc-embedding conjecture**  *(Geometry & topology)*
> Every group Gamma is good in the four-dimensional disc-embedding sense: for every based height1.5 disc-like capped grope G^c (with its standard smooth four-dimensional thickening and framed attaching region) and every homomorphism phi:pi_1(G^c)->Gamma, there exists an immersed disc D->G^c whose fram…

**251 — Shafarevich Holomorphic-Convexity Conjecture**  *(Geometry & topology)*
> For every connected smooth complex projective variety X, its universal covering complex manifold X-tilde is holomorphically convex: for every compact K contained in X-tilde, the set {z in X-tilde: |f(z)|<=sup_{w in K}|f(w)| for every global holomorphic function f on X-tilde} is compact. This is the …

**254 — Morrison-Kawamata Cone Conjecture**  *(Geometry & topology)*
> For every projective Q-factorial klt pair (X, Delta) over the complex numbers with K_X + Delta numerically trivial, prove both that Aut(X, Delta) acting on the effective nef cone Nef^e(X) and that PsAut(X, Delta) acting on the effective movable cone Mov^e(X) have rational polyhedral fundamental doma…

**256 — Michel Boundary Rigidity Conjecture for Simple Manifolds**  *(Geometry & topology)*
> Let M be a compact smooth manifold with nonempty boundary of dimension n>=3, and g,g' smooth simple Riemannian metrics: the boundary is strictly convex, every two points are joined by a unique geodesic, and there are no conjugate points. Assert that whenever d_g(x,y)=d_g'(x,y) for all boundary point…

**272 — Kuznetsov Rationality Conjecture for Cubic Fourfolds**  *(Geometry & topology)*
> For every smooth cubic fourfold X contained in P^5_C, let Ku(X) be the full right-orthogonal subcategory of D^b(coh X) consisting of objects E with Hom(O_X(i),E[j])=0 for i=0,1,2 and all integers j. The Kuznetsov rationality conjecture asserts: X is rational, meaning birational over C to P^4_C, if a…

**288 — Complex linearity of closed-surface mapping class groups by genus**  *(Geometry & topology)*
> For every integer g >= 3, let S_g be the closed connected orientable surface of genus g and Mod(S_g) its group of isotopy classes of orientation-preserving homeomorphisms. Determine exactly the set of such genera g for which there exist an integer n >= 1 and an injective homomorphism Mod(S_g) -> GL_…

**297 — Hartshorne Conjecture on complete intersections in codimension two**  *(Geometry & topology)*
> Prove that for every integer N >= 7, every smooth codimension-two subvariety X of complex projective space P^N is the scheme-theoretic intersection of two hypersurfaces.

**298 — Vassiliev Separation by Abelian-Valued Finite-Type Invariants**  *(Geometry & topology)*
> For every pair of non-isotopic smooth closed oriented unframed knots K_1,K_2 in S^3, assert that there exist an abelian group A, a nonnegative integer d and an A-valued Vassiliev invariant v of order at most d with v(K_1) != v(K_2). Knots are taken up to ambient isotopy respecting their orientation,…

**299 — Slice-Ribbon Conjecture**  *(Geometry & topology)*
> Is every smoothly slice knot in S^3 (one that bounds a smoothly embedded disk in the 4-ball) a ribbon knot (one bounding an immersed disk in S^3 with only ribbon singularities)?

**330 — Original Dubrovin conjecture for Fano manifolds**  *(Geometry & topology)*
> For every smooth projective complex Fano manifold F, prove the original Dubrovin conjecture in the form recalled in Galkin-Golyshev-Iritani Section 4.6: (1) the (big) quantum cohomology of F is generically semisimple if and only if the bounded derived category D^b_coh(F) admits a full exceptional co…

**335 — Jones Unknot Conjecture**  *(Geometry & topology)*
> Prove or disprove: a knot K in S^3 has Jones polynomial V_K = 1 if and only if K is the unknot (equivalently, every nontrivial knot has nontrivial Jones polynomial).

**339 — Polynomial-time unknot recognition**  *(Geometry & topology)*
> Determine whether there is a polynomial-time algorithm that, given a knot diagram or an equivalent finite encoding of a knot in three-space, decides whether the knot is the unknot.

**342 — Arnold Chord Conjecture in Higher Dimensions**  *(Geometry & topology)*
> Prove that for every closed co-oriented contact manifold (Y, xi) of dimension 2n+1 with n >= 2, every contact form alpha for xi, and every closed Legendrian submanifold Lambda of Y, there exists a Reeb chord of Lambda: a non-constant trajectory of the Reeb vector field of alpha starting and ending o…

**343 — Bott Conjecture: nonnegatively curved simply connected manifolds are rationally elliptic**  *(Geometry & topology)*
> Prove that every compact simply connected manifold M admitting a metric of nonnegative sectional curvature is rationally elliptic, i.e., the Betti numbers of its loop space grow at most polynomially for every field of coefficients.

---

When finished, state how many of the 22 records returned `NONE` and how many returned `NOT FOUND`. Those two counts, plus every record you marked RESOLVED or CLOSED IN PRACTICE, are the headline result of this chunk.

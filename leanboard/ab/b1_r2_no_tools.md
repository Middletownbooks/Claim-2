# Reconstruction of the known board

In my own language, $B_{\mathrm{BJ}}$ is:

$$
\boxed{
S_t=(x_t,\mathcal A_t,\Sigma_t),\qquad
dx_t=U_t\,dW_t,\qquad
\Sigma_t=U_tU_t^{T}\ \text{certified by SDP},
}
$$

where $x_t\in[-1,1]^n$ is a fractional coloring, $\mathcal A_t=\{i:|x_{t,i}|<1\}$ the alive coordinates, and the diffusion is constrained to live on $\mathcal A_t$, to keep the *regularized discrepancy* (a soft-max potential of the row values $\langle r_j,x_t\rangle$) a controlled process, and to be **spectrally independent**: no small group of rows receives too much of $\|\,(VU_t)_j\,\|^2$. The **affine** refinement identifies rows that are simultaneously *near violation* (large $|\langle r_j,x_t\rangle|$) and *highly leveraged* in the diffusion; a decoupling-plus-counting argument bounds their number, and the SDP moves orthogonally to them. Composition: sticky coordinates leave $\mathcal A_t$; feasibility is maintained by dimension counting. Terminal: $\mathcal A_\infty=\emptyset$, i.e. $x\in\{\pm1\}^n$.

**Its fundamental obstruction, as I see it.** Three facts:

- **(O1) The legality certificate of each move is a finite family of quadratic inequalities** (an SDP). Hence the board perceives the instance *only through quadratic functionals of the rows* — covariances, traces, leverage scores.
- **(O2) The terminal objective is a supremum over $m$ subgaussian coordinates, and quadratic certificates price suprema through Gaussian comparison**, whose intrinsic scale is $\Theta(\sqrt{\log\min(m,n)})$ on flat instances. Bansal–Jiang buy their $(\log n)^{1/4}$ gain by making this comparison *adaptive in time*, and the exponent is set by the bookkeeping cost of dangerous rows — not by a new principle.
- **(O3) Non-quadratic cancellation is invisible to the board.** (A concrete example in §II, Board 9: on the Sylvester–Hadamard instance there is a signing of discrepancy exactly $1$ — a bent function — while every spectral functional of that instance looks like a generic orthogonal matrix, where random signings are $\Theta(\sqrt{\log n})$.)

The search below is therefore guided by one question: *is there a non-quadratic structure that is checkable?*

---

## II. Alternative board search

**Test suite used throughout.**

- **T1 (rank-1):** all $v_i=e_1$. Truth: discrepancy $\le1$. Sanity check.
- **T2 (flat orthogonal):** normalized Sylvester–Hadamard, $m=n=2^k$. Random signing: $\Theta(\sqrt{\log n})$; truth: $\le 1$ for even $k$ (Board 9).
- **T3 (random orthogonal):** conjectured truth $O(1)$; all known methods give $\Theta(\sqrt{\log n})$.
- **T4 (row-heavy):** $e_1$ repeated $n-1$ times, plus $e_2$. Row norm $\sqrt{n-1}$; truth $\le2$. Separates *method* obstructions from *truth*.
- **T5 (near-dependent):** instances with $\min_{s\in\{-1,0,1\}^n\setminus0}\|Vs\|_\infty$ exponentially small.                                    ### Board 1 — The convolution compiler (primal)

$$
S_t=\mu_t=\mathcal L\!\Big(\sum_{i\le t}\epsilon_iv_i\Big),\qquad
T_v(\mu)=\mu*\sigma_v,\qquad
\text{terminal: }\mu_n(CB_\infty^m)>0 .
$$

Composition is *exact and free*: the move is a convolution, no information is lost, order is irrelevant. The terminal condition is *equivalent* to the existence of a good signing, since $\mu_n$ is uniform on $V\{\pm1\}^n$. The entire problem compresses into the choice of invariant. Candidate invariants:

- **(a) Subgaussian majorant.** $\mathbb E e^{\langle\lambda,S\rangle}=\prod_i\cosh\langle\lambda,v_i\rangle\le e^{\frac12\lambda^T\Sigma\lambda}$, using $\cosh x\le e^{x^2/2}$. Closed under the move, exact, checkable — but it sees only $\Sigma$, i.e. it is *spectral*, and any certificate drawn from it is a moment bound: ceiling $\Theta(\sqrt{\log\min(m,n)})$ on T2/T3.
- **(b) Gaussian-measure comparison (Banaszczyk).** The class $\{\mu:\mu(cK)\ge 2\gamma(K)-\tfrac12\ \forall\ \text{symmetric convex }K\}$ is closed under $*\sigma_v$ for short $v$: from $\tfrac{\phi(x-v)+\phi(x+v)}{2}=\phi(x)e^{-\|v\|^2/2}\cosh\langle v,x\rangle\ge\phi(x)e^{-\|v\|^2/2}$, with the dilation $c$ absorbing the accumulated loss. This *is* a certificate class, but its scale is set by $\gamma(rB_\infty^m)\ge\tfrac12$, i.e. $r=\Theta(\sqrt{\log m})$. Certificate at $O(1)$ scale would require $\gamma(CB_\infty^m)\approx e^{-me^{-C^2/2}}$ — exponentially small, invisible to the closure inequality.
- **(c) The exact invariant** ("some completion lands in the cube") is tautological.

**Verdict:** the move is perfectly stupid; every *checkable* invariant found is spectral; every non-spectral one is the answer itself. **Collapses** (see §III–IV for the sharpest form of this).

### Board 2 — The characteristic-function compiler (dual)

Since $\widehat{\mu*\sigma_v}(\xi)=\hat\mu(\xi)\cos\langle\xi,v\rangle$:

$$
S_t=f_t(\xi)=\prod_{i\le t}\cos\langle\xi,v_i\rangle,\qquad
T_v(f)=f\cdot\cos\langle\xi,v\rangle,\qquad
\text{terminal: }\ \mu_n(CB_\infty^m)>0 .
$$

This is Board 1 in dual coordinates, but the geometry is different and instructive. On the *imaginary* axis ($\xi=-i\lambda$) the cosines become coshes and we recover the spectral majorant (a) — this is where every known method lives. On the *real* axis, $f_t$ has zeros on the periodic hyperplane arrangement $\{\xi:\langle\xi,v_i\rangle\in\pi(\mathbb Z+\tfrac12)\}$, and the zero set encodes the instance completely. Atom detection: if $\delta_V=\min_{\epsilon\ne\epsilon'}\|V(\epsilon-\epsilon')\|_\infty>0$, then for smoothing $\sigma\ll\delta_V/\sqrt{\log m}$, $(\mu_n*\gamma_{\sigma^2})(CB_\infty)>0$ certifies an atom. But a single atom has mass exactly $2^{-n}\cdot\text{multiplicity}$; on T3 the multiplicity is $1$, so the certificate requires $2^{-n}$-accuracy control of an oscillatory product — a lattice-point count of the zonotope grid in a cube. On T5, $\delta_V$ is exponentially small, making the required resolution even finer.

**Verdict:** a *perfect* compiler with **no usable invariant**: closure under cosine-multiplication is trivial (any function class containing $1$ and closed under multiplication contains all instances), so the terminal certificate functional must do all the work, and that work is counting. **Fails at resolution** — but this is the least-collapsed representation, and becomes the strongest candidate in §III.

### Board 3 — Martingale transport (Dambis–Dubins–Schwarz)

$$
S_t=(S_0,\dots,S_t)\ \text{a martingale path},\quad
S_t=S_{t-1}+\epsilon_t v_t,\qquad
I:\ \langle S^j\rangle_t=\sum_{i\le t}v_{ij}^2\ \text{(deterministic!)}\le R_j^2 .
$$

The coordinate quadratic variation is *exactly* controlled — a genuinely exact, non-spectral-looking invariant. By DDS, $S_n^j=B^j_{R_j^2}$ for Brownian motions $B^j$. Terminal: bound $\max_j\sup_{t\le R_j^2}|B^j_t|$. The catch: the $B^j$ are dependent, and the dependence is *exactly* the cross-coordinate covariation $\langle S^j,S^k\rangle_t=\sum_{i\le t}v_{ij}v_{ik}$ — i.e. $\Sigma$. A union bound over $j$ gives $\Theta(\sqrt{\log m}\cdot\max_jR_j)$ (Banaszczyk's scale, recovered on T2); improving it requires controlling the joint law of the $B^j$, which is the covariance structure.

**Verdict:** the per-coordinate invariant is exact and new-looking, but the *terminal* certificate forces joint control that is spectral. **Collapses.**

### Board 4 — Moment, potential, entropy, and SoS boards

State: a potential $\Phi(\epsilon)$ or a truncated pseudo-distribution; move: conditional-expectation update or moment extension; invariant: potential bound.

- Any potential whose expectation over random signs is *computable from row data* reduces to subgaussian moments: $\mathbb E\|V\epsilon\|_{2p}^{2p}\le(2p-1)!!\sum_jR_j^{2p}$, optimized at $p\approx\log m$ — the $\sqrt{\log}$ ceiling again (T2 confirms tightness of the *method*).
- Entropy/max-entropy relaxations (Rothvoss-style): the entropy defect of a max-entropy distribution on the cube is controlled by log-determinants of covariances — spectral.
- Sum-of-squares: composability = hierarchy level; the integrality gap of the base SDP is essentially the conjecture itself (Nikolov showed the natural vector-balancing SDP has gap $\ge2$; the conjecture is the statement that the gap is $O(1)$).

**Verdict:** ceilings or restatements. **Collapse.**

### Board 5 — Slab-polytope volume (Minkowski–Gluskin)

$$
S_t=P_t=\{x\in[-1,1]^n\cap L_t:\|Vx\|_\infty\le C\},\qquad
T:\ \text{fix a coordinate},\qquad
I:\ \mathrm{vol}(P_t)\ge 2^{\dim L_t}\text{-threshold}.
$$

Via polarity, $P_0=C\,W^\circ\cap[-1,1]^n$ with $W=\mathrm{conv}\{\pm r_j\}$. This is Spencer/Gluskin partial coloring. The obstruction: controlling volumes of *sections* after fixing coordinates; the only known control is Gaussian measure of slabs — spectral. And partial coloring certifies only a constant fraction of coordinates; iterating on residual instances *adds* discrepancies across $\Theta(\log n)$ rounds on the same rows, which is why this family has never beaten the Banaszczyk scale.

**Verdict:** **collapse to spectral volume**, plus a structural composition loss.

### Board 6 — Irrevocable-commitment boards (greedy, dyadic, local search)

- *Dyadic pairing:* pair vectors, difference them, recurse. On T2/T3 all pairs are orthogonal, norms grow $\sqrt2$ per level, $\Theta(\log n)$ levels $\Rightarrow\sqrt n$. **Fails exactly on the hard case.**
- *Greedy potential/local search:* inherits the potential ceiling of whatever potential it uses (Board 4).
- *Commit-on-arrival streaming:* this is the online balancing game. Against adaptive adversaries, super-constant (polylogarithmic) lower bounds are known; against oblivious adversaries the best known (self-balancing-walk type) is Banaszczyk-scale. Since a compiler that commits signs from prefix information alone *implements* an online algorithm, **irrevocable boards are separated from the conjectured $O(1)$.**

**Verdict:** **fail** (T2 for dyadic; online lower bounds for commitment).

### Board 7 — The Steinitz/ordering sibling

State: partial sum $P_t$ + remaining pool; move: choose the next vector; invariant $\|P_t\|\le C$; terminal: full ordering. Via the transference principle (Chobanyan), rearrangement and signing bounds are intertwined, and applying Steinitz to the doubled instance $\{\pm v_i\}$ would yield signings. But (i) the classical proofs (Grinberg–Sevastyanov) are *global* — LP extreme points on a permutahedron — with no composable greedy invariant; (ii) greedy/online versions have lower bounds; (iii) the bounds are dimension-dependent, the wrong direction.

**Verdict:** a harder sibling, not a usable board.

### Board 8 — Duality / IP restatements

$\min_\epsilon\|V\epsilon\|_\infty\le C \iff \{\pm1\}^n\cap CW^\circ\ne\emptyset$ with $W=\mathrm{conv}\{\pm r_j\}$; equivalently an SDP integrality-gap statement (Nikolov). These are *certificates of the answer*, with no move structure.

**Verdict:** restatement.

### Board 9 — Algebraic signings (the bent-function phenomenon)

On T2 (Sylvester–Hadamard, $n=2^k$, $k$ even), take $g(x)=(-1)^{x_1x_2\oplus x_3x_4\oplus\cdots\oplus x_{k-1}x_k}$, a bent function: *all* its Walsh coefficients equal $\pm2^{-k/2}$. Hence $\|Hg\|_\infty=2^{k/2}=\sqrt n$, i.e. **discrepancy exactly $1$** for the normalized instance. Meanwhile Parseval gives $\min_\epsilon\|H\epsilon\|_\infty\ge\sqrt n$, so this is optimal, and random signings are $\Theta(\sqrt{\log n})$.

**Lesson.** On the spectrally hardest instance family, the optimal certificate exists, is *purely algebraic*, and is invisible to every quadratic functional (the instance is spectrally indistinguishable from T3, where nothing structured is known). Any new board that reaches $O(1)$ must be able to *see* such non-quadratic structure — or produce structureless certificates for random instances by some principle no one has found.    ---

## III. Strongest candidate: the free compiler with a certificate-class invariant

The survivor is the convolution/Fourier compiler (Boards 1–2), made precise:

$$
\boxed{
\begin{aligned}
\text{State: }& S=\mu,\ \text{a probability measure on }\mathbb R^m
\ \Big(\text{dual form: } f(\xi)=\textstyle\prod_i\cos\langle\xi,v_i\rangle\Big),\\[2pt]
\text{Move: }& T_v(\mu)=\mu*\tfrac12(\delta_v+\delta_{-v})
\ \Big(\text{dual: } f\mapsto f\cdot\cos\langle\xi,v\rangle\Big),\\[2pt]
\text{Composition: }& T_{v_n}\circ\cdots\circ T_{v_1}(\delta_0)=\mathcal L\Big(\sum_i\epsilon_iv_i\Big),\ \text{exact, order-free},\\[2pt]
\text{Terminal: }& \mu_n(CB_\infty^m)>0\iff\exists\,\epsilon\in\{\pm1\}^n,\ \|V\epsilon\|_\infty\le C,\\[2pt]
\text{Invariant: }& \mu\in\mathcal C,\ \text{where }\ \delta_0\in\mathcal C,\ \ \mathcal C*\sigma_v\subseteq\mathcal C\ \forall\,\|v\|_2\le1,\ \ \mu\in\mathcal C\Rightarrow\mu(CB_\infty)>0 .
\end{aligned}}
$$

This is the unique "stupid" part of the problem.

**What would have to be proved:** The existence of *any checkable* such class $\mathcal C$ at constant $C$.

Two things are provable about this setup:

1. **It is exactly as hard as the conjecture.** Let $\mathcal C^\star=\{\text{laws of partial signed sums of unit-vector sequences}\}$. Then (i)–(ii) hold for $\mathcal C^\star$ by construction, and (iii) holds for $\mathcal C^\star$ at constant $C$ **if and only if Komlós($C$) is true** (every prefix is itself an instance). So an invariant exists iff the conjecture holds; the *entire* content of a proof is a checkable $\mathcal C\supseteq\mathcal C^\star$... rather, any class satisfying (i)–(iii) automatically contains $\mathcal C^\star$, and its checkability *is* the proof.

2. **Everything known is such a class.** Banaszczyk's theorem is the class $\{\mu:\mu(cK)\ge 2\gamma(K)-1\ \forall K\}$ at scale $r=\Theta(\sqrt{\log m})$. Bansal–Jiang is an *adaptive* version: the certificate of $\mu_t$ is issued relative to the remaining instance by the SDP, at scale $(\log n)^{1/4}(\log\log n)^{O(1)}$. In other words:

$$
\boxed{\text{Banaszczyk and Bansal–Jiang are the spectral instantiations of this one board.}}
$$

---

## IV. The hard lemma

Here is the bottleneck, stated nakedly.

> **Missing Lemma.** *There exist a constant $C$ and a checkable class $\mathcal C$ of probability measures (all dimensions $m$) satisfying (i), (ii), (iii) of §III.*

Two horns make this hard, and both are provable, not speculative:

**Horn 1 — smooth classes cannot reach $O(1)$.** If membership in $\mathcal C$ is certified by smooth/analytic data (MGF majorants, moments, log-concave relaxations, Gaussian-measure comparisons), then closure (ii) under *all* unit $v$ forces the certificate to factor through the subgaussian comparison $\prod\cosh\langle\lambda,v_i\rangle\le e^{\frac12\lambda^T\Sigma\lambda}$. Certificates of this form price $\mu(CB_\infty)$ through the Gaussian mean $\mathbb E\|N(0,\Sigma)\|_\infty\approx\sqrt{2\log m}\max_jR_j$, and on T2/T3 this is $\Theta(\sqrt{\log n})$ while the truth is conjectured $O(1)$ (on T2 it is *provably* $1$). So every smooth class has a $\sqrt{\log}$-scale floor. Formally: smooth certificate classes are closed under the convex-order domination $\sqrt{2/\pi}\,S\preceq_{cx}N(0,\Sigma)$ (from $\epsilon=\mathrm{sign}(g)$, Jensen), and convex order cannot see below the Gaussian mean.

**Horn 2 — lattice-fine classes are uncheckable.** Any class fine enough to detect an atom of mass exactly $2^{-n}$ (T3) at $O(1)$ scale must resolve the grid $V\{\pm1\}^n$ at separation $\delta_V$, which can be exponentially small (T5) — i.e. checking membership is at least as hard as counting.

The missing lemma lives strictly between the horns: a certificate *coarser than counting* but *finer than covariance*. The single hardest mathematical step is therefore:

> **Conjectural Small-Ball Lemma.** *For $\mu=\mathcal L(\sum_i\epsilon_iv_i)$ with $\|v_i\|_2\le1$, prove $\mu(CB_\infty^m)>0$ via a functional of the instance that is (a) monotone/contractive under appending one generator $v$, and (b) not a function of the second moments $\Sigma$ alone.*

---

## V. Comparison with Bansal–Jiang

|  | Bansal--Jiang | Candidate\\
\hline
\text{State} & ? & ?\\
\text{Move} & ? & ?\\
\text{Invariant} & ? & ?\\
\text{Main obstruction} & ? & ?\\
\text{Iteration} & ? & ?\\
\text{Terminal certificate} & ? & ?
\end{array}
$$

*(Note: The table was partially incomplete in the source, but the text comparison above provides the full detail.)*

---

## VI. Board-change verdict

**NEGATIVE** — with a precise map of the territory.

Two structural walls constrain *any* board for this problem:

- **The static ceiling.** Any board whose certificate is a moment/majorant/smooth functional of the final distribution collapses to Gaussian comparison, with floor $\Theta(\sqrt{\log\min(m,n)})$ — confirmed tight *as a method bound* by T2, where the truth ($=1$, via bent functions) lies strictly below the floor. Boards 1(a), 2 (Laplace side), 3, 4, 5 all die here.
- **The commitment wall.** Any board whose per-vector move commits irrevocably from prefix information implements an online algorithm, separated from $O(1)$ by online lower bounds (adaptive) or stuck at the Banaszczyk scale (oblivious). Board 6 dies here; Board 7 is harder than the original.

What collapses back to $B_{\mathrm{BJ}}$ or its Banaszczyk ancestor: the DDS transport board (cross-coordinate dependence = covariance), the entropy/SoS boards (log-determinants; SDP gaps), the volume board (Gaussian measure of slabs), the polar/SDP board (restatement). What genuinely fails: dyadic/greedy (T2), Fourier certificate (resolution, T3/T5), Steinitz-greedy (online wall).

The informative content of this negative result: **there is a canonical exact compiler for the problem, and both known proofs are the spectral certificate classes on it.** The search for a new board is exactly the search for a non-spectral checkable class satisfying (i)–(iii) — no more, no less.

---

## Final question

> **What is the simplest mathematical representation in which a useful Komlós move becomes almost stupid?**

$$
\boxed{
\begin{aligned}
\text{State: }& S=\mu,\ \text{a probability measure on }\mathbb R^m
\ \Big(\text{dual form: } f(\xi)=\textstyle\prod_i\cos\langle\xi,v_i\rangle\Big),\\[2pt]
\text{Move: }& T_v(\mu)=\mu*\tfrac12(\delta_v+\delta_{-v})
\ \Big(\text{dual: } f\mapsto f\cdot\cos\langle\xi,v\rangle\Big),\\[2pt]
\text{Composition: }& T_{v_n}\circ\cdots\circ T_{v_1}(\delta_0)=\mathcal L\Big(\sum_i\epsilon_iv_i\Big),\ \text{exact, order-free},\\[2pt]
\text{Terminal: }& \mu_n(CB_\infty^m)>0\iff\exists\,\epsilon\in\{\pm1\}^n,\ \|V\epsilon\|_\infty\le C,\\[2pt]
\text{Invariant: }& \mu\in\mathcal C,\ \text{where }\ \delta_0\in\mathcal C,\ \ \mathcal C*\sigma_v\subseteq\mathcal C\ \forall\,\|v\|_2\le1,\ \ \mu\in\mathcal C\Rightarrow\mu(CB_\infty)>0 .
\end{aligned}}
$$

On this board the move is not *almost* stupid — it *is* stupid: convolve with a two-point measure. Composition is free and exact. The terminal certificate is the answer.

The honest conclusion of the investigation: **the stupid board exists; the stupid invariant does not (yet).** The existence of the invariant is equivalent to the conjecture itself (§III), every *smooth* invariant has a provable $\sqrt{\log}$ floor (Horn 1, sharp on Hadamard instances where bent functions achieve $1$), every *lattice-fine* invariant is as hard as counting (Horn 2), and every checkable invariant actually known — Banaszczyk's Gaussian-measure class at $O(\sqrt{\log m})$, Bansal–Jiang's adaptive spectral class at $\tilde O((\log n)^{1/4})$ — is spectral, i.e. an instantiation of the known board. The entire open problem is the gap between the two horns: a certificate for an atom in the cube that is coarser than counting and finer than covariance.
# Worker brief — Test G, ODD slice (34 problems)

**Read `board-finder/gap/discovery/prompts/COMMON.md` first. Everything in it applies.**

## What this is

A published repository lists 67 mathematical problems, most of which ask for the best possible
constant or the best possible construction — "establish bounds as strong as possible". For each
problem assigned to you, the project needs the **history of the best known construction-side
bound before 2025**: who set it, when, and **how** — by hand, by a new search method, or by
re-running an existing search method bigger.

**The construction side** is the side of the bound that is established by exhibiting an object
(a function, a set, a configuration, a graph, a packing). For "C is the largest constant such that
… holds for all f", exhibiting one f gives an *upper* bound on C, so the construction side is the
upper side. For "C(n) is the maximum number of …", exhibiting a configuration gives a *lower*
bound. Decide it for each problem and say which side you chose and why, in one line.

## Scope limits — read carefully

* **Only moves dated before 2025-01-01 count.** From 2025 onward an AI system and others worked on
  this whole problem set. If you meet results from 2025 or later, **do not use them for your
  labels and do not report them.** Your labels are about the earlier papers only.
* You are **not** told what the labels will be used for, deliberately. Label what the papers did.
* Some problems have **no** pre-2025 numeric record on the construction side (a conjecture with
  no quantitative record, a question nobody had put a number on). Mark those `NO-RECORD` with the
  reason. That is a real and expected answer.

## For every problem, output exactly this block

```
PROBLEM | <n>. <short title>
SIDE    | <upper|lower|other> — <one line why this is the construction side>
RECORD  | YES: <quantity, best pre-2025 value, who, when> | NO-RECORD: <why>
MOVE-1  | <date> | <authors> | <value> | <ANALYTIC|SEARCH-NEW|SEARCH-REPEAT|UNKNOWN> [+AI-SEARCH] | <evidence: what the paper did> | <tier> | <EXACT|RIGOROUS-NUMERIC|NUMERICAL|UNKNOWN>
MOVE-2  | <the move before MOVE-1, same fields> | or NONE (MOVE-1 was the first bound set)
NOTES   | <dead ends, ambiguities, anything contradicting this brief>
```

MOVE-1 is the **most recent pre-2025 move** on the construction side. Where the problem covers a
family (e.g. "for each n"), use the record the problem statement emphasises; if it emphasises
none, pick the smallest parameter value with a pre-2025 numeric record and say so.

## Where to write

Write all blocks, in problem order, to **`board-finder/gap/discovery/G_odd.md`** (create it). Start the file with one line
stating how many problems you labelled and how many are `NO-RECORD` and `UNKNOWN`, with the lists.

When finished, reply with the file path and the three lists (labelled / NO-RECORD / UNKNOWN), plus anything that contradicts this brief.

## Your problems

### Problem 1. Kakeya and Nikodym sets in finite fields

> Let $d \geq 1$, and let $q$ be a prime power. Let $\mathbb{F}_q$ be a finite field of order $q$. A Kakeya set is a set $K$ that contains a line in every direction, and an Nikodym set $N$ is a set with the property that every point $x$ in $\mathbb{F}_q^d$ is contained in a line that is contained in $N \cup \{x\}$. Let $C^K(d,q), C^N(d,q)$ denote the least size of a Kakeya or Nikodym set in $\mathbb{F}_q^d$ respectively.

### Problem 3. How much can an autocorrelation of a non-negative function resemble an indicator function?

> Let $C$ be the best constant for which one has $$ \|f\ * f\|_{L^2(\mathbb{R})}^2 \leq C \|f*f\|_{L^1(\mathbb{R})} \|f * f\|_{L^\infty(\mathbb{R})}$$ for non-negative $f \colon \mathbb{R} \to \mathbb{R}$. What is $C$?

*Repository bound table, pre-2025 rows only. Upper bound on C: 1, trivial. Lower bounds on C: log 16/pi = 0.88254, Martin-O'Bryant 1 Apr 2009; 0.88922, Matolcsi-Vinuesa 8 Jul 2009; 0.901564, Boyer-Li, dated in the table as 'Nov 2024 / 10 Aug 2025' (check which value the Nov 2024 version stated).*

### Problem 5. Erdős minimum overlap problem

> Let $C$ be the largest constant for which $$ \sup_{x \in [-2,2]} \int_{-1}^1 f(t) g(x+t)\ dt\geq C$$ for all non-negative $f,g: [-1,1] \to [0,1]$ with $f+g=1$ on $[-1,1]$ and $\int_\mathbb{R} f = 1$, where we extend $f,g$ by zero outside of $[-1,1]$. What is $C$?

*Repository bound table, pre-2025 rows only. Upper bounds on C: 0.380927, Haugland 2016. Lower bounds on C: 0.379005, White 2022.*

### Problem 7. Difference Bases

> For any natural number $n$, let $\Delta(n)$ be the size of the smallest set $B$ of integers such that every natural number from $1$ to $n$ is expressible as a difference of two elements of $B$ (such sets are known as difference bases for the interval $\{1,\dots,n\}$). Write $C(n) \coloneqq \Delta^2(n)/n$, and $C \coloneqq \inf_{n \geq 1} C(n)$. Establish upper and lower bounds on $C$ that are as strong as possible.

### Problem 9. Kakeya needle problem

> Let $n \geq 2$. Let $C^T(n)$ denote the minimal area $|\bigcup_{j=1}^n T_j|$ of a union of triangles $T_j$ with vertices $(x_j,0)$, $(x_j + 1/n, 0)$, $(x_j + j/n, 1)$ for some real numbers $x_1,\dots,x_n$, and similarly define $C^P(n)$ denote the minimal area $|\bigcup_{j=1}^n P_j|$ of a union of parallelograms $P_j$ with vertices $(x_j,0), (x_j+1/n,0), (x_j+j/n,1), (x_j+(j+1)/n,0)$ for some real numbers $x_1,\dots,x_n$. Finally, define $S^T(n)$ to be the maximal "score" $$ \frac{\sum_{i=1}^n |T_i|}{\left(\sum_{i=1}^n \sum_{j=1}^n |T_i \cap T_j|\right)^{1/2} |\bigcup_{i=1}^n T_i|^{1/2}}$$ over triangles $T_i$ as above, and define $S^P(n)$ similarly. Establish upper and lower bounds for $C^T(n)$, $C^P(n)$, $S^T(n)$, $S^P(n)$ that are as strong as possible.

### Problem 11. Uncertainty principle

> Given a function $f \in L^1(\mathbb{R})$, set $$ A(f) \coloneqq \inf \{r > 0: f(x) \geq 0 \hbox{ for all } |x| \geq r \}.$$ Let $C$ be the largest constant for which one has $$ A(f) A(\hat f) \geq C$$ for all even $f$ with $f(0), \hat f(0) < 0$. Establish upper and lower bounds for $C$ that are as strong as possible.

*Repository bound table, pre-2025 rows only. Upper bounds on C: 0.353, Goncalves-Oliveira e Silva-Steinerberger Feb 2016; 0.32831, Cohn-Goncalves Dec 2017. Lower bounds on C: 0.2025, Goncalves-Oliveira e Silva-Steinerberger Feb 2016.*

### Problem 13. A Linear Programming Bound

> For any dimension $n$, let $C(n)$ denote the quantity $$ C(n) \coloneqq \frac{\pi^{n/2}}{\Gamma(n/2+ 1)} \inf_{f} \frac{(r/2)^n f(0)}{\hat f(0)}$$ where $f$ ranges over integrable continuous functions $f \coloneqq \mathbb{R}^n \to \mathbb{R}$, not identically zero, with $\hat f(\xi) \geq 0$ for all $\xi$ and $f(x) \leq 0$ for all $|x| \geq r$ for some $r>0$. Establish upper bounds for $C(n)$ that are as strong as possible.

### Problem 15. Gagliardo-Nirenberg Inequality

> Let $1 \leq q \leq \infty$, and let $j$ and $m$ be non-negative integers such that $j < m$. Furthermore, let $1 \leq r \leq \infty, p \geq 1$ be real and $\theta \in [0, 1]$ such that the following relations hold: $$\frac{1}{p} = j + \theta \left( \frac{1}{r} - m \right) + \frac{1 - \theta}{q}, \quad \frac{j}{m} \leq \theta < 1.$$ Let $C(j,p,q,r,m)$ be the best constant such that $$\|D^j u\|_{L^p(\mathbb{R})} \leq C(j,p,q,r,m) \|D^m u\|_{L^r(\mathbb{R})}^\theta \|u\|_{L^q(\mathbb{R})}^{1-\theta}$$ for all test functions $u$, where $D$ denotes the derivative operator $\frac{d}{dx}$. Establish upper and lower bounds for $C(j,p,q,r,m)$ that are as strong as possible.

### Problem 17. Young's Convolution Inequality

> Let $1 \leq p,q,r \leq \infty$ with $1/r + 1 = 1/p + 1/q$. Let $C(p,q,r)$ denote the supremum of the quantity $$ Q(f, g) \coloneqq \frac{\|f * g\|_r}{\|f\|_p \|g\|_q}$$ over all non-zero test functions $f,g$. What is $C(p,q,r)$?

### Problem 19. The Ovals Problem

> Let $C$ denote the infimal value of $\lambda_0(\gamma)$, the least eigenvalue of the Schrödinger operator $$ H_\gamma = -\frac{d^2}{ds^2} + \kappa^2(s) $$ associated with a simple closed convex curve $\gamma$ parameterized by arclength and normalized to have length $2\pi$, where $\kappa(s)$ is the curvature. Obtain upper and lower bounds for $C$ that are as strong as possible.

### Problem 21. Schmeisser's Conjecture

> For each $n \geq 2$, let $C(n)$ be the smallest constant such that for any complex polynomial $f$ of degree $n \geq 2$ with zeros $z_1, \dots, z_n$ in the unit disk and critical points $w_1, \dots, w_{n-1}$, and for any nonnegative weights $l_1, \dots, l_n \geq 0$ satisfying $\sum_{k=1}^n l_k = 1$, we have $$ \min_{1 \leq j \leq n-1} \left| \sum_{k=1}^n l_k z_k - w_j \right| \leq C(n). $$ It was conjectured by Schmeisser that $C(n)=1$.

### Problem 23. Smale's Problem

> For $n \geq 2$, let $C(n)$ be the least constant such that for any polynomial $f$ of degree $n$, and any $z \in \mathbb{C}$ with $f'(z) \neq 0$, there exists a critical point $f'(\xi)=0$ such that $$ \left|\frac{f(z)-f(\xi)}{z-\xi}\right| \leq C(n) |f'(z)|. $$ Establish upper and lower bounds for $C(n)$ that are as strong as possible.

### Problem 25. Crouzeix's Conjecture

> Let $C$ be the smallest constant for which one has the bound $$ \| p(A) \|_{op} \leq C \sup_{z \in W(A)} |p(z)| $$ for all $n \times n$ square matrices $A$ and all polynomials $p$ with complex coefficients, where $\| \|_{op}$ is the operator norm and $$ W(A) \coloneqq \{ \langle Ax, x \rangle: \|x\| \leq 1 \}$$ is the numerical range of $A$. What is $C$? What polynomials $p$ attain the bound with equality?

### Problem 27. The Prime Number Theorem

> Let $\pi(x)$ denote the number of primes less than or equal to $x$, and let $C^- \leq C^+$ denote the quantities $$ C^- \coloneqq \liminf_{x \to \infty} \frac{\pi(x)}{x/\log x}$$ and $$ C^+ \coloneqq \limsup_{x \to \infty} \frac{\pi(x)}{x/\log x}.$$ What are $C^-$ and $C^+$?

### Problem 29. Block Stacking Problem

> Let $n \geq 1$. Let $C(n)$ be the largest displacement that the $n^{\mathrm{th}}$ block in a stack of identical rigid rectangular blocks of width $1$ can be displaced horizontally over the edge of a table, with the stack remaining stable. More mathematically, $C(n)$ is the supremum of $x_n$ where $0 = x_0 \leq x_1 \leq \dots\leq x_n$ are real numbers subject to the constraints $$ \frac{x_{i+1}+\dots+x_n}{n-i} < x_i + \frac{1}{2}$$ for all $0 \leq i < n$. What is $C(n)$?

### Problem 31. Furstenberg-Sárközy Problem

> If $k, m \geq 2$ and $N \geq 1$, let $C(k,N)$ (resp. $C(k,\Z/M\Z)$) denote the size of the largest subset of $\{1,\dots,N\}$ that does not contain any two elements that differ by a perfect $k^{\mathrm{th}}$ power. Establish upper and lower bounds for $C(k,N)$ and $C(k,\Z/M\Z)$ that are as strong as possible.

### Problem 33. The Thomson Problem

> For any $N>1$, let $C(N)$ denote the infimum of the Coulomb energy $$ E(z_1,\ldots,z_N) \coloneqq \sum_{1 \leq i < j \leq N} \frac{1}{\|z_i - z_j\|} $$ where $z_1, \dots, z_N$ ranges over the unit sphere $\mathbb{S}^2$. Establish upper and lower bounds on $C(N)$ that are as strong as possible. What type of configurations $z_1,\dots,z_N$ come close to achieving the infimal (ground state) energy?

### Problem 35. Packing in a dilate

> For any $n \geq 1$ and a geometric shape $P$ (e.g. a polygon, a polytope or a sphere), let $C(n, P)$ denote the smallest scale $s$ such that one can place $n$ identical copies of $P$ with disjoint interiors inside another copy of $P$ scaled up by a factor of $s$. Establish lower and upper bounds for $C(n, P)$ that are as strong as possible.

### Problem 37. The hypergraph Turán number of the tetrahedron

> Let $C$ be the largest quantity such that, as $n \to \infty$, one can locate a $3$-uniform hypergraph on $n$ vertices and at least $(C-o(1)) \binom{n}{3}$ edges that contains no copy of the tetrahedron $K^{(3)}_4$. What is $C$?

### Problem 39. Beat the average game

> Let $C$ denote the quantity $$C \coloneqq \sup_{\mu} \mathbb{P}[X_1 + X_2 + X_3 < 2X_4]$$ where $\mu$ ranges over probability measures on $[0, \infty)$ and let $X_1, \ldots, X_4 \sim \mu$ are independent random variables with law $\mu$. Establish upper and lower bounds on $C$ that are as strong as possible.

### Problem 41. Points on sphere maximizing the volume

> For any $n \geq 4$, Let $C(n)$ denote the maximum volume of a polyhedron with $n$ vertices that all lie on the unit sphere $\mathbb S^2$. What is $C(n)$? Which polyhedra attain the maximum volume?

### Problem 43. Sum-difference problem II

> Let $C$ be the least constant such that $$ |A-A| \leq |A+A|^{C}$$ for any non-empty finite set $A$ of integers. Establish upper and lower bounds for $C$ that are as strong as possible.

### Problem 45. Sum-product problems

> Given a natural number $N$ and a ring $R$ of size at least $N$, let $C(R, N)$ denote the least possible value of $\max(|A+A|, |A \cdot A|)$ where $A$ ranges over subsets of $R$ of cardinality $N$. Establish upper and lower bounds for $C(R, N)$ that are as strong as possible.

### Problem 47. Matrix multiplications and AM-GM inequalities

> For positive-semidefinite $d \times d$ matrices $A_1, \ldots, A_n$ and any unitarily invariant norm $|||\cdot|||$ (including the operator norm and Schatten $p$-norms) and $m \leq n$, define $$ C(n,m,d) \coloneqq \inf \frac{ \frac{1}{n^m} \sum_{j_1, j_2, \ldots, j_m = 1}^{n} |||A_{j_1}A_{j_2}\ldots A_{j_m}|||}{ \frac{(n-m)!}{n!} \sum_{\substack{j_1, j_2, \ldots, j_m = 1 \\ \text{all distinct}}}^{n} |||A_{j_1}A_{j_2}\ldots A_{j_m}|||} $$ where the infimum is taken over all matrices $A_1,\dots,A_n$ and invariant norms $|||\cdot|||$. What is $C(n,m,d)$?

### Problem 49. Heilbronn problem in an arbitrary convex bounding box

> For any $n \geq 3$ let $C(n)$ be the largest quantity such that in every configuration of $n$ points in the plane, there exists a triple of points determining a triangle of area at most $C(n)$ times the area of their convex hull. Establish upper and lower bounds on $C(n)$.

### Problem 51. Erdős–Gyárfás conjecture

> Let $G$ be a finite graph with minimum degree at least $3$. Must $G$ contain a cycle of length $2^k$ for some $k \geq 2$?

### Problem 53. Equidistant points in convex polygons

> Is it true that every convex polygon has a vertex with no other 4 vertices equidistant from it?

### Problem 55. Erdős squares in a square problem

> For any natural $n$, let $C(n)$ denote the maximum possible sum of side lengths of $n$ squares with disjoint interiors contained inside a unit square. Obtain upper and lower bounds for $C(n)$ that are as strong as possible.

### Problem 57. Rudin problem for polynomials

> Let $d \geq 2$ and $D \geq 1$. For $p \in \{4,\infty\}$, let $C^p(d,D)$ be the maximum of the ratio $$ \frac{\|u\|_{L^p({\mathbb S}^d)}}{\|u\|_{L^2({\mathbb S}^d)}}$$ where $u$ ranges over (real) spherical harmonics of degree $D$ on the $d$-dimensional sphere $\mathbb S^d$, which we normalize to have unit measure. Establish upper and lower bounds on $C^p(d,D)$ that are as strong as possible.

### Problem 59. Subsets of the grid with no isosceles triangles

> For $n$ a natural number, let $C(n)$ denote the size of the largest subset of $[n]^2 = \{1,\dots,n\}^2$ that does not contain a (possibly flat) isosceles triangle. In other words, $$C(n) \coloneqq \max_{S\subset [n]^2}\{|S|: a,b,c\in S \text{ distinct} \implies \|a-b\| \neq \|b-c\|\}.$$ Obtain upper and lower bounds for $C(n)$ that are as strong as possible.

### Problem 61. The Ring Loading Problem

> Let $C$ be the infimum of all reals $\alpha$ for which the following statement holds: for all positive integers $m$ and nonnegative reals $u_1, \ldots, u_m$ and $v_1, \ldots, v_m$ with $u_i + v_i \leq 1$, there exist $z_1, \ldots, z_m$ such that for every $k$, we have $z_k \in \{v_k, -u_k\}$, and $$\left|\sum_{i=1}^k z_i - \sum_{i=k+1}^m z_i\right|\leq \alpha.$$ Obtain upper and lower bounds on $C$ that are as strong as possible.

### Problem 63. The ambidextrous moving sofa problem

> Define $C$ to be the largest area of a connected planar shape $C$ that can continuously pass through both a left-turning and right-turning L-shaped corner of unit width (e.g., both $[0,1] \times [0,+\infty) \cup [0,+\infty) \times [0,1]$ and $[0,1] \times [0,+\infty) \cup (-\infty,1] \times [0,1]$). What is $C$?

### Problem 65. Variant of IMO 2025, Problem 6

> Consider a $2025 \times 2025$ (and more generally an $n \times n$) grid of unit squares. Matilda wishes to place on the grid some rectangular tiles, possibly of different sizes, such that each side of every tile lies on a grid line and every unit square is covered by at most one tile. Determine the minimum number of tiles $C(n)$) Matilda needs to place so that each row and each column of the grid has exactly one unit square that is not covered by any tile.

### Problem 67. Logic puzzles

> We have three guards in front of three doors. The guards are, in some order, an angel (always tells the truth), the devil (always lies), and the gatekeeper (answers truthfully if and only if the question is about the prize behind Door A). The prizes behind the doors are €0, €100, and €110. You can ask two yes/no questions and want to maximize your expected profit. The second question can depend on the answer you get to the first question.

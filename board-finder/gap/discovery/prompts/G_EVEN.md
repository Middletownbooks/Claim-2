# Worker brief — Test G, EVEN slice (33 problems)

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

Write all blocks, in problem order, to **`board-finder/gap/discovery/G_even.md`** (create it). Start the file with one line
stating how many problems you labelled and how many are `NO-RECORD` and `UNKNOWN`, with the lists.

**Your final reply must contain ONLY: the file path, and the counts and lists of NO-RECORD and UNKNOWN problems. Do not put any labels, move kinds or dates in your reply** — this slice is held out and the adjudicator must not see its labels until a later step. Anything that contradicts the brief goes in the file's NOTES, not in the reply.

## Your problems

### Problem 2. An autocorrelation problem related to Sidon sets

> Let $C$ denote the largest constant for which one has $$ \max_{-1/2 \leq t \leq 1/2} \int_\mathbb{R} f(t-x) f(x)\ dx \geq C \left(\int_{-1/4}^{1/4} f(x)\ dx\right)^2 $$ for all non-negative $f \colon \mathbb{R} \to \mathbb{R}$. What is $C$?

*Repository bound table, pre-2025 rows only. Upper bounds on C: pi/2 = 1.57059, Schinzel-Schmidt 2002; 1.50992, Matolcsi-Vinuesa 8 Jul 2009. Lower bounds on C: 1, trivial; 1.182778, Martin-O'Bryant 30 Sep 2004; 1.262, Martin-O'Bryant 1 Apr 2009; 1.2748, Matolcsi-Vinuesa 8 Jul 2009.*

### Problem 4. An autocorrelation problem with functions that can take negative values

> Let $C$ be the best constant for which one has $$ \max_{-1/2 \leq t \leq 1/2}\left |\int_\mathbb{R} f(t-x) f(x)\ dx\right| \geq C \left(\int_{-1/4}^{1/4} f(x)\ dx\right)^2$$ for all $f \colon [-1/4,1/4] \to \mathbb{R}$ (note $f$ can take negative values). What is $C$?

### Problem 6. An autocorrelation problem related to difference bases

> Let $C$ be the smallest constant such that $$ \min_{0 \leq t \leq 1} \int_\mathbb{R} f(x) f(x+t)\ dx \leq C \|f\|_{L^1(\mathbb{R})}^2 $$ for $f \in L^1(\mathbb{R})$. What is $C$?

### Problem 8. Kissing numbers

> For a dimension $n \geq 1$, define the kissing number $C(n)$ to be the maximum number of non-overlapping unit spheres that can be arranged to simultaneously touch a central unit sphere in $n$-dimensional space. Establish upper and lower bounds on $C(n)$ that are as strong as possible.

### Problem 10. 3D Kakeya problem

> Let $n \geq 2$. Let $C(n)$ denote the minimal volume $|\bigcup_{j=1}^n \bigcup_{k=1}^n P_{j,k}|$ of prisms $P_{j,k}$ with vertices $$\begin{align*} \&\quad (x_{j,k},y_{j,k},0), \left(x_{j,k}+\frac{1}{n},y_{j,k},0\right), \left(x_{j,k},y_{j,k}+\frac{1}{n},0\right), \left(x_{j,k}+\frac{1}{n},y_{j,k}+\frac{1}{n},0\right),\ &\left(x_{j,k}+\frac{j}{n},y_{j,k}+\frac{k}{n},1\right), \left(x_{j,k}+\frac{j+1}{n},y_{j,k}+\frac{k}{n},1\right), \left(x_{j,k}+\frac{j}{n},y_{j,k}+\frac{k+1}{n},0\right), \left(x_{j,k}+\frac{j+1}{n},y_{j,k}+\frac{k+1}{n},1\right) \end{align*}$$ for some real numbers $x_{j,k}, y_{j,k}$. Establish upper and lower bounds for $C(n)$ that are as strong as possible.

### Problem 12. Sphere Packing

> For any dimension $n$, let $C(n)$ denote the maximal density of a packing of $\mathbb{R}^n$ by unit spheres. Establish upper and lower bounds on $C(n)$ that are as strong as possible.

### Problem 14. Hausdorff-Young Inequality

> For $1 \leq p \leq 2$, let $C(p)$ be the best constant such that $$ \| \hat f \|_{L^{p'}(\mathbb{R})} \leq C(p) \| f \|_{L^p(\mathbb{R})} $$ holds for all test functions $f \colon \mathbb{R} \to \mathbb{R}$. Here $p' \coloneqq \frac{p}{p-1}$ is the dual exponent of $p$. What is $C(p)$?

### Problem 16. Special Case of Gagliardo-Nirenberg Inequality

> Let $2 < p < \infty$. Let $C(p)$ denote the supremum of the quantities $$ Q(f) \coloneqq \frac{\|f\|_{L^p(\mathbb{R})}^{4p}}{\|f\|_{L^2(\mathbb{R})}^{2(p+2)} \|f'\|_{L^2(\mathbb{R})}^{2(p-2)}}$$ for all smooth rapidly decaying $f$, not identically zero. Establish upper and lower bounds for $C(p)$ that are as strong as possible.

### Problem 18. Hardy-Littlewood Maximal Inequality

> Let $C$ denote the best constant for which $$ \left| \{ x: \sup_{h>0} \frac{1}{2h} \int_{x-h}^{x+h} f(y) dy \geq \lambda \} \right| \leq \frac{C}{\lambda} \int_\mathbb{R} f(x) dx$$ for absolutely integrable non-negative $f \colon \mathbb{R} \to \mathbb{R}$. What is $C$?

### Problem 20. Sendov's Conjecture

> For each $n \geq 2$, let $C(n)$ be the smallest constant such that for any complex polynomial $f$ of degree $n \geq 2$ with zeros $z_1, \dots, z_n$ in the unit disk and critical points $w_1, \dots, w_{n-1}$, $$ \max_{1 \leq k \leq n} \min_{1 \leq j \leq n-1} |z_k - w_j| \leq C(n). $$ Sendov conjectured that $C(n)=1$.

### Problem 22. Borcea's Conjecture

> For any $1 \leq p < \infty$ and $n \geq 2$, let $C(p,n)$ be the smallest constant such that for any complex polynomial $f$ of degree $n$ with zeroes $z_1,\dots,z_n$ satisfying $$ \frac{1}{n} \sum_{i=1}^n |z_i|^p \leq 1, $$ and every zero $f(\zeta)=0$ of $f$, there exists a critical point $f'(\xi) = 0$ of $f$ with $|\xi - \zeta| \leq C(p,n)$. What is $C(p,n)$?

### Problem 24. de Bruin-Sharma Problem

> For $n \geq 4$, let $\Omega(n)$ be the set of pairs $(\alpha,\beta) \in \mathbb{R}_+^2$ such that, whenever $P$ is a degree $n$ polynomial whose roots $z_1,\dots,z_n$ sum to zero, and $\xi_1,\dots,\xi_{n-1}$ are the critical points (roots of $P'$), that $$|\xi_1|^4 + \dots + |\xi_{n-1}|^4 \leq \alpha (|z_1|^4 + \dots + |z_n|^4) + \beta (|z_1|^2 + \dots + |z_n|^2)^2.$$ What is $\Omega(n)$?

### Problem 26. Sidorenko's Conjecture

> A graphon is a symmetric measurable function $W \colon [0,1]^2 \to [0,1]$. Given a graphon $W$ and a finite graph $H = (V(H),E(H))$, the homomorphism density $t(H,W)$ is defined as $$ t(H,W) = \int_{[0,1]^{V(H)}} \prod_{\{v,w\} \in E(H)} W(x_v,x_w)\ \prod_{v \in V(H)} dx_v.$$ For a finite bipartite graph $H$, let $C(H)$ denote the least constant for which $$t(H, W) \geq t(K_2, W)^{C(H)}$$ holds for all graphons $W$, where $K_2$ is the complete graph on two vertices. What is $C(H)$?

### Problem 28. Golay's Merit Factor

> For $n \geq 1$, let $\mathbb{U}_{n}$ denote the set of polynomials $p(z)$ of degree $n$ with coefficients $\pm 1$. Define $$ C^-(n) \coloneqq \max_{p \in \mathbb{U}_{n}} \left(\min_{|z|=1}\frac{|p(z)|}{\sqrt{n+1}}\right) $$ $$ C^+(n) \coloneqq \min_{p \in \mathbb{U}_{n}}\left(\max_{|z|=1}\frac{|p(z)|}{\sqrt{n+1}}\right) $$ $$ C^w(n) \coloneqq \min_{p \in \mathbb{U}_{n}}\left(\max_{|z|=1}\frac{|p(z)|}{\sqrt{n+1}} - \min_{|z|=1}\frac{|p(z)|}{\sqrt{n+1}}\right) $$ $$ C^4(n) \coloneqq \min_{p \in \mathbb{U}_{n}} \frac{(n+1)^2}{\int_0^1 |p(e^{2\pi \theta})|^4\ d\theta - (n+1)^2} $$ (The quantity being minimized for $C^4(n)$ is known as Golay's merit factor for $p$.) What is the behavior of $C^-(n)$, $C^+(n)$, $C^w(n)$, $C^4(n)$ as $n \to \infty$?

### Problem 30. The Arithmetic Kakeya Conjecture

> For each slope $r \in \mathbb{R} \cup \{\infty\}$ define the projection $\pi_r : \mathbb{R}^2 \to \mathbb{R}$ by $\pi_r(a,b) = a + rb$ for $r \neq \infty$ and $\pi_\infty(a,b)=b$. Given a set $r_1,\dots,r_k, r_\infty$ of distinct slopes, we let $C(\{r_1,\dots,r_k\}; r_\infty)$ be the smallest constant for which the following is true: if $X,Y$ are discrete random variables (not necessarily independent) taking values in a finite set of reals, then $$ {\mathbf H}(\pi_{r_\infty}(X,Y)) \leq C(\{r_1,\dots,r_k\}; r_\infty) \max_{i=1,\dots,k} {\mathbf H}(\pi_{r_i}(X,Y)),$$ where $ {\mathbf H}(X) = -\sum_{x} P(X = x) \log(P(X=x))$ is the entropy of a random variable and $x$ ranges over the values taken by $X$. The arithmetic Kakeya conjecture asserts that $C(\{r_1,\dots,r_k\}; r_\infty)$ can be made arbitrarily close to $1$.

### Problem 32. Spherical Designs

> A spherical $t$-design on the $d$-dimensional sphere $S^d \subset \R^{d+1}$ is a finite set of points $X \subset S^d$ such that for any polynomial $P$ of degree at most $t$, the average value of $P$ over $X$ is equal to the average value of $P$ over the entire sphere $S^d$. For each $t \in \mathbb{N}$, let $C(d,t)$ be the minimal number of points in a spherical $t$-design. Establish upper and lower bounds on $C(d,t)$ that are as strong as possible.

### Problem 34. Tammes problem

> For $N \geq 2$, let $C(N)$ denote the maximal value of the energy $$E(z_1,\dots,z_N) \coloneqq \min_{1 \leq i < j \leq N} \|z_i-z_j\|$$ where $z_1,\dots,z_N$ range over points in $\mathbb{S}^2$. Establish upper and lower bounds on $C(N)$ that are as strong as possible. What type of configurations $z_1,\dots,z_N$ come close to achieving the maximal energy?

### Problem 36. Circle packing in a square / rectangle

> For any $n \geq 1$, let $C(n)$ denote the largest sum $\sum_{i=1}^n r_i$ of radii such that one can place $n$ disjoint open disks of radius $r_1,\dots,r_n$ inside the unit square, and let $C'(n)$ denote the largest sum $\sum_{i=1}^n r_i$ of radii such that one can place $n$ disjoint open disks of radius $r_1,\dots,r_n$ inside a rectangle of perimeter $4$. Establish upper and lower bounds for $C(n)$ and $C'(n)$ that are as strong as possible.

### Problem 38. Factoring $N!$ into $N$ numbers

> For a natural number $N$, let $C(N)$ be the largest quantity such that $N!$ can be factored into $N$ factors that are greater than or equal to $C(N)$ (see OEIS A034258 ). Establish upper and lower bounds on $C(N)$ that are as strong as possible.

### Problem 40. Erdős discrepancy problem

> The discrepancy of a sign pattern $a_1,\dots,a_N \in \{-1,+1\}$ is the maximum value of $|a_d + a_{2d} + \dots + a_{kd}|$ for homogeneous progressions $d,\dots,kd$ in $\{1,\dots,N\}$. For any $D \geq 1$, let $C(D)$ denote the largest $N$ for which there exists a sign pattern $a_1,\dots,a_N$ of discrepancy at most $C$. Establish upper and lower bounds on $C(D)$ that are as strong as possible.

### Problem 42. Sum-difference problem I

> Let $C$ be the least constant such that $$ |A+A|/|A| \leq (|A-A|/|A|)^{C}$$ for any non-empty finite set $A$ of integers. Establish upper and lower bounds for $C$ that are as strong as possible.

### Problem 44. Sum-difference problem III

> Let $C$ be the supremum of all constants such that there exist arbitrarily large finite sets of integers $A,B$ with $|A+B| \lesssim |A|$ and $|A-B| \gtrsim |A|^{C}$. Establish upper and lower bounds for $C$ that are as strong as possible.

### Problem 46. Minimal triangle density in graphs

> For $0 \leq \rho \leq 1$, let $C(\rho)$ denote the largest quantity such that any graph on $n$ vertices and $(\rho+o(1)) \binom{n}{2}$ edges will have at least $(C(\rho)-o(1)) \binom{n}{3}$ triangles. What is $C(\rho)$?

### Problem 48. Heilbronn problem in a fixed bounding box

> For any $n \geq 3$ and any convex body $K$ in the plane, let $C(n,K)$ be the largest quantity such that in every configuration of $n$ points in $K$, there exists a triple of points determining a triangle of area at most $C(n,K)$ times the area of $K$. Establish upper and lower bounds on $C(n,K)$.

### Problem 50. Max to min ratios

> Let $n,d \geq 2$. Let $C(d,n)$ denote the largest quantity such that, given any $n$ distinct points $x_1,\dots,x_n$ in $\R^d$, the maximum distance $\max_{1 \leq i < j \leq n} \|x_i-x_j\|$ between the points is at least $C(d,n)$ times the minimum distance $\min_{1 \leq i < j \leq n} \|x_i-x_j\|$. Establish upper and lower bounds for $C(d,n)$. What are the configurations that attain the minimal ratio between the two distances?

### Problem 52. Erdős squarefree problem

> For any natural number $N$, let $C(N)$ denote the largest cardinality of a subset $A$ of $\{1,\dots,N\}$ with the property that $ab+1$ is square-free for all $a,b \in A$. Establish upper and lower bounds for $C(N)$ that are as strong as possible.

### Problem 54. Pairwise touching cylinders

> Is it possible for seven infinite circular cylinders $C_1,\dots,C_7$ of unit radius to touch all the others?

### Problem 56. Good asymptotic constructions of Szemerédi--Trotter

> If $n,m$ are natural numbers, let $C(n,m)$ denote the maximum number of incidences that are possible between $n$ points and $m$ lines in the plane. Establish upper and lower bounds on $C(n,m)$ that are as strong as possible.

### Problem 58. Erdős--Szekeres Happy Ending problem

> For $k \geq 3$, let $C(k)$ be the smallest integer such that every set of $C(k)$ points in the plane in general position contains a convex $k$-gon. Obtain upper and lower bounds for $C(k)$ that are as strong as possible.

### Problem 60. The no 5 on a sphere problem

> For $n$ a natural number, let $C(n)$ denote the size of the largest subset of $[n]^3 = \{1,\dots,n\}^3$ such that no 5 points lie on a sphere or a plane. Obtain upper and lower bounds for $C(n)$ that are as strong as possible.

### Problem 62. The moving sofa problem

> Define $C$ to be the largest area of a connected bounded subset $S$ of $\R^2$ that can continuously pass through an $L$-shaped corner of unit width (e.g., $[0,1] \times [0,+\infty) \cup [0,+\infty) \times [0,1]$). What is $C$?

### Problem 64. The three-dimensional moving sofa problem with two perpendicular turns

> Define $C$ to be the largest volume of a connected bounded subset $S_3$ of $\R^3$ that can continuously pass through a three-dimensional snake-shaped corridor with a unit square cross-section, consisting of two turns in the $x-y$ and $y-z$ planes that are far apart. What is $C$?

### Problem 66. The function guessing game

> Write a program that is able to guess a hidden function. $f \colon \R\rightarrow \R$. Your program will receive a reward of $1000$ currency units for every function that it guessed correctly (the $L^1$ norm of the difference between the correct and the guessed functions had to be below a small threshold). To gather information about the hidden function, your program is allowed to (1) evaluate the function at any point for $1$ currency unit, (2) to ask a simple yes/no question from an Oracle who knows the hidden function for $10$ currency units, and (3) to ask any question from a different LLM that does not know the hidden function for $10$ currency units, and optionally execute any code returned by it.

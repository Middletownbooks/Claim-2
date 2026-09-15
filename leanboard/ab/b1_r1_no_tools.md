Thinking...
Evaluating Gaussian measures
I'm pondering whether the "Gaussian measure condition" is sufficient, but I'm uncertain about the Fisher support theorem due to volume and norm considerations at the start. I think I might need to test the K ℓ1 ball radius c m. The product supports a cube inside the ℓ1 m space, so that seems fine. Additionally, I believe I need a unit Euclidean ball scaled by √m to support the product Fisher through integration by parts.
Exploring invariants in mathematics
I’m diving into the concept of central closure P and how it relates to total directional variation under the maximum operation. I'm curious about the role of antipodal symmetry as a "balanced" invariant that is stronger than what Fisher's method preserves, leading to a result of zero. Also, there's this idea of defining concavity through a "translation deficit function." I’ll need to unpack those concepts to better understand their relationships and implications!
Evaluating binary trees and energy
I'm considering "binary trees of vector sums" with a focus on the invariant total quadratic energy and how it relates to amortized cancellation. There's a hard lemma around the total coordinate accumulation constant. It might link to standard hierarchical pairing, which leads back to the work of Banaszczyk. However, it feels like I’m overlooking a genuinely combinatorial aspect, and I'm not quite sure about the viability of this sharp approach.
Evaluating Euclidean kernel properties
I'm considering whether the kernel invariant Euclidean ball might allow for a lower visibility radius influenced by the constant CCC and the square root of mmm. I wonder if the visibility radius of the ball diminishes only when encountering new independent directions. It seems that the sum of squared coordinates could be bounded. Initially, with a constant cube CCC, the diagonal vectors might cause some loss in magnitude ∣vj∣|v_j|∣vj∣, yet the alignment could extend in other directions.
Analyzing representation calculations
I’m considering how classification and representation might impact the user's acceptance of a negative answer. It seems strong independent investigation could give a more substantive response instead of a tautology. Checking the token budget, I believe we've used 13k from a total allowance of 30k, leaving about 27k. I need to create solid mathematics by exploring the mean value property with superharmonic compact functions while ensuring the proper function conditions are met.
Exploring the max operator
I'm pondering whether the max operator has a subinvariant probability μ for all functions. I think that when I integrate the maximum of a shifted function, it should be greater than or equal to the integral of the function itself. This seems to relate to transport with stationary velocities, but I can't find a common μ concentrated in this context. However, I find the Bellman capacity to be an interesting invariant functional since it involves integrating with respect to μ while maximizing the translations.
Clarifying final responses
I need to ensure the final verdict is both honest and rigorous while addressing all parts. I think I should present the simplest useful approach by averaging using invariant Fisher methods. However, there are some missing elements. The final question should focus on the invariant and terminal condition, even if it's not fully proven. I'll wrap up with a state density, but I still need to clarify that some limitations and unresolved invariants exist.
Considering invariants for proof
I'm looking at the new invariants and how they can help with the proof. By adding a companion g and keeping the same shape and phase, I believe this can lead to a stronger invariant, which could serve as a candidate. I think I should label it as a BOARD CHANGE CANDIDATE since the new representation is explicit and potentially a more robust version of the original theorem. However, the user advises against renaming the equivalent statement.
Planning structure and length
I’m considering the final length, aiming for about 6,500 to 8,500 tokens to ensure thoroughness for the user. I think writing between 5,000 and 7,000 tokens will make sense. I’ll organize it into sections, starting with an opening summary that’s candid. I won't focus on proof improvement, but rather detail a new exact analytic compiler and a conjectural invariant. I’m thinking simple alternatives may not be the best route this time.
I. Reconstruction of the known board
Write
A=[v1 ⋯ vn]∈Rm×n,A=[v_1\ \cdots\ v_n]\in\mathbb R^{m\times n},A=[v1 ⋯ vn]∈Rm×n,
and let aj⊤a_j^\topaj⊤ be its jjj-th row. The objective is
ϵ∈{−1,1}n,∥Aϵ∥∞≤C.\epsilon\in\{-1,1\}^n,\qquad \|A\epsilon\|_\infty\le C.ϵ∈{−1,1}n,∥Aϵ∥∞≤C.
I take the Bansal–Jiang architecture in the question as given, without assuming additional details of its implementation.
Its state consists of a fractional point xxx, its active coordinates, and information about the discrepancy AxAxAx. Writing the diffusion as
dx=B dW,dx=B\,dW,dx=BdW,
the covariance is Q=BB⊤⪰0Q=BB^\top\succeq0Q=BB⊤⪰0. For example, the instantaneous variance of row jjj is
aj⊤Qaj.a_j^\top Q a_j.aj⊤Qaj.
The central difficulty is that controlling these variances individually is not enough. Their interaction with the current discrepancy matters. Directions that are harmless in a homogeneous quadratic calculation can be harmful in the current affine configuration.
The architecture is therefore:

1. Identify constraints that threaten the current discrepancy control.
2. Prove that they occupy only a controlled amount of dimension.
3. Choose a nondegenerate covariance avoiding them.
4. Continue until all coordinates are fixed.

Its fundamental obstruction is:
Can enough freedom to finish rounding survive all discrepancy constraints?\boxed{\text{Can enough freedom to finish rounding survive all discrepancy constraints?}}Can enough freedom to finish rounding survive all discrepancy constraints?
The SDP certifies the surviving freedom; spectral and affine-spectral conditions organize the constraints.
None of the diffusion, SDP, or continuous fractional path is part of the statement of Komlós. They are mechanisms for resolving that obstruction.
Outcome of this investigation
I did not obtain a new discrepancy bound. I found:

* two fairly strong obstructions to naive composable boards;
* an algebraic relaxation that loses essential information;
* a deterministic convolution board with elementary updates and a precise, but unproved, comparison invariant.

The last is my strongest candidate. Its missing lemma contains substantial new mathematics; the elementary invariants do not establish it.
II. Alternative board search
A. A bounded residual game: genuinely simple, but impossible
Consider the most literal compiler:
S=z∈K⊂Rm,Tv(z)∈{z+v,z−v},S=z\in K\subset\mathbb R^m, \qquad T_v(z)\in\{z+v,z-v\},S=z∈K⊂Rm,Tv(z)∈{z+v,z−v},
where KKK is a fixed bounded set.
The proposed invariant is simply z∈Kz\in Kz∈K. Composition would produce a signing while keeping every partial sum in KKK.
Unfortunately, no nonempty bounded KKK can satisfy
z∈K, ∥v∥2≤1⟹z+v∈K or z−v∈Kz\in K,\ \|v\|_2\le1 \quad\Longrightarrow\quad z+v\in K\ \text{or}\ z-v\in Kz∈K, ∥v∥2≤1⟹z+v∈K or z−v∈K
when m≥2m\ge2m≥2.
Proof. Put
R2=sup⁡z∈K∥z∥22.R^2=\sup_{z\in K}\|z\|_2^2.R2=z∈Ksup∥z∥22.
Choose z∈Kz\in Kz∈K with ∥z∥22>R2−1\|z\|_2^2>R^2-1∥z∥22>R2−1, and choose a unit vector v⊥zv\perp zv⊥z. Then
∥z±v∥22=∥z∥22+1>R2.\|z\pm v\|_2^2=\|z\|_2^2+1>R^2.∥z±v∥22=∥z∥22+1>R2.
Both choices leave KKK. □\square□
This does not contradict offline vector balancing. It shows that a universally composable board cannot merely retain one committed, bounded residual.
Structural lesson. A successful sequential representation must allow at least one of:

* retrospective changes to earlier signs;
* simultaneous retention of multiple histories;
* intermediate states that are not themselves bounded discrepancies.

This is a useful restriction on the search space.
B. Stationary signed transport: exact composition, fatal uncertainty obstruction
A more sophisticated proposal is to retain a probability distribution rather than one residual.
State
A random point XXX with a fixed law μ\muμ.
Move
For every ∥v∥2≤1\|v\|_2\le1∥v∥2≤1, find a coupling
X,Y∼μ,Y−X∈{−v,v}.X,Y\sim\mu,\qquad Y-X\in\{-v,v\}.X,Y∼μ,Y−X∈{−v,v}.
Invariant and composition
The marginal law remains exactly μ\muμ. Composing the couplings gives
Xn−X0=∑i=1nϵivi.X_n-X_0=\sum_{i=1}^n\epsilon_i v_i.Xn−X0=i=1∑nϵivi.
If
μ([−R,R]m)>1/2,\mu([-R,R]^m)>1/2,μ([−R,R]m)>1/2,
then, without needing independence,
Pr⁡(X0,Xn∈[−R,R]m)>0.\Pr(X_0,X_n\in[-R,R]^m)>0.Pr(X0,Xn∈[−R,R]m)>0.
Consequently some signing has discrepancy at most 2R2R2R.
This would be an exceptionally clean compiler.
Falsification
Let μ^(ξ)=Eei⟨ξ,X⟩\widehat\mu(\xi)=\mathbb E e^{i\langle \xi,X\rangle}μ(ξ)=Eei⟨ξ,X⟩. Whenever
⟨ξ,v⟩=π,\langle \xi,v\rangle=\pi,⟨ξ,v⟩=π,
the signed-step condition gives
ei⟨ξ,Y⟩=−ei⟨ξ,X⟩.e^{i\langle \xi,Y\rangle}=-e^{i\langle \xi,X\rangle}.ei⟨ξ,Y⟩=−ei⟨ξ,X⟩.
Equal marginals therefore force
μ^(ξ)=0.\widehat\mu(\xi)=0.μ(ξ)=0.
For every ∥ξ∥2≥π\|\xi\|_2\ge\pi∥ξ∥2≥π, take
v=πξ∥ξ∥22.v=\frac{\pi\xi}{\|\xi\|_2^2}.v=∥ξ∥22πξ.
This is legal, so
supp⁡μ^⊆πB2m.\operatorname{supp}\widehat\mu\subseteq \pi B_2^m.suppμ⊆πB2m.
Since ∣μ^∣≤1|\widehat\mu|\le1∣μ∣≤1, Fourier inversion gives a density ρ\rhoρ satisfying
∥ρ∥∞≤vol⁡(πB2m)(2π)m=vol⁡(B2m)2m.\|\rho\|_\infty \le \frac{\operatorname{vol}(\pi B_2^m)}{(2\pi)^m} = \frac{\operatorname{vol}(B_2^m)}{2^m}.∥ρ∥∞≤(2π)mvol(πB2m)=2mvol(B2m).
Hence
μ([−R,R]m)≤Rmvol⁡(B2m).\mu([-R,R]^m) \le R^m\operatorname{vol}(B_2^m).μ([−R,R]m)≤Rmvol(B2m).
A fixed positive cube mass thus requires
R≥cm.R\ge c\sqrt m.R≥cm.
In fact, a compactly supported common stationary law is impossible: its Fourier transform would be analytic and vanish on an open set.
Verdict on this board: exact stationarity under every signed unit translation is too rigid. It imposes a Fourier uncertainty cost worse than the desired discrepancy bound.
This rules out a substantial family of superficially attractive measure-preserving transformations.
C. Parity lattices: the move is easy, but the certificate is wrong
Signs can be written as
ϵi=1−2zi,zi∈{0,1}.\epsilon_i=1-2z_i,\qquad z_i\in\{0,1\}.ϵi=1−2zi,zi∈{0,1}.
Thus the signing problem asks whether
A1−2A{0,1}nA\mathbf1-2A\{0,1\}^nA1−2A{0,1}n
meets a constant cube.
An algebraic relaxation replaces {0,1}n\{0,1\}^n{0,1}n by Zn\mathbb Z^nZn.
State
The odd-coefficient coset
A1+2AZn.A\mathbf1+2A\mathbb Z^n.A1+2AZn.
Move
Append a generator and update the coset.
Proposed invariant
A bounded distance from the coset to the origin.
Terminal problem
A nearby point gives odd integers qiq_iqi, not necessarily signs:
∥∑iqivi∥∞≤C,qi∈2Z+1.\left\|\sum_iq_iv_i\right\|_\infty\le C, \qquad q_i\in2\mathbb Z+1.i∑qivi∞≤C,qi∈2Z+1.
The distinction is real. Let NNN be odd and large, and take
v1=(1,0),v2=(N−1,N−3).v_1=(1,0),\qquad v_2=(N^{-1},N^{-3}).v1=(1,0),v2=(N−1,N−3).
Both have Euclidean norm at most one. The odd coefficients (1,−N)(1,-N)(1,−N) give
v1−Nv2=(0,−N−2),v_1-Nv_2=(0,-N^{-2}),v1−Nv2=(0,−N−2),
whereas every signing has first-coordinate magnitude at least
1−N−1.1-N^{-1}.1−N−1.
This example does not disprove a constant bound. It demonstrates that an excellent odd-lattice certificate can contain essentially no useful sign information.
For rank-deficient real systems, AZnA\mathbb Z^nAZn may even be nondiscrete, making the relaxation still less informative.
Structural lesson. The coefficient box is not bookkeeping. Restoring it requires a new rounding theorem, and the lattice relaxation alone supplies no such transformation.
Similarly, replacing signed sums by their convex hull loses too much: the resulting zonotope always contains zero.
D. Endpoint convolution versus segment convolution
Here is the most promising alternative.
Replace a signing search by a comparison between two distributions:

* a discrete sum of independent endpoint choices;
* a continuous sum of independent points on the same segments.

The continuous distribution is analytically well behaved. The discrete one retains exact signing information.
State
A pair of smoothed densities (f,g)(f,g)(f,g).
Move
For a new vector vvv,
f′(x)=f(x−v)+f(x+v)2,f'(x)=\frac{f(x-v)+f(x+v)}2,f′(x)=2f(x−v)+f(x+v),
while
g′(x)=12∫−11g(x−tv) dt.g'(x)=\frac12\int_{-1}^1g(x-tv)\,dt.g′(x)=21∫−11g(x−tv)dt.
These are elementary deterministic operators.
Invariants already available

* total mass;
* symmetry;
* a dimension-free bound on directional Fisher information;
* log-concavity of the continuous companion ggg.

Proposed additional invariant
A pointwise comparison
f(x)≥θmg(x),f(x)\ge \theta^m g(x),f(x)≥θmg(x),
with a fixed amount of initial smoothing and constants independent of the number of vectors.
Terminal certificate
Since g(0)>0g(0)>0g(0)>0, the comparison would give f(0)>0f(0)>0f(0)>0. Compact support of the initial smoothing kernel then turns this positivity into an actual signing.
Unlike the stationary-transport proposal, this board does not commit to signs as the vectors arrive. Signs are extracted backwards from the completed convolution.
The following sections make this candidate precise.
III. Strongest candidate: a paired-convolution board
1. An explicit compact smoothing kernel
Use the even, log-concave probability density
p(t)=1516(1−t2)21{∣t∣<1}.p(t)=\frac{15}{16}(1-t^2)^2\mathbf1_{\{|t|<1\}}.p(t)=1615(1−t2)21{∣t∣<1}.
For R≥1R\ge1R≥1, define
κR(x)=∏j=1m1Rp(xj/R).\kappa_R(x) = \prod_{j=1}^m \frac1R p(x_j/R).κR(x)=j=1∏mR1p(xj/R).
Important properties are:
supp⁡κR=[−R,R]m,\operatorname{supp}\kappa_R=[-R,R]^m,suppκR=[−R,R]m,
with strict positivity in the interior, and
J(κR)=10R2Im,J(\kappa_R)=\frac{10}{R^2}I_m,J(κR)=R210Im,
where
J(h)=∫∇h(x)∇h(x)⊤h(x) dx.J(h)=\int \frac{\nabla h(x)\nabla h(x)^\top}{h(x)}\,dx.J(h)=∫h(x)∇h(x)∇h(x)⊤dx.
Indeed,
∫−11p′(t)2p(t) dt=10.\int_{-1}^1\frac{p'(t)^2}{p(t)}\,dt=10.∫−11p(t)p′(t)2dt=10.
Thus compact support in a constant cube is compatible with dimension-free directional Fisher information. No Gaussian maximum is involved.
2. The state and update
Let
bv=12(δv+δ−v)b_v=\frac12(\delta_v+\delta_{-v})bv=21(δv+δ−v)
and let uvu_vuv be the law of UvUvUv, with UUU uniform on [−1,1][-1,1][−1,1].
Start with
S0=(f0,g0)=(κR,κ1).S_0=(f_0,g_0)=(\kappa_R,\kappa_1).S0=(f0,g0)=(κR,κ1).
The exact update is
Tv(f,g)=(f∗bv,  g∗uv).\boxed{ T_v(f,g)=(f*b_v,\;g*u_v). }Tv(f,g)=(f∗bv,g∗uv).
After ttt vectors,
ft=κR∗bv1∗⋯∗bvt,f_t=\kappa_R*b_{v_1}*\cdots*b_{v_t},ft=κR∗bv1∗⋯∗bvt,
gt=κ1∗uv1∗⋯∗uvt.g_t=\kappa_1*u_{v_1}*\cdots*u_{v_t}.gt=κ1∗uv1∗⋯∗uvt.
The factorization can be retained as part of the state for certificate extraction. There is no claim that explicitly evaluating these densities is computationally cheap.
3. What is genuinely preserved
Mass and symmetry. Both remain symmetric probability densities.
Fisher information. Mixtures of translates cannot increase Fisher information:
J ⁣(∫h( ⋅−z) dν(z))⪯J(h).J\!\left(\int h(\,\cdot-z)\,d\nu(z)\right)\preceq J(h).J(∫h(⋅−z)dν(z))⪯J(h).
One proof writes the new score as the conditional expectation of the old score and applies conditional Jensen. Therefore
J(ft)⪯10R2Imfor every t.\boxed{J(f_t)\preceq \frac{10}{R^2}I_m\quad\text{for every }t.}J(ft)⪯R210Imfor every t.
Equivalently, for every direction www,
∫(Dwft)2ft≤10R2∥w∥22.\int \frac{(D_wf_t)^2}{f_t} \le \frac{10}{R^2}\|w\|_2^2.∫ft(Dwft)2≤R210∥w∥22.
This is a true, nonaccumulating analytic invariant.
Log-concavity of the companion. Each segment measure uvu_vuv is log-concave in the usual possibly lower-dimensional sense. Convolution preserves log-concavity, so every gtg_tgt is log-concave.
Moreover,
gt(0)>0.g_t(0)>0.gt(0)>0.
For an elementary justification, there is positive probability that all the continuous coefficients are sufficiently close to zero, placing their vector sum inside the positivity region of κ1\kappa_1κ1.
4. The proposed useful invariant
Define
I(f,g)=inf⁡{x:g(x)>0}f(x)g(x).I(f,g)=\inf_{\{x:g(x)>0\}}\frac{f(x)}{g(x)}.I(f,g)={x:g(x)>0}infg(x)f(x).
The desired invariant is
I(ft,gt)≥θm\boxed{I(f_t,g_t)\ge\theta^m}I(ft,gt)≥θm
for universal R>1R>1R>1 and θ>0\theta>0θ>0.
Initially this holds with θ=1/R\theta=1/Rθ=1/R, because
κR(x)≥R−mκ1(x).\kappa_R(x)\ge R^{-m}\kappa_1(x).κR(x)≥R−mκ1(x).
The exponential dependence on mmm here is not a discrepancy loss. Only strict positivity is needed for the certificate. The support radius RRR, not the lower-bound magnitude, determines the discrepancy.
5. Terminal extraction is elementary
Expanding the discrete convolution gives
fn(0)=2−n∑ϵ∈{−1,1}nκR ⁣(∑iϵivi).f_n(0) = 2^{-n} \sum_{\epsilon\in\{-1,1\}^n} \kappa_R\!\left(\sum_i\epsilon_i v_i\right).fn(0)=2−nϵ∈{−1,1}n∑κR(i∑ϵivi).
Every summand is nonnegative. Thus
fn(0)>0⟹∃ϵ:∥∑iϵivi∥∞<R.f_n(0)>0 \quad\Longrightarrow\quad \exists\epsilon: \left\|\sum_i\epsilon_iv_i\right\|_\infty<R.fn(0)>0⟹∃ϵ:i∑ϵivi∞<R.
There is also a backwards extraction rule. From
ft(y)=12ft−1(y−vt)+12ft−1(y+vt)>0,f_t(y) = \frac12f_{t-1}(y-v_t)+\frac12f_{t-1}(y+v_t)>0,ft(y)=21ft−1(y−vt)+21ft−1(y+vt)>0,
choose either positive branch. Starting at y=0,t=ny=0,t=ny=0,t=n, repeat until reaching a point where κR\kappa_RκR is positive.
This determines the signs.
The essential signing move would therefore become:
At each backwards step, choose a positive summand.\boxed{\text{At each backwards step, choose a positive summand.}}At each backwards step, choose a positive summand.
That move really is simple. The difficulty has been transferred entirely into proving positivity survives the forward construction.
IV. The hard lemma
Proposed endpoint–segment comparison lemma
Conjectural lemma. There are universal constants R>1R>1R>1 and θ>0\theta>0θ>0 such that, in every dimension and for every finite family ∥vi∥2≤1\|v_i\|_2\le1∥vi∥2≤1,
κR∗bv1∗⋯∗bvn ≥ θm κ1∗uv1∗⋯∗uvn\boxed{ \kappa_R*b_{v_1}*\cdots*b_{v_n} \ \ge\ \theta^m\, \kappa_1*u_{v_1}*\cdots*u_{v_n} }κR∗bv1∗⋯∗bvn ≥ θmκ1∗uv1∗⋯∗uvn
pointwise on Rm\mathbb R^mRm.
This is a precise, stronger-than-necessary analytic target. It would imply constant Komlós discrepancy immediately.
It would also say more than central positivity: the discrete endpoint sums, enlarged by a fixed cube, cover the region occupied by the continuously filled zonotope with a quantitative density comparison.
I do not have a proof of this lemma. It is not a consequence established here of Fisher information, convex order, or log-concavity.
What its local version would need to accomplish
For pairs generated from the same previous vectors, it would have to justify
f≥θmg⟹f∗bv≥θm(g∗uv),f\ge\theta^m g \quad\Longrightarrow\quad f*b_v\ge\theta^m(g*u_v),f≥θmg⟹f∗bv≥θm(g∗uv),
using the special paired-convolution structure and the original smoothing reserve R−1R-1R−1.
The crucial requirement is that the reserve not be spent afresh at every step.
A proof merely replacing RRR by R+1R+1R+1 after each vector is useless. A proof that needs RRR to grow with the number of effective directions also fails to settle the question.
Why the available invariants are insufficient
1. Small Fisher information does not exclude a central hole
Take
h(x)=12κR(x−Le1)+12κR(x+Le1),L>R.h(x)=\frac12\kappa_R(x-Le_1)+\frac12\kappa_R(x+Le_1), \qquad L>R.h(x)=21κR(x−Le1)+21κR(x+Le1),L>R.
Then
h(0)=0,h(0)=0,h(0)=0,
but
J(h)⪯10R2Im.J(h)\preceq \frac{10}{R^2}I_m.J(h)⪯R210Im.
The density is symmetric, normalized, and can have arbitrarily small directional Fisher information. Nevertheless it has no mass at the origin.
Thus Fisher information alone cannot be the terminal invariant.
2. Pointwise comparison is not closed for arbitrary density pairs
This is a sharper obstruction to a naive local proof.
In dimension two, let
f=g=κL,f=g=\kappa_L,f=g=κL,
and take
v=(a,a),a=1/2.v=(a,a),\qquad a=1/\sqrt2.v=(a,a),a=1/2.
Choose
x=(L−δ,−L+δ),0<δ<a.x=(L-\delta,-L+\delta),\qquad 0<\delta<a.x=(L−δ,−L+δ),0<δ<a.
Then one coordinate of x+vx+vx+v exceeds LLL, and one coordinate of x−vx-vx−v is below −L-L−L. Consequently
(f∗bv)(x)=0.(f*b_v)(x)=0.(f∗bv)(x)=0.
But for sufficiently small ∣t∣|t|∣t∣, x−tvx-tvx−tv lies inside the original cube, so
(g∗uv)(x)>0.(g*u_v)(x)>0.(g∗uv)(x)>0.
This example has:

* f=gf=gf=g;
* symmetry;
* log-concavity;
* arbitrarily small Fisher information when LLL is large.

Yet endpoint averaging destroys domination by segment averaging.
Therefore no closure theorem based only on those properties can work. The different initial smoothing scales and their common convolution ancestry must do genuine work.
Falsification tests on the actual candidate
One vector
There is no immediate obstruction.
For example, take R=4R=4R=4. If
(κ1∗uv)(x)>0,(\kappa_1*u_v)(x)>0,(κ1∗uv)(x)>0,
then ∥x∥∞<2\|x\|_\infty<2∥x∥∞<2. Hence
∥x±v∥∞<3,\|x\pm v\|_\infty<3,∥x±v∥∞<3,
and both endpoint kernel values are positive.
More quantitatively,
(κ4∗bv)(x)≥(p(3/4)4p(0))m(κ1∗uv)(x).(\kappa_4*b_v)(x) \ge \left(\frac{p(3/4)}{4p(0)}\right)^m (\kappa_1*u_v)(x).(κ4∗bv)(x)≥(4p(0)p(3/4))m(κ1∗uv)(x).
This is an actual one-step comparison. It does not establish iteration.
Orthogonal coordinate vectors
If the vectors are distinct coordinate vectors, both densities factor by coordinates. The comparison reduces to one-dimensional factors, and the preceding one-step estimate supplies a bound of the form θm\theta^mθm.
Thus this elementary orthogonal test is compatible with the proposal.
Repeated vectors
For v1=⋯=vn=vv_1=\cdots=v_n=vv1=⋯=vn=v, central positivity is immediate for R>1R>1R>1: the signed sum can be 000 or ±v\pm v±v.
But this example exposes a problem with covariance-based attempts to prove the comparison.
For repeated scalar steps aaa, smoothing produces persistent lattice phases. For fixed xxx, along either parity subsequence,
fN(x)∼2πN∑k∈Zk≡N(mod2)κR(x−ak).f_N(x) \sim \sqrt{\frac{2}{\pi N}} \sum_{\substack{k\in\mathbb Z\\k\equiv N\!\!\!\pmod2}} \kappa_R(x-ak).fN(x)∼πN2k∈Zk≡N(mod2)∑κR(x−ak).
The periodic factor need not be constant. Its parity oscillation survives even though the covariance grows smoothly.
Consequently, a local estimate that predicts every density change solely from the covariance increment can fail. Any successful proof must tolerate arithmetic phase oscillations rather than charging each oscillation as new error.
Nearly dependent vectors
This is the most serious unresolved test.
Near dependencies create many possible endpoint collisions and gaps. Fisher information sees average smoothness; covariance sees quadratic spread. Neither identifies whether a particular microscopic gap survives around the point being tested.
The candidate lemma asserts that a fixed cube smoothing eliminates all relevant gaps, uniformly through repeated convolution. That assertion is the bottleneck, not a technical afterthought.
Dimension much larger than the number of vectors
The full-dimensional initial kernels avoid singular-density problems. The factor θm\theta^mθm may be extremely small but remains positive.
There is no immediate contradiction in this regime, but this observation is not evidence of general closure.
What makes this more than the original positivity restatement?
The identity fn(0)>0  ⟺  f_n(0)>0\ifffn(0)>0⟺ a bounded signing exists is only a representation.
The additional proposal is the comparison with a specific, continuously filled, log-concave companion, under the same sequence of elementary operators. That is a stronger and independently falsifiable analytic statement.
It provides tools absent from a bare support formulation:

* convolution structure;
* a log-concave reference;
* exact directional Fisher-information control;
* explicit separation of macroscopic spread from lattice phase.

Nevertheless, it could be false even if Komlós is true. Its formulation is progress in identifying a possible bottleneck, not evidence that the bottleneck is easy.
V. Comparison with Bansal–Jiang
Bansal–Jiang architecturePaired-convolution candidateStateFractional point and geometric constraintsTwo densities and their factorizationMoveChoose an admissible diffusionEndpoint and segment averagingMain invariantSpectral/affine-spectral controlConjectural pointwise density dominationMain obstructionEnough admissible movement remainsFixed smoothing eliminates endpoint holesIterationAdaptive stochastic evolutionExact deterministic convolutionTerminal certificateAll fractional coordinates are integralfn(0)>0, then backwards branch selection\begin{array}{c|c|c} & \text{Bansal--Jiang architecture} & \text{Paired-convolution candidate}\\ \hline \text{State} & \text{Fractional point and geometric constraints} & \text{Two densities and their factorization}\\ \text{Move} & \text{Choose an admissible diffusion} & \text{Endpoint and segment averaging}\\ \text{Main invariant} & \text{Spectral/affine-spectral control} & \text{Conjectural pointwise density domination}\\ \text{Main obstruction} & \text{Enough admissible movement remains} & \text{Fixed smoothing eliminates endpoint holes}\\ \text{Iteration} & \text{Adaptive stochastic evolution} & \text{Exact deterministic convolution}\\ \text{Terminal certificate} & \text{All fractional coordinates are integral} & f_n(0)>0,\ \text{then backwards branch selection} \end{array}StateMoveMain invariantMain obstructionIterationTerminal certificateBansal–Jiang architectureFractional point and geometric constraintsChoose an admissible diffusionSpectral/affine-spectral controlEnough admissible movement remainsAdaptive stochastic evolutionAll fractional coordinates are integralPaired-convolution candidateTwo densities and their factorizationEndpoint and segment averagingConjectural pointwise density dominationFixed smoothing eliminates endpoint holesExact deterministic convolutionfn(0)>0, then backwards branch selection
Which known-board components disappear?

* Fractional coloring: absent. No point travels through [−1,1]n[-1,1]^n[−1,1]n.
* Itô evolution: absent. The updates are deterministic operators.
* SDP: absent from the formulation.
* Continuous evolution: replaced by one discrete convolution per vector.
* Dangerous-row selection: absent. There is no active subset of rows to avoid.
* Spectral independence: not the proposed signing invariant.
* Affine spectral independence: replaced, conjecturally, by a global spatial comparison between two densities.

Fisher information was written as a matrix for convenience, but it is not playing the role of a covariance-feasibility constraint. No diffusion matrix is being chosen, and Fisher control alone demonstrably does not yield the certificate.
What has not disappeared?
The coordinate cube remains intrinsic to the objective. The two-dimensional corner counterexample shows that incompatible coordinate demands are not merely an artifact of the Bansal–Jiang notation.
The candidate changes how that incompatibility is represented:
dangerous affine constraints⟶holes in a smoothed endpoint-sum distribution.\text{dangerous affine constraints} \quad\longrightarrow\quad \text{holes in a smoothed endpoint-sum distribution}.dangerous affine constraints⟶holes in a smoothed endpoint-sum distribution.
Whether the latter obstruction is easier to control is unresolved. A proof of the comparison lemma might ultimately reintroduce sophisticated discrepancy machinery. Nothing established here rules that out.
VI. Board-change verdict
BOARD CHANGE CANDIDATE
A different, exactly composable representation has emerged:

* the state is analytic rather than a fractional coloring;
* every forward move is a fixed averaging operator;
* a continuous companion supplies automatic central positivity;
* a compact-support comparison would convert that positivity into a signing;
* signs are recovered retrospectively by choosing positive branches.

But the useful comparison invariant is conjectural. The invariants proved here—mass, symmetry, Fisher control, and companion log-concavity—are insufficient. The corner and separated-bump examples establish that insufficiency explicitly.
Accordingly:
No constant bound, asymptotic improvement, or efficient algorithm was proved.\boxed{\text{No constant bound, asymptotic improvement, or efficient algorithm was proved.}}No constant bound, asymptotic improvement, or efficient algorithm was proved.
The principal research target is now sharply stated: can a fixed compact smoothing reserve compare endpoint convolution to segment convolution through arbitrarily many unit-vector factors?
Direct answer to the final question
The simplest representation I found in which a potentially useful Komlós move becomes almost stupid is a pair of smoothed convolution densities:
State:S=(f,g),S0=(κR,κ1),Move:Tv(f,g)=(f(⋅−v)+f(⋅+v)2,  12∫−11g(⋅−tv) dt),Desired invariant:f≥θmgwith universal R,θ>0,Terminal condition:gn(0)>0⟹fn(0)>0⟹∃ϵ:∥Aϵ∥∞<R.\boxed{ \begin{aligned} \text{State:}\quad&S=(f,g),\qquad S_0=(\kappa_R,\kappa_1),\\[2mm] \text{Move:}\quad&T_v(f,g)= \left( \frac{f(\cdot-v)+f(\cdot+v)}2,\; \frac12\int_{-1}^1g(\cdot-tv)\,dt \right),\\[2mm] \text{Desired invariant:}\quad&f\ge\theta^m g \quad\text{with universal }R,\theta>0,\\[2mm] \text{Terminal condition:}\quad& g_n(0)>0 \Longrightarrow f_n(0)>0 \Longrightarrow \exists\epsilon:\|A\epsilon\|_\infty<R. \end{aligned} }State:Move:Desired invariant:Terminal condition:S=(f,g),S0=(κR,κ1),Tv(f,g)=(2f(⋅−v)+f(⋅+v),21∫−11g(⋅−tv)dt),f≥θmgwith universal R,θ>0,gn(0)>0⟹fn(0)>0⟹∃ϵ:∥Aϵ∥∞<R.
The transformation is elementary and composes exactly. Preservation of the displayed comparison is the unsolved mathematical step.
# Blind re-encoding — case 1, sensitivity conjecture (cutoff 2019-06-30)

state: induced subgraph H of Q_n (or its restriction to a sub-cube of dimension
k <= n), together with an assumed cap d on the max degree, and the running
vertex count inside that sub-cube relative to half its size.

move: recursive bisection — fix a coordinate, split the k-cube into two
(k-1)-faces, pass to whichever holds more than half the local vertex mass,
charging the crossing perfect matching to the degree budget. EXPLICIT
combinatorial construction, not an existence theorem. (encoder marked this
reconstruction MEMORY)

invariant: (i) the assumed degree cap d carried into the sub-cube; (ii) the
"more than half" property up to lower-order slack; what is tracked across levels
is the relation between current dimension k and d.

composition: bisection composes only a bounded number of times; a degree cap d
limits crossing edges per level, so roughly d levels are needed before a
contradiction. Per-level loss is exponential rather than linear in the useful
margin, giving n = 2^O(d), i.e. d = Omega(log n) rather than Omega(sqrt n).

terminal: an explicit vertex of H with degree > d inside H — a direct
contradiction, certifying m(n) >= d for that n.

bound: m(n) >= (1/2 - o(1)) log_2 n — Chung, Furedi, Graham, Seymour, JCTA 49
(1988) 180-187. Unimproved 1988-2019. Same paper constructs an induced subgraph
on 2^(n-1)+1 vertices with max degree exactly ceil(sqrt n), so no lower bound can
exceed sqrt n.

leaks:
 - factor "log n vs sqrt n" | mechanism ITERATION COUNT | the recursion composes
   for only ~d levels and the dimension budget grows exponentially in d rather
   than quadratically; that gap separates proved n = 2^O(d) from believed
   n = O(d^2).
 - factor "the (1/2 - o(1)) constant" | mechanism MULTIPLICATIVE INVARIANT |
   lower-order slack in the "more than half" invariant compounds across ~log n
   halvings.
 - factor "gap between Omega(log n) and any n^eps" | mechanism TERMINAL
   CERTIFICATE TOO WEAK | the terminal contradiction only fires once n exceeds a
   threshold exponential in d, and the double-counting inequality cannot be run
   in reverse.

sources: CFGS 1988 (fetched); Gotsman-Linial 1992 (page range MEMORY);
Nisan-Szegedy 1994.

RECOGNITION: YES — names Huang, arXiv 1907.00847, 1 July 2019, one day after the
cutoff; signed adjacency matrix with eigenvalues +/- sqrt n plus interlacing.
Self-reported contamination, quoted: the sqrt n target is legitimately
pre-cutoff (CFGS's own construction), BUT "my confidence in labeling the log n
ceiling as a 'method artifact' ... is reinforced by hindsight ... A strictly
cutoff-blind assessment would have had to hedge this as 'conjectured to be an
artifact' with less certainty, since no one before 1 July 2019 had a proof that
a fundamentally different method could do better — that was exactly the open
question."

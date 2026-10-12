# Blind re-encoding — case 8, Spencer set discrepancy (cutoff 1984-12-31)

state: a partial colouring x in {-1,0,+1}^n, carried with a Chernoff-type
potential Phi_i(x) per set, estimating the chance that set i's final imbalance
exceeds a target tau under random completion of the uncoloured points.

move: colour one more point. The choice is an EXPLICIT formula (compute both
potentials, take the smaller); that a non-increasing choice always exists is
guaranteed by an averaging/existence theorem, since a parent's potential is the
average of its two children's.

invariant: sum_i Phi_i(x) never increases, and is calibrated below 1 at the
start.

composition: the invariant is additive across exactly n terms and never
increases across n moves, so it is still below 1 at the end; since Phi_i >= 1
whenever set i's imbalance exceeds tau, every set simultaneously respects the
bound. Encoder's own words: the steps chain only because there are just n error
terms, one per set, "which is exactly the union bound."

terminal: a full colouring with sum Phi_i < 1 certifies max imbalance <= tau
across all n sets at once.

bound: O(sqrt(n log n)) for every n-by-n system — random colouring plus Chernoff
plus union bound over the n sets, constructivisable by the Erdos-Selfridge
potential paradigm. Notes Beck-Fiala (1981) 2t-1 is orthogonal, beating this
only when t = o(sqrt(n/log n)). Notes the matching Omega(sqrt n) lower bound was
already in hand via the Hadamard construction, so a sqrt(log n) gap was open and
acknowledged at the cutoff.

leaks:
 - "sqrt(log n)" | UNION BOUND OVER MANY ITEMS | to keep the sum below 1 over n
   sets, each Phi_i must be forced to about 1/n, and Chernoff then requires
   tau ~ sqrt(2n ln n). The factor enters at that calibration step, from paying a
   separate 1/n budget per set rather than from any structural obstruction.

sources (all <= 1984): Beck-Fiala 1981; Beck, Combinatorica 1 (1981) 319-325 and
209-216; Olson-Spencer 1978; Erdos-Spencer 1974 (MEMORY); Erdos-Selfridge 1973
(MEMORY).

RECOGNITION: YES — Spencer, Six Standard Deviations Suffice, Trans. AMS 289
(1985) 679-706, disc <= 6 sqrt(n), removing the sqrt(log n). Self-reported
contamination, same shape as the other three: kept out of state, move, bound and
sources, but informed the leaks field — while noting the diagnosis was itself
openly available pre-1985, given the matching Omega(sqrt n) lower bound.

## NOTE: this is the first case where the leak agrees

Fable's P1 case 8 leak: "sqrt(log n) comes from the union bound over sets."
Blind encoder: same factor, same mechanism (UNION BOUND OVER MANY ITEMS), same
step. AGREE on both factor and mechanism.

Cases 1, 2 and 5 all diverged on the leading leak mechanism. Case 8 does not.
The apparent difference is how forced the diagnosis is: here the bound literally
contains a per-set budget of 1/n and the matching lower bound was already known,
so there is essentially one available reading. Where several readings are
available, the two encoders picked different ones.

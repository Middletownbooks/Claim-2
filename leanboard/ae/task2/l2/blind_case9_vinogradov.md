# Blind re-encoding — case 9, Vinogradov MVT (cutoff 2011-12-31)

The encoder opened by flagging the cutoff itself: Wooley's efficient congruencing
paper reached arXiv on 3 Jan 2011, so it counts as KNOWN BEFORE the stated
cutoff, even though the Annals publication is 2012. It reported both, saying
that conflating them "would misdate the real gap".

state: a mean-value bound at a given depth of an inductive scheme, plus the
auxiliary system of solutions restricted to residue classes mod p^m.
move: a differencing/congruencing step. The algebra (substitution + Holder) is an
EXPLICIT formula; the claim that solutions concentrate on an efficient set of
residue classes rests on averaging/pigeonhole - "you know such an efficient class
exists, not which one" - so that half needs an EXISTENCE THEOREM.
invariant: the shape of the bound and its loss exponent Delta_m under a recursion
(classically Delta_m <= (1-1/k)Delta_{m-1} + O(k)), plus total variable count.
composition: each move reduces depth by one; accumulated loss stays boundable -
geometrically in the classical method, linearly under efficient congruencing.
terminal: J_{s,k}(X) << X^{2s-k(k+1)/2+eps}.

bound AT THE STATED CUTOFF: s >= k(k+1), Wooley, arXiv:1101.0574 (3 Jan 2011),
Annals 175 (2012) 1575-1627 - the first threshold a bounded multiple of the
conjectured k(k+1)/2. It SUPERSEDED the classical s >= (1+o(1)) k^2 log k
(Vinogradov-Linnik, sharpened by Karatsuba-Stechkin and Wooley 1992).

leaks:
 - "the constant 2 in s >= k(k+1) vs conjectured k(k+1)/2" | ITERATION COUNT |
   per-step surplus requirements compound across ~k stages.
 - "the log k in the classical k^2 log k" | ITERATION COUNT | the classical
   recursion contracts only geometrically, needing ~k log k iterations at O(k)
   each.
 - "the eps in X^eps" | TERMINAL CERTIFICATE TOO WEAK | parameters optimised per
   target eps; never a single bound with explicit log saving.

RECOGNITION: YES - names the full Main Conjecture resolved post-cutoff by
Wooley's nested efficient congruencing and by Bourgain-Demeter-Guth decoupling
(Annals 184, 2016). Contamination again localised to leaks: "it shaped my
confidence in labeling the leaks as genuine method-artifacts", not the bound.

## THIS CASE EXPOSES AN ERROR IN MY OWN L2 DESIGN

Fable's P1 case 9 gives the before-bound as the classical s ~ c k^2 log k, with
efficient congruencing as the after-board. That before/after split is coherent.

I chose cutoff 2011-12-31 intending "before Wooley". That was wrong: Wooley's
paper was on arXiv from 3 Jan 2011, eleven months inside my cutoff. So the two
encodings are answering different questions - Fable describes the pre-2011
classical state, the blind encoder correctly describes the state at the date I
actually specified.

Consequence: **case 9's bound field is not interpretable as a diff.** The
divergence measures my dating error, not encoder disagreement. Fable's own
"medium confidence" flag on this line turns out to concern a claim that is
correct for the classical method; the fault is in my cutoff, not its bound.

The blind encoder handled this better than the instruction deserved - it did not
silently pick one reading, but flagged the ambiguity up front and reported both.

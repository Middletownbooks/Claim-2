# Template v2.1 — two changes

Clean text: `template_v2_1.txt`. `template_v2.txt` is left byte-identical as
the version Phase W actually ran, so the diff is auditable.

Length 2,412 → 2,653 words. Exactly two changes; everything else is unchanged.

## Change 1 — SCOPE CHECK can no longer be discharged at the domain boundary

**Evidence: Phase W, Finding 4.** Both v2 arms invoked the clause. One executed
it well: V2-A ran its mechanism unchanged on p = 17 (succeeds) and p = 73
(fails at the divisor-existence step, where its algebra predicts), and named the
step. The other discharged it for free: V2-B applied the mechanism to n = 1,
observed 1/x + 1/y + 1/z ≤ 3 < 4, and called that "breaks exactly at the stated
domain boundary".

V2-B's observation is true and worthless. The mechanism is not applied at n = 1
at all; the inequality holds whatever the mechanism is; and the domain boundary
is available in every problem, so a clause that accepts it discriminates
nothing. The v2 wording invited this by listing "a boundary parameter value"
among the acceptable targets.

v2.1 removes that phrase, requires the target to be one where the mechanism
*would plausibly appear to succeed and must not*, requires the named breaking
step to be a step **of the mechanism**, and closes the escape explicitly:

> If the only breaking point you can find is the domain boundary, report the
> SCOPE CHECK as NOT PERFORMED rather than as passed.

The last clause matters more than the rest. Under v2 a weak scope check reads
as a passed one; under v2.1 it reads as an absent one, which is what it is.

## Change 2 — new named principle: COVERAGE DIRECTION

**Evidence: the claim shape in arXiv 2508.07383**, plus Phase W's own returns.

The paper constructs polynomial families p_i(x, y, z) such that a = 4p_i + 1 is
always an integer for which 4/a = 1/b + 1/c + 1/d is explicitly solvable, and
reports that one family generates all such prime values up to at least
1.2 × 10¹⁰. Its own abstract states that a ≡ 1 mod 4 remains the open case, so
it is not claiming to settle the conjecture — but the shape of the claim is
exactly the one no clause of v2 addressed, and it is the shape three of my own
agents produced independently.

The failure it guards against: **a construction that emits only valid instances
says nothing about the instances it does not emit.** There are two containments
and they are not the same theorem —

* every output of the map is a solvable instance (usually easy; usually not the
  theorem), versus
* every instance of the target type is an output of the map (usually the
  theorem; usually unproved).

Exhibiting a family and checking that it happens to hit every target instance
below a bound establishes the first containment and a *finite* check of the
second. v2's non-target list already bans finite verification, and its
QUANTIFIER ORDER principle covers the ∃/∀ swap in adversarial settings, but
neither names this constructive version, where the seduction is that the
construction is genuinely correct and genuinely infinite.

Phase W supplies the illustration from inside the experiment. Every family all
three agents produced emits only valid solutions — verified exactly here, zero
failures across every family — and the three still cover just 75.4%, 75.5% and
93.4% of primes below 20,000. Correct output, incomplete image. That gap is the
whole conjecture.

The new clause is placed in §4 next to QUANTIFIER ORDER and requires the map,
its image, the target set, and an explicit statement of which containment is
being claimed.

## What was deliberately not changed

Nothing else. Phase W showed the substrate declaration, the coverage check, the
measurement-validity counterfactual and the verification ladder all executing as
intended in both v2 arms — V2-B's "its value under falsity is indistinguishable
from its value under truth" is the counterfactual clause working verbatim. The
temptation after a phase that goes well is to add more rules; the Phase V
finding that the heaviest prompt produced the sloppiest derivation argues
against it.

## What has not been checked

I could not read arXiv 2508.07383. arxiv.org and every mirror tried
(export.arxiv.org, huggingface.co, alphaxiv.org, api.semanticscholar.org) are
blocked by this environment's egress proxy, so the description above comes from
the title and abstract via search, not from the text. **No claim in that paper
has been verified here, and none is disputed here.** The clause it motivated
stands on its own reasoning and on the Phase W measurements.

A search result also lists a companion preprint, arXiv 2508.07367, titled
"Almost a Complete Proof of the Generalized Erdős–Straus Conjecture:
5/a = 1/b + 1/c + 1/d". That is a factual observation about a title, not about
the mathematics, which I have equally not read: "almost a complete proof" is
precisely the state both templates route to return-condition (c), and both ban
from (a).

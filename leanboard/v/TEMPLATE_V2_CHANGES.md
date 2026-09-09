# Template v2 — what changed and why

Refined for **open problems** specifically, which is what the original was
designed for and what the Phase V test problem (a solved counting question)
could not exercise. Clean text for instantiation: `template_v2.txt`.

Length: original 2,353 words → v2 2,412 words (+2.5%). Five sections of new
content were added and paid for by deleting the repetition documented in
`template_analysis.md` (the ICC example appeared five times, the
fixed-point/free-action example four).

## The six substantive changes

### 1. §0 SUBSTRATE DECLARATION — new

The template's highest-value clause is "audited by agents who did not
contribute to it", and a prompt cannot enforce it. In Phase V, Template-1
responded to the audit section by producing a checklist of ✓ ticks on its own
argument — the appearance of an audit performed by the author of the thing
audited. §0 makes the operator declare what actually exists (agent count,
independent auditor, proof assistant, budget meter, problem status) and
forbids role-playing the rest:

> Reporting a protocol step as performed when its substrate was absent is the
> most serious violation in this document — more serious than an unproved
> lemma, because an unproved lemma is visible to the next reader and a
> fabricated check is not.

Rules requiring substrate are marked **(S)** throughout, so a single-agent run
can tell at a glance which parts of the protocol it is not running.

### 2. §7 COVERAGE and MEASUREMENT VALIDITY — new

The structural gap found in Phase V: all ~30 original checks are a taxonomy of
**commission**. None asks whether the case list is complete or whether a
quantity measures what its name says. This programme's two real errors both
sat in that blind spot and would have passed every original clause —
Phase S's architecture metric (54% driven by the rate of the tactic `have`;
every computation in it correct) and Phase U's prediction ledger (ten entries
all scored correctly, drawn from four of ten pre-registration documents;
adding the missing six reversed the conclusion, Fisher p = 1.0000 → 0.0389).

COVERAGE demands the enumeration rule plus two counts — items the rule yields,
items actually treated — and routes the difference to the gap ledger.
MEASUREMENT VALIDITY demands the counterfactual value ("what would this number
be if the claim were false?") and the largest-component share of any composite.

### 3. §5 anti-self-certification — new

Directly from the observed failure. Template-1 wrote a SCOPE CHECK formula,
|V|·(7k−10)/2 ≥ 5(1+c), which at k = 3 gives |V| ≥ 20/11, asserted
"so |V| ≥ 20 … ✓", then wrote "Wait, let me recalculate carefully", abandoned
the formula, and left the ✓ standing. Two rules now close that:

> A check is reported by its content, not by its verdict. […] A line asserting
> that a check passed, without exhibiting what was computed, is void, and the
> check counts as not performed. Checklists of ticks are not audit output and
> are discarded unread.

> If you abandon a computation mid-stream — "wait", "let me redo this",
> "actually" — every conclusion downstream of it is void until recomputed. A
> superseded verdict may not be left standing beside the computation that
> superseded it.

### 4. §4 factored into named principles, with a cross-domain example bank

The algebra examples (ICC, free action, primitivity) are stated once under
RECIPE–PROPERTY INCOMPATIBILITY and referred to by name elsewhere. The bank now
includes a counting/parity entry (Euler, degree-sum, Hall) so that the
principle is not learnable as "watch out for centres". This matters because the
repetition was a pattern-matching hazard: an agent can learn the named examples
instead of the principle.

**BARRIER CHECK** is added, and is the change most specific to open problems.
Before a family gets a second agent it must say whether a known no-go theorem
excludes mechanisms of its type and what feature of this one escapes. On an
open problem the dominant waste is re-walking a road with a published wall
across it, and the original template had no clause for it. Consulting barrier
results is explicitly permitted (they are standard background); consulting the
problem's own status and history remains forbidden.

### 5. §8 VERIFICATION LADDER — new

`[PROOF ASSISTANT]` had no fallback, and no Lean toolchain has been reachable
anywhere in this programme (`elan` is egress-blocked), so the clause was
unreachable and silently dropped. Five rungs now, from machine-checked down to
"unverified, and says so in its first sentence", with the rung reached reported
in the return.

### 6. §9 budget in observable units; disproof track resourced

"Total budget: [T] of compute time, with mandatory checkpoints every [T/8]" is
unmeasurable by an agent that cannot see its own consumption, and "no early
return before [T/2]" is a live cost hazard. Checkpoints are now keyed to
countable events (artifacts returned, waves completed), and the search ends on
a substantive condition — [W] consecutive waves with no new controlled
invariant — rather than on a clock the agent cannot read. The disproof track,
asserted but unresourced in the original, now holds a floor share of [N].

Also added, from this programme's own practice: per-claim provenance tags in
§3 (DERIVED HERE / STANDARD / COMPUTED / CONJECTURED / ASSUMED, with untagged
prose read as ASSUMED), and one line at the end of §9 that removes the
incentive to fabricate on a problem that cannot be solved:

> (c) is a success condition of this protocol, not a failure of it. On an open
> problem it is the expected outcome. A correct (c) is worth more than an (a)
> that does not survive.

## What was deliberately kept unchanged

SCOPE CHECK (the strongest item in the original, and the one clause Phase V
showed to be behaviourally active — both template agents invoked the
dodecahedron boundary case, neither control did); the three-valued return with
the explicit ban on the space between; the conjunct-enumeration rule; the
"artifacts only, no status reports" rule; DERIVATION DISCIPLINE (a)+(b).

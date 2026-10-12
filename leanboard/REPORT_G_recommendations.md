# Report G — Research recommendation

Answers to the twelve questions of §18. Every claim traces to `bridge_ledger.json`
or to a file path quoted in Reports A–E. Versions in `README.md`.

## 1. Which completed theorem has the highest board value?

**Fundamental theorem of arithmetic**, as formalized by the typeclass
`UniqueFactorizationMonoid` (B = 0.908; 61 referencing files across 6 areas).
It wins because mathlib recorded it as an *interface* — the only `class` among
265 board declarations — rather than as a statement about ℕ.

## 2. Which completed theorem has the highest bridge value?

**Fundamental theorem of arithmetic again** (R = 0.931), with the **binomial
theorem** (`add_pow`, R = 0.787) a clear second and the widest measured domain
spread on the board — **36 files across 9 distinct areas**. If bridge value were
defined by cross-domain reach alone, `add_pow` would win outright; under the
declared weights the typeclass edges it out. Both are defensible and both are
reported.

(`add_pow`'s figures come after a correction: the declaration index initially
attributed the name to `Mathlib/Algebra/Tropical/Basic.lean`. See Report A §A.2.)

## 3. Which completed theorem is the strongest existing hub?

`UniqueFactorizationMonoid` — top of both dimensions, and not close. Runners-up
are the two Chinese-remainder formalizations
(`Ideal.quotientInfRingEquivPiQuotient`, `ZMod.chineseRemainder`) and the
`QuotientGroup` cluster (three isomorphism theorems + orbit–stabilizer).

## 4. Which missing theorem has the highest prospective board value?

At **class** level (the resolution the evidence supports): the MSC-57
differential-topology cluster — Stokes, de Rham, Poincaré–Hopf, Ehresmann,
h-cobordism and ~78 others over a comparatively thin `Geometry` area. Formalizing
their shared infrastructure would add more new territory than any single target.

At **target** level: the **Modularity theorem** would add the most mathematics,
and is correspondingly the least tractable (difficulty 5, an active multi-year
external project).

## 5. Which missing theorem has the highest prospective bridge value?

**Mordell–Weil.** It is the unique missing edge between a deep leaf region
(elliptic curves: 19 modules, depth 1 927, reach **76**) and the well-connected
number-field region (44 modules, reach 468). mathlib names it in exactly two
modules, and both exist to serve it.

## 6. Which missing theorem gives the best board-expansion efficiency?

**Weak Mordell–Weil** (`E(K)/2E(K)` finite) — not Mordell–Weil itself. Three of
the four ingredients are already proved (`AddCommGroup W.Point`, Northcott
heights with `finite_naiveHeight_le`, descent via `AddCommGroup.fg_of_descent'`,
and `finite_torsion`), and weak MW's own prerequisites — class-number finiteness
and Dirichlet's unit theorem — are formalized. It is one missing piece that
completes a corridor, which is the definition of high R/D.

The automated ranking in `scores.json` disagrees and puts MSC-57 first; it is
class-level and cannot see any of the per-target facts above. Where the
automated score and the inspected evidence conflict, I report both and trust the
inspection.

## 7. What is the most promising FLT-adjacent bridge?

*(Revised after Report H.)* Within mathlib, the answer below stands. Across Lean
as a whole it does not: `anthropics/fermats-last-theorem` already contains the
modular-curve, automorphic-form, Néron-model and deformation-theory
infrastructure whose absence made this question interesting. The most promising
FLT-adjacent bridge is therefore now an **integration** question — which of
those 165 mathlib-absent namespaces could be upstreamed — not a mathematical
one. See Report H.4.


**Cyclotomic fields**, via `FLT/Three.lean` → `NumberField/Cyclotomic/*` →
`NumberField` (468 importers) — the only route by which today's FLT files touch
a connected region (`ACTUAL_LEAN_DEPENDENCY`). Second: **Mason–Stothers/abc**
(proved in `FLT/MasonStothers.lean`) toward the height machinery — standard
mathematics, no formal link yet (`PLAUSIBLE_FORMAL_BRIDGE`). The Frey-curve /
modularity route is `SPECULATIVE_RESEARCH_BRIDGE` from mathlib's current state.

Note the framing correction: FLT itself is a **statement only** in mathlib and
its region has **4 transitive importers**. FLT is not a bridge; its
neighbourhood is.

## 8. What are the largest currently reachable Lean regions?

By modules: Algebra (1 360), CategoryTheory (1 116), Analysis (808), Data (656),
RingTheory (~560), Topology (~520). By *reach*, the foundation regions dominate
(`Data`: mean 3 000 transitive importers; `Algebra`: 2 177). The largest region
the 1000+ board does not touch at all is **CategoryTheory** — a seventh of the
library, invisible to any board-driven strategy.

## 9. What regions are blocked by missing bridge infrastructure?

*(Items 1–2 revised after Report H: the infrastructure exists in Lean, outside
mathlib and pinned to an older Mathlib, so these are integration blocks rather
than mathematical ones.)*

1. **Elliptic curves / arithmetic geometry** — blocked, in mathlib, on weak
   Mordell–Weil. Untouched by the FLT artifact, which needs no Mordell–Weil.
2. **Modular forms ↔ elliptic curves** — no import between them in mathlib;
   modularity is the missing link, and it **is proved** (in the semistable,
   a_ℓ-matching form) in the FLT artifact.
3. **Differential topology** — blocked on integration on manifolds and de Rham
   cohomology.
4. **Analytic number theory** — PNT attributed outside mathlib, leaving a hole
   where the region's keystone belongs.

## 10. Should Lean bridge value become an explicit objective in the laboratory?

**No — not as a scoring term, on the evidence collected here.** Three reasons,
each empirical:

* **It would reward redundancy.** The one rule our laboratory actually
  discovered (`U(m,k) ⟺ λ(m) ∣ k−1`) lands on `Monoid.exponent` /
  `ArithmeticFunction.carmichael`, the highest-traffic pads in its
  neighbourhood — and mathlib can already almost state it
  (`pow_carmichael` plus `exponent_dvd_iff_forall_pow_eq_one`). A bridge-value
  objective would have scored that discovery *highest* precisely because it was
  already there. High-traffic pads are high-traffic because their neighbourhood
  is thoroughly worked out.
* **It is a proxy for maturity, not for value.** Every component measurable
  here — usage, importers, domain spread — is large exactly where mathematics
  has already been formalized. Optimizing it steers search toward settled
  territory, which is the opposite of discovery.
* **We already have direct evidence that this kind of term misbehaves.** In the
  previous phase's deformation-invention experiment, the objective's
  "cross-modulus invariance" component *penalized* the deepest family (E scored
  0.10) because its governing invariants were inexpressible in the available
  vocabulary. A Lean-bridge term is the same species of measure and would fail
  the same way: it scores what the representation can already see.

The prompt's sharper formulation — *search for true statements that instantiate
powerful existing abstractions* — is worth distinguishing. As stated it rewards
superficial compatibility (anything of the form `∀ g, gⁿ = 1` "instantiates"
`Monoid.exponent`). What would be genuinely valuable is the harder inverse:
statements that **fail** to instantiate any existing abstraction while still
being true, compressible and extrapolating — those mark places where mathlib has
no interface yet, which is where a new interface (the highest-value artifact by
Report A's own measurements) would go.

## 11. If yes, at what stage should it enter the loop?

Not as a scoring term. It should enter **after** falsification, as a *routing
and reporting* step: once a candidate has survived freeze-and-final-holdout, ask
"which pad does this land on, and does that pad already know this?" Used this
way it is a filter against rediscovery and a formalization roadmap, not a search
bias. Concretely: run `proximity`-style matching from the candidate's shape to
`bridge_ledger.json`, and flag the candidate as *redundant*, *instantiating*, or
**interface-creating** — the last being the only category worth escalating.

## 12. What should the next computational theorem-space experiment be?

**Hold out objects, not axis ranges** — the experiment recommended at the end of
the previous phase, and now with a concrete target supplied by this map.

The laboratory's measured ceiling is that it produces per-object tables:
fitted on m ≤ 30 it cannot beat the majority-class baseline on unseen moduli
(0.90823 vs 0.90823). The missing capability is the map `m ↦ λ(m)` — a
*cross-object law*. This map is not a hypothesis the current feature language
can express, and it is exactly what `ArithmeticFunction.carmichael` is.

So the next experiment has a natural, non-arbitrary shape:

1. Give the learner a language that can name functions of the object (not only
   features of it) — e.g. multiplicativity, `f(ab) = lcm(f(a), f(b))` for
   coprime `a, b`, prime-power base cases.
2. Fit on `m ≤ 30`, hold out `m ∈ [31, 48]` **as objects**, and require
   prediction of the unseen object's period.
3. Success criterion fixed in advance: beat the majority baseline on held-out
   moduli by a margin that survives the same freeze-and-final protocol.

If it succeeds, the discovered law is `carmichael_lcm` / `carmichael_mul` /
`carmichael_factorization` — all three already in
`Mathlib/NumberTheory/ArithmeticFunction/Carmichael.lean`, which makes them a
**perfect scoring rubric**: we can check the discovery against a formal
statement without the system ever seeing it. That is a rare thing — a discovery
experiment with a machine-checkable answer key that is not available to the
learner.

And the honest expectation, from Report E: even full success would rediscover
known mathematics. Its value is as a *capability* test — can the system make the
per-object → cross-object jump at all — not as a mathematical contribution. That
capability is the precondition for everything the program is ultimately aiming
at; the Lean board's most useful message in this phase is that we are not yet
close to needing it.

---

## Bottom line for the strategic question

*Can the 1000-theorem board be treated as a playing board with measurable board
and bridge value?* **Partly, and the failure is as informative as the success.**

* Board value and bridge value **are** measurable for the 215 completed entries,
  they are **genuinely different quantities** (Pythagoras: high fame, zero
  reach; `add_pow`: modest fame, 9 areas), and the measurement contradicts the
  fame ordering — which is the result worth having.
* They are **not** measurable for the 954 missing targets. Everything computable
  about a missing target is a property of its class. Report B says so rather
  than dressing class statistics as a ranking.
* The board itself is a **poor map of Lean**: 73% of its formalized entries are
  formal cul-de-sacs, its top node is a typeclass rather than a theorem, and it
  is blind to CategoryTheory, a seventh of the library. **Regions, not board
  entries, are the right unit** — which is why Report C is the part of this
  phase most likely to be useful later.

# Phase 14 — Lean status

**Nothing in this project has been formally verified. `formally_verified_theorems` is 0 in
every run summary, and that number is accurate.**

## What was attempted

No Lean toolchain is installed in the audit container (`which lean lake elan` → nothing,
`~/.elan` absent). Installing one requires network egress that the environment's policy
proxy denies:

```
$ curl -sSI https://elan.lean-lang.org/elan-init.sh
curl: (56) CONNECT tunnel failed, response 403
```

and the proxy's own status endpoint records the denial:

```
"recentRelayFailures": [{ "kind": "connect_rejected",
  "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
  "host": "elan.lean-lang.org:443" }]
```

GitHub access in this session is scoped to two repositories, so fetching a Lean release
from `leanprover/lean4` is refused as well. Per the environment's documented policy,
organisation policy denials are reported, not worked around. Mathlib is additionally a
multi-gigabyte dependency whose build would not fit the session budget even if egress were
open.

## What exists instead

* `lean/EClassification.lean` — the classification stated in Lean 4 / Mathlib syntax using
  `ZMod m`, `Nat.factorization` and `Monoid.exponent (ZMod m)ˣ`, plus the paper proof as a
  structured comment. **It has never been elaborated.** It may well contain elaboration
  errors; no claim is made that it type-checks. It contains no `sorry` because it contains
  no proof at all.
* `runs/*/targets.lean` — the laboratory's own auto-generated output. These are `def … : Prop`
  statements of the *frozen decoder*, not of the classification, and are labelled
  `UNCHECKED SPECIFICATION` by the generator itself.

## Where the formalisation boundary lies

Independently of tooling, the honest boundary is this: what the experiment produced is a
finite table (48 threshold/period pairs), and a Lean statement of *that* is a 48-case
disjunction with no mathematical content. The statement worth verifying is the auditor's
Phase 13 theorem, which the experiment did **not** produce. So formalisation here would
verify the auditor's mathematics, not the laboratory's discovery — a distinction that
matters more than the missing toolchain.

The hard step for a future formalisation is not the two mechanism lemmas (both are short)
but transporting a `∀ x : ZMod m` statement across `ZMod.chineseRemainder` and relating
`Monoid.exponent` of a product of unit groups to the `lcm` of the factors' exponents.

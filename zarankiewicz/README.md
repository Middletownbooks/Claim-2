# Zarankiewicz / K₇,₁₁ working area

This branch exists because the only copy of the search program lived in a chat sandbox, which
has no version control and is lost when the conversation ends. It is the durable home for that
work and for everything downstream of it.

**Branch:** `claude/zarankiewicz-k711`, cut from the lab branch at `e9f4261` so it carries the
Woodall reading, the verified (4,6)-set, the register and the protocol ledger.

**Integration rule, same as the lab branch:** another instance works on the lab branch, so this
branch **merges from it and never rebases onto it**, and nothing here is force-pushed. When
something is worth landing, it lands by merge.

## Why this is a separate branch and not more of `board-finder/gap/v4/`

The v4 directory is the *selection* lineage — a triage rubric, a target scored against it, a
headroom argument. What happens next is not selection, it is a build: a canonical-form
enumerator, a positive control against a 1988 result, and a decision between porting and
rewriting. That is a different kind of artefact with a different failure mode, and keeping it
out of the gate documents stops a build log from reading like evidence.

The v4 artefacts stay where they are and are referenced, not moved; `board-finder/tools/check_paths.py`
holds a baseline of 89 unresolved citations that moving files would disturb for no gain.

## What is here

| | |
|---|---|
| `zarankiewicz/intake/` | where relayed code and raw output land, with the provenance stamp each needs |
| `zarankiewicz/verify_orbit_bounds.py` | the bound-free orbit ladders that falsify the relayed level counts |
| `zarankiewicz/PREREG_INTAKE.md` | `P-44`, registered before any of the program is seen |

## What is already established here

Three relayed (7,7) level counts are checkable from this side and **none is a count of
isomorphism classes of *k*-element subsets of *V*(CO₇) at any antisum threshold** — 13 against the
ladder 1, 2, 6, 14, …; 377 between 280 and 1,710; 29,099 between 12,484 and 38,309. The *k* = 4
row is convention-independent, since no ordering rule can raise a class count. The **sign** of the
error is undetermined, because the misses change direction with the threshold, so both earlier
directional readings are withdrawn.

## The standing rule this area exists to enforce

`D67`: **a measurement moves as code or as raw output, never as a number in prose.** Nine rounds
of correspondence corrected reasoning in both directions and degraded every number that described
a run. Nothing in this directory may cite a figure that arrived as a figure. If a number is used
in an estimate, either the routine that produced it or the file it wrote is in `intake/`, or the
number is recorded as uninterpreted.

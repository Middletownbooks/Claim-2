# Intake

Nothing here yet. This is the landing spec, so that what arrives is usable rather than just
stored.

## What is wanted, smallest first

| | what | why it is first |
|---|---|---|
| 1 | the **canonicalisation routine**, verbatim, and the predicate deciding whether a node is kept | settles what the level counts count, which is currently unresolvable from either side |
| 2 | the **search driver**, enough to re-run (7,7) end to end, plus the line that increments the level counter | the counter is exactly what is in dispute |
| 3 | the **raw output files** of the runs already reported — the files, not the summaries | `D67` |
| 4 | the **(4,6)-set certificate** as the program emits it | a positive control before the port is trusted on anything new |

## Provenance stamp

Each arrival gets a sibling `*.provenance.md` naming: what produced it; what the wall-clock
budget per call was; whether the run completed or was truncated, and at what depth; and which
tier it sits at — `PRIMARY-VERIFIED-LOCALLY` only once it has been run here, `SECONDARY-RELAYED`
until then. A file with no stamp is not citable.

## The constraint on asking

`D57`(ii): a relay message carries no repository path, no branch, no file name and no internal
identifier. **Where code lands is the operator's decision and is never stated in the request.**
The request names the code; the operator moves the bits. That the destination now exists does not
change what may be written in a relay.

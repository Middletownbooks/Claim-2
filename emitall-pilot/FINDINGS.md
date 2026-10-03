# emitall pilot on STATUS.md

Tool: `BootLoops-ai/bootloops` `tools/emitall` (MIT, read-only clone, not modified).
Target: `STATUS.md` §2 ("What is established"), the 2026-09-09 revision.
Spec: `claims_status.json`. Raw output: `run_output.txt`, `report.json`.

Re-run (from this directory, with a bootloops checkout beside the repo):

    python3 <bootloops>/tools/emitall/run.py claims_status.json --out report.json

## Result: 41 headlines re-emitted, 34 MATCH, 7 FINDINGS (exit 1)

Every claim was quoted exactly as STATUS.md prints it (thousands separators dropped).
Receipts are the committed JSON files; receipts were not regenerated.

### Matches (34)
- Laboratory/cross-object: phase-0 0.90823 vs 0.90823; K 18/18, 1.00000 vs 0.90278;
  L 12/12, 0/6, 0.715 vs 0.917; +1 expression 18/18, 1.000; licensing 0.667 / 1.000.
- Lean board: 1,199 entries = 214 + 1 + 30 + 954; 72% zero-use is 191/265 = 72.08%,
  recomputed from `usage.json` per-declaration rows.
- FLT: 29,511 theorems; 1,696 modules (19.9%); Q 0.677; 36 communities; 282 interfaces; 15.5%.
- NS: 303 modules.
- Report O: breadth beats frequency on 0 of 6 splits (checked per split).

### Findings (7), in decreasing order of importance

1. **The NS "strict" numbers have no committed receipt (4 findings).**
   `leanboard/ns/phase1.json` and `phase1_loose.json` are **byte-identical** and both hold the
   *loose* run (Q 0.000, 1 community >=100, largest 48,496, bottleneck 0.0001). STATUS.md and
   REPORT_O quote the strict run (Q 0.503, 13 communities, bottleneck 0.59, top-1% 17.7%).
   `phase1.py` writes `phase1.json` unconditionally (line 175), so the strict output was
   evidently overwritten by the loose run. The claim Report O leans on, "broad seams replicate",
   therefore rests on numbers that cannot be re-emitted from the repo as committed. The fix is
   to re-run `phase1.py` under the strict rule and commit the output under its own name.
   This needs the NS source tree, which I did not have.
   Side-effect: the 0/6 forecast result is checked, but against the file's forecast block only;
   I could not tell whether that block came from the strict or the loose run.
2. **NS coverage is 3.6%, not 3.5%.** 303 / 8,513 = 3.559%. `ns_analysis.json` stores
   `coverage_fraction` rounded to 4 d.p. (0.0355), and quoting 3.5% passes against *that*
   (control row kept in the spec). A first-pass tool result of MATCH here is a false comfort:
   emitall checks the quote against the receipt field, not against the raw counts behind it.
3. **FLT "~4,184 upstreamable" has no receipt.** `upstreamable.json` holds 4,281
   (`self_contained`) and 4,577 (`mathlib_vocabulary_only`). REPORT_I derives 4,184 by a further
   filter (the proof file also imports no repo definition) and "3,043 cite nothing"; neither
   is stored. STATUS.md and the SUMMARY quote 4,184, so the number is a documented derivation
   whose output was never saved.
4. **NS "49,365 declarations" vs 49,379 in `ns_analysis.json`** (a difference of 14). Report O
   calls 49,365 "declaration names"; the receipt counts by kind. Probably a different universe,
   not an error, but nothing in the repo reconciles them. Unresolved.

### What this says about the tool
- It found real receipt gaps in a 41-row pilot, which is the failure mode it is
  built for. Two of the seven findings (3 and 4) are likely universe/definition differences
  rather than errors, and the spec's `note` fields say so.
- Limits met: no list comprehensions or conditional expressions in the expression language
  (use `where`/`len`); a match is only as good as the receipt field's own precision (finding 2);
  claims with no stored receipt can only be recorded as findings, not checked.
- Not covered, because no JSON receipt exists: the 186 s runtime, 70,720 queries, 648 errors
  (these are only in `theorem-lab/audit/REPORT.md` prose), Report M's term-formation results,
  and the "55% of NS definitions" figure. These need receipts before emitall can check them.

### Suggested follow-ups
1. Regenerate and commit the strict NS run as `phase1_strict.json`; re-run this spec.
2. Persist the 4,184 / 3,043 subsets from REPORT_I's derivation.
3. Add receipts (even small JSON) for the audit figures and Report M, then extend the spec.

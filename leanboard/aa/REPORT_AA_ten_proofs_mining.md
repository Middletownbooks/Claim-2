# REPORT AA — Mining the ten-proofs corpus for bridges

Corpus: `openai/ten-proofs`, cloned at HEAD. Ten developments, one `.lean`
file each, all on `import Mathlib` — so any identifier not declared locally is
library vocabulary, which makes the exportability test clean.

18,223 theorems and lemmas parsed across the ten.

## Headline: there is almost nothing to mine, and my earlier number was wrong

A declaration is worth upstreaming when its **statement** mentions no locally
declared object — it is a fact about mathlib objects that happens to live in
this repo. On that test:

**3 of 18,223 theorems qualify (0.016%).**

All three are in GapCVP, all three are trivial `List.finRange` facts, and two
of the three are the *same theorem declared twice* with the binder renamed
(`row` vs `rank`) — a duplicate within a single development, not a bridge.

```
finRange_idxOf?_eq_some  (row  : Fin count) : (List.finRange count).idxOf? row  = some row.val
finRange_idxOf?_eq_some  (rank : Fin count) : (List.finRange count).idxOf? rank = some rank.val
finRange_findIdx?_of_find? ...
```

## Correction: Phase S's `exportable_fraction` is buggy

`leanboard/s/census.py` scored a theorem exportable when its statement tokens
did not intersect the set of own definition names. Its tokenizer is

```python
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
```

which captures **dotted** names, while the `own` set holds **bare** declaration
names. So a statement referring to `SoficGroups.componentVertexMidrank` yields
that token, `own` contains `componentVertexMidrank`, the intersection is empty,
and the theorem is scored exportable although it plainly references a local
definition. Every fully-qualified local reference is missed.

Worked instance, `NonSoficGroup.sum_componentVertexMidrank`:

```
tokens found      : ['SoficGroups.componentVertexMidrank']
own set           : {'componentVertexMidrank'}
intersection      : set()        -> scored EXPORTABLE, wrongly
```

Of the 264 NonSoficGroup theorems Phase S called exportable, the strict test
clears **none**; the blame is dominated by qualified references to local
namespaces (`SoficGroups.boundary` 61, `SoficGroups.SoficApproximation` 26,
`SoficGroups.partitionWordCrossing` 24, …).

| | Phase S figure | corrected |
|---|---|---|
| CompactnessAndDegeneracy | 9.6% | 0 |
| ConnesRigidity | 13.2% | 0 |
| EhrhartVolumeInequality | 5.6% | 0 |
| GapCVP | 4.6% | 3 (0.1%) |
| MetricCodes | 11.7% | 0 |
| MulticolorTriangleRamsey | 16.7% | 0 |
| NonSoficGroup | 24.9% | 0 |
| Permanent | 15.5% | 0 |
| QuantumParallelRepetition | 8.1% | 0 |
| SpherePacking | 17.5% | 0 |
| **total** | **1,992 (10.9%)** | **3 (0.016%)** |

The parse itself is sound — re-running Phase S's own predicate on my parse
reproduces its published numbers (MulticolorTriangleRamsey 16.7% exactly), so
the discrepancy is the predicate, not the extraction.

This is the second time in this programme a correctly-computed metric turned
out to measure something other than its name (after Phase S's 54%-`have`
architecture metric), and both were in Phase S.

## Which pairs share ground, generic substrate removed

From `leanboard/s/distance.json`, ranking by `vocab_rare` (the 59 generic
mathlib vocabulary declarations excluded):

| pair | shared rare vocabulary |
|---|---|
| EhrhartVolumeInequality ↔ SpherePacking | 0.193 |
| ConnesRigidity ↔ NonSoficGroup | 0.185 |
| NonSoficGroup ↔ QuantumParallelRepetition | 0.159 |
| MetricCodes ↔ QuantumParallelRepetition | 0.156 |
| MetricCodes ↔ SpherePacking | 0.150 |

median 0.081, min 0.023. By shared interface the top pair is the same
(EhrhartVolumeInequality ↔ SpherePacking, 0.236), with MetricCodes ↔ Permanent
second at 0.205.

The two top pairs are mathematically unsurprising — lattice-point counting
next to sphere packing, and property (T)/rigidity next to soficity — which is
mild evidence the distance measure tracks something real. But an overlap of
0.19 on rare vocabulary, with zero exportable statements underneath it, is
shared *background*, not a shared *lemma*.

## What this means for mining

**Corrects my recommendation of the previous turn.** I said the ten-proofs
collection was likely a better hunting ground than FLT or NS. On the strict
criterion that is wrong: this corpus yields three trivial list lemmas, two of
them the same lemma twice.

The reason is structural and visible in the census: every one of these
developments is a bespoke tower — `own_definitions` runs from 43
(MulticolorTriangleRamsey) to 4,314 (GapCVP) — and essentially every theorem
is stated in terms of that tower. A theorem about `SoficApproximation` or
`paletteBlockLabel` cannot be lifted anywhere, however elegant, because the
subject does not exist outside the file.

Note the NS figure from the previous turn (113 statements with ≥6 mathlib
tokens) is a **different and looser** measure, not comparable to the 3 here.
Running the strict test on NS would need its source, which this environment
does not hold; I am not claiming a comparison.

The honest conclusion: **upstreamable-lemma mining is not where the value is
in any of these artifacts.** What generalises across such developments is
architecture and technique, not statements — which is consistent with Phase T
finding construction-trajectory transport falsified at the statement level
while L1 Lean-token style remained source-specific.

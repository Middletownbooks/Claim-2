# Pre-registration — blind region discovery on the FLT citation graph

Written and committed **before** the clustering is run and before any result is
inspected. The question, from the supervising researcher: can the major proof
regions and their interfaces be recovered from the graph alone?

## What the algorithm may see

Only the citation graph: 29 511 integer node ids and 106 897 directed edges
(`flt/flt_graph.json`). **Node names are stripped before clustering.** No
`PROOF-PATH.md`, no namespaces, no knowledge that the root is FLT, no statement
text. Names are re-attached only for scoring, after the clustering is frozen.

This matters because the repository states its theorem names are machine
generated and its Lean statements, not its names, are authoritative.

## Method

1. Undirected view of the citation graph.
2. Deterministic asynchronous label propagation: nodes visited in ascending id;
   each takes the most frequent label among its neighbours, ties broken by
   smallest label; at most 40 rounds or until no label changes.
3. For each community: size, internal edges, boundary edges, and its
   **interface set** = members with at least one cross-community edge.
   Bottleneck ratio = |interface| / |community|.
4. Region graph: communities as nodes, edges weighted by cross-community
   citation count.
5. Second, independent view: cluster theorems by the set of repository
   definition modules their **statements** import (opaque identifiers, not
   names), to test whether statement vocabulary and citation structure agree.

## Pre-registered predictions

* **P1 (decomposability).** The graph yields between 5 and 60 communities of
  size ≥ 100, not one giant blob. *If this fails, the honest conclusion is that
  the proof is not modular at this granularity and structural "bridge value"
  does not apply to it — a negative result worth reporting.*
* **P2 (largest region).** The largest community corresponds, after unblinding,
  predominantly to modular curves — the namespace holding 26% of all theorems.
* **P3 (narrow interfaces).** The median bottleneck ratio over communities of
  size ≥ 100 is below 0.25: regions connect through comparatively few nodes.
* **P4 (narrative recovery).** Each community of size ≥ 500 maps to at most one
  of PROOF-PATH's six steps by majority namespace — i.e. the graph's own
  decomposition does not cut across the human account of the proof.
* **P5 (agreement).** Communities from citation structure and clusters from
  statement vocabulary agree better than chance (measured by adjusted mutual
  information against a permuted baseline).

## Scoring

Each prediction is scored as stated, before any weight-tuning, and failures are
reported. Namespaces and PROOF-PATH are held-out ground truth and are consulted
only in step 5 of the analysis.

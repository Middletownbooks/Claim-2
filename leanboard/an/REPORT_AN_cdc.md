# Arm AN — the Cycle Double Cover claim: `openai/cdc-lean` and Kintali's paper

**Targets.** Two independently claimed proofs of the **Cycle Double Cover Conjecture**, announced
the same week of July 2026:

- **`openai/cdc-lean`** — VibeMathed entry "Cycle Double Cover", significance 55, `lean-checked`,
  `ai-discovered`, GPT-5.6 Sol Ultra, no human collaborators, announced 10 July 2026. Cloned at
  HEAD `577e9d9`.
- **Kintali, *Three-Bit Flows and Cycle Covers Part I*, arXiv:2607.14140v1** (13 July 2026), whose
  §11 explicitly compares itself to OpenAI's: *"OpenAI's proof is linear-algebraic while our proof
  is graph-theoretic... Both papers share the high-level flow to label arguments."*

**What I am not saying.** I have not verified that CDC is proved, and nothing here should be read
that way. CDC has a long history of claimed proofs with later-found gaps — the site's own note says
exactly that, and that mathematicians are treating it cautiously pending independent review. What
follows is what is checkable from outside.

---

## 1. Kintali's construction executes and produces valid covers — `verify_cdc_construction.py`

The pipeline is entirely finite, so I implemented it end to end: nowhere-zero `F₂³` flow → vertex
triangles → the gluing system `t_u ⊕ t_v ⊕ ε_e f(e) = d_e` solved over `F₂` → label subgraphs →
components. Then I checked the output really is a cycle double cover.

Nine properties per graph — bridgeless, cubic, Lemma 4.6, **gluing system solvable**, sides agree,
pairs are 2-element, every vertex degree 0 or 2, components are cycles, **every edge covered
exactly twice** — on 15 graphs:

| | result |
|---|---|
| K₄, θ-multigraph, K₃,₃, Q₃ | 9/9 each |
| **Petersen** | 9/9, 5 cycles |
| **Blanuša snark 1** | 9/9, 7 cycles |
| **flower snarks J₅, J₇, J₉** | 9/9 each |
| 6 random cubic graphs, n = 12…22 | 9/9 each |

**The construction works on every snark tested**, including the non-3-edge-colourable cases that
are the whole difficulty. That is not a proof, but it rules out the cheapest failure modes.

**Why the construction is not trivial**, which is worth stating because it is easy to
underestimate: from a nowhere-zero `F₂³` flow, the obvious even subgraphs are
`D_r = {e : r·f(e) = 1}` for the seven nonzero `r`. Each edge lies in **four** of those seven, not
two — a quadruple cover. Getting **two** is the entire game, and it is what the triangle-gluing
machinery delivers. (The easy `F₂²` case — nowhere-zero 4-flow, equivalently 3-edge-colourable —
gives `c₁, c₂, c₁⊕c₂` covering each edge exactly twice, which is the classical result.)

## 2. The Lean is clean, and small

16 files, **7,156 lines**. No `sorry`, no `admit`, no `native_decide`, no `unsafe`, **no `axiom`
declarations** anywhere outside comments. Lean pinned to `v4.31.0`, Mathlib to `9a9483a…`.
`VERIFICATION.md` records a 1,727-job build and `#print axioms` returning exactly the three
standard axioms. Its own `Audit.lean` plus a ripgrep scan is the documented check.

For contrast with arm AM: **this repo declares no project-specific axioms at all**, where
PrimeGaps186 declares three in its trusted statement file.

## 3. The statement audit — and the definitions hold up

The final theorem is

```lean
theorem cycleDoubleCover_of_bridgeless (G : FiniteGraph V E) (hb : G.Bridgeless) :
    Nonempty G.CycleDoubleCover
```

over the repo's **own** `FiniteGraph`, `Bridgeless` and `Cycle` — none of them Mathlib's. So unlike
the zeta development (arm AK), which states its theorems against Mathlib's `riemannZeta`, here the
statement is only as good as three custom definitions. Each is finite, so I brute-forced all three
over **every loopless multigraph with n ≤ 5, m ≤ 6 and no isolated vertices — 4,860 graphs**:

| definition | as written in the repo | textbook meaning | mismatches |
|---|---|---|---:|
| `Cycle` | nonempty, **inclusion-minimal even edge set** | connected and 2-regular | **0** |
| `Bridgeless` | **no vertex subset whose cut has exactly one edge** | no edge whose deletion disconnects | **0** |
| `CycleDoubleCover` | `List Cycle` with each edge in exactly 2 | multiset, each edge exactly twice | — (direct) |

The `Cycle` definition is the one that mattered most, because a weaker reading — "even subgraph"
rather than "cycle" — would have made the theorem far less than CDC. It is not weaker: a minimal
nonempty even edge set is exactly a graphic-matroid circuit, hence a genuine cycle, and the
docstring's claim to that effect is correct. Parallel pairs give honest length-two cycles
(`parallelPairCycle`), and `singleton_not_even` is what looplessness buys.

**The definitions say what they should.**

## 4. The one real scope finding: the theorem is the *loopless* case

`loopless : ∀ e, endAt e 0 ≠ endAt e 1` is a **structure field** of `FiniteGraph` (and of
`CubicGraph`). A multigraph with a loop is therefore **not a term of the type at all** — the
theorem cannot even be stated for it, let alone applied.

The conjecture, as Kintali states it (Conjecture 1.3) and as it is standardly given, is *"Every
finite bridgeless multigraph has a cycle double cover."* Kintali's Proposition 3.1 Step 1 handles
loops explicitly: delete them, cover the rest, reinsert two copies of each loop, since a loop is
itself a cycle. **That step is not formalized here.**

This is a small gap and a trivial one mathematically — but it is a gap between the formal statement
and the conjecture, and it is exactly the kind of thing a statement audit exists to find. To the
repo's credit, **both `README.md` and `VERIFICATION.md` say "loopless" in their first sentence**;
the restriction is disclosed, not hidden. The site's entry, which reads "Cycle Double Cover
Conjecture … resolved", does not carry the qualifier.

## 5. What remains, and why the tier is right

Everything above is compatible with the proof being correct **and** with it having a gap in the
mathematics I did not reach. What I checked is that the artifact compiles clean at source level,
that its definitions mean what they say, and that the sibling paper's construction actually
produces cycle double covers on hard inputs. What I did not check, and cannot:

1. **The kernel.** No toolchain here; the 1,727-job build is the repo's own record.
2. **The Jaeger–Kilpatrick formalization** — `JaegerKilpatrick.lean` is 1,223 lines and
   `NashWilliams.lean` is 3,657, together **68% of the development**. The external input is being
   proved in-repo rather than assumed, which is a point in its favour and also the largest
   unaudited surface.
3. **The mathematics of the gluing argument at scale.** I verified its local lemmas by hand and its
   output by computation on 15 graphs; neither is a proof.

`lean-checked` is the correct tier, and the site's caution — *"the Cycle Double Cover Conjecture
has a history of claimed proofs later found to have gaps"* — is the right posture. **Two
independent AI-assisted claims in the same week, sharing a high-level method, is a pattern worth
watching rather than a confirmation:** common-mode error is exactly what shared methodology
produces.

## 6. Next

1. **The loop reduction is a few dozen lines** and would close the gap between the formal statement
   and the conjecture. It is the single highest-value contribution to this artifact.
2. **`NashWilliams.lean` + `JaegerKilpatrick.lean` are the audit surface**, at 4,880 lines and no
   external reference to check against — they are formalizing the eight-flow theorem from scratch.
3. **Kintali's paper is "Part I"** and is a separate artifact from the Lean; nothing in
   `openai/cdc-lean` corresponds to it. If the site lists them separately, they should not be
   treated as corroborating each other — they are two claims, not one claim twice.

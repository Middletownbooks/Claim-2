# Woodall tight / pseudo-tight — code handoff

*Upstream README, as received. Reproduced verbatim except that one malformed code fence in the
original paste has been closed so the file renders.*

Everything needed to re-derive the (4,6) counterexample, re-run the controls, and
continue the K7,11 headroom work. Pure Python + numpy. No network.

```
python3 reproduce.py                # all externally-anchored controls, ~90 s
python3 reproduce.py --certificate  # + full certificate for the published set
python3 reproduce.py --n6           # + exhaustive n=6 sweep (6,930 classes)
```

| file | contents |
|---|---|
| `cog.py` | CO_n: construction, canonicalisation, labels, antipodes, distances, relabel group, stabiliser, `class_canon` (isomorph canonical form in \|M\|·2n maps, not 2·n!) |
| `checkers.py` | Q-family construction (4 readings), Forced/Possible, shortest-antipath label sets, `pseudo_tight`, `is_tight`, `bracket` — all generalised to any m |
| `search.py` | staircase, the node-keep predicate (documented clause by clause), search driver with exact level counter, `thm7_availability`, `ablation_valid` |
| `generator.py` | the certified generator: pair-optimal straight-line drawings, crossing counts by segment intersection, `realise` |
| `certificate.py` | the 14 reading-independent (4,6) counterexamples, the published one's witness and certificate, the m=5 propagation data |
| `reproduce.py` | the control suite |

## What is established

- **The counterexample.** A (4,6)-set pseudo-tight and not tight under *every* admissible reading of "antipath". Answers Woodall p.663 (i) affirmatively, refutes (ii). Touches neither Zarankiewicz nor Hill, and leaves K7,7 / K7,9 intact.
- **The bracket.** pseudo-tight at `both` ∧ not tight at `arbitrary` ⟺ holds at every reading. Exact, not conservative. **Boundary: fixed objects only** — it fails for counts and universal negatives, because the conjunction is a *window* in the lattice. Measured: n=6 counts 48/19/54/22, core 14.
- **Two-sided validation.** Over-strictness: pair-optimal drawings must be tight (`generator.py`). Over-permissiveness: Woodall's ≥10 non-pseudo-tight (4,7)-subsets per antisum-79 (7,7)-set. Both directions are required — the ≥10 bound passes under all four readings and cannot discriminate.
- **Theorem 7 availability does not propagate.** m=7 via m′∈{2,4}; m=9 via m′=4 only; **m=11 none**, because the hypotheses need exact antisum bounds at (7,7) and (9,7) and the true minima are 79 and 140.
- **Deficit-weakened Theorem 7.** `antisum ≥ Z(m)Z(n) − d₂ − (m−m′)·d₃`; at m=11, m′=4 gives ≥223. Verified arithmetically over odd m<20, odd n<14, even m′<n.
- **Ablation.** Theorem 7 bought **1.30×** at (7,7) to depth 5 (both configs complete; exact). The cumulative ratio equals the *deepest-level* ratio — the last level holds 96% of the tree — so per-level ratios must **not** be compounded. Log-linear fit: ~1.4–1.5 at depth 7, ~1.8–1.9 at depth 11.
- **Frontier at (11,7).** Populated below the top rung: 288 sets at antisum 221 before abort. Distribution unreliable (truncated DFS); nothing yet at 219.

## What is NOT established, in priority order

1. **What the weakened Theorem 7 buys.** Four attempts, all invalid by `ablation_valid`. The bottleneck is the prune's `C(k−1,3)` rescan: 20 triples at m=7, **120 at m=11**, measured at 217k nodes/s without vs 98k/s with — so it must shrink the tree by >2.2× just to break even in wall clock. **Make the (4,n)-subset check incremental before retrying.** Maintain, per node, the minimum antisum over 4-subsets containing each element, updated in O(k²) on push rather than rescanned in O(k³).
2. **(9,7) ablation** — the ON run never completes; same fix applies.
3. **(7,7) depths 6–7** — same.
4. **Whether anything lives below antisum 221 at (11,7).** Parity makes 219 the next rung.
5. **Any structural characterisation of these sets.** Two hypotheses dead. Window *mass* separates at n=6 (AUC 0.811) but runs backwards across n — n=5 has ~3× the mean width and zero counterexamples. Slack-*count* does better at n=6 (AUC 0.869) but decays to 0.639 at n=7, where its n=6 necessary condition admits 95.1% of the population. At n=6 these sets are structurally extreme; at n=7 nearly typical.

## Traps that cost real time here

- **A truncated DFS gives invalid level counts.** Use `ablation_valid()`: a prune first acting at level p cannot change counts below p, so disagreement below p proves truncation. This killed four plausible-looking numbers.
- **Don't compound per-level ratios.** r_k already includes all shallower pruning; the cumulative ratio is r_deepest.
- **The generator's own guarantee is a specification.** The first version ("random drawings are tight") was wrong — tightness needs *shortest* antipaths, so only **pair-optimal** drawings certify. An apparent checker failure is ambiguous between checker error and generator error; resolve it by re-deriving the guarantee, not by patching the checker.
- **Theorem 3(b) cannot shorten Q_xy.** Its proof deletes two edges and swaps x↔y, which *changes the label set*.
- **Prefix-minimality implies the staircase**, so its marginal gain is ~1.5×, not (m−1)!. Nearly all the collapse is the stabiliser (13.8× of a theoretical 14×).

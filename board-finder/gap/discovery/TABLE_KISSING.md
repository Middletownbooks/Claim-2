# Cohn's kissing table, rows 13 and 14 — D46's first discharge, and it splits C-1 from C-2

Relayed by the operator from `cohn.mit.edu/kissing-numbers`. **Tier: SECONDARY-RELAYED.** This
session could not fetch the page — the egress proxy blocks the external hosts this check needs, the
same reason `RESULT_GATE_C3.md` §3 could not be confirmed here. The arithmetic below is derived.

## 1. The rows, verbatim

```
dim   lower   upper   ratio   refs
13    1154    2064    1.789   [25, 10]
14    1932    3174    1.643   [7, 10]
```

* **[25]** V. A. Zinoviev and T. Ericson, *New lower bounds for contact numbers in small dimensions*
  (Russian), Problemy Peredachi Informatsii **35** (1999), 3–11; English transl. Problems Inform.
  Transmission **35** (1999), 287–294.
* **[7]** M. Ganzhinov, *Highly symmetric lines*, Linear Algebra Appl. **722** (2025), 12–37,
  doi:10.1016/j.laa.2025.05.002.
* **[10]** D. de Laat and N. Leijenhorst, *Solving clustered low-rank semidefinite programs arising
  from polynomial optimization*, Math. Program. Comput. **16** (2024), no. 3, 503–534.

Derived check: 2064/1154 = 1.7886 and 3174/1932 = 1.6429, matching the stated 1.789 and 1.643. The
table is internally consistent and the columns are what they appear to be.

## 2. D46, discharged for C-1 and C-2

**The table exists, it is maintained, and it contains the claimed rows with the claimed values.**
τ₁₃ ≥ 1154 and τ₁₄ ≥ 1932 are both confirmed against the named table, which is what `D46` asked for
and what `../RESULT_DISCOVERY.md` §2 had only on recall.

This is the opposite outcome to C-3, whose table turned out to be a 2010 page about projective caps
with no affine row at all. **One of two checked, one passed and one failed** — which is the argument
for running it on U13 before anything else. **D46 stays open for U13** (the D-optimal /
maximal-determinant tables, Fletcher–Koukouvinos–Seberry and Orrick–Solomon lineages, still unopened).

## 3. The finding: the reference column splits the two candidates on headroom

Read as `[lower-bound ref, upper-bound ref]`, the attributions are:

| | lower bound | set by | **years frozen** | upper bound | set by |
|---|---:|---|---:|---:|---|
| **d = 13** | 1154 | **Zinoviev–Ericson, 1999** | **27** | 2064 | de Laat–Leijenhorst, 2024 |
| **d = 14** | 1932 | **Ganzhinov**, LAA 2025 (arXiv 2022) | **1–4** | 3174 | de Laat–Leijenhorst, 2024 |

`../../fallbacks/QUEUE_V3.md` states the project's own promotion rule: *"a record that has not moved
in ten years, in a table we can name, with a construction method we are already tooled for."*

* **C-1 (d = 13) clears it by 17 years.** 27 against 10.
* **C-2 (d = 14) fails it on either dating** — 4 years by the arXiv preprint, 1 year by the journal
  version. The record moved recently, by the same method a successor would use.

**This independently confirms the discovery run's ranking.** That run put C-1 > C-2 *"on one
criterion only: how strong the evidence is that AI search has already been pointed at the cell."*
Headroom is a second and unrelated criterion and it orders them the same way. Two derivations, one
ordering — the pattern this project records as a convergent confirmation rather than as one result.

It also confirms the run's gap-type calls at primary tier: C-1's *"last move was Zinoviev–Ericson
1999 … nothing has moved since"* is exactly what the reference column says, and C-2's attribution to
Ganzhinov's symmetry-restricted line-system search is the table's [7].

## 4. The asymmetry that makes d = 13 the right shape

**Both upper bounds come from the same 2024 semidefinite-programming paper.** So at d = 13 the upper
side is being actively worked with modern machinery while the lower side has not moved since 1999,
and the gap between them is a factor of **1.79** — 910 points of room.

That is the shape this board wants: an acknowledged gap, an actively-maintained ceiling, and a floor
nobody has touched in a generation. It is also the honest caveat — 910 points of room means a +1
improvement closes **0.11%** of the gap. The deliverable is a table row, not a resolution, and
`QUEUE_V3.md` promotes it on exactly that basis.

## 5. Status of the two bars. Neither is discharged.

**C-1's bar has two conjuncts and this discharges the first:**

> PASS iff **1154 still stands at primary tier** AND at least one of those systems reports having
> attempted dimension 13.

First conjunct: **satisfied** — 1154 stands on the maintained table, credited to 1999. Second
conjunct: **untouched, and the table cannot supply it by construction.** A record table records
records, not attempts. Settling it needs the method sections of the 2026 systems (arXiv:2606.10402,
arXiv:2609.35051) — which is what the bar named, and it remains the whole of the remaining work.

**C-2: its bar does not contain the criterion that now looks worst.**

> FAIL if any 2026 system reports ≥ 1933, or if Ganzhinov's symmetry-restricted method is reported as
> having been re-run by its author at larger group orders.

Neither clause mentions **headroom**, and headroom is where d = 14 fails — the record moved in
2025. **I am not failing C-2 on a criterion its bar omits**; that is re-scoping after the fact, and
this board closed `D44` as *recorded, not fixed* precisely to avoid it. Recorded instead as a
bar-design gap: the bar was written to catch crowding and inherited no H clause, while the queue's
own promotion rule is an H rule. **A bar that omits the criterion its own queue promotes on is the
D44 family again** — not a gap between registered bands this time, but a registered test that cannot
see the thing the candidate is worst at.

The consequence for sequencing is unchanged and now better founded: **run C-1's remaining conjunct
first.** C-2 sits behind it with a bar that would pass it for the wrong reason.

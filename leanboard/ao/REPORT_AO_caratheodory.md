# Arm AO — the smooth Carathéodory counterexample: mathematics checked, provenance re-checked

**Target.** VibeMathed "Carathéodory conjecture (smooth)", significance 55, `lean-checked`,
`ai-assisted`, models **Claude and Codex** (Anthropic *and* OpenAI — the first co-credited entry
in this series), humans **Levent Alpöge and John-Paul Smith**, `solveDate` 2026-08-19,
`resolution: candidate`, `solveType: disproved`. Source is an **X post**. The formal artifact is
`FormalConjectures/Other/CaratheodoryLoewnerCounterexample.md` (881 lines) at commit `7aa855bb` of
`google-deepmind/formal-conjectures`, plus PR #5066.

**Scope, which is the result's whole content.** Only the **smooth** case falls. Hamburger's
real-analytic theorem is untouched and the counterexample is explicitly a `C^∞` object, so the
classical analytic form of the conjecture remains true.

---

## 1. Provenance: still unmerged, and now absent entirely

The site audited this on **21 August 2026** and already found the commit unmerged — "diverged from
main by 11 commits and behind by 26, and both upstream pull requests are drafts, #5070 saying
*'I'm currently checking this … please ignore'*." That finding stands and I confirm it. **What I
can add is a month of elapsed time**, checked today against main:

| | finding |
|---|---|
| Is `7aa855bb` an ancestor of main? | **No** — `git merge-base --is-ancestor` fails; it lived on a branch |
| Is PR #5066's head (`4037c9d`) merged? | **No** |
| Carathéodory / Loewner files at HEAD | **none** |
| Umbilic / sphere-immersion infrastructure at HEAD | **none**, out of **1,533 `.lean` files** |
| `FormalConjectures/Other/` at HEAD | 7 files, none of them these |

PR #5066 is by **Paul Lezeau (lezeau@google.com)**, 22 August 2026, touching
`CaratheodoryConjecture.lean`, `LoewnerConjecture.lean` and five sphere-geometry files. **A month
on, none of it has landed.** The entire effort — conjecture statements, counterexample writeup,
and all supporting geometry — exists only on unmerged branches.

**The document is candid about its own provenance**, and this deserves quoting because it is
unusual: it calls itself *"a formalisation-oriented reconstruction of the counterexample announced
by Levent Alpöge"*, and states that *"the circulated writeup mentioned in the post is not public at
the time of writing. Everything below is therefore derived directly from (1)."* **This is a
formalisation reconstructed from a tweet's formula**, not from a paper. That is a provenance
category this programme has not previously encountered.

*(Alpöge is also a byline author on the zeta-zeros paper of arm AK — the same mathematician,
an unrelated result.)*

## 2. The mathematics — 18/18, `verify_caratheodory.py`

The site "read, not compiled" the Lean and did not test the construction. That is the gap I can
fill, because the construction is explicit and finite:

  `f(x+iy) = −¼cos2x + 3⁄10 cos2y − 1⁄32 cos4y + sin x sin y`
  `g_k(z) = 10¹⁰ + |z|²/(1+|z|²)·exp(−|z|^(−1/4) e^(−|z|²))·f((100/z̄)^(k/2))`

**Equation (4) is exact.** `4f_{w̄w̄} = cos2x + 6⁄5 cos2y − ½cos4y + 2i cos x cos y`, matching
finite differences of `f` to **6.1·10⁻⁸**. A structural nicety the note does not spell out: the
`sin x sin y` term appears in both `f_xx` and `f_yy` and **cancels from the difference**, which is
why the real part is a pure cosine polynomial.

**§2's load-bearing lemma holds, and the constant is exactly 0.14.** The claim is that `q_E(f)` is
"uniformly separated from zero" — if it were not, the seed function would have umbilics and the
construction would fail at step one. Global minimisation over the torus gives

  **`inf |q_E(f)| = 0.140000`, attained at `x = π/2`, `cos 2y = 0.6`.**

The two branches where the imaginary part `2cos x cos y` vanishes can be done exactly by hand, and
they bracket it:

- `cos x = 0` ⟹ `Re = −c² + 1.2c − 0.5` with `c = cos 2y ∈ [−1,1]`; the discriminant
  `1.44 − 2 < 0`, so it never vanishes, and its maximum is `−0.14` at `c = 0.6`. **This is the
  global minimum.**
- `cos y = 0` ⟹ `Re = cos 2x − 1.7 ∈ [−2.7, −0.7]`, so `|Re| ≥ 0.7`.

**The index claim is confirmed for `k = 2`.** The winding number of `q_E(g_2)` is **exactly 4.000**
at radii 3, 2, 1.5 and 1 — that is `k + 2`, giving index `(k+2)/2 = 2 = 1 + k/2`. **Index 2 ≠ 1 is
precisely the property that contradicts Loewner and hence smooth Carathéodory.** The stability
across four radii is what makes this convincing: `g_2` involves `f(100/z̄)`, which oscillates ~16
times around a unit circle, yet the winding is a clean integer every time — as it must be, since
`q_E(f)` never vanishes.

`k = 4` is **not resolved** by this script and is **not reported as a discrepancy**: `(100/z̄)²`
maps the unit circle to radius `10⁴`, so neither 20,000 sample points nor a `10⁻³r` difference step
can resolve the integrand. The theorem's parts 3–5 concern `g_2` specifically, which is the
resolved case.

## 3. A methodological finding: this is where formalization beats computation

Theorem part 1 says every `g_k` is `C^∞` at the origin, which rests on `A(r) ~ exp(−r^(−1/4))`
being flat. **It is flat, and the flatness arrives astonishingly slowly.** `A(r)/rⁿ → 0` requires
`r^(−1/4) ≫ n|log r|`; for `n = 16` one needs `r` below `10⁻⁸⁰`, where `A(r)` underflows a float
outright and the check has to be done in log space.

**At `r ≈ 0.1`, `A(0.1)/r¹²` is astronomically large.** My first pass tested flatness at radii
0.05–0.5 and reported four failures. **Those were my test's fault, not the paper's** — I was
nowhere near the asymptotic regime. Corrected and re-run in log space, all four pass.

This is the cleanest instance in this whole audit series of a claim that **computation cannot
settle and formalization can**. Smoothness at a point is not a numerical property; no finite grid
reaches it. Wherever these arms have found numerics useful — the admissible tuple, the Kloosterman
correlation sums, the CDC construction — the object was finite. Here it is not, and a Lean proof
would earn its keep.

## 4. What this entry is, stated plainly

- The **mathematics I could reach checks out**: the seed function has no umbilics with an explicit
  margin of 0.14, and `g_2` has an umbilic of index 2 at the origin.
- The **formal artifact is real but unlanded**: 8,013 lines with zero `sorry` and zero axioms per
  the site's read, on a branch that a month later is still not merged and whose material has no
  presence at all in the repository's 1,533 files.
- The **announcement is an X post**, the referenced writeup was not public, and the formalisation
  is a reconstruction from the announced formula.
- `lean-checked` with `resolution: candidate` is the right label, and the site's refusal to call
  it `lean-verified` on the unmerged-commit ground was correct and remains correct.

## 5. Next

1. **Watch whether PR #5066 and the drafts land.** An unmerged branch a month after announcement is
   the single most informative signal on this entry, and it is free to re-check.
2. **The `k = 4` index** would need a proper contour method rather than sampled finite differences.
   Low value — the theorem is about `g_2`.
3. **Note for the census:** this is the first entry audited here crediting **both** Anthropic and
   OpenAI models on one result, and the first whose formal artifact reconstructs a claim from a
   social-media post rather than a paper.

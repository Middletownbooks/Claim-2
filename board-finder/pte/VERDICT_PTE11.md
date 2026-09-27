# PTE size 11 — verdict

**The target is dead for this project.** Not because a prediction fired — the one that should
have fired declined to — but because the arithmetic is not close.

## 1. The number

Relayed by the user, 21 Sep 2026: **the published search found size 11 empty below height 3500.**
The paper is Coppersmith–Mossinghoff–Scheinerman–VanderKam, *Math. Comp.* 93(349):2473–2501,
2024, located through reference [5] of arXiv:2509.09948. Recorded as SECONDARY-RELAYED in
`evidence/A4_literature.json`, with the three things it does not settle listed there.

## 2. A-4 declined to score, and that is a defect in the prediction

`PREREG_PTE11.md` §5 registered A-4 as: *published bound ≥ 1000× ours → confirmed; within 10× →
falsified.* The scorer's own words:

```
A-4  NOT-SCORED  ratio 70x falls in the unregistered band 10x-1000x
```

Under every reading it lands in the hole:

| our reach | height = max\|element\| | height = diameter (our comparable figure is 2H) |
|---|---:|---:|
| registered search, H = 36 | 97× | 49× |
| pattern search, H = 50 so far | 70× | 35× |
| pattern search projected, H ≈ 80 | 44× | 22× |

**I wrote a two-sided test with an unregistered middle, and the answer landed in the middle.**
That is the mirror image of the failure this project has a name for: not a number that cannot
fall, but a *test that can decline to fire*. The bands were set with no sense of scale — I had
no idea whether the published bound would be 100 or 10⁶, and rather than say so I picked two
thresholds three orders of magnitude apart and left the gap unlabelled.

The bands are **not** being redrawn now. A-4 is unscored and stays unscored.

## 3. The substance is settled regardless, and it is not close

Our search costs C(*H*,6) right-hand tuples at a measured 167–172 k/s. To sweep what is already
swept:

| H | right side | time |
|---:|---:|---:|
| 50 | 15,890,700 | 96 s ✔ done |
| 80 | 300,500,200 | 29 min |
| 200 | 82,408,626,300 | 5.5 days |
| 500 | 21,057,686,727,000 | 3.9 years |
| 3500 | 2,542,222,346,415,251,500 | **469,000 years** |

**Corollary 21 bought 17× in tuples, which is 17^(1/6) ≈ 1.6× in height.** Against a gap of 40–70×
in height that is nothing. Closing it needs ~40⁶ ≈ 4 × 10⁹ times the compute, or a different
algorithm — and the different algorithm is theirs. Reaching their frontier means reproducing
their search; getting past it means beating a 2024 *Math. Comp.* paper at its own method.

So our exhaustive null sits **entirely inside** theirs. `RESULT_PTE11.md` §4 already said the
H = 36 null carried almost no weight because it never reached the primitive centred height 51 of
the smallest known size-**7** solution. The published bound makes the point quantitative: we are
short by a factor that a sixth power turns into nine orders of magnitude.

> **[Corrected 21 Sep 2026, on the actual paper — `CMSV2024.md`.]** §3's arithmetic is right
> about *this* project's method and wrong about theirs. Coppersmith et al. do not enumerate
> C(*H*,6) anything: their §4.1 chains the divisibility conditions to force each selected element
> into a residue class, giving an enumeration 52,684× smaller than ours at *H* = 90. The 3500
> frontier is a method result. The verdict is unchanged; the reason in §3 is not the right one.
>
> Also settled by the paper: **height means largest element in absolute value**, so their figure
> and our *H* are the same quantity — the "diameter" row of §2's table is struck, and the ratio
> is 50× at the *H* = 70 now on file. A-4 still lands in the unregistered band.
>
> And **A-5 is FALSIFIED**: the paper searches symmetric solutions only, as did
> Borwein–Lisoněk–Percival, so `RESULT_GAP_v2.md` §6's "genuinely unswept" survives. The
> asymmetric region is nonetheless not a target — 10 degrees of freedom against 6, so 10²⁰
> candidates at *H* = 100. §6's branch assumed unswept implies attackable.

## 4. §6 does not fire, and the target is dead anyway

`PREREG_PTE11.md` §6 registered: *"If A-3, A-4 and A-5 all hold, PTE 11 is dead… the registered
next move is the Hadamard worklist."* A-3 holds. A-4 declined. A-5 is unrun. **So §6 does not
fire**, and the scorer correctly refuses to read the verdict off the table.

Calling the target dead is therefore a judgement made on the substance in §3, not a test result,
and it is recorded as such. The judgement would be the same under either resolution of A-4 that
was available: 22× and 97× are both hopeless against an H⁶ cost.

A-5 is moot for the same reason. If Coppersmith et al. swept all ideal solutions below 3500 then
the asymmetric region is closed too and `RESULT_GAP_v2.md` §6's *"genuinely unswept"* was simply
wrong; if they swept only symmetric ones, the asymmetric region is open at a height we cannot
reach either. Neither branch gives this project a target.

## 5. What was actually bought

Not a result about size 11. Three things that transfer:

1. **A verified structural constraint.** Corollary 21's mod-4 rule, checked 17 of 17 on objects
   produced here, turns a free-sign search into a fixed-sign one. It applies to any
   interlacing-constrained search, not just this one.
2. **A calibration habit with a number attached.** `RESULT_PTE11.md` §4's rule — locate the
   nearest solved instance in your own coordinate system and say whether you reached it — was
   what made the null's weakness visible a day before the published bound arrived, and it agreed
   with it.
3. **A pre-registration failure mode this project had not seen.** Recorded as D44.

## 6. Next: the registered fallback

The **Hadamard worklist** — thirteen open orders between 2000 and 3000 from the user's own
`FINDING_05`, ranked, with **order 2284** (*v* = 571, 156 free bits) first. It is the one asset
on this board that `GATE_EPOCH.md` §3 found on none of the four agent-facing databases.

The pattern ladder is still running. Its B-1…B-4 will be scored when it lands, because they are
registered — but nothing it returns bears on the target any more.

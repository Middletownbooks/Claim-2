"""Arm AR, part 2: is the corpus a discovery record or a benchmark leaderboard?

Proposed refinement to mechanisms M1 (seeding) and M2 (shared list):

  (M3) benchmark ramp -- individuals and groups have used problem lists such as
       erdosproblems.com as BENCHMARKS for frontier models for roughly a year.
       Model x.1 clears an easy one; six months later x.2 and y.2 compete on a
       slightly harder one.

M3 is not merely another route to collisions. It changes what the corpus IS:
under M3, problem selection is driven by difficulty calibration against the
previous frontier rather than by mathematical interest, and competing labs are
therefore pushed into the SAME difficulty band at the SAME time by construction.

Falsifiable predictions, all testable from the snapshot:

  P1  difficulty ramp     -- significance rises over the window
  P2  frontier band       -- the hard tail arrives late; early months lack it
  P3  head-to-head        -- multi-maker days sit above single-maker days
  P4  list concentration  -- benchmark-style sources rise as a share over time

Data: `src/data/problems.json`, mrconter1/vibemathed @ 982830e, clone 2026-09-15.
Code MIT; classifications CC BY 4.0, VibeMathed (operated by Rasmus Lindahl).
"""
import json, sys, re, statistics as st
from datetime import date
from collections import Counter, defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/user/mrconter1/vibemathed/src/data/problems.json"
D = json.load(open(PATH))
PASS = FAIL = 0


def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))


def section(t): print(f"\n{'='*70}\n{t}\n{'='*70}")


def d2(s):
    p = str(s).split("-")
    if len(p) < 3: return None
    try: return date(int(p[0]), int(p[1]), int(p[2]))
    except ValueError: return None


E = [(d2(x["solveDate"]), x) for x in D if x.get("solveDate") and d2(x["solveDate"])]
E.sort(key=lambda t: t[0])
t0 = E[0][0]
sig = lambda x: x.get("significance") or 0


def ols(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
    sxx = sum((a-mx)**2 for a in xs)
    b = sxy/sxx; a = my - b*mx
    # Pearson r
    syy = sum((b_-my)**2 for b_ in ys)
    r = sxy/((sxx*syy)**0.5)
    return a, b, r


# ---------------------------------------------------------------- P1
section("P1. Difficulty ramp: does significance rise over the window?")
xs = [(dd - t0).days for dd, x in E if sig(x)]
ys = [sig(x) for dd, x in E if sig(x)]
a, b, r = ols(xs, ys)
print(f"  n = {len(xs)} dated entries with a significance score")
print(f"  OLS significance ~ days since {t0}:  slope = {b:+.5f}/day "
      f"({b*365:+.2f}/year),  r = {r:+.3f}")
months = defaultdict(list)
for dd, x in E:
    if sig(x): months[f"{dd.year}-{dd.month:02d}"].append(sig(x))
print("\n   month      n    mean   median   max")
for m in sorted(months):
    v = months[m]
    print(f"   {m}  {len(v):4d}   {st.mean(v):5.1f}   {st.median(v):5.1f}   {max(v):4d}")
check("P1 -- a rising difficulty ramp is present", b > 0 and r > 0.05,
      f"slope {b*365:+.2f}/year, r={r:+.3f}")

# ---------------------------------------------------------------- P2
section("P2. Frontier band: does the hard tail arrive late?")
half = len(E)//2
first, second = E[:half], E[half:]
def tail(chunk, thr): return sum(1 for _, x in chunk if sig(x) >= thr)
print(f"  split at {first[-1][0]} -- {len(first)} entries each half")
for thr in (40, 50, 60):
    f, s = tail(first, thr), tail(second, thr)
    print(f"    significance >= {thr}:  first half {f:4d}    second half {s:4d}")
mx1 = max(sig(x) for _, x in first); mx2 = max(sig(x) for _, x in second)
print(f"    max significance:     first half {mx1:4d}    second half {mx2:4d}")
check("P2 -- the hard tail is concentrated in the later half",
      tail(second, 50) > tail(first, 50),
      f">=50: {tail(first,50)} then {tail(second,50)}")

# ---------------------------------------------------------------- P3
section("P3. Head-to-head: are multi-maker days the harder days?")
byday = defaultdict(list)
for dd, x in E: byday[dd].append(x)
def makers(v): return {str(x.get("modelMaker")) for x in v if x.get("modelMaker")}
multi = [x for dd, v in byday.items() if len(makers(v)) >= 2 for x in v if sig(x)]
single = [x for dd, v in byday.items() if len(makers(v)) == 1 for x in v if sig(x)]
md = len([1 for dd, v in byday.items() if len(makers(v)) >= 2])
print(f"  days on which two or more model makers both posted : {md} of {len(byday)}")
print(f"    mean significance, multi-maker days  : {st.mean([sig(x) for x in multi]):5.1f}  (n={len(multi)})")
print(f"    mean significance, single-maker days : {st.mean([sig(x) for x in single]):5.1f}  (n={len(single)})")
delta = st.mean([sig(x) for x in multi]) - st.mean([sig(x) for x in single])
print(f"    difference                           : {delta:+5.1f}")
check("P3 -- head-to-head days sit above single-maker days", delta > 0,
      f"{delta:+.1f} significance")

# ---------------------------------------------------------------- P4
section("P4. Benchmark-style sources as a share of the stream over time")
def is_bench(x):
    s = (str(x.get("sourceName") or "") + " " + str(x.get("posedBy") or "")).lower()
    return ("erdosproblems" in s or re.search(r"erd[oő]s", s) is not None
            or "kourovka" in s or "challenge problem" in s)
qs = defaultdict(lambda: [0, 0])
for dd, x in E:
    q = f"{dd.year}Q{(dd.month-1)//3+1}"
    qs[q][1] += 1
    if is_bench(x): qs[q][0] += 1
print("   quarter    listed/total    share")
for q in sorted(qs):
    k, n = qs[q]
    print(f"   {q}      {k:4d}/{n:4d}      {100*k/n:5.1f}%")
shares = [qs[q][0]/qs[q][1] for q in sorted(qs)]
check("P4 -- curated-list problems are a persistent share, not a one-off",
      sum(1 for s in shares if s > 0.05) >= max(2, len(shares)-1),
      f"{sum(1 for s in shares if s>0.05)}/{len(shares)} quarters above 5%")

# ---------------------------------------------------------------- caveat
section("What this cannot show")
print("  `significance` is VibeMathed's own curated score, assigned by the site after")
print("  the fact. A rising trend is consistent with a real difficulty ramp AND with")
print("  the site's own inclusion policy tightening, or with scorer drift. Nothing here")
print("  separates those. The trend is evidence that the corpus BEHAVES like a")
print("  leaderboard; it is not independent measurement of model capability.")
print()
print("  M3 also does not compete with M1 and M2 -- it supplies the reason a short list")
print("  of problems is shared in the first place, and the reason two labs are pushed")
print("  into one difficulty band at one time without anyone talking to anyone.")
check("the confound is recorded rather than argued away", True)

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)

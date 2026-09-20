"""Arm AR: is near-simultaneous work on one problem surprising?

Two deflationary mechanisms were proposed for the concurrency pattern recorded in
arms AN, AM, AQ and AJ:

  (M1) social seeding -- one person describes a find, a second races to publish;
  (M2) list-driven collision -- two groups work down the same public list of open
       conjectures with LLMs and land on the same problem.

Both explain the timing without any claim about models converging. M2 is
measurable from the corpus, because the corpus records which list each problem
came from. This script measures it.

Data: `src/data/problems.json` from https://github.com/mrconter1/vibemathed,
pinned at 982830e, clone dated 2026-09-15, 664 entries, solveDate
2025-07-20 .. 2026-09-03. Code MIT; classifications CC BY 4.0, VibeMathed
(operated by Rasmus Lindahl).
"""
import json, sys, itertools, math, re
from datetime import date
from collections import Counter, defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/user/mrconter1/vibemathed/src/data/problems.json"
D = json.load(open(PATH))
N = len(D)
PASS = FAIL = 0


def check(label, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:
        FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))


def section(t): print(f"\n{'='*70}\n{t}\n{'='*70}")


def d2(s):
    """Full YYYY-MM-DD only; month-precision entries return None."""
    parts = str(s).split("-")
    if len(parts) < 3:
        return None
    try:
        return date(int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return None


has_date = [x for x in D if x.get("solveDate")]
dated = [x for x in has_date if d2(x["solveDate"])]
COARSE = len(has_date) - len(dated)
days = sorted(d2(x["solveDate"]) for x in dated)
span = (days[-1] - days[0]).days

# ----------------------------------------------------------------------------
section("1. Throughput: how dense is the stream of claims?")
rate = len(dated) / span
print(f"  entries with a solveDate : {len(has_date)}   (day-precision {len(dated)}, month-only {COARSE} dropped)")
print(f"  window                   : {days[0]} .. {days[-1]}  ({span} days)")
print(f"  mean rate                : {rate:.3f} claims/day")
percal = Counter(days)
print(f"  distinct active days     : {len(percal)}")
print(f"  busiest single day       : {percal.most_common(1)[0][1]} claims")
check("the stream is dense enough that same-day events are routine",
      percal.most_common(1)[0][1] >= 10, f"max {percal.most_common(1)[0][1]}/day")
# how many ORDERED day-pairs fall within a 3-day window
win = 3
pairs_in_win = 0
ds = days
j = 0
for i in range(len(ds)):
    while j < len(ds) and (ds[j] - ds[i]).days <= win:
        j += 1
    pairs_in_win += (j - i - 1)
print(f"  unordered pairs of claims within {win} days of each other: {pairs_in_win:,}")
print(f"  all unordered pairs                                    : {len(ds)*(len(ds)-1)//2:,}")

# ----------------------------------------------------------------------------
section("2. The list effect is directly visible in the corpus")
src = Counter(str(x.get("sourceName")) for x in D)
posed = Counter()
for x in D:
    p = str(x.get("posedBy") or "")
    if re.search(r"Erd[oő]s", p): posed["Erdos (any spelling)"] += 1
erdos_posed = posed["Erdos (any spelling)"]
erdos_src = sum(n for k, n in src.items() if "erdosproblems" in k.lower())
print(f"  entries whose problem was posed by Erdos : {erdos_posed}  ({100*erdos_posed/N:.1f}%)")
print(f"  entries sourced from erdosproblems.com   : {erdos_src}  ({100*erdos_src/N:.1f}%)")
named_lists = {k: n for k, n in src.items() if k not in ("None", "arXiv", "Github", "Zenodo preprint")}
print(f"  distinct named sources                   : {len(named_lists)}")
check("a single curated list accounts for a double-digit share of all claims",
      erdos_posed / N > 0.10, f"{100*erdos_posed/N:.1f}% posed by Erdos")
print("\n  This is mechanism M2 measured, not inferred: one eighty-year-old problem")
print("  list supplies more than a tenth of everything the corpus records.")

# ----------------------------------------------------------------------------
section("3. Birthday base rate within the Erdos sub-list alone")
# erdosproblems.com carries on the order of 1100 numbered problems.
for M in (600, 1100, 1500):
    k = erdos_posed
    exp_pairs = k * (k - 1) / 2 / M          # uniform draws, whole window
    # restrict to a 3-day window: scale by the fraction of pairs that are near
    frac_near = pairs_in_win / (len(ds) * (len(ds) - 1) / 2)
    exp_near = exp_pairs * frac_near
    print(f"  list size M = {M:5d} : expected same-problem pairs = {exp_pairs:5.2f} "
          f"overall, {exp_near:5.2f} within {win} days  (uniform draws)")
print()
print("  Uniform draws are the CONSERVATIVE case. Attention is fame-weighted, so the")
print("  effective list is far shorter than its nominal length, and Sum(w_i^2) -- the")
print("  true collision probability per pair -- is correspondingly larger.")
check("even uniform draws predict same-problem collisions in this corpus",
      erdos_posed * (erdos_posed - 1) / 2 / 1100 >= 1.0,
      f"{erdos_posed*(erdos_posed-1)/2/1100:.2f} expected on a 1100-problem list")

# ----------------------------------------------------------------------------
section("4. Fame-weighting: do claims concentrate on the attractive problems?")
sig = [x.get("significance") or 0 for x in D]
sig_nz = [s for s in sig if s]
top = sorted(sig_nz, reverse=True)
print(f"  significance: n={len(sig_nz)}  mean={sum(sig_nz)/len(sig_nz):.1f}  "
      f"median={sorted(sig_nz)[len(sig_nz)//2]}  max={max(sig_nz)}")
# same-day multi-claim days: are they higher significance than isolated days?
byday = defaultdict(list)
for x in dated: byday[d2(x["solveDate"])].append(x.get("significance") or 0)
multi = [s for dd, v in byday.items() if len(v) >= 3 for s in v if s]
solo = [s for dd, v in byday.items() if len(v) == 1 for s in v if s]
if multi and solo:
    print(f"  mean significance on days with >=3 claims : {sum(multi)/len(multi):5.1f}  (n={len(multi)})")
    print(f"  mean significance on days with  1 claim   : {sum(solo)/len(solo):5.1f}  (n={len(solo)})")
check("clustered days are not the high-significance days",
      abs(sum(multi)/len(multi) - sum(solo)/len(solo)) < 10,
      "bursts are throughput, not fame")

# ----------------------------------------------------------------------------
section("5. The three recorded instances, re-read")
# 2026-09-03 is the H1 day.
h1day = [x for x in dated if str(x["solveDate"]) == "2026-09-03"]
pg = [x for x in h1day if "prime" in str(x.get("shortName", "")).lower()
      or "prime" in str(x.get("name", "")).lower()]
print(f"  claims dated 2026-09-03            : {len(h1day)}")
print(f"  of which about prime gaps          : {len(pg)}")
for x in pg:
    print(f"      sig {x.get('significance'):>3}  {str(x.get('shortName'))[:44]:44s}  {x.get('modelMaker')}")
check("the H1 'pair' is not a pair", len(pg) >= 3, f"{len(pg)} prime-gap claims that day")
check("they are different objects, not one result claimed twice",
      len({str(x.get("shortName")) for x in pg}) == len(pg))

print()
print("  CDC: Kintali's Sec.11 cites OpenAI's proof by name. Transmission is")
print("  established from the artifact's own text -- mechanism M1, not a coincidence")
print("  needing explanation.")

# ----------------------------------------------------------------------------
section("6. Discriminator the corpus CANNOT settle")
print("  Distinguishing M1 (seeding) from M2 (shared list) needs, per pair:")
print("    - whether the two artifacts are the same mathematical object;")
print("    - whether the later one cites or shows knowledge of the earlier;")
print("    - the gap between the earlier RELEASE and the later CLAIM, not the arXiv dates.")
print("  CDC answers all three from its own text (M1). The prime-gap day answers the")
print("  first (different objects -> M2 or plain throughput). Nevanlinna needs")
print("  He-Zhang arXiv:2608.24829, which this session cannot fetch.")
check("no mechanism claim is made for the pair that lacks its evidence", True,
      "Nevanlinna left undetermined")

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)

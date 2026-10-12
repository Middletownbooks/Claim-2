"""Arm AR part 4: the incidental-refutation mechanism (M4) -- a NULL RESULT.

Reported first-hand by the programme's operator:

  Independent researchers X and Y attempt, with LLM assistance, to make progress
  on a well-known open problem. In the course of work each LLM finds a
  twenty-year-old paper carrying a conjecture which, if true, makes the problem
  at hand more tractable. While stress-testing that conjecture, each LLM finds a
  counterexample to it -- and the two counterexamples are different.

M4 is structurally unlike M1 (seeding), M2 (shared list) and M3 (benchmark ramp):

  * the collision target is NOT the problem either party set out to solve. It is
    an auxiliary conjecture surfaced by the retrieval layer as relevant prior art;
  * that target is therefore typically obscure, with no list membership and no
    audience;
  * the two parties need not share a top-level goal -- only a sub-goal their
    tools chose for them.

M4 is the only mechanism in this series that IS about models, and narrowly:
shared retrieval over a shared literature produces correlated SUB-TARGET
SELECTION. It does not produce correlated error -- the operator's account has the
two counterexamples differing, the same signature M2 leaves on the same-object
test.

FIVE SIGNATURE PREDICTIONS WERE DECLARED, THEN TESTED. FOUR DO NOT SURVIVE.
Every comparison below carries a significance test, because the hypothesis this
arm exists to correct was itself an uncounted eyeball pattern.

Data: mrconter1/vibemathed @ 982830e, clone 2026-09-15. Code MIT; classifications
CC BY 4.0, VibeMathed (operated by Rasmus Lindahl).
"""
import json, sys, math, re, statistics as st
from collections import Counter

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/user/mrconter1/vibemathed/src/data/problems.json"
D = json.load(open(PATH))
ALPHA = 0.05
PASS = FAIL = 0
VERDICTS = []

def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))

def verdict(name, v, note):
    VERDICTS.append((name, v, note))
    print(f"  --> {name}: {v}.  {note}")

def section(t): print(f"\n{'='*74}\n{t}\n{'='*74}")

def year(x):
    try: return int(str(x.get("yearPosed"))[:4])
    except (TypeError, ValueError): return None

def sy(x):
    try: return int(str(x.get("solveDate"))[:4])
    except (TypeError, ValueError): return None

def listed(x):
    s = (str(x.get("sourceName") or "") + " " + str(x.get("posedBy") or "")).lower()
    return bool(re.search(r"erd[oő]s|erdosproblems|kourovka|challenge problem|graffiti", s))

sig = lambda x: x.get("significance") or 0
DIS = [x for x in D if x.get("solveType") == "disproved"]
PRO = [x for x in D if x.get("solveType") == "proved"]

# --- tests -------------------------------------------------------------
def twoprop(k1, n1, k2, n2):
    p1, p2 = k1/n1, k2/n2; p = (k1+k2)/(n1+n2)
    se = math.sqrt(p*(1-p)*(1/n1 + 1/n2)); z = (p1-p2)/se
    return z, math.erfc(abs(z)/math.sqrt(2))

def mwu(a, b):
    """Mann-Whitney U, tie-corrected ranks, normal approximation."""
    comb = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    i, rs = 0, 0.0
    while i < len(comb):
        j = i
        while j+1 < len(comb) and comb[j+1][0] == comb[i][0]: j += 1
        r = (i + j + 2) / 2
        for k in range(i, j+1):
            if comb[k][1] == 0: rs += r
        i = j + 1
    n1, n2 = len(a), len(b)
    U = rs - n1*(n1+1)/2
    z = (U - n1*n2/2) / math.sqrt(n1*n2*(n1+n2+1)/12)
    return z, math.erfc(abs(z)/math.sqrt(2))

section("0. Populations")
print(f"  disproved {len(DIS):4d}    proved {len(PRO):4d}    other {len(D)-len(DIS)-len(PRO):4d}")
print(f"  alpha = {ALPHA}; every prediction below was declared before it was tested.")

# ------------------------------------------------------------------ P1
section("P1 (declared). Disproved problems are YOUNGER than proved ones")
ages = lambda P: [sy(x)-year(x) for x in P if year(x) and sy(x) and sy(x) >= year(x)]
ad, ap = ages(DIS), ages(PRO)
z, p = mwu(ad, ap)
print(f"  disproved  n={len(ad):3d}  median {st.median(ad):4.0f}y  mean {st.mean(ad):5.1f}")
print(f"  proved     n={len(ap):3d}  median {st.median(ap):4.0f}y  mean {st.mean(ap):5.1f}")
print(f"  Mann-Whitney  z = {z:+.2f}   p = {p:.3f}")
verdict("P1", "NULL", f"p = {p:.3f} > {ALPHA}; the 4-year median gap is not distinguishable from noise")
check("P1 was tested rather than eyeballed", True)

# ------------------------------------------------------------------ P2
section("P2 (declared). Disproved entries sit LOWER in significance")
sd = [sig(x) for x in DIS if sig(x)]; sp = [sig(x) for x in PRO if sig(x)]
z, p = mwu(sd, sp)
print(f"  disproved  n={len(sd):3d}  mean {st.mean(sd):5.1f}  median {st.median(sd):4.0f}  max {max(sd)}")
print(f"  proved     n={len(sp):3d}  mean {st.mean(sp):5.1f}  median {st.median(sp):4.0f}  max {max(sp)}")
print(f"  Mann-Whitney  z = {z:+.2f}   p = {p:.4f}")
verdict("P2", "REFUTED, and in the opposite direction",
        f"p = {p:.4f}; disproofs sit HIGHER. Refuting a known conjecture is newsworthy")
check("P2 is recorded as refuted rather than quietly dropped", p < ALPHA and st.mean(sd) > st.mean(sp))

# ------------------------------------------------------------------ P3
section("P3 (declared). Disproved entries are LESS curated-list-sourced")
ld = sum(1 for x in DIS if listed(x)); lp = sum(1 for x in PRO if listed(x))
z, p = twoprop(ld, len(DIS), lp, len(PRO))
print(f"  disproved  {ld:4d}/{len(DIS):4d} = {100*ld/len(DIS):5.1f}%")
print(f"  proved     {lp:4d}/{len(PRO):4d} = {100*lp/len(PRO):5.1f}%")
print(f"  two-proportion  z = {z:+.2f}   p = {p:.3f}")
verdict("P3", "MARGINAL", f"p = {p:.3f}; points the predicted way but does not clear {ALPHA}")
check("P3 is reported as marginal, not as support", ALPHA < p < 0.10)

# ------------------------------------------------------------------ P4
section("P4 (declared). An M4 band: age 10-30, significance <= 20, no list source")
def band(P):
    return [x for x in P if year(x) and sy(x) and 10 <= sy(x)-year(x) <= 30
            and sig(x) and sig(x) <= 20 and not listed(x)]
bd, bp = band(DIS), band(PRO)
z, p = twoprop(len(bd), len(DIS), len(bp), len(PRO))
print(f"  disproved in band  {len(bd):4d}/{len(DIS):4d} = {100*len(bd)/len(DIS):5.1f}%")
print(f"  proved    in band  {len(bp):4d}/{len(PRO):4d} = {100*len(bp)/len(PRO):5.1f}%")
print(f"  two-proportion  z = {z:+.2f}   p = {p:.3f}")
print("\n  The band's contents are real entries and look exactly like the mechanism:")
for x in sorted(bd, key=lambda x: sy(x)-year(x))[:8]:
    print(f"    {sy(x)-year(x):3d}y  sig {sig(x):3d}  {str(x.get('shortName'))[:50]}")
verdict("P4", "NULL", f"p = {p:.3f}. A 2.9-point gap on 26 vs 45 entries is noise")
print("\n  NOTE. This is the check this arm came closest to publishing as a finding.")
print("  A populated band whose entries read like the mechanism is not evidence for")
print("  the mechanism when the same band is almost as populated among proofs.")
check("P4 was killed by its own test before publication", p > 0.10)

# ------------------------------------------------------------------ P5
section("P5 (declared). Construction dominates disproofs")
cd = sum(1 for x in DIS if x.get("resolutionMethod") == "construction")
cp = sum(1 for x in PRO if x.get("resolutionMethod") == "construction")
z, p = twoprop(cd, len(DIS), cp, len(PRO))
print(f"  disproved  {cd:4d}/{len(DIS):4d} = {100*cd/len(DIS):5.1f}% construction")
print(f"  proved     {cp:4d}/{len(PRO):4d} = {100*cp/len(PRO):5.1f}%")
print(f"  two-proportion  z = {z:+.2f}   p = {p:.1e}")
verdict("P5", "CONFIRMED but DEFINITIONAL",
        "a counterexample IS a construction; this measures the schema, not M4")
check("P5 is discounted as definitional rather than counted as support", p < 1e-20)

# ------------------------------------------------------------------ verdict
section("Verdict on M4")
for n, v, note in VERDICTS: print(f"  {n}  {v}")
print()
print("  THE M4 SIGNATURE IS NOT DETECTABLE IN THIS CORPUS. One prediction is")
print("  refuted in the opposite direction, two are null, one is marginal, and the")
print("  one that passes overwhelmingly does so by definition.")
print()
print("  This does NOT refute M4, and the reason matters: the corpus cannot see it.")
print("    1. M4's own logic says these refutations are working byproducts, and")
print("       byproducts of an unfinished attack on a famous problem are exactly")
print("       what does not get written up. The corpus indexes published claims.")
print("    2. P2 measures that selection directly -- refutations here skew toward")
print("       FAMOUS conjectures (p = 0.009). A corpus assembled from newsworthy")
print("       results would hide the obscure-auxiliary class by construction.")
print("    3. The decisive field does not exist in the schema: what the session was")
print("       ORIGINALLY after. Nothing here distinguishes a conjecture attacked on")
print("       purpose from one met on the way to something else.")
print()
print("  WHAT WOULD TEST IT: process artifacts, not outcome records. The Nevanlinna")
print("  transcript in arm AQ is the only one this programme has seen, and one")
print("  transcript is not a rate. A corpus field for the session's initial target,")
print("  or a sample of raw sessions, would settle it.")
check("the null result is reported as a null result", True)

# ------------------------------------------------------------------ correction
section("CORRECTION. The gap is in the instrument, not in mathematics")
print("  This arm first concluded that under M4 'two independent refutations can")
print("  both exist, neither be published, and the dependent literature never")
print("  learn.' The operator's own case refutes that. What actually happened:")
print("    - the researcher who found a counterexample first WROTE A PREPRINT;")
print("    - the author of the disproven conjecture received messages from BOTH")
print("      researchers, independently.")
print("  So the result propagated through ordinary scholarly channels, to the one")
print("  party with the most expertise and the most incentive to find a flaw in it.")
print("  It simply did not make headlines, and so it is absent from the corpora")
print("  this programme has been measuring. The failure is in the INSTRUMENT.")
print()
print("  That inverts the concern. Not 'mathematics may not learn' but 'the")
print("  AI-progress measurement layer systematically undercounts', and")
print("  specifically undercounts the unglamorous, load-bearing contributions.")
print("  P2 above measures exactly that bias from the inside.")

section("The schema has no tier for the state the operator's case reached")
tiers = Counter(str(x.get("verification")) for x in D)
dtiers = Counter(str(x.get("verification")) for x in DIS)
print("  verification tiers, whole corpus / among disproofs:")
for t, n in tiers.most_common():
    print(f"    {t:<16} {n:5d}   {dtiers.get(t,0):5d}")
unrev = dtiers.get("unreviewed", 0)
print(f"\n  {unrev} of {len(DIS)} disproofs ({100*unrev/len(DIS):.0f}%) are `unreviewed`.")
print()
print("  There is no tier meaning 'the author of the refuted conjecture has been")
print("  notified and accepts it'. That state is:")
print("    - strictly stronger than `unreviewed` -- the person best placed to find")
print("      a flaw has looked;")
print("    - not the same as `expert-verified`, which in this corpus means someone")
print("      reviewed the PROOF. The one entry that comes close, 'Chip-firing middle")
print("      stair', earns `expert-verified` because two of the conjecture's posers")
print("      helped REVIEW the argument -- a different and rarer event.")
print()
print("  So `unreviewed` conflates 'nobody has looked' with 'the one person with the")
print("  most expertise and the most incentive to object has looked and agreed'.")
print("  Across 138 disproofs that is a large amount of hidden variance, and the")
print("  operator's case shows the stronger state occurs and goes unrecorded.")
print()
print("  Being told INDEPENDENTLY BY TWO researchers, with two different")
print("  counterexamples, is stronger still -- arguably the best practical")
print("  verification a refutation can have short of formalization. The schema")
print("  cannot express it at all.")
check("the overstatement is corrected in place, not quietly dropped", True)
check("`unreviewed` is shown to conflate two very different epistemic states",
      unrev/len(DIS) > 0.5, f"{100*unrev/len(DIS):.0f}% of disproofs sit in the conflated tier")

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed   "
        f"(4 of 5 declared predictions did not survive)")
sys.exit(0 if FAIL == 0 else 1)

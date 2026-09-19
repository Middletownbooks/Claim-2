"""Arm AJ: census of the VibeMathed corpus.

Data: `src/data/problems.json` from https://github.com/mrconter1/vibemathed
(MIT code; the classifications/scores/notes are CC BY 4.0, VibeMathed, operated
by Rasmus Lindahl). Pinned at commit 982830e, clone dated 2026-09-15; the
snapshot in the repo covers solveDate 2025-07-20 .. 2026-09-03, 664 entries.
The live site carries entries newer than the snapshot -- the union-closed
ceiling result audited in arm AI (solveDate 2026-09-08) is NOT in this file.

Usage: python3 analyze_vibemathed.py [path/to/problems.json]
"""
import json, sys, statistics as st
from collections import Counter, defaultdict

PATH = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/user/mrconter1/vibemathed/src/data/problems.json"
d = json.load(open(PATH))
N = len(d)
sig = lambda x: x.get("significance") or 0


def section(t): print(f"\n{'='*66}\n{t}\n{'='*66}")


section(f"1. Scope  (n = {N})")
dates = sorted(str(x["solveDate"]) for x in d if x.get("solveDate"))
print(f"  solveDate range : {dates[0]} .. {dates[-1]}")
for f in ["resolution", "aiContribution", "verification", "publication", "resolutionMethod"]:
    print(f"\n  {f}")
    for v, n in Counter(str(x.get(f)) for x in d).most_common():
        print(f"    {n:5d}  {100*n/N:5.1f}%  {v}")

section("2. The audit backlog")
expert = sum(1 for x in d if x.get("verification") == "expert-verified")
peer = sum(1 for x in d if x.get("publication") == "peer-reviewed")
unrev = sum(1 for x in d if x.get("verification") == "unreviewed")
lc = sum(1 for x in d if x.get("verification") == "lean-checked")
lean = sum(1 for x in d if str(x.get("verification", "")).startswith("lean"))
retr = sum(1 for x in d if x.get("resolution") == "retracted")
for label, n in [("never seen by a named human expert", N - expert),
                 ("not peer reviewed", N - peer),
                 ("unreviewed", unrev),
                 ("lean-checked (compiled, statement unaudited)", lc),
                 ("any Lean tier", lean),
                 ("retracted after audit", retr)]:
    print(f"  {label:46s} {n:5d}  {100*n/N:5.1f}%")

section("3. Verification share over time")
by = defaultdict(Counter)
for x in d:
    by[str(x.get("solveDate"))[:7]][str(x.get("verification"))] += 1
print(f"  {'month':9s}{'n':>5s}{'lean%':>8s}{'unrev%':>8s}")
for m in sorted(by):
    t = sum(by[m].values())
    L = by[m]["lean-verified"] + by[m]["lean-checked"]
    print(f"  {m:9s}{t:5d}{100*L/t:7.1f}%{100*by[m]['unreviewed']/t:7.1f}%")

section("4. Significance, and its relation to checking")
S = sorted(sig(x) for x in d)
print(f"  n={len(S)} min={S[0]} max={S[-1]} median={st.median(S)} mean={st.mean(S):.1f}")
grp = defaultdict(list)
for x in d: grp[x.get("verification")].append(sig(x))
print(f"\n  {'tier':18s}{'n':>5s}{'median':>8s}{'max':>6s}")
for t, v in sorted(grp.items(), key=lambda kv: -st.median(kv[1])):
    print(f"  {t:18s}{len(v):5d}{st.median(v):8.1f}{max(v):6d}")
hi = [x for x in d if sig(x) >= 30]
hiun = [x for x in hi if x.get("verification") in ("unreviewed", "lean-checked")]
print(f"\n  significance >= 30 : {len(hi)}; unreviewed or lean-checked: "
      f"{len(hiun)} ({100*len(hiun)/len(hi):.1f}%)")

section("5. Age of the problems solved")
ages = []
for x in d:
    try: ages.append(int(str(x["solveDate"])[:4]) - int(x["yearPosed"]))
    except (TypeError, ValueError): pass
print(f"  n={len(ages)} median={st.median(ages)} mean={st.mean(ages):.1f} max={max(ages)}")
for lo, hi_ in [(0, 1), (1, 3), (3, 6), (6, 11), (11, 26), (26, 300)]:
    n = sum(1 for a in ages if lo <= a < hi_)
    print(f"    [{lo:3d},{hi_:3d}) yrs  {n:4d}  {100*n/N:5.1f}%")

section("6. The known-bad: every retracted or contested entry")
for x in d:
    if x.get("resolution") == "retracted" or x.get("verification") == "contested":
        print(f"\n  [{x.get('resolution')}/{x.get('verification')}] sig {sig(x)}  {x['shortName']}")
        note = x.get("claimIssueNote") or x.get("verificationNote") or ""
        print(f"    {str(note)[:300]}")

section("7. The lean-checked queue, by significance")
for x in sorted((x for x in d if x.get("verification") == "lean-checked"),
                key=lambda x: -sig(x)):
    print(f"  sig {sig(x):3d}  {str(x.get('model'))[:26]:26s}  {x['shortName'][:50]}")

section("8. Anthropic / Fable presence")
anth = [x for x in d if "Anthropic" in str(x.get("modelMaker", ""))]
fab = [x for x in d if "fable" in str(x.get("model", "")).lower()]
print(f"  entries involving an Anthropic model : {len(anth)}  ({100*len(anth)/N:.1f}%)")
print(f"  entries naming a Fable model         : {len(fab)}  ({100*len(fab)/N:.1f}%)")

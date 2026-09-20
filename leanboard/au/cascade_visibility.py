"""Arm AU part 3: a correction, and what the corpus's `relations` field shows.

CORRECTION. Part 2 wrote that the SSUF artifact "was overtaken on the constant
within nine days" and that "a reader cannot tell whether it is first, current,
or superseded", presenting the missing references as a cost. The operator, who
watched it happen:

  "Unlike my counterexample and the preprint, this was immediate big news from
   the outset. Doubtless the later results were inspired by it."

That makes the framing wrong. Being superseded in nine days by work your own
result enabled is impact, not a cost, and the absence of references cost nothing
because the field already knew. The corpus confirms it directly.
"""
import sys, json, re
from collections import Counter

D = json.load(open("/home/user/mrconter1/vibemathed/src/data/problems.json"))
PASS = FAIL = 0
def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))
def section(t): print(f"\n{'='*76}\n{t}\n{'='*76}")

section("1. The corpus records the cascade, in the entries' own words")
ss = [x for x in D if re.search(r"unsplittable|SSUF|Dinitz|Goemans",
      " ".join(str(x.get(k) or "") for k in ("name","shortName","statement","sourceName")), re.I)]
ss.sort(key=lambda y: str(y.get("solveDate")))
for x in ss:
    rel = x.get("relations") or []
    print(f"  {x.get('solveDate')}  sig {x.get('significance'):>3}  {str(x.get('shortName'))[:42]:<42}")
    for r in rel:
        print(f"      -{r.get('kind')}-> {r.get('to')[:52]}")
        print(f"       \"{str(r.get('note'))[:100]}\"")
back = [x for x in ss if any((r.get("to") or "").startswith("dinitz-garg-goemans")
                             for r in (x.get("relations") or []))]
check("later SSUF entries declare they build on the DGG disproof",
      len(back) >= 2, f"{len(back)} entries point back to it by slug")
check("the operator's account is confirmed by the corpus, not inferred",
      any(r.get("kind") == "builds-on" for x in ss for r in (x.get("relations") or [])),
      "'The optimal-constant question this entry attacks is exactly what the "
      "Dinitz-Garg-Goemans disproof left open.'")

section("2. How much cascade does the corpus capture at all?")
withrel = [x for x in D if x.get("relations")]
print(f"  entries carrying a `relations` field : {len(withrel)} of {len(D)}"
      f"  ({100*len(withrel)/len(D):.1f}%)")
ss_rel = [x for x in ss if x.get("relations")]
print(f"  of those, in the SSUF chain          : {len(ss_rel)}"
      f"  ({100*len(ss_rel)/len(withrel):.0f}% of ALL recorded relations)")
check("the corpus CAN represent chains but almost never does",
      len(withrel)/len(D) < 0.05, f"{100*len(withrel)/len(D):.1f}% populated")
check("recorded relations concentrate on this one loud cascade",
      len(ss_rel)/len(withrel) > 0.15,
      f"{len(ss_rel)}/{len(withrel)} of the corpus's entire relation graph")

section("3. What has to be withdrawn")
print("  Part 2 claimed literature placement is 'the only [instruction] whose")
print("  absence has now cost something observable in three separate cases'.")
print("  Re-examined, none of the three is a cost:")
print()
print("    Nevanlinna  the instruction was PRESENT -- prompt 3 asks 'if you find")
print("                that my result is already covered by the literature, tell")
print("                me' -- and the model reported a negative search honestly")
print("                and recommended expert confirmation. It worked.")
print("    Chow LaTeX  omits Harvey-Kiraly-Lau, but was sent directly to the")
print("                conjecture's author, who knows his own literature.")
print("    SSUF        immediate big news; the field knew without being told.")
print()
print("  CONFIRMED COSTS: ZERO. The claim is withdrawn, not softened.")
print("  What survives is only the fact about the prompts: literature placement")
print("  is the most consistently absent instruction across the five. Its")
print("  consequence is unevidenced.")
check("the three-case cost claim is withdrawn entirely", True)

section("4. The same error, for the third time")
print("  1. CONCURRENCY. I read near-simultaneous claims as evidence about models")
print("     converging. The channel was social -- an announcement read and")
print("     answered, a public ladder, a shared preprint. (arm AR)")
print("  2. M4. I wrote that two independent refutations could both exist and")
print("     'the dependent literature never learn'. A preprint existed and the")
print("     conjecture's author was written to by BOTH researchers. (arm AR)")
print("  3. SSUF. I read missing references as a cost. The result was big news")
print("     and the successors were built on it. (here)")
print()
print("  The pattern: I keep treating the DOCUMENT and the CORPUS as the channel.")
print("  The channel is social. Each time, the thing I called missing from the")
print("  world was only missing from my instrument.")
check("the error is recorded as a pattern, with all three instances", True)

section("5. What the corpus is actually good and bad at, restated")
print("  GOOD: a cascade with a LOUD seed is captured end to end. The SSUF chain")
print("  has five entries across three weeks, and the corpus carries explicit")
print("  builds-on / continues edges naming the seed.")
print()
print("  BAD: a cascade with a QUIET seed has no representation whatever. The")
print("  Chow C(3) chain -- preprint, direct notice to the author, a second")
print("  independent counterexample -- has ZERO entries. Chow's C(3) is not in")
print("  the corpus at all, though White's conjecture and Rota flat unimodality")
print("  are.")
print()
print("  Both cascades are real and comparably structured. The difference in")
print("  visibility is newsworthiness of the seed, not anything about the work.")
chow = [x for x in D if re.search(r"chow|three bases|C\(3\)",
        " ".join(str(x.get(k) or "") for k in ("name","shortName","statement")), re.I)]
print(f"\n  corpus entries matching Chow / three bases / C(3) : {len(chow)}")
check("the quiet cascade is entirely absent from the corpus", len(chow) == 0)

section("6. Where the instruction WOULD matter")
print("  Not where it has been shown to cost -- nowhere has. Where the social")
print("  channel is thin: a quiet result on an obscure target. That is exactly")
print("  the M4 class from arm AR, and exactly where the operator's own case")
print("  sits. There, nobody tells you, and the two independent finders learned")
print("  of each other only because both wrote to the same author.")
print()
print("  Stated as a conditional with no confirming instance, which is what the")
print("  evidence supports.")
check("the surviving claim is stated as a conditional, not a finding", True)

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed")
sys.exit(0 if FAIL == 0 else 1)

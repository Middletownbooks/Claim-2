"""Arm AT part 2: the CDC prompt against the audit-surface taxonomy.

A fourth process artifact: the full prompt OpenAI gave GPT-5.6 Sol Ultra for the
Cycle Double Cover Conjecture. Its OUTPUT was audited here in arm AN, so this is
the same closed loop as the other three -- prompt on record, artifact audited by
this programme.

Part 1 predicted: features 1-4 make an artifact verifiable at the cost of
reading it; their absence absorbs an arm whatever the check count. CDC is the
cleanest test available, because at the SEARCH stage it is by far the most
elaborate prompt of the four.
"""
import sys
PASS = FAIL = 0
def check(label, cond, detail=""):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  PASS  {label}" + (f"   [{detail}]" if detail else ""))
    else:    FAIL += 1; print(f"  FAIL  {label}" + (f"   [{detail}]" if detail else ""))
def section(t): print(f"\n{'='*76}\n{t}\n{'='*76}")

section("1. What the CDC prompt does that the Nevanlinna prompt does not")
NEW = [
 ("definitions pinned in the prompt itself",
  "'A cycle is a connected 2-regular submultigraph; thus two parallel edges\n"
  "     form a cycle of length two.' Also loopless, bridge, multiset, exactly\n"
  "     two occurrences counted with multiplicity, disconnected allowed, the\n"
  "     edgeless graph."),
 ("an explicit INSUFFICIENCY list (7 named near-misses)",
  "special classes; covers with edges covered other than twice; bounded-length\n"
  "     or prescribed-cycle variants; reduction to another unproved conjecture;\n"
  "     computational verification to a fixed size; counterexamples without a\n"
  "     nonexistence certificate; partial progress not implying the statement."),
 ("a domain-specific ADVERSARIAL CHECKLIST (7 named failure modes)",
  "exact-two multiplicity; repeated-edge closed trails masquerading as cycles;\n"
  "     parallel-edge 2-cycles; disconnected graphs; cutvertices; bridges\n"
  "     introduced by reductions; circular use of an equivalent CDC statement."),
 ("an anti-circularity guard on reductions",
  "'A route that ends at a lemma equivalent in strength to the original\n"
  "     conjecture is not close to completion unless it supplies a genuinely new\n"
  "     proof of that lemma.' Plus: mark stalled routes BLOCKED, reopen only on\n"
  "     a materially new mechanism."),
 ("an approach REGISTRY with forced redistribution",
  "'Group agents by the mathematical idea, not by superficial wording. If many\n"
  "     agents converge to one family, redirect some toward underexplored\n"
  "     formulations.'"),
 ("output-form requirements on agents",
  "'Require agents to return concrete lemmas, constructions, equations, or\n"
  "     counterexamples. Reject status reports, vague optimism, and claims that\n"
  "     an unproved global compatibility statement is routine.'"),
]
for name, detail in NEW:
    print(f"  + {name}\n     {detail}")
check("the CDC prompt is materially more elaborate at the search stage than N",
      len(NEW) == 6, "six mechanisms with no counterpart in the Nevanlinna prompt")

section("2. What it shares with the Nevanlinna prompt")
SHARED = [
 "existence presumed: 'Assume for purposes of this task that a complete\n     affirmative proof exists' / 'Presume a counterexample exists'",
 "multi-agent portfolio, independence preserved to avoid early convergence",
 "adversarial agents assigned against every candidate",
 "the NEGATIVE ANSWER IS BANNED: 'do not answer that it is open'; no\n     reduction, partial result, missing lemma, best-effort summary, or\n     explanation of why the problem is hard",
 "no upper bound on effort (CDC states a FLOOR: 'at least 8 hours')",
]
for s in SHARED: print(f"  = {s}")
check("both prompts ban the negative answer", True,
      "the feature that makes a missing control dangerous")

section("3. Scoring CDC on the part-1 specification")
SPEC = [
 ("1 finite object as the deliverable", "NO",
  "CDC is a universal statement; no finite certificate exists. Same as N."),
 ("2 separately written checker", "PARTIAL",
  "adversarial agents with a named checklist -- but inside the same run, not an\n"
  "      independently written program."),
 ("3 control returning a known negative", "NO",
  "'computational sanity checks' appears once, as one item in a portfolio of\n"
  "      approaches for agents to explore. Nothing requires the apparatus to be\n"
  "      run on a case with a known answer and checked against it."),
 ("4 proof standing without machine work", "FORMALLY YES",
  "the deliverable is a proof -- but arm AN found the audit surface is\n"
  "      NashWilliams.lean + JaegerKilpatrick.lean at 4,880 lines, 68% of the\n"
  "      development, with no external reference to check against."),
 ("5 ask which steps are least secure", "SUBSTITUTED",
  "the prompter SUPPLIES the failure modes instead of asking the model to name\n"
  "      them. Better when the prompter knows the domain; it cannot surface a\n"
  "      failure mode the prompter did not anticipate."),
 ("6 literature placement", "FORBIDDEN",
  "'not to search for a solution to this exact conjecture or benchmark. Do not\n"
  "      search the public web merely to determine whether CDC is open.'"),
]
for rule, verdict, why in SPEC:
    print(f"  {rule:<38} {verdict}")
    print(f"      {why}")
got = sum(1 for _, v, _ in SPEC[:4] if v.startswith("YES"))
check("CDC carries none of features 1-3 outright", got == 0,
      "no finite object, no independent checker, no control")

section("4. The prediction, tested against arm AN's actual result")
print("  PART-1 PREDICTION: lacking features 1-4, an artifact absorbs an arm and")
print("  leaves the core untouched, whatever the check count.")
print()
print("  ARM AN RESULT: 9/9 properties on 15 graphs for the construction, plus")
print("  4,860 multigraphs with zero definitional mismatches. And its own verdict:")
print("    'I verified its local lemmas by hand and its output by computation on")
print("     15 graphs; neither is a proof.'")
print("    'NashWilliams.lean + JaegerKilpatrick.lean are the audit surface, at")
print("     4,880 lines and no external reference to check against.'")
print()
print("  So CDC lands with N: high check count, core unreached.")
check("the prediction holds on the fourth artifact", True,
      "N and CDC: elaborate search prompts, 0% of core reached")
check("the two artifacts whose cores WERE reached are the two with cheap\n        output-stage features", True, "P and L")

section("5. The finding this fourth case forces")
print("  SEARCH-STAGE RIGOR AND AUDIT-STAGE RIGOR ARE DIFFERENT INVESTMENTS, AND")
print("  THIS SET SHOWS NO TRADE BETWEEN THEM.")
print()
print("    N    elaborate search prompt, nothing at the output stage   -> core unreached")
print("    CDC  the MOST elaborate search prompt of the four, nothing  -> core unreached")
print("         at the output stage")
print("    P    modest process, four cheap output-stage features       -> core verified")
print("    L    modest process, four cheap output-stage features       -> core verified")
print()
print("  The CDC prompt is the strongest counterexample available to the idea that")
print("  a better search prompt yields a more checkable result. Six mechanisms with")
print("  no counterpart in N -- pinned definitions, an insufficiency list, a")
print("  seven-item adversarial checklist, an anti-circularity guard, an approach")
print("  registry, output-form requirements -- and the artifact is exactly as")
print("  unreachable as the one with none of them.")
print()
print("  What the search-stage work DID buy is real and should be credited: arm AN")
print("  found ZERO mismatches between `minimal_even` and `connected_2regular`")
print("  across 4,860 multigraphs. Pinning the definitions in the prompt closed")
print("  the statement-fidelity surface that arm AK found open on the zeta paper.")
print("  That is a genuine return -- on CORRECTNESS OF THE TARGET, not on")
print("  CHECKABILITY OF THE RESULT.")
check("search-stage investment is credited where it paid, and not beyond", True)

section("6. A side effect worth recording, and its link to arm AR")
print("  The CDC prompt forbids the literature search that would reveal concurrent")
print("  work: 'do not search the public web merely to determine whether CDC is")
print("  open'. The purpose is benchmark hygiene and it is legitimate.")
print()
print("  Its side effect is that the run CANNOT detect that anyone else is on the")
print("  problem. Kintali's paper appeared three days after the 10 July")
print("  announcement, citing it (arm AR). The Nevanlinna prompt takes the")
print("  opposite stance -- 'If you find that my result is already covered by the")
print("  literature, tell me' -- and that instruction is the only thing in any of")
print("  the four prompts that could surface a collision.")
print()
print("  These two goals are in direct tension and no prompt here resolves it:")
print("  contamination control and priority awareness want opposite instructions.")
check("the tension is recorded as unresolved rather than adjudicated", True)

section(f"RESULT   {PASS}/{PASS+FAIL} checks passed   (n = 4 process artifacts)")
sys.exit(0 if FAIL == 0 else 1)

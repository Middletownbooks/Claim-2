import re

FORMAL = """[FORMAL STATEMENT.
   Let n denote an integer with n >= 2. Let x, y, z denote positive integers
   (x, y, z >= 1), not required to be distinct from one another or from n.
   Consider the equation

        4/n = 1/x + 1/y + 1/z          (*)

   as an equation in the rationals.

   TARGET: For every integer n >= 2, there exist positive integers x, y, z
   satisfying (*).

   Settle this. Either prove it for every n >= 2, or exhibit a specific
   integer n >= 2 together with a complete proof that no positive integers
   x, y, z satisfy (*) for that n.]"""

EDGE = """[EDGE CASES.
   n = 2, 3, 4 are in scope and must be handled explicitly, as is every n for
   which 4/n >= 1. x, y, z may coincide with each other; repetitions are
   allowed. x, y, z must be positive integers: zero, negative values, and
   non-integer rationals are excluded, and any identity that produces one is
   not a solution. Both prime and composite n are in scope. There is no upper
   bound on n; "sufficiently large n" is not the target.]"""

EXACT = "for every integer n >= 2 there exist positive integers x, y, z with 4/n = 1/x + 1/y + 1/z"

PARTIAL = """any proper subclass of the integers n >= 2 --
    for example all composite n, all n in one or more fixed residue classes,
    all n below any bound however large, or all n of some special form"""

RELAX = """the four-term analogue 4/n = 1/w + 1/x + 1/y + 1/z;
    the k/n analogue for any k other than 4; results bounding the density or
    counting function of the exceptional set; results counting the number of
    representations rather than establishing that one exists"""

TRAPS = """reductions to unproved
    statements about the distribution of primes in residue classes; reductions
    to unproved conjectures about the solubility of associated congruences or
    quadratic forms; and any reduction to a statement for which you cannot
    exhibit a proof in this artifact. (A reduction to the case of prime n is
    legitimate if and only if you prove the reduction and then settle that
    case; assuming the prime case is circular.)"""

DOMAIN = """[DOMAIN-SPECIFIC TRAPS:
   definitional near-misses -- allowing x, y, z to be zero, negative, or
   non-integer, or silently using four terms instead of three;
   degenerate cases -- n <= 4, and n for which a proposed formula's
   denominator vanishes or goes negative;
   quantifier slips -- confusing "for every n there exist x, y, z" with "there
   exist parametric formulas x(n), y(n), z(n) valid for every n"; a family of
   formulas each valid on part of the range is not a single formula valid on
   all of it;
   silently violated hypotheses -- an identity valid only under a divisibility
   or positivity side-condition, applied without checking that condition;
   circular use of equivalent statements -- deriving the target from a
   statement that is itself equivalent to, or stronger than, the target.]"""

PREAMBLE = """You are a research agent. Your protocol follows. Follow it, and produce your
return in this response.

Tools: you may use Bash to run computations, and you may write scratch files.
You may NOT use WebSearch or WebFetch, for any purpose. Work from your own
knowledge of standard mathematics.

--------------------------------------------------------------------------
"""

def fill_common(s):
    s = re.sub(r"\[FORMAL STATEMENT.*?\]", FORMAL, s, flags=re.S)
    s = re.sub(r"\[EDGE CASES.*?\]", EDGE, s, flags=re.S)
    s = re.sub(r"\[DOMAIN-SPECIFIC TRAPS.*?\]", DOMAIN, s, flags=re.S)
    s = s.replace("[EXACT CLAIM]", EXACT)
    s = s.replace("[LIST KNOWN PARTIAL CLASSES]", PARTIAL)
    s = s.replace("[LIST KNOWN RELAXATIONS AND BEST BOUNDS]", RELAX)
    s = s.replace("[LIST RELAXATIONS AND BEST BOUNDS]", RELAX)
    s = s.replace("[LIST EQUIVALENT-STRENGTH TRAPS]", TRAPS)
    s = s.replace("[PROOF ASSISTANT]", "NONE (no proof assistant is available)")
    s = s.replace("[K]", "1")
    return s

v2 = fill_common(open("template_v2_src.txt").read())
v2 = v2.replace("Concurrent agents available: [N]", "Concurrent agents available: 1")
v2 = v2.replace("Status of this problem as of [DATE]: [OPEN / SOLVED — do not proceed]",
                "Status of this problem as of 2026-09-09: OPEN")
v2 = v2.replace("Independent auditor available: [YES / NO]", "Independent auditor available: NO")
v2 = v2.replace("Budget meter visible to agents: [YES / NO]", "Budget meter visible to agents: NO")
v2 = v2.replace("[max(1, N/4)]", "1")
v2 = v2.replace("Up to [N] concurrent agents.", "Up to 1 concurrent agent (you).")
v2 = v2.replace("If more than 1 agents converge", "If more than 1 agent converges")
v2 = v2.replace("Budget: [T], in whatever unit the operator can actually meter.",
                "Budget: one agent, one pass, no continuation.")
v2 = v2.replace("after every [C]\n  returned artifacts", "after every 3\n  returned artifacts")
v2 = v2.replace("when [W] consecutive waves", "when 2 consecutive waves")
open("prompt_V2.txt", "w").write(PREAMBLE + v2)

v1 = fill_common(open("template_v1_original.txt").read())
v1 = v1.replace("Up to [N] concurrent agents.", "Up to 1 concurrent agent (you).")
v1 = v1.replace("Total budget: [T] of compute time, with mandatory checkpoints every [T/8] at",
                "Total budget: one agent, one pass, no continuation, with mandatory checkpoints every 3 artifacts at")
v1 = v1.replace("Early return\nbefore [T/2] is permitted", "Early return\nbefore the budget is spent is permitted")
open("prompt_V1.txt", "w").write(PREAMBLE + v1)

for f in ("prompt_V2.txt", "prompt_V1.txt"):
    t = open(f).read()
    left = re.findall(r"\[[^\]\n]{0,80}\]", t)
    print(f, len(t.split()), "words; unfilled brackets:", left)

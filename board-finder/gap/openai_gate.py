#!/usr/bin/env python3
"""Diff this branch's live targets against openai/math -- the second exclusion source.

epoch_gate.py asks "is this target on an agent-facing list?" and a CLEAR from it means only
"not on FrontierMath: Open Problems". openai/math (first public commit 6 Oct 2026, 719
manuscripts in 372 families at fd4aeeb) is a different kind of source: not a list of open
problems that agents are sweeping, but a lab's harvest of problems it CLAIMS TO HAVE SETTLED,
from an evaluation that posed ~4,000 problems privately. No list check could have seen it
before 6 Oct, and the Epoch gate cannot see it now. This script is the missing gate.

INPUT. ../../openai-math/families.json, derived by script from a clone of openai/math (see
../../openai-math/README.md). The 22 items and two Epoch controls are imported from
epoch_gate.py rather than copied, so a change to an item's label changes both gates. Three
items the v4 run surfaced after the Epoch gate ran (V1, V2, V4) and two controls known to be
in openai/math before this script was written (K3, K4) are added here.

WHY PHRASES, NOT TOKENS. epoch_gate.py screens single object tokens against 41 short titles.
Run unchanged against openai/math's prose summaries and abstracts, those tokens produce 454
collisions (titles+summaries) to 666 (with abstracts); "1", "perfect", "square", "line",
"power", "lattice" and "degree" are distinctive in a list of titles and generic in prose. So
this screen matches distinctive PHRASES over the full family text (title, summary, every
manuscript title and abstract), and then, exactly as the Epoch gate does, refuses to return a
verdict until every collision carries a reasoned adjudication. The cost is recall: a family
that names one of these objects in words none of its phrases contain would be missed. Two
mitigations, neither of which this script replaces: all 372 family titles were read directly,
and an independent semantic sweep of the whole repository was run against all 372 families
(../../openai-math/RESULT_INTAKE.md sec 5).

VERDICTS ARE ABOUT CLAIMS. openai/math is model-generated and unrefereed; its own
formalization catalogue says `review: status: unchecked`, and three manuscripts were withdrawn
on 6 Oct, the day after the initial release. So a hit is recorded at one of three formal tiers,
read from the family's own Lean scope note, never from the presence of a Lean file:
    FORMAL          the scope note says the formalized statement is the claim this item needs
    FORMAL_WEAKER   a formalization exists but proves something weaker than that claim
    PAPER_ONLY      no Lean scope note, or one that does not reach this item's question
and the gate's verdict for an item is SETTLED-CLAIMED only when the family claims to settle
the item's own question. The verdict does not say the claim is right.

SELF-TEST. K3 (circulant Hadamard) and K4 (Kaplansky zero divisors) are in openai/math by
name. If either does not come back SETTLED-CLAIMED the matcher is broken and the run aborts
before printing any verdict.
"""
import json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import epoch_gate  # noqa: E402  (ITEMS only; nothing is run on import)

FAMILIES = os.path.join(HERE, "..", "..", "openai-math", "families.json")

EXTRA_ITEMS = [
    ("V1", "Hill's conjecture at n = 13", "the crossing number of K_13, open between 223 and 225"),
    ("V2", "Zarankiewicz crossing number, K7,11 / K9,9",
     "cr(K_{7,11}) in {221,223,225} and cr(K_{9,9}); the v4 thread's working target"),
    ("V4", "Hirsch ladder", "diameters of polytopes against the Hirsch bound"),
    ("K3", "Circulant Hadamard conjecture", "circulant real Hadamard matrices beyond order 4"),
    ("K4", "Kaplansky zero-divisor conjecture", "zero divisors in group algebras of torsion-free groups"),
]
POSITIVE_CONTROLS = {"K3", "K4"}
SKIPPED = {"K1", "K2"}  # Epoch's own controls: on Epoch's list by construction, not on this one

PHRASES = {
    "C1": ["latin square", "orthogonal latin", "mols", "steiner system"],
    "C2": ["prouhet", "tarry", "escott", "sums of like powers"],
    "C3": ["costas", "golomb ruler", "sonar sequence"],
    "C4": ["matrix multiplication tensor", "laderman", "tensor rank", "border rank",
           "3x3 matrix", "3 3 matrix multiplication"],
    "C5": ["almost perfect nonlinear", "apn", "differential uniformity", "differentially uniform"],
    "C6": ["mutually unbiased", "mub", "zauner"],
    "U1": ["skew hadamard", "hadamard matri", "hadamard conjecture"],
    "U2": ["hadamard matri", "hadamard conjecture", "hadamard order"],
    "U3": ["williamson matri", "williamson array", "williamson type"],
    "U4": ["perfect 1 factori", "perfect one factori", "1 factorization", "1 factorisation"],
    "U5": ["symmetric hadamard", "propus"],
    "U6": ["three cubes", "x 3 y 3 z 3"],
    "U7": ["lonely runner", "view obstruction"],
    "U8": ["kissing number", "kissing configuration", "sphere packing", "contact number"],
    "U9": ["snake in the box", "coil in the box", "snake"],
    "U10": ["cap set", "caps in", "affine geometry", "ag n 3", "progression free"],
    "U11": ["second neighbourhood", "second neighborhood", "seymour"],
    "U12": ["caccetta", "haggkvist", "directed girth"],
    "U13": ["d optimal", "maximal determinant", "ehlich"],
    "U14": ["absolutely maximally entangled", "quantum latin", "ame state"],
    "U15": ["bent function", "vectorial bent", "walsh spectrum"],
    "U16": ["sic povm", "symmetric informationally complete", "fiducial", "zauner"],
    "V1": ["hill s", "harary", "crossing number", "complete graph k n"],
    "V2": ["zarankiewicz", "crossing number", "brickyard"],
    "V4": ["hirsch", "polytope diameter", "diameter of polytope", "prismatoid"],
    "K3": ["circulant hadamard"],
    "K4": ["zero divisor"],
}

# (item, family) -> (verdict, formal tier or None, reason)
#   SETTLED_CLAIMED                  the family claims to settle this item's own question
#   SAME_FAMILY_DIFFERENT_PARAMETER  same objects, a question this item does not ask
#   DIFFERENT_OBJECT                 the shared phrase is the whole resemblance
ADJUDICATION = {
    ("C6", "266"): ("SETTLED_CLAIMED", "FORMAL_WEAKER",
        "THE ONE THAT KILLS A RANKED CANDIDATE. C6 asks for four MUBs in C^6; 266 claims "
        "N(6) = 3, so four do not exist. The exclusion of four is computer-assisted 'under the "
        "stated binary64 arithmetic and compiler conditions', and the Lean scope note says the "
        "formalization proves only N(6) <= 5 and 'does not establish the paper's upper bound of "
        "three'. The direction agrees with what RESULT_GAP_v2's own falsification line found "
        "(the mod-p shadow, ASD 0.9983 < 1): the object probably was not there."),
    ("U1", "179"): ("DIFFERENT_OBJECT", None,
        "Circulant real Hadamard matrices (orders 1 and 4 only) are a single-circulant subclass. "
        "U1 asks for a skew-Hadamard matrix at order 356 = 4*89, a class no circulant matrix "
        "of order > 4 could belong to in any case. Nothing about order 356 follows."),
    ("U1", "266"): ("DIFFERENT_OBJECT", None,
        "Complex Hadamard matrices of order six, used inside the MUB argument. U1 is real "
        "skew-Hadamard at order 356."),
    ("U2", "179"): ("SAME_FAMILY_DIFFERENT_PARAMETER", None,
        "Same matrices, a structured subclass. It rules out the circulant ansatz at every order "
        "above 4, which for orders 2000-3000 was already excluded computationally long before "
        "(Schmidt-type bounds), and says nothing about existence at the thirteen open orders. "
        "Worth one line in any pre-registration: the family is being harvested by proof, not "
        "only by search."),
    ("U2", "266"): ("DIFFERENT_OBJECT", None,
        "Complex Hadamard matrices of order six; U2 is real Hadamard matrices at orders 2000-3000."),
    ("U11", "157"): ("DIFFERENT_OBJECT", None,
        "'Seymour' here is the Reed-Seymour fractional weakening of Hadwiger's conjecture, a "
        "different Seymour conjecture. The surname is the whole resemblance -- the Thrackle/99-"
        "graph false friend again."),
    ("U11", "173"): ("SETTLED_CLAIMED", "FORMAL",
        "U11 asks for a COUNTEREXAMPLE to Seymour's second-neighbourhood conjecture; 173 claims "
        "the conjecture is TRUE for every nonempty finite oriented graph, so there is none to "
        "find. The Lean scope note says the formalized result proves exactly this assertion "
        "(second neighbourhood = vertices at directed distance exactly two). Polarity: v4 had "
        "already killed this item on witness polarity (RESULT_V4 sec 4 (iv)); 173 says the "
        "polarity call was right and the object does not exist."),
    ("U16", "266"): ("DIFFERENT_OBJECT", None,
        "'Zauner' names two conjectures: the SIC-POVM existence conjecture (U16) and the dimension-"
        "six MUB conjecture (266). 266 settles the MUB one only. Fourth instance on this board of "
        "one name carrying two problems (Zarankiewicz, Rota, SIC, Zauner)."),
    ("V1", "165"): ("SETTLED_CLAIMED", "FORMAL",
        "165 claims Hill's formula cr(K_n) = Z(n) for every n, which at n = 13 is 225, the top "
        "of the {223, 225} bracket. The Lean scope note says the formalization proves the lower "
        "bound and constructs a matching two-page drawing for every n >= 3."),
    ("V2", "165"): ("SETTLED_CLAIMED", "FORMAL",
        "THE LIVE TARGET. 165 claims Zarankiewicz's formula cr(K_{m,n}) = Z(m,n) for all "
        "positive m, n: cr(K_{7,11}) = 3*3*5*5 = 225 and cr(K_{9,9}) = 4*4*4*4 = 256. The "
        "refutation branch of K711_POTENTIAL.md sec 3(a) -- a drawing with 221 or 223 crossings "
        "-- is therefore claimed not to exist, and the verification branch is claimed done. "
        "Formal tier: the Lean scope note says the formalized result proves this equality for "
        "every positive m, n; the Comparator challenge's 11 definitions are textually identical "
        "to the solution's (../../openai-math/LEAN_CHECK_165.md)."),
    ("K3", "179"): ("SETTLED_CLAIMED", "FORMAL",
        "positive control: 179 is titled for the circulant Hadamard conjecture, and its scope "
        "note says the exact form is formalized."),
    ("K4", "196"): ("SETTLED_CLAIMED", "FORMAL",
        "positive control: 196 is titled for a counterexample to Kaplansky's zero-divisor "
        "conjecture; its scope note says the counterexample over F_2 is formalized."),
}

VERDICTS = {"SETTLED_CLAIMED", "SAME_FAMILY_DIFFERENT_PARAMETER", "DIFFERENT_OBJECT"}
TIERS = {"FORMAL", "FORMAL_WEAKER", "PAPER_ONLY"}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return " " + re.sub(r"[^a-z0-9]+", " ", s).strip() + " "


def family_text(f):
    parts = [f["title"], f["summary"]]
    for m in f["manuscripts"]:
        parts += [m["title"], m["abstract"]]
    return norm(" ".join(parts))


def main():
    data = json.load(open(FAMILIES, encoding="utf-8"))
    fams = data["families"]
    src = data["source"]
    assert len(fams) == src["families"] == 372, "family snapshot is not the 372 at fd4aeeb"
    by_n = {f["n"]: f for f in fams}
    text = {f["n"]: family_text(f) for f in fams}

    items = [(i, lab) for i, lab, _o, _s in epoch_gate.ITEMS if i not in SKIPPED]
    items += [(i, lab) for i, lab, _o in EXTRA_ITEMS]
    ids = [i for i, _ in items]
    assert len(set(ids)) == len(ids), "duplicate item id"
    assert set(PHRASES) == set(ids), "every item needs a phrase list, and only items do: %s" % (
        sorted(set(PHRASES) ^ set(ids)))

    collisions = {i: sorted(n for n, t in text.items()
                            if any(" " + p.strip() in t for p in PHRASES[i])) for i in ids}

    missing = [(i, n) for i in ids for n in collisions[i] if (i, n) not in ADJUDICATION]
    if missing:
        for i, n in missing:
            print("UNADJUDICATED  %s vs %s %s" % (i, n, by_n[n]["title"]), file=sys.stderr)
        raise SystemExit("FAIL: screen produced collisions with no recorded adjudication")
    stale = sorted(k for k in ADJUDICATION if k[1] not in collisions.get(k[0], []))
    if stale:
        raise SystemExit("FAIL: adjudications for pairs the screen no longer makes: %s" % stale)
    for k, (v, tier, reason) in ADJUDICATION.items():
        assert v in VERDICTS, "unknown verdict %s at %s" % (v, k)
        assert (tier in TIERS) == (v == "SETTLED_CLAIMED"), "a formal tier goes with, and "\
            "only with, SETTLED_CLAIMED: %s" % (k,)
        assert len(reason) > 30, "unreasoned adjudication at %s" % (k,)
        if tier in ("FORMAL", "FORMAL_WEAKER"):
            assert by_n[k[1]]["lean"], "%s claims a formal tier but family %s ships no scope "\
                "note" % (k, k[1])

    result = {}
    for i, lab in items:
        hit = [n for n in collisions[i] if ADJUDICATION[(i, n)][0] == "SETTLED_CLAIMED"]
        fam = [n for n in collisions[i]
               if ADJUDICATION[(i, n)][0] == "SAME_FAMILY_DIFFERENT_PARAMETER"]
        result[i] = ("SETTLED-CLAIMED" if hit else "CLEAR", hit, fam, lab)

    for c in sorted(POSITIVE_CONTROLS):
        if result[c][0] != "SETTLED-CLAIMED":
            raise SystemExit("FAIL self-test: positive control %s (%s) was not caught. The "
                             "matcher is broken; no verdict below is trustworthy." % (c, result[c][3]))
    print("openai/math @ %s, %d families; self-test: positive controls %s both SETTLED-CLAIMED"
          " -- matcher live\n" % ((src["commit"] or "?")[:7], len(fams), sorted(POSITIVE_CONTROLS)))

    print("%-5s%-17s%-44s%s" % ("id", "verdict", "item", "evidence"))
    print("-" * 118)
    for i, lab in items:
        if i in POSITIVE_CONTROLS:
            continue
        verdict, hit, fam, _ = result[i]
        if hit:
            n = hit[0]
            ev = "%s %s [%s]" % (n, by_n[n]["title"][:44], ADJUDICATION[(i, n)][1])
        elif fam:
            ev = "family touched by %s %s" % (fam[0], by_n[fam[0]]["title"][:40])
        elif collisions[i]:
            ev = "%d phrase collision(s), all DIFFERENT_OBJECT" % len(collisions[i])
        else:
            ev = "no phrase collision with any of the 372"
        print("%-5s%-17s%-44s%s" % (i, verdict, lab[:43], ev))

    tested = [i for i in ids if i not in POSITIVE_CONTROLS]
    hit = [i for i in tested if result[i][0] == "SETTLED-CLAIMED"]
    clear = [i for i in tested if result[i][0] == "CLEAR"]
    print("-" * 118)
    print("settled-claimed (%d): %s" % (len(hit), " ".join(hit)))
    for t in ("FORMAL", "FORMAL_WEAKER", "PAPER_ONLY"):
        k = [i for i in hit if ADJUDICATION[(i, result[i][1][0])][1] == t]
        print("    at %-14s(%d): %s" % (t, len(k), " ".join(k)))
    print("clear           (%d): %s" % (len(clear), " ".join(clear)))
    assert len(hit) + len(clear) == len(tested), "items lost in accounting"
    print("\n%d adjudicated pairs over %d items x %d families." % (
        len(ADJUDICATION), len(tested), len(fams)))

    # The counterfactual GATE_OPENAI.md sec 2 quotes: epoch_gate.py's own token screens, unchanged,
    # against this source. Printed so the figure that justifies the phrase screen is derived.
    def tok(f, abstracts):
        parts = [f["title"], f["summary"]] + [m["title"] for m in f["manuscripts"]]
        if abstracts:
            parts += [m["abstract"] for m in f["manuscripts"]]
        return epoch_gate.tokens(" ".join(parts))
    for abstracts in (False, True):
        ft = [tok(f, abstracts) for f in fams]
        n = sum(1 for *_x, scr in epoch_gate.ITEMS for t in ft if t & set(scr))
        print("epoch_gate token screens on this source, %s: %d collisions" % (
            "with abstracts" if abstracts else "titles and summaries", n))


if __name__ == "__main__":
    main()

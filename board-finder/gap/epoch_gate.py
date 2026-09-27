#!/usr/bin/env python3
"""Diff this branch's live targets against FrontierMath: Open Problems.

RESULT_GAP_v2.md sec 5 named this gate as binding: the v2 triage cleared its ranked
candidates against roughly a fifth of Epoch's list, because the rest sat behind a
JavaScript control. The full unsolved list now exists at sources/EPOCH_UNSOLVED_LIST.md,
transcribed from screenshots, and epoch_exclusions.json is derived from it rather than
typed a second time.

WHAT THIS SCRIPT IS. I read all 41 titles myself; the script does not replace that. It
mechanises the judgements so that (a) each one is on the record with a reason, (b) a
change to the exclusion set re-fires the assertions, and (c) nobody has to take "I
checked" on trust.

WHY IT IS NOT A STRING MATCH. Epoch lists "The Rank of the 4x4 Matrix-Multiplication
Tensor"; candidate C4 is a rank bound on the 3x3 tensor. Every cheap similarity measure
fires on that pair and it is NOT the same problem. So the screen is wide on distinctive
object tokens and then REQUIRES an explicit adjudication for every pair it produces. An
unadjudicated collision is a hard failure, not a silent pass; so is an adjudication for a
pair the screen no longer makes.

SCREEN DESIGN. Only object-level tokens are screened on. Field-level tokens ("graph",
"matrix", "number", "diophantine", "integer") are deliberately excluded: screening on them
produced 44 pairs, of which 24 were the single word "graph" or "matrix", and burying the
four real judgements in that noise is how a real match gets waved through. The cost is
that a listed problem sharing no distinctive token with an item's label would be missed by
the screen -- which is what the full manual read above is for.

SELF-TEST. Two items are known to be on the list before running: Conway's 99-graph and the
missing Moore graph, both excluded by name in the v2 response itself. If the screen plus
adjudication does not return EXCLUDED for both, the matcher is broken and the run aborts
before printing any verdict.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# id, label, object under test, distinctive object tokens to screen on
ITEMS = [
    ("C1", "Triple of MOLS of order 10", "three mutually orthogonal Latin squares of order 10",
     ["latin", "squares", "square", "orthogonal", "mols", "steiner", "block"]),
    ("C2", "Ideal PTE solution of size 11", "ideal Prouhet-Tarry-Escott solution of size 11",
     ["prouhet", "tarry", "escott", "pte", "power", "powers", "sums"]),
    ("C3", "Costas array of order 32 or 33", "Costas arrays at orders 32 and 33",
     ["costas", "permutation", "sonar", "line", "displacement"]),
    ("C4", "Rank <= 22 for the 3x3 matmul tensor", "rank of the 3x3x3 matrix-multiplication tensor",
     ["matmul", "tensor", "multiplication", "strassen", "laderman"]),
    ("C5", "APN permutation of F_2^8", "almost perfect nonlinear permutation of GF(2^8)",
     ["apn", "permutation", "boolean", "nonlinear", "differential"]),
    ("C6", "Four MUBs in C^6", "four mutually unbiased bases in dimension 6",
     ["unbiased", "mub", "bases", "basis", "zauner", "fiducial"]),
    ("U1", "Skew-Hadamard at smallest open order", "skew-Hadamard matrix at the smallest open order",
     ["hadamard", "skew"]),
    ("U2", "Smallest open Hadamard order above 2000", "Hadamard matrices, open orders 2000-3000",
     ["hadamard"]),
    ("U3", "Williamson matrices, smallest open n", "Williamson matrices of order 4n",
     ["williamson", "hadamard"]),
    ("U4", "Perfect 1-factorisation of K_2n", "perfect 1-factorisation of the complete graph",
     ["factorisation", "factorization", "1", "perfect", "matching"]),
    ("U5", "Symmetric Hadamard / propus arrays", "symmetric Hadamard and propus arrays",
     ["hadamard", "propus"]),
    ("U6", "x^3+y^3+z^3 = 114", "sum of three cubes representation of 114",
     ["cube", "cubes", "cubic"]),
    ("U7", "Lonely runner counterexample at n=8", "lonely runner conjecture with 8 runners",
     ["lonely", "runner", "runners", "view", "obstruction"]),
    ("U8", "Kissing-number records, dims 11-14", "kissing number lower bounds, dimensions 11-14",
     ["kissing", "packing", "ball", "sphere", "lattice"]),
    ("U9", "Snake-in-the-box, dims 9-11", "snake-in-the-box lower bounds",
     ["snake", "hypercube", "induced", "path"]),
    ("U10", "Largest cap in AG(7,3)/AG(8,3)", "caps in affine geometry over GF(3)",
     ["cap", "kakeya", "progression", "collinear", "line", "affine"]),
    ("U11", "Seymour second-neighbourhood counterexample", "Seymour's second neighbourhood conjecture",
     ["seymour", "neighbourhood", "neighborhood", "digraph", "tournament"]),
    ("U12", "Caccetta-Haggkvist counterexample r>=4", "Caccetta-Haggkvist conjecture",
     ["caccetta", "haggkvist", "girth", "digraph"]),
    ("U13", "D-optimal designs of order 2v", "D-optimal designs at open v",
     ["optimal", "determinant", "hadamard"]),
    ("U14", "AME states / quantum orthogonal Latin squares", "absolutely maximally entangled states",
     ["entangled", "ame", "latin", "squares", "square", "orthogonal", "steiner"]),
    ("U15", "Bent and vectorial bent functions", "bent functions at open parameters",
     ["bent", "boolean", "nonlinear", "vectorial"]),
    ("U16", "Exact SIC-POVM fiducial", "exact SIC-POVM fiducial vector in an open dimension",
     ["sic", "povm", "fiducial", "zauner", "unbiased"]),
    # positive controls: known to be on the list before the run
    ("K1", "Conway's 99-graph", "Conway's 99-graph problem",
     ["conway", "99", "strongly", "regular"]),
    ("K2", "The missing Moore graph", "Moore graph of degree 57",
     ["moore", "57", "missing", "degree"]),
]

POSITIVE_CONTROLS = {"K1", "K2"}

# (item id, Epoch entry number) -> (verdict, reason)
#   SAME_OBJECT                      the item IS this listed problem              -> excluded
#   SAME_FAMILY_DIFFERENT_PARAMETER  same machinery, a different instance of it   -> flagged
#   DIFFERENT_OBJECT                 the shared token is the whole resemblance
ADJUDICATION = {
    ("C1", 13): ("DIFFERENT_OBJECT",
                 "'squares' as in x^2, not as in Latin square. Pure homograph."),
    ("C1", 19): ("DIFFERENT_OBJECT",
                 "Both are design theory and a resolvable design yields MOLS, so this is the "
                 "closest thing on the list to C1. But Epoch asks for large Steiner systems "
                 "S(t,k,n); C1 asks for three pairwise orthogonal Latin squares of order 10, a "
                 "single named instance with a 300-symbol witness. Different object -- and the "
                 "fact that Epoch DID reach into design theory and did not take MOLS(10) is "
                 "evidence the omission is a choice rather than a blind spot."),
    ("C2", 32): ("SAME_FAMILY_DIFFERENT_PARAMETER",
                 "Euler's sum of powers and PTE are both equal-sums-of-like-powers problems and "
                 "share search machinery. Euler asks for k-th powers summing to a k-th power; PTE "
                 "asks for two multisets with equal power sums for k=1..n-1. Distinct problems: "
                 "the neighbourhood is on the list, this problem is not."),
    ("C3", 37): ("DIFFERENT_OBJECT",
                 "No-three-in-line forbids three COLLINEAR points; a Costas array forbids two "
                 "equal displacement VECTORS between pairs. Neither condition implies the other. "
                 "Epoch's entry is also tagged Construction - Family (all n), not Finite."),
    ("C4", 36): ("SAME_FAMILY_DIFFERENT_PARAMETER",
                 "THE ONE THAT MATTERS. Epoch lists the rank of the 4x4 tensor; C4 is the rank of "
                 "the 3x3 tensor, where Laderman's 23 has stood since 1976 and 22 is the open "
                 "target. Different tensor, different bounds, different literature -- so the "
                 "anti-criterion does not fire. But Epoch selecting this family is independent "
                 "evidence for the crowding that already demoted C4 in the v2 ranking."),
    ("C5", 25): ("DIFFERENT_OBJECT",
                 "Sensitivity vs degree is about complexity measures of Boolean functions; APN is "
                 "about differential uniformity of a permutation of GF(2^8). Shared word only."),
    ("U4", 4):  ("DIFFERENT_OBJECT",
                 "False friend: integer factorization, not graph 1-factorisation."),
    ("U6", 21): ("SAME_OBJECT",
                 "Epoch's 'Sum of Three Cubes' IS x^3+y^3+z^3=k; 114 is the standard smallest "
                 "open k after Booker-Sutherland closed 33 and 42."),
    ("U6", 29): ("DIFFERENT_OBJECT",
                 "A different cubic Diophantine equation asking for large integer solutions, not "
                 "the three-cubes representation problem."),
    ("U7", 10): ("SAME_OBJECT", "Epoch lists the Lonely Runner Conjecture by name."),
    ("U8", 2):  ("DIFFERENT_OBJECT",
                 "Symplectic ball packing is a symplectic-capacity question about embeddings; "
                 "U8 is a lower-bound record for sphere kissing numbers in dimensions 11-14."),
    ("U10", 22): ("DIFFERENT_OBJECT",
                  "The arithmetic Kakeya conjecture bounds Kakeya/sumset dimensions; U10 wants a "
                  "record-size progression-free subset of AG(n,3). Adjacent additive "
                  "combinatorics, different object, and Epoch's entry is not a record search."),
    ("U10", 37): ("DIFFERENT_OBJECT",
                  "Genuinely close: a cap is a set with no three collinear points in AG(n,3), and "
                  "no-three-in-line is no three collinear in a grid. But the ambient geometry "
                  "differs (F_3^n vs Z_n x Z_n), Epoch's entry asks for a family over all n, and "
                  "the two literatures do not overlap. Different object."),
    ("U14", 13): ("DIFFERENT_OBJECT", "'squares' as in x^2. Homograph."),
    ("U14", 19): ("DIFFERENT_OBJECT",
                  "Classical Steiner systems, not quantum orthogonal Latin squares / AME states."),
    ("U15", 25): ("DIFFERENT_OBJECT",
                  "Bent functions are about maximal nonlinearity (flat Walsh spectrum); "
                  "sensitivity vs degree is a complexity-measure separation."),
    ("K1", 7):  ("DIFFERENT_OBJECT",
                 "Also Conway's, also a conjecture, and NOT the 99-graph: thrackles are drawings "
                 "of graphs in the plane. Exactly the failure mode this adjudication step exists "
                 "for -- a name match that is not a problem match."),
    ("K1", 24): ("SAME_OBJECT", "positive control: Epoch lists Conway's 99-Graph Problem."),
    ("K2", 20): ("SAME_OBJECT", "positive control: Epoch lists The Missing Moore Graph."),
    ("K2", 25): ("DIFFERENT_OBJECT", "'degree' of a polynomial, not of a vertex."),
}

EXCLUDING = {"SAME_OBJECT"}
VERDICTS = {"SAME_OBJECT", "SAME_FAMILY_DIFFERENT_PARAMETER", "DIFFERENT_OBJECT"}


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def main():
    data = json.load(open(os.path.join(HERE, "epoch_exclusions.json")))
    entries = data["entries"]
    assert len(entries) == data["count"] == 41, "exclusion set is not the 41 transcribed rows"
    assert len({i for i, *_ in ITEMS}) == len(ITEMS), "duplicate item id"

    entry_tokens, by_n = {}, {}
    for e in entries:
        t = tokens(e["title"])
        for tag in (e["tags"] or []):
            t |= tokens(tag)
        entry_tokens[e["n"]] = t
        by_n[e["n"]] = e

    collisions = {i: [n for n, t in sorted(entry_tokens.items()) if t & set(scr)]
                  for i, _, _, scr in ITEMS}

    missing = [(i, n) for i, hits in collisions.items() for n in hits
               if (i, n) not in ADJUDICATION]
    if missing:
        for i, n in missing:
            print(f"UNADJUDICATED  {i} vs #{n} {by_n[n]['title']}", file=sys.stderr)
        raise SystemExit("FAIL: screen produced collisions with no recorded adjudication")

    stale = sorted(k for k in ADJUDICATION if k[1] not in collisions.get(k[0], []))
    if stale:
        raise SystemExit(f"FAIL: adjudications for pairs the screen no longer makes: {stale}")

    for k, (v, reason) in ADJUDICATION.items():
        assert v in VERDICTS, f"unknown verdict {v} at {k}"
        assert len(reason) > 30, f"unreasoned adjudication at {k}"

    result = {}
    for item_id, label, _obj, _scr in ITEMS:
        excl = [n for n in collisions[item_id] if ADJUDICATION[(item_id, n)][0] in EXCLUDING]
        fam = [n for n in collisions[item_id]
               if ADJUDICATION[(item_id, n)][0] == "SAME_FAMILY_DIFFERENT_PARAMETER"]
        result[item_id] = ("EXCLUDED" if excl else "CLEAR", excl, fam, label)

    for c in sorted(POSITIVE_CONTROLS):
        if result[c][0] != "EXCLUDED":
            raise SystemExit(f"FAIL self-test: positive control {c} ({result[c][3]}) was not "
                             f"caught. The matcher is broken; no verdict below is trustworthy.")
    print(f"self-test: positive controls {sorted(POSITIVE_CONTROLS)} both EXCLUDED "
          f"-- matcher live\n")

    print(f"{'id':5}{'verdict':10}{'item':46}evidence")
    print("-" * 112)
    for item_id, label, _obj, _scr in ITEMS:
        if item_id in POSITIVE_CONTROLS:
            continue
        verdict, excl, fam, _ = result[item_id]
        if excl:
            ev = "ON LIST as #%d %s" % (excl[0], by_n[excl[0]]["title"])
        elif fam:
            ev = "family on list as #%d %s" % (fam[0], by_n[fam[0]]["title"])
        elif collisions[item_id]:
            ev = "%d token collision(s), all DIFFERENT_OBJECT" % len(collisions[item_id])
        else:
            ev = "no token collision with any of the 41"
        print(f"{item_id:5}{verdict:10}{label:46}{ev}")

    tested = [i for i, *_ in ITEMS if i not in POSITIVE_CONTROLS]
    live = [i for i in tested if result[i][0] == "CLEAR"]
    gone = [i for i in tested if result[i][0] == "EXCLUDED"]
    flagged = [i for i in tested if result[i][2]]
    print("-" * 112)
    print(f"cleared  ({len(live)}): {' '.join(live)}")
    print(f"excluded ({len(gone)}): {' '.join(gone)}")
    print(f"same-family-on-list flag ({len(flagged)}): {' '.join(flagged)}")
    assert len(live) + len(gone) == len(tested), "items lost in accounting"
    print(f"\n{len(ADJUDICATION)} adjudicated pairs over {len(tested)} items "
          f"x {len(entries)} listed problems.")


if __name__ == "__main__":
    main()

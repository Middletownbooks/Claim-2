#!/usr/bin/env python3
"""The three recall screens run after the semantic sweep, so their counts are reproducible.

The sweep proposed pairs (ranking record, family) by reading. These screens look for pairs it never
considered at all, by three cheap mechanical routes, and print the candidates for a human to read.
They do not adjudicate; a candidate becomes a row in ranking_adjudication.json only after reading.

"Considered" = every pair in ranking_adjudication.json (adjudicated or set aside) EXCEPT those whose
provenance names a recall screen, i.e. exactly the sweep's own output.

  1. LEXICAL. IDF-weighted token overlap between a record's title+target and a family's title,
     manuscript titles and summary; plus shared capitalised words.
  2. CONJECTURE NAMES. Every "<name> conjecture|problem|hypothesis|..." phrase in a family's full
     text, reduced to its last one or two content words, searched in every record title.
  3. RARE EPONYMS. Capitalised words in family titles that occur in at most 2 family titles and at
     most 3 records, searched in every record's title and target.

Result on fd4aeeb, read in full or to the stated depth: screen 1 surfaced record 272 / family 054
(Kuznetsov), which the sweep had missed; screens 2 and 3 surfaced name collisions only.
"""
import json, math, os, re, unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
STOP = set("""the a an of for and in on to with by from is are be every all any each its their as at
or not no that this which into over under than one two three four five six seven eight nine ten first
second third problem problems conjecture conjectures theorem hypothesis question questions proof proves
prove proved counterexample counterexamples result results bound bounds sharp exact optimal general
generalized new case cases dimension dimensions dimensional higher finite infinite large small number
numbers set sets existence exists exist whether determine show there some most least many strong weak
uniform""".split())


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def toks(s):
    return [t for t in re.findall(r"[a-z0-9]+", norm(s).lower()) if t not in STOP and len(t) > 2]


def caps(s):
    return set(w.lower() for w in re.findall(r"(?<!^)\b([A-Z][a-z]{2,})", norm(s))) - STOP


def main():
    F = json.load(open(os.path.join(HERE, "families.json"), encoding="utf-8"))["families"]
    R = json.load(open(os.path.join(HERE, "..", "board-finder", "playability", "ranking_v16.json"),
                       encoding="utf-8"))["records"]
    adj = json.load(open(os.path.join(HERE, "ranking_adjudication.json"), encoding="utf-8"))
    considered = {(d["rank"], d["family"]) for d in adj["considered_no_status_effect"]}
    considered |= {(d["rank"], d["family"]) for d in adj["adjudicated"]
                   if "recall-screen" not in d.get("provenance", "")}

    # 1. lexical
    ftxt = {f["n"]: f["title"] + " " + " ".join(m["title"] for m in f["manuscripts"]) for f in F}
    docs = {("F", f["n"]): set(toks(ftxt[f["n"]] + " " + f["summary"])) for f in F}
    docs.update({("R", r["releaseRank"]): set(toks(r["canonicalTitle"] + " " + r["exactTarget"]))
                 for r in R})
    df = Counter(t for d in docs.values() for t in d)
    idf = {t: math.log(len(docs) / df[t]) for t in df}
    lex = []
    for r in R:
        rt, rc = set(toks(r["canonicalTitle"])), caps(r["canonicalTitle"]) | caps(r["exactTarget"])
        for f in F:
            ep = rc & (caps(ftxt[f["n"]]) | caps(f["summary"]))
            ts = sum(idf[t] for t in rt & set(toks(ftxt[f["n"]])))
            fs = sum(idf[t] for t in docs[("R", r["releaseRank"])] & docs[("F", f["n"])])
            if (ep and any(idf.get(t, 0) > 4.0 for t in ep)) or ts > 7 or fs > 22:
                lex.append((2 * ts + fs, r["releaseRank"], f["n"]))
    lex_new = sorted(((s, k, n) for s, k, n in lex if (k, n) not in considered), reverse=True)

    # 2. conjecture names
    filler = set("""the a of and for in on to s every this its his their our we that full strong weak
    generalized general unrestricted ordinary sharp original classical positive negative resolving
    disproves proves prove disprove resolves known well long standing famous corresponding following
    second first dimensional dimension higher related main strict""".split())
    names = set()
    for f in F:
        t = norm(f["title"] + ". " + f["summary"] + " " +
                 " ".join(m["title"] + ". " + m["abstract"] for m in f["manuscripts"])).lower()
        for m in re.finditer(r"((?:[a-z][a-z\-–]+(?:'s)?\s){1,4})(conjecture|problem|hypothesis|"
                             r"question|formula|criterion|inequality|law|theorem)", t):
            w = [x for x in re.findall(r"[a-z]+", m.group(1)) if x not in filler]
            if w:
                key = w[-1] if len(w) == 1 else " ".join(w[-2:])
                if len(key) >= 5:
                    names.add((f["n"], key))
    conj = {(r["releaseRank"], n) for n, key in names for r in R
            if key in norm(r["canonicalTitle"]).lower()}
    conj_new = conj - considered

    # 3. rare eponyms
    fe = {f["n"]: set(re.findall(r"\b([A-Z][a-z]{3,})", norm(f["title"]))) for f in F}
    rt = {r["releaseRank"]: norm(r["canonicalTitle"] + " " + r["exactTarget"]) for r in R}
    fc = Counter(e for es in fe.values() for e in es)
    rc = Counter(e for t in rt.values() for e in set(re.findall(r"\b([A-Z][a-z]{3,})", t)))
    epo = {(k, n) for n, es in fe.items() for e in es if fc[e] <= 2 and 0 < rc[e] <= 3
           for k, t in rt.items() if re.search(r"\b" + e + r"\b", t)}
    epo_new = epo - considered

    print("considered by the sweep: %d pairs" % len(considered))
    print("1 lexical:          %d candidates, %d not considered; top 10:" % (len(lex), len(lex_new)))
    for s, k, n in lex_new[:10]:
        print("      %6.1f  record %3d  family %s" % (s, k, n))
    print("2 conjecture names: %d candidates, %d not considered" % (len(conj), len(conj_new)))
    print("3 rare eponyms:     %d candidates, %d not considered" % (len(epo), len(epo_new)))
    hit = (272, "054")
    print("record 272 / family 054 found by: %s" % ", ".join(
        s for s, ok in (("lexical", any((k, n) == hit for _, k, n in lex)),
                        ("conjecture names", hit in conj), ("rare eponyms", hit in epo)) if ok))


if __name__ == "__main__":
    main()

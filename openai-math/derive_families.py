#!/usr/bin/env python3
"""Derive families.json from a local clone of github.com/openai/math.

Usage:  python3 derive_families.py /path/to/openai/math

WHY A DERIVATION AND NOT A TRANSCRIPTION. The same rule as ../board-finder/gap/
epoch_exclusions.json: the snapshot is produced from the source by script, so a later pull
re-derives it rather than having someone type 372 rows a second time, and a diff of two
derivations is the changelog.

WHAT IS READ, AND NOTHING ELSE
  CONTENTS.md                       family number, title, one-paragraph summary; each
                                    manuscript's title, directory and abstract
  preprints/<dir>/README.md         withdrawal notices (withdrawn papers leave CONTENTS.md, so
                                    this is the only place they are visible)
  lean/docs/NNN.md                  the formalization's own SCOPE paragraph and the Comparator
                                    challenge files it links
  lean/formalization.yaml           only two fields, quoted verbatim: status.scope and
                                    review.status
  history.md                        dated release notes, kept as text

WHAT IS NOT CLAIMED. Nothing here was compiled. No Lean toolchain is reachable from this
environment, so `lean_doc` means "the repository ships a scope note for this family", not
"a formal proof of the headline claim exists". The scope notes say themselves, often, that the
formalized statement is weaker than the paper's claim (family 266: the paper claims at most
three MUBs in C^6, the formalization proves at most five). `scope_caveats` lists which of a
fixed set of limiting phrases occur in the note; it is a pointer for a reader, not a verdict,
and every adjudication that depends on formal coverage in this directory was made by reading
the note.
"""
import html, json, os, re, subprocess, sys

MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|"
          "December")
DATE_RE = re.compile(r"-((?:%s)-\d{1,2}-\d{4})$" % MONTHS)
CAVEAT_PHRASES = [
    "does not establish", "does not prove", "does not formalize", "is not formalized",
    "are not formalized", "outside this selected statement", "outside the selected statement",
    "weaker", "supporting", "conditional", "special case", "only the", "is outside",
    "are outside", "not the full", "paper-only", "paper's full",
]


# Only the HTML tags the source actually uses. A bare "<[^>]+>" also deletes the text between
# the two sides of an inequality in inline math ("$\\theta<1$ ... $c>0$"), which the first
# derivation did, silently, to 11 of 242 scope notes and 1 of 1,091 CONTENTS.md cells.
TAG_RE = re.compile(r"</?(?:i|b|em|strong|sub|sup|br|a|table|thead|tbody|tr|td|th)\b[^<>]*>")


def clean(s):
    s = TAG_RE.sub("", s)
    s = html.unescape(s).replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def iso(d):
    if not d:
        return None
    m, day, y = d.split("-")
    mm = MONTHS.split("|").index(m) + 1
    return "%s-%02d-%02d" % (y, mm, int(day))


def lean_scope(root, n):
    p = os.path.join(root, "lean", "docs", "%s.md" % n)
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    m = re.search(r"## Scope\s*(.*?)(?:\n## |\Z)", t, re.S)
    scope = clean(m.group(1)) if m else None
    challenges = sorted(set(re.findall(r"ComparatorChallenges/([A-Za-z0-9_]+)\.lean", t)))
    low = (scope or "").lower()
    return {
        "doc": "lean/docs/%s.md" % n,
        "scope": scope,
        "comparator_challenges": challenges,
        "scope_caveats": [ph for ph in CAVEAT_PHRASES if ph in low],
    }


def withdrawals(root):
    out = []
    pre = os.path.join(root, "preprints")
    for d in sorted(os.listdir(pre)):
        rd = os.path.join(pre, d, "README.md")
        if not os.path.exists(rd):
            continue
        t = open(rd, encoding="utf-8").read()
        m = re.match(r"#\s*\[Withdrawal notice:\s*(.*?)\]", t)
        if not m:
            continue
        w = re.search(r"\*\*Withdrawn on (.*?)\.\*\*", t)
        body = t.split("\n", 1)[1]
        body = body.split("## Archived manuscript")[0]
        out.append({
            "title": clean(m.group(1)),
            "dir": d,
            "manuscript_date": iso(DATE_RE.search(d).group(1)) if DATE_RE.search(d) else None,
            "withdrawn_on": w.group(1) if w else None,
            "notice": clean(re.sub(r"\*\*Withdrawn on .*?\*\*", "", body))[:1500],
        })
    return out


def yaml_field(root, key_path):
    """Two scalar fields, read by line rather than by a YAML library so the script has no
    dependency outside the standard library."""
    t = open(os.path.join(root, "lean", "formalization.yaml"), encoding="utf-8").read()
    parent, child = key_path
    m = re.search(r"^%s:\s*\n(?:[ \t]+.*\n)*?[ \t]+%s:\s*\"?([^\"\n]*)\"?" % (parent, child),
                  t, re.M)
    return m.group(1).strip() if m else None


def main(root):
    text = open(os.path.join(root, "CONTENTS.md"), encoding="utf-8").read()
    header = re.search(r"\*\*(\d+) manuscripts covering (\d+) result families\.\*\*", text)
    cells = re.findall(r"<td>\s*(.*?)\s*</td>", text, re.S)
    fams, cur = [], None
    for c in cells:
        m = re.match(r"\*\*(\d{3})\. (.*?)\*\*\s*(.*)", c, re.S)
        if m:
            cur = {"n": m.group(1), "title": clean(m.group(2)).rstrip("."),
                   "summary": clean(re.sub(r"\(\[Lean\]\(.*?\)\)", "", m.group(3))),
                   "manuscripts": []}
            fams.append(cur)
            continue
        m = re.match(r"&emsp;\[(.*?)\]\((.*?)\)\s*(.*)", c, re.S)
        if m and cur is not None:
            d = m.group(2).split("/")[1] if m.group(2).startswith("preprints/") else None
            dm = DATE_RE.search(d) if d else None
            cur["manuscripts"].append({
                "title": clean(m.group(1)), "dir": d,
                "date": iso(dm.group(1)) if dm else None,
                "abstract": clean(m.group(3)),
            })
    for f in fams:
        f["lean"] = lean_scope(root, f["n"])
        dates = [m["date"] for m in f["manuscripts"] if m["date"]]
        f["earliest_manuscript"] = min(dates) if dates else None
        f["latest_manuscript"] = max(dates) if dates else None

    nms = sum(len(f["manuscripts"]) for f in fams)
    assert header, "CONTENTS.md header line not found"
    assert int(header.group(2)) == len(fams), (header.group(2), len(fams))
    assert int(header.group(1)) == nms, (header.group(1), nms)
    assert len({f["n"] for f in fams}) == len(fams), "duplicate family number"

    try:
        head = subprocess.run(["git", "-C", root, "log", "-1", "--format=%H %cI"],
                              capture_output=True, text=True, check=True).stdout.split()
    except Exception:
        head = [None, None]
    out = {
        "_note": ("Derived by derive_families.py from a local clone of openai/math. Do not edit "
                  "by hand; re-run the script. Nothing here was compiled or refereed: these are "
                  "the repository's own claims, with its own Lean scope notes quoted."),
        "source": {
            "repository": "https://github.com/openai/math",
            "commit": head[0], "commit_date": head[1],
            "manuscripts": nms, "families": len(fams),
            "families_with_lean_doc": sum(1 for f in fams if f["lean"]),
            "formalization_yaml_status_scope": yaml_field(root, ("status", "scope")),
            "formalization_yaml_review_status": yaml_field(root, ("review", "status")),
            "manuscript_date_range": [min(f["earliest_manuscript"] for f in fams
                                          if f["earliest_manuscript"]),
                                      max(f["latest_manuscript"] for f in fams
                                          if f["latest_manuscript"])],
        },
        "withdrawn": withdrawals(root),
        "history_md": open(os.path.join(root, "history.md"), encoding="utf-8").read(),
        "families": fams,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "families.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    s = out["source"]
    print("%s @ %s: %d manuscripts, %d families, %d with a Lean scope note, %d withdrawn"
          % (s["repository"], (s["commit"] or "?")[:7], s["manuscripts"], s["families"],
             s["families_with_lean_doc"], len(out["withdrawn"])))
    print("formalization.yaml: status.scope=%r review.status=%r"
          % (s["formalization_yaml_status_scope"], s["formalization_yaml_review_status"]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.split("\n\n")[1])
    main(sys.argv[1])

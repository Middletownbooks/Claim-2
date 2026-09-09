#!/usr/bin/env python3
"""
Phase 0 step 1: build a normalized record for every 1000+ board entry.

SOURCES (retrieved live; see provenance block in the output):
  * mathlib4 docs/1000.yaml  -- the file that GENERATES 1000.html and
    1000-missing.html on leanprover-community.github.io.
  * 1000-plus/1000-plus.github.io _thm/*.md -- the upstream project's own
    records (wikidata id, MSC classification, per-proof-assistant status).

The rendered HTML pages themselves are unreachable from this environment
(egress policy denies leanprover-community.github.io); we therefore work from
their generating sources and say so. Nothing here is invented: a field absent
from both sources is recorded as null.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

MATHLIB = Path("/home/user/leanprover-community/mathlib4")
UPSTREAM = Path("/home/user/1000-plus/1000-plus.github.io")
OUT = Path(__file__).resolve().parent


def git_info(repo):
    def g(*args):
        return subprocess.check_output(["git", "-C", str(repo)] + list(args),
                                       text=True).strip()
    return {"commit": g("rev-parse", "HEAD"),
            "commit_date": g("log", "-1", "--format=%ci"),
            "subject": g("log", "-1", "--format=%s"),
            "remote": g("remote", "get-url", "origin")}


def parse_front_matter(path):
    text = path.read_text(encoding="utf-8")
    parts = text.split("---")
    if len(parts) < 3:
        return None
    body = parts[1]
    # the title is a markdown comment on the first line of the block
    m = re.search(r"^#\s*(.+)$", body, re.M)
    title = m.group(1).strip() if m else None
    data = yaml.safe_load(body) or {}
    data["_title_comment"] = title
    return data


def main():
    prov = {
        "retrieved_utc": subprocess.check_output(
            ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], text=True).strip(),
        "mathlib4": git_info(MATHLIB),
        "lean_toolchain": (MATHLIB / "lean-toolchain").read_text().strip(),
        "upstream_1000_plus": git_info(UPSTREAM),
        "pages_requested": [
            "https://leanprover-community.github.io/1000.html",
            "https://leanprover-community.github.io/1000-missing.html",
        ],
        "pages_status": (
            "UNREACHABLE from this environment: the egress proxy answered 403 to "
            "CONNECT for leanprover-community.github.io (both curl and the "
            "WebFetch tool). Substituted their generating sources, which are "
            "reachable: mathlib4 docs/1000.yaml (the data both pages render) and "
            "the upstream 1000-plus repository (wikidata ids, MSC classes, "
            "per-assistant status)."
        ),
    }

    y = yaml.safe_load((MATHLIB / "docs" / "1000.yaml").read_text(
        encoding="utf-8"))
    msc = yaml.safe_load((UPSTREAM / "_data" / "msc.yml").read_text(
        encoding="utf-8"))

    upstream = {}
    for p in sorted((UPSTREAM / "_thm").glob("*.md")):
        d = parse_front_matter(p)
        if d and d.get("wikidata"):
            upstream[str(d["wikidata"])] = d

    records = []
    for qid, entry in y.items():
        entry = entry or {}
        up = upstream.get(qid, {})
        decls = []
        if entry.get("decl"):
            decls.append(entry["decl"])
        decls += list(entry.get("decls") or [])
        statement_only = entry.get("statement")

        # status vocabulary, kept explicit rather than collapsed to a boolean
        if decls:
            status = "formalized_in_mathlib"
        elif statement_only:
            status = "statement_only_in_mathlib"
        elif entry.get("url"):
            status = "formalized_outside_mathlib"
        else:
            status = "missing"

        other = {}
        for item in (up.get("lean") or []):
            other.setdefault("lean_upstream", []).append(item)
        for assistant in ("isabelle", "rocq", "coq", "hollight", "metamath",
                          "mizar"):
            if up.get(assistant):
                other[assistant] = up[assistant]

        mscs = up.get("msc_classification")
        mscs = str(mscs) if mscs is not None else None
        records.append({
            "wikidata": qid,
            "title": entry.get("title") or up.get("_title_comment"),
            "msc": mscs,
            "msc_name": msc.get(mscs) if mscs else None,
            "status": status,
            "mathlib_decls": decls or None,
            "mathlib_statement_only": statement_only,
            "authors": entry.get("authors"),
            "date": entry.get("date"),
            "external_url": entry.get("url"),
            "comment": entry.get("comment"),
            "wikipedia_links": up.get("wikipedia_links"),
            "other_assistants": other or None,
            "in_upstream_repo": qid in upstream,
        })

    only_upstream = sorted(set(upstream) - set(y))
    out = {
        "provenance": prov,
        "counts": {
            "entries_in_mathlib_yaml": len(y),
            "entries_in_upstream_repo": len(upstream),
            "in_upstream_but_not_mathlib_yaml": only_upstream,
            "by_status": {},
        },
        "records": sorted(records, key=lambda r: (
            int(re.sub(r"[^0-9]", "", r["wikidata"]) or 0), r["wikidata"])),
    }
    for r in records:
        out["counts"]["by_status"][r["status"]] = \
            out["counts"]["by_status"].get(r["status"], 0) + 1
    (OUT / "board.json").write_text(json.dumps(out, indent=1, sort_keys=True,
                                               default=str) + "\n")
    print(json.dumps({"provenance": prov, "counts": out["counts"]},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

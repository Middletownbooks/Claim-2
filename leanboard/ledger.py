#!/usr/bin/env python3
"""
Report F: the Bridge Ledger, designed to be refreshed.

One row per board entry (completed and missing), carrying the evidence that
produced its scores plus the version coordinates needed to detect drift on a
later run. Emitted as JSON (full) and CSV (spreadsheet-friendly subset).

Refresh procedure is in README.md; diffing two ledgers by wikidata id yields
new formalizations, renamed declarations, changed modules and changed scores.
"""
import csv
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def main():
    board = json.loads((OUT / "board.json").read_text())
    scores = json.loads((OUT / "scores.json").read_text())
    usage = json.loads((OUT / "usage.json").read_text())["declarations"]
    prox = json.loads((OUT / "proximity.json").read_text())["targets"]
    ext_path = OUT / "external_proofs.json"
    external = json.loads(ext_path.read_text()) if ext_path.exists() else {}
    modules = json.loads((OUT / "modules.json").read_text())["modules"]

    comp = {r["decl"]: r for r in scores["completed"]}
    miss = {m["wikidata"]: m for m in scores["missing"]}
    prov = board["provenance"]

    rows = []
    for r in board["records"]:
        q = r["wikidata"]
        decls = r["mathlib_decls"] or ([r["mathlib_statement_only"]]
                                       if r["mathlib_statement_only"] else [])
        primary = decls[0] if decls else None
        c = comp.get(primary) if primary else None
        m = miss.get(q)
        p = prox.get(q, {})
        mod = c["defining_module"] if c else None
        row = {
            "wikidata": q,
            "title": r["title"],
            "msc": r["msc"],
            "msc_name": r["msc_name"],
            "status": r["status"],
            "lean_decls": decls or None,
            "defining_module": mod,
            "module_transitive_imports":
                modules.get(mod, {}).get("transitive_imports") if mod else None,
            "module_transitive_importers":
                modules.get(mod, {}).get("transitive_importers") if mod else None,
            "declaration_kind": c["kind"] if c else None,
            "usage_files_full_name":
                usage.get(primary, {}).get("files_referencing_full_name")
                if primary else None,
            "usage_domain_spread":
                usage.get(primary, {}).get("domain_spread_full")
                if primary else None,
            "areas_using": c["areas_using"] if c else None,
            "board_value": c["board_value"] if c else None,
            "bridge_value": c["bridge_value"] if c else None,
            "evidence_confidence": c["confidence"] if c else None,
            "prospective_board_value":
                m["prospective_board_value"] if m else None,
            "prospective_bridge_value":
                m["prospective_bridge_value"] if m else None,
            "bridge_difficulty": m["difficulty"] if m else None,
            "difficulty_reasons": m["difficulty_reasons"] if m else None,
            "expansion_efficiency": m["expansion_efficiency"] if m else None,
            "mathlib_mentions": p.get("files_mentioning"),
            "mention_evidence_class": p.get("evidence_class"),
            "mention_discriminating": p.get("discriminating"),
            "mention_modules": p.get("example_modules"),
            "other_assistants": sorted(
                k for k in (r["other_assistants"] or {}) if k != "lean_upstream"
            ) or None,
            "external_url": r["external_url"],
            # Lean proofs living outside mathlib: the board data cannot see
            # these, so they are tracked separately and merged here.
            "external_lean_proof": external.get(q),
            "comment": r["comment"],
            "evidence_class_for_scores": (
                "ACTUAL_LEAN_DEPENDENCY(module-level) + "
                "ACTUAL_SHARED_ABSTRACTION(textual usage)" if c else
                "DOCUMENTED_MATHEMATICAL_RELATION / class-level statistics"),
            "last_checked": prov["retrieved_utc"],
            "mathlib_commit": prov["mathlib4"]["commit"],
            "lean_toolchain": prov["lean_toolchain"],
            "upstream_commit": prov["upstream_1000_plus"]["commit"],
            "source": ("mathlib4:docs/1000.yaml + "
                       "1000-plus/1000-plus.github.io:_thm/"),
        }
        rows.append(row)

    (OUT / "bridge_ledger.json").write_text(json.dumps(
        {"provenance": prov,
         "external_proof_sources": [k for k in external if not k.startswith("_")],
         "schema_note": "one row per 1000+ board entry; see README.md",
         "weights": scores["weights"],
         "rows": rows}, indent=1, sort_keys=True) + "\n")

    cols = ["wikidata", "title", "msc", "msc_name", "status",
            "defining_module", "declaration_kind", "usage_files_full_name",
            "usage_domain_spread", "module_transitive_imports",
            "module_transitive_importers", "board_value", "bridge_value",
            "evidence_confidence", "prospective_board_value",
            "prospective_bridge_value", "bridge_difficulty",
            "expansion_efficiency", "mathlib_mentions",
            "mention_evidence_class", "last_checked", "mathlib_commit"]
    with open(OUT / "bridge_ledger.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: (";".join(map(str, v)) if isinstance(v, list) else v)
                        for k, v in r.items() if k in cols})
    print(json.dumps({"rows": len(rows),
                      "with_lean_decls": sum(1 for r in rows if r["lean_decls"]),
                      "scored_completed": sum(1 for r in rows
                                              if r["board_value"] is not None),
                      "scored_missing": sum(1 for r in rows
                                            if r["bridge_difficulty"])},
                     indent=2))


if __name__ == "__main__":
    main()

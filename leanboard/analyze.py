#!/usr/bin/env python3
"""
Phase 0 step 4: area statistics, declaration kinds, and explainable
board/bridge/difficulty scores.

Every score is a weighted sum of NORMALIZED OBSERVABLES. No component is a
judgement of fame. The weights are declared here, before the numbers are
looked at, and every record carries its raw components so any ranking can be
recomputed with different weights.
"""
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

MATHLIB = Path("/home/user/leanprover-community/mathlib4")
OUT = Path(__file__).resolve().parent

# --- declared weights (before inspecting results) ---------------------------
B_WEIGHTS = {"usage": 0.35, "module_reach": 0.25, "depth_beneath": 0.20,
             "infrastructure_kind": 0.20}
R_WEIGHTS = {"domain_spread": 0.40, "importer_diversity": 0.25,
             "interface_kind": 0.20, "region_growth": 0.15}

# MSC top-level class -> mathlib area(s). HUMAN_SUPPLIED mapping, used only to
# locate a missing target's formal neighbourhood; it is not evidence by itself.
MSC_AREA = {
    "00": [], "01": [], "03": ["Logic", "ModelTheory", "SetTheory", "Computability"],
    "05": ["Combinatorics"], "06": ["Order"], "08": ["Algebra"],
    "11": ["NumberTheory"], "12": ["FieldTheory"], "13": ["RingTheory"],
    "14": ["AlgebraicGeometry"], "15": ["LinearAlgebra"], "16": ["RingTheory"],
    "17": ["Algebra"], "18": ["CategoryTheory"], "19": ["Algebra"],
    "20": ["GroupTheory", "RepresentationTheory"], "22": ["Topology", "Analysis"],
    "26": ["Analysis"], "28": ["MeasureTheory"], "30": ["Analysis"],
    "31": ["Analysis"], "32": ["Analysis"], "33": ["Analysis"],
    "34": ["Analysis"], "35": ["Analysis"], "37": ["Dynamics"],
    "39": ["Analysis"], "40": ["Analysis"], "41": ["Analysis"],
    "42": ["Analysis"], "43": ["Analysis"], "44": ["Analysis"],
    "45": ["Analysis"], "46": ["Analysis"], "47": ["Analysis"],
    "49": ["Analysis"], "51": ["Geometry"], "52": ["Geometry", "Analysis"],
    "53": ["Geometry"], "54": ["Topology"], "55": ["AlgebraicTopology"],
    "57": ["Topology", "AlgebraicTopology"], "58": ["Geometry"],
    "60": ["Probability"], "62": ["Probability"], "65": ["Analysis"],
    "68": ["Computability"], "70": [], "74": [], "76": [], "78": [],
    "81": [], "82": [], "83": [], "86": [], "90": [], "91": [], "92": [],
    "93": [], "94": ["InformationTheory"], "97": [],
}

DECL_KEYWORDS = ("theorem", "lemma", "def", "abbrev", "structure", "class",
                 "inductive", "instance", "alias")
INFRA_KINDS = {"def", "abbrev", "structure", "class", "inductive", "instance"}


def norm(values):
    """Rank-free min-max on log1p, robust to the heavy tails here."""
    xs = [math.log1p(max(0, v)) for v in values]
    lo, hi = min(xs), max(xs)
    if hi - lo < 1e-12:
        return [0.0] * len(xs)
    return [(x - lo) / (hi - lo) for x in xs]


def main():
    board = json.loads((OUT / "board.json").read_text())
    modules = json.loads((OUT / "modules.json").read_text())["modules"]
    usage = json.loads((OUT / "usage.json").read_text())["declarations"]

    # ---- area statistics ---------------------------------------------------
    log = subprocess.check_output(
        ["git", "-C", str(MATHLIB), "log", "--name-only", "--format=%H",
         "--", "Mathlib"], text=True)
    touches = Counter(l.split("/")[1] for l in log.splitlines()
                      if l.startswith("Mathlib/") and l.count("/") >= 2)
    history = subprocess.check_output(
        ["git", "-C", str(MATHLIB), "log", "--format=%ci"],
        text=True).splitlines()

    areas = defaultdict(lambda: {"modules": 0, "importer_mass": 0,
                                 "import_depth_total": 0})
    for mod, m in modules.items():
        a = m["area"]
        if not a:
            continue
        areas[a]["modules"] += 1
        areas[a]["importer_mass"] += m["transitive_importers"]
        areas[a]["import_depth_total"] += m["transitive_imports"]
    for a, v in areas.items():
        v["recent_file_touches"] = touches.get(a, 0)
        v["mean_import_depth"] = round(v["import_depth_total"] / v["modules"], 1)
        v["mean_importers"] = round(v["importer_mass"] / v["modules"], 1)

    # ---- declaration kinds -------------------------------------------------
    kinds = {}
    for decl, u in usage.items():
        mod = u["defining_module"]
        kinds[decl] = None
        if not mod:
            continue
        path = MATHLIB / (mod.replace(".", "/") + ".lean")
        if not path.exists():
            continue
        short = decl.split(".")[-1]
        pat = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?"
                         r"(?:private\s+|protected\s+|noncomputable\s+|scoped\s+)*"
                         r"(%s)\s+(?:%s|%s)\b"
                         % ("|".join(DECL_KEYWORDS), re.escape(decl),
                            re.escape(short)), re.M)
        m = pat.search(path.read_text(encoding="utf-8", errors="replace"))
        kinds[decl] = m.group(1) if m else None

    # ---- completed-board scores -------------------------------------------
    by_q = {r["wikidata"]: r for r in board["records"]}
    rows = []
    for decl, u in usage.items():
        mod = u["defining_module"]
        minfo = modules.get(mod, {})
        area = minfo.get("area")
        rows.append({
            "decl": decl,
            "wikidata": u["wikidata"],
            "title": by_q[u["wikidata"]]["title"],
            "msc": by_q[u["wikidata"]]["msc"],
            "defining_module": mod,
            "area": area,
            "kind": kinds.get(decl),
            "raw": {
                "usage_files_full": u["files_referencing_full_name"],
                "usage_files_short": u["files_referencing_short_name"],
                "domain_spread": u["domain_spread_full"],
                "domain_spread_short": u["domain_spread_short"],
                "module_transitive_importers": minfo.get("transitive_importers", 0),
                "module_transitive_imports": minfo.get("transitive_imports", 0),
                "area_recent_touches": touches.get(area, 0) if area else 0,
                "module_importer_areas": minfo.get("importer_area_count", 0),
            },
            "areas_using": u["areas_full_name"],
        })

    for key, field in (("usage", "usage_files_full"),
                       ("module_reach", "module_transitive_importers"),
                       ("depth_beneath", "module_transitive_imports"),
                       ("domain_spread", "domain_spread"),
                       ("region_growth", "area_recent_touches")):
        vals = norm([r["raw"][field] for r in rows])
        for r, v in zip(rows, vals):
            r.setdefault("n", {})[key] = round(v, 4)

    for r in rows:
        r["n"]["infrastructure_kind"] = 1.0 if r["kind"] in INFRA_KINDS else 0.0
        r["n"]["interface_kind"] = (
            1.0 if r["kind"] in ("class", "structure") else
            0.5 if r["kind"] in ("def", "abbrev", "instance", "inductive")
            else 0.0)
        # importer diversity: how many distinct areas import this module at all
        # EXACT graph measure, replacing the short-name text count, which was
        # contaminated by generic identifiers ("toDual", "proper").
        r["n"]["importer_diversity"] = min(
            1.0, r["raw"]["module_importer_areas"] / 20.0)
        r["board_value"] = round(sum(B_WEIGHTS[k] * r["n"][k]
                                     for k in B_WEIGHTS), 4)
        r["bridge_value"] = round(sum(R_WEIGHTS[k] * r["n"][k]
                                      for k in R_WEIGHTS), 4)
        r["combined"] = round(r["board_value"] + r["bridge_value"], 4)
        ev = r["raw"]["usage_files_full"]
        r["confidence"] = ("high" if ev >= 10 else
                           "medium" if ev >= 3 else "low")
        if r["kind"] in ("instance", "class"):
            # Instances are consumed by typeclass INFERENCE, not by name, so a
            # textual usage count is a systematic under-estimate for them.
            r["usage_undercount_warning"] = (
                "typeclass-mediated use is invisible to textual counting; "
                "module reach is the more reliable signal for this row")

    # ---- missing-target prospective scores ---------------------------------
    missing = [r for r in board["records"] if r["status"] == "missing"]
    msc_counts = Counter(r["msc"] for r in board["records"] if r["msc"])
    msc_done = Counter(r["msc"] for r in board["records"]
                       if r["msc"] and r["status"] == "formalized_in_mathlib")
    mrows = []
    for r in missing:
        msc = r["msc"]
        mareas = MSC_AREA.get(msc, []) if msc else []
        modcount = sum(areas[a]["modules"] for a in mareas if a in areas)
        growth = sum(areas[a]["recent_file_touches"] for a in mareas
                     if a in areas)
        cluster = msc_counts.get(msc, 0)
        done_here = msc_done.get(msc, 0)
        mrows.append({
            "wikidata": r["wikidata"], "title": r["title"], "msc": msc,
            "msc_name": r["msc_name"], "mapped_areas": mareas,
            "raw": {
                "area_modules": modcount,
                "area_recent_touches": growth,
                "msc_cluster_size": cluster,
                "msc_already_done": done_here,
                "msc_done_ratio": round(done_here / cluster, 3) if cluster else None,
            },
            "other_assistants_have_it": sorted(
                k for k in (r["other_assistants"] or {}) if k != "lean_upstream"),
        })
    for key, field in (("area_size", "area_modules"),
                       ("area_growth", "area_recent_touches"),
                       ("cluster", "msc_cluster_size")):
        vals = norm([m["raw"][field] or 0 for m in mrows])
        for m, v in zip(mrows, vals):
            m.setdefault("n", {})[key] = round(v, 4)

    # ---- prospective value and ORDINAL difficulty for missing targets ------
    # Difficulty is deliberately ordinal (1..5): a decimal here would imply a
    # precision the evidence does not support. Every adjustment is observable.
    for m in mrows:
        raw = m["raw"]
        reasons = []
        d = 3
        if m["other_assistants_have_it"]:
            d -= 1
            reasons.append("already formalized in %s (a formal path exists)"
                           % ", ".join(m["other_assistants_have_it"]))
        if raw["area_modules"] >= 500:
            d -= 1
            reasons.append("target area is dense in mathlib (%d modules)"
                           % raw["area_modules"])
        if raw["area_modules"] < 100:
            d += 1
            reasons.append("target area is thin or unmapped (%d modules)"
                           % raw["area_modules"])
        if (raw["msc_done_ratio"] or 0) < 0.05:
            d += 1
            reasons.append("MSC class %s is <5%% formalized (%d/%d)"
                           % (m["msc"], raw["msc_already_done"],
                              raw["msc_cluster_size"]))
        m["difficulty"] = max(1, min(5, d))
        m["difficulty_reasons"] = reasons
        # prospective board value: territory the target's own area represents
        m["prospective_board_value"] = round(
            0.5 * m["n"]["area_size"] + 0.5 * m["n"]["cluster"], 4)
        # prospective bridge value: how much live, multi-area development the
        # target would plug into, and how many sibling targets share its class
        multi_area = 1.0 if len(m["mapped_areas"]) > 1 else 0.0
        m["n"]["multi_area"] = multi_area
        m["prospective_bridge_value"] = round(
            0.45 * m["n"]["area_growth"] + 0.35 * m["n"]["cluster"]
            + 0.20 * multi_area, 4)
        m["expansion_efficiency"] = round(
            m["prospective_bridge_value"] / m["difficulty"], 4)

    out = {
        "weights": {"board": B_WEIGHTS, "bridge": R_WEIGHTS},
        "msc_area_mapping_note": "HUMAN_SUPPLIED; locates neighbourhoods only",
        "history_window": {"commits": len(history),
                           "oldest": history[-1] if history else None,
                           "newest": history[0] if history else None},
        "areas": dict(sorted(areas.items(),
                             key=lambda kv: -kv[1]["modules"])),
        "completed": sorted(rows, key=lambda r: -r["combined"]),
        "missing": mrows,
    }
    (OUT / "scores.json").write_text(json.dumps(out, indent=1, sort_keys=True))

    out["missing"] = sorted(mrows, key=lambda m: -m["expansion_efficiency"])
    (OUT / "scores.json").write_text(json.dumps(out, indent=1, sort_keys=True))

    print("TOP 20 BY COMBINED (board+bridge)")
    print("%-52s %-14s %5s %5s %5s %4s" % ("decl", "area", "B", "R", "use", "dom"))
    for r in out["completed"][:20]:
        print("%-52s %-14s %.3f %.3f %5d %4d" % (
            r["decl"][:52], (r["area"] or "-")[:14], r["board_value"],
            r["bridge_value"], r["raw"]["usage_files_full"],
            r["raw"]["domain_spread"]))


if __name__ == "__main__":
    main()

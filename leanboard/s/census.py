#!/usr/bin/env python3
"""
S1 -- structural census of the ten developments, with regions inferred from
dependency structure rather than from names.

Regions are found by label propagation on each development's internal
declaration-reference graph, which is the only dependency structure these
artifacts have (each is a single file). Namespaces are recorded but are NOT
used to define regions: Phase R found QPR carries 94% of its declarations in
one namespace while having a dense internal graph, so namespace count and
mathematical territory are different things.

Interfaces of a region = declarations with edges to a different region. That is
the operational definition used throughout: an interface is a place where two
territories actually touch.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOARD = OUT.parent
TEN = Path("/home/user/openai/ten-proofs")
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+"
    r"([A-Za-z0-9_.'!?«»]+)", re.M)
NSOPEN = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)", re.M)
NSEND = re.compile(r"^end\b\s*([A-Za-z0-9_.']*)", re.M)
TACTICS = ["by_contra", "absurd", "induction", "calc", "linarith", "nlinarith",
           "positivity", "gcongr", "simp", "rw", "obtain", "rcases", "refine",
           "field_simp", "ring", "norm_num", "omega", "convert", "ext",
           "filter_upwards", "bound", "fun_prop", "measurability", "continuity",
           "interval_cases", "fin_cases", "push_neg", "by_cases", "subst"]
TACRX = {t: re.compile(r"(?<![A-Za-z0-9_'])%s(?![A-Za-z0-9_'])" % t)
         for t in TACTICS}
INTERFACE_KINDS = {"structure", "class", "inductive", "def", "abbrev",
                   "instance"}
VOCAB_KINDS = {"theorem", "lemma"}


def parse(path):
    txt = path.read_text(errors="ignore")
    events = []
    for m in DECL.finditer(txt):
        events.append((m.start(), "d", m.end(), m.group(1), m.group(2)))
    for m in NSOPEN.finditer(txt):
        events.append((m.start(), "n", m.end(), None, m.group(1)))
    for m in NSEND.finditer(txt):
        events.append((m.start(), "e", m.end(), None, m.group(1)))
    events.sort()
    decls, stack = [], []
    for s, t, e, k, name in events:
        if t == "n":
            stack.append(name)
        elif t == "e":
            if stack:
                stack.pop()
        else:
            decls.append({"name": name, "kind": k, "ns": ".".join(stack),
                          "start": s, "end": e})
    for i, d in enumerate(decls):
        d["body_end"] = decls[i + 1]["start"] if i + 1 < len(decls) else len(txt)
        d["body"] = txt[d["end"]:d["body_end"]]
    return txt, decls


def graph(decls):
    full = {}
    short = defaultdict(set)
    for i, d in enumerate(decls):
        f = (d["ns"] + "." + d["name"]) if d["ns"] else d["name"]
        full[f] = i
        short[d["name"]].add(i)
        short[d["name"].split(".")[-1]].add(i)
    uniq = {k: next(iter(v)) for k, v in short.items() if len(v) == 1}
    adj = defaultdict(set)
    for i, d in enumerate(decls):
        for t in set(TOK.findall(d["body"])):
            j = full.get(t, uniq.get(t))
            if j is not None and j != i:
                adj[i].add(j)
    return adj


def communities(n, adj, seed=20260909, rounds=30):
    """Label propagation on the undirected version."""
    und = defaultdict(set)
    for i, vs in adj.items():
        for j in vs:
            und[i].add(j)
            und[j].add(i)
    lab = list(range(n))
    rng = random.Random(seed)
    order = list(range(n))
    for _ in range(rounds):
        rng.shuffle(order)
        moved = 0
        for i in order:
            if not und[i]:
                continue
            c = Counter(lab[j] for j in und[i])
            best = max(c.items(), key=lambda kv: (kv[1], -kv[0]))[0]
            if best != lab[i]:
                lab[i] = best
                moved += 1
        if not moved:
            break
    return lab


def main():
    kinds = json.loads((OUT / "kinds.json").read_text())
    mlnames = set(json.loads((BOARD / "decls.json").read_text())["index"])
    known = {d for d in mlnames if d in kinds}
    ml_iface = {d for d in known if kinds[d] in INTERFACE_KINDS}
    ml_vocab = {d for d in known if kinds[d] in VOCAB_KINDS}
    print("mathlib with known kind: %d (%d interface, %d vocabulary)"
          % (len(known), len(ml_iface), len(ml_vocab)), flush=True)

    census = {}
    vocab_sets = {}
    for p in sorted(TEN.glob("*.lean")):
        if p.name == "All.lean":
            continue
        txt, decls = parse(p)
        adj = graph(decls)
        n = len(decls)
        edges = sum(len(v) for v in adj.values())
        lab = communities(n, adj)
        comm = Counter(lab)
        big = [c for c, k in comm.items() if k >= 20]
        # interfaces: declarations with an edge crossing a community boundary
        cross = 0
        iface_nodes = set()
        for i, vs in adj.items():
            for j in vs:
                if lab[i] != lab[j]:
                    cross += 1
                    iface_nodes.add(i)
                    iface_nodes.add(j)
        # own definitions (board-specific)
        own = {d["name"] for d in decls if d["kind"] in INTERFACE_KINDS}
        own |= {d["name"].split(".")[-1] for d in decls
                if d["kind"] in INTERFACE_KINDS}
        own -= mlnames
        own -= {x.split(".")[-1] for x in mlnames}
        exportable = 0
        thm = 0
        lens = []
        for d in decls:
            if d["kind"] not in ("theorem", "lemma"):
                continue
            thm += 1
            stmt = d["body"].split(":=")[0]
            lens.append(len(stmt))
            if not (set(TOK.findall(stmt)) & own):
                exportable += 1
        toks = set(TOK.findall(txt))
        vocab_sets[p.stem] = {"iface": sorted(toks & ml_iface),
                              "vocab": sorted(toks & ml_vocab)}
        tac = {t: len(rx.findall(txt)) for t, rx in TACRX.items()}
        nz = [v for v in tac.values() if v]
        census[p.stem] = {
            "declarations": n, "theorems": thm,
            "definitions": sum(1 for d in decls
                               if d["kind"] in INTERFACE_KINDS),
            "namespaces": len({d["ns"] for d in decls}),
            "edges": edges, "mean_out_degree": round(edges / n, 2),
            "communities_total": len(comm),
            "communities_ge_20": len(big),
            "largest_community_frac": round(max(comm.values()) / n, 3),
            "cross_community_edges": cross,
            "cross_edge_fraction": round(cross / edges, 4) if edges else 0,
            "interface_nodes": len(iface_nodes),
            "interface_node_fraction": round(len(iface_nodes) / n, 3),
            "own_definitions": len(own),
            "exportable": exportable,
            "exportable_fraction": round(exportable / thm, 4) if thm else 0,
            "median_statement_len": sorted(lens)[len(lens) // 2] if lens else 0,
            "mathlib_interface_decls": len(vocab_sets[p.stem]["iface"]),
            "mathlib_vocab_decls": len(vocab_sets[p.stem]["vocab"]),
            "tactic_diversity": len(nz),
            "tactic_entropy": round(
                -sum((v / sum(nz)) * (v / sum(nz) and __import__("math").log(v / sum(nz)))
                     for v in nz), 3) if nz else 0,
        }
        print("%-32s decls=%-5d comm>=20=%-3d largest=%.2f xedge=%.3f "
              "iface=%.2f exp=%.3f"
              % (p.stem, n, census[p.stem]["communities_ge_20"],
                 census[p.stem]["largest_community_frac"],
                 census[p.stem]["cross_edge_fraction"],
                 census[p.stem]["interface_node_fraction"],
                 census[p.stem]["exportable_fraction"]), flush=True)

    json.dump({"label": "COMPUTED_FROM_ARTIFACT", "census": census},
              open(OUT / "census.json", "w"), indent=1)
    json.dump(vocab_sets, open(OUT / "vocab_sets.json", "w"))


if __name__ == "__main__":
    main()

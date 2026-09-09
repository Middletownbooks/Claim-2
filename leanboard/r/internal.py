#!/usr/bin/env python3
"""
R2 -- QPR's internal structure: the graph that has to substitute for a module
dependency graph, because the artifact is one file.

Declarations are extracted in order with their source spans; an edge a -> b
means b's body references a. Names are matched fully qualified and by last
component, with the last-component match accepted only when it is unambiguous
inside the file -- the ambiguity that misattributed `add_pow` in Report A.

Reported so the numbers sit beside FLT's citation graph (106 897 edges,
max depth 118) and NS's module graph.
"""
import json
import re
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

OUT = Path(__file__).resolve().parent
TEN = Path("/home/user/openai/ten-proofs")
DECL = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+"
    r"([A-Za-z0-9_.'!?«»]+)", re.M)
NSOPEN = re.compile(r"^namespace\s+([A-Za-z0-9_.']+)", re.M)
NSEND = re.compile(r"^end\b\s*([A-Za-z0-9_.']*)", re.M)
TOK = re.compile(r"[A-Za-z_«][A-Za-z0-9_.'»]*")


def build(path):
    txt = path.read_text(errors="ignore")
    events = []
    for m in DECL.finditer(txt):
        events.append(("decl", m.start(), m.end(), m.group(1), m.group(2)))
    for m in NSOPEN.finditer(txt):
        events.append(("ns", m.start(), m.end(), None, m.group(1)))
    for m in NSEND.finditer(txt):
        events.append(("end", m.start(), m.end(), None, m.group(1)))
    events.sort(key=lambda e: e[1])

    decls = []
    stack = []
    for kind, s, e, dk, name in events:
        if kind == "ns":
            stack.append(name)
        elif kind == "end":
            if stack and (not name or stack[-1].endswith(name.split(".")[-1])):
                stack.pop()
        else:
            full = ".".join(stack + [name]) if stack else name
            decls.append({"name": name, "full": full, "kind": dk,
                          "start": s, "end": e, "ns": ".".join(stack)})
    for i, d in enumerate(decls):
        d["body_end"] = decls[i + 1]["start"] if i + 1 < len(decls) else len(txt)

    full_index = {d["full"]: i for i, d in enumerate(decls)}
    # NOTE: a set, not a list. Adding both the name and its last component to
    # the same key made every simple name look ambiguous, which dropped all but
    # 5 of the file's edges.
    short = defaultdict(set)
    for i, d in enumerate(decls):
        short[d["name"]].add(i)
        short[d["name"].split(".")[-1]].add(i)
    unambiguous = {k: next(iter(v)) for k, v in short.items() if len(v) == 1}

    edges = defaultdict(set)
    for i, d in enumerate(decls):
        body = txt[d["end"]:d["body_end"]]
        for t in set(TOK.findall(body)):
            j = full_index.get(t)
            if j is None:
                j = unambiguous.get(t)
            if j is not None and j != i:
                edges[i].add(j)
    return txt, decls, edges


def stats(decls, edges):
    n = len(decls)
    m = sum(len(v) for v in edges.values())
    indeg = Counter()
    for i, vs in edges.items():
        for j in vs:
            indeg[j] += 1
    # longest path in the DAG of "declared earlier" edges (acyclic by order)
    depth = [0] * n
    for i in range(n):
        for j in edges.get(i, ()):
            if j < i:
                depth[i] = max(depth[i], depth[j] + 1)
    return {"declarations": n, "edges": m,
            "mean_out_degree": round(m / n, 2),
            "max_depth": max(depth) if depth else 0,
            "isolated": sum(1 for i in range(n)
                            if not edges.get(i) and indeg[i] == 0),
            "most_cited": [(decls[j]["full"], c) for j, c in
                           indeg.most_common(15)]}


def main():
    which = sys.argv[1:] or ["QuantumParallelRepetition"]
    out = {"label": "COMPUTED_FROM_ARTIFACT", "files": {}}
    for w in which:
        p = TEN / (w + ".lean")
        txt, decls, edges = build(p)
        s = stats(decls, edges)
        nss = Counter(d["ns"] for d in decls)
        s["namespaces"] = nss.most_common(20)
        s["namespace_count"] = len(nss)
        out["files"][w] = s
        print("== %s" % w)
        print("   %d declarations, %d internal edges, mean out-degree %.2f, "
              "max depth %d, %d isolated"
              % (s["declarations"], s["edges"], s["mean_out_degree"],
                 s["max_depth"], s["isolated"]))
        print("   %d namespaces; top:" % s["namespace_count"])
        for k, v in s["namespaces"][:12]:
            print("      %-52s %d" % (k or "(root)", v))
        print("   most-cited internal declarations:")
        for k, v in s["most_cited"][:10]:
            print("      %-58s %d" % (k[:58], v))
        print()
    (OUT / "internal.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()

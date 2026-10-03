#!/usr/bin/env python3
"""ref-check / emitall-style: recompute the CITATIONS.md status tables from citations.json."""
import collections, json, sys
rows = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "../../proof-protocol/citations.json"))["rows"]
norm = lambda s: s.split(" (")[0].split(" AS OF")[0]
last = {r["id"]: r for r in rows}
print("rows ever written:", len(rows), dict(collections.Counter(norm(r["status"]) for r in rows)))
print("distinct claims  :", len(last), dict(collections.Counter(norm(r["status"]) for r in last.values())))

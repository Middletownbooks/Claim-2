Run records written by `search_symmetric.py --out`. **Empty by design at registration** —
`score_pte11.py` is committed before any of these exist, and reports every prediction that
depends on them as NOT-SCORED rather than as a pass.

`RUN_LOG.json`, when it exists, carries the operator's fields that no script can infer:
`stopped_by` (one of `memory`, `clock`, `completed`), `memory_headroom` (bool), and
`budget_exhausted` (bool).

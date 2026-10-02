# The heartbeat staleness check was wrong, and it passed while being wrong

## What happened

A heartbeat fired at 00:08:08 and was delivered at ~00:33 — about 25 minutes late. In the interval
I had done the clean calibration, found the production-discount problem, fixed the script, and
relaunched the sweep. Its instructions were superseded: it would have launched a second sweep
alongside the running one.

## Why the check I wrote did not catch it

> *"confirm this notification's `queued at` time matches the trigger that just fired"*

It **did** match — 00:08:08 against that trigger's own fire time. The check passed. It was testing
the wrong proposition: **not which trigger fired, but whether a newer one exists.**

## The correct test

| | |
|---|---|
| notification `queued at` | 00:08:08 |
| live trigger `created_at` | 00:08:27 |
| created **after** the notification was queued | **superseded** |

If `list_triggers` shows a live trigger whose `created_at` is later than this notification's
`queued at`, this notification is from a trigger I have already replaced — whatever its own fire
time says. Nineteen seconds of overlap was enough to make the difference invisible to the old test.

## Why it mattered twice

This is the **second** late heartbeat in the session. The first named level 4 and `sweep/` and would
have pooled incompatible results; this one would have double-launched. Both were caught, the first
by noticing the superseded content and this one by luck — I happened to remember arming a
replacement. **A check that relies on remembering is not a check.**

## The rule now carried in every heartbeat

```
Call list_triggers.  If any live trigger's created_at is LATER than this
notification's "queued at", this heartbeat is superseded: check state, report,
and do nothing else -- no launch, no commit, no re-arm.
```

The asymmetry is deliberate. A missed heartbeat costs one idle cycle; a stale one acted on costs a
double-launched job whose rates are meaningless, or a commit of results that should never be pooled.

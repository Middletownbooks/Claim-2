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

---

# It was wrong a second time, and passed again

## What happened

A heartbeat **scheduled for 06:10:00** was delivered at **06:20:33** — ten minutes late. By 06:12 I
had already handled the thing it was sent to handle: the harness notified me that cycle 6's
background task had exited, I relaunched as cycle 7, committed and pushed shards 41-45, and armed a
replacement heartbeat for 06:57.

## Why the corrected check still did not catch it

| | |
|---|---|
| heartbeat **scheduled** for | 06:10:00 |
| replacement trigger `created_at` | 06:12:26 |
| notification `queued at` | 06:20:33 |

`created_at` 06:12:26 is **earlier** than `queued at` 06:20:33, so the test above returned *not
superseded* — and the heartbeat was superseded. The replacement was created in the gap between when
this heartbeat was due and when it was delivered.

The fault is the reference point. `queued at` is when the message was **delivered**, which on a late
delivery is well after the moment the heartbeat's instructions stopped describing reality. Anything
created in that gap is invisible. The scheduled fire time is the moment the instructions were meant
to apply, so that is what a replacement has to be compared against.

## The test now

```
Read the scheduled run time from the "This run was scheduled for ..." reminder
(fall back to "queued at" only if there is none).  Call list_triggers.  If any
live trigger's created_at is LATER than that SCHEDULED time, this heartbeat is
superseded: check state, report, and do nothing else -- no launch, no commit,
no re-arm.
```

Scheduled time is always at or before queued-at, so this test fires in every case the old one did
and in the late-delivery case it missed. It is strictly more conservative, which is the right
direction given the asymmetry: a missed heartbeat costs one idle cycle, a stale one acted on costs a
double-launched job or two live heartbeats drifting apart.

## What it would have cost here

The guard "if a cycle IS running, do not start a second one" would have stopped the double launch —
that layer held. But step 4 re-arms unconditionally, so acting on this heartbeat would have left
**two live heartbeats** on the same session, each re-arming its own successor, both committing and
both reporting. The protection came from a different rule than the one meant to provide it.

## Three versions of one check

1. *does queued-at match the trigger that just fired* — tested which trigger fired, not whether a
   newer one exists;
2. *is any live trigger's created_at later than queued-at* — right proposition, wrong reference
   point, blind to anything created during a late delivery;
3. *is any live trigger's created_at later than the SCHEDULED fire time* — current.

Each version passed on the case that broke it. A check that has never failed in anger has not been
tested; these were.

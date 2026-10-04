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

---

# It was wrong a third time, blinded by the fix it recommends

## What happened

Cycle 43's completion notification arrived at **09:29**, six minutes before the heartbeat armed for
**09:35**. The cycle was processed on the notification: gate timed, 219 bin regenerated and
verified, cycle 44 launched at 09:32:03, shards 288-296 committed and pushed as `df582f1`. Then the
09:35 heartbeat was moved to 11:00 with `update_trigger` — and the update landed at **09:35:29**,
eleven seconds after the trigger had already fired at **09:35:18**.

So a heartbeat was delivered carrying the pre-cycle-43 state: 288 shards, 85 rows in the 219 bin,
ten gate medians, `HEAD cd8bc56`. Every figure in it had moved.

## Why version 3 did not catch it

| | |
|---|---|
| heartbeat **scheduled** for | 09:35:18 |
| live trigger `created_at` | 08:11:37 |
| live trigger `updated_at` | 09:35:29 |

`created_at` is **earlier** than the scheduled time, so version 3 returned *not superseded*. It was
superseded by 11 seconds.

The blind spot is the mechanism version 3 recommends, in the same paragraph as the check:

> *"An UPDATED trigger keeps its created_at, which is why update_trigger beats delete-and-recreate."*

That is true and it is good advice — a preserved `created_at` is why an update does not look like a
replacement. It is also exactly why an update made *after* a firing is invisible to a `created_at`
comparison. The sentence recommending the mechanism and the check it defeats were written next to
each other and neither noticed the other.

## The test now

Two tests, because the first is still metadata about the trigger and the second is not.

```
1. Call list_triggers.  If any live trigger's created_at OR updated_at is later
   than this heartbeat's SCHEDULED time, it is superseded.

2. Read this prompt's own STATE block and compare it with the repository:
     git log --oneline -1                     vs the HEAD it names
     ls sweep_L5/sh_*.json | wc -l            vs the shard count it names
   If either disagrees, the prompt is stale -- whatever the timestamps say.
```

Test 2 is the one to trust. Versions 1, 2 and 3 all failed the same way: each asked a question about
the trigger's bookkeeping, and each time the bookkeeping was consistent with a world that had moved
on. Test 2 asks the repository what has happened. It cannot be defeated by a preserved timestamp, a
late delivery, or a trigger updated at the wrong moment, because it does not read any of them — a
prompt that names a HEAD the repository has moved past is stale by inspection, and the prompt names
its HEAD precisely so this test exists.

## Four versions of one check

1. *does queued-at match the trigger that just fired* — tested which trigger fired, not whether a
   newer one exists;
2. *is any live trigger's created_at later than queued-at* — right proposition, wrong reference
   point, blind to anything created during a late delivery;
3. *is any live trigger's created_at later than the SCHEDULED fire time* — blind to an **update**,
   which preserves `created_at` by design;
4. *either timestamp later than scheduled, **or** the prompt's STATE block disagreeing with the
   repository* — current.

Each of the first three passed on the case that broke it. The fourth adds the first test in this
sequence that does not depend on the trigger describing itself honestly.

## What it would have cost here

Everything in step 4's "re-arm unconditionally" plus a redundant pass over work already pushed: the
gate re-timed against a running cycle (instrument 21, directly — rule 1 forbids exactly that), a
second sweep attempt stopped only by the "if a cycle IS running, do not start a second" guard, and
a report quoting 288 shards and 85 rows some twenty minutes after 297 and 104 were pushed. As
before, the protection would have come from a different rule than the one meant to provide it.

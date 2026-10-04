# `pgrep -f` matches the shell that runs it, and so does `pkill -f`

Four times now a `-f` pattern has found the shell that ran it rather than the process it was
aimed at — three checks reporting confidently on a process they were not looking at,
because `pgrep -f <pattern>` matches against **full command lines**, and the command line of
the shell running the check contains the pattern — it is in the command itself.

| when | the check | what it actually matched |
|---|---|---|
| cycle 4's exit | `pgrep -af 'zsearch -m 11'` | its own wrapper shell. Reported **ALIVE after the cycle had exited** — i.e. ALIVE unconditionally. Four cores would have sat idle for a whole heartbeat interval while the sweep was reported healthy. |
| cycle 14, age | `ps -p $(pgrep -f 'python3 sweep.py' \| head -1)` | **three** wrapper shells plus the real process; `head -1` picked a wrapper. Reported the cycle as 0 seconds old when it was 51 minutes in. |
| cycle 42's heartbeat | `pkill -f check_gate.py` | the calling shell, which contains the pattern. The target did die, and so did the shell that asked, exit 144 mid-command. The same rule, with an **action** rather than a check on the end of it. |

The second one is the instructive one: I had already found and documented the first, written the
fix into the heartbeat, and then introduced the identical bug in a different command two hours
later. Knowing the rule did not help, because I did not recognise the new command as an instance
of it.

## What works

```sh
pgrep -x zsearch                        # match the process NAME exactly: cannot self-match,
                                        # because the shell's name is bash, not zsearch
pgrep -f '^python3 sweep\.py'           # anchor to the start of the command line: the wrapper's
                                        # line starts with /bin/bash, so it is excluded
zs=$(pgrep -x zsearch | head -1)        # or derive from a known child, which is immune by
pp=$(ps -o ppid= -p "$zs" | tr -d ' ')  # construction -- the child was exec'd by the thing
ps -o lstart,etime -p "$pp"             # you are asking about
```

The last form is what the heartbeat now uses for cycle age. It gave `Fri Oct 2 14:48:05, 51:08`
against the self-matched version's `00:00` for the same cycle at the same instant.

## The general shape

An instrument whose own operation is visible to itself will report on itself. `pgrep -f`,
`ps | grep`, `history | grep`, log scans that match the scanner's own output line — same failure
every time, and for a *check* it is always a **false positive**: the check says the thing is
there, because the asking made it there. Put an action on the end instead of a check and the
same match becomes a self-inflicted one — `pkill -f` kills the caller, and no error says so
until the caller stops existing. To kill a known background process, prefer its PID, its exact
name (`pkill -x`), or the harness that started it.

Prefer a check that cannot see itself: an exact name match, an anchored pattern, a PID from a
file, or a question asked of a child rather than of the whole process table.

## Why it kept passing

None of these raised an error. The check ran, printed a plausible PID and a plausible time, and
was wrong — the same property that made the first two versions of the heartbeat staleness test
pass on the cases that broke them (HEARTBEAT_STALENESS.md), and that made the first survivor
reproducibility test pass while exercising no parallelism at all
(SURVIVOR_REPRODUCIBILITY.md). A check that cannot fail is not a check.

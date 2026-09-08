#!/usr/bin/env python3
"""
External oracle worlds for the hidden-world benchmark (Phases 9-11).

Speaks exactly the laboratory's worker protocol:
    stdin : one JSON request per line  {"family","coord","op"}
    stdout: one JSON response per line {"truth","witness","fail_count",
                                        "pass_count","profile","evaluated"}

The laboratory is started with --oracle-command "python3 audit/worlds.py --world X"
and is never told which world it is talking to.

WORLD A  arithmetic   : the real predicates (same mathematics as lab.py's real oracle,
                        re-implemented here independently of it).
WORLD B  synthetic    : two interacting latent mechanisms per modulus, derived from a
                        keyed hash rather than from number theory. Structured, learnable
                        in principle, but unrelated to primes.
WORLD C  adversarial  : deliberately deceptive. Every row looks exactly like world B
                        inside the calibration window and then changes law outside it.
                        A finite-data pattern learner that does not extrapolate honestly
                        will export a false theorem here.

The break coordinates of world C are fixed constants declared here, before any run,
so the deception is preregistered rather than tuned.
"""
import argparse
import hashlib
import json
import math
import sys

# ---- preregistered constants for the adversarial world -------------------
# Everything at or below these coordinates obeys the "advertised" law;
# strictly above, the law changes. They sit above the calibration window and
# below the final window of the runs used in this audit.
C_BREAK_R = 10          # r-axis break (validation window ends at r=10)
C_BREAK_D = 102         # d-axis break (validation window ends at d=102)
C_BREAK_K = 40          # k-axis break for the T/U families


def _h(*parts):
    s = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(s.encode()).hexdigest(), 16)


def latent_threshold(m):
    """Hidden r-threshold: 1..4, keyed, no arithmetic meaning."""
    return 1 + _h("thr", m) % 4


def latent_period(m):
    """Hidden d-period: 2..40, keyed, no arithmetic meaning."""
    return 2 + _h("per", m) % 39


def latent_offset(m):
    """Hidden residue class inside the period."""
    return _h("off", m) % latent_period(m)


def hidden_B(family, coord):
    if family == "E":
        m, r, d = coord
        return (r >= latent_threshold(m)
                and d % latent_period(m) == latent_offset(m))
    m, k = coord
    return k % latent_period(m) == latent_offset(m)


def hidden_C(family, coord):
    """Agrees with B up to the break, then flips its law."""
    if family == "E":
        m, r, d = coord
        inside = r <= C_BREAK_R and d <= C_BREAK_D
        if inside:
            return hidden_B("E", coord)
        # Outside: the period silently doubles and the threshold disappears.
        return (d % (2 * latent_period(m)) == latent_offset(m))
    m, k = coord
    if k <= C_BREAK_K:
        return hidden_B(family, (m, k))
    return k % (2 * latent_period(m)) == latent_offset(m)


def answer(world, request):
    family = request["family"]
    coord = tuple(int(x) for x in request["coord"])
    op = request.get("op", "full")
    if family not in ("T", "E", "U"):
        raise ValueError("Unknown family")
    if op not in ("full", "witness"):
        raise ValueError("Unknown operation")
    if len(coord) != (3 if family == "E" else 2):
        raise ValueError("Wrong arity")
    if any(x < 1 for x in coord):
        raise ValueError("All parameters must be positive")

    m = coord[0]

    if world == "A":
        if family == "E":
            _, r, d = coord

            def outcome(x):
                return pow(x, r + d, m) == pow(x, r, m)
        else:
            _, k = coord

            def outcome(x):
                if family == "U" and math.gcd(x, m) != 1:
                    return None
                return pow(x, k, m) == x
    else:
        hidden = (hidden_B if world == "B" else hidden_C)(family, coord)

        def outcome(x):
            if family == "U" and x % 2 == 0 and m > 2:
                return None
            return bool(hidden or x != 0)

    profile = []
    checked = 0
    witness = None
    for x in range(m):
        y = outcome(x)
        profile.append(y)
        if y is not None:
            checked += 1
        if y is False and witness is None:
            witness = x
            if op == "witness":
                return {"witness": witness, "evaluated": checked}
    if op == "witness":
        return {"witness": None, "evaluated": checked}

    failures = sum(y is False for y in profile)
    return {
        "truth": failures == 0,
        "witness": witness,
        "fail_count": failures,
        "pass_count": sum(y is True for y in profile),
        "profile": profile,
        "evaluated": checked,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--world", choices=("A", "B", "C"), required=True)
    args = p.parse_args()
    for line in sys.stdin:
        try:
            r = answer(args.world, json.loads(line))
        except Exception as exc:
            r = {"error": repr(exc)}
        print(json.dumps(r, sort_keys=True, separators=(",", ":")), flush=True)


if __name__ == "__main__":
    main()

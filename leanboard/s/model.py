#!/usr/bin/env python3
"""
S4 -- the core falsification (brief section 15).

  Does interface overlap I(A,B) predict transport T(A->B) beyond what generic
  vocabulary overlap V(A,B), pool sizes and statement length already explain?

Design choices that matter:

* Transport is the SIZE-MATCHED measurement, so pool size is removed by
  construction rather than regressed out. Pool sizes are still offered to the
  model as covariates for the raw measurement.
* Interface and vocabulary are the mathlib TYPE-level and LEMMA-level
  alphabets. They are 83% correlated, which is reported as a limit on the
  design's power rather than hidden.
* Significance is by DEVELOPMENT-LABEL permutation, not by pair count. With 8
  to 10 developments the effective sample size is the number of developments,
  not the number of pairs, and permuting labels is what respects that.
"""
import json
import math
import random
import statistics as st
from pathlib import Path

OUT = Path(__file__).resolve().parent
SEED = 20260909
NPERM = 20000


def pear(a, b):
    ma, mb = st.mean(a), st.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** .5
    return num / den if den else 0.0


def ols_resid(y, Xs):
    n = len(y)
    k = len(Xs) + 1
    X = [[1.0] + [Xs[j][i] for j in range(len(Xs))] for i in range(n)]
    A = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(k)] +
         [sum(X[i][a] * y[i] for i in range(n))] for a in range(k)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        if abs(A[c][c]) < 1e-12:
            continue
        for r in range(k):
            if r != c:
                f = A[r][c] / A[c][c]
                A[r] = [A[r][j] - f * A[c][j] for j in range(k + 1)]
    b = [A[i][k] / A[i][i] if abs(A[i][i]) > 1e-12 else 0 for i in range(k)]
    pred = [sum(b[j] * X[i][j] for j in range(k)) for i in range(n)]
    return [y[i] - pred[i] for i in range(n)], b


def partial(y, x, ctrl):
    ry, _ = ols_resid(y, ctrl)
    rx, _ = ols_resid(x, ctrl)
    return pear(rx, ry)


def main():
    D = json.loads((OUT / "distance.json").read_text())
    T = json.loads((OUT / "transport.json").read_text())
    C = json.loads((OUT / "census.json").read_text())["census"]
    M = D["matrices"]

    for tag, key in (("SIZE-MATCHED", "size_matched"), ("RAW", "raw")):
        pairs = []
        for k, v in T[key].items():
            src, tgt = k.split("->")
            pairs.append({
                "src": src, "tgt": tgt, "T": v,
                "V": M["vocab"][src][tgt], "I": M["iface"][src][tgt],
                "Vr": M["vocab_rare"][src][tgt], "Ir": M["iface_rare"][src][tgt],
                "A": M["arch"][src][tgt],
                "lnNs": math.log(T["pool_sizes"][src]),
                "lnNt": math.log(T["pool_sizes"][tgt]),
                "Ls": math.log(C[src]["median_statement_len"] + 1),
                "Lt": math.log(C[tgt]["median_statement_len"] + 1),
            })
        y = [p["T"] for p in pairs]
        devs = sorted({p["src"] for p in pairs} | {p["tgt"] for p in pairs})
        print("\n=== %s transport, %d ordered pairs, %d developments"
              % (tag, len(pairs), len(devs)))
        print("    mean T = %.4f" % st.mean(y))

        base_ctrl = ([[p["lnNs"] for p in pairs], [p["lnNt"] for p in pairs],
                      [p["Ls"] for p in pairs], [p["Lt"] for p in pairs]]
                     if key == "raw" else
                     [[p["Ls"] for p in pairs], [p["Lt"] for p in pairs]])

        results = {}
        for label, xk, ctrl in (
            ("V alone", "V", []),
            ("I alone", "I", []),
            ("V | controls", "V", base_ctrl),
            ("I | controls", "I", base_ctrl),
            ("I | V + controls", "I", base_ctrl + [[p["V"] for p in pairs]]),
            ("V | I + controls", "V", base_ctrl + [[p["I"] for p in pairs]]),
            ("Ir | Vr + controls", "Ir", base_ctrl + [[p["Vr"] for p in pairs]]),
            ("Vr | Ir + controls", "Vr", base_ctrl + [[p["Ir"] for p in pairs]]),
            ("Arch | controls", "A", base_ctrl),
        ):
            x = [p[xk] for p in pairs]
            r = partial(y, x, ctrl) if ctrl else pear(x, y)
            # development-label permutation
            lookup = {(p["src"], p["tgt"]): p for p in pairs}
            rng = random.Random(SEED)
            cnt = used = 0
            for _ in range(NPERM):
                perm = devs[:]
                rng.shuffle(perm)
                m = dict(zip(devs, perm))
                yy, xx, cc = [], [], [[] for _ in ctrl]
                for i, p in enumerate(pairs):
                    q = lookup.get((m[p["src"]], m[p["tgt"]]))
                    if q is None:
                        continue
                    yy.append(p["T"])
                    xx.append(q[xk])
                    for j, col in enumerate(ctrl):
                        cc[j].append(col[i])
                if len(yy) < 12:
                    continue
                used += 1
                rr = partial(yy, xx, cc) if ctrl else pear(xx, yy)
                if abs(rr) >= abs(r):
                    cnt += 1
            p_val = cnt / used if used else float("nan")
            results[label] = {"r": round(r, 4), "p": round(p_val, 4),
                              "perms_used": used}
            print("    %-22s r = %+.4f   p = %.4f" % (label, r, p_val))

        (OUT / ("model_%s.json" % key)).write_text(
            json.dumps({"label": "EXPERIMENTAL_RESULT", "measure": key,
                        "n_pairs": len(pairs), "developments": devs,
                        "mean_T": round(st.mean(y), 5),
                        "collinearity_r_I_V": round(
                            pear([p["I"] for p in pairs],
                                 [p["V"] for p in pairs]), 4),
                        "results": results}, indent=1) + "\n")


if __name__ == "__main__":
    main()

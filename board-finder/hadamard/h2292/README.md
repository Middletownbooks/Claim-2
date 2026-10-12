# h2292 — the verified core for H(2292)

| file | what |
|---|---|
| `core.txt` | the four ±1 core sequences, length m = 572 |
| `paley_struct.py` | exhibits the Paley(11) + ×29 structure: CRT to Z₅₂ × Z₁₁, the three-value coset form, K / N₋ / N₊, the Corollary 1 norm identity, and the 5 × 3 = 15 factorisation of the multiplier group |
| `verify_2292.py` | self-contained verifier: builds the 2292×2292 matrix from `core.txt` plus the stated border and certifies `H Hᵀ = 2292 I`, with a one-sign-flip negative control |

```
python3 verify_2292.py          # exits 0 only if the claim passes and the corruption fails
python3 paley_struct.py         # the design structure the core actually sits in
```

The 2292×2292 matrix is **not committed** — it is 5.25M entries and regenerable
in seconds. The core plus the assembler is the artifact, which is the same
convention `Cooperative-AI-Defense/hadamard/findings` uses.

Report: `../VERIFY_2292.md`.

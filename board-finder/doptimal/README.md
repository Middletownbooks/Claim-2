# D-optimal designs (U13) — parallel track to the Hadamard programme

| file | what it is |
|---|---|
| `PROMPT_U13_TRANSFER.md` | **the handover.** Self-contained transfer audit for the instance working Hadamard: where the two problems coincide, where the analogy breaks, and why running them in parallel is a diagnostic for Hadamard rather than a hedge against it |
| `transfer_check.py` | the local verification behind the prompt's VERIFIED claims — PAF invariants, exhaustive small-order search, two-square admissibility, Monte Carlo density coefficients |
| `VERIFIED_OUTPUT.txt` | its recorded output |

The earlier `../fallbacks/prompts/U13_D_OPTIMAL.md` is a **different document and still stands**:
it is the go/no-go gate for U13 as a *replacement* target if the Hadamard kill test fails. This
directory is for U13 as a *parallel* track while Hadamard is live.

Two claims in that older prompt are corrected here. It said the transfer "should be a port rather
than a build" on the strength of the shared PAF condition. That is right about the descent and the
residual arithmetic (§2.1, verified) and wrong about two things it did not consider: the
meet-in-the-middle neighbourhood shrinks by a factor of M² with two blocks instead of four (§3.3),
and halving the free bits while holding the equation count fixed may empty the orbit ansatz
altogether at the orders of interest (§3.2). The second is the one that decides whether this is a
port or a rebuild.

# Design flaw in my own case set, recorded before rater B returned

The five scored cases (C1–C5) are **before/after contrasts**: each says what was
done before an advance and what was done after. The three calibration cases
(K1–K3) are **static board descriptions**: each describes one board, with no
"before" to contrast against.

Asking "which transformation does this describe?" is therefore **ill-posed for
K1–K3**. A rater has to infer what changed from a description of only one state.
Rater A's response confirms the problem is live: it answered all three and
flagged all three as UNKNOWN in the recognition probe, having to lean on an
internal cross-reference ("the same body transform as before" in K3 tying it
to K1) rather than on the item itself.

Consequences, stated before B's answers are known:

1. **The calibration agreement figure is not interpretable** as a sanity check on
   the vocabulary. It measures agreement on an ill-posed task. I will report it
   but will not use it to argue either way.
2. **It does not contaminate the scored result.** C1–C5 are all proper
   before/after contrasts, and kappa is computed on those five only.
3. **This is my error, not the handoff's.** The commission asked for held-out
   after-boards; I supplied board descriptions for the calibration items and
   contrasts for the scored ones, which are not the same object.

The fix for any rerun: state every case as a before/after contrast, including
the calibration ones. Until then the calibration column is decoration.

Separately worth flagging for the P3 record: rater A assigned K3
(Guo–Fang–Lu) the label WORK MOVED, not DE-TENSORIZE. The originating
instance's own analysis of that case identified the mechanism as
multiplicative-to-averaging — i.e. DE-TENSORIZE. If B agrees with A, then the
taxonomy's author and an independent rater disagree about the single case the
taxonomy was induced from, which is a stronger negative result than a low kappa
on the scored cases would be.

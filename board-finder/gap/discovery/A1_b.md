# A1_b — Arm 1b: the `II` records nobody assessed (worker output)

Worker: cheap-tier research worker. Date of run: 2026-09-29. Tools: WebSearch only (no page fetches unless stated). Almost every factual cell is `SEARCH-SUMMARY` (seen in a search-result summary, source not read) or `RECALL`. No git used.

SUMMARY TABLE

| rank | S0 | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|
| 375 | PASS | FAIL | FAIL | PASS (see block) | PASS | PASS (see block) |
| 385 | PASS | PASS (see block) | CANNOT EVALUATE | CANNOT EVALUATE | PASS | PASS (see block) |
| 410 | CANNOT EVALUATE | FAIL | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 413 | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 417 | CANNOT EVALUATE | FAIL | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 428 | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 441 | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 450 | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 479 | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 221 (check, not counted) | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 282 (check, not counted) | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 337 (check, not counted) | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |

Derived from the blocks below by script. Only 375 and 385 were assessed with sourced search summaries; the WebSearch budget was exhausted afterwards, so records 410-479 and the three checks rest on RECALL and carry CANNOT EVALUATE except where a verdict follows from the record text and the brief's own definitions (410 S1/S2, 417 S1/S2). Cells marked '(see block)' are PASS with a caveat stated in the block (375 S3 is mechanical and vacuous; 375 S5 is proof-type; 385 S1 is formal and would refute the headline).


---

```
RECORD      | 375 — Sharp asymptotic order of minimal star discrepancy in each dimension d >= 3
QUANTITY    | the exponent of log N in inf over N-point sets of the unnormalised star discrepancy Delta_d(N), fixed d >= 3
LOWER       | Delta_d(N) >= c_d (log N)^{(d-1)/2 + eta_d}, some 0 < eta_d < 1/2 (Bilyk-Lacey-Vagharshakyan, "On the small ball inequality in all dimensions", 2008; d=3 case Bilyk-Lacey 2008; d=3 explicit eta_3 < 1/(32+4*sqrt(41)) ~ 0.0174, Puchhammer, arXiv:1602.01307, 2016). Baseline exponent (d-1)/2 is Roth 1954. | SEARCH-SUMMARY (BLV statement, Puchhammer abstract seen in search results; sources not read) | EXACT (asymptotic theorem, not a numeric estimate) ; BLV = REFEREED per RECALL (J. Funct. Anal. 2008, not verified this session), Puchhammer = UNKNOWN referee status
UPPER       | Delta_d(N) = O((log N)^{d-1}) from Halton/Hammersley-type constructions (normalised D*_N = O((log N)^{d-1}/N); "often conjectured to be best possible, still open"). Date of the original construction: 1960s (RECALL, not verified). No improvement of the exponent d-1 found. | SEARCH-SUMMARY for the statement; RECALL for attribution/date | EXACT ; REFEREED (classical) / UNKNOWN for exact original reference
BOUND OBJ   | lower: PROOF — an analytic (small-ball / Riesz-product) argument; no finite object can bound an asymptotic exponent ; upper: ALGORITHM — an explicit construction family valid for every N whose bound is universally quantified over N (a finite point set bounds Delta_d only at its own N)
S0 OPEN     | PASS — search summaries state the exact order is "one of the most famous open problems" and the (log N)^{d-1} lower-bound conjecture is unproven for arbitrary point sets; no resolution claim (withdrawn or otherwise) found. Levin's recent results are said (SEARCH-SUMMARY) to prove the conjectured lower bound only for specific constructions (digital nets, Halton points, Frolov lattices), not for arbitrary point sets. | SEARCH-SUMMARY
S1 COUPLED  | FAIL — headline is an asymptotic-order question; route (a) does not apply (headline is the order as N->infinity, not an extremum whose single object bounds it); route (b) no published bound on the headline was certificate-checked; no published lifting theorem turning a finite point set into an asymptotic exponent appeared in any result I saw; NO search was targeted at lifting theorems, so the verdict rests on the sourced BOUND OBJ classification (lower = proof, upper = construction family, per search summaries) plus the plain fact that one finite N-point set bounds Delta_d only at its own N. Finite N-point sets bound only the finite analogue Delta_d(N) at one N. | SEARCH-SUMMARY (negative result from searches; not a proof that no such theorem exists)
S2 VETO     | FAIL — no WITNESS bound object exists on either side (lower = PROOF, upper = ALGORITHM family); the upper-side object is an ALGORITHM, which is vetoed as stated. (Short answer, S1 FAIL.)
MOVE-1      | 2016-02 | F. Puchhammer | explicit eta_3 < 0.0174 for d=3 (not a new best exponent for general d; makes the existence result of Bilyk-Lacey explicit) | ANALYTIC | abstract: "builds upon their methods to verify that the above result holds with eta < 1/(32+4 sqrt(41))" | SEARCH-SUMMARY
MOVE-2      | 2008 | Bilyk-Lacey-Vagharshakyan | exponent (d-1)/2 + eta_d, eta_d>0, all d >= 3 (previous best: Roth 1954, (d-1)/2) | ANALYTIC | proof via the small ball inequality (hand-derived analytic argument) | SEARCH-SUMMARY (kind inferred from the paper being a pure-analysis proof titled "small ball inequality"; text not read — treat kind as SEARCH-SUMMARY-level)
            | (move on the UPPER side: none found after the 1960s constructions; date RECALL.)
S3 IDEA     | PASS (mechanical only) — MOVE-1 is ANALYTIC; but there is no coupled side (S1 FAIL) so the PASS carries no information.
S4 CROWDED  | PASS — searched: "AlphaEvolve OR message-passing Monte Carlo OR reinforcement learning star discrepancy"; "star discrepancy lower bound exponent improved beyond BLV 2024 2025 2026"; "star discrepancy open problem order of magnitude gap 2025 improvement". Found AI/large-scale-optimisation work only on the FINITE analogue (MPMC, arXiv:2405.15059 / PNAS 2024; gradient-descent post-processing arXiv:2511.10496; arXiv:2604.00786 seen only as a truncated title 'Finding Low Star Discrepancy 3D Kronecker Point Sets Using Algorithm ...'), none moving an asymptotic exponent. No AI move on the exponent found. | SEARCH-SUMMARY
S5 DELIVER  | PASS (in form) — named published bound: BLV lower exponent (d-1)/2+eta_d (or Puchhammer's eta_3 < 0.0174). Abstract sentence: "We prove that the unnormalised star discrepancy of any N-point set in [0,1)^3 is at least c (log N)^{1+eta} with eta = <larger value than 0.0174>." (This is a PROOF-type improvement, not witness-type.) | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — the frontier is an exponent, not a size/dimension/order; searched for dated methods differing by a factor >= 2 in a frontier parameter; nothing applicable.
BITS_SEARCH | UNDEFINED — no named search ansatz for a witness bounding the asymptotic exponent, and no published density estimate.
VERIF CLASS | PROOF
NOTES       | Consistency with brief: fine. Dead end: no lifting theorem found. The moving quantity in the 2024-26 AI/optimisation literature is the finite-N minimal discrepancy in low d (e.g. "Constructing optimal star discrepancy sets", Proc. AMS Ser. B 2025, seen only as title) — that is a finite analogue and, per S1, does not count. Normalisation warning: the headline uses the unnormalised count discrepancy; literature quotes both normalised (D*_N, divide by N) and unnormalised forms.
```

```
RECORD      | 385 — Lieb-Thirring Conjecture on the Sharp Constant for Riesz Means of Order One in Three Dimensions
QUANTITY    | the ratio L_{1,3} / L^cl_{1,3} of the optimal Lieb-Thirring constant (gamma=1, d=3) to the semiclassical constant 1/(15 pi^2) (formula Gamma(g+1)/((4pi)^{d/2} Gamma(g+1+d/2)) evaluated locally: = 0.0067547456 = 1/(15 pi^2))
LOWER       | L_{1,3} >= L^cl_{1,3} = 1/(15 pi^2) (semiclassical/Weyl lower bound; standard, no dated paper found this session). Tier: RECALL for the fact and its attribution; the definition of L^cl and the statement that L_{gamma,d} >= L^cl was not seen as a sourced sentence. Value 1/(15 pi^2) itself: PRIMARY-VERIFIED-LOCALLY (arithmetic from the formula) | RECALL / PRIMARY-VERIFIED-LOCALLY (value only) | EXACT ; REFEREED-classical (UNKNOWN for exact reference)
UPPER       | L_{1,3} <= (2/sqrt 3) L^cl_{1,3} ~ 1.1547 L^cl = 0.0077997 (locally computed), from Read & Schulz, "The sharp one-dimensional Lieb-Thirring inequality for the sum of eigenvalues", arXiv:2609.10478, dated 2026-09-14 in search summary; abstract (as summarised): 1D best constant with exponent one is 4/(3 sqrt3 pi), and via operator-valued potentials L_{1,d} <= (2/sqrt 3) L^cl_{1,d} in every dimension. Local check: 4/(3 sqrt3 pi) / L^cl_{1,1} = 1.15470 = 2/sqrt 3, consistent. Previous best: 1.44655 L^cl (Corso-Ried), before that 1.456 L^cl (Frank-Hundertmark-Jex-Nam, "The Lieb-Thirring inequality revisited", arXiv:1808.09017, J. Eur. Math. Soc.), before that pi/sqrt3 ~ 1.814 (Eden-Foias d=1 1991, extended to all d by Dolbeault-Laptev-Loss 2008). | SEARCH-SUMMARY (all of it; sources not read) | EXACT (analytic inequality; no numerics) ; PREPRINT (2609.10478 is 2 weeks old at run date, refereeing status UNKNOWN); earlier items REFEREED per summaries (FHJN JEMS; Corso-Ried CMP 406:50 (2025) is a different paper — the "variational problem" paper on CLR/LT, seen as title/journal ref; the exact reference for "1.44655" not identified)
BOUND OBJ   | lower: WITNESS only if the conjecture is false — a potential V with Tr(-Delta+V)_- / int V_-^{5/2} > L^cl (L_{1,3} is a sup over potentials V, RECALL of the definition); the present lower bound L^cl is a limit (Weyl/semiclassical), not attained by any V ; upper: PROOF — an analytic inequality (Rumin kinetic-energy method, operator-valued 1D sharp inequality + dimensional lifting)
S0 OPEN     | PASS — headline (L_{1,3} = L^cl) unresolved: best proven ratio is 2/sqrt3 (PREPRINT, Sep 2026). Search summaries state it is "believed that L_{gamma,d} = L^cl for gamma >= 1, d >= 3", i.e. still a conjecture. Numerics in the literature give critical gamma_c(3) ~ 0.8627 (SEARCH-SUMMARY; numerical). No resolution claim found. | SEARCH-SUMMARY
S1 COUPLED  | PASS (route (a), FORMAL) — L_{1,3} is by definition the sup over potentials V of the ratio, so any V exceeding L^cl is a one-sided (lower) bound on the headline quantity itself. CAVEAT for the adjudicator: such a witness would REFUTE the headline (the headline asks to PROVE equality, which the conjecture predicts is true; literature summary says believed true). The witness side can move only by disproving the conjecture; the upper side, which is the one that has actually moved, is PROOF-only. Extremal characterisation: standard variational definition of the best constant (RECALL); no dated citation read. | RECALL (definition) / SEARCH-SUMMARY (belief L=L^cl)
S2 VETO     | CANNOT EVALUATE — missing: any source showing that Tr(-Delta+V)_- for an explicit V on R^3 can be enclosed rigorously enough to certify "ratio > L^cl" by a terminating computation. Only non-rigorous numerical investigations seen (arXiv:1206.1473 "Best constants in Lieb-Thirring inequalities: a numerical investigation", title/summary only). Not an ALGORITHM-type object and no undecidability indicated, so not FAIL either.
MOVE-1      | (coupled = lower side) date not found | not found | L^cl (semiclassical) | UNKNOWN | no source read this session giving who/when/how the lower bound L_{1,3} >= L^cl was established (RECALL: Weyl-law/scaling argument, Lieb-Thirring 1976, ANALYTIC — not sourced) | RECALL
MOVE-2      | NONE (the lower side has not moved beyond L^cl per all summaries seen)
            | (moves on the UPPER side, for the record: 2026-09-14 Read-Schulz 2/sqrt3 [ANALYTIC, per abstract summary: proof of sharp 1D inequality + operator-valued extension; SEARCH-SUMMARY]; Corso-Ried 1.44655 [ANALYTIC-refinement of Rumin method per summary; year not established]; 2018 FHJN 1.456 [ANALYTIC, "building on Rumin's direct kinetic method"]. None AI-SEARCH.)
S3 IDEA     | CANNOT EVALUATE — MOVE-1 kind is UNKNOWN for the coupled (lower) side (no dated move found). If RECALL is accepted it would be ANALYTIC (classical semiclassical bound), which would read PASS; not asserted.
S4 CROWDED  | PASS — searched: "Lieb-Thirring inequality counterexample numerical optimization neural network OR AlphaEvolve OR machine learning search potential d=3 gamma=1"; "Mathematical exploration and discovery at scale AlphaEvolve Lieb-Thirring ..."; "Lieb-Thirring conjecture d=3 gamma=1 ... counterexample not known". Found: AlphaEvolve was applied (arXiv:2511.02864, Georgiev-Gomez-Serrano-Tao-Wagner, per summary) to the Benguria-Loss OVALS problem, which is connected to the d=1, gamma=1 (two-bound-state) Lieb-Thirring constant — not to L_{1,3}; and it "did not obtain the ovals" (summary). No AI/large-scale-optimisation move on the d=3 lower side found; the lower side has not moved. | SEARCH-SUMMARY
S5 DELIVER  | PASS (in form) — named published bound L_{1,3} >= L^cl = 1/(15 pi^2) (and the conjecture L_{1,3} = L^cl). Abstract sentence for a witness-type improvement: "We exhibit an explicit potential V on R^3 for which Tr(-Delta+V)_- exceeds (1/(15 pi^2)) int V_-^{5/2}, so L_{1,3} > L^cl and the Lieb-Thirring conjecture fails at (gamma,d) = (1,3)." (If the conjecture is true this sentence can never be written; that is the caveat under S1.) | SEARCH-SUMMARY
DIVERGENCE  | NONE FOUND — frontier parameter is a constant ratio, not a dimension/size/order; searched for methods on the same object with reach differing by >= 2 in a size parameter; none applicable.
BITS_SEARCH | UNDEFINED — numerical searches for optimisers exist (arXiv:1206.1473, arXiv:2010.02981 fixed-point algorithm, titles only) but no named ansatz for a counterexample potential at (1,3) AND no published density estimate were found.
VERIF CLASS | witness route (counterexample V): RIGOROUS-NUMERIC (would need certified eigenvalue enclosures; not evidenced, see S2) ; upper-bound route (the side that actually moves): PROOF
NOTES       | (1) CONTRADICTION among search summaries about the upper bound: one summary of arXiv:math-ph/9906013 (Hundertmark-Laptev-Weidl 1999 per title) said "L_{1,3} <= 2 L^cl < 0.013509" as best known; I verified 2*L^cl = 0.0135095 arithmetically but that number is NOT the current best — later results (1.456, 1.44655, 2/sqrt3) are smaller; I discard that summary line. (2) Another summary attributed the 2/sqrt3 bound to "the same authors" as Corso-Ried; the other summary attributed it to Read-Schulz (arXiv:2609.10478). I record Read-Schulz because two separate summaries name that paper's abstract; attribution still SEARCH-SUMMARY. (3) The ratio-monotonicity-in-dimension route (1D constant -> d=3) is asserted only via the abstract's "in every dimension"; I did not read the proof. (4) Summaries say the original LT conjecture FAILS for d=3, 1/2<gamma<1 and critical gamma_c(3)~0.8627 numerically; gamma=1 lies above gamma_c so L=L^cl is the expected value there (SEARCH-SUMMARY). (5) An arXiv "An Improved Bound for the Ovals Problem" (arXiv:2609.10775, Sep 2026, title only) is a d=1 object and not this record.
```

```
RECORD      | 410 — Smallest number of variables for undecidable Hilbert's Tenth Problem over Z
QUANTITY    | the least n such that Diophantine solvability over Z is undecidable for integer polynomials in at most n variables
LOWER       | n >= 2, since one variable is decidable (rational-root-type argument); whether n = 2 (general degree) is decidable is, per RECALL, open. No source read. | RECALL | EXACT ; UNKNOWN
UPPER       | undecidable with 11 integer unknowns (Z.-W. Sun, early 1990s) and with 9 natural-number unknowns (Matiyasevich; Jones 1982); the 9-over-N figure does NOT transfer to Z as 9. No source read; whether anything below 11 over Z has been shown since is unchecked. | RECALL | EXACT ; UNKNOWN
BOUND OBJ   | lower: ALGORITHM/PROOF — a decision procedure plus proof that it is correct (decidability side); upper: ALGORITHM — a universal polynomial with fewer unknowns, whose correctness is universally quantified over all parameter values (the brief itself lists 'universal polynomial' under ALGORITHM)
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible.
S1 COUPLED  | FAIL — follows from the record text plus the brief's own taxonomy (DEFINITIONAL, not literature): a bound on n moves only by a universal polynomial/reduction (ALGORITHM) or a decision procedure (ALGORITHM/PROOF); neither side's bound object is a WITNESS. Values above are RECALL and do not enter this verdict. | DEFINITIONAL
S2 VETO     | FAIL (vetoed) — the moving bound object is an ALGORITHM (universal polynomial), which the brief vetoes. DEFINITIONAL.
MOVE-1      | early 1990s (RECALL) | Z.-W. Sun | 11 unknowns over Z | UNKNOWN | no source read; RECALL suggests hand-derived reductions but the kind is not assigned from recall | RECALL
MOVE-2      | 1982 (RECALL) | Jones (publication of Matiyasevich's 9-unknown result over N) | 9 over N | UNKNOWN | no source read | RECALL
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — the named published bound would be 'undecidable with 11 integer unknowns' (RECALL); its currency is unverified. Abstract sentence if it moved: 'We show Hilbert's Tenth Problem is undecidable for polynomials in fewer than 11 integer unknowns.' (PROOF-type, not witness-type.)
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — no named search ansatz with a published density estimate found (not searched).
VERIF CLASS | PROOF
NOTES       | Everything factual here is RECALL. The one thing I can assert without a source is structural: the 'undecidable' side is an ALGORITHM-type object by the brief's definition, so S1/S2 fail regardless of the current numbers.
```

```
RECORD      | 413 — Zarankiewicz Problem on K_{t,t}-Free Bipartite Graphs
QUANTITY    | the exponent/order of ex(n, K_{t,t}) for each fixed t >= 2 (bipartite, n vertices)
LOWER       | RECALL: tight Theta(n^{2-1/t}) for t = 2, 3 (Reiman / Brown / Erdos-Renyi-Sos); for t >= 4 the general lower bound is of order n^{2-2/(t+1)} (probabilistic deletion) with better exponents only for K_{t,s} with s much larger than t (Alon-Ronyai-Szabo norm graphs; Bukh random algebraic constructions). No source read this session; recent improvements unchecked. | RECALL | EXACT (asymptotic) ; REFEREED per recall, UNKNOWN for references
UPPER       | RECALL: ex(n, K_{t,t}) = O(n^{2-1/t}) (Kovari-Sos-Turan, 1954; double counting). No source read. | RECALL | EXACT (asymptotic) ; REFEREED
BOUND OBJ   | lower: PROOF / construction family (an algebraic or probabilistic construction valid for all n, proved K_{t,t}-free; a single finite graph bounds the value at one n only) — RECALL ; upper: PROOF (new counting argument)
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible. RECALL: open for t >= 4.
S1 COUPLED  | CANNOT EVALUATE — asymptotic-order headline, so PASS needs a cited published lifting theorem from a finite K_{t,t}-free graph to an exponent bound; I neither found nor could search for one (RECALL: none known to me). A FAIL would rest on evidence of absence I do not have.
S2 VETO     | CANNOT EVALUATE — no candidate witness established (S1 unevaluated). RECALL: the property 'K_{t,t}-free' is decidable for a finite graph.
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — named bounds (recalled): Kovari-Sos-Turan upper; probabilistic lower for t >= 4. Currency unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched; nothing found.
VERIF CLASS | PROOF (asymptotic-order improvement); CHECK only for a finite-n analogue, which is not the headline
NOTES       | All RECALL. Structurally identical to 375 (asymptotic-order headline) but 375 had sourced search summaries for its bound objects; here I have none, hence CANNOT EVALUATE rather than FAIL.
```

```
RECORD      | 417 — Exact Consistency Strength of the Proper Forcing Axiom (PFA)
QUANTITY    | the position of PFA in the large-cardinal consistency-strength hierarchy (lower bound in inner-model terms, upper bound by forcing from a large cardinal)
LOWER       | RECALL: PFA implies large-cardinal strength well beyond measurable cardinals (inner models with Woodin cardinals; Todorcevic/Steel-type results). Exact current best not sourced. | RECALL | UNKNOWN ; UNKNOWN
UPPER       | RECALL: PFA is consistent relative to a supercompact cardinal (Baumgartner). Exact current best not sourced. | RECALL | EXACT ; REFEREED per recall
BOUND OBJ   | lower: PROOF (inner-model / core-model theory); upper: PROOF (forcing construction and its verification) — neither is a finite object
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible. RECALL: gap between Woodin-type lower bound and supercompact upper bound remains.
S1 COUPLED  | FAIL — DEFINITIONAL from the record text and the brief's taxonomy: consistency strength is a position in an infinite hierarchy of large cardinals; the quantity is not an extremum over finitely describable objects, and bounds move by theorems in set theory (PROOF), not by a witness whose value a terminating computation fixes. Values above are RECALL and do not enter the verdict. | DEFINITIONAL
S2 VETO     | FAIL — no WITNESS bound object exists (both sides PROOF). DEFINITIONAL; short answer since S1 FAIL.
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — currency of the recalled bounds unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — no search ansatz; nothing found (not searched).
VERIF CLASS | PROOF
NOTES       | Only the structural verdicts are issued; all values RECALL.
```

```
RECORD      | 428 — Exact value of the site-percolation threshold on the square lattice
QUANTITY    | p_c of Bernoulli site percolation on Z^2, tracked through rigorous lower/upper bounds (numerical estimate 0.592746 is given in the record text)
LOWER       | RECALL: rigorous lower bound about 0.556 (van den Berg-Ermakov, 1996, believed computer-assisted). Not sourced. | RECALL | RIGOROUS-NUMERIC (per recall, unverified) ; REFEREED per recall
UPPER       | RECALL: rigorous upper bound about 0.679492 (attribution not recalled reliably). Not sourced. | RECALL | RIGOROUS-NUMERIC (per recall, unverified) ; UNKNOWN
BOUND OBJ   | lower: WITNESS candidate (a finite computation certifying the bound; RECALL only) ; upper: WITNESS candidate (same, RECALL only) ; the record text separately states the 0.592746 estimate is NUMERICAL (not a bound)
S0 OPEN     | CANNOT EVALUATE — the record text says no exact value is known; not independently checked, and no check for resolution claims was possible.
S1 COUPLED  | CANNOT EVALUATE — route (b) (a published bound on p_c itself established by a finite certificate checked by terminating computation) is suggested by RECALL of the 1990s computer-assisted bounds, but I have no source for what those papers did or for the current best bounds. Not asserted either way.
S2 VETO     | CANNOT EVALUATE — depends on S1's certificate; not evidenced.
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — the named published bounds (recalled) would change on a rigorous improvement; currency unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched.
VERIF CLASS | RIGOROUS-NUMERIC (if the certificate route holds; unverified)
NOTES       | Recalled to be one of the more promising-looking records structurally, so it deserves a sourced follow-up. Also note statistical confidence intervals (not rigorous) exist in the literature per recall; they must not be confused with bounds.
```

```
RECORD      | 441 — Witsenhausen Counterexample: Optimal Strategy and Cost
QUANTITY    | the minimum over strategy pairs (u1 = f(x0), u2 = g(z2)) of expected cost k E[u1^2] + E[x2^2], as a function of (k, sigma)
LOWER       | RECALL: Witsenhausen's 1968 lower bound and later numerical/analytic lower bounds; approximate optimality within a constant factor (Grover-Park-Sahai) — not sourced. | RECALL | UNKNOWN ; UNKNOWN
UPPER       | RECALL: costs of specific nonlinear (step-like) strategies found by numerical search (e.g. hierarchical search, Lee-Lau-Ho 2001) at benchmark (k, sigma); exact benchmark values not recalled reliably, so none given. | RECALL | NUMERICAL (cost of a given strategy is computable to rigorous numeric precision in principle) ; UNKNOWN
BOUND OBJ   | lower: PROOF (analytic or optimal-transport argument) ; upper: WITNESS — a strategy pair (f, g), e.g. a step function f with g the conditional mean, whose cost is a finite quadrature (RECALL for the strategies actually used)
S0 OPEN     | CANNOT EVALUATE — no source read; RECALL says the exact optimum is unknown. No check for 2025-2026 claims.
S1 COUPLED  | CANNOT EVALUATE — route (a) holds structurally from the record text (the optimal cost is an infimum over strategy pairs, so any pair bounds it from above), but PASS also needs a published bound on the headline moved by such a witness; I could not source the published bound table (RECALL only).
S2 VETO     | CANNOT EVALUATE — cost of a given step-function strategy is an explicit Gaussian integral (RECALL), but I have no source showing rigorous certified evaluation is what the literature does.
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — a benchmark-cost table exists per recall but was not read.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched; no ansatz-with-density source.
VERIF CLASS | RIGOROUS-NUMERIC (for a strategy-cost step; unverified)
NOTES       | A sourced follow-up is needed before any verdict; the strategy-search literature is exactly the kind AI/optimisation crowding (S4) must be checked against.
```

```
RECORD      | 450 — Exact critical exponents of oriented percolation in 1+1 dimensions
QUANTITY    | the exponents rho, eta, nu at the critical point of 1+1 oriented percolation (exact values)
LOWER       | NOT FOUND — no rigorous bound on these exponents recalled or sourced. | NOT FOUND | UNKNOWN ; UNKNOWN
UPPER       | NOT FOUND — same. Numerical estimates exist (series/Monte-Carlo, Jensen 1999 per recall; values not given because not sourced). | RECALL | NUMERICAL ; UNKNOWN
BOUND OBJ   | NONE if only numerical estimates exist (the brief's own example of NONE) — unverified; no bounded side identified
S0 OPEN     | CANNOT EVALUATE — record text says unknown; not checked.
S1 COUPLED  | CANNOT EVALUATE — no bounded side identified; whether rigorous bounds exist was not searched.
S2 VETO     | CANNOT EVALUATE — no witness identified.
MOVE-1      | not found | not found | not found | UNKNOWN | no source | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — no named bound identified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF (any rigorous bound on an exponent); numerical estimates are not bounds
NOTES       | Any verdict here needs a source on whether rigorous exponent bounds exist.
```

```
RECORD      | 479 — Ruzsa-Szemeredi (6,3)-Problem on Triple Systems
QUANTITY    | the order of f(n,6,3), max edges of a 3-uniform hypergraph on n vertices with no 6 vertices spanning 3 edges
LOWER       | RECALL: n^2 / e^{O(sqrt(log n))} via Behrend's 3-AP-free sets (Ruzsa-Szemeredi 1976); a 2024 improvement of Behrend's construction (Elsholtz-Hunter-Proske-Sauermann) may transfer — unverified. | RECALL | EXACT (asymptotic) ; REFEREED per recall
UPPER       | RECALL: o(n^2) (Ruzsa-Szemeredi, via triangle removal), with a quantitative form through Fox's removal bound — unverified. | RECALL | EXACT ; REFEREED per recall
BOUND OBJ   | lower: PROOF/construction family (a finite 3-AP-free set A in [N] gives a (6,3)-free triple system with N|A| edges at one size — RECALL — but the asymptotic bound needs an all-N family) ; upper: PROOF
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible. RECALL: gap between n^{2-o(1)} and o(n^2) is open.
S1 COUPLED  | CANNOT EVALUATE — asymptotic-order headline; a cited lifting theorem would be needed and I could neither find nor search for one. RECALL of the finite 3-AP-free-set-to-hypergraph construction is not itself a published lifting theorem for the asymptotic order.
S2 VETO     | CANNOT EVALUATE — not established (S1 unevaluated); RECALL: '(6,3)-free' is decidable for a finite system.
MOVE-1      | not found | not found | not found | UNKNOWN | no source | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — named bounds recalled; currency unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched.
VERIF CLASS | PROOF
NOTES       | All RECALL.
```

```
RECORD      | 221 — Exact satisfiability threshold for random k-SAT, k = 3 (CONSISTENCY CHECK, not counted)
QUANTITY    | the threshold ratio r_3 (clauses/variables) for random 3-SAT
LOWER       | RECALL: 3.52 (algorithmic analyses, Kaporis-Kirousis-Lalas / Hajiaghayi-Sorkin, c. 2002-2003). | RECALL | EXACT ; REFEREED per recall
UPPER       | RECALL: about 4.49 (first-moment-type refinements, Diaz et al. 2009); statistical-physics estimate about 4.267 is NUMERICAL/non-rigorous. | RECALL | EXACT (4.49) ; NUMERICAL (4.267) ; UNKNOWN
BOUND OBJ   | lower: PROOF (analysis of a satisfying-assignment algorithm; the ALGORITHM is analysed, not a witness) ; upper: PROOF (moment method)
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible.
S1 COUPLED  | CANNOT EVALUATE — asymptotic-threshold headline (no finite-object lifting known to me); RECALL only.
S2 VETO     | CANNOT EVALUATE — not established (S1 unevaluated).
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — currency of recalled bounds unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched.
VERIF CLASS | PROOF (or RIGOROUS-NUMERIC for a numeric-evaluation step; unverified)
NOTES       | Brief statement 'lower bound 3.52 unmoved since 2003': my RECALL agrees that 3.52 is the value I know, but I have no source on any post-2003 move, so I can neither confirm nor contradict it. No contradiction found (no evidence either way).
```

```
RECORD      | 282 — Exact unassisted quantum capacity of the qubit depolarizing channel (CONSISTENCY CHECK, not counted)
QUANTITY    | Q(D_p) for each p, tracked through lower bounds (coherent-information / code constructions) and upper bounds (e.g. SDP / degradable-extension bounds)
LOWER       | RECALL: lower bounds from coherent information of n-letter channels/degenerate codes (DiVincenzo-Shor-Smolin 1998 line). Current best not sourced. | RECALL | RIGOROUS-NUMERIC (per recall) ; UNKNOWN
UPPER       | RECALL: upper bounds from Smith-Smolin-type and later SDP methods. Current best not sourced. | RECALL | RIGOROUS-NUMERIC (per recall) ; UNKNOWN
BOUND OBJ   | lower: WITNESS candidate (an n-letter input state/code with computed coherent information; Q is a limit of such quantities, RECALL of the LSD formula) ; upper: PROOF/certificate (unverified)
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible.
S1 COUPLED  | CANNOT EVALUATE — route (a) is suggested structurally by the regularised coherent-information formula, but no citation was read; not asserted.
S2 VETO     | CANNOT EVALUATE — not established (S1 unevaluated).
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — currency of recalled bounds unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched.
VERIF CLASS | PROOF (or RIGOROUS-NUMERIC for a numeric-evaluation step; unverified)
NOTES       | Brief statement 'bounds tightened in 2025 by arXiv:2506.03429': I could not read or search for that paper (arXiv blocked; budget exhausted). Neither confirmed nor contradicted.
```

```
RECORD      | 337 — Capacity of the binary deletion channel (CONSISTENCY CHECK, not counted)
QUANTITY    | C_del(d) for each deletion probability d, tracked through achievable-rate lower bounds and converse upper bounds
LOWER       | RECALL: lower bounds from random codes with Markov/ run-length input distributions (Mitzenmacher-Drinea, Kirsch-Drinea, Kanoria-Montanari, others). Current best not sourced. | RECALL | RIGOROUS-NUMERIC / EXACT (per recall) ; UNKNOWN
UPPER       | RECALL: upper bounds via auxiliary-channel/ numerical methods (Fertonani-Duman, Rahmati-Duman). Current best not sourced. | RECALL | RIGOROUS-NUMERIC (per recall) ; UNKNOWN
BOUND OBJ   | lower: PROOF/analysis of a code ensemble (achievable rate) ; upper: PROOF (converse) — unverified
S0 OPEN     | CANNOT EVALUATE — no source read this session on the current status; RECALL only (stale-recall risk), and no check for 2025-2026 resolution claims was possible.
S1 COUPLED  | CANNOT EVALUATE — function-valued capacity for all d; no citation for a finite certificate route was read.
S2 VETO     | CANNOT EVALUATE — not established (S1 unevaluated).
MOVE-1      | not found | not found | not found | UNKNOWN | no source read | RECALL
MOVE-2      | NONE FOUND (not searched)
S3 IDEA     | CANNOT EVALUATE — no MOVE could be sourced, so S3 cannot be derived.
S4 CROWDED  | CANNOT EVALUATE — no search for AI-driven or large-scale-optimisation moves on or after 2025-01-01 was possible (WebSearch budget exhausted after records 375 and 385; a later attempt was refused). Partial datum only (SECONDARY-RELAYED, keyword/title check of files I read): this record is not among the 67 titles of the AlphaEvolve problem repository (local file board-finder/gap/discovery/aerp_problems_2026-09-29.json) and its keywords do not appear in the teorth/optimizationproblems README table (raw.githubusercontent.com). Two channels only; not evidence of absence elsewhere.
S5 DELIVER  | CANNOT EVALUATE — currency of recalled bounds unverified.
DIVERGENCE  | NOT SEARCHED (search budget exhausted) — no claim either way
BITS_SEARCH | UNDEFINED — not searched.
VERIF CLASS | PROOF (or RIGOROUS-NUMERIC for a numeric-evaluation step; unverified)
NOTES       | Brief statement 'arXiv:2609.19412 narrowed the gap to a hundredth of a bit (Sep 2026)': not readable here (arXiv blocked, search budget exhausted); neither confirmed nor contradicted. Even if true, 'narrowed' is not 'closed': whether it makes the record dead is an adjudication question.
```


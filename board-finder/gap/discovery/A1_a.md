# A1_a — Arm 1a worker output (10 records)

Summary table (derived from the blocks below by script):

| rank | S0 | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|
| 17 | CANNOT EVALUATE | FAIL | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 186 | PASS | FAIL | PASS | PASS | PASS | PASS |
| 199 | CANNOT EVALUATE | FAIL | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 246 | CANNOT EVALUATE | FAIL | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 277 | PASS | CANNOT EVALUATE | PASS | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 288 | CANNOT EVALUATE | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 308 | PASS | PASS | PASS | PASS | FAIL | PASS |
| 351 | CANNOT EVALUATE | FAIL | FAIL | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 353 | PASS | CANNOT EVALUATE | PASS | CANNOT EVALUATE | CANNOT EVALUATE | CANNOT EVALUATE |
| 368 | PASS | PASS | PASS | CANNOT EVALUATE | CANNOT EVALUATE | PASS |

## Run notes (read first)

* The session-wide WebSearch budget (200/200) was exhausted part-way through this run (shared with other workers). About 27 searches were mine, spent on records 186, 308, 368. Records 17, 199, 246, 277, 288, 351, 353 got **no web search**. Where a gate needs a dated 2026 fact I did not obtain, the answer is CANNOT EVALUATE and the block says what is missing.
* Sources actually read (SECONDARY-RELAYED): raw.githubusercontent.com files of teorth/optimizationproblems (README.md, constants/10a.md), teorth/erdosproblems (data/problems.yaml), google-deepmind/formal-conjectures (ErdosProblems/{142,147,562,563,564,572}.lean), jstoobysmith/Thomson-N-8-Warrant README; local repo files aerp_problems_2026-09-29.json and aerp_outcomes.json. arXiv, sota2.com, Cambridge Cluster Database, OEIS were not readable.
* Everything tagged SEARCH-SUMMARY is a search-result summary of an arXiv abstract or page that I did not read.
* Environment date is 2026-09-29; many relevant items are 2026 preprints (unrefereed).

---

```
RECORD      | 17 — BQP Versus NP: Complete Language-Class Relation
QUANTITY    | none numeric: the truth values of NP ⊆ BQP and BQP ⊆ NP (class inclusions), no tracked bound
LOWER       | NOT FOUND (no numeric bound exists for a class relation) | n/a | UNKNOWN
UPPER       | NOT FOUND | n/a | UNKNOWN
BOUND OBJ   | lower: NONE — nothing quantitative to move ; upper: NONE — settling NP ⊆ BQP would need a poly-time quantum algorithm for an NP-complete problem (ALGORITHM, universally quantified correctness); settling BQP ⊄ NP or NP ⊄ BQP needs a new separation argument (PROOF)
S0 OPEN     | CANNOT EVALUATE — RECALL: no unconditional relation known (only oracle results, e.g. Raz–Tal BQP vs PH relative to an oracle). I read no dated 2026 source, so I cannot report or exclude resolution claims. The brief's own label says open.
S1 COUPLED  | FAIL — headline is a class relation, not an extremum over finitely describable objects (route a fails); no published bound is established by a finite certificate (route b fails); no asymptotic quantity, so no lifting theorem applies | RECALL
S2 VETO     | FAIL — the only object that could move the NP ⊆ BQP side is an ALGORITHM (vetoed by definition); the other side is a PROOF
MOVE-1      | NONE (no tracked bound has moved; nothing to date)
MOVE-2      | NONE
S3 IDEA     | CANNOT EVALUATE — no coupled side and no move
S4 CROWDED  | CANNOT EVALUATE — did not search (budget exhausted)
S5 DELIVER  | CANNOT EVALUATE — no maintained table or numeric published bound identified for this record
DIVERGENCE  | NONE FOUND — not searched; no frontier parameter exists for this record
BITS_SEARCH | UNDEFINED — no witness ansatz
VERIF CLASS | PROOF
NOTES       | Structural mismatch with the brief's template: this record has no tracked quantity. FAIL on S1/S2 rests on the definition of the gates plus RECALL, not on a source read this session.
```

```
RECORD      | 186 — Order of Magnitude of Maximum 3-Term-AP-Free Subsets of {1,...,N}
QUANTITY    | r_3(N), the maximum size of a 3-AP-free subset of {1..N}, as an asymptotic order (exp(-C sqrt(log N)) versus exp(-c (log N)^(1/6)/loglog N) savings)
LOWER       | r_3(N) >= N / 2^{(C+o(1)) sqrt(log_2 N)} with C = 2 sqrt(log_2(24/7)) ≈ 2.667 (Behrend had 2 sqrt 2 ≈ 2.828); Elsholtz–Hunter–Proske–Sauermann, arXiv 2406.12290, June 2024 | SEARCH-SUMMARY (arXiv abstract via search) | EXACT (asymptotic, proved constant) ; PREPRINT (search found no journal confirmation)
UPPER       | r_3(N) <= N exp(-c (log N)^{1/6} / log log N); Raghavan, arXiv 2603.27045, 2026 | SEARCH-SUMMARY (abstract and a second search result citing it as the current best) | EXACT (asymptotic, proved) ; PREPRINT
BOUND OBJ   | lower: PROOF — asymptotic construction family with an optimised constant; a fixed finite AP-free set only bounds r_3 at one N ; upper: PROOF — Fourier-analytic argument (Kelley–Meka line: exponent 1/12, then Bloom–Sisask 1/9, then Raghavan 1/6/loglog)
S0 OPEN     | PASS — gap between the two bounds is quasi-polynomial-scale; Erdős problem 142 (r_k(N) asymptotics, $10000) has status "open" in teorth/erdosproblems data/problems.yaml at HEAD (last_update 2025-08-31) | SECONDARY-RELAYED for the DB status, SEARCH-SUMMARY for the bounds. No resolution claim seen.
S1 COUPLED  | FAIL — asymptotic-order headline. r_3 is a max over sets, so a finite set is a one-sided bound only for that N (a finite analogue). The only lifting I know is the product/digit-expansion construction (3-AP-free A in [m] gives 3-AP-free sets of size |A|^k in [(2m-1)^k]); it yields only N^{alpha} with alpha<1, far weaker than Behrend scale, so it cannot move either published bound. No lifting theorem to the Behrend scale found. | RECALL (product lemma) ; caveat: I could not read the EHPS paper to check whether its construction has a finite-certificate component.
S2 VETO     | PASS (moot) — for a finite set the predicate (no x+z=2y with distinct x,y,z) is decidable and computed in finite time
MOVE-1      | 2024-06 | Elsholtz, Hunter, Proske, Sauermann | constant 2 sqrt(log_2(24/7)) | ANALYTIC | abstract: "first improvement upon Behrend's classical construction beyond lower-order factors ... constant 2√2 improved to 2√(log_2(24/7))" — a proved closed-form constant for all large N (lower side; NOT a coupled side) | SEARCH-SUMMARY
MOVE-2      | 2026 (arXiv 2603.27045; month not read) | Raghavan | exponent (log N)^{1/6}/loglog N | ANALYTIC | "iterated variant of the Kelley–Meka sifting argument plus improved Bloom–Sisask bootstrapping of Croot–Sisask almost-periodicity" (upper side, PROOF side) | SEARCH-SUMMARY
S3 IDEA     | PASS (moot, S1 FAIL) — MOVE-1 kind ANALYTIC, from an abstract only
S4 CROWDED  | PASS (moot) — searched: "AlphaEvolve cap set OR arithmetic progression OR Behrend improved 2025"; "3-term AP improved bound 2025 r_3(N)"; "Behrend improvement EHPS follow-up better constant"; "r_3 exact values A003002". Found no AI-driven move of the lower-bound constant. Found a June 2026 finite-analogue campaign (Ergezer, arXiv 2606.04016: MIP/SAT with DRAT proofs, r_3(212) >= 43; OEIS b-file to N=211) — finite analogue, not the headline; AI involvement not established.
S5 DELIVER  | PASS (moot) — named published bound: the EHPS constant / Raghavan exponent. Sentence: "We improve the constant in the Behrend-type lower bound for r_3(N) below 2 sqrt(log_2(24/7))." This is a PROOF-type step, not a witness step.
DIVERGENCE  | NONE FOUND — searched OEIS A003002 summary and the r_3(212) campaign; found one exact-computation frontier (N≈211/212) and no second dated method with reach ratio >= 2
BITS_SEARCH | UNDEFINED — no named ansatz plus published density estimate found
VERIF CLASS | PROOF (headline-level step); a finite witness would be CHECK
NOTES       | The brief's stated upper bound (log N)^{1/6}/loglog N matches Raghavan 2026 (preprint), newer than the Bloom–Sisask 1/9 that I recalled: my recall was stale. "Published" upper bound is an unrefereed preprint.
```

```
RECORD      | 199 — Exact Asymptotic Waring Function G(k)
QUANTITY    | G(k) for each k>=3 (least s with every sufficiently large integer a sum of s k-th powers)
LOWER       | RECALL only: G(3)>=4, G(4)=16 (Davenport 1939), G(k)>=k+1 generally, G(2^r)>=4*2^r; other k not recalled reliably | RECALL | EXACT ; REFEREED (classical)
UPPER       | RECALL only: G(3)<=7 (Linnik 1943); G(k) <= k(log k + log log k + O(1)) (Wooley 1992) with later constant improvements I cannot date; small-k values from Vaughan–Wooley not recalled reliably | RECALL | EXACT ; REFEREED
BOUND OBJ   | lower: PROOF — congruence/local obstruction arguments ; upper: PROOF — circle method / Hardy–Littlewood–Vinogradov, efficient congruencing
S0 OPEN     | CANNOT EVALUATE — RECALL says open in general (G(k) known only for k=2,4); no 2025-26 source read
S1 COUPLED  | FAIL — G(k) is a "for all sufficiently large N" statement: not an extremum over finite objects, and a finite computation cannot certify an upper bound on G (finitely many exceptions are asymptotic). Finite computation only bounds the threshold, not G. | RECALL
S2 VETO     | FAIL — no witness object; moving objects are PROOFs (the circle-method argument is not a finite string with decidable check)
MOVE-1      | UNKNOWN — most recent move not identified (no search)
MOVE-2      | NONE identified
S3 IDEA     | CANNOT EVALUATE — MOVE-1 unknown
S4 CROWDED  | CANNOT EVALUATE — did not search
S5 DELIVER  | CANNOT EVALUATE — no maintained table read
DIVERGENCE  | NONE FOUND — not searched
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF
NOTES       | All numbers here are RECALL and may be years stale. The brief's parenthetical about zeros/positive summands is a statement-equivalence, no issue found.
```

```
RECORD      | 246 — Zagier's dimension conjecture for classical multiple zeta values
QUANTITY    | dim_Q Z_k versus d_k (d_k = d_{k-2}+d_{k-3}), per weight k
LOWER       | RECALL: no general lower bound beyond trivial; transcendence input only (Apéry: zeta(3) irrational; Ball–Rivoal / Zudilin partial odd-zeta results) | RECALL | EXACT ; REFEREED
UPPER       | dim Z_k <= d_k — Terasoma 2002, Deligne–Goncharov 2005, Brown 2012 (mixed Tate motives over Z) | RECALL | EXACT ; REFEREED
BOUND OBJ   | lower: PROOF — transcendence/independence argument ; upper: PROOF (already established; motivic)
S0 OPEN     | CANNOT EVALUATE — RECALL: upper bound proved, lower bound (hence the equality) open; no 2026 source read; corpus label "open_with_solved_subcases" is consistent
S1 COUPLED  | FAIL — no side is moved by a witness. A numerical PSLQ relation among MZVs would be NUMERICAL, not a rigorous certificate; the upper bound d_k already holds, so a relation would need a proof of an identity outside the motivic framework. Lower side needs independence proofs. | RECALL
S2 VETO     | FAIL — no witness with a terminating exact/rigorous check
MOVE-1      | UNKNOWN — none dated (no search)
MOVE-2      | NONE
S3 IDEA     | CANNOT EVALUATE
S4 CROWDED  | CANNOT EVALUATE — did not search
S5 DELIVER  | CANNOT EVALUATE — I recall numerical MZV data-mine tables exist but did not read them
DIVERGENCE  | NONE FOUND — not searched
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF
NOTES       | Recall of large-weight numerical verifications (PSLQ up to about weight 22) is unsourced and is NUMERICAL evidence only.
```

```
RECORD      | 277 — Growth Rate of 3-Uniform Hypergraph Ramsey Numbers
QUANTITY    | r_3(t) growth: lower 2^{c t^2} versus upper 2^{2^{c t log t}}
LOWER       | RECALL: r_3(t) >= 2^{c t^2} (Erdős–Hajnal) | RECALL | EXACT ; REFEREED
UPPER       | RECALL: r_3(t) <= 2^{2^{c t log t}} (Erdős–Rado) | RECALL | EXACT ; REFEREED
BOUND OBJ   | lower: PROOF — improving to 2^{2^{ct}} needs a new construction family (a coloring per t; finite colorings only bound specific t) ; upper: PROOF
S0 OPEN     | PASS — Erdős problem 564 ("is R_3(n) >= 2^{2^{cn}} for some c>0?", $500) has status "open" (last_update 2025-08-31) in teorth/erdosproblems data/problems.yaml, and formal-conjectures ErdosProblems/564.lean is `research open`; Erdős 562 (r-uniform tower-height conjecture) also open | SECONDARY-RELAYED. No web search for 2026 resolution claims was possible, so a claim missing from the DB would not be seen.
S1 COUPLED  | CANNOT EVALUATE — asymptotic headline; a coloring of triples on N points with no monochromatic t-set is a finite witness for one t, but I could not read or recall reliably a published lifting theorem taking a finite 3-uniform coloring to an asymptotic bound (stepping-up as I recall goes from k-uniform to (k+1)-uniform for k>=3). Missing: statement of stepping-up for the 2→3 case and any 3-uniform lifting.
S2 VETO     | PASS — predicate "no monochromatic t-subset" is decidable by finite check (derived; exponential but terminating)
MOVE-1      | UNKNOWN — recent moves not searched
MOVE-2      | NONE
S3 IDEA     | CANNOT EVALUATE
S4 CROWDED  | CANNOT EVALUATE — did not search
S5 DELIVER  | CANNOT EVALUATE
DIVERGENCE  | NONE FOUND — not searched
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF for a headline improvement; CHECK for a finite coloring
NOTES       | Small-t exact values (e.g. r_3(4)=13) are finite analogues and do not bear on the headline.
```

```
RECORD      | 288 — Complex linearity of closed-surface mapping class groups by genus
QUANTITY    | the set of genera g>=3 with Mod(S_g) linear over C (a set of integers; no numeric bound)
LOWER       | NOT FOUND — RECALL: Mod(S_1)=SL2(Z) and Mod(S_2) are linear (Bigelow–Budney, Korkmaz); nothing known for g>=3 | RECALL | EXACT ; REFEREED
UPPER       | NOT FOUND — no nonlinearity result known for any g>=3 (RECALL) | RECALL | UNKNOWN
BOUND OBJ   | lower (linear genera): PROOF — a faithful representation whose injectivity needs a proof, not a finite check ; upper (nonlinear genera): PROOF
S0 OPEN     | CANNOT EVALUATE — RECALL open; no 2026 source read
S1 COUPLED  | FAIL — no numeric tracked quantity; both directions are PROOFs (faithfulness of an explicit representation is a universal statement) | RECALL
S2 VETO     | CANNOT EVALUATE — whether faithfulness of a given rep is decidable here I could not establish
MOVE-1      | NONE identified
MOVE-2      | NONE
S3 IDEA     | CANNOT EVALUATE
S4 CROWDED  | CANNOT EVALUATE — did not search
S5 DELIVER  | CANNOT EVALUATE
DIVERGENCE  | NONE FOUND — not searched
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF
NOTES       | Record shape (boolean per genus) does not fit the tracked-bound template.
```

```
RECORD      | 308 — Exact Real Grothendieck Constant
QUANTITY    | K_G^R = sup over real matrices of (SDP value)/(max over signs)
LOWER       | 6π/11 ≈ 1.713596, Saha–Li–Xue–Chaudhuri–Klivans–Kothari–Meka, arXiv 2608.11158, 11 Aug 2026 (previous: Davie 1984 / Reeds 1991 K_DR ≈ 1.676957; then K_DR+1e-12 Jones–Malavolta 31 Mar 2026; K_DR+1e-26 Heilman 2026) | SECONDARY-RELAYED (teorth/optimizationproblems README and constants/10a.md) + SEARCH-SUMMARY | EXACT (closed form) ; PREPRINT
UPPER       | π/(2 ln(1+√2)) − 1e-4 ≈ 1.78211, same team, arXiv 2608.11158, Aug 2026 (Krivine 1979 gave 1.782214; BMMN 2011 strict improvement; Heilman −1e-5; Li et al −6.039e-5). A newer preprint, Bo Peng arXiv 2609.20074 (17 Sep 2026), claims computer-assisted K_G <= 1.7813 (degree-11 Hermite threshold, degree-51 polynomial, interval-certified head plus analytic tail bound), and cites an intermediate "system-tested" 1.7813319810625639; not yet in the Tao table | SECONDARY-RELAYED for the table value; SEARCH-SUMMARY for Peng | EXACT for the closed form; RIGOROUS-NUMERIC for Peng ; PREPRINT
BOUND OBJ   | lower: WITNESS (route a: a matrix plus unit vectors with ratio above the record) — but the current record 6π/11 itself is a PROOF (limitations of Krivine schemes), and the relayed page says all earlier lower bounds came from explicit gap instances ; upper: PROOF (Krivine-type rounding scheme with analysis; Peng's is computer-assisted with an analytic tail)
S0 OPEN     | PASS — bounds 1.7136 <= K_G <= 1.7821 unequal | SECONDARY-RELAYED. Related claims are all bounds, none a resolution.
S1 COUPLED  | PASS — route (a): K_G is by definition a supremum over finite matrices of a ratio, so any single matrix with all unit vectors gives a lower bound on K_G itself (not a finite analogue). Cited: definition on constants/10a.md. Caveat: a matrix must beat 6π/11 to move the record. | SECONDARY-RELAYED (definition), RECALL (argument)
S2 VETO     | PASS — for explicit unit vectors the numerator is a finite sum (exact if rational vectors), the denominator is a max over finitely many sign patterns; terminating
MOVE-1      | 2026-08-11 | Saha, Li, Xue, Chaudhuri, Klivans, Kothari, Meka | 6π/11 | ANALYTIC +AI-SEARCH | relayed page: "proved by establishing asymptotic limitations of Krivine schemes rather than by constructing explicit gap instances"; authors state the bounds "were discovered by a long-running collaborative effort of humans and a long-horizon AI research system that we engineered" | SECONDARY-RELAYED (Tao page text; paper not read)
MOVE-2      | 2026-03-31 | Jones, Malavolta | K_DR + 1e-12 | ANALYTIC | "perturbative analysis of the Davie–Reeds operator" (Heilman concurrent, K_DR+1e-26) | SECONDARY-RELAYED
S3 IDEA     | PASS — MOVE-1 kind ANALYTIC (but note this move was not a witness)
S4 CROWDED  | FAIL — coupled (lower) side moved on 2026-08-11 by a human plus long-horizon AI research system, per the authors. Searches: 4 queries on K_G bounds/AI/Frank-Wolfe.
S5 DELIVER  | PASS — named table: Tao–Davis–Ivanisvili optimization-constants repo, entry 10a (lower bound column). Sentence: "We exhibit an explicit matrix whose Grothendieck ratio exceeds 6π/11, improving the lower bound on the real Grothendieck constant."
DIVERGENCE  | Only at mixed precision, finite-order analogue K_G(d): certified Frank-Wolfe lower bounds for 3<=d<=9 (arXiv 2409.03739, 2024, SEARCH-SUMMARY, published per search) versus heuristic see-saw candidate bounds for d up to 24 (arXiv 2609.35399, 2026 preprint; NUMERICAL, "conditional on conjectured binary optima being exact"). Ratio 24/9 ≈ 2.67, but the larger reach is not rigorous and the object is K_G(d), not K_G.
BITS_SEARCH | UNDEFINED — 2609.35399 describes cubic-kernel ansatz but no density estimate seen
VERIF CLASS | RIGOROUS-NUMERIC in general (CHECK if the unit vectors are exact rational)
NOTES       | Tao repo table upper bound (1.78211) lags Peng 2609.20074. The heuristic paper 2609.35399 conjectures K_G >= 9π/16 ≈ 1.767146 (unproved). The brief's premise "lower bound is a witness object" is only partly true: the newest lower bound is not. Surprising for the adjudicator: this record is coupled but already crowded by an AI system.
```

```
RECORD      | 351 — Exact Capacity Region of the Two-User Gaussian Interference Channel
QUANTITY    | capacity region of the Gaussian IC in the weak/moderately weak interference regime (a set of rate pairs)
LOWER       | RECALL: Han–Kobayashi achievable region with Gaussian inputs; Etkin–Tse–Wang 2008 within 1 bit of capacity | RECALL | EXACT ; REFEREED
UPPER       | RECALL: genie-aided outer bounds (Etkin–Tse–Wang; Kramer); sum capacity known in the noisy-interference regime (Shang–Kramer–Chen, Motahari–Khandani, Annapureddy–Veeravalli 2009); strong-interference region known (Sato, Han–Kobayashi 1981) | RECALL | EXACT ; REFEREED
BOUND OBJ   | lower: PROOF/ALGORITHM — a coding scheme with achievability proof ; upper: PROOF — converse
S0 OPEN     | CANNOT EVALUATE — RECALL: strong regime solved, weak-regime region open; no 2026 source read
S1 COUPLED  | FAIL — region of rate pairs; inner bound moved by a coding scheme with a proof, outer bound by a converse; no finite witness fixes a bound | RECALL
S2 VETO     | FAIL — the bound object is a coding scheme (ALGORITHM/PROOF)
MOVE-1      | UNKNOWN — none dated
MOVE-2      | NONE
S3 IDEA     | CANNOT EVALUATE
S4 CROWDED  | CANNOT EVALUATE — did not search
S5 DELIVER  | CANNOT EVALUATE
DIVERGENCE  | NONE FOUND — not searched
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF
NOTES       | Headline mixes solved (strong) and open (moderately weak) regimes; the brief's "in the moderately weak and strong regimes" includes a solved subcase per RECALL.
```

```
RECORD      | 353 — Asymptotic Turán Numbers of Even Cycles
QUANTITY    | exponent/order of ex(n,C_{2k}) for fixed k
LOWER       | RECALL: Ω(n^{1+2/(3k-3+ε)}) with ε in {0,1} by parity (Lazebnik–Ustimenko–Woldar 1995); Θ(n^{1+1/k}) only for k=2,3,5 (Erdős–Rényi–Sós/Brown; Benson; Wenger) | RECALL | EXACT ; REFEREED
UPPER       | RECALL: O(k n^{1+1/k}) (Bondy–Simonovits 1974), constants improved by Verstraëte, Pikhurko, Bukh–Jiang (80 sqrt(k) log k), later ones I cannot date | RECALL | EXACT ; REFEREED
BOUND OBJ   | lower: PROOF — algebraic graph families with girth arguments (a fixed finite graph bounds one n) ; upper: PROOF
S0 OPEN     | PASS — Erdős problem 572 (ex(n;C_{2k}) >> n^{1+1/k}, k>=3) has status "open" in teorth/erdosproblems data/problems.yaml at HEAD (formalized 2026-09-09) and `research open` in formal-conjectures ErdosProblems/572.lean; the file cites Bondy–Simonovits and LUW95 | SECONDARY-RELAYED. It covers only the lower-bound question; no 2026 web search was possible.
S1 COUPLED  | CANNOT EVALUATE — asymptotic headline; ex(n,C_{2k}) is a max over graphs (finite analogue only). I know of no lifting theorem from a finite C_{2k}-free graph to an exponent, but could not search for one. Missing: any literature check for such a lifting.
S2 VETO     | PASS — "C_{2k}-free" is decidable on a finite graph
MOVE-1      | UNKNOWN — not searched
MOVE-2      | NONE
S3 IDEA     | CANNOT EVALUATE
S4 CROWDED  | CANNOT EVALUATE — did not search
S5 DELIVER  | CANNOT EVALUATE
DIVERGENCE  | NONE FOUND — not searched
BITS_SEARCH | UNDEFINED
VERIF CLASS | PROOF for exponent moves; CHECK for a finite graph
NOTES       | formal-conjectures 572.lean says k>=3 although k=3 and 5 have matching bounds by RECALL; the Lean file statement differs from my recall.
```

```
RECORD      | 368 — Thomson problem
QUANTITY    | C(N) = minimum Coulomb energy of N points on S^2, per N (upper bounds by configurations, lower bounds by LP/SDP or proof)
LOWER       | exactly proved optimal only for N=1..6 (Yudin N=4,6; Schwartz N=5, computer-assisted, 2013) and N=12 (Cohn–Kumar 2007); N=8 square antiprism claimed in arXiv 2609.22077 (Sept 2026, Lean-checked, computer-assisted for all s>=0) and in an AI-produced Lean "warrant" (Tooby-Smith, Zughaid; N=7 claimed "trivial" by same techniques, unverified). General-N lower bounds: LP (Yudin) and three-point SDP (Cohn–Woo) certificates, values NOT FOUND | SEARCH-SUMMARY (proved cases), SECONDARY-RELAYED (warrant README) | EXACT for proved N ; REFEREED for N<=6,12 ; PREPRINT/ANNOUNCED for N=8
UPPER       | best-known configuration energies per N: Wales Cambridge Cluster Database (RECALL, unreadable) ; Lai–Hao–Xiao–Fu (Expert Systems with Applications 238, 2024) improved N=360 ; E(282)=37147.294418 matched by AlphaEvolve (EinsteinArena); Lavrov–Nikonov, Zenodo 2026-09-14, first lowest-known configurations for N=5000, 7500, 10000 (method unread). Specific values other than N=282 NOT FOUND | SEARCH-SUMMARY | NUMERICAL (putative minima; energies could be certified RIGOROUS-NUMERIC) ; REFEREED for Lai 2024, ANNOUNCED for Zenodo data
BOUND OBJ   | lower: PROOF (LP/SDP certificate plus argument; finite certificates only for special N) ; upper: WITNESS — a point configuration whose energy is computed by terminating arithmetic
S0 OPEN     | PASS — headline "for each N" unresolved: proved for N in {1..6,12}, N=8 newly claimed (preprint), all other N putative only | SEARCH-SUMMARY, SECONDARY-RELAYED. Resolution claims: N=8 (arXiv 2609.22077, PREPRINT; AI-produced Lean warrant, self-described as "not a proof") — data, not a resolution of the headline.
S1 COUPLED  | PASS — route (a): C(N) is a min over configurations, so any configuration gives a published-bound-type upper estimate on C(N) for that fixed N (per-N headline, not a finite analogue). Cited: definition in AlphaEvolve problem 33 statement (local aerp_problems_2026-09-29.json) | SECONDARY-RELAYED (local file), RECALL (tables)
S2 VETO     | PASS — energy is an explicit closed form; a configuration's energy is computable by interval arithmetic in finite time
MOVE-1      | 2026-09-14 | Lavrov, Nikonov | lowest-known energies for N=5000/7500/10000 (first entries) | UNKNOWN | search summary gives no method; no earlier record for those N | SEARCH-SUMMARY
MOVE-2      | 2024 | Lai, Hao, Xiao, Fu | improved best-known energy at N=360 | SEARCH-NEW | "population-based algorithm with two-phase local optimisation, early stopping, random perturbation, distance-based population update with a novel distance function, population rebuilding" | SEARCH-SUMMARY
S3 IDEA     | CANNOT EVALUATE — most recent dated move has kind UNKNOWN, and recency itself cannot be established because the maintained table's history is unreadable
S4 CROWDED  | CANNOT EVALUATE — AI arm: searched "Thomson AlphaEvolve/RL/ML/GPU record", "AlphaEvolve Thomson N=282", "EinsteinArena N=282 ..." and read local status grid: AlphaEvolve problem 33 = "Matched literature bound / N/A" (no improvement); EinsteinArena N=282 holds 37147.294418 (the known value). Found no AI-driven improvement. Unevaluated: the "large-scale optimisation tooling" arm (Zenodo N>=5000 data, method unread; Wales table history blocked).
S5 DELIVER  | PASS — named table: Cambridge Cluster Database Thomson entries (RECALL); also Lai et al. 2024 tables (SEARCH-SUMMARY). Sentence: "We report a configuration of N unit charges on the sphere with Coulomb energy lower than the previously best-known value, improving the putative minimum energy at N."
DIVERGENCE  | Across senses only: proof frontier N=12 (Cohn–Kumar 2007, EXACT, REFEREED; or N=8 preprint) versus numerical frontier N=10000 (Lavrov–Nikonov 2026, NUMERICAL, ANNOUNCED), ratio ≈ 833 (or 1250) — not comparable claims. Within numerical: Wales table to N≈972 (RECALL) versus N=10000, ratio ≈ 10, but the N=10000 configurations are not verified minima.
BITS_SEARCH | UNDEFINED — arXiv 2506.08398 (search summary) says the number of local minima grows exponentially with N, but no ansatz-plus-density estimate for witnesses
VERIF CLASS | RIGOROUS-NUMERIC
NOTES       | Local outcomes file marks AlphaEvolve problem 33 as "light" (matched literature). Bounds tables for this record could not be read (blocked class). The N=8 claim postdates the brief's "open_with_solved_subcases" label.
```

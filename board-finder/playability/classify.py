#!/usr/bin/env python3
"""Witness-reachability classification of the ProofAtlas top-500 ranking.

Criterion, applied to every record's exactTarget:

    Is there a SINGLE FINITE OBJECT, checkable by a terminating computation,
    that settles one branch of the problem?

Two sweeps produced a 55-item and an 86-item candidate pool; every candidate
was then adjudicated by hand and the verdict recorded in VERDICTS below.
Records absent from VERDICTS are class U. The lexical sweeps are reproduced
here only so the recall path is auditable -- they are NOT the classifier.

Usage:  python3 classify.py            # writes classification.json, prints census
"""
import json, re, collections, statistics, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, 'ranking_v16.json')
OUT  = os.path.join(HERE, 'classification.json')

# --------------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------------
CLASSES = {
 'P1' : 'existence-headed; the YES branch is a finite checkable witness',
 'P2' : 'universal-headed; the NO branch is a finite checkable counterexample',
 'P2n': 'as P2, but the certificate is rigorous-numeric rather than exact-symbolic',
 'P2p': 'as P2, but only ONE of the failure modes is finitely certifiable',
 'W'  : 'a finite witness exists but its defining predicate is not decidable',
 'A'  : 'existence of an ALGORITHM; witness finite, correctness universal',
 'II' : 'exact-value / optimality determination (a record, not a witness)',
 'U'  : 'no finite witness on either branch',
}
PLAYABLE = ('P1', 'P2', 'P2n', 'P2p')

# --------------------------------------------------------------------------
# Hand-adjudicated verdicts.  rank -> (class, what the witness is)
# --------------------------------------------------------------------------
VERDICTS = {
  # ---- P1: exhibit the object -------------------------------------------
   49: ('P1', 'a polynomial over Q with Galois group G; per-group instance'),
  106: ('P1', 'a curve plus r independent points certifies rank >= r'),
  132: ('P1', 'a rational point on y^2=x^3-n^2x certifies n congruent (YES side only)'),
  235: ('P1', 'd^2 vectors with |<vi,vj>|^2=1/(d+1); exact algebraic SICs are known'),
  239: ('P1', 'an odd N with sigma(N)=2N; the divisor sum is checkable'),
  331: ('P1', 'a Hadamard matrix of order 4k; H H^T = 4k I'),
  390: ('P1', 'for fixed r, a colouring of [1,N] is a finite SAT instance'),
  393: ('P1', 'an incidence structure of order 12; finite check'),
  426: ('P1', '7 MUBs in D=6 would be an explicit finite set of bases'),
  # ---- P2: exhibit the counterexample ------------------------------------
   22: ('P2', 'one even n admitting no prime pair'),
   79: ('P2', 'one graph with no K_{t+1} minor that is not t-colourable'),
  257: ('P2', 'a finite H plus a rational step graphon refutes the inequality'),
  273: ('P2', 'one prime p with p | h+(Q(zeta_p))'),
  275: ('P2', 'one triple (p,E,E-prime); isogeny classes are computable'),
  280: ('P2', 'an explicit idempotent in K[G]; cf. Gardam on the unit conjecture'),
  287: ('P2', 'one finite group; k_0(B) is computable'),
  295: ('P2', 'one finite bridgeless graph with no such flow'),
  300: ('P2', 'one finite group / block'),
  307: ('P2', 'one n; the inner existential is bounded, so the predicate is decidable'),
  322: ('P2', 'two finite graphs sharing a deck'),
  335: ('P2', 'one diagram; Jones is computable and unknot recognition is decidable'),
  345: ('P2', '2^(n-2)+1 points in general position with no n in convex position'),
  348: ('P2', 'one 6-tuple A^x+B^y=C^z with A,B,C coprime'),
  355: ('P2', 'one 4-edge-connected multigraph with no nowhere-zero 3-flow'),
  356: ('P2', 'one finite group with k(B) > |D|'),
  401: ('P2', 'two Bruhat intervals; KL polynomials are computable'),
  429: ('P2', 'one vertex-transitive graph with no Hamiltonian path'),
  458: ('P2', 'one k-uniform family F exceeding the stated bound'),
  472: ('P2', 'one finite group; character table and Galois action are computable'),
  488: ('P2', 'one pair (x,y) with pi(x+y) > pi(x)+pi(y)'),
  493: ('P2', 'one parallelohedron that is not affinely Voronoi'),
  495: ('P2', 'one multigraph with list index > chromatic index'),
  500: ('P2', 'one n with tau(n)=0'),
  # ---- weaker certificates ----------------------------------------------
    9: ('P2n', 'an off-line zero rigorously boxed by the argument principle'),
  161: ('P2p', 'a cycle is a finite certificate; a divergent trajectory is not'),
  # ---- finite witness, undecidable predicate -----------------------------
  299: ('W', 'a knot diagram -- but "slice and not ribbon" is not decidable'),
  474: ('W', 'a finite group -- but contractibility of the order complex is not'),
  # ---- algorithm-existence ----------------------------------------------
   16: ('A', 'polynomial-time integer factorization'),
   24: ('A', "Hilbert's Tenth over Q"),
   80: ('A', 'graph isomorphism in P'),
  129: ('A', 'a simplex pivot rule'),
  203: ('A', 'effective Roth'),
  212: ('A', 'the Skolem problem'),
  236: ('A', 'perfect matching in deterministic NC'),
  247: ('A', 'constant-query locally decodable codes'),
  259: ('A', 'SDP feasibility in P'),
  310: ('A', 'deterministic exact bipartite matching'),
  339: ('A', 'polynomial-time unknot recognition'),
  411: ('A', 'the P-matrix linear complementarity problem'),
  434: ('A', 'computability of the Shannon capacity of finite graphs'),
  463: ('A', "Hilbert's Tenth over C(t)"),
  465: ('A', "Condon's simple stochastic games"),
  498: ('A', 'a positive counting rule for Schubert structure constants'),
  # ---- exact value / optimality -----------------------------------------
   17: ('II', ''), 186: ('II', ''), 199: ('II', ''), 221: ('II', ''),
  246: ('II', ''), 277: ('II', ''), 282: ('II', ''), 288: ('II', ''),
  308: ('II', ''), 337: ('II', ''), 351: ('II', ''), 353: ('II', ''),
  368: ('II', ''), 375: ('II', ''), 385: ('II', ''), 410: ('II', ''),
  413: ('II', ''), 417: ('II', ''), 428: ('II', ''), 441: ('II', ''),
  450: ('II', ''), 479: ('II', ''),
}

# --------------------------------------------------------------------------
# Recall sweeps -- kept so the candidate pool is auditable, not used to classify
# --------------------------------------------------------------------------
EX = re.compile(r'(there exists?\b|there is a\b|there are\b|\bexhibit\b|\bconstruct\b'
                r'|\bdoes there exist\b|\bexistence of\b|\bfind a\b|\bfind an\b|\bsome\b)', re.I)
UN = re.compile(r'(\bfor every\b|\bfor all\b|\bfor any\b|\bfor each\b|\bevery\b'
                r'|\ball \b|\beach \b|\bany \b|\bnever\b|\bno \b)', re.I)
# PROMPT.md step 2 (the leak table) needs a bound with pushable parameters.
QUANT = re.compile(r'(O\(|Omega\(|Theta\(|\bsqrt|\^\{|\blog\b|asymptot|order of magnitude'
                   r'|\bat most\b|\bat least\b|<=|>=|\bbound\b|\bexponent\b|\brate\b'
                   r'|\bconstant\b|\bdiscrepancy\b|\bcomplexity\b|\bdimension\b)', re.I)

def prefix(t):
    """Which quantifier heads the statement. An existential NESTED under a
    universal does not make a problem playable -- its witness is a constant."""
    e, u = EX.search(t), UN.search(t)
    if e and u: return 'E' if e.start() < u.start() else 'U'
    return 'E' if e else ('U' if u else None)

# --------------------------------------------------------------------------
def main():
    d = json.load(open(SRC))
    recs = d['records']
    rows = []
    for r in recs:
        rank = r['releaseRank']
        cls, why = VERDICTS.get(rank, ('U', ''))
        ws = r.get('researchWorkspaces') or []
        rows.append(dict(
            rank=rank, problemId=r['problemId'], title=r['canonicalTitle'],
            cls=cls, witness=why, playable=cls in PLAYABLE,
            domain=r['primaryDomain'], status=r['releaseStatus'],
            familyId=r.get('familyId'), familyMemberCount=r.get('familyMemberCount'),
            hasWorkspace=bool(ws), workspaceCount=len(ws),
            quantitative=bool(QUANT.search(r['exactTarget'])),
            quantifierPrefix=prefix(r['exactTarget']),
            exactTarget=r['exactTarget'],
        ))
    rows.sort(key=lambda x: x['rank'])
    json.dump(dict(
        source=d['publicationId'], releaseVersion=d['releaseVersion'],
        editionDate=d['editionDate'], classes=CLASSES, records=rows,
    ), open(OUT, 'w'), indent=1)

    n = len(rows)
    cnt = collections.Counter(x['cls'] for x in rows)
    print(f'n = {n}')
    for c in ['P1','P2','P2n','P2p','W','A','II','U']:
        print(f'  {c:4s} {cnt[c]:3d}  {100*cnt[c]/n:5.1f}%')
    play = [x for x in rows if x['playable']]
    print(f'\nfinite-witness playable: {len(play)}/{n} = {100*len(play)/n:.1f}%')

    print('\nplayable by rank band:')
    for lo in range(0, 500, 50):
        sub = [x for x in rows if lo < x['rank'] <= lo+50]
        p = sum(1 for x in sub if x['playable'])
        print(f'  {lo+1:3d}-{lo+50:3d}: {p:2d}/{len(sub):2d}  ' + '#'*p)

    print('\nplayable by domain:')
    dn = collections.Counter(x['domain'] for x in rows)
    dp = collections.Counter(x['domain'] for x in play)
    for dom, tot in dn.most_common():
        print(f'  {dp[dom]:2d}/{tot:3d}  {100*dp[dom]/tot:4.1f}%  {dom}')

    ws = [x for x in rows if x['hasWorkspace']]
    pw = [x for x in play if x['hasWorkspace']]
    print(f'\nworkspaces: {len(ws)}/{n} ({100*len(ws)/n:.0f}%) overall, '
          f'{len(pw)}/{len(play)} ({100*len(pw)/len(play):.0f}%) of playable')
    print('workspace density by rank band:')
    for lo in range(0, 500, 50):
        sub = [x for x in rows if lo < x['rank'] <= lo+50]
        w = sum(1 for x in sub if x['hasWorkspace'])
        print(f'  {lo+1:3d}-{lo+50:3d}: {w:2d}/{len(sub):2d} {100*w/len(sub):5.1f}%  ' + '#'*w)

    print('\nPLAYABLE AND UNWORKSPACED:')
    for x in play:
        if not x['hasWorkspace']:
            print(f"  {x['rank']:3d} [{x['cls']:3s}] {x['title'][:62]}")

    q = [x for x in rows if x['quantitative']]
    print(f'\nleak-table applicable (quantitative target, lexical upper bound): '
          f'{len(q)}/{n} = {100*len(q)/n:.0f}%')
    print(f'  of the {len(play)} playable: {sum(1 for x in play if x["quantitative"])} quantitative, '
          f'{sum(1 for x in play if not x["quantitative"])} purely yes/no')

if __name__ == '__main__':
    main()

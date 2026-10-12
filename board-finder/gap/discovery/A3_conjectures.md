# A3 — bounded test of conjecture generation (DRAFT, written incrementally)

STATUS: Step 1 done (12 statements written down BEFORE any check was run). Checks in progress.
Counts/lists section will be filled in at the end (see "DERIVED COUNTS" — currently empty).

## DERIVED COUNTS AND LISTS

(to be filled after all twelve are checked)

## NOTATION (used in the statements)

For A in {+1,-1}^n (or {-1,0,+1}^n), indices in Z_n:
PAF_A(s) = sum_{i in Z_n} A(i) A(i+s mod n)   (periodic autocorrelation)
NAF_A(s) = sum_{i=0}^{n-1-s} A(i) A(i+s)      (aperiodic autocorrelation), E(A) = sum_{s=1}^{n-1} NAF_A(s)^2.
"Skew-symmetric" (n = 2m+1): A(m+i) = (-1)^i A(m-i) for 1 <= i <= m.
"Symmetric": A(-s) = A(s) in Z_n.

## STEP 1 — THE TWELVE STATEMENTS (frozen text, written before any checking)

C1  For every odd n with 3 <= n <= 41 there exist A, B in {+-1}^n with PAF_A(s) + PAF_B(s) = -2 for every s in Z_n \ {0}.

C2  For every odd n with 3 <= n <= 41 such that 4n-2 is a sum of two integer squares, there exist A, B in {+-1}^n with PAF_A(s) + PAF_B(s) = +2 for every s in Z_n \ {0}. (Two-circulant D-optimal design of order 2n.)

C3  There exists A in {+-1}^34 with PAF_A(s) in {+2, -2} for every s in Z_34 \ {0}.

C4  For every odd n with 3 <= n <= 41: min over all A in {+-1}^n of E(A) equals min over skew-symmetric A in {+-1}^n of E(A).

C5  There exists an integer v, 3 <= v <= 63, v = 3 mod 4, such that (i) v is not prime, AND (ii) v != 2^m - 1 for every m, AND (iii) v is not q(q+2) with q and q+2 both prime powers, AND (iv) Z_v contains a cyclic Hadamard difference set, i.e. a subset D with |D| = (v-1)/2 whose +-1 indicator A satisfies PAF_A(s) = -1 for all s != 0.

C6  For every n with 2 <= n <= 10 and every integer w with 1 <= w <= 2n that is a sum of two integer squares, there exist A, B in {-1,0,+1}^n with wt(A) + wt(B) = w (wt = number of nonzero entries) and PAF_A(s) + PAF_B(s) = 0 for every s in Z_n \ {0}.

C7  For every prime p = 1 mod 4 with 5 <= p <= 101 there exists A in {+-1}^p with PAF_A(s) in {+1, -3} for every s in Z_p \ {0}.

C8  There exists a Hadamard matrix of order 668.

C9  Turyn-type sequences of length 42 exist: there exist A, B, C in {+-1}^42 and D in {+-1}^41 with NAF_A(s) + NAF_B(s) + 2 NAF_C(s) + 2 NAF_D(s) = 0 for every 1 <= s <= 41 (NAF_D(41) := 0).

C10 There exist A, B in {+-1}^90 with PAF_A(s) + PAF_B(s) = 0 for every s in Z_90 \ {0} (a periodic Golay pair of length 90).

C11 For every prime p = 1 mod 4 with 5 <= p <= 61 there exist A in {+-1}^p and a unit u in Z_p^* such that PAF_A(s) + PAF_A(us) = -2 for every s in Z_p \ {0}. (An SDS(-2) pair B = A o u that is a multiplier-image of A.)

C12 For every odd n with 3 <= n <= 41 such that 4n-2 is a sum of two integer squares, there exist SYMMETRIC A, B in {+-1}^n (A(-s)=A(s), B(-s)=B(s)) with PAF_A(s) + PAF_B(s) = +2 for every s in Z_n \ {0}.

(Per-statement blocks with checks follow below as they are completed.)

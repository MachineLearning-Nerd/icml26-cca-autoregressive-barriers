# Claim-to-evidence audit

The four anchored claims are listed in `repro/configs/live_claims.json`. The
first three correspond to the paper's two barriers and the fourth records their
direct Section 4 composition consequence.

| Claim | Producer | Evidence | Interpretation |
| --- | --- | --- | --- |
| C1 — next-token `(0,0)`-CCA can fail sequence-level `(ε,δ)`-CCA | `run_theorem4.py` → `theorem4.witness()` → `verify_claims.py` | 42 cells from 7 epsilon values × 6 delta values; exact finite support, conditional uncredited law, counterfactual law, and strict event inequality | `VERIFIED_SCOPED`; the grid is evidence for the paper's displayed construction, not a formal universal proof. |
| C2 — rollout CCA can require more than the per-token guarantee suggests | `theorem4.max_dp_log_ratio()` plus `proof_audits.py` | 42 path-bound cells and 24 independently generated branching trace systems | `VERIFIED_SCOPED`; the finite-support oracle is two-sided and can report infinity when support differs, while the paper's finite certificate `-log(p)` is checked separately. |
| C3 — approximate CCA retrofit needs exponentially many queries | `run_theorem5.py` → `theorem5.optimal_credit_lp()` | 3,048 cells: all marked strings for lengths 1–7, 4 epsilon values, and 3 gamma values; each LP recovers gamma and each decision tree reaches `2^ell` | `VERIFIED_SCOPED`; the exact finite family and the independently checked reduction support the stated lower-bound mechanism. |
| C4 — next-token CCA does not compose autoregressively | `verify_claims.py` bound to `theorem4.rollout()` | The same exact counterexample as C1, with an independently implemented rollout oracle | `VERIFIED_SCOPED`; this is a consequence claim, not a second model implementation. |

## Producer details

### Theorem 4 construction

`repro/src/theorem4.py` encodes only the finite predictor printed in the paper:
the token support is `{a,b}` with a terminal marker, and the document-present
and document-removed kernels are represented explicitly. It enumerates both
the next-token law and the finite autoregressive rollout. The verifier checks
that every witness has per-token zero-CCA support and violates the declared
rollout event inequality.

### Theorem 4.3 path certificate

For each witness, the code reports the paper's finite path certificate
`-log(p)`. The same module also computes the smallest two-sided pure-DP
epsilon for the finite conditional and counterfactual output laws. The
independent `proof_audits.py` module uses separately generated branching
probabilities to check the trace-product inequality rather than importing the
counterexample's intermediate values.

### Section 5 hard family

`repro/src/theorem5.py` constructs the marked-string family `M_z`. The LP keeps
the no-credit mass as variables and maximizes retained mass subject to the two
pure-CCA likelihood inequalities. The marked-string oracle exposes no
target-specific answer until the hidden string is queried, so exhaustive
deterministic search records the exact `2^ell` worst case. The proof audit also
checks the interval bound, the Yao query floor, and the prefix-recovery sample
count used in the retrofit reduction.

## Negative and scope controls

- The tests include exact support checks and a strict rollout violation check.
- The LP test uses a target and parameters not used by the producer's first
  row, and the decision-tree test reaches length 6.
- The source PDF is hash-pinned; no author executable is imported or run.
- The finite grid does not by itself prove an asymptotic theorem or certify
  every possible epsilon, delta, alpha, or gamma value.

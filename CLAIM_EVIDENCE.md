# Claim-to-evidence audit

This dossier separates the four anchored finite claims from the paper's
formal proofs and asymptotic interpretation.

| Claim | Status | Producer path | Checker path | Evidence boundary |
| --- | --- | --- | --- | --- |
| C1 — a next-token (0,0)-CCA predictor can fail sequence-level (epsilon,delta)-CCA | VERIFIED_SCOPED | <code>run_theorem4.py</code> and <code>theorem4.witness()</code> | <code>verify_claims.py</code> and focused tests | 42 exact finite witness cells; not a formal universal proof. |
| C2 — rollout CCA can require more than the per-token guarantee suggests | VERIFIED_SCOPED | <code>theorem4.max_dp_log_ratio()</code> and <code>proof_audits.py</code> | finite path certificate and independent branching traces | 42 construction cells plus 24 independently generated trace cells; pathwise certificate is checked separately. |
| C3 — approximate CCA retrofitting needs exponentially many black-box queries | VERIFIED_SCOPED | <code>run_theorem5.py</code> and <code>theorem5.optimal_credit_lp()</code> | LP, decision-tree, Yao, and sample-complexity checks | 3,048 hard-family cells through length 7 plus independent reduction checks; asymptotic theorem remains paper-level. |
| C4 — next-token CCA does not compose autoregressively | VERIFIED_SCOPED | <code>verify_claims.py</code> bound to <code>theorem4.rollout()</code> | same independent rollout oracle as C1 | Direct consequence of the exact C1 counterexample; no second model is asserted. |

## C1 and C4

The clean-room finite-state oracle encodes the paper's binary-token predictor,
terminal marker, document-present/document-removed kernels, and autoregressive
rollout. Across 7 epsilon and 6 delta settings it verifies exact support,
conditional uncredited law, counterfactual law, and a strict sequence-level
event inequality. C4 is the direct composition consequence of that same
counterexample.

## C2

The oracle computes the two-sided finite-support rollout parameter and the
paper's pathwise certificate <code>-log(p)</code>. The independent proof audit
generates separate branching probabilities and checks trace multiplication and
normalization. Support mismatch is retained as a real boundary, not hidden by
a finite numerical approximation.

## C3

The hard family <code>M_z</code> is solved by exact augmentation LPs. Every
marked string through length 7 is checked across 4 epsilon values and 3 gamma
values, for 3,048 cells. The marked-string decision tree reaches exactly
<code>2^ell</code> worst-case queries. Independent cells audit the interval
bound, Yao query floor, and prefix-recovery sample complexity.

## Explicit non-claims

- The finite grids do not replace the paper's formal proof or establish every
  possible parameter value.
- No language model is trained or evaluated.
- No author executable, dataset, empirical benchmark, or external score is
  claimed.

# Barriers to Counterfactual Credit Attribution for Autoregressive Models

Full-scope reproduction of the four current ICML 2026 challenge claims for
OpenReview `F8dIPCR1ly` / arXiv `2605.01425`.

The evidence is an exact construction audit, not a language-model proxy:

- Theorem 4.2: enumerate the published finite counterexample and check both
  the per-token `(0,0)`-CCA property and the rollout violation for every
  sampled `(epsilon, delta, p)` witness.
- Theorem 4.3: independently calculate the pathwise lower bound from rollout
  probabilities and compare it with the minimal exact CCA parameter.
- Theorem 5.5: enumerate the paper's `M_z` family across a full length grid,
  solve its optimal-credit LP independently, and verify the explicit
  query-complexity reduction.
- Section 4: bind the duplicated composition-consequence claim to the same
  construction while requiring an independently implemented rollout oracle.

No external model, training run, or reduced-scale benchmark is used.

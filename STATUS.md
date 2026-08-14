# Status

- Paper: *Barriers to Counterfactual Credit Attribution for Autoregressive Models*
- Authors: Aloni Cohen; Chenhao Zhang
- OpenReview: `F8dIPCR1ly`
- arXiv: `2605.01425v1`
- State: `SCOPED_PASS`
- Strict paper-level status: `NOT_READY`
- Canonical branch: `main`

## Current evidence

- Theorem 4.2/4.3: 42 predeclared `(epsilon, delta)` witness cells pass exact
  support checks, rollout violation checks, and the pathwise lower-bound
  comparison.
- Independent Theorem 4.3 audit: 24 branching trace cells pass the chain-rule
  multiplication and normalization checks.
- Section 5: 3,048 exact LP cells cover every marked string for lengths 1–7,
  four epsilon values, and three gamma values. Every LP recovers the claimed
  credit; the marked-string search requires exactly `2^ell` queries.
- Independent Section 5 audit: 72 LP proof cells plus six Yao query-floor and
  six sample-complexity cells pass.
- Focused tests pass with the pinned dependencies in `repro/requirements.txt`.

The final gate writes the current hashes and detailed machine-readable results
to `publication_gate.json` and the matching files in `outputs/`.

## Limits

This is a clean-room audit of the finite constructions and selected proof
steps. It is not a formal proof checker, does not train or evaluate a model,
and does not execute author code. No dataset, GPU run, or empirical benchmark
is part of this theory-paper repository.

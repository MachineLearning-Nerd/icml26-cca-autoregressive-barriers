# Scoped reproduction report

## Final verdict

| Claim | Verdict | Meaning |
| --- | --- | --- |
| C1 | VERIFIED_SCOPED | The exact finite Theorem 4.2 counterexample passes across 42 declared parameter cells. |
| C2 | VERIFIED_SCOPED | The pathwise rollout certificate and independent branching-trace audit pass. |
| C3 | VERIFIED_SCOPED | Exact LP and query-tree cells recover the finite hard family and its exponential search mechanism. |
| C4 | VERIFIED_SCOPED | The direct autoregressive non-composition consequence is reproduced from the C1 oracle. |

The publication gate is <code>SCOPED_PASS</code> with overall status
<code>VERIFIED_SCOPED_WITH_EXACT_FINITE_CONSTRUCTION_AUDIT</code>. The strict
paper-level status remains <code>NOT_READY</code>.

## Established

- 42 exact Theorem 4 witness cells pass.
- 24 independent branching trace systems and 108 proof-audit rows pass.
- 3,048 Theorem 5 hard-family LP cells pass, with exact worst-case query
  search through length 7.
- Evidence, source PDF, claim contract, and artifact manifest are hash-bound.

## Not established

- Finite checks do not replace the paper's formal proofs or prove all
  asymptotic quantifiers.
- No autoregressive model, dataset, benchmark, author executable, or score is
  reproduced.

## Publication policy

Publish the finite construction audit with its limits. Do not present it as a
machine-checked proof or as empirical evidence about a trained language model.

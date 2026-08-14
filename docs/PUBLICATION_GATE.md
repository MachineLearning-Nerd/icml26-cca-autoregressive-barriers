# Publication gate

`repro/src/publication_gate.py` is the deterministic final gate for this
repository. It passes only when the declared finite evidence can be regenerated
and every public artifact is hash-consistent.

The gate:

1. regenerates the Theorem 4 witness grid, Section 5 LP grid, and independent
   proof-audit CSV;
2. reruns `verify_claims.py` and the focused pytest suite;
3. rebuilds the evidence bundle and deterministic artifact manifest;
4. checks the pinned paper hash, claim count, row counts, bundle records, and
   manifest records;
5. rejects tracked private workspace exports or stale `.trackio` metadata; and
6. writes byte-identical gate JSON files at the root and under `outputs/`.

The gate status is `SCOPED_PASS` with overall status
`VERIFIED_SCOPED_WITH_EXACT_FINITE_CONSTRUCTION_AUDIT`. `NOT_READY` remains the
strict paper-level status because formal proofs, author code, and empirical
experiments are outside this clean-room theory audit.

# Complete branch and history map

## Top-level refs

| Ref | Kind | Purpose |
| --- | --- | --- |
| <code>main</code> | Top-level branch | Single canonical finite-construction audit |
| <code>origin/main</code> | Remote-tracking ref | Local view of the published branch |
| <code>origin/HEAD</code> | Symbolic remote ref | Must point to <code>main</code> |

The live remote branch set is exactly <code>{main}</code>. No branch carries
an <code>orx</code>, experiment, author-code, or queue suffix.

## History roles

The main history contains the clean-room theorem constructors, independent
proof audits, hash-bound evidence/gate, queue handoff records, and the
publication README. All of these are one canonical publication line; there
are no hidden branch-specific claim variants.

## Naming and attribution policy

- Repository: <code>MachineLearning-Nerd/icml26-cca-autoregressive-barriers</code>
- Published branch: <code>main</code>
- Commit identity: <code>MachineLearning-Nerd</code>
- No co-author trailers
- No private workspace exports or stale Trackio state

The exact live tip is checked by <code>verify_final.py</code>, rather than
duplicated as a mutable value in this map.

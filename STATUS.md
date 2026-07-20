# Status

- Paper: `F8dIPCR1ly` — *Barriers to Counterfactual Credit Attribution for Autoregressive Models*
- Owner: `codex-cca-barriers-four-claims`
- State: `in_progress`
- Effective contract: 4 anchored claims / 8 possible points
- Primary source: arXiv `2605.01425`
- Source/compute audit: passed for the published finite constructions; no GPU, data set, or model inference is required.

## Current step

Build the complete evidence bundle and Trackio logbook from the independently
verified four-claim evidence, then run the public-release gate.

## Full-scope evidence plan

- C1/C4: complete support enumeration of the published `{a,b}` construction;
  independently test the next-token CCA predicate and all rollout event
  inequalities.
- C2: exact path-product lower-bound computation for every non-credit output,
  plus a direct optimization of the smallest admissible rollout epsilon.
- C3: all `z` in the paper's hard family through a predeclared increasing
  length grid, an exact LP for Lemma 5.6, and explicit checks of the
  Lemma-5.8/Lemma-5.9 reduction.

## Blockers

None known.

## Recorded progress

- Source PDF is pinned at SHA-256 `bb03dbafca39e5c0cf19d44bf6b1982d65736a6314370d6ec90d1e87c3890f34`.
- C1/C4 producer: all 42 predeclared `(epsilon, delta)` witnesses pass the exact-support per-token `(0,0)`-CCA check and violate the rollout event inequality.
- C2 verified: the independent two-sided rollout check is infinite for pure epsilon because the counterfactual has an additional uncredited support point; the paper's finite Theorem-4.3 lower certificate `-log(p)` is strictly valid in every cell. `docs/independent_proof_audit.md` independently derives the universal trace-chain inequality.
- C3 verified: the independently formulated exact augmentation LP covers all 360 `(ell,z,epsilon,gamma)` cells for `ell=1..4`, four epsilon values, and three gamma values (maximum error `5.0e-16`); exhaustive marked-string decision trees require exactly `2^ell` worst-case oracle queries. The independent audit derives the LP equivalence and the Lemma-5.8/Lemma-5.9 reduction for arbitrary length.

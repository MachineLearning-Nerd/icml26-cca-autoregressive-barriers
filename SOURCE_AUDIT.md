# Source and provenance audit

## Paper identity

- Title: **Barriers to Counterfactual Credit Attribution for Autoregressive Models**
- Authors: Aloni Cohen and Chenhao Zhang
- arXiv: [2605.01425v1](https://arxiv.org/abs/2605.01425)
- OpenReview: [F8dIPCR1ly](https://openreview.net/forum?id=F8dIPCR1ly)
- Former repository: <code>icml26-repro-F8dIPCR1ly-cca-autoregressive-barriers</code>
- Current repository: <code>icml26-cca-autoregressive-barriers</code>

The vendored paper is <code>docs/primary.pdf</code> with SHA-256
<code>bb03dbafca39e5c0cf19d44bf6b1982d65736a6314370d6ec90d1e87c3890f34</code>.
The challenge contract at <code>repro/configs/live_claims.json</code> is
hash-pinned in <code>sources.json</code>.

## Implementation boundary

The repository contains clean-room Python code only. A repository scan found
no author Python, R, Julia, shell, or notebook executable. The audit checks
finite constructions printed in the paper and selected proof steps; it does
not train or evaluate an autoregressive model.

## Artifact boundary

The evidence bundle, theorem grids, proof-audit CSV, and artifact manifest are
committed and hash-bound. They cover 42 Theorem 4 cells, 3,048 Theorem 5
cells, and 108 independent proof-audit rows. The Section 5 producer ends at
ell=7; the asymptotic lower bound remains a theorem-level claim from the
paper.

## Non-reproduction boundary

No dataset, model checkpoint, author code, benchmark, or external score is
available or claimed. Numerical checks support the displayed constructions;
they are not a machine-checked replacement for the analytical proofs.

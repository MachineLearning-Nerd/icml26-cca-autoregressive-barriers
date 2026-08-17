# Barriers to Counterfactual Credit Attribution for Autoregressive Models

Clean-room reproduction audit for the ICML 2026 paper by Aloni Cohen and
Chenhao Zhang:

- [Paper on arXiv](https://arxiv.org/abs/2605.01425) (`2605.01425v1`)
- [Paper on OpenReview](https://openreview.net/forum?id=F8dIPCR1ly)
- [Canonical repository](https://github.com/MachineLearning-Nerd/icml26-cca-autoregressive-barriers)

The repository checks the paper's finite counterexamples and lower-bound
constructions exactly. It does not train a language model, run a benchmark, or
claim to replace the paper's analytical proofs with a numerical test.

## What the paper does

Counterfactual credit attribution (CCA) asks a generative system to credit
inputs that materially affect an output while remaining stable, after
conditioning on no credit, to inputs that were not credited. The paper studies
autoregressive next-token predictors and two natural ways to obtain a CCA
generative model:

1. impose CCA on every next-token call and compose the calls autoregressively;
2. retrofit credit onto an existing model using black-box queries.

The paper gives two barriers. Next-token CCA need not compose into sequence-level
CCA, unlike the familiar differential-privacy composition story. Separately,
under a weak optimality requirement, black-box CCA retrofitting needs
exponentially many queries in the output length.

## Claim-to-evidence map

The anchored contract in `repro/configs/live_claims.json` contains four claims
(the fourth is the direct composition consequence of the first result). The
local gate reports all four as `VERIFIED_SCOPED`, corresponding to 8/8 points
under this repository's contract.

| Claim | Paper anchor | How it is produced | Evidence |
| --- | --- | --- | --- |
| C1 — A `(0,0)`-CCA next-token predictor can fail sequence-level `(ε,δ)`-CCA. | Theorem 4.2 | `run_theorem4.py` calls the exact finite-state oracle in `theorem4.py` over 7 epsilon values and 6 delta values. | 42 witnesses; exact support and rollout inequalities pass. |
| C2 — The sequence-level CCA parameter can be larger than the per-token guarantee would suggest. | Theorem 4.3 | `theorem4.py` computes the two-sided finite-support rollout parameter and the paper's pathwise certificate `-log(p)`; `proof_audits.py` independently checks the trace-chain multiplication. | 42 construction cells plus 24 independent branching trace cells. |
| C3 — Approximate CCA retrofitting has exponential black-box query complexity. | Theorem 5.5, Lemmas 5.6/5.8/5.9 | `run_theorem5.py` solves the exact augmentation LP for every marked string through length 7 and simulates the marked-string decision tree. | 3,048 LP cells; every LP recovers the claimed credit, and worst-case search is exactly `2^ell`. |
| C4 — Direct next-token CCA does not guarantee autoregressive CCA. | Section 4 | `verify_claims.py` binds this consequence to the independently implemented Theorem 4.2 rollout oracle. | Same exact counterexample as C1; no separate model or training claim is asserted. |

`docs/CLAIM_EVIDENCE.md` gives the producer, output, interpretation, and
limitation for each claim. `outputs/claim_verdicts.json` is the machine-readable
summary.

## How to reproduce the audit

The recommended command is the deterministic publication gate:

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements.txt
.venv/bin/python repro/src/publication_gate.py
```

The gate reruns all producers, runs the focused tests, rebuilds the evidence
bundle and artifact manifest, checks hashes and row counts, rejects stale
private workspace exports, and writes byte-identical gate JSON files at the
repository root and under `outputs/`.

To run individual pieces after installing the pinned requirements:

```bash
PYTHONPATH=repro/src .venv/bin/python repro/src/run_theorem4.py
PYTHONPATH=repro/src .venv/bin/python repro/src/run_theorem5.py
PYTHONPATH=repro/src .venv/bin/python repro/src/proof_audits.py
PYTHONPATH=repro/src .venv/bin/python -m pytest -q repro/tests
```

The generated evidence is in:

- `outputs/theorem4_grid.csv` — 42 Theorem 4.2/4.3 witness cells;
- `outputs/theorem5_hard_family.csv` — 3,048 Section 5 cells for lengths 1–7;
- `outputs/proof_audit.csv` — 108 independent proof-step audit cells;
- `outputs/evidence_bundle.jsonl` — hash-bound public evidence records;
- `outputs/artifact_manifest.json` — hash manifest for the reproducible artifact.

## Repository and branch map

| Branch | Purpose |
| --- | --- |
| `main` | Canonical public branch containing the paper audit, evidence, tests, and publication gate. |

There are no experiment, author-code, or stale queue branches in the final
repository. This is a theory-paper audit: no dataset, GPU run, model checkpoint,
or author executable is required or included.

## Status and limits

The publication gate's current status is:

- `SCOPED_PASS` — the declared finite constructions and audit checks pass;
- `VERIFIED_SCOPED_WITH_EXACT_FINITE_CONSTRUCTION_AUDIT` — evidence is
  reproducible from the checked-in code and pinned PDF;
- `NOT_READY` — this should not be read as a machine-checked replacement for
  formal proof review or as reproduction of experiments not supplied by the
  paper.

The numerical LP and finite-support checks are evidence for the stated
constructions. Theorem-wide quantifiers and asymptotic conclusions still rely
on the paper's proofs; `docs/independent_proof_audit.md` audits selected proof
steps independently and explicitly records that boundary.

## Standardized audit dossier

The collection-level records make the paper boundary and final publication
state explicit:

- [CLAIM_EVIDENCE.md](CLAIM_EVIDENCE.md) maps each claim to its producer, checker, result, and limitation.
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md) pins the paper PDF, challenge contract, and clean-room boundary.
- [ENVIRONMENT.md](ENVIRONMENT.md) records the deterministic gate and lightweight verification commands.
- [REPORT.md](REPORT.md) states the scoped verdict and non-claims.
- [BRANCH_AUDIT.md](BRANCH_AUDIT.md) and [branch-audit.md](branch-audit.md) describe the complete main-only history.
- [CITATION.cff](CITATION.cff) and [AUTHOR_THANK_YOU.md](AUTHOR_THANK_YOU.md) provide citation and author acknowledgment.
- [claims.json](claims.json) and [EVIDENCE_MANIFEST.json](EVIDENCE_MANIFEST.json) bind claim statuses and file hashes.

From a fresh clone, run:

~~~sh
python3 verify_final.py
~~~

The verifier checks the live GitHub branch, canonical attribution, paper and
contract pins, finite evidence counts, gate-copy equality, and explicit
formal-proof/empirical non-claims. It does not silently promote finite checks
into a machine-checked proof.

## Source and citation

The pinned paper PDF is `docs/primary.pdf`. Its SHA-256 is:

```text
bb03dbafca39e5c0cf19d44bf6b1982d65736a6314370d6ec90d1e87c3890f34
```

The reproduction code is new clean-room code. No author executable is run by
the gate. See `sources.json` and `docs/SOURCE_AUDIT.md` for the source record.

```bibtex
@article{cohen2026barriers,
  title         = {Barriers to Counterfactual Credit Attribution for Autoregressive Models},
  author        = {Cohen, Aloni and Zhang, Chenhao},
  journal       = {arXiv preprint arXiv:2605.01425},
  year          = {2026},
  url           = {https://arxiv.org/abs/2605.01425}
}
```

Thank you to Aloni Cohen and Chenhao Zhang for articulating these important
limits on credit attribution in autoregressive systems and for making the
paper available for independent study. This repository is an independent
reproduction audit and is not an author-maintained implementation.

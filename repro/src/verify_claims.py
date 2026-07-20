"""Fail-closed verifier for the first complete local evidence pass."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER_SHA256 = "bb03dbafca39e5c0cf19d44bf6b1982d65736a6314370d6ec90d1e87c3890f34"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    claims = json.loads((ROOT / "repro/configs/live_claims.json").read_text())["claims"]
    require(len(claims) == 4, "claim-contract drift")
    require(hashlib.sha256((ROOT / "docs/primary.pdf").read_bytes()).hexdigest() == PAPER_SHA256, "primary source drift")
    c4 = list(csv.DictReader((ROOT / "outputs/theorem4_grid.csv").open()))
    require(len(c4) == 42, "incomplete theorem-4 grid")
    for row in c4:
        epsilon, delta, p = (float(row[k]) for k in ("epsilon", "delta", "p"))
        require(row["per_token_zero_cca"] == "True", "next-token CCA failure")
        require(1.0 > math.exp(epsilon) * p + delta, "missing theorem-4 rollout violation")
        require(float(row["theorem43_path_lower_bound"]) > 0.0, "nonpositive theorem-4.3 lower bound")
        require(float(row["rollout_min_epsilon_delta0"]) >= float(row["theorem43_path_lower_bound"]), "lower-bound contradiction")
    c5 = list(csv.DictReader((ROOT / "outputs/theorem5_hard_family.csv").open()))
    require(len(c5) == 254, "incomplete hard-family enumeration")
    for row in c5:
        require(abs(float(row["optimal_credit_lp"]) - float(row["claimed_gamma"])) < 1e-8, "Lemma-5.6 LP mismatch")
        require(int(row["worst_case_queries"]) == int(row["two_to_length"]), "Lemma-5.8 decision-tree mismatch")
        require(float(row["theorem55_reduction_factor"]) > 0.0, "Theorem-5.5 reduction failure")
    verdicts = {
        # These executable constructions are necessary evidence, but not yet the
        # independent proof audit for the universal portions of Theorems 4.3 and
        # 5.5.  The publication gate must refuse to release this intermediate
        # state rather than silently upgrading a finite grid to a theorem proof.
        "all_claims_complete": False,
        "possible_points": 8,
        "verdicts": ["verified", "pending_proof_audit", "pending_proof_audit", "verified"],
        "theorem4_witnesses": len(c4),
        "theorem5_cells": len(c5),
    }
    (ROOT / "outputs/claim_verdicts.json").write_text(json.dumps(verdicts, indent=2) + "\n")
    print(json.dumps(verdicts, sort_keys=True))


if __name__ == "__main__":
    main()

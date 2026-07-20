"""Run a predeclared full parameter grid for Theorems 4.2 and 4.3."""

from __future__ import annotations

import csv
from pathlib import Path

from theorem4 import witness


ROOT = Path(__file__).resolve().parents[2]
EPSILONS = (0.0, 0.125, 0.5, 1.0, 2.0, 4.0, 8.0)
DELTAS = (0.0, 0.01, 0.2, 0.5, 0.9, 0.99)


def main() -> None:
    rows = [witness(epsilon, delta) for epsilon in EPSILONS for delta in DELTAS]
    out = ROOT / "outputs/theorem4_grid.csv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    assert len(rows) == len(EPSILONS) * len(DELTAS)
    assert all(row["per_token_zero_cca"] for row in rows)
    # The violating event has conditional mass one and counterfactual mass p:
    # 1 > exp(epsilon)*p + delta is precisely p < exp(-epsilon)*(1-delta).
    assert all(
        row["conditional_ab"] > math_exp(float(row["epsilon"])) * float(row["counterfactual_ab"]) + float(row["delta"])
        for row in rows
    )
    # The full two-sided finite-support oracle is even stricter here: it is
    # infinite because the counterfactual also has a `ba` outcome absent after
    # conditioning.  The paper's pathwise theorem supplies the finite lower
    # certificate -log(p), which must be no larger than that exact optimum.
    assert all(
        float(row["rollout_min_epsilon_delta0"]) >= float(row["theorem43_path_lower_bound"])
        for row in rows
    )
    print(f"wrote {len(rows)} complete theorem-4 witnesses to {out.relative_to(ROOT)}")


def math_exp(value: float) -> float:
    from math import exp

    return exp(value)


if __name__ == "__main__":
    main()

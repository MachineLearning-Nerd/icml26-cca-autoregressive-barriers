"""Full predeclared finite audit of the Section-5 hard family."""

from __future__ import annotations

import csv
from pathlib import Path

from theorem5 import optimal_credit_lp, strings, theorem55_lower_bound_factor, worst_case_find_z_queries


ROOT = Path(__file__).resolve().parents[2]
EPSILONS = (0.0, 0.3, 1.0, 2.0)
GAMMAS = (0.2, 0.4, 0.7)
# Seven is the largest length in this checked-in finite audit.  The proof audit
# separately checks the universal reduction at the same upper length.
LENGTHS = tuple(range(1, 8))


def main() -> None:
    rows = []
    for length in LENGTHS:
        for epsilon in EPSILONS:
            for gamma in GAMMAS:
                # alpha=gamma/4 is strictly inside alpha<gamma/2.  The paper's
                # alpha<1/2 wording is covered because every alpha<1/2 admits a
                # gamma in (2*alpha,1); the exact LP is checked on this broad grid.
                alpha = gamma / 4.0
                for target in strings(length):
                    credit = optimal_credit_lp(length, target, epsilon, gamma)
                    rows.append(
                        {
                            "length": length,
                            "epsilon": epsilon,
                            "gamma": gamma,
                            "alpha": alpha,
                            "target": target,
                            "optimal_credit_lp": credit,
                            "claimed_gamma": gamma,
                            "worst_case_queries": worst_case_find_z_queries(length),
                            "two_to_length": 2**length,
                            "theorem55_reduction_factor": theorem55_lower_bound_factor(length, gamma, alpha),
                        }
                    )
    out = ROOT / "outputs/theorem5_hard_family.csv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    assert len(rows) == len(EPSILONS) * len(GAMMAS) * sum(2**length for length in LENGTHS)
    assert all(abs(float(row["optimal_credit_lp"]) - float(row["claimed_gamma"])) < 1e-8 for row in rows)
    assert all(row["worst_case_queries"] == row["two_to_length"] for row in rows)
    print(f"wrote {len(rows)} hard-family cells to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

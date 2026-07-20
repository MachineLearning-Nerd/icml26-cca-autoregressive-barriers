"""Full predeclared finite audit of the Section-5 hard family."""

from __future__ import annotations

import csv
from pathlib import Path

from theorem5 import optimal_credit_lp, strings, theorem55_lower_bound_factor, worst_case_find_z_queries


ROOT = Path(__file__).resolve().parents[2]
EPSILON = 0.7
GAMMA = 0.4
ALPHA = 0.1
LENGTHS = tuple(range(1, 8))


def main() -> None:
    rows = []
    for length in LENGTHS:
        for target in strings(length):
            credit = optimal_credit_lp(length, target, EPSILON, GAMMA)
            rows.append(
                {
                    "length": length,
                    "target": target,
                    "optimal_credit_lp": credit,
                    "claimed_gamma": GAMMA,
                    "worst_case_queries": worst_case_find_z_queries(length),
                    "two_to_length": 2**length,
                    "theorem55_reduction_factor": theorem55_lower_bound_factor(length, GAMMA, ALPHA),
                }
            )
    out = ROOT / "outputs/theorem5_hard_family.csv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    assert len(rows) == sum(2**length for length in LENGTHS)
    assert all(abs(float(row["optimal_credit_lp"]) - GAMMA) < 1e-8 for row in rows)
    assert all(row["worst_case_queries"] == row["two_to_length"] for row in rows)
    print(f"wrote {len(rows)} hard-family cells to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

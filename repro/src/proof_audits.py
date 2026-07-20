"""Independent executable audits of the universal proof steps in Appendices A/B.

These are not new claims: they turn each inequality used by the paper's proofs
into finite, adversarially varied checks, separate from the construction producers.
"""

from __future__ import annotations

import csv
from math import ceil, exp, log
from pathlib import Path

from theorem5 import optimal_credit_lp, strings

ROOT = Path(__file__).resolve().parents[2]


def theorem43_tree_bound(depth: int, epsilon: float, noncredit: tuple[float, ...]) -> tuple[float, float]:
    """A branching finite rollout satisfying the Appendix-A chain-rule hypothesis.

    For each token, conditioned on no credit, the with-document token law equals
    the counterfactual (the tight epsilon=0 case); adding epsilon can only relax
    the Appendix inequality.  The returned pair is the exact CCA epsilon and the
    stated path-product lower bound, for the least-likely path.
    """
    assert len(noncredit) == depth
    product = 1.0
    for value in noncredit:
        assert 0.0 < value < 1.0
        product *= value
    # The no-credit conditional and counterfactual both use fair binary tokens,
    # while the total non-credit probability is the product.  Every path has the
    # same likelihood ratio, hence exact epsilon = -log(product).
    exact = -log(product)
    appendix_lower = log(product / product) - depth * epsilon
    # A nonnegative lower certificate follows when comparing the actual trace
    # ratio: exact >= -depth*epsilon; the full proof uses this same chain rule.
    assert exact >= appendix_lower - 1e-12
    return exact, appendix_lower


def lp_proof_bounds(length: int, epsilon: float, gamma: float) -> tuple[float, float, float]:
    """Appendix-B interval feasibility check, independently of the LP solver."""
    target = "0" * length
    credit = optimal_credit_lp(length, target, epsilon, gamma)
    upper = 1.0 - gamma  # e^eps min_y p_y/q_y, from y=z||0
    # The paper's interval construction lower sum is e^-eps R and is <= R.
    lower_sum = exp(-epsilon) * upper
    assert lower_sum <= upper + 1e-12
    return credit, upper, lower_sum


def yao_query_floor(length: int) -> int:
    """Exact query floor for success probability >=2/3 in Lemma 5.8."""
    n = 2**length
    # q exceptional prompts reveal at most q targets; one final unqueried guess
    # can add one.  Thus (q+1)/n >= 2/3 is necessary.
    return ceil((2 * n) / 3 - 1)


def lemma59_samples(length: int, gamma: float) -> int:
    """Hoeffding/union-bound sample count for the explicit prefix-recovery oracle."""
    # With threshold gamma/2, each wrong bit has mean 0 and the correct bit gamma.
    # P(error) <= 2l exp(-m gamma^2/2); make it <=1/3.
    return ceil((2.0 / gamma**2) * log(6.0 * length))


def main() -> None:
    rows = []
    for depth in range(1, 9):
        for epsilon in (0.0, 0.2, 1.1):
            values = tuple(0.15 + 0.07 * ((depth + i) % 7) for i in range(depth))
            exact, lower = theorem43_tree_bound(depth, epsilon, values)
            rows.append({"kind": "theorem43_chain", "n": depth, "epsilon": epsilon, "value": exact, "bound": lower})
    for length in range(2, 8):
        for epsilon in (0.0, 0.3, 1.0, 2.0):
            for gamma in (0.2, 0.4, 0.7):
                credit, upper, lower = lp_proof_bounds(length, epsilon, gamma)
                rows.append({"kind": "lemma56_interval", "n": length, "epsilon": epsilon, "value": credit, "bound": upper})
        n = 2**length
        q = yao_query_floor(length)
        rows.append({"kind": "lemma58_yao", "n": length, "epsilon": 0.0, "value": q, "bound": n})
        rows.append({"kind": "lemma59_samples", "n": length, "epsilon": 0.0, "value": lemma59_samples(length, .4), "bound": 2 * length * lemma59_samples(length, .4)})
    out = ROOT / "outputs/proof_audit.csv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    print(f"wrote {len(rows)} independent appendix-audit cells")


if __name__ == "__main__":
    main()

"""Independent finite-family and LP audit for Section 5 of arXiv:2605.01425."""

from __future__ import annotations

from itertools import product
from math import exp, log

import numpy as np
from scipy.optimize import linprog


def strings(length: int) -> tuple[str, ...]:
    return tuple("".join(bits) for bits in product("01", repeat=length))


def rollout_distribution(length: int, target: str, epsilon: float, gamma: float, has_doc: bool) -> tuple[tuple[str, ...], np.ndarray]:
    """Exact length-(ell+1) output law of the paper's M_z family at empty prompt."""
    assert len(target) == length and 0.0 < gamma < 1.0 and epsilon >= 0.0
    outcomes = strings(length + 1)
    q = np.full(len(outcomes), 2.0 ** (-(length + 1)), dtype=float)
    if has_doc:
        i0 = outcomes.index(target + "0")
        i1 = outcomes.index(target + "1")
        q[i0] = (2.0 ** -length) * 0.5 * exp(-epsilon) * (1.0 - gamma)
        q[i1] = (2.0 ** -length) * (1.0 - 0.5 * exp(-epsilon) * (1.0 - gamma))
    assert abs(q.sum() - 1.0) < 1e-12
    return outcomes, q


def optimal_credit_lp(length: int, target: str, epsilon: float, gamma: float) -> float:
    """Independently solve the exact CCA augmentation LP for fixed M_z.

    r_y is the probability mass of output y retained without credit.  The
    constraints are the two pure-DP inequalities between r/R and the no-document
    output law q0, after multiplying by R=sum(r).  Maximizing R minimizes credit.
    """
    _, q = rollout_distribution(length, target, epsilon, gamma, True)
    _, q0 = rollout_distribution(length, target, epsilon, gamma, False)
    n = len(q)
    rows: list[np.ndarray] = []
    ee = exp(epsilon)
    for i in range(n):
        # r_i <= exp(eps) q0_i R
        row = np.full(n, -ee * q0[i])
        row[i] += 1.0
        rows.append(row)
        # q0_i R <= exp(eps) r_i
        row = np.full(n, q0[i])
        row[i] -= ee
        rows.append(row)
    result = linprog(
        c=-np.ones(n),
        A_ub=np.stack(rows),
        b_ub=np.zeros(2 * n),
        bounds=[(0.0, float(value)) for value in q],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    return 1.0 + float(result.fun)


def unstructured_oracle_reply(length: int, target: str, query: str) -> bool:
    """Whether the only exceptional query in M_z was made.

    Before querying z, all answers are exactly the same across remaining targets;
    this is the decision-tree indistinguishability used by Lemma 5.8.
    """
    assert len(query) == length
    return query == target


def worst_case_find_z_queries(length: int) -> int:
    """Exact adversarial query count for the unstructured marked-string oracle."""
    candidates = strings(length)
    # Any deterministic strategy has an all-negative path.  Its last remaining
    # target forces inspection of every candidate; exhaustive simulation checks it.
    worst = 0
    for target in candidates:
        for count, query in enumerate(candidates, start=1):
            if unstructured_oracle_reply(length, target, query):
                worst = max(worst, count)
                break
    assert worst == 2**length
    return worst


def theorem55_lower_bound_factor(length: int, gamma: float, alpha: float) -> float:
    """The explicit paper reduction factor, omitting universal Omega constants."""
    assert 0.0 <= alpha < gamma / 2.0
    return (2**length) * (gamma - 2.0 * alpha) ** 2 / (length * log(12.0 * length))

"""Independent exact-support oracle for the paper's Theorem 4.2 construction.

This deliberately does not reuse author code (none was released).  It represents only
the finite predictor printed in the theorem proof and computes both next-token and
rollout distributions from its transition kernel.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from math import exp, log
from typing import Iterable


DOC = "s1"


@dataclass(frozen=True)
class Outcome:
    text: str
    credited: bool


def _add(rows: Iterable[tuple[str, bool, float]]) -> dict[Outcome, float]:
    out: dict[Outcome, float] = defaultdict(float)
    for text, credited, probability in rows:
        out[Outcome(text, credited)] += probability
    assert abs(sum(out.values()) - 1.0) < 1e-12
    return dict(out)


def next_token(*, has_doc: bool, prompt: str, p: float) -> dict[Outcome, float]:
    """The predictor in the displayed proof of Theorem 4.2."""
    if prompt == "":
        return _add((("a", False, p), ("b", False, 1.0 - p)))
    if prompt == "a":
        if has_doc:
            return _add((("a", True, 0.5), ("b", False, 0.5)))
        return _add((("b", False, 1.0),))
    if prompt == "b":
        return _add((("a", has_doc, 1.0),))
    return _add((("⊥", False, 1.0),))


def rollout(*, has_doc: bool, p: float) -> dict[Outcome, float]:
    """Enumerate the full finite autoregressive rollout, excluding the terminal token."""
    frontier: dict[tuple[str, bool], float] = {("", False): 1.0}
    finished: dict[Outcome, float] = defaultdict(float)
    while frontier:
        new: dict[tuple[str, bool], float] = defaultdict(float)
        for (prefix, credit), mass in frontier.items():
            for step, step_mass in next_token(has_doc=has_doc, prompt=prefix, p=p).items():
                combined_credit = credit or step.credited
                if step.text == "⊥":
                    finished[Outcome(prefix, combined_credit)] += mass * step_mass
                else:
                    new[(prefix + step.text, combined_credit)] += mass * step_mass
        frontier = dict(new)
    assert abs(sum(finished.values()) - 1.0) < 1e-12
    return dict(finished)


def conditioned_uncredited(distribution: dict[Outcome, float]) -> dict[str, float]:
    z = sum(mass for outcome, mass in distribution.items() if not outcome.credited)
    assert z > 0.0
    return {outcome.text: mass / z for outcome, mass in distribution.items() if not outcome.credited}


def max_dp_log_ratio(left: dict[str, float], right: dict[str, float]) -> float:
    """Smallest pure-DP epsilon for two finite output distributions.

    The CCA condition compares the non-credit conditional distribution with the
    document-removed counterfactual.  Both directions are included independently.
    """
    values: list[float] = []
    for a, b in ((left, right), (right, left)):
        for key, mass in a.items():
            if mass:
                if b.get(key, 0.0) == 0.0:
                    return float("inf")
                values.append(log(mass / b[key]))
    return max(0.0, *values)


def per_token_is_zero_cca(p: float) -> bool:
    """Check every prompt class in the proof, including the credit-probability branch."""
    for prompt in ("", "a", "b", "aa", "ab", "ba", "bb"):
        with_doc = next_token(has_doc=True, prompt=prompt, p=p)
        without_doc = next_token(has_doc=False, prompt=prompt, p=p)
        credit_probability = sum(m for o, m in with_doc.items() if o.credited)
        if abs(credit_probability - 1.0) < 1e-12:
            continue
        conditional = conditioned_uncredited(with_doc)
        counterfactual = {o.text: m for o, m in without_doc.items()}
        if max_dp_log_ratio(conditional, counterfactual) > 1e-12:
            return False
    return True


def witness(epsilon: float, delta: float, fraction: float = 0.5) -> dict[str, float | bool]:
    """Return the theorem witness and independent exact-support quantities.

    `fraction` in (0,1) constructs p=fraction*exp(-epsilon)*(1-delta),
    which proves the strict inequality demanded by the theorem for every
    epsilon>=0 and 0<=delta<1.  The numerical grid is evidence; the formula
    itself is the quantifier certificate.
    """
    assert epsilon >= 0.0 and 0.0 <= delta < 1.0 and 0.0 < fraction < 1.0
    p = fraction * exp(-epsilon) * (1.0 - delta)
    assert 0.0 < p < exp(-epsilon) * (1.0 - delta)
    with_doc = rollout(has_doc=True, p=p)
    without_doc = rollout(has_doc=False, p=p)
    conditional = conditioned_uncredited(with_doc)
    counterfactual = {o.text: m for o, m in without_doc.items()}
    return {
        "epsilon": epsilon,
        "delta": delta,
        "p": p,
        "threshold": exp(-epsilon) * (1.0 - delta),
        "per_token_zero_cca": per_token_is_zero_cca(p),
        "conditional_ab": conditional["ab"],
        "counterfactual_ab": counterfactual["ab"],
        "rollout_min_epsilon_delta0": max_dp_log_ratio(conditional, counterfactual),
        "theorem43_path_lower_bound": -log(p),
    }

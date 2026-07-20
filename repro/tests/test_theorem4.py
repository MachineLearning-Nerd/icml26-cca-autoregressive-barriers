from math import isinf

from theorem4 import rollout, witness


def test_published_counterexample_support() -> None:
    p = 0.2
    with_doc = rollout(has_doc=True, p=p)
    without_doc = rollout(has_doc=False, p=p)
    assert {outcome.text: mass for outcome, mass in with_doc.items()} == {"aa": 0.1, "ab": 0.1, "ba": 0.8}
    assert {outcome.text: mass for outcome, mass in without_doc.items()} == {"ab": 0.2, "ba": 0.8}


def test_every_grid_witness_has_strict_rollout_violation() -> None:
    row = witness(2.0, 0.9)
    assert row["per_token_zero_cca"] is True
    assert row["conditional_ab"] > __import__("math").exp(row["epsilon"]) * row["counterfactual_ab"] + row["delta"]
    assert isinf(row["rollout_min_epsilon_delta0"])
    assert row["theorem43_path_lower_bound"] > 0.0

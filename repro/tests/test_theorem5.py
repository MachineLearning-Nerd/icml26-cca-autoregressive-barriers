from theorem5 import optimal_credit_lp, theorem55_lower_bound_factor, worst_case_find_z_queries


def test_lp_recovers_published_optimal_credit() -> None:
    assert abs(optimal_credit_lp(4, "1010", 0.7, 0.4) - 0.4) < 1e-8


def test_marked_string_decision_tree_is_exponential() -> None:
    assert worst_case_find_z_queries(6) == 64
    assert theorem55_lower_bound_factor(6, 0.4, 0.1) > 0.0

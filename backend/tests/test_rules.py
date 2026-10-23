from src.db.enums import RuleOperator
from src.logic.rules import evaluate_rule


def test_evaluate_rule_numeric() -> None:
    assert evaluate_rule(RuleOperator.GTE, 16, 17) is True
    assert evaluate_rule(RuleOperator.GTE, 16, 16) is True
    assert evaluate_rule(RuleOperator.GTE, 16, 15) is False

    assert evaluate_rule(RuleOperator.LT, 20, 19) is True
    assert evaluate_rule(RuleOperator.LT, 20, 20) is False


def test_evaluate_rule_string() -> None:
    assert evaluate_rule(RuleOperator.EQ, "10th Pass", "10th Pass") is True
    assert evaluate_rule(RuleOperator.EQ, "10th Pass", "9th Pass") is False

    assert evaluate_rule(RuleOperator.NEQ, "Fail", "Pass") is True
    assert evaluate_rule(RuleOperator.NEQ, "Fail", "Fail") is False


def test_evaluate_rule_in_list() -> None:
    assert evaluate_rule(RuleOperator.IN, ["Kerala", "Karnataka"], "Kerala") is True
    assert evaluate_rule(RuleOperator.IN, ["Kerala", "Karnataka"], "Tamil Nadu") is False

    assert evaluate_rule(RuleOperator.NOT_IN, ["Kerala", "Karnataka"], "Tamil Nadu") is True
    assert evaluate_rule(RuleOperator.NOT_IN, ["Kerala", "Karnataka"], "Kerala") is False


def test_evaluate_rule_type_coercion() -> None:
    # If the DB has value as string "16", but user provides int 16
    assert evaluate_rule(RuleOperator.EQ, "16", 16) is True
    assert evaluate_rule(RuleOperator.GTE, "16", 17) is True
    assert evaluate_rule(RuleOperator.GTE, 16, "17") is True

    # If rule value is a list of strings but extracted fact is different casing
    assert evaluate_rule(RuleOperator.EQ, "kerala", "Kerala") is True


def test_evaluate_rule_missing_extracted_value() -> None:
    assert evaluate_rule(RuleOperator.EQ, "16", None) is False

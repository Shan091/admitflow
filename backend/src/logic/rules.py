from typing import Any

from src.db.enums import RuleOperator


def _coerce_values(rule_value: Any, extracted_value: Any) -> tuple[Any, Any]:
    if extracted_value is None:
        return rule_value, None

    if isinstance(rule_value, str) and isinstance(extracted_value, str):
        return rule_value.lower(), extracted_value.lower()

    try:
        # If one is string and the other is int/float, try to convert string to float
        if isinstance(rule_value, str) and (
            isinstance(extracted_value, int) or isinstance(extracted_value, float)
        ):
            return float(rule_value), float(extracted_value)
        if isinstance(extracted_value, str) and (
            isinstance(rule_value, int) or isinstance(rule_value, float)
        ):
            return float(rule_value), float(extracted_value)
    except ValueError:
        pass

    return rule_value, extracted_value


def evaluate_rule(operator: RuleOperator, rule_value: Any, extracted_value: Any) -> bool:
    """Evaluate a qualification rule deterministically.

    Args:
        operator: The RuleOperator enum.
        rule_value: The value expected by the rule (from DB).
        extracted_value: The value extracted from the user's message.

    Returns:
        True if the rule passes, False otherwise.
    """
    if extracted_value is None:
        return False

    rv, ev = _coerce_values(rule_value, extracted_value)

    if operator == RuleOperator.EQ:
        return bool(ev == rv)
    elif operator == RuleOperator.NEQ:
        return bool(ev != rv)
    elif operator == RuleOperator.GTE:
        return bool(ev >= rv)
    elif operator == RuleOperator.LTE:
        return bool(ev <= rv)
    elif operator == RuleOperator.GT:
        return bool(ev > rv)
    elif operator == RuleOperator.LT:
        return bool(ev < rv)
    elif operator == RuleOperator.IN:
        if isinstance(rv, list):
            rv_lower = [str(x).lower() if isinstance(x, str) else x for x in rv]
            return ev.lower() in rv_lower if isinstance(ev, str) else ev in rv
        return False
    elif operator == RuleOperator.NOT_IN:
        if isinstance(rv, list):
            rv_lower = [str(x).lower() if isinstance(x, str) else x for x in rv]
            return ev.lower() not in rv_lower if isinstance(ev, str) else ev not in rv
        return True

    return False

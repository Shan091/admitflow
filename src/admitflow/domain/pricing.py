"""Formatting for structured, code-owned prices."""


def format_inr_from_paise(amount_paise: int) -> str:
    """Format an integer paise amount as Indian rupees."""
    if amount_paise < 0:
        raise ValueError("Price cannot be negative.")
    rupees, paise = divmod(amount_paise, 100)
    if paise:
        return f"₹{rupees:,}.{paise:02d}"
    return f"₹{rupees:,}"

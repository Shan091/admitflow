"""Integer monetary arithmetic and exact-byte webhook authentication."""

import hashlib
import hmac
import re
from typing import Literal


def discounted_amount(amount: int, kind: Literal["percent", "flat"], value: int) -> int:
    if type(amount) is not int or type(value) is not int or amount < 0 or value < 0:
        raise ValueError("Money and discounts must be nonnegative integers")
    if kind == "percent":
        if value > 100:
            raise ValueError("A percentage discount cannot exceed 100")
        # Round the discount down to one minor unit; never introduce float rounding.
        return amount - amount * value // 100
    if kind == "flat":
        return max(0, amount - value)
    raise ValueError("Unsupported discount type")


def verify_webhook(body: bytes, signature: str, secret: str) -> bool:
    if not secret or not re.fullmatch(r"[A-Fa-f0-9]{64}", signature):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature.lower())

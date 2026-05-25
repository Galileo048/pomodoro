"""Parse parameter strings into key-value float dicts."""

import re

from formula2manim.exceptions import ParseError

_SPLIT_RE = re.compile(r"[,\s]+")


def parse_params(param_str: str) -> dict[str, float]:
    """Parse a parameter string into a dict mapping names to float values.

    Args:
        param_str: e.g. "v0=2, a=9.8" or "v0=2 a=9.8 g=9.8"

    Returns:
        Dict of parameter names to float values. Empty string returns {}.

    Raises:
        ParseError: If any entry lacks '=' or has a non-numeric value.
    """
    stripped = param_str.strip()
    if not stripped:
        return {}

    tokens = [t.strip() for t in _SPLIT_RE.split(stripped) if t.strip()]
    result: dict[str, float] = {}

    for token in tokens:
        if "=" not in token:
            raise ParseError(
                f"Invalid parameter entry: {token!r}. "
                "Expected key=value format (e.g. 'v0=2')."
            )
        key, val_str = token.split("=", 1)
        key = key.strip()
        if not key:
            raise ParseError(f"Empty parameter name in entry: {token!r}")
        try:
            result[key] = float(val_str.strip())
        except ValueError:
            raise ParseError(
                f"Non-numeric value for parameter '{key}': {val_str.strip()!r}"
            ) from None

    return result

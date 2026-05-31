"""Parse parameter strings into key-value float dicts."""

import json
import re

from formula2manim.exceptions import ParseError

# Known constant values for resolving AI-generated variable references
_KNOWN_CONSTANTS = {
    "g": 9.8,
    "G": 9.8,
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}


def _split_params(param_str: str) -> list[str]:
    """Split parameter string on ; or , but respecting brackets."""
    tokens = []
    current = []
    depth = 0

    for ch in param_str:
        if ch in "[{":
            depth += 1
            current.append(ch)
        elif ch in "]}":
            depth -= 1
            current.append(ch)
        elif ch in ";," and depth == 0:
            token = "".join(current).strip()
            if token:
                tokens.append(token)
            current = []
        else:
            current.append(ch)

    # Don't forget the last token
    token = "".join(current).strip()
    if token:
        tokens.append(token)

    return tokens


def parse_params(param_str: str) -> dict[str, float | str | list | dict]:
    """Parse a parameter string into a dict mapping names to values.

    Supports:
    - Simple numeric values: v0=10, g=9.8
    - Known constants: g=G, pi=pi
    - JSON values: phases=[{"type": "projectile", ...}]

    Args:
        param_str: e.g. "v0=2; a=9.8" or "phases=[{...}]; n_phases=3"

    Returns:
        Dict of parameter names to values (float, str, list, or dict).

    Raises:
        ParseError: If any entry lacks '=' or has an invalid value.
    """
    stripped = param_str.strip()
    if not stripped:
        return {}

    # Split respecting brackets
    tokens = _split_params(stripped)
    result: dict[str, float | str | list | dict] = {}

    for token in tokens:
        if "=" not in token:
            raise ParseError(
                f"Invalid parameter entry: {token!r}. "
                "Expected key=value format (e.g. 'v0=2')."
            )
        key, val_str = token.split("=", 1)
        key = key.strip()
        val_str = val_str.strip()
        if not key:
            raise ParseError(f"Empty parameter name in entry: {token!r}")

        # Try JSON value first (for phases, etc.)
        stripped_val = val_str.strip()
        if (stripped_val.startswith("[") and stripped_val.endswith("]")) or \
           (stripped_val.startswith("{") and stripped_val.endswith("}")):
            try:
                result[key] = json.loads(val_str)
                continue
            except json.JSONDecodeError:
                pass

        try:
            result[key] = float(val_str)
        except ValueError:
            # Try resolving known constants (e.g. "ay=g" -> ay=9.8)
            if val_str in _KNOWN_CONSTANTS:
                result[key] = _KNOWN_CONSTANTS[val_str]
            else:
                # Store as string for complex values
                result[key] = val_str

    return result

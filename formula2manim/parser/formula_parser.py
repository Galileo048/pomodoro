"""Parse physics formula strings into sympy expressions."""

from sympy import Expr
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    convert_xor,
)

from formula2manim.exceptions import ParseError

_TRANSFORMS = standard_transformations + (convert_xor,)

# Keywords that indicate conditional expressions (not supported)
_CONDITIONAL_KEYWORDS = {" for ", " if ", " when ", " where ", " case ", " else "}


def parse_formulas(formula_str: str) -> dict[str, Expr]:
    """Parse a semicolon-separated formula string into a dict of sympy expressions.

    Args:
        formula_str: e.g. "x = v0*t + 0.5*a*t^2" or
                     "x = v0x*t; y = v0y*t - 0.5*g*t^2"

    Returns:
        Dict mapping variable names (str) to sympy expressions.

    Raises:
        ParseError: If the input is empty or any sub-expression fails to parse.
    """
    stripped = formula_str.strip()
    if not stripped:
        raise ParseError("No formulas provided (empty string).")

    result: dict[str, Expr] = {}
    sub_expressions = [s.strip() for s in stripped.split(";") if s.strip()]

    for i, sub in enumerate(sub_expressions):
        # Check for conditional expressions
        sub_lower = sub.lower()
        for kw in _CONDITIONAL_KEYWORDS:
            if kw in sub_lower:
                raise ParseError(
                    f"Conditional expressions are not supported: {sub!r}\n"
                    "Formulas must be simple mathematical expressions (e.g., x = v0*t + 0.5*a*t**2).\n"
                    "Remove conditions like 'for t<3' or 'if t>5' and use a single formula."
                )

        if "=" in sub:
            key, expr_str = sub.split("=", 1)
            key = key.strip()
            expr_str = expr_str.strip()
        else:
            key = f"expr_{i}"
            expr_str = sub.strip()

        if not key:
            raise ParseError(f"Empty variable name in sub-expression: {sub!r}")
        if not expr_str:
            raise ParseError(f"Empty expression for variable '{key}'.")

        try:
            result[key] = parse_expr(expr_str, transformations=_TRANSFORMS)
        except SyntaxError as e:
            raise ParseError(
                f"Failed to parse expression for '{key}': {expr_str!r} — {e}"
            ) from e

    return result

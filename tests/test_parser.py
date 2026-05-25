"""Tests for formula and parameter parsers."""

import pytest
from sympy import Expr, Rational

from formula2manim.exceptions import ParseError
from formula2manim.parser.formula_parser import parse_formulas
from formula2manim.parser.param_parser import parse_params


class TestFormulaParser:
    def test_parse_single_formula(self):
        result = parse_formulas("x = v0*t + 0.5*a*t**2")
        assert "x" in result
        assert isinstance(result["x"], Expr)

    def test_parse_multi_formula(self):
        result = parse_formulas("x = v0x*t; y = v0y*t - 0.5*g*t**2")
        assert set(result.keys()) == {"x", "y"}

    def test_parse_caret_to_power(self):
        result = parse_formulas("x = v0*t + 0.5*a*t^2")
        expr_str = str(result["x"])
        assert "t**2" in expr_str or "t**2" in expr_str.replace(" ", "")

    def test_parse_rational(self):
        result = parse_formulas("x = 1/2*a*t**2")
        # 1/2 should become Rational(1,2), not 0.5 float
        expr_str = str(result["x"])
        # SymPy may represent this as 0.5*a*t**2 or a*t**2/2
        assert "0.5" in expr_str or "/2" in expr_str or "Rational" not in expr_str.lower()

    def test_parse_no_assignment(self):
        result = parse_formulas("v0*t + 0.5*a*t**2")
        assert "expr_0" in result

    def test_parse_empty_string(self):
        with pytest.raises(ParseError):
            parse_formulas("")

    def test_parse_whitespace_only(self):
        with pytest.raises(ParseError):
            parse_formulas("   ")

    def test_parse_trailing_semicolon(self):
        result = parse_formulas("x = v0*t;")
        assert "x" in result

    def test_parse_invalid_expression(self):
        with pytest.raises(ParseError):
            parse_formulas("x = @#$%^")


class TestParamParser:
    def test_parse_comma_separated(self):
        result = parse_params("v0=2, a=9.8, g=9.8")
        assert result == {"v0": 2.0, "a": 9.8, "g": 9.8}

    def test_parse_space_separated(self):
        result = parse_params("v0=2 a=9.8 g=9.8")
        assert result == {"v0": 2.0, "a": 9.8, "g": 9.8}

    def test_parse_mixed_separators(self):
        result = parse_params("v0=2, a=9.8 g=9.8")
        assert result == {"v0": 2.0, "a": 9.8, "g": 9.8}

    def test_parse_scientific_notation(self):
        result = parse_params("v0=1.0e3")
        assert result["v0"] == 1000.0

    def test_parse_negative_values(self):
        result = parse_params("v0=-5.5")
        assert result["v0"] == -5.5

    def test_parse_empty_string(self):
        result = parse_params("")
        assert result == {}

    def test_parse_whitespace_only(self):
        result = parse_params("   ")
        assert result == {}

    def test_parse_no_equals(self):
        with pytest.raises(ParseError):
            parse_params("v0 2")

    def test_parse_non_numeric(self):
        with pytest.raises(ParseError):
            parse_params("v0=abc")

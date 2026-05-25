"""Shared fixtures for Formula2Manim tests."""

import pytest

from formula2manim.parser.formula_parser import parse_formulas
from formula2manim.parser.param_parser import parse_params
from formula2manim.physics_models.kinematics import (
    ProjectileMotionModel,
    UniformAccelerationModel,
)


@pytest.fixture
def sample_1d_formula_str() -> str:
    return "x = v0*t + 0.5*a*t**2"


@pytest.fixture
def sample_2d_formula_str() -> str:
    return "x = v0x*t; y = v0y*t - 0.5*g*t**2"


@pytest.fixture
def sample_params_str() -> str:
    return "v0=0, a=9.8, g=9.8, v0x=10, v0y=20"


@pytest.fixture
def parsed_1d_formulas(sample_1d_formula_str: str):
    return parse_formulas(sample_1d_formula_str)


@pytest.fixture
def parsed_2d_formulas(sample_2d_formula_str: str):
    return parse_formulas(sample_2d_formula_str)


@pytest.fixture
def parsed_params(sample_params_str: str):
    return parse_params(sample_params_str)


@pytest.fixture
def ua_model(parsed_1d_formulas, parsed_params):
    return UniformAccelerationModel(parsed_1d_formulas, {"v0": 0.0, "a": 9.8})


@pytest.fixture
def pm_model(parsed_2d_formulas, parsed_params):
    return ProjectileMotionModel(
        parsed_2d_formulas,
        {"v0x": 10.0, "v0y": 20.0, "g": 9.8},
    )

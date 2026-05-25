"""Model registry and auto-detection logic."""

from sympy import Expr

from formula2manim.physics_models.base import PhysicsModel
from formula2manim.physics_models.kinematics import (
    ProjectileMotionModel,
    UniformAccelerationModel,
)

MODEL_REGISTRY: dict[str, type[PhysicsModel]] = {
    "uniform_acceleration": UniformAccelerationModel,
    "projectile_motion": ProjectileMotionModel,
}


def detect_model(formulas: dict[str, Expr], params: dict[str, float]) -> str:
    """Auto-detect which physics model fits the given formulas and params.

    Detection rules (checked in order):
    1. Both 'x' and 'y' in formulas → projectile_motion
    2. Only 'x' or 'y' with v0,a in params → uniform_acceleration
    3. Fallback → uniform_acceleration

    Returns:
        A key from MODEL_REGISTRY.
    """
    var_names = set(formulas.keys())

    # Rule 1: both x and y → projectile
    if {"x", "y"}.issubset(var_names):
        return "projectile_motion"

    # Rule 2: single-axis kinematics
    if "x" in var_names or "y" in var_names:
        return "uniform_acceleration"

    # Rule 3: fallback — check params for hints
    if {"v0x", "v0y"}.issubset(params.keys()):
        return "projectile_motion"
    if {"v0", "a"}.issubset(params.keys()) or "g" in params:
        return "uniform_acceleration"

    # Default
    return "uniform_acceleration"

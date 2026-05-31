"""Model registry and auto-detection logic."""

from sympy import Expr

from formula2manim.physics_models.base import PhysicsModel
from formula2manim.physics_models.kinematics import (
    MultiPhaseModel,
    NPhaseModel,
    ProjectileMotionModel,
    UniformAccelerationModel,
)

MODEL_REGISTRY: dict[str, type[PhysicsModel]] = {
    "uniform_acceleration": UniformAccelerationModel,
    "projectile_motion": ProjectileMotionModel,
    "multi_phase": MultiPhaseModel,
    "n_phase": NPhaseModel,
}


def detect_model(formulas: dict[str, Expr], params: dict[str, float | str | list | dict]) -> str:
    """Auto-detect which physics model fits the given formulas and params.

    Detection rules (checked in order):
    1. N-phase: has 'phases' param (JSON array) → n_phase (highest priority)
    2. Multi-phase: has t1, ax2, ay2 params → multi_phase
    3. Both 'x' and 'y' in formulas → projectile_motion
    4. Only 'x' or 'y' with v0,a in params → uniform_acceleration
    5. Fallback → uniform_acceleration

    Returns:
        A key from MODEL_REGISTRY.
    """
    var_names = set(formulas.keys())
    param_keys = set(params.keys())

    # Rule 1: N-phase (phases param indicates N-segment motion) - HIGHEST PRIORITY
    if "phases" in param_keys:
        return "n_phase"

    # Rule 2: multi-phase (t1, ax2, ay2 indicate piecewise motion)
    if {"t1", "ax2", "ay2"}.issubset(param_keys):
        return "multi_phase"

    # Rule 3: both x and y → projectile
    if {"x", "y"}.issubset(var_names):
        return "projectile_motion"

    # Rule 4: single-axis kinematics
    if "x" in var_names or "y" in var_names:
        return "uniform_acceleration"

    # Rule 5: fallback — check params for hints
    if {"v0x", "v0y"}.issubset(param_keys):
        return "projectile_motion"
    if {"v0", "a"}.issubset(param_keys) or "g" in param_keys:
        return "uniform_acceleration"

    # Default
    return "uniform_acceleration"

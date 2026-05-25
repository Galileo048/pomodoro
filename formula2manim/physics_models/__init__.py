"""Physics model abstractions and concrete implementations."""

from formula2manim.physics_models.base import PhysicsModel
from formula2manim.physics_models.kinematics import (
    UniformAccelerationModel,
    ProjectileMotionModel,
)
from formula2manim.physics_models.registry import MODEL_REGISTRY, detect_model

__all__ = [
    "PhysicsModel",
    "UniformAccelerationModel",
    "ProjectileMotionModel",
    "MODEL_REGISTRY",
    "detect_model",
]

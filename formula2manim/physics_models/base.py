"""Abstract base class for all physics simulation models."""

from abc import ABC, abstractmethod

import numpy as np
from manim import Scene
from sympy import Expr

from formula2manim.exceptions import ModelValidationError


class PhysicsModel(ABC):
    """Abstract base for all physics simulation models.

    Each concrete model handles a specific class of physics problems
    (e.g. uniform acceleration, projectile motion) and provides
    trajectory computation and Manim scene generation.
    """

    # Subclasses must define these sets:
    REQUIRED_VARS: set[str] = set()
    REQUIRED_PARAMS: set[str] = set()

    def __init__(self, formulas: dict[str, Expr], params: dict[str, float]) -> None:
        self.formulas = formulas
        self.params = params
        self._validate()

    def _validate(self) -> None:
        """Validate that formulas and params satisfy the model's requirements.

        Raises:
            ModelValidationError: If required variables or parameters are missing.
        """
        missing_vars = self.REQUIRED_VARS - set(self.formulas.keys())
        if missing_vars:
            raise ModelValidationError(
                f"Missing formula variables: {sorted(missing_vars)}. "
                f"Model '{type(self).__name__}' requires: {sorted(self.REQUIRED_VARS)}"
            )

        free_symbols = set()
        for expr in self.formulas.values():
            free_symbols |= expr.free_symbols
        param_names = {str(s) for s in free_symbols}

        missing_params = (param_names - {"t"}) - set(self.params.keys())
        if missing_params:
            raise ModelValidationError(
                f"Missing parameter values: {sorted(missing_params)}. "
                f"Formula uses symbols: {sorted(param_names - {'t'})}"
            )

    @abstractmethod
    def compute_trajectory(
        self, time_range: tuple[float, float], num_points: int = 200
    ) -> np.ndarray:
        """Compute Nx2 trajectory array where each row is [x(t), y(t)].

        For purely 1D motion the y column is all zeros.
        """
        ...

    @abstractmethod
    def get_manim_scene_class(self, **kwargs: object) -> type[Scene]:
        """Return a dynamically constructed Manim Scene class for this model."""
        ...

    @abstractmethod
    def get_latex_label(self) -> str:
        """Return a LaTeX-formatted string describing the formula(s)."""
        ...

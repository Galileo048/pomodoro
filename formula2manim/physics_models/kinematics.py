"""Concrete physics models: uniform acceleration and projectile motion."""

import numpy as np
from sympy import lambdify, latex, symbols

from formula2manim.physics_models.base import PhysicsModel

_t = symbols("t")


class UniformAccelerationModel(PhysicsModel):
    """1D uniform acceleration: x = v0*t + 0.5*a*t^2

    Requires:
        formulas: {'x': Expr(t)}
        params: {'v0': float, 'a': float}
    """

    REQUIRED_VARS = {"x"}
    REQUIRED_PARAMS = {"v0", "a"}

    def compute_trajectory(
        self, time_range: tuple[float, float], num_points: int = 200
    ) -> np.ndarray:
        t_vals = np.linspace(time_range[0], time_range[1], num_points)

        x_expr = self.formulas["x"]
        subs_params = {symbols(k): v for k, v in self.params.items()}
        x_sub = x_expr.subs(subs_params)
        x_func = lambdify(_t, x_sub, "numpy")

        x_vals = np.asarray(x_func(t_vals), dtype=np.float64)
        if x_vals.ndim == 0:
            x_vals = np.full_like(t_vals, float(x_vals))

        return np.column_stack([x_vals, np.zeros_like(t_vals)])

    def get_manim_scene_class(self, **kwargs: object) -> type:
        from manim import Scene
        return Scene

    def get_latex_label(self) -> str:
        x_expr = self.formulas["x"]
        subs_params = {symbols(k): v for k, v in self.params.items()}
        x_sub = x_expr.subs(subs_params)
        return latex(x_sub)

    def get_axis_labels(self) -> tuple[str, str]:
        return ("t", "x")


class ProjectileMotionModel(PhysicsModel):
    """2D projectile motion: x = v0x*t, y = v0y*t - 0.5*g*t^2

    Requires:
        formulas: {'x': Expr(t), 'y': Expr(t)}
        params: {'v0x': float, 'v0y': float, 'g': float}
    """

    REQUIRED_VARS = {"x", "y"}
    REQUIRED_PARAMS = {"v0x", "v0y", "g"}

    def compute_trajectory(
        self, time_range: tuple[float, float], num_points: int = 200
    ) -> np.ndarray:
        t_vals = np.linspace(time_range[0], time_range[1], num_points)

        subs_params = {symbols(k): v for k, v in self.params.items()}

        x_expr = self.formulas["x"].subs(subs_params)
        y_expr = self.formulas["y"].subs(subs_params)

        x_func = lambdify(_t, x_expr, "numpy")
        y_func = lambdify(_t, y_expr, "numpy")

        x_vals = np.asarray(x_func(t_vals), dtype=np.float64)
        y_vals = np.asarray(y_func(t_vals), dtype=np.float64)

        if x_vals.ndim == 0:
            x_vals = np.full_like(t_vals, float(x_vals))
        if y_vals.ndim == 0:
            y_vals = np.full_like(t_vals, float(y_vals))

        return np.column_stack([x_vals, y_vals])

    def get_manim_scene_class(self, **kwargs: object) -> type:
        from manim import Scene
        return Scene

    def get_latex_label(self) -> str:
        x_expr = self.formulas["x"]
        y_expr = self.formulas["y"]
        subs_params = {symbols(k): v for k, v in self.params.items()}
        x_latex = latex(x_expr.subs(subs_params))
        y_latex = latex(y_expr.subs(subs_params))
        return f"{x_latex} \\\\ {y_latex}"

    def get_axis_labels(self) -> tuple[str, str]:
        return ("x", "y")

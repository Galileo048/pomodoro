"""Concrete physics models: uniform acceleration, projectile motion, multi-phase, and N-phase."""

import json
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


class NPhaseModel(PhysicsModel):
    """N-phase motion with arbitrary motion types per phase.

    Supports: linear, projectile, circular, harmonic motion types.
    Each phase has: t_start, t_end, type, and type-specific params.

    Requires:
        formulas: {'x': Expr, 'y': Expr} (ignored, used for compatibility)
        params: {'n_phases': int, 'phases': str (JSON list)}
    """

    REQUIRED_VARS = {"x", "y"}
    REQUIRED_PARAMS = {"n_phases", "phases"}

    # Supported motion types
    MOTION_TYPES = {
        "linear", "projectile", "circular", "harmonic",
        "uniform_accel", "damped_harmonic",
    }

    def _validate(self) -> None:
        """Validate phases structure."""
        from formula2manim.exceptions import ModelValidationError

        missing_vars = self.REQUIRED_VARS - set(self.formulas.keys())
        if missing_vars:
            raise ModelValidationError(
                f"Missing formula variables: {sorted(missing_vars)}. "
                f"NPhaseModel requires: {sorted(self.REQUIRED_VARS)}"
            )
        missing_params = self.REQUIRED_PARAMS - set(self.params.keys())
        if missing_params:
            raise ModelValidationError(
                f"Missing parameter values: {sorted(missing_params)}. "
                f"NPhaseModel requires: {sorted(self.REQUIRED_PARAMS)}"
            )

        # Parse and validate phases JSON
        phases = self._parse_phases()
        if not phases:
            raise ModelValidationError("No phases defined.")

        for i, phase in enumerate(phases):
            if "type" not in phase:
                raise ModelValidationError(f"Phase {i+1}: missing 'type'")
            if phase["type"] not in self.MOTION_TYPES:
                raise ModelValidationError(
                    f"Phase {i+1}: unknown type '{phase['type']}'. "
                    f"Supported: {sorted(self.MOTION_TYPES)}"
                )
            if "t_start" not in phase or "t_end" not in phase:
                raise ModelValidationError(
                    f"Phase {i+1}: missing 't_start' or 't_end'"
                )

    def _parse_phases(self) -> list[dict]:
        """Parse phases from params (JSON string or list)."""
        phases_raw = self.params.get("phases", "[]")
        if isinstance(phases_raw, str):
            return json.loads(phases_raw)
        return phases_raw

    def _compute_phase(
        self, phase: dict, t_arr: np.ndarray,
        x0: float, y0: float, vx0: float, vy0: float
    ) -> tuple[np.ndarray, np.ndarray, float, float, float, float]:
        """Compute trajectory for a single phase.

        Returns:
            (x_vals, y_vals, x_end, y_end, vx_end, vy_end)
        """
        p = phase.get("params", {})
        motion_type = phase["type"]
        dt = t_arr - t_arr[0]  # time relative to phase start

        if motion_type == "linear":
            vx = p.get("vx", vx0)
            vy = p.get("vy", vy0)
            x = x0 + vx * dt
            y = y0 + vy * dt
            return x, y, x[-1], y[-1], vx, vy

        elif motion_type == "projectile":
            vx = p.get("vx", vx0)
            vy = p.get("vy", vy0)
            g = p.get("g", 9.8)
            x = x0 + vx * dt
            y = y0 + vy * dt - 0.5 * g * dt**2
            return x, y, x[-1], y[-1], vx, vy - g * (t_arr[-1] - t_arr[0])

        elif motion_type == "uniform_accel":
            vx = p.get("vx", vx0)
            vy = p.get("vy", vy0)
            ax = p.get("ax", 0)
            ay = p.get("ay", 0)
            x = x0 + vx * dt + 0.5 * ax * dt**2
            y = y0 + vy * dt + 0.5 * ay * dt**2
            return x, y, x[-1], y[-1], vx + ax * dt[-1], vy + ay * dt[-1]

        elif motion_type == "circular":
            cx = p.get("cx", x0)
            cy = p.get("cy", y0)
            r = p.get("r", 2)
            omega = p.get("omega", 1.5)
            phase_offset = p.get("phase", 0)
            x = cx + r * np.cos(omega * dt + phase_offset)
            y = cy + r * np.sin(omega * dt + phase_offset)
            vx_end = -r * omega * np.sin(omega * dt[-1] + phase_offset)
            vy_end = r * omega * np.cos(omega * dt[-1] + phase_offset)
            return x, y, x[-1], y[-1], vx_end, vy_end

        elif motion_type == "harmonic":
            A = p.get("A", 1)
            omega = p.get("omega", 2)
            phi = p.get("phi", 0)
            axis = p.get("axis", "x")  # "x" or "y"
            if axis == "x":
                x = x0 + A * np.sin(omega * dt + phi)
                y = np.full_like(t_arr, y0)
                vx_end = A * omega * np.cos(omega * dt[-1] + phi)
                return x, y, x[-1], y[-1], vx_end, 0
            else:
                x = np.full_like(t_arr, x0)
                y = y0 + A * np.sin(omega * dt + phi)
                vy_end = A * omega * np.cos(omega * dt[-1] + phi)
                return x, y, x[-1], y[-1], 0, vy_end

        elif motion_type == "damped_harmonic":
            A = p.get("A", 1)
            omega = p.get("omega", 2)
            gamma = p.get("gamma", 0.1)  # damping coefficient
            phi = p.get("phi", 0)
            x = x0 + A * np.exp(-gamma * dt) * np.cos(omega * dt + phi)
            y = np.full_like(t_arr, y0)
            # Approximate velocity
            vx_end = -A * np.exp(-gamma * dt[-1]) * (
                gamma * np.cos(omega * dt[-1] + phi) +
                omega * np.sin(omega * dt[-1] + phi)
            )
            return x, y, x[-1], y[-1], vx_end, 0

        else:
            raise ValueError(f"Unknown motion type: {motion_type}")

    def compute_trajectory(
        self, time_range: tuple[float, float], num_points: int = 200
    ) -> np.ndarray:
        phases = self._parse_phases()
        if not phases:
            return np.zeros((num_points, 2))

        # Sort phases by start time
        phases.sort(key=lambda p: p["t_start"])

        # Compute points per phase
        total_time = time_range[1] - time_range[0]
        all_x, all_y = [], []
        x0, y0, vx0, vy0 = 0.0, 0.0, 0.0, 0.0

        for i, phase in enumerate(phases):
            t_start = phase["t_start"]
            t_end = phase["t_end"]
            phase_duration = t_end - t_start

            if phase_duration <= 0:
                continue

            # Allocate points proportional to duration
            n_points = max(2, int(num_points * phase_duration / total_time))
            if i == len(phases) - 1:  # last phase gets remaining points
                n_points = num_points - sum(max(2, int(num_points * (p["t_end"] - p["t_start"]) / total_time)) for p in phases[:-1])
                n_points = max(2, n_points)

            t_arr = np.linspace(t_start, t_end, n_points)
            x_vals, y_vals, x0, y0, vx0, vy0 = self._compute_phase(
                phase, t_arr, x0, y0, vx0, vy0
            )

            if i == 0:
                all_x.append(x_vals)
                all_y.append(y_vals)
            else:
                # Skip first point to avoid duplicate
                all_x.append(x_vals[1:])
                all_y.append(y_vals[1:])

        x_combined = np.concatenate(all_x)
        y_combined = np.concatenate(all_y)

        return np.column_stack([x_combined, y_combined])

    def get_manim_scene_class(self, **kwargs: object) -> type:
        from manim import Scene
        return Scene

    def get_latex_label(self) -> str:
        phases = self._parse_phases()
        labels = []
        for i, phase in enumerate(phases[:3], 1):  # Show max 3 phases
            t_start = phase["t_start"]
            t_end = phase["t_end"]
            motion_type = phase["type"]
            labels.append(f"Phase {i} ({t_start:.1f}-{t_end:.1f}s): {motion_type}")
        if len(phases) > 3:
            labels.append(f"... +{len(phases)-3} more phases")
        return " \\\\ ".join(labels)

    def get_axis_labels(self) -> tuple[str, str]:
        return ("x", "y")

    def get_phase_colors(self) -> list[str]:
        """Return colors for each phase (for multi-color trajectory rendering)."""
        colors = ["BLUE", "ORANGE", "GREEN", "RED", "PURPLE", "YELLOW", "CYAN"]
        phases = self._parse_phases()
        return [colors[i % len(colors)] for i in range(len(phases))]


class MultiPhaseModel(PhysicsModel):
    """Multi-phase motion with piecewise acceleration.

    Phase 1 (0 to t1): projectile motion with v0x, v0y, g
    Phase 2 (t1 to t_end): additional accelerations ax2, ay2

    Requires:
        formulas: {'x': Expr, 'y': Expr} (phase 1 formulas)
        params: {'v0x', 'v0y', 'g', 't1', 'ax2', 'ay2', 'h0', 't_end'}
    """

    REQUIRED_VARS = {"x", "y"}
    REQUIRED_PARAMS = {"v0x", "v0y", "g", "t1", "ax2", "ay2", "h0", "t_end"}

    def _validate(self) -> None:
        """Override to allow extra params beyond formula free symbols."""
        missing_vars = self.REQUIRED_VARS - set(self.formulas.keys())
        if missing_vars:
            from formula2manim.exceptions import ModelValidationError
            raise ModelValidationError(
                f"Missing formula variables: {sorted(missing_vars)}. "
                f"MultiPhaseModel requires: {sorted(self.REQUIRED_VARS)}"
            )
        missing_params = self.REQUIRED_PARAMS - set(self.params.keys())
        if missing_params:
            from formula2manim.exceptions import ModelValidationError
            raise ModelValidationError(
                f"Missing parameter values: {sorted(missing_params)}. "
                f"MultiPhaseModel requires: {sorted(self.REQUIRED_PARAMS)}"
            )

    def compute_trajectory(
        self, time_range: tuple[float, float], num_points: int = 200
    ) -> np.ndarray:
        p = self.params
        v0x = p["v0x"]
        v0y = p["v0y"]
        g = p["g"]
        t1 = p["t1"]
        ax2 = p["ax2"]
        ay2 = p["ay2"]
        h0 = p["h0"]
        t_end = p["t_end"]

        # Phase 1: projectile from t=0 to t=t1
        n1 = max(1, int(num_points * t1 / t_end))
        n2 = num_points - n1

        t_arr1 = np.linspace(0, t1, n1)
        x1 = v0x * t_arr1
        y1 = h0 + v0y * t_arr1 - 0.5 * g * t_arr1**2

        # State at transition
        x_at_t1 = x1[-1]
        y_at_t1 = y1[-1]
        vx_at_t1 = v0x  # constant in phase 1
        vy_at_t1 = v0y - g * t1

        # Phase 2: t1 to t_end
        t_arr2 = np.linspace(t1, t_end, n2)
        dt2 = t_arr2 - t1
        x2 = x_at_t1 + vx_at_t1 * dt2 + 0.5 * ax2 * dt2**2
        y2 = y_at_t1 + vy_at_t1 * dt2 + 0.5 * ay2 * dt2**2

        # Concatenate (skip first point of phase 2 to avoid duplicate)
        x_vals = np.concatenate([x1, x2[1:]])
        y_vals = np.concatenate([y1, y2[1:]])

        return np.column_stack([x_vals, y_vals])

    def get_manim_scene_class(self, **kwargs: object) -> type:
        from manim import Scene
        return Scene

    def get_latex_label(self) -> str:
        p = self.params
        return (
            f"Phase 1: v_{{0x}}={p['v0x']:.1f}, v_{{0y}}={p['v0y']:.1f} \\\\ "
            f"Phase 2: a_{{x2}}={p['ax2']:.2f}, a_{{y2}}={p['ay2']:.2f}"
        )

    def get_axis_labels(self) -> tuple[str, str]:
        return ("x", "y")

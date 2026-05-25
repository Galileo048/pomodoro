"""Tests for physics models and model detection."""

import numpy as np
import pytest

from formula2manim.exceptions import ModelValidationError
from formula2manim.parser.formula_parser import parse_formulas
from formula2manim.parser.param_parser import parse_params
from formula2manim.physics_models.kinematics import (
    ProjectileMotionModel,
    UniformAccelerationModel,
)
from formula2manim.physics_models.registry import detect_model


class TestUniformAccelerationModel:
    def test_validate_success(self):
        formulas = parse_formulas("x = v0*t + 0.5*a*t**2")
        model = UniformAccelerationModel(formulas, {"v0": 0.0, "a": 9.8})
        assert model is not None

    def test_validate_missing_var(self):
        formulas = parse_formulas("z = v0*t")
        with pytest.raises(ModelValidationError):
            UniformAccelerationModel(formulas, {"v0": 0.0, "a": 9.8})

    def test_validate_missing_param(self):
        formulas = parse_formulas("x = v0*t + 0.5*a*t**2")
        with pytest.raises(ModelValidationError):
            UniformAccelerationModel(formulas, {"v0": 0.0})

    def test_trajectory_shape(self, ua_model):
        traj = ua_model.compute_trajectory((0, 5), num_points=100)
        assert traj.shape == (100, 2)

    def test_trajectory_rest(self):
        formulas = parse_formulas("x = v0*t + 0.5*a*t**2")
        model = UniformAccelerationModel(formulas, {"v0": 0.0, "a": 10.0})
        traj = model.compute_trajectory((0, 1), num_points=3)

        # At t=0: x=0
        assert traj[0, 0] == pytest.approx(0.0)
        # At t=1: x = 0.5*10*1^2 = 5.0
        assert traj[-1, 0] == pytest.approx(5.0)

    def test_trajectory_initial_velocity(self):
        formulas = parse_formulas("x = v0*t + 0.5*a*t**2")
        model = UniformAccelerationModel(formulas, {"v0": 10.0, "a": 0.0})
        traj = model.compute_trajectory((0, 2), num_points=3)
        # At t=0: x=0
        assert traj[0, 0] == pytest.approx(0.0)
        # At t=2: x = 10*2 + 0 = 20
        assert traj[-1, 0] == pytest.approx(20.0)

    def test_y_column_zero(self, ua_model):
        traj = ua_model.compute_trajectory((0, 5))
        assert np.all(traj[:, 1] == 0.0)

    def test_latex_label(self, ua_model):
        label = ua_model.get_latex_label()
        assert "t" in label
        assert len(label) > 0


class TestProjectileMotionModel:
    def test_validate_success(self):
        formulas = parse_formulas("x = v0x*t; y = v0y*t - 0.5*g*t**2")
        model = ProjectileMotionModel(
            formulas, {"v0x": 10.0, "v0y": 20.0, "g": 9.8}
        )
        assert model is not None

    def test_validate_missing_var(self):
        formulas = parse_formulas("x = v0x*t")
        with pytest.raises(ModelValidationError):
            ProjectileMotionModel(formulas, {"v0x": 10.0, "v0y": 20.0, "g": 9.8})

    def test_validate_missing_param(self):
        formulas = parse_formulas("x = v0x*t; y = v0y*t - 0.5*g*t**2")
        with pytest.raises(ModelValidationError):
            ProjectileMotionModel(formulas, {"v0x": 10.0, "v0y": 20.0})

    def test_trajectory_shape(self, pm_model):
        traj = pm_model.compute_trajectory((0, 3), num_points=100)
        assert traj.shape == (100, 2)

    def test_trajectory_horizontal_only(self):
        """v0y=0, g=0: body moves only horizontally."""
        formulas = parse_formulas("x = v0x*t; y = v0y*t - 0.5*g*t**2")
        model = ProjectileMotionModel(formulas, {"v0x": 10.0, "v0y": 0.0, "g": 0.0})
        traj = model.compute_trajectory((0, 2), num_points=3)

        assert traj[0, 0] == pytest.approx(0.0)
        assert traj[-1, 0] == pytest.approx(20.0)
        assert np.all(traj[:, 1] == 0.0)

    def test_trajectory_parabolic(self, pm_model):
        """At t=0 and t=2*v0y/g, y should be 0 (on ground)."""
        traj = pm_model.compute_trajectory((0, 4.0816), num_points=100)

        # Starting point
        assert traj[0, 1] == pytest.approx(0.0)

        # Time of flight: t = 2*v0y/g = 40/9.8 ≈ 4.0816
        assert traj[-1, 1] == pytest.approx(0.0, abs=0.01)

    def test_max_height(self, pm_model):
        """Max height at t=v0y/g: y_max = v0y^2/(2g)."""
        traj = pm_model.compute_trajectory((0, 4.0816), num_points=500)
        y_max = traj[:, 1].max()
        expected = 20.0**2 / (2 * 9.8)  # ≈ 20.408
        assert y_max == pytest.approx(expected, rel=1e-2)

    def test_latex_label(self, pm_model):
        label = pm_model.get_latex_label()
        assert "\\\\" in label
        assert len(label) > 0


class TestModelDetection:
    def test_detect_2d(self):
        formulas = parse_formulas("x = v0x*t; y = v0y*t - 0.5*g*t**2")
        params = {"v0x": 10.0, "v0y": 20.0, "g": 9.8}
        assert detect_model(formulas, params) == "projectile_motion"

    def test_detect_1d_x(self):
        formulas = parse_formulas("x = v0*t + 0.5*a*t**2")
        params = {"v0": 0.0, "a": 9.8}
        assert detect_model(formulas, params) == "uniform_acceleration"

    def test_detect_1d_y(self):
        formulas = parse_formulas("y = v0*t - 0.5*g*t**2")
        params = {"v0": 20.0, "g": 9.8}
        assert detect_model(formulas, params) == "uniform_acceleration"

    def test_detect_fallback(self):
        formulas = parse_formulas("z = k*t")
        params = {"k": 1.0}
        assert detect_model(formulas, params) == "uniform_acceleration"

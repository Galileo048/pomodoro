"""
平抛运动 | 高中物理
物体以水平初速度抛出，在重力作用下运动
"""
from manim import *
import numpy as np


class ProjectileScene(Scene):
    def construct(self):
        v0x = __PARAM_v0x__
        v0y = __PARAM_v0y__
        g = __PARAM_g__

        t_flight = (v0y + np.sqrt(v0y**2 + 0)) / g if v0y >= 0 else 0
        if t_flight <= 0:
            t_flight = 2 * abs(v0y) / g if g > 0 else 5
        t_max = t_flight * 1.05

        def x(t):
            return v0x * t

        def y(t):
            return v0y * t - 0.5 * g * t * t

        x_range = v0x * t_max

        axes = Axes(
            x_range=[-0.5, x_range * 1.1, max(0.5, x_range / 8)],
            y_range=[min(-1, -0.5 * g * t_flight**2 * 1.2), max(v0y**2 / (2 * g) * 1.3, 2), 2],
            axis_config={"include_numbers": False},
            x_length=7, y_length=5.5, tips=True,
        )
        self.add(axes)
        self.add(Text("x (m)", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("y (m)", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        # Trajectory
        traj = axes.plot_parametric_curve(
            lambda t: np.array([x(t), y(t)]), t_range=[0, t_flight],
            color=BLUE, stroke_width=3)
        self.add(traj)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(x(t_tracker.get_value()), y(t_tracker.get_value())),
            color=RED, radius=0.1))
        self.add(dot)

        # Velocities
        vx_arrow = always_redraw(lambda: Arrow(
            axes.c2p(x(t_tracker.get_value()), y(t_tracker.get_value())),
            axes.c2p(x(t_tracker.get_value()) + v0x * 0.3, y(t_tracker.get_value())),
            color=GREEN, buff=0))
        vy_arrow = always_redraw(lambda: Arrow(
            axes.c2p(x(t_tracker.get_value()), y(t_tracker.get_value())),
            axes.c2p(x(t_tracker.get_value()), y(t_tracker.get_value()) + (v0y - g * t_tracker.get_value()) * 0.3),
            color=YELLOW, buff=0))
        self.add(vx_arrow, vy_arrow)

        # Info
        panel = Rectangle(width=3.2, height=2.0, fill_color=BLACK,
                          fill_opacity=0.8, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25)
        self.add(panel)
        pc = panel.get_center()
        t_lbl = Text("t =", font_size=22).move_to(pc + UP * 0.55 + LEFT * 1.0)
        t_num = always_redraw(lambda: Text(f"{t_tracker.get_value():.2f}s",
            font_size=22, color=YELLOW).next_to(t_lbl, RIGHT, buff=0.1))
        v_lbl = Text("vy =", font_size=22).move_to(pc + DOWN * 0.05 + LEFT * 1.0)
        v_num = always_redraw(lambda: Text(f"{v0y - g * t_tracker.get_value():.2f}",
            font_size=22, color=YELLOW).next_to(v_lbl, RIGHT, buff=0.1))
        self.add(t_lbl, t_num, v_lbl, v_num)

        self.wait(0.3)
        self.play(t_tracker.animate.set_value(t_flight), run_time=5, rate_func=linear)
        self.wait(2)

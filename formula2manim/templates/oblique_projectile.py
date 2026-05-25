"""
斜抛运动 | 高中物理
物体以初速度 v0 和角度 theta 抛出
"""
from manim import *
import numpy as np


class ObliqueProjectileScene(Scene):
    def construct(self):
        v0 = __PARAM_v0__
        angle_deg = __PARAM_angle__
        g = __PARAM_g__

        angle = np.radians(angle_deg)
        v0x = v0 * np.cos(angle)
        v0y = v0 * np.sin(angle)

        t_flight = 2 * v0y / g
        t_max = t_flight * 1.1

        def x(t):
            return v0x * t

        def y(t):
            return v0y * t - 0.5 * g * t * t

        x_range = v0x * t_flight
        y_max = v0y**2 / (2 * g)

        axes = Axes(
            x_range=[-0.5, x_range * 1.1, max(0.5, x_range / 8)],
            y_range=[-1, y_max * 1.3, max(0.5, y_max / 5)],
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

        # Max height marker
        t_peak = v0y / g
        peak = Dot(axes.c2p(x(t_peak), y(t_peak)), color=GREEN, radius=0.08)
        peak_lbl = Text(f"最高点 ({x(t_peak):.1f}, {y(t_peak):.1f})",
                        font_size=18, color=GREEN).next_to(peak, UP, buff=0.15)
        self.add(peak, peak_lbl)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(x(t_tracker.get_value()), y(t_tracker.get_value())),
            color=RED, radius=0.1))
        self.add(dot)

        # Info
        panel = Rectangle(width=3.2, height=1.8, fill_color=BLACK,
                          fill_opacity=0.8, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25)
        self.add(panel)
        pc = panel.get_center()
        t_lbl = Text("t =", font_size=22).move_to(pc + UP * 0.5 + LEFT * 1.0)
        t_num = always_redraw(lambda: Text(f"{t_tracker.get_value():.2f}s",
            font_size=22, color=YELLOW).next_to(t_lbl, RIGHT, buff=0.1))
        pos_lbl = Text("(x,y) =", font_size=22).move_to(pc + DOWN * 0.15 + LEFT * 1.0)
        pos_num = always_redraw(lambda: Text(
            f"({x(t_tracker.get_value()):.1f},{y(t_tracker.get_value()):.1f})",
            font_size=22, color=GREEN).next_to(pos_lbl, RIGHT, buff=0.1))
        self.add(t_lbl, t_num, pos_lbl, pos_num)

        self.wait(0.3)
        self.play(t_tracker.animate.set_value(t_flight), run_time=6, rate_func=linear)
        self.wait(2)

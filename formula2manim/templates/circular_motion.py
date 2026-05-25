"""
匀速圆周运动 | 高中物理
显示位置矢量、速度矢量、向心加速度矢量
"""
from manim import *
import numpy as np


class CircularMotionScene(Scene):
    def construct(self):
        r = __PARAM_radius__
        omega = __PARAM_omega__
        n_periods = __PARAM_periods__
        T = 2 * np.pi / omega
        t_max = n_periods * T

        def pos(t):
            return np.array([r * np.cos(omega * t), r * np.sin(omega * t)])

        def vel(t):
            return np.array([-r * omega * np.sin(omega * t), r * omega * np.cos(omega * t)])

        pad = r * 1.5
        axes = Axes(
            x_range=[-pad, pad, r / 2],
            y_range=[-pad, pad, r / 2],
            axis_config={"include_numbers": False},
            x_length=5.5, y_length=5.5, tips=True,
        )
        self.add(axes)
        self.add(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        # Circle
        circle = Circle(radius=axes.x_axis.unit_size * r, color=BLUE, stroke_width=2)
        circle.move_to(axes.c2p(0, 0))
        self.add(circle)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(axes.c2p(pos(t_tracker.get_value())[0],
                                                  pos(t_tracker.get_value())[1]),
                                        color=RED, radius=0.1))
        self.add(dot)

        # Radius line
        r_line = always_redraw(lambda: Line(
            axes.c2p(0, 0),
            axes.c2p(pos(t_tracker.get_value())[0], pos(t_tracker.get_value())[1]),
            color=GRAY, stroke_width=1))
        self.add(r_line)

        # Velocity arrow
        v_arrow = always_redraw(lambda: Arrow(
            axes.c2p(pos(t_tracker.get_value())[0], pos(t_tracker.get_value())[1]),
            axes.c2p(pos(t_tracker.get_value())[0] + vel(t_tracker.get_value())[0] * 0.2,
                     pos(t_tracker.get_value())[1] + vel(t_tracker.get_value())[1] * 0.2),
            color=GREEN, buff=0))
        self.add(v_arrow)

        # Labels
        v_text = Text(f"v = {r * omega:.1f} m/s", font_size=22, color=GREEN).to_corner(UR, buff=0.3)
        a_text = Text(f"a = {r * omega**2:.1f} m/s^2", font_size=22, color=YELLOW)
        a_text.next_to(v_text, DOWN, buff=0.1, aligned_edge=LEFT)
        self.add(v_text, a_text)

        self.wait(0.3)
        self.play(t_tracker.animate.set_value(t_max), run_time=8, rate_func=linear)
        self.wait(2)

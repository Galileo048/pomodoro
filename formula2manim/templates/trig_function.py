"""
三角函数图像 | 高中数学
y = A*sin(omega*x + phi) -- 可调振幅、频率、相位
"""
from manim import *
import numpy as np


class TrigFunctionScene(Scene):
    def construct(self):
        A = __PARAM_A__
        omega = __PARAM_omega__
        phi = __PARAM_phi__

        T = 2 * np.pi / omega if omega > 0 else 2 * np.pi
        x_max = T * 3
        x_min = -T * 0.5

        def f(x):
            return A * np.sin(omega * x + phi)

        def g(x):
            return A * np.cos(omega * x + phi)

        axes = Axes(
            x_range=[x_min, x_max, T / 2],
            y_range=[-A * 1.8, A * 1.8, max(0.5, A / 4)],
            axis_config={"include_numbers": False},
            x_length=9, y_length=4.5, tips=True,
        )
        self.play(Create(axes), run_time=1.2)
        self.play(
            Write(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)),
            Write(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25)),
            run_time=0.4,
        )

        # sin curve
        sin_curve = axes.plot(f, color=RED, stroke_width=3, x_range=[x_min, x_max])
        sin_lbl = Text(f"sin: y={A}*sin({omega}x+{phi})", font_size=20, color=RED)
        sin_lbl.to_corner(UR, buff=0.3)
        self.play(Create(sin_curve), Write(sin_lbl), run_time=2)

        # cos curve
        cos_curve = axes.plot(g, color=BLUE, stroke_width=2, x_range=[x_min, x_max])
        cos_lbl = Text(f"cos: y={A}*cos({omega}x+{phi})", font_size=20, color=BLUE)
        cos_lbl.next_to(sin_lbl, DOWN, buff=0.1, aligned_edge=LEFT)
        self.play(Create(cos_curve), Write(cos_lbl), run_time=1.5)

        # Phase shift marker
        shift = -phi / omega if omega > 0 else 0
        if x_min <= shift <= x_max:
            shift_line = DashedLine(
                axes.c2p(shift, -A * 1.8),
                axes.c2p(shift, A * 1.8),
                color=YELLOW, stroke_width=1,
            )
            shift_lbl = Text(f"相位={phi:.1f}rad", font_size=18, color=YELLOW)
            shift_lbl.next_to(shift_line, UP, buff=0.1)
            self.play(Create(shift_line), Write(shift_lbl), run_time=0.8)

        self.wait(3)

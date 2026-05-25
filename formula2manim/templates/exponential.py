"""
指数函数 & 对数函数 | 高中数学
y = a^x 和 y = log_a(x) -- 可调底数 a
"""
from manim import *
import numpy as np


class ExponentialScene(Scene):
    def construct(self):
        base = __PARAM_base__

        x_max = 4 if base > 1 else 4
        x_min = -2 if base > 1 else -4

        def exp_f(x):
            return base ** max(x, -100)

        def log_f(x):
            return np.log(max(x, 0.001)) / np.log(base)

        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[-2, base ** x_max * 1.1 if base > 1 else 10, 2],
            axis_config={"include_numbers": False},
            x_length=7, y_length=6, tips=True,
        )
        self.add(axes)
        self.add(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        # Exponential
        exp_curve = axes.plot(exp_f, color=RED, stroke_width=3,
                              x_range=[max(x_min, -2), min(x_max, 4)])
        exp_lbl = Text(f"y = {base}^x", font_size=24, color=RED)
        exp_lbl.next_to(axes.c2p(2, exp_f(2)), UP, buff=0.3)
        self.add(exp_curve, exp_lbl)

        # Logarithm
        log_curve = axes.plot(log_f, color=BLUE, stroke_width=3,
                              x_range=[0.05, min(x_max, 5)])
        log_lbl = Text(f"y = log_{base}(x)", font_size=24, color=BLUE)
        log_lbl.next_to(axes.c2p(3, log_f(3)), DOWN, buff=0.3)
        self.add(log_curve, log_lbl)

        # Diagonal y=x for symmetry
        diag = axes.plot(lambda x: x, color=GRAY, stroke_width=1,
                         stroke_opacity=0.5, x_range=[-1, x_max])
        self.add(diag)
        self.add(Text("y=x", font_size=16, color=GRAY)
                 .next_to(axes.c2p(3, 3), UP, buff=0.1))

        self.wait(3)

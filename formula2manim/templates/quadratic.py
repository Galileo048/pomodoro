"""
二次函数（抛物线）| 高中数学
y = ax^2 + bx + c  -- 可调 a, b, c
"""
from manim import *
import numpy as np


class QuadraticScene(Scene):
    def construct(self):
        a = __PARAM_a__
        b = __PARAM_b__
        c = __PARAM_c__

        def f(x):
            return a * x * x + b * x + c

        vertex_x = -b / (2 * a) if abs(a) > 0.001 else 0
        vertex_y = f(vertex_x)
        disc = b * b - 4 * a * c
        roots = []
        if abs(a) > 0.001 and disc >= 0:
            sqrt_d = np.sqrt(disc)
            roots = [(-b - sqrt_d) / (2 * a), (-b + sqrt_d) / (2 * a)]

        x_half = max(4, abs(vertex_x) + 3, (max(roots) + 1) if roots else 4)
        x_lo, x_hi = vertex_x - x_half, vertex_x + x_half
        y_vals = [f(x) for x in np.linspace(x_lo, x_hi, 100)]
        y_lo, y_hi = min(y_vals) - 1, max(y_vals) + 1

        axes = Axes(
            x_range=[x_lo, x_hi, max(0.5, x_half / 5)],
            y_range=[y_lo, y_hi, max(0.5, (y_hi - y_lo) / 8)],
            axis_config={"include_numbers": False},
            x_length=8, y_length=5.5, tips=True,
        )
        self.play(Create(axes), run_time=1.2)
        self.play(
            Write(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)),
            Write(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25)),
            run_time=0.4,
        )

        # Parabola
        curve = axes.plot(f, color=BLUE, stroke_width=3, x_range=[x_lo, x_hi])
        eq = Text(f"y = {a}x^2 + {b}x + {c}", font_size=24, color=BLUE).to_corner(UR, buff=0.3)
        self.play(Create(curve), Write(eq), run_time=2)

        # Vertex
        v_dot = Dot(axes.c2p(vertex_x, vertex_y), color=RED, radius=0.08)
        v_lbl = Text(f"顶点({vertex_x:.2f},{vertex_y:.2f})", font_size=18, color=RED)
        v_lbl.next_to(v_dot, UP if a < 0 else DOWN, buff=0.15)
        self.play(FadeIn(v_dot), Write(v_lbl), run_time=0.8)

        # Roots
        for rx in roots:
            r_dot = Dot(axes.c2p(rx, 0), color=GREEN, radius=0.08)
            r_lbl = Text(f"({rx:.2f},0)", font_size=18, color=GREEN)
            r_lbl.next_to(r_dot, DOWN if a > 0 else UP, buff=0.12)
            self.play(FadeIn(r_dot), Write(r_lbl), run_time=0.6)

        self.wait(3)

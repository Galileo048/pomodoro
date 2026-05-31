"""
割线→切线 极限演示 | 高中数学·导数
演示函数在 x=a 处的导数定义：Δx→0 时割线趋近于切线
"""
from manim import *
import numpy as np
from math import sin, cos, exp, log, sqrt, pi, e


class SecantToTangentScene(Scene):
    def construct(self):
        a = __PARAM_a__
        h_start = __PARAM_h_start__
        code = r"__PARAM_func_expr__"

        def f(x):
            ns = {"x": x, "sin": sin, "cos": cos, "exp": exp,
                  "log": log, "sqrt": sqrt, "pi": pi, "e": e}
            return float(eval(code, {"__builtins__": {}}, ns))

        f_prime = (f(a + 0.0001) - f(a)) / 0.0001

        x_lo, x_hi = a - 2.5, a + 3.5
        y_vals = [f(x) for x in np.linspace(x_lo, x_hi, 100)]
        y_lo, y_hi = min(y_vals) - 1, max(y_vals) + 3

        axes = Axes(
            x_range=[x_lo, x_hi, 1],
            y_range=[y_lo, y_hi, 1],
            axis_config={"include_numbers": False, "font_size": 20},
            x_length=7, y_length=5.5, tips=True,
        )
        self.play(Create(axes), run_time=1.2)
        self.play(
            Write(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)),
            Write(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25)),
            run_time=0.4,
        )

        # Curve
        curve = axes.plot(f, color=BLUE, stroke_width=3)
        curve_lbl = Text(f"f(x)={code}", font_size=20, color=BLUE)
        curve_lbl.next_to(axes.c2p(a + 2, f(a + 2)), UP)
        self.play(Create(curve), Write(curve_lbl), run_time=2)

        # Fixed point P
        P = Dot(axes.c2p(a, f(a)), color=RED, radius=0.1)
        P_lbl = Text("P", font_size=22, color=RED).next_to(P, DL, buff=0.12)
        self.play(FadeIn(P), Write(P_lbl), run_time=0.5)

        # Moving point Q
        h_tracker = ValueTracker(h_start)
        Q = always_redraw(lambda: Dot(
            axes.c2p(a + h_tracker.get_value(), f(a + h_tracker.get_value())),
            color=YELLOW, radius=0.1))
        Q_lbl = always_redraw(lambda: Text("Q", font_size=22, color=YELLOW)
            .next_to(axes.c2p(a + h_tracker.get_value(), f(a + h_tracker.get_value())),
                     UR, buff=0.12))
        self.play(FadeIn(Q), Write(Q_lbl), run_time=0.5)

        # Secant line
        secant = always_redraw(lambda: Line(
            axes.c2p(a, f(a)),
            axes.c2p(a + h_tracker.get_value(), f(a + h_tracker.get_value())),
            color=GREEN, stroke_width=2.5))
        self.play(Create(secant), run_time=0.5)

        # Info panel
        panel = Rectangle(width=3.8, height=2.6, fill_color="#1a1a2e",
                          fill_opacity=0.85, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25).set_z_index(10)
        self.play(FadeIn(panel), run_time=0.4)
        pc = panel.get_center()

        dy_lbl = Text("Δy =", font_size=24).move_to(pc + UP * 0.85 + LEFT * 1.2)
        dy_num = always_redraw(lambda: Text(f"{f(a + h_tracker.get_value()) - f(a):.4f}",
            font_size=24, color=YELLOW).next_to(dy_lbl, RIGHT, buff=0.15))
        dx_lbl = Text("Δx =", font_size=24).move_to(pc + UP * 0.25 + LEFT * 1.2)
        dx_num = always_redraw(lambda: Text(f"{h_tracker.get_value():.4f}",
            font_size=24, color=YELLOW).next_to(dx_lbl, RIGHT, buff=0.15))
        slope_lbl = Text("Δy/Δx =", font_size=24).move_to(pc + DOWN * 0.35 + LEFT * 1.2)
        slope_num = always_redraw(lambda: Text(
            f"{(f(a + h_tracker.get_value()) - f(a)) / h_tracker.get_value():.4f}",
            font_size=24, color=GREEN).next_to(slope_lbl, RIGHT, buff=0.15))
        lim_lbl = Text(f"→ f'({a}) = {f_prime:.3f}", font_size=20, color=RED)
        lim_lbl.move_to(pc + DOWN * 0.95)

        self.play(Write(dy_lbl), Write(dx_lbl), Write(slope_lbl), Write(lim_lbl), run_time=0.8)
        self.add(dy_num, dx_num, slope_num)

        # Animate Q → P
        self.wait(0.3)
        self.play(h_tracker.animate.set_value(0.02), run_time=6, rate_func=smooth)
        self.wait(0.3)

        # Tangent line
        tangent = axes.plot(lambda x: f_prime * (x - a) + f(a), color=RED,
                            stroke_width=2.5, x_range=[x_lo + 0.5, x_hi - 0.5])
        t_lbl = Text(f"切线 y={f_prime:.2f}x+{f(a)-f_prime*a:.2f}", font_size=22, color=RED)
        t_lbl.next_to(lim_lbl, DOWN, buff=0.12)
        self.play(Create(tangent), Write(t_lbl), run_time=1.5)
        self.play(Create(SurroundingRectangle(VGroup(slope_lbl, slope_num),
                        color=GREEN, buff=0.1)), run_time=0.8)
        self.wait(3)

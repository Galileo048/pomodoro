"""
定积分（黎曼和→面积）| 高中数学
矩形数量从少到多，从黎曼和逼近定积分
"""
from manim import *
import numpy as np


class RiemannSumScene(Scene):
    def construct(self):
        code = r"__PARAM_func_expr__"
        x_min = __PARAM_x_min__
        x_max = __PARAM_x_max__
        max_n = __PARAM_max_rects__

        def f(x):
            ns = {"x": x, "sin": np.sin, "cos": np.cos, "exp": np.exp,
                  "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e, "abs": abs}
            return float(eval(code, {"__builtins__": {}}, ns))

        axes = Axes(
            x_range=[x_min - 0.5, x_max + 0.5, 0.5],
            y_range=[-0.5, max(f(x) for x in np.linspace(x_min, x_max, 50)) * 1.3, 1],
            axis_config={"include_numbers": False},
            x_length=7, y_length=5, tips=True,
        )
        self.add(axes)
        self.add(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        # Curve
        curve = axes.plot(f, color=BLUE, stroke_width=3, x_range=[x_min, x_max])
        self.add(curve)
        self.add(Text(f"f(x)={code}", font_size=22, color=BLUE)
                 .next_to(axes.c2p((x_min + x_max) / 2, f((x_min + x_max) / 2)), UP))

        # n rectangles
        n_tracker = ValueTracker(2)

        rects = always_redraw(lambda: self._make_rects(
            axes, f, x_min, x_max, int(n_tracker.get_value())))
        self.add(rects)

        # Info
        panel = Rectangle(width=3.2, height=1.6, fill_color=BLACK,
                          fill_opacity=0.8, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25)
        self.add(panel)
        pc = panel.get_center()

        n_lbl = Text("矩形数:", font_size=22).move_to(pc + UP * 0.4 + LEFT * 0.8)
        n_num = always_redraw(lambda: Text(f"{int(n_tracker.get_value())}",
            font_size=22, color=YELLOW).next_to(n_lbl, RIGHT, buff=0.1))
        sum_lbl = Text("黎曼和:", font_size=22).move_to(pc + DOWN * 0.25 + LEFT * 0.8)
        sum_num = always_redraw(lambda: Text(
            f"{self._riemann_sum(f, x_min, x_max, int(n_tracker.get_value())):.4f}",
            font_size=22, color=GREEN).next_to(sum_lbl, RIGHT, buff=0.1))
        self.add(n_lbl, n_num, sum_lbl, sum_num)

        self.wait(0.5)
        self.play(n_tracker.animate.set_value(max_n), run_time=8, rate_func=smooth)
        self.wait(2)

    def _riemann_sum(self, f, a, b, n):
        dx = (b - a) / n
        return sum(f(a + i * dx) * dx for i in range(n))

    def _make_rects(self, axes, f, a, b, n):
        dx = (b - a) / n
        group = VGroup()
        for i in range(n):
            xi = a + i * dx
            h = f(xi)
            if h >= 0:
                rect = Rectangle(
                    width=axes.x_axis.unit_size * dx,
                    height=axes.y_axis.unit_size * h,
                    color=YELLOW, fill_opacity=0.4, stroke_width=1,
                )
                rect.move_to(axes.c2p(xi + dx / 2, h / 2), aligned_edge=DOWN)
                group.add(rect)
        return group

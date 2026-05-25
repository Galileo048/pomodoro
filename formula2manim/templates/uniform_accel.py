"""
匀加速直线运动 | 高中物理
x = v0*t + 0.5*a*t^2  -- 可调初速度和加速度
"""
from manim import *


class UniformAccelScene(Scene):
    def construct(self):
        v0 = __PARAM_v0__
        a = __PARAM_a__
        t_max = __PARAM_t_max__

        def x(t):
            return v0 * t + 0.5 * a * t * t

        def v(t):
            return v0 + a * t

        # Axes
        axes = Axes(
            x_range=[-0.5, t_max * 1.1, max(1, t_max / 5)],
            y_range=[-5, x(t_max) * 1.2, max(1, x(t_max) / 8)],
            axis_config={"include_numbers": False},
            x_length=7, y_length=5.5, tips=True,
        )
        self.add(axes)
        self.add(Text("t (s)", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("x (m)", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        # Curve
        curve = axes.plot(x, color=BLUE, stroke_width=3, x_range=[0, t_max])
        self.add(curve)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(t_tracker.get_value(), x(t_tracker.get_value())),
            color=RED, radius=0.1))
        self.add(dot)

        # Info panel
        panel = Rectangle(width=3.2, height=2.6, fill_color=BLACK,
                          fill_opacity=0.8, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25)
        self.add(panel)
        pc = panel.get_center()

        eq_lbl = Text(f"x = {v0}t + {0.5*a}*t^2", font_size=22, color=BLUE)
        eq_lbl.move_to(pc + UP * 0.85 + LEFT * 0.5)
        t_lbl = Text("t =", font_size=22).move_to(pc + UP * 0.25 + LEFT * 1.0)
        t_num = always_redraw(lambda: Text(f"{t_tracker.get_value():.2f} s",
            font_size=22, color=YELLOW).next_to(t_lbl, RIGHT, buff=0.1))
        x_lbl = Text("x =", font_size=22).move_to(pc + DOWN * 0.25 + LEFT * 1.0)
        x_num = always_redraw(lambda: Text(f"{x(t_tracker.get_value()):.2f} m",
            font_size=22, color=YELLOW).next_to(x_lbl, RIGHT, buff=0.1))
        v_lbl = Text("v =", font_size=22).move_to(pc + DOWN * 0.75 + LEFT * 1.0)
        v_num = always_redraw(lambda: Text(f"{v(t_tracker.get_value()):.2f} m/s",
            font_size=22, color=GREEN).next_to(v_lbl, RIGHT, buff=0.1))

        self.add(eq_lbl, t_lbl, t_num, x_lbl, x_num, v_lbl, v_num)

        # Animate
        self.wait(0.5)
        self.play(t_tracker.animate.set_value(t_max), run_time=8, rate_func=linear)
        self.wait(2)

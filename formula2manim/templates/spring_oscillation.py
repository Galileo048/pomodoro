"""
简谐振动（弹簧振子）| 高中物理
左侧：弹簧振子动画 | 右侧：位移-时间 x=A*sin(ωt) 曲线
"""
from manim import *
import numpy as np


class SpringOscillationScene(Scene):
    def construct(self):
        A = __PARAM_amplitude__
        omega = __PARAM_omega__
        n_cycles = __PARAM_cycles__
        T = 2 * np.pi / omega
        t_max = n_cycles * T

        # ── Left: Spring animation ──
        left_axes = Axes(
            x_range=[-A * 1.5, A * 1.5, A / 2],
            y_range=[-1, 1, 0.5],
            axis_config={"include_numbers": False},
            x_length=4, y_length=2, tips=False,
        )
        left_axes.to_edge(LEFT, buff=0.8).shift(UP * 2)
        eq_line = DashedLine(left_axes.c2p(-A * 1.5, 0), left_axes.c2p(A * 1.5, 0),
                             color=GRAY, stroke_width=1)
        self.play(Create(left_axes), Create(eq_line), run_time=1)
        self.play(Write(Text("平衡位置", font_size=16, color=GRAY)
                        .next_to(eq_line, UP, buff=0.1).shift(RIGHT * 1)),
                  run_time=0.4)

        # ── Right: x-t Curve ──
        right_axes = Axes(
            x_range=[0, t_max * 1.05, T if T > 0.5 else 0.5],
            y_range=[-A * 1.3, A * 1.3, A / 2],
            axis_config={"include_numbers": False},
            x_length=6, y_length=3, tips=True,
        )
        right_axes.to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
        self.play(Create(right_axes), run_time=1)
        self.play(
            Write(Text("t", font_size=22).next_to(right_axes.x_axis.get_end(), DOWN, buff=0.2)),
            Write(Text("x", font_size=22).next_to(right_axes.y_axis.get_end(), LEFT, buff=0.2)),
            run_time=0.4,
        )

        # x-t curve
        curve = right_axes.plot(lambda t: A * np.sin(omega * t), color=BLUE,
                                stroke_width=2, x_range=[0, t_max])
        self.play(Create(curve), run_time=2)

        # Mass + curve dot
        t_tracker = ValueTracker(0)
        mass = always_redraw(lambda: Circle(radius=0.2, color=RED, fill_opacity=0.8)
            .move_to(left_axes.c2p(A * np.sin(omega * t_tracker.get_value()), 0)))
        c_dot = always_redraw(lambda: Dot(
            right_axes.c2p(t_tracker.get_value(), A * np.sin(omega * t_tracker.get_value())),
            color=RED, radius=0.08))
        self.play(FadeIn(mass), FadeIn(c_dot), run_time=0.5)

        # Info
        info = Text(f"A={A:.1f}  omega={omega:.1f}  T={T:.2f}s", font_size=22, color=WHITE)
        info.to_edge(DOWN, buff=0.5)
        self.play(Write(info), run_time=0.5)

        self.wait(0.2)
        self.play(t_tracker.animate.set_value(t_max), run_time=10, rate_func=linear)
        self.wait(2)

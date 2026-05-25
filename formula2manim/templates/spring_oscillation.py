"""
简谐振动（弹簧振子）| 高中物理
左侧：弹簧振子动画 | 右侧：位移-时间 x=A*sin(ωt) 曲线
"""
from manim import *
import numpy as np


class SpringOscillationScene(Scene):
    def construct(self):
        A = __PARAM_amplitude__       # 振幅
        omega = __PARAM_omega__       # 角频率
        n_cycles = __PARAM_cycles__   # 周期数
        T = 2 * np.pi / omega
        t_max = n_cycles * T

        # ── Left: Spring animation ──
        left_axes = Axes(
            x_range=[-A * 1.5, A * 1.5, A / 2],
            y_range=[-1, 1, 0.5],
            axis_config={"include_numbers": False},
            x_length=4, y_length=2, tips=False,
        )
        left_axes.to_edge(LEFT, buff=0.8)
        left_axes.shift(UP * 2)
        self.add(left_axes)

        # Mass
        t_tracker = ValueTracker(0)
        mass = always_redraw(lambda: Circle(radius=0.2, color=RED, fill_opacity=0.8)
            .move_to(left_axes.c2p(A * np.sin(omega * t_tracker.get_value()), 0)))
        self.add(mass)

        # Equilibrium line
        eq_line = DashedLine(left_axes.c2p(-A * 1.5, 0), left_axes.c2p(A * 1.5, 0),
                             color=GRAY, stroke_width=1)
        self.add(eq_line)
        self.add(Text("平衡位置", font_size=16, color=GRAY)
                 .next_to(eq_line, UP, buff=0.1).shift(RIGHT * 1))

        # ── Right: x-t Curve ──
        right_axes = Axes(
            x_range=[0, t_max * 1.05, T if T > 0.5 else 0.5],
            y_range=[-A * 1.3, A * 1.3, A / 2],
            axis_config={"include_numbers": False},
            x_length=6, y_length=3, tips=True,
        )
        right_axes.to_edge(RIGHT, buff=0.5)
        right_axes.shift(UP * 1.5)
        self.add(right_axes)
        self.add(Text("t", font_size=22).next_to(right_axes.x_axis.get_end(), DOWN, buff=0.2))
        self.add(Text("x", font_size=22).next_to(right_axes.y_axis.get_end(), LEFT, buff=0.2))

        # x-t curve
        curve = right_axes.plot(lambda t: A * np.sin(omega * t),
                                color=BLUE, stroke_width=2, x_range=[0, t_max])
        self.add(curve)

        # Curve dot
        c_dot = always_redraw(lambda: Dot(
            right_axes.c2p(t_tracker.get_value(),
                           A * np.sin(omega * t_tracker.get_value())),
            color=RED, radius=0.08))
        self.add(c_dot)

        # Info
        info = Text(f"A={A:.1f}  omega={omega:.1f}  T={T:.2f}s",
                    font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        self.add(info)

        self.wait(0.3)
        self.play(t_tracker.animate.set_value(t_max), run_time=10, rate_func=linear)
        self.wait(2)

"""
波的传播 | 高中物理
一维行波 y=A*sin(2pi(x/lambda - t/T)) 向右传播
"""
from manim import *
import numpy as np


class WaveScene(Scene):
    def construct(self):
        A = __PARAM_amplitude__
        wavelength = __PARAM_wavelength__
        speed = __PARAM_speed__

        T = wavelength / speed

        def wave(x, t):
            return A * np.sin(2 * np.pi * (x / wavelength - t / T))

        axes = Axes(
            x_range=[0, wavelength * 4, wavelength / 2],
            y_range=[-A * 1.5, A * 1.5, A / 2],
            axis_config={"include_numbers": False},
            x_length=10, y_length=4, tips=True,
        )
        self.add(axes)
        self.add(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        # Animated wave
        t_tracker = ValueTracker(0)

        wave_curve = always_redraw(lambda: axes.plot(
            lambda x: wave(x, t_tracker.get_value()),
            color=BLUE, stroke_width=2.5, x_range=[0, wavelength * 4],
        ))
        self.add(wave_curve)

        # Moving dot on wave (follows a specific x position)
        x0 = wavelength
        dot = always_redraw(lambda: Dot(
            axes.c2p(x0, wave(x0, t_tracker.get_value())),
            color=RED, radius=0.08))
        self.add(dot)

        # Info
        info = Text(f"A={A:.1f}  lambda={wavelength:.1f}  v={speed:.1f}  T={T:.2f}",
                    font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        self.add(info)

        self.wait(0.3)
        self.play(t_tracker.animate.set_value(T * 3), run_time=8, rate_func=linear)
        self.wait(2)

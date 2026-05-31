"""
多阶段运动 | 高中物理
支持分段运动：平抛+电场、加速+减速等
"""
from manim import *
import numpy as np


class MultiPhaseScene(Scene):
    def construct(self):
        # Phase 1: 0 ~ t1 (平抛)
        v0x = __PARAM_v0x__
        v0y = __PARAM_v0y__
        g = __PARAM_g__
        t1 = __PARAM_t1__

        # Phase 2: t1 ~ t_end (加电场)
        ax2 = __PARAM_ax2__
        ay2 = __PARAM_ay2__

        h0 = __PARAM_h0__
        t_end = __PARAM_t_end__

        # --- Phase 1: 平抛 0~t1 ---
        def x1(t):
            return v0x * t

        def y1(t):
            return h0 + v0y * t - 0.5 * g * t**2

        def vx1(t):
            return v0x

        def vy1(t):
            return v0y - g * t

        # --- Phase 2: t1~t_end (电场) ---
        x_at_t1 = x1(t1)
        y_at_t1 = y1(t1)
        vx_at_t1 = vx1(t1)
        vy_at_t1 = vy1(t1)

        def x2(t):
            dt = t - t1
            return x_at_t1 + vx_at_t1 * dt + 0.5 * ax2 * dt**2

        def y2(t):
            dt = t - t1
            return y_at_t1 + vy_at_t1 * dt + 0.5 * ay2 * dt**2

        def vx2(t):
            return vx_at_t1 + ax2 * (t - t1)

        def vy2(t):
            return vy_at_t1 + ay2 * (t - t1)

        # Combined functions
        def x(t):
            return x1(t) if t <= t1 else x2(t)

        def y(t):
            return y1(t) if t <= t1 else y2(t)

        def vx(t):
            return vx1(t) if t <= t1 else vx2(t)

        def vy(t):
            return vy1(t) if t <= t1 else vy2(t)

        # --- Compute trajectory ---
        n_phase1 = int(t1 / t_end * 200)
        n_phase2 = 200 - n_phase1
        t_arr1 = np.linspace(0, t1, n_phase1)
        t_arr2 = np.linspace(t1, t_end, n_phase2)
        t_arr = np.concatenate([t_arr1, t_arr2])

        x_vals = np.array([x(t) for t in t_arr])
        y_vals = np.array([y(t) for t in t_arr])

        x_min, x_max = float(x_vals.min()), float(x_vals.max())
        y_min, y_max = float(y_vals.min()), float(y_vals.max())

        x_pad = max(1.0, (x_max - x_min) * 0.15)
        y_pad = max(1.0, (y_max - y_min) * 0.15)

        axes = Axes(
            x_range=[x_min - x_pad, x_max + x_pad, max(1, (x_max - x_min) / 8)],
            y_range=[y_min - y_pad, y_max + y_pad, max(1, (y_max - y_min) / 6)],
            axis_config={"include_numbers": False, "font_size": 24},
            x_length=7, y_length=5.5, tips=True,
        )
        x_l = Text("x (m)", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)
        y_l = Text("y (m)", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25)
        self.play(Create(axes), Write(x_l), Write(y_l), run_time=1.5)

        # Phase 1 trajectory (blue)
        traj1 = VMobject(color=BLUE, stroke_width=3)
        pts1 = [axes.c2p(float(x(t)), float(y(t))) for t in t_arr1]
        traj1.set_points_smoothly(pts1)

        # Phase 2 trajectory (orange)
        traj2 = VMobject(color=ORANGE, stroke_width=3)
        pts2 = [axes.c2p(float(x(t)), float(y(t))) for t in t_arr2]
        traj2.set_points_smoothly(pts2)

        # Phase 1 label
        phase1_lbl = Text("Phase 1: Projectile", font_size=18, color=BLUE)
        phase1_lbl.to_corner(UL, buff=0.3).shift(DOWN * 0.5)

        # Phase 2 label
        phase2_lbl = Text("Phase 2: + Electric Field", font_size=18, color=ORANGE)
        phase2_lbl.next_to(phase1_lbl, DOWN, buff=0.15)

        # Show phase 1
        self.play(Write(phase1_lbl), run_time=0.5)
        self.play(Create(traj1), run_time=2)

        # Show phase 2
        self.play(Write(phase2_lbl), run_time=0.5)
        self.play(Create(traj2), run_time=2)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(float(x(t_tracker.get_value())), float(y(t_tracker.get_value()))),
            color=RED, radius=0.1))
        self.play(FadeIn(dot, scale=0.5), run_time=0.5)

        # Velocity arrow
        vel_arrow = always_redraw(lambda: Arrow(
            axes.c2p(float(x(t_tracker.get_value())), float(y(t_tracker.get_value()))),
            axes.c2p(
                float(x(t_tracker.get_value()) + vx(t_tracker.get_value()) * 0.15),
                float(y(t_tracker.get_value()) + vy(t_tracker.get_value()) * 0.15)),
            color=GREEN, buff=0, stroke_width=3))
        self.play(GrowArrow(vel_arrow), run_time=0.5)

        # t=3 marker
        t3_dot = Dot(axes.c2p(float(x(t1)), float(y(t1))), color=YELLOW, radius=0.08)
        t3_lbl = Text(f"t={t1}s", font_size=18, color=YELLOW)
        t3_lbl.next_to(t3_dot, UP, buff=0.15)
        self.play(FadeIn(t3_dot), Write(t3_lbl), run_time=0.5)

        # Info panel
        panel = Rectangle(width=3.2, height=2.0, fill_color="#1a1a2e",
                          fill_opacity=0.85, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25).set_z_index(10)
        self.play(FadeIn(panel), run_time=0.4)
        pc = panel.get_center()
        t_l = Text("t =", font_size=20).move_to(pc + UP * 0.5 + LEFT * 0.8)
        h_l = Text("h =", font_size=20).move_to(pc + DOWN * 0.1 + LEFT * 0.8)
        self.play(Write(t_l), Write(h_l), run_time=0.5)

        t_num = always_redraw(lambda: Text(f"{t_tracker.get_value():.2f}s",
            font_size=20, color=YELLOW).next_to(t_l, RIGHT, buff=0.1))
        h_num = always_redraw(lambda: Text(f"{y(t_tracker.get_value()):.1f}m",
            font_size=20, color=YELLOW).next_to(h_l, RIGHT, buff=0.1))
        self.add(t_num, h_num)

        # Animate
        self.wait(0.3)
        self.play(t_tracker.animate.set_value(t_end), run_time=10, rate_func=linear)
        self.wait(2)

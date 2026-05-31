"""
动量守恒（弹性碰撞）| 高中物理
两球相向运动→碰撞→分离，不重叠
"""
from manim import *
import numpy as np


class CollisionScene(Scene):
    def construct(self):
        m1 = __PARAM_m1__
        m2 = __PARAM_m2__
        v1i = __PARAM_v1i__
        v2i = __PARAM_v2i__

        # Elastic collision formulas
        v1f = ((m1 - m2) * v1i + 2 * m2 * v2i) / (m1 + m2)
        v2f = (2 * m1 * v1i + (m2 - m1) * v2i) / (m1 + m2)

        def ball_r(m):
            return min(0.25 + 0.12 * np.sqrt(abs(m)), 0.6)

        r1 = ball_r(m1)
        r2 = ball_r(m2)
        max_speed = max(abs(v1i), abs(v2i), abs(v1f), abs(v2f), 1)
        pad = max_speed * 1.2 + r1 + r2 + 1
        line_len = 2 * pad

        axes = NumberLine(
            x_range=[-pad, pad, max(0.5, pad / 8)],
            include_numbers=False, length=10,
        )
        unit_sz = 10 / line_len  # screen units per data unit

        self.play(Create(axes), run_time=1)
        self.play(Write(Text("x (m)", font_size=24).next_to(
            axes.get_end(), DOWN, buff=0.2)), run_time=0.3)

        def x2p(x):
            return axes.number_to_point(x)

        # Place balls far enough apart
        sep = r1 + r2 + 1.0  # data-unit separation between centers
        start1 = -sep / 2
        start2 = sep / 2

        ball1 = Circle(radius=r1 * unit_sz, color=RED, fill_opacity=0.8)
        ball1.move_to(x2p(start1))
        ball2 = Circle(radius=r2 * unit_sz, color=BLUE, fill_opacity=0.8)
        ball2.move_to(x2p(start2))

        lbl1 = Text(f"m1={m1:.1f}kg", font_size=18, color=RED).next_to(ball1, DOWN, buff=0.3)
        lbl2 = Text(f"m2={m2:.1f}kg", font_size=18, color=BLUE).next_to(ball2, DOWN, buff=0.3)
        self.play(FadeIn(ball1), FadeIn(ball2), Write(lbl1), Write(lbl2), run_time=1)

        # Velocity arrows
        arr1 = Arrow(ball1.get_center(),
                     ball1.get_center() + RIGHT * max(0.3, abs(v1i) * 0.3) * np.sign(v1i or 1),
                     color=GREEN, buff=0) if abs(v1i) > 0.01 else None
        arr2 = Arrow(ball2.get_center(),
                     ball2.get_center() + RIGHT * max(0.3, abs(v2i) * 0.3) * np.sign(v2i or 1),
                     color=GREEN, buff=0) if abs(v2i) > 0.01 else None
        if arr1:
            self.play(GrowArrow(arr1), run_time=0.3)
        if arr2:
            self.play(GrowArrow(arr2), run_time=0.3)

        # Info panels
        def mk_panel(anchor):
            r = Rectangle(width=3.6, height=2.6, fill_color=BLACK,
                          fill_opacity=0.85, stroke_color=GRAY, stroke_width=1)
            r.to_corner(anchor, buff=0.25).set_z_index(10)
            return r

        panel_l = mk_panel(UL)
        panel_r = mk_panel(UR)
        self.play(FadeIn(panel_l), FadeIn(panel_r), run_time=0.5)

        # Left panel: before
        pc_l = panel_l.get_center()
        items_l = VGroup()
        title_l = Text("── 碰撞前 ──", font_size=22, color=WHITE)
        items_l.add(title_l)
        for txt, clr in [(f"v1 = {v1i:.2f} m/s", GREEN),
                          (f"v2 = {v2i:.2f} m/s", GREEN),
                          (f"p  = {m1*v1i+m2*v2i:.2f}", WHITE),
                          (f"Ek = {0.5*m1*v1i**2+0.5*m2*v2i**2:.1f}", GRAY)]:
            t = Text(txt, font_size=20, color=clr)
            items_l.add(t)
        items_l.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        items_l.move_to(pc_l)
        self.play(Write(items_l), run_time=1)

        # Right panel: after (title)
        pc_r = panel_r.get_center()
        title_r = Text("── 碰撞后 (弹性) ──", font_size=22, color=WHITE).move_to(pc_r + UP * 0.8)
        self.play(Write(title_r), run_time=0.4)

        self.wait(0.5)

        # ── Phase 1: approach until edges touch ──
        # Move balls to collision point: edges touch at midpoint
        collide_center1 = -r1 - 0.02  # ball1's right edge just left of ball2's left edge
        collide_center2 = r2 + 0.02

        collide_time = min(abs(start1 - collide_center1) / max(abs(v1i), 0.1),
                           abs(start2 - collide_center2) / max(abs(v2i), 0.1),
                           2.0)
        approach_time = max(0.8, collide_time * 0.4)

        if v1i > v2i:
            # Ball1 catches up from left, or they approach each other
            self.play(
                ball1.animate.move_to(x2p(collide_center1)),
                ball2.animate.move_to(x2p(collide_center2)),
                run_time=approach_time,
                rate_func=linear,
            )
        else:
            # Same direction, ball2 ahead. Skip collision approach.
            pass

        # Flash effect at collision
        flash = Circle(radius=0.3, color=YELLOW, fill_opacity=0.9).move_to(
            (x2p(collide_center1) + x2p(collide_center2)) / 2)
        self.play(Flash(flash, color=YELLOW, line_length=0.8, flash_radius=0.6), run_time=0.6)

        # ── Phase 2: after collision ──
        items_r = VGroup()
        for txt, clr in [(f"v1' = {v1f:.2f} m/s", YELLOW),
                          (f"v2' = {v2f:.2f} m/s", YELLOW),
                          (f"p  = {m1*v1f+m2*v2f:.2f}", WHITE),
                          (f"Ek = {0.5*m1*v1f**2+0.5*m2*v2f**2:.1f}", GRAY)]:
            t = Text(txt, font_size=20, color=clr)
            items_r.add(t)
        items_r.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        items_r.move_to(pc_r)
        self.play(Write(items_r), run_time=1)

        # Move apart with clear separation
        r1_data = r1
        r2_data = r2
        sep_after = r1_data + r2_data + 2.0  # generous post-collision separation
        final1 = -sep_after / 2
        final2 = sep_after / 2

        self.play(
            ball1.animate.move_to(x2p(final1)),
            ball2.animate.move_to(x2p(final2)),
            run_time=2.5,
            rate_func=smooth,
        )
        self.wait(2)

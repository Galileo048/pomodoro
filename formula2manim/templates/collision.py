"""
动量守恒（弹性碰撞）| 高中物理
两球碰撞，显示碰撞前后速度变化
"""
from manim import *


class CollisionScene(Scene):
    def construct(self):
        m1 = __PARAM_m1__
        m2 = __PARAM_m2__
        v1i = __PARAM_v1i__
        v2i = __PARAM_v2i__

        # Elastic collision formulas
        v1f = ((m1 - m2) * v1i + 2 * m2 * v2i) / (m1 + m2)
        v2f = (2 * m1 * v1i + (m2 - m1) * v2i) / (m1 + m2)

        # Number line
        total_len = max(abs(v1i), abs(v2i), abs(v1f), abs(v2f)) * 1.5 + 4
        axes = NumberLine(
            x_range=[-total_len / 2, total_len / 2, 1],
            include_numbers=False, length=10,
        )
        self.add(axes)
        self.add(Text("x (m)", font_size=24).next_to(axes.get_end(), DOWN, buff=0.2))

        # Initial positions
        pos1_start = axes.number_to_point(-2)
        pos2_start = axes.number_to_point(2)

        # Balls as circles with radius proportional to mass
        r1 = 0.2 + 0.15 * m1
        r2 = 0.2 + 0.15 * m2
        ball1 = Circle(radius=r1, color=RED, fill_opacity=0.8).move_to(pos1_start)
        ball2 = Circle(radius=r2, color=BLUE, fill_opacity=0.8).move_to(pos2_start)
        self.add(ball1, ball2)
        self.add(Text(f"m1={m1:.1f}", font_size=18, color=RED).next_to(ball1, DOWN, buff=0.2))
        self.add(Text(f"m2={m2:.1f}", font_size=18, color=BLUE).next_to(ball2, DOWN, buff=0.2))

        # Velocity arrows
        def vel_len(v):
            return max(0.05, abs(v) * 0.3)

        arr1 = Arrow(ball1.get_center(), ball1.get_center() + RIGHT * vel_len(v1i) * np.sign(v1i),
                     color=GREEN, buff=0)
        arr2 = Arrow(ball2.get_center(), ball2.get_center() + RIGHT * vel_len(v2i) * np.sign(v2i),
                     color=GREEN, buff=0)
        self.add(arr1, arr2)

        # Info
        v1i_t = Text(f"v1 = {v1i:.1f} m/s", font_size=22, color=GREEN).to_corner(UR, buff=0.3)
        v2i_t = Text(f"v2 = {v2i:.1f} m/s", font_size=22, color=GREEN)
        v2i_t.next_to(v1i_t, DOWN, buff=0.1, aligned_edge=LEFT)
        mom_t = Text(f"p = {m1*v1i+m2*v2i:.1f} kg*m/s", font_size=22, color=WHITE)
        mom_t.next_to(v2i_t, DOWN, buff=0.1, aligned_edge=LEFT)
        self.add(v1i_t, v2i_t, mom_t)

        self.wait(1)

        # Animate collision
        self.play(
            ball1.animate.move_to(axes.number_to_point(0)),
            ball2.animate.move_to(axes.number_to_point(0)),
            run_time=1.5,
        )

        # After collision
        v1f_t = Text(f"v1' = {v1f:.1f} m/s", font_size=22, color=YELLOW)
        v1f_t.next_to(v2i_t, DOWN, buff=0.1, aligned_edge=LEFT)
        v2f_t = Text(f"v2' = {v2f:.1f} m/s", font_size=22, color=YELLOW)
        v2f_t.next_to(v1f_t, DOWN, buff=0.1, aligned_edge=LEFT)
        self.add(v1f_t, v2f_t)

        self.play(
            ball1.animate.move_to(axes.number_to_point(v1f * 0.5)),
            ball2.animate.move_to(axes.number_to_point(v2f * 0.5)),
            run_time=2,
        )
        self.wait(2)

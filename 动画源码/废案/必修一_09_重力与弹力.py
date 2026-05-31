from manim import *
import numpy as np


class GravityElasticForce(Scene):
    """3.1 重力与弹力"""

    def construct(self):
        # ===== 标题 =====
        title = Text("3.1 重力与弹力", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 第一部分：重力 =====
        part1 = Text("重力", font_size=30, color=GREEN)
        part1.to_edge(UP)
        self.play(Write(part1), run_time=0.5)

        # 物体
        box = Rectangle(width=1.5, height=1, color=BLUE, fill_opacity=0.8)
        box.move_to(ORIGIN + UP * 0.5)
        box_label = Text("m", font_size=22, color=WHITE).move_to(box)

        self.play(Create(box), Write(box_label))

        # 重力箭头（动态）
        mass = ValueTracker(1)
        g_val = 9.8

        g_arrow = always_redraw(lambda: Arrow(
            box.get_bottom(),
            box.get_bottom() + DOWN * (mass.get_value() * 0.8),
            color=YELLOW, buff=0, stroke_width=4,
        ))

        g_text = always_redraw(lambda: MathTex(
            f"G = mg = {mass.get_value():.1f} \\times 9.8 = {mass.get_value() * g_val:.1f} N",
            font_size=24, color=YELLOW,
        ).next_to(g_arrow, RIGHT, buff=0.2))

        # 重力加速度
        g_info = MathTex("g = 9.8 m/s^2", font_size=22, color=GRAY)
        g_info.move_to(RIGHT * 3 + UP * 2)

        self.play(GrowArrow(g_arrow), Write(g_text), Write(g_info))

        # 动画：改变质量
        self.play(mass.animate.set_value(2), run_time=1)
        self.play(mass.animate.set_value(0.5), run_time=1)
        self.play(mass.animate.set_value(1.5), run_time=1)

        # 重心
        center_dot = Dot(box.get_center(), color=RED, radius=0.1)
        center_label = Text("重心", font_size=16, color=RED).next_to(center_dot, RIGHT, buff=0.1)

        self.play(Create(center_dot), Write(center_label))
        self.wait(1)

        # ===== 清场 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ===== 第二部分：弹力 =====
        part2 = Text("弹力", font_size=30, color=GREEN)
        part2.to_edge(UP)
        self.play(Write(part2), run_time=0.5)

        # 墙壁
        wall = Rectangle(width=0.3, height=2, color=GRAY, fill_opacity=0.8)
        wall.move_to(LEFT * 4.5)
        self.play(Create(wall))

        # 弹簧（动态）
        spring_start = LEFT * 4.3
        n_coils = 10

        # 初始长度（用x坐标）
        spring_x = ValueTracker(-1)

        spring = always_redraw(lambda: self.create_spring(
            spring_start,
            np.array([spring_x.get_value(), 0, 0]),
            n_coils,
        ))

        # 滑块
        block = always_redraw(lambda: Rectangle(
            width=0.8, height=0.8, color=BLUE, fill_opacity=0.8,
        ).move_to(np.array([spring_x.get_value() + 0.4, 0, 0])))

        # 弹力箭头
        k_val = 50  # 弹簧系数

        force_arrow = always_redraw(lambda: Arrow(
            block.get_center(),
            block.get_center() + LEFT * max(0, (4.3 + spring_x.get_value()) * 0.5),
            color=GREEN, buff=0, stroke_width=3,
        ))

        force_text = always_redraw(lambda: MathTex(
            f"F = kx = {k_val} \\times {max(0, 4.3 + spring_x.get_value()):.1f} = {k_val * max(0, 4.3 + spring_x.get_value()):.0f} N",
            font_size=22, color=GREEN,
        ).next_to(force_arrow, DOWN, buff=0.2))

        # 平衡位置
        eq_line = DashedLine(
            np.array([-1, -1, 0]), np.array([-1, 1.5, 0]),
            color=GRAY, dash_length=0.1,
        )
        eq_label = Text("平衡位置", font_size=16, color=GRAY).next_to(eq_line, DOWN, buff=0.1)

        self.add(spring, block, force_arrow, force_text)
        self.play(Create(eq_line), Write(eq_label))

        # 动画：拉伸弹簧
        self.play(spring_x.animate.set_value(1), run_time=1.5)
        self.play(spring_x.animate.set_value(-3), run_time=1.5)
        self.play(spring_x.animate.set_value(0.5), run_time=1)

        # 胡克定律
        hooke = MathTex("F = kx", font_size=28, color=YELLOW)
        hooke.move_to(RIGHT * 3 + UP * 2)
        self.play(Write(hooke))
        self.wait(1)

        # ===== 总结 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        summary_title = Text("3.1 重力与弹力 - 总结", font_size=36, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            VGroup(
                Text("重力", font_size=24, color=YELLOW),
                Text("：G = mg，方向竖直向下", font_size=24, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("弹力", font_size=24, color=GREEN),
                Text("：F = kx，方向指向恢复原状", font_size=24, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            Text("胡克定律：弹力与形变量成正比", font_size=20, color=GRAY),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def create_spring(self, start, end, n_coils):
        """创建弹簧"""
        points = [start]
        for i in range(n_coils):
            x = start[0] + (i + 0.5) * (end[0] - start[0]) / n_coils
            y = 0.3 if i % 2 == 0 else -0.3
            points.append(np.array([x, y, 0]))
        points.append(end)
        spring = VMobject(color=GREEN, stroke_width=2)
        spring.set_points_as_corners(points)
        return spring

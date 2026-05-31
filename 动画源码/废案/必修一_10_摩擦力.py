from manim import *
import numpy as np


class FrictionForce(Scene):
    """3.2 摩擦力"""

    def construct(self):
        # ===== 标题 =====
        title = Text("3.2 摩擦力", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 第一部分：静摩擦力 =====
        part1 = Text("静摩擦力", font_size=30, color=GREEN)
        part1.to_edge(UP)
        self.play(Write(part1), run_time=0.5)

        # 地面
        ground = Line(LEFT * 5 + DOWN * 1.5, RIGHT * 5 + DOWN * 1.5, color=GRAY, stroke_width=3)
        self.play(Create(ground))

        # 物体
        box = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.8)
        box.move_to(ORIGIN + DOWN * 1.1)
        box_label = Text("m", font_size=18, color=WHITE).move_to(box)

        self.play(Create(box), Write(box_label))

        # 推力（动态）
        push_force = ValueTracker(0)
        max_static = 10  # 最大静摩擦力

        push_arrow = always_redraw(lambda: Arrow(
            box.get_left(),
            box.get_left() + LEFT * (push_force.get_value() * 0.15),
            color=RED, buff=0, stroke_width=3,
        ) if push_force.get_value() > 0 else Line(ORIGIN, ORIGIN, color=RED))

        push_text = always_redraw(lambda: MathTex(
            f"F = {push_force.get_value():.1f} N",
            font_size=20, color=RED,
        ).next_to(push_arrow, LEFT, buff=0.1))

        # 静摩擦力
        static_friction = always_redraw(lambda: Arrow(
            box.get_right(),
            box.get_right() + RIGHT * (min(push_force.get_value(), max_static) * 0.15),
            color=GREEN, buff=0, stroke_width=3,
        ) if push_force.get_value() > 0 else Line(ORIGIN, ORIGIN, color=GREEN))

        static_text = always_redraw(lambda: MathTex(
            f"f = {min(push_force.get_value(), max_static):.1f} N",
            font_size=20, color=GREEN,
        ).next_to(static_friction, RIGHT, buff=0.1))

        self.add(push_arrow, push_text, static_friction, static_text)

        # 动画：逐渐增大推力
        self.play(push_force.animate.set_value(5), run_time=1.5)
        self.play(push_force.animate.set_value(8), run_time=1.5)
        self.play(push_force.animate.set_value(10), run_time=1)

        # 标注最大静摩擦力
        max_text = MathTex("f_{max} = 10 N", font_size=22, color=YELLOW)
        max_text.move_to(RIGHT * 3 + UP * 1)
        self.play(Write(max_text))

        # ===== 第二部分：滑动摩擦力 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        part2 = Text("滑动摩擦力", font_size=30, color=GREEN)
        part2.to_edge(UP)
        self.play(Write(part2), run_time=0.5)

        # 地面
        ground2 = Line(LEFT * 5 + DOWN * 1.5, RIGHT * 5 + DOWN * 1.5, color=GRAY, stroke_width=3)
        self.play(Create(ground2))

        # 物体
        box2 = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.8)
        box2.move_to(LEFT * 3 + DOWN * 1.1)
        box2_label = Text("m", font_size=18, color=WHITE).move_to(box2)

        self.play(Create(box2), Write(box2_label))

        # 推力
        push_arrow2 = Arrow(
            box2.get_left(), box2.get_left() + LEFT * 1.5,
            color=RED, buff=0, stroke_width=3,
        )
        push_text2 = MathTex("F = 15 N", font_size=20, color=RED)
        push_text2.next_to(push_arrow2, LEFT, buff=0.1)

        # 滑动摩擦力
        mu = 0.5  # 摩擦系数
        N = 9.8  # 支持力
        f_sliding = mu * N

        sliding_arrow = Arrow(
            box2.get_right(), box2.get_right() + RIGHT * (f_sliding * 0.15),
            color=GREEN, buff=0, stroke_width=3,
        )
        sliding_text = MathTex(f"f = \\mu N = {mu} \\times {N:.0f} = {f_sliding:.1f} N", font_size=20, color=GREEN)
        sliding_text.next_to(sliding_arrow, RIGHT, buff=0.1)

        self.play(
            GrowArrow(push_arrow2), Write(push_text2),
            GrowArrow(sliding_arrow), Write(sliding_text),
        )

        # 动态：物体滑动
        t_tracker = ValueTracker(0)

        def update_box(mob):
            x = -3 + t_tracker.get_value() * 0.5
            mob.move_to(np.array([x, -1.1, 0]))

        box2.add_updater(update_box)

        # 速度显示
        v_text = always_redraw(lambda: MathTex(
            f"v = {t_tracker.get_value() * 0.5:.1f} m/s",
            font_size=18, color=YELLOW,
        ).next_to(box2, UP, buff=0.2))

        self.add(v_text)
        self.play(t_tracker.animate.set_value(4), run_time=2, rate_func=linear)
        box2.remove_updater(update_box)

        # 公式
        formula = MathTex("f = \\mu N", font_size=28, color=YELLOW)
        formula.move_to(RIGHT * 3 + UP * 1)
        self.play(Write(formula))

        # 摩擦系数说明
        mu_info = VGroup(
            Text("μ：动摩擦因数（与材料和粗糙程度有关）", font_size=18, color=GRAY),
            Text("N：正压力（垂直于接触面的力）", font_size=18, color=GRAY),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        mu_info.move_to(RIGHT * 3 + DOWN * 0.5)
        self.play(Write(mu_info))
        self.wait(1)

        # ===== 总结 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        summary_title = Text("3.2 摩擦力 - 总结", font_size=36, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            VGroup(
                Text("静摩擦力", font_size=22, color=GREEN),
                Text("：0 ≤ f ≤ f_max，与外力平衡", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("滑动摩擦力", font_size=22, color=YELLOW),
                Text("：f = μN，方向与相对运动相反", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("最大静摩擦力", font_size=22, color=RED),
                Text("：略大于滑动摩擦力", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

from manim import *
import numpy as np


class ConcurrentForceEquilibrium(Scene):
    """3.5 共点力的平衡"""

    def construct(self):
        # ===== 标题 =====
        title = Text("3.5 共点力的平衡", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 平衡条件 =====
        condition = Text("平衡条件", font_size=30, color=GREEN)
        condition.to_edge(UP)
        self.play(Write(condition), run_time=0.5)

        # 平衡公式
        eq_formula = MathTex("\\sum \\vec{F} = 0", font_size=48, color=YELLOW)
        eq_formula.move_to(UP * 1)
        self.play(Write(eq_formula))

        # 说明
        explain = VGroup(
            Text("物体处于静止或匀速直线运动状态", font_size=22, color=WHITE),
            Text("合力为零", font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.2)
        explain.move_to(DOWN * 0.5)
        self.play(Write(explain))
        self.wait(1)

        # ===== 三力平衡演示 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        demo_text = Text("三力平衡演示", font_size=30, color=GREEN)
        demo_text.to_edge(UP)
        self.play(Write(demo_text), run_time=0.5)

        # 中心点
        center = Dot(ORIGIN, color=WHITE, radius=0.1)
        self.play(Create(center))

        # 三个力（首尾相接形成闭合三角形）
        # 力1：向上
        F1_arrow = Arrow(ORIGIN, UP * 2, color=RED, buff=0, stroke_width=3)
        F1_label = MathTex("\\vec{F}_1", font_size=20, color=RED)
        F1_label.next_to(F1_arrow, RIGHT, buff=0.1)

        # 力2：向左下
        F2_arrow = Arrow(ORIGIN, LEFT * 1.7 + DOWN * 1, color=GREEN, buff=0, stroke_width=3)
        F2_label = MathTex("\\vec{F}_2", font_size=20, color=GREEN)
        F2_label.next_to(F2_arrow, LEFT, buff=0.1)

        # 力3：向右下
        F3_arrow = Arrow(ORIGIN, RIGHT * 1.7 + DOWN * 1, color=YELLOW, buff=0, stroke_width=3)
        F3_label = MathTex("\\vec{F}_3", font_size=20, color=YELLOW)
        F3_label.next_to(F3_arrow, RIGHT, buff=0.1)

        self.play(
            GrowArrow(F1_arrow), Write(F1_label),
            GrowArrow(F2_arrow), Write(F2_label),
            GrowArrow(F3_arrow), Write(F3_label),
        )

        # 力的三角形（首尾相接）
        triangle = Polygon(
            UP * 2,
            UP * 2 + LEFT * 1.7 + DOWN * 1,
            ORIGIN,
            color=WHITE, stroke_width=2, fill_opacity=0.1,
        )

        # 辅助线
        d1 = DashedLine(UP * 2, UP * 2 + LEFT * 1.7 + DOWN * 1, color=GRAY, dash_length=0.1)
        d2 = DashedLine(UP * 2 + LEFT * 1.7 + DOWN * 1, ORIGIN, color=GRAY, dash_length=0.1)
        d3 = DashedLine(ORIGIN, UP * 2, color=GRAY, dash_length=0.1)

        self.play(Create(triangle), Create(d1), Create(d2), Create(d3))

        # 标注闭合
        closed_text = Text("力的三角形闭合 → 合力为零", font_size=22, color=YELLOW)
        closed_text.move_to(DOWN * 2)
        self.play(Write(closed_text))

        # 动态：改变力的大小
        scale_tracker = ValueTracker(1)

        def update_F1(mob):
            mob.put_start_and_end_on(ORIGIN, UP * 2 * scale_tracker.get_value())

        def update_F2(mob):
            mob.put_start_and_end_on(ORIGIN, (LEFT * 1.7 + DOWN * 1) * scale_tracker.get_value())

        def update_F3(mob):
            mob.put_start_and_end_on(ORIGIN, (RIGHT * 1.7 + DOWN * 1) * scale_tracker.get_value())

        def update_triangle(mob):
            p1 = UP * 2 * scale_tracker.get_value()
            p2 = p1 + (LEFT * 1.7 + DOWN * 1) * scale_tracker.get_value()
            p3 = ORIGIN
            mob.set_points_as_corners([p1, p2, p3, p1])

        F1_arrow.add_updater(update_F1)
        F2_arrow.add_updater(update_F2)
        F3_arrow.add_updater(update_F3)
        triangle.add_updater(update_triangle)

        # 动画
        self.play(scale_tracker.animate.set_value(0.7), run_time=1)
        self.play(scale_tracker.animate.set_value(1.3), run_time=1)
        self.play(scale_tracker.animate.set_value(1), run_time=1)

        F1_arrow.remove_updater(update_F1)
        F2_arrow.remove_updater(update_F2)
        F3_arrow.remove_updater(update_F3)
        triangle.remove_updater(update_triangle)

        self.wait(1)

        # ===== 总结 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        summary_title = Text("3.5 共点力的平衡 - 总结", font_size=36, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            MathTex("\\sum \\vec{F} = 0", font_size=36, color=YELLOW),
            Text("物体处于平衡状态", font_size=22, color=WHITE),
            Text("平衡条件：合力为零", font_size=22, color=WHITE),
            Text("三力平衡：力的三角形闭合", font_size=22, color=GREEN),
            Text("多力平衡：多边形法则", font_size=22, color=GREEN),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

from manim import *
import numpy as np


class ForceCompositionDecomposition(Scene):
    """3.4 力的合成和分解"""

    def construct(self):
        # ===== 标题 =====
        title = Text("3.4 力的合成和分解", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 第一部分：力的合成 =====
        part1 = Text("力的合成 - 平行四边形法则", font_size=30, color=GREEN)
        part1.to_edge(UP)
        self.play(Write(part1), run_time=0.5)

        # 原点
        origin = ORIGIN

        # 力F1
        F1_end = RIGHT * 3 + UP * 1.5
        F1 = Arrow(origin, F1_end, color=GREEN, buff=0, stroke_width=3)
        F1_label = MathTex("\\vec{F}_1", font_size=24, color=GREEN)
        F1_label.next_to(F1, RIGHT, buff=0.1)

        # 力F2
        F2_end = RIGHT * 1.5 + UP * 3
        F2 = Arrow(origin, F2_end, color=YELLOW, buff=0, stroke_width=3)
        F2_label = MathTex("\\vec{F}_2", font_size=24, color=YELLOW)
        F2_label.next_to(F2, UP, buff=0.1)

        self.play(GrowArrow(F1), Write(F1_label))
        self.play(GrowArrow(F2), Write(F2_label))

        # 平行四边形
        parallelogram = Polygon(
            origin, F1_end, F1_end + F2_end, F2_end,
            color=WHITE, stroke_width=2, fill_opacity=0.1,
        )

        # 辅助线
        d1 = DashedLine(F1_end, F1_end + F2_end, color=GRAY, dash_length=0.1)
        d2 = DashedLine(F2_end, F1_end + F2_end, color=GRAY, dash_length=0.1)

        self.play(Create(parallelogram), Create(d1), Create(d2))

        # 合力
        R_end = F1_end + F2_end
        R = Arrow(origin, R_end, color=RED, buff=0, stroke_width=4)
        R_label = MathTex("\\vec{R} = \\vec{F}_1 + \\vec{F}_2", font_size=24, color=RED)
        R_label.next_to(R, RIGHT, buff=0.1)

        self.play(GrowArrow(R), Write(R_label))

        # 动态：改变F1的角度
        angle_tracker = ValueTracker(0)

        def update_F1(mob):
            angle = angle_tracker.get_value()
            new_end = np.array([3 * np.cos(angle), 1.5 + 1.5 * np.sin(angle), 0])
            mob.put_start_and_end_on(origin, new_end)

        def update_F1_label(mob):
            mob.next_to(F1.get_end(), RIGHT, buff=0.1)

        def update_parallelogram(mob):
            F1_new = F1.get_end()
            F2_new = F2.get_end()
            R_new = F1_new + F2_new - origin
            mob.set_points_as_corners([origin, F1_new, R_new, F2_new, origin])

        def update_d1(mob):
            mob.put_start_and_end_on(F1.get_end(), F1.get_end() + F2_end - origin)

        def update_d2(mob):
            mob.put_start_and_end_on(F2.get_end(), F2.get_end() + F1_end - origin)

        def update_R(mob):
            R_new = F1.get_end() + F2.get_end() - origin
            mob.put_start_and_end_on(origin, R_new)

        def update_R_label(mob):
            mob.next_to(R.get_end(), RIGHT, buff=0.1)

        F1.add_updater(update_F1)
        F1_label.add_updater(update_F1_label)
        parallelogram.add_updater(update_parallelogram)
        d1.add_updater(update_d1)
        d2.add_updater(update_d2)
        R.add_updater(update_R)
        R_label.add_updater(update_R_label)

        # 动画
        self.play(angle_tracker.animate.set_value(PI / 4), run_time=2)
        self.play(angle_tracker.animate.set_value(-PI / 6), run_time=2)

        F1.remove_updater(update_F1)
        F1_label.remove_updater(update_F1_label)
        parallelogram.remove_updater(update_parallelogram)
        d1.remove_updater(update_d1)
        d2.remove_updater(update_d2)
        R.remove_updater(update_R)
        R_label.remove_updater(update_R_label)

        self.wait(1)

        # ===== 第二部分：力的分解 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        part2 = Text("力的分解", font_size=30, color=GREEN)
        part2.to_edge(UP)
        self.play(Write(part2), run_time=0.5)

        # 一个力分解为两个分力
        # 原力
        F_arrow = Arrow(ORIGIN, RIGHT * 4 + UP * 2, color=RED, buff=0, stroke_width=4)
        F_label = MathTex("\\vec{F}", font_size=24, color=RED)
        F_label.next_to(F_arrow, RIGHT, buff=0.1)

        self.play(GrowArrow(F_arrow), Write(F_label))

        # 分解方向1（水平）
        F1_arrow = Arrow(ORIGIN, RIGHT * 4, color=GREEN, buff=0, stroke_width=3)
        F1_label2 = MathTex("\\vec{F}_1", font_size=22, color=GREEN)
        F1_label2.next_to(F1_arrow, DOWN, buff=0.1)

        # 分解方向2（竖直）
        F2_arrow = Arrow(ORIGIN, UP * 2, color=YELLOW, buff=0, stroke_width=3)
        F2_label2 = MathTex("\\vec{F}_2", font_size=22, color=YELLOW)
        F2_label2.next_to(F2_arrow, LEFT, buff=0.1)

        # 辅助线
        d1_2 = DashedLine(F1_arrow.get_end(), F_arrow.get_end(), color=GRAY, dash_length=0.1)
        d2_2 = DashedLine(F2_arrow.get_end(), F_arrow.get_end(), color=GRAY, dash_length=0.1)

        self.play(
            GrowArrow(F1_arrow), Write(F1_label2),
            GrowArrow(F2_arrow), Write(F2_label2),
            Create(d1_2), Create(d2_2),
        )

        # 公式
        formula = MathTex("\\vec{F} = \\vec{F}_1 + \\vec{F}_2", font_size=28, color=WHITE)
        formula.move_to(DOWN * 2)
        self.play(Write(formula))

        # 分解方式不唯一
        note = Text("分解方式不唯一，通常按效果分解", font_size=18, color=GRAY)
        note.move_to(DOWN * 2.8)
        self.play(Write(note))
        self.wait(1)

        # ===== 总结 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        summary_title = Text("3.4 力的合成和分解 - 总结", font_size=36, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            Text("合成：平行四边形法则", font_size=22, color=GREEN),
            MathTex("\\vec{R} = \\vec{F}_1 + \\vec{F}_2", font_size=26, color=WHITE),
            Text("分解：合成的逆运算", font_size=22, color=YELLOW),
            MathTex("\\vec{F} = \\vec{F}_1 + \\vec{F}_2", font_size=26, color=WHITE),
            Text("正交分解：将力分解到两个互相垂直的方向", font_size=20, color=GRAY),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

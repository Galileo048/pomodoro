from manim import *
import numpy as np


class NewtonThirdLaw(Scene):
    """3.3 牛顿第三定律"""

    def construct(self):
        # ===== 标题 =====
        title = Text("3.3 牛顿第三定律", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 核心内容 =====
        law_text = Text("作用力与反作用力", font_size=30, color=GREEN)
        law_text.to_edge(UP)
        self.play(Write(law_text), run_time=0.5)

        # 两个物体
        obj_a = Rectangle(width=1.2, height=1, color=BLUE, fill_opacity=0.8)
        obj_a.move_to(LEFT * 2)
        label_a = Text("A", font_size=24, color=WHITE).move_to(obj_a)

        obj_b = Rectangle(width=1.2, height=1, color=RED, fill_opacity=0.8)
        obj_b.move_to(RIGHT * 2)
        label_b = Text("B", font_size=24, color=WHITE).move_to(obj_b)

        self.play(Create(obj_a), Write(label_a), Create(obj_b), Write(label_b))

        # 作用力（A对B）
        force_ab = Arrow(
            obj_a.get_right(), obj_b.get_left(),
            color=GREEN, buff=0.2, stroke_width=4,
        )
        force_ab_text = MathTex("\\vec{F}_{AB}", font_size=24, color=GREEN)
        force_ab_text.next_to(force_ab, UP, buff=0.1)

        # 反作用力（B对A）
        force_ba = Arrow(
            obj_b.get_left(), obj_a.get_right(),
            color=YELLOW, buff=0.2, stroke_width=4,
        )
        force_ba_text = MathTex("\\vec{F}_{BA}", font_size=24, color=YELLOW)
        force_ba_text.next_to(force_ba, DOWN, buff=0.1)

        self.play(
            GrowArrow(force_ab), Write(force_ab_text),
            GrowArrow(force_ba), Write(force_ba_text),
        )

        # 牛顿第三定律公式
        law_formula = MathTex("\\vec{F}_{AB} = -\\vec{F}_{BA}", font_size=32, color=WHITE)
        law_formula.move_to(DOWN * 2)
        self.play(Write(law_formula))

        # 特点说明
        features = VGroup(
            Text("大小相等", font_size=20, color=GREEN),
            Text("方向相反", font_size=20, color=YELLOW),
            Text("作用在不同物体上", font_size=20, color=RED),
            Text("同时产生、同时消失", font_size=20, color=BLUE),
        ).arrange(RIGHT, buff=0.5)
        features.move_to(DOWN * 2.8)

        for f in features:
            self.play(Write(f), run_time=0.5)

        self.wait(1)

        # ===== 碰撞演示 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        collision_text = Text("碰撞演示", font_size=30, color=GREEN)
        collision_text.to_edge(UP)
        self.play(Write(collision_text), run_time=0.5)

        # 两个小球
        ball_a = Circle(radius=0.4, color=BLUE, fill_opacity=0.8)
        ball_a.move_to(LEFT * 3)
        ball_a_label = Text("A", font_size=18, color=WHITE).move_to(ball_a)

        ball_b = Circle(radius=0.4, color=RED, fill_opacity=0.8)
        ball_b.move_to(RIGHT * 3)
        ball_b_label = Text("B", font_size=18, color=WHITE).move_to(ball_b)

        self.play(
            Create(ball_a), Write(ball_a_label),
            Create(ball_b), Write(ball_b_label),
        )

        # 动态参数
        t_tracker = ValueTracker(0)

        # 速度箭头
        v_a_arrow = always_redraw(lambda: Arrow(
            ball_a.get_right(),
            ball_a.get_right() + RIGHT * max(0, 1 - t_tracker.get_value() * 0.5),
            color=GREEN, buff=0, stroke_width=3,
        ) if t_tracker.get_value() < 2 else Line(ORIGIN, ORIGIN, color=GREEN))

        v_b_arrow = always_redraw(lambda: Arrow(
            ball_b.get_left(),
            ball_b.get_left() + LEFT * max(0, 1 - t_tracker.get_value() * 0.5),
            color=YELLOW, buff=0, stroke_width=3,
        ) if t_tracker.get_value() < 2 else Line(ORIGIN, ORIGIN, color=YELLOW))

        # 碰撞后的力
        force_ab_arrow = always_redraw(lambda: Arrow(
            ball_a.get_right(),
            ball_a.get_right() + LEFT * 0.8,
            color=GREEN, buff=0, stroke_width=4,
        ) if t_tracker.get_value() >= 2 else Line(ORIGIN, ORIGIN, color=GREEN))

        force_ba_arrow = always_redraw(lambda: Arrow(
            ball_b.get_left(),
            ball_b.get_left() + RIGHT * 0.8,
            color=YELLOW, buff=0, stroke_width=4,
        ) if t_tracker.get_value() >= 2 else Line(ORIGIN, ORIGIN, color=YELLOW))

        self.add(v_a_arrow, v_b_arrow, force_ab_arrow, force_ba_arrow)

        # 运动动画
        def update_a(mob):
            if t_tracker.get_value() < 2:
                x = -3 + t_tracker.get_value() * 1.5
                mob.move_to(np.array([x, 0, 0]))

        def update_b(mob):
            if t_tracker.get_value() < 2:
                x = 3 - t_tracker.get_value() * 1.5
                mob.move_to(np.array([x, 0, 0]))
            elif t_tracker.get_value() >= 2:
                x = 0 + (t_tracker.get_value() - 2) * 1.5
                mob.move_to(np.array([x, 0, 0]))

        def update_a_label(mob):
            mob.move_to(ball_a.get_center())

        def update_b_label(mob):
            mob.move_to(ball_b.get_center())

        ball_a.add_updater(update_a)
        ball_b.add_updater(update_b)
        ball_a_label.add_updater(update_a_label)
        ball_b_label.add_updater(update_b_label)

        # 动画
        self.play(t_tracker.animate.set_value(2), run_time=1.5, rate_func=linear)

        # 碰撞瞬间
        collision_flash = Circle(radius=0.3, color=WHITE, fill_opacity=0.8)
        collision_flash.move_to(ORIGIN)
        self.play(Create(collision_flash), run_time=0.1)
        self.play(FadeOut(collision_flash), run_time=0.1)

        # 碰撞后显示力
        force_text = MathTex("\\vec{F}_{AB} = -\\vec{F}_{BA}", font_size=28, color=WHITE)
        force_text.move_to(DOWN * 2)
        self.play(Write(force_text))

        # 继续运动
        self.play(t_tracker.animate.set_value(4), run_time=1.5, rate_func=linear)

        ball_a.remove_updater(update_a)
        ball_b.remove_updater(update_b)
        ball_a_label.remove_updater(update_a_label)
        ball_b_label.remove_updater(update_b_label)

        self.wait(1)

        # ===== 总结 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        summary_title = Text("3.3 牛顿第三定律 - 总结", font_size=36, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            Text("两个物体之间的作用力和反作用力", font_size=22, color=WHITE),
            Text("总是大小相等、方向相反、作用在同一直线上", font_size=22, color=WHITE),
            MathTex("\\vec{F}_{AB} = -\\vec{F}_{BA}", font_size=28, color=YELLOW),
            Text("作用力和反作用力同时产生、同时消失", font_size=20, color=GRAY),
            Text("分别作用在两个不同的物体上", font_size=20, color=GRAY),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

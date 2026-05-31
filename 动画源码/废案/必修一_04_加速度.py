from manim import *
import numpy as np


class Acceleration(Scene):
    """1.4 速度变化快慢的描述——加速度"""

    def construct(self):
        # ===== 标题 =====
        title = Text("1.4 速度变化快慢的描述——加速度", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # ===== 加速度定义 =====
        def_label = Text("加速度的定义", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(def_label))

        # 加速度公式
        a_formula = MathTex("a = \\frac{\\Delta v}{\\Delta t}", font_size=36, color=YELLOW)
        a_formula.move_to(UP * 1)
        self.play(Write(a_formula))

        # 单位
        unit = VGroup(
            Text("单位：", font_size=24, color=WHITE),
            MathTex("m/s^2", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.1)
        unit.move_to(UP * 0)
        self.play(Write(unit))

        # 物理意义
        meaning = Text("加速度描述速度变化的快慢", font_size=20, color=RED)
        meaning.move_to(DOWN * 1)
        self.play(Write(meaning))
        self.wait(1)

        # ===== 匀加速运动的v-t图 =====
        self.clear_all()
        title2 = Text("1.4 速度变化快慢的描述——加速度", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=0.5)

        vt_label = Text("匀加速直线运动的v-t图", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(vt_label))

        # 坐标系
        ax = Axes(
            x_range=[0, 6, 1], y_range=[0, 25, 5],
            x_length=7, y_length=4,
            axis_config={"include_numbers": False, "include_tip": True},
        ).shift(DOWN * 0.5)

        x_label = ax.get_x_axis_label("t/s")
        y_label = ax.get_y_axis_label("v/(m/s)")
        self.play(Create(ax), Write(x_label), Write(y_label))

        # v-t图（倾斜直线）
        a_val = 4
        graph = ax.plot(lambda t: a_val * t, x_range=[0, 5.5, 0.01], color=GREEN)
        self.play(Create(graph))

        # 标注斜率=加速度
        slope_label = MathTex("slope = a = 4 m/s^2", font_size=22, color=GREEN)
        slope_label.move_to(ax.c2p(4, 18))
        self.play(Write(slope_label))

        # 公式
        v_formula = MathTex("v = at", font_size=24, color=YELLOW)
        v_formula.move_to(ax.c2p(2, 22))
        self.play(Write(v_formula))

        # 动态点在v-t图上运动
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(t_tracker.get_value(), a_val * t_tracker.get_value()), color=RED, radius=0.08))
        v_line = always_redraw(lambda: DashedLine(
            ax.c2p(t_tracker.get_value(), 0),
            ax.c2p(t_tracker.get_value(), a_val * t_tracker.get_value()),
            color=RED, dash_length=0.1,
        ))
        v_value = always_redraw(lambda: MathTex(
            f"v = {a_val * t_tracker.get_value():.0f} m/s",
            font_size=18, color=RED,
        ).next_to(dot, RIGHT, buff=0.1))

        self.add(dot, v_line, v_value)
        self.play(t_tracker.animate.set_value(4), run_time=3, rate_func=linear)
        self.wait(1)

        # ===== 加速度的方向 =====
        self.clear_all()
        title3 = Text("1.4 速度变化快慢的描述——加速度", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title3), run_time=0.5)

        dir_label = Text("加速度的方向", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(dir_label))

        # 加速运动
        accel_text = Text("加速运动：a与v同向", font_size=20, color=GREEN)
        accel_text.move_to(UP * 1)
        self.play(Write(accel_text))

        # 小球加速运动（带动态参数）
        ground1 = Line(LEFT * 5 + DOWN * 0.3, RIGHT * 5 + DOWN * 0.3, color=GRAY, stroke_width=2)
        self.play(Create(ground1))

        ball1 = Circle(radius=0.2, color=BLUE, fill_opacity=1).move_to(LEFT * 4 + DOWN * 0.1)
        ball1_label = Text("m", font_size=14, color=WHITE).move_to(ball1)
        self.play(Create(ball1), Write(ball1_label))

        # 动态速度箭头
        t_tracker1 = ValueTracker(0)
        a1 = 2  # 加速度

        v_arrow1 = always_redraw(lambda: Arrow(
            ball1.get_center() + RIGHT * 0.25,
            ball1.get_center() + RIGHT * (0.25 + min(t_tracker1.get_value() * a1 * 0.15, 2)),
            color=GREEN, buff=0, stroke_width=3,
        ))
        a_arrow1 = always_redraw(lambda: Arrow(
            ball1.get_center() + RIGHT * 0.25 + UP * 0.5,
            ball1.get_center() + RIGHT * 1.25 + UP * 0.5,
            color=RED, buff=0, stroke_width=3,
        ))
        v_text1 = always_redraw(lambda: MathTex(
            f"v = {t_tracker1.get_value() * a1:.1f} m/s",
            font_size=16, color=GREEN,
        ).next_to(v_arrow1.get_end(), UP, buff=0.1))
        a_text1 = MathTex("a = const.", font_size=16, color=RED).next_to(a_arrow1, UP, buff=0.05)

        self.add(v_arrow1, a_arrow1, v_text1)
        self.play(Write(a_text1))

        # 小球向右加速运动
        def update_ball1(mob):
            t = t_tracker1.get_value()
            x = -4 + 0.5 * a1 * t ** 2
            mob.move_to(np.array([x, -0.1, 0]))
            ball1_label.move_to(mob)

        ball1.add_updater(update_ball1)

        self.play(t_tracker1.animate.set_value(3), run_time=2, rate_func=linear)
        ball1.remove_updater(update_ball1)
        self.wait(0.5)

        # 减速运动
        decel_text = Text("减速运动：a与v反向", font_size=20, color=RED)
        decel_text.move_to(DOWN * 1)
        self.play(Write(decel_text))

        ground2 = Line(LEFT * 5 + DOWN * 1.8, RIGHT * 5 + DOWN * 1.8, color=GRAY, stroke_width=2)
        self.play(Create(ground2))

        ball2 = Circle(radius=0.2, color=BLUE, fill_opacity=1).move_to(LEFT * 4 + DOWN * 1.6)
        ball2_label = Text("m", font_size=14, color=WHITE).move_to(ball2)
        self.play(Create(ball2), Write(ball2_label))

        # 动态速度箭头（减速）
        t_tracker2 = ValueTracker(0)
        v0 = 6  # 初速度
        a2 = -2  # 加速度（负）

        v_arrow2 = always_redraw(lambda: Arrow(
            ball2.get_center() + RIGHT * 0.25,
            ball2.get_center() + RIGHT * (0.25 + max(v0 + a2 * t_tracker2.get_value(), 0) * 0.15),
            color=GREEN, buff=0, stroke_width=3,
        ))
        a_arrow2 = always_redraw(lambda: Arrow(
            ball2.get_center() + RIGHT * 0.25 + UP * 0.5,
            ball2.get_center() + LEFT * 0.75 + UP * 0.5,
            color=RED, buff=0, stroke_width=3,
        ))
        v_text2 = always_redraw(lambda: MathTex(
            f"v = {max(v0 + a2 * t_tracker2.get_value(), 0):.1f} m/s",
            font_size=16, color=GREEN,
        ).next_to(v_arrow2.get_end(), UP, buff=0.1))
        a_text2 = MathTex("a = const.", font_size=16, color=RED).next_to(a_arrow2, UP, buff=0.05)

        self.add(v_arrow2, a_arrow2, v_text2)
        self.play(Write(a_text2))

        # 小球向右减速运动
        def update_ball2(mob):
            t = t_tracker2.get_value()
            x = -4 + v0 * t + 0.5 * a2 * t ** 2
            mob.move_to(np.array([x, -1.6, 0]))
            ball2_label.move_to(mob)

        ball2.add_updater(update_ball2)

        self.play(t_tracker2.animate.set_value(2.5), run_time=2, rate_func=linear)
        ball2.remove_updater(update_ball2)
        self.wait(1)

        # ===== 总结 =====
        self.clear_all()
        summary_title = Text("1.4 速度变化快慢的描述——加速度", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            Text("加速度：速度变化量与时间的比值", font_size=20, color=WHITE),
            Text("公式：a = Δv/Δt", font_size=20, color=GREEN),
            Text("单位：m/s²", font_size=20, color=YELLOW),
            Text("加速运动：a与v同向，v增大", font_size=20, color=GREEN),
            Text("减速运动：a与v反向，v减小", font_size=20, color=RED),
            Text("v-t图的斜率 = 加速度", font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

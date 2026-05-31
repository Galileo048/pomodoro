from manim import *
import numpy as np


class VelocityTimeRelation(Scene):
    """2.2 匀变速直线运动的速度与时间的关系"""

    def construct(self):
        # ===== 标题 =====
        title = Text("2.2 匀变速直线运动的速度与时间的关系", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # ===== 公式推导 =====
        formula_label = Text("速度公式推导", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(formula_label))

        formulas = VGroup(
            MathTex("a = \\frac{v - v_0}{t}", font_size=28, color=WHITE),
            MathTex("v - v_0 = at", font_size=28, color=GREEN),
            MathTex("v = v_0 + at", font_size=36, color=YELLOW),
        ).arrange(DOWN, buff=0.4)
        formulas.move_to(ORIGIN)

        for f in formulas:
            self.play(Write(f), run_time=0.8)

        self.wait(1)

        # ===== v-t图：初速度不为零 =====
        self.clear_all()
        title2 = Text("2.2 匀变速直线运动的速度与时间的关系", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=0.5)

        vt_label = Text("v-t图：初速度不为零的匀加速", font_size=24, color=GREEN).move_to(UP * 2)
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

        # 参数
        v0 = 5
        a_val = 3

        # v-t图
        graph = ax.plot(lambda t: v0 + a_val * t, x_range=[0, 5.5, 0.01], color=GREEN)
        self.play(Create(graph))

        # 初速度标注
        v0_dot = Dot(ax.c2p(0, v0), color=YELLOW, radius=0.08)
        v0_label = MathTex(f"v_0 = {v0} m/s", font_size=20, color=YELLOW)
        v0_label.next_to(v0_dot, LEFT, buff=0.2)
        self.play(Create(v0_dot), Write(v0_label))

        # 斜率=加速度
        slope_label = MathTex(f"slope = a = {a_val} m/s^2", font_size=20, color=GREEN)
        slope_label.move_to(ax.c2p(4, 20))
        self.play(Write(slope_label))

        # 动态点
        t_tracker = ValueTracker(0)
        point = always_redraw(lambda: Dot(
            ax.c2p(t_tracker.get_value(), v0 + a_val * t_tracker.get_value()),
            color=RED, radius=0.08,
        ))
        v_line = always_redraw(lambda: DashedLine(
            ax.c2p(t_tracker.get_value(), 0),
            ax.c2p(t_tracker.get_value(), v0 + a_val * t_tracker.get_value()),
            color=RED, dash_length=0.1,
        ))
        pos_text = always_redraw(lambda: MathTex(
            f"v = {v0} + {a_val} \\times {t_tracker.get_value():.1f} = {v0 + a_val * t_tracker.get_value():.1f} m/s",
            font_size=18, color=RED,
        ).to_edge(DOWN))

        self.add(point, v_line, pos_text)

        # 动画
        self.play(t_tracker.animate.set_value(4), run_time=3, rate_func=linear)
        self.wait(0.5)

        # ===== 总结 =====
        self.clear_all()
        summary_title = Text("2.2 匀变速直线运动的速度与时间的关系", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            Text("速度公式：v = v₀ + at", font_size=24, color=YELLOW),
            Text("v₀：初速度（t=0时的速度）", font_size=20, color=WHITE),
            Text("a：加速度（恒定）", font_size=20, color=GREEN),
            Text("v-t图：倾斜直线", font_size=20, color=BLUE),
            Text("斜率 = 加速度", font_size=20, color=RED),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

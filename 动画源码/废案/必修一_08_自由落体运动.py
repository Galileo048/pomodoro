from manim import *
import numpy as np


class FreeFall(Scene):
    """2.4 自由落体运动"""

    def construct(self):
        # ===== 标题 =====
        title = Text("2.4 自由落体运动", font_size=40, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # ===== 自由落体定义 =====
        def_label = Text("自由落体运动", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(def_label))

        # 条件
        conditions = VGroup(
            Text("条件：初速度为零", font_size=20, color=WHITE),
            Text("只受重力作用", font_size=20, color=WHITE),
            Text("加速度 g = 9.8 m/s²", font_size=20, color=YELLOW),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        conditions.move_to(UP * 0.5)
        self.play(Write(conditions))
        self.wait(1)

        # ===== 小球下落动画 =====
        self.clear_all()
        title2 = Text("2.4 自由落体运动", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=0.5)

        fall_label = Text("小球自由下落", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(fall_label))

        # 地面
        ground = Line(LEFT * 4 + DOWN * 2, RIGHT * 4 + DOWN * 2, color=GRAY, stroke_width=3)
        self.play(Create(ground))

        # 小球
        ball = Circle(radius=0.2, color=RED, fill_opacity=1)
        ball.move_to(UP * 3)
        self.play(Create(ball))

        # 动态参数
        g = 9.8
        t_tracker = ValueTracker(0)

        # 动态显示
        h_text = always_redraw(lambda: MathTex(
            f"h = \\frac{{1}}{{2}}gt^2 = \\frac{{1}}{{2}} \\times 9.8 \\times {t_tracker.get_value():.1f}^2 = {0.5 * g * t_tracker.get_value() ** 2:.1f} m",
            font_size=18, color=YELLOW,
        ).to_edge(DOWN))

        v_text = always_redraw(lambda: MathTex(
            f"v = gt = 9.8 \\times {t_tracker.get_value():.1f} = {g * t_tracker.get_value():.1f} m/s",
            font_size=18, color=GREEN,
        ).next_to(h_text, UP, buff=0.2))

        # 速度箭头（动态）
        v_arrow = always_redraw(lambda: Arrow(
            ball.get_center(),
            ball.get_center() + DOWN * min(g * t_tracker.get_value() * 0.1, 2),
            color=GREEN, buff=0, stroke_width=3,
        ))

        self.add(h_text, v_text, v_arrow)

        # 小球下落
        def update_ball(mob):
            t = t_tracker.get_value()
            y = 3 - 0.5 * g * t ** 2 * 0.3  # 缩放
            if y < -1.8:
                y = -1.8
            mob.move_to(np.array([0, y, 0]))

        ball.add_updater(update_ball)

        self.play(t_tracker.animate.set_value(1.5), run_time=2, rate_func=linear)
        ball.remove_updater(update_ball)

        # 轨迹
        trail = DashedLine(UP * 3, ball.get_center(), color=RED, dash_length=0.1)
        self.play(Create(trail))
        self.wait(0.5)

        # ===== 公式总结 =====
        self.clear_all()
        summary_title = Text("2.4 自由落体运动", font_size=40, color=BLUE).to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            MathTex("v = gt", font_size=28, color=GREEN),
            MathTex("h = \\frac{1}{2}gt^2", font_size=28, color=YELLOW),
            MathTex("v^2 = 2gh", font_size=28, color=RED),
            Text("g = 9.8 m/s²（重力加速度）", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.4)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

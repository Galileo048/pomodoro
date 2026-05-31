from manim import *
import numpy as np


class DisplacementTimeRelation(Scene):
    """2.3 匀变速直线运动的位移与时间的关系"""

    def construct(self):
        # ===== 标题 =====
        title = Text("2.3 匀变速直线运动的位移与时间的关系", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # ===== 面积法推导 =====
        area_label = Text("面积法推导位移公式", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(area_label))

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

        # 动态填充面积
        t_tracker = ValueTracker(0)

        # 面积 = 梯形面积
        area = always_redraw(lambda: Polygon(
            ax.c2p(0, 0),
            ax.c2p(t_tracker.get_value(), 0),
            ax.c2p(t_tracker.get_value(), v0 + a_val * t_tracker.get_value()),
            ax.c2p(0, v0),
            color=[BLUE, GREEN],
            fill_opacity=0.3,
        ))

        # 位移公式
        s_text = always_redraw(lambda: MathTex(
            f"s = v_0 t + \\frac{{1}}{{2}}at^2 = {v0} \\times {t_tracker.get_value():.1f} + \\frac{{1}}{{2}} \\times {a_val} \\times {t_tracker.get_value():.1f}^2 = {v0 * t_tracker.get_value() + 0.5 * a_val * t_tracker.get_value() ** 2:.1f} m",
            font_size=16, color=YELLOW,
        ).to_edge(DOWN))

        self.add(area, s_text)

        # 动画
        self.play(t_tracker.animate.set_value(4), run_time=3, rate_func=linear)
        self.wait(0.5)

        # ===== 公式总结 =====
        self.clear_all()
        title2 = Text("2.3 匀变速直线运动的位移与时间的关系", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=0.5)

        formula_label = Text("位移公式", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(formula_label))

        formulas = VGroup(
            MathTex("s = v_0 t + \\frac{1}{2}at^2", font_size=36, color=YELLOW),
            Text("v₀：初速度", font_size=20, color=WHITE),
            Text("a：加速度", font_size=20, color=GREEN),
            Text("t：时间", font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.3)
        formulas.move_to(ORIGIN)

        for f in formulas:
            self.play(Write(f), run_time=0.6)

        self.wait(1)

        # ===== x-t图 =====
        self.clear_all()
        title3 = Text("2.3 匀变速直线运动的位移与时间的关系", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title3), run_time=0.5)

        xt_label = Text("x-t图：抛物线", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(xt_label))

        # 坐标系
        ax2 = Axes(
            x_range=[0, 6, 1], y_range=[0, 50, 10],
            x_length=7, y_length=4,
            axis_config={"include_numbers": False, "include_tip": True},
        ).shift(DOWN * 0.5)

        x_label2 = ax2.get_x_axis_label("t/s")
        y_label2 = ax2.get_y_axis_label("s/m")
        self.play(Create(ax2), Write(x_label2), Write(y_label2))

        # 参数
        v0 = 5
        a_val = 3

        # x-t曲线（抛物线）
        graph2 = ax2.plot(lambda t: v0 * t + 0.5 * a_val * t ** 2, x_range=[0, 5.5, 0.01], color=BLUE)
        self.play(Create(graph2))

        # 标注
        graph_label = MathTex("s = v_0 t + \\frac{1}{2}at^2", font_size=22, color=BLUE)
        graph_label.move_to(ax2.c2p(4, 40))
        self.play(Write(graph_label))

        # 动态点
        t_tracker2 = ValueTracker(0)
        point = always_redraw(lambda: Dot(
            ax2.c2p(t_tracker2.get_value(), v0 * t_tracker2.get_value() + 0.5 * a_val * t_tracker2.get_value() ** 2),
            color=RED, radius=0.08,
        ))
        pos_text = always_redraw(lambda: MathTex(
            f"t={t_tracker2.get_value():.1f}s, s={v0 * t_tracker2.get_value() + 0.5 * a_val * t_tracker2.get_value() ** 2:.1f}m",
            font_size=18, color=RED,
        ).to_edge(DOWN))

        self.add(point, pos_text)

        # 动画
        self.play(t_tracker2.animate.set_value(4), run_time=3, rate_func=linear)
        self.wait(1)

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

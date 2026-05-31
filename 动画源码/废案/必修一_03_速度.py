from manim import *
import numpy as np


class Velocity(Scene):
    """1.3 位置变化快慢的描述——速度"""

    def construct(self):
        # ===== 标题 =====
        title = Text("1.3 位置变化快慢的描述——速度", font_size=36, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # ===== 速度的定义 =====
        def_label = Text("速度的定义", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(def_label))

        # 速度公式
        v_formula = MathTex("v = \\frac{\\Delta x}{\\Delta t}", font_size=36, color=YELLOW)
        v_formula.move_to(UP * 1)
        self.play(Write(v_formula))

        # 单位
        unit = VGroup(
            Text("单位：", font_size=24, color=WHITE),
            MathTex("m/s", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.1)
        unit.move_to(UP * 0)
        self.play(Write(unit))

        # 矢量性
        vector_note = Text("速度是矢量，方向与运动方向相同", font_size=20, color=RED)
        vector_note.move_to(DOWN * 1)
        self.play(Write(vector_note))
        self.wait(1)

        # ===== 匀速直线运动的v-t图 =====
        self.clear_all()
        title2 = Text("1.3 位置变化快慢的描述——速度", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=0.5)

        vt_label = Text("匀速直线运动的v-t图", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(vt_label))

        # 坐标系
        ax = Axes(
            x_range=[0, 6, 1], y_range=[0, 5, 1],
            x_length=7, y_length=4,
            axis_config={"include_numbers": False, "include_tip": True},
        ).shift(DOWN * 0.5)

        x_label = ax.get_x_axis_label("t/s")
        y_label = ax.get_y_axis_label("v/(m/s)")
        self.play(Create(ax), Write(x_label), Write(y_label))

        # v-t图（水平线）
        v_val = 3
        graph = ax.plot(lambda t: v_val, x_range=[0, 5, 0.01], color=GREEN)
        self.play(Create(graph))

        # 标注速度值
        v_mark = MathTex(f"v = {v_val} m/s", font_size=22, color=GREEN)
        v_mark.move_to(ax.c2p(4, 3.8))
        self.play(Write(v_mark))

        # 动态点在v-t图上运动
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(ax.c2p(t_tracker.get_value(), v_val), color=RED, radius=0.08))
        v_line = always_redraw(lambda: DashedLine(
            ax.c2p(t_tracker.get_value(), 0),
            ax.c2p(t_tracker.get_value(), v_val),
            color=RED, dash_length=0.1,
        ))

        # 面积=位移（动态）
        area = always_redraw(lambda: ax.get_area(
            graph, x_range=[0, t_tracker.get_value()],
            color=[GREEN, BLUE], opacity=0.3,
        ))
        s_text = always_redraw(lambda: MathTex(
            f"s = vt = {v_val} \\times {t_tracker.get_value():.1f} = {v_val * t_tracker.get_value():.1f} m",
            font_size=18, color=YELLOW,
        ).move_to(ax.c2p(2, 1.5)))

        self.add(dot, v_line, area, s_text)

        # 动画
        self.play(t_tracker.animate.set_value(4), run_time=2, rate_func=linear)
        self.wait(0.5)

        # ===== 变速运动的v-t图 =====
        self.clear_all()
        title3 = Text("1.3 位置变化快慢的描述——速度", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(title3), run_time=0.5)

        var_label = Text("变速运动的v-t图", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(var_label))

        # 坐标系
        ax2 = Axes(
            x_range=[0, 6, 1], y_range=[0, 5, 1],
            x_length=7, y_length=4,
            axis_config={"include_numbers": False, "include_tip": True},
        ).shift(DOWN * 0.5)

        x_label2 = ax2.get_x_axis_label("t/s")
        y_label2 = ax2.get_y_axis_label("v/(m/s)")
        self.play(Create(ax2), Write(x_label2), Write(y_label2))

        # 变速v-t图（曲线）
        graph2 = ax2.plot(lambda t: 0.5 * t ** 1.5, x_range=[0, 5.5, 0.01], color=BLUE)
        self.play(Create(graph2))

        # 标注
        graph_label = MathTex("v = f(t)", font_size=22, color=BLUE)
        graph_label.move_to(ax2.c2p(4, 4))
        self.play(Write(graph_label))

        # 动态点在曲线上运动
        t_tracker2 = ValueTracker(0)
        point = always_redraw(lambda: Dot(
            ax2.c2p(t_tracker2.get_value(), 0.5 * t_tracker2.get_value() ** 1.5),
            color=RED, radius=0.08,
        ))
        v_line2 = always_redraw(lambda: DashedLine(
            ax2.c2p(t_tracker2.get_value(), 0),
            ax2.c2p(t_tracker2.get_value(), 0.5 * t_tracker2.get_value() ** 1.5),
            color=RED, dash_length=0.1,
        ))
        pos_text2 = always_redraw(lambda: MathTex(
            f"v = {0.5 * t_tracker2.get_value() ** 1.5:.2f} m/s",
            font_size=18, color=RED,
        ).next_to(point, RIGHT, buff=0.1))

        self.add(point, v_line2, pos_text2)

        # 动画
        self.play(t_tracker2.animate.set_value(4), run_time=2, rate_func=linear)

        # 平均速度
        avg_v = MathTex("\\bar{v} = \\frac{\\Delta x}{\\Delta t}", font_size=22, color=YELLOW)
        avg_v.move_to(DOWN * 2)
        self.play(Write(avg_v))

        # 瞬时速度
        inst_v = MathTex("v = \\lim_{\\Delta t \\to 0} \\frac{\\Delta x}{\\Delta t}", font_size=22, color=RED)
        inst_v.move_to(DOWN * 2.8)
        self.play(Write(inst_v))
        self.wait(1)

        # ===== 总结 =====
        self.clear_all()
        summary_title = Text("1.3 位置变化快慢的描述——速度", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            Text("速度：位移与时间的比值", font_size=20, color=WHITE),
            Text("平均速度：一段时间内的平均快慢", font_size=20, color=GREEN),
            Text("瞬时速度：某一时刻的快慢", font_size=20, color=RED),
            Text("速率：速度的大小（标量）", font_size=20, color=GRAY),
            Text("v-t图：匀速为水平线，变速为曲线", font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.6)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

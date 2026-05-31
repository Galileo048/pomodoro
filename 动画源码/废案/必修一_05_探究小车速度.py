from manim import *
import numpy as np


class ExperimentCarVelocity(Scene):
    """2.1 实验：探究小车速度随时间变化的规律"""

    def construct(self):
        # ===== 标题 =====
        title = Text("2.1 实验：探究小车速度随时间变化的规律", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # ===== 虚拟纸带 =====
        tape_label = Text("虚拟纸带", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(tape_label))

        # 纸带
        tape = Line(LEFT * 5 + UP * 0.5, RIGHT * 5 + UP * 0.5, color=WHITE, stroke_width=2)
        self.play(Create(tape))

        # 纸带上的点（间距逐渐增大 = 加速运动）
        n_points = 12
        x_positions = [0]
        for i in range(1, n_points):
            # 匀加速：x = 0.5 * a * t^2
            x = 0.5 * 0.3 * i ** 2
            x_positions.append(x)

        # 归一化到屏幕宽度
        x_max = x_positions[-1]
        x_screen = [-4.5 + (x / x_max) * 9 for x in x_positions]

        dots = VGroup()
        for i, x in enumerate(x_screen):
            dot = Dot(np.array([x, 0.5, 0]), color=RED, radius=0.06)
            dots.add(dot)

        # 动态显示点间距
        self.play(Create(dots), run_time=1)

        # 标注相邻点间距
        for i in range(len(x_screen) - 1):
            if i % 2 == 0:  # 只标注偶数点
                gap = x_screen[i + 1] - x_screen[i]
                brace = Brace(
                    Line(np.array([x_screen[i], 0.3, 0]), np.array([x_screen[i + 1], 0.3, 0])),
                    direction=DOWN,
                    color=YELLOW,
                )
                gap_text = MathTex(f"\\Delta x_{i + 1}", font_size=14, color=YELLOW)
                gap_text.next_to(brace, DOWN, buff=0.05)
                self.play(Create(brace), Write(gap_text), run_time=0.2)

        # 说明
        note = Text("点间距逐渐增大 → 速度在增加", font_size=18, color=YELLOW)
        note.move_to(DOWN * 0.5)
        self.play(Write(note))
        self.wait(1)

        # ===== 逐差法 =====
        self.clear_all()
        title2 = Text("2.1 实验：探究小车速度随时间变化的规律", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title2), run_time=0.5)

        diff_label = Text("逐差法计算加速度", font_size=24, color=GREEN).move_to(UP * 2)
        self.play(Write(diff_label))

        # 公式推导
        formulas = VGroup(
            MathTex("\\Delta x = aT^2", font_size=28, color=YELLOW),
            MathTex("a = \\frac{\\Delta x}{T^2}", font_size=28, color=GREEN),
            MathTex("a = \\frac{(x_4+x_5+x_6)-(x_1+x_2+x_3)}{9T^2}", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4)
        formulas.move_to(ORIGIN)

        for f in formulas:
            self.play(Write(f), run_time=0.8)

        self.wait(1)

        # ===== v-t图 =====
        self.clear_all()
        title3 = Text("2.1 实验：探究小车速度随时间变化的规律", font_size=32, color=BLUE).to_edge(UP)
        self.play(Write(title3), run_time=0.5)

        vt_label = Text("实验数据 → v-t图", font_size=24, color=GREEN).move_to(UP * 2)
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

        # 实验数据点
        data_points = [(0.5, 1.0), (1.0, 1.8), (1.5, 2.5), (2.0, 3.2), (2.5, 4.0), (3.0, 4.8)]
        dots_data = VGroup()
        for t, v in data_points:
            dot = Dot(ax.c2p(t, v), color=RED, radius=0.08)
            dots_data.add(dot)

        self.play(Create(dots_data), run_time=1)

        # 拟合直线
        fit_line = ax.plot(lambda t: 1.3 * t + 0.3, x_range=[0, 3.5, 0.01], color=GREEN)
        self.play(Create(fit_line))

        # 标注斜率
        slope_label = MathTex("a = 1.3 m/s^2", font_size=22, color=GREEN)
        slope_label.move_to(ax.c2p(2.5, 4.5))
        self.play(Write(slope_label))

        # 动态点
        t_tracker = ValueTracker(0)
        point = always_redraw(lambda: Dot(
            ax.c2p(t_tracker.get_value(), 1.3 * t_tracker.get_value() + 0.3),
            color=YELLOW, radius=0.1,
        ))
        pos_text = always_redraw(lambda: MathTex(
            f"t={t_tracker.get_value():.1f}s, v={1.3 * t_tracker.get_value() + 0.3:.1f}m/s",
            font_size=18, color=YELLOW,
        ).to_edge(DOWN))

        self.add(point, pos_text)
        self.play(t_tracker.animate.set_value(3), run_time=2, rate_func=linear)

        # 结论
        conclusion = Text("v-t图是直线 → 匀加速运动", font_size=20, color=YELLOW)
        conclusion.move_to(DOWN * 2)
        self.play(Write(conclusion))
        self.wait(1)

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

from manim import *
import numpy as np

class TrigFunctions(Scene):
    """三角函数图像 - sin/cos 变换"""

    def construct(self):
        # ========== 第一部分：标题 ==========
        title = Text("三角函数图像", font_size=52, color=BLUE)
        subtitle = Text("Trigonometric Functions", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ========== 第二部分：基本正弦函数 ==========
        t1 = Text("y = sin x", font_size=42, color=YELLOW)
        t1.to_edge(UP)
        self.play(Write(t1), run_time=0.8)

        # 坐标系
        axes = Axes(
            x_range=[-2 * PI, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        )

        # x轴标签（π刻度）
        x_labels = VGroup()
        pi_values = [-2, -1, 1, 2]
        pi_labels = ["-2\\pi", "-\\pi", "\\pi", "2\\pi"]
        for val, label_text in zip(pi_values, pi_labels):
            label = MathTex(label_text, font_size=18)
            label.next_to(axes.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels.add(label)

        y_label = axes.get_y_axis_label("y", direction=UP)

        self.play(Create(axes), Write(x_labels), Write(y_label), run_time=1)

        # 正弦曲线
        sine_graph = axes.plot(
            lambda x: np.sin(x),
            x_range=[-2 * PI, 2 * PI, 0.01],
            color=YELLOW,
        )
        sine_label = MathTex("y = \\sin x", font_size=24, color=YELLOW)
        sine_label.next_to(axes.c2p(PI / 2, 1), UR, buff=0.2)

        self.play(Create(sine_graph), Write(sine_label), run_time=2)
        self.wait(1)

        # 标注关键点
        key_points = [
            (0, 0, "(0, 0)"),
            (PI / 2, 1, "(\\pi/2, 1)"),
            (PI, 0, "(\\pi, 0)"),
            (3 * PI / 2, -1, "(3\\pi/2, -1)"),
            (2 * PI, 0, "(2\\pi, 0)"),
        ]

        dots = VGroup()
        point_labels = VGroup()
        for x_val, y_val, label_text in key_points:
            dot = Dot(axes.c2p(x_val, y_val), color=RED, radius=0.06)
            label = MathTex(label_text, font_size=16, color=RED)
            label.next_to(dot, UP, buff=0.1)
            dots.add(dot)
            point_labels.add(label)

        self.play(Create(dots), Write(point_labels), run_time=1.5)
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第三部分：振幅变换 ==========
        t2 = Text("振幅变换：y = A sin x", font_size=38, color=BLUE)
        t2.to_edge(UP)
        self.play(Write(t2), run_time=0.8)

        axes2 = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        )

        x_labels2 = VGroup()
        for val, label_text in zip(pi_values, pi_labels):
            label = MathTex(label_text, font_size=18)
            label.next_to(axes2.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels2.add(label)

        self.play(Create(axes2), Write(x_labels2), run_time=1)

        # 不同振幅的正弦曲线
        amplitudes = [0.5, 1, 2]
        colors = [GREEN, YELLOW, RED]
        A_values = ["0.5", "1", "2"]

        graphs = []
        labels = []

        for A, color, A_str in zip(amplitudes, colors, A_values):
            graph = axes2.plot(
                lambda x, a=A: a * np.sin(x),
                x_range=[-2 * PI, 2 * PI, 0.01],
                color=color,
            )
            label = MathTex(f"A = {A_str}", font_size=20, color=color)
            graphs.append(graph)
            labels.append(label)

        # 标签位置
        labels[0].move_to(axes2.c2p(PI / 2, 0.8))
        labels[1].move_to(axes2.c2p(PI / 2, 1.5))
        labels[2].move_to(axes2.c2p(PI / 2, 2.5))

        # 动画：依次显示
        for graph, label in zip(graphs, labels):
            self.play(Create(graph), Write(label), run_time=1)

        # 标注振幅
        amp_line = DashedLine(
            axes2.c2p(0, 0),
            axes2.c2p(0, 2),
            color=RED,
            dash_length=0.1,
        )
        amp_label = MathTex("A = 2", font_size=22, color=RED)
        amp_label.next_to(amp_line, RIGHT, buff=0.1)

        self.play(Create(amp_line), Write(amp_label))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第四部分：周期变换 ==========
        t3 = Text("周期变换：y = sin ωx", font_size=38, color=BLUE)
        t3.to_edge(UP)
        self.play(Write(t3), run_time=0.8)

        axes3 = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        )

        x_labels3 = VGroup()
        for val, label_text in zip(pi_values, pi_labels):
            label = MathTex(label_text, font_size=18)
            label.next_to(axes3.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels3.add(label)

        self.play(Create(axes3), Write(x_labels3), run_time=1)

        # 不同频率的正弦曲线
        omegas = [0.5, 1, 2]
        colors3 = [GREEN, YELLOW, PURPLE]
        omega_labels = ["0.5", "1", "2"]

        graphs3 = []
        labels3 = []

        for omega, color, omega_str in zip(omegas, colors3, omega_labels):
            graph = axes3.plot(
                lambda x, w=omega: np.sin(w * x),
                x_range=[-2 * PI, 2 * PI, 0.01],
                color=color,
            )
            label = MathTex(f"\\omega = {omega_str}", font_size=20, color=color)
            graphs3.append(graph)
            labels3.append(label)

        # 标签位置
        labels3[0].move_to(axes3.c2p(PI, 1.2))
        labels3[1].move_to(axes3.c2p(PI / 2, 1.2))
        labels3[2].move_to(axes3.c2p(PI / 4, 1.2))

        # 动画
        for graph, label in zip(graphs3, labels3):
            self.play(Create(graph), Write(label), run_time=1)

        # 标注周期
        period_line = DashedLine(
            axes3.c2p(0, -1.3),
            axes3.c2p(2 * PI, -1.3),
            color=PURPLE,
            dash_length=0.1,
        )
        period_label = MathTex("T = 2\\pi", font_size=22, color=PURPLE)
        period_label.next_to(period_line, DOWN, buff=0.1)

        self.play(Create(period_line), Write(period_label))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第五部分：相位变换 ==========
        t4 = Text("相位变换：y = sin(x + φ)", font_size=38, color=BLUE)
        t4.to_edge(UP)
        self.play(Write(t4), run_time=0.8)

        axes4 = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        )

        x_labels4 = VGroup()
        for val, label_text in zip(pi_values, pi_labels):
            label = MathTex(label_text, font_size=18)
            label.next_to(axes4.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels4.add(label)

        self.play(Create(axes4), Write(x_labels4), run_time=1)

        # 基准线 y = sin x
        base_graph = axes4.plot(
            lambda x: np.sin(x),
            x_range=[-2 * PI, 2 * PI, 0.01],
            color=YELLOW,
        )
        base_label = MathTex("y = \\sin x", font_size=20, color=YELLOW)
        base_label.move_to(axes4.c2p(PI / 2, 1.2))

        self.play(Create(base_graph), Write(base_label), run_time=1)

        # 相位偏移的正弦曲线
        phase_shifts = [PI / 4, PI / 2, PI]
        colors4 = [GREEN, RED, PURPLE]
        phase_labels = ["\\pi/4", "\\pi/2", "\\pi"]

        graphs4 = []
        labels4 = []

        for phi, color, phi_str in zip(phase_shifts, colors4, phase_labels):
            graph = axes4.plot(
                lambda x, p=phi: np.sin(x + p),
                x_range=[-2 * PI, 2 * PI, 0.01],
                color=color,
            )
            label = MathTex(f"\\varphi = {phi_str}", font_size=20, color=color)
            graphs4.append(graph)
            labels4.append(label)

        # 标签位置
        labels4[0].move_to(axes4.c2p(-PI / 4, 1.2))
        labels4[1].move_to(axes4.c2p(-PI / 2, 1.2))
        labels4[2].move_to(axes4.c2p(-PI, 1.2))

        # 动画
        for graph, label in zip(graphs4, labels4):
            self.play(Create(graph), Write(label), run_time=1)

        # 标注相位偏移
        shift_arrow = Arrow(
            axes4.c2p(0, -1.3),
            axes4.c2p(-PI / 2, -1.3),
            color=RED,
            buff=0,
        )
        shift_label = MathTex("\\Delta x = -\\frac{\\pi}{2}", font_size=22, color=RED)
        shift_label.next_to(shift_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(shift_arrow), Write(shift_label))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第六部分：综合变换 ==========
        t5 = Text("综合变换：y = A sin(ωx + φ) + k", font_size=36, color=BLUE)
        t5.to_edge(UP)
        self.play(Write(t5), run_time=0.8)

        axes5 = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-2, 4, 1],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        ).shift(DOWN * 0.5)

        x_labels5 = VGroup()
        for val, label_text in zip(pi_values, pi_labels):
            label = MathTex(label_text, font_size=18)
            label.next_to(axes5.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels5.add(label)

        self.play(Create(axes5), Write(x_labels5), run_time=1)

        # 综合变换曲线
        A, omega, phi, k = 1.5, 2, PI / 4, 1

        # 分步显示参数
        param_text = VGroup(
            MathTex(f"A = {A}", font_size=22, color=GREEN),
            MathTex(f"\\omega = {omega}", font_size=22, color=YELLOW),
            MathTex(f"\\varphi = \\frac{{\\pi}}{{4}}", font_size=22, color=RED),
            MathTex(f"k = {k}", font_size=22, color=PURPLE),
        ).arrange(RIGHT, buff=0.5)
        param_text.move_to(RIGHT * 3 + UP * 2.5)

        for param in param_text:
            self.play(Write(param), run_time=0.5)

        # 绘制曲线
        final_graph = axes5.plot(
            lambda x: A * np.sin(omega * x + phi) + k,
            x_range=[-2 * PI, 2 * PI, 0.01],
            color=WHITE,
        )
        final_label = MathTex(
            f"y = {A}\\sin({omega}x + \\frac{{\\pi}}{{4}}) + {k}",
            font_size=24,
            color=WHITE,
        )
        final_label.move_to(axes5.c2p(PI / 2, 3.5))

        self.play(Create(final_graph), Write(final_label), run_time=2)

        # 标注振幅和中线
        midline = DashedLine(
            axes5.c2p(-2 * PI, k),
            axes5.c2p(2 * PI, k),
            color=PURPLE,
            dash_length=0.1,
        )
        midline_label = MathTex("y = k = 1", font_size=18, color=PURPLE)
        midline_label.next_to(axes5.c2p(2 * PI, k), UP, buff=0.1)

        amp_line2 = DashedLine(
            axes5.c2p(0, k),
            axes5.c2p(0, k + A),
            color=GREEN,
            dash_length=0.1,
        )
        amp_label2 = MathTex("A = 1.5", font_size=18, color=GREEN)
        amp_label2.next_to(amp_line2, RIGHT, buff=0.1)

        self.play(
            Create(midline), Write(midline_label),
            Create(amp_line2), Write(amp_label2),
        )
        self.wait(3)

        # ========== 第七部分：cos函数 ==========
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        t6 = Text("cos 函数与 sin 函数的关系", font_size=38, color=BLUE)
        t6.to_edge(UP)
        self.play(Write(t6), run_time=0.8)

        axes6 = Axes(
            x_range=[-2 * PI, 2 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        )

        x_labels6 = VGroup()
        for val, label_text in zip(pi_values, pi_labels):
            label = MathTex(label_text, font_size=18)
            label.next_to(axes6.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels6.add(label)

        self.play(Create(axes6), Write(x_labels6), run_time=1)

        # sin曲线
        sin_graph = axes6.plot(
            lambda x: np.sin(x),
            x_range=[-2 * PI, 2 * PI, 0.01],
            color=YELLOW,
        )
        sin_label = MathTex("y = \\sin x", font_size=22, color=YELLOW)
        sin_label.move_to(axes6.c2p(PI / 2, 1.2))

        # cos曲线
        cos_graph = axes6.plot(
            lambda x: np.cos(x),
            x_range=[-2 * PI, 2 * PI, 0.01],
            color=BLUE,
        )
        cos_label = MathTex("y = \\cos x", font_size=22, color=BLUE)
        cos_label.move_to(axes6.c2p(0, 1.2))

        self.play(Create(sin_graph), Write(sin_label), run_time=1.5)
        self.play(Create(cos_graph), Write(cos_label), run_time=1.5)

        # 标注相位差
        shift_arrow2 = Arrow(
            axes6.c2p(0, -1.3),
            axes6.c2p(PI / 2, -1.3),
            color=RED,
            buff=0,
        )
        shift_label2 = MathTex("\\frac{\\pi}{2}", font_size=22, color=RED)
        shift_label2.next_to(shift_arrow2, DOWN, buff=0.1)

        relation = MathTex(
            "\\cos x = \\sin(x + \\frac{\\pi}{2})",
            font_size=24,
            color=RED,
        )
        relation.move_to(RIGHT * 3 + UP * 2.5)

        self.play(GrowArrow(shift_arrow2), Write(shift_label2))
        self.play(Write(relation))
        self.wait(3)

        # 结束
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        summary = VGroup(
            Text("三角函数变换总结", font_size=36, color=BLUE),
            MathTex("y = A\\sin(\\omega x + \\varphi) + k", font_size=30, color=WHITE),
            VGroup(
                Text("A → 振幅", font_size=22, color=GREEN),
                Text("ω → 周期", font_size=22, color=YELLOW),
                Text("φ → 相位", font_size=22, color=RED),
                Text("k → 上下平移", font_size=22, color=PURPLE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2),
        ).arrange(DOWN, buff=0.4)
        summary.move_to(ORIGIN)

        for mob in summary:
            self.play(Write(mob), run_time=0.8)

        self.wait(3)
        self.play(FadeOut(summary))

from manim import *
import numpy as np

class SimpleHarmonicMotion(Scene):
    """简谐振动 - 弹簧振子与图像分析"""

    def construct(self):
        # ========== 第一部分：标题 ==========
        title = Text("简谐振动", font_size=52, color=BLUE)
        subtitle = Text("Simple Harmonic Motion", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ========== 第二部分：弹簧振子动画 ==========
        t1 = Text("弹簧振子", font_size=42, color=BLUE)
        t1.to_edge(UP)
        self.play(Write(t1), run_time=0.8)

        # 墙壁
        wall = Rectangle(
            width=0.3,
            height=2,
            color=GRAY,
            fill_opacity=0.8,
        ).move_to(LEFT * 5.5)

        # 弹簧（用锯齿线表示）
        spring_start = LEFT * 5.3
        spring_end = LEFT * 2
        n_coils = 8
        coil_width = 0.3
        spring_points = [spring_start]
        for i in range(n_coils):
            x = spring_start[0] + (i + 0.5) * (spring_end[0] - spring_start[0]) / n_coils
            y_offset = coil_width if i % 2 == 0 else -coil_width
            spring_points.append(np.array([x, y_offset, 0]))
        spring_points.append(spring_end)

        spring = VMobject(color=GREEN, stroke_width=3)
        spring.set_points_as_corners(spring_points)

        # 滑块（质量块）
        block = Rectangle(
            width=0.8,
            height=0.8,
            color=BLUE,
            fill_opacity=0.8,
        ).move_to(spring_end + RIGHT * 0.4)

        # 平衡位置标记
        eq_line = DashedLine(
            LEFT * 2 + UP * 1.5,
            LEFT * 2 + DOWN * 1.5,
            color=GRAY,
            dash_length=0.1,
        )
        eq_label = Text("平衡位置", font_size=18, color=GRAY)
        eq_label.next_to(eq_line, UP, buff=0.1)

        # 位移箭头
        disp_arrow = Arrow(
            LEFT * 2,
            LEFT * 1,
            color=YELLOW,
            buff=0,
        )
        disp_label = MathTex("x", font_size=24, color=YELLOW)
        disp_label.next_to(disp_arrow, UP, buff=0.1)

        # 参数显示
        params = VGroup(
            MathTex("T = 2\\pi\\sqrt{\\frac{m}{k}}", font_size=22, color=WHITE),
            MathTex("f = \\frac{1}{T}", font_size=22, color=WHITE),
            MathTex("\\omega = \\frac{2\\pi}{T}", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        params.move_to(RIGHT * 3.5 + UP * 1)

        # 组装
        self.play(
            Create(wall),
            Create(spring),
            Create(block),
            Create(eq_line),
            Write(eq_label),
            Write(params),
        )
        self.wait(0.5)

        # ========== 弹簧振子运动动画 ==========
        A = 2  # 振幅
        omega = 2  # 角频率
        t = 0
        dt = 0.03
        center_x = -2  # 平衡位置x坐标

        current_block = block
        current_spring = spring

        while t < 2 * PI / omega:
            t += dt

            # 位移
            x_disp = A * np.sin(omega * t)
            block_x = center_x + x_disp * 0.8  # 缩放

            # 新滑块位置
            new_block = Rectangle(
                width=0.8,
                height=0.8,
                color=BLUE,
                fill_opacity=0.8,
            ).move_to(np.array([block_x + 0.4, 0, 0]))

            # 新弹簧
            new_spring_end = np.array([block_x - 0.4, 0, 0])
            new_spring_points = [spring_start]
            for i in range(n_coils):
                x = spring_start[0] + (i + 0.5) * (new_spring_end[0] - spring_start[0]) / n_coils
                y_offset = coil_width if i % 2 == 0 else -coil_width
                new_spring_points.append(np.array([x, y_offset, 0]))
            new_spring_points.append(new_spring_end)

            new_spring = VMobject(color=GREEN, stroke_width=3)
            new_spring.set_points_as_corners(new_spring_points)

            # 位移箭头
            if abs(x_disp) > 0.1:
                new_disp_arrow = Arrow(
                    np.array([center_x, 0, 0]),
                    np.array([block_x, 0, 0]),
                    color=YELLOW,
                    buff=0,
                )
            else:
                new_disp_arrow = Arrow(
                    np.array([center_x, 0, 0]),
                    np.array([center_x + 0.01, 0, 0]),
                    color=YELLOW,
                    buff=0,
                )

            self.play(
                ReplacementTransform(current_block, new_block),
                ReplacementTransform(current_spring, new_spring),
                ReplacementTransform(disp_arrow, new_disp_arrow),
                run_time=dt * 2,
                rate_func=linear,
            )

            current_block = new_block
            current_spring = new_spring
            disp_arrow = new_disp_arrow

        self.wait(1)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第三部分：位移-时间图像 ==========
        t2 = Text("位移-时间图像", font_size=40, color=BLUE)
        t2.to_edge(UP)
        self.play(Write(t2), run_time=0.8)

        axes = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        ).shift(DOWN * 0.3)

        # x轴标签（π刻度）
        x_labels = VGroup()
        pi_vals = [1, 2]
        pi_texts = ["\\pi", "2\\pi"]
        for val, text in zip(pi_vals, pi_texts):
            label = MathTex(text, font_size=18)
            label.next_to(axes.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels.add(label)

        # 原点标签
        zero_label = MathTex("0", font_size=18)
        zero_label.next_to(axes.c2p(0, 0), DOWN + LEFT, buff=0.1)
        x_labels.add(zero_label)

        t_label = axes.get_x_axis_label("t", direction=RIGHT)
        x_label = axes.get_y_axis_label("x", direction=UP)

        self.play(Create(axes), Write(x_labels), Write(t_label), Write(x_label), run_time=1)

        # 位移曲线
        A_val = 1
        omega_val = 1
        x_graph = axes.plot(
            lambda t: A_val * np.sin(omega_val * t),
            x_range=[0, 2 * PI, 0.01],
            color=YELLOW,
        )
        x_label_graph = MathTex("x = A\\sin(\\omega t)", font_size=24, color=YELLOW)
        x_label_graph.move_to(axes.c2p(PI / 2, 1.3))

        self.play(Create(x_graph), Write(x_label_graph), run_time=2)

        # 标注振幅
        amp_line = DashedLine(
            axes.c2p(0, A_val),
            axes.c2p(2 * PI, A_val),
            color=RED,
            dash_length=0.1,
        )
        amp_label = MathTex("A", font_size=22, color=RED)
        amp_label.next_to(axes.c2p(2 * PI, A_val), UP, buff=0.1)

        amp_line_neg = DashedLine(
            axes.c2p(0, -A_val),
            axes.c2p(2 * PI, -A_val),
            color=RED,
            dash_length=0.1,
        )

        self.play(
            Create(amp_line), Create(amp_line_neg), Write(amp_label),
        )

        # 标注周期
        period_arrow = Arrow(
            axes.c2p(0, -1.3),
            axes.c2p(2 * PI, -1.3),
            color=PURPLE,
            buff=0,
        )
        period_label = MathTex("T", font_size=22, color=PURPLE)
        period_label.next_to(period_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(period_arrow), Write(period_label))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第四部分：速度-时间图像 ==========
        t3 = Text("速度-时间图像", font_size=40, color=BLUE)
        t3.to_edge(UP)
        self.play(Write(t3), run_time=0.8)

        axes2 = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        ).shift(DOWN * 0.3)

        x_labels2 = VGroup()
        for val, text in zip(pi_vals, pi_texts):
            label = MathTex(text, font_size=18)
            label.next_to(axes2.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels2.add(label)
        zero_label2 = MathTex("0", font_size=18)
        zero_label2.next_to(axes2.c2p(0, 0), DOWN + LEFT, buff=0.1)
        x_labels2.add(zero_label2)

        t_label2 = axes2.get_x_axis_label("t", direction=RIGHT)
        v_label = axes2.get_y_axis_label("v", direction=UP)

        self.play(Create(axes2), Write(x_labels2), Write(t_label2), Write(v_label), run_time=1)

        # 速度曲线（余弦）
        v_graph = axes2.plot(
            lambda t: A_val * omega_val * np.cos(omega_val * t),
            x_range=[0, 2 * PI, 0.01],
            color=GREEN,
        )
        v_label_graph = MathTex("v = A\\omega\\cos(\\omega t)", font_size=24, color=GREEN)
        v_label_graph.move_to(axes2.c2p(PI / 4, 1.3))

        self.play(Create(v_graph), Write(v_label_graph), run_time=2)

        # 标注最大速度
        v_max_label = MathTex("v_{max} = A\\omega", font_size=20, color=GREEN)
        v_max_label.move_to(axes2.c2p(PI * 1.5, 1.3))

        self.play(Write(v_max_label))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第五部分：加速度-时间图像 ==========
        t4 = Text("加速度-时间图像", font_size=40, color=BLUE)
        t4.to_edge(UP)
        self.play(Write(t4), run_time=0.8)

        axes3 = Axes(
            x_range=[0, 2 * PI + 0.5, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": False,
                "font_size": 18,
                "include_tip": True,
            },
        ).shift(DOWN * 0.3)

        x_labels3 = VGroup()
        for val, text in zip(pi_vals, pi_texts):
            label = MathTex(text, font_size=18)
            label.next_to(axes3.c2p(val * PI, 0), DOWN, buff=0.15)
            x_labels3.add(label)
        zero_label3 = MathTex("0", font_size=18)
        zero_label3.next_to(axes3.c2p(0, 0), DOWN + LEFT, buff=0.1)
        x_labels3.add(zero_label3)

        t_label3 = axes3.get_x_axis_label("t", direction=RIGHT)
        a_label = axes3.get_y_axis_label("a", direction=UP)

        self.play(Create(axes3), Write(x_labels3), Write(t_label3), Write(a_label), run_time=1)

        # 加速度曲线（负正弦）
        a_graph = axes3.plot(
            lambda t: -A_val * omega_val ** 2 * np.sin(omega_val * t),
            x_range=[0, 2 * PI, 0.01],
            color=RED,
        )
        a_label_graph = MathTex("a = -A\\omega^2\\sin(\\omega t)", font_size=24, color=RED)
        a_label_graph.move_to(axes3.c2p(PI / 2, -1.3))

        self.play(Create(a_graph), Write(a_label_graph), run_time=2)

        # 标注关系
        relation = MathTex("a = -\\omega^2 x", font_size=22, color=RED)
        relation.move_to(axes3.c2p(PI * 1.5, -1.3))

        self.play(Write(relation))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第六部分：三图对比 ==========
        t5 = Text("x-v-a 对比", font_size=40, color=BLUE)
        t5.to_edge(UP)
        self.play(Write(t5), run_time=0.8)

        # 三个小坐标系
        small_axes = []
        graphs = []
        colors = [YELLOW, GREEN, RED]
        labels_text = ["x = A\\sin(\\omega t)", "v = A\\omega\\cos(\\omega t)", "a = -A\\omega^2\\sin(\\omega t)"]
        y_labels_text = ["x", "v", "a"]

        for i in range(3):
            ax = Axes(
                x_range=[0, 2 * PI, PI],
                y_range=[-1.2, 1.2, 0.5],
                x_length=3,
                y_length=2.5,
                axis_config={
                    "include_numbers": False,
                    "include_tip": True,
                    "font_size": 14,
                },
            )
            ax.move_to(np.array([-4 + i * 4, 0, 0]))
            small_axes.append(ax)

            # 曲线
            if i == 0:  # sin
                graph = ax.plot(
                    lambda t: np.sin(t),
                    x_range=[0, 2 * PI, 0.01],
                    color=colors[i],
                )
            elif i == 1:  # cos
                graph = ax.plot(
                    lambda t: np.cos(t),
                    x_range=[0, 2 * PI, 0.01],
                    color=colors[i],
                )
            else:  # -sin
                graph = ax.plot(
                    lambda t: -np.sin(t),
                    x_range=[0, 2 * PI, 0.01],
                    color=colors[i],
                )
            graphs.append(graph)

        # 标签
        title_labels = VGroup()
        for i, (label_text, y_label_text) in enumerate(zip(labels_text, y_labels_text)):
            label = MathTex(label_text, font_size=18, color=colors[i])
            label.move_to(np.array([-4 + i * 4, 2, 0]))
            title_labels.add(label)

            y_lab = MathTex(y_label_text, font_size=18, color=colors[i])
            y_lab.next_to(small_axes[i].get_y_axis(), LEFT, buff=0.1)

        # 动画
        for i in range(3):
            self.play(
                Create(small_axes[i]),
                Create(graphs[i]),
                Write(title_labels[i]),
                run_time=1,
            )

        # 相位关系
        phase_text = VGroup(
            Text("相位关系：", font_size=22, color=WHITE),
            VGroup(
                MathTex("v", font_size=20, color=GREEN),
                Text(" 超前 ", font_size=18, color=WHITE),
                MathTex("x", font_size=20, color=YELLOW),
                MathTex("\\frac{\\pi}{2}", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                MathTex("a", font_size=20, color=RED),
                Text(" 超前 ", font_size=18, color=WHITE),
                MathTex("v", font_size=20, color=GREEN),
                MathTex("\\frac{\\pi}{2}", font_size=20, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        phase_text.move_to(DOWN * 2.5)

        for mob in phase_text:
            self.play(Write(mob), run_time=0.5)

        self.wait(3)

        # ========== 第七部分：能量守恒 ==========
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        t6 = Text("能量守恒", font_size=40, color=BLUE)
        t6.to_edge(UP)
        self.play(Write(t6), run_time=0.8)

        # 能量公式
        energy_formulas = VGroup(
            MathTex("E_k = \\frac{1}{2}mv^2", font_size=28, color=GREEN),
            MathTex("E_p = \\frac{1}{2}kx^2", font_size=28, color=YELLOW),
            MathTex("E = E_k + E_p = \\frac{1}{2}kA^2", font_size=28, color=RED),
        ).arrange(DOWN, buff=0.4)
        energy_formulas.move_to(UP * 1)

        for formula in energy_formulas:
            self.play(Write(formula), run_time=0.8)

        # 能量柱状图
        bar_group = VGroup()
        n_bars = 20
        for i in range(n_bars):
            t_val = i * 2 * PI / n_bars
            x_val = np.sin(t_val)
            v_val = np.cos(t_val)

            ke = 0.5 * v_val ** 2  # 动能
            pe = 0.5 * x_val ** 2  # 势能

            ke_bar = Rectangle(
                width=0.3,
                height=ke * 2,
                color=GREEN,
                fill_opacity=0.8,
            )
            pe_bar = Rectangle(
                width=0.3,
                height=pe * 2,
                color=YELLOW,
                fill_opacity=0.8,
            )

            ke_bar.move_to(np.array([-5 + i * 0.5, -2 + ke, 0]))
            pe_bar.next_to(ke_bar, UP, buff=0)

            bar_group.add(ke_bar, pe_bar)

        # 图例
        legend = VGroup(
            VGroup(
                Rectangle(width=0.3, height=0.3, color=GREEN, fill_opacity=0.8),
                Text("动能", font_size=18, color=GREEN),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Rectangle(width=0.3, height=0.3, color=YELLOW, fill_opacity=0.8),
                Text("势能", font_size=18, color=YELLOW),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(RIGHT, buff=0.5)
        legend.move_to(DOWN * 3)

        self.play(Create(bar_group), Write(legend), run_time=2)

        # 总能量线
        total_line = DashedLine(
            np.array([-5.5, -1, 0]),
            np.array([5.5, -1, 0]),
            color=RED,
            dash_length=0.1,
        )
        total_label = MathTex("E = \\frac{1}{2}kA^2 = \\text{const.}", font_size=22, color=RED)
        total_label.next_to(total_line, UP, buff=0.1)

        self.play(Create(total_line), Write(total_label))
        self.wait(3)

        # ========== 结束 ==========
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        summary = VGroup(
            Text("简谐振动总结", font_size=36, color=BLUE),
            MathTex("x = A\\sin(\\omega t + \\varphi)", font_size=28, color=YELLOW),
            MathTex("v = A\\omega\\cos(\\omega t + \\varphi)", font_size=28, color=GREEN),
            MathTex("a = -A\\omega^2\\sin(\\omega t + \\varphi)", font_size=28, color=RED),
            MathTex("T = 2\\pi\\sqrt{\\frac{m}{k}}", font_size=28, color=WHITE),
        ).arrange(DOWN, buff=0.3)
        summary.move_to(ORIGIN)

        for mob in summary:
            self.play(Write(mob), run_time=0.8)

        self.wait(3)
        self.play(FadeOut(summary))

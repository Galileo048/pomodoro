from manim import *
import numpy as np


class TimeDisplacement(Scene):
    """1.2 时间 位移 - 全新重写"""

    def construct(self):
        # ===== 标题 =====
        title = Text("1.2 时间 位移", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 第一部分：时刻与时间间隔 =====
        part1 = Text("时刻与时间间隔", font_size=30, color=GREEN)
        part1.to_edge(UP)
        self.play(Write(part1), run_time=0.5)

        # 时间轴
        timeline = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            include_numbers=True,
            font_size=22,
            color=WHITE,
        ).shift(DOWN * 0.5)

        t_ax_label = MathTex("t/s", font_size=20, color=GRAY).next_to(timeline.get_end(), RIGHT, buff=0.1)
        self.play(Create(timeline), Write(t_ax_label))

        # 时刻点（动态）
        t1 = ValueTracker(2)
        t2 = ValueTracker(7)

        # 时刻1
        dot1 = always_redraw(lambda: Dot(timeline.number_to_point(t1.get_value()), color=RED, radius=0.12))
        label1 = always_redraw(lambda: VGroup(
            Text("t₁ =", font_size=18, color=RED),
            MathTex(f"{t1.get_value():.0f}", font_size=18, color=RED),
            Text("s", font_size=18, color=RED),
        ).arrange(RIGHT, buff=0.05).next_to(dot1, UP, buff=0.25))

        # 时刻2
        dot2 = always_redraw(lambda: Dot(timeline.number_to_point(t2.get_value()), color=BLUE, radius=0.12))
        label2 = always_redraw(lambda: VGroup(
            Text("t₂ =", font_size=18, color=BLUE),
            MathTex(f"{t2.get_value():.0f}", font_size=18, color=BLUE),
            Text("s", font_size=18, color=BLUE),
        ).arrange(RIGHT, buff=0.05).next_to(dot2, UP, buff=0.25))

        # 时间间隔箭头
        interval = always_redraw(lambda: Arrow(
            timeline.number_to_point(t1.get_value()),
            timeline.number_to_point(t2.get_value()),
            color=YELLOW, buff=0, stroke_width=4,
        ))

        # 时间间隔文字
        interval_text = always_redraw(lambda: VGroup(
            Text("Δt =", font_size=22, color=YELLOW),
            MathTex(f"{t2.get_value() - t1.get_value():.0f}", font_size=22, color=YELLOW),
            Text("s", font_size=22, color=YELLOW),
        ).arrange(RIGHT, buff=0.1).next_to(interval, UP, buff=0.2))

        self.add(dot1, label1, dot2, label2, interval, interval_text)

        # 动画：改变时刻
        self.play(t1.animate.set_value(3), run_time=1)
        self.play(t2.animate.set_value(8), run_time=1)

        # 标注
        note1 = Text("时刻：一个瞬间（时间轴上的点）", font_size=18, color=RED)
        note1.move_to(DOWN * 1.8)
        note2 = Text("时间间隔：一个过程（两点之间的距离）", font_size=18, color=YELLOW)
        note2.move_to(DOWN * 2.3)
        self.play(Write(note1), Write(note2))
        self.wait(1)

        # ===== 清场 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ===== 第二部分：位移与路程 =====
        part2 = Text("位移与路程", font_size=30, color=GREEN)
        part2.to_edge(UP)
        self.play(Write(part2), run_time=0.5)

        # 曲线路径
        path_points = [
            LEFT * 4 + DOWN * 1,
            LEFT * 2 + UP * 0.5,
            RIGHT * 0.5 + DOWN * 0.8,
            RIGHT * 2.5 + UP * 0.3,
            RIGHT * 4 + DOWN * 1,
        ]
        path = VMobject(color=GRAY, stroke_width=3)
        path.set_points_smoothly(path_points)

        # 起点A
        A = Dot(path_points[0], color=GREEN, radius=0.15)
        A_label = Text("A", font_size=22, color=GREEN).next_to(A, DOWN, buff=0.15)

        # 终点B
        B = Dot(path_points[-1], color=RED, radius=0.15)
        B_label = Text("B", font_size=22, color=RED).next_to(B, DOWN, buff=0.15)

        self.play(Create(path), Create(A), Create(B))
        self.play(Write(A_label), Write(B_label))

        # 位移箭头（直线）
        displacement = Arrow(path_points[0], path_points[-1], color=YELLOW, buff=0, stroke_width=4)
        disp_label = Text("位移", font_size=20, color=YELLOW)
        disp_label.next_to(displacement.get_center(), UP, buff=0.15)

        self.play(GrowArrow(displacement), Write(disp_label))

        # 动态小球
        ball = Dot(path_points[0], color=BLUE, radius=0.12)
        self.add(ball)

        # 动态参数
        progress = ValueTracker(0)

        # 小球沿路径运动
        def update_ball(mob):
            p = min(progress.get_value() / 10, 1)
            mob.move_to(path.point_from_proportion(p))

        ball.add_updater(update_ball)

        # 动态路程显示
        path_len = always_redraw(lambda: Text(
            f"路程 = {progress.get_value():.1f}",
            font_size=20, color=GRAY,
        ).move_to(LEFT * 3 + UP * 2))

        # 动态位移大小显示
        disp_size = always_redraw(lambda: Text(
            f"位移大小 = {np.linalg.norm(path.point_from_proportion(min(progress.get_value() / 10, 1)) - path_points[0]):.1f}",
            font_size=20, color=YELLOW,
        ).move_to(RIGHT * 2 + UP * 2))

        self.add(path_len, disp_size)

        # 动画：小球运动
        self.play(progress.animate.set_value(10), run_time=3, rate_func=linear)
        ball.remove_updater(update_ball)

        # 路径标注
        path_label = Text("路程：轨迹的长度（标量）", font_size=18, color=GRAY)
        path_label.move_to(DOWN * 2)
        disp_formula = MathTex("\\vec{s} = \\vec{r}_B - \\vec{r}_A", font_size=24, color=YELLOW)
        disp_formula.move_to(DOWN * 2.8)
        self.play(Write(path_label), Write(disp_formula))
        self.wait(1)

        # ===== 清场 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ===== 第三部分：x-t图 =====
        part3 = Text("位移-时间图像", font_size=30, color=GREEN)
        part3.to_edge(UP)
        self.play(Write(part3), run_time=0.5)

        # 坐标系
        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=7,
            y_length=4,
            axis_config={"include_numbers": False, "include_tip": True},
        ).shift(DOWN * 0.3)

        x_label = ax.get_x_axis_label("t/s", direction=RIGHT)
        y_label = ax.get_y_axis_label("x/m", direction=UP)
        self.play(Create(ax), Write(x_label), Write(y_label))

        # 曲线
        graph = ax.plot(lambda t: 0.8 * t ** 1.5, x_range=[0, 5.5, 0.01], color=BLUE)
        self.play(Create(graph))

        # 动态点
        t = ValueTracker(0)

        # 动态点
        point = always_redraw(lambda: Dot(
            ax.c2p(t.get_value(), 0.8 * t.get_value() ** 1.5),
            color=RED, radius=0.1,
        ))

        # 辅助线
        v_line = always_redraw(lambda: DashedLine(
            ax.c2p(t.get_value(), 0),
            ax.c2p(t.get_value(), 0.8 * t.get_value() ** 1.5),
            color=RED, dash_length=0.1,
        ))
        h_line = always_redraw(lambda: DashedLine(
            ax.c2p(0, 0.8 * t.get_value() ** 1.5),
            ax.c2p(t.get_value(), 0.8 * t.get_value() ** 1.5),
            color=RED, dash_length=0.1,
        ))

        # 动态坐标显示
        coord_text = always_redraw(lambda: VGroup(
            MathTex("t =", font_size=20, color=RED),
            MathTex(f"{t.get_value():.1f}", font_size=20, color=RED),
            MathTex("s,", font_size=20, color=RED),
            MathTex("x =", font_size=20, color=RED),
            MathTex(f"{0.8 * t.get_value() ** 1.5:.1f}", font_size=20, color=RED),
            MathTex("m", font_size=20, color=RED),
        ).arrange(RIGHT, buff=0.08).to_edge(DOWN))

        self.add(point, v_line, h_line, coord_text)

        # 动画
        self.play(t.animate.set_value(4.5), run_time=3, rate_func=linear)
        self.wait(1)

        # ===== 总结 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        summary_title = Text("1.2 时间 位移 - 总结", font_size=36, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.5)

        summary = VGroup(
            VGroup(
                Text("时刻", font_size=22, color=RED),
                Text("：时间轴上的一个点", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("时间间隔", font_size=22, color=YELLOW),
                Text("：两个时刻之间的间隔", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("位移", font_size=22, color=GREEN),
                Text("：从起点到终点的有向线段（矢量）", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("路程", font_size=22, color=GRAY),
                Text("：运动轨迹的长度（标量）", font_size=22, color=WHITE),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.8)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

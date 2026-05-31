"""
第1期：什么是导数？（切线斜率的动画）
时长：约6分钟 | 11镜
知识点：导数的几何意义与定义
v3: 3b1b风格 — ValueTracker平滑动画 + 实时信息面板
"""
from manim import *
import numpy as np

# 3b1b 配色
BG = "#1C1C1C"
BLUE = "#58C4DD"
GREEN = "#83C167"
YELLOW = "#FFFF00"
RED = "#FF6666"
WHITE = "#FFFFFF"
GRAY = "#888888"
DARK_GRAY = "#444444"

CN = "Microsoft YaHei"


class DerivativeScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ================================================================
        # 镜01：标题 (0-15s)
        # ================================================================
        title = Text("什么是导数？", font=CN, font_size=52, color=WHITE)
        subtitle = Text("从割线到切线的旅程", font=CN, font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title, run_time=2))
        self.play(FadeIn(subtitle, shift=UP * 0.2, run_time=1))
        self.wait(2.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ================================================================
        # 镜02-03：坐标系 + 抛物线 (15-60s)
        # ================================================================
        axes = Axes(
            x_range=[-0.5, 4, 1],
            y_range=[-1, 13, 2],
            x_length=7,
            y_length=5.5,
            axis_config={"include_tip": True, "color": GRAY, "stroke_width": 1.5},
            tips=True,
        )
        x_label = MathTex("x", color=GRAY).scale(0.7).next_to(axes.x_axis.get_end(), DR, buff=0.15)
        y_label = MathTex("y", color=GRAY).scale(0.7).next_to(axes.y_axis.get_end(), LEFT, buff=0.15)

        # 手动刻度
        tick_group = VGroup()
        for x in range(1, 4):
            tick = Text(str(x), font_size=16, color=GRAY)
            tick.next_to(axes.c2p(x, 0), DOWN, buff=0.1)
            tick_group.add(tick)
        for y in [2, 4, 6, 8, 10, 12]:
            tick = Text(str(y), font_size=16, color=GRAY)
            tick.next_to(axes.c2p(0, y), LEFT, buff=0.1)
            tick_group.add(tick)

        self.play(Create(axes, run_time=1.5))
        self.play(FadeIn(x_label), FadeIn(y_label), FadeIn(tick_group), run_time=0.5)
        self.wait(0.5)

        # 函数曲线
        def f(x):
            return x ** 2

        curve = axes.plot(f, color=BLUE, stroke_width=3)
        curve_label = MathTex("y = x^2", color=BLUE).scale(0.75)
        curve_label.next_to(axes.c2p(3, 9), UR, buff=0.15)

        self.play(Create(curve, run_time=2))
        self.play(FadeIn(curve_label, run_time=0.8))
        self.wait(1)

        # ================================================================
        # 镜04-06：固定P点 + 割线 + 斜率计算 (60-160s)
        # ================================================================
        a = 1.0  # P点x坐标

        # 固定点 P
        P = Dot(axes.c2p(a, f(a)), color=YELLOW, radius=0.1)
        P_label = MathTex("P", color=YELLOW).scale(0.75).next_to(P, DL, buff=0.12)
        self.play(FadeIn(P, scale=0.5, run_time=0.5))
        self.play(FadeIn(P_label, run_time=0.3))
        self.wait(1)

        # ValueTracker 控制 Q 的位置
        h_tracker = ValueTracker(2.0)

        # 动点 Q — y方向偏移0.15，不贴在曲线上
        def q_pos():
            x = a + h_tracker.get_value()
            return axes.c2p(x, f(x) + 0.15)

        Q_dot = always_redraw(lambda: Dot(q_pos(), color=RED, radius=0.12))
        Q_glow = always_redraw(lambda: Dot(q_pos(), color=RED, radius=0.25, fill_opacity=0.2, stroke_width=0))
        Q = VGroup(Q_glow, Q_dot)

        Q_label = always_redraw(lambda: MathTex("Q", color=RED).scale(0.8).next_to(
            q_pos(), UR, buff=0.2
        ))

        # 动态割线（连到曲线上的真实位置，不是偏移后的Q）
        secant = always_redraw(lambda: Line(
            axes.c2p(a, f(a)),
            axes.c2p(a + h_tracker.get_value(), f(a + h_tracker.get_value())),
            color=GREEN, stroke_width=2.5,
        ))

        # Q 出场时闪烁一下，和曲线区分开
        self.play(FadeIn(Q, scale=1.5, run_time=0.3))
        self.play(Q_dot.animate.set_fill(WHITE, opacity=1), run_time=0.15)
        self.play(Q_dot.animate.set_fill(RED, opacity=1), run_time=0.15)
        self.play(FadeIn(Q_label, run_time=0.3))
        self.play(Create(secant, run_time=1))
        self.wait(1)

        # ── 右上角信息面板（3b1b 标志性元素）──
        # 半透明薄底板，不抢眼
        panel = Rectangle(
            width=4.0, height=3.0,
            fill_color=BG, fill_opacity=0.6,
            stroke_color=DARK_GRAY, stroke_width=0.8, stroke_opacity=0.4,
        )
        panel.to_corner(UR, buff=0.25)

        # 三行文字，用 VGroup 统一定位，行间距 0.55
        dx_label = Text("Δx =", font_size=22, color=WHITE)
        dx_num = always_redraw(lambda: Text(
            f"{h_tracker.get_value():.4f}", font_size=22, color=YELLOW
        ).next_to(dx_label, RIGHT, buff=0.2))

        dy_label = Text("Δy =", font_size=22, color=WHITE)
        dy_num = always_redraw(lambda: Text(
            f"{f(a + h_tracker.get_value()) - f(a):.4f}", font_size=22, color=YELLOW
        ).next_to(dy_label, RIGHT, buff=0.2))

        slope_label = Text("Δy/Δx =", font_size=22, color=WHITE)
        slope_num = always_redraw(lambda: Text(
            f"{(f(a + h_tracker.get_value()) - f(a)) / h_tracker.get_value():.4f}",
            font_size=22, color=GREEN,
        ).next_to(slope_label, RIGHT, buff=0.2))

        # 每行：标签 + 数值 左对齐
        row1 = VGroup(dx_label, dx_num).arrange(RIGHT, buff=0.2)
        row2 = VGroup(dy_label, dy_num).arrange(RIGHT, buff=0.2)
        row3 = VGroup(slope_label, slope_num).arrange(RIGHT, buff=0.2)

        # 三行纵向排列，左对齐
        rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        rows.move_to(panel.get_center() + UP * 0.15)

        slope_num = always_redraw(lambda: Text(
            f"{(f(a + h_tracker.get_value()) - f(a)) / h_tracker.get_value():.4f}",
            font_size=22, color=GREEN,
        ).next_to(slope_label, RIGHT, buff=0.15))

        limit_text = Text("→ f'(1) = 2", font_size=18, color=RED)
        limit_text.next_to(rows, DOWN, buff=0.25)

        # 也放进一个 VGroup 方便整体管理
        panel_content = VGroup(rows, limit_text)
        panel_content.move_to(panel.get_center())

        self.play(FadeIn(panel), run_time=0.5)
        self.play(FadeIn(panel_content, run_time=0.8))
        self.wait(1.5)

        # ================================================================
        # 镜07-08：Q 向 P 平滑移动 (160-240s)
        # ================================================================
        # 3b1b 核心：ValueTracker 平滑动画，信息面板实时更新
        self.play(
            h_tracker.animate.set_value(0.02),
            run_time=8,
            rate_func=smooth,
        )
        self.wait(1)

        # 高亮最终斜率
        slope_box = SurroundingRectangle(
            row3, color=GREEN, buff=0.1,
        )
        self.play(Create(slope_box, run_time=0.5))
        self.wait(2)

        # ================================================================
        # 镜09：切线从P点向两侧生长出来 (240-280s)
        # ================================================================
        tangent = axes.plot(
            lambda x: 2 * (x - a) + f(a),
            color=RED, stroke_width=2.5,
            x_range=[-0.2, 3.5],
        )
        tangent_label = Text("切线: y = 2x - 1", font=CN, font_size=22, color=RED)
        tangent_label.next_to(limit_text, DOWN, buff=0.15)

        # 从 P 点位置向两侧展开，而不是突然出现
        self.play(GrowFromPoint(tangent, point=axes.c2p(a, f(a)), run_time=2))
        self.play(FadeIn(tangent_label, shift=LEFT * 0.3, run_time=0.8))
        self.wait(2.5)

        # ================================================================
        # 镜10：导数定义公式 (280-330s)
        # ================================================================
        # 清除所有图形元素
        self.play(
            *[FadeOut(m) for m in [
                axes, x_label, y_label, tick_group,
                curve, curve_label,
                P, P_label, Q, Q_label, secant, tangent,
                panel, panel_content, tangent_label, slope_box,
            ]],
            run_time=0.8,
        )

        definition = MathTex(
            "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
            color=WHITE,
        ).scale(0.95)

        def_box = SurroundingRectangle(definition, color=BLUE, buff=0.3, stroke_width=2)

        geom = VGroup(
            Text("几何意义：", font=CN, font_size=26, color=YELLOW),
            Text("割线斜率的极限 = 切线斜率", font=CN, font_size=26, color=WHITE),
        ).arrange(RIGHT, buff=0.25)
        geom.next_to(def_box, DOWN, buff=0.5)

        self.play(FadeIn(definition, scale=0.85, run_time=1.5))
        self.play(Create(def_box, run_time=1))
        self.play(FadeIn(geom, shift=UP * 0.2, run_time=1))
        self.wait(3)

        # ================================================================
        # 镜11：用定义验证 y=x² (330-360s)
        # ================================================================
        self.play(FadeOut(definition), FadeOut(def_box), FadeOut(geom), run_time=0.5)

        steps = VGroup(
            MathTex("f(x) = x^2"),
            MathTex("f(x+h) = (x+h)^2 = x^2 + 2xh + h^2"),
            MathTex("f(x+h) - f(x) = 2xh + h^2"),
            MathTex("\\frac{f(x+h) - f(x)}{h} = 2x + h"),
            MathTex("f'(x) = \\lim_{h \\to 0}(2x + h) = 2x"),
        ).scale(0.65)
        steps.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        steps.move_to(ORIGIN)

        for i, step in enumerate(steps):
            color = GREEN if i == len(steps) - 1 else WHITE
            step.set_color(color)
            num = Text(f"({i+1})", font_size=18, color=GRAY)
            num.next_to(step, LEFT, buff=0.25)
            self.play(FadeIn(num, run_time=0.2), FadeIn(step, shift=RIGHT * 0.2, run_time=0.6))
            self.wait(0.5)

        result_box = SurroundingRectangle(steps[-1], color=YELLOW, buff=0.12, stroke_width=2)
        self.play(Create(result_box, run_time=0.5))
        self.wait(3)

        # ================================================================
        # 结尾
        # ================================================================
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)

        end = VGroup(
            Text("导数 = 切线斜率 = 瞬时变化率", font=CN, font_size=36, color=BLUE),
        )
        self.play(FadeIn(end, shift=UP * 0.3, run_time=1.5))
        self.wait(3)
        self.play(FadeOut(end, run_time=1))

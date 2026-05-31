"""
第4期：梯度下降如何找到最低点？
时长：约7分钟 | 11镜
知识点：梯度下降算法 | 难度：⭐⭐⭐⭐
讲解重点：从一维到二维的梯度下降，学习率选择，局部/全局最小值

分两个场景：
- GradientDescent2D：镜01-06, 09, 11（2D部分）
- GradientDescent3D：镜07-08, 10（3D部分）
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
ORANGE = "#FF8C42"
PURPLE = "#bc8cff"

CN = "Microsoft YaHei"


# ================================================================
# 2D 场景：镜01-06, 09, 11
# ================================================================
class GradientDescent2D(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── 镜01：标题 ──
        title = Text("梯度下降如何找到最低点？", font=CN, font_size=40, color=WHITE)
        subtitle = Text("机器学习优化的核心算法", font=CN, font_size=22, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title, run_time=2))
        self.play(FadeIn(subtitle, shift=UP*0.2, run_time=1))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ── 镜02：抛物线 y=(x-2)²+1 ──
        axes = Axes(
            x_range=[-0.5, 4, 1], y_range=[-0.5, 6, 1],
            x_length=7, y_length=4.5,
            axis_config={"include_tip": True, "color": GRAY, "stroke_width": 1.5},
        ).shift(DOWN*0.3)

        def f(x):
            return (x - 2)**2 + 1

        curve = axes.plot(f, color=BLUE, stroke_width=3)
        curve_label = MathTex("y = (x-2)^2 + 1", color=BLUE).scale(0.7)
        curve_label.next_to(axes.c2p(4, 10), UR, buff=0.1)

        # 最低点
        min_dot = Dot(axes.c2p(2, 1), color=RED, radius=0.1)
        min_label = Text("最低点 (2,1)", font=CN, font_size=18, color=RED)
        min_label.next_to(min_dot, DOWN, buff=0.15)

        self.play(Create(axes, run_time=1))
        self.play(Create(curve, run_time=2))
        self.play(FadeIn(curve_label, run_time=0.5))
        self.play(FadeIn(min_dot), FadeIn(min_label), run_time=0.8)
        self.wait(2)

        # ── 镜03：球在 x=0 处，计算导数 ──
        ball = Dot(axes.c2p(0, f(0)), color=YELLOW, radius=0.12)
        ball_label = Text("起点 x=0", font=CN, font_size=16, color=YELLOW)
        ball_label.next_to(ball, UP, buff=0.15)

        # 切线（导数 = 2(x-2)，在 x=0 处 = -4）
        tangent = DashedLine(
            axes.c2p(-0.5, f(0) + (-4)*(-0.5)),
            axes.c2p(0.5, f(0) + (-4)*(0.5)),
            color=GREEN, stroke_width=2, dash_length=0.08,
        )
        slope_text = MathTex("f'(0) = -4", color=GREEN).scale(0.65)
        slope_text.next_to(tangent, UP, buff=0.15)

        self.play(FadeIn(ball), FadeIn(ball_label), run_time=0.5)
        self.play(Create(tangent), FadeIn(slope_text), run_time=1)
        self.wait(1.5)

        # ── 镜04：负梯度方向移动 ──
        # 梯度箭头（向上，正方向）
        grad_arrow = Arrow(
            axes.c2p(0, f(0)), axes.c2p(0, f(0)+2),
            color=RED, stroke_width=2, buff=0,
        )
        grad_label = Text("梯度", font=CN, font_size=16, color=RED)
        grad_label.next_to(grad_arrow, RIGHT, buff=0.1)

        # 负梯度箭头（向下，下降方向）
        neg_arrow = Arrow(
            axes.c2p(0, f(0)), axes.c2p(0.4, f(0.4)),
            color=GREEN, stroke_width=2, buff=0,
        )
        neg_label = Text("负梯度（下降方向）", font=CN, font_size=16, color=GREEN)
        neg_label.next_to(neg_arrow, DOWN, buff=0.1)

        self.play(GrowArrow(grad_arrow), FadeIn(grad_label), run_time=0.8)
        self.play(GrowArrow(neg_arrow), FadeIn(neg_label), run_time=0.8)
        self.wait(1)

        # 公式
        formula = MathTex("x_{new} = x - \\alpha \\cdot f'(x)", color=YELLOW).scale(0.65)
        formula.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(formula, shift=UP*0.2, run_time=0.8))
        self.wait(1.5)

        # 清除辅助元素
        self.play(
            FadeOut(tangent), FadeOut(slope_text),
            FadeOut(grad_arrow), FadeOut(grad_label),
            FadeOut(neg_arrow), FadeOut(neg_label),
            FadeOut(formula), FadeOut(ball_label),
            run_time=0.5,
        )

        # ── 镜05-06：迭代过程 ──
        alpha = 0.3  # 学习率
        x = 0.0
        path_dots = [Dot(axes.c2p(x, f(x)), color=YELLOW, radius=0.08)]

        # 迭代 20 步
        for i in range(20):
            grad = 2 * (x - 2)
            x_new = x - alpha * grad
            new_dot = Dot(axes.c2p(x_new, f(x_new)), color=YELLOW, radius=0.08)
            path_dots.append(new_dot)
            x = x_new

        # 连线路径
        path_lines = VGroup()
        for i in range(len(path_dots)-1):
            line = Line(
                path_dots[i].get_center(), path_dots[i+1].get_center(),
                color=YELLOW, stroke_width=1.5, stroke_opacity=0.6,
            )
            path_lines.add(line)

        # 动画：球一步步跳到最低点
        self.play(FadeOut(ball), run_time=0.3)

        for i in range(1, min(8, len(path_dots))):
            self.play(
                FadeIn(path_dots[i], scale=0.5),
                Create(path_lines[i-1]),
                run_time=0.4,
            )

        # 快速播放剩余步骤
        for i in range(8, len(path_dots)):
            self.play(
                FadeIn(path_dots[i], scale=0.5),
                Create(path_lines[i-1]),
                run_time=0.15,
        )

        # 最终球在最低点
        final_ball = Dot(axes.c2p(2, f(2)), color=YELLOW, radius=0.12)
        converge_text = Text("收敛到最低点!", font=CN, font_size=20, color=GREEN)
        converge_text.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(final_ball), FadeIn(converge_text), run_time=0.8)
        self.wait(2)

        # 清场
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜09：学习率对比（分屏）──
        def make_lr_scene(lr, label_text, color, pos):
            """创建一个学习率对比小场景"""
            ax = Axes(
                x_range=[-1, 5, 1], y_range=[-1, 8, 1],
                x_length=3.5, y_length=3,
                axis_config={"stroke_width": 1, "color": DARK_GRAY},
            )
            c = ax.plot(lambda x: (x-2)**2 + 1, color=BLUE, stroke_width=2)

            # 迭代路径
            x_val = 0.0
            dots = [Dot(ax.c2p(x_val, (x_val-2)**2+1), color=color, radius=0.06)]
            for _ in range(15):
                grad = 2 * (x_val - 2)
                x_val = x_val - lr * grad
                dots.append(Dot(ax.c2p(x_val, (x_val-2)**2+1), color=color, radius=0.06))

            lbl = Text(label_text, font=CN, font_size=18, color=color)
            lbl.next_to(ax, DOWN, buff=0.15)

            lr_text = MathTex(f"\\alpha = {lr}", color=color).scale(0.5)
            lr_text.next_to(lbl, DOWN, buff=0.1)

            return VGroup(ax, c, VGroup(*dots), lbl, lr_text)

        s_left = make_lr_scene(1.2, "学习率太大：震荡!", RED, LEFT*4)
        s_mid = make_lr_scene(0.3, "学习率合适：收敛", GREEN, ORIGIN)
        s_right = make_lr_scene(0.05, "学习率太小：极慢", ORANGE, RIGHT*4)

        all_lr = VGroup(s_left, s_mid, s_right).arrange(RIGHT, buff=0.5)
        all_lr.move_to(ORIGIN)

        lr_title = Text("学习率的选择至关重要", font=CN, font_size=28, color=YELLOW)
        lr_title.to_edge(UP, buff=0.3)

        self.play(FadeIn(lr_title, run_time=0.5))
        self.play(
            FadeIn(s_left, shift=UP*0.3, run_time=0.8),
            FadeIn(s_mid, shift=UP*0.3, run_time=0.8),
            FadeIn(s_right, shift=UP*0.3, run_time=0.8),
        )
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜11：公式总结 ──
        formula_final = MathTex(
            "\\theta = \\theta - \\alpha \\nabla J(\\theta)",
            color=YELLOW,
        ).scale(1.0)
        formula_box = SurroundingRectangle(formula_final, color=YELLOW, buff=0.25)

        meanings = VGroup(
            Text("θ — 参数", font=CN, font_size=20, color=WHITE),
            Text("α — 学习率", font=CN, font_size=20, color=GREEN),
            Text("∇J(θ) — 损失函数的梯度", font=CN, font_size=20, color=BLUE),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        meanings.next_to(formula_box, DOWN, buff=0.5)

        self.play(FadeIn(formula_final, scale=0.85, run_time=1.5))
        self.play(Create(formula_box, run_time=0.8))
        self.play(FadeIn(meanings, shift=UP*0.2, run_time=1))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ================================================================
# 3D 场景：镜07-08, 10
# ================================================================
class GradientDescent3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = BG

        # 设置3D相机角度：正面俯视
        self.set_camera_orientation(phi=65*DEGREES, theta=-30*DEGREES)

        # ── 镜07：3D碗形曲面 J(θ₀,θ₁) = θ₀² + θ₁² ──
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[0, 12, 2],
            x_length=6, y_length=6, z_length=5,
        )

        # 碗形曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 + v**2),
            u_range=[-2.5, 2.5], v_range=[-2.5, 2.5],
            resolution=(30, 30),
            fill_opacity=0.6,
            fill_color=BLUE,
            stroke_width=0.5,
            stroke_color=DARK_GRAY,
        )

        # 标签
        j_label = MathTex("J(\\theta_0, \\theta_1) = \\theta_0^2 + \\theta_1^2", color=WHITE).scale(0.6)
        j_label.to_edge(UP, buff=0.3)

        self.play(Create(axes, run_time=1.5))
        self.play(Create(surface, run_time=3))
        self.play(FadeIn(j_label), run_time=0.5)
        self.wait(2)

        # ── 镜08：球沿曲面下降 ──
        # 起始点 (2, 2, 8)
        start_pos = axes.c2p(2, 2, 8)
        ball = Sphere(radius=0.12, color=YELLOW, resolution=(24, 24))
        ball.set_fill(YELLOW, opacity=0.9)
        ball.set_stroke(WHITE, width=1.5)
        ball.move_to(start_pos)

        # 迭代下降，记录路径
        alpha = 0.15
        x0, x1 = 2.0, 2.0
        path_positions = []

        for i in range(15):
            grad0 = 2 * x0
            grad1 = 2 * x1
            x0 = x0 - alpha * grad0
            x1 = x1 - alpha * grad1
            path_positions.append(axes.c2p(x0, x1, x0**2 + x1**2))

        # 逐帧移动球 + 同时画轨迹线
        self.play(FadeIn(ball), run_time=0.5)

        # 分段动画：每几步一组，让运动可见
        for i in range(0, len(path_positions), 3):
            chunk = path_positions[i:i+3]
            if not chunk:
                continue
            anims = [ball.animate.move_to(chunk[-1])]
            # 画这段的轨迹线
            line_start = ball.get_center() if i == 0 else path_positions[i-1]
            for j, pos in enumerate(chunk):
                if j > 0:
                    seg = Line(line_start if j == 0 else chunk[j-1], pos,
                              color=YELLOW, stroke_width=2, stroke_opacity=0.6)
                    self.add(seg)
                line_start = pos
            self.play(*anims, run_time=0.5)

        self.wait(2)

        # 拉远看全貌
        self.move_camera(phi=60*DEGREES, theta=-30*DEGREES, run_time=2)
        self.wait(2)

        # ── 镜10：局部最小 vs 全局最小（复杂曲面）──
        self.play(
            FadeOut(surface), FadeOut(axes), FadeOut(ball), FadeOut(j_label),
            run_time=0.8,
        )

        # 复杂曲面：有多个谷
        axes2 = ThreeDAxes(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-2, 5, 1],
            x_length=7, y_length=7, z_length=4,
        )

        # 多谷函数：有明显的局部最小和全局最小
        def complex_func(u, v):
            return (u**2 + v**2) + 2*np.sin(3*u)*np.sin(3*v) + 4

        complex_surface = Surface(
            lambda u, v: axes2.c2p(u, v, complex_func(u, v)),
            u_range=[-3.5, 3.5], v_range=[-3.5, 3.5],
            resolution=(50, 50),
            fill_opacity=0.6,
            fill_color=PURPLE,
            stroke_width=0.3,
            stroke_color=DARK_GRAY,
        )

        self.play(Create(axes2, run_time=1))
        self.play(Create(complex_surface, run_time=3))

        # 找实际的局部最小和全局最小
        # 全局最小在 (0,0) 附近
        # 局部最小在 (±1, ±1) 附近
        local_min = Dot(axes2.c2p(1, 1, complex_func(1, 1)), color=ORANGE, radius=0.1)
        global_min = Dot(axes2.c2p(0, 0, complex_func(0, 0)), color=RED, radius=0.1)

        local_label = Text("局部最小", font=CN, font_size=16, color=ORANGE)
        local_label.next_to(local_min, UP, buff=0.2)
        global_label = Text("全局最小", font=CN, font_size=16, color=RED)
        global_label.next_to(global_min, UP, buff=0.2)

        self.play(FadeIn(local_min), FadeIn(global_min), run_time=0.5)
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)


# ================================================================
# 渲染入口
# ================================================================
# 低质量测试：python -m manim render -ql 动画源码/第4期_梯度下降.py GradientDescent2D
# 高质量渲染：python -m manim render -qh 动画源码/第4期_梯度下降.py GradientDescent2D
# 3D场景：    python -m manim render -qh 动画源码/第4期_梯度下降.py GradientDescent3D

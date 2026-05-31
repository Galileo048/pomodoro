"""
第2期：e^(iπ) + 1 = 0 为什么最美？
时长：约5分30秒 | 10镜
知识点：欧拉公式与泰勒展开 | 难度：⭐⭐⭐
讲解重点：通过泰勒展开严格证明欧拉公式，揭示五个常数的统一

核心 Manim 类：ComplexPlane, Circle, Dot, Angle, MathTex,
              SurroundingRectangle, Transform, VGroup, always_redraw
"""
from manim import *
import numpy as np

# ============================================================
# 3b1b 经典配色方案
# ============================================================
BG = "#1C1C1C"          # 深灰背景
BLUE = "#58C4DD"        # 主曲线/主色调
GREEN = "#83C167"       # 辅助元素
YELLOW = "#FFFF00"      # 高亮强调
RED = "#FF6666"         # 关键点/警示
WHITE = "#FFFFFF"       # 正文
GRAY = "#888888"        # 次要文字
DARK_GRAY = "#444444"   # 暗色线条

# 中文字体
CN = "Microsoft YaHei"


class EulerFormulaScene(Scene):
    """欧拉公式完整动画场景"""

    def construct(self):
        # 设置深色背景
        self.camera.background_color = BG

        # ================================================================
        # 镜01：五个常数依次出现 (0-15s)
        # 神秘氛围，五个数字环绕排列
        # ================================================================
        # 五个常数及其含义
        constants_data = [
            ("e", "自然对数的底"),
            ("i", "虚数单位"),
            ("\\pi", "圆周率"),
            ("1", "乘法单位元"),
            ("0", "加法单位元"),
        ]

        # 创建五个常数，围成圆形排列
        radius = 2.0  # 环绕半径
        const_mobs = VGroup()
        for idx, (sym, meaning) in enumerate(constants_data):
            # 计算角度：从上方开始，顺时针均匀分布
            angle = PI / 2 - idx * 2 * PI / len(constants_data)
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)

            # 常数符号（大号）
            char = MathTex(sym, color=WHITE).scale(1.5)
            char.move_to([x, y, 0])

            const_mobs.add(char)

        # 逐个弹入显示，带缩放效果
        for mob in const_mobs:
            self.play(
                mob.animate.scale(1.3).set_color(YELLOW),
                run_time=0.3,
            )
            self.play(
                mob.animate.scale(1 / 1.3).set_color(WHITE),
                run_time=0.2,
            )
            self.wait(0.3)

        self.wait(1)

        # 标题文字
        title = Text("这五个数字，完美统一在一个公式中", font=CN, font_size=28, color=GRAY)
        title.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(title, shift=UP * 0.2, run_time=1))
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.8,
        )

        # ================================================================
        # 镜02：复平面展开 (15-40s)
        # 实轴水平标注 Re，虚轴垂直标注 Im
        # ================================================================
        # 创建复平面
        plane = ComplexPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=7,
            background_line_style={
                "stroke_color": DARK_GRAY,
                "stroke_width": 0.5,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 1.5,
            },
        )

        # 坐标轴标签
        re_label = Text("Re", font_size=22, color=GRAY).next_to(plane.get_right(), DOWN, buff=0.2)
        im_label = Text("Im", font_size=22, color=GRAY).next_to(plane.get_top(), LEFT, buff=0.2)
        origin_label = Text("O", font_size=18, color=GRAY).next_to(plane.get_origin(), DL, buff=0.1)

        # 动画：复平面从中心展开
        self.play(Create(plane, run_time=2))
        self.play(
            FadeIn(re_label), FadeIn(im_label), FadeIn(origin_label),
            run_time=0.5,
        )

        # 解说文字
        info = Text("复平面：横轴实部 Re，纵轴虚部 Im", font=CN, font_size=22, color=GRAY)
        info.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(info, shift=UP * 0.2, run_time=0.8))
        self.wait(2)
        self.play(FadeOut(info), run_time=0.5)

        # ================================================================
        # 镜03：单位圆绘制 (40-70s)
        # 圆心在原点，半径为1
        # ================================================================
        # 单位圆
        unit_circle = Circle(
            radius=plane.get_x_unit_size(),  # 单位长度
            color=BLUE,
            stroke_width=2.5,
        )
        unit_circle.move_to(plane.get_origin())

        # 半径标注
        radius_line = Line(
            plane.get_origin(),
            plane.c2p(1, 0),
            color=GREEN,
            stroke_width=2,
        )
        radius_label = MathTex("r = 1", color=GREEN).scale(0.7)
        radius_label.next_to(radius_line.get_center(), DOWN, buff=0.15)

        # 创建动画
        self.play(Create(unit_circle, run_time=2))
        self.play(Create(radius_line), FadeIn(radius_label), run_time=0.8)

        info2 = Text("单位圆：圆心在原点，半径为1", font=CN, font_size=22, color=GRAY)
        info2.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(info2, shift=UP * 0.2, run_time=0.8))
        self.wait(2)
        self.play(FadeOut(info2), FadeOut(radius_line), FadeOut(radius_label), run_time=0.5)

        # ================================================================
        # 镜04：动点沿单位圆运动 (70-100s)
        # 从(1,0)开始，逆时针运动，角度θ标注
        # ================================================================
        # ValueTracker 控制角度 θ
        theta_tracker = ValueTracker(0)

        # 动点（带发光圈）
        dot = always_redraw(lambda: Dot(
            plane.c2p(
                np.cos(theta_tracker.get_value()),
                np.sin(theta_tracker.get_value()),
            ),
            color=YELLOW,
            radius=0.1,
        ))
        dot_glow = always_redraw(lambda: Dot(
            plane.c2p(
                np.cos(theta_tracker.get_value()),
                np.sin(theta_tracker.get_value()),
            ),
            color=YELLOW,
            radius=0.25,
            fill_opacity=0.2,
            stroke_width=0,
        ))

        # 从原点到动点的连线（半径）
        radius = always_redraw(lambda: Line(
            plane.get_origin(),
            plane.c2p(
                np.cos(theta_tracker.get_value()),
                np.sin(theta_tracker.get_value()),
            ),
            color=GREEN,
            stroke_width=2,
        ))

        # 角度弧线（用 ParametricFunction 手动画弧，确保跟上动点）
        def get_arc():
            """根据当前 theta 值绘制从 0 到 theta 的弧线"""
            t = theta_tracker.get_value()
            if abs(t) < 0.01:
                return VMobject()
            # 弧线参数方程：x = r*cos(s), y = r*sin(s), s 从 0 到 t
            arc = ParametricFunction(
                lambda s: plane.c2p(0.6 * np.cos(s), 0.6 * np.sin(s)),
                t_range=[0, t, 0.02],
                color=YELLOW,
                stroke_width=2,
            )
            return arc

        angle_arc = always_redraw(get_arc)

        # 角度标签 θ（跟动点同步运动，回到原点）
        theta_label = always_redraw(lambda: MathTex(
            "\\theta", color=YELLOW
        ).scale(0.7).move_to(
            plane.c2p(0.85 * np.cos(theta_tracker.get_value()),
                       0.85 * np.sin(theta_tracker.get_value()))
        ))

        # 位置标签 e^(iθ)
        pos_label = always_redraw(lambda: MathTex(
            "e^{i\\theta}", color=BLUE
        ).scale(0.7).next_to(
            plane.c2p(
                np.cos(theta_tracker.get_value()),
                np.sin(theta_tracker.get_value()),
            ), UR, buff=0.15
        ))

        # 显示所有元素
        self.play(
            FadeIn(dot, scale=0.5),
            FadeIn(dot_glow),
            Create(radius),
            run_time=0.5,
        )
        self.play(FadeIn(pos_label), run_time=0.3)

        # 动点沿单位圆逆时针运动一圈
        self.play(
            Create(angle_arc),
            FadeIn(theta_label),
            run_time=0.5,
        )

        # 平滑运动：θ 从 0 到 2π
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=6,
            rate_func=smooth,
        )
        self.wait(1)

        # 解说
        info3 = Text("动点位置 = e^(iθ)", font=CN, font_size=22, color=BLUE)
        info3.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(info3, shift=UP * 0.2, run_time=0.8))
        self.wait(2)
        self.play(FadeOut(info3), run_time=0.5)

        # ================================================================
        # 镜05：泰勒展开推导 (100-140s)
        # e^x 的泰勒展开，代入 x=iθ
        # ================================================================
        # 清除图形元素（保留复平面做背景）
        self.play(
            FadeOut(dot), FadeOut(dot_glow),
            FadeOut(radius), FadeOut(angle_arc),
            FadeOut(theta_label), FadeOut(pos_label),
            FadeOut(unit_circle),
            run_time=0.5,
        )

        # e^x 的泰勒展开式
        taylor_e = MathTex(
            "e^x = 1 + x + \\frac{x^2}{2!} + \\frac{x^3}{3!} + \\frac{x^4}{4!} + \\cdots",
            color=WHITE,
        ).scale(0.75)
        taylor_e.to_edge(UP, buff=0.5)

        box_e = SurroundingRectangle(taylor_e, color=BLUE, buff=0.15)

        self.play(FadeIn(taylor_e, scale=0.85, run_time=1.5))
        self.play(Create(box_e, run_time=0.8))
        self.wait(1.5)

        # 代入 x = iθ
        sub_text = Text("令 x = iθ", font=CN, font_size=24, color=YELLOW)
        sub_text.next_to(box_e, DOWN, buff=0.3)

        self.play(FadeIn(sub_text, shift=UP * 0.2, run_time=0.8))
        self.wait(1.5)

        # 代入后的展开式
        taylor_i = MathTex(
            "e^{i\\theta} = 1 + i\\theta + \\frac{(i\\theta)^2}{2!} + \\frac{(i\\theta)^3}{3!} + \\cdots",
            color=WHITE,
        ).scale(0.65)
        taylor_i.next_to(sub_text, DOWN, buff=0.4)

        self.play(FadeIn(taylor_i, shift=UP * 0.2, run_time=1.2))
        self.wait(2)

        # ================================================================
        # 镜06：i 的幂次循环 (140-180s)
        # i⁰=1, i¹=i, i²=-1, i³=-i
        # ================================================================
        self.play(
            FadeOut(taylor_e), FadeOut(box_e),
            FadeOut(sub_text), FadeOut(taylor_i),
            run_time=0.5,
        )

        # i 的幂次循环展示
        powers = VGroup(
            MathTex("i^0 = 1", color=WHITE),
            MathTex("i^1 = i", color=BLUE),
            MathTex("i^2 = -1", color=RED),
            MathTex("i^3 = -i", color=GREEN),
            MathTex("i^4 = 1", color=WHITE),
        ).scale(0.7)
        powers.arrange(RIGHT, buff=0.5)
        powers.to_edge(UP, buff=0.5)

        # 逐个显示
        for power in powers:
            self.play(FadeIn(power, shift=UP * 0.2, run_time=0.5))
            self.wait(0.5)

        # 高亮循环
        cycle_box = SurroundingRectangle(powers, color=YELLOW, buff=0.15)
        self.play(Create(cycle_box, run_time=0.5))

        info4 = Text("i 的幂次每4次循环一次", font=CN, font_size=22, color=GRAY)
        info4.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(info4, shift=UP * 0.2, run_time=0.5))
        self.wait(2)
        self.play(FadeOut(info4), run_time=0.5)

        # ================================================================
        # 镜07：虚实部分离 → 欧拉公式 (180-220s)
        # 实部：cosθ，虚部：sinθ
        # ================================================================
        self.play(
            FadeOut(powers), FadeOut(cycle_box),
            run_time=0.5,
        )

        # 实部（中文用 Text，公式用 MathTex，组合在一起）
        real_label = Text("实部: ", font=CN, font_size=20, color=BLUE)
        real_formula = MathTex(
            "1 - \\frac{\\theta^2}{2!} + \\frac{\\theta^4}{4!} - \\cdots = \\cos\\theta",
            color=BLUE,
        ).scale(0.65)
        real_part = VGroup(real_label, real_formula).arrange(RIGHT, buff=0.1)
        real_part.to_edge(UP, buff=0.8)

        # 虚部
        imag_label = Text("虚部: ", font=CN, font_size=20, color=GREEN)
        imag_formula = MathTex(
            "\\theta - \\frac{\\theta^3}{3!} + \\frac{\\theta^5}{5!} - \\cdots = \\sin\\theta",
            color=GREEN,
        ).scale(0.65)
        imag_part = VGroup(imag_label, imag_formula).arrange(RIGHT, buff=0.1)
        imag_part.next_to(real_part, DOWN, buff=0.4)

        self.play(FadeIn(real_part, shift=RIGHT * 0.3, run_time=1))
        self.wait(1)
        self.play(FadeIn(imag_part, shift=RIGHT * 0.3, run_time=1))
        self.wait(1.5)

        # 合并 → 欧拉公式
        euler_formula = MathTex(
            "e^{i\\theta} = \\cos\\theta + i\\sin\\theta",
            color=YELLOW,
        ).scale(0.9)
        # 先定位公式，再创建矩形框（确保框跟上公式位置）
        euler_formula.move_to(ORIGIN + UP * 0.3)
        euler_box = SurroundingRectangle(euler_formula, color=YELLOW, buff=0.2)

        self.play(
            FadeOut(real_part), FadeOut(imag_part),
            run_time=0.5,
        )
        self.play(
            FadeIn(euler_formula, scale=0.85, run_time=1.5),
        )
        # 矩形框单独创建，确保位置正确
        euler_box.move_to(euler_formula.get_center())
        self.play(Create(euler_box, run_time=1))
        self.wait(3)

        # ================================================================
        # 镜08：令 θ=π → 欧拉恒等式 (220-260s)
        # ================================================================
        self.play(
            FadeOut(euler_formula), FadeOut(euler_box),
            run_time=0.5,
        )

        # 代入 θ=π 的推导步骤
        steps = VGroup(
            MathTex("\\theta = \\pi", color=WHITE),
            MathTex("e^{i\\pi} = \\cos\\pi + i\\sin\\pi", color=WHITE),
            MathTex("= -1 + i \\cdot 0", color=WHITE),
            MathTex("= -1", color=WHITE),
        ).scale(0.7)
        steps.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        steps.move_to(ORIGIN + UP * 0.5)

        for step in steps:
            self.play(FadeIn(step, shift=RIGHT * 0.3, run_time=0.8))
            self.wait(1)

        # 移项得到最终形式（先定位，再建框）
        final = MathTex("e^{i\\pi} + 1 = 0", color=YELLOW).scale(1.1)
        final.next_to(steps, DOWN, buff=0.6)

        self.play(FadeIn(final, scale=0.8, run_time=1.5))

        # 框在公式定位之后再创建
        final_box = SurroundingRectangle(final, color=YELLOW, buff=0.25)
        self.play(Create(final_box, run_time=1))
        self.wait(3)

        # ================================================================
        # 镜09：五个常数汇聚 (260-300s)
        # e^(iπ)+1=0 居中，五个常数环绕
        # ================================================================
        self.play(
            *[FadeOut(m) for m in self.mobjects if m != plane],
            FadeOut(plane),
            run_time=0.8,
        )

        # 最终公式居中放大
        big_formula = MathTex("e^{i\\pi} + 1 = 0", color=YELLOW).scale(1.5)
        self.play(FadeIn(big_formula, scale=0.5, run_time=1.5))

        # 五个常数环绕（缩小半径，确保不超出画面）
        const_final = VGroup(
            MathTex("e", color=BLUE).scale(1.0),
            MathTex("i", color=GREEN).scale(1.0),
            MathTex("\\pi", color=RED).scale(1.0),
            MathTex("1", color=WHITE).scale(1.0),
            MathTex("0", color=GRAY).scale(1.0),
        )

        # 围成圆形（半径从3.2缩小到2.5）
        for idx, c in enumerate(const_final):
            angle = PI / 2 - idx * 2 * PI / 5
            c.move_to(2.5 * np.cos(angle) * RIGHT + 2.5 * np.sin(angle) * UP)

        # 逐个弹入
        for c in const_final:
            self.play(
                c.animate.scale(1.3),
                run_time=0.2,
            )
            self.play(
                c.animate.scale(1 / 1.3),
                run_time=0.15,
            )

        # 含义标注（缩小字号，半径也缩小到3.3）
        meanings = VGroup(
            Text("e — 增长", font=CN, font_size=14, color=BLUE),
            Text("i — 想象", font=CN, font_size=14, color=GREEN),
            Text("π — 几何", font=CN, font_size=14, color=RED),
            Text("1 — 单位", font=CN, font_size=14, color=WHITE),
            Text("0 — 虚无", font=CN, font_size=14, color=GRAY),
        )
        for idx, m in enumerate(meanings):
            angle = PI / 2 - idx * 2 * PI / 5
            m.move_to(3.3 * np.cos(angle) * RIGHT + 3.3 * np.sin(angle) * UP)

        self.play(*[FadeIn(m, run_time=0.3) for m in meanings])
        self.wait(3)

        # ================================================================
        # 镜10：总结回顾 (300-330s)
        # 复平面→单位圆→欧拉公式→欧拉恒等式
        # ================================================================
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.8,
        )

        # 流程图
        flow = VGroup(
            Text("复平面", font=CN, font_size=24, color=BLUE),
            Text("→", font_size=24, color=GRAY),
            Text("单位圆", font=CN, font_size=24, color=GREEN),
            Text("→", font_size=24, color=GRAY),
            Text("欧拉公式", font=CN, font_size=24, color=YELLOW),
            Text("→", font_size=24, color=GRAY),
            Text("欧拉恒等式", font=CN, font_size=24, color=RED),
        ).arrange(RIGHT, buff=0.3)
        flow.move_to(ORIGIN + UP * 0.5)

        self.play(FadeIn(flow, shift=UP * 0.3, run_time=1.5))
        self.wait(1)

        # 结语
        end = Text("数学之美：简洁而深刻", font=CN, font_size=32, color=YELLOW)
        end.next_to(flow, DOWN, buff=0.8)
        self.play(FadeIn(end, shift=UP * 0.2, run_time=1))
        self.wait(3)

        # 最终淡出
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

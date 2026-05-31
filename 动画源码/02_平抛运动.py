from manim import *

class ProjectileMotion(Scene):
    """平抛运动 - 轨迹分解与公式推导（y轴向上为正）"""

    def construct(self):
        # ========== 第一部分：标题 ==========
        title = Text("平抛运动", font_size=52, color=BLUE)
        subtitle = Text("Projectile Motion", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ========== 第二部分：运动分解示意图 ==========
        t1 = Text("运动分解", font_size=40, color=BLUE)
        t1.to_edge(UP)
        self.play(Write(t1), run_time=0.8)

        # 坐标原点（左下角）
        origin = np.array([-4, -2, 0])

        # 水平方向（x轴）→ 向右
        x_axis = Arrow(origin, origin + RIGHT * 5, color=GREEN, buff=0)
        x_label = Text("水平方向：匀速直线运动", font_size=20, color=GREEN)
        x_label.next_to(x_axis, DOWN, buff=0.2)
        x_formula = MathTex("x = v_0 t", font_size=24, color=GREEN)
        x_formula.next_to(x_label, DOWN, buff=0.15)

        # 竖直方向（y轴）→ 向上为正
        y_axis = Arrow(origin, origin + UP * 4, color=YELLOW, buff=0)
        y_label = Text("竖直方向：自由落体运动", font_size=20, color=YELLOW)
        y_label.next_to(y_axis, LEFT, buff=0.2)
        y_formula = MathTex("y = h_0 - \\frac{1}{2}gt^2", font_size=24, color=YELLOW)
        y_formula.next_to(y_label, LEFT, buff=0.15)

        # 合运动（抛物线轨迹，从高处向右下方运动）
        v0 = 3
        g = 9.8
        h0 = 3.5  # 初始高度（在origin坐标系中）
        t_max = 0.8
        points = []
        for t in np.linspace(0, t_max, 50):
            x = origin[0] + v0 * t
            y = origin[1] + h0 - 0.5 * g * t ** 2
            if x <= 1 and y >= -2:
                points.append(np.array([x, y, 0]))

        if len(points) > 1:
            trajectory = VMobject(color=RED)
            trajectory.set_points_smoothly(points)
            trajectory.set_stroke(width=3)

        traj_label = Text("合运动：抛物线", font_size=20, color=RED)
        traj_label.move_to(RIGHT * 0.5 + UP * 0.5)

        # 标注起点
        start_dot = Dot(np.array([origin[0], origin[1] + h0, 0]), color=RED, radius=0.08)
        start_label = Text("起点", font_size=16, color=RED)
        start_label.next_to(start_dot, UP, buff=0.1)

        # 动画
        self.play(GrowArrow(x_axis), Write(x_label), Write(x_formula), run_time=1)
        self.play(GrowArrow(y_axis), Write(y_label), Write(y_formula), run_time=1)
        self.play(
            Create(start_dot), Write(start_label),
            Create(trajectory), Write(traj_label),
            run_time=1.5,
        )
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第三部分：参数化演示 ==========
        t2 = Text("参数化演示", font_size=40, color=BLUE)
        t2.to_edge(UP)
        self.play(Write(t2), run_time=0.8)

        # 坐标系（y轴向上）
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "include_tip": True,
            },
        ).shift(DOWN * 0.5)

        x_label2 = axes.get_x_axis_label("x / m", direction=RIGHT)
        y_label2 = axes.get_y_axis_label("y / m", direction=UP)

        self.play(Create(axes), Write(x_label2), Write(y_label2), run_time=1)

        # 不同初速度的轨迹（从高处发射，向下弯曲）
        v0_values = [2, 3, 4]
        colors = [GREEN, BLUE, PURPLE]
        g = 9.8
        h0_screen = 4.5  # 初始高度（屏幕坐标）
        t_max = 0.9

        trajectories = []
        labels = []

        for v0, color in zip(v0_values, colors):
            points = []
            for t in np.linspace(0, t_max, 100):
                x = v0 * t
                y = h0_screen - 0.5 * g * t ** 2
                if x <= 5.5 and y >= 0:
                    points.append(axes.c2p(x, y))

            if len(points) > 1:
                traj = VMobject(color=color)
                traj.set_points_smoothly(points)
                traj.set_stroke(width=2.5)
                trajectories.append(traj)

                label = MathTex(f"v_0 = {v0} m/s", font_size=20, color=color)
                labels.append(label)

        # 标签位置
        labels[0].move_to(axes.c2p(4.5, 1))
        labels[1].move_to(axes.c2p(5, 2))
        labels[2].move_to(axes.c2p(5.5, 3))

        # 动画
        for traj, label in zip(trajectories, labels):
            self.play(Create(traj), Write(label), run_time=1)

        self.wait(1)

        # 标注初速度方向（水平向右）
        start_dot2 = Dot(axes.c2p(0, h0_screen), color=RED, radius=0.1)
        v0_arrow = Arrow(
            axes.c2p(0, h0_screen),
            axes.c2p(1, h0_screen),
            color=RED,
            buff=0,
        )
        v0_label = MathTex("v_0", font_size=24, color=RED)
        v0_label.next_to(v0_arrow, UP, buff=0.1)

        # 高度标注
        h_arrow = Arrow(
            axes.c2p(0, 0),
            axes.c2p(0, h0_screen),
            color=YELLOW,
            buff=0,
        )
        h_label = MathTex("h_0", font_size=22, color=YELLOW)
        h_label.next_to(h_arrow, LEFT, buff=0.1)

        self.play(
            Create(start_dot2), GrowArrow(v0_arrow), Write(v0_label),
            GrowArrow(h_arrow), Write(h_label),
        )
        self.wait(2)

        # 清场
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        # ========== 第四部分：小球平抛演示 ==========
        t3 = Text("小球平抛演示", font_size=40, color=BLUE)
        t3.to_edge(UP)
        self.play(Write(t3), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(t3))

        # 地面（底部）
        ground = Line(
            LEFT * 5.5 + DOWN * 2.5,
            RIGHT * 5.5 + DOWN * 2.5,
            color=GRAY,
            stroke_width=3,
        )

        # 发射平台（左侧高台）
        platform = Rectangle(
            width=0.5,
            height=2,
            color=GRAY,
            fill_opacity=0.5,
        ).move_to(LEFT * 5 + DOWN * 1.5)

        # 小球初始位置（平台顶部）
        ball_start = LEFT * 5 + UP * 0.5
        ball = Circle(radius=0.15, color=RED, fill_opacity=1)
        ball.move_to(ball_start)

        # 初速度箭头（水平向右）
        v0_arr = Arrow(
            ball.get_center(),
            ball.get_center() + RIGHT * 1.5,
            color=GREEN,
            buff=0,
        )
        v0_text = MathTex("v_0", font_size=22, color=GREEN)
        v0_text.next_to(v0_arr, UP, buff=0.1)

        # 时间显示
        time_display = Text("t = 0.0s", font_size=26, color=WHITE)
        time_display.to_edge(UP)

        # 公式
        formula_group = VGroup(
            MathTex("x = v_0 t", font_size=22, color=GREEN),
            MathTex("y = h_0 - \\frac{1}{2}gt^2", font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        formula_group.to_edge(DOWN)

        # 组装
        self.play(
            Create(ground),
            Create(platform),
            Create(ball),
            GrowArrow(v0_arr),
            Write(v0_text),
            Write(time_display),
            Write(formula_group),
        )
        self.wait(0.5)

        # ========== 平抛运动动画 ==========
        v0 = 3  # 初速度 m/s
        g = 9.8  # 重力加速度
        h0 = 3  # 初始高度（屏幕单位）
        scale = 0.8  # 屏幕缩放
        t = 0
        dt = 0.03
        trail_points = []

        current_time = time_display

        while t < 1.0:
            t += dt

            # 物理坐标
            x_phys = v0 * t
            y_phys = h0 - 0.5 * g * t ** 2

            # 屏幕坐标（y向上为正）
            screen_x = -5 + x_phys * scale
            screen_y = -2 + y_phys * scale

            if screen_x > 5.5 or screen_y < -2.5:
                break

            new_pos = np.array([screen_x, screen_y, 0])

            # 轨迹线
            trail_points.append(new_pos.copy())
            if len(trail_points) > 1:
                trail = VMobject(color=RED, stroke_width=2)
                trail.set_points_as_corners(trail_points)

            # 水平速度分量（始终向右）
            vx_arrow = Arrow(
                new_pos,
                new_pos + RIGHT * 0.8,
                color=GREEN,
                buff=0,
            )

            # 竖直速度分量（向下，越来越大）
            vy = g * t
            vy_len = min(vy * 0.08, 1.5)
            vy_arrow = Arrow(
                new_pos,
                new_pos + DOWN * vy_len,
                color=YELLOW,
                buff=0,
            )

            # 合速度（切线方向）
            v_total = np.sqrt(v0 ** 2 + vy ** 2)
            angle = np.arctan2(vy, v0)
            v_len = min(v_total * 0.08, 2)
            v_arrow = Arrow(
                new_pos,
                new_pos + np.array([v_len * np.cos(angle), -v_len * np.sin(angle), 0]),
                color=RED,
                buff=0,
            )

            # 时间显示
            new_time = Text(f"t = {t:.1f}s", font_size=26, color=WHITE)
            new_time.to_edge(UP)

            # 动画
            anims = [
                ball.animate.move_to(new_pos),
                ReplacementTransform(current_time, new_time),
            ]

            if len(trail_points) > 1:
                anims.append(Create(trail))

            self.play(*anims, run_time=dt * 1.5, rate_func=linear)

            current_time = new_time

        self.wait(2)

        # ========== 第五部分：公式总结 ==========
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        summary_title = Text("平抛运动公式总结", font_size=42, color=BLUE)
        summary_title.to_edge(UP)
        self.play(Write(summary_title), run_time=0.8)

        formulas = VGroup(
            VGroup(
                Text("水平方向：", font_size=24, color=GREEN),
                MathTex("x = v_0 t", font_size=28, color=GREEN),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("竖直方向：", font_size=24, color=YELLOW),
                MathTex("y = h_0 - \\frac{1}{2}gt^2", font_size=28, color=YELLOW),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("合速度：", font_size=24, color=RED),
                MathTex("v = \\sqrt{v_0^2 + (gt)^2}", font_size=28, color=RED),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("轨迹方程：", font_size=24, color=PURPLE),
                MathTex("y = h_0 - \\frac{g}{2v_0^2}x^2", font_size=28, color=PURPLE),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        formulas.move_to(ORIGIN)

        for formula in formulas:
            self.play(Write(formula), run_time=0.8)

        self.wait(3)

        # 结束
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        end_text = Text("平抛运动：水平匀速 + 竖直自由落体", font_size=28, color=BLUE)
        self.play(Write(end_text), run_time=1)
        self.wait(2)
        self.play(FadeOut(end_text))

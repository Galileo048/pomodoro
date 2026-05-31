from manim import *

class UniformAcceleration(Scene):
    """匀变速直线运动 - 速度-时间图像动画"""

    def construct(self):
        # ========== 第一部分：标题 ==========
        title = Text("匀变速直线运动", font_size=48, color=BLUE)
        subtitle = Text("Velocity-Time Graph", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ========== 第二部分：坐标系 ==========
        # 创建坐标轴
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 30, 5],
            x_length=8,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 24,
                "include_tip": True,
            },
            tips=True,
        )

        # 坐标轴标签
        x_label = axes.get_x_axis_label("t / s", direction=RIGHT)
        y_label = axes.get_y_axis_label("v / (m/s)", direction=UP)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)

        # ========== 第三部分：函数曲线 ==========
        # 匀加速：v = at，取 a = 5 m/s²
        a = 5  # 加速度

        # 绘制 v-t 曲线
        graph = axes.plot(
            lambda t: a * t,
            x_range=[0, 5.5, 0.01],
            color=YELLOW,
        )

        graph_label = axes.get_graph_label(
            graph,
            label="v = 5t",
            direction=UL,
            buff=0.2,
            color=YELLOW,
        )

        self.play(Create(graph), Write(graph_label), run_time=2)

        # ========== 第四部分：面积填充 ==========
        # 填充曲线下方面积（表示位移）
        area = axes.get_area(
            graph,
            x_range=[0, 4],
            color=[BLUE, GREEN],
            opacity=0.3,
        )

        area_text = Text("面积 = 位移", font_size=20, color=GREEN)
        area_text.move_to(RIGHT * 4.5 + DOWN * 0.5)

        self.play(FadeIn(area), run_time=1)
        self.play(Write(area_text), run_time=0.8)
        self.wait(1)

        # ========== 第五部分：关键点标注 ==========
        # 标注 t=4s 时的速度
        t_val = 4
        v_val = a * t_val

        # 竖直虚线
        v_line = DashedLine(
            axes.c2p(t_val, 0),
            axes.c2p(t_val, v_val),
            color=RED,
            dash_length=0.1,
        )

        # 水平虚线
        h_line = DashedLine(
            axes.c2p(0, v_val),
            axes.c2p(t_val, v_val),
            color=RED,
            dash_length=0.1,
        )

        # 点
        dot = Dot(axes.c2p(t_val, v_val), color=RED, radius=0.08)

        # 标注文字
        t_label = MathTex("t = 4s", font_size=24, color=RED)
        t_label.next_to(axes.c2p(t_val, 0), DOWN, buff=0.2)

        v_label = MathTex("v = 20 m/s", font_size=24, color=RED)
        v_label.next_to(axes.c2p(t_val, v_val), UR, buff=0.15)

        self.play(
            Create(v_line),
            Create(h_line),
            Create(dot),
            Write(t_label),
            Write(v_label),
            run_time=1.5,
        )
        self.wait(1)

        # ========== 第六部分：公式展示 ==========
        formula_group = VGroup()

        f1 = MathTex("v = at", font_size=32, color=WHITE)
        f2 = MathTex("v = 5 \\times 4 = 20 \\, m/s", font_size=28, color=YELLOW)
        f2.next_to(f1, DOWN, buff=0.3)

        formula_group.add(f1, f2)
        formula_group.move_to(RIGHT * 3.5 + UP * 2)

        box = SurroundingRectangle(formula_group, color=BLUE, buff=0.2)

        self.play(Write(f1), run_time=0.8)
        self.play(Write(f2), run_time=0.8)
        self.play(Create(box), run_time=0.5)
        self.wait(2)

        # ========== 第七部分：运动小球动画 ==========
        # 切换到新场景
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8,
        )

        # 标题
        t2 = Text("小球运动演示", font_size=40, color=BLUE)
        self.play(Write(t2), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(t2))

        # 地面
        ground = Line(
            LEFT * 5.5 + DOWN * 2,
            RIGHT * 5.5 + DOWN * 2,
            color=GRAY,
            stroke_width=3,
        )

        # 刻度线
        ticks = VGroup()
        for i in range(-5, 6):
            tick = Line(
                ground.get_start() + RIGHT * (i + 5.5) * 0.91,
                ground.get_start() + RIGHT * (i + 5.5) * 0.91 + UP * 0.15,
                color=GRAY,
            )
            ticks.add(tick)

        # 小球
        ball = Circle(radius=0.3, color=RED, fill_opacity=1)
        ball.move_to(LEFT * 5 + DOWN * 1.5)

        # 速度箭头
        velocity_arrow = Arrow(
            ball.get_center() + RIGHT * 0.4,
            ball.get_center() + RIGHT * 2,
            color=GREEN,
            buff=0,
        )

        # 加速度箭头
        accel_arrow = Arrow(
            ball.get_center() + RIGHT * 0.4 + UP * 0.6,
            ball.get_center() + RIGHT * 1.5 + UP * 0.6,
            color=YELLOW,
            buff=0,
        )

        # 标签
        v_tag = Text("v", font_size=24, color=GREEN)
        v_tag.next_to(velocity_arrow, UP, buff=0.1)

        a_tag = Text("a", font_size=24, color=YELLOW)
        a_tag.next_to(accel_arrow, UP, buff=0.1)

        # 时间显示
        time_display = Text("t = 0.0s", font_size=28, color=WHITE)
        time_display.to_edge(UP)

        # 公式
        formula = MathTex("v = at = 5t", font_size=28, color=YELLOW)
        formula.to_edge(DOWN)

        # 组装动画
        self.play(
            Create(ground),
            Create(ticks),
            Create(ball),
            Write(time_display),
            Write(formula),
        )

        self.play(
            GrowArrow(velocity_arrow),
            GrowArrow(accel_arrow),
            Write(v_tag),
            Write(a_tag),
        )
        self.wait(0.5)

        # ========== 运动动画 ==========
        # 小球做匀加速运动：x = 0.5 * a * t^2
        t_end = 4  # 总时间
        dt = 0.05  # 时间步长（增大以减少抖动）
        t = 0

        # 记录当前位置
        current_pos = ball.get_center()
        current_v_arrow = velocity_arrow
        current_a_arrow = accel_arrow
        current_v_tag = v_tag
        current_a_tag = a_tag
        current_time = time_display

        while t < t_end:
            t += dt
            x = 0.5 * a * t ** 2
            # 映射到屏幕坐标
            screen_x = -5 + x * 0.4  # 缩放因子

            if screen_x > 5:
                break

            new_pos = np.array([screen_x, -1.5, 0])

            # 速度 v = at
            v_now = a * t

            # 速度箭头长度
            arrow_len = min(v_now * 0.1, 3)

            new_v_arrow = Arrow(
                new_pos + RIGHT * 0.4,
                new_pos + RIGHT * (0.4 + arrow_len),
                color=GREEN,
                buff=0,
            )

            new_a_arrow = Arrow(
                new_pos + RIGHT * 0.4 + UP * 0.6,
                new_pos + RIGHT * 1.5 + UP * 0.6,
                color=YELLOW,
                buff=0,
            )

            new_v_tag = Text("v", font_size=24, color=GREEN)
            new_v_tag.next_to(new_v_arrow, UP, buff=0.1)

            new_time = Text(f"t = {t:.1f}s", font_size=28, color=WHITE)
            new_time.to_edge(UP)

            self.play(
                ball.animate.move_to(new_pos),
                ReplacementTransform(current_v_arrow, new_v_arrow),
                ReplacementTransform(current_a_arrow, new_a_arrow),
                ReplacementTransform(current_v_tag, new_v_tag),
                ReplacementTransform(current_time, new_time),
                run_time=dt * 2,
                rate_func=linear,
            )

            current_v_arrow = new_v_arrow
            current_a_arrow = new_a_arrow
            current_v_tag = new_v_tag
            current_time = new_time

        self.wait(2)

        # ========== 结束 ==========
        end_text = Text("匀加速运动：v 随 t 均匀增大", font_size=28, color=BLUE)
        end_text.to_edge(UP)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.5,
        )

        self.play(Write(end_text), run_time=1)
        self.wait(2)
        self.play(FadeOut(end_text))

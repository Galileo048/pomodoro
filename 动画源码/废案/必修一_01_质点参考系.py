from manim import *
import numpy as np


class ParticleReferenceFrame(Scene):
    """1.1 质点 参考系 - 全新重写"""

    def construct(self):
        # ===== 标题 =====
        title = Text("1.1 质点 参考系", font_size=44, color=BLUE)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(title))

        # ===== 第一部分：地面参考系 =====
        part1 = Text("地面参考系", font_size=30, color=GREEN)
        part1.to_edge(UP)
        self.play(Write(part1), run_time=0.5)

        # 地面
        ground = Line(LEFT * 5.5 + DOWN * 1.5, RIGHT * 5.5 + DOWN * 1.5, color=GRAY, stroke_width=4)
        ground_marks = VGroup()
        for i in range(-5, 6):
            mark = Line(
                np.array([i, -1.5, 0]),
                np.array([i, -1.3, 0]),
                color=GRAY, stroke_width=2,
            )
            ground_marks.add(mark)

        # 坐标轴
        axis = Arrow(LEFT * 5 + DOWN * 1.5, RIGHT * 5 + DOWN * 1.5, color=WHITE, buff=0, stroke_width=2)
        axis_label = MathTex("x", font_size=22, color=WHITE).next_to(axis, RIGHT, buff=0.1)

        self.play(Create(ground), Create(ground_marks), GrowArrow(axis), Write(axis_label))

        # 小车
        car_body = Rectangle(width=1.2, height=0.6, color=BLUE, fill_opacity=0.9)
        wheel1 = Circle(radius=0.15, color=GRAY, fill_opacity=1).move_to(car_body.get_left() + DOWN * 0.3)
        wheel2 = Circle(radius=0.15, color=GRAY, fill_opacity=1).move_to(car_body.get_right() + DOWN * 0.3)
        car = VGroup(car_body, wheel1, wheel2)
        car.move_to(LEFT * 4 + DOWN * 0.9)

        # 速度箭头
        v_arrow = Arrow(
            car.get_right() + RIGHT * 0.1,
            car.get_right() + RIGHT * 1.5,
            color=GREEN, buff=0, stroke_width=3,
        )
        v_text = MathTex("\\vec{v}", font_size=24, color=GREEN).next_to(v_arrow, UP, buff=0.1)

        self.play(Create(car))
        self.play(GrowArrow(v_arrow), Write(v_text))

        # 动态参数
        t = ValueTracker(0)
        v = 2.5

        # 位置显示
        pos_display = always_redraw(lambda: VGroup(
            MathTex("x =", font_size=22, color=WHITE),
            MathTex(f"{v * t.get_value():.1f}", font_size=22, color=YELLOW),
            MathTex("m", font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.1).to_edge(DOWN))

        self.add(pos_display)

        # 小车运动
        def update_car(mob):
            x = -4 + v * t.get_value()
            mob.move_to(np.array([x, -0.9, 0]))

        def update_v_arrow(mob):
            start = car.get_right() + RIGHT * 0.1
            end = car.get_right() + RIGHT * 1.5
            mob.put_start_and_end_on(start, end)

        def update_v_text(mob):
            mob.next_to(v_arrow, UP, buff=0.1)

        car.add_updater(update_car)
        v_arrow.add_updater(update_v_arrow)
        v_text.add_updater(update_v_text)

        self.play(t.animate.set_value(3.5), run_time=3, rate_func=linear)

        car.remove_updater(update_car)
        v_arrow.remove_updater(update_v_arrow)
        v_text.remove_updater(update_v_text)

        # 结论
        result = Text("地面参考系：车向前运动", font_size=22, color=GREEN)
        result.to_edge(DOWN)
        self.play(Write(result))
        self.wait(1)

        # ===== 清场 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ===== 第二部分：车参考系 =====
        part2 = Text("车参考系（以车为标准）", font_size=30, color=YELLOW)
        part2.to_edge(UP)
        self.play(Write(part2), run_time=0.5)

        # 车（固定在原点）
        car2_body = Rectangle(width=1.2, height=0.6, color=BLUE, fill_opacity=0.9)
        car2_w1 = Circle(radius=0.15, color=GRAY, fill_opacity=1).move_to(car2_body.get_left() + DOWN * 0.3)
        car2_w2 = Circle(radius=0.15, color=GRAY, fill_opacity=1).move_to(car2_body.get_right() + DOWN * 0.3)
        car2 = VGroup(car2_body, car2_w1, car2_w2)
        car2.move_to(ORIGIN + DOWN * 0.9)

        car2_label = Text("车（静止）", font_size=18, color=BLUE).next_to(car2, DOWN, buff=0.2)

        # 坐标轴
        axis2 = Arrow(LEFT * 5 + DOWN * 1.5, RIGHT * 5 + DOWN * 1.5, color=WHITE, buff=0, stroke_width=2)
        axis2_label = MathTex("x'", font_size=22, color=WHITE).next_to(axis2, RIGHT, buff=0.1)

        self.play(Create(car2), Write(car2_label), GrowArrow(axis2), Write(axis2_label))

        # 地面上的一个点（树）
        tree = VGroup(
            Rectangle(width=0.3, height=0.8, color=GREEN, fill_opacity=0.8),
            Circle(radius=0.25, color=GREEN, fill_opacity=0.8),
        )
        tree[1].move_to(tree[0].get_top() + UP * 0.2)
        tree.move_to(RIGHT * 3.5 + DOWN * 0.9)
        tree_label = Text("树", font_size=16, color=GREEN).next_to(tree, DOWN, buff=0.1)

        self.play(Create(tree), Write(tree_label))

        # 动态参数
        t2 = ValueTracker(0)

        # 位置显示
        pos_display2 = always_redraw(lambda: VGroup(
            MathTex("x' =", font_size=22, color=WHITE),
            MathTex(f"{3.5 - v * t2.get_value():.1f}", font_size=22, color=YELLOW),
            MathTex("m", font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.1).to_edge(DOWN))

        self.add(pos_display2)

        # 树运动
        def update_tree(mob):
            x = 3.5 - v * t2.get_value()
            mob.move_to(np.array([x, -0.9, 0]))

        def update_tree_label(mob):
            mob.next_to(tree, DOWN, buff=0.1)

        tree.add_updater(update_tree)
        tree_label.add_updater(update_tree_label)

        self.play(t2.animate.set_value(2.5), run_time=2.5, rate_func=linear)

        tree.remove_updater(update_tree)
        tree_label.remove_updater(update_tree_label)

        # 结论
        result2 = Text("车参考系：树在后退", font_size=22, color=YELLOW)
        result2.to_edge(DOWN)
        self.play(Write(result2))
        self.wait(1)

        # ===== 清场 =====
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ===== 第三部分：质点概念 =====
        part3 = Text("质点", font_size=30, color=RED)
        part3.to_edge(UP)
        self.play(Write(part3), run_time=0.5)

        # 物体 vs 质点
        obj = Rectangle(width=1.5, height=0.8, color=BLUE, fill_opacity=0.8)
        obj_label = Text("物体", font_size=18, color=WHITE).move_to(obj)

        arrow = Arrow(RIGHT * 0.5, RIGHT * 2, color=WHITE, buff=0.2)
        dot = Dot(RIGHT * 3, color=RED, radius=0.15)
        dot_label = Text("质点", font_size=18, color=RED).next_to(dot, DOWN, buff=0.2)

        self.play(Create(obj), Write(obj_label))
        self.play(GrowArrow(arrow), Create(dot), Write(dot_label))

        # 条件
        conditions = VGroup(
            Text("当物体的大小和形状对研究问题", font_size=20, color=WHITE),
            Text("影响很小时，可视为质点", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.1)
        conditions.move_to(DOWN * 1.5)
        self.play(Write(conditions))

        # 示例
        example = VGroup(
            Text("例：地球绕太阳 → 可视为质点", font_size=18, color=GREEN),
            Text("例：火车过桥 → 不能视为质点", font_size=18, color=RED),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        example.move_to(DOWN * 2.5)
        self.play(Write(example))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

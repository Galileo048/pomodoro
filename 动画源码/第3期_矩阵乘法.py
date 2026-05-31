"""
第3期：矩阵乘法到底在做什么？
时长：约6分钟 | 10镜
知识点：矩阵与线性变换 | 难度：⭐⭐⭐
讲解重点：旋转、缩放、剪切三种变换，矩阵乘法的几何意义
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

CN = "Microsoft YaHei"


class MatrixMultiplicationScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ================================================================
        # 镜01：标题
        # ================================================================
        title = Text("矩阵乘法到底在做什么？", font=CN, font_size=44, color=WHITE)
        subtitle = Text("线性变换的复合", font=CN, font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title, run_time=2))
        self.play(FadeIn(subtitle, shift=UP * 0.2, run_time=1))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ================================================================
        # 镜02：坐标系 + 单位正方形
        # ================================================================
        axes = Axes(
            x_range=[-1, 4, 1], y_range=[-1, 4, 1],
            x_length=6, y_length=6,
            axis_config={"include_tip": True, "color": GRAY, "stroke_width": 1.5},
        ).shift(DOWN * 0.3 + LEFT * 1)

        x_label = MathTex("x", color=GRAY).scale(0.7).next_to(axes.x_axis.get_end(), DR, buff=0.1)
        y_label = MathTex("y", color=GRAY).scale(0.7).next_to(axes.y_axis.get_end(), LEFT, buff=0.1)

        # 手动刻度
        ticks = VGroup()
        for v in range(1, 4):
            t1 = Text(str(v), font_size=16, color=GRAY).next_to(axes.c2p(v, 0), DOWN, buff=0.1)
            t2 = Text(str(v), font_size=16, color=GRAY).next_to(axes.c2p(0, v), LEFT, buff=0.1)
            ticks.add(t1, t2)

        self.play(Create(axes, run_time=1.5))
        self.play(FadeIn(x_label), FadeIn(y_label), FadeIn(ticks), run_time=0.5)

        # 单位正方形（四个顶点）
        o = axes.c2p(0, 0)
        pa = axes.c2p(1, 0)
        pb = axes.c2p(1, 1)
        pc = axes.c2p(0, 1)

        square = Polygon(o, pa, pb, pc, fill_color=BLUE, fill_opacity=0.3,
                         stroke_color=BLUE, stroke_width=2)

        self.play(Create(square, run_time=1.5))
        self.wait(1)

        # ================================================================
        # 镜03：基向量
        # ================================================================
        origin = axes.c2p(0, 0)

        i_vec = Arrow(origin, axes.c2p(1, 0), color=RED, stroke_width=3, buff=0)
        j_vec = Arrow(origin, axes.c2p(0, 1), color=GREEN, stroke_width=3, buff=0)

        # 用 Text 替代 MathTex \vec，避免字体问题
        i_label = Text("i", font_size=28, color=RED, weight=BOLD).next_to(i_vec, DOWN, buff=0.12)
        j_label = Text("j", font_size=28, color=GREEN, weight=BOLD).next_to(j_vec, LEFT, buff=0.12)

        self.play(GrowArrow(i_vec), FadeIn(i_label), run_time=0.8)
        self.play(GrowArrow(j_vec), FadeIn(j_label), run_time=0.8)

        info2 = Text("基向量：i = (1,0) 沿x轴，j = (0,1) 沿y轴", font=CN, font_size=20, color=GRAY)
        info2.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(info2, shift=UP * 0.2, run_time=0.8))
        self.wait(2)
        self.play(FadeOut(info2), run_time=0.5)

        # ================================================================
        # 辅助函数：手动变换点
        # ================================================================
        def tp(matrix, point):
            """2x2矩阵作用于axes坐标点，返回屏幕坐标"""
            x, y = point
            return axes.c2p(matrix[0][0]*x + matrix[0][1]*y,
                            matrix[1][0]*x + matrix[1][1]*y)

        def make_arrow(mat, end, color):
            """从原点到变换后端点的箭头"""
            return Arrow(origin, tp(mat, end), color=color, stroke_width=3, buff=0)

        def make_square(mat):
            """变换后的正方形"""
            return Polygon(
                origin, tp(mat, (1,0)), tp(mat, (1,1)), tp(mat, (0,1)),
                fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=2,
            )

        def make_vertex_labels(mat):
            """实时显示四个顶点坐标"""
            coords = [(0,0), (1,0), (1,1), (0,1)]
            labels = VGroup()
            for cx, cy in coords:
                nx = mat[0][0]*cx + mat[0][1]*cy
                ny = mat[1][0]*cx + mat[1][1]*cy
                # 格式化坐标，整数不显示小数点
                sx = f"{nx:.0f}" if abs(nx - round(nx)) < 0.01 else f"{nx:.1f}"
                sy = f"{ny:.0f}" if abs(ny - round(ny)) < 0.01 else f"{ny:.1f}"
                t = Text(f"({sx},{sy})", font_size=14, color=GRAY)
                t.move_to(tp(mat, (cx, cy)))
                # 把标签放到顶点外侧
                direction = tp(mat, (cx, cy)) - origin
                if np.linalg.norm(direction) > 0.1:
                    t.shift(direction / np.linalg.norm(direction) * 0.35)
                labels.add(t)
            return labels

        # 原始顶点坐标标签
        orig_labels = make_vertex_labels([[1,0],[0,1]])
        self.play(FadeIn(orig_labels), run_time=0.5)

        # ================================================================
        # 镜04：旋转 90°
        # ================================================================
        rot_mat = [[0, -1], [1, 0]]

        rot_matrix_tex = MathTex(
            "R = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=YELLOW,
        ).scale(0.75).to_edge(UP, buff=0.3).to_edge(RIGHT, buff=0.5)
        rot_text = Text("旋转 90°", font=CN, font_size=20, color=YELLOW)
        rot_text.next_to(rot_matrix_tex, DOWN, buff=0.2)

        self.play(FadeIn(rot_matrix_tex), FadeIn(rot_text), run_time=0.8)
        self.wait(0.5)

        # 变换后的元素
        new_i = make_arrow(rot_mat, (1,0), RED)
        new_j = make_arrow(rot_mat, (0,1), GREEN)
        new_sq = make_square(rot_mat)
        new_labels = make_vertex_labels(rot_mat)

        # i/j 标签跟随箭头新位置
        new_i_label = Text("i", font_size=28, color=RED, weight=BOLD)
        new_i_label.next_to(new_i.get_end(), DOWN, buff=0.12)
        new_j_label = Text("j", font_size=28, color=GREEN, weight=BOLD)
        new_j_label.next_to(new_j.get_end(), LEFT, buff=0.12)

        self.play(
            Transform(i_vec, new_i), Transform(j_vec, new_j),
            Transform(i_label, new_i_label), Transform(j_label, new_j_label),
            Transform(square, new_sq),
            Transform(orig_labels, new_labels),
            run_time=2,
        )
        self.wait(2)

        # 恢复
        self.play(
            Transform(i_vec, Arrow(origin, axes.c2p(1,0), color=RED, stroke_width=3, buff=0)),
            Transform(j_vec, Arrow(origin, axes.c2p(0,1), color=GREEN, stroke_width=3, buff=0)),
            Transform(i_label, Text("i", font_size=28, color=RED, weight=BOLD).next_to(axes.c2p(1,0), DOWN, buff=0.12)),
            Transform(j_label, Text("j", font_size=28, color=GREEN, weight=BOLD).next_to(axes.c2p(0,1), LEFT, buff=0.12)),
            Transform(square, Polygon(origin, axes.c2p(1,0), axes.c2p(1,1), axes.c2p(0,1),
                         fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=2)),
            Transform(orig_labels, make_vertex_labels([[1,0],[0,1]])),
            FadeOut(rot_matrix_tex), FadeOut(rot_text),
            run_time=1,
        )

        # ================================================================
        # 镜05：缩放 2倍
        # ================================================================
        sc_mat = [[2, 0], [0, 2]]

        sc_tex = MathTex(
            "S = \\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}", color=GREEN,
        ).scale(0.75).to_edge(UP, buff=0.3).to_edge(RIGHT, buff=0.5)
        sc_text = Text("均匀缩放 2倍", font=CN, font_size=20, color=GREEN)
        sc_text.next_to(sc_tex, DOWN, buff=0.2)

        self.play(FadeIn(sc_tex), FadeIn(sc_text), run_time=0.8)
        self.wait(0.5)

        # 缩放后 i/j 标签跟随
        ni_sc = make_arrow(sc_mat, (1,0), RED)
        nj_sc = make_arrow(sc_mat, (0,1), GREEN)
        nil_sc = Text("i", font_size=28, color=RED, weight=BOLD).next_to(ni_sc.get_end(), DOWN, buff=0.12)
        njl_sc = Text("j", font_size=28, color=GREEN, weight=BOLD).next_to(nj_sc.get_end(), LEFT, buff=0.12)

        self.play(
            Transform(i_vec, ni_sc), Transform(j_vec, nj_sc),
            Transform(i_label, nil_sc), Transform(j_label, njl_sc),
            Transform(square, make_square(sc_mat)),
            Transform(orig_labels, make_vertex_labels(sc_mat)),
            run_time=2,
        )
        self.wait(2)

        # 恢复
        self.play(
            Transform(i_vec, Arrow(origin, axes.c2p(1,0), color=RED, stroke_width=3, buff=0)),
            Transform(j_vec, Arrow(origin, axes.c2p(0,1), color=GREEN, stroke_width=3, buff=0)),
            Transform(i_label, Text("i", font_size=28, color=RED, weight=BOLD).next_to(axes.c2p(1,0), DOWN, buff=0.12)),
            Transform(j_label, Text("j", font_size=28, color=GREEN, weight=BOLD).next_to(axes.c2p(0,1), LEFT, buff=0.12)),
            Transform(square, Polygon(origin, axes.c2p(1,0), axes.c2p(1,1), axes.c2p(0,1),
                         fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=2)),
            Transform(orig_labels, make_vertex_labels([[1,0],[0,1]])),
            FadeOut(sc_tex), FadeOut(sc_text),
            run_time=1,
        )

        # ================================================================
        # 镜06：水平剪切
        # ================================================================
        sh_mat = [[1, 1], [0, 1]]

        sh_tex = MathTex(
            "H = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}", color=ORANGE,
        ).scale(0.75).to_edge(UP, buff=0.3).to_edge(RIGHT, buff=0.5)
        sh_text = Text("水平剪切", font=CN, font_size=20, color=ORANGE)
        sh_text.next_to(sh_tex, DOWN, buff=0.2)

        self.play(FadeIn(sh_tex), FadeIn(sh_text), run_time=0.8)
        self.wait(0.5)

        # 剪切后 i/j 标签跟随
        ni_sh = make_arrow(sh_mat, (1,0), RED)
        nj_sh = make_arrow(sh_mat, (0,1), GREEN)
        nil_sh = Text("i", font_size=28, color=RED, weight=BOLD).next_to(ni_sh.get_end(), DOWN, buff=0.12)
        njl_sh = Text("j", font_size=28, color=GREEN, weight=BOLD).next_to(nj_sh.get_end(), LEFT, buff=0.12)

        self.play(
            Transform(i_vec, ni_sh), Transform(j_vec, nj_sh),
            Transform(i_label, nil_sh), Transform(j_label, njl_sh),
            Transform(square, make_square(sh_mat)),
            Transform(orig_labels, make_vertex_labels(sh_mat)),
            run_time=2,
        )
        self.wait(2)

        # 恢复并清场
        self.play(
            *[FadeOut(m) for m in [i_vec, j_vec, i_label, j_label, square, orig_labels,
                                    axes, x_label, y_label, ticks]],
            FadeOut(sh_tex), FadeOut(sh_text),
            run_time=0.8,
        )

        # ================================================================
        # 镜07：三种变换对比（每个场景独立坐标系）
        # ================================================================
        def make_scene(mat, label_text, color):
            """创建一个变换对比小场景"""
            ax = Axes(
                x_range=[-1, 3, 1], y_range=[-1, 3, 1],
                x_length=3, y_length=3,
                axis_config={"stroke_width": 1, "color": DARK_GRAY},
            )
            # 用小坐标系自己的 c2p 来计算变换后的位置
            def small_tp(point):
                x, y = point
                nx = mat[0][0]*x + mat[0][1]*y
                ny = mat[1][0]*x + mat[1][1]*y
                return ax.c2p(nx, ny)

            # 原始正方形（灰色虚线）
            orig = DashedVMobject(Polygon(
                ax.c2p(0,0), ax.c2p(1,0), ax.c2p(1,1), ax.c2p(0,1),
                stroke_color=GRAY, stroke_width=1.5, fill_opacity=0,
            ), num_dashes=20)
            # 变换后正方形
            trans = Polygon(
                small_tp((0,0)), small_tp((1,0)), small_tp((1,1)), small_tp((0,1)),
                fill_color=color, fill_opacity=0.3,
                stroke_color=color, stroke_width=2,
            )

            label = Text(label_text, font=CN, font_size=18, color=color)
            label.next_to(ax, DOWN, buff=0.15)

            mat_display = MathTex(
                f"\\begin{{bmatrix}} {mat[0][0]} & {mat[0][1]} \\\\ {mat[1][0]} & {mat[1][1]} \\end{{bmatrix}}",
                color=color,
            ).scale(0.45).next_to(label, DOWN, buff=0.1)

            return VGroup(ax, orig, trans, label, mat_display)

        compare_title = Text("三种线性变换对比", font=CN, font_size=28, color=YELLOW)
        compare_title.to_edge(UP, buff=0.3)

        # 每个场景：坐标系 + 正方形 编成一组，这样移动坐标系时正方形跟着动
        def make_base_scene():
            ax = Axes(
                x_range=[-1, 3, 1], y_range=[-1, 3, 1],
                x_length=3, y_length=3,
                axis_config={"stroke_width": 1, "color": DARK_GRAY},
            )
            sq = Polygon(
                ax.c2p(0,0), ax.c2p(1,0), ax.c2p(1,1), ax.c2p(0,1),
                stroke_color=GRAY, stroke_width=1.5, fill_color=GRAY, fill_opacity=0.15,
            )
            return VGroup(ax, sq), ax, sq

        scene1, ax1, sq1 = make_base_scene()
        scene2, ax2, sq2 = make_base_scene()
        scene3, ax3, sq3 = make_base_scene()

        # 三个场景水平排列
        all_scenes = VGroup(scene1, scene2, scene3).arrange(RIGHT, buff=0.8)
        all_scenes.move_to(UP * 0.3)

        l1 = Text("旋转 90°", font=CN, font_size=16, color=RED).next_to(scene1, DOWN, buff=0.15)
        l2 = Text("缩放 2倍", font=CN, font_size=16, color=GREEN).next_to(scene2, DOWN, buff=0.15)
        l3 = Text("水平剪切", font=CN, font_size=16, color=ORANGE).next_to(scene3, DOWN, buff=0.15)

        self.play(FadeIn(compare_title, run_time=0.5))
        self.play(
            FadeIn(scene1), FadeIn(scene2), FadeIn(scene3),
            FadeIn(l1), FadeIn(l2), FadeIn(l3),
            run_time=1,
        )
        self.wait(1)

        # 变换动画：逐个变换正方形
        def small_tp(ax, mat, point):
            x, y = point
            return ax.c2p(mat[0][0]*x + mat[0][1]*y, mat[1][0]*x + mat[1][1]*y)

        # 变换1：旋转
        t1 = Polygon(
            small_tp(ax1, [[0,-1],[1,0]], (0,0)),
            small_tp(ax1, [[0,-1],[1,0]], (1,0)),
            small_tp(ax1, [[0,-1],[1,0]], (1,1)),
            small_tp(ax1, [[0,-1],[1,0]], (0,1)),
            fill_color=RED, fill_opacity=0.3, stroke_color=RED, stroke_width=2,
        )
        self.play(Transform(sq1, t1), run_time=1.5)

        # 变换2：缩放
        t2 = Polygon(
            small_tp(ax2, [[2,0],[0,2]], (0,0)),
            small_tp(ax2, [[2,0],[0,2]], (1,0)),
            small_tp(ax2, [[2,0],[0,2]], (1,1)),
            small_tp(ax2, [[2,0],[0,2]], (0,1)),
            fill_color=GREEN, fill_opacity=0.3, stroke_color=GREEN, stroke_width=2,
        )
        self.play(Transform(sq2, t2), run_time=1.5)

        # 变换3：剪切
        t3 = Polygon(
            small_tp(ax3, [[1,1],[0,1]], (0,0)),
            small_tp(ax3, [[1,1],[0,1]], (1,0)),
            small_tp(ax3, [[1,1],[0,1]], (1,1)),
            small_tp(ax3, [[1,1],[0,1]], (0,1)),
            fill_color=ORANGE, fill_opacity=0.3, stroke_color=ORANGE, stroke_width=2,
        )
        self.play(Transform(sq3, t3), run_time=1.5)

        summary = Text("矩阵 = 线性变换", font=CN, font_size=24, color=YELLOW)
        summary.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(summary, shift=UP*0.2, run_time=0.8))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜08：矩阵乘法 = 变换复合（先 R 再 S）
        # ================================================================
        # 用一个坐标系，分步演示
        comp_ax = Axes(
            x_range=[-3,4,1], y_range=[-3,4,1], x_length=7, y_length=7,
            axis_config={"stroke_width":1, "color": DARK_GRAY},
        )
        comp_title = Text("先旋转R，再缩放S", font=CN, font_size=28, color=YELLOW)
        comp_title.to_edge(UP, buff=0.3)

        self.play(Create(comp_ax), FadeIn(comp_title), run_time=1)

        # 小坐标系里的 tp
        def ctp(mat, point):
            x, y = point
            return comp_ax.c2p(mat[0][0]*x + mat[0][1]*y, mat[1][0]*x + mat[1][1]*y)

        # 原始正方形
        origin_c = comp_ax.c2p(0,0)
        orig_sq = Polygon(
            origin_c, comp_ax.c2p(1,0), comp_ax.c2p(1,1), comp_ax.c2p(0,1),
            fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=2,
        )
        orig_label = Text("原始", font=CN, font_size=18, color=GRAY)
        orig_label.next_to(orig_sq, DOWN, buff=0.1)

        self.play(Create(orig_sq), FadeIn(orig_label), run_time=0.8)

        # 第一步：旋转 R = [[0,-1],[1,0]]
        R_mat = [[0, -1], [1, 0]]
        r_label = MathTex("R = \\begin{bmatrix} 0 & -1 \\\\ 1 & 0 \\end{bmatrix}", color=RED).scale(0.6)
        r_label.to_edge(RIGHT, buff=0.5).shift(UP*1)

        rotated_sq = Polygon(
            origin_c, ctp(R_mat,(1,0)), ctp(R_mat,(1,1)), ctp(R_mat,(0,1)),
            fill_color=RED, fill_opacity=0.3, stroke_color=RED, stroke_width=2,
        )

        step1 = Text("第1步：旋转 90°", font=CN, font_size=20, color=RED)
        step1.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(r_label), FadeIn(step1), run_time=0.5)
        self.play(Transform(orig_sq, rotated_sq), run_time=2)
        self.wait(1.5)

        # 第二步：缩放 S = [[2,0],[0,2]] 作用在旋转后的结果上
        S_mat = [[2, 0], [0, 2]]
        # 复合：先 R 再 S = S·R
        SR_mat = [[S_mat[0][0]*R_mat[0][0]+S_mat[0][1]*R_mat[1][0],
                    S_mat[0][0]*R_mat[0][1]+S_mat[0][1]*R_mat[1][1]],
                   [S_mat[1][0]*R_mat[0][0]+S_mat[1][1]*R_mat[1][0],
                    S_mat[1][0]*R_mat[0][1]+S_mat[1][1]*R_mat[1][1]]]

        s_label = MathTex("S = \\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}", color=GREEN).scale(0.6)
        s_label.next_to(r_label, DOWN, buff=0.4)

        final_sq = Polygon(
            origin_c, ctp(SR_mat,(1,0)), ctp(SR_mat,(1,1)), ctp(SR_mat,(0,1)),
            fill_color=GREEN, fill_opacity=0.3, stroke_color=GREEN, stroke_width=2,
        )

        step2 = Text("第2步：缩放 2倍", font=CN, font_size=20, color=GREEN)
        step2.to_edge(DOWN, buff=0.5)

        self.play(FadeOut(step1), FadeIn(s_label), FadeIn(step2), run_time=0.5)
        self.play(Transform(orig_sq, final_sq), run_time=2)
        self.wait(1.5)

        # 显示复合结果
        sr_label = MathTex("S \\cdot R = \\begin{bmatrix} 0 & -2 \\\\ 2 & 0 \\end{bmatrix}", color=YELLOW).scale(0.6)
        sr_label.next_to(s_label, DOWN, buff=0.4)

        result_label = Text("结果：旋转+缩放 = 复合变换", font=CN, font_size=20, color=YELLOW)
        result_label.to_edge(DOWN, buff=0.5)

        self.play(FadeOut(step2), FadeIn(sr_label), FadeIn(result_label), run_time=0.8)
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜09：行乘列计算规则
        # ================================================================
        title9 = Text("矩阵乘法的计算规则", font=CN, font_size=32, color=YELLOW)
        title9.to_edge(UP, buff=0.4)
        self.play(FadeIn(title9, run_time=0.8))

        calc_steps = VGroup(
            MathTex("(S \\cdot R)_{11} = 2 \\times 0 + 0 \\times 1 = 0", color=WHITE),
            MathTex("(S \\cdot R)_{12} = 2 \\times (-1) + 0 \\times 0 = -2", color=WHITE),
            MathTex("(S \\cdot R)_{21} = 0 \\times 0 + 2 \\times 1 = 2", color=WHITE),
            MathTex("(S \\cdot R)_{22} = 0 \\times (-1) + 2 \\times 0 = 0", color=WHITE),
        ).scale(0.65)
        calc_steps.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        calc_steps.move_to(ORIGIN)

        for step in calc_steps:
            self.play(FadeIn(step, shift=RIGHT*0.2, run_time=0.7))
            self.wait(0.8)

        rule = Text("行 × 列 = 对应元素乘积之和", font=CN, font_size=22, color=GREEN)
        rule.to_edge(DOWN, buff=0.4)
        rule_box = SurroundingRectangle(rule, color=GREEN, buff=0.15)
        self.play(FadeIn(rule, shift=UP*0.2, run_time=0.8))
        self.play(Create(rule_box, run_time=0.5))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜10：总结
        # ================================================================
        core1 = VGroup(
            Text("矩阵", font=CN, font_size=28, color=BLUE),
            MathTex("\\leftrightarrow", color=GRAY).scale(0.8),
            Text("线性变换", font=CN, font_size=28, color=BLUE),
        ).arrange(RIGHT, buff=0.2)

        core2 = VGroup(
            Text("矩阵乘法", font=CN, font_size=28, color=GREEN),
            MathTex("\\leftrightarrow", color=GRAY).scale(0.8),
            Text("变换复合", font=CN, font_size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.2)

        core = VGroup(core1, core2).arrange(DOWN, buff=0.5).move_to(UP*0.5)

        self.play(FadeIn(core1, shift=UP*0.3, run_time=1))
        self.wait(1)
        self.play(FadeIn(core2, shift=UP*0.3, run_time=1))
        self.wait(2)

        end = Text("下次看到矩阵乘法，想想它在变换什么", font=CN, font_size=24, color=YELLOW)
        end.next_to(core, DOWN, buff=0.8)
        self.play(FadeIn(end, shift=UP*0.2, run_time=1))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

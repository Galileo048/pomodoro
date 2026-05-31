"""
第5期：曼德勃罗集的无限之美
时长：约8分钟 | 13镜
知识点：分形几何、曼德勃罗集、朱利亚集 | 难度：⭐⭐⭐⭐
讲解重点：迭代定义、具体计算、放大探索、朱利亚集、科赫雪花、谢尔宾斯基三角形

渲染注意：镜06-08需要 NumPy + PIL 计算像素，渲染较慢
"""
from manim import *
import numpy as np
from PIL import Image
import os

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


def mandelbrot_image(x_min, x_max, y_min, y_max, width=800, height=600, max_iter=100):
    """计算曼德勃罗集像素图像，返回 PIL Image"""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=float)

    mask = np.ones(C.shape, dtype=bool)
    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]
        escaped = mask & (np.abs(Z) > 2)
        iterations[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
        mask[escaped] = False

    # 着色：发散的点按迭代次数着色，不发散的点为黑色
    colors = np.zeros((*C.shape, 3), dtype=np.uint8)
    valid = iterations > 0
    t = iterations[valid] / max_iter
    colors[valid, 0] = (9 * (1-t) * t**3 * 255).astype(np.uint8)
    colors[valid, 1] = (15 * (1-t)**2 * t**2 * 255).astype(np.uint8)
    colors[valid, 2] = (8.5 * (1-t)**3 * t * 255).astype(np.uint8)

    return Image.fromarray(colors)


class MandelbrotScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── 镜01：标题 ──
        title = Text("曼德勃罗集的无限之美", font=CN, font_size=44, color=WHITE)
        subtitle = Text("分形几何的奇迹", font=CN, font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title, run_time=2))
        self.play(FadeIn(subtitle, shift=UP*0.2, run_time=1))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ── 镜02：复平面 ──
        plane = ComplexPlane(
            x_range=[-2.5, 1, 0.5], y_range=[-1.5, 1.5, 0.5],
            x_length=9, y_length=6,
            background_line_style={"stroke_color": DARK_GRAY, "stroke_width": 0.5},
            axis_config={"stroke_color": GRAY, "stroke_width": 1.5},
        )
        re_label = Text("Re", font_size=20, color=GRAY).next_to(plane.get_right(), DOWN, buff=0.15)
        im_label = Text("Im", font_size=20, color=GRAY).next_to(plane.get_top(), LEFT, buff=0.15)

        self.play(Create(plane, run_time=1.5))
        self.play(FadeIn(re_label), FadeIn(im_label), run_time=0.5)

        info = Text("复平面上每个点 c，进行迭代：z = z² + c", font=CN, font_size=20, color=GRAY)
        info.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(info, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(FadeOut(info), run_time=0.5)

        # ── 镜03：迭代公式展开 ──
        self.play(FadeOut(plane), FadeOut(re_label), FadeOut(im_label), run_time=0.5)

        formulas = VGroup(
            MathTex("z_0 = 0", color=WHITE),
            MathTex("z_1 = 0^2 + c = c", color=WHITE),
            MathTex("z_2 = c^2 + c", color=WHITE),
            MathTex("z_3 = (c^2 + c)^2 + c", color=WHITE),
        ).scale(0.75)
        formulas.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        formulas.move_to(ORIGIN)

        for form in formulas:
            self.play(FadeIn(form, shift=RIGHT*0.3, run_time=0.8))
            self.wait(1)

        rule = Text("若 |zₙ| 始终 ≤ 2 → c 属于曼德勃罗集", font=CN, font_size=20, color=GREEN)
        rule.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rule, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜04：具体例子 c = 0.3 + 0.5i（收敛）──
        ex_title = Text("例1: c = 0.3 + 0.5i", font=CN, font_size=24, color=BLUE)
        ex_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(ex_title, run_time=0.5))

        # 计算迭代
        c = 0.3 + 0.5j
        z = 0
        iter_texts = VGroup()
        for i in range(6):
            z = z**2 + c
            txt = MathTex(f"z_{i+1} = {z.real:.3f} {z.imag:+.3f}i", color=WHITE).scale(0.65)
            iter_texts.add(txt)
        iter_texts.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        iter_texts.move_to(ORIGIN)

        for t in iter_texts:
            self.play(FadeIn(t, shift=RIGHT*0.2, run_time=0.5))
            self.wait(0.5)

        conv_text = Text("|zₙ| 始终 ≤ 2 → 收敛！属于集合", font=CN, font_size=20, color=GREEN)
        conv_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(conv_text, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜05：c = 1（发散）──
        ex2_title = Text("例2: c = 1", font=CN, font_size=24, color=RED)
        ex2_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(ex2_title, run_time=0.5))

        c2 = 1
        z2 = 0
        iter_texts2 = VGroup()
        for i in range(5):
            z2 = z2**2 + c2
            txt = MathTex(f"z_{i+1} = {z2}", color=RED if z2 > 2 else WHITE).scale(0.65)
            iter_texts2.add(txt)
        iter_texts2.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        iter_texts2.move_to(ORIGIN)

        for t in iter_texts2:
            self.play(FadeIn(t, shift=RIGHT*0.2, run_time=0.5))
            self.wait(0.5)

        div_text = Text("|zₙ| → ∞ → 发散！不属于集合", font=CN, font_size=20, color=RED)
        div_text.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(div_text, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜06：曼德勃罗集全貌渲染 ──
        render_text = Text("渲染曼德勃罗集...", font=CN, font_size=24, color=GRAY)
        self.play(FadeIn(render_text, run_time=0.5))

        # 计算像素图像
        img = mandelbrot_image(-2.5, 1.0, -1.5, 1.5, width=800, height=600, max_iter=100)
        img_path = os.path.join(os.path.dirname(__file__), "temp_mandelbrot.png")
        img.save(img_path)

        self.play(FadeOut(render_text), run_time=0.3)

        # 显示图像
        mb_img = ImageMobject(img_path)
        mb_img.set_height(5.5)
        self.play(FadeIn(mb_img, scale=0.9, run_time=2))
        self.wait(2)

        # ── 镜07-08：放大动画 ──
        # 放大到边界区域
        zoom_targets = [
            (-0.745, 0.186, 0.5),   # 第1次放大
            (-0.7436, 0.1319, 0.05), # 第2次放大
            (-0.74364, 0.13171, 0.005), # 第3次放大
        ]

        for zx, zy, scale in zoom_targets:
            # 计算放大区域
            w = 3.5 * scale
            h = 2.5 * scale
            zoom_img = mandelbrot_image(zx-w, zx+w, zy-h, zy+h, width=800, height=600, max_iter=200)
            zoom_path = os.path.join(os.path.dirname(__file__), "temp_zoom.png")
            zoom_img.save(zoom_path)

            new_mb = ImageMobject(zoom_path)
            new_mb.set_height(5.5)

            # 放大倍数标注
            mag = int(3.5 / (2*w)) if w > 0 else 1
            mag_text = Text(f"×{mag}", font_size=28, color=YELLOW)
            mag_text.to_corner(UR, buff=0.3)

            self.play(
                FadeOut(mb_img), FadeIn(new_mb, run_time=1.5),
                FadeIn(mag_text, run_time=0.5),
            )
            mb_img = new_mb
            self.wait(1.5)
            self.play(FadeOut(mag_text), run_time=0.3)

        # ── 镜09：朱利亚集对比 ──
        self.play(FadeOut(mb_img), run_time=0.5)

        julia_title = Text("朱利亚集 vs 曼德勃罗集", font=CN, font_size=28, color=YELLOW)
        julia_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(julia_title, run_time=0.5))

        # 计算两个朱利亚集
        def julia_image(c_val, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5, width=400, height=400, max_iter=100):
            x = np.linspace(x_min, x_max, width)
            y = np.linspace(y_min, y_max, height)
            Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
            C = np.full(Z.shape, c_val)
            iterations = np.zeros(Z.shape, dtype=float)
            mask = np.ones(Z.shape, dtype=bool)
            for i in range(max_iter):
                Z[mask] = Z[mask]**2 + C[mask]
                escaped = mask & (np.abs(Z) > 2)
                iterations[escaped] = i + 1
                mask[escaped] = False
            colors = np.zeros((*Z.shape, 3), dtype=np.uint8)
            valid = iterations > 0
            t = iterations[valid] / max_iter
            colors[valid, 0] = (9*(1-t)*t**3*255).astype(np.uint8)
            colors[valid, 1] = (15*(1-t)**2*t**2*255).astype(np.uint8)
            colors[valid, 2] = (8.5*(1-t)**3*t*255).astype(np.uint8)
            return Image.fromarray(colors)

        # c 在曼德勃罗集内 → 连通
        j1 = julia_image(-0.7 + 0.27015j)
        j1_path = os.path.join(os.path.dirname(__file__), "temp_julia1.png")
        j1.save(j1_path)
        j1_img = ImageMobject(j1_path).set_height(3)
        j1_label = Text("c 在集合内 → 连通", font=CN, font_size=16, color=GREEN)
        j1_label.next_to(j1_img, DOWN, buff=0.1)
        j1_group = Group(j1_img, j1_label).shift(LEFT*3)

        # c 在曼德勃罗集外 → 碎片
        j2 = julia_image(0.355 + 0.355j)
        j2_path = os.path.join(os.path.dirname(__file__), "temp_julia2.png")
        j2.save(j2_path)
        j2_img = ImageMobject(j2_path).set_height(3)
        j2_label = Text("c 在集合外 → 碎片", font=CN, font_size=16, color=RED)
        j2_label.next_to(j2_img, DOWN, buff=0.1)
        j2_group = Group(j2_img, j2_label).shift(RIGHT*3)

        self.play(
            FadeIn(j1_group, shift=UP*0.3, run_time=1),
            FadeIn(j2_group, shift=UP*0.3, run_time=1),
        )
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜10：科赫雪花 ──
        koch_title = Text("科赫雪花", font=CN, font_size=28, color=YELLOW)
        koch_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(koch_title, run_time=0.5))

        def koch_points(p1, p2, order):
            """递归生成科赫曲线点，输入输出都是 numpy 3D 数组"""
            if order == 0:
                return [p1, p2]
            d = p2 - p1
            a = p1 + d/3
            b = p1 + 2*d/3
            # 等边三角形顶点：把 (x,y) 当复数旋转 -60°
            dx, dy = d[0], d[1]
            cos_a, sin_a = np.cos(-PI/3), np.sin(-PI/3)
            # 从 a 出发，沿 d/3 旋转得到 tip
            rel = (b - a)
            tip_x = a[0] + rel[0]*cos_a - rel[1]*sin_a
            tip_y = a[1] + rel[0]*sin_a + rel[1]*cos_a
            tip = np.array([tip_x, tip_y, 0])
            pts = []
            pts += koch_points(p1, a, order-1)[:-1]
            pts += koch_points(a, tip, order-1)[:-1]
            pts += koch_points(tip, b, order-1)[:-1]
            pts += koch_points(b, p2, order-1)
            return pts

        # 等边三角形三个顶点
        r = 2.5
        v1 = np.array([r*np.cos(PI/2), r*np.sin(PI/2), 0])
        v2 = np.array([r*np.cos(PI/2 + 2*PI/3), r*np.sin(PI/2 + 2*PI/3), 0])
        v3 = np.array([r*np.cos(PI/2 + 4*PI/3), r*np.sin(PI/2 + 4*PI/3), 0])

        # 逐代显示
        for order in range(5):
            pts = []
            pts += koch_points(v1, v2, order)[:-1]
            pts += koch_points(v2, v3, order)[:-1]
            pts += koch_points(v3, v1, order)[:-1]
            pts.append(pts[0])

            koch_poly = VMobject(color=BLUE, stroke_width=1.5)
            koch_poly.set_points_as_corners(pts)
            koch_poly.shift(DOWN*0.3)

            gen_text = Text(f"第{order}代", font=CN, font_size=20, color=GRAY)
            gen_text.to_edge(DOWN, buff=0.3)

            if order == 0:
                self.play(Create(koch_poly, run_time=1.5), FadeIn(gen_text), run_time=0.5)
            else:
                self.play(Transform(prev_koch, koch_poly), FadeOut(prev_gen), FadeIn(gen_text), run_time=1)

            prev_koch = koch_poly
            prev_gen = gen_text
            self.wait(0.8)

        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects if m != koch_title], run_time=0.8)

        # ── 镜11：谢尔宾斯基三角形 ──
        self.play(FadeOut(koch_title), run_time=0.3)

        sierp_title = Text("谢尔宾斯基三角形", font=CN, font_size=28, color=YELLOW)
        sierp_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(sierp_title, run_time=0.5))

        def sierpinski_triangles(order, v1, v2, v3):
            """递归生成谢尔宾斯基三角形"""
            if order == 0:
                return [Polygon(v1, v2, v3, fill_color=BLUE, fill_opacity=0.5,
                               stroke_color=BLUE, stroke_width=1)]
            m1 = (v1 + v2) / 2
            m2 = (v2 + v3) / 2
            m3 = (v1 + v3) / 2
            tris = []
            tris += sierpinski_triangles(order-1, v1, m1, m3)
            tris += sierpinski_triangles(order-1, m1, v2, m2)
            tris += sierpinski_triangles(order-1, m3, m2, v3)
            return tris

        sv1 = np.array([0, 2.5, 0])
        sv2 = np.array([-2.5, -1.5, 0])
        sv3 = np.array([2.5, -1.5, 0])

        prev_sierp = None
        for order in range(5):
            tris = sierpinski_triangles(order, sv1, sv2, sv3)
            sierp_group = VGroup(*tris).shift(DOWN*0.3)

            gen_text = Text(f"第{order}代", font=CN, font_size=20, color=GRAY)
            gen_text.to_edge(DOWN, buff=0.3)

            if order == 0:
                self.play(FadeIn(sierp_group, run_time=1), FadeIn(gen_text), run_time=0.5)
            else:
                self.play(
                    FadeOut(prev_sierp), FadeIn(sierp_group, run_time=1),
                    FadeOut(prev_gen), FadeIn(gen_text),
                    run_time=1,
                )

            prev_sierp = sierp_group
            prev_gen = gen_text
            self.wait(0.8)

        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜12：分形特征总结 ──
        features = VGroup(
            Text("自相似性：局部与整体相似", font=CN, font_size=22, color=BLUE),
            Text("分数维：维度不是整数", font=CN, font_size=22, color=GREEN),
            Text("无限细节：永远有新结构", font=CN, font_size=22, color=YELLOW),
            Text("简单规则 → 复杂结果", font=CN, font_size=22, color=RED),
        ).arrange(DOWN, buff=0.4)
        features.move_to(ORIGIN)

        for feat in features:
            self.play(FadeIn(feat, shift=RIGHT*0.3, run_time=0.8))
            self.wait(1)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ── 镜13：结束 ──
        end = Text("数学之美，在于简单中蕴含无穷", font=CN, font_size=32, color=YELLOW)
        self.play(FadeIn(end, shift=UP*0.3, run_time=1.5))
        self.wait(3)
        self.play(FadeOut(end, run_time=1.5))


# ================================================================
# 渲染入口
# ================================================================
# 2D场景：python -m manim render -ql 动画源码/第5期_曼德勃罗集.py MandelbrotScene
# 注意：镜06-08的像素计算可能需要 30-60 秒

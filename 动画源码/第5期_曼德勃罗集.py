"""
第5期：曼德勃罗集的无限之美
时长：约8分钟 | 13镜
知识点：分形几何、曼德勃罗集、朱利亚集 | 难度：⭐⭐⭐⭐
讲解重点：迭代定义、具体计算、放大探索、朱利亚集、科赫雪花、谢尔宾斯基三角形

v2: 改进着色方案 + 放大动画 + 分形构造
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
PURPLE = "#bc8cff"

CN = "Microsoft YaHei"

# 3b1b 九色调色板
COLORS_3B1B = [
    (0, 6, 92),     # #00065c  深蓝
    (6, 30, 126),   # #061e7e
    (12, 55, 160),  # #0c37a0
    (32, 90, 188),  # #205abc
    (66, 135, 211), # #4287d3
    (217, 237, 228),# #D9EDE4  浅青
    (240, 249, 228),# #F0F9E4
    (186, 159, 106),# #BA9F6A  暖棕
    (87, 55, 6),    # #573706  深棕
]


def mandelbrot_image(x_min, x_max, y_min, y_max, width=800, height=600, max_iter=100):
    """计算曼德勃罗集像素图像，使用3b1b着色方案"""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]
        escaped = mask & (np.abs(Z) > 2)
        # 平滑迭代计数（3b1b 的 log技巧，消除色带）
        if np.any(escaped):
            iterations[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped]) + 1e-10))
        mask[escaped] = False

    # 3b1b 九色渐变着色
    colors = np.zeros((*C.shape, 3), dtype=np.uint8)
    valid = iterations > 0
    t = (iterations[valid] / max_iter) ** 0.5  # sqrt 缩放，让细节更丰富

    # 九色分段插值
    n_colors = len(COLORS_3B1B)
    for ch in range(3):
        color_values = np.array([c[ch] for c in COLORS_3B1B], dtype=float)
        # 将 t 映射到颜色梯度
        idx = t * (n_colors - 1)
        idx_low = np.clip(np.floor(idx).astype(int), 0, n_colors - 2)
        idx_high = idx_low + 1
        frac = idx - idx_low
        colors[valid, ch] = (
            color_values[idx_low] * (1 - frac) + color_values[idx_high] * frac
        ).astype(np.uint8)

    # 不发散的点为黑色
    return Image.fromarray(colors)


def julia_image(c_val, x_min=-1.5, x_max=1.5, y_min=-1.5, y_max=1.5,
                width=400, height=400, max_iter=100):
    """计算朱利亚集像素图像"""
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    Z = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    C = np.full(Z.shape, c_val)
    iterations = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]
        escaped = mask & (np.abs(Z) > 2)
        if np.any(escaped):
            iterations[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped]) + 1e-10))
        mask[escaped] = False

    colors = np.zeros((*Z.shape, 3), dtype=np.uint8)
    valid = iterations > 0
    t = (iterations[valid] / max_iter) ** 0.5
    n_colors = len(COLORS_3B1B)
    for ch in range(3):
        color_values = np.array([c[ch] for c in COLORS_3B1B], dtype=float)
        idx = t * (n_colors - 1)
        idx_low = np.clip(np.floor(idx).astype(int), 0, n_colors - 2)
        idx_high = idx_low + 1
        frac = idx - idx_low
        colors[valid, ch] = (
            color_values[idx_low] * (1 - frac) + color_values[idx_high] * frac
        ).astype(np.uint8)
    return Image.fromarray(colors)


class MandelbrotScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        temp_dir = os.path.dirname(os.path.abspath(__file__))

        # ================================================================
        # 镜01：标题
        # ================================================================
        title = Text("曼德勃罗集的无限之美", font=CN, font_size=44, color=WHITE)
        subtitle = Text("分形几何的奇迹", font=CN, font_size=24, color=PURPLE)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(title, run_time=2))
        self.play(FadeIn(subtitle, shift=UP*0.2, run_time=1))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # ================================================================
        # 镜02：复平面
        # ================================================================
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
        self.play(FadeOut(info), FadeOut(plane), FadeOut(re_label), FadeOut(im_label), run_time=0.8)

        # ================================================================
        # 镜03：迭代公式展开
        # ================================================================
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

        rule = VGroup(
            Text("若 |zₙ| 始终 ≤ 2 → ", font=CN, font_size=20, color=WHITE),
            Text("属于集合", font=CN, font_size=20, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        rule.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(rule, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜04：例1 c=0.3+0.5i（收敛）
        # ================================================================
        ex1_title = Text("例1: c = 0.3 + 0.5i", font=CN, font_size=24, color=BLUE)
        ex1_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(ex1_title, run_time=0.5))

        c = 0.3 + 0.5j
        z = 0
        iter_group = VGroup()
        for i in range(6):
            z = z**2 + c
            txt = MathTex(f"z_{i+1} = {z.real:.3f} {z.imag:+.3f}i", color=WHITE).scale(0.65)
            iter_group.add(txt)
        iter_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        iter_group.move_to(ORIGIN)

        for t in iter_group:
            self.play(FadeIn(t, shift=RIGHT*0.2, run_time=0.5))
            self.wait(0.5)

        conv = VGroup(
            Text("|zₙ| 始终 ≤ 2 → ", font=CN, font_size=20, color=WHITE),
            Text("收敛！属于集合", font=CN, font_size=20, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        conv.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(conv, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜05：例2 c=1（发散）
        # ================================================================
        ex2_title = Text("例2: c = 1", font=CN, font_size=24, color=RED)
        ex2_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(ex2_title, run_time=0.5))

        c2 = 1
        z2 = 0
        iter_group2 = VGroup()
        for i in range(5):
            z2 = z2**2 + c2
            color = RED if z2 > 2 else WHITE
            txt = MathTex(f"z_{i+1} = {z2}", color=color).scale(0.65)
            iter_group2.add(txt)
        iter_group2.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        iter_group2.move_to(ORIGIN)

        for t in iter_group2:
            self.play(FadeIn(t, shift=RIGHT*0.2, run_time=0.5))
            self.wait(0.5)

        div = VGroup(
            Text("|zₙ| → ∞ → ", font=CN, font_size=20, color=WHITE),
            Text("发散！不属于集合", font=CN, font_size=20, color=RED),
        ).arrange(RIGHT, buff=0.1)
        div.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(div, shift=UP*0.2, run_time=0.8))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜06：曼德勃罗集全貌渲染
        # ================================================================
        render_txt = Text("渲染曼德勃罗集...", font=CN, font_size=24, color=GRAY)
        self.play(FadeIn(render_txt, run_time=0.5))

        img = mandelbrot_image(-2.5, 1.0, -1.5, 1.5, width=800, height=600, max_iter=100)
        img_path = os.path.join(temp_dir, "temp_mb_full.png")
        img.save(img_path)

        self.play(FadeOut(render_txt), run_time=0.3)

        mb_img = ImageMobject(img_path).set_height(5.5)
        self.play(FadeIn(mb_img, scale=0.9, run_time=2))
        self.wait(2)

        # ================================================================
        # 镜07-08：放大动画
        # ================================================================
        zoom_targets = [
            (-0.745, 0.186, 0.5, 3),
            (-0.7436, 0.1319, 0.05, 30),
            (-0.74364, 0.13171, 0.005, 300),
            (-0.743643, 0.131715, 0.0005, 3000),
        ]

        for zx, zy, scale, mag in zoom_targets:
            w = 3.5 * scale
            h = 2.5 * scale
            zoom_img = mandelbrot_image(zx-w, zx+w, zy-h, zy+h, width=800, height=600, max_iter=min(200 + mag//10, 500))
            zoom_path = os.path.join(temp_dir, f"temp_zoom_{mag}.png")
            zoom_img.save(zoom_path)

            new_mb = ImageMobject(zoom_path).set_height(5.5)

            mag_label = VGroup(
                Text("×", font_size=24, color=YELLOW),
                Text(f"{mag}", font_size=28, color=YELLOW),
            ).arrange(RIGHT, buff=0.05)
            mag_label.to_corner(UR, buff=0.3)

            self.play(FadeOut(mb_img), run_time=0.3)
            self.play(FadeIn(new_mb, run_time=1.5), FadeIn(mag_label, run_time=0.5))
            mb_img = new_mb
            self.wait(1.5)
            self.play(FadeOut(mag_label), run_time=0.3)

        self.play(FadeOut(mb_img), run_time=0.5)

        # ================================================================
        # 镜09：朱利亚集对比
        # ================================================================
        julia_title = Text("朱利亚集 vs 曼德勃罗集", font=CN, font_size=28, color=YELLOW)
        julia_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(julia_title, run_time=0.5))

        # c 在集合内 → 连通
        j1 = julia_image(-0.7 + 0.27015j)
        j1_path = os.path.join(temp_dir, "temp_julia1.png")
        j1.save(j1_path)
        j1_img = ImageMobject(j1_path).set_height(3)
        j1_label = VGroup(
            Text("c 在集合内 → ", font=CN, font_size=16, color=WHITE),
            Text("连通", font=CN, font_size=16, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        j1_label.next_to(j1_img, DOWN, buff=0.1)
        j1_group = Group(j1_img, j1_label).shift(LEFT*3)

        # c 在集合外 → 碎片
        j2 = julia_image(0.355 + 0.355j)
        j2_path = os.path.join(temp_dir, "temp_julia2.png")
        j2.save(j2_path)
        j2_img = ImageMobject(j2_path).set_height(3)
        j2_label = VGroup(
            Text("c 在集合外 → ", font=CN, font_size=16, color=WHITE),
            Text("碎片", font=CN, font_size=16, color=RED),
        ).arrange(RIGHT, buff=0.1)
        j2_label.next_to(j2_img, DOWN, buff=0.1)
        j2_group = Group(j2_img, j2_label).shift(RIGHT*3)

        self.play(
            FadeIn(j1_group, shift=UP*0.3, run_time=1),
            FadeIn(j2_group, shift=UP*0.3, run_time=1),
        )
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜10：科赫雪花（5代动画）
        # ================================================================
        koch_title = Text("科赫雪花", font=CN, font_size=28, color=YELLOW)
        koch_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(koch_title, run_time=0.5))

        def koch_points(p1, p2, order):
            """递归生成科赫曲线点"""
            if order == 0:
                return [p1, p2]
            d = p2 - p1
            a = p1 + d/3
            b = p1 + 2*d/3
            cos_a, sin_a = np.cos(-PI/3), np.sin(-PI/3)
            rel = b - a
            tip_x = a[0] + rel[0]*cos_a - rel[1]*sin_a
            tip_y = a[1] + rel[0]*sin_a + rel[1]*cos_a
            tip = np.array([tip_x, tip_y, 0])
            pts = []
            pts += koch_points(p1, a, order-1)[:-1]
            pts += koch_points(a, tip, order-1)[:-1]
            pts += koch_points(tip, b, order-1)[:-1]
            pts += koch_points(b, p2, order-1)
            return pts

        r = 2.5
        v1 = np.array([r*np.cos(PI/2), r*np.sin(PI/2), 0])
        v2 = np.array([r*np.cos(PI/2 + 2*PI/3), r*np.sin(PI/2 + 2*PI/3), 0])
        v3 = np.array([r*np.cos(PI/2 + 4*PI/3), r*np.sin(PI/2 + 4*PI/3), 0])

        prev_koch = None
        prev_gen = None
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
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜11：谢尔宾斯基三角形（5代）
        # ================================================================
        sierp_title = Text("谢尔宾斯基三角形", font=CN, font_size=28, color=YELLOW)
        sierp_title.to_edge(UP, buff=0.3)
        self.play(FadeIn(sierp_title, run_time=0.5))

        def sierpinski_tris(order, v1, v2, v3):
            """递归生成谢尔宾斯基三角形"""
            if order == 0:
                return [Polygon(v1, v2, v3, fill_color=BLUE, fill_opacity=0.5,
                               stroke_color=BLUE, stroke_width=1)]
            m1 = (v1 + v2) / 2
            m2 = (v2 + v3) / 2
            m3 = (v1 + v3) / 2
            tris = []
            tris += sierpinski_tris(order-1, v1, m1, m3)
            tris += sierpinski_tris(order-1, m1, v2, m2)
            tris += sierpinski_tris(order-1, m3, m2, v3)
            return tris

        sv1 = np.array([0, 2.5, 0])
        sv2 = np.array([-2.5, -1.5, 0])
        sv3 = np.array([2.5, -1.5, 0])

        prev_sierp = None
        prev_gen = None
        for order in range(5):
            tris = sierpinski_tris(order, sv1, sv2, sv3)
            sierp_group = VGroup(*tris).shift(DOWN*0.3)
            gen_text = Text(f"第{order}代", font=CN, font_size=20, color=GRAY)
            gen_text.to_edge(DOWN, buff=0.3)

            if order == 0:
                self.play(FadeIn(sierp_group, run_time=1), FadeIn(gen_text), run_time=0.5)
            else:
                self.play(FadeOut(prev_sierp), FadeIn(sierp_group, run_time=1),
                          FadeOut(prev_gen), FadeIn(gen_text), run_time=1)
            prev_sierp = sierp_group
            prev_gen = gen_text
            self.wait(0.8)

        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜12：分形特征总结
        # ================================================================
        features = VGroup(
            VGroup(
                Text("自相似性", font=CN, font_size=24, color=BLUE),
                Text(" — 局部与整体相似", font=CN, font_size=20, color=GRAY),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("分数维", font=CN, font_size=24, color=GREEN),
                Text(" — 维度不是整数", font=CN, font_size=20, color=GRAY),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("无限细节", font=CN, font_size=24, color=YELLOW),
                Text(" — 永远有新结构", font=CN, font_size=20, color=GRAY),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("简单规则", font=CN, font_size=24, color=RED),
                Text(" → 复杂结果", font=CN, font_size=20, color=GRAY),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.45)
        features.move_to(ORIGIN)

        for feat in features:
            self.play(FadeIn(feat, shift=RIGHT*0.3, run_time=0.8))
            self.wait(1)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

        # ================================================================
        # 镜13：结束
        # ================================================================
        end = Text("数学之美，在于简单中蕴含无穷", font=CN, font_size=32, color=YELLOW)
        self.play(FadeIn(end, shift=UP*0.3, run_time=1.5))
        self.wait(3)
        self.play(FadeOut(end, run_time=1.5))

        # 清理临时文件
        for f in ["temp_mb_full.png", "temp_julia1.png", "temp_julia2.png"]:
            try: os.remove(os.path.join(temp_dir, f))
            except: pass
        for f in os.listdir(temp_dir):
            if f.startswith("temp_zoom_"):
                try: os.remove(os.path.join(temp_dir, f))
                except: pass

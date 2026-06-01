"""
第6期：流动的几何（意识流抽象动画）
时长：约3分钟 | 14镜 | 5幕
风格：抽象 / 意识流 / 流体动态
"从虚无中诞生一个点，逐渐演化为线、面、体，最终化为混沌，再归于虚无"

v2: 全部改为2D，避免ThreeDScene渲染慢的问题
"""
from manim import *
import numpy as np
import random

# 配色
BG = "#0a0a0a"
RED = "#FF6B6B"
TEAL = "#4ECDC4"
BLUE = "#45B7D1"
MINT = "#96CEB4"
YELLOW = "#FFEAA7"
PLUM = "#DDA0DD"
WHITE = "#FFFFFF"
GOLD = "#FFD700"
PALETTE = [RED, TEAL, BLUE, MINT, PLUM]


class FlowingGeometry(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ================================================================
        # 第一幕：虚无中的觉醒（0:00-0:30）
        # ================================================================

        # ── 镜01：光点诞生 + 呼吸脉动（0:00-0:08）──
        core = Dot(ORIGIN, color=WHITE, radius=0.05)
        g1 = Dot(ORIGIN, color=WHITE, radius=0.15, fill_opacity=0.15, stroke_width=0)
        g2 = Dot(ORIGIN, color=BLUE, radius=0.3, fill_opacity=0.08, stroke_width=0)
        g3 = Dot(ORIGIN, color=TEAL, radius=0.5, fill_opacity=0.04, stroke_width=0)
        breath = VGroup(g3, g2, g1, core)

        self.play(FadeIn(breath, scale=0.1, run_time=2))
        for _ in range(3):
            self.play(breath.animate.scale(1.5).set_opacity(0.6),
                      run_time=1.2, rate_func=there_and_back)

        # ── 镜02：分裂 + 缠绕（0:08-0:18）──
        da = Dot(ORIGIN, color=TEAL, radius=0.08)
        db = Dot(ORIGIN, color=RED, radius=0.08)
        ta = TracedPath(da.get_center, stroke_color=TEAL, stroke_width=2, stroke_opacity=0.6)
        tb = TracedPath(db.get_center, stroke_color=RED, stroke_width=2, stroke_opacity=0.6)

        self.play(FadeOut(breath), run_time=0.5)
        self.add(ta, tb)
        self.play(FadeIn(da), FadeIn(db), run_time=0.5)

        # 利萨如曲线缠绕
        t = ValueTracker(0)
        da.add_updater(lambda m: m.move_to([1.5*np.sin(3*t.get_value()), 1.5*np.sin(2*t.get_value()), 0]))
        db.add_updater(lambda m: m.move_to([-1.5*np.sin(3*t.get_value()), -1.5*np.sin(2*t.get_value()), 0]))
        self.play(t.animate.set_value(4*PI), run_time=8, rate_func=smooth)
        da.clear_updaters()
        db.clear_updaters()

        # ── 镜03：螺旋曲线展开（0:18-0:30）──
        self.play(FadeOut(da), FadeOut(db), run_time=0.5)

        # 用2D参数曲线模拟螺旋展开
        spiral1 = ParametricFunction(
            lambda s: np.array([1.5*np.cos(s)*np.exp(-s*0.08), 1.5*np.sin(s)*np.exp(-s*0.08), 0]),
            t_range=[0, 8*PI, 0.02], color=TEAL, stroke_width=2,
        )
        spiral2 = ParametricFunction(
            lambda s: np.array([1.5*np.cos(s+PI)*np.exp(-s*0.08), 1.5*np.sin(s+PI)*np.exp(-s*0.08), 0]),
            t_range=[0, 8*PI, 0.02], color=RED, stroke_width=2,
        )

        self.play(Create(spiral1, run_time=3), Create(spiral2, run_time=3))
        self.wait(2)

        self.play(FadeOut(spiral1), FadeOut(spiral2), FadeOut(ta), FadeOut(tb), run_time=1)

        # ================================================================
        # 第二幕：形态的绽放（0:30-1:15）
        # ================================================================

        # ── 镜04：嵌套多边形（0:30-0:45）──
        outer = Circle(radius=2.5, color=BLUE, stroke_width=2)
        self.play(Create(outer, run_time=1))

        polys = VGroup()
        for n, c in enumerate([3,4,5,6,7], start=1):
            r = 2.5 - n*0.35
            p = RegularPolygon(n, radius=r, color=c, stroke_width=2)
            p.set_fill(c, opacity=0.1)
            polys.add(p)

        for p in polys:
            self.play(Create(p, run_time=0.8))
            self.wait(0.3)

        # ── 镜05：多边形变形流动（0:45-1:00）──
        cur = polys[-1].copy()
        for tn in [8, 10, 12, 16, 20]:
            tgt = RegularPolygon(tn, radius=0.8, color=PALETTE[tn%5], stroke_width=2)
            tgt.set_fill(PALETTE[tn%5], opacity=0.15)
            self.play(Transform(cur, tgt), run_time=0.6, rate_func=smooth)
        self.wait(1)

        # ── 镜06：碎裂爆发（1:00-1:15）──
        self.play(FadeOut(outer), FadeOut(polys), FadeOut(cur), run_time=0.5)

        frags = VGroup()
        for _ in range(30):
            a = random.uniform(0, 2*PI)
            sz = random.uniform(0.05, 0.2)
            c = random.choice(PALETTE)
            f = Triangle(fill_color=c, fill_opacity=0.7, stroke_color=c, stroke_width=1).scale(sz)
            frags.add(f)

        self.play(*[FadeIn(f, scale=0.1) for f in frags], run_time=0.3)

        anims = []
        for f in frags:
            a = random.uniform(0, 2*PI)
            d = random.uniform(1, 5)
            anims.append(f.animate.move_to(d*np.array([np.cos(a), np.sin(a), 0])).rotate(random.uniform(0, 2*PI)))
        self.play(*anims, run_time=2, rate_func=rush_into)
        self.wait(1)

        # ================================================================
        # 第三幕：混沌与秩序（1:15-2:00）
        # ================================================================

        # ── 镜07：谢尔宾斯基自组织（1:15-1:30）──
        self.play(*[FadeOut(f) for f in frags], run_time=0.8)

        def sierpinski(ord, v1, v2, v3):
            if ord == 0:
                return [Polygon(v1, v2, v3, fill_color=TEAL, fill_opacity=0.6, stroke_color=TEAL, stroke_width=1)]
            m1,m2,m3 = (v1+v2)/2,(v2+v3)/2,(v1+v3)/2
            return sierpinski(ord-1,v1,m1,m3)+sierpinski(ord-1,m1,v2,m2)+sierpinski(ord-1,m3,m2,v3)

        prev = None
        for o in range(6):
            v1,v2,v3 = np.array([0,2.5,0]),np.array([-2.5,-1.5,0]),np.array([2.5,-1.5,0])
            g = VGroup(*sierpinski(o, v1, v2, v3))
            if o == 0:
                self.play(FadeIn(g, run_time=1))
            else:
                self.play(Transform(prev, g), run_time=1.5)
            prev = g
            self.wait(0.5)

        # ── 镜08：催眠旋转（1:30-1:45）──
        ghosts = VGroup()
        for i in range(4):
            gh = prev.copy().set_fill(opacity=0.08*(4-i)).set_stroke(opacity=0.03*(4-i))
            ghosts.add(gh)
        self.add(ghosts)

        self.play(
            Rotate(prev, 2*PI, run_time=4, rate_func=linear),
            *[Rotate(g, 2*PI*(0.8+0.1*i), run_time=4, rate_func=linear) for i,g in enumerate(ghosts)],
            run_time=4,
        )

        # ── 镜09：液化交融（1:45-2:00）──
        # 先退场三角形，再让有机形态出现
        organic = ParametricFunction(
            lambda t: np.array([(1.5+0.5*np.sin(3*t))*np.cos(t), (1.5+0.5*np.sin(3*t))*np.sin(t), 0]),
            t_range=[0, 2*PI, 0.01], color=PLUM, stroke_width=2,
        )
        layers = VGroup()
        for i in range(4):
            l = ParametricFunction(
                lambda t, i=i: np.array([
                    (1.5+0.3*np.sin((3+i)*t+i*0.5))*np.cos(t+i*0.3),
                    (1.5+0.3*np.sin((3+i)*t+i*0.5))*np.sin(t+i*0.3), 0]),
                t_range=[0, 2*PI, 0.01], color=PALETTE[i], stroke_width=1.5, stroke_opacity=0.5,
            )
            layers.add(l)

        # 暴力清除所有谢尔宾斯基相关元素
        for mob in list(self.mobjects):
            self.remove(mob)
        self.wait(0.3)
        self.play(Create(organic, run_time=2), FadeIn(layers, run_time=2))
        self.wait(1)

        # ================================================================
        # 第四幕：回归与超越（2:00-2:45）
        # ================================================================

        self.play(FadeOut(prev), FadeOut(layers), run_time=0.8)

        # ── 镜10：螺旋环（2:00-2:15）──
        ring = ParametricFunction(
            lambda t: np.array([(2+0.3*np.sin(5*t))*np.cos(t), (2+0.3*np.sin(5*t))*np.sin(t), 0]),
            t_range=[0, 2*PI, 0.01], color=BLUE, stroke_width=2,
        )
        ring2 = ParametricFunction(
            lambda t: np.array([(2+0.3*np.sin(5*t+1))*np.cos(t+0.2), (2+0.3*np.sin(5*t+1))*np.sin(t+0.2), 0]),
            t_range=[0, 2*PI, 0.01], color=TEAL, stroke_width=1.5, stroke_opacity=0.4,
        )
        self.play(Create(ring, run_time=2), Create(ring2, run_time=2))

        # ── 镜11：光点沿环运动（2:15-2:30）──
        walker = Dot(color=GOLD, radius=0.1)
        glow = Dot(color=GOLD, radius=0.25, fill_opacity=0.3, stroke_width=0)
        trace = TracedPath(walker.get_center, stroke_color=GOLD, stroke_width=3, stroke_opacity=0.5)
        self.add(trace)
        self.play(FadeIn(VGroup(glow, walker)), run_time=0.5)

        wt = ValueTracker(0)
        def ring_pos(t):
            return np.array([(2+0.3*np.sin(5*t))*np.cos(t), (2+0.3*np.sin(5*t))*np.sin(t), 0])
        walker.add_updater(lambda m: m.move_to(ring_pos(wt.get_value())))
        glow.add_updater(lambda m: m.move_to(ring_pos(wt.get_value())))
        self.play(wt.animate.set_value(2*PI), run_time=5, rate_func=smooth)
        walker.clear_updaters()
        glow.clear_updaters()

        # ── 镜12：星空（2:30-2:45）──
        self.play(FadeOut(ring), FadeOut(ring2), FadeOut(VGroup(glow,walker)), FadeOut(trace), run_time=0.8)

        stars = VGroup()
        for _ in range(80):
            x,y = random.uniform(-5,5), random.uniform(-3,3)
            sz = random.uniform(0.02, 0.08)
            br = random.uniform(0.4, 1.0)
            s = Dot([x,y,0], color=WHITE, radius=sz)
            s.set_fill(WHITE, opacity=br)
            stars.add(s)

        self.play(FadeIn(stars, run_time=2))
        self.play(Rotate(stars, PI, run_time=5, rate_func=smooth))
        self.wait(1)

        # ================================================================
        # 第五幕：归于虚无（2:45-3:00）
        # ================================================================

        # ── 镜13：坍缩 ──
        self.play(stars.animate.scale(0.01).move_to(ORIGIN), run_time=3, rate_func=rush_into)

        # ── 镜14：熄灭 ──
        fd = Dot(ORIGIN, color=WHITE, radius=0.08)
        fg = Dot(ORIGIN, color=WHITE, radius=0.2, fill_opacity=0.2, stroke_width=0)
        self.play(FadeOut(stars), FadeIn(fg), FadeIn(fd), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(fd), fg.animate.scale(2).set_opacity(0), run_time=2, rate_func=rush_into)
        self.wait(1)

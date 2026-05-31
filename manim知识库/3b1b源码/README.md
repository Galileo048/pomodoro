# 3Blue1Brown 源码参考

## 仓库
- 视频源码: https://github.com/3b1b/videos
- Manim引擎: https://github.com/3b1b/manim

## 导数相关
- 位置: `_2017/chapter1.py` 等
- 核心技巧: ValueTracker + always_redraw 平滑动画
- 切线: `TangentLine(curve, alpha, length)`

## 曼德勃罗集
- Python: `_2021/holomorphic_dynamics.py`（3644行）
- GPU Shader: `manimlib/shaders/mandelbrot_fractal/frag.glsl`
- 调色板: 9色（深蓝→浅青→暖棕）
- 放大: 通过 scale_factor/offset uniform 实时重算，不重新渲染位图

## 核心设计模式

### 1. Pi Creature 角色系统
```python
randy = PiCreature(mode="happy")
self.play(randy.change_mode, "thinking")
bubble = SpeechBubble()
bubble.set_text("Interesting!")
```

### 2. InteractiveScene（快速原型）
```python
class MyScene(InteractiveScene):
    def construct(self):
        tracker = ValueTracker(0)
        mob = always_redraw(lambda: ...)
        self.play(tracker.animate.set_value(target))
```

### 3. 复平面可视化
```python
s_plane = ComplexPlane((-3, 3), (-3, 3))
s_trackers = Group(ComplexValueTracker(+2j), ComplexValueTracker(-2j))
```

### 4. 颜色编码
```python
t2c = {"x(t)": TEAL, "x'(t)": RED, "x''(t)": GREEN, R"\omega": PINK}
ode = Tex(R"m x''(t) + ...", t2c=t2c)
```

### 5. 指数衰减/增长
```python
amp_tracker = ValueTracker(1.0)
amp_tracker.add_updater(lambda m: m.set_value(0.98 * m.get_value()))
```

### 6. 3D 相机控制
```python
frame.reorient(-14, 82, 0, (-4.89, 2.68, 3.02), 10.32)
self.play(frame.animate.reorient(0, 0, 0, ...), run_time=3)
```

## 3b1b 配色方案
```python
BLUE_3B1B = BLUE_C      # 主曲线
GREEN_3B1B = GREEN_C    # 辅助元素
YELLOW_3B1B = YELLOW_C  # 高亮强调
RED_3B1B = RED_C        # 关键点/警示
BACKGROUND_COLOR = "#0a0a0a"  # 极深背景
```

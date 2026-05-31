# Formula2Manim 模板设计工作流

## 概述

本文档说明如何使用 Claude + manim_skill 设计新的 Manim 模板，并将其集成到 Formula2Manim 中。

## 工作流程

### 1. 描述场景

告诉 Claude 你想要的动画场景：

```
我需要一个模板来演示"弹簧振子的简谐振动"。
参数：振幅 A，角频率 ω，周期数
显示：弹簧、质点、位移-时间曲线同步动画
```

### 2. Claude 生成模板

Claude 会使用 manim_skill 的最佳实践生成高质量模板：

- 遵循 Manim Community v0.18+ 规范
- 使用 `.animate` 进行动画
- 使用 `rate_func=smooth` 实现自然运动
- 使用 `axes.c2p()` 进行坐标转换
- 使用 `ValueTracker + always_redraw` 实现动态元素
- 合理的动画时长（0.5-3秒/动画）
- 深色背景配色方案

### 3. 注册模板

使用模板生成器注册到 Formula2Manim：

```bash
python -m formula2manim.tools.template_generator \
    --name "简谐振动（弹簧振子）" \
    --category "物理" \
    --description "弹簧振子的简谐振动，同步显示位移-时间曲线" \
    --scene-class "SpringOscillationScene" \
    --params "amplitude=1.5; omega=2; cycles=3" \
    --register
```

### 4. 测试模板

在 GUI 中选择新模板，调整参数，点击渲染。

## 最佳实践清单

### 动画设计

- [ ] 使用 `.animate` 进行简单变换
- [ ] 设置合理的 `run_time`（0.5-3秒）
- [ ] 使用 `rate_func=smooth`（自然运动）或 `linear`（匀速）
- [ ] 同时动画使用单个 `self.play()`，顺序动画使用多个

### 视觉设计

- [ ] 深色背景：`#1a1a2e` 或 `#0d1117`
- [ ] 轨迹颜色：YELLOW、CYAN、ORANGE
- [ ] 运动物体：RED、PINK、GREEN
- [ ] 标签：WHITE、GRAY
- [ ] 点大小：0.06-0.12

### 代码质量

- [ ] 使用 `axes.c2p()` 进行坐标转换
- [ ] 使用 `VGroup` 进行分组
- [ ] 使用 `ValueTracker + always_redraw` 实现动态元素
- [ ] LaTeX 使用原始字符串 `r"..."`
- [ ] 参数使用 `__PARAM_key__` 占位符

### 模板结构

```python
"""
模板名称 | 类别
描述
"""
from manim import *
import numpy as np


class TemplateScene(Scene):
    def construct(self):
        # 1. 参数声明
        param1 = __PARAM_param1__
        param2 = __PARAM_param2__

        # 2. 计算轨迹
        t_arr = np.linspace(0, t_max, 200)
        x_vals = np.array([...])
        y_vals = np.array([...])

        # 3. 创建坐标轴
        axes = Axes(...)
        self.play(Create(axes), ...)

        # 4. 创建轨迹
        traj = VMobject(color=YELLOW, stroke_width=3)
        traj.set_points_smoothly(pts)

        # 5. 创建动态元素
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(...))
        self.play(FadeIn(dot), ...)

        # 6. 动画
        self.play(Create(traj), run_time=3, rate_func=smooth)
        self.play(t_tracker.animate.set_value(t_max), run_time=7, rate_func=linear)
        self.wait(2)
```

## 示例：设计一个新模板

### 场景描述

"匀速圆周运动：显示质点做圆周运动，同时显示速度矢量和向心加速度矢量"

### Claude 生成的模板

```python
"""
匀速圆周运动 | 高中物理
显示质点做圆周运动，同步显示速度和向心加速度矢量
"""
from manim import *
import numpy as np


class CircularMotionScene(Scene):
    def construct(self):
        # Parameters
        radius = __PARAM_radius__  # 2
        omega = __PARAM_omega__  # 1.5
        periods = __PARAM_periods__  # 2

        # Computed values
        t_max = periods * 2 * np.pi / omega

        # Circle path
        circle = Circle(radius=radius, color=BLUE, stroke_width=2)
        self.play(Create(circle), run_time=1)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            circle.get_center() + radius * np.array([
                np.cos(omega * t_tracker.get_value()),
                np.sin(omega * t_tracker.get_value()),
                0
            ]),
            color=RED, radius=0.12
        ))
        self.play(FadeIn(dot), run_time=0.5)

        # Velocity arrow (tangent)
        vel_arrow = always_redraw(lambda: Arrow(
            dot.get_center(),
            dot.get_center() + 0.5 * np.array([
                -np.sin(omega * t_tracker.get_value()),
                np.cos(omega * t_tracker.get_value()),
                0
            ]),
            color=GREEN, buff=0, stroke_width=3
        ))
        self.add(vel_arrow)

        # Centripetal acceleration arrow
        acc_arrow = always_redraw(lambda: Arrow(
            dot.get_center(),
            circle.get_center(),
            color=YELLOW, buff=0.1, stroke_width=3
        ))
        self.add(acc_arrow)

        # Labels
        vel_label = Text("v", font_size=20, color=GREEN)
        vel_label.next_to(vel_arrow.get_end(), UP, buff=0.1)
        acc_label = Text("a_c", font_size=20, color=YELLOW)
        acc_label.next_to(acc_arrow.get_center(), LEFT, buff=0.1)

        # Animate
        self.play(t_tracker.animate.set_value(t_max), run_time=10, rate_func=linear)
        self.wait(1)
```

### 注册命令

```bash
python -m formula2manim.tools.template_generator \
    --name "圆周运动" \
    --category "物理" \
    --description "匀速圆周运动，显示位置、速度、向心加速度矢量" \
    --scene-class "CircularMotionScene" \
    --params "radius=2; omega=1.5; periods=2" \
    --register
```

## 故障排除

### 常见问题

1. **动画卡顿**
   - 减少 `run_time`
   - 使用 `rate_func=linear` 替代 `smooth`

2. **坐标转换错误**
   - 确保使用 `axes.c2p()` 而不是手动计算
   - 检查 `x_range` 和 `y_range` 是否合理

3. **LaTeX 编译失败**
   - 使用 `Text` 替代 `MathTex`
   - 或确保系统安装了 LaTeX

4. **颜色不显示**
   - 使用 Manim 内置颜色常量（RED, BLUE, etc.）
   - 或使用十六进制字符串 "#RRGGBB"

## 参考资源

- [Manim Community 文档](https://docs.manim.community/)
- [manim_skill 最佳实践](./manim_best_practices.md)
- [Formula2Manim 模板示例](../templates/)

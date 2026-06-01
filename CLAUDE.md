# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

数学可视化动画系列——用 Manim 制作中学数学/物理教学动画视频，发布到抖音和B站。

## 目录结构

```
动画源码/          ← Manim Python 源码
动画视频/          ← 最终渲染的 MP4 视频
```

**命名规则：** 源码和视频文件名保持一致，如 `第1期_什么是导数.py` → `第1期_什么是导数.mp4`

## 渲染命令

```bash
# 低质量预览（快速测试）
python -m manim render -ql 动画源码/第1期_什么是导数.py DerivativeScene

# 高质量渲染（发布用）
python -m manim render -pqh 动画源码/第1期_什么是导数.py DerivativeScene
```

## 大创项目信息

**项目名称：** 基于Manim与AI辅助的中学数理可视化教学资源开发与双载体传播

**团队结构：** 物理师范 + 数学师范 + 计算机 + 网工

**核心产出：**
- Manim程序化动画视频（15-20个）
- 互动式可视化学习APP（可选）
- 个人网站（GitHub Pages）
- B站/抖音合集发布

**技术路线：** 内容选题 → 脚本设计 → AI辅助动画制作 → 视频合成 → 双载体发布 → 反馈迭代

**申报策略：**
- 定位为"教育技术创新类"项目，避免被归为"教学实践"
- 关键词：跨平台开发、程序化动画引擎、AI辅助编程、参数化可视化
- 利用B站播放量和GitHub提交记录作为成果证明

## Manim 动画吸引力技巧

参考：`media/Manim动画吸引力技巧指南.docx`

### 核心原则
- **节奏感**：有快有慢，有张有驰，用 rate_func 控制
- **悬念感**：先展示问题，再揭示答案
- **统一性**：风格、颜色、节奏保持一致
- **简洁性**：每帧只传达一个核心信息
- **情感共鸣**：技术是手段，情感是目的

### 文字动效
| 效果 | 代码 | 适用场景 |
|------|------|----------|
| 逐字打字 | `AddTextLetterByLetter(text, run_time=3)` | 引入新概念 |
| 弹入 | `text.animate.scale(1.2).set_color(YELLOW)` → 缩回 | 活泼强调 |
| 滑入 | `text.shift(LEFT*5)` → `animate.shift(RIGHT*5)` | 列表项展示 |
| 高亮框 | `SurroundingRectangle(keyword, color=YELLOW)` | 突出关键词 |
| 文字变形 | `Transform(text1, text2)` / `ReplacementTransform` | 概念转换 |

### 场景切换
| 效果 | 实现 |
|------|------|
| 淡入淡出 | `FadeOut(scene1), FadeIn(scene2)` |
| 推拉镜头 | `self.camera.frame.animate.scale(0.5).move_to(target)` |
| 平移转场 | `self.camera.frame.animate.shift(RIGHT * 5)` |
| 刷屏效果 | Rectangle 从一侧滑入覆盖 |

### 高级技巧
- **TracedPath**：物体运动留下光痕 `TracedPath(dot.get_center, stroke_color=YELLOW)`
- **缓动函数**：smooth（自然）、ease_in（加速）、ease_out（减速）、there_and_back（往复）、wiggle（抖动）
- **层次感**：远处物体更小、更淡、更透明 `scale(0.5).set_opacity(0.3)`
- **时间节奏**：引入 0.5-1s，展示 1-3s，过渡 0.3-0.5s，停顿 0.5-1s
- **ValueTracker + always_redraw**：平滑动画的核心模式（3b1b 风格）
- **实时信息面板**：右上角半透明面板显示动态数据
- **角度弧线**：优先用 `ParametricFunction` 手动画弧，不要用 `Arc`（`Arc` 的 `move_to` 定位不准，弧线容易跟丢动点）：
  ```python
  def get_arc():
      t = theta_tracker.get_value()
      if abs(t) < 0.01:
          return VMobject()
      return ParametricFunction(
          lambda s: plane.c2p(0.6 * np.cos(s), 0.6 * np.sin(s)),
          t_range=[0, t, 0.02], color=YELLOW, stroke_width=2,
      )
  angle_arc = always_redraw(get_arc)
  ```

### 配色方案
| 风格 | 主色调 | 适用场景 |
|------|--------|----------|
| 科技感 | 蓝色、青色、白色 | 数学、编程、未来 |
| 温暖感 | 橙色、黄色、粉色 | 教育、人文、故事 |
| 高对比 | 黑色、白色、红色 | 强调、警示、重点 |
| 梦幻感 | 紫色、蓝紫色、粉蓝色 | 艺术、抽象 |
| 自然感 | 绿色、棕色、蓝绿色 | 生物、环保 |

### 3b1b 经典配色
```python
BG = "#1C1C1C"        # 深灰背景
BLUE = "#58C4DD"      # 主曲线
GREEN = "#83C167"     # 辅助元素
YELLOW = "#FFFF00"    # 高亮强调
RED = "#FF6666"       # 关键点/警示
```

### 常见错误
- 动画过快 → 增加 run_time 或分步展示
- 信息过载 → 每帧只传达一个点
- 颜色混乱 → 定义统一配色方案
- 转场突兀 → 加入过渡动画
- 缺乏聚焦 → 用 SurroundingRectangle 或镜头运动引导视线

### 节奏参考（动画时间表模板）
| 时间 | 动作 | 技巧 |
|------|------|------|
| 0:00-0:03 | 问题文字弹入 | Pop-in + 黄色 |
| 0:03-0:08 | 曲线画出 | TracedPath 轨迹 |
| 0:08-0:15 | 镜头推近 | Zoom 细节 |
| 0:15-0:25 | 核心动画 | 逐渐接近，节奏感 |
| 0:25-0:35 | 公式出现 | Typewriter |
| 0:35-0:45 | 总结归纳 | Transform 过渡 |

### 踩坑记录与经验总结（3期实战）

#### 1. 线性变换：不要用 ApplyMatrix
`ApplyMatrix` 对整个 mobject 做屏幕空间变换，会连位置一起移，原点跑掉。
**正确做法：** 手动算变换后端点位置，用 `Transform` 动画过渡：
```python
def tp(matrix, point):
    """2x2矩阵作用于坐标点，返回屏幕坐标"""
    x, y = point
    return axes.c2p(matrix[0][0]*x + matrix[0][1]*y,
                    matrix[1][0]*x + matrix[1][1]*y)

new_arrow = Arrow(origin, tp(mat, (1,0)), color=RED, stroke_width=3, buff=0)
self.play(Transform(i_vec, new_arrow), run_time=2)
```

#### 2. 角度弧线：用 ParametricFunction，不用 Arc
`Arc` 的 `move_to` 定位不准，弧线容易跟丢动点。
**正确做法：** 用 `ParametricFunction` 手动画弧：
```python
def get_arc():
    t = theta_tracker.get_value()
    if abs(t) < 0.01:
        return VMobject()
    return ParametricFunction(
        lambda s: plane.c2p(0.6*np.cos(s), 0.6*np.sin(s)),
        t_range=[0, t, 0.02], color=YELLOW, stroke_width=2,
    )
angle_arc = always_redraw(get_arc)
```

#### 3. 中文不能放进 MathTex
LaTeX 不支持 Unicode 中文字符，会报错 `Unicode character`。
**正确做法：** 中文用 `Text(font=CN)`，和 `MathTex` 用 `VGroup` 组合：
```python
label = Text("实部: ", font="Microsoft YaHei", font_size=20, color=BLUE)
formula = MathTex("1 - x^2/2! + ...", color=BLUE).scale(0.65)
combined = VGroup(label, formula).arrange(RIGHT, buff=0.1)
```

#### 4. VGroup 移动坐标系时子物体不跟
`VGroup(axes, square).move_to(...)` 会移动坐标系，但正方形顶点如果用 `ax.c2p()` 定位则自动跟随。如果正方形是独立创建的，必须编入同一个 VGroup。

#### 5. SurroundingRectangle 要在公式定位之后创建
先 `formula.next_to(...)` 定位，再 `SurroundingRectangle(formula)` 建框，否则框会留在原位。

#### 6. 动点贴在曲线上看不清
给动点加发光圈 + 出场闪烁脉冲，y 方向微偏移 0.15 与曲线拉开层次。

#### 7. 信息面板不要太实
半透明 `fill_opacity=0.6` + 背景色，不要用纯黑 85%。文字行间距 ≥ 0.55 防重叠。

#### 8. ManimCE 不支持 corner_radius
`Rectangle` 和 `SurroundingRectangle` 没有 `corner_radius` 参数，去掉即可。

#### 9. Transform 匹配标签跟随
变换箭头时，标签也要一起 Transform 到新位置：
```python
new_label = Text("i", font_size=28, color=RED, weight=BOLD)
new_label.next_to(new_arrow.get_end(), DOWN, buff=0.12)
self.play(Transform(i_vec, new_arrow), Transform(i_label, new_label))
```

#### 10. ThreeDScene 相机控制
3D 相机没有 `frame` 属性，不能用 `self.camera.frame.animate`。
**正确做法：** 用 `set_camera_orientation` 和 `move_camera`：
```python
self.set_camera_orientation(phi=65*DEGREES, theta=-30*DEGREES)  # 初始角度
self.move_camera(phi=60*DEGREES, theta=-30*DEGREES, run_time=2)  # 动态移动
```

#### 11. ImageMobject 不能放 VGroup
`ImageMobject` 不是 `VMobject`，不能用 `VGroup` 组合。
**正确做法：** 用 `Group`：
```python
group = Group(image_mobject, text_label)  # 不是 VGroup
```

#### 12. 3D 球体材质
默认 Sphere 太透明。加 `set_fill` + `set_stroke`：
```python
ball = Sphere(radius=0.12, color=YELLOW)
ball.set_fill(YELLOW, opacity=0.9)
ball.set_stroke(WHITE, width=1.5)
```

#### 15. FadeOut 对深层嵌套 VGroup 不可靠
`FadeOut` 对多层嵌套的 VGroup（如递归生成的分形）可能无法完全清除子物体。
**正确做法：** 用 `self.remove(mob)` 强制从场景中删除：
```python
# 不可靠
self.play(FadeOut(sierpinski_group))
# 可靠
self.play(FadeOut(sierpinski_group))
self.remove(sierpinski_group)  # 强制清除
# 或者暴力清屏
for mob in list(self.mobjects):
    self.remove(mob)
```

#### 16. rate_func=there_and_back 的陷阱
`Transform` 配合 `rate_func=there_and_back` 会让物体变过去再变回来，最终回到原始状态。如果目的是让物体消失变成新形态，不要用 `there_and_back`，改用 `smooth`。

#### 17. 分形构造经验
- **科赫雪花**：递归分割线段，中间加三角形凸起，用 `ParametricFunction` 或递归点列表
- **谢尔宾斯基三角形**：递归分割三角形，保留三个子三角形，去掉中间的
- 递归深度不宜超过 5-6 层，否则渲染极慢

#### 18. 意识流/抽象动画经验
- **呼吸脉动**：`scale` + `set_opacity` 配合 `there_and_back`
- **光痕效果**：`TracedPath` 追踪运动轨迹
- **催眠旋转**：多层半透明副本（ghost）以不同速度旋转
- **清屏**：抽象动画场景切换时，用 `self.remove` 暴力清除，避免 FadeOut 残影

#### 13. 像素渲染（曼德勃罗集等）
用 NumPy + PIL 计算像素图像，保存为临时 PNG，再用 `ImageMobject` 显示：
```python
img = mandelbrot_image(x_min, x_max, y_min, y_max, width=800, height=600)
img.save("temp.png")
mb_img = ImageMobject("temp.png")
mb_img.set_height(5.5)
```

#### 14. ThreeDScene + ParametricFunction 极慢
`ThreeDScene` + `ParametricFunction` + `Create` 组合渲染极慢（14镜动画渲染超过10分钟）。
**经验：** 如果动画大部分是 2D 内容，尽量避免用 `ThreeDScene`，改用纯 2D + `ParametricFunction` 模拟 3D 效果（如螺旋线用 2D 参数方程表示）。

#### 14. 3b1b 曼德勃罗集实现（GPU Shader 方案）
3b1b 用 GPU 片段着色器实时渲染，不是 CPU 逐像素计算。
参考：`3b1b/videos/_2021/holomorphic_dynamics.py` + `3b1b/manim/manimlib/shaders/mandelbrot_fractal/frag.glsl`

**核心 shader 逻辑：**
```glsl
for(int n = 0; n < int(n_steps); n++){
    z = complex_mult(z, z) + c;       // z = z² + c
    if(length(z) > 2.0){
        // 平滑迭代计数，避免色带
        float_n += log(2.0) / log(length(z));
        color = float_to_color(sqrt(float_n), ...);
        break;
    }
}
if(stable) color = black;  // 集合内的点为黑色
```

**9 调色板（3b1b 专用）：**
```python
MANDELBROT_COLORS = [
    "#00065c", "#061e7e", "#0c37a0", "#205abc",
    "#4287d3", "#D9EDE4", "#F0F9E4", "#BA9F6A", "#573706",
]  # 深蓝→浅青→暖棕
```

**放大动画原理：**
不重新渲染位图，通过 `scale_factor` 和 `offset` uniform 改变 GPU 计算区域，实时重算。
```python
self.uniforms["scale_factor"] = plane.get_x_unit_size()
self.uniforms["offset"] = plane.get_center()
```

**Mandelbrot vs Julia 区别：**
- Mandelbrot：像素位置 = c 参数，z₀ = 0（参数空间）
- Julia：c 固定，像素位置 = z₀（种子空间）
- shader 里只需切换 `mandelbrot` 布尔标志

**平滑着色技巧：**
`float_n + log(escape_radius) / log(|z|)` 消除离散迭代的色带。

#### 15. NumPy 曼德勃罗集（CPU 方案，我们当前用的）
```python
def mandelbrot_image(x_min, x_max, y_min, y_max, width=800, height=600, max_iter=100):
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    C = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    Z = np.zeros_like(C)
    iterations = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)
    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]
        escaped = mask & (np.abs(Z) > 2)
        # 平滑着色
        iterations[escaped] = i + 1 - np.log2(np.log2(np.abs(Z[escaped])))
        mask[escaped] = False
    # 着色：发散的点按迭代次数着色，不发散的点为黑色
    colors = np.zeros((*C.shape, 3), dtype=np.uint8)
    valid = iterations > 0
    t = iterations[valid] / max_iter
    colors[valid, 0] = (9*(1-t)*t**3*255).astype(np.uint8)
    colors[valid, 1] = (15*(1-t)**2*t**2*255).astype(np.uint8)
    colors[valid, 2] = (8.5*(1-t)**3*t*255).astype(np.uint8)
    return Image.fromarray(colors)
```

## 用户偏好

- 始终使用中文回复用户
- Manim 动画源码放到 `动画源码/` 目录，最终渲染视频放到 `动画视频/` 目录
- 源码文件名和视频文件名保持一致（如 `第1期_什么是导数.py` → `第1期_什么是导数.mp4`）
- Manim 代码必须写详细的中文注释，每个函数、每个动画步骤都要说明用途
- **重要的东西和可能用到的源码都要放到 `manim知识库/` 里保存**（参考资源、踩坑经验、优秀源码片段、外部项目的关键代码等）

## Manim 知识库检索规则

制作任何 Manim 动画前，**必须先检索 `manim知识库/` 文件夹**：
1. 查看 `manim知识库/README.md` 了解目录结构和检索流程
2. 按主题查对应子文件夹（物理项目/数学项目/AI工具/3b1b源码）
3. 遇到技术问题先查本文件的踩坑记录（#1-#15）
4. 制作中文教育动画时，优先参考中文项目（Moqiyun、mathanim-desktop、manim_gpt）

### 关键参考资源
| 资源 | Stars | 链接 | 用途 |
|------|-------|------|------|
| Math-To-Manim | 2263 | https://github.com/HarleyCoops/Math-To-Manim | AI文本/图片→Manim动画 |
| manim-tutorial-CN | 1218 | https://github.com/cai-hust/manim-tutorial-CN | Manim中文入门教程 |
| AnimationsWithManim | 1222 | https://github.com/Elteoremadebeethoven/AnimationsWithManim | 完整动画课程 |
| TheoremExplainAgent | 1492 | https://github.com/TIGER-AI-Lab/TheoremExplainAgent | AI定理视频解释 |
| manim-physics | 396 | https://github.com/Matheart/manim-physics | 物理插件（力学/电磁学/光学/波动） |
| manim_skill | 891 | https://github.com/adithya-s-k/manim_skill | AI agent生成3b1b风格动画 |
| manim-slides | 864 | https://github.com/jeertmans/manim-slides | Manim动画→幻灯片 |
| manim-kindergarten | 组织 | https://github.com/manim-kindergarten | 中文Manim社区（文档+示例） |
| Moqiyun | 3 | https://github.com/Qiyun-cmd/Moqiyun.github.io | 最全中文数学+物理动画源码 |
| 3b1b videos | 10760 | https://github.com/3b1b/videos | 3Blue1Brown 所有视频源码 |
| B站-數心 | -- | https://space.bilibili.com/346660989 | manim-physics作者 |
| B站-痴佬 | -- | https://space.bilibili.com/289813724 | Manim动画创作者 |
| B站-五点七边 | -- | https://space.bilibili.com/643755221 | 数学/物理Manim动画 |

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec

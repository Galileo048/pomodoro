# 物理与数学 Manim 动画优秀项目调研报告

## 📅 调研日期: 2026-05-31

---

## 🌟 一、核心框架与引擎

### 1. 3Blue1Brown 官方 Manim
- **GitHub**: https://github.com/3b1b/manim
- **Stars**: 87,239 ⭐
- **简介**: Grant Sanderson (3Blue1Brown) 创建的数学动画引擎，用于制作解释性数学视频
- **特点**:
  - 最原始的 Manim 版本
  - 专注于数学可视化
  - 支持 LaTeX 渲染、3D 场景、几何变换
  - B站/YouTube 上最流行的数学动画风格

### 2. Manim Community Edition (ManimCE)
- **GitHub**: https://github.com/ManimCommunity/manim
- **Stars**: 38,720 ⭐
- **简介**: 社区维护的 Manim 分支，功能更完善
- **特点**:
  - 更稳定的 API
  - 更好的文档
  - 支持 Jupyter Notebook 交互
  - 推荐用于生产环境

---

## 🔬 二、物理模拟项目（重点推荐）

### 1. manim-physics ⭐⭐⭐⭐⭐
- **GitHub**: https://github.com/Matheart/manim-physics
- **Stars**: 396 ⭐
- **简介**: Manim 物理模拟插件，支持多种物理分支
- **文档**: https://manim-physics.readthedocs.io/en/latest/
- **支持的物理领域**:
  - 刚体力学 (Rigid Mechanics)
  - 电磁学 (Electromagnetism)
  - 波动学 (Wave)
  - 光学 (Optics)
  - 电动力学 (Electrodynamics)
- **安装**:
  ```bash
  pip install manim-physics
  ```
- **示例代码**:
  ```python
  from manim_physics import *

  class MagneticFieldExample(ThreeDScene):
      def construct(self):
          wire = Wire(Circle(2).rotate(PI / 2, UP))
          mag_field = MagneticField(wire)
          self.set_camera_orientation(PI / 3, PI / 4)
          self.add(wire, mag_field)
  ```
- **⚠️ 注意**: 作者表示可能没有时间维护，欢迎贡献者参与

### 2. Math-To-Manim ⭐⭐⭐⭐⭐
- **GitHub**: https://github.com/HarleyCoops/Math-To-Manim
- **Stars**: 2,256 ⭐
- **简介**: 从文本和图像创建史诗级数学和物理动画
- **特点**:
  - 使用 DeepSeek R1 等推理模型
  - 自动生成课程计划、数学包、故事板
  - 支持 3D 动画 (QED、闵可夫斯基时空等)
  - 有 GRPO 语义流形动画
- **应用场景**:
  - 教学视频制作
  - 数学概念可视化
  - 物理现象演示

### 3. KimiK2Manim
- **GitHub**: https://github.com/HarleyCoops/KimiK2Manim
- **Stars**: 62 ⭐
- **简介**: 使用 Kimi K2 Thinking 创建数学和物理解释动画
- **特点**: 基于 Kimi 的推理能力生成动画代码

---

## 🎨 三、数学可视化项目

### 1. Manim.js
- **GitHub**: https://github.com/JazonJiao/Manim.js
- **Stars**: 441 ⭐
- **简介**: 用 JavaScript (p5.js) 复刻 3Blue1Brown 的数学动画引擎
- **特点**:
  - Web 端运行
  - 无需 Python 环境
  - 适合前端开发者

### 2. ManimCat
- **GitHub**: https://github.com/Wing900/ManimCat
- **Stars**: 357 ⭐
- **简介**: AI 生成数学动画，支持自然语言输入
- **特点**:
  - 高质量 Manim 渲染
  - LaTeX 支持
  - 自动代码修复
  - 中文友好

### 3. manim-visualizations
- **GitHub**: https://github.com/modorethegreat/manim-visualizations
- **简介**: 数学与物理可视化合集
- **涵盖主题**:
  - 混沌理论
  - 量子力学
  - 相对论
  - 波动物理
  - 数学之美

---

## 📚 四、教程与学习资源

### 1. Awesome Manim
- **GitHub**: https://github.com/ManimCommunity/awesome-manim
- **Stars**: 494 ⭐
- **简介**: Manim 用户和内容创作者数据库
- **内容**: 大量教程、插件、示例链接

### 2. from_scratch
- **GitHub**: https://github.com/gabriel-trigo/from_scratch
- **简介**: 物理主题动画源码
- **包含内容**:
  - 理想气体 (ideal_gas)
  - 抛物线安全 (safety_parabola)

### 3. Varniex/animations
- **GitHub**: https://github.com/Varniex/animations
- **Stars**: 71 ⭐
- **简介**: Varniex 频道视频的动画源码

---

## 🎓 五、特定物理主题项目

### 电磁学
| 项目 | 链接 | 说明 |
|------|------|------|
| ManimAnimations | https://github.com/abaret-phys/ManimAnimations | 电磁学课程动画（电场、高斯定律、安培定律等） |
| manim_emft | https://github.com/hasantahir/manim_emft | 电磁场与微波技术视频 |
| PlaneWavePropagation | https://github.com/chandansaipavanpadala/PlaneWavePropagation-Manim | 平面波传播可视化 |

### 波动与振动
| 项目 | 链接 | 说明 |
|------|------|------|
| shm-superposition | https://github.com/brinterwastaken/shm-superposition | 简谐运动与波叠加动画 |
| Signal-Processing--3D-SineWave | https://github.com/youroldmangaming/Signal-Processing--3D-SineWave-Animation | 3D 正弦波动画 |
| diffgeom-pulse | https://github.com/jackChallis/diffgeom-pulse | 阻尼余弦波 3D 线框动画 |

### 微分方程
| 项目 | 链接 | 说明 |
|------|------|------|
| Manim_ODE | https://github.com/v1kastiwari/Manim_ODE | 微分方程可视化（方向场、等倾线） |
| differential-equations-project | https://github.com/palmenros/differential-equations-project | 微分方程课程项目 |
| pendulumSimulation | https://github.com/enzo200325/pendulumSimulation | 摆的 ODE 模拟 |

### 其他物理主题
| 项目 | 链接 | 说明 |
|------|------|------|
| Physics-Simulations | https://github.com/CVC97/Physics-Simulations | C 语言物理仿真 + Manim 动画 |
| Lorentz-Solver-V2 | https://github.com/ihsan-sa/Lorentz-Solver-V2 | 电磁场中粒子路径模拟 |
| interplanetary-transport-network | https://github.com/lukechu10/interplanetary-transport-network | 行星际运输网络模拟 |

---

## 🛠️ 六、实用工具与扩展

### 1. Visura
- **GitHub**: https://github.com/Devansh-Sabharwal/Visura
- **简介**: 输入概念，AI 自动生成 Manim 动画
- **特点**: 无需 Manim 配置，支持 2D 动画

### 2. Askit.
- **GitHub**: https://github.com/SwayingWheatfield/Askit.
- **简介**: 实时交互式 AI 学习平台
- **特点**:
  - 使用 Bullet Physics 引擎
  - 微观模型可视化
  - AI 辅助学习

### 3. manim-skill
- **GitHub**: https://github.com/Yusuke710/manim-skill
- **简介**: Claude Code 的 Manim 技能插件
- **功能**: 自动规划场景、编写代码、渲染视频

---

## 📊 七、项目对比分析

| 项目 | Stars | 物理 | 数学 | AI辅助 | 3D | 易用性 |
|------|-------|------|------|--------|-----|--------|
| manim (3b1b) | 87k | ⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ✅ | ⭐⭐⭐ |
| ManimCE | 38k | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | ✅ | ⭐⭐⭐⭐ |
| manim-physics | 396 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ✅ | ⭐⭐⭐⭐ |
| Math-To-Manim | 2.2k | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| ManimCat | 357 | ⭐⭐ | ⭐⭐⭐⭐ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |

---

## 🎯 八、对 Formula2Manim 项目的启示

### 可以借鉴的设计模式

1. **manim-physics 的模块化架构**
   - 按物理领域组织代码（刚体、电磁、波动等）
   - 提供统一的 API 接口
   - 值得参考: `physics_models/` 目录结构

2. **Math-To-Manim 的 AI 工作流**
   - 使用推理模型生成动画代码
   - 自动生成课程计划和故事板
   - 值得参考: `ai_assistant/` 模块的扩展

3. **ManimCat 的自动修复功能**
   - 代码生成后自动验证和修复
   - 值得参考: 可以添加到 GUI 的实时预览功能

### 建议的功能扩展

1. **增加物理模型类型**
   - 电磁学模型（库仑定律、安培定律）
   - 波动模型（驻波、行波叠加）
   - 热力学模型（理想气体状态方程）

2. **增强 AI 能力**
   - 支持更多推理模型（DeepSeek R1, Kimi K2）
   - 自动生成课程大纲
   - 添加语音解说生成

3. **改善用户体验**
   - 实时预览功能（参考 Visura）
   - 模板库扩展
   - 导出格式支持（GIF、MP4、WebM）

---

## 🔗 九、参考资源汇总

### 官方资源
- Manim 官方文档: https://docs.manim.community/
- ManimCE GitHub: https://github.com/ManimCommunity/manim
- 3Blue1Brown YouTube: https://www.youtube.com/@3blue1brown

### 社区资源
- Awesome Manim: https://github.com/ManimCommunity/awesome-manim
- manim-physics 文档: https://manim-physics.readthedocs.io/
- Manim Discord 社区

### 中文资源
- B站 Manim 教程搜索: "manim 教程"
- Math-to-Manim-CH: https://github.com/HarleyCoops/Math-to-Manim-CH (中文版)

---

## 📝 十、总结与建议

### 核心发现

1. **manim-physics 是目前最完整的物理模拟插件**，支持刚体、电磁、波动等多个领域
2. **Math-To-Manim 展示了 AI 辅助动画生成的巨大潜力**，使用 DeepSeek R1 等推理模型
3. **社区生态丰富**，有大量教程、示例和扩展插件
4. **中文资源正在增长**，Math-to-Manim-CH 等项目值得关注

### 对 Formula2Manim 的建议

1. **短期目标**
   - 集成 manim-physics 插件，扩展物理模型支持
   - 参考 Math-To-Manim 的 AI 工作流，增强 DeepSeek 集成
   - 添加更多预设模板（电磁学、波动等）

2. **中期目标**
   - 开发实时预览功能
   - 支持更多推理模型
   - 添加课程计划自动生成

3. **长期目标**
   - 构建完整的教学资源平台
   - 支持多语言（中英文）
   - 集成交互式学习功能

---

*报告生成时间: 2026-05-31*
*调研工具: GitHub API*
*数据来源: GitHub 仓库、README 文档、项目描述*

---

## 💻 十一、代码示例合集

### 示例1: 理想气体模拟 (from_scratch)

```python
from manim import *
import numpy as np
import pandas as pd

class IdealGasScene(Scene):
    def construct(self):
        num_particles = 100
        box_size = 200
        box_size_manim = 5

        # 读取预计算的位置和速度数据
        pos = np.array(pd.read_csv("ideal_gas/pos.csv"))[1:, 1:]
        vel = np.array(pd.read_csv("ideal_gas/vel.csv"))[1:, 1:]

        def plot_simulation():
            box = Square(side_length=box_size_manim)\
                .move_to(axes.coords_to_point(box_size/2, box_size/2))
            particles = get_particles()
            return VGroup(box, *particles)

        def get_particles():
            particles = []
            for i in range(0, pos.shape[1], 2):
                particles.append(Dot(axes.coords_to_point(
                    *(pos[int(tracker.get_value()), i: i + 2])),
                    radius=(2/box_size)*box_size_manim,
                    color=BLUE))
            return particles

        tracker = ValueTracker(0)

        axes = Axes(
            x_range=[0, 200],
            y_range=[0, 200],
            x_length=5,
            y_length=5,
            axis_config={"color": WHITE},
            tips=False)

        a = always_redraw(plot_simulation)

        self.add(a)
        self.play(tracker.animate.set_value((pos.shape[0] - 1)/30),
            rate_func=rate_functions.linear,
            run_time=2)
        self.play(a.animate.scale(0.5), run_time=1)
        self.play(tracker.animate.set_value((pos.shape[0] - 1)/30 + 100),
            rate_func=rate_functions.linear,
            run_time=2)
```

### 示例2: 安全抛物线 (from_scratch)

```python
import numpy as np
from manim import *

class SafetyParabola(Scene):
    def construct(self):
        # 物理参数
        v0 = 10  # 初速度
        g = 10   # 重力加速度

        # 单条轨迹
        def get_trajectory(theta, tracker):
            graph = axes.plot(
                lambda x: np.tan(theta)*x - g*x**2/(2*(v0*np.cos(theta))**2),
                x_range=[-tracker.get_value(), 0] if theta > np.pi/2 else [0, tracker.get_value()],
                color=BLUE)
            return graph

        # 安全抛物线
        def get_safety_parabola():
            graph = axes.plot(
                lambda x: v0**2/(2*g) - g*x**2/(2*v0**2),
                x_range=[-12, parabola_tracker.get_value()],
                color=PINK)
            return graph

        # 轨迹族动画
        def draw_collection():
            graphs = []
            for angle in angles:
                if angle < np.pi / 2:
                    graphs.append(get_trajectory(angle, tracker))
            return VGroup(*graphs)

        # 执行动画
        self.play(Create(axes))
        self.play(tracker.animate.set_value(10), run_time=2)
        self.play(Create(get_safety_parabola()), color=PINK)
```

### 示例3: 磁场可视化 (manim-physics)

```python
from manim_physics import *

class MagneticFieldExample(ThreeDScene):
    def construct(self):
        # 创建载流导线
        wire = Wire(Circle(2).rotate(PI / 2, UP))
        # 生成磁场线
        mag_field = MagneticField(wire)

        # 设置3D相机视角
        self.set_camera_orientation(PI / 3, PI / 4)
        self.add(wire, mag_field)
```

### 示例4: 电磁波传播 (PlaneWavePropagation)

```python
from manim import *
import numpy as np

class PlaneWavePropagation(Scene):
    def construct(self):
        # 电场分量
        def E_field(x, t):
            return np.exp(-0.1 * x) * np.cos(2 * np.pi * (x - t))

        # 创建波形
        wave = always_redraw(lambda: self.plot_wave())

        # 坐标轴
        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[-2, 2, 0.5],
            axis_config={"color": WHITE}
        )

        # 添加标签
        title = Text("平面波在有损介质中的传播").to_edge(UP)

        self.add(axes, title)
        self.play(Create(wave), run_time=5)
```

---

## 🎯 十二、Formula2Manim 可以直接复用的代码模式

### 1. ValueTracker 动画控制模式

```python
# 用于控制动画进度
tracker = ValueTracker(0)
mob = always_redraw(lambda: some_function(tracker.get_value()))
self.play(tracker.animate.set_value(target_value))
```

### 2. 轨迹绘制模式

```python
def get_trajectory(params, tracker):
    return axes.plot(
        lambda x: physics_function(x, params),
        x_range=[0, tracker.get_value()],
        color=BLUE
    )
```

### 3. 粒子系统模式

```python
def get_particles(positions, time_step):
    particles = []
    for pos in positions[time_step]:
        particles.append(Dot(pos, radius=0.05, color=BLUE))
    return VGroup(*particles)
```

### 4. 3D 场景模式

```python
class Physics3DScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi, theta)
        # 添加3D对象
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait()
```

---

## 📚 十三、学习路径建议

### 初学者路径

1. **基础入门**
   - 学习 ManimCE 官方文档
   - 掌握基本对象（Circle, Square, Line）
   - 学习动画方法（Create, Transform, FadeIn）

2. **物理模拟入门**
   - 使用 manim-physics 插件
   - 学习 ValueTracker 控制动画
   - 掌握 Axes 坐标系绘制

3. **AI 辅助开发**
   - 研究 Math-To-Manim 的工作流
   - 学习如何用 AI 生成动画代码
   - 掌握代码调试和优化技巧

### 进阶路径

1. **高级动画技巧**
   - 学习 3D 场景构建
   - 掌握相机控制
   - 学习自定义 Mobject

2. **物理建模**
   - 学习数值积分方法
   - 掌握轨迹计算
   - 学习参数化动画

3. **项目开发**
   - 研究 Formula2Manim 架构
   - 学习 GUI 开发（PyQt6）
   - 掌握 AI 集成技术

---

*报告完成于: 2026-05-31*
*总项目数: 30+*
*涵盖领域: 物理模拟、数学可视化、电磁学、波动、微分方程*
*推荐项目: manim-physics, Math-To-Manim, ManimCat*

# 物理 Manim 项目参考

## manim-physics 插件（396⭐）⭐⭐⭐⭐⭐
- GitHub: https://github.com/Matheart/manim-physics
- 安装: `pip install manim-physics`
- 文档: https://manim-physics.readthedocs.io
- 作者: Matheart（數心），B站: space.bilibili.com/346660989

### 支持的物理领域（高中直接对应）
1. **刚体力学**：重力、碰撞、摆、刚体动力学（基于 pymunk 引擎）
2. **电磁学**：静电学（Charge/ElectricField 类）、静磁学
3. **光学**：透镜、射线追踪
4. **波动**

### 常用代码模式
```python
from manim_physics import *

# 重力场景
class GravityDemo(SpaceScene):
    def construct(self):
        ground = Line(LEFT * 4, RIGHT * 4).shift(DOWN * 2)
        ball = Circle(radius=0.3).shift(UP * 2)
        self.add(ball)
        self.make_rigid_body(ball)
        self.make_ground(ground)
        self.wait(5)

# 电场可视化
class ElectricFieldDemo(Scene):
    def construct(self):
        plane = ComplexPlane()
        charge = Charge(1, plane.c2p(0, 0))  # 正电荷
        field = ElectricField(charge)
        self.add(plane, charge, field)
        self.wait(3)
```

## Math-To-Manim（AI生成，2263⭐）⭐⭐⭐⭐⭐
- GitHub: https://github.com/HarleyCoops/Math-To-Manim
- 功能：文本/图片 → Manim 动画 + 学习笔记
- 中文版: https://github.com/HarleyCoops/Math-to-Manim-CH

## TheoremExplainAgent（ACL 2025，1492⭐）
- GitHub: https://github.com/TIGER-AI-Lab/TheoremExplainAgent
- 功能：AI 自动生成定理解释视频（用 Manim）

## from_scratch（粒子模拟，9⭐）
- GitHub: https://github.com/gabriel-trigo/from_scratch
- 内容：理想气体模拟、抛体运动（安全抛物线）、3D盒子
- 技术：3D场景渲染、粒子系统、轨迹动画

## elbrujo325/manim-physics（电磁学3D）
- GitHub: https://github.com/elbrujo325/manim-physics
- 内容：高斯定律、电场、电势、电偶极、静电能
- 技术：ArrowVectorField、ThreeDScene+相机旋转、Instagram竖版

## Physics-with-Manim（AP Physics C）
- GitHub: https://github.com/nathanliow/Physics-with-Manim
- 内容：安培定律、毕奥-萨伐尔定律

## overtones（波动）
- GitHub: https://github.com/chlorkrake/overtones
- 内容：波的泛音/谐波

## 智能物理教学动画系统（中文）
- GitHub: https://github.com/NIGHTVIYAGE6/physics-manim-app

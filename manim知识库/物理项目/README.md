# 物理 Manim 项目参考

## manim-physics 插件（396⭐）
- GitHub: https://github.com/Matheart/manim-physics
- 安装: `pip install manim-physics`
- 文档: https://manim-physics.readthedocs.io

### 支持的物理领域
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

## Physics-with-Manim（AP Physics C）
- GitHub: https://github.com/nathanliow/Physics-with-Manim
- 内容：安培定律、毕奥-萨伐尔定律
- 对标 AP Physics C 课程

## from_scratch（粒子模拟）
- GitHub: https://github.com/gabriel-trigo/from_scratch
- 内容：理想气体模拟、抛体运动（安全抛物线）、3D盒子
- 技术：3D场景渲染、粒子系统、轨迹动画

## elbrujo325/manim-physics（电磁学3D）
- GitHub: https://github.com/elbrujo325/manim-physics
- 内容：高斯定律（3D高斯面）、电场（库仑定律+叠加+场线）、电势（等势面）、电偶极、静电能
- 技术：ArrowVectorField、ThreeDScene+相机旋转、Instagram竖版(1080x1920)

## 智能物理教学动画系统（中文）
- GitHub: https://github.com/NIGHTVIYAGE6/physics-manim-app
- 中文物理教学系统

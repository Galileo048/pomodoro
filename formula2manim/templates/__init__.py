"""Manim 场景模板注册表 — 高中物理 & 数学."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

_TEMPLATES_DIR = Path(__file__).resolve().parent


class ParamDef(TypedDict):
    label: str       # 中文标签
    default: str     # 默认值（字符串，会替换到模板中）
    type: str        # "float" | "int" | "text"


class TemplateDef(TypedDict):
    name: str                        # 中文名称
    category: str                    # "物理" | "数学"
    description: str                 # 一句话描述
    file: str                        # 模板文件名（相对于 templates/ 目录）
    scene_class: str                 # Manim Scene 类名
    params: dict[str, ParamDef]      # 可调参数


TEMPLATES: list[TemplateDef] = [
    # ═══════════ 物理 ═══════════
    {
        "name": "匀加速直线运动",
        "category": "物理",
        "description": "物体以恒定加速度做直线运动，显示位移公式和实时速度",
        "file": "uniform_accel.py",
        "scene_class": "UniformAccelScene",
        "params": {
            "v0": {"label": "初速度 v₀ (m/s)", "default": "0", "type": "float"},
            "a": {"label": "加速度 a (m/s²)", "default": "3", "type": "float"},
            "t_max": {"label": "时间 (s)", "default": "10", "type": "float"},
        },
    },
    {
        "name": "平抛运动",
        "category": "物理",
        "description": "水平抛出物体，显示水平和竖直分运动及合速度",
        "file": "projectile.py",
        "scene_class": "ProjectileScene",
        "params": {
            "v0x": {"label": "水平初速度 v₀ₓ (m/s)", "default": "10", "type": "float"},
            "v0y": {"label": "竖直初速度 v₀ᵧ (m/s)", "default": "0", "type": "float"},
            "g": {"label": "重力加速度 g (m/s²)", "default": "9.8", "type": "float"},
        },
    },
    {
        "name": "斜抛运动",
        "category": "物理",
        "description": "物体以一定角度抛出，显示抛物线轨迹及最高点",
        "file": "oblique_projectile.py",
        "scene_class": "ObliqueProjectileScene",
        "params": {
            "v0": {"label": "初速度大小 v₀ (m/s)", "default": "20", "type": "float"},
            "angle": {"label": "抛出角度 θ (°)", "default": "45", "type": "float"},
            "g": {"label": "重力加速度 g (m/s²)", "default": "9.8", "type": "float"},
        },
    },
    {
        "name": "圆周运动",
        "category": "物理",
        "description": "匀速圆周运动，显示位置、速度、向心加速度矢量",
        "file": "circular_motion.py",
        "scene_class": "CircularMotionScene",
        "params": {
            "radius": {"label": "半径 r (m)", "default": "2", "type": "float"},
            "omega": {"label": "角速度 ω (rad/s)", "default": "1.5", "type": "float"},
            "periods": {"label": "周期数", "default": "2", "type": "float"},
        },
    },
    {
        "name": "简谐振动（弹簧振子）",
        "category": "物理",
        "description": "弹簧振子的简谐振动，同步显示位移-时间曲线",
        "file": "spring_oscillation.py",
        "scene_class": "SpringOscillationScene",
        "params": {
            "amplitude": {"label": "振幅 A (m)", "default": "1.5", "type": "float"},
            "omega": {"label": "角频率 ω (rad/s)", "default": "2", "type": "float"},
            "cycles": {"label": "周期数", "default": "3", "type": "float"},
        },
    },
    {
        "name": "动量守恒碰撞",
        "category": "物理",
        "description": "一维弹性碰撞演示动量守恒，显示碰撞前后速度",
        "file": "collision.py",
        "scene_class": "CollisionScene",
        "params": {
            "m1": {"label": "球1质量 m₁ (kg)", "default": "2", "type": "float"},
            "m2": {"label": "球2质量 m₂ (kg)", "default": "1", "type": "float"},
            "v1i": {"label": "球1初速度 v₁ (m/s)", "default": "3", "type": "float"},
            "v2i": {"label": "球2初速度 v₂ (m/s)", "default": "0", "type": "float"},
        },
    },
    {
        "name": "波的传播",
        "category": "物理",
        "description": "一维行波的传播，显示质点的振动和波形移动",
        "file": "wave.py",
        "scene_class": "WaveScene",
        "params": {
            "amplitude": {"label": "振幅 A", "default": "0.8", "type": "float"},
            "wavelength": {"label": "波长 λ", "default": "3", "type": "float"},
            "speed": {"label": "波速 v (m/s)", "default": "2", "type": "float"},
        },
    },
    {
        "name": "多阶段运动",
        "category": "物理",
        "description": "分段运动：平抛+电场、加速+减速等，不同阶段用不同颜色显示",
        "file": "multi_phase.py",
        "scene_class": "MultiPhaseScene",
        "params": {
            "v0x": {"label": "水平初速度 v₀ₓ (m/s)", "default": "10", "type": "float"},
            "v0y": {"label": "竖直初速度 v₀ᵧ (m/s)", "default": "0", "type": "float"},
            "g": {"label": "重力加速度 g (m/s²)", "default": "9.8", "type": "float"},
            "t1": {"label": "阶段1结束时间 t₁ (s)", "default": "3", "type": "float"},
            "ax2": {"label": "阶段2水平加速度 aₓ₂ (m/s²)", "default": "-6.93", "type": "float"},
            "ay2": {"label": "阶段2竖直加速度 aᵧ₂ (m/s²)", "default": "-6.93", "type": "float"},
            "h0": {"label": "初始高度 h₀ (m)", "default": "20", "type": "float"},
            "t_end": {"label": "总时间 t_end (s)", "default": "20", "type": "float"},
        },
    },
    {
        "name": "N阶段运动",
        "category": "物理",
        "description": "支持任意数量的分段运动，每段可独立设置运动类型（匀速、抛体、圆周、简谐等）",
        "file": "n_phase.py",
        "scene_class": "NPhaseScene",
        "params": {
            "phases": {"label": "运动阶段 (JSON格式)", "default": '[{"t_start":0,"t_end":3,"type":"projectile","params":{"vx":10,"vy":0,"g":9.8}},{"t_start":3,"t_end":10,"type":"linear","params":{"vx":10,"vy":-30}},{"t_start":10,"t_end":15,"type":"circular","params":{"cx":100,"cy":0,"r":3,"omega":1.5}}]', "type": "text"},
            "n_phases": {"label": "阶段数量", "default": "3", "type": "int"},
        },
    },
    # ═══════════ 数学 ═══════════
    {
        "name": "割线→切线（导数定义）",
        "category": "数学",
        "description": "动态展示 Δx→0 时割线趋近于切线，实时显示 Δy/Δx",
        "file": "secant_to_tangent.py",
        "scene_class": "SecantToTangentScene",
        "params": {
            "a": {"label": "固定点 x 坐标", "default": "1", "type": "float"},
            "h_start": {"label": "初始 Δx", "default": "2", "type": "float"},
            "func_expr": {"label": "函数表达式", "default": "x**2", "type": "text"},
        },
    },
    {
        "name": "定积分（黎曼和→面积）",
        "category": "数学",
        "description": "从黎曼和逼近定积分，矩形数量逐渐增加",
        "file": "riemann_sum.py",
        "scene_class": "RiemannSumScene",
        "params": {
            "func_expr": {"label": "被积函数 f(x)", "default": "x**2", "type": "text"},
            "x_min": {"label": "积分下限 a", "default": "0", "type": "float"},
            "x_max": {"label": "积分上限 b", "default": "2", "type": "float"},
            "max_rects": {"label": "最大矩形数", "default": "50", "type": "int"},
        },
    },
    {
        "name": "二次函数（抛物线）",
        "category": "数学",
        "description": "y=ax²+bx+c，可调 a, b, c 参数观察图像变化",
        "file": "quadratic.py",
        "scene_class": "QuadraticScene",
        "params": {
            "a": {"label": "二次项系数 a", "default": "1", "type": "float"},
            "b": {"label": "一次项系数 b", "default": "-2", "type": "float"},
            "c": {"label": "常数项 c", "default": "1", "type": "float"},
        },
    },
    {
        "name": "三角函数图像",
        "category": "数学",
        "description": "y=A·sin(ωx+φ)，可调振幅、频率、相位",
        "file": "trig_function.py",
        "scene_class": "TrigFunctionScene",
        "params": {
            "A": {"label": "振幅 A", "default": "2", "type": "float"},
            "omega": {"label": "角频率 ω", "default": "1", "type": "float"},
            "phi": {"label": "相位 φ (弧度)", "default": "0", "type": "float"},
        },
    },
    {
        "name": "指数函数与对数",
        "category": "数学",
        "description": "y=aˣ 和 y=logₐx 的图像，可调底数 a",
        "file": "exponential.py",
        "scene_class": "ExponentialScene",
        "params": {
            "base": {"label": "底数 a", "default": "2", "type": "float"},
        },
    },
]


def get_template_dir() -> Path:
    return _TEMPLATES_DIR


def get_template_path(filename: str) -> Path:
    return _TEMPLATES_DIR / filename


def get_template_by_name(name: str) -> TemplateDef | None:
    for t in TEMPLATES:
        if t["name"] == name:
            return t
    return None

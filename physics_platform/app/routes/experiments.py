"""
交互动画实验路由模块
====================

本模块处理所有交互动画实验的请求：
- 实验列表页（/experiments）
- 实验运行页（/experiment/<experiment_id>）

路由蓝图：experiments_bp

实验结构：
    每个实验是一个独立的 Canvas 动画，包含：
    1. 物理/数学模型计算
    2. Canvas 绘制
    3. 控制面板（滑块、按钮）
    4. 实时数据展示
    5. 图表（可选）

扩展方式：
    在 EXPERIMENTS 字典中注册新实验，
    在 templates/experiments/ 目录下创建对应的 HTML 片段。

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

from flask import Blueprint, render_template
from flask_login import login_required

# 创建蓝图实例
experiments_bp = Blueprint('experiments', __name__)


# ============================================================
# 实验注册表
# ============================================================
# 每个实验包含：id, title, description, category, template
EXPERIMENTS = [
    {
        'id': 'projectile',
        'title': '平抛运动',
        'description': '水平匀速 + 竖直自由落体',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'params': '初速度、高度、重力加速度',
    },
    {
        'id': 'freefall',
        'title': '自由落体运动',
        'description': '只受重力，初速度为零',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'params': '高度、星球重力加速度',
    },
    {
        'id': 'projectile_angle',
        'title': '斜抛运动',
        'description': '不同角度的抛体轨迹对比',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'params': '初速度、抛射角、重力加速度',
    },
    {
        'id': 'trig_function',
        'title': '三角函数 y=Asin(ωx+φ)',
        'description': '振幅、频率、相位实时调节',
        'category': '数学',
        'tags': ['三角函数', 'Canvas'],
        'params': 'A、ω、φ',
    },
]


# ============================================================
# 实验列表页
# ============================================================
@experiments_bp.route('/experiments')
@login_required
def experiment_list():
    """实验列表页 - 展示所有可用的交互动画实验"""
    return render_template('experiments.html', experiments=EXPERIMENTS)


# ============================================================
# 实验运行页
# ============================================================
@experiments_bp.route('/experiment/<experiment_id>')
@login_required
def run(experiment_id):
    """
    运行指定的交互动画实验

    参数：
        experiment_id: 实验编号（如 'projectile'）

    每个实验有独立的模板文件，包含完整的 Canvas 动画逻辑。
    """
    # 查找实验信息
    experiment = None
    for exp in EXPERIMENTS:
        if exp['id'] == experiment_id:
            experiment = exp
            break

    if not experiment:
        return render_template('404.html'), 404

    # 渲染对应的实验模板
    # 模板文件名规则：experiment_<experiment_id>.html
    template_name = f'experiments/experiment_{experiment_id}.html'
    return render_template(template_name, experiment=experiment)

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
        'level': '高中',
        'params': '初速度、高度、重力加速度',
    },
    {
        'id': 'freefall',
        'title': '自由落体运动',
        'description': '只受重力，初速度为零',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'level': '高中',
        'params': '高度、星球重力加速度',
    },
    {
        'id': 'projectile_angle',
        'title': '斜抛运动',
        'description': '不同角度的抛体轨迹对比',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'level': '高中',
        'params': '初速度、抛射角、重力加速度',
    },
    {
        'id': 'trig_function',
        'title': '三角函数 y=Asin(ωx+φ)',
        'description': '振幅、频率、相位实时调节',
        'category': '数学',
        'tags': ['三角函数', 'Canvas'],
        'level': '高中',
        'params': 'A、ω、φ',
    },
    {
        'id': 'linear',
        'title': '一次函数 y=kx+b',
        'description': '斜率控制旋转，截距控制平移',
        'category': '数学',
        'tags': ['一次函数', 'Canvas'],
        'level': '高中',
        'params': 'k、b',
    },
    {
        'id': 'quadratic',
        'title': '二次函数 y=ax²+bx+c',
        'description': '抛物线、顶点、对称轴、判别式',
        'category': '数学',
        'tags': ['二次函数', 'Canvas'],
        'level': '高中',
        'params': 'a、b、c',
    },
    {
        'id': 'exponential',
        'title': '指数函数 y=aˣ',
        'description': 'a>1增长，0<a<1衰减',
        'category': '数学',
        'tags': ['指数函数', 'Canvas'],
        'level': '高中',
        'params': '底数 a',
    },
    {
        'id': 'ellipse',
        'title': '椭圆 x²/a²+y²/b²=1',
        'description': '拖动椭圆上的点验证|PF₁|+|PF₂|=2a',
        'category': '数学',
        'tags': ['椭圆', 'Canvas'],
        'level': '高中',
        'params': '半长轴a、半短轴b',
    },
    {
        'id': 'normal',
        'title': '正态分布 N(μ,σ²)',
        'description': '钟形曲线，68-95-99.7法则',
        'category': '数学',
        'tags': ['概率统计', 'Canvas'],
        'level': '高中',
        'params': 'μ、σ',
    },
    {
        'id': 'derivative',
        'title': '导数的几何意义',
        'description': '割线趋近切线，Δx→0时斜率→导数值',
        'category': '数学',
        'tags': ['导数', 'Canvas'],
        'level': '高中',
        'params': '函数选择、x₀、Δx',
    },
    {
        'id': 'integral',
        'title': '定积分几何意义',
        'description': '阴影面积，蓝正红负，黎曼和逼近',
        'category': '数学',
        'tags': ['积分', 'Canvas'],
        'level': '高中',
        'params': '函数选择、a、b、n',
    },
    {
        'id': 'newton',
        'title': '牛顿第二定律 F=ma',
        'description': '力与加速度成正比，与质量成反比',
        'category': '物理',
        'tags': ['动力学', 'Canvas'],
        'level': '高中',
        'params': '合外力F、质量m',
    },
    {
        'id': 'spring',
        'title': '弹簧弹力 胡克定律',
        'description': 'F=-kx，简谐运动，能量守恒',
        'category': '物理',
        'tags': ['振动', 'Canvas'],
        'level': '高中',
        'params': '劲度系数k、质量m、振幅A',
    },
    {
        'id': 'circular',
        'title': '匀速圆周运动',
        'description': 'v=ωR, a=v²/R，向心加速度与投影SHM',
        'category': '物理',
        'tags': ['圆周运动', 'Canvas'],
        'level': '高中',
        'params': '半径R、角速度ω',
    },
    {
        'id': 'pendulum',
        'title': '单摆运动',
        'description': 'T=2π√(L/g)，相图与能量守恒',
        'category': '物理',
        'tags': ['振动', 'Canvas'],
        'level': '高中',
        'params': '摆长L、初始角度θ₀、重力加速度g',
    },
    {
        'id': 'friction',
        'title': '摩擦力实验',
        'description': 'f=μN，静摩擦与滑动摩擦',
        'category': '物理',
        'tags': ['力学', 'Canvas'],
        'level': '高中',
        'params': '质量m、摩擦系数μ、推力F',
    },
    {
        'id': 'energy',
        'title': '机械能守恒',
        'description': '½mv² + mgh = const',
        'category': '物理',
        'tags': ['能量', 'Canvas'],
        'level': '高中',
        'params': '初始高度h、初速度v₀、摩擦系数μ',
    },
    {
        'id': 'collision',
        'title': '弹性碰撞',
        'description': '动量守恒 + 动能守恒',
        'category': '物理',
        'tags': ['碰撞', 'Canvas'],
        'level': '高中',
        'params': 'm₁、m₂、v₁、v₂',
    },
    {
        'id': 'shm',
        'title': '弹簧振子 简谐运动',
        'description': 'x=A·cos(ωt+φ), ω=√(k/m)',
        'category': '物理',
        'tags': ['振动', 'Canvas'],
        'level': '高中',
        'params': '质量m、劲度系数k、振幅A',
    },
    {
        'id': 'uniform_motion',
        'title': '匀速直线运动',
        'description': 'x = x₀ + v·t，速度恒定',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'level': '高中',
        'params': '初速度v₀、初始位置x₀',
    },
    {
        'id': 'uniform_acceleration',
        'title': '匀变速直线运动',
        'description': 'v = v₀ + at; x = v₀t + ½at²',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'level': '高中',
        'params': '初速度v₀、加速度a',
    },
    {
        'id': 'vertical_throw',
        'title': '竖直上抛运动',
        'description': 'v = v₀ − gt; h = v₀t − ½gt²',
        'category': '物理',
        'tags': ['运动学', 'Canvas'],
        'level': '高中',
        'params': '初速度v₀、重力加速度g',
    },
    {
        'id': 'force_analysis',
        'title': '受力分析（共点力平衡）',
        'description': '多力合成与分解，判断平衡状态',
        'category': '物理',
        'tags': ['力学', 'Canvas'],
        'level': '高中',
        'params': 'F₁大小/角度、F₂大小/角度',
    },
    {
        'id': 'work',
        'title': '功与功率',
        'description': 'W=Fs·cosθ，正功/负功/不做功',
        'category': '物理',
        'tags': ['力学', 'Canvas'],
        'level': '高中',
        'params': '力F、位移s、夹角θ',
    },
    {
        'id': 'kinetic_energy',
        'title': '动能定理',
        'description': 'W合=½mv²−½mv₀²，合外力做功等于动能变化',
        'category': '物理',
        'tags': ['力学', 'Canvas'],
        'level': '高中',
        'params': '初速度v₀、合力F、质量m',
    },
    {
        'id': 'inelastic',
        'title': '非弹性碰撞',
        'description': '动量守恒，恢复系数e控制弹性程度',
        'category': '物理',
        'tags': ['动量', 'Canvas'],
        'level': '高中',
        'params': 'm₁、m₂、v₁、v₂、恢复系数e',
    },
    {
        'id': 'coulomb',
        'title': '库仑定律',
        'description': 'F=kq₁q₂/r²，同号排斥异号吸引',
        'category': '物理',
        'tags': ['电磁学', 'Canvas'],
        'level': '高中',
        'params': '电荷量q₁/q₂、距离r',
    },
    {
        'id': 'lens',
        'title': '凸透镜成像',
        'description': '1/u+1/v=1/f，三条特征光线',
        'category': '物理',
        'tags': ['光学', 'Canvas'],
        'level': '高中',
        'params': '物距u、焦距f',
    },
    {
        'id': 'refraction',
        'title': '光的折射（斯涅尔定律）',
        'description': 'n₁sinθ₁=n₂sinθ₂，全反射检测',
        'category': '物理',
        'tags': ['光学', 'Canvas'],
        'level': '高中',
        'params': '入射角θ₁、折射率n₁/n₂',
    },
    {
        'id': 'logarithm',
        'title': '对数函数 y=log_a(x)',
        'description': '底数a变化时曲线形态，与指数函数关于y=x对称',
        'category': '数学',
        'tags': ['对数函数', 'Canvas'],
        'level': '高中',
        'params': '底数a',
    },
    {
        'id': 'power',
        'title': '幂函数 y=x^n',
        'description': '多条幂函数曲线对比，过定点(1,1)',
        'category': '数学',
        'tags': ['幂函数', 'Canvas'],
        'level': '高中',
        'params': '指数n',
    },
    {
        'id': 'circle',
        'title': '圆的方程 (x-a)²+(y-b)²=r²',
        'description': '标准方程与一般方程，圆心半径可调',
        'category': '数学',
        'tags': ['圆', 'Canvas'],
        'level': '高中',
        'params': '圆心(a,b)、半径r',
    },
    {
        'id': 'parabola',
        'title': '抛物线 y²=2px',
        'description': '焦点、准线与抛物线定义，|PF|=|到准线距离|验证',
        'category': '数学',
        'tags': ['抛物线', 'Canvas'],
        'level': '高中',
        'params': '焦参数p',
    },
    {
        'id': 'line_circle',
        'title': '直线与圆的位置关系',
        'description': '距离d与半径r比较：相交/相切/相离',
        'category': '数学',
        'tags': ['直线圆', 'Canvas'],
        'level': '高中',
        'params': '斜率k、截距b、半径r',
    },
    {
        'id': 'vector',
        'title': '向量的加法与减法',
        'description': '平行四边形法则，合成向量与差向量',
        'category': '数学',
        'tags': ['向量', 'Canvas'],
        'level': '高中',
        'params': '向量a(x₁,y₁)、向量b(x₂,y₂)',
    },
    # ============================================================
    # 大学数学实验（新增）
    # ============================================================
    {
        'id': 'matrix',
        'title': '矩阵变换 2D',
        'description': '线性变换可视化：基向量、面积缩放、旋转/错切/反射',
        'category': '数学',
        'tags': ['线性代数', 'Canvas'],
        'level': '大学',
        'params': '2x2矩阵 [a,b;c,d]',
    },
    {
        'id': 'complex',
        'title': '复数运算',
        'description': '复平面可视化：向量表示、乘法旋转缩放、除法与共轭',
        'category': '数学',
        'tags': ['复变函数', 'Canvas'],
        'level': '大学',
        'params': 'z₁=a+bi, z₂=c+di',
    },
    {
        'id': 'fourier',
        'title': '傅里叶级数',
        'description': '正弦波叠加逼近任意周期波形，频谱分析与Gibbs现象',
        'category': '数学',
        'tags': ['傅里叶分析', 'Canvas'],
        'level': '大学',
        'params': '谐波项数N、目标波形(方波/三角波/锯齿波)',
    },
    {
        'id': 'taylor',
        'title': '泰勒展开',
        'description': '用多项式逼近函数，逐项增加观察精度变化',
        'category': '数学',
        'tags': ['泰勒级数', 'Canvas'],
        'level': '大学',
        'params': '函数选择、展开点x₀、项数N',
    },
    {
        'id': 'probability',
        'title': '常见概率分布',
        'description': 'PMF/PDF与CDF，蒙特卡洛抽样收敛模拟',
        'category': '数学',
        'tags': ['概率论', 'Canvas'],
        'level': '大学',
        'params': '均匀/伯努利/二项/泊松分布，分布参数',
    },
    {
        'id': 'gradient',
        'title': '梯度与等高线',
        'description': '多元函数等高线图、梯度向量场、方向导数',
        'category': '数学',
        'tags': ['多元微积分', 'Canvas'],
        'level': '大学',
        'params': '函数选择、动点P位置、方向角θ',
    },
    # ============================================================
    # 大学物理实验（新增）
    # ============================================================
    {
        'id': 'wave',
        'title': '简谐波',
        'description': 'y=A·sin(ωt−kx)，波的传播与质点振动',
        'category': '物理',
        'tags': ['波动', 'Canvas'],
        'level': '大学',
        'params': '振幅A、波长λ、频率f',
    },
    {
        'id': 'interference',
        'title': '双缝干涉',
        'description': 'Δx=λL/d，Young双缝干涉条纹与强度分布',
        'category': '物理',
        'tags': ['光学', 'Canvas'],
        'level': '大学',
        'params': '波长λ、缝距d、屏距L',
    },
    {
        'id': 'rc',
        'title': 'RC电路充放电',
        'description': 'τ=RC，Vc=V₀(1−e^(−t/RC))，指数充放电过程',
        'category': '物理',
        'tags': ['电磁学', 'Canvas'],
        'level': '大学',
        'params': '电阻R、电容C、电源电压V₀',
    },
    {
        'id': 'lorentz',
        'title': '洛伦兹力',
        'description': 'F=qvB，带电粒子在磁场中做匀速圆周运动',
        'category': '物理',
        'tags': ['电磁学', 'Canvas'],
        'level': '大学',
        'params': '速度v、磁感应强度B、电荷量q、质量m',
    },
    {
        'id': 'induction',
        'title': '电磁感应（法拉第定律）',
        'description': 'ε=−NdΦ/dt，导体切割磁感线产生感应电动势',
        'category': '物理',
        'tags': ['电磁学', 'Canvas'],
        'level': '大学',
        'params': '磁场B、线圈面积S、匝数N、运动速度v',
    },
    {
        'id': 'thermo',
        'title': '气体状态方程 pV=nRT',
        'description': '理想气体状态方程，等温/等压/等容/绝热过程',
        'category': '物理',
        'tags': ['热力学', 'Canvas'],
        'level': '大学',
        'params': '温度T、体积V、物质的量n',
    },
    # ===== 初中物理 =====
    {
        'id': 'sound',
        'title': '声音的传播',
        'description': '声波在不同介质中的传播，波形与波速',
        'category': '物理',
        'level': '初中',
        'tags': ['声学', 'Canvas'],
        'params': '介质类型、温度、频率',
    },
    {
        'id': 'mirror',
        'title': '平面镜成像',
        'description': '物像对称，虚像与实像的区别',
        'category': '物理',
        'level': '初中',
        'tags': ['光学', 'Canvas'],
        'params': '物体位置、观察角度',
    },
    {
        'id': 'circuit',
        'title': '简单电路',
        'description': '欧姆定律，串联/并联电路',
        'category': '物理',
        'level': '初中',
        'tags': ['电学', 'Canvas'],
        'params': '电压V、电阻R、电路类型',
    },
    {
        'id': 'lever',
        'title': '杠杆原理',
        'description': 'F₁L₁=F₂L₂，力臂与平衡',
        'category': '物理',
        'level': '初中',
        'tags': ['力学', 'Canvas'],
        'params': '力臂L₁/L₂、阻力F₂',
    },
    {
        'id': 'buoyancy',
        'title': '浮力',
        'description': '阿基米德原理，浮沉条件',
        'category': '物理',
        'level': '初中',
        'tags': ['力学', 'Canvas'],
        'params': '物体密度、液体密度、体积',
    },
    {
        'id': 'density',
        'title': '密度',
        'description': 'ρ=m/V，常见材料密度对比',
        'category': '物理',
        'level': '初中',
        'tags': ['力学', 'Canvas'],
        'params': '质量m、体积V',
    },
    # ===== 初中数学 =====
    {
        'id': 'coordinate',
        'title': '平面直角坐标系',
        'description': '四象限、坐标、对称点',
        'category': '数学',
        'level': '初中',
        'tags': ['坐标系', 'Canvas'],
        'params': '点P坐标(x,y)',
    },
    {
        'id': 'factorization',
        'title': '因式分解可视化',
        'description': '代数拼图面积模型，判别式与根',
        'category': '数学',
        'level': '初中',
        'tags': ['代数', 'Canvas'],
        'params': '系数a、b、c',
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

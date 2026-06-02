"""
Flask 应用工厂模块
==================

本模块是整个 Web 应用的入口，负责：
1. 创建 Flask 应用实例
2. 配置数据库连接（SQLite）
3. 初始化用户认证扩展（Flask-Login）
4. 注册所有路由蓝图（auth、videos、quiz、diagnosis）
5. 自动创建数据库表（如果不存在）

使用方式：
    from app import create_app
    app = create_app()

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# 加载 .env 文件中的环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# ============================================================
# 全局扩展实例
# ============================================================
# SQLAlchemy：ORM 数据库操作，用于定义模型和执行 SQL 查询
# 这些实例在 create_app() 中通过 init_app() 绑定到具体的应用
db = SQLAlchemy()

# Flask-Login：用户会话管理，处理登录/登出/会话保持
# login_view：未登录用户访问需要登录的页面时，自动跳转到登录页
# login_message：跳转时显示的提示信息
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请先登录'

# CSRFProtect：跨站请求伪造保护
# 所有 POST 表单请求都需要携带 CSRF token
csrf = CSRFProtect()


def create_app(config_name=None):
    """
    Flask 应用工厂函数

    参数：
        config_name: 配置名称（本项目暂未使用，预留扩展）

    返回：
        配置完成的 Flask 应用实例

    流程：
        1. 创建 Flask 应用
        2. 设置密钥和数据库路径
        3. 初始化扩展
        4. 注册蓝图（路由模块）
        5. 创建数据库表
    """
    app = Flask(__name__)

    # ========================================================
    # 应用配置
    # ========================================================

    # SECRET_KEY：Flask 用于加密 session cookie 和 CSRF token
    # 生产环境必须修改为随机密钥！可用 os.urandom(24) 生成
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'physics-platform-dev-key-change-in-production'
    )

    # 数据库连接字符串
    # SQLite 数据库文件存放在项目根目录下的 physics.db
    # os.path.abspath(__file__) 获取当前文件的绝对路径
    # dirname 两次得到项目根目录（app/__init__.py -> app/ -> 根目录）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'physics.db'
    )

    # 禁用 SQLAlchemy 的修改跟踪功能，节省内存
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ========================================================
    # 初始化扩展
    # ========================================================
    # 将 db 和 login_manager 绑定到当前应用
    # 这样在 models.py 中导入 db 时，才能正确工作
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # ========================================================
    # 注册蓝图（Blueprint）
    # ========================================================
    # 蓝图是 Flask 的模块化机制，每个蓝图负责一组相关的路由
    # auth_bp    → 用户认证（登录/注册/登出）
    # videos_bp  → 视频系统（列表/播放/进度上报）
    # quiz_bp    → 测试系统（答题/提交/评分）
    # diagnosis_bp → 诊断系统（薄弱点分析/推荐）
    from app.routes.auth import auth_bp
    from app.routes.videos import videos_bp
    from app.routes.quiz import quiz_bp
    from app.routes.diagnosis import diagnosis_bp
    from app.routes.experiments import experiments_bp
    from app.routes.teacher import teacher_bp
    from app.routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(experiments_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)

    # ========================================================
    # 创建数据库表
    # ========================================================
    # db.create_all() 会根据 models.py 中定义的模型自动创建表
    # 如果表已存在则跳过，不会删除已有数据
    # app_app_context() 是必要的，因为 db 操作需要在应用上下文中执行
    with app.app_context():
        db.create_all()

    return app

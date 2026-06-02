"""
数据库模型定义模块
==================

本模块定义了平台所有数据库表对应的 Python 类（ORM 模型）。

每个类对应一张数据库表，类的属性对应表的列。
Flask-SQLAlchemy 会自动将这些类转换为 SQL 语句。

数据表关系：
    users ──1:N──> quiz_records ──N:1──> questions
    users ──1:N──> watch_records ──N:1──> videos

模型列表：
    - User：用户表（注册/登录信息）
    - Video：视频表（Manim 动画视频元数据）
    - Question：测试题表（选择题题库）
    - QuizRecord：答题记录表（用户每次答题的记录）
    - WatchRecord：观看记录表（用户观看视频的进度）

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


# ============================================================
# 用户模型
# ============================================================
class User(UserMixin, db.Model):
    """
    用户模型 - 对应 users 表

    继承说明：
        - db.Model：Flask-SQLAlchemy 的基类，提供 ORM 功能
        - UserMixin：Flask-Login 的混入类，提供 is_authenticated 等属性

    属性：
        id:             用户 ID（主键，自增）
        username:       用户名（唯一，不能为空）
        password_hash:  密码哈希值（不存储明文密码！）
        email:          邮箱（可选）
        grade:          年级（默认"高一"）
        created_at:     注册时间
        last_login:     最后登录时间
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(100))
    grade = db.Column(db.String(10), default='高一')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """
        设置密码 - 将明文密码转换为哈希值存储

        使用 Werkzeug 的 generate_password_hash 函数，
        采用 pbkdf2:sha256 算法，自动加盐，安全性高。

        参数：
            password: 用户输入的明文密码
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        验证密码 - 将输入的密码与存储的哈希值比对

        参数：
            password: 用户输入的明文密码

        返回：
            True: 密码正确
            False: 密码错误
        """
        return check_password_hash(self.password_hash, password)


# ============================================================
# Flask-Login 用户加载回调
# ============================================================
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login 的用户加载回调函数

    当用户通过 session 保持登录状态时，Flask-Login 会调用此函数
    根据 user_id 从数据库加载用户对象。

    参数：
        user_id: 用户 ID（字符串类型，来自 session cookie）

    返回：
        User 对象或 None
    """
    return User.query.get(int(user_id))


# ============================================================
# 视频模型
# ============================================================
class Video(db.Model):
    """
    视频模型 - 对应 videos 表

    存储 Manim 动画视频的元数据信息。
    视频文件本身存放在 app/static/videos/ 目录，数据库只存路径。

    属性：
        id:             视频 ID（主键）
        title:          视频标题（如"匀变速直线运动"）
        description:    视频描述（详细介绍内容）
        topic:          知识点名称（如"匀变速直线运动"）
        topic_id:       知识点编号（如"kinematics_01"，用于关联题目）
        subject:        学科（默认"物理"）
        chapter:        章节（如"运动学"，用于分类筛选）
        video_path:     视频文件相对路径（如"videos/01_匀变速.mp4"）
        cover_path:     封面图路径（可选）
        duration:       视频时长（秒）
        difficulty:     难度等级（1-5）
        prerequisites:  前置知识点（JSON 数组字符串）
        related:        关联知识点（JSON 数组字符串）
        created_at:     创建时间
    """
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    topic = db.Column(db.String(100), nullable=False)
    topic_id = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(20), default='物理')
    chapter = db.Column(db.String(50))
    video_path = db.Column(db.String(300), nullable=False)
    cover_path = db.Column(db.String(300))
    duration = db.Column(db.Integer)
    difficulty = db.Column(db.Integer, default=2)
    # prerequisites 和 related 存储 JSON 数组字符串
    # 例如: '["kinematics_01", "kinematics_02"]'
    # 读取时需要用 json.loads() 解析
    prerequisites = db.Column(db.Text)
    related = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


# ============================================================
# 测试题模型
# ============================================================
class Question(db.Model):
    """
    测试题模型 - 对应 questions 表

    存储选择题题库。每道题关联一个知识点（topic_id），
    可以通过知识点筛选题目进行组卷。

    属性：
        id:             题目 ID（主键）
        topic_id:       关联知识点编号（如"kinematics_01"）
        content:        题目内容
        option_a:       选项 A
        option_b:       选项 B
        option_c:       选项 C
        option_d:       选项 D
        answer:         正确答案（A/B/C/D 之一）
        explanation:    答案解析
        difficulty:     难度等级（1-5）
        created_at:     创建时间
    """
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=2)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


# ============================================================
# 答题记录模型
# ============================================================
class QuizRecord(db.Model):
    """
    答题记录模型 - 对应 quiz_records 表

    记录用户每次答题的详细信息，用于：
    1. 诊断算法统计知识点正确率
    2. 学习进度追踪
    3. 数据分析

    属性：
        id:             记录 ID（主键）
        user_id:        用户 ID（外键 → users.id）
        question_id:    题目 ID（外键 → questions.id）
        user_answer:    用户的答案（A/B/C/D）
        is_correct:     是否正确（True/False）
        response_time:  答题用时（秒，可选）
        answered_at:    答题时间

    关系：
        question: 通过 question_id 关联到 Question 模型
                  可以用 record.question.content 获取题目内容
    """
    __tablename__ = 'quiz_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.String(1))
    is_correct = db.Column(db.Boolean)
    response_time = db.Column(db.Integer)
    answered_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # SQLAlchemy 关系定义：通过外键自动关联
    # 使用方法：record.question → Question 对象
    question = db.relationship('Question', backref='records')

    # 数据库索引：加速按用户查询答题记录
    __table_args__ = (
        db.Index('idx_quiz_user_id', 'user_id'),
        db.Index('idx_quiz_question_id', 'question_id'),
    )


# ============================================================
# 观看记录模型
# ============================================================
class WatchRecord(db.Model):
    """
    观看记录模型 - 对应 watch_records 表

    记录用户观看视频的进度，支持：
    1. 记录观看进度百分比（0-100）
    2. 标记是否看完（progress >= 95% 视为看完）
    3. 进度只能前进不能后退（防止回退）

    属性：
        id:               记录 ID（主键）
        user_id:          用户 ID（外键 → users.id）
        video_id:         视频 ID（外键 → videos.id）
        watch_progress:   观看进度（0-100 的整数）
        is_completed:     是否看完（True/False）
        watched_at:       最后更新时间

    关系：
        video: 通过 video_id 关联到 Video 模型
    """
    __tablename__ = 'watch_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    watch_progress = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    watched_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # 关系定义：record.video → Video 对象
    video = db.relationship('Video', backref='watch_records')

    # 数据库索引：加速按用户查询观看记录
    __table_args__ = (
        db.Index('idx_watch_user_id', 'user_id'),
        db.Index('idx_watch_video_id', 'video_id'),
    )


# ============================================================
# 收藏模型
# ============================================================
class Favorite(db.Model):
    """
    收藏模型 - 对应 favorites 表

    记录用户收藏的视频或实验，支持：
    1. 收藏/取消收藏切换
    2. 按类型区分（video / experiment）
    3. 唯一约束防止重复收藏

    属性：
        id:         主键
        user_id:    用户 ID（外键）
        item_type:  收藏类型（'video' 或 'experiment'）
        item_id:    收藏对象 ID（视频 ID 或实验文件名）
        created_at: 收藏时间
    """
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'video' / 'experiment'
    item_id = db.Column(db.String(100), nullable=False)   # 视频ID 或 实验文件名
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # 唯一约束：同一用户不能重复收藏同一项目
    __table_args__ = (
        db.UniqueConstraint('user_id', 'item_type', 'item_id', name='uq_user_favorite'),
        db.Index('idx_fav_user_id', 'user_id'),
    )

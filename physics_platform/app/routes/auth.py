"""
用户认证路由模块
================

本模块处理所有与用户认证相关的请求：
- 首页重定向（/）
- 用户登录（/login）
- 用户注册（/register）
- 用户登出（/logout）

路由蓝图：auth_bp
注册前缀：无（使用根路径 /）

安全说明：
- 密码使用 Werkzeug 的哈希算法存储，数据库中不保存明文
- 登录状态通过 Flask-Login 的 session 保持
- 所有密码操作都在服务端完成

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

from datetime import datetime, timezone
from urllib.parse import urlparse
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

# 创建蓝图实例
# Blueprint 是 Flask 的模块化机制，将路由分组管理
auth_bp = Blueprint('auth', __name__)


# ============================================================
# 首页路由
# ============================================================
@auth_bp.route('/')
def index():
    """
    首页 - 根据登录状态重定向

    已登录 → 跳转到视频列表页
    未登录 → 跳转到登录页
    """
    if current_user.is_authenticated:
        if current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))


# ============================================================
# 登录路由
# ============================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页面

    GET 请求：显示登录表单
    POST 请求：处理登录逻辑

    登录流程：
    1. 验证用户名和密码是否为空
    2. 从数据库查找用户
    3. 验证密码哈希
    4. 更新最后登录时间
    5. 调用 login_user() 建立会话
    6. 重定向到视频列表页（或之前访问的页面）
    """
    # 已登录用户直接跳转
    if current_user.is_authenticated:
        return redirect(url_for('videos.video_list'))

    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # 验证：用户名和密码不能为空
        if not username or not password:
            flash('请填写用户名和密码', 'error')
            return render_template('login.html')

        # 从数据库查找用户
        user = User.query.filter_by(username=username).first()

        # 验证用户存在且密码正确
        if user is None or not user.check_password(password):
            flash('用户名或密码错误', 'error')
            return render_template('login.html')

        # 更新最后登录时间
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # 建立登录会话
        # login_user() 会将用户信息存入 session cookie
        login_user(user)

        # 登录后跳转到之前访问的页面（如果有）
        # request.args.get('next') 来自 Flask-Login 的重定向参数
        # 安全检查：防止开放重定向攻击（只允许本站内部跳转）
        next_page = request.args.get('next')
        if next_page and urlparse(next_page).netloc:
            next_page = None

        # 根据角色跳转到不同首页
        if next_page:
            return redirect(next_page)
        if user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        return redirect(url_for('student.dashboard'))

    # GET 请求：显示登录表单
    return render_template('login.html')


# ============================================================
# 注册路由
# ============================================================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册页面

    注册流程：
    1. 表单验证（用户名长度、密码一致性、密码长度）
    2. 检查用户名是否已存在
    3. 创建用户对象并设置密码哈希
    4. 保存到数据库
    5. 跳转到登录页
    """
    if current_user.is_authenticated:
        return redirect(url_for('videos.video_list'))

    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        email = request.form.get('email', '').strip()
        grade = request.form.get('grade', '高一')
        role = request.form.get('role', 'student')

        # ---- 表单验证 ----

        # 必填字段验证
        if not username or not password:
            flash('请填写用户名和密码', 'error')
            return render_template('register.html')

        # 用户名长度验证
        if len(username) < 2 or len(username) > 50:
            flash('用户名长度需在 2-50 个字符之间', 'error')
            return render_template('register.html')

        # 密码一致性验证
        if password != confirm:
            flash('两次输入的密码不一致', 'error')
            return render_template('register.html')

        # 密码长度验证
        if len(password) < 6:
            flash('密码长度至少 6 个字符', 'error')
            return render_template('register.html')

        # 用户名唯一性验证
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'error')
            return render_template('register.html')

        # ---- 创建用户 ----
        if role not in ('student', 'teacher'):
            role = 'student'
        user = User(username=username, email=email, grade=grade, role=role)
        user.set_password(password)  # 生成密码哈希
        db.session.add(user)
        db.session.commit()

        flash('注册成功，请登录', 'success')
        return redirect(url_for('auth.login'))

    # GET 请求：显示注册表单
    return render_template('register.html')


# ============================================================
# 登出路由
# ============================================================
@auth_bp.route('/logout')
@login_required  # 必须登录才能登出
def logout():
    """
    登出 - 清除用户会话

    logout_user() 会清除 session 中的用户信息，
    用户回到未登录状态。
    """
    logout_user()
    return redirect(url_for('auth.login'))


# ============================================================
# 个人中心路由
# ============================================================
@auth_bp.route('/profile')
@login_required
def profile():
    """
    个人中心页面 - 显示用户信息和学习概览

    功能：
        1. 显示用户基本信息（用户名、年级、注册时间）
        2. 显示学习统计（视频观看数、答题数、正确率）
        3. 提供修改个人信息的入口（二期功能）
    """
    return render_template('profile.html')


@auth_bp.route('/profile/update', methods=['POST'])
@login_required
def profile_update():
    """处理个人中心的修改保存"""
    grade = request.form.get('grade', '').strip()
    email = request.form.get('email', '').strip()
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_new_password', '')

    # 更新年级
    if grade in ('高一', '高二', '高三'):
        current_user.grade = grade

    # 更新邮箱
    current_user.email = email

    # 修改密码（仅在用户填写了新密码时）
    if new_password:
        if len(new_password) < 6:
            flash('密码长度至少 6 个字符', 'error')
            return redirect(url_for('auth.profile'))
        if new_password != confirm_password:
            flash('两次输入的新密码不一致', 'error')
            return redirect(url_for('auth.profile'))
        current_user.set_password(new_password)

    db.session.commit()
    flash('个人信息已更新', 'success')
    return redirect(url_for('auth.profile'))

"""
教师端路由模块
=============

本模块处理教师端所有功能：
- 教师控制台首页（/teacher/dashboard）
- 班级管理（/teacher/classes, /teacher/class/<id>）
- 发布作业（/teacher/assignment/new）
- 作业列表（/teacher/assignments）
- 数据统计（/teacher/statistics）

路由蓝图：teacher_bp
注册前缀：/teacher

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-02
"""

import json
import secrets
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    User, Video, Question, QuizRecord, WatchRecord,
    Class, ClassMember, Assignment, AssignmentRecord
)

# 创建蓝图实例
teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')


def teacher_required(f):
    """教师权限装饰器：只允许教师角色访问"""
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'teacher':
            flash('仅教师可访问此页面', 'error')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated


# ============================================================
# 教师控制台首页
# ============================================================
@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    """
    教师控制台首页

    显示：
    1. 快捷操作入口（创建班级、发布作业、数据统计）
    2. 我的班级列表（学生人数、平均正确率）
    3. 最近作业及完成情况
    """
    # 获取教师创建的班级
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    class_list = []
    for cls in classes:
        member_count = ClassMember.query.filter_by(class_id=cls.id).count()
        # 计算班级平均正确率
        member_ids = [m.student_id for m in ClassMember.query.filter_by(class_id=cls.id).all()]
        avg_accuracy = 0
        if member_ids:
            records = QuizRecord.query.filter(QuizRecord.user_id.in_(member_ids)).all()
            if records:
                correct = sum(1 for r in records if r.is_correct)
                avg_accuracy = round(correct / len(records) * 100)
        class_list.append({
            'id': cls.id,
            'name': cls.name,
            'invite_code': cls.invite_code,
            'student_count': member_count,
            'avg_accuracy': avg_accuracy,
        })

    # 获取最近的作业
    assignments = Assignment.query.filter_by(
        teacher_id=current_user.id
    ).order_by(Assignment.created_at.desc()).limit(5).all()

    assignment_list = []
    for a in assignments:
        cls = Class.query.get(a.class_id)
        total_students = ClassMember.query.filter_by(class_id=a.class_id).count()
        completed_count = AssignmentRecord.query.filter_by(assignment_id=a.id).count()
        records = AssignmentRecord.query.filter_by(assignment_id=a.id).all()
        avg_score = round(sum(r.score or 0 for r in records) / len(records)) if records else 0

        assignment_list.append({
            'id': a.id,
            'title': a.title,
            'class_name': cls.name if cls else '未知班级',
            'due_date': a.due_date.strftime('%m-%d') if a.due_date else '无期限',
            'completed_count': completed_count,
            'total_students': total_students,
            'avg_score': avg_score,
        })

    return render_template('teacher/dashboard.html',
                           classes=class_list,
                           recent_assignments=assignment_list)


# ============================================================
# 班级管理
# ============================================================
@teacher_bp.route('/classes')
@teacher_required
def classes():
    """教师班级列表"""
    class_list = Class.query.filter_by(teacher_id=current_user.id).all()
    result = []
    for cls in class_list:
        member_count = ClassMember.query.filter_by(class_id=cls.id).count()
        result.append({
            'id': cls.id,
            'name': cls.name,
            'invite_code': cls.invite_code,
            'student_count': member_count,
            'created_at': cls.created_at.strftime('%Y-%m-%d'),
        })
    return render_template('teacher/classes.html', classes=result)


@teacher_bp.route('/class/new', methods=['GET', 'POST'])
@teacher_required
def new_class():
    """创建新班级"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('请输入班级名称', 'error')
            return render_template('teacher/new_class.html')

        # 生成 6 位邀请码
        invite_code = secrets.token_hex(3).upper()

        cls = Class(
            name=name,
            teacher_id=current_user.id,
            invite_code=invite_code
        )
        db.session.add(cls)
        db.session.commit()

        flash(f'班级创建成功！邀请码：{invite_code}', 'success')
        return redirect(url_for('teacher.dashboard'))

    return render_template('teacher/new_class.html')


@teacher_bp.route('/class/<int:class_id>')
@teacher_required
def class_detail(class_id):
    """班级详情 - 查看学生列表和学习统计"""
    cls = Class.query.get_or_404(class_id)
    if cls.teacher_id != current_user.id:
        flash('无权访问此班级', 'error')
        return redirect(url_for('teacher.dashboard'))

    # 获取班级成员
    members = ClassMember.query.filter_by(class_id=class_id).all()
    student_list = []
    for m in members:
        student = User.query.get(m.student_id)
        if not student:
            continue
        # 统计该学生的答题情况
        records = QuizRecord.query.filter_by(user_id=student.id).all()
        total = len(records)
        correct = sum(1 for r in records if r.is_correct)
        accuracy = round(correct / total * 100) if total > 0 else 0

        student_list.append({
            'id': student.id,
            'username': student.username,
            'grade': student.grade,
            'joined_at': m.joined_at.strftime('%Y-%m-%d'),
            'total_questions': total,
            'accuracy': accuracy,
        })

    return render_template('teacher/class_detail.html',
                           cls={'id': cls.id, 'name': cls.name, 'invite_code': cls.invite_code},
                           students=student_list)


# ============================================================
# 发布作业
# ============================================================
@teacher_bp.route('/assignment/new', methods=['GET', 'POST'])
@teacher_required
def new_assignment():
    """发布新作业"""
    # 获取教师的班级列表
    classes = Class.query.filter_by(teacher_id=current_user.id).all()

    # 获取所有知识点（从视频表提取）
    videos = Video.query.all()
    topics = {}
    for v in videos:
        if v.topic_id not in topics:
            topics[v.topic_id] = v.topic
    topic_list = [{'id': k, 'name': v} for k, v in topics.items()]

    if request.method == 'POST':
        class_id = request.form.get('class_id', type=int)
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        topic_ids = request.form.getlist('topic_ids')
        question_count = request.form.get('question_count', 10, type=int)
        due_date_str = request.form.get('due_date', '')

        if not class_id or not title:
            flash('请填写班级和作业标题', 'error')
            return render_template('teacher/new_assignment.html',
                                   classes=classes, topics=topic_list)

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                pass

        assignment = Assignment(
            class_id=class_id,
            teacher_id=current_user.id,
            title=title,
            description=description,
            topic_ids=json.dumps(topic_ids),
            question_count=question_count,
            due_date=due_date,
        )
        db.session.add(assignment)
        db.session.commit()

        flash('作业发布成功！', 'success')
        return redirect(url_for('teacher.assignments'))

    return render_template('teacher/new_assignment.html',
                           classes=classes, topics=topic_list)


# ============================================================
# 作业列表
# ============================================================
@teacher_bp.route('/assignments')
@teacher_required
def assignments():
    """教师发布的所有作业"""
    assignment_list = Assignment.query.filter_by(
        teacher_id=current_user.id
    ).order_by(Assignment.created_at.desc()).all()

    result = []
    for a in assignment_list:
        cls = Class.query.get(a.class_id)
        total_students = ClassMember.query.filter_by(class_id=a.class_id).count()
        completed_count = AssignmentRecord.query.filter_by(assignment_id=a.id).count()
        records = AssignmentRecord.query.filter_by(assignment_id=a.id).all()
        avg_score = round(sum(r.score or 0 for r in records) / len(records)) if records else 0

        is_urgent = False
        if a.due_date:
            try:
                due = a.due_date.replace(tzinfo=timezone.utc) if a.due_date.tzinfo is None else a.due_date
                is_urgent = due < datetime.now(timezone.utc)
            except Exception:
                is_urgent = False

        result.append({
            'id': a.id,
            'title': a.title,
            'class_name': cls.name if cls else '未知',
            'due_date': a.due_date.strftime('%Y-%m-%d') if a.due_date else '无期限',
            'completed_count': completed_count,
            'total_students': total_students,
            'avg_score': avg_score,
            'is_urgent': is_urgent,
            'created_at': a.created_at.strftime('%Y-%m-%d'),
        })

    return render_template('teacher/assignments.html', assignments=result)


@teacher_bp.route('/assignment/<int:assignment_id>')
@teacher_required
def assignment_detail(assignment_id):
    """作业详情 - 查看完成情况"""
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.teacher_id != current_user.id:
        flash('无权访问', 'error')
        return redirect(url_for('teacher.assignments'))

    cls = Class.query.get(assignment.class_id)

    # 获取班级所有学生
    members = ClassMember.query.filter_by(class_id=assignment.class_id).all()
    records = AssignmentRecord.query.filter_by(assignment_id=assignment_id).all()
    record_map = {r.student_id: r for r in records}

    student_results = []
    for m in members:
        student = User.query.get(m.student_id)
        if not student:
            continue
        rec = record_map.get(student.id)
        student_results.append({
            'username': student.username,
            'completed': rec is not None,
            'score': rec.score if rec else None,
            'correct_count': rec.correct_count if rec else None,
            'total_count': rec.total_count if rec else None,
            'completed_at': rec.completed_at.strftime('%m-%d %H:%M') if rec and rec.completed_at else '-',
        })

    # 解析关联知识点
    topic_ids = json.loads(assignment.topic_ids) if assignment.topic_ids else []
    topic_names = []
    for tid in topic_ids:
        v = Video.query.filter_by(topic_id=tid).first()
        topic_names.append(v.topic if v else tid)

    return render_template('teacher/assignment_detail.html',
                           assignment=assignment,
                           cls={'name': cls.name} if cls else None,
                           students=student_results,
                           topic_names=topic_names)


# ============================================================
# 撤回（删除）作业
# ============================================================
@teacher_bp.route('/assignment/<int:assignment_id>/delete', methods=['POST'])
@teacher_required
def delete_assignment(assignment_id):
    """
    撤回作业 - 删除作业及其所有完成记录

    安全检查：
    1. 只能删除自己创建的作业
    2. 同时删除关联的 assignment_records
    """
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.teacher_id != current_user.id:
        flash('无权操作', 'error')
        return redirect(url_for('teacher.assignments'))

    title = assignment.title

    # 先删除关联的完成记录
    AssignmentRecord.query.filter_by(assignment_id=assignment_id).delete()
    db.session.delete(assignment)
    db.session.commit()

    flash(f'已撤回作业：{title}', 'success')
    return redirect(url_for('teacher.assignments'))


# ============================================================
# 数据统计
# ============================================================
@teacher_bp.route('/statistics')
@teacher_required
def statistics():
    """教师数据统计总览"""
    # 获取所有班级
    classes = Class.query.filter_by(teacher_id=current_user.id).all()
    total_students = 0
    total_questions = 0
    total_correct = 0

    class_stats = []
    for cls in classes:
        members = ClassMember.query.filter_by(class_id=cls.id).all()
        member_ids = [m.student_id for m in members]
        student_count = len(member_ids)
        total_students += student_count

        if member_ids:
            records = QuizRecord.query.filter(QuizRecord.user_id.in_(member_ids)).all()
            cls_correct = sum(1 for r in records if r.is_correct)
            cls_total = len(records)
            total_questions += cls_total
            total_correct += cls_correct
            avg_acc = round(cls_correct / cls_total * 100) if cls_total > 0 else 0
        else:
            avg_acc = 0

        class_stats.append({
            'name': cls.name,
            'student_count': student_count,
            'total_questions': len(records) if member_ids else 0,
            'avg_accuracy': avg_acc,
        })

    overall_accuracy = round(total_correct / total_questions * 100) if total_questions > 0 else 0

    return render_template('teacher/statistics.html',
                           classes=class_stats,
                           total_students=total_students,
                           total_questions=total_questions,
                           overall_accuracy=overall_accuracy)

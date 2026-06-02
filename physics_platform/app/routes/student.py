"""
学生端路由模块
=============

本模块处理学生端扩展功能：
- 学生控制台首页（/student/dashboard）
- 加入班级（/student/join-class）
- 我的班级（/student/class）
- 学习报告（/student/report）
- AI 答疑助手（/student/ai-tutor）
- 知识图谱（/student/knowledge-graph）

路由蓝图：student_bp
注册前缀：/student

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-02
"""

import json
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    User, Video, Question, QuizRecord, WatchRecord,
    Class, ClassMember, Assignment, AssignmentRecord
)

# 创建蓝图实例
student_bp = Blueprint('student', __name__, url_prefix='/student')


def student_required(f):
    """学生权限装饰器：只允许学生角色访问"""
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'student':
            flash('仅学生可访问此页面', 'error')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated


# ============================================================
# 学生控制台首页
# ============================================================
@student_bp.route('/dashboard')
@student_required
def dashboard():
    """
    学生控制台首页

    显示：
    1. 学习概览卡片（学习时长、正确率、视频进度、实验完成数）
    2. 我的班级信息
    3. 待完成作业列表
    4. 薄弱知识点提示
    """
    # ---- 学习统计 ----
    # 观看的视频数
    watched_videos = WatchRecord.query.filter_by(
        user_id=current_user.id, is_completed=True
    ).count()
    total_videos = Video.query.count()

    # 答题统计
    records = QuizRecord.query.filter_by(user_id=current_user.id).all()
    total_questions = len(records)
    total_correct = sum(1 for r in records if r.is_correct)
    avg_accuracy = round(total_correct / total_questions * 100) if total_questions > 0 else 0

    # 学习时长（估算：每视频平均 10 分钟）
    total_study_hours = round(watched_videos * 10 / 60, 1)

    # ---- 我的班级 ----
    my_class = None
    class_member = ClassMember.query.filter_by(student_id=current_user.id).first()
    if class_member:
        cls = Class.query.get(class_member.class_id)
        if cls:
            teacher = User.query.get(cls.teacher_id)
            my_class = {
                'id': cls.id,
                'name': cls.name,
                'teacher_name': teacher.username if teacher else '未知',
            }

    # ---- 待完成作业 ----
    pending_assignments = []
    if class_member:
        assignments = Assignment.query.filter_by(class_id=class_member.class_id).all()
        for a in assignments:
            # 检查是否已完成
            existing = AssignmentRecord.query.filter_by(
                assignment_id=a.id, student_id=current_user.id
            ).first()
            if existing:
                continue

            # 计算剩余天数
            days_left = None
            is_urgent = False
            if a.due_date:
                try:
                    due = a.due_date.replace(tzinfo=timezone.utc) if a.due_date.tzinfo is None else a.due_date
                    delta = due - datetime.now(timezone.utc)
                    days_left = max(0, delta.days)
                    is_urgent = days_left <= 1
                except Exception:
                    pass

            # 获取知识点名称
            topic_ids = json.loads(a.topic_ids) if a.topic_ids else []
            topic_names = []
            for tid in topic_ids:
                v = Video.query.filter_by(topic_id=tid).first()
                topic_names.append(v.topic if v else tid)

            pending_assignments.append({
                'id': a.id,
                'title': a.title,
                'topic_names': ', '.join(topic_names[:3]),
                'days_left': days_left,
                'is_urgent': is_urgent,
            })

    # ---- 薄弱知识点 ----
    # 从诊断逻辑复用
    from app.routes.diagnosis import diagnose_user
    diag_results = diagnose_user(current_user.id)
    weak_topics = [
        {'name': r['topic_name'], 'accuracy': r['accuracy'], 'id': r['topic_id']}
        for r in diag_results if r['level'] in ('薄弱', '待巩固')
    ][:5]

    return render_template('student/dashboard.html',
                           total_study_hours=total_study_hours,
                           avg_accuracy=avg_accuracy,
                           watched_videos=watched_videos,
                           total_videos=total_videos,
                           my_class=my_class,
                           pending_assignments=pending_assignments,
                           weak_topics=weak_topics)


# ============================================================
# 加入班级
# ============================================================
@student_bp.route('/join-class', methods=['POST'])
@student_required
def join_class():
    """通过邀请码加入班级"""
    invite_code = request.form.get('invite_code', '').strip().upper()
    if not invite_code:
        flash('请输入邀请码', 'error')
        return redirect(url_for('student.dashboard'))

    cls = Class.query.filter_by(invite_code=invite_code).first()
    if not cls:
        flash('邀请码无效，请检查后重试', 'error')
        return redirect(url_for('student.dashboard'))

    # 检查是否已在班级中
    existing = ClassMember.query.filter_by(
        class_id=cls.id, student_id=current_user.id
    ).first()
    if existing:
        flash('你已经在这个班级中了', 'info')
        return redirect(url_for('student.class_page'))

    # 加入班级
    member = ClassMember(class_id=cls.id, student_id=current_user.id)
    db.session.add(member)
    db.session.commit()

    flash(f'成功加入班级：{cls.name}', 'success')
    return redirect(url_for('student.class_page'))


# ============================================================
# 我的班级
# ============================================================
@student_bp.route('/class')
@student_required
def class_page():
    """学生查看所在班级和作业"""
    class_member = ClassMember.query.filter_by(student_id=current_user.id).first()
    if not class_member:
        flash('你还没有加入任何班级', 'info')
        return redirect(url_for('student.dashboard'))

    cls = Class.query.get(class_member.class_id)
    if not cls:
        flash('班级不存在', 'error')
        return redirect(url_for('student.dashboard'))

    teacher = User.query.get(cls.teacher_id)

    # 获取班级作业
    assignments = Assignment.query.filter_by(class_id=cls.id).order_by(
        Assignment.created_at.desc()
    ).all()

    assignment_list = []
    for a in assignments:
        record = AssignmentRecord.query.filter_by(
            assignment_id=a.id, student_id=current_user.id
        ).first()

        days_left = None
        is_urgent = False
        if a.due_date:
            try:
                due = a.due_date.replace(tzinfo=timezone.utc) if a.due_date.tzinfo is None else a.due_date
                delta = due - datetime.now(timezone.utc)
                days_left = max(0, delta.days)
                is_urgent = days_left <= 1 and not record
            except Exception:
                pass

        assignment_list.append({
            'id': a.id,
            'title': a.title,
            'description': a.description or '',
            'due_date': a.due_date.strftime('%Y-%m-%d') if a.due_date else '无期限',
            'completed': record is not None,
            'score': record.score if record else None,
            'days_left': days_left,
            'is_urgent': is_urgent,
        })

    # 班级成员数
    member_count = ClassMember.query.filter_by(class_id=cls.id).count()

    return render_template('student/class_page.html',
                           cls={'name': cls.name, 'invite_code': cls.invite_code},
                           teacher_name=teacher.username if teacher else '未知',
                           assignments=assignment_list,
                           member_count=member_count)


# ============================================================
# 做作业页面
# ============================================================
@student_bp.route('/assignment/<int:assignment_id>/do')
@student_required
def do_assignment(assignment_id):
    """
    做作业页面 - 显示作业题目供学生答题

    流程：
    1. 检查作业是否存在、学生是否在该班级
    2. 检查是否已完成（不允许重做）
    3. 根据作业的 topic_ids 和 question_count 从题库抽题
    4. 渲染答题页面
    """
    import random

    assignment = Assignment.query.get_or_404(assignment_id)

    # 检查学生是否在该班级
    class_member = ClassMember.query.filter_by(
        class_id=assignment.class_id, student_id=current_user.id
    ).first()
    if not class_member:
        flash('你不在该班级中', 'error')
        return redirect(url_for('student.dashboard'))

    # 检查是否已完成
    existing = AssignmentRecord.query.filter_by(
        assignment_id=assignment_id, student_id=current_user.id
    ).first()
    if existing:
        flash('你已经完成过这个作业了', 'info')
        return redirect(url_for('student.class_page'))

    # 解析关联知识点
    topic_ids = json.loads(assignment.topic_ids) if assignment.topic_ids else []
    if not topic_ids:
        flash('该作业未关联知识点', 'error')
        return redirect(url_for('student.class_page'))

    # 从题库抽题：按知识点筛选，随机抽取
    all_questions = Question.query.filter(
        Question.topic_id.in_(topic_ids)
    ).all()

    if not all_questions:
        flash('该作业关联的知识点暂无题目', 'error')
        return redirect(url_for('student.class_page'))

    count = min(assignment.question_count or 10, len(all_questions))
    selected = random.sample(all_questions, count)

    # 获取知识点名称
    topic_names = {}
    for tid in topic_ids:
        v = Video.query.filter_by(topic_id=tid).first()
        topic_names[tid] = v.topic if v else tid

    # 序列化题目（带上索引，模板用）
    questions_data = []
    for idx, q in enumerate(selected):
        questions_data.append({
            'idx': idx,
            'id': q.id,
            'question': q.content,
            'options': [q.option_a, q.option_b, q.option_c, q.option_d],
            'answer': 'ABCD'.index(q.answer),
            'explanation': q.explanation or '',
            'topic_name': topic_names.get(q.topic_id, q.topic_id),
        })

    return render_template('student/do_assignment.html',
                           assignment=assignment,
                           questions=questions_data,
                           total_count=count)


# ============================================================
# 提交作业 API
# ============================================================
@student_bp.route('/api/assignment/<int:assignment_id>/submit', methods=['POST'])
@login_required
def submit_assignment(assignment_id):
    """
    提交作业答案

    请求格式：
        POST /api/assignment/<id>/submit
        Content-Type: application/json
        Body: {"answers": [{"question_id": 1, "answer": "C"}, ...]}

    处理流程：
    1. 验证作业和学生身份
    2. 逐题评分
    3. 保存到 AssignmentRecord
    4. 同时保存到 QuizRecord（用于诊断）
    5. 返回成绩
    """
    assignment = Assignment.query.get_or_404(assignment_id)

    # 验证学生在班级中
    class_member = ClassMember.query.filter_by(
        class_id=assignment.class_id, student_id=current_user.id
    ).first()
    if not class_member:
        return jsonify({'error': '无权操作'}), 403

    # 检查是否已提交
    existing = AssignmentRecord.query.filter_by(
        assignment_id=assignment_id, student_id=current_user.id
    ).first()
    if existing:
        return jsonify({'error': '已经提交过了'}), 400

    data = request.get_json()
    answers = data.get('answers', [])

    if not answers:
        return jsonify({'error': '答案不能为空'}), 400

    correct_count = 0
    total = len(answers)

    for item in answers:
        question_id = item.get('question_id')
        user_answer = item.get('answer', '').upper()

        question = Question.query.get(question_id)
        if not question:
            continue

        is_correct = user_answer == question.answer
        if is_correct:
            correct_count += 1

        # 保存到 quiz_records（用于诊断系统）
        record = QuizRecord(
            user_id=current_user.id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
        )
        db.session.add(record)

    # 计算得分（百分制）
    score = round(correct_count / total * 100) if total > 0 else 0

    # 保存作业完成记录
    assignment_record = AssignmentRecord(
        assignment_id=assignment_id,
        student_id=current_user.id,
        score=score,
        correct_count=correct_count,
        total_count=total,
        completed_at=datetime.now(timezone.utc),
    )
    db.session.add(assignment_record)
    db.session.commit()

    return jsonify({
        'score': score,
        'correct_count': correct_count,
        'total': total,
        'message': f'作业提交成功！得分：{score}分（{correct_count}/{total}）'
    })


# ============================================================
# 学习报告
# ============================================================
@student_bp.route('/report')
@student_required
def report():
    """学习报告 - 数据可视化"""
    # 获取答题记录
    records = QuizRecord.query.filter_by(user_id=current_user.id).all()

    # 基础统计
    total = len(records)
    correct = sum(1 for r in records if r.is_correct)
    overall_accuracy = round(correct / total * 100) if total > 0 else 0

    # 近 7 天学习时长（按天统计答题数 * 平均 2 分钟/题）
    study_dates = []
    study_hours = []
    for i in range(6, -1, -1):
        day = datetime.now(timezone.utc) - timedelta(days=i)
        day_str = day.strftime('%m/%d')
        day_records = [r for r in records if r.answered_at and
                       r.answered_at.date() == day.date()]
        study_dates.append(day_str)
        study_hours.append(round(len(day_records) * 2 / 60, 1))

    # 知识点掌握分布
    from app.routes.diagnosis import diagnose_user
    diag = diagnose_user(current_user.id)
    mastered_count = sum(1 for d in diag if d['level'] == '已掌握')
    learning_count = sum(1 for d in diag if d['level'] == '待巩固')
    weak_count = sum(1 for d in diag if d['level'] == '薄弱')

    # 各知识点正确率
    question_types = [d['topic_name'][:6] for d in diag[:8]]
    type_accuracies = [d['accuracy'] for d in diag[:8]]

    # 能力评分（简化版）
    ability_scores = [
        min(100, overall_accuracy + 10),   # 概念理解
        min(100, overall_accuracy - 5),    # 公式运用
        min(100, overall_accuracy + 5),    # 图像分析
        min(100, overall_accuracy - 10),   # 实验探究
        min(100, overall_accuracy),        # 综合应用
    ]

    # 学习建议
    suggestions = []
    weak_topics = [d for d in diag if d['level'] in ('薄弱', '待巩固')]
    for wt in weak_topics[:3]:
        suggestions.append({
            'icon': '⚠️',
            'title': f'加强「{wt["topic_name"]}」',
            'description': f'当前正确率 {wt["accuracy"]}%，建议多做练习',
            'link': url_for('videos.video_list', topic=wt['topic_id']),
        })

    if not suggestions:
        suggestions.append({
            'icon': '🎉',
            'title': '继续保持！',
            'description': '你目前没有明显的薄弱知识点',
            'link': url_for('videos.video_list'),
        })

    return render_template('student/report.html',
                           report_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                           weekly_hours=round(sum(study_hours), 1),
                           weekly_trend=15,  # 简化：固定值
                           mastery_rate=overall_accuracy,
                           class_rank=max(1, 30 - correct),
                           class_total=30,
                           study_dates=study_dates,
                           study_hours=study_hours,
                           mastered_count=mastered_count,
                           learning_count=learning_count,
                           weak_count=weak_count,
                           question_types=question_types,
                           type_accuracies=type_accuracies,
                           ability_scores=ability_scores,
                           suggestions=suggestions)


# ============================================================
# AI 答疑助手页面
# ============================================================
@student_bp.route('/ai-tutor')
@student_required
def ai_tutor():
    """AI 物理助教聊天页面"""
    return render_template('student/ai_tutor.html')


# ============================================================
# AI 答疑 API
# ============================================================
@student_bp.route('/api/ai-tutor', methods=['POST'])
@login_required
def api_ai_tutor():
    """AI 答疑接口 - 调用 DeepSeek API"""
    import os
    import requests as http_requests

    data = request.get_json()
    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': '问题不能为空'}), 400

    api_key = os.environ.get('DEEPSEEK_API_KEY', '')
    if not api_key:
        return jsonify({
            'answer': 'AI 答疑服务暂未配置。请联系管理员配置 DeepSeek API 密钥。'
        })

    system_prompt = """你是一位高中物理 AI 助教，专门帮助学生理解物理概念和解题。

你的特点：
1. 用通俗易懂的语言解释复杂概念
2. 喜欢使用类比和可视化描述
3. 解题时一步步引导，而不是直接给答案
4. 使用 LaTeX 格式写公式，如 $F = ma$
5. 鼓励学生思考，培养物理直觉

回答要简洁实用，适合高中生阅读。"""

    try:
        response = http_requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': f'学生问题：{question}'}
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content']
            return jsonify({'answer': answer})
        else:
            return jsonify({'answer': 'AI 服务暂时不可用，请稍后重试。'}), 502

    except Exception as e:
        return jsonify({'answer': f'AI 服务连接失败：{str(e)}'}), 502


# ============================================================
# 知识图谱页面
# ============================================================
@student_bp.route('/knowledge-graph')
@student_required
def knowledge_graph():
    """高中物理知识图谱可视化"""
    # 构建知识点节点
    videos = Video.query.all()
    topic_map = {}
    for v in videos:
        if v.topic_id not in topic_map:
            topic_map[v.topic_id] = {
                'id': v.topic_id,
                'name': v.topic,
                'accuracy': 0,
                'status': 'locked',
            }

    # 获取用户的答题情况
    from app.routes.diagnosis import diagnose_user
    diag = diagnose_user(current_user.id)
    diag_map = {d['topic_id']: d for d in diag}

    nodes = []
    for tid, info in topic_map.items():
        if tid in diag_map:
            d = diag_map[tid]
            info['accuracy'] = d['accuracy']
            if d['level'] == '已掌握':
                info['status'] = 'mastered'
            elif d['level'] == '待巩固':
                info['status'] = 'learning'
            else:
                info['status'] = 'weak'
        else:
            # 有视频但没做过题
            info['status'] = 'learning'

        nodes.append({
            'id': info['id'],
            'name': info['name'],
            'status': info['status'],
            'accuracy': info['accuracy'],
        })

    # 构建关联（基于 videos 表的 prerequisites 和 related）
    links = []
    for v in videos:
        if v.prerequisites:
            try:
                prereqs = json.loads(v.prerequisites)
                for p in prereqs:
                    if p in topic_map:
                        links.append({'source': p, 'target': v.topic_id})
            except (json.JSONDecodeError, TypeError):
                pass

    # 如果没有预设关联，用简单分类生成
    if not links:
        topic_ids = list(topic_map.keys())
        for i in range(len(topic_ids) - 1):
            links.append({'source': topic_ids[i], 'target': topic_ids[i + 1]})

    return render_template('student/knowledge_graph.html',
                           graph_nodes=nodes,
                           graph_links=links)

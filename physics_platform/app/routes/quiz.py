"""
测试系统路由模块
================

本模块处理所有与测试/答题相关的请求：
- 答题页面（/quiz/<topic_id>）- 显示指定知识点的题目
- 提交答案（/api/quiz/submit）- 接收答案并评分

路由蓝图：quiz_bp

答题流程：
    1. 用户点击"开始测试"→ 跳转到 /quiz/<topic_id>
    2. 后端从题库随机抽取 5 道题
    3. 前端逐题展示，用户点击选项
    4. 即时反馈对错（前端 JS 处理）
    5. 全部答完后提交到 /api/quiz/submit
    6. 后端保存答题记录并返回得分

组卷策略：
    - 每次随机抽取 5 道题（如果题目不足 5 道则全部显示）
    - 按知识点（topic_id）筛选题目
    - 保证每次测试的题目不同（随机性）

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

import random
import re
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Question, QuizRecord

# 创建蓝图实例
quiz_bp = Blueprint('quiz', __name__)


# ============================================================
# 答题页面路由
# ============================================================
@quiz_bp.route('/quiz/<topic_id>')
@login_required
def quiz_page(topic_id):
    """
    答题页面 - 获取指定知识点的测试题

    参数：
        topic_id: 知识点编号（如 "kinematics_01"）
        count:    题量（查询参数，可选，默认 5，范围 3-20）
        difficulty: 难度（查询参数，可选，1-3，0=全部）

    组卷逻辑：
        1. 查询该知识点的所有题目
        2. 按难度筛选（如果指定）
        3. 随机抽取指定数量的题目
    """
    from app.models import Video

    # 安全验证：topic_id 只允许字母、数字和下划线
    if not re.match(r'^[a-zA-Z0-9_]+$', topic_id):
        return render_template('quiz.html',
                               questions=[],
                               topic_id=topic_id,
                               topic_name='无效的知识点')

    # 获取查询参数
    count = request.args.get('count', 5, type=int)
    difficulty = request.args.get('difficulty', 0, type=int)
    count = max(3, min(20, count))  # 限制 3-20 题

    # 查询该知识点的所有题目
    query = Question.query.filter_by(topic_id=topic_id)
    if difficulty > 0:
        query = query.filter_by(difficulty=difficulty)
    questions = query.all()

    # 没有题目时显示空状态
    if not questions:
        return render_template('quiz.html',
                               questions=[],
                               topic_id=topic_id,
                               topic_name='未知知识点',
                               quiz_count=count,
                               quiz_difficulty=difficulty)

    # 随机抽取指定数量的题目
    selected = random.sample(questions, min(count, len(questions)))

    # 从视频表获取中文名称
    video = Video.query.filter_by(topic_id=topic_id).first()
    topic_name = video.topic if video else topic_id

    # 序列化为 JSON 可序列化的字典列表
    questions_data = [{
        'id': q.id,
        'question': q.content,
        'options': [q.option_a, q.option_b, q.option_c, q.option_d],
        'answer': 'ABCD'.index(q.answer),
        'explanation': q.explanation or '',
        'formula': ''
    } for q in selected]

    return render_template('quiz.html',
                           questions=questions_data,
                           topic_id=topic_id,
                           topic_name=topic_name,
                           quiz_count=count,
                           quiz_difficulty=difficulty)


# ============================================================
# 提交答案 API
# ============================================================
@quiz_bp.route('/api/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    """
    提交答案 - 接收用户答案并评分

    请求格式：
        POST /api/quiz/submit
        Content-Type: application/json
        Body: {
            "answers": [
                {"question_id": 1, "answer": "C"},
                {"question_id": 2, "answer": "A"},
                ...
            ]
        }

    处理流程：
        1. 遍历每道题的答案
        2. 与数据库中的正确答案比对
        3. 保存答题记录到 quiz_records 表
        4. 计算总分和正确率
        5. 返回详细结果（供前端展示）

    响应格式：
        {
            "score": 80,           // 总分（百分制）
            "correct_count": 4,    // 正确题数
            "total": 5,            // 总题数
            "results": [...]       // 每道题的详细结果
        }

    注意：
        - 每道题的答题记录都会保存到数据库
        - 这些记录用于诊断算法分析薄弱知识点
    """
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'error': '缺少答案数据'}), 400

    answers = data['answers']  # [{question_id, answer}, ...]
    results = []
    correct_count = 0
    total = len(answers)

    # 遍历每道题的答案
    for item in answers:
        qid = item.get('question_id')
        user_answer = item.get('answer', '').upper()  # 统一转大写

        # 从数据库获取题目
        question = Question.query.get(qid)
        if not question:
            continue

        # 判断是否正确
        is_correct = user_answer == question.answer
        if is_correct:
            correct_count += 1

        # 保存答题记录到数据库
        # 这些记录会被诊断算法用来分析薄弱知识点
        record = QuizRecord(
            user_id=current_user.id,
            question_id=qid,
            user_answer=user_answer,
            is_correct=is_correct
        )
        db.session.add(record)

        # 收集每道题的结果（供前端展示解析）
        results.append({
            'question_id': qid,
            'content': question.content,
            'correct_answer': question.answer,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'explanation': question.explanation
        })

    # 批量提交到数据库
    db.session.commit()

    # 计算得分（百分制）
    score = round(correct_count / total * 100) if total > 0 else 0

    return jsonify({
        'score': score,
        'correct_count': correct_count,
        'total': total,
        'results': results
    })

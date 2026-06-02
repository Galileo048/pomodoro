"""
学生端路由模块
=============

本模块处理学生端扩展功能：
- 学生控制台首页（/student/dashboard）
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
    User, Video, Question, QuizRecord, WatchRecord, Favorite
)

# 创建蓝图实例
student_bp = Blueprint('student', __name__, url_prefix='/student')


# ============================================================
# 学生控制台首页
# ============================================================
@student_bp.route('/dashboard')
@login_required
def dashboard():
    """
    学生控制台首页

    显示：
    1. 学习概览卡片（学习时长、正确率、视频进度）
    2. 薄弱知识点提示
    """
    # ---- 学习统计 ----
    watched_videos = WatchRecord.query.filter_by(
        user_id=current_user.id, is_completed=True
    ).count()
    total_videos = Video.query.count()

    records = QuizRecord.query.filter_by(user_id=current_user.id).all()
    total_questions = len(records)
    total_correct = sum(1 for r in records if r.is_correct)
    avg_accuracy = round(total_correct / total_questions * 100) if total_questions > 0 else 0

    total_study_hours = round(watched_videos * 10 / 60, 1)

    # ---- 薄弱知识点 ----
    from app.routes.diagnosis import diagnose_user
    diag_results = diagnose_user(current_user.id)
    weak_topics = [
        {'name': r['topic_name'], 'accuracy': r['accuracy'], 'id': r['topic_id']}
        for r in diag_results if r['level'] in ('薄弱', '待巩固')
    ][:5]

    # ---- 最近学习（最近 5 条观看记录）----
    recent_records = WatchRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(WatchRecord.watched_at.desc()).limit(5).all()

    recent_videos = []
    seen_ids = set()
    for wr in recent_records:
        if wr.video_id not in seen_ids:
            seen_ids.add(wr.video_id)
            recent_videos.append({
                'id': wr.video.id,
                'title': wr.video.title,
                'progress': wr.watch_progress,
                'chapter': wr.video.chapter or '未分类',
            })

    # ---- 我的收藏（最近 5 个）----
    fav_records = Favorite.query.filter_by(
        user_id=current_user.id
    ).order_by(Favorite.created_at.desc()).limit(5).all()

    favorites = []
    for fav in fav_records:
        if fav.item_type == 'video':
            video = Video.query.get(int(fav.item_id))
            if video:
                favorites.append({
                    'type': 'video',
                    'title': video.title,
                    'url': url_for('videos.video_play', video_id=video.id),
                })
        elif fav.item_type == 'experiment':
            from app.routes.experiments import EXPERIMENTS
            for exp in EXPERIMENTS:
                if exp['id'] == fav.item_id:
                    favorites.append({
                        'type': 'experiment',
                        'title': exp['title'],
                        'url': url_for('experiments.run', experiment_id=exp['id']),
                    })
                    break

    return render_template('student/dashboard.html',
                           total_study_hours=total_study_hours,
                           avg_accuracy=avg_accuracy,
                           watched_videos=watched_videos,
                           total_videos=total_videos,
                           weak_topics=weak_topics,
                           recent_videos=recent_videos,
                           favorites=favorites)


# ============================================================
# 学习报告
# ============================================================
@student_bp.route('/report')
@login_required
def report():
    """学习报告 - 数据可视化"""
    records = QuizRecord.query.filter_by(user_id=current_user.id).all()

    total = len(records)
    correct = sum(1 for r in records if r.is_correct)
    overall_accuracy = round(correct / total * 100) if total > 0 else 0

    study_dates = []
    study_hours = []
    for i in range(6, -1, -1):
        day = datetime.now(timezone.utc) - timedelta(days=i)
        day_str = day.strftime('%m/%d')
        day_records = [r for r in records if r.answered_at and
                       r.answered_at.date() == day.date()]
        study_dates.append(day_str)
        study_hours.append(round(len(day_records) * 2 / 60, 1))

    from app.routes.diagnosis import diagnose_user
    diag = diagnose_user(current_user.id)
    mastered_count = sum(1 for d in diag if d['level'] == '已掌握')
    learning_count = sum(1 for d in diag if d['level'] == '待巩固')
    weak_count = sum(1 for d in diag if d['level'] == '薄弱')

    question_types = [d['topic_name'][:6] for d in diag[:8]]
    type_accuracies = [d['accuracy'] for d in diag[:8]]

    ability_scores = [
        min(100, overall_accuracy + 10),
        min(100, overall_accuracy - 5),
        min(100, overall_accuracy + 5),
        min(100, overall_accuracy - 10),
        min(100, overall_accuracy),
    ]

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
                           weekly_trend=15,
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
@login_required
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
@login_required
def knowledge_graph():
    """高中物理知识图谱可视化"""
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
            info['status'] = 'learning'

        nodes.append({
            'id': info['id'],
            'name': info['name'],
            'status': info['status'],
            'accuracy': info['accuracy'],
        })

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

    if not links:
        topic_ids = list(topic_map.keys())
        for i in range(len(topic_ids) - 1):
            links.append({'source': topic_ids[i], 'target': topic_ids[i + 1]})

    return render_template('student/knowledge_graph.html',
                           graph_nodes=nodes,
                           graph_links=links)

"""
学习诊断路由模块
================

本模块处理学习诊断相关的请求：
- 诊断报告页（/diagnosis）- 显示薄弱知识点分析
- 诊断 API（/api/diagnosis）- 返回 JSON 格式的诊断数据

路由蓝图：diagnosis_bp

诊断算法说明：
    1. 获取用户最近 30 天的答题记录
    2. 按知识点（topic_id）统计正确率
    3. 根据正确率分级判定：
       - 正确率 < 60% → "薄弱"（红色，推荐重看视频）
       - 60% ≤ 正确率 < 80% → "待巩固"（黄色）
       - 正确率 ≥ 80% → "已掌握"（绿色）
    4. 按正确率升序排列（最薄弱的排在前面）

设计决策：
    - MVP 阶段使用纯规则判断，不调用 AI API
    - 简单、快速、可解释
    - 二期可接入 DeepSeek API 生成自然语言解释

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

import os
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, jsonify, abort, request
from flask_login import login_required, current_user
import requests
from app import db
from app.models import QuizRecord, Video, Question

# 创建蓝图实例
diagnosis_bp = Blueprint('diagnosis', __name__)


def diagnose_user(user_id):
    """
    诊断用户薄弱知识点（纯规则判断，不调用 AI）

    参数：
        user_id: 用户 ID

    返回：
        list: 诊断结果列表，按正确率升序排列
        每个元素包含：
            - topic_id:         知识点编号
            - topic_name:       知识点名称
            - accuracy:         正确率（0-100 的整数）
            - level:            掌握程度（"薄弱"/"待巩固"/"已掌握"）
            - total:            该知识点的总答题数
            - correct:          该知识点的正确答题数
            - recommended_video_id:    推荐视频 ID（如有）
            - recommended_video_title: 推荐视频标题（如有）

    算法时间复杂度：O(n)，n = 答题记录数
    """
    # 获取最近 30 天的答题记录
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    records = QuizRecord.query.filter(
        QuizRecord.user_id == user_id,
        QuizRecord.answered_at >= cutoff
    ).all()

    # 没有答题记录时返回空列表
    if not records:
        return []

    # 按知识点统计正确率，并收集错题
    # topic_stats 结构：{topic_id: {correct: N, total: N, topic_name: str, wrong_questions: [...]}}
    topic_stats = {}
    for record in records:
        # 跳过无效记录（题目已被删除的情况）
        if record.question is None:
            continue

        topic = record.question.topic_id

        if topic not in topic_stats:
            # 从视频表获取中文名称
            v = Video.query.filter_by(topic_id=topic).first()
            topic_stats[topic] = {
                'correct': 0,
                'total': 0,
                'topic_name': v.topic if v else topic,
                'wrong_questions': []
            }

        topic_stats[topic]['total'] += 1
        if record.is_correct:
            topic_stats[topic]['correct'] += 1
        else:
            # 收集错题详情
            topic_stats[topic]['wrong_questions'].append({
                'question_id': record.question_id,
                'content': record.question.content,
                'your_answer': record.user_answer,
                'correct_answer': record.question.answer,
                'explanation': record.question.explanation or ''
            })

    # 计算正确率，分级判定
    results = []
    for topic, stats in topic_stats.items():
        accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0

        # 分级判定（阈值参考教育测量学标准）
        if accuracy < 0.6:
            level = '薄弱'      # 需要重新学习
        elif accuracy < 0.8:
            level = '待巩固'    # 需要额外练习
        else:
            level = '已掌握'    # 可以进入下一阶段

        # 查找推荐视频（该知识点对应的视频）
        recommended_video = Video.query.filter_by(topic_id=topic).first()

        results.append({
            'topic_id': topic,
            'topic_name': stats['topic_name'],
            'accuracy': round(accuracy * 100),  # 转为百分比整数
            'level': level,
            'total': stats['total'],
            'correct': stats['correct'],
            'wrong_questions': stats['wrong_questions'],
            'recommended_video_id': recommended_video.id if recommended_video else None,
            'recommended_video_title': recommended_video.title if recommended_video else None
        })

    # 按正确率升序排列（最薄弱的排在前面，方便优先处理）
    results.sort(key=lambda x: x['accuracy'])
    return results


# ============================================================
# 诊断报告页面
# ============================================================
@diagnosis_bp.route('/diagnosis')
@login_required
def diagnosis_page():
    """
    诊断报告页 - 显示用户的学习薄弱点分析

    页面展示：
        1. 顶部总览：总题数、正确数、正确率
        2. 统计卡片：薄弱/待巩固/已掌握 的知识点数量
        3. 知识点详情：每个知识点的正确率、状态、推荐视频
        4. 薄弱点高亮：红色标记需要重点关注的知识点
    """
    results = diagnose_user(current_user.id)

    # 计算总览数据
    total_questions = sum(r['total'] for r in results)
    total_correct = sum(r['correct'] for r in results)
    overall_accuracy = round(total_correct / total_questions * 100) if total_questions > 0 else 0

    # 统计各等级的知识点数量
    weak_count = sum(1 for r in results if r['level'] == '薄弱')
    consolidate_count = sum(1 for r in results if r['level'] == '待巩固')
    mastered_count = sum(1 for r in results if r['level'] == '已掌握')

    return render_template('diagnosis.html',
                           results=results,
                           total_questions=total_questions,
                           total_correct=total_correct,
                           overall_accuracy=overall_accuracy,
                           weak_count=weak_count,
                           consolidate_count=consolidate_count,
                           mastered_count=mastered_count)


# ============================================================
# 诊断数据 API
# ============================================================
@diagnosis_bp.route('/api/diagnosis')
@login_required
def api_diagnosis():
    """
    获取诊断数据（JSON API）

    返回格式：
        {
            "results": [
                {
                    "topic_id": "kinematics_01",
                    "topic_name": "kinematics_01",
                    "accuracy": 40,
                    "level": "薄弱",
                    "total": 5,
                    "correct": 2,
                    "recommended_video_id": 1,
                    "recommended_video_title": "匀变速直线运动"
                },
                ...
            ]
        }

    用途：
        - 前端异步加载诊断数据
        - 未来可被 AI 诊断模块调用
    """
    results = diagnose_user(current_user.id)
    return jsonify({'results': results})


# ============================================================
# 错题详情页面
# ============================================================
@diagnosis_bp.route('/diagnosis/wrong/<topic_id>')
@login_required
def wrong_questions(topic_id):
    """
    错题详情页 - 显示指定知识点的所有错题记录

    同一道题如果答错多次，会重复显示（每次答题都是一条记录）
    按答题时间倒序排列（最新的在前面）
    """
    # 获取该知识点的所有错题记录
    records = QuizRecord.query.filter(
        QuizRecord.user_id == current_user.id,
        QuizRecord.is_correct == False
    ).join(Question).filter(
        Question.topic_id == topic_id
    ).order_by(QuizRecord.answered_at.desc()).all()

    if not records:
        abort(404)

    # 从视频表获取知识点的中文名称
    video = Video.query.filter_by(topic_id=topic_id).first()
    topic_name = video.topic if video else topic_id

    # 获取推荐视频
    recommended_video = Video.query.filter_by(topic_id=topic_id).first()

    return render_template('wrong_questions.html',
                           records=records,
                           topic_id=topic_id,
                           topic_name=topic_name,
                           recommended_video=recommended_video)


# ============================================================
# 删除错题记录
# ============================================================
@diagnosis_bp.route('/api/wrong/delete/<int:record_id>', methods=['POST'])
@login_required
def delete_wrong_record(record_id):
    """删除一条答题记录（错题）"""
    record = QuizRecord.query.get_or_404(record_id)
    # 安全检查：只能删除自己的记录
    if record.user_id != current_user.id:
        return jsonify({'error': '无权操作'}), 403
    topic_id = record.question.topic_id if record.question else None
    db.session.delete(record)
    db.session.commit()
    return jsonify({'success': True, 'topic_id': topic_id})


# ============================================================
# 批量删除某知识点的错题
# ============================================================
@diagnosis_bp.route('/api/wrong/delete-all/<topic_id>', methods=['POST'])
@login_required
def delete_all_wrong_records(topic_id):
    """删除某知识点的所有错题记录"""
    records = QuizRecord.query.filter(
        QuizRecord.user_id == current_user.id,
        QuizRecord.is_correct == False
    ).join(Question).filter(Question.topic_id == topic_id).all()

    count = len(records)
    for r in records:
        db.session.delete(r)
    db.session.commit()
    return jsonify({'success': True, 'deleted': count, 'topic_id': topic_id})


# ============================================================
# AI 诊断 API（调用 DeepSeek）
# ============================================================
# DeepSeek API 配置（从环境变量读取）
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'


@diagnosis_bp.route('/api/ai-diagnosis', methods=['POST'])
@login_required
def ai_diagnosis():
    """
    AI 诊断 - 调用 DeepSeek API 分析薄弱知识点

    请求格式：
        POST /api/ai-diagnosis
        Content-Type: application/json
        Body: {"topic_id": "kinematics_01"}  (可选，不传则分析所有薄弱点)

    响应格式：
        {
            "analysis": "AI 生成的诊断分析...",
            "recommendations": ["建议1", "建议2", ...]
        }
    """
    data = request.get_json() or {}
    topic_id = data.get('topic_id')

    # 检查 API 密钥是否配置
    if not DEEPSEEK_API_KEY:
        return jsonify({
            'analysis': '⚠️ AI 诊断服务暂未配置。\n\n请联系管理员配置 DeepSeek API 密钥后即可使用此功能。\n\n当前你可以通过「查看错题」功能手动分析薄弱知识点。',
            'recommendations': []
        })

    # 获取用户的薄弱知识点
    results = diagnose_user(current_user.id)

    # 如果指定了 topic_id，只分析该知识点
    if topic_id:
        results = [r for r in results if r['topic_id'] == topic_id]

    # 只分析薄弱和待巩固的知识点
    weak_results = [r for r in results if r['level'] in ('薄弱', '待巩固')]

    if not weak_results:
        return jsonify({
            'analysis': '恭喜！你目前没有明显的薄弱知识点。继续保持！',
            'recommendations': []
        })

    # 构建发给 DeepSeek 的提示词
    wrong_details = []
    for r in weak_results:
        wrong_info = f"【{r['topic_name']}】正确率 {r['accuracy']}%，共 {r['total']} 题答对 {r['correct']} 题"
        if r.get('wrong_questions'):
            wrong_qs = r['wrong_questions'][:3]  # 最多取 3 道错题
            for wq in wrong_qs:
                wrong_info += f"\n  - 题目: {wq['content']}"
                wrong_info += f"\n    学生答: {wq['your_answer']}，正确答案: {wq['correct_answer']}"
                if wq.get('explanation'):
                    wrong_info += f"\n    解析: {wq['explanation']}"
        wrong_details.append(wrong_info)

    prompt = f"""你是一位高中物理教学专家。请分析以下学生的物理学习薄弱点，并给出个性化的学习建议。

学生答题情况：
{chr(10).join(wrong_details)}

请用中文回答，包含以下内容：
1. 学情分析：简要总结学生的薄弱环节（2-3句话）
2. 错因分析：分析学生可能的错误原因
3. 学习建议：给出3-5条具体的改进建议（每条一句话）
4. 重点提醒：指出最需要优先补强的1-2个知识点

回答要简洁实用，适合高中生阅读。"""

    try:
        # 调用 DeepSeek API
        response = requests.post(
            DEEPSEEK_API_URL,
            headers={
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': '你是一位专业的高中物理教师，擅长分析学生的学习薄弱点并给出针对性建议。'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 1000
            },
            timeout=30
        )

        if response.status_code != 200:
            return jsonify({'error': f'AI 服务暂时不可用 (HTTP {response.status_code})'}), 502

        result = response.json()
        ai_text = result['choices'][0]['message']['content']

        # 从 AI 回复中提取建议列表
        recommendations = []
        for line in ai_text.split('\n'):
            line = line.strip()
            if line.startswith(('3.', '4.', '建议', '重点', '-', '·', '•')):
                # 去掉编号前缀
                clean = line.lstrip('0123456789.、-·• ')
                if clean and len(clean) > 5:
                    recommendations.append(clean)

        return jsonify({
            'analysis': ai_text,
            'recommendations': recommendations[:5]  # 最多5条建议
        })

    except requests.exceptions.Timeout:
        return jsonify({'error': 'AI 服务响应超时，请稍后重试'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'AI 服务连接失败: {str(e)}'}), 502
    except (KeyError, IndexError) as e:
        return jsonify({'error': 'AI 服务返回格式异常'}), 500

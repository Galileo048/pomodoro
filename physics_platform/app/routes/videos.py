"""
视频系统路由模块
================

本模块处理所有与视频相关的请求：
- 视频列表页（/videos）- 按章节分类展示
- 视频播放页（/video/<id>）- 播放单个视频
- 观看进度上报（/api/progress）- 前端定时上报进度

路由蓝图：videos_bp
需要登录：所有路由都需要 @login_required

进度上报机制：
    前端 JavaScript 每 10 秒调用 /api/progress 接口，
    上报当前观看进度（0-100 的整数百分比）。
    进度只能前进不能后退，防止用户拖动进度条后进度回退。

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

import json
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Video, WatchRecord

# 创建蓝图实例
videos_bp = Blueprint('videos', __name__)


# ============================================================
# 视频列表页
# ============================================================
@videos_bp.route('/videos')
@login_required
def video_list():
    """
    视频列表页 - 按章节分类展示所有视频

    支持按章节筛选：/videos?chapter=运动学

    返回数据：
        videos:          视频列表（按 ID 排序）
        chapters:        所有章节名称（用于筛选标签）
        current_chapter: 当前选中的章节（用于高亮）
    """
    # 获取章节筛选参数
    chapter = request.args.get('chapter', '')

    # 构建查询
    query = Video.query
    if chapter:
        query = query.filter_by(chapter=chapter)

    # 按 ID 排序（即按导入顺序）
    videos = query.order_by(Video.id).all()

    # 获取所有不重复的章节名称（用于页面上的筛选标签）
    chapters = db.session.query(Video.chapter) \
        .distinct() \
        .filter(Video.chapter.isnot(None)) \
        .all()
    chapters = [c[0] for c in chapters]

    return render_template('video_list.html',
                           videos=videos,
                           chapters=chapters,
                           current_chapter=chapter)


# ============================================================
# 视频播放页
# ============================================================
@videos_bp.route('/video/<int:video_id>')
@login_required
def video_play(video_id):
    """
    视频播放页 - 播放单个视频

    参数：
        video_id: 视频 ID（URL 路径参数）

    功能：
        1. 显示视频播放器（Video.js）
        2. 显示视频信息（标题、描述、难度等）
        3. 显示观看进度
        4. 显示关联视频推荐
        5. 提供"开始测试"按钮

    关联视频逻辑：
        从视频的 related 字段（JSON 数组）读取关联知识点 ID，
        然后查询对应视频。例如 related='["kinematics_02"]'
        会显示"平抛运动"视频作为推荐。
    """
    # 获取视频，不存在则返回 404
    video = Video.query.get_or_404(video_id)

    # 获取当前用户的观看进度
    record = WatchRecord.query.filter_by(
        user_id=current_user.id,
        video_id=video_id
    ).first()
    progress = record.watch_progress if record else 0

    # 解析关联视频（JSON 数组 → 视频对象列表）
    related_ids = []
    if video.related:
        try:
            related_ids = json.loads(video.related)
        except (json.JSONDecodeError, TypeError):
            # JSON 解析失败时忽略关联视频
            pass

    related_videos = []
    for rid in related_ids:
        v = Video.query.filter_by(topic_id=rid).first()
        if v:
            related_videos.append(v)

    return render_template('video_play.html',
                           video=video,
                           progress=progress,
                           related_videos=related_videos)


# ============================================================
# 观看进度上报 API
# ============================================================
@videos_bp.route('/api/progress', methods=['POST'])
@login_required
def update_progress():
    """
    上报观看进度（JSON API）

    请求格式：
        POST /api/progress
        Content-Type: application/json
        Body: {"video_id": 1, "progress": 45}

    响应格式：
        成功: {"success": true, "progress": 45}
        失败: {"error": "错误信息"}

    进度更新规则：
        - 进度范围限制在 0-100
        - 只更新更大的进度值（防止回退）
        - 进度 >= 95% 时标记为"已看完"

    注意事项：
        - 前端每 10 秒调用一次
        - 页面关闭时通过 sendBeacon 发送最终进度
        - 视频暂停时不发送请求
    """
    # 解析请求体（支持 JSON 和 FormData 两种格式）
    # fetch 使用 JSON，sendBeacon 使用 FormData
    if request.content_type and 'application/json' in request.content_type:
        data = request.get_json()
    else:
        data = request.form.to_dict() if request.form else None

    if not data:
        return jsonify({'error': '无效请求'}), 400

    video_id = data.get('video_id')
    progress = data.get('progress', 0)

    # 参数验证
    if not video_id:
        return jsonify({'error': '缺少 video_id'}), 400

    # 限制进度范围（0-100 的整数）
    progress = max(0, min(100, int(progress)))

    # 查找或创建观看记录
    record = WatchRecord.query.filter_by(
        user_id=current_user.id,
        video_id=video_id
    ).first()

    if record:
        # 关键：只更新更大的进度值
        # 如果用户拖动进度条回到前面，进度不应该回退
        if progress > record.watch_progress:
            record.watch_progress = progress
            # 进度 >= 95% 视为看完
            if progress >= 95:
                record.is_completed = True
    else:
        # 首次观看，创建新记录
        record = WatchRecord(
            user_id=current_user.id,
            video_id=video_id,
            watch_progress=progress,
            is_completed=progress >= 95
        )
        db.session.add(record)

    db.session.commit()
    return jsonify({'success': True, 'progress': progress})

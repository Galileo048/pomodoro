"""
搜索蓝图
========
提供全局搜索功能，支持搜索视频和实验。

路由：
    GET /search?q=关键词         搜索结果页
    GET /api/search/suggestions  搜索建议（AJAX）
"""

from flask import Blueprint, request, render_template, jsonify
from app.models import Video
from app.routes.experiments import EXPERIMENTS

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search_page():
    """搜索结果页面"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', 'all')

    results = {
        'videos': [],
        'experiments': [],
    }

    if query:
        # 搜索视频：标题或描述包含关键词
        if category in ('all', 'videos'):
            results['videos'] = Video.query.filter(
                Video.title.contains(query) |
                Video.description.contains(query) |
                Video.topic.contains(query)
            ).limit(20).all()

        # 搜索实验：标题或描述包含关键词
        if category in ('all', 'experiments'):
            results['experiments'] = [
                exp for exp in EXPERIMENTS
                if query in exp['title'] or query in exp.get('description', '')
            ]

    return render_template('search/results.html',
                           query=query,
                           results=results,
                           category=category)


@search_bp.route('/api/search/suggestions')
def search_suggestions():
    """搜索建议 API（输入时自动补全）"""
    query = request.args.get('q', '').strip()
    if len(query) < 1:
        return jsonify([])

    suggestions = []

    # 视频建议
    videos = Video.query.filter(
        Video.title.contains(query)
    ).limit(5).all()
    for v in videos:
        suggestions.append({
            'type': 'video',
            'title': v.title,
            'id': v.id,
            'url': f'/videos/{v.id}'
        })

    # 实验建议
    for exp in EXPERIMENTS:
        if query in exp['title']:
            suggestions.append({
                'type': 'experiment',
                'title': exp['title'],
                'id': exp['id'],
                'url': f'/experiment/{exp["id"]}'
            })
            if len(suggestions) >= 8:
                break

    return jsonify(suggestions)

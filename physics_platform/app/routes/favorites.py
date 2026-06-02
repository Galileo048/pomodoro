"""
收藏功能蓝图
============
提供视频和实验的收藏/取消收藏功能。

路由：
    POST /api/favorites/toggle    切换收藏状态
    GET  /api/favorites/check     检查是否已收藏
    GET  /api/favorites/list      获取用户收藏列表
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Favorite

favorites_bp = Blueprint('favorites', __name__)


@favorites_bp.route('/api/favorites/toggle', methods=['POST'])
@login_required
def toggle_favorite():
    """切换收藏状态（已收藏则取消，未收藏则添加）"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '无效请求'}), 400

    item_type = data.get('item_type')  # 'video' 或 'experiment'
    item_id = str(data.get('item_id', ''))

    if item_type not in ('video', 'experiment') or not item_id:
        return jsonify({'error': '参数错误'}), 400

    # 查找现有收藏
    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first()

    if existing:
        # 已收藏 → 取消
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status': 'removed', 'is_favorite': False})
    else:
        # 未收藏 → 添加
        favorite = Favorite(
            user_id=current_user.id,
            item_type=item_type,
            item_id=item_id
        )
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added', 'is_favorite': True})


@favorites_bp.route('/api/favorites/check')
@login_required
def check_favorite():
    """检查指定项目是否已收藏"""
    item_type = request.args.get('item_type')
    item_id = request.args.get('item_id')

    is_favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        item_type=item_type,
        item_id=item_id
    ).first() is not None

    return jsonify({'is_favorite': is_favorite})


@favorites_bp.route('/api/favorites/list')
@login_required
def list_favorites():
    """获取当前用户的所有收藏"""
    item_type = request.args.get('item_type')  # 可选筛选

    query = Favorite.query.filter_by(user_id=current_user.id)
    if item_type:
        query = query.filter_by(item_type=item_type)

    favorites = query.order_by(Favorite.created_at.desc()).all()

    return jsonify([{
        'id': f.id,
        'item_type': f.item_type,
        'item_id': f.item_id,
        'created_at': f.created_at.isoformat() if f.created_at else None
    } for f in favorites])

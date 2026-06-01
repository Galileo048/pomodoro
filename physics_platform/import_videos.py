"""
视频元数据导入脚本
==================

功能：
    从 videos.json 文件读取视频信息，写入 SQLite 数据库。

用法：
    cd physics_platform
    python import_videos.py

视频文件放置：
    将 MP4 文件手动复制到 app/static/videos/ 目录
    本脚本只导入元数据（标题、描述、路径等），不复制视频文件

去重规则：
    按 topic_id 去重——如果 topic_id 已存在则跳过

videos.json 格式：
    [
        {
            "title": "视频标题",
            "description": "视频描述",
            "topic": "知识点名称",
            "topic_id": "kinematics_01",
            "chapter": "运动学",
            "video_path": "videos/01_xxx.mp4",
            "duration": 300,
            "difficulty": 2,
            "prerequisites": [],
            "related": ["kinematics_02"]
        },
        ...
    ]

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

import json
import os
import sys

# 将项目根目录添加到 Python 路径
# 这样才能正确导入 app 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Video


def import_videos():
    """导入视频元数据到数据库"""

    # 构建 videos.json 的完整路径（与本脚本同目录）
    json_path = os.path.join(os.path.dirname(__file__), 'videos.json')

    # 检查文件是否存在
    if not os.path.exists(json_path):
        print(f"错误: 找不到 {json_path}")
        print("请先创建 videos.json 文件")
        return

    # 读取 JSON 数据
    with open(json_path, 'r', encoding='utf-8') as f:
        videos = json.load(f)

    # 创建 Flask 应用（需要应用上下文才能操作数据库）
    app = create_app()
    with app.app_context():
        imported = 0
        skipped = 0

        for v in videos:
            # 检查是否已存在（按 topic_id 去重）
            existing = Video.query.filter_by(topic_id=v['topic_id']).first()
            if existing:
                print(f"  跳过: {v['title']} (topic_id={v['topic_id']} 已存在)")
                skipped += 1
                continue

            # 创建 Video 对象
            # prerequisites 和 related 存储为 JSON 字符串
            video = Video(
                title=v['title'],
                description=v.get('description', ''),
                topic=v['topic'],
                topic_id=v['topic_id'],
                chapter=v.get('chapter', ''),
                video_path=v['video_path'],
                cover_path=v.get('cover_path', ''),
                duration=v.get('duration', 0),
                difficulty=v.get('difficulty', 2),
                prerequisites=json.dumps(v.get('prerequisites', []), ensure_ascii=False),
                related=json.dumps(v.get('related', []), ensure_ascii=False)
            )
            db.session.add(video)
            imported += 1
            print(f"  导入: {v['title']}")

        # 提交到数据库
        db.session.commit()
        print(f"\n完成! 导入 {imported} 个视频, 跳过 {skipped} 个")


if __name__ == '__main__':
    import_videos()

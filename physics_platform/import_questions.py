"""
题库导入脚本
============

功能：
    从 questions.json 文件读取题目，写入 SQLite 数据库。

用法：
    cd physics_platform
    python import_questions.py

去重规则：
    按 (topic_id, content) 联合去重
    如果两个字段都匹配则跳过（同一知识点下不允许重复题目）

questions.json 格式：
    [
        {
            "topic_id": "kinematics_01",
            "content": "题目内容",
            "option_a": "选项 A",
            "option_b": "选项 B",
            "option_c": "选项 C",
            "option_d": "选项 D",
            "answer": "C",
            "explanation": "答案解析",
            "difficulty": 1
        },
        ...
    ]

author_id 说明：
    - answer 字段必须是 A/B/C/D 之一（不区分大小写，脚本会自动转大写）
    - difficulty 范围 1-5（1=简单，5=困难）

作者：高中物理 AI 自适应学习平台团队
日期：2026-06-01
"""

import json
import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Question


def import_questions():
    """导入题库到数据库"""

    # 构建 questions.json 的完整路径
    json_path = os.path.join(os.path.dirname(__file__), 'questions.json')

    # 检查文件是否存在
    if not os.path.exists(json_path):
        print(f"错误: 找不到 {json_path}")
        print("请先创建 questions.json 文件")
        return

    # 读取 JSON 数据
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # 创建 Flask 应用
    app = create_app()
    with app.app_context():
        imported = 0
        skipped = 0

        for q in questions:
            # 按 (topic_id, content) 联合去重
            # 同一知识点下不允许有两道完全相同的题目
            existing = Question.query.filter_by(
                topic_id=q['topic_id'],
                content=q['content']
            ).first()
            if existing:
                skipped += 1
                continue

            # 创建 Question 对象
            # answer 自动转大写，确保一致性
            question = Question(
                topic_id=q['topic_id'],
                content=q['content'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                answer=q['answer'].upper(),
                explanation=q.get('explanation', ''),
                difficulty=q.get('difficulty', 2)
            )
            db.session.add(question)
            imported += 1

        # 提交到数据库
        db.session.commit()
        print(f"完成! 导入 {imported} 道题, 跳过 {skipped} 道")


if __name__ == '__main__':
    import_questions()

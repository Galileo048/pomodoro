# 高中物理 AI 自适应学习平台

## 项目简介

基于 Flask + SQLite 的高中物理自适应学习平台，包含：
- 用户注册/登录系统
- Manim 动画视频播放
- 在线测试（选择题）
- 学习诊断（薄弱知识点分析）

## 技术栈

- Python 3.10+ / Flask 3.1 / Flask-Login / Flask-SQLAlchemy
- SQLite 数据库
- Bootstrap 5 + Video.js + ECharts（前端）
- HTML/CSS/JavaScript

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 导入视频元数据
python import_videos.py

# 3. 导入题库
python import_questions.py

# 4. 启动开发服务器
python run.py

# 5. 访问 http://localhost:5000
```

## 目录结构

```
├── app/
│   ├── __init__.py          # Flask 应用工厂
│   ├── models.py            # 数据库模型（ORM）
│   ├── routes/
│   │   ├── auth.py          # 用户认证（登录/注册/登出）
│   │   ├── videos.py        # 视频系统（列表/播放/进度）
│   │   ├── quiz.py          # 测试系统（答题/评分）
│   │   └── diagnosis.py     # 学习诊断（薄弱点分析）
│   ├── templates/           # HTML 模板（Jinja2）
│   └── static/              # 静态资源（CSS/JS/视频）
├── schema.sql               # 数据库建表 SQL（参考文档）
├── import_videos.py         # 视频元数据导入脚本
├── import_questions.py      # 题库导入脚本
├── videos.json              # 视频数据文件
├── questions.json           # 题库数据文件
├── requirements.txt         # Python 依赖
└── run.py                   # 启动入口
```

## 数据库表结构

| 表名 | 用途 | 关键字段 |
|------|------|----------|
| users | 用户信息 | username, password_hash, grade |
| videos | 视频元数据 | title, topic_id, video_path, chapter |
| questions | 测试题库 | topic_id, content, options, answer |
| quiz_records | 答题记录 | user_id, question_id, is_correct |
| watch_records | 观看记录 | user_id, video_id, watch_progress |

## 诊断算法

- 正确率 < 60% → "薄弱"（推荐重看视频）
- 60% ≤ 正确率 < 80% → "待巩固"
- 正确率 ≥ 80% → "已掌握"

## 备份信息

- 备份日期：2026-06-01
- 所有源码包含详细中文注释
- 设计文档：`~/.gstack/projects/Galileo048-pomodoro/门捷列夫-master-design-20260601-123704.md`

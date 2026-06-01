-- ============================================================
-- 高中物理 AI 自适应学习平台 - 数据库建表 SQL
-- ============================================================
--
-- 本文件定义了平台所有数据表的结构。
-- 实际使用中，表结构由 Flask-SQLAlchemy 的 models.py 自动创建，
-- 本文件仅作为参考和文档。
--
-- 数据表关系图：
--
--   ┌─────────┐       ┌─────────────┐       ┌─────────┐
--   │  users  │───────│quiz_records │───────│questions│
--   │ 用户表  │  1:N  │  答题记录表  │  N:1  │  题目表  │
--   └────┬────┘       └─────────────┘       └─────────┘
--        │
--        │ 1:N          ┌─────────────┐       ┌─────────┐
--        └──────────────│watch_records│───────│ videos  │
--                       │  观看记录表  │  N:1  │  视频表  │
--                       └─────────────┘       └─────────┘
--
-- 作者：高中物理 AI 自适应学习平台团队
-- 日期：2026-06-01
-- ============================================================


-- ------------------------------------------------------------
-- 用户表 (users)
-- ------------------------------------------------------------
-- 存储用户注册信息和登录凭证
-- 密码以哈希形式存储（password_hash），不保存明文
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 用户 ID，自增主键
    username VARCHAR(50) UNIQUE NOT NULL,     -- 用户名，唯一且不能为空
    password_hash VARCHAR(256) NOT NULL,      -- 密码哈希值（Werkzeug 生成）
    email VARCHAR(100),                       -- 邮箱（可选）
    grade VARCHAR(10) DEFAULT '高一',          -- 年级，默认高一
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 注册时间
    last_login TIMESTAMP                      -- 最后登录时间
);


-- ------------------------------------------------------------
-- 视频表 (videos)
-- ------------------------------------------------------------
-- 存储 Manim 动画视频的元数据
-- 视频文件存放在 app/static/videos/ 目录，数据库只存路径
CREATE TABLE IF NOT EXISTS videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 视频 ID，自增主键
    title VARCHAR(200) NOT NULL,              -- 视频标题（如"匀变速直线运动"）
    description TEXT,                         -- 视频描述（详细介绍）
    topic VARCHAR(100) NOT NULL,              -- 知识点名称
    topic_id VARCHAR(50) NOT NULL,            -- 知识点编号（如"kinematics_01"，用于关联题目）
    subject VARCHAR(20) DEFAULT '物理',        -- 学科（默认物理）
    chapter VARCHAR(50),                      -- 章节（如"运动学"，用于分类筛选）
    video_path VARCHAR(300) NOT NULL,         -- 视频文件相对路径
    cover_path VARCHAR(300),                  -- 封面图路径（可选）
    duration INTEGER,                         -- 视频时长（秒）
    difficulty INTEGER DEFAULT 2              -- 难度等级（1-5）
        CHECK(difficulty BETWEEN 1 AND 5),
    prerequisites TEXT,                       -- 前置知识点（JSON 数组字符串）
    related TEXT,                             -- 关联知识点（JSON 数组字符串）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间
);


-- ------------------------------------------------------------
-- 测试题表 (questions)
-- ------------------------------------------------------------
-- 存储选择题题库
-- 每道题关联一个知识点（topic_id），支持按知识点组卷
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 题目 ID，自增主键
    topic_id VARCHAR(50) NOT NULL,            -- 关联知识点编号
    content TEXT NOT NULL,                    -- 题目内容
    option_a TEXT NOT NULL,                   -- 选项 A
    option_b TEXT NOT NULL,                   -- 选项 B
    option_c TEXT NOT NULL,                   -- 选项 C
    option_d TEXT NOT NULL,                   -- 选项 D
    answer CHAR(1) NOT NULL                   -- 正确答案（A/B/C/D 之一）
        CHECK(answer IN ('A','B','C','D')),
    explanation TEXT,                         -- 答案解析
    difficulty INTEGER DEFAULT 2              -- 难度等级（1-5）
        CHECK(difficulty BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 创建时间
);


-- ------------------------------------------------------------
-- 答题记录表 (quiz_records)
-- ------------------------------------------------------------
-- 记录用户每次答题的详细信息
-- 用于诊断算法分析薄弱知识点和学习进度追踪
CREATE TABLE IF NOT EXISTS quiz_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 记录 ID，自增主键
    user_id INTEGER NOT NULL,                 -- 用户 ID（外键）
    question_id INTEGER NOT NULL,             -- 题目 ID（外键）
    user_answer CHAR(1),                      -- 用户的答案（A/B/C/D）
    is_correct BOOLEAN,                       -- 是否正确（True/False）
    response_time INTEGER,                    -- 答题用时（秒，可选）
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 答题时间
    FOREIGN KEY (user_id) REFERENCES users(id),       -- 关联用户表
    FOREIGN KEY (question_id) REFERENCES questions(id) -- 关联题目表
);


-- ------------------------------------------------------------
-- 观看记录表 (watch_records)
-- ------------------------------------------------------------
-- 记录用户观看视频的进度
-- 支持进度百分比追踪和"已看完"标记
CREATE TABLE IF NOT EXISTS watch_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,     -- 记录 ID，自增主键
    user_id INTEGER NOT NULL,                 -- 用户 ID（外键）
    video_id INTEGER NOT NULL,                -- 视频 ID（外键）
    watch_progress INTEGER DEFAULT 0          -- 观看进度（0-100 的整数百分比）
        CHECK(watch_progress BETWEEN 0 AND 100),
    is_completed BOOLEAN DEFAULT 0,           -- 是否看完（True/False）
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 最后更新时间
    FOREIGN KEY (user_id) REFERENCES users(id),      -- 关联用户表
    FOREIGN KEY (video_id) REFERENCES videos(id)     -- 关联视频表
);

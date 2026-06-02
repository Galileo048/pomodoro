# 高中物理 AI 自适应学习平台 — 项目进度

> 最后更新：2026-06-02

---

## 一、项目概况

- **项目名称**：基于Manim与AI辅助的中学数理可视化教学资源开发与双载体传播
- **技术栈**：Flask 3.1 + SQLite + Flask-Login + Flask-WTF + ECharts + DeepSeek API
- **GitHub 仓库**：https://github.com/Galileo048/pomodoro
- **本地运行**：`python run.py` → http://localhost:5000

---

## 二、已完成功能

### 1. 用户系统
- [x] 用户注册（用户名/密码/年级）
- [x] 用户登录/登出
- [x] Flask-Login 会话管理
- [x] CSRF 保护
- [x] 密码哈希存储

### 2. 视频学习
- [x] 视频列表页（卡片式布局、分类筛选）
- [x] 视频播放页（Video.js 播放器）
- [x] 观看进度记录
- [x] 视频封面渐变背景
- [x] 收藏按钮（hover 显示）

### 3. 交互动画实验
- [x] 79 个 Canvas 交互实验（初中/高中/大学）
- [x] 物理实验：力学、电磁学、光学、波动、热学
- [x] 数学实验：函数、几何、概率、微积分
- [x] 实验列表页（按难度分级筛选）
- [x] 收藏按钮

### 4. 知识测验
- [x] 按知识点组卷
- [x] 选择题答题界面
- [x] 答题反馈（正确/错误+解析）
- [x] 得分统计
- [x] 答题记录保存

### 5. AI 智能功能
- [x] 知识诊断（基于答题数据统计正确率）
- [x] AI 学情分析（DeepSeek API）
- [x] AI 答疑助手（聊天界面）
- [x] 知识图谱可视化（ECharts 力导向图）

### 6. 学习报告
- [x] 核心指标卡片（学习时长、正确率、排名）
- [x] 近 7 天学习趋势图（ECharts 折线图）
- [x] 知识点掌握分布（饼图）
- [x] 各知识点正确率（柱状图）
- [x] 综合能力评估（雷达图）
- [x] 学习建议

### 7. 搜索功能
- [x] 导航栏搜索入口
- [x] 搜索结果页（视频+实验分类）
- [x] 输入自动补全（AJAX）
- [x] 分类筛选（全部/视频/实验）
- [x] Ctrl+K 快捷键

### 8. 收藏功能
- [x] 视频/实验收藏按钮
- [x] Toggle 切换 API
- [x] 控制台收藏列表展示

### 9. 主题切换
- [x] 深色/浅色主题
- [x] localStorage 记忆
- [x] 导航栏切换按钮
- [x] 全站 CSS 变量适配
- [x] ECharts 图表主题适配

### 10. UI/UX 优化
- [x] 首页 Hero 区域（粒子动画背景）
- [x] 卡片式布局（渐变边框、悬浮放大、发光效果）
- [x] 微交互动画（水波纹按钮、下划线动画、脉冲呼吸灯、浮动图标）
- [x] 骨架屏加载状态（Shimmer 动画）
- [x] 空状态设计（浮动图标+引导文案）
- [x] 页面过渡动画（淡入淡出）
- [x] 响应式设计（移动端适配）
- [x] 自定义滚动条

### 11. 学生控制台
- [x] 学习概览卡片（时长/正确率/视频进度/实验数）
- [x] 最近学习板块（进度条）
- [x] 我的收藏板块
- [x] 薄弱知识点提示
- [x] 快捷入口（视频/实验/报告/AI/图谱/搜索）

### 12. 性能优化
- [x] 图片懒加载（loading="lazy"）
- [x] 数据库索引（quiz_records、watch_records、favorites）
- [x] CDN 加速（Bootstrap 5、Video.js）
- [x] CSS 冗余清理

---

## 三、数据库表结构

| 表名 | 说明 | 关键字段 |
|------|------|----------|
| users | 用户表 | id, username, password_hash, grade |
| videos | 视频表 | id, title, topic, topic_id, chapter, difficulty |
| questions | 题库表 | id, topic_id, content, option_a~d, answer, explanation |
| quiz_records | 答题记录 | user_id, question_id, user_answer, is_correct |
| watch_records | 观看记录 | user_id, video_id, watch_progress, is_completed |
| favorites | 收藏表 | user_id, item_type, item_id (唯一约束) |

---

## 四、路由结构

| 路径 | 说明 | 需登录 |
|------|------|--------|
| `/` | 首页 | 否 |
| `/login` | 登录 | 否 |
| `/register` | 注册 | 否 |
| `/videos` | 视频列表 | 否 |
| `/video/<id>` | 视频播放 | 是 |
| `/experiments` | 实验列表 | 是 |
| `/experiment/<id>` | 实验运行 | 是 |
| `/quiz/<topic_id>` | 知识测验 | 是 |
| `/diagnosis` | 知识诊断 | 是 |
| `/search` | 搜索 | 否 |
| `/student/dashboard` | 学生控制台 | 是 |
| `/student/report` | 学习报告 | 是 |
| `/student/ai-tutor` | AI 答疑 | 是 |
| `/student/knowledge-graph` | 知识图谱 | 是 |
| `/api/favorites/toggle` | 收藏切换 | 是 |
| `/api/favorites/check` | 收藏检查 | 是 |
| `/api/search/suggestions` | 搜索建议 | 否 |

---

## 五、实验清单（79 个）

### 初中物理（6 个）
声音传播、平面镜成像、简单电路、杠杆原理、浮力、密度

### 初中数学（2 个）
平面直角坐标系、因式分解可视化

### 高中物理（40+ 个）
平抛运动、自由落体、斜抛运动、牛顿第二定律、弹簧弹力、匀速圆周运动、单摆、摩擦力、机械能守恒、弹性碰撞、简谐运动、匀速/匀变速直线运动、竖直上抛、受力分析、功与功率、动能定理、非弹性碰撞、库仑定律、凸透镜成像、光的折射、全反射、凹透镜成像、双缝干涉、单缝衍射、机械波、波的叠加、驻波、氢原子能级、电场线、带电粒子运动、洛伦兹力、电磁感应、交流电、光电效应

### 高中数学（20+ 个）
三角函数、一次/二次函数、指数/对数/幂函数、椭圆/双曲线/抛物线、正态分布、导数几何意义、定积分、圆的方程、直线与圆、向量运算、排列组合、等差/等比数列

### 大学数学（6 个）
矩阵变换、复数运算、傅里叶级数、泰勒展开、概率分布、梯度与等高线

### 大学物理（6 个）
简谐波、双缝干涉、RC 电路、洛伦兹力、电磁感应、气体状态方程

---

## 六、项目结构

```
physics_platform/
├── app/
│   ├── __init__.py          # 应用工厂
│   ├── models.py            # 数据库模型
│   ├── routes/
│   │   ├── auth.py          # 认证路由
│   │   ├── videos.py        # 视频路由
│   │   ├── quiz.py          # 测验路由
│   │   ├── diagnosis.py     # 诊断路由
│   │   ├── experiments.py   # 实验路由（79 个实验注册表）
│   │   ├── student.py       # 学生端路由
│   │   ├── search.py        # 搜索路由
│   │   └── favorites.py     # 收藏路由
│   ├── templates/
│   │   ├── base.html        # 基础模板（导航+主题切换）
│   │   ├── index.html       # 首页 Hero
│   │   ├── login.html       # 登录
│   │   ├── register.html    # 注册
│   │   ├── video_list.html  # 视频列表
│   │   ├── video_play.html  # 视频播放
│   │   ├── quiz.html        # 知识测验
│   │   ├── diagnosis.html   # 知识诊断
│   │   ├── experiments.html # 实验列表
│   │   ├── experiments/     # 79 个实验模板
│   │   ├── student/         # 学生端页面
│   │   └── search/          # 搜索结果页
│   └── static/
│       └── css/style.css    # 主样式表（3200+ 行）
├── physics.db               # SQLite 数据库
├── run.py                   # 启动脚本
└── PROJECT_PROGRESS.md      # 本文件
```

---

## 七、后续计划

### 内容扩充
- [ ] 视频内容扩充至 15-20 个
- [ ] 题库扩充至 60-100 道
- [ ] 添加更多实验（目标 100+）

### 功能完善
- [ ] 导出 PDF 学习报告
- [ ] 学习路径推荐
- [ ] 错题本功能
- [ ] 学习提醒/打卡

### 部署上线
- [ ] 云服务器部署
- [ ] 域名配置
- [ ] HTTPS 证书
- [ ] 数据库迁移至 PostgreSQL

---

## 八、Git 提交记录

| 日期 | 提交 | 说明 |
|------|------|------|
| 2026-06-02 | a9c7578 | feat: 网站全面优化（UI/UX+搜索/收藏/主题+性能） |
| 2026-06-01 | 45c78e7 | style: 玻璃拟态卡片 + 圆点标记 + UI优化 |
| 2026-06-01 | e9d14fd | chore: 品牌更新 + 79个实验添加教育内容 |
| 2026-06-01 | ac60429 | feat: 为全部79个交互动画添加教育内容 |
| 2026-06-01 | 3e00441 | feat: 高中交互动画扩充至59个，总计79个实验 |
| 2026-06-01 | b695068 | fix: 实验列表页分类筛选按钮支持JS过滤 |

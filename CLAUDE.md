# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

数学可视化动画系列——用 Manim 制作中学数学/物理教学动画视频，发布到抖音和B站。

## 目录结构

```
动画源码/          ← Manim Python 源码
动画视频/          ← 最终渲染的 MP4 视频
```

**命名规则：** 源码和视频文件名保持一致，如 `第1期_什么是导数.py` → `第1期_什么是导数.mp4`

## 渲染命令

```bash
# 低质量预览（快速测试）
python -m manim render -ql 动画源码/第1期_什么是导数.py DerivativeScene

# 高质量渲染（发布用）
python -m manim render -pqh 动画源码/第1期_什么是导数.py DerivativeScene
```

## 大创项目信息

**项目名称：** 基于Manim与AI辅助的中学数理可视化教学资源开发与双载体传播

**团队结构：** 物理师范 + 数学师范 + 计算机 + 网工

**核心产出：**
- Manim程序化动画视频（15-20个）
- 互动式可视化学习APP（可选）
- 个人网站（GitHub Pages）
- B站/抖音合集发布

**技术路线：** 内容选题 → 脚本设计 → AI辅助动画制作 → 视频合成 → 双载体发布 → 反馈迭代

**申报策略：**
- 定位为"教育技术创新类"项目，避免被归为"教学实践"
- 关键词：跨平台开发、程序化动画引擎、AI辅助编程、参数化可视化
- 利用B站播放量和GitHub提交记录作为成果证明

## Manim 动画吸引力技巧

参考：`media/Manim动画吸引力技巧指南.docx`

### 核心原则
- **节奏感**：有快有慢，有张有驰，用 rate_func 控制
- **悬念感**：先展示问题，再揭示答案
- **统一性**：风格、颜色、节奏保持一致
- **简洁性**：每帧只传达一个核心信息
- **情感共鸣**：技术是手段，情感是目的

### 文字动效
| 效果 | 代码 | 适用场景 |
|------|------|----------|
| 逐字打字 | `AddTextLetterByLetter(text, run_time=3)` | 引入新概念 |
| 弹入 | `text.animate.scale(1.2).set_color(YELLOW)` → 缩回 | 活泼强调 |
| 滑入 | `text.shift(LEFT*5)` → `animate.shift(RIGHT*5)` | 列表项展示 |
| 高亮框 | `SurroundingRectangle(keyword, color=YELLOW)` | 突出关键词 |
| 文字变形 | `Transform(text1, text2)` / `ReplacementTransform` | 概念转换 |

### 场景切换
| 效果 | 实现 |
|------|------|
| 淡入淡出 | `FadeOut(scene1), FadeIn(scene2)` |
| 推拉镜头 | `self.camera.frame.animate.scale(0.5).move_to(target)` |
| 平移转场 | `self.camera.frame.animate.shift(RIGHT * 5)` |
| 刷屏效果 | Rectangle 从一侧滑入覆盖 |

### 高级技巧
- **TracedPath**：物体运动留下光痕 `TracedPath(dot.get_center, stroke_color=YELLOW)`
- **缓动函数**：smooth（自然）、ease_in（加速）、ease_out（减速）、there_and_back（往复）、wiggle（抖动）
- **层次感**：远处物体更小、更淡、更透明 `scale(0.5).set_opacity(0.3)`
- **时间节奏**：引入 0.5-1s，展示 1-3s，过渡 0.3-0.5s，停顿 0.5-1s
- **ValueTracker + always_redraw**：平滑动画的核心模式（3b1b 风格）
- **实时信息面板**：右上角半透明面板显示动态数据

### 配色方案
| 风格 | 主色调 | 适用场景 |
|------|--------|----------|
| 科技感 | 蓝色、青色、白色 | 数学、编程、未来 |
| 温暖感 | 橙色、黄色、粉色 | 教育、人文、故事 |
| 高对比 | 黑色、白色、红色 | 强调、警示、重点 |
| 梦幻感 | 紫色、蓝紫色、粉蓝色 | 艺术、抽象 |
| 自然感 | 绿色、棕色、蓝绿色 | 生物、环保 |

### 3b1b 经典配色
```python
BG = "#1C1C1C"        # 深灰背景
BLUE = "#58C4DD"      # 主曲线
GREEN = "#83C167"     # 辅助元素
YELLOW = "#FFFF00"    # 高亮强调
RED = "#FF6666"       # 关键点/警示
```

### 常见错误
- 动画过快 → 增加 run_time 或分步展示
- 信息过载 → 每帧只传达一个点
- 颜色混乱 → 定义统一配色方案
- 转场突兀 → 加入过渡动画
- 缺乏聚焦 → 用 SurroundingRectangle 或镜头运动引导视线

### 节奏参考（动画时间表模板）
| 时间 | 动作 | 技巧 |
|------|------|------|
| 0:00-0:03 | 问题文字弹入 | Pop-in + 黄色 |
| 0:03-0:08 | 曲线画出 | TracedPath 轨迹 |
| 0:08-0:15 | 镜头推近 | Zoom 细节 |
| 0:15-0:25 | 核心动画 | 逐渐接近，节奏感 |
| 0:25-0:35 | 公式出现 | Typewriter |
| 0:35-0:45 | 总结归纳 | Transform 过渡 |

## 用户偏好

- 始终使用中文回复用户
- Manim 动画源码放到 `动画源码/` 目录，最终渲染视频放到 `动画视频/` 目录
- 源码文件名和视频文件名保持一致（如 `第1期_什么是导数.py` → `第1期_什么是导数.mp4`）
- Manim 代码必须写详细的中文注释，每个函数、每个动画步骤都要说明用途

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
- Author a backlog-ready spec/issue → invoke /spec

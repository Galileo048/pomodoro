# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Formula2Manim generates Manim animations from physics/math formulas with optional DeepSeek AI assistance. The tool parses SymPy expressions, detects physics models, computes trajectories, and renders animated videos.

## Key Commands

```bash
# Install dependencies
pip install -r requirements.txt
pip install -e .  # Register f2m CLI globally

# Run the CLI
f2m -f "x = v0*t + 0.5*a*t**2" -p "v0=0, a=9.8" --t-range "0,10"
f2m --describe "A ball thrown at 45 degrees" --ai  # AI-assisted

# Validate without rendering
f2m -f "x = v0*t" -p "v0=10" --dry-run -v

# Run tests
pytest tests/ -v
pytest tests/test_parser.py -v  # Single test file
```

## Architecture

**Pipeline:** CLI (`cli.py`) → Parser (`parser/`) → Physics Model (`physics_models/`) → Scene Builder (`manim_scenes/`) → Manim render

**Core components:**
- `parser/formula_parser.py` - SymPy formula parsing with variable extraction
- `parser/param_parser.py` - Parameter string parsing ("v0=0, a=9.8")
- `physics_models/registry.py` - Model auto-detection via variable/parameter heuristics
- `physics_models/kinematics.py` - UniformAcceleration, ProjectileMotion models
- `manim_scenes/scene_builder.py` - Dynamic Manim scene generation from trajectory data
- `ai_assistant/client.py` - DeepSeek API client (formula generation, model suggestion, scene enhancement, error diagnosis)
- `gui.py` - PyQt6 GUI with live Manim editor

**Templates** (`templates/`) - Pre-built Manim scenes for specific physics/math scenarios (circular motion, wave, spring, etc.)

**Model detection** (`registry.py`): Uses variable names and parameter presence to auto-select physics model. AI can override for ambiguous cases.

## Configuration

Environment variables (set in `.env` or shell):
- `DEEPSEEK_API_KEY` - Required for `--ai` features
- `F2M_OUTPUT_DIR` - Output directory (default: `./outputs`)
- `F2M_QUALITY` - Default quality: l/m/h/p/k
- `F2M_FPS` - Default FPS

## Adding Physics Models

1. Create class inheriting `PhysicsModel` in `physics_models/`
2. Implement `validate()`, `compute_trajectory()`, `get_latex_label()`
3. Register in `physics_models/registry.py` with detection heuristics

## Windows Notes

CLI handles Windows console encoding automatically (UTF-8 reconfiguration in `cli.py`).

## 大创项目信息

**项目名称：** 基于Manim与AI辅助的中学数理可视化教学资源开发与双载体传播

**团队结构：** 物理师范 + 数学师范 + 计算机 + 网工

**核心产出：**
- Manim程序化动画视频（15-20个）
- 互动式可视化学习APP（可选）
- 个人网站（GitHub Pages）
- B站合集发布

**技术路线：** 内容选题 → 脚本设计 → AI辅助动画制作 → 视频合成 → 双载体发布 → 反馈迭代

**申报策略：**
- 定位为"教育技术创新类"项目，避免被归为"教学实践"
- 关键词：跨平台开发、程序化动画引擎、AI辅助编程、参数化可视化
- 利用B站播放量和GitHub提交记录作为成果证明

**文件位置：** 详细规划见 `docx_content.txt`（DeepSeek对话记录）

## 用户偏好

- 始终使用中文回复用户

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

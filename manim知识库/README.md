# Manim 知识库

本文件夹是 Manim 动画制作的参考资源库。制作动画前应先检索此文件夹。

## 目录结构

```
manim知识库/
├── README.md                  ← 本文件（索引+检索规则）
├── 分镜脚本_第1-3期.docx      ← 已完成的分镜脚本
├── 分镜脚本_第4-5期.docx      ← 已完成的分镜脚本
├── 物理项目/                  ← 物理相关 Manim 项目参考
│   └── README.md
├── 数学项目/                  ← 数学相关 Manim 项目参考
│   └── README.md
├── AI工具/                    ← AI+Manim 工具参考
│   └── README.md
├── 3b1b源码/                  ← 3Blue1Brown 源码分析
│   ├── README.md
│   └── 曼德勃罗集_CPU方案.py
└── 技巧与经验/                ← 制作技巧和踩坑记录
    └── Manim动画吸引力技巧指南.docx
```

## 检索规则（制作动画前必读）

### 1. 新动画制作流程
制作任何 Manim 动画前，按以下顺序检索：
1. **分镜脚本** → 看是否已有对应主题的分镜
2. **技巧与经验/** → 看 `CLAUDE.md` 中的踩坑记录（#1-#15）
3. **物理项目/ 或 数学项目/** → 看是否有类似主题的现成代码可参考
4. **3b1b源码/** → 看 3b1b 是否有类似的动画模式
5. **AI工具/** → 如果需要自动化生成，参考 AI 工具方案

### 2. 按主题检索
| 主题 | 先看 | 再看 |
|------|------|------|
| 力学（运动/力/能量） | 物理项目/manim-physics | 3b1b源码/ |
| 电磁学（电场/磁场） | 物理项目/elbrujo325 | 物理项目/manim-physics |
| 光学（透镜/射线） | 物理项目/manim-physics | 物理项目/manim-fa-physics |
| 波动 | 物理项目/overtones | 物理项目/manim-physics |
| 微积分（导数/积分） | 数学项目/Moqiyun | 3b1b源码/ |
| 线性代数（矩阵/变换） | 3b1b源码/ | CLAUDE.md 踩坑记录 |
| 复数/欧拉公式 | 3b1b源码/ | CLAUDE.md 踩坑记录 |
| 分形（曼德勃罗集） | 3b1b源码/曼德勃罗集 | CLAUDE.md #14-#15 |
| 3D场景 | 物理项目/from_scratch | CLAUDE.md #10 |
| 像素渲染 | CLAUDE.md #13-#15 | 3b1b源码/ |

### 3. 技术问题检索
遇到技术问题时，优先查 `CLAUDE.md` 中的踩坑记录：
- 线性变换 → #1（不用 ApplyMatrix）
- 角度弧线 → #2（用 ParametricFunction）
- 中文文字 → #3（不能放 MathTex）
- 坐标系移动 → #4（VGroup + ax.c2p）
- 矩形框 → #5（先定位再建框）
- 动点可见性 → #6（发光圈+偏移）
- 信息面板 → #7（半透明+行间距）
- corner_radius → #8（ManimCE 不支持）
- 标签跟随 → #9（Transform 一起动）
- 3D相机 → #10（用 move_camera）
- ImageMobject → #11（用 Group）
- 球体材质 → #12（set_fill+set_stroke）
- 像素渲染 → #13-#15
- 3b1b GPU方案 → #14

### 4. 中文资源优先
制作中文教育动画时，优先参考：
1. `物理项目/README.md` 中的中文项目
2. `数学项目/README.md` 中的 Moqiyun（最全中文资源）
3. `AI工具/README.md` 中的 mathanim-desktop 和 manim_gpt

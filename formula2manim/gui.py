r"""Formula2Manim v3 — 物理 & 数学动画生成器 (美化版).

用法:
    python -m formula2manim.gui
    f2m-gui  (pip install -e . 后)
"""

from __future__ import annotations

import os, subprocess, sys, threading, time, traceback, uuid
from pathlib import Path
from tkinter import Tk, StringVar, DoubleVar
from tkinter import ttk, filedialog, messagebox

from formula2manim.templates import TEMPLATES as SCENE_TEMPLATES, get_template_path
from formula2manim.templates import TemplateDef

# ═══════════════════════════════════════════════════════════════════════
# Design tokens — 统一配色
# ═══════════════════════════════════════════════════════════════════════
BG0    = "#0b0b1a"   # 主背景 (最深)
BG1    = "#12122a"   # 卡片背景
BG2    = "#1a1a3e"   # 悬浮层
ACCENT = "#7c8cf8"   # 主色调 (柔和蓝紫)
GREEN  = "#50c878"   # 成功/导出
AMBER  = "#f0a050"   # 警告/AI
RED    = "#f05a5a"   # 错误
PINK   = "#e090d0"   # AI 按钮
CYAN   = "#5cc8c8"   # 信息
TEXT   = "#d0d0e8"   # 主文字
TEXT2  = "#8888b0"   # 辅助文字
TEXT3  = "#606088"   # 提示文字
BORDER = "#252550"   # 边框线

FONT_TITLE  = ("Microsoft YaHei", 17, "bold")
FONT_SEC    = ("Microsoft YaHei", 11, "bold")
FONT_BODY   = ("Microsoft YaHei", 9)
FONT_SMALL  = ("Microsoft YaHei", 8)
FONT_CODE   = ("Cascadia Code", 10)
FONT_BTN    = ("Microsoft YaHei", 10)
FONT_BTN_SM = ("Microsoft YaHei", 9)

QUALITY_OPTIONS: dict[str, str] = {
    "低画质 480p (快速预览)": "l", "标准 720p 30fps": "m",
    "高清 1080p 60fps": "h", "超清 1440p": "p", "4K 2160p": "k",
}


# ═══════════════════════════════════════════════════════════════════════
class Formula2ManimGUI:
    """主界面"""

    def __init__(self, root: Tk) -> None:
        self.root = root
        root.title("Formula2Manim v3 — 物理公式 & 数学动画生成器")
        root.geometry("800x820"); root.minsize(700, 720)
        root.configure(bg=BG0)

        # State
        self.quality_var   = StringVar(value="标准 720p 30fps")
        self.status_var    = StringVar(value="就绪 — 选择模板输入描述即可开始")
        self.progress_var  = DoubleVar(value=0.0)
        self.output_var    = StringVar(value=str(Path("./outputs").resolve()))
        self.latest_video: str | None = None
        self._stop_flag    = threading.Event()
        self._param_widgets: dict[str, ttk.Entry] = {}
        self._selected_template: TemplateDef | None = None
        self._tab_var: str = "物理"
        self._tpl_combo_vars: dict[str, StringVar] = {}
        self._tpl_desc_vars: dict[str, StringVar] = {}
        self._param_frames: dict[str, ttk.Frame] = {}
        self._card: ttk.Frame = ttk.Frame()

        self._setup_theme()
        self._build_ui()
        self.root.after(100, lambda: self.status_var.set(
            "就绪 — 选择一个模板或输入描述开始"))

    # ── Theme ──────────────────────────────────────────────────────────
    def _setup_theme(self) -> None:
        s = ttk.Style()
        s.theme_use("clam")

        # Base
        s.configure(".", background=BG0, foreground=TEXT, font=FONT_BODY)
        s.configure("TFrame", background=BG0)
        s.configure("TNotebook", background=BG0, borderwidth=0)
        s.configure("TNotebook.Tab", font=FONT_BTN, padding=(16, 7),
                    background=BG1, foreground=TEXT2, borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", BG2)],
              foreground=[("selected", ACCENT)], expand=[("selected", (0, 0, 0, 2))])

        # Cards
        s.configure("Card.TFrame", background=BG1, relief="flat", borderwidth=1)
        s.configure("Card2.TFrame", background=BG2, relief="flat", borderwidth=1)

        # Labels
        s.configure("Title.TLabel", font=FONT_TITLE, foreground=ACCENT, background=BG0)
        s.configure("Section.TLabel", font=FONT_SEC, foreground=TEXT, background=BG1)
        s.configure("Hint.TLabel", font=FONT_SMALL, foreground=TEXT3, background=BG1)
        s.configure("Hint2.TLabel", font=FONT_SMALL, foreground=TEXT3, background=BG2)
        s.configure("Status.TLabel", font=FONT_BODY, foreground=TEXT, background=BG0)
        s.configure("Accent.TLabel", font=FONT_BODY, foreground=ACCENT, background=BG1)

        # Buttons
        s.configure("TButton", font=FONT_BTN, background="#2a2a50",
                    foreground=TEXT, borderwidth=0, padding=(12, 7))
        s.map("TButton", background=[("active", "#3a3a68")],
              foreground=[("active", "#ffffff")])

        # Primary
        s.configure("Primary.TButton", font=("Microsoft YaHei", 11, "bold"),
                    background=ACCENT, foreground="#ffffff", borderwidth=0,
                    padding=(16, 10))
        s.map("Primary.TButton",
              background=[("active", "#9aa8ff")], foreground=[("active", "#ffffff")])

        # AI
        s.configure("AI.TButton", font=("Microsoft YaHei", 11, "bold"),
                    background="#9070d0", foreground="#ffffff", borderwidth=0,
                    padding=(14, 9))
        s.map("AI.TButton", background=[("active", "#a888e8")])

        # Export
        s.configure("Export.TButton", font=FONT_BTN_SM,
                    background="#2a6040", foreground=GREEN, borderwidth=0,
                    padding=(12, 7))
        s.map("Export.TButton", background=[("active", "#3a7858")])

        # Template buttons
        s.configure("Tpl.TButton", font=("Microsoft YaHei", 10, "bold"),
                    background=BG2, foreground=TEXT, borderwidth=1,
                    padding=(14, 8))
        s.map("Tpl.TButton", background=[("active", "#2a2a55")],
              foreground=[("active", "#ffffff")])

        s.configure("Tpl2.TButton", font=FONT_BTN_SM,
                    background=BG2, foreground=TEXT2, borderwidth=1,
                    padding=(10, 6))
        s.map("Tpl2.TButton", background=[("active", "#282850")])

        # Entry
        s.configure("TEntry", fieldbackground=BG2, foreground=TEXT,
                    insertcolor=ACCENT, borderwidth=2, relief="flat",
                    font=FONT_CODE, padding=8)
        s.map("TEntry", fieldbackground=[("focus", "#1e1e3e")],
              bordercolor=[("focus", ACCENT)])

        # Combobox
        s.configure("TCombobox", fieldbackground=BG2, foreground=TEXT,
                    arrowcolor=TEXT, font=FONT_BODY)
        s.map("TCombobox", fieldbackground=[("readonly", BG2)])

        # Progress bar
        s.configure("TProgressbar", background=ACCENT, troughcolor=BG1,
                    borderwidth=0, thickness=6)
        s.configure("Sep.TSeparator", background=BORDER)

    # ── Build ──────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        main = ttk.Frame(self.root, padding=14)
        main.pack(fill="both", expand=True)

        # ═══ Header ═══
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="Formula2Manim v3",
                  style="Title.TLabel").pack(side="left")
        ttk.Label(header,
                  text="物理公式 & 数学动画 · AI 驱动 · 一键生成",
                  font=FONT_SMALL, foreground=TEXT3, background=BG0
                  ).pack(side="left", padx=12)

        # ═══ Tabs ═══
        nb = ttk.Notebook(main)
        nb.pack(fill="x", pady=(0, 8))
        nb.configure(height=300)

        phys_f = ttk.Frame(nb); nb.add(phys_f, text="  物理模板  ")
        self._build_template_tab(phys_f, "物理")

        math_f = ttk.Frame(nb); nb.add(math_f, text="  数学模板  ")
        self._build_template_tab(math_f, "数学")

        ai_f = ttk.Frame(nb); nb.add(ai_f, text="  🤖 AI 生成  ")
        self._build_ai_tab(ai_f)

        live_f = ttk.Frame(nb); nb.add(live_f, text="  💻 实时编辑  ")
        self._build_live_tab(live_f)

        # ═══ Settings bar ═══
        self._section_begin(main, "⚙ 输出设置")
        bar = ttk.Frame(self._card)
        bar.pack(fill="x", pady=4)
        for i in range(4):
            bar.grid_columnconfigure(i, weight=1)

        ttk.Label(bar, text="视频画质", style="Hint.TLabel").grid(row=0, column=0, sticky="w")
        self.quality_combo = ttk.Combobox(
            bar, textvariable=self.quality_var,
            values=list(QUALITY_OPTIONS.keys()),
            state="readonly", width=22)
        self.quality_combo.grid(row=1, column=0, padx=(0, 8), sticky="ew")

        ttk.Label(bar, text="输出目录", style="Hint.TLabel").grid(row=0, column=1, sticky="w",
                                                                   columnspan=3)
        of = ttk.Frame(bar); of.grid(row=1, column=1, columnspan=3, sticky="ew")
        ttk.Entry(of, textvariable=self.output_var, font=FONT_SMALL).pack(
            side="left", fill="x", expand=True)
        ttk.Button(of, text="📂", width=4, command=self._browse_output).pack(
            side="left", padx=(3, 0))
        self._section_end()

        # ═══ Action buttons ═══
        btn_bar = ttk.Frame(main)
        btn_bar.pack(fill="x", pady=(8, 6))

        left_btns = ttk.Frame(btn_bar)
        left_btns.pack(side="left")
        ttk.Button(left_btns, text="🚀 渲染动画", style="Primary.TButton",
                   command=self._render_current).pack(side="left", padx=(0, 8))
        ttk.Button(left_btns, text="📋 导出代码", style="Export.TButton",
                   command=self._export_code).pack(side="left", padx=(0, 8))

        right_btns = ttk.Frame(btn_bar)
        right_btns.pack(side="right")
        ttk.Button(right_btns, text="📂 打开目录", style="TButton",
                   command=self._open_output).pack(side="left", padx=(4, 0))
        ttk.Button(right_btns, text="▶ 播放视频", style="TButton",
                   command=self._play_latest).pack(side="left", padx=(4, 0))

        # ═══ Status ═══
        ttk.Separator(main, orient="horizontal", style="Sep.TSeparator").pack(
            fill="x", pady=(0, 6))
        status_frame = ttk.Frame(main)
        status_frame.pack(fill="x")

        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var,
                                            mode="indeterminate", length=160)
        self.progress_bar.pack(side="left", padx=(0, 8))
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var,
                                      style="Status.TLabel")
        self.status_label.pack(side="left", fill="x", expand=True)

        ttk.Label(main, text="SymPy + Manim Community + DeepSeek  |  v3.0",
                  font=FONT_SMALL, foreground=TEXT3, background=BG0
                  ).pack(pady=(8, 0))

    # ═══════════ TAB: 模板 ═══════════════════════════════════════════════
    def _build_template_tab(self, parent: ttk.Frame, category: str) -> None:
        templates = [t for t in SCENE_TEMPLATES if t["category"] == category]
        inner = ttk.Frame(parent, style="Card.TFrame", padding=10)
        inner.pack(fill="both", expand=True)

        # Title
        title_text = "物理场景模板" if category == "物理" else "数学动画模板"
        ttk.Label(inner, text=title_text, style="Section.TLabel").pack(anchor="w")

        # Template cards in a grid
        cards = ttk.Frame(inner, style="Card.TFrame")
        cards.pack(fill="x", pady=(6, 8))
        cols = 4
        for i, tpl in enumerate(templates):
            card = ttk.Frame(cards, style="Card2.TFrame", padding=8)
            card.grid(row=i // cols, column=i % cols, padx=3, pady=3, sticky="nsew")
            for c in range(cols):
                cards.grid_columnconfigure(c, weight=1)

            ttk.Label(card, text=tpl["name"], font=("Microsoft YaHei", 10, "bold"),
                      foreground=TEXT, background=BG2).pack(anchor="w")
            ttk.Label(card, text=tpl["description"], font=FONT_SMALL,
                      foreground=TEXT3, background=BG2, wraplength=130).pack(
                          anchor="w", pady=(2, 5))
            ttk.Button(card, text="选择此模板", style="Tpl2.TButton",
                       command=lambda t=tpl: self._on_tpl_select_card(t)
                       ).pack(anchor="w")

        # Parameter area (shown when template selected)
        ttk.Separator(inner, orient="horizontal", style="Sep.TSeparator").pack(
            fill="x", pady=2)
        param_label = ttk.Label(inner, text="📐 参数调整 (选择模板后出现)",
                                style="Hint.TLabel")
        param_label.pack(anchor="w", pady=(4, 2))

        pf = ttk.Frame(inner, style="Card2.TFrame", padding=6)
        pf.pack(fill="x")
        self._param_frames[category] = pf

        # Pre-select first template
        if templates:
            self._on_tpl_select_card(templates[0])

    def _on_tpl_select_card(self, tpl: TemplateDef) -> None:
        self._selected_template = tpl
        self._tab_var = tpl["category"]
        self._build_param_inputs()
        self.status_var.set(f"已选择「{tpl['name']}」— 修改参数后点击渲染")

    def _build_param_inputs(self) -> None:
        tpl = self._selected_template
        if not tpl:
            return
        cat = tpl["category"]
        pf = self._param_frames.get(cat)
        if not pf:
            return
        for w in pf.winfo_children():
            w.destroy()
        self._param_widgets.clear()

        if not tpl["params"]:
            ttk.Label(pf, text="此模板无可调参数", style="Hint2.TLabel").pack(anchor="w")
            return

        ttk.Label(pf, text="调整参数后点击渲染:", style="Hint2.TLabel").pack(anchor="w", pady=(0, 4))
        for key, pdef in tpl["params"].items():
            row = ttk.Frame(pf, style="Card2.TFrame")
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=pdef["label"], style="Hint2.TLabel",
                      width=20, anchor="e").pack(side="left", padx=(0, 6))
            e = ttk.Entry(row, font=FONT_CODE, width=14)
            e.insert(0, pdef["default"])
            e.pack(side="left")
            self._param_widgets[key] = e

    # ═══════════ TAB: 手动公式 ═══════════════════════════════════════════
    # ═══════════ TAB: AI ═════════════════════════════════════════════════
    def _build_ai_tab(self, parent: ttk.Frame) -> None:
        inner = ttk.Frame(parent, style="Card.TFrame", padding=14)
        inner.pack(fill="both", expand=True)

        ttk.Label(inner, text="🤖 AI 智能生成 — 用自然语言描述物理场景",
                  style="Section.TLabel").pack(anchor="w")
        ttk.Label(inner, text="支持中文描述，AI 自动生成公式、参数、配色并渲染动画",
                  style="Hint.TLabel").pack(anchor="w", pady=(2, 10))

        self.ai_entry = ttk.Entry(inner, font=("Microsoft YaHei", 12))
        self.ai_entry.pack(fill="x", pady=(0, 10))
        self.ai_entry.insert(0, "一个球从 20 米高处以 10m/s 的速度水平抛出")

        ttk.Button(inner, text="🤖 让 AI 生成并渲染", style="AI.TButton",
                   command=self._render_ai).pack(side="left")
        ttk.Label(inner, text="DeepSeek API 密钥已配置 (.env)",
                  style="Hint.TLabel").pack(side="left", padx=12)

    # ═══════════ TAB: 实时编辑 ═══════════════════════════════════════════
    def _build_live_tab(self, parent: ttk.Frame) -> None:
        inner = ttk.Frame(parent, style="Card.TFrame", padding=14)
        inner.pack(fill="both", expand=True)

        ttk.Label(inner, text="💻 实时 Manim 代码编辑器",
                  style="Section.TLabel").pack(anchor="w", pady=(0, 8))

        desc = (
            "独立的代码编辑器窗口，支持:\n"
            "  • 直接编辑 Manim 源码，实时渲染预览\n"
            "  • AI 辅助修改代码 (输入「把背景改成深蓝」等)\n"
            "  • 快捷修改按钮 (变色/变速/加元素)\n"
            "  • 撤销 / 导出 / 保存 / 打开文件"
        )
        ttk.Label(inner, text=desc, font=FONT_BODY, foreground=TEXT2,
                  background=BG1).pack(anchor="w", pady=(0, 12))

        ttk.Button(inner, text="🚀 打开空白编辑器", style="Primary.TButton",
                   command=lambda: self._launch_live_editor("")
                   ).pack(side="left", padx=(0, 8))
        ttk.Button(inner, text="📋 用当前模板代码打开", style="AI.TButton",
                   command=self._launch_live_with_template
                   ).pack(side="left", padx=(0, 8))

    def _launch_live_editor(self, code: str = "") -> None:
        from formula2manim.live_editor import LiveEditor
        w = Tk(); LiveEditor(w, code)

    def _launch_live_with_template(self) -> None:
        tpl = self._selected_template
        if tpl:
            path = get_template_path(tpl["file"])
            if path.exists():
                source = path.read_text(encoding="utf-8")
                for key, pdef in tpl["params"].items():
                    val = self._param_widgets.get(key, None)
                    source = source.replace(
                        f"__PARAM_{key}__",
                        val.get().strip() if val else pdef["default"])
                self._launch_live_editor(source)
                return
        self._launch_live_editor()

    # ═══════════ ACTIONS ═════════════════════════════════════════════════
    def _section_begin(self, parent, title):
        self._card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        self._card.pack(fill="x", pady=(0, 6))
        ttk.Label(self._card, text=title, style="Section.TLabel").pack(anchor="w")
    def _section_end(self):
        pass

    def _browse_output(self):
        p = filedialog.askdirectory(title="选择输出目录")
        if p:
            self.output_var.set(p)
    def _open_output(self):
        d = self.output_var.get(); os.makedirs(d, exist_ok=True); os.startfile(d)
    def _play_latest(self):
        if self.latest_video and Path(self.latest_video).exists():
            os.startfile(self.latest_video)
        else:
            messagebox.showinfo("提示", "还没有渲染成功的视频")
    def _get_tab(self):
        try:
            nb = self.root.winfo_children()[0].winfo_children()[1]
            return ["physics", "math", "ai", "live"][nb.index(nb.select())]
        except Exception:
            return "physics"

    def _render_current(self):
        tab = self._get_tab()
        if tab in ("physics", "math"): self._render_template()
        elif tab == "ai": self._render_ai()
        else: messagebox.showinfo("提示", "请切换到模板/公式/AI 标签页")

    # ── Render template ───────────────────────────────────────────────
    def _render_template(self):
        if not self._selected_template:
            messagebox.showwarning("提示", "请先选择一个模板"); return
        tpl = self._selected_template
        source = self._build_template_source(tpl)
        out_dir = Path(self.output_var.get())
        quality = self.quality_var.get()
        self._ui_busy(True)
        self.status_var.set(f"正在渲染「{tpl['name']}」...")
        threading.Thread(target=self._template_worker,
                         args=(source, tpl["name"], out_dir, quality, False),
                         daemon=True).start()

    def _export_code(self):
        if not self._selected_template:
            messagebox.showwarning("提示", "请先选择一个模板"); return
        tpl = self._selected_template
        source = self._build_template_source(tpl)
        out_dir = Path(self.output_var.get())
        self._ui_busy(True)
        self.status_var.set(f"正在导出「{tpl['name']}」代码...")
        threading.Thread(target=self._template_worker,
                         args=(source, tpl["name"], out_dir, "m", True),
                         daemon=True).start()

    def _build_template_source(self, tpl):
        """Build the source code with parameter substitution (call on main thread)."""
        path = get_template_path(tpl["file"])
        source = path.read_text(encoding="utf-8")
        for key in tpl["params"]:
            w = self._param_widgets.get(key, None)
            val = w.get().strip() if w else tpl["params"][key]["default"]
            source = source.replace(f"__PARAM_{key}__", val)
        return source

    def _template_worker(self, source, name, out_dir, quality, export_only):
        try:
            out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
            safe_name = name.replace(" ", "_").replace("→", "to")
            gen_path = out_dir / f"{safe_name}.py"
            gen_path.write_text(source, encoding="utf-8")

            if export_only:
                save = filedialog.asksaveasfilename(
                    title="保存 Manim 源码", initialfile=f"{safe_name}.py",
                    defaultextension=".py", filetypes=[("Python", "*.py")])
                if save:
                    Path(save).write_text(source, encoding="utf-8")
                    self.root.after(0, lambda: self._on_export_ok(save))
                else:
                    self.root.after(0, lambda: self._ui_busy(False))
                return

            q = QUALITY_OPTIONS.get(quality, "m")
            cmd = [sys.executable, "-m", "manim", "render", f"-q{q}",
                   "--media_dir", str(out_dir.resolve()), str(gen_path.resolve())]
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               timeout=300, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            if r.returncode != 0:
                msg = (r.stdout + r.stderr)[-2000:]
                self.root.after(0, lambda: self._on_err(f"渲染失败\n{msg}"))
                return
            video = self._find_video_path(r.stdout + r.stderr, str(out_dir))
            if video:
                self.latest_video = video
                self.root.after(0, lambda: self._on_ok(video))
            else:
                self.root.after(0, lambda: self._on_err("未找到输出视频"))
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self._on_err("渲染超时 (5分钟)"))
        except Exception as e:
            self.root.after(0, lambda: self._on_err(f"{e}"))

    def _find_video_path(self, cli_output: str, output_dir: str) -> str | None:
        """Parse the video path from CLI output or find the newest mp4."""
        import re
        # Try to find a path ending in .mp4 from CLI output
        for line in cli_output.split("\n"):
            m = re.search(r"([A-Za-z]:[^\s]*?\.mp4)", line)
            if m:
                p = Path(m.group(1))
                if p.exists():
                    return str(p)
        # Fallback: find newest mp4 in output directory
        try:
            mp4s = sorted(
                Path(output_dir).rglob("*.mp4"),
                key=lambda x: x.stat().st_mtime, reverse=True,
            )
            return str(mp4s[0]) if mp4s else None
        except Exception:
            return None

    # ── Render AI ─────────────────────────────────────────────────────
    def _render_ai(self):
        desc = self.ai_entry.get().strip()
        if not desc: messagebox.showwarning("提示", "请输入自然语言描述"); return
        # Read on main thread
        quality = self.quality_var.get()
        output = self.output_var.get()
        self._ui_busy(True); self.status_var.set("🤖 AI 正在生成...")
        threading.Thread(target=self._ai_worker,
                         args=(desc, quality, output), daemon=True).start()

    def _ai_worker(self, desc, quality, output):
        try:
            cmd = [sys.executable, "-m", "formula2manim.cli", "--describe", desc, "--ai",
                   "-o", output,
                   "--quality", QUALITY_OPTIONS.get(quality, "m"), "-v"]
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               timeout=300, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            out = (r.stdout + r.stderr)
            if r.returncode != 0:
                self.root.after(0, lambda: self._on_err(f"失败\n{out[-2000:]}"))
                return
            video = self._find_video_path(out, output)
            if video:
                self.latest_video = video
                self.root.after(0, lambda: self._on_ok(video))
            else:
                self.root.after(0, lambda: self._on_err(f"未找到视频\n{out[-500:]}"))
        except Exception as e:
            self.root.after(0, lambda: self._on_err(f"{e}"))

    # ── Callbacks ─────────────────────────────────────────────────────
    def _on_ok(self, path):
        self._ui_busy(False); self.status_var.set(f"✅ 渲染成功！")
        if messagebox.askyesno("渲染成功", f"视频已生成:\n\n{path}\n\n是否播放？"):
            os.startfile(path)

    def _on_export_ok(self, path):
        self._ui_busy(False); self.status_var.set(f"✅ 代码已导出: {path}")
        messagebox.showinfo("导出成功", f"源码已保存:\n{path}")

    def _on_err(self, msg):
        self._ui_busy(False); self.status_var.set(f"❌ 出错")
        messagebox.showerror("出错了", msg[:2000])

    def _ui_busy(self, busy: bool):
        s = "disabled" if busy else "normal"
        for w in [self.ai_entry, self.quality_combo]:
            try: w.configure(state=s)
            except Exception: pass
        if busy:
            self.progress_bar.configure(mode="indeterminate"); self.progress_bar.start()
        else:
            self.progress_bar.stop(); self.progress_bar.configure(mode="determinate")


# ═══════════════════════════════════════════════════════════════════════
def main():
    os.makedirs("./outputs", exist_ok=True)
    root = Tk()
    Formula2ManimGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

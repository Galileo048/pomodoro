"""实时交互式 Manim 代码编辑器 v2 (美化版) — AI 辅助修改 + 即时渲染."""

from __future__ import annotations

import os, subprocess, sys, threading, time, traceback, uuid
from pathlib import Path
from tkinter import Tk, StringVar, DoubleVar, BooleanVar
from tkinter import ttk, filedialog, messagebox, Text, END, NONE

from formula2manim.config import DEEPSEEK_API_KEY
from formula2manim.exceptions import DeepSeekAPIError

# ═══════════════ Design tokens ═══════════════
BG0   = "#0b0b1a"; BG1   = "#12122a"; BG2   = "#1a1a3e"
ACC   = "#7c8cf8"; GRN   = "#50c878"; AMB   = "#f0a050"
RED   = "#f05a5a"; PNK   = "#9070d0"; CYAN  = "#5cc8c8"
TEXT  = "#d0d0e8"; TXT2  = "#8888b0"; TXT3  = "#606088"
FONT  = ("Consolas", 11)

QMAP: dict[str, str] = {
    "低画质 480p": "l", "标准 720p": "m", "高清 1080p": "h",
    "超清 1440p": "p", "4K 2160p": "k",
}


class LiveEditor:
    def __init__(self, root: Tk, initial_code: str = "") -> None:
        self.root = root
        root.title("实时 Manim 代码编辑器 — Formula2Manim")
        root.geometry("1150x760"); root.minsize(950, 620)
        root.configure(bg=BG0)

        self._setup_theme()

        self.quality_var = StringVar(value="标准 720p")
        self.status_var  = StringVar(value="就绪 — 编辑代码后点击渲染，或使用 AI 辅助修改")
        self.progress_var = DoubleVar(value=0.0)
        self.ai_ok = BooleanVar(value=bool(DEEPSEEK_API_KEY))
        self._hist: list[str] = []

        self._build_ui()
        self._set_code(initial_code or DEFAULT_CODE)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

    def _setup_theme(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure(".", background=BG0, foreground=TEXT)
        s.configure("TFrame", background=BG0)
        s.configure("Card.TFrame", background=BG1, relief="flat", borderwidth=1)
        s.configure("Card2.TFrame", background=BG2, relief="flat", borderwidth=1)

        s.configure("Sec.TLabel", font=("Microsoft YaHei", 11, "bold"),
                    foreground=TEXT, background=BG1)
        s.configure("Hint.TLabel", font=("Microsoft YaHei", 8),
                    foreground=TXT3, background=BG1)
        s.configure("Hint2.TLabel", font=("Microsoft YaHei", 8),
                    foreground=TXT3, background=BG2)
        s.configure("Title.TLabel", font=("Microsoft YaHei", 14, "bold"),
                    foreground=ACC, background=BG0)
        s.configure("Status.TLabel", font=("Microsoft YaHei", 9),
                    foreground=TEXT, background=BG0)

        s.configure("TButton", font=("Microsoft YaHei", 9),
                    background="#2a2a50", foreground=TEXT, borderwidth=0, padding=(10, 6))
        s.map("TButton", background=[("active", "#3a3a68")])
        s.configure("Primary.TButton", font=("Microsoft YaHei", 11, "bold"),
                    background=ACC, foreground="#fff", borderwidth=0, padding=(14, 9))
        s.map("Primary.TButton", background=[("active", "#9aa8ff")])
        s.configure("AI.TButton", font=("Microsoft YaHei", 10, "bold"),
                    background=PNK, foreground="#fff", borderwidth=0, padding=(12, 7))
        s.map("AI.TButton", background=[("active", "#a888e8")])
        s.configure("Export.TButton", font=("Microsoft YaHei", 9, "bold"),
                    background="#2a6040", foreground=GRN, borderwidth=0, padding=(10, 6))
        s.map("Export.TButton", background=[("active", "#3a7858")])
        s.configure("Small.TButton", font=("Microsoft YaHei", 8),
                    background=BG2, foreground=TXT2, borderwidth=1, padding=(6, 4))
        s.map("Small.TButton", background=[("active", "#2a2a55")])
        s.configure("TEntry", fieldbackground=BG2, foreground=TEXT,
                    insertcolor=ACC, borderwidth=2, relief="flat", padding=6)
        s.map("TEntry", bordercolor=[("focus", ACC)])
        s.configure("TProgressbar", background=ACC, troughcolor=BG1, thickness=4)

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # ── Header ──
        hdr = ttk.Frame(main)
        hdr.pack(fill="x", pady=(0, 6))
        ttk.Label(hdr, text="💻 实时 Manim 代码编辑器", style="Title.TLabel").pack(side="left")
        if not self.ai_ok.get():
            ttk.Label(hdr, text="⚠ AI 不可用 (设置 DEEPSEEK_API_KEY)",
                      font=("Microsoft YaHei", 8), foreground=AMB, background=BG0
                      ).pack(side="left", padx=10)

        # ── Paned: left=code, right=AI ──
        pw = ttk.PanedWindow(main, orient="horizontal")
        pw.pack(fill="both", expand=True)

        # Left: Code
        left = ttk.Frame(pw, style="Card.TFrame", padding=6)
        pw.add(left, weight=3)
        ttk.Label(left, text="📝 Manim 源码", style="Sec.TLabel").pack(anchor="w", pady=(0, 4))

        cf = ttk.Frame(left); cf.pack(fill="both", expand=True)
        self.editor = Text(cf, font=FONT, bg="#0a0a16", fg=TEXT,
                           insertbackground=ACC, wrap=NONE, undo=True,
                           relief="flat", borderwidth=2, highlightthickness=0,
                           selectbackground="#3a3a68", selectforeground="#ffffff",
                           padx=8, pady=8)
        self.editor.pack(side="left", fill="both", expand=True)
        vs = ttk.Scrollbar(cf, orient="vertical", command=self.editor.yview)
        vs.pack(side="right", fill="y")
        hs = ttk.Scrollbar(left, orient="horizontal", command=self.editor.xview)
        hs.pack(side="bottom", fill="x")
        self.editor.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)

        # Right: AI chat
        right = ttk.Frame(pw, style="Card.TFrame", padding=8)
        pw.add(right, weight=1)

        ttk.Label(right, text="🤖 AI 修改代码", style="Sec.TLabel").pack(anchor="w")
        ttk.Label(right, text="输入修改要求，AI 生成新的完整代码:",
                  style="Hint.TLabel").pack(anchor="w", pady=(3, 4))

        self.chat_in = ttk.Entry(right, font=("Microsoft YaHei", 10))
        self.chat_in.pack(fill="x", pady=(0, 4))
        self.chat_in.insert(0, "把背景改成深蓝色，轨迹线改成橙色")
        self.chat_in.bind("<Return>", lambda e: self._ai_modify())

        bf = ttk.Frame(right); bf.pack(fill="x", pady=(0, 6))
        ttk.Button(bf, text="🤖 AI 修改代码", style="AI.TButton",
                   command=self._ai_modify).pack(side="left", fill="x", expand=True)
        ttk.Button(bf, text="↩ 撤销", style="TButton",
                   command=self._undo).pack(side="left", padx=(4, 0))

        # Quick commands
        ttk.Label(right, text="快捷指令:", style="Hint.TLabel").pack(anchor="w", pady=(6, 0))
        qf = ttk.Frame(right); qf.pack(fill="x", pady=(2, 6))
        cmds = [
            ("深色背景", "把背景改成深色 #1a1a2e"),
            ("金色轨迹", "把轨迹线改成金色"),
            ("2X加速", "把动画速度加快一倍"),
            ("放慢", "放慢动画速度"),
            ("红点", "把动点改成红色半径0.12"),
            ("网格", "在坐标轴下方添加网格"),
            ("公式位置", "把公式标签移到左上角"),
            ("大字体", "把所有文字字号加大4pt"),
            ("切线", "添加切线并标注斜率"),
        ]
        for i, (lbl, cmd) in enumerate(cmds):
            ttk.Button(qf, text=lbl, style="Small.TButton",
                       command=lambda c=cmd: self._quick(c)
                       ).grid(row=i // 3, column=i % 3, padx=1, pady=1, sticky="ew")
            qf.grid_columnconfigure(i % 3, weight=1)

        # Log
        ttk.Label(right, text="操作记录:", style="Hint.TLabel").pack(anchor="w", pady=(6, 2))
        self.log = Text(right, font=("Microsoft YaHei", 8), bg="#0a0a16",
                        fg=TXT3, wrap="word", height=8, relief="flat",
                        borderwidth=1, state="disabled")
        self.log.pack(fill="both", expand=True, pady=(0, 4))

        # ── Bottom bar ──
        bot = ttk.Frame(main); bot.pack(fill="x", pady=(8, 0))
        ttk.Button(bot, text="🚀 渲染动画", style="Primary.TButton",
                   command=self._render).pack(side="left", padx=(0, 6))
        ttk.Button(bot, text="📋 导出代码", style="Export.TButton",
                   command=self._export).pack(side="left", padx=(0, 6))
        ttk.Button(bot, text="📂 打开", style="TButton",
                   command=self._open).pack(side="left", padx=(0, 6))
        ttk.Button(bot, text="💾 保存", style="TButton",
                   command=self._save).pack(side="left", padx=(0, 6))

        ttk.Label(bot, text="画质:").pack(side="left", padx=(14, 3))
        qc = ttk.Combobox(bot, textvariable=self.quality_var,
                          values=list(QMAP.keys()), state="readonly", width=12)
        qc.pack(side="left", padx=(0, 10))
        ttk.Label(bot, text="输出:").pack(side="left", padx=(8, 3))
        self.out_entry = ttk.Entry(bot, font=("Consolas", 9), width=18)
        self.out_entry.pack(side="left")
        self.out_entry.insert(0, str(Path("./outputs").resolve()))

        # Status
        sf = ttk.Frame(main); sf.pack(fill="x", pady=(6, 0))
        self.pbar = ttk.Progressbar(sf, variable=self.progress_var,
                                    mode="indeterminate", length=140)
        self.pbar.pack(side="left", padx=(0, 8))
        ttk.Label(sf, textvariable=self.status_var, style="Status.TLabel").pack(
            side="left", fill="x", expand=True)

    # ── Code ────────────────────────────────────────────────────────
    def _code(self): return self.editor.get("1.0", END).rstrip()
    def _set_code(self, code, save_hist=False):
        if save_hist and self._code():
            self._hist.append(self._code())
        self.editor.delete("1.0", END); self.editor.insert("1.0", code)
    def _undo(self):
        if self._hist:
            self._set_code(self._hist.pop()); self._add_log("↩ 已撤销")
        else: self._add_log("没有可撤销的修改")

    # ── AI ──────────────────────────────────────────────────────────
    def _quick(self, req):
        self.chat_in.delete(0, "end"); self.chat_in.insert(0, req); self._ai_modify()

    def _ai_modify(self):
        req = self.chat_in.get().strip()
        if not req: self._add_log("请输入修改要求"); return
        if not self.ai_ok.get():
            messagebox.showwarning("AI 不可用", "请设置 DEEPSEEK_API_KEY 环境变量"); return
        code = self._code()
        if not code.strip(): self._add_log("代码为空"); return

        self._add_log(f"🤖 {req}")
        self._busy(True); self.status_var.set("AI 正在修改代码...")

        self.chat_in.delete(0, "end")
        threading.Thread(target=self._ai_worker, args=(code, req), daemon=True).start()

    def _ai_worker(self, code, req):
        try:
            from formula2manim.ai_assistant.client import DeepSeekClient
            c = DeepSeekClient()
            new = c.modify_code(code, req)
            if new and len(new) > 50 and "manim" in new.lower():
                self.root.after(0, lambda: self._on_ai_ok(new, req))
            else:
                self.root.after(0, lambda: self._on_ai_fail("AI 返回代码无效", new))
        except DeepSeekAPIError as e:
            self.root.after(0, lambda: self._on_ai_fail(str(e), ""))
        except Exception as e:
            self.root.after(0, lambda: self._on_ai_fail(f"{e}", ""))

    def _on_ai_ok(self, code, req):
        self._busy(False); self._set_code(code, save_hist=True)
        self._add_log(f"✅ 修改完成"); self.status_var.set("代码已修改 — 点击渲染查看效果")
    def _on_ai_fail(self, err, raw):
        self._busy(False); self._add_log(f"❌ {err[:150]}")
        self.status_var.set("AI 修改失败"); messagebox.showerror("AI 失败", err[:500])

    # ── Render ──────────────────────────────────────────────────────
    def _render(self):
        code = self._code()
        if not code.strip(): self._add_log("代码为空"); return
        uid = uuid.uuid4().hex[:6]
        out = Path(self.out_entry.get().strip() or "./outputs")
        out.mkdir(parents=True, exist_ok=True)
        tmp = out / f"__live_{uid}.py"
        tmp.write_text(code, encoding="utf-8")
        # Read on main thread
        quality = self.quality_var.get()

        self._busy(True); self.status_var.set("正在渲染...")
        self._add_log(f"🚀 渲染 {tmp.name}")
        threading.Thread(target=self._render_worker,
                         args=(tmp, out, quality), daemon=True).start()

    def _render_worker(self, script, out, quality):
        try:
            q = QMAP.get(quality, "m")
            cmd = [sys.executable, "-m", "manim", "render", f"-q{q}",
                   "--media_dir", str(out.resolve()), str(script.resolve())]
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                               timeout=300, env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            all_out = (r.stdout or "") + (r.stderr or "")
            if r.returncode != 0:
                self.root.after(0, lambda: self._on_err(all_out[-2000:]))
                return
            mp4s = sorted(
                (p for p in out.rglob("*.mp4")
                 if p.stat().st_mtime >= time.time() - 10),
                key=lambda x: x.stat().st_mtime, reverse=True,
            )
            if mp4s:
                self.root.after(0, lambda: self._on_ok(str(mp4s[0])))
            else:
                self.root.after(0, lambda: self._on_err("未找到视频文件"))
        except subprocess.TimeoutExpired:
            self.root.after(0, lambda: self._on_err("渲染超时 (5分钟)"))
        except Exception as e:
            self.root.after(0, lambda: self._on_err(f"{e}"))

    def _on_ok(self, path):
        self._busy(False); self._add_log(f"✅ 渲染成功"); self.status_var.set("渲染成功！")
        if messagebox.askyesno("渲染成功", f"视频已生成:\n\n{path}\n\n是否播放？"):
            os.startfile(path)
    def _on_err(self, msg):
        self._busy(False); self._add_log(f"❌ 渲染失败"); self.status_var.set("渲染失败")
        messagebox.showerror("渲染失败", msg[:2000])

    # ── File I/O ────────────────────────────────────────────────────
    def _open(self):
        p = filedialog.askopenfilename(filetypes=[("Python", "*.py"), ("All", "*.*")])
        if p:
            self._set_code(Path(p).read_text(encoding="utf-8"))
            self._hist.clear(); self._add_log(f"📂 {p}")
    def _save(self):
        p = filedialog.asksaveasfilename(defaultextension=".py",
                                         filetypes=[("Python", "*.py")])
        if p:
            Path(p).write_text(self._code(), encoding="utf-8")
            self._add_log(f"💾 {p}"); self.status_var.set(f"已保存: {p}")
    def _export(self):
        p = filedialog.asksaveasfilename(defaultextension=".py",
                                         filetypes=[("Python", "*.py")])
        if p:
            Path(p).write_text(self._code(), encoding="utf-8")
            self._add_log(f"📋 已导出: {p}"); self.status_var.set(f"代码已导出")
            messagebox.showinfo("导出成功", f"源码已保存到:\n{p}")

    # ── Helpers ─────────────────────────────────────────────────────
    def _add_log(self, msg):
        self.log.configure(state="normal"); self.log.insert(END, msg + "\n")
        self.log.see(END); self.log.configure(state="disabled")
    def _busy(self, busy):
        s = "disabled" if busy else "normal"
        for w in [self.editor, self.chat_in, self.out_entry]:
            try: w.configure(state=s)
            except Exception: pass
        if busy:
            self.pbar.configure(mode="indeterminate"); self.pbar.start()
        else:
            self.pbar.stop(); self.pbar.configure(mode="determinate")


DEFAULT_CODE = '''\
"""Custom Manim scene."""
from manim import *

class MyScene(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-0.5, 4, 0.5],
            y_range=[-1, 12, 2],
            axis_config={"include_numbers": False},
            x_length=7, y_length=5.5, tips=True,
        )
        self.add(axes)
        self.add(Text("x", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25))
        self.add(Text("y", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25))

        curve = axes.plot(lambda x: x**2, color=BLUE, stroke_width=3)
        self.add(curve)

        t = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(t.get_value(), t.get_value()**2),
            color=RED, radius=0.08))
        self.add(dot)

        self.play(t.animate.set_value(3), run_time=4, rate_func=linear)
        self.wait(2)
'''


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("file", nargs="?")
    args = p.parse_args()
    code = Path(args.file).read_text(encoding="utf-8") if args.file and Path(args.file).exists() else ""
    root = Tk()
    LiveEditor(root, code)
    root.mainloop()

if __name__ == "__main__":
    main()

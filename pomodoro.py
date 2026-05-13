import tkinter as tk
from tkinter import ttk
import math
import platform

MODES = {
    "work":       {"label": "专注工作", "minutes": 25, "color": "#e74c3c"},
    "short_break": {"label": "短休息",   "minutes": 5,  "color": "#2ecc71"},
    "long_break":  {"label": "长休息",   "minutes": 15, "color": "#3498db"},
}

LONG_BREAK_INTERVAL = 4  # every 4 work sessions → long break


class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("番茄钟")
        self.geometry("380x480")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self.session_count = 0
        self.mode = "work"
        self.remaining = MODES["work"]["minutes"] * 60
        self.total = self.remaining
        self.running = False
        self.after_id = None

        self._build_ui()
        self._update_display()

    # ── build UI ──────────────────────────────────────────────

    def _build_ui(self):
        # Top frame: mode label + session counter
        top = tk.Frame(self, bg="#1e1e2e")
        top.pack(pady=(30, 5))

        self.mode_label = tk.Label(
            top, text="", font=("Microsoft YaHei", 16, "bold"),
            bg="#1e1e2e", fg="#e74c3c",
        )
        self.mode_label.pack()

        self.session_label = tk.Label(
            top, text="", font=("Microsoft YaHei", 10),
            bg="#1e1e2e", fg="#6c6c8a",
        )
        self.session_label.pack(pady=(4, 0))

        # Timer display
        self.timer_label = tk.Label(
            self, text="25:00", font=("Consolas", 52, "bold"),
            bg="#1e1e2e", fg="#cdd6f4",
        )
        self.timer_label.pack(pady=(10, 5))

        # Progress ring canvas
        self.canvas = tk.Canvas(
            self, width=200, height=200,
            bg="#1e1e2e", highlightthickness=0,
        )
        self.canvas.pack(pady=(0, 15))

        # Buttons
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack()

        self.start_btn = tk.Button(
            btn_frame, text="开始", font=("Microsoft YaHei", 11),
            width=8, bg="#a6e3a1", fg="#1e1e2e",
            activebackground="#94d89f", relief="flat", cursor="hand2",
            command=self.start,
        )
        self.start_btn.pack(side="left", padx=4)

        self.pause_btn = tk.Button(
            btn_frame, text="暂停", font=("Microsoft YaHei", 11),
            width=8, bg="#f9e2af", fg="#1e1e2e",
            activebackground="#f0d98a", relief="flat", cursor="hand2",
            command=self.pause,
        )
        self.pause_btn.pack(side="left", padx=4)

        self.reset_btn = tk.Button(
            btn_frame, text="重置", font=("Microsoft YaHei", 11),
            width=8, bg="#f38ba8", fg="#1e1e2e",
            activebackground="#e07a94", relief="flat", cursor="hand2",
            command=self.reset,
        )
        self.reset_btn.pack(side="left", padx=4)

        # Mode switch buttons
        mode_frame = tk.Frame(self, bg="#1e1e2e")
        mode_frame.pack(pady=(12, 5))

        self.work_btn = tk.Button(
            mode_frame, text="工作 25min", font=("Microsoft YaHei", 9),
            width=10, bg="#e74c3c", fg="#fff",
            activebackground="#c0392b", relief="flat", cursor="hand2",
            command=lambda: self.switch_mode("work"),
        )
        self.work_btn.pack(side="left", padx=3)

        self.short_btn = tk.Button(
            mode_frame, text="短休 5min", font=("Microsoft YaHei", 9),
            width=10, bg="#27ae60", fg="#fff",
            activebackground="#1e8449", relief="flat", cursor="hand2",
            command=lambda: self.switch_mode("short_break"),
        )
        self.short_btn.pack(side="left", padx=3)

        self.long_btn = tk.Button(
            mode_frame, text="长休 15min", font=("Microsoft YaHei", 9),
            width=10, bg="#2980b9", fg="#fff",
            activebackground="#1f618d", relief="flat", cursor="hand2",
            command=lambda: self.switch_mode("long_break"),
        )
        self.long_btn.pack(side="left", padx=3)

        # Always on top checkbox
        self.topmost_var = tk.BooleanVar(value=True)
        self.attributes("-topmost", True)
        topmost_cb = ttk.Checkbutton(
            self, text="窗口置顶", variable=self.topmost_var,
            command=self._toggle_topmost,
        )
        topmost_cb.pack(pady=(10, 5))

        # Style the checkbutton for dark theme
        style = ttk.Style(self)
        style.configure("TCheckbutton",
                         background="#1e1e2e", foreground="#cdd6f4",
                         font=("Microsoft YaHei", 9))

    # ── timer logic ───────────────────────────────────────────

    def start(self):
        if self.running:
            return
        self.running = True
        self._tick()

    def pause(self):
        self.running = False
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        self.pause()
        self.remaining = MODES[self.mode]["minutes"] * 60
        self.total = self.remaining
        self._update_display()

    def _tick(self):
        if not self.running:
            return
        if self.remaining <= 0:
            self._timer_finished()
            return
        self.remaining -= 1
        self._update_display()
        self.after_id = self.after(1000, self._tick)

    def _timer_finished(self):
        self.running = False
        self._play_sound()

        if self.mode == "work":
            self.session_count += 1
            if self.session_count % LONG_BREAK_INTERVAL == 0:
                self.switch_mode("long_break")
            else:
                self.switch_mode("short_break")
        else:
            self.switch_mode("work")

    # ── mode switching ────────────────────────────────────────

    def switch_mode(self, mode):
        self.pause()
        self.mode = mode
        self.remaining = MODES[mode]["minutes"] * 60
        self.total = self.remaining
        self._update_display()

    # ── display ───────────────────────────────────────────────

    def _update_display(self):
        color = MODES[self.mode]["color"]
        label = MODES[self.mode]["label"]

        self.mode_label.config(text=label, fg=color)
        self.timer_label.config(text=self._fmt_time(self.remaining))

        if self.mode == "work":
            self.session_label.config(
                text=f"Pomodoro #{self.session_count + 1}"
            )
        else:
            self.session_label.config(
                text=f"已完成 {self.session_count} 个番茄"
            )

        self._draw_progress(color)

    def _draw_progress(self, color):
        self.canvas.delete("all")
        cx, cy, r = 100, 100, 80
        w = 12

        # Background ring
        self.canvas.create_arc(
            cx - r, cy - r, cx + r, cy + r,
            start=90, extent=360,
            width=w, outline="#313244", style="arc",
        )

        # Foreground ring: extent proportional to remaining time
        fraction = self.remaining / self.total if self.total > 0 else 0
        extent = 360 * fraction

        if extent > 0:
            self.canvas.create_arc(
                cx - r, cy - r, cx + r, cy + r,
                start=90, extent=extent,
                width=w, outline=color, style="arc",
            )

        # Center text: remaining time
        self.canvas.create_text(
            cx, cy - 6, text=self._fmt_time(self.remaining),
            font=("Consolas", 22, "bold"), fill="#cdd6f4",
        )
        self.canvas.create_text(
            cx, cy + 22, text=MODES[self.mode]["label"],
            font=("Microsoft YaHei", 10), fill="#6c6c8a",
        )

    @staticmethod
    def _fmt_time(seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    # ── extras ────────────────────────────────────────────────

    def _toggle_topmost(self):
        self.attributes("-topmost", self.topmost_var.get())

    def _play_sound(self):
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except ImportError:
            self.bell()


if __name__ == "__main__":
    app = PomodoroApp()
    app.mainloop()

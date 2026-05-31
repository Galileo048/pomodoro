"""
N阶段运动 | 高中物理
支持任意数量的分段运动，每段可独立设置运动类型
"""
from manim import *
import numpy as np
import json


class NPhaseScene(Scene):
    def construct(self):
        # Parse phases from JSON
        phases_json = __PARAM_phases__
        phases = json.loads(phases_json) if isinstance(phases_json, str) else phases_json
        n_phases = len(phases)

        # Phase colors
        phase_colors = [BLUE, ORANGE, GREEN, RED, PURPLE, YELLOW, TEAL]
        colors = [phase_colors[i % len(phase_colors)] for i in range(n_phases)]

        # Compute trajectories for each phase
        all_trajectories = []
        x0, y0, vx0, vy0 = 0.0, 0.0, 0.0, 0.0

        for i, phase in enumerate(phases):
            t_start = phase["t_start"]
            t_end = phase["t_end"]
            t_arr = np.linspace(t_start, t_end, 50)
            dt = t_arr - t_start

            p = phase.get("params", {})
            motion_type = phase["type"]

            if motion_type == "linear":
                vx = p.get("vx", vx0)
                vy = p.get("vy", vy0)
                x = x0 + vx * dt
                y = y0 + vy * dt
                x_end, y_end = x[-1], y[-1]
                vx_end, vy_end = vx, vy

            elif motion_type == "projectile":
                vx = p.get("vx", vx0)
                vy = p.get("vy", vy0)
                g = p.get("g", 9.8)
                x = x0 + vx * dt
                y = y0 + vy * dt - 0.5 * g * dt**2
                x_end, y_end = x[-1], y[-1]
                vx_end, vy_end = vx, vy - g * (t_end - t_start)

            elif motion_type == "uniform_accel":
                vx = p.get("vx", vx0)
                vy = p.get("vy", vy0)
                ax = p.get("ax", 0)
                ay = p.get("ay", 0)
                x = x0 + vx * dt + 0.5 * ax * dt**2
                y = y0 + vy * dt + 0.5 * ay * dt**2
                x_end, y_end = x[-1], y[-1]
                vx_end, vy_end = vx + ax * dt[-1], vy + ay * dt[-1]

            elif motion_type == "circular":
                cx = p.get("cx", x0)
                cy = p.get("cy", y0)
                r = p.get("r", 2)
                omega = p.get("omega", 1.5)
                phase_offset = p.get("phase", 0)
                x = cx + r * np.cos(omega * dt + phase_offset)
                y = cy + r * np.sin(omega * dt + phase_offset)
                x_end, y_end = x[-1], y[-1]
                vx_end = -r * omega * np.sin(omega * dt[-1] + phase_offset)
                vy_end = r * omega * np.cos(omega * dt[-1] + phase_offset)

            elif motion_type == "harmonic":
                A = p.get("A", 1)
                omega = p.get("omega", 2)
                phi = p.get("phi", 0)
                axis = p.get("axis", "x")
                if axis == "x":
                    x = x0 + A * np.sin(omega * dt + phi)
                    y = np.full_like(t_arr, y0)
                    vx_end = A * omega * np.cos(omega * dt[-1] + phi)
                    vy_end = 0
                else:
                    x = np.full_like(t_arr, x0)
                    y = y0 + A * np.sin(omega * dt + phi)
                    vx_end = 0
                    vy_end = A * omega * np.cos(omega * dt[-1] + phi)
                x_end, y_end = x[-1], y[-1]

            elif motion_type == "damped_harmonic":
                A = p.get("A", 1)
                omega = p.get("omega", 2)
                gamma = p.get("gamma", 0.1)
                phi = p.get("phi", 0)
                x = x0 + A * np.exp(-gamma * dt) * np.cos(omega * dt + phi)
                y = np.full_like(t_arr, y0)
                x_end, y_end = x[-1], y[-1]
                vx_end = -A * np.exp(-gamma * dt[-1]) * (
                    gamma * np.cos(omega * dt[-1] + phi) +
                    omega * np.sin(omega * dt[-1] + phi)
                )
                vy_end = 0

            else:
                x = np.full_like(t_arr, x0)
                y = np.full_like(t_arr, y0)
                x_end, y_end = x0, y0
                vx_end, vy_end = vx0, vy0

            all_trajectories.append(np.column_stack([x, y]))
            x0, y0, vx0, vy0 = x_end, y_end, vx_end, vy_end

        # Combine all trajectories
        trajectory = np.vstack(all_trajectories)

        x_vals = trajectory[:, 0]
        y_vals = trajectory[:, 1]
        x_min, x_max = float(x_vals.min()), float(x_vals.max())
        y_min, y_max = float(y_vals.min()), float(y_vals.max())

        x_pad = max(1.0, (x_max - x_min) * 0.15)
        y_pad = max(1.0, (y_max - y_min) * 0.15)

        # Axes
        axes = Axes(
            x_range=[x_min - x_pad, x_max + x_pad, max(1, (x_max - x_min) / 8)],
            y_range=[y_min - y_pad, y_max + y_pad, max(1, (y_max - y_min) / 6)],
            axis_config={"include_numbers": False, "font_size": 24},
            x_length=7, y_length=5.5, tips=True,
        )
        x_l = Text("x (m)", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)
        y_l = Text("y (m)", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25)
        self.play(Create(axes), Write(x_l), Write(y_l), run_time=1.5)

        # Draw each phase trajectory
        start_idx = 0
        phase_labels = []
        for i, (phase, color) in enumerate(zip(phases, colors)):
            t_start = phase["t_start"]
            t_end = phase["t_end"]
            motion_type = phase["type"]
            n_pts = len(all_trajectories[i])
            end_idx = start_idx + n_pts

            # Create trajectory for this phase
            pts = [axes.c2p(float(x), float(y))
                   for x, y in trajectory[start_idx:end_idx]]
            traj = VMobject(color=color, stroke_width=3)
            traj.set_points_smoothly(pts)

            # Phase label
            lbl = Text(f"Phase {i+1}: {motion_type}", font_size=16, color=color)
            if i == 0:
                lbl.to_corner(UL, buff=0.3).shift(DOWN * 0.5)
            else:
                lbl.next_to(phase_labels[-1], DOWN, buff=0.1)
            phase_labels.append(lbl)

            self.play(Write(lbl), run_time=0.3)
            self.play(Create(traj), run_time=2)

            start_idx = end_idx

        # Transition markers
        idx = 0
        for i, phase in enumerate(phases[:-1], 1):
            idx += len(all_trajectories[i-1]) - 1
            t_val = phase["t_end"]
            dot = Dot(axes.c2p(float(trajectory[idx, 0]), float(trajectory[idx, 1])),
                      color=YELLOW, radius=0.08)
            lbl = Text(f"t={t_val:.1f}s", font_size=14, color=YELLOW)
            lbl.next_to(dot, UP, buff=0.1)
            self.play(FadeIn(dot), Write(lbl), run_time=0.3)

        # Moving dot
        t_tracker = ValueTracker(0)
        t_end = phases[-1]["t_end"]

        def get_pos():
            t = t_tracker.get_value()
            # Find which phase we're in
            for i, phase in enumerate(phases):
                if phase["t_start"] <= t <= phase["t_end"]:
                    dt = t - phase["t_start"]
                    phase_duration = phase["t_end"] - phase["t_start"]
                    if phase_duration > 0:
                        frac = dt / phase_duration
                    else:
                        frac = 0
                    # Interpolate within this phase
                    n_pts = len(all_trajectories[i])
                    idx = int(frac * (n_pts - 1))
                    idx = max(0, min(idx, n_pts - 1))
                    # Add offset for previous phases
                    offset = sum(len(all_trajectories[j]) for j in range(i))
                    pos_idx = offset + idx
                    return axes.c2p(float(trajectory[pos_idx, 0]),
                                    float(trajectory[pos_idx, 1]))
            # Default to last point
            return axes.c2p(float(trajectory[-1, 0]), float(trajectory[-1, 1]))

        dot = always_redraw(lambda: Dot(get_pos(), color=RED, radius=0.1))
        self.play(FadeIn(dot, scale=0.5), run_time=0.5)

        # Info panel
        panel = Rectangle(width=3.2, height=1.5, fill_color="#1a1a2e",
                          fill_opacity=0.85, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25).set_z_index(10)
        self.play(FadeIn(panel), run_time=0.4)

        # Animate
        self.wait(0.3)
        self.play(t_tracker.animate.set_value(t_end), run_time=10, rate_func=linear)
        self.wait(2)

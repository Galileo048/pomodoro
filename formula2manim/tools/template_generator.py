"""Template generator for Formula2Manim.

Generates high-quality Manim templates following manim_skill best practices.

Usage:
    python -m formula2manim.tools.template_generator \
        --name "Simple Harmonic Motion" \
        --category "物理" \
        --description "弹簧振子的简谐振动" \
        --params "amplitude=1.5; omega=2; cycles=3" \
        --scene-class "SHMScene"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Template for a basic Manim scene with axes and animated trajectory
SCENE_TEMPLATE = '''\
"""
{name} | {category}
{description}
"""
from manim import *
import numpy as np


class {scene_class}(Scene):
    def construct(self):
        # Parameters
{params_code}

        # Compute trajectory
        t_arr = np.linspace(0, t_max, 200)
        x_vals = np.array([x_func(t) for t in t_arr])
        y_vals = np.array([y_func(t) for t in t_arr])

        x_min, x_max = float(x_vals.min()), float(x_vals.max())
        y_min, y_max = float(y_vals.min()), float(y_vals.max())

        x_pad = max(1.0, (x_max - x_min) * 0.15)
        y_pad = max(1.0, (y_max - y_min) * 0.15)

        # Axes
        axes = Axes(
            x_range=[x_min - x_pad, x_max + x_pad, max(1, (x_max - x_min) / 8)],
            y_range=[y_min - y_pad, y_max + y_pad, max(1, (y_max - y_min) / 6)],
            axis_config={{"include_numbers": False, "font_size": 24}},
            x_length=7, y_length=5.5, tips=True,
        )
        x_l = Text("x (m)", font_size=24).next_to(axes.x_axis.get_end(), DOWN, buff=0.25)
        y_l = Text("y (m)", font_size=24).next_to(axes.y_axis.get_end(), LEFT, buff=0.25)
        self.play(Create(axes), Write(x_l), Write(y_l), run_time=1.5)

        # Trajectory
        traj = VMobject(color=YELLOW, stroke_width=3)
        pts = [axes.c2p(float(x), float(y)) for x, y in zip(x_vals, y_vals)]
        traj.set_points_smoothly(pts)

        # Moving dot
        t_tracker = ValueTracker(0)
        dot = always_redraw(lambda: Dot(
            axes.c2p(float(x_func(t_tracker.get_value())),
                     float(y_func(t_tracker.get_value()))),
            color=RED, radius=0.1))
        self.play(FadeIn(dot, scale=0.5), run_time=0.5)

        # Info panel
        panel = Rectangle(width=3.2, height=1.5, fill_color="#1a1a2e",
                          fill_opacity=0.85, stroke_color=GRAY, stroke_width=1)
        panel.to_corner(UR, buff=0.25).set_z_index(10)
        self.play(FadeIn(panel), run_time=0.4)

        # Animate
        self.wait(0.3)
        self.play(Create(traj), run_time=3, rate_func=smooth)
        self.play(t_tracker.animate.set_value(t_max), run_time=7, rate_func=linear)
        self.wait(2)
'''


def generate_params_code(params: dict[str, str]) -> str:
    """Generate Python code for parameter declarations."""
    lines = []
    for key, default in params.items():
        lines.append(f"        {key} = __PARAM_{key}__  # {default}")
    return "\n".join(lines)


def generate_template(
    name: str,
    category: str,
    description: str,
    scene_class: str,
    params: dict[str, str],
) -> str:
    """Generate a Manim template source code."""
    params_code = generate_params_code(params)

    return SCENE_TEMPLATE.format(
        name=name,
        category=category,
        description=description,
        scene_class=scene_class,
        params_code=params_code,
    )


def register_template(
    name: str,
    category: str,
    description: str,
    filename: str,
    scene_class: str,
    params: dict[str, dict],
) -> None:
    """Register a template in __init__.py."""
    init_path = Path(__file__).parent.parent / "templates" / "__init__.py"
    content = init_path.read_text(encoding="utf-8")

    # Build the new template entry
    params_str = ",\n            ".join(
        f'"{k}": {{"label": "{v["label"]}", "default": "{v["default"]}", "type": "{v["type"]}"}}'
        for k, v in params.items()
    )

    new_entry = f'''    {{
        "name": "{name}",
        "category": "{category}",
        "description": "{description}",
        "file": "{filename}",
        "scene_class": "{scene_class}",
        "params": {{
            {params_str}
        }},
    }},'''

    # Find the insertion point (before the closing bracket of TEMPLATES list)
    # Look for the last template entry and insert after it
    insert_marker = "]\n\n\ndef get_template_dir"
    if insert_marker in content:
        content = content.replace(insert_marker, f"\n{new_entry}\n{insert_marker}")
        init_path.write_text(content, encoding="utf-8")
        print(f"Registered template '{name}' in {init_path}")
    else:
        print(f"Warning: Could not find insertion point in {init_path}")
        print("Please manually add the template entry.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Formula2Manim templates"
    )
    parser.add_argument("--name", required=True, help="Template name (Chinese)")
    parser.add_argument("--category", required=True, choices=["物理", "数学"],
                        help="Category")
    parser.add_argument("--description", required=True, help="One-line description")
    parser.add_argument("--scene-class", required=True, help="Manim Scene class name")
    parser.add_argument("--params", required=True,
                        help="Parameters as key=default;... pairs")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory (default: templates/)")
    parser.add_argument("--register", action="store_true",
                        help="Register in __init__.py")

    args = parser.parse_args()

    # Parse params
    params = {}
    for part in args.params.split(";"):
        part = part.strip()
        if "=" in part:
            key, default = part.split("=", 1)
            params[key.strip()] = {
                "label": key.strip(),
                "default": default.strip(),
                "type": "float",
            }

    # Generate filename
    safe_name = re.sub(r'[^\w]', '_', args.name.replace(" ", "_"))
    filename = f"{safe_name.lower()}.py"

    # Generate template
    source = generate_template(
        name=args.name,
        category=args.category,
        description=args.description,
        scene_class=args.scene_class,
        params={k: v["default"] for k, v in params.items()},
    )

    # Write template file
    output_dir = Path(args.output_dir) if args.output_dir else (
        Path(__file__).parent.parent / "templates"
    )
    output_path = output_dir / filename
    output_path.write_text(source, encoding="utf-8")
    print(f"Generated template: {output_path}")

    # Register if requested
    if args.register:
        register_template(
            name=args.name,
            category=args.category,
            description=args.description,
            filename=filename,
            scene_class=args.scene_class,
            params=params,
        )

    print(f"\nTemplate '{args.name}' created successfully!")
    print(f"File: {output_path}")
    if args.register:
        print("Registered in __init__.py")


if __name__ == "__main__":
    main()

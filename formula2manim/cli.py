"""CLI entry point for Formula2Manim."""

from __future__ import annotations

import argparse
import sys
import os
from pathlib import Path
from typing import Any

# Fix Windows console encoding for Rich
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from formula2manim import __version__
from formula2manim.config import (
    DEFAULT_FPS,
    DEFAULT_NUM_POINTS,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_QUALITY,
    DEFAULT_T_MAX,
    DEFAULT_T_MIN,
)
from formula2manim.exceptions import (
    DeepSeekAPIError,
    Formula2ManimError,
    ParseError,
    RenderingError,
)
from formula2manim.manim_scenes.scene_builder import build_and_render
from formula2manim.parser.formula_parser import parse_formulas
from formula2manim.parser.param_parser import parse_params
from formula2manim.physics_models.registry import MODEL_REGISTRY, detect_model

console = Console()


def _parse_t_range(raw: str) -> tuple[float, float]:
    """Parse a 'min,max' string into a (float, float) tuple."""
    parts = raw.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            "Time range must be 'min,max' (e.g. '0,5')."
        )
    try:
        t_min = float(parts[0].strip())
        t_max = float(parts[1].strip())
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid numeric values in time range: {raw!r}"
        )
    if t_min >= t_max:
        raise argparse.ArgumentTypeError(
            f"t_min ({t_min}) must be less than t_max ({t_max})."
        )
    return (t_min, t_max)


def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="f2m",
        description=(
            "Formula2Manim — Generate Manim animations from physics/math "
            "formulas with optional DeepSeek AI assistance."
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"formula2manim {__version__}"
    )

    input_group = parser.add_argument_group("Input (choose one)")
    input_group.add_argument(
        "-f", "--formulas",
        type=str,
        help="Formula string (semicolon-separated), e.g. 'x = v0*t + 0.5*a*t**2'",
    )
    input_group.add_argument(
        "--describe",
        type=str,
        help="Natural language description of the physics scenario (requires --ai).",
    )

    parser.add_argument(
        "-p", "--params",
        type=str,
        default="",
        help="Parameter string, e.g. 'v0=0, a=9.8'",
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        choices=list(MODEL_REGISTRY.keys()),
        help="Physics model to use. Auto-detected if not specified.",
    )
    parser.add_argument(
        "--t-range",
        type=_parse_t_range,
        default=f"{DEFAULT_T_MIN},{DEFAULT_T_MAX}",
        help="Time range as 'min,max' (default: '%(default)s').",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory (default: '%(default)s').",
    )
    parser.add_argument(
        "--quality",
        type=str,
        choices=["l", "m", "h", "p", "k"],
        default=DEFAULT_QUALITY,
        help="Video quality: l=480p15, m=720p30, h=1080p60 (default: '%(default)s').",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=DEFAULT_FPS,
        help="Frames per second (default: %(default)s).",
    )
    parser.add_argument(
        "--num-points",
        type=int,
        default=DEFAULT_NUM_POINTS,
        help="Number of trajectory sample points (default: %(default)s).",
    )

    ai_group = parser.add_argument_group("AI Assistance (DeepSeek)")
    ai_group.add_argument(
        "--ai",
        action="store_true",
        help="Enable AI-assisted enhancements (model suggestion, scene styling).",
    )
    ai_group.add_argument(
        "--ai-model",
        type=str,
        default=None,
        help="DeepSeek model name (default: deepseek-chat).",
    )
    ai_group.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="DeepSeek API key (or set DEEPSEEK_API_KEY env var).",
    )

    debug_group = parser.add_argument_group("Debug")
    debug_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and validate only, do not render.",
    )
    debug_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output.",
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    """Main CLI entry point."""
    parser = build_argparser()
    args = parser.parse_args(argv)

    # --- Input validation ---
    if args.describe and not args.ai:
        console.print(
            "[red]Error:[/] --describe requires --ai flag to be set.\n"
            "Use: f2m --describe '...' --ai --api-key YOUR_KEY"
        )
        sys.exit(1)

    if not args.formulas and not args.describe:
        console.print(
            "[red]Error:[/] Either --formulas or --describe is required."
        )
        sys.exit(1)

    if args.formulas and args.describe:
        console.print(
            "[red]Error:[/] Use either --formulas or --describe, not both."
        )
        sys.exit(1)

    try:
        # --- AI: Natural language → formula ---
        if args.describe:
            from formula2manim.ai_assistant.client import DeepSeekClient

            console.print("[cyan]Asking DeepSeek to generate formula...[/]")
            ai = DeepSeekClient(
                api_key=args.api_key,
                model=args.ai_model or "deepseek-chat",
            )
            result = ai.generate_formula(args.describe)

            formulas_str = result["formulas"]
            params_str = result.get("params", args.params)
            explanation = result.get("explanation", "")
            suggested_t = result.get("suggested_t_range", "")

            console.print(
                Panel.fit(
                    f"[bold]Formulas:[/] {formulas_str}\n"
                    f"[bold]Params:[/]   {params_str}",
                    title="AI Generated",
                    border_style="green",
                )
            )
            if explanation:
                console.print(f"[dim]{explanation}[/]")

            # Use AI-suggested t_range if user didn't override
            if suggested_t and args.t_range == (DEFAULT_T_MIN, DEFAULT_T_MAX):
                try:
                    args.t_range = _parse_t_range(suggested_t)
                    if args.verbose:
                        console.print(
                            f"[dim]Using AI-suggested time range: {args.t_range}[/]"
                        )
                except argparse.ArgumentTypeError:
                    pass
        else:
            formulas_str = args.formulas
            params_str = args.params

        # --- Parse formulas and params ---
        console.print("[cyan]Parsing formulas and parameters...[/]")
        formulas = parse_formulas(formulas_str)
        params = parse_params(params_str)

        if args.verbose:
            console.print(f"[dim]Variables: {list(formulas.keys())}[/]")
            console.print(f"[dim]Parameters: {list(params.keys())}[/]")

        # --- Determine model ---
        ai_client = None
        model_name = args.model

        if model_name is None:
            # Always use deterministic detection first
            model_name = detect_model(formulas, params)
            if args.verbose:
                console.print(f"[dim]Auto-detected model: {model_name}[/]")

            # AI can override for ambiguous cases (but not n_phase/multi_phase)
            if args.ai and model_name not in ("n_phase", "multi_phase"):
                from formula2manim.ai_assistant.client import DeepSeekClient

                console.print("[cyan]Asking AI to suggest a model...[/]")
                ai_client = DeepSeekClient(
                    api_key=args.api_key,
                    model=args.ai_model or "deepseek-chat",
                )
                suggestion = ai_client.suggest_model(formulas, params)
                model_name = suggestion.get("model", model_name)
                confidence = suggestion.get("confidence", 0)
                reasoning = suggestion.get("reasoning", "")
                console.print(
                    f"[green]AI suggests:[/] {model_name} "
                    f"(confidence: {confidence:.0%})"
                )
                if args.verbose and reasoning:
                    console.print(f"[dim]{reasoning}[/]")

        if model_name not in MODEL_REGISTRY:
            console.print(
                f"[red]Error:[/] Unknown model '{model_name}'. "
                f"Available: {list(MODEL_REGISTRY.keys())}"
            )
            sys.exit(1)

        model_cls = MODEL_REGISTRY[model_name]
        console.print(f"[green]Using model:[/] {model_cls.__name__}")

        # --- Instantiate model ---
        console.print("[cyan]Validating model...[/]")
        try:
            model = model_cls(formulas, params)
        except Formula2ManimError as e:
            console.print(f"[red]Model validation error:[/] {e}")
            sys.exit(1)

        # --- Compute trajectory ---
        console.print("[cyan]Computing trajectory...[/]")
        trajectory = model.compute_trajectory(args.t_range, args.num_points)

        x_vals = trajectory[:, 0]
        y_vals = trajectory[:, 1]

        if args.verbose:
            table = Table(title="Trajectory Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Points", str(len(trajectory)))
            table.add_row("X range", f"[{x_vals.min():.3g}, {x_vals.max():.3g}]")
            table.add_row("Y range", f"[{y_vals.min():.3g}, {y_vals.max():.3g}]")
            table.add_row(
                "Duration", f"{args.t_range[1] - args.t_range[0]:.3g} s"
            )
            console.print(table)

        # --- AI Enhancements ---
        enhancements: dict[str, Any] = {}
        if args.ai:
            from formula2manim.ai_assistant.client import DeepSeekClient

            if ai_client is None:
                ai_client = DeepSeekClient(
                    api_key=args.api_key,
                    model=args.ai_model or "deepseek-chat",
                )

            console.print("[cyan]Asking AI for visual enhancements...[/]")
            try:
                model_info = {
                    "type": model_name,
                    "variables": list(formulas.keys()),
                    "parameters": params,
                    "formulas": {k: str(v) for k, v in formulas.items()},
                    "x_range": [float(x_vals.min()), float(x_vals.max())],
                    "y_range": [float(y_vals.min()), float(y_vals.max())],
                    "duration": args.t_range[1] - args.t_range[0],
                }
                enhancements = ai_client.enhance_scene(model_info)
                if args.verbose:
                    console.print(f"[dim]Enhancements: {enhancements}[/]")
            except DeepSeekAPIError as e:
                console.print(f"[yellow]AI enhancement failed:[/] {e}")

        # --- Dry run ---
        if args.dry_run:
            console.print()
            console.print(
                Panel.fit(
                    f"[bold]Model:[/] {model_cls.__name__}\n"
                    f"[bold]Formulas:[/] {formulas_str}\n"
                    f"[bold]Params:[/] {params_str}\n"
                    f"[bold]Time range:[/] {args.t_range}\n"
                    f"[bold]Points:[/] {args.num_points}\n"
                    f"[bold]LaTeX:[/] {model.get_latex_label()}",
                    title="Dry Run — Validation Passed",
                    border_style="green",
                )
            )
            return

        # --- Render ---
        console.print("[cyan]Rendering animation with Manim...[/]")
        console.print("[dim]This may take a minute or two...[/]")

        # Get axis labels from model
        x_label, y_label = "x", "y"
        if hasattr(model, "get_axis_labels"):
            x_label, y_label = model.get_axis_labels()  # type: ignore[misc]

        try:
            video_path = build_and_render(
                trajectory=trajectory,
                t_range=args.t_range,
                latex_label=model.get_latex_label(),
                params=params,
                x_label=x_label,
                y_label=y_label,
                output_dir=args.output,
                fps=args.fps,
                quality=args.quality,
                enhancements=enhancements,
            )
        except RenderingError as e:
            console.print(f"[red]Rendering failed:[/] {e}")

            # Try AI diagnosis
            if args.ai and ai_client is not None:
                console.print("[cyan]Asking AI to diagnose the error...[/]")
                try:
                    diagnosis = ai_client.diagnose_error(
                        str(e), str(formulas_str), str(params_str)
                    )
                    console.print(
                        Panel.fit(
                            f"[bold]Diagnosis:[/] {diagnosis.get('diagnosis', '?')}\n"
                            f"[bold]Suggestion:[/] {diagnosis.get('suggestion', '?')}",
                            title="AI Error Diagnosis",
                            border_style="yellow",
                        )
                    )
                except DeepSeekAPIError:
                    pass
            sys.exit(1)

        console.print()
        console.print(
            Panel.fit(
                f"[bold]Video:[/] {video_path}\n"
                f"[bold]Model:[/] {model_cls.__name__}\n"
                f"[bold]Duration:[/] {args.t_range[1] - args.t_range[0]:.1f}s",
                title="[green]Animation Rendered Successfully",
                border_style="green",
            )
        )

    except Formula2ManimError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user.[/]")
        sys.exit(130)


if __name__ == "__main__":
    main()

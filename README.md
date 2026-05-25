# Formula2Manim

Generate Manim animations from physics/math formulas with optional DeepSeek AI assistance.

## Features

- Parse physics formulas (SymPy) and parameter values
- Auto-detect physics model (uniform acceleration, projectile motion)
- Generate Manim animations with dynamic axes, moving dots, and trajectory curves
- **DeepSeek AI integration**: describe a scenario in natural language and get a rendered animation
- AI-suggested visual enhancements (colors, annotations, camera settings)
- AI-powered error diagnosis for rendering failures

## Installation

```bash
# Clone the repo
cd formula2manim

# Install dependencies
pip install -r requirements.txt
```

Alternatively, install as a package:

```bash
pip install -e .
```

This registers the `f2m` command globally.

## Dependencies

- Python 3.10+
- Manim Community 0.18+
- SymPy, NumPy, Rich, python-dotenv
- OpenAI SDK (for DeepSeek API, optional)

## Quick Start

### Basic usage (no AI)

Uniform acceleration — a car starting from rest at 3 m/s²:

```bash
f2m -f "x = v0*t + 0.5*a*t**2" -p "v0=0, a=3" --t-range "0,10"
```

Projectile motion — a ball thrown at 10 m/s horizontally:

```bash
f2m -f "x = v0x*t; y = v0y*t - 0.5*g*t**2" -p "v0x=10, v0y=0, g=9.8" --t-range "0,2.04"
```

### AI-assisted (natural language)

Set your DeepSeek API key first:

```bash
export DEEPSEEK_API_KEY=sk-your-key-here
```

Then describe a scenario:

```bash
f2m --describe "A ball is thrown at 20 m/s at a 45-degree angle" --ai
```

The AI will:
1. Generate the formulas and parameters
2. Select the appropriate physics model
3. Suggest visual enhancements (colors, annotations)
4. Render the animation

### Quality options

| Flag | Resolution | FPS |
|------|-----------|-----|
| `-ql` | 480p | 15 |
| `-qm` | 720p | 30 (default) |
| `-qh` | 1080p | 60 |
| `-qp` | 1440p | 60 |
| `-qk` | 2160p | 60 |

```bash
f2m -f "x = v0*t + 0.5*a*t**2" -p "v0=0, a=9.8" --quality h
```

### Validation only (no rendering)

```bash
f2m -f "x = v0x*t; y = v0y*t - 0.5*g*t**2" -p "v0x=10, v0y=20, g=9.8" --dry-run -v
```

## CLI Reference

```
f2m [OPTIONS]

Input (choose one):
  -f, --formulas TEXT    Formula string (semicolon-separated)
  --describe TEXT         Natural language description (requires --ai)

Options:
  -p, --params TEXT       Parameters: "v0=0, a=9.8"
  -m, --model CHOICE      Model: uniform_acceleration | projectile_motion
  --t-range TEXT           Time range: "min,max" (default: "0,5")
  -o, --output PATH       Output directory (default: ./outputs)
  --quality CHAR           l|m|h|p|k (default: m)
  --fps INT               Frames per second (default: 30)

AI:
  --ai                    Enable AI-assisted features
  --ai-model TEXT         Model name (default: deepseek-chat)
  --api-key TEXT          DeepSeek API key

Debug:
  --dry-run               Validate only, don't render
  -v, --verbose           Verbose output
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `DEEPSEEK_API_KEY` | DeepSeek API key | (required for --ai) |
| `F2M_OUTPUT_DIR` | Default output directory | `./outputs` |
| `F2M_QUALITY` | Default video quality | `m` |
| `F2M_FPS` | Default FPS | `30` |
| `F2M_AI_MODEL` | Default AI model | `deepseek-chat` |

## Project Structure

```
formula2manim/
├── parser/
│   ├── formula_parser.py    # SymPy formula parsing
│   └── param_parser.py      # Parameter string parsing
├── physics_models/
│   ├── base.py              # Abstract PhysicsModel class
│   ├── kinematics.py        # UniformAcceleration, ProjectileMotion
│   └── registry.py          # Model registry + auto-detection
├── manim_scenes/
│   └── scene_builder.py     # Dynamic Manim scene generation
├── ai_assistant/
│   ├── client.py            # DeepSeek API client
│   └── prompts.py           # System prompts for AI tasks
├── cli.py                   # CLI entry point (argparse + rich)
├── config.py                # Configuration and env vars
└── exceptions.py            # Custom exception hierarchy
```

## Running Tests

```bash
pytest tests/ -v
```

## License

MIT

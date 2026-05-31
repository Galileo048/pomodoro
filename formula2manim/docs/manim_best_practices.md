# Manim Community Edition — Best Practices Reference

> Source: adithya-s-k/manim_skill (manimce-best-practices)

## Scene Structure

```python
from manim import *

class MyScene(Scene):
    def setup(self):
        self.camera.background_color = "#1a1a2e"  # optional

    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait(1)
```

- `setup()` runs before `construct()` — use for initialization
- `self.add()` = instant (no animation), `self.play()` = animated
- Scene types: `Scene` (2D), `ThreeDScene` (3D), `MovingCameraScene` (zoom/pan)

## Animations

### .animate syntax (preferred)
```python
self.play(square.animate.shift(RIGHT))
self.play(circle.animate.scale(2).set_color(RED))
```

### Common animation classes
```python
Create(mobj)              # Draw progressively
Write(text)               # Write text/equations
FadeIn(mobj) / FadeOut()  # Fade
Transform(a, b)           # Morph a into b
ReplacementTransform(a,b) # Replace a with b
MoveAlongPath(dot, path)  # Move along path
GrowArrow(arrow)          # Grow arrow
```

### Timing
```python
self.play(Create(c), run_time=2)           # duration
self.play(c.animate.shift(RIGHT), rate_func=smooth)  # easing
```

Rate functions: `smooth` (default, natural), `linear` (constant), `there_and_back`, `rush_into`, `rush_from`, `ease_out_bounce`

### Simultaneous vs Sequential
```python
self.play(Create(c), FadeIn(s))           # simultaneous
self.play(Create(c)); self.play(FadeIn(s)) # sequential
```

## LaTeX / MathTex

```python
eq = MathTex(r"E = mc^2", font_size=48)
eq2 = MathTex(r"\frac{a}{b}", color=BLUE)
eq3 = MathTex(r"\int_0^\infty e^{-x} dx")

# Color parts
eq.set_color_by_tex("E", RED)

# Split for animation control
eq = MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2")
eq[0].set_color(RED)  # 'a'
```

- Always use raw strings `r"..."`
- `MathTex` = auto math mode, `Tex` = raw LaTeX
- Use `substrings_to_isolate` for reliable coloring

## Axes & Graphing

```python
axes = Axes(
    x_range=[-5, 5, 1],
    y_range=[-3, 3, 1],
    x_length=10, y_length=6,
    axis_config={"include_numbers": True, "font_size": 24},
    tips=False,
)
x_label = axes.get_x_axis_label("x")
y_label = axes.get_y_axis_label("y")

# Plot function
curve = axes.plot(lambda x: x**2, color=BLUE)

# Plot parametric
traj = axes.plot_parametric_curve(
    lambda t: np.array([x(t), y(t)]),
    t_range=[0, 5], color=RED
)

# Coordinate conversion
point = axes.c2p(2, 1)   # math coords -> screen coords
coords = axes.p2c(point)  # screen -> math coords
```

## Colors

```python
# Named colors
RED, GREEN, BLUE, YELLOW, ORANGE, PINK, PURPLE, WHITE, BLACK, GREY

# Shades (A=lightest to E=darkest)
BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_E

# Hex
Circle(color="#FF5733")

# Fill + stroke
square.set_fill(RED, opacity=0.5)
square.set_stroke(BLUE, width=4)

# Gradient
text.set_color_by_gradient(RED, YELLOW, GREEN)
```

## Text

```python
text = Text("Hello", font_size=36, color=WHITE)
text = Text("中文", font="Microsoft YaHei")
math_label = MathTex(r"x^2", font_size=24)
```

## Positioning

```python
obj.move_to(ORIGIN)
obj.next_to(other, RIGHT, buff=0.3)
obj.to_corner(UR, buff=0.2)
obj.shift(UP * 2 + RIGHT)
obj.align_to(other, LEFT)
```

## Groups

```python
group = VGroup(obj1, obj2, obj3)
group.arrange(RIGHT, buff=0.5)
group.arrange_in_grid(rows=2)
group.center()
```

## Updaters & ValueTracker

```python
t = ValueTracker(0)
dot = always_redraw(lambda: Dot(
    axes.c2p(t.get_value(), f(t.get_value())),
    color=RED
))
self.play(t.animate.set_value(5), run_time=4)
```

## CLI Rendering

```bash
manim -pql scene.py SceneName    # low quality, preview
manim -pqh scene.py SceneName    # high quality
manim --format gif scene.py      # GIF output
python -m manim render -qm scene.py SceneName
```

Quality flags: `-ql` (480p15), `-qm` (720p30), `-qh` (1080p60), `-qk` (2160p60)

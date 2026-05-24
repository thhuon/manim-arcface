# ManimGL ArcFace Animation Project — Coding Rules

This skill file defines all rules for the ManimGL ArcFace educational animation project.

---

## Project Overview

| Item | Value |
|------|-------|
| **Framework** | ManimGL (3b1b version) |
| **Style** | 3Blue1Brown — cinematic, geometric, intuition-first |
| **Output** | `.mp4` via ffmpeg, 1920×1080 (1080p), 60fps |
| **Audience** | Undergrad CS students with basic ML knowledge |

---

## CRITICAL: Graphical & Aesthetic Guidelines


## IMPORTANT: No Manual Shape Primitives for Complex Objects

> **DO NOT** manually code complex realistic objects (smartphones, laptops, lock icons) using native Manim shapes (arcs, polygons, rectangles). Instead, **STRICTLY** combine external SVG assets with native Manim mathematical components.

### Background

```python
# Use dark grey background - NOT pure black
self.camera.background_color = "#1C1C1C"  # Dark grey
# Alternative: "#111111" for very dark
```

### Color Palette (Minimalist Premium Theme)

```python
# Neutral objects
WHITE = "#FFFFFF"

# Secondary elements
GREY = "#888888"
DARK_GREY = "#444444"

# Data elements - Vibrant but clean Pastel/Neon tones
CYAN = "#00FFFF"
TEAL = "#008080"
GOLD = "#FFD700"

# Additional accent colors
ACCENT_BLUE = "#4fc3f7"  # Sky blue
```

### Line Weight (Technical Blueprint Appearance)

```python
# Keep stroke_width THIN and SHARP
# Ideal range: 1.5 to 2.5
# AVOID thick, cartoonish outlines

# For outlines
stroke_width = 1.5  # Thin technical lines
stroke_width = 2.0  # Standard thin
stroke_width = 2.5  # Maximum for emphasis
```

### Fill Opacity

```python
# Objects should primarily be OUTLINES
fill_opacity = 0

# If shading is required, keep HIGHLY TRANSPARENT
fill_opacity = 0.05   # Very subtle
fill_opacity = 0.1    # Barely visible
```

---

## Scene Asset Specification & Composition

### External SVG Elements

```python
# Import CLEAN, MINIMALIST OUTLINE icons for:
# - Laptop
# - Smartphone
# - Secure padlock

# Store SVG files in scenes/decorations/
laptop_icon = SVGMobject("scenes/decorations/laptop.svg")
phone_icon = SVGMobject("scenes/decorations/phone.svg")
lock_icon = SVGMobject("scenes/decorations/lock.svg")
```

### Arrangement

```python
# Group devices in VGroup
devices = VGroup(laptop_icon, phone_icon)
devices.arrange(RIGHT, buff=2)
devices.center()

# Place lock on device screen
lock_icon.move_to(phone_icon.get_center())
```

### Native Manim Elements (Mathematical Layer)

```python
# Background data streams - matrix layout or binary streams
# Use MathTex with dark grey color and reduced opacity
data_stream = MathTex("0 1 0 1 1 0", color="#444444", opacity=0.3)

# Glowing scanning bar/beam - thin line with neon color
scan_bar = Line(start, end, stroke_color=CYAN, stroke_width=1.5)
```

---

## Animation & Camera Directives

### Step 1: SVG Rendering

```python
# Use Create() or Write() for elegant vector path tracing
self.play(Create(svg_object), run_time=2.5)
self.play(Write(svg_object), run_time=2.5)
```

### Step 2: 2D to 3D Morph/Transition

```python
# MUST use ReplacementTransform to clean memory space
self.play(
    ReplacementTransform(svg_objects, wireframe_3d),
    run_time=2
)
```

### Step 3: Camera Motion (3D Scenes)

```python
# Use MovingCameraScene or ThreeDScene for 3D camera hooks
class MyScene(ThreeDScene):
    def construct(self):
        # Smooth camera frame movement
        self.play(
            self.frame.animate.move_to(target_position),
            run_time=2,
            rate_func=smooth
        )

        # Zoom in
        self.play(
            self.frame.animate.scale(0.8),
            run_time=1.5
        )

        # Orbital rotation around Y-axis
        self.play(
            self.frame.animate.reorient(theta_degrees=30),
            run_time=3
        )

        # Continuous ambient rotation
        self.frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
```

### Pacing Rules

```python
# Camera transitions
rate_func=smooth

# Continuous processes (data streaming)
rate_func=linear

# All major animations
run_time=2-3
```

---

## Typography

```python
# For equations and LaTeX
title = Tex(r"\text{Your Text}", font_size=72, color=WHITE)

# For descriptions - use Consolas font
code_text = Text("description", font="Consolas", font_size=24)

# Font size reference (144pt = 1 manim unit height)
EQUATION_SIZE = 72
DESCRIPTION_SIZE = 24
TITLE_SIZE = 72
SUBTITLE_SIZE = 32
```

---

## Animation Patterns

### Smooth Transforms
```python
FadeTransform(source, target)
ReplacementTransform(source, target)  # Preferred for clean transitions
TransformMatchingShapes(source, target, path_arc=PI/2)
Create(mobject)                       # SVG/vector path tracing
Write(mobject)                        # Text writing
```

### Grid and Plane Reveals
```python
grid = NumberPlane((-10, 10), (-5, 5))
grid.set_stroke(GREY, 1.5)  # Thin lines
grid.add_coordinate_labels(font_size=24)
self.play(Create(grid))  # Use Create instead of ShowCreation
```

### Matrix/Transform Animations
```python
self.play(grid.animate.apply_matrix(matrix), run_time=3, rate_func=smooth)
```

### Color Gradients
```python
grid.set_submobject_colors_by_gradient(CYAN, TEAL, GOLD)
```

### Dynamic Values and Updaters
```python
ValueTracker() + always_redraw()
self.play(x_tracker.animate.set_value(new_val))
```

### Clustered Animations
```python
AnimationGroup()
LaggedStart()           # Stagger animations
LaggedStartMap()        # Map animation to group
```

### Text Animations
```python
Write(text)              # Write appearance
FadeIn(text, UP)        # Fade in from direction
FadeOut(text, shift=DOWN)
```

### Geometric Reveals
```python
Create()         # Vector path creation (preferred)
ShowCreation()   # Legacy creation
GrowArrow()
MoveAlongPath()
Rotate()
```

---

## Visual Style Rules

### 3B1B Visual Principles
1. **Minimal Text** — Explain through geometry, not words
2. **Clean Backgrounds** — Dark backgrounds make colors pop
3. **Slow Reveals** — Let viewers absorb each concept
4. **Smooth Camera** — Use `run_time=3-6` for major movements
5. **Backstroke** — Add subtle outlines for readability (if needed on complex backgrounds)

### Arranging and Positioning
```python
group.arrange(RIGHT)
group.to_edge(UP)
vgroup.arrange(DOWN, buff=0.8)
```

---

## Transitions

### Between Scenes
```python
# 1-second fade to black → fade in new scene
self.wait(0.5)
self.play(FadeOut(VGroup(objects...)))
self.play(FadeIn(new_objects...))
```

### Camera Reset
```python
self.frame.animate.move_to(ORIGIN)
self.frame.reorient(phi_degrees=70, theta_degrees=-45)
```

---

## 3D Scene Guidelines

### When to Use ThreeDScene
- Scene 7: Evolution (timeline with 3D elements)
- Scene 8: ArcFace Core (hypersphere visualization)
- Any scene requiring sphere/unit circle visualizations

### Sphere and Surface
```python
# Wireframe sphere
sphere = Sphere(radius=1.5, resolution=(12, 24))
sphere_mesh = SurfaceMesh(sphere, stroke_color=CYAN, stroke_opacity=0.6)
sphere_mesh.set_stroke(width=1.5)  # Thin lines

# Glowing dots on surface
point_cloud = GlowDots(
    points=np.array(points_list),
    radius=0.08,
    glow_factor=2.0,
    color=CYAN
)
```

### 3D Face Wireframe (from scene00)
```python
sphere = Sphere(radius=1.5, resolution=(12, 24))
sphere_mesh = SurfaceMesh(sphere, stroke_color="#4fc3f7", stroke_opacity=0.6)
sphere_mesh.set_stroke(width=1.5)

# Glowing points with thin lines
point_cloud = GlowDots(
    points=np.array(points),
    radius=0.08,
    glow_factor=2.0,
    color="#4fc3f7"
)
```

---

## File Structure

```
manim-arcface-2/
├── requirements.txt
├── example_scenes.py          # Reference examples
├── main.py                    # Scene order, config, render
├── videos/                    # Output directory
├── manimlib/                  # ManimGL core library
└── scenes/
    ├── __init__.py
    ├── decorations/           # SVG assets
    │   ├── laptop.svg
    │   ├── phone.svg
    │   ├── lock.svg
    │   └── 3b1b_accent.svg
    ├── scene00_introduction.py
    ├── scene01_hook.py
    ├── scene02_pipeline.py
    └── ...
```

---

## Render Commands

```bash
# Preview (with preview window)
manimgl main.py SceneName -s

# Write to video file
LD_LIBRARY_PATH=/home/aster/.local/lib:$LD_LIBRARY_PATH manimgl main.py SceneName -w

# Write and open after render
manimgl main.py SceneName -w -o
```

---

## Common Patterns

### GlowDots Creation
```python
import numpy as np
np.random.seed(42)  # For reproducibility
n_points = 30
points_on_sphere = []

for _ in range(n_points):
    theta = np.random.uniform(0, 2 * PI)
    phi = np.random.uniform(0, PI)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.cos(phi)
    z = radius * np.sin(phi) * np.sin(theta)
    points_on_sphere.append([x, y, z])

point_cloud = GlowDots(
    points=np.array(points_on_sphere),
    radius=0.08,
    glow_factor=2.0,
    color=CYAN
)
```

### Object Converging Animation
```python
self.play(
    stream_cloud.animate.move_to([5, 0, 0]),
    run_time=2,
    rate_func=smooth
)
```

---

## Scene Flow Constants

| Transition | Duration |
|------------|----------|
| Fade between scenes | 1 second |
| Major camera movement | 3-6 seconds |
| Text reveal | 1-1.5 seconds |
| Object creation | 2-3 seconds |
| SVG trace animation | 2-3 seconds |

### Scene Order (Total Flow)
Introduction → Hook → Pipeline → Challenges → Embedding Space → Softmax Introduction → Softmax Limitation → Evolution → ArcFace Core → Why It Works → Applications → Closing

---

## Development Workflow

1. **Create SVG assets** for complex objects (laptop, phone, lock) in `scenes/decorations/`
2. **Create scene file** in `scenes/` directory
3. **Test locally** with `manimgl main.py SceneName -s`
4. **Export video** with `manimgl main.py SceneName -w`
5. **Add to scene list** in `main.py`
6. **Commit changes** with descriptive message

---

## Important Notes

- **ALWAYS use SVG assets** for realistic objects (devices, icons) - never manually draw with primitives
- **ALWAYS use `from manimlib import *`** at the top of scene files
- Use `import numpy as np` for mathematical operations
- Set random seeds (`np.random.seed(42)`) for reproducible point distributions
- Reset camera before scene transitions
- Prefer geometric intuition over text explanations
- Keep line weights thin (1.5-2.5) for technical blueprint aesthetic
- Use `Create()` or `Write()` instead of `ShowCreation()` for SVG elements

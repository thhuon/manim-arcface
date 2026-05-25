# ManimGL ArcFace Animation Project — Coding Rules

>This file defines all rules for the ManimGL ArcFace educational animation project.
>All rules below are **mandatory** for every scene file. Read them before writing code.

---

## Project Overview

| Item | Value |
|------|-------|
| **Framework** | ManimGL (3b1b version) |
| **Style** | 3Blue1Brown — cinematic, geometric, intuition-first |
| **Output** | `.mp4` via ffmpeg, 1920×1080 (1080p), 60fps |
| **Audience** | Undergrad CS students with basic ML knowledge |

---

## Rule 1: ABSOLUTE TYPOGRAPHY — NO PLAIN TEXT

> **STRICTLY PROHIBITED:** `Text(...)`, plain system fonts, any non-LaTeX text rendering.

Every piece of text — titles, labels, equations, subtitles — **MUST** be written in LaTeX:

```python
# ✅ CORRECT — LaTeX with raw string
main_title = Tex(r"\text{Understanding ArcFace}", font_size=72, color=WHITE)
subtitle   = Tex(r"\text{The Geometry of Face Recognition}", font_size=32, color="#cccccc")

# ❌ WRONG — plain Text object
title = Text("Understanding ArcFace", font_size=72)   # FORBIDDEN
label = Text("embedding", font_size=24)              # FORBIDDEN
```

**Font size reference (144pt = 1 manim unit height):**
```python
TITLE_SIZE     = 72   # Main title
SUBTITLE_SIZE = 32   # Secondary text
EQUATION_SIZE = 72   # Math expressions
LABEL_SIZE    = 24   # Small labels
```

**Always use `r"..."` (raw string)** to prevent LaTeX backslash syntax errors.

---

## Rule 2: HYBRID VECTOR ASSETS — NO PRIMITIVE CODE FOR COMPLEX SHAPES

> **STRICTLY PROHIBITED:** Drawing smartphones, laptops, padlocks, icons, or any real-world object using `Arc`, `Line`, `Polygon`, `Circle`, `Rectangle`, or any combination of primitive shapes.

All complex objects **MUST** be SVG files imported via `SVGMobject`:

```python
def get_svg_path(filename: str) -> str:
    import os
    return os.path.join(
        os.path.dirname(__file__), "decorations", filename
    )

def white_svg(filename: str, height: float):
    """Load SVG as crisp solid-white flat vector."""
    return SVGMobject(
        file_name=get_svg_path(filename),
        height=height,
    ).set_fill(WHITE, 1.0).set_stroke(WHITE, 1.5)

# Usage
devices   = white_svg("devices.svg",     height=2.5)
lock      = white_svg("lock.svg",        height=1.0)
face_id   = white_svg("face-id.svg",     height=1.0)
lock_open = white_svg("lock-open.svg",   height=1.0)
```

**Color & Solid Structure Rule (MANDATORY for every SVGMobject):**
```python
.set_fill(WHITE, 1.0)    # Solid white fill, opacity 100%
.set_stroke(WHITE, 1.5)  # Thin 1.5-width white outline
```
This guarantees crisp, solid white flat vectors and prevents broken outlines or unexpected fills.

**SVG storage:** `scenes/decorations/*.svg`

---

## Rule 3: ORTHOGRAPHIC CAMERA — ZERO CAMERA MODIFICATIONS

> **STRICTLY PROHIBITED:** 3D camera orientation, `.reorient()`, `.rotate()` on camera frame, `phi_degrees`, `theta_degrees`, `ThreeDScene` for camera control.

**Base class rule:** Always extend `Scene`, never `ThreeDScene` (unless a scene genuinely needs a 3D sphere/unit-circle that absolutely requires `ThreeDScene`, and even then the camera frame must never be rotated).

```python
# ✅ CORRECT
class MyScene(Scene):
    def construct(self):
        self.camera.background_color = "#111111"   # 3B1B dark grey

# ❌ WRONG — no camera modifications allowed
class MyScene(ThreeDScene):
    def construct(self):
        self.frame.reorient(phi_degrees=70, ...)    # FORBIDDEN
        self.frame.animate.rotate(...)              # FORBIDDEN
```

**Background:** Always `self.camera.background_color = "#111111"` (dark grey, 3B1B aesthetic). Never pure black.

---

## Rule 4: ZERO OVERLAP — NO HARDCODED COORDINATES

> **STRICTLY PROHIBITED:** Hardcoded absolute coordinates like `[2, 1, 0]`, `np.array([3, 0, 0])`, `move_to([x, y, 0])`.

**Always use relative positioning:**

```python
# ✅ CORRECT — VGroup.arrange handles spacing automatically
left_group   = VGroup(svg1, svg2).arrange(DOWN, buff=0.3)
center_group = VGroup(icon, arrow).arrange(DOWN, buff=0.3)

diagram = VGroup(left_group, center_group, right_group)
diagram.arrange(RIGHT, buff=0.8)
diagram.move_to(ORIGIN)    # only ORIGIN is allowed as anchor

# Title block
title_block = VGroup(main_title, subtitle)
title_block.arrange(DOWN, buff=0.4)
title_block.to_edge(DOWN, buff=1.0)

# ✅ CORRECT — .next_to for fine positioning
label.next_to(arrow, UP, buff=0.3)

# ❌ WRONG — absolute numbers
obj.move_to([2, 1, 0])    # FORBIDDEN
arrow.shift(RIGHT * 2.5)  # allowed if relative to another object, not absolute
```

`.arrange()`, `.next_to()`, `.to_edge()`, `.shift()` from an existing object's edge — these mathematically guarantee zero physical overlap.

---

## Rule 5: ANIMATION — USE ShowCreation (NOT Create)

> ManimGL does **not** have `Create`; use `ShowCreation` for SVG/vector path tracing.

```python
# ✅ CORRECT
self.play(ShowCreation(svg_object), run_time=2.5)

# ❌ WRONG
self.play(Create(svg_object), ...)    # Create does not exist in ManimGL
```

**Animation patterns:**
```python
FadeIn(obj, shift=UP)           # Title reveal with upward slide
FadeOut(obj)                    # Clean disappear
ShowCreation(obj)               # SVG/vector path trace
ReplacementTransform(a, b)     # Clean memory transition
TransformMatchingShapes(a, b)   # Shape-preserving morph
FadeTransform(a, b)            # Cross-fade between objects
Write(tex_obj)                  # LaTeX writing animation
```

**Pacing:**
```python
rate_func=smooth   # Camera transitions, morphs
rate_func=linear   # Continuous processes (data streams)
run_time=2-3       # Standard for most animations
run_time=4-6       # Camera/slow reveals
```

---

## Background & Color Palette

```python
# Background — always dark grey, NOT pure black
self.camera.background_color = "#111111"   # 3B1B dark grey

# Neutral objects — WHITE
WHITE     = "#FFFFFF"

# Secondary elements
GREY      = "#888888"
DARK_GREY = "#444444"

# Accent colors (use sparingly)
CYAN      = "#00FFFF"
TEAL      = "#008080"
GOLD      = "#FFD700"
```

**Line weight:** `stroke_width = 1.5` (thin, technical). Range 1.5–2.5 max.

---

## Typography (LaTeX Only)

```python
# Equations and titles — ALWAYS via Tex/MathTex
main_title = Tex(r"\text{Understanding ArcFace}", font_size=72, color=WHITE)
subtitle   = Tex(r"\text{The Geometry of Face Recognition}", font_size=32, color="#cccccc")
equation   = MathTex(r"f(x) = \frac{1}{1 + e^{-x}}", font_size=48, color=WHITE)

# ❌ Text() is FORBIDDEN for any visible text
label = Text("embedding")   # NEVER
```

---

## File Structure

```
manim-arcface-2/
├── requirements.txt
├── manimlib/                  # ManimGL core library
└── scenes/
    ├── __init__.py
    ├── decorations/           # SVG assets (white_svg() loader)
    │   ├── devices.svg
    │   ├── lock.svg
    │   ├── lock-open.svg
    │   └── face-id.svg
    ├── scene00_introduction.py
    ├── scene01_hook.py
    └── ...
```

---

## Render Commands

```bash
# Write to video file (medium quality 720p)
python3 -m manimlib scenes/SceneFile.py SceneName -w -m

# Preview (with window)
python3 -m manimlib scenes/SceneFile.py SceneName

# HD 1080p
python3 -m manimlib scenes/SceneFile.py SceneName -w --hd
```

---

## Scene Flow (Total Arc)

Introduction → Hook → Pipeline → Challenges → Embedding Space → Softmax Introduction → Softmax Limitation → Evolution → ArcFace Core → Why It Works → Applications → Closing

---

## Quick Reference Checklist (before every commit)

- [ ] `from manimlib import *` at top of every scene file
- [ ] `class MyScene(Scene)` — never `ThreeDScene` unless 3D is required
- [ ] `self.camera.background_color = "#111111"`
- [ ] All text via `Tex(r"...")` or `MathTex(r"...")` — NO `Text()`
- [ ] Complex objects via `white_svg("filename.svg", height=X)` — NO primitives
- [ ] Every SVGMobject has `.set_fill(WHITE, 1.0).set_stroke(WHITE, 1.5)`
- [ ] Zero hardcoded coordinates — use `.arrange()`, `.next_to()`, `.to_edge()`
- [ ] Animations use `ShowCreation` not `Create`
- [ ] Raw strings `r"..."` for all LaTeX text inputs
- [ ] `np.random.seed(42)` for reproducible point distributions

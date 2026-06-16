"""
Shared utilities and constants for all scenes.
This module provides reusable helper functions, color palette, and visual element factories.
"""

from manimlib.mobject.mobject import Group
from manimlib.mobject.types.image_mobject import ImageMobject
from manimlib.mobject.geometry import Arrow, Line, DashedLine, Dot, Arc
from manimlib.mobject.types.vectorized_mobject import VGroup
from manimlib.mobject.svg.tex_mobject import Tex
from manimlib import *
import os


# =============================================================================
# COLOR PALETTE - Consistent throughout all scenes
# Based on 3Blue1Brown cinematic dark theme
# =============================================================================

# --- Background Colors ---
DARK = "#090D14"       # Deep navy black - main background
PANEL = "#101722"      # Slightly lighter panel backgrounds

# --- Primary Accent Colors ---
CYAN = "#00D4FF"      # Electric cyan - primary highlight, pipeline stages, active elements
GREEN = "#3EF7A0"     # Mint green - success, identity confirmed, matching
BLUE = "#4A7DFF"      # Royal blue - secondary accent, database elements

# --- Neutral Colors ---
WHITE = "#FFFFFF"     # Soft white - main text, active elements
MUTED = "#8A94A6"     # Slate gray - secondary text, labels, inactive elements

# --- Semantic Colors ---
RED = "#FF4757"        # Vibrant red - danger, false accept, errors, warnings
YELLOW = "#FFD43B"    # Warm yellow - caution, false reject, identity mismatch
ORANGE = "#FF9F43"    # Warm orange - highlights, accent variation
SHADOW = "#CC8855"    # Muted terracotta - cluster 2, secondary differentiation

# --- Legacy Aliases ---
ACCENT = CYAN          # Alias for ACCENT (used in scene03)


# =============================================================================
# ASSET PATH HELPER
# =============================================================================

def asset_path(filename: str) -> str:
    """Return the absolute path to a decoration asset file."""
    return os.path.join(
        os.path.dirname(__file__),
        "decorations",
        filename,
    )


# =============================================================================
# UTILITY FUNCTIONS - Basic building blocks
# =============================================================================

def latex(text: str, size: int = 28, color=WHITE):
    """Create a styled LaTeX text element with consistent coloring."""
    obj = Tex(text, font_size=size)
    obj.set_color(color)
    return obj


def glow_copy(mob, color=CYAN, width=7, opacity=0.18):
    """Create a copy with soft glow effect (for highlight animations)."""
    g = mob.copy()
    g.set_stroke(color=color, width=width, opacity=opacity)
    return g


def make_box(label_lines, width=2.35, height=1.28, stroke=CYAN, font_size=22):
    """Create a rounded rectangle box with centered text labels inside."""
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.16,
        stroke_color=stroke,
        stroke_width=2,
        fill_color=PANEL,
        fill_opacity=0.10,
    )
    labels = VGroup(*[latex(line, size=font_size) for line in label_lines])
    labels.arrange(DOWN, buff=0.08)
    labels.move_to(box)
    return VGroup(box, labels)


def make_vector(values, font_size=19):
    """Create a column vector display with brackets around values."""
    entries = VGroup(*[latex(str(v), size=font_size) for v in values])
    entries.arrange(DOWN, buff=0.08)
    left = Line(entries.get_corner(UL) + 0.10 * LEFT, entries.get_corner(DL) + 0.10 * LEFT, stroke_color=WHITE, stroke_width=1.4)
    right = Line(entries.get_corner(UR) + 0.10 * RIGHT, entries.get_corner(DR) + 0.10 * RIGHT, stroke_color=WHITE, stroke_width=1.4)
    return VGroup(left, entries, right)


# =============================================================================
# VISUAL ELEMENT FACTORIES - Reusable graphic components
# =============================================================================

def make_camera_icon():
    """Construct a stylized camera icon from geometric shapes."""
    body = RoundedRectangle(width=1.18, height=0.78, corner_radius=0.12, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
    lens = Circle(radius=0.24, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
    inner = Circle(radius=0.13, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
    lens.move_to(body)
    inner.move_to(lens)
    top = RoundedRectangle(width=0.42, height=0.18, corner_radius=0.05, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
    top.next_to(body, UP, buff=0)
    flash = Circle(radius=0.055, stroke_color=WHITE, stroke_width=1.2, fill_opacity=0)
    flash.move_to(body.get_corner(UR) + 0.18 * LEFT + 0.14 * DOWN)
    return VGroup(body, lens, inner, top, flash)


def make_abstract_face():
    """Construct a minimalist face icon: circle + eyes + nose + mouth."""
    face = Circle(radius=0.68, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
    eye_l = Dot(radius=0.055, color=CYAN).move_to(face.get_center() + 0.22 * LEFT + 0.16 * UP)
    eye_r = Dot(radius=0.055, color=CYAN).move_to(face.get_center() + 0.22 * RIGHT + 0.16 * UP)
    nose = VGroup(
        Line(face.get_center() + 0.07 * UP, face.get_center() + 0.08 * LEFT + 0.18 * DOWN),
        Line(face.get_center() + 0.08 * LEFT + 0.18 * DOWN, face.get_center() + 0.08 * RIGHT + 0.18 * DOWN),
    ).set_stroke(WHITE, 1.4)
    mouth = Arc(radius=0.25, start_angle=200 * DEGREES, angle=140 * DEGREES, stroke_color=WHITE, stroke_width=2)
    mouth.move_to(face.get_center() + 0.33 * DOWN)
    return VGroup(face, eye_l, eye_r, nose, mouth)


def make_landmarks():
    """Create 5 facial landmark dots (eyes, nose tip, mouth corners)."""
    dots = VGroup()
    for p in [0.25 * LEFT + 0.20 * UP, 0.25 * RIGHT + 0.20 * UP, ORIGIN, 0.20 * LEFT + 0.28 * DOWN, 0.20 * RIGHT + 0.28 * DOWN]:
        dots.add(Dot(point=p, radius=0.045, color=CYAN))
    return dots


def make_pixel_grid(size=2.15, n=8):
    """Create an 8x8 grid overlay to represent pixelation concept."""
    grid = VGroup()
    step = size / n
    for i in range(n + 1):
        offset = -size / 2 + i * step
        grid.add(Line(LEFT * size / 2 + UP * offset, RIGHT * size / 2 + UP * offset, stroke_color=WHITE, stroke_width=0.45, stroke_opacity=0.28))
        grid.add(Line(DOWN * size / 2 + RIGHT * offset, UP * size / 2 + RIGHT * offset, stroke_color=WHITE, stroke_width=0.45, stroke_opacity=0.28))
    return grid


def make_neural_network():
    """Create a small neural network visualization: 3-5-5-3 architecture."""
    layers = [3, 5, 5, 3]
    groups = VGroup()
    for count in layers:
        col = VGroup(*[Circle(radius=0.105, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0) for _ in range(count)])
        col.arrange(DOWN, buff=0.15)
        groups.add(col)
    groups.arrange(RIGHT, buff=0.46)

    edges = VGroup()
    for a, b in zip(groups[:-1], groups[1:]):
        for n1 in a:
            for n2 in b:
                edges.add(Line(n1.get_center(), n2.get_center(), stroke_color=WHITE, stroke_width=0.7, stroke_opacity=0.26))
    return VGroup(edges, groups)

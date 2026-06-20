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
import random
from PIL import Image


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


def tex_text(text: str) -> str:
    """Escape plain text for use inside LaTeX \\text{...} blocks."""
    return (
        str(text)
        .replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
    )


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


# =============================================================================
# POLISHED LAYOUT HELPERS - Shared by the first three rewritten scenes
# =============================================================================

def fit_to_bounds(mob, max_width=None, max_height=None):
    """Scale a mobject down until it fits inside the requested bounds."""
    if max_width is not None and mob.get_width() > max_width:
        mob.set_width(max_width)
    if max_height is not None and mob.get_height() > max_height:
        mob.set_height(max_height)
    return mob


def make_scene_title(title, subtitle=None, title_size=42, subtitle_size=22, color=WHITE):
    """Create a compact two-line title block that stays clear of the frame edge."""
    title_mob = latex(rf"\textbf{{{tex_text(title)}}}", size=title_size, color=color)
    if subtitle is None:
        title_mob.to_edge(UP, buff=0.45)
        return title_mob

    subtitle_mob = latex(rf"\text{{{tex_text(subtitle)}}}", size=subtitle_size, color=MUTED)
    group = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.12)
    group.to_edge(UP, buff=0.38)
    return group


def make_badge(label, color=CYAN, font_size=19, h_buff=0.22, v_buff=0.11):
    """Create a small labelled pill for short state and concept labels."""
    text = latex(rf"\text{{{tex_text(label)}}}", size=font_size, color=color)
    box = RoundedRectangle(
        width=text.get_width() + 2 * h_buff,
        height=text.get_height() + 2 * v_buff,
        corner_radius=0.10,
        stroke_color=color,
        stroke_width=1.5,
        fill_color=PANEL,
        fill_opacity=0.45,
    )
    text.move_to(box)
    return VGroup(box, text)


def make_image_card(
    filename,
    width=1.45,
    height=1.70,
    label=None,
    label_color=MUTED,
    stroke_color=WHITE,
    label_size=15,
    show_frame=True,
):
    """Create a fixed-size image card with an optional non-overlapping label."""
    image = ImageMobject(asset_path(filename))
    fit_to_bounds(image, width, height)
    group = Group(image)
    label_anchor = image
    if show_frame:
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_color=stroke_color,
            stroke_width=1.2,
            fill_color=PANEL,
            fill_opacity=0.22,
        )
        image.move_to(frame)
        group.add(frame)
        label_anchor = frame
    if label is not None:
        label_mob = latex(rf"\text{{{tex_text(label)}}}", size=label_size, color=label_color)
        label_mob.next_to(label_anchor, DOWN, buff=0.08)
        group.add(label_mob)
    return group


def make_stage_card(index, title, subtitle, color=CYAN, width=2.75, height=1.25):
    """Create a pipeline stage card with a stable fixed footprint."""
    box = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=2,
        fill_color=PANEL,
        fill_opacity=0.30,
    )
    number = Circle(radius=0.20, stroke_color=color, stroke_width=1.6, fill_color=PANEL, fill_opacity=0.85)
    number_label = latex(rf"\textbf{{{index}}}", size=17, color=color).move_to(number)
    number_group = VGroup(number, number_label)
    number_group.move_to(box.get_left() + RIGHT * 0.38 + UP * 0.36)

    title_mob = latex(rf"\textbf{{{tex_text(title)}}}", size=20, color=WHITE)
    subtitle_mob = latex(rf"\text{{{tex_text(subtitle)}}}", size=16, color=MUTED)
    label_group = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.06)
    label_group.move_to(box.get_center() + RIGHT * 0.24)
    fit_to_bounds(label_group, width - 0.65, height - 0.20)
    label_group.move_to(box.get_center() + RIGHT * 0.24)
    return VGroup(box, number_group, label_group)


def make_flow_arrow(start, end, color=CYAN, stroke_width=2.4):
    """Create a consistent low-noise flow arrow."""
    return Arrow(
        start,
        end,
        buff=0.10,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.16,
    )


def make_double_arrow(start, end, color=CYAN, stroke_width=2.0):
    """Create a double-headed arrow for ManimGL versions without DoubleArrow."""
    return VGroup(
        Arrow(
            start,
            end,
            buff=0.06,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.10,
        ),
        Arrow(
            end,
            start,
            buff=0.06,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.10,
        ),
    )


def make_pixel_matrix(n=10, side=2.75, seed=1, color=CYAN):
    """Create a deterministic pixel matrix with readable block contrast."""
    rng = random.Random(seed)
    cells = VGroup()
    cell_side = side / n
    for row in range(n):
        for col in range(n):
            opacity = rng.uniform(0.12, 0.90)
            cell = Square(
                side_length=cell_side,
                stroke_color=WHITE,
                stroke_width=0.35,
                fill_color=color if rng.random() > 0.40 else WHITE,
                fill_opacity=opacity,
            )
            x = (col - (n - 1) / 2) * cell_side
            y = ((n - 1) / 2 - row) * cell_side
            cell.move_to(np.array([x, y, 0]))
            cells.add(cell)
    return cells


def make_pixel_matrix_from_image(filename, n=10, side=2.75, sample_box=None):
    """Create a pixel matrix by sampling averaged colors from an image asset."""
    image = Image.open(asset_path(filename)).convert("RGB")
    if sample_box is not None:
        image = image.crop(sample_box)
    image = image.resize((n, n), Image.Resampling.BILINEAR)

    cells = VGroup()
    cell_side = side / n
    for row in range(n):
        for col in range(n):
            r, g, b = image.getpixel((col, row))
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            cell = Square(
                side_length=cell_side,
                stroke_color=BLACK,
                stroke_width=0.18,
                stroke_opacity=0.35,
                fill_color=hex_color,
                fill_opacity=1.0,
            )
            x = (col - (n - 1) / 2) * cell_side
            y = ((n - 1) / 2 - row) * cell_side
            cell.move_to(np.array([x, y, 0]))
            cells.add(cell)
    return cells


def make_embedding_cluster(center, color=CYAN, radius=0.085, scale=1.0, count=6):
    """Create a compact deterministic dot cluster around a center point."""
    offsets = [
        ORIGIN,
        0.34 * RIGHT + 0.10 * UP,
        0.22 * LEFT + 0.24 * UP,
        0.24 * RIGHT + 0.28 * DOWN,
        0.36 * LEFT + 0.14 * DOWN,
        0.02 * RIGHT + 0.40 * UP,
    ]
    dots = VGroup()
    for offset in offsets[:count]:
        dots.add(Dot(point=center + offset * scale, color=color, radius=radius))
    return dots


def make_panel(width=5.8, height=4.5, stroke_color=MUTED, fill_opacity=0.12):
    """Create a subtle fixed panel without heavy card styling."""
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.10,
        stroke_color=stroke_color,
        stroke_width=1.2,
        fill_color=PANEL,
        fill_opacity=fill_opacity,
    )


def make_svg_icon(filename, height=0.85, color=WHITE):
    """Load an SVG asset as a simple white line/fill icon."""
    icon = SVGMobject(file_name=asset_path(filename), height=height)
    icon.set_fill(color, opacity=0.0)
    icon.set_stroke(color=color, width=2.0, opacity=1.0)
    return icon


def clear_scene(scene, run_time=0.65, wait_time=0.35):
    """Fade out all current scene mobjects and pause briefly."""
    if scene.mobjects:
        scene.play(FadeOut(Group(*scene.mobjects)), run_time=run_time)
    if wait_time:
        scene.wait(wait_time)

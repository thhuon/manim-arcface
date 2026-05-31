from manimlib import *
import os
from scenes.utils import *


# =============================================================================
# SCENE-SPECIFIC HELPERS - SVG loaders for scene00
# =============================================================================

def clean_stroke_svg(filename: str, height: float):
    """
    Load SVG using 3Blue1Brown blueprint style:
    No flat fills, outline-only stroke assets.
    """
    return SVGMobject(
        file_name=asset_path(filename),
        height=height,
    ).set_fill(WHITE, opacity=0.0).set_stroke(color=WHITE, width=2.0)


def filled_svg(filename: str, height: float, fill_opacity: float = 1.0):
    """
    Load SVG with white fill.
    """
    return SVGMobject(
        file_name=asset_path(filename),
        height=height,
    ).set_fill(WHITE, opacity=fill_opacity)


class Scene00Introduction(Scene):
    """
    Sub-Screen 1: Device flow diagram — sequential reveal left to right.
    Sub-Screen 2: Grand LaTeX title fades in.
    """

    def construct(self):
        self.camera.background_color = "#111111"

        # ── STEP 1: Asset Loading & Proportional Scaling ──────────────────────

        # LEFT: devices.svg with white fill
        devices = filled_svg("devices.svg", height=2.5)
        devices.scale(1.8)

        # Closed lock — sits strictly above devices
        lock_closed = filled_svg("lock.svg", height=1.0)
        lock_closed.scale(0.65)
        lock_closed.next_to(devices, UP, buff=0.3)

        left_group = VGroup(devices, lock_closed)

        # CENTER: extended arrow + "FaceID" LaTeX label above
        center_arrow = Arrow(LEFT, RIGHT, stroke_color=WHITE, stroke_width=4)
        center_arrow.scale(1.6)

        face_id_label = Tex(r"\text{FaceID}", font_size=36, color=WHITE)
        face_id_label.next_to(center_arrow, UP, buff=0.3)

        center_group = VGroup(center_arrow, face_id_label)

        # RIGHT: open lock
        lock_open = filled_svg("lock-open.svg", height=1.0)
        lock_open.scale(0.8)
        right_group = lock_open

        # ── STEP 2: Horizontal Spacing & Maximizing Screen Coverage ───────────

        main_diagram = VGroup(left_group, center_group, right_group)
        main_diagram.arrange(RIGHT, buff=1.5)
        main_diagram.scale(1.2)
        main_diagram.move_to(ORIGIN)

        # ── STEP 3: Title Block (Sub-Screen 2) ─────────────────────────────

        line1 = Tex(r"\textbf{Understanding ArcFace}", font_size=72, color=WHITE)
        line2 = Tex(r"\text{The Geometry of Face Recognition}", font_size=32, color="#cccccc")
        title_block = VGroup(line1, line2)
        title_block.arrange(DOWN, buff=0.4)
        title_block.move_to(ORIGIN)

        # ── STEP 4: Animation Sequence ───────────────────────────────────────

        # Sub-Screen 1: sequential reveal left → center → right
        self.play(FadeIn(left_group), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(center_group), run_time=0.5)
        self.wait(0.3)
        self.play(FadeIn(right_group), run_time=0.5)
        self.wait(1.5)

        # Transition: fade out diagram
        self.play(FadeOut(main_diagram), run_time=0.8)

        # Sub-Screen 2: fade in LaTeX title
        self.play(FadeIn(title_block), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(title_block), run_time=1.0)
        self.wait(0.5)

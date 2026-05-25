from manimlib import *


def get_svg_path(filename: str) -> str:
    """Get full path to SVG file in decorations folder."""
    import os
    return os.path.join(
        os.path.dirname(__file__),
        "decorations",
        filename
    )


def white_svg(filename: str, height: float):
    """Load SVG as crisp solid-white flat vector."""
    return SVGMobject(
        file_name=get_svg_path(filename),
        height=height,
    ).set_fill(WHITE, 1.0).set_stroke(WHITE, 1.5)


class Scene00Introduction(Scene):
    """
    Sub-Screen 1: Device flow diagram — uniform scaling, no distortion.
    Sub-Screen 2: LaTeX title fades in after diagram fades out.
    """

    def construct(self):
        self.camera.background_color = "#111111"

        # ── STEP 1: Asset Loading & Proportional Scaling ──────────────────────

        # LEFT: devices.svg — dominant element, scaled up uniformly
        devices = white_svg("devices.svg", height=2.5)
        devices.scale(1.8)

        # Closed lock — scaled down, sits strictly above devices
        lock_closed = white_svg("lock.svg", height=1.0)
        lock_closed.scale(0.65)
        lock_closed.next_to(devices, UP, buff=0.3)

        left_group = VGroup(devices, lock_closed)

        # CENTER: extended arrow + "FaceID" LaTeX label above
        center_arrow = Arrow(LEFT, RIGHT, stroke_color=WHITE, stroke_width=4)
        center_arrow.scale(1.6)

        face_id_label = Tex(r"\text{FaceID}", font_size=36, color=WHITE)
        face_id_label.next_to(center_arrow, UP, buff=0.3)

        center_group = VGroup(center_arrow, face_id_label)

        # RIGHT: open lock — matches closed lock scale exactly
        lock_open = white_svg("lock-open.svg", height=1.0)
        lock_open.scale(0.8)
        right_group = lock_open

        # ── STEP 2: Horizontal Spacing & Maximizing Screen Coverage ───────────

        main_diagram = VGroup(left_group, center_group, right_group)
        main_diagram.arrange(RIGHT, buff=1.5)
        main_diagram.scale(1.2)
        main_diagram.move_to(ORIGIN)

        # ── STEP 3: Title Block (Sub-Screen 2) ───────────────────────────────

        line1 = Tex(r"\textbf{Understanding ArcFace}", font_size=72, color=WHITE)
        line2 = Tex(r"\text{The Geometry of Face Recognition}", font_size=32, color="#cccccc")
        title_block = VGroup(line1, line2)
        title_block.arrange(DOWN, buff=0.4)
        title_block.move_to(ORIGIN)

        # ── STEP 4: Animation Sequence ───────────────────────────────────────

        # Sub-Screen 1: reveal diagram left → center → right
        self.play(ShowCreation(left_group),   run_time=1.2)
        self.play(ShowCreation(center_group), run_time=1.0)
        self.play(ShowCreation(right_group),  run_time=0.8)
        self.wait(1.5)

        # Transition: fade out diagram
        self.play(FadeOut(main_diagram), run_time=0.8)

        # Sub-Screen 2: fade in LaTeX title (no shift — appears directly)
        self.play(FadeIn(title_block), run_time=1.5)
        self.wait(2.5)

        self.play(FadeOut(title_block), run_time=1.0)
        self.wait(0.5)

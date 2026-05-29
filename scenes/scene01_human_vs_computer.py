from manimlib.mobject.mobject import Group
from manimlib.mobject.types.image_mobject import ImageMobject
from manimlib.mobject.geometry import Arrow
from manimlib.mobject.types.vectorized_mobject import VGroup
from typing import Any
from manimlib.mobject.svg.tex_mobject import Tex
from manimlib import *
import os
import random


def get_asset_path(filename: str) -> str:
    """Return the absolute path to a decoration asset file."""
    return os.path.join(
        os.path.dirname(__file__),
        "decorations",
        filename,
    )


class Scene01_HumanVsComputer(Scene):
    """
    Beat 1 — Human recognition: static camera, intuition → aha_moment,
              staggered reveal: arrow+aha+brain → (1s) → bulb+label.
    Beat 2 — Computer view: face_bg + mesh_overlay (matched bounds) → 8x8 matrix.
    Beat 3 — Pipeline title on a perfectly clean canvas.
    """

    def construct(self):
        self.camera.background_color = "#111111"

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 1 — Human recognition (static camera, no movement)
        # ─────────────────────────────────────────────────────────────────────

        # intuition.png — directly at final upper-left position
        intuition = ImageMobject(get_asset_path("intuition.png"))
        intuition.scale(0.85)
        intuition.move_to(LEFT * 2.5 + UP * 1.2)

        # aha_moment.png — raster, matched height to intuition (native colors)
        aha_moment = ImageMobject(get_asset_path("aha_moment.png"))
        aha_moment.set_height(intuition.get_height())

        # Brain symbol — native SVG colors, larger scale
        brain = SVGMobject(file_name=get_asset_path("brain.svg"))
        brain.scale(0.7)

        # Light-bulb symbol — native SVG colors, placed above brain
        bulb = SVGMobject(file_name=get_asset_path("bulb.svg"))
        bulb.scale(0.5)
        bulb.next_to(brain, UP, buff=0.35)
        bulb.shift(RIGHT * 0.75)           

        # Symbols group: bulb stacked above brain (vertical)
        symbols_group = VGroup(brain, bulb)

        # Human label — LaTeX, white, right of symbols
        human_label = Tex(r"\text{Human: Intuitive Match}", font_size=32)
        human_label.set_color(WHITE)
        human_label.next_to(brain, RIGHT, buff=1)
        # Align vertical centers for sleek infographic look
        # human_label.align_to(symbols_group, UP)

        # Bottom row: symbols + label — centered on screen
        bottom_row_group = Group(symbols_group, human_label)
        bottom_row_group.next_to(intuition, DOWN, buff=0.25)
        bottom_row_group.move_to(bottom_row_group.get_center()[1] * UP)

        # Arrow: data flow from intuition (left) → aha_moment (right)
        row1_arrow = Arrow(
            LEFT,
            RIGHT,
            color=WHITE,
            stroke_width=2,
        )

        # Top row: intuition + arrow + aha_moment
        top_row_group = Group(intuition, row1_arrow, aha_moment)
        top_row_group.arrange(RIGHT, buff=0.6)
        top_row_group.move_to(UP * 1.5)

        # Master group for wipe
        beat1_master_group = Group(top_row_group, bottom_row_group)
        beat1_group = Group(beat1_master_group)

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 2 — Computer view
        # ─────────────────────────────────────────────────────────────────────

        # face_scan — positioned left side, matrix on right
        face_scan = ImageMobject(get_asset_path("face_scan.png"))
        face_scan.set_height(FRAME_HEIGHT * 0.8)

        # matrix_block — 8x8 grid, positioned right
        random.seed(42)
        all_cells = []
        for r in range(8):
            for c in range(8):
                entry = Tex(str(random.randint(0, 9)), font_size=22)
                entry.move_to(
                    RIGHT * (c * 0.42 - 8 * 0.42 / 2 + 0.21)
                    + UP * (r * 0.42 - 8 * 0.42 / 2 + 0.21)
                )
                all_cells.append(entry)

        matrix_block = VGroup(*all_cells)

        # Brackets around the matrix
        bracket_height = matrix_block.get_height() + 0.3
        left_bracket = Line(UP * bracket_height / 2, DOWN * bracket_height / 2)
        right_bracket = Line(UP * bracket_height / 2, DOWN * bracket_height / 2)

        left_bracket.next_to(matrix_block, LEFT, buff=0.15)
        right_bracket.next_to(matrix_block, RIGHT, buff=0.15)

        left_bracket.set_stroke(color=WHITE, width=3)
        right_bracket.set_stroke(color=WHITE, width=3)

        # Group matrix with brackets
        matrix_with_brackets = VGroup(left_bracket, matrix_block, right_bracket)
        matrix_with_brackets.scale(1.75)

        # computer_arrow —> connects face_scan to matrix_with_brackets
        computer_arrow = Arrow(
            matrix_with_brackets.get_left() + LEFT * 0.3,
            face_scan.get_right() + RIGHT * 0.3,
            color=WHITE,
            stroke_width=3,
        )

        # Beat 2 row: face + arrow + matrix —> auto-arranged
        beat2_row = Group(face_scan, computer_arrow, matrix_with_brackets)
        beat2_row.arrange(RIGHT, buff=0.5)
        beat2_row.scale(0.8)
        beat2_row.move_to(ORIGIN)
        beat2_row.move_to(np.array([0, beat2_row.get_center()[1], 0])) # make the beat2_row in the center of the frame
        beat2_row.set_width(FRAME_WIDTH * 0.8) # make the beat2_row width is the width of the frame

        # Computer label below
        computer_label = Tex(
            r"\text{Computer: Pixels and Numbers}",
            font_size=32,
        )
        computer_label.next_to(beat2_row, DOWN, buff=0.5)

        beat2_group = Group[Group[ImageMobject | Arrow | VGroup] | Tex](beat2_row, computer_label)

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 3 — Pipeline title (clean canvas)
        # ─────────────────────────────────────────────────────────────────────

        line1 = Tex(r"\textbf{Face Recognition Pipeline}", font_size=54)
        line2 = Tex(
            r"\text{What happens when we look into a camera?}",
            font_size=28,
        )
        line2.set_color("#cccccc")

        title_block = VGroup(line1, line2)
        title_block.arrange(DOWN, buff=0.35)
        title_block.move_to(ORIGIN)

        # ─────────────────────────────────────────────────────────────────────
        # ANIMATION SEQUENCE — static camera throughout
        # ─────────────────────────────────────────────────────────────────────

        # ══ BEAT 1 — Static camera, staggered reveal ════════════════════════

        # Step 1: intuition fades in at final position (no movement)
        self.play(FadeIn(intuition), run_time=1.0)
        self.wait(0.5)

        # Step 2: simultaneously — arrow grows, aha_moment fades in, brain appears
        self.play(
            FadeIn(brain),
            run_time=1.0,
        )
        
        # Step 3: exactly 1s later — bulb pops up above brain, label fades in
        self.play(
            FadeIn(row1_arrow),
            FadeIn(aha_moment),
            FadeIn(bulb),
            run_time=1.0,
        )
        
        self.wait(0.25)

        self.play(
            FadeIn(human_label),
            run_time=0.8,
        )
        self.wait(1.5)

        # Wipe Beat 1 to black
        self.play(FadeOut(beat1_group), run_time=0.8)
        self.wait(0.3)

        # ══ BEAT 2 — Computer view ══════════════════════════════════════════
        # Step 1: face_scan fades in, computer_arrow grows, matrix_block fades in
        self.play(FadeIn(face_scan), FadeIn(computer_arrow), run_time=0.8)
        self.wait(0.5)

        # Step 2: brackets + matrix cells fade in
        self.play(
            FadeIn(left_bracket),
            FadeIn(right_bracket),
            LaggedStart(*[FadeIn(cell) for cell in all_cells], lag_ratio=0.055),
            run_time=2.5,
        )
        self.wait(0.5)

        # Step 3: computer_label fades in
        self.play(FadeIn(computer_label), run_time=0.8)
        self.wait(0.5)

        
        self.wait(0.8)

        # Wipe Beat 2 to black
        self.play(FadeOut(beat2_group), run_time=0.8)
        self.wait(0.4)

        # ══ BEAT 3 — Title on clean canvas ════════════════════════════════

        self.play(FadeIn(title_block), run_time=1.2)
        self.wait(0.5)
        self.wait(2.5)
        self.play(FadeOut(title_block), run_time=1.0)
        self.wait(0.5)

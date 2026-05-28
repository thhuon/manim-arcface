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
    Beat 1 — Human recognition: static camera, trump_intuition → trump_aha,
              staggered reveal: arrow+aha+brain → (1s) → bulb+label.
    Beat 2 — Computer view: face_bg + mesh_overlay (matched bounds) → 8x8 matrix.
    Beat 3 — Pipeline title on a perfectly clean canvas.
    """

    def construct(self):
        self.camera.background_color = "#111111"

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 1 — Human recognition (static camera, no movement)
        # ─────────────────────────────────────────────────────────────────────

        # trump_intuition.png — directly at final upper-left position
        trump_intuition = ImageMobject(get_asset_path("trump_intuition.png"))
        trump_intuition.scale(0.85)
        trump_intuition.move_to(LEFT * 2.5 + UP * 1.2)

        # trump_aha.png — raster, matched height to trump_intuition (native colors)
        trump_aha = ImageMobject(get_asset_path("trump_aha.png"))
        trump_aha.set_height(trump_intuition.get_height())

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
        bottom_row_group.next_to(trump_intuition, DOWN, buff=0.25)
        bottom_row_group.move_to(bottom_row_group.get_center()[1] * UP)

        # Arrow: data flow from trump_intuition (left) → trump_aha (right)
        row1_arrow = Arrow(
            LEFT,
            RIGHT,
            color=WHITE,
            stroke_width=2,
        )

        # Top row: trump_intuition + arrow + trump_aha
        top_row_group = Group(trump_intuition, row1_arrow, trump_aha)
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

        # computer_arrow — connects face_scan to matrix_block
        computer_arrow = Arrow(
            matrix_block.get_left() + LEFT * 0.3,
            face_scan.get_right() + RIGHT * 0.3,
            color=WHITE,
            stroke_width=3,
        )

        # Beat 2 row: face + arrow + matrix — auto-arranged
        beat2_row = Group(face_scan, computer_arrow, matrix_block)
        beat2_row.arrange(RIGHT, buff=0.5)
        beat2_row.scale(0.8)
        beat2_row.move_to(ORIGIN)

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

        # Step 1: trump_intuition fades in at final position (no movement)
        self.play(FadeIn(trump_intuition), run_time=1.0)
        self.wait(0.5)

        # Step 2: simultaneously — arrow grows, trump_aha fades in, brain appears
        self.play(
            FadeIn(brain),
            run_time=1.0,
        )
        
        # Step 3: exactly 1s later — bulb pops up above brain, label fades in
        self.play(
            FadeIn(row1_arrow),
            FadeIn(trump_aha),
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

        # Step 2: matrix_block cells fade in, computer_arrow grows
        self.play(
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

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


class Scene1_HumanVsComputer(Scene):
    """
    Beat 1 — Human recognition: trump_intuition grid → glowing arrow → trump_aha + intuition symbols.
    Beat 2 — Computer view: face_bg + mesh_overlay → glowing arrow → 8×8 numeric matrix.
    Beat 3 — Pipeline transition: clear canvas → centered title block.
    """

    def construct(self):
        self.camera.background_color = "#111111"

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 1 — Human side
        # ─────────────────────────────────────────────────────────────────────

        # 2×3 raster face grid (ImageMobject)
        trump_img = ImageMobject(get_asset_path("trump_intuition.png"))
        trump_img.scale(0.48)
        trump_img.move_to(LEFT * 3.6 + DOWN * 0.2)

        # Vector outline around the grid (VMobject)
        trump_outline = SurroundingRectangle(
            trump_img,
            color=WHITE,
            stroke_width=1.5,
            fill_opacity=0.0,
            buff=0.2,
        )

        # Use Group — VGroup rejects ImageMobject
        human_face_block = Group(trump_img, trump_outline)

        # trump_aha SVG — the "aha moment" cartoon face (VMobject)
        trump_aha = SVGMobject(file_name=get_asset_path("trump-aha.svg"))
        trump_aha.set_height(1.8)

        # Brain symbol (stroke-only, 3Blue1Brown style)
        brain = SVGMobject(file_name=get_asset_path("brain.svg"))
        brain.set_fill(opacity=0.0).set_stroke(color=BLUE_A, width=2.0).set_height(0.8)

        # Light-bulb symbol (stroke-only)
        bulb = SVGMobject(file_name=get_asset_path("bulb.svg"))
        bulb.set_fill(opacity=0.0).set_stroke(color=BLUE_A, width=2.0).set_height(0.8)

        # Stack brain + bulb horizontally, place above trump_aha (all VMobject)
        symbols = VGroup(brain, bulb).arrange(RIGHT, buff=0.5)
        symbols.next_to(trump_aha, UP, buff=0.25)

        human_aha_block = Group(trump_aha, symbols)

        # Horizontal assembly: explicit positioning (Group doesn't have .arrange)
        human_arrow = Arrow(
            human_face_block.get_right() + RIGHT * 0.25,
            RIGHT * 0.35,
            stroke_color=BLUE_A,
            stroke_width=2.5,
            buff=0.0,
        )

        human_row = Group(human_face_block, human_arrow, human_aha_block)
        human_row.arrange(RIGHT, buff=0.5)  # VGroup method inherited via Mobject

        # MathTex label beneath the row
        human_label = Tex(r"\text{Human: Intuitive Match}", font_size=32)
        human_label.next_to(human_row, DOWN, buff=0.4)

        human_group = Group(human_row, human_label)
        # Position the whole human group on the left half of the screen
        human_group.move_to(LEFT * 1.5 + UP * 0.4)

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 2 — Computer side
        # ─────────────────────────────────────────────────────────────────────

        # Raster face background at 75 % opacity (ImageMobject)
        face_bg = ImageMobject(get_asset_path("face_bg.png"))
        face_bg.set_opacity(0.75)
        face_bg.set_height(2.6)

        # Vector mathematical mesh overlaid on the face (VMobject)
        mesh = SVGMobject(file_name=get_asset_path("mesh_overlay.svg"))
        mesh.set_height(face_bg.get_height())
        mesh.set_stroke(color=BLUE_A, width=1.5).set_fill(opacity=0.0)
        mesh.move_to(face_bg.get_center())

        # Group: face_bg (ImageMobject) + mesh (VMobject)
        face_mesh_block = Group(face_bg, mesh)

        # 8×8 numeric matrix generated in nested Python loops (all MathTex = VMobject)
        random.seed(42)
        matrix_entries = []
        for _ in range(8):
            row = []
            for _ in range(8):
                digit = random.randint(0, 9)
                entry = Tex(str(digit), font_size=22)
                row.append(entry)
            matrix_entries.append(row)

        # Place each entry on an 8×8 grid with uniform 0.42 spacing
        for r in range(8):
            for c in range(8):
                matrix_entries[r][c].move_to(
                    RIGHT * (c * 0.42 - 8 * 0.42 / 2 + 0.21)
                    + UP * (r * 0.42 - 8 * 0.42 / 2 + 0.21)
                )

        # Collect all 64 cells as a flat list for LaggedStart
        all_cells = [cell for row in matrix_entries for cell in row]

        # matrix_block: pure VMobject, stays VGroup
        matrix_block = VGroup(*all_cells)

        # Computer label beneath the computer block
        computer_label = Tex(
            r"\text{Computer: Pixels and Numbers}",
            font_size=32,
        )

        # Horizontal assembly: explicit positioning
        computer_arrow = Arrow(
            face_mesh_block.get_right() + RIGHT * 0.35,
            RIGHT * 2.5,
            stroke_color=BLUE_A,
            stroke_width=2.5,
            buff=0.0,
        )

        computer_row = Group(face_mesh_block, computer_arrow, matrix_block)
        computer_row.arrange(RIGHT, buff=0.4)

        computer_label.next_to(computer_row, DOWN, buff=0.4)

        computer_group = Group(computer_row, computer_label)
        # Position the whole computer group on the right half of the screen
        computer_group.move_to(RIGHT * 1.5 + UP * 0.4)

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 3 — Pipeline transition elements
        # ─────────────────────────────────────────────────────────────────────

        # Vertically stacked Tex title block, centered
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
        # ANIMATION SEQUENCE
        # ─────────────────────────────────────────────────────────────────────

        # Beat 1 — fade in the human recognition group
        self.play(FadeIn(human_group), run_time=1.2)
        self.wait(1.5)

        # Beat 2 — fade in the face background, draw the mesh, then
        # fade in the arrow and matrix, stream cells, dim human side
        self.play(FadeIn(face_mesh_block), run_time=0.8)
        self.wait(0.3)
        self.play(ShowCreation(mesh), run_time=1.5)
        self.wait(0.4)

        self.play(FadeIn(computer_group), run_time=0.8)
        self.wait(0.5)

        # Stream matrix entries one-by-one
        self.play(
            LaggedStart(*[FadeIn(cell) for cell in all_cells], lag_ratio=0.055),
            run_time=2.5,
        )
        self.wait(0.8)

        # Dim human side to pull viewer attention to the computer side
        self.play(human_group.animate.set_opacity(0.3), run_time=0.8)
        self.wait(1.0)

        # Beat 3 — clear the canvas, then reveal the pipeline title
        self.play(FadeOut(human_group), FadeOut(computer_group), run_time=0.8)
        self.wait(0.4)

        self.play(FadeIn(title_block), run_time=1.2)
        self.wait(0.5)

        # Hold final frame
        self.wait(2.5)

        self.play(FadeOut(title_block), run_time=1.0)
        self.wait(0.5)

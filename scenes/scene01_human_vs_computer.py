from manimlib import *
import os
import random
from scenes.utils import *


# =============================================================================
# SCENE 01 - Human vs Computer
# =============================================================================

class Scene01_HumanVsComputer(Scene):
    """
    Beat 1 — Human recognition: static camera, intuition → aha_moment,
              staggered reveal: arrow+aha+brain → (1s) → bulb+label.
    Beat 2 — Computer view: face_bg + mesh_overlay (matched bounds) → 8x8 matrix.
    Beat 3 — Pipeline title on a perfectly clean canvas.
    """

    def construct(self):
        self.camera.background_color = DARK

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 1 — Human recognition (static camera, no movement)
        # ─────────────────────────────────────────────────────────────────────

        # intuition.png — directly at final upper-left position
        intuition = ImageMobject(asset_path("intuition.png"))
        intuition.scale(0.85)
        intuition.move_to(LEFT * 2.5 + UP * 1.2)

        # aha_moment.png — raster, matched height to intuition (native colors)
        aha_moment = ImageMobject(asset_path("aha_moment.png"))
        aha_moment.set_height(intuition.get_height())

        # Brain symbol — native SVG colors, larger scale
        brain = SVGMobject(file_name=asset_path("brain.svg"))
        brain.scale(0.7)

        # Light-bulb symbol — native SVG colors, placed above brain
        bulb = SVGMobject(file_name=asset_path("bulb.svg"))
        bulb.scale(0.5)
        bulb.next_to(brain, UP, buff=0.35)
        bulb.shift(RIGHT * 0.75)

        # Symbols group: bulb stacked above brain (vertical)
        symbols_group = VGroup(brain, bulb)

        # Human label — LaTeX, white, right of symbols
        human_label = Tex(r"\text{Human: Intuitive Match}", font_size=32)
        human_label.set_color(WHITE)
        human_label.next_to(brain, RIGHT, buff=1)

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
        face_scan = ImageMobject(asset_path("face_scan.png"))
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
        beat2_row.move_to(np.array([0, beat2_row.get_center()[1], 0]))
        beat2_row.set_width(FRAME_WIDTH * 0.8)

        # Computer label below
        computer_label = Tex(
            r"\text{Computer: Pixels and Numbers}",
            font_size=32,
        )
        computer_label.next_to(beat2_row, DOWN, buff=0.5)

        beat2_group = Group(beat2_row, computer_label)

        # ─────────────────────────────────────────────────────────────────────
        # BEAT 3 — Pipeline title (clean canvas)
        # ─────────────────────────────────────────────────────────────────────

        line1 = Tex(r"\textbf{Face Recognition Pipeline}", font_size=54)
        line2 = Tex(
            r"\text{What happens when we look into a camera?}",
            size=28,
            color=MUTED
        )

        title_block = VGroup(line1, line2)
        title_block.arrange(DOWN, buff=0.35)
        title_block.move_to(ORIGIN)

        # ─────────────────────────────────────────────────────────────────────
        # ANIMATION SEQUENCE — static camera throughout
        # ─────────────────────────────────────────────────────────────────────

        # ══ BEAT 1 — Static camera, staggered reveal ════════════════════════

        self.play(FadeIn(intuition), run_time=1.0)
        self.wait(0.5)

        self.play(
            FadeIn(brain),
            run_time=1.0,
        )

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

        self.play(FadeIn(face_scan), FadeIn(computer_arrow), run_time=0.8)
        self.wait(0.5)

        self.play(
            FadeIn(left_bracket),
            FadeIn(right_bracket),
            LaggedStart(*[FadeIn(cell) for cell in all_cells], lag_ratio=0.055),
            run_time=2.5,
        )
        self.wait(0.5)

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


# =============================================================================
# SCENE 02 - Face Recognition Pipeline
# =============================================================================

class Scene02_Pipeline(Scene):

    def construct(self):
        """Main animation sequence: intro -> 4 deep dives -> final overview."""
        self.camera.background_color = DARK
        self.frame = self.camera.frame
        self.pipeline = self.create_pipeline()

        self.play_intro_pipeline()
        self.deep_dive_stage_1()
        self.restore_pipeline(highlight_index=0)
        self.deep_dive_stage_2()
        self.restore_pipeline(highlight_index=1)
        self.deep_dive_stage_3()
        self.restore_pipeline(highlight_index=2)
        self.deep_dive_stage_4()
        self.restore_pipeline(highlight_index=3)
        self.final_overview()

    def create_pipeline(self):
        """Build the 5-stage pipeline diagram: Input -> Detection -> Feature -> Matching -> Identity."""
        title = latex(r"\textbf{Face Recognition Pipeline}", size=45)

        stages = VGroup(
            make_box([r"\text{Input}", r"\text{Image / Video}"], width=2.25),
            make_box([r"\text{Detection}", r"\&\ \text{Alignment}"], width=2.45),
            make_box([r"\text{Feature}", r"\text{Extraction}"], width=2.35),
            make_box([r"\text{Matching}", r"/\ \text{Verification}"], width=2.55),
            make_box([r"\text{Identity}", r"\text{Face ID}"], width=2.15),
        )
        stages.arrange(RIGHT, buff=0.58)

        arrows = VGroup()
        for left_box, right_box in zip(stages[:-1], stages[1:]):
            arrows.add(Arrow(left_box.get_right(), right_box.get_left(), buff=0.12, color=CYAN, stroke_width=2.1, max_tip_length_to_length_ratio=0.16))

        db = make_box([r"\text{Database of}", r"\text{Enrolled Users}"], width=2.30, height=0.88, stroke=BLUE, font_size=16)
        db.next_to(stages[3], DOWN, buff=0.50)
        db_arrow = Arrow(stages[3].get_bottom(), db.get_top(), buff=0.10, color=BLUE, stroke_width=1.8, max_tip_length_to_length_ratio=0.22)

        diagram = VGroup(stages, arrows, db, db_arrow)
        whole = VGroup(title, diagram)
        title.to_edge(UP, buff=0.42)
        diagram.center()
        whole.stages = stages
        whole.arrows = arrows
        whole.database = db
        whole.database_arrow = db_arrow
        whole.title = title
        return whole

    def play_intro_pipeline(self):
        """Animate the pipeline diagram appearing: title, then stages one by one, then database."""
        self.frame.set_width(FRAME_WIDTH)
        self.play(FadeIn(self.pipeline.title), run_time=0.8)
        for i, stage in enumerate(self.pipeline.stages):
            self.play(FadeIn(stage), run_time=0.35)
            if i < len(self.pipeline.arrows):
                self.play(GrowArrow(self.pipeline.arrows[i]), run_time=0.28)
        self.play(FadeIn(self.pipeline.database), GrowArrow(self.pipeline.database_arrow), run_time=0.45)
        for stage in self.pipeline.stages[:-1]:
            self.pulse(stage)
        self.wait(0.7)

    def zoom_to_stage_then_black(self, index, title_lines):
        """Zoom into a pipeline stage, fade to black, then show the stage title."""
        target = self.pipeline.stages[index]
        self.play(self.frame.animate.set_width(target.get_width() * 3.0).move_to(target), run_time=0.9)
        self.wait(0.15)
        self.play(FadeOut(self.pipeline), run_time=0.55)
        self.play(self.frame.animate.set_width(FRAME_WIDTH).move_to(ORIGIN), run_time=0.2)

        stage_title = VGroup(*[latex(line, size=size, color=color) for line, size, color in title_lines])
        stage_title.arrange(DOWN, buff=0.16)
        stage_title.to_edge(UP, buff=0.45)
        self.play(FadeIn(stage_title), run_time=0.55)
        return stage_title

    # -------------------------------------------------------------------------
    # STAGE 1: Input Image - Camera captures raw pixels
    # -------------------------------------------------------------------------
    def deep_dive_stage_1(self):
        """Stage 1: Show camera icon capturing image, pixel grid overlay, raw pixel formula."""
        header = self.zoom_to_stage_then_black(0, [
            (r"\text{Stage 1}", 34, CYAN),
            (r"\textbf{Input Image/Video}", 45, WHITE),
        ])

        camera = make_camera_icon()
        camera.scale(1.5)
        face_image = ImageMobject(asset_path("face_scan.png"), height=2.0)
        face_image.scale(2.0)

        upper_line = always_redraw(lambda: DashedLine(
            camera.get_right(),
            face_image.get_left() + UP * 0.85,
            color=CYAN,
            stroke_width=2,
            dash_length=0.08
        ))

        lower_line = always_redraw(lambda: DashedLine(
            camera.get_right(),
            face_image.get_left() + DOWN * 0.85,
            color=CYAN,
            stroke_width=2,
            dash_length=0.08
        ))

        formula = VGroup(
            latex(r"\textbf{Raw pixels}", size=40, color=CYAN),
            latex(r"\mathbf{I}\in\mathbb{R}^{H\times W\times 3}", size=35, color=WHITE),
        ).arrange(DOWN, buff=0.15).move_to(face_image.get_center() + DOWN * 0.5)

        content = Group(camera, upper_line, lower_line, face_image, formula)
        content.arrange(RIGHT, buff=0.55)

        content.set_width(FRAME_WIDTH * 0.92)

        content.next_to(header, DOWN, buff=0.70)
        content.move_to(np.array([0, content.get_center()[1], 0]))

        self.play(FadeIn(camera), run_time=0.45)
        self.play(FadeIn(face_image), run_time=0.65)
        self.play(GrowArrow(upper_line), GrowArrow(lower_line), run_time=0.65)
        self.play(FadeIn(formula), run_time=0.45)
        self.wait(1.2)
        upper_line.clear_updaters()
        lower_line.clear_updaters()
        self.play(FadeOut(Group(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 2: Detection & Alignment - Locate, crop, normalize face pose
    # -------------------------------------------------------------------------
    def deep_dive_stage_2(self):
        """Stage 2: Show face detection flow - locate -> crop -> estimate -> normalize."""
        header = self.zoom_to_stage_then_black(1, [
            (r"\text{Stage 2}", 34, CYAN),
            (r"\textbf{Detection \& Alignment}", 45, WHITE),
        ])

        face_img = ImageMobject(asset_path("detection_alignmemt_face.png"))
        face_img.scale(0.9)

        flow = Group(face_img)
        flow.arrange(RIGHT, buff=0.52)
        flow.move_to(np.array([0, flow.get_center()[1], 0]))
        label_1 = VGroup(
            latex(r"\text{Locate face region}", size=24, color=WHITE),
            latex(r"\text{in the image}", size=24, color=WHITE),
        ).arrange(DOWN, buff=0.05)

        label_1.next_to(flow, DOWN, buff=0.20)
        label_1.set_x(face_img.get_left()[0] + face_img.get_width() * 1/8)

        label_2 = VGroup(
            latex(r"\text{Normalize pose, scale,}", size=24, color=WHITE),
            latex(r"\text{and position}", size=24, color=WHITE),
        ).arrange(DOWN, buff=0.05)
        label_2.next_to(flow, DOWN, buff=0.20)
        label_2.set_x(face_img.get_left()[0] + face_img.get_width() * 7/8)

        content = Group(flow, label_1, label_2)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(face_img), FadeIn(label_1), FadeIn(label_2), run_time=0.65)
        self.wait(1.2)
        self.play(FadeOut(Group(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 3: Feature Extraction - Neural network transforms to embedding
    # -------------------------------------------------------------------------
    def deep_dive_stage_3(self):
        """Stage 3: Show face -> neural network -> embedding vector transformation."""
        header = self.zoom_to_stage_then_black(2, [
            (r"\text{Stage 3}", 34, CYAN),
            (r"\textbf{Feature Extraction}", 45, WHITE),
        ])

        aligned_img = ImageMobject(asset_path("feature_extraction.png"), height=2.2)
        aligned_label = latex(r"\text{Aligned Face}", size=24, color=WHITE)
        aligned = Group(aligned_img, aligned_label)
        aligned.arrange(DOWN, buff=0.15)

        net = make_neural_network().scale(1.5)
        net_label = latex(r"\text{Neural Network}", size=24, color=WHITE)
        net_group = Group(net, net_label)
        net_group.arrange(DOWN, buff=0.15)

        vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31], font_size=24)
        vec.move_to(vec.get_center() + RIGHT * 0.5)
        x_eq = latex(r"\mathbf{x}=", size=24, color=WHITE)
        embedding = VGroup(x_eq, vec).arrange(RIGHT, buff=0.15)
        embedding_label = latex(r"\text{Learned representation}", size=24, color=WHITE)
        embedding_group = VGroup(embedding, embedding_label)
        embedding_group.arrange(DOWN, buff=0.15)

        main = Group(aligned, net_group, embedding_group).arrange(RIGHT, buff=1.2)
        arrows = VGroup(
            Arrow(aligned.get_right(), net_group.get_left(), buff=0.25, color=CYAN, stroke_width=2.5),
            Arrow(net_group.get_right(), embedding_group.get_left(), buff=0.25, color=CYAN, stroke_width=2.5),
        )

        content = Group(main, arrows)
        content.set_width(FRAME_WIDTH * 0.92)
        content.next_to(header, DOWN, buff=0.80)

        self.play(FadeIn(aligned), run_time=0.45)
        self.play(GrowArrow(arrows[0]), FadeIn(net_group), run_time=0.65)
        self.play(GrowArrow(arrows[1]), FadeIn(embedding_group), run_time=0.65)
        self.wait(1.2)
        self.play(FadeOut(Group(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 4: Matching / Verification - Compare embeddings with database
    # -------------------------------------------------------------------------
    def deep_dive_stage_4(self):
        """Stage 4: Show query embedding being compared to database with similarity scores."""
        header = self.zoom_to_stage_then_black(3, [
            (r"\text{Stage 4}", 34, CYAN),
            (r"\textbf{Matching / Verification}", 45, WHITE),
        ])

        query_title = latex(r"\text{Query embedding}", size=24, color=MUTED)
        query_vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31, r"\cdots"], font_size=22)
        query_vec.move_to(query_vec.get_center() + RIGHT * 0.5)
        query = VGroup(query_title, query_vec).arrange(DOWN, buff=0.22)

        rows = VGroup()
        scores = [0.32, 0.18, 0.97, 0.21]

        for idx, score in enumerate(scores):
            row_box = RoundedRectangle(
                width=3.5,
                height=0.55,
                corner_radius=0.08,
                stroke_color=WHITE,
                stroke_width=1.3,
                fill_opacity=0
            )

            user = latex(rf"\text{{User {idx + 1:03d}}}", size=20, color=WHITE)
            sim = latex(rf"{score:.2f}", size=20, color=GREEN if score == max(scores) else WHITE)

            row_content = VGroup(user, sim).arrange(RIGHT, buff=1.3)
            row_content.move_to(row_box)

            row = VGroup(row_box, row_content)

            if score == max(scores):
                row[0].set_stroke(color=GREEN, width=2.5)

            rows.add(row)

        rows.arrange(DOWN, buff=0.18)

        db_title = latex(r"\text{Database of enrolled users}", size=24, color=MUTED)
        database = VGroup(db_title, rows).arrange(DOWN, buff=0.22)

        face_img = ImageMobject(asset_path("face_normal.png"))
        face_img.scale(0.5)

        identity_label = latex(r"\text{Face ID: User 003}", size=24, color=GREEN)

        identity_box = RoundedRectangle(
            width=identity_label.get_width() + 0.45,
            height=identity_label.get_height() + 0.25,
            corner_radius=0.12,
            stroke_color=GREEN,
            stroke_width=2.5,
            fill_opacity=0
        )

        identity_label.move_to(identity_box)

        identity_card = VGroup(identity_box, identity_label)
        identity = Group(face_img, identity_card)

        identity.arrange(DOWN, buff=0.20)

        main = Group(query, database, identity).arrange(RIGHT, buff=1.0)
        main.set_width(FRAME_WIDTH * 0.85)

        formula = latex(
            r"\cos(\theta)=\frac{\mathbf{x}\cdot\mathbf{w}}{|\mathbf{x}||\mathbf{w}|}",
            size=26,
            color=WHITE
        )

        formula_box = RoundedRectangle(
            width=3.8,
            height=0.65,
            corner_radius=0.1,
            stroke_color=CYAN,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.3
        )

        formula.move_to(formula_box)
        formula_group = VGroup(formula_box, formula)

        formula_exp = latex(
            r"\text{higher similarity = closer match}",
            size=20,
            color=CYAN
        )

        formula_row = Group(formula_group, formula_exp).arrange(RIGHT, buff=0.65)
        formula_row.scale(1.25)
        formula_row.next_to(main, DOWN, buff=0.5)
        formula_row.align_to(main, LEFT)
        formula_row.move_to(np.array([0, formula_row.get_center()[1], 0]))

        content = Group(main, formula_row)
        content.next_to(header, DOWN, buff=0.35)
        content.move_to(np.array([0, content.get_center()[1], 0]))

        lines = VGroup()
        target_rows = rows

        for i, row in enumerate(target_rows):
            color = GREEN if i == 2 else MUTED
            opacity = 0.95 if i == 2 else 0.35

            line = DashedLine(
                query_vec.get_right() + RIGHT * 0.08,
                row.get_left() + LEFT * 0.08,
                color=color,
                stroke_width=2.0 if i == 2 else 1.2,
                stroke_opacity=opacity,
                dash_length=0.08
            )

            lines.add(line)

        out_arrow = Arrow(
            rows[2].get_right() + RIGHT * 0.12,
            identity.get_left() + LEFT * 0.12,
            buff=0.0,
            color=GREEN,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.15
        )

        formula_arrow = Arrow(
            formula_group.get_right(),
            formula_exp.get_left(),
            buff=0.05,
            color=CYAN,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )

        self.play(FadeIn(query), run_time=0.45)
        self.play(FadeIn(database), run_time=0.55)

        self.play(
            LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio=0.10),
            run_time=0.75
        )
        self.play(GrowArrow(out_arrow), run_time=0.45)
        self.wait(0.25)
        self.play(FadeIn(identity), run_time=0.45)

        self.play(FadeIn(formula_group), run_time=0.45)
        self.play(GrowArrow(formula_arrow), FadeIn(formula_exp), run_time=0.45)

        self.wait(1.2)

        self.play(
            FadeOut(Group(header, content, lines, formula_arrow, out_arrow)),
            run_time=0.65
        )

    # -------------------------------------------------------------------------
    # PIPELINE RESTORATION & OVERVIEW
    # -------------------------------------------------------------------------
    def restore_pipeline(self, highlight_index=None):
        """Recreate and show the pipeline diagram, optionally highlighting one stage."""
        self.frame.set_width(FRAME_WIDTH)
        self.frame.move_to(ORIGIN)
        self.pipeline = self.create_pipeline()
        self.play(FadeIn(self.pipeline), run_time=0.65)
        if highlight_index is not None:
            self.pulse(self.pipeline.stages[highlight_index])
        self.wait(0.35)

    def final_overview(self):
        """Final sequence: pulse all stages, show closing message, fade out."""
        for i in range(4):
            self.pulse(self.pipeline.stages[i])
        self.pulse(self.pipeline.stages[-1], color=GREEN)
        closing = VGroup(
            latex(r"\text{A journey from pixels to identity.}", size=28, color=CYAN),
            latex(r"\text{This is the foundation of ArcFace.}", size=24, color=WHITE),
        ).arrange(DOWN, buff=0.18)

        closing.scale(1.5)
        closing.next_to(self.pipeline, DOWN, buff=0.40)
        closing.move_to(np.array([0, closing.get_center()[1], 0]))
        self.play(FadeIn(closing), run_time=0.65)
        self.wait(1.0)
        self.play(FadeOut(VGroup(self.pipeline, closing)), run_time=0.9)

    # -------------------------------------------------------------------------
    # ANIMATION HELPERS
    # -------------------------------------------------------------------------
    def pulse(self, stage, color=CYAN):
        """Create a highlight pulse effect on a stage box (for emphasis)."""
        outline = stage[0]
        halo = glow_copy(outline, color=color)
        self.add(halo, outline)
        self.play(
            outline.animate.set_stroke(color=color, width=3.4),
            halo.animate.set_stroke(opacity=0.30),
            run_time=0.18,
        )
        self.play(
            outline.animate.set_stroke(color=color, width=2.0),
            FadeOut(halo),
            run_time=0.24,
        )

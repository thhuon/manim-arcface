from manimlib import *
import os
import random
from scenes.utils import *


# =============================================================================
# ADDITIONAL HELPERS - SVG specific to scene02
# =============================================================================

def safe_svg(filename: str, scale_factor: float = 1.0, stroke_color=WHITE):
    """Load SVG with stroke-only style (no fill), returns None if file missing."""
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    obj = SVGMobject(file_name=path)
    obj.set_fill(opacity=0)
    obj.set_stroke(color=stroke_color, width=1.5)
    obj.scale(scale_factor)
    return obj


# =============================================================================
# MAIN SCENE CLASS - Face Recognition Pipeline Animation
# =============================================================================

class Scene02_FaceRecognitionPipeline(Scene):

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
        title = latex(r"\textbf{Face Recognition Pipeline}", size=38)

        stages = VGroup(
            make_box([r"\text{Input}", r"\text{Image / Video}"], width=2.25),
            make_box([r"\text{Detection}", r"\&\ \text{Alignment}"], width=2.45),
            make_box([r"\text{Feature}", r"\text{Extraction}"], width=2.35),
            make_box([r"\text{Matching}", r"/\ \text{Verification}"], width=2.55),
            make_box([r"\text{Identity}", r"\text{Face ID}"], width=2.15),
        )
        stages.arrange(RIGHT, buff=0.58)
        stages.center()  # Center the stages horizontally

        arrows = VGroup()
        for left_box, right_box in zip(stages[:-1], stages[1:]):
            arrows.add(Arrow(left_box.get_right(), right_box.get_left(), buff=0.12, color=CYAN, stroke_width=2.1, max_tip_length_to_length_ratio=0.16))

        db = make_box([r"\text{Database of}", r"\text{Enrolled Users}"], width=2.30, height=0.88, stroke=BLUE, font_size=16)
        db.next_to(stages[3], DOWN, buff=0.50)
        db_arrow = Arrow(stages[3].get_bottom(), db.get_top(), buff=0.10, color=BLUE, stroke_width=1.8, max_tip_length_to_length_ratio=0.22)

        diagram = VGroup(stages, arrows, db, db_arrow)
        whole = VGroup(title, diagram)
        whole.arrange(DOWN, buff=0.55)
        whole.to_edge(UP, buff=0.42)  # Position the whole diagram at the top of the screen
        whole.stages = stages
        whole.arrows = arrows
        whole.database = db
        whole.database_arrow = db_arrow
        whole.title = title
        return whole

    def play_intro_pipeline(self):
        """Animate the pipeline diagram appearing: title, then stages one by one, then database."""
        self.frame.set_width(FRAME_WIDTH)  # Set the frame width to the full width of the screen
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
            (r"\textbf{Stage 1}", 42, CYAN),
            (r"\text{Input Image/Video}", 34, WHITE),
        ])

        camera = make_camera_icon()
        face_image = ImageMobject(asset_path("face_scan.png")).set_height(2.0)

        left_line = Line(camera.get_right(), face_image.get_left(), color=CYAN, stroke_width=2)
        right_line = Line(camera.get_right(), face_image.get_right(), color=CYAN, stroke_width=2)

        formula = VGroup(
            latex(r"\text{Raw pixels}", size=24, color=MUTED),
            latex(r"\mathbf{I}\in\mathbb{R}^{H\times W\times 3}", size=27, color=WHITE),
        ).arrange(DOWN, buff=0.15)

        content = Group(camera, left_line, right_line, face_image, formula)
        content.arrange(RIGHT, buff=0.55)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(camera), run_time=0.45)
        self.play(FadeIn(face_image), run_time=0.65)
        self.play(GrowArrow(left_line), GrowArrow(right_line), run_time=0.65)
        self.play(FadeIn(formula), run_time=0.45)
        self.wait(1.2)
        self.play(FadeOut(Group(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 2: Detection & Alignment - Locate, crop, normalize face pose
    # -------------------------------------------------------------------------
    def deep_dive_stage_2(self):
        """Stage 2: Show face detection flow - locate -> crop -> estimate -> normalize."""
        header = self.zoom_to_stage_then_black(1, [
            (r"\textbf{Stage 2}", 34, CYAN),
            (r"\text{Detection \& Alignment}", 45, WHITE),
        ])

        # Replace all face graphics with single image
        face_img = ImageMobject(asset_path("detection_alignment_face.png")).set_height(2.2)

        flow = Group(face_img)
        flow.arrange(RIGHT, buff=0.52)
        labels = VGroup(
            latex(r"\text{Face Detection \& Alignment}", size=19, color=MUTED),
        )
        labels.next_to(flow, DOWN, buff=0.20)

        content = Group(flow, labels)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(face_img), FadeIn(labels), run_time=0.65)
        self.wait(1.2)
        self.play(FadeOut(Group(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 3: Feature Extraction - Neural network transforms to embedding
    # -------------------------------------------------------------------------
    def deep_dive_stage_3(self):
        """Stage 3: Show face -> neural network -> embedding vector transformation."""
        header = self.zoom_to_stage_then_black(2, [
            (r"\textbf{Stage 3}", 34, CYAN),
            (r"\text{Feature Extraction}", 45, WHITE),
        ])

        aligned = VGroup(
            RoundedRectangle(width=1.55, height=1.78, corner_radius=0.12, stroke_color=WHITE, stroke_width=1.8, fill_opacity=0),
            make_abstract_face().scale(0.58),
        )
        aligned[1].move_to(aligned[0])
        net = make_neural_network()
        vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31], font_size=20)
        x_eq = latex(r"\mathbf{x}=", size=28)
        embedding = VGroup(x_eq, vec).arrange(RIGHT, buff=0.15)

        feature_tiles = VGroup(*[
            Square(side_length=0.28, stroke_color=MUTED, stroke_width=1.0, fill_color=WHITE, fill_opacity=0.05)
            for _ in range(6)
        ])
        feature_tiles.arrange(RIGHT, buff=0.10)
        tile_label = latex(r"\text{local patterns }\rightarrow\text{ learned representation}", size=20, color=MUTED)
        lower = VGroup(feature_tiles, tile_label).arrange(DOWN, buff=0.16)

        main = VGroup(aligned, net, embedding).arrange(RIGHT, buff=0.62)
        arrows = VGroup(
            Arrow(aligned.get_right(), net.get_left(), buff=0.18, color=CYAN, stroke_width=2),
            Arrow(net.get_right(), embedding.get_left(), buff=0.18, color=CYAN, stroke_width=2),
        )
        content = VGroup(main, arrows, lower).arrange(DOWN, buff=0.42)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(aligned), run_time=0.45)
        self.play(GrowArrow(arrows[0]), FadeIn(net), run_time=0.65)
        self.play(GrowArrow(arrows[1]), FadeIn(embedding), run_time=0.65)
        self.play(FadeIn(lower), run_time=0.45)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 4: Matching / Verification - Compare embeddings with database
    # -------------------------------------------------------------------------
    def deep_dive_stage_4(self):
        """Stage 4: Show query embedding being compared to database with similarity scores."""
        header = self.zoom_to_stage_then_black(3, [
            (r"\textbf{Stage 4}", 34, CYAN),
            (r"\text{Matching / Verification}", 45, WHITE),
        ])

        query_title = latex(r"\text{Query embedding}", size=20, color=MUTED)
        query_vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31], font_size=18)
        query = VGroup(query_title, query_vec).arrange(DOWN, buff=0.18)

        rows = VGroup()
        scores = [0.32, 0.18, 0.97, 0.21]
        for idx, score in enumerate(scores):
            row_box = RoundedRectangle(width=2.95, height=0.45, corner_radius=0.07, stroke_color=MUTED, stroke_width=1.1, fill_opacity=0)
            user = latex(rf"\text{{User {idx + 1:03d}}}", size=16, color=WHITE)
            sim = latex(rf"{score:.2f}", size=16, color=GREEN if score == max(scores) else MUTED)
            row_content = VGroup(user, sim).arrange(RIGHT, buff=1.05)
            row_content.move_to(row_box)
            row = VGroup(row_box, row_content)
            if score == max(scores):
                row[0].set_stroke(color=GREEN, width=2.0)
            rows.add(row)
        rows.arrange(DOWN, buff=0.12)
        db_title = latex(r"\text{Database of enrolled users}", size=19, color=MUTED)
        database = VGroup(db_title, rows).arrange(DOWN, buff=0.18)

        identity = VGroup(
            RoundedRectangle(width=1.92, height=0.90, corner_radius=0.10, stroke_color=GREEN, stroke_width=2.0, fill_opacity=0),
            latex(r"\text{Face ID: User 003}", size=20, color=GREEN),
        )
        identity[1].move_to(identity[0])

        main = VGroup(query, database, identity).arrange(RIGHT, buff=0.52)
        lines = VGroup()
        for i, row in enumerate(rows):
            color = GREEN if i == 2 else MUTED
            opacity = 0.95 if i == 2 else 0.35
            lines.add(DashedLine(query_vec.get_right(), row.get_left(), color=color, stroke_width=1.7 if i == 2 else 1.0, stroke_opacity=opacity))
        out_arrow = Arrow(database.get_right(), identity.get_left(), buff=0.16, color=GREEN, stroke_width=2.0)
        formula = latex(r"\cos(\theta)=\frac{\mathbf{x}\cdot\mathbf{w}}{|\mathbf{x}||\mathbf{w}|}", size=24, color=MUTED)
        formula.next_to(main, DOWN, buff=0.42)

        content = VGroup(main, lines, out_arrow, formula)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(query), run_time=0.45)
        self.play(FadeIn(database), run_time=0.55)
        self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio=0.10), run_time=0.75)
        self.play(GrowArrow(out_arrow), FadeIn(identity), run_time=0.55)
        self.play(FadeIn(formula), run_time=0.45)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, content)), run_time=0.65)

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
        closing.next_to(self.pipeline, DOWN, buff=0.40)
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
# from manimlib import *
# import os
# import random
# from scenes.utils import *


# # =============================================================================
# # ADDITIONAL HELPERS - SVG specific to scene02
# # =============================================================================

# def safe_svg(filename: str, scale_factor: float = 1.0, stroke_color=WHITE):
#     """Load SVG with stroke-only style (no fill), returns None if file missing."""
#     path = asset_path(filename)
#     if not os.path.exists(path):
#         return None
#     obj = SVGMobject(file_name=path)
#     obj.set_fill(opacity=0)
#     obj.set_stroke(color=stroke_color, width=1.5)
#     obj.scale(scale_factor)
#     return obj


# # =============================================================================
# # MAIN SCENE CLASS - Face Recognition Pipeline Animation
# # =============================================================================

# class Scene02_FaceRecognitionPipeline(Scene):

#     def construct(self):
#         """Main animation sequence: intro -> 4 deep dives -> final overview."""
#         self.camera.background_color = DARK
#         self.frame = self.camera.frame
#         self.pipeline = self.create_pipeline()

#         self.play_intro_pipeline()
#         self.deep_dive_stage_1()
#         self.restore_pipeline(highlight_index=0)
#         self.deep_dive_stage_2()
#         self.restore_pipeline(highlight_index=1)
#         self.deep_dive_stage_3()
#         self.restore_pipeline(highlight_index=2)
#         self.deep_dive_stage_4()
#         self.restore_pipeline(highlight_index=3)
#         self.final_overview()

#     def create_pipeline(self):
#         """Build the 5-stage pipeline diagram: Input -> Detection -> Feature -> Matching -> Identity."""
#         title = latex(r"\textbf{Face Recognition Pipeline}", size=38)

#         stages = VGroup(
#             make_box([r"\text{Input}", r"\text{Image / Video}"], width=2.25),
#             make_box([r"\text{Detection}", r"\&\ \text{Alignment}"], width=2.45),
#             make_box([r"\text{Feature}", r"\text{Extraction}"], width=2.35),
#             make_box([r"\text{Matching}", r"/\ \text{Verification}"], width=2.55),
#             make_box([r"\text{Identity}", r"\text{Face ID}"], width=2.15),
#         )
#         stages.arrange(RIGHT, buff=0.58)
#         stages.center()  # Center the stages horizontally

#         arrows = VGroup()
#         for left_box, right_box in zip(stages[:-1], stages[1:]):
#             arrows.add(Arrow(left_box.get_right(), right_box.get_left(), buff=0.12, color=CYAN, stroke_width=2.1, max_tip_length_to_length_ratio=0.16))

#         db = make_box([r"\text{Database of}", r"\text{Enrolled Users}"], width=2.30, height=0.88, stroke=BLUE, font_size=16)
#         db.next_to(stages[3], DOWN, buff=0.50)
#         db_arrow = Arrow(stages[3].get_bottom(), db.get_top(), buff=0.10, color=BLUE, stroke_width=1.8, max_tip_length_to_length_ratio=0.22)

#         diagram = VGroup(stages, arrows, db, db_arrow)
#         whole = VGroup(title, diagram)
#         whole.arrange(DOWN, buff=0.55)
#         whole.to_edge(UP, buff=0.42)  # Position the whole diagram at the top of the screen
#         whole.stages = stages
#         whole.arrows = arrows
#         whole.database = db
#         whole.database_arrow = db_arrow
#         whole.title = title
#         return whole

#     def play_intro_pipeline(self):
#         """Animate the pipeline diagram appearing: title, then stages one by one, then database."""
#         self.frame.set_width(FRAME_WIDTH)  # Set the frame width to the full width of the screen
#         self.play(FadeIn(self.pipeline.title), run_time=0.8)
#         for i, stage in enumerate(self.pipeline.stages):
#             self.play(FadeIn(stage), run_time=0.35)
#             if i < len(self.pipeline.arrows):
#                 self.play(GrowArrow(self.pipeline.arrows[i]), run_time=0.28)
#         self.play(FadeIn(self.pipeline.database), GrowArrow(self.pipeline.database_arrow), run_time=0.45)
#         for stage in self.pipeline.stages[:-1]:
#             self.pulse(stage)
#         self.wait(0.7)

#     def zoom_to_stage_then_black(self, index, title_lines):
#         """Zoom into a pipeline stage, fade to black, then show the stage title."""
#         target = self.pipeline.stages[index]
#         self.play(self.frame.animate.set_width(target.get_width() * 3.0).move_to(target), run_time=0.9)
#         self.wait(0.15)
#         self.play(FadeOut(self.pipeline), run_time=0.55)
#         self.play(self.frame.animate.set_width(FRAME_WIDTH).move_to(ORIGIN), run_time=0.2)

#         stage_title = VGroup(*[latex(line, size=size, color=color) for line, size, color in title_lines])
#         stage_title.arrange(DOWN, buff=0.16)
#         stage_title.to_edge(UP, buff=0.45)
#         self.play(FadeIn(stage_title), run_time=0.55)
#         return stage_title

#     # -------------------------------------------------------------------------
#     # STAGE 1: Input Image - Camera captures raw pixels
#     # -------------------------------------------------------------------------
#     def deep_dive_stage_1(self):
#         """Stage 1: Show camera icon capturing image, pixel grid overlay, raw pixel formula."""
#         header = self.zoom_to_stage_then_black(0, [
#             (r"\textbf{Stage 1}", 42, CYAN),
#             (r"\text{Input Image/Video}", 34, WHITE),
#         ])

#         camera = make_camera_icon()
#         face_image = ImageMobject(asset_path("face_scan.png")).scale_to_height(2.0)

#         left_line = Line(camera.get_right(), face_image.get_left(), color=CYAN, stroke_width=2)
#         right_line = Line(camera.get_right(), face_image.get_right(), color=CYAN, stroke_width=2)

#         formula = VGroup(
#             latex(r"\text{Raw pixels}", size=24, color=MUTED),
#             latex(r"\mathbf{I}\in\mathbb{R}^{H\times W\times 3}", size=27, color=WHITE),
#         ).arrange(DOWN, buff=0.15)

#         content = VGroup(camera, left_line, right_line, face_image, formula)
#         content.arrange(RIGHT, buff=0.55)
#         content.next_to(header, DOWN, buff=0.70)

#         self.play(FadeIn(camera), run_time=0.45)
#         self.play(FadeIn(face_image), run_time=0.65)
#         self.play(GrowArrow(left_line), GrowArrow(right_line), run_time=0.65)
#         self.play(FadeIn(formula), run_time=0.45)
#         self.wait(1.2)
#         self.play(FadeOut(VGroup(header, content)), run_time=0.65)

#     # -------------------------------------------------------------------------
#     # STAGE 2: Detection & Alignment - Locate, crop, normalize face pose
#     # -------------------------------------------------------------------------
#     def deep_dive_stage_2(self):
#         """Stage 2: Show face detection flow - locate -> crop -> estimate -> normalize."""
#         header = self.zoom_to_stage_then_black(1, [
#             (r"\textbf{Stage 2}", 34, CYAN),
#             (r"\text{Detection \& Alignment}", 45, WHITE),
#         ])

#         # Replace all face graphics with single image
#         face_img = ImageMobject(asset_path("detection_alignment_face.png")).scale_to_height(2.2)

#         flow = VGroup(face_img)
#         flow.arrange(RIGHT, buff=0.52)
#         labels = VGroup(
#             latex(r"\text{Face Detection \& Alignment}", size=19, color=MUTED),
#         )
#         labels.next_to(flow, DOWN, buff=0.20)

#         content = VGroup(flow, labels)
#         content.next_to(header, DOWN, buff=0.70)

#         self.play(FadeIn(face_img), FadeIn(labels), run_time=0.65)
#         self.wait(1.2)
#         self.play(FadeOut(VGroup(header, content)), run_time=0.65)

#     # -------------------------------------------------------------------------
#     # STAGE 3: Feature Extraction - Neural network transforms to embedding
#     # -------------------------------------------------------------------------
#     def deep_dive_stage_3(self):
#         """Stage 3: Show face -> neural network -> embedding vector transformation."""
#         header = self.zoom_to_stage_then_black(2, [
#             (r"\textbf{Stage 3}", 34, CYAN),
#             (r"\text{Feature Extraction}", 45, WHITE),
#         ])

#         aligned = VGroup(
#             RoundedRectangle(width=1.55, height=1.78, corner_radius=0.12, stroke_color=WHITE, stroke_width=1.8, fill_opacity=0),
#             make_abstract_face().scale(0.58),
#         )
#         aligned[1].move_to(aligned[0])
#         net = make_neural_network()
#         vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31], font_size=20)
#         x_eq = latex(r"\mathbf{x}=", size=28)
#         embedding = VGroup(x_eq, vec).arrange(RIGHT, buff=0.15)

#         feature_tiles = VGroup(*[
#             Square(side_length=0.28, stroke_color=MUTED, stroke_width=1.0, fill_color=WHITE, fill_opacity=0.05)
#             for _ in range(6)
#         ])
#         feature_tiles.arrange(RIGHT, buff=0.10)
#         tile_label = latex(r"\text{local patterns }\rightarrow\text{ learned representation}", size=20, color=MUTED)
#         lower = VGroup(feature_tiles, tile_label).arrange(DOWN, buff=0.16)

#         main = VGroup(aligned, net, embedding).arrange(RIGHT, buff=0.62)
#         arrows = VGroup(
#             Arrow(aligned.get_right(), net.get_left(), buff=0.18, color=CYAN, stroke_width=2),
#             Arrow(net.get_right(), embedding.get_left(), buff=0.18, color=CYAN, stroke_width=2),
#         )
#         content = VGroup(main, arrows, lower).arrange(DOWN, buff=0.42)
#         content.next_to(header, DOWN, buff=0.70)

#         self.play(FadeIn(aligned), run_time=0.45)
#         self.play(GrowArrow(arrows[0]), FadeIn(net), run_time=0.65)
#         self.play(GrowArrow(arrows[1]), FadeIn(embedding), run_time=0.65)
#         self.play(FadeIn(lower), run_time=0.45)
#         self.wait(1.2)
#         self.play(FadeOut(VGroup(header, content)), run_time=0.65)

#     # -------------------------------------------------------------------------
#     # STAGE 4: Matching / Verification - Compare embeddings with database
#     # -------------------------------------------------------------------------
#     def deep_dive_stage_4(self):
#         """Stage 4: Show query embedding being compared to database with similarity scores."""
#         header = self.zoom_to_stage_then_black(3, [
#             (r"\textbf{Stage 4}", 34, CYAN),
#             (r"\text{Matching / Verification}", 45, WHITE),
#         ])

#         query_title = latex(r"\text{Query embedding}", size=20, color=MUTED)
#         query_vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31], font_size=18)
#         query = VGroup(query_title, query_vec).arrange(DOWN, buff=0.18)

#         rows = VGroup()
#         scores = [0.32, 0.18, 0.97, 0.21]
#         for idx, score in enumerate(scores):
#             row_box = RoundedRectangle(width=2.95, height=0.45, corner_radius=0.07, stroke_color=MUTED, stroke_width=1.1, fill_opacity=0)
#             user = latex(rf"\text{{User {idx + 1:03d}}}", size=16, color=WHITE)
#             sim = latex(rf"{score:.2f}", size=16, color=GREEN if score == max(scores) else MUTED)
#             row_content = VGroup(user, sim).arrange(RIGHT, buff=1.05)
#             row_content.move_to(row_box)
#             row = VGroup(row_box, row_content)
#             if score == max(scores):
#                 row[0].set_stroke(color=GREEN, width=2.0)
#             rows.add(row)
#         rows.arrange(DOWN, buff=0.12)
#         db_title = latex(r"\text{Database of enrolled users}", size=19, color=MUTED)
#         database = VGroup(db_title, rows).arrange(DOWN, buff=0.18)

#         identity = VGroup(
#             RoundedRectangle(width=1.92, height=0.90, corner_radius=0.10, stroke_color=GREEN, stroke_width=2.0, fill_opacity=0),
#             latex(r"\text{Face ID: User 003}", size=20, color=GREEN),
#         )
#         identity[1].move_to(identity[0])

#         main = VGroup(query, database, identity).arrange(RIGHT, buff=0.52)
#         lines = VGroup()
#         for i, row in enumerate(rows):
#             color = GREEN if i == 2 else MUTED
#             opacity = 0.95 if i == 2 else 0.35
#             lines.add(DashedLine(query_vec.get_right(), row.get_left(), color=color, stroke_width=1.7 if i == 2 else 1.0, stroke_opacity=opacity))
#         out_arrow = Arrow(database.get_right(), identity.get_left(), buff=0.16, color=GREEN, stroke_width=2.0)
#         formula = latex(r"\cos(\theta)=\frac{\mathbf{x}\cdot\mathbf{w}}{|\mathbf{x}||\mathbf{w}|}", size=24, color=MUTED)
#         formula.next_to(main, DOWN, buff=0.42)

#         content = VGroup(main, lines, out_arrow, formula)
#         content.next_to(header, DOWN, buff=0.70)

#         self.play(FadeIn(query), run_time=0.45)
#         self.play(FadeIn(database), run_time=0.55)
#         self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio=0.10), run_time=0.75)
#         self.play(GrowArrow(out_arrow), FadeIn(identity), run_time=0.55)
#         self.play(FadeIn(formula), run_time=0.45)
#         self.wait(1.2)
#         self.play(FadeOut(VGroup(header, content)), run_time=0.65)

#     # -------------------------------------------------------------------------
#     # PIPELINE RESTORATION & OVERVIEW
#     # -------------------------------------------------------------------------
#     def restore_pipeline(self, highlight_index=None):
#         """Recreate and show the pipeline diagram, optionally highlighting one stage."""
#         self.frame.set_width(FRAME_WIDTH)
#         self.frame.move_to(ORIGIN)
#         self.pipeline = self.create_pipeline()
#         self.play(FadeIn(self.pipeline), run_time=0.65)
#         if highlight_index is not None:
#             self.pulse(self.pipeline.stages[highlight_index])
#         self.wait(0.35)

#     def final_overview(self):
#         """Final sequence: pulse all stages, show closing message, fade out."""
#         for i in range(4):
#             self.pulse(self.pipeline.stages[i])
#         self.pulse(self.pipeline.stages[-1], color=GREEN)
#         closing = VGroup(
#             latex(r"\text{A journey from pixels to identity.}", size=28, color=CYAN),
#             latex(r"\text{This is the foundation of ArcFace.}", size=24, color=WHITE),
#         ).arrange(DOWN, buff=0.18)
#         closing.next_to(self.pipeline, DOWN, buff=0.40)
#         self.play(FadeIn(closing), run_time=0.65)
#         self.wait(1.0)
#         self.play(FadeOut(VGroup(self.pipeline, closing)), run_time=0.9)

#     # -------------------------------------------------------------------------
#     # ANIMATION HELPERS
#     # -------------------------------------------------------------------------
#     def pulse(self, stage, color=CYAN):
#         """Create a highlight pulse effect on a stage box (for emphasis)."""
#         outline = stage[0]
#         halo = glow_copy(outline, color=color)
#         self.add(halo, outline)
#         self.play(
#             outline.animate.set_stroke(color=color, width=3.4),
#             halo.animate.set_stroke(opacity=0.30),
#             run_time=0.18,
#         )
#         self.play(
#             outline.animate.set_stroke(color=color, width=2.0),
#             FadeOut(halo),
#             run_time=0.24,
#         )

from typing import Any
from manimlib import *
import os
import random


# =============================================================================
# COLOR PALETTE - Consistent throughout the scene for visual harmony
# =============================================================================

CYAN = "#00D4FF"
BLUE = "#4A7DFF"
WHITE = "#F2F6FF"
MUTED = "#8A94A6"
DARK = "#090D14"
PANEL = "#101722"
GREEN = "#3EF7A0" 


# =============================================================================
# UTILITY FUNCTIONS - Path resolution and SVG helpers
# =============================================================================

def asset_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "decorations", filename)


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
# HELPER FUNCTIONS - Basic building blocks for UI elements
# =============================================================================

def latex(text: str, size: int = 28, color=WHITE):
    """Create a styled LaTeX text element with consistent coloring."""
    obj = Tex(text, font_size=size)
    obj.set_color(color)
    return obj


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


def glow_copy(mob, color=CYAN, width=7, opacity=0.18):
    """Create a copy with soft glow effect (for highlight animations)."""
    g = mob.copy()
    g.set_stroke(color=color, width=width, opacity=opacity)
    return g


# =============================================================================
# VISUAL ELEMENT FACTORIES - Build reusable graphic components
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


def make_vector(values, font_size=19):
    """Create a column vector display with brackets around values."""
    entries = VGroup(*[latex(str(v), size=font_size) for v in values])
    entries.arrange(DOWN, buff=0.08)
    left = Line(entries.get_corner(UL) + 0.10 * LEFT, entries.get_corner(DL) + 0.10 * LEFT, stroke_color=WHITE, stroke_width=1.4)
    right = Line(entries.get_corner(UR) + 0.10 * RIGHT, entries.get_corner(DR) + 0.10 * RIGHT, stroke_color=WHITE, stroke_width=1.4)
    return VGroup(left, entries, right)


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
        # Title stays at top, diagram centered on screen
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
        # upper_line = DashedLine(camera.get_top(), face_image.get_top(), color=CYAN, stroke_width=2).rotate(30 * DEGREES) # up to 30 degrees
        # lower_line = DashedLine(camera.get_bottom(), face_image.get_bottom(), color=CYAN, stroke_width=2).rotate(-30 * DEGREES) # down to 30 degrees

        formula = VGroup(
            latex(r"\textbf{Raw pixels}", size=40, color=CYAN),  
            latex(r"\mathbf{I}\in\mathbb{R}^{H\times W\times 3}", size=35, color=WHITE),
        ).arrange(DOWN, buff=0.15).move_to(face_image.get_center() + DOWN * 0.5)

        content = Group(camera, upper_line, lower_line, face_image, formula)
        content.arrange(RIGHT, buff=0.55)

        content.set_width(FRAME_WIDTH * 0.92) # make sure the content is within the frame

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

        # Replace all face graphics with single image
        face_img = ImageMobject(asset_path("detection_alignment_face.png"))
        face_img.scale(0.9)

        flow = Group(face_img)
        flow.arrange(RIGHT, buff=0.52)
        # center the flow in the frame
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

        # Replace face graphic with aligned face image
        aligned_img = ImageMobject(asset_path("feature_extraction.png"), height=2.2)
        aligned_label = latex(r"\text{Aligned Face}", size=24, color=WHITE)
        aligned = Group(aligned_img, aligned_label)
        aligned.arrange(DOWN, buff=0.15)

        # Larger neural network
        net = make_neural_network().scale(1.5)
        net_label = latex(r"\text{Neural Network}", size=24, color=WHITE)
        net_group = Group(net, net_label)
        net_group.arrange(DOWN, buff=0.15)

        # Larger embedding vector
        vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31], font_size=24)
        # make the vector longer
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
        content.set_width(FRAME_WIDTH * 0.92) # make sure the content is within the frame
        content.next_to(header, DOWN, buff=0.80)

        self.play(FadeIn(aligned), run_time=0.45)
        self.play(GrowArrow(arrows[0]), FadeIn(net_group), run_time=0.65)
        self.play(GrowArrow(arrows[1]), FadeIn(embedding_group), run_time=0.65)
        self.wait(1.2)
        self.play(FadeOut(Group(header, content)), run_time=0.65)

    # -------------------------------------------------------------------------
    # STAGE 4: Matching / Verification - Compare embeddings with database
    # -------------------------------------------------------------------------
    # def deep_dive_stage_4(self):
    #     """Stage 4: Show query embedding being compared to database with similarity scores."""
    #     header = self.zoom_to_stage_then_black(3, [
    #         (r"\text{Stage 4}", 34, CYAN),
    #         (r"\textbf{Matching / Verification}", 45, WHITE),
    #     ])

    #     # Scale up query vector
    #     query_title = latex(r"\text{Query embedding}", size=24, color=MUTED)
    #     query_vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31, r"\cdots"], font_size=22)
    #     query_vec.move_to(query_vec.get_center() + RIGHT * 0.5)
    #     query = VGroup(query_title, query_vec).arrange(DOWN, buff=0.22)

    #     # Scale up database rows
    #     rows = VGroup()
    #     scores = [0.32, 0.18, 0.97, 0.21]
    #     for idx, score in enumerate(scores):
    #         row_box = RoundedRectangle(width=3.5, height=0.55, corner_radius=0.08, stroke_color=WHITE, stroke_width=1.3, fill_opacity=0)
    #         user = latex(rf"\text{{User {idx + 1:03d}}}", size=20, color=WHITE)
    #         sim = latex(rf"{score:.2f}", size=20, color=GREEN if score == max(scores) else WHITE)
    #         row_content = VGroup(user, sim).arrange(RIGHT, buff=1.3)
    #         row_content.move_to(row_box)
    #         row = VGroup(row_box, row_content)
    #         if score == max(scores):
    #             row[0].set_stroke(color=GREEN, width=2.5)
    #         rows.add(row)
    #     rows.arrange(DOWN, buff=0.18)
    #     db_title = latex(r"\text{Database of enrolled users}", size=24, color=MUTED)
    #     database = VGroup(db_title, rows).arrange(DOWN, buff=0.22)

    #     # Add face image above Face ID
    #     face_img = ImageMobject(asset_path("face_normal.png"))
    #     face_img.scale(0.5)
    #     identity_label = latex(r"\text{Face ID: User 003}", size=24, color=GREEN)
    #     identity_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.12, stroke_color=GREEN, stroke_width=2.5, fill_opacity=0)
    #     identity_label.move_to(identity_box)
    #     identity_card = VGroup(identity_box, identity_label)
    #     identity = Group(face_img, identity_card)
    #     # identity.next_to(face_img.get_center() + DOWN * 1.25)
    #     identity.arrange(DOWN, buff=0.20)

    #     # Main layout with scaled components
    #     main = Group(query, database, identity).arrange(RIGHT, buff=1.0)
    #     main.set_width(FRAME_WIDTH * 0.85) # make sure the content is within the frame

    #     # Connection lines from query to database
    #     lines = VGroup[DashedLine]()
    #     target_rows = rows

    #     for i, row in enumerate(target_rows):
    #         color = GREEN if i == 2 else MUTED
    #         opacity = 0.95 if i == 2 else 0.35

    #         line = always_redraw(lambda row=row, i=i, color=color, opacity=opacity: DashedLine(
    #             query_vec.get_right() + RIGHT * 0.08,
    #             row.get_left() + LEFT * 0.08,
    #             color=color,
    #             stroke_width=2.0 if i == 2 else 1.2,
    #             stroke_opacity=opacity,
    #             dash_length=0.08
    #         ))

    #         lines.add(line)
            
    #     out_arrow = Arrow(database.get_right(), identity.get_left(), buff=0.2, color=GREEN, stroke_width=2.5)

    #     # Arrow from query to database
    #     query_db_arrow = Arrow(
    #         query.get_right() + RIGHT * 0.1,
    #         database.get_left() + LEFT * 0.1,
    #         buff=0.0,
    #         color=CYAN,
    #         stroke_width=2,
    #         max_tip_length_to_length_ratio=0.15
    #     )


    #     # Formula with box and arrow to explanation
    #     formula = latex(r"\cos(\theta)=\frac{\mathbf{x}\cdot\mathbf{w}}{|\mathbf{x}||\mathbf{w}|}", size=28, color=WHITE)
    #     formula_box = RoundedRectangle(width=3.8, height=0.65, corner_radius=0.1, stroke_color=CYAN, stroke_width=2, fill_color=PANEL, fill_opacity=0.3)
    #     formula.move_to(formula_box)
    #     formula_group = VGroup(formula_box, formula)

    #     formula_exp = latex(r"\text{higher similarity = closer match}", size=22, color=CYAN)
    #     formula_exp.next_to(formula_group, RIGHT, buff=0.4)

    #     formula_arrow = Arrow(
    #         formula_group.get_right(),
    #         formula_exp.get_left(),
    #         buff=0.05,
    #         color=CYAN,
    #         stroke_width=2,
    #         max_tip_length_to_length_ratio=0.2
    #     )

    #     content = Group(main, lines, query_db_arrow, out_arrow, formula_group, formula_arrow, formula_exp)
    #     content.arrange(DOWN, buff=0.40)
    #     content.next_to(header, DOWN, buff=0.60)
    #     content.move_to(np.array([0, content.get_center()[1], 0])) # center the content in the frame

    #     self.play(FadeIn(query), run_time=0.45)
    #     self.play(FadeIn(database), run_time=0.55)
    #     self.play(GrowArrow(query_db_arrow), run_time=0.45)
    #     self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio=0.10), run_time=0.75)
    #     self.play(GrowArrow(out_arrow), FadeIn(identity), run_time=0.55)
    #     self.play(FadeIn(formula_group), run_time=0.45)
    #     self.play(GrowArrow(formula_arrow), FadeIn(formula_exp), run_time=0.45)
    #     self.wait(1.2)
    #     lines.clear_updaters()    
    #     self.play(FadeOut(Group(header, content)), run_time=0.65)
    def deep_dive_stage_4(self):
        """Stage 4: Show query embedding being compared to database with similarity scores."""
        header = self.zoom_to_stage_then_black(3, [
            (r"\text{Stage 4}", 34, CYAN),
            (r"\textbf{Matching / Verification}", 45, WHITE),
        ])

        # Scale up query vector
        query_title = latex(r"\text{Query embedding}", size=24, color=MUTED)
        query_vec = make_vector([0.12, -0.45, 0.83, r"\cdots", 0.23, -0.31, r"\cdots"], font_size=22)
        query_vec.move_to(query_vec.get_center() + RIGHT * 0.5)
        query = VGroup(query_title, query_vec).arrange(DOWN, buff=0.22)

        # Scale up database rows
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

        # Add face image above Face ID
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

        # identity_card nằm bên dưới face_img
        identity.arrange(DOWN, buff=0.20)

        # Main layout with scaled components
        main = Group(query, database, identity).arrange(RIGHT, buff=1.0)
        main.set_width(FRAME_WIDTH * 0.85)  # make sure the content is within the frame

        # Formula with box and arrow to explanation
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
        formula_row.move_to(np.array([0, formula_row.get_center()[1], 0]))   # make the formular in the center of the frame

        content = Group(main, formula_row)
        content.next_to(header, DOWN, buff=0.35)
        content.move_to(np.array([0, content.get_center()[1], 0]))  # center the content in the frame

        # Connection lines from query to database
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
  
        # Arrow from database to identity
        out_arrow = Arrow(
            rows[2].get_right() + RIGHT * 0.12,
            identity.get_left() + LEFT * 0.12,
            buff=0.0,
            color=GREEN,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.15
        )

        # Arrow from formula to formula_exp
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
        closing.move_to(np.array([0, closing.get_center()[1], 0])) # make the closing message in the center of the frame
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
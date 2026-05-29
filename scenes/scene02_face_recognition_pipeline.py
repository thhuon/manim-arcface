from manimlib import *
import os
import random


CYAN = "#00D4FF"
BLUE = "#4A7DFF"
WHITE = "#F2F6FF"
MUTED = "#8A94A6"
DARK = "#090D14"
PANEL = "#101722"
GREEN = "#3EF7A0"


def asset_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "decorations", filename)


def safe_svg(filename: str, scale_factor: float = 1.0, stroke_color=WHITE):
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    obj = SVGMobject(file_name=path)
    obj.set_fill(opacity=0)
    obj.set_stroke(color=stroke_color, width=1.5)
    obj.scale(scale_factor)
    return obj


def latex(text: str, size: int = 28, color=WHITE):
    obj = Tex(text, font_size=size)
    obj.set_color(color)
    return obj


def make_box(label_lines, width=2.35, height=1.28, stroke=CYAN, font_size=22):
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
    g = mob.copy()
    g.set_stroke(color=color, width=width, opacity=opacity)
    return g


def make_camera_icon():
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
    dots = VGroup()
    for p in [0.25 * LEFT + 0.20 * UP, 0.25 * RIGHT + 0.20 * UP, ORIGIN, 0.20 * LEFT + 0.28 * DOWN, 0.20 * RIGHT + 0.28 * DOWN]:
        dots.add(Dot(point=p, radius=0.045, color=CYAN))
    return dots


def make_pixel_grid(size=2.15, n=8):
    grid = VGroup()
    step = size / n
    for i in range(n + 1):
        offset = -size / 2 + i * step
        grid.add(Line(LEFT * size / 2 + UP * offset, RIGHT * size / 2 + UP * offset, stroke_color=WHITE, stroke_width=0.45, stroke_opacity=0.28))
        grid.add(Line(DOWN * size / 2 + RIGHT * offset, UP * size / 2 + RIGHT * offset, stroke_color=WHITE, stroke_width=0.45, stroke_opacity=0.28))
    return grid


def make_neural_network():
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
    entries = VGroup(*[latex(str(v), size=font_size) for v in values])
    entries.arrange(DOWN, buff=0.08)
    left = Line(entries.get_corner(UL) + 0.10 * LEFT, entries.get_corner(DL) + 0.10 * LEFT, stroke_color=WHITE, stroke_width=1.4)
    right = Line(entries.get_corner(UR) + 0.10 * RIGHT, entries.get_corner(DR) + 0.10 * RIGHT, stroke_color=WHITE, stroke_width=1.4)
    return VGroup(left, entries, right)


class Scene02_FaceRecognitionPipeline(Scene):
    def construct(self):
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
        title = latex(r"\textbf{Face Recognition Pipeline}", size=38)

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
        whole.arrange(DOWN, buff=0.55)
        whole.to_edge(UP, buff=0.42)
        whole.stages = stages
        whole.arrows = arrows
        whole.database = db
        whole.database_arrow = db_arrow
        whole.title = title
        return whole

    def play_intro_pipeline(self):
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

    def deep_dive_stage_1(self):
        header = self.zoom_to_stage_then_black(0, [
            (r"\textbf{Stage 1}", 42, CYAN),
            (r"\text{Input Image}", 34, WHITE),
        ])

        camera = make_camera_icon()
        face_frame = RoundedRectangle(width=2.20, height=2.20, corner_radius=0.18, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
        face = make_abstract_face().scale(0.88).move_to(face_frame)
        grid = make_pixel_grid(size=2.12).move_to(face_frame)
        image_pack = VGroup(face_frame, face, grid)

        arrow = Arrow(camera.get_right(), image_pack.get_left(), buff=0.24, color=CYAN, stroke_width=2)
        formula = VGroup(
            latex(r"\text{Raw pixels}", size=24, color=MUTED),
            latex(r"\mathbf{I}\in\mathbb{R}^{H\times W\times 3}", size=27, color=WHITE),
        ).arrange(DOWN, buff=0.15)

        content = VGroup(camera, arrow, image_pack, formula)
        content.arrange(RIGHT, buff=0.55)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(camera), run_time=0.45)
        self.play(GrowArrow(arrow), FadeIn(image_pack), run_time=0.65)
        self.play(FadeIn(formula), run_time=0.45)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, content)), run_time=0.65)

    def deep_dive_stage_2(self):
        header = self.zoom_to_stage_then_black(1, [
            (r"\textbf{Stage 2}", 42, CYAN),
            (r"\text{Detection \& Alignment}", 34, WHITE),
        ])

        raw_frame = RoundedRectangle(width=1.78, height=2.05, corner_radius=0.12, stroke_color=MUTED, stroke_width=1.5, fill_opacity=0)
        raw_face = make_abstract_face().scale(0.70).rotate(-12 * DEGREES).move_to(raw_frame)
        bbox = RoundedRectangle(width=1.22, height=1.50, corner_radius=0.08, stroke_color=CYAN, stroke_width=2.2, fill_opacity=0).move_to(raw_frame)
        landmarks = make_landmarks().scale(1.15).rotate(-12 * DEGREES).move_to(raw_frame)
        crop = VGroup(bbox.copy(), raw_face.copy()).scale(0.92)

        tilted = VGroup(
            RoundedRectangle(width=1.60, height=1.82, corner_radius=0.12, stroke_color=CYAN, stroke_width=1.6, fill_opacity=0),
            make_abstract_face().scale(0.62),
            make_landmarks().scale(1.00),
        )
        tilted[1].move_to(tilted[0])
        tilted[2].move_to(tilted[0])
        tilted.rotate(-14 * DEGREES)

        aligned = VGroup(
            RoundedRectangle(width=1.60, height=1.82, corner_radius=0.12, stroke_color=CYAN, stroke_width=2.2, fill_opacity=0),
            make_abstract_face().scale(0.62),
            make_landmarks().scale(1.00),
            DashedLine(UP * 0.95, DOWN * 0.95, color=BLUE, stroke_width=1.1),
            DashedLine(LEFT * 0.85, RIGHT * 0.85, color=BLUE, stroke_width=1.1),
        )
        aligned[1].move_to(aligned[0])
        aligned[2].move_to(aligned[0])
        aligned[3].move_to(aligned[0])
        aligned[4].move_to(aligned[0])

        flow = VGroup(VGroup(raw_frame, raw_face, bbox, landmarks), crop, tilted, aligned)
        flow.arrange(RIGHT, buff=0.52)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.15, color=CYAN, stroke_width=2) for a, b in zip(flow[:-1], flow[1:])])
        labels = VGroup(
            latex(r"\text{Locate face region}", size=19, color=MUTED),
            latex(r"\text{Crop}", size=19, color=MUTED),
            latex(r"\text{Estimate pose}", size=19, color=MUTED),
            latex(r"\text{Normalize pose, scale, and position}", size=19, color=MUTED),
        )
        for item, lab in zip(flow, labels):
            lab.next_to(item, DOWN, buff=0.20)

        content = VGroup(flow, arrows, labels)
        content.next_to(header, DOWN, buff=0.70)

        self.play(FadeIn(flow[0][0]), FadeIn(flow[0][1]), run_time=0.45)
        self.play(FadeIn(bbox), FadeIn(landmarks), FadeIn(labels[0]), run_time=0.55)
        for i in range(3):
            self.play(GrowArrow(arrows[i]), FadeIn(flow[i + 1]), FadeIn(labels[i + 1]), run_time=0.55)
        self.wait(1.2)
        self.play(FadeOut(VGroup(header, content)), run_time=0.65)

    def deep_dive_stage_3(self):
        header = self.zoom_to_stage_then_black(2, [
            (r"\textbf{Stage 3}", 42, CYAN),
            (r"\text{Feature Extraction}", 34, WHITE),
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

    def deep_dive_stage_4(self):
        header = self.zoom_to_stage_then_black(3, [
            (r"\textbf{Stage 4}", 42, CYAN),
            (r"\text{Matching / Verification}", 34, WHITE),
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

    def restore_pipeline(self, highlight_index=None):
        self.frame.set_width(FRAME_WIDTH)
        self.frame.move_to(ORIGIN)
        self.pipeline = self.create_pipeline()
        self.play(FadeIn(self.pipeline), run_time=0.65)
        if highlight_index is not None:
            self.pulse(self.pipeline.stages[highlight_index])
        self.wait(0.35)

    def final_overview(self):
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

    def pulse(self, stage, color=CYAN):
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

from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 01 - Face Recognition Pipeline
# Four clear stages: input -> detection/alignment -> features -> matching.
# =============================================================================


class Scene01_Pipeline(Scene):
    SAFE_WIDTH = 12.25
    SAFE_HEIGHT = 6.80

    def construct(self):
        self.camera.background_color = DARK
        self.frame = self.camera.frame

        self.pipeline = self.create_pipeline()
        self.beat1_overview()
        self.clear_and_wait()
        self.beat2_input_image()
        self.clear_and_wait()
        self.beat3_detection_alignment()
        self.clear_and_wait()
        self.beat4_feature_extraction()
        self.clear_and_wait()
        self.beat5_matching_verification()
        self.clear_and_wait()
        self.beat6_final_overview()

    # -------------------------------------------------------------------------
    # Pipeline overview
    # -------------------------------------------------------------------------
    def create_pipeline(self):
        title = make_scene_title(
            "Face Recognition Pipeline",
            "Four fast stages turn raw pixels into an identity decision",
            title_size=42,
        )
        stages = VGroup(
            make_stage_card(1, "Input Image", "camera frame", color=CYAN),
            make_stage_card(2, "Detection", "crop + align", color=BLUE),
            make_stage_card(3, "Features", "neural network", color=ORANGE),
            make_stage_card(4, "Matching", "compare embeddings", color=GREEN),
        )
        stages.arrange(RIGHT, buff=0.38)
        stages.set_width(12.15)
        stages.move_to(DOWN * 0.15)

        arrows = VGroup(*[
            make_flow_arrow(stages[i].get_right(), stages[i + 1].get_left(), color=WHITE, stroke_width=2.0)
            for i in range(3)
        ])
        pipeline = VGroup(title, stages, arrows)
        pipeline.title = title
        pipeline.stages = stages
        pipeline.arrows = arrows
        return pipeline

    def beat1_overview(self):
        self.play(FadeIn(self.pipeline.title), run_time=0.55)
        for i, stage in enumerate(self.pipeline.stages):
            self.play(FadeIn(stage, shift=0.12 * UP), run_time=0.32)
            if i < len(self.pipeline.arrows):
                self.play(GrowArrow(self.pipeline.arrows[i]), run_time=0.22)

        timeline = Line(
            self.pipeline.stages[0].get_left() + DOWN * 1.06,
            self.pipeline.stages[-1].get_right() + DOWN * 1.06,
            color=MUTED,
            stroke_width=1.2,
        )
        dot = Dot(color=YELLOW, radius=0.08).move_to(timeline.get_start())
        packet = RoundedRectangle(
            width=0.34,
            height=0.22,
            corner_radius=0.04,
            stroke_color=YELLOW,
            stroke_width=1.4,
            fill_color=YELLOW,
            fill_opacity=0.22,
        ).move_to(self.pipeline.stages[0].get_left() + RIGHT * 0.35 + UP * 0.08)
        fast = latex(r"\text{usually less than one second}", size=22, color=YELLOW)
        fast.next_to(timeline, DOWN, buff=0.22)
        self.play(ShowCreation(timeline), FadeIn(dot), FadeIn(packet), FadeIn(fast), run_time=0.45)
        stage_targets = [
            stage.get_center() + UP * 0.08
            for stage in self.pipeline.stages
        ]
        time_targets = [
            interpolate(timeline.get_start(), timeline.get_end(), i / (len(stage_targets) - 1))
            for i in range(len(stage_targets))
        ]
        for stage, packet_target, dot_target in zip(self.pipeline.stages, stage_targets, time_targets):
            glow = glow_copy(stage[0], color=stage[0].get_stroke_color(), width=6, opacity=0.10)
            self.play(
                dot.animate.move_to(dot_target),
                packet.animate.move_to(packet_target),
                FadeIn(glow),
                stage[0].animate.set_stroke(width=3.0),
                run_time=0.28,
                rate_func=linear,
            )
            self.play(stage[0].animate.set_stroke(width=2.0), FadeOut(glow), run_time=0.12)
        self.wait(0.7)

    # -------------------------------------------------------------------------
    # Stage 1 - input
    # -------------------------------------------------------------------------
    def beat2_input_image(self):
        header = make_scene_title("Stage 1: Input Image", "The camera captures raw RGB values", title_size=39)
        camera = make_camera_icon().scale(1.25)
        camera.move_to(LEFT * 4.65 + UP * 0.25)

        face = make_image_card("face_scan.png", width=2.15, height=2.58, stroke_color=CYAN)
        face.move_to(LEFT * 1.25 + UP * 0.08)
        face_label = make_badge("captured frame", color=CYAN, font_size=19)
        face_label.next_to(face, DOWN, buff=0.16)

        grid = make_pixel_grid(size=2.15, n=8)
        grid.move_to(face)

        matrix = make_pixel_matrix_from_image("face_scan.png", n=10, side=2.35)
        matrix.move_to(RIGHT * 2.40 + UP * 0.08)
        matrix_label = make_badge(r"RGB tensor", color=BLUE, font_size=19)
        matrix_label.next_to(matrix, DOWN, buff=0.16)
        channels = VGroup(
            make_badge("R", color=RED, font_size=16, h_buff=0.13, v_buff=0.07),
            make_badge("G", color=GREEN, font_size=16, h_buff=0.13, v_buff=0.07),
            make_badge("B", color=BLUE, font_size=16, h_buff=0.13, v_buff=0.07),
        ).arrange(RIGHT, buff=0.12)
        channels.next_to(matrix, UP, buff=0.15)

        fov = VGroup(
            DashedLine(camera.get_right(), face.get_left() + UP * 0.86, color=CYAN, stroke_width=1.5, dash_length=0.08),
            DashedLine(camera.get_right(), face.get_left() + DOWN * 0.86, color=CYAN, stroke_width=1.5, dash_length=0.08),
        )
        arrow = make_flow_arrow(face.get_right(), matrix.get_left(), color=WHITE)
        formula = latex(r"\mathbf{I}\in\mathbb{R}^{H\times W\times 3}", size=32, color=WHITE)
        formula.to_edge(DOWN, buff=0.58)
        fit_to_bounds(formula, max_width=11.0)
        layout = Group(header, camera, face, face_label, grid, matrix, matrix_label, channels, fov, arrow, formula)
        self.fit_group_to_frame(layout)

        scan_line = Line(
            face.get_left() + RIGHT * 0.08,
            face.get_right() + LEFT * 0.08,
            color=CYAN,
            stroke_width=3.0,
            stroke_opacity=0.90,
        )
        scan_line.move_to(face.get_top() + DOWN * 0.22)
        scan_target = scan_line.copy().move_to(face.get_bottom() + UP * 0.22)
        sample_ids = [4, 17, 29, 41, 52, 63, 76, 88]
        particles = VGroup(*[
            Dot(point=face.get_center(), color=matrix[i].get_fill_color(), radius=0.045)
            for i in sample_ids
        ])
        targets = [matrix[i].get_center() for i in sample_ids]

        self.play(FadeIn(header), run_time=0.5)
        self.play(FadeIn(camera), run_time=0.35)
        self.play(FadeIn(face), FadeIn(face_label), ShowCreation(fov), run_time=0.65)
        self.play(FadeIn(grid), ShowCreation(scan_line), run_time=0.35)
        self.play(Transform(scan_line, scan_target), run_time=0.80, rate_func=linear)
        self.play(FadeOut(scan_line), FadeIn(channels), run_time=0.25)
        self.play(GrowArrow(arrow), run_time=0.35)
        self.add(particles)
        self.play(
            LaggedStart(*[
                dot.animate.move_to(target)
                for dot, target in zip(particles, targets)
            ], lag_ratio=0.035),
            run_time=0.85,
            rate_func=smooth,
        )
        self.play(FadeOut(particles), run_time=0.15)
        self.play(
            LaggedStart(*[FadeIn(cell, scale=1.15) for cell in matrix], lag_ratio=0.006),
            FadeIn(matrix_label),
            run_time=1.2,
        )
        self.play(FadeIn(formula), run_time=0.45)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Stage 2 - detection and alignment
    # -------------------------------------------------------------------------
    def beat3_detection_alignment(self):
        header = make_scene_title("Stage 2: Detection & Alignment", "Find the face, remove clutter, standardize pose", title_size=38)

        full = ImageMobject(asset_path("face_scan.png"), height=3.55)
        full.move_to(LEFT * 4.15 + DOWN * 0.05)
        full_frame = RoundedRectangle(
            width=full.get_width() + 0.22,
            height=full.get_height() + 0.22,
            corner_radius=0.10,
            stroke_color=MUTED,
            stroke_width=1.2,
            fill_opacity=0,
        ).move_to(full)

        bbox = RoundedRectangle(
            width=full.get_width() * 0.58,
            height=full.get_height() * 0.72,
            corner_radius=0.07,
            stroke_color=CYAN,
            stroke_width=3.0,
            fill_opacity=0,
        ).move_to(full.get_center() + DOWN * 0.03)

        noise = VGroup(
            Rectangle(width=full.get_width() + 0.20, height=0.72, fill_color=DARK, fill_opacity=0.58, stroke_opacity=0),
            Rectangle(width=0.60, height=full.get_height(), fill_color=DARK, fill_opacity=0.58, stroke_opacity=0),
        )
        noise[0].move_to(full.get_top() + DOWN * 0.35)
        noise[1].move_to(full.get_left() + RIGHT * 0.28)

        lm_positions = [
            full.get_center() + LEFT * 0.42 + UP * 0.42,
            full.get_center() + RIGHT * 0.42 + UP * 0.42,
            full.get_center() + UP * 0.05,
            full.get_center() + LEFT * 0.30 + DOWN * 0.50,
            full.get_center() + RIGHT * 0.30 + DOWN * 0.50,
        ]
        landmarks = VGroup(*[Dot(point=p, radius=0.060, color=GREEN) for p in lm_positions])
        mesh = VGroup(
            Line(lm_positions[0], lm_positions[2], color=GREEN, stroke_width=1.4, stroke_opacity=0.70),
            Line(lm_positions[1], lm_positions[2], color=GREEN, stroke_width=1.4, stroke_opacity=0.70),
            Line(lm_positions[2], lm_positions[3], color=GREEN, stroke_width=1.4, stroke_opacity=0.70),
            Line(lm_positions[2], lm_positions[4], color=GREEN, stroke_width=1.4, stroke_opacity=0.70),
            Line(lm_positions[3], lm_positions[4], color=GREEN, stroke_width=1.4, stroke_opacity=0.70),
        )

        cropped = make_image_card("detection_alignment_face.png", width=1.95, height=2.35, stroke_color=BLUE)
        cropped.move_to(ORIGIN + RIGHT * 0.10 + DOWN * 0.05)
        tilted = cropped.copy().rotate(-8 * DEGREES)
        aligned = make_image_card("face_normal.png", width=1.95, height=2.35, stroke_color=GREEN)
        aligned.move_to(RIGHT * 4.05 + DOWN * 0.05)
        guide = DashedLine(aligned.get_left() + UP * 0.42, aligned.get_right() + UP * 0.42,
                           color=YELLOW, stroke_width=1.5, dash_length=0.10)

        labels = VGroup(
            make_badge("detect", color=CYAN, font_size=18).next_to(bbox, DOWN, buff=0.14),
            make_badge("crop", color=BLUE, font_size=18).next_to(cropped, DOWN, buff=0.15),
            make_badge("align", color=GREEN, font_size=18).next_to(aligned, DOWN, buff=0.15),
        )
        arrows = VGroup(
            make_flow_arrow(full.get_right(), cropped.get_left(), color=CYAN),
            make_flow_arrow(cropped.get_right(), aligned.get_left(), color=GREEN),
        )
        caption = latex(r"\text{A cleaner, normalized face is easier for the network to compare.}", size=25, color=WHITE)
        caption.to_edge(DOWN, buff=0.50)
        layout = Group(header, full, full_frame, bbox, noise, landmarks, mesh, tilted, cropped, aligned, guide, labels, arrows, caption)
        self.fit_group_to_frame(layout)
        scan_line = Line(
            full.get_left() + RIGHT * 0.08,
            full.get_right() + LEFT * 0.08,
            color=CYAN,
            stroke_width=3.0,
            stroke_opacity=0.80,
        )
        scan_line.move_to(full.get_top() + DOWN * 0.25)
        scan_target = scan_line.copy().move_to(full.get_bottom() + UP * 0.25)
        crop_ghost = bbox.copy()
        crop_target = RoundedRectangle(
            width=tilted.get_width(),
            height=tilted.get_height(),
            corner_radius=0.07,
            stroke_color=BLUE,
            stroke_width=2.4,
            fill_opacity=0,
        ).move_to(tilted)

        self.play(FadeIn(header), run_time=0.5)
        self.play(FadeIn(full), ShowCreation(full_frame), run_time=0.55)
        self.play(ShowCreation(scan_line), run_time=0.20)
        self.play(Transform(scan_line, scan_target), run_time=0.75, rate_func=linear)
        self.play(FadeOut(scan_line), run_time=0.16)
        self.play(ShowPassingFlash(bbox.copy(), time_width=1.2), run_time=0.75)
        self.add(bbox)
        self.play(FadeIn(noise), FadeIn(labels[0]), run_time=0.38)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in landmarks], lag_ratio=0.08), run_time=0.55)
        self.play(ShowCreation(mesh), run_time=0.4)
        self.play(Transform(crop_ghost, crop_target), GrowArrow(arrows[0]), FadeIn(tilted), FadeIn(labels[1]), run_time=0.65)
        self.play(FadeOut(crop_ghost), run_time=0.12)
        self.play(Transform(tilted, cropped), run_time=0.65)
        self.play(GrowArrow(arrows[1]), FadeIn(aligned), ShowCreation(guide), FadeIn(labels[2]), run_time=0.65)
        self.play(ShowPassingFlash(guide.copy().set_stroke(width=4.0), time_width=1.0), run_time=0.55)
        self.play(FadeIn(caption), run_time=0.45)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Stage 3 - feature extraction
    # -------------------------------------------------------------------------
    def beat4_feature_extraction(self):
        header = make_scene_title("Stage 3: Feature Extraction", "A neural network turns a face into an embedding vector", title_size=38)

        face = make_image_card("feature_extraction.png", width=1.75, height=2.10, stroke_color=CYAN)
        face.move_to(LEFT * 5.15 + DOWN * 0.10)
        face_label = make_badge("aligned face", color=CYAN, font_size=18)
        face_label.next_to(face, DOWN, buff=0.14)

        net = make_neural_network().scale(1.45)
        net.move_to(LEFT * 1.15 + DOWN * 0.03)
        net_label = make_badge("CNN feature layers", color=ORANGE, font_size=18)
        net_label.next_to(net, DOWN, buff=0.22)

        feature_tiles = VGroup()
        tile_labels = ["edges", "texture", "eyes", "nose", "jaw"]
        for i, label in enumerate(tile_labels):
            tile = RoundedRectangle(
                width=0.78,
                height=0.58,
                corner_radius=0.06,
                stroke_color=CYAN if i < 2 else GREEN,
                stroke_width=1.3,
                fill_color=PANEL,
                fill_opacity=0.50,
            )
            text = latex(rf"\text{{{label}}}", size=13, color=WHITE)
            text.move_to(tile)
            feature_tiles.add(VGroup(tile, text))
        feature_tiles.arrange(RIGHT, buff=0.12)
        feature_tiles.move_to(RIGHT * 2.75 + UP * 1.08)
        feature_label = latex(r"\text{features get more abstract}", size=20, color=MUTED)
        feature_label.next_to(feature_tiles, DOWN, buff=0.12)

        vector = make_vector([r"0.12", r"-0.44", r"0.83", r"\vdots", r"0.31"], font_size=21)
        vector.move_to(RIGHT * 4.75 + DOWN * 0.42)
        vector_label = make_badge("embedding", color=GREEN, font_size=20)
        vector_label.next_to(vector, DOWN, buff=0.18)

        arrows = VGroup(
            make_flow_arrow(face.get_right(), net.get_left(), color=CYAN),
            make_flow_arrow(net.get_right(), feature_tiles.get_left(), color=ORANGE),
            make_flow_arrow(feature_tiles.get_bottom() + DOWN * 0.05, vector.get_top() + UP * 0.05, color=GREEN),
        )

        wave_path = Line(net.get_left() + LEFT * 0.25, net.get_right() + RIGHT * 0.25)
        wave_dots = VGroup(*[
            Dot(point=wave_path.get_start(), color=YELLOW, radius=0.050)
            for _ in range(3)
        ])

        note = latex(
            r"\text{The vector is not a name. It is learned identity information.}",
            size=25,
            color=WHITE,
        )
        note.to_edge(DOWN, buff=0.50)
        fit_to_bounds(note, max_width=12.0)
        layout = Group(header, face, face_label, net, net_label, feature_tiles, feature_label, vector, vector_label, arrows, note)
        self.fit_group_to_frame(layout)

        layer_boxes = VGroup(*[
            RoundedRectangle(
                width=layer.get_width() + 0.24,
                height=layer.get_height() + 0.24,
                corner_radius=0.08,
                stroke_color=YELLOW,
                stroke_width=2.0,
                fill_opacity=0,
            ).move_to(layer)
            for layer in net[1]
        ])
        feature_particles = VGroup(*[
            Dot(point=face.get_right() + 0.12 * RIGHT, color=CYAN if i < 3 else GREEN, radius=0.045)
            for i in range(8)
        ])
        particle_targets = [
            feature_tiles[i % len(feature_tiles)].get_center() + 0.08 * ((i % 2) * RIGHT + ((i // 2) % 2) * UP)
            for i in range(8)
        ]

        self.play(FadeIn(header), run_time=0.5)
        self.play(FadeIn(face), FadeIn(face_label), run_time=0.5)
        self.play(GrowArrow(arrows[0]), FadeIn(net), FadeIn(net_label), run_time=0.65)
        self.add(wave_dots)
        self.play(
            LaggedStart(*[MoveAlongPath(dot, wave_path) for dot in wave_dots], lag_ratio=0.18),
            LaggedStart(*[ShowPassingFlash(box, time_width=0.90) for box in layer_boxes], lag_ratio=0.18),
            run_time=1.25,
            rate_func=smooth,
        )
        self.play(FadeOut(wave_dots), run_time=0.2)
        self.play(GrowArrow(arrows[1]), FadeIn(feature_tiles), FadeIn(feature_label), run_time=0.65)
        self.add(feature_particles)
        self.play(
            LaggedStart(*[
                particle.animate.move_to(target)
                for particle, target in zip(feature_particles, particle_targets)
            ], lag_ratio=0.04),
            run_time=0.75,
        )
        self.play(FadeOut(feature_particles), run_time=0.15)
        self.play(LaggedStart(*[tile.animate.shift(0.08 * UP) for tile in feature_tiles], lag_ratio=0.05), run_time=0.25)
        self.play(LaggedStart(*[tile.animate.shift(0.08 * DOWN) for tile in feature_tiles], lag_ratio=0.05), run_time=0.25)
        self.play(GrowArrow(arrows[2]), FadeIn(vector), FadeIn(vector_label), run_time=0.65)
        for entry in vector[1]:
            self.play(entry.animate.set_color(GREEN), run_time=0.08)
        self.play(FadeIn(note), run_time=0.45)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Stage 4 - matching and verification
    # -------------------------------------------------------------------------
    def beat5_matching_verification(self):
        header = make_scene_title("Stage 4: Matching / Verification", "Compare the query embedding with enrolled embeddings", title_size=38)

        query = Group(
            make_image_card("face_scan.png", width=1.25, height=1.45, stroke_color=YELLOW),
            make_vector([r"0.12", r"-0.44", r"\vdots", r"0.31"], font_size=18),
        ).arrange(DOWN, buff=0.22)
        query.move_to(LEFT * 4.90 + UP * 0.05)
        query_label = make_badge("query embedding", color=YELLOW, font_size=18)
        query_label.next_to(query, DOWN, buff=0.16)

        db_title = latex(r"\text{enrolled database}", size=23, color=MUTED)
        rows = VGroup()
        row_data = [
            ("Person A", "0.42", BLUE),
            ("Person B", "0.71", CYAN),
            ("Person C", "0.93", GREEN),
            ("Person D", "0.28", ORANGE),
        ]
        for name, score, color in row_data:
            box = RoundedRectangle(
                width=3.35,
                height=0.54,
                corner_radius=0.07,
                stroke_color=GREEN if score == "0.93" else MUTED,
                stroke_width=2.1 if score == "0.93" else 1.1,
                fill_color=PANEL,
                fill_opacity=0.35,
            )
            name_mob = latex(rf"\text{{{name}}}", size=18, color=color)
            score_mob = latex(score, size=18, color=GREEN if score == "0.93" else WHITE)
            content = VGroup(name_mob, score_mob).arrange(RIGHT, buff=1.08)
            content.move_to(box)
            rows.add(VGroup(box, content))
        rows.arrange(DOWN, buff=0.16)
        database = VGroup(db_title, rows).arrange(DOWN, buff=0.22)
        database.move_to(LEFT * 0.60 + UP * 0.05)

        lines = VGroup()
        for i, row in enumerate(rows):
            lines.add(DashedLine(
                query.get_right() + RIGHT * 0.10,
                row.get_left() + LEFT * 0.08,
                color=GREEN if i == 2 else MUTED,
                stroke_width=2.1 if i == 2 else 1.0,
                stroke_opacity=0.95 if i == 2 else 0.34,
                dash_length=0.08,
            ))

        formula = latex(r"\text{similarity}(\mathbf{f}_q,\mathbf{f}_i)=\cos(\theta)", size=27, color=WHITE)
        formula_box = RoundedRectangle(
            width=formula.get_width() + 0.42,
            height=0.62,
            corner_radius=0.08,
            stroke_color=CYAN,
            stroke_width=1.6,
            fill_color=PANEL,
            fill_opacity=0.42,
        )
        formula.move_to(formula_box)
        formula_group = VGroup(formula_box, formula)
        formula_group.next_to(database, DOWN, buff=0.45)

        score_bars = VGroup()
        for row, (_, score, color) in zip(rows, row_data):
            value = float(score)
            base = row[0].get_left() + RIGHT * 1.72 + DOWN * 0.17
            track = Line(base, base + RIGHT * 1.16, color=MUTED, stroke_width=2.0, stroke_opacity=0.35)
            bar = Line(base, base + RIGHT * (1.16 * value), color=GREEN if value > 0.90 else color, stroke_width=3.2)
            score_bars.add(VGroup(track, bar))

        result_img = make_image_card("face_normal.png", width=1.35, height=1.55, stroke_color=GREEN)
        result_badge = make_badge("Verified: Person C", color=GREEN, font_size=21)
        result = Group(result_img, result_badge).arrange(DOWN, buff=0.22)
        result.move_to(RIGHT * 4.25 + UP * 0.08)
        out_arrow = make_flow_arrow(rows[2].get_right(), result.get_left(), color=GREEN)

        threshold = latex(r"\text{0.93 > threshold}", size=21, color=GREEN)
        threshold.next_to(out_arrow, UP, buff=0.15)
        layout = Group(header, query, query_label, database, lines, formula_group, result, out_arrow, threshold, score_bars)
        self.fit_group_to_frame(layout)
        query_start = query.get_right() + RIGHT * 0.10
        query_pulse = Dot(point=query_start, color=YELLOW, radius=0.070)
        query_paths = VGroup(*[
            Line(query_start, row.get_left() + LEFT * 0.08, color=YELLOW, stroke_width=1.0, stroke_opacity=0.0)
            for row in rows
        ])

        self.play(FadeIn(header), run_time=0.5)
        self.play(FadeIn(query), FadeIn(query_label), run_time=0.5)
        self.play(FadeIn(database), run_time=0.55)
        self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio=0.10), run_time=0.75)
        self.play(LaggedStart(*[ShowCreation(group[0]) for group in score_bars], lag_ratio=0.05), run_time=0.35)
        self.add(query_pulse)
        for path, bar_group in zip(query_paths, score_bars):
            self.play(MoveAlongPath(query_pulse, path), ShowCreation(bar_group[1]), run_time=0.25, rate_func=smooth)
            query_pulse.move_to(query_start)
        self.play(FadeOut(query_pulse), run_time=0.15)
        self.play(FadeIn(formula_group), run_time=0.45)
        self.play(rows[2][0].animate.set_fill(GREEN, opacity=0.12), FadeIn(threshold), run_time=0.35)
        self.play(rows[2][0].animate.set_stroke(GREEN, width=3.2), score_bars[2][1].animate.set_stroke(width=5.0), run_time=0.28)
        self.play(rows[2][0].animate.set_stroke(GREEN, width=2.1), score_bars[2][1].animate.set_stroke(width=3.2), run_time=0.22)
        self.play(GrowArrow(out_arrow), FadeIn(result), run_time=0.65)
        self.wait(0.9)

    # -------------------------------------------------------------------------
    # Final recap
    # -------------------------------------------------------------------------
    def beat6_final_overview(self):
        self.pipeline = self.create_pipeline()
        self.play(FadeIn(self.pipeline), run_time=0.65)
        for stage in self.pipeline.stages:
            self.pulse(stage)

        closing = VGroup(
            latex(r"\text{Raw pixels become a compact identity embedding.}", size=29, color=CYAN),
            latex(r"\text{Every stage shapes the final accuracy.}", size=25, color=WHITE),
        ).arrange(DOWN, buff=0.16)
        closing.next_to(self.pipeline.stages, DOWN, buff=0.72)
        self.play(FadeIn(closing), run_time=0.55)
        self.wait(1.0)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def pulse(self, stage, color=CYAN):
        outline = stage[0]
        halo = glow_copy(outline, color=color)
        self.add(halo, outline)
        self.play(
            outline.animate.set_stroke(color=color, width=3.2),
            halo.animate.set_stroke(opacity=0.30),
            run_time=0.16,
        )
        self.play(
            outline.animate.set_stroke(color=color, width=2.0),
            FadeOut(halo),
            run_time=0.22,
        )

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def fit_group_to_frame(self, group, center=ORIGIN):
        fit_to_bounds(group, max_width=self.SAFE_WIDTH, max_height=self.SAFE_HEIGHT)
        group.move_to(center)
        return group

from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 00 - Introduction
# Clear visual arc: same face images -> pixels -> latent identity -> open set.
# =============================================================================


class Scene00Introduction(Scene):
    SAFE_WIDTH = 12.10
    SAFE_TOP = 3.50
    SAFE_BOTTOM = -1.05
    SAFE_HEIGHT = SAFE_TOP - SAFE_BOTTOM

    def construct(self):
        self.camera.background_color = DARK
        self.frame = self.camera.frame

        self.beat_a_same_identity_grid()
        self.clear_and_wait()
        self.beat_b_pixels_vs_identity()
        self.clear_and_wait()
        self.beat_c_latent_identity()
        self.clear_and_wait()
        self.beat_d_open_set_bridge()

    # -------------------------------------------------------------------------
    # Beat A - same identity, different images
    # -------------------------------------------------------------------------
    def beat_a_same_identity_grid(self):
        title = make_scene_title(
            "Same Identity, Different Images?",
            title_size=39,
        )

        face_files = [
            "face_1.png", "face_2.png", "face_3.png", "face_4.png",
            "face_5.png", "face_6.png", "face_7.png", "face_8.png",
            "face_9.png", "face_10.png", "face_11.png", "face_12.png",
        ]
        cards = Group(*[
            make_image_card(fname, width=1.28, height=1.42, show_frame=False)
            for fname in face_files
        ])
        cards.arrange_in_grid(3, 4, buff=0.13)
        cards.move_to(DOWN * 0.08)
        fit_to_bounds(cards, max_width=7.45, max_height=4.60)

        bottom_note = latex(r"\text{same person, different conditions}", size=24, color=GREEN)
        bottom_note.next_to(cards, DOWN, buff=0.20)

        human_label = VGroup(
            make_abstract_face().scale(0.45),
            latex(r"\text{human intuition}", size=24, color=CYAN),
        ).arrange(RIGHT, buff=0.18)
        human_label.next_to(cards, RIGHT, buff=0.32)
        fit_to_bounds(human_label, max_width=2.15)

        layout = Group(title, cards, bottom_note, human_label)
        self.fit_group_to_subtitle_area(layout)

        scan_line = Line(
            cards.get_left() + UP * cards.get_height() / 2,
            cards.get_right() + UP * cards.get_height() / 2,
            color=CYAN,
            stroke_width=3,
            stroke_opacity=0.65,
        )
        scan_line.shift(UP * 0.12)
        focus = cards[5].copy()
        focus.generate_target()
        focus.target.scale(1.16)
        focus.target.move_to(cards[5])

        self.play(FadeIn(title), run_time=0.55)
        self.play(
            LaggedStart(*[FadeIn(card, shift=0.14 * UP) for card in cards],
                        lag_ratio=0.045),
            run_time=1.6,
        )
        self.play(ShowPassingFlash(scan_line), run_time=1.0)
        self.play(
            MoveToTarget(focus),
            cards[5].animate.scale(1.08),
            run_time=0.36,
        )
        self.play(cards[5].animate.scale(1 / 1.08), FadeOut(focus), run_time=0.28)
        self.play(
            LaggedStart(*[
                card.animate.shift(0.06 * UP if i % 2 == 0 else 0.06 * DOWN)
                for i, card in enumerate(cards)
            ], lag_ratio=0.025),
            run_time=0.45,
        )
        self.play(
            LaggedStart(*[
                card.animate.shift(0.06 * DOWN if i % 2 == 0 else 0.06 * UP)
                for i, card in enumerate(cards)
            ], lag_ratio=0.025),
            run_time=0.45,
        )
        self.play(FadeIn(bottom_note), run_time=0.45)
        self.play(FadeIn(human_label, shift=0.15 * LEFT), run_time=0.55)
        self.play(
            bottom_note.animate.scale(1.06),
            run_time=0.32,
        )
        self.play(
            bottom_note.animate.scale(1 / 1.06),
            run_time=0.28,
        )
        self.wait(0.7)

    # -------------------------------------------------------------------------
    # Beat B - computer view: pixels change
    # -------------------------------------------------------------------------
    def beat_b_pixels_vs_identity(self):
        title = make_scene_title(
            "A Computer Sees Numbers",
            title_size=39,
        )

        face = make_image_card("face_3.png", width=2.10, height=2.48, show_frame=False)
        face.move_to(LEFT * 4.55 + UP * 0.30)
        face_label = make_badge("image", color=CYAN, font_size=20)
        face_label.next_to(face, DOWN, buff=0.16)

        matrix = make_pixel_matrix_from_image("face_3.png", n=14, side=3.10)
        matrix.move_to(RIGHT * 1.30 + UP * 0.24)
        matrix_label = make_badge("pixel matrix", color=BLUE, font_size=20)
        matrix_label.next_to(matrix, DOWN, buff=0.18)

        zoom_cells = VGroup()
        numbers = VGroup()
        values = ["RGB", "skin", "hair", "light"]
        for i, value in enumerate(values):
            cell = Square(
                side_length=0.52,
                stroke_color=YELLOW,
                stroke_width=1.2,
                fill_color=PANEL,
                fill_opacity=0.85,
            )
            cell.move_to(RIGHT * (4.52 + (i % 2) * 0.62) + UP * (0.54 - (i // 2) * 0.62))
            num = latex(rf"\text{{{value}}}", size=13, color=WHITE).move_to(cell)
            zoom_cells.add(cell)
            numbers.add(num)
        zoom_group = VGroup(zoom_cells, numbers)
        zoom_title = latex(r"\text{sampled colors}", size=18, color=YELLOW)
        zoom_title.next_to(zoom_group, UP, buff=0.16)

        statement = latex(
            r"\text{Pixels change } \neq \text{ identity changes}",
            size=34,
            color=WHITE,
        )
        statement.next_to(Group(face, matrix, zoom_group), DOWN, buff=0.34)
        fit_to_bounds(statement, max_width=9.80)

        layout = Group(title, face, face_label, matrix, matrix_label, zoom_group, zoom_title, statement)
        self.fit_group_to_subtitle_area(layout)

        matrix_start = matrix.copy()
        matrix_start.replace(face, stretch=True)
        matrix_start.set_opacity(0.0)

        arrow = make_flow_arrow(face.get_right() + RIGHT * 0.18, matrix.get_left() + LEFT * 0.18, color=WHITE)
        moving_pixels = self.make_particles_from_group(face, count=28, color=CYAN, radius=0.025)
        target_points = self.sample_points_from_group(matrix, len(moving_pixels))

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(face), FadeIn(face_label), run_time=0.55)
        self.play(GrowArrow(arrow), run_time=0.4)
        self.play(FadeIn(moving_pixels), run_time=0.18)
        self.play(
            *[dot.animate.move_to(point) for dot, point in zip(moving_pixels, target_points)],
            run_time=0.95,
            rate_func=smooth,
        )
        self.play(
            LaggedStart(*[
                Transform(start_cell, end_cell)
                for start_cell, end_cell in zip(matrix_start, matrix)
            ],
                        lag_ratio=0.006),
            FadeIn(matrix_label),
            run_time=1.5,
        )
        self.play(FadeOut(moving_pixels), run_time=0.25)
        self.play(
            LaggedStart(*[
                cell.animate.scale(1.12).set_stroke(color=YELLOW, width=0.55, opacity=0.70)
                for cell in matrix[45:53]
            ], lag_ratio=0.03),
            run_time=0.35,
        )
        self.play(
            LaggedStart(*[
                cell.animate.scale(1 / 1.12).set_stroke(color=BLACK, width=0.18, opacity=0.35)
                for cell in matrix[45:53]
            ], lag_ratio=0.03),
            run_time=0.35,
        )
        self.play(FadeIn(zoom_group), FadeIn(zoom_title), run_time=0.55)
        self.play(FadeIn(statement), run_time=0.65)
        self.wait(0.9)

    # -------------------------------------------------------------------------
    # Beat C - what identity is made from
    # -------------------------------------------------------------------------
    def beat_c_latent_identity(self):
        title = make_scene_title(
            "What Are We Actually Recognizing?",
            title_size=37,
        )

        face = ImageMobject(asset_path("face_normal.png"), height=2.50)
        face.move_to(LEFT * 3.05 + UP * 0.22)

        similar_faces = Group(
            make_image_card("face_A.png", width=0.88, height=1.00, label="similar eyes", label_color=MUTED, label_size=12, show_frame=False),
            make_image_card("face_B.png", width=0.88, height=1.00, label="similar pose", label_color=MUTED, label_size=12, show_frame=False),
            make_image_card("face_C.png", width=0.88, height=1.00, label="similar shape", label_color=MUTED, label_size=12, show_frame=False),
        ).arrange(RIGHT, buff=0.42)
        similar_faces.move_to(RIGHT * 2.28 + UP * 0.92)

        no_single_feature = make_badge("one feature is not enough", color=RED, font_size=20)
        no_single_feature.next_to(similar_faces, DOWN, buff=0.24)

        identity_dot = Dot(color=GREEN, radius=0.20)
        identity_ring = Circle(radius=0.54, stroke_color=GREEN, stroke_width=2.2, fill_opacity=0)
        identity = VGroup(identity_ring, identity_dot)
        identity.move_to(RIGHT * 2.42 + DOWN * 0.62)
        identity_label = latex(r"\text{latent identity}", size=24, color=GREEN)
        identity_label.next_to(identity, RIGHT, buff=0.22)

        combo_label = latex(r"\text{unique combination}", size=23, color=GREEN)
        combo_label.move_to(RIGHT * 2.28 + DOWN * 0.02)

        flow = VGroup(
            make_badge("pixels", color=MUTED, font_size=18),
            make_badge("network", color=CYAN, font_size=18),
            make_badge("embedding", color=WHITE, font_size=18),
            make_badge("identity", color=GREEN, font_size=18),
        ).arrange(RIGHT, buff=0.42)
        flow.move_to(DOWN * 1.18)

        features = VGroup()
        feature_specs = [
            (face.get_center() + LEFT * 0.28 + UP * 0.39, "eyes", CYAN),
            (face.get_center() + RIGHT * 0.02 + DOWN * 0.01, "nose", YELLOW),
            (face.get_center() + RIGHT * 0.03 + DOWN * 0.41, "mouth", GREEN),
        ]
        for point, label, color in feature_specs:
            marker = Dot(point=point, radius=0.060, color=color)
            text = make_badge(label, color=color, font_size=15)
            text.next_to(marker, RIGHT, buff=0.10)
            features.add(VGroup(marker, text))

        visual_block = Group(
            face,
            features,
            similar_faces,
            no_single_feature,
            identity,
            identity_label,
            combo_label,
            flow,
        )
        visual_block.move_to(DOWN * 0.10)
        title.next_to(visual_block, UP, buff=0.28)
        master_layout = Group(title, visual_block)
        self.fit_group_to_subtitle_area(master_layout)

        flow_arrows = VGroup(*[
            make_flow_arrow(flow[i].get_right(), flow[i + 1].get_left(), color=CYAN, stroke_width=1.7)
            for i in range(len(flow) - 1)
        ])
        feature_lines = VGroup(*[
            Line(feature[0].get_center(), combo_label.get_left() + LEFT * 0.10, color=feature[0].get_color(), stroke_width=1.5, stroke_opacity=0.55)
            for feature in features
        ])
        feature_particles = VGroup(*[
            Dot(point=feature[0].get_center(), radius=0.035, color=feature[0].get_color())
            for feature in features
        ])

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(face), run_time=0.55)
        for feature in features:
            self.play(GrowFromCenter(feature[0]), FadeIn(feature[1]), run_time=0.28)
        self.play(LaggedStart(*[ShowCreation(line) for line in feature_lines], lag_ratio=0.12), run_time=0.55)
        self.play(FadeIn(feature_particles), run_time=0.20)
        self.play(
            *[
                particle.animate.move_to(combo_label.get_center())
                for particle in feature_particles
            ],
            run_time=0.72,
            rate_func=smooth,
        )
        self.play(FadeIn(similar_faces, shift=0.20 * UP), run_time=0.65)
        self.play(FadeIn(no_single_feature), FadeIn(combo_label), run_time=0.55)
        self.play(FadeOut(feature_particles), FadeOut(feature_lines), run_time=0.25)
        self.play(TransformFromCopy(combo_label, identity_label), FadeIn(identity), run_time=0.75)
        self.play(identity.animate.scale(1.12), run_time=0.22)
        self.play(identity.animate.scale(1 / 1.12), run_time=0.22)
        self.play(FadeIn(flow), LaggedStart(*[GrowArrow(a) for a in flow_arrows], lag_ratio=0.16), run_time=0.9)
        self.play(
            LaggedStart(*[badge.animate.scale(1.05) for badge in flow], lag_ratio=0.10),
            run_time=0.32,
        )
        self.play(
            LaggedStart(*[badge.animate.scale(1 / 1.05) for badge in flow], lag_ratio=0.10),
            run_time=0.32,
        )
        self.wait(0.9)

    # -------------------------------------------------------------------------
    # Beat D - open-set recognition bridge
    # -------------------------------------------------------------------------
    def beat_d_open_set_bridge(self):
        title = make_scene_title(
            "Open-Set Recognition",
            title_size=38,
        )

        left_center = LEFT * 3.10 + DOWN * 0.15
        right_center = RIGHT * 3.10 + DOWN * 0.15
        left_width, right_width = 5.25, 5.25
        left_height, right_height = 4.25, 4.25

        left_label = latex(r"\text{closed-set classifier}", size=23, color=MUTED)
        left_label.move_to(left_center + UP * (left_height / 2 + 0.30))
        right_label = latex(r"\text{identity space}", size=23, color=GREEN)
        right_label.move_to(right_center + UP * (right_height / 2 + 0.30))

        class_cards = VGroup(
            make_badge("Person A", color=BLUE, font_size=18),
            make_badge("Person B", color=CYAN, font_size=18),
            make_badge("Person C", color=ORANGE, font_size=18),
        ).arrange(DOWN, buff=0.24)
        class_cards.move_to(left_center + RIGHT * 0.55)

        query = make_image_card("face_scan.png", width=1.10, height=1.28, label="new face", label_color=YELLOW, show_frame=False)
        query.move_to(left_center + LEFT * (left_width / 2 - 1.05) + DOWN * 0.45)
        query_mark = latex(r"\text{?}", size=38, color=YELLOW)
        query_mark.next_to(query, UP, buff=0.10)

        cluster_a = make_embedding_cluster(right_center + LEFT * 1.15 + UP * 0.82, BLUE)
        cluster_b = make_embedding_cluster(right_center + RIGHT * 1.20 + UP * 0.55, GREEN)
        cluster_c = make_embedding_cluster(right_center + LEFT * 0.70 + DOWN * 1.25, ORANGE)
        new_dot = Dot(point=right_center + RIGHT * 0.58 + DOWN * 0.80, color=YELLOW, radius=0.13)
        new_dot_label = latex(r"\text{new identity}", size=17, color=YELLOW)
        new_dot_label.next_to(new_dot, RIGHT, buff=0.12)

        space_labels = VGroup(
            latex(r"\text{A}", size=16, color=BLUE).next_to(cluster_a, DOWN, buff=0.08),
            latex(r"\text{B}", size=16, color=GREEN).next_to(cluster_b, DOWN, buff=0.08),
            latex(r"\text{C}", size=16, color=ORANGE).next_to(cluster_c, DOWN, buff=0.08),
        )

        bridge_statement = latex(
            r"\text{Face recognition needs a general identity space, not memorized names.}",
            size=26,
            color=WHITE,
        )
        fit_to_bounds(bridge_statement, max_width=12.0)
        bridge_statement.next_to(Group(query, class_cards, cluster_a, cluster_b, cluster_c, new_dot), DOWN, buff=0.36)

        layout = Group(
            title,
            left_label,
            right_label,
            class_cards,
            query,
            query_mark,
            cluster_a,
            cluster_b,
            cluster_c,
            new_dot,
            new_dot_label,
            space_labels,
            bridge_statement,
        )
        self.fit_group_to_subtitle_area(layout)

        forced_arrow = make_flow_arrow(query.get_right(), class_cards[1].get_left(), color=RED, stroke_width=2.0)
        forced_label = make_badge("forced old label", color=RED, font_size=17)
        forced_label.next_to(forced_arrow, UP, buff=0.14)

        self.play(FadeIn(title), FadeIn(left_label), FadeIn(right_label), run_time=0.6)
        self.play(FadeIn(query), FadeIn(query_mark), FadeIn(class_cards), run_time=0.55)
        self.play(
            LaggedStart(*[card.animate.shift(0.08 * RIGHT) for card in class_cards], lag_ratio=0.08),
            run_time=0.25,
        )
        self.play(
            LaggedStart(*[card.animate.shift(0.08 * LEFT) for card in class_cards], lag_ratio=0.08),
            run_time=0.25,
        )
        self.play(GrowArrow(forced_arrow), FadeIn(forced_label), run_time=0.5)
        self.play(WiggleOutThenIn(query_mark, run_time=0.75))
        travel_dot = Dot(point=query.get_center(), radius=0.08, color=YELLOW)
        travel_target = new_dot.get_center() + LEFT * 1.40 + DOWN * 0.40
        path_to_space = CubicBezier(
            query.get_center(),
            query.get_center() + RIGHT * 1.45 + UP * 1.15,
            new_dot.get_center() + LEFT * 1.20 + UP * 0.55,
            travel_target,
        )
        self.play(
            FadeOut(forced_arrow),
            FadeOut(forced_label),
            query.animate.move_to(travel_target).scale(0.55),
            FadeIn(travel_dot),
            run_time=0.8,
        )
        self.play(MoveAlongPath(travel_dot, path_to_space), run_time=1.0, rate_func=smooth)
        self.play(
            LaggedStart(
                FadeIn(cluster_a), FadeIn(cluster_b), FadeIn(cluster_c),
                FadeIn(space_labels), FadeIn(new_dot), FadeIn(new_dot_label),
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.play(FadeOut(travel_dot), new_dot.animate.scale(1.25), run_time=0.25)
        self.play(new_dot.animate.scale(1 / 1.25), run_time=0.25)
        self.play(FadeIn(bridge_statement), run_time=0.65)
        self.wait(0.9)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def fit_group_to_subtitle_area(self, group):
        fit_to_bounds(group, max_width=self.SAFE_WIDTH, max_height=self.SAFE_HEIGHT)
        group.shift(LEFT * group.get_center()[0])
        group.shift(UP * (self.SAFE_TOP - group.get_top()[1]))
        if group.get_bottom()[1] < self.SAFE_BOTTOM:
            group.shift(UP * (self.SAFE_BOTTOM - group.get_bottom()[1]))
        group.shift(LEFT * group.get_center()[0])
        return group

    def make_particles_from_group(self, group, count=20, color=CYAN, radius=0.03):
        points = self.sample_points_from_group(group, count)
        return VGroup(*[
            Dot(point=point, radius=radius, color=color)
            for point in points
        ])

    def sample_points_from_group(self, group, count):
        left = group.get_left()[0]
        right = group.get_right()[0]
        bottom = group.get_bottom()[1]
        top = group.get_top()[1]
        points = []
        for i in range(count):
            alpha = 0 if count == 1 else i / (count - 1)
            x = interpolate(left, right, (i % 7) / 6)
            y = interpolate(bottom, top, (int(alpha * 11) % 5) / 4)
            points.append(np.array([x, y, 0]))
        return points

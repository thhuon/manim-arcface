from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 02 - Challenges
# Visual proof of why a high-quality embedding space is necessary.
# =============================================================================


class Scene02_Challenges(Scene):
    SAFE_WIDTH = 12.25
    SAFE_HEIGHT = 6.80

    def construct(self):
        self.camera.background_color = DARK
        self.frame = self.camera.frame

        self.beat_a_good_embedding()
        self.clear_and_wait()
        self.beat_b_intra_class_variation()
        self.clear_and_wait()
        self.beat_c_inter_class_similarity()
        self.clear_and_wait()
        self.beat_d_real_world_pressure()
        self.clear_and_wait()
        self.beat_e_open_set_transition()

    # -------------------------------------------------------------------------
    # Beat A - ideal embedding space
    # -------------------------------------------------------------------------
    def beat_a_good_embedding(self):
        title = make_scene_title(
            "What Makes A Good Embedding Space?",
            "Same identities should be close; different identities need room",
            title_size=38,
        )
        plane = make_panel(width=9.25, height=5.25, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.15)

        centers = [
            plane.get_center() + LEFT * 2.55 + UP * 1.03,
            plane.get_center() + RIGHT * 2.42 + UP * 0.86,
            plane.get_center() + DOWN * 1.32,
        ]
        colors = [BLUE, GREEN, ORANGE]
        labels = ["Person A", "Person B", "Person C"]

        clusters = VGroup(*[
            make_embedding_cluster(center, color=color, scale=0.90, count=6)
            for center, color in zip(centers, colors)
        ])
        start_clusters = clusters.copy()
        start_clusters.arrange(RIGHT, buff=0.38)
        start_clusters.move_to(plane.get_center())
        start_clusters.set_stroke(opacity=0.95)
        cluster_rings = VGroup(*[
            Ellipse(width=1.55, height=1.15, stroke_color=color, stroke_width=1.8, fill_opacity=0).move_to(cluster)
            for cluster, color in zip(clusters, colors)
        ])
        cluster_labels = VGroup(*[
            latex(rf"\text{{{label}}}", size=20, color=color).next_to(ring, DOWN, buff=0.12)
            for label, color, ring in zip(labels, colors, cluster_rings)
        ])

        pull_arrows = VGroup(*[
            Arrow(
                dot.get_center() + 0.18 * (dot.get_center() - clusters[0].get_center()),
                clusters[0].get_center(),
                buff=0.03,
                color=CYAN,
                stroke_width=1.2,
                max_tip_length_to_length_ratio=0.24,
            )
            for dot in clusters[0]
        ])
        separation = make_double_arrow(
            centers[0] + RIGHT * 0.95 + DOWN * 0.08,
            centers[1] + LEFT * 0.95 + DOWN * 0.08,
            color=YELLOW,
            stroke_width=2.0,
        )
        separation_label = latex(r"\text{large margin}", size=20, color=YELLOW)
        separation_label.next_to(separation, DOWN, buff=0.12)

        goals = VGroup(
            make_badge("intra-class compactness", color=CYAN, font_size=19),
            make_badge("inter-class separation", color=YELLOW, font_size=19),
        ).arrange(RIGHT, buff=0.45)
        goals.to_edge(DOWN, buff=0.46)
        layout = Group(title, plane, clusters, start_clusters, cluster_rings, cluster_labels, pull_arrows, separation, separation_label, goals)
        self.fit_group_to_frame(layout)
        noisy_cloud = VGroup(*[
            Dot(point=plane.get_center() + np.array([(-3.8 + i * 0.58) % 7.6 - 3.8, 1.9 - (i % 7) * 0.56, 0]),
                radius=0.050, color=[BLUE, GREEN, ORANGE][i % 3])
            for i in range(24)
        ])

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(plane), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(dot, scale=1.25) for dot in noisy_cloud], lag_ratio=0.015), run_time=0.65)
        self.play(
            LaggedStart(*[
                Transform(noisy_cloud[i], start_clusters[i % len(start_clusters)][i % len(start_clusters[i % len(start_clusters)])])
                for i in range(len(noisy_cloud))
            ], lag_ratio=0.01),
            run_time=0.80,
        )
        self.play(FadeOut(noisy_cloud), run_time=0.15)
        self.play(LaggedStart(*[FadeIn(cluster, scale=1.05) for cluster in start_clusters], lag_ratio=0.08), run_time=0.35)
        self.play(
            LaggedStart(*[
                Transform(start_cluster, cluster)
                for start_cluster, cluster in zip(start_clusters, clusters)
            ], lag_ratio=0.12),
            run_time=1.0,
        )
        clusters = start_clusters
        self.play(FadeIn(cluster_rings), FadeIn(cluster_labels), run_time=0.65)
        self.play(LaggedStart(*[GrowArrow(a) for a in pull_arrows], lag_ratio=0.04), run_time=0.65)
        self.play(ShowCreation(separation), FadeIn(separation_label), run_time=0.55)
        self.play(FadeIn(goals), run_time=0.55)
        for ring in cluster_rings:
            self.play(ring.animate.scale(1.08), run_time=0.12)
            self.play(ring.animate.scale(1 / 1.08), run_time=0.12)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat B - intra-class variation
    # -------------------------------------------------------------------------
    def beat_b_intra_class_variation(self):
        title = make_scene_title(
            "Challenge 1: Intra-Class Variation",
            "The same person can look very different across conditions",
            title_size=37,
        )

        face_specs = [
            ("face_1.png", "front"),
            ("face_5.png", "low light"),
            ("face_9.png", "formal"),
            ("face_13.png", "pose"),
            ("face_17.png", "occlusion"),
        ]
        faces = Group(*[
            make_image_card(fname, width=1.25, height=1.46, label=label, label_color=YELLOW, stroke_color=MUTED)
            for fname, label in face_specs
        ])
        faces.arrange(RIGHT, buff=0.28)
        faces.move_to(UP * 1.46)

        plane = make_panel(width=10.2, height=2.55, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 1.32)
        plane_label = latex(r"\text{embedding space}", size=20, color=MUTED)
        plane_label.next_to(plane, UP, buff=0.10)

        scattered_positions = [
            plane.get_center() + LEFT * 3.55 + UP * 0.45,
            plane.get_center() + LEFT * 1.75 + DOWN * 0.40,
            plane.get_center() + LEFT * 0.15 + UP * 0.55,
            plane.get_center() + RIGHT * 1.82 + DOWN * 0.22,
            plane.get_center() + RIGHT * 3.40 + UP * 0.20,
        ]
        compact_positions = [
            plane.get_center() + LEFT * 0.24 + UP * 0.17,
            plane.get_center() + RIGHT * 0.18 + UP * 0.14,
            plane.get_center() + DOWN * 0.06,
            plane.get_center() + LEFT * 0.10 + DOWN * 0.27,
            plane.get_center() + RIGHT * 0.30 + DOWN * 0.19,
        ]
        dots = VGroup(*[
            Dot(point=pos, radius=0.095, color=BLUE)
            for pos in scattered_positions
        ])
        transform_arrows = VGroup(*[
            make_flow_arrow(face.get_bottom() + DOWN * 0.04, dot.get_center() + UP * 0.05, color=CYAN, stroke_width=1.4)
            for face, dot in zip(faces, dots)
        ])

        bad_ring = Ellipse(width=7.70, height=1.50, stroke_color=RED, stroke_width=2.0, fill_opacity=0)
        bad_ring.move_to(plane.get_center() + LEFT * 0.02)
        bad_label = make_badge("bad: scattered same identity", color=RED, font_size=19)
        bad_label.next_to(bad_ring, DOWN, buff=0.10)

        compact_ring = Ellipse(width=1.25, height=0.88, stroke_color=GREEN, stroke_width=2.2, fill_opacity=0)
        compact_ring.move_to(plane.get_center())
        compact_label = make_badge("desired: compact cluster", color=GREEN, font_size=19)
        compact_label.next_to(compact_ring, DOWN, buff=0.12)

        pull_lines = VGroup(*[
            Arrow(dot.get_center(), compact_ring.get_center(), buff=0.10, color=GREEN,
                  stroke_width=1.2, stroke_opacity=0.60, max_tip_length_to_length_ratio=0.18)
            for dot in dots
        ])
        layout = Group(title, faces, plane, plane_label, dots, transform_arrows, bad_ring, bad_label, compact_ring, compact_label, pull_lines)
        self.fit_group_to_frame(layout)
        ghost_faces = Group(*[face.copy() for face in faces])

        self.play(FadeIn(title), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(face, shift=0.12 * UP) for face in faces], lag_ratio=0.08), run_time=0.9)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.45)
        self.play(LaggedStart(*[GrowArrow(a) for a in transform_arrows], lag_ratio=0.06), run_time=0.55)
        self.add(ghost_faces)
        self.play(
            LaggedStart(*[
                Transform(ghost, dot)
                for ghost, dot in zip(ghost_faces, dots)
            ], lag_ratio=0.08),
            run_time=0.90,
        )
        self.play(FadeOut(ghost_faces), LaggedStart(*[FadeIn(dot, scale=1.25) for dot in dots], lag_ratio=0.08), run_time=0.25)
        self.play(ShowCreation(bad_ring), FadeIn(bad_label), run_time=0.55)
        self.play(dots[1].animate.shift(UP * 0.18 + LEFT * 0.16), dots[3].animate.shift(DOWN * 0.17 + RIGHT * 0.14), run_time=0.30)
        self.play(dots[1].animate.shift(DOWN * 0.18 + RIGHT * 0.16), dots[3].animate.shift(UP * 0.17 + LEFT * 0.14), run_time=0.30)
        self.wait(0.35)
        self.play(FadeOut(bad_ring), FadeOut(bad_label), FadeIn(pull_lines), run_time=0.45)
        self.play(
            LaggedStart(*[
                dot.animate.move_to(target)
                for dot, target in zip(dots, compact_positions)
            ], lag_ratio=0.06),
            run_time=1.15,
        )
        self.play(FadeOut(pull_lines), ShowCreation(compact_ring), FadeIn(compact_label), run_time=0.55)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat C - inter-class similarity
    # -------------------------------------------------------------------------
    def beat_c_inter_class_similarity(self):
        title = make_scene_title(
            "Challenge 2: Inter-Class Similarity",
            "Different people can land dangerously close without enough margin",
            title_size=37,
        )

        face_a = make_image_card("face_A.png", width=1.65, height=1.92, label="Person A", label_color=BLUE, stroke_color=BLUE)
        face_b = make_image_card("face_B.png", width=1.65, height=1.92, label="Person B", label_color=GREEN, stroke_color=GREEN)
        faces = Group(face_a, face_b).arrange(RIGHT, buff=5.35)
        faces.move_to(UP * 1.18)

        plane = make_panel(width=8.85, height=3.22, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 1.25)
        boundary = Line(plane.get_top() + DOWN * 0.26, plane.get_bottom() + UP * 0.26,
                        color=RED, stroke_width=2.4, stroke_opacity=0.82)
        boundary.move_to(plane.get_center())
        boundary_label = latex(r"\text{fragile boundary}", size=19, color=RED)
        boundary_label.next_to(boundary, UP, buff=0.13)

        dot_a = Dot(point=plane.get_center() + LEFT * 0.38 + DOWN * 0.10, color=BLUE, radius=0.12)
        dot_b = Dot(point=plane.get_center() + RIGHT * 0.35 + UP * 0.08, color=GREEN, radius=0.12)
        q_dot = Dot(point=plane.get_center() + RIGHT * 0.08 + DOWN * 0.35, color=YELLOW, radius=0.10)
        labels = VGroup(
            latex(r"\text{A}", size=17, color=BLUE).next_to(dot_a, DOWN, buff=0.08),
            latex(r"\text{B}", size=17, color=GREEN).next_to(dot_b, UP, buff=0.08),
            latex(r"\text{query}", size=17, color=YELLOW).next_to(q_dot, DOWN, buff=0.08),
        )

        arrows = VGroup(
            make_flow_arrow(face_a.get_bottom(), dot_a.get_center() + UP * 0.08, color=BLUE, stroke_width=1.5),
            make_flow_arrow(face_b.get_bottom(), dot_b.get_center() + UP * 0.08, color=GREEN, stroke_width=1.5),
        )
        risk = latex(
            r"\text{small inter-class distance } \rightarrow \text{ misclassification risk}",
            size=26,
            color=YELLOW,
        )
        risk.to_edge(DOWN, buff=0.48)
        fit_to_bounds(risk, max_width=12.0)

        margin = make_double_arrow(dot_a.get_center(), dot_b.get_center(), color=YELLOW, stroke_width=2.0)
        margin_label = latex(r"\text{too close}", size=18, color=YELLOW)
        margin_label.next_to(margin, UP, buff=0.10)
        safe_margin = make_double_arrow(
            plane.get_center() + LEFT * 2.15 + DOWN * 0.74,
            plane.get_center() + RIGHT * 2.15 + DOWN * 0.74,
            color=GREEN,
            stroke_width=2.0,
        )
        safe_label = latex(r"\text{needed: wider separation}", size=18, color=GREEN)
        safe_label.next_to(safe_margin, DOWN, buff=0.10)
        layout = Group(title, faces, plane, boundary, boundary_label, dot_a, dot_b, q_dot, labels, arrows, risk, margin, margin_label, safe_margin, safe_label)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(faces), run_time=0.65)
        self.play(FadeIn(plane), run_time=0.35)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=0.55)
        self.play(FadeIn(dot_a), FadeIn(dot_b), FadeIn(VGroup(labels[0], labels[1])), run_time=0.45)
        self.play(ShowCreation(boundary), FadeIn(boundary_label), run_time=0.45)
        self.play(ShowCreation(margin), FadeIn(margin_label), run_time=0.45)
        self.play(FadeIn(q_dot), FadeIn(labels[2]), run_time=0.35)
        self.play(q_dot.animate.shift(RIGHT * 0.36), run_time=0.35)
        self.play(q_dot.animate.shift(LEFT * 0.62), run_time=0.45)
        self.play(WiggleOutThenIn(q_dot, run_time=0.65), FadeIn(risk), run_time=0.75)
        self.play(
            dot_a.animate.move_to(plane.get_center() + LEFT * 2.15 + DOWN * 0.74),
            dot_b.animate.move_to(plane.get_center() + RIGHT * 2.15 + DOWN * 0.74),
            FadeOut(margin),
            FadeOut(margin_label),
            run_time=0.85,
        )
        self.play(ShowCreation(safe_margin), FadeIn(safe_label), run_time=0.45)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat D - real world use cases
    # -------------------------------------------------------------------------
    def beat_d_real_world_pressure(self):
        title = make_scene_title(
            "Why Accuracy Matters",
            "Face recognition is often used where mistakes are visible and costly",
            title_size=38,
        )

        card_specs = [
            ("face-id.svg", "Phone unlock", "tilt + low light", CYAN),
            ("scan_component.svg", "Security camera", "low resolution", YELLOW),
            ("lock.svg", "eKYC / ID check", "selfie vs document", GREEN),
        ]
        cards = VGroup()
        for icon_file, heading, caption, color in card_specs:
            bg = RoundedRectangle(
                width=3.45,
                height=2.62,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=1.8,
                fill_color=PANEL,
                fill_opacity=0.34,
            )
            icon = make_svg_icon(icon_file, height=0.82, color=color)
            heading_mob = latex(rf"\textbf{{{heading}}}", size=22, color=WHITE)
            caption_mob = latex(rf"\text{{{caption}}}", size=17, color=MUTED)
            content = VGroup(icon, heading_mob, caption_mob).arrange(DOWN, buff=0.18)
            content.move_to(bg)
            cards.add(VGroup(bg, content))
        cards.arrange(RIGHT, buff=0.46)
        cards.move_to(UP * 0.20)

        badges = VGroup(
            make_badge("stable", color=GREEN, font_size=20),
            make_badge("accurate", color=GREEN, font_size=20),
            make_badge("robust", color=GREEN, font_size=20),
        ).arrange(RIGHT, buff=0.42)
        badges.next_to(cards, DOWN, buff=0.45)

        summary = latex(
            r"\text{The embedding must generalize, not memorize a fixed list of names.}",
            size=27,
            color=WHITE,
        )
        summary.to_edge(DOWN, buff=0.48)
        fit_to_bounds(summary, max_width=12.2)
        layout = Group(title, cards, badges, summary)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(card, shift=0.15 * UP) for card in cards], lag_ratio=0.15), run_time=0.9)
        for card in cards:
            icon = card[1][0]
            self.play(icon.animate.scale(1.15), run_time=0.12)
            self.play(icon.animate.scale(1 / 1.15), run_time=0.12)
        self.play(LaggedStart(*[FadeIn(badge) for badge in badges], lag_ratio=0.12), run_time=0.55)
        for card in cards:
            self.play(card[0].animate.set_stroke(width=3.0), run_time=0.16)
            self.play(card[0].animate.set_stroke(width=1.8), run_time=0.16)
        self.play(FadeIn(summary), run_time=0.55)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat E - transition into embedding-space scenes
    # -------------------------------------------------------------------------
    def beat_e_open_set_transition(self):
        title = make_scene_title(
            "Open-Set Reminder",
            "A new face should be placed by geometry, not forced into old labels",
            title_size=38,
        )

        query = make_image_card("face_scan.png", width=1.55, height=1.82, label="new query", label_color=YELLOW, stroke_color=YELLOW)
        query.move_to(LEFT * 4.30 + UP * 0.15)
        q_mark = latex(r"\text{?}", size=38, color=YELLOW)
        q_mark.next_to(query, UP, buff=0.12)

        space = make_panel(width=6.75, height=4.75, stroke_color=GREEN, fill_opacity=0.06)
        space.move_to(RIGHT * 2.18 + DOWN * 0.08)

        clusters = VGroup(
            make_embedding_cluster(space.get_center() + LEFT * 1.78 + UP * 1.15, BLUE, count=5),
            make_embedding_cluster(space.get_center() + RIGHT * 1.52 + UP * 0.85, GREEN, count=5),
            make_embedding_cluster(space.get_center() + LEFT * 1.18 + DOWN * 1.22, ORANGE, count=5),
        )
        labels = VGroup(
            latex(r"\text{Known A}", size=17, color=BLUE).next_to(clusters[0], DOWN, buff=0.08),
            latex(r"\text{Known B}", size=17, color=GREEN).next_to(clusters[1], DOWN, buff=0.08),
            latex(r"\text{Known C}", size=17, color=ORANGE).next_to(clusters[2], DOWN, buff=0.08),
        )
        new_dot_start = query.get_right() + RIGHT * 0.40
        new_dot = Dot(point=new_dot_start, color=YELLOW, radius=0.13)
        new_target = space.get_center() + RIGHT * 0.72 + DOWN * 0.68
        new_label = latex(r"\text{new identity}", size=18, color=YELLOW)
        new_label.next_to(new_target, RIGHT, buff=0.12)
        crowd = VGroup(*[
            Dot(
                point=space.get_center() + np.array([
                    -2.75 + (i % 9) * 0.68,
                    -1.75 + (i // 9) * 0.62,
                    0,
                ]),
                color=MUTED,
                radius=0.035,
            )
            for i in range(45)
        ])

        arrow = make_flow_arrow(query.get_right(), space.get_left(), color=YELLOW)
        question = latex(
            r"\text{Where should this face lie in identity space?}",
            size=29,
            color=CYAN,
        )
        question.to_edge(DOWN, buff=0.50)
        fit_to_bounds(question, max_width=12.0)

        transition = VGroup(
            latex(r"\text{Next: Embedding Space}", size=38, color=CYAN),
            latex(r"\text{a geometric view of face identity}", size=24, color=WHITE),
        ).arrange(DOWN, buff=0.16)
        transition.move_to(ORIGIN)
        layout = Group(title, query, q_mark, space, clusters, labels, crowd, new_dot, new_label, arrow, question)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(query), FadeIn(q_mark), run_time=0.55)
        self.play(FadeIn(space), LaggedStart(*[FadeIn(dot, scale=1.2) for dot in crowd], lag_ratio=0.004), run_time=0.70)
        self.play(LaggedStart(*[FadeIn(c) for c in clusters], lag_ratio=0.12), FadeIn(labels), run_time=0.85)
        self.play(GrowArrow(arrow), FadeIn(new_dot), run_time=0.45)
        self.play(new_dot.animate.move_to(new_target), run_time=1.0, rate_func=smooth)
        self.play(FadeIn(new_label), FadeIn(question), WiggleOutThenIn(q_mark, run_time=0.65), run_time=0.75)
        self.wait(0.8)
        clear_scene(self, run_time=0.65, wait_time=0.15)
        self.play(FadeIn(transition), run_time=0.8)
        self.wait(1.0)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def fit_group_to_frame(self, group, center=ORIGIN):
        fit_to_bounds(group, max_width=self.SAFE_WIDTH, max_height=self.SAFE_HEIGHT)
        group.move_to(center)
        return group

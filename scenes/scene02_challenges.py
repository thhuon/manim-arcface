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

        card = make_centered_title_card("Challenges")
        self.play(FadeIn(card), run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(card), run_time=0.5)

        self.beat_a_good_embedding()
        self.clear_and_wait()
        self.beat_b_intra_class_variation()
        self.clear_and_wait()
        self.beat_c_inter_class_similarity()
        self.clear_and_wait()
        self.beat_d_open_set_recognition()
        self.clear_and_wait()
        self.beat_e_conclusion_and_transition()

    # -------------------------------------------------------------------------
    # Beat A - ideal embedding space
    # -------------------------------------------------------------------------
    def beat_a_good_embedding(self):
        title = make_scene_title(
            "What Makes A Good Embedding Space?",
            title_size=38,
        )
        plane = make_panel(width=9.25, height=5.25, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.15)
        plane_label = self.make_embedding_space_label(plane, size=18)
        principle = latex(
            r"\text{Same identities should be close; different identities need room}",
            size=21,
            color=WHITE,
        )
        fit_to_bounds(principle, max_width=plane.get_width() - 0.90)
        principle.move_to(plane.get_bottom() + UP * 0.42)

        centers = [
            plane.get_center() + LEFT * 2.55 + UP * 1.03,
            plane.get_center() + RIGHT * 2.42 + UP * 0.86,
            plane.get_center() + DOWN * 0.95,
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

        layout = Group(
            title, plane, plane_label, principle,
            clusters, start_clusters, cluster_rings, cluster_labels,
            pull_arrows, separation, separation_label,
        )
        self.fit_group_to_frame(layout)
        noisy_cloud = VGroup(*[
            Dot(point=plane.get_center() + np.array([(-3.8 + i * 0.58) % 7.6 - 3.8, 1.9 - (i % 7) * 0.56, 0]),
                radius=0.050, color=[BLUE, GREEN, ORANGE][i % 3])
            for i in range(24)
        ])

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.35)
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
        self.play(FadeIn(principle), run_time=0.55)
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

        face_specs = ["face_1.png", "face_5.png", "face_9.png", "face_13.png", "face_17.png"]
        faces = Group(*[
            make_image_card(fname, width=1.25, height=1.46, show_frame=False)
            for fname in face_specs
        ])
        faces.arrange(RIGHT, buff=0.28)
        faces.move_to(UP * 1.46)

        plane = make_panel(width=10.2, height=2.55, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 1.32)
        plane_label = self.make_embedding_space_label(plane, size=18)

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
        compact_targets = VGroup(*[
            Dot(point=pos, radius=0.095, color=BLUE).set_opacity(0)
            for pos in compact_positions
        ])
        transform_arrows = VGroup(*[
            make_flow_arrow(face.get_bottom() + DOWN * 0.04, dot.get_center() + UP * 0.05, color=CYAN, stroke_width=1.4)
            for face, dot in zip(faces, dots)
        ])

        bad_ring = self.make_enclosing_ring(dots, RED, x_buff=0.62, y_buff=0.42, stroke_width=2.0)
        bad_label = make_badge("bad: scattered same identity", color=RED, font_size=19)
        bad_label.next_to(bad_ring, DOWN, buff=0.10)

        compact_ring = self.make_enclosing_ring(compact_targets, GREEN, x_buff=0.54, y_buff=0.44, stroke_width=2.2)
        compact_label = make_badge("desired: compact cluster", color=GREEN, font_size=19)
        compact_label.next_to(compact_ring, DOWN, buff=0.12)

        pull_lines = VGroup(*[
            Arrow(dot.get_center(), target.get_center(), buff=0.10, color=GREEN,
                  stroke_width=1.2, stroke_opacity=0.60, max_tip_length_to_length_ratio=0.18)
            for dot, target in zip(dots, compact_targets)
        ])
        layout = Group(
            title, faces, plane, plane_label, dots, compact_targets,
            transform_arrows, bad_ring, bad_label,
            compact_ring, compact_label, pull_lines,
        )
        self.fit_group_to_frame(layout)
        ghost_faces = Group(*[face.copy() for face in faces])

        self.play(FadeIn(title), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(face, shift=0.12 * UP) for face in faces], lag_ratio=0.08), run_time=0.9)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.45)
        self.play(LaggedStart(*[GrowArrow(a) for a in transform_arrows], lag_ratio=0.06), run_time=0.55)
        self.add(ghost_faces)
        self.play(FadeOut(ghost_faces), run_time=0.90)
        self.play(LaggedStart(*[FadeIn(dot, scale=1.25) for dot in dots], lag_ratio=0.08), run_time=0.25)
        self.play(ShowCreation(bad_ring), FadeIn(bad_label), run_time=0.55)
        self.play(dots[1].animate.shift(UP * 0.18 + LEFT * 0.16), dots[3].animate.shift(DOWN * 0.17 + RIGHT * 0.14), run_time=0.30)
        self.play(dots[1].animate.shift(DOWN * 0.18 + RIGHT * 0.16), dots[3].animate.shift(UP * 0.17 + LEFT * 0.14), run_time=0.30)
        self.wait(0.35)
        self.play(FadeOut(bad_ring), FadeOut(bad_label), FadeIn(pull_lines), run_time=0.45)
        self.play(
            LaggedStart(*[
                dot.animate.move_to(target.get_center())
                for dot, target in zip(dots, compact_targets)
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

        face_files = ["clusterB_1.png", "clusterB_2.png", "clusterB_3.png", "clusterB_4.png"]
        identity_colors = [BLUE, GREEN, ORANGE, PURPLE]
        identity_names = ["Person A", "Person B", "Person C", "Person D"]
        faces = Group(*[
            make_image_card(fname, width=1.18, height=1.58, show_frame=False)
            for fname in face_files
        ])
        faces.arrange(RIGHT, buff=0.72)
        faces.move_to(UP * 1.68)
        face_labels = VGroup(*[
            latex(rf"\text{{{name}}}", size=16, color=color).next_to(face, DOWN, buff=0.07)
            for face, name, color in zip(faces, identity_names, identity_colors)
        ])

        plane = make_panel(width=8.85, height=3.05, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 1.35)
        plane_label = self.make_embedding_space_label(plane, size=18)
        boundary = Line(plane.get_top() + DOWN * 0.26, plane.get_bottom() + UP * 0.26,
                        color=RED, stroke_width=2.4, stroke_opacity=0.82)
        boundary.move_to(plane.get_center())
        boundary_label = latex(r"\text{fragile boundary}", size=19, color=RED)
        boundary_label.next_to(boundary, UP, buff=0.13)

        dot_positions = [
            plane.get_center() + LEFT * 0.62 + DOWN * 0.08,
            plane.get_center() + RIGHT * 0.50 + UP * 0.10,
            plane.get_center() + LEFT * 0.22 + UP * 0.24,
            plane.get_center() + RIGHT * 0.12 + DOWN * 0.32,
        ]
        dots = VGroup(*[
            Dot(point=pos, color=color, radius=0.105)
            for pos, color in zip(dot_positions, identity_colors)
        ])
        dot_a, dot_b, dot_c, dot_d = dots
        q_dot = Dot(point=plane.get_center() + RIGHT * 0.08 + DOWN * 0.50, color=YELLOW, radius=0.10)
        labels = VGroup(
            latex(r"\text{A}", size=17, color=BLUE).next_to(dot_a, DOWN, buff=0.08),
            latex(r"\text{B}", size=17, color=GREEN).next_to(dot_b, UP, buff=0.08),
            latex(r"\text{C}", size=17, color=ORANGE).next_to(dot_c, UP, buff=0.08),
            latex(r"\text{D}", size=17, color=PURPLE).next_to(dot_d, DOWN, buff=0.08),
            latex(r"\text{query}", size=17, color=YELLOW).next_to(q_dot, DOWN, buff=0.08),
        )

        arrows = VGroup(*[
            make_flow_arrow(face.get_bottom(), dot.get_center() + UP * 0.08, color=color, stroke_width=1.5)
            for face, dot, color in zip(faces, dots, identity_colors)
        ])
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
        separated_targets = [
            plane.get_center() + LEFT * 2.15 + DOWN * 0.74,
            plane.get_center() + RIGHT * 2.15 + DOWN * 0.74,
            plane.get_center() + LEFT * 2.40 + UP * 0.20,
            plane.get_center() + RIGHT * 2.40 + UP * 0.20,
        ]
        safe_dots = VGroup(*[
            Dot(point=pos, color=color, radius=0.105).set_opacity(0)
            for pos, color in zip(separated_targets, identity_colors)
        ])
        safe_labels = VGroup(
            latex(r"\text{A}", size=17, color=BLUE).next_to(safe_dots[0], DOWN, buff=0.08),
            latex(r"\text{B}", size=17, color=GREEN).next_to(safe_dots[1], DOWN, buff=0.08),
            latex(r"\text{C}", size=17, color=ORANGE).next_to(safe_dots[2], UP, buff=0.08),
            latex(r"\text{D}", size=17, color=PURPLE).next_to(safe_dots[3], UP, buff=0.08),
        )
        safe_labels.set_opacity(0)
        layout = Group(
            title, faces, face_labels, plane, plane_label,
            boundary, boundary_label, dots, q_dot, labels, arrows,
            risk, margin, margin_label, safe_dots, safe_labels,
            safe_margin, safe_label,
        )
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(faces), FadeIn(face_labels), run_time=0.65)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.35)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=0.55)
        self.play(FadeIn(dots), FadeIn(VGroup(labels[0], labels[1], labels[2], labels[3])), run_time=0.45)
        self.play(ShowCreation(boundary), FadeIn(boundary_label), run_time=0.45)
        self.play(ShowCreation(margin), FadeIn(margin_label), run_time=0.45)
        self.play(FadeIn(q_dot), FadeIn(labels[4]), run_time=0.35)
        self.play(q_dot.animate.shift(RIGHT * 0.36), run_time=0.35)
        self.play(q_dot.animate.shift(LEFT * 0.62), run_time=0.45)
        self.play(WiggleOutThenIn(q_dot, run_time=0.65), FadeIn(risk), run_time=0.75)
        self.play(
            dot_a.animate.move_to(safe_dots[0].get_center()),
            dot_b.animate.move_to(safe_dots[1].get_center()),
            dot_c.animate.move_to(safe_dots[2].get_center()),
            dot_d.animate.move_to(safe_dots[3].get_center()),
            labels[0].animate.move_to(safe_labels[0].get_center()),
            labels[1].animate.move_to(safe_labels[1].get_center()),
            labels[2].animate.move_to(safe_labels[2].get_center()),
            labels[3].animate.move_to(safe_labels[3].get_center()),
            FadeOut(margin),
            FadeOut(margin_label),
            run_time=0.85,
        )
        self.play(ShowCreation(safe_margin), FadeIn(safe_label), run_time=0.45)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat D - Challenge 3: Open-Set Recognition
    # PLAN Narration D:
    # "Bài toán còn trở nên khó khăn hơn khi số lượng danh tính
    # ngày càng tăng... Khi số lượng danh tính tăng lên, không gian
    # biểu diễn trở nên ngày càng đông đúc. Việc duy trì ranh giới
    # rõ ràng giữa các lớp trở nên khó khăn hơn rất nhiều... Một khuôn
    # mặt hoàn toàn mới có thể xuất hiện mà mô hình chưa từng nhìn
    # thấy... mô hình phải học được những quy luật tổng quát về danh
    # tính... mục tiêu cuối cùng là xây dựng một không gian biểu diễn có
    # khả năng khái quát hóa tốt."
    # -------------------------------------------------------------------------
    def beat_d_open_set_recognition(self):
        title = make_scene_title(
            "Challenge 3: Open-Set Recognition",
            "New identities keep appearing — can the system handle the unknown?",
            title_size=37,
        )

        # ---- Single embedding space panel ----
        plane = make_panel(width=11.0, height=5.60, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.10)
        plane_label = self.make_embedding_space_label(plane, size=18)

        # ---- Phase 1: Two known identities with clear boundary ----
        center_a = plane.get_center() + LEFT * 2.20 + UP * 0.50
        center_b = plane.get_center() + RIGHT * 2.20 + DOWN * 0.50

        cluster_a = make_embedding_cluster(center_a, color=BLUE, scale=0.78, count=4)
        cluster_b = make_embedding_cluster(center_b, color=GREEN, scale=0.78, count=4)
        dot_a_label = latex(r"\text{A}", size=17, color=BLUE).next_to(cluster_a, UP, buff=0.06)
        dot_b_label = latex(r"\text{B}", size=17, color=GREEN).next_to(cluster_b, DOWN, buff=0.06)

        boundary = Line(
            plane.get_top() + DOWN * 0.40,
            plane.get_bottom() + UP * 0.40,
            color=RED, stroke_width=2.0, stroke_opacity=0.80,
        )
        boundary.move_to(plane.get_center())
        boundary_label = latex(r"\text{clear boundary}", size=18, color=RED)
        boundary_label.next_to(boundary, UP, buff=0.12)

        # ---- Phase 2: New identities proliferate, boundary blurs ----
        center_c = plane.get_center() + LEFT * 0.20 + UP * 0.70
        center_d = plane.get_center() + RIGHT * 0.40 + UP * 0.60
        center_e = plane.get_center() + LEFT * 0.80 + DOWN * 0.80

        cluster_c = make_embedding_cluster(center_c, color=ORANGE, scale=0.68, count=3)
        cluster_d = make_embedding_cluster(center_d, color=PURPLE, scale=0.68, count=3)
        cluster_e = make_embedding_cluster(center_e, color=PINK, scale=0.68, count=3)

        dot_c_label = latex(r"\text{C}", size=16, color=ORANGE).next_to(cluster_c, UP, buff=0.06)
        dot_d_label = latex(r"\text{D}", size=16, color=PURPLE).next_to(cluster_d, DOWN, buff=0.06)
        dot_e_label = latex(r"\text{E}", size=16, color=PINK).next_to(cluster_e, UP, buff=0.06)

        # blurred boundary: multiple overlapping lines
        blur_boundary_1 = Line(
            plane.get_center() + UP * 0.05 + LEFT * 0.30,
            plane.get_center() + DOWN * 0.05 + RIGHT * 0.30,
            color=RED, stroke_width=2.0, stroke_opacity=0.45,
        )
        blur_boundary_2 = Line(
            plane.get_center() + UP * 0.20 + LEFT * 0.10,
            plane.get_center() + DOWN * 0.20 + RIGHT * 0.10,
            color=RED, stroke_width=1.5, stroke_opacity=0.30,
        )
        blur_label = latex(r"\text{boundaries overlap}", size=18, color=RED)
        blur_label.next_to(plane.get_center() + DOWN * 0.90, DOWN, buff=0.08)

        # ---- Phase 3: Completely new face appears ----
        new_face = make_image_card(
            "face_scan.png", width=1.50, height=1.75,
            label="unseen face", label_color=YELLOW, stroke_color=YELLOW,
        )
        new_face.move_to(plane.get_center() + LEFT * 4.85 + UP * 0.40)

        new_dot = Dot(
            point=plane.get_center() + RIGHT * 0.10 + UP * 0.15,
            color=YELLOW, radius=0.12,
        )
        new_dot_target = Dot(
            point=center_d + RIGHT * 0.70 + UP * 0.30,
            color=YELLOW, radius=0.12,
        ).set_opacity(0)
        new_dot_label = latex(r"\text{?}", size=28, color=YELLOW)
        new_dot_label.move_to(new_dot.get_center() + UP * 0.38)

        arrow_new = make_flow_arrow(
            new_face.get_right() + RIGHT * 0.05,
            new_dot.get_center() + LEFT * 0.18,
            color=YELLOW, stroke_width=1.8,
        )

        # connection line: new dot placed by geometry (similarity to cluster D)
        connection_line = Line(
            new_dot.get_center(),
            center_d,
            color=YELLOW, stroke_width=1.5, stroke_opacity=0.60,
        )

        # ---- Bottom summary text ----
        summary = latex(
            r"\text{Generalization, not memorization — the embedding must work for any face.}",
            size=26,
            color=WHITE,
        )
        summary.to_edge(DOWN, buff=0.48)
        fit_to_bounds(summary, max_width=12.0)

        layout = Group(
            title, plane, plane_label,
            cluster_a, cluster_b, cluster_c, cluster_d, cluster_e,
            dot_a_label, dot_b_label, dot_c_label, dot_d_label, dot_e_label,
            boundary, boundary_label,
            blur_boundary_1, blur_boundary_2, blur_label,
            new_face, new_dot, new_dot_target, new_dot_label, arrow_new, connection_line,
            summary,
        )
        self.fit_group_to_frame(layout)

        # ---- Phase 1: Two known identities + clear boundary ----
        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.35)
        self.play(FadeIn(cluster_a), FadeIn(dot_a_label), run_time=0.30)
        self.play(FadeIn(cluster_b), FadeIn(dot_b_label), run_time=0.30)
        self.play(ShowCreation(boundary), FadeIn(boundary_label), run_time=0.50)
        self.wait(0.60)

        # ---- Phase 2: New identities proliferate, boundary blurs ----
        self.play(
            FadeIn(cluster_c), FadeIn(dot_c_label),
            FadeIn(cluster_d), FadeIn(dot_d_label),
            FadeIn(cluster_e), FadeIn(dot_e_label),
            run_time=0.80,
        )
        self.play(FadeOut(boundary), FadeOut(boundary_label), run_time=0.35)
        self.play(
            LaggedStart(*[
                ShowCreationThenDestruction(blur_boundary_1),
                ShowCreationThenDestruction(blur_boundary_2),
            ], lag_ratio=0.20),
            FadeIn(blur_label),
            run_time=0.70,
        )
        self.wait(0.45)

        # ---- Phase 3: New unseen face appears ----
        self.play(FadeIn(new_face), FadeIn(arrow_new), run_time=0.50)
        self.play(
            FadeIn(new_dot),
            FadeIn(new_dot_label),
            GrowArrow(connection_line),
            run_time=0.65,
        )
        # Show new dot placed by geometric similarity (near D)
        self.play(
            new_dot.animate.move_to(new_dot_target.get_center()),
            new_dot_label.animate.move_to(new_dot_target.get_center() + UP * 0.38),
            connection_line.animate.become(
                Line(
                    new_dot_target.get_center(),
                    cluster_d.get_center(),
                    color=YELLOW, stroke_width=1.5, stroke_opacity=0.60,
                )
            ),
            run_time=1.0,
            rate_func=smooth,
        )
        # Bounce the question mark to emphasize uncertainty
        self.play(WiggleOutThenIn(new_dot_label, run_time=0.70), run_time=0.75)

        self.play(FadeIn(summary), run_time=0.55)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat E - Conclusion + Embedding Transition
    # PLAN Narration E: "Vì vậy, một hệ thống Face Recognition hiệu quả cần giải
    # quyết: 1) cùng một người phải đưa lại gần nhau trong không gian biểu diễn;
    # 2) những người khác nhau phải tách biệt đủ xa; 3) cấu trúc vẫn phải duy trì
    # khả năng tổng quát hóa cho những danh tính chưa từng xuất hiện...
    # Các vấn đề trọng tâm mà ArcFace tập trung giải quyết."
    # PLAN Narration F: "Tới đây, ta hiểu được rằng các danh tính phải được gom
    # thành cụm và biểu diễn ở một không gian nào đó. Để hiểu cách các hệ thống
    # hiện đại xây dựng không gian đó, chúng ta cần tìm hiểu: Embedding."
    # -------------------------------------------------------------------------
    def beat_e_conclusion_and_transition(self):
        title = make_scene_title(
            "Summary: The Three Geometric Goals",
            "Compact clusters · Clear separation · Generalizable structure",
            title_size=37,
        )

        plane = make_panel(width=10.0, height=5.50, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.08)
        plane_label = self.make_embedding_space_label(plane, size=18)

        # two known clusters plus one unseen identity for open-set generalization
        center_a = plane.get_center() + LEFT * 2.40 + UP * 0.90
        center_b = plane.get_center() + RIGHT * 2.40 + UP * 0.90
        new_identity_center = plane.get_center() + DOWN * 1.05
        centers = [center_a, center_b]
        colors = [BLUE, GREEN]

        clusters = VGroup(*[
            make_embedding_cluster(c, color=col, scale=0.82, count=5)
            for c, col in zip(centers, colors)
        ])
        rings = VGroup(*[
            Ellipse(width=1.55, height=1.15, stroke_color=col, stroke_width=1.8, fill_opacity=0).move_to(c)
            for c, col in zip(centers, colors)
        ])
        cluster_labels = VGroup(*[
            latex(rf"\text{{{lbl}}}", size=20, color=col).next_to(ring, DOWN, buff=0.10)
            for lbl, col, ring in zip(["Person A", "Person B"], colors, rings)
        ])

        # goal badges: intra-class compact, inter-class separation, open-set generalization
        goal_a = make_badge("intra-class compact", color=CYAN, font_size=18)
        goal_a.next_to(rings[0], DOWN, buff=0.85)
        goal_b = make_badge("inter-class separation", color=YELLOW, font_size=18)
        goal_b.next_to(rings[1], DOWN, buff=0.85)
        new_dot = Dot(point=new_identity_center, color=YELLOW, radius=0.12)
        new_label = latex(r"\text{new identity}", size=18, color=YELLOW)
        new_label.next_to(new_dot, RIGHT, buff=0.12)
        goal_c = make_badge("open-set generalization", color=GREEN, font_size=18)
        goal_c.next_to(new_dot, DOWN, buff=0.72)
        goals = VGroup(goal_a, goal_b, goal_c)

        # arrows from each goal badge to its cluster
        goal_arrow_a = Arrow(goal_a.get_top(), rings[0].get_bottom() + DOWN * 0.12,
                             buff=0.05, color=CYAN, stroke_width=1.2, max_tip_length_to_length_ratio=0.22)
        goal_arrow_b = Arrow(goal_b.get_top(), rings[1].get_bottom() + DOWN * 0.12,
                             buff=0.05, color=YELLOW, stroke_width=1.2, max_tip_length_to_length_ratio=0.22)
        goal_arrow_c = Arrow(goal_c.get_top(), new_dot.get_bottom(),
                             buff=0.05, color=GREEN, stroke_width=1.2, max_tip_length_to_length_ratio=0.22)
        goal_arrows = VGroup(goal_arrow_a, goal_arrow_b, goal_arrow_c)

        # separation double arrow between cluster A and B
        sep_arrow = make_double_arrow(
            centers[0] + RIGHT * 0.85 + DOWN * 0.05,
            centers[1] + LEFT * 0.85 + DOWN * 0.05,
            color=YELLOW,
            stroke_width=2.0,
        )
        sep_label = latex(r"\text{large margin}", size=19, color=YELLOW)
        sep_label.next_to(sep_arrow, DOWN, buff=0.10)

        # geometric framing text at bottom
        framing = latex(
            r"\text{Identity space must be organized geometrically — not just labeled.}",
            size=26,
            color=WHITE,
        )
        framing.to_edge(DOWN, buff=0.48)
        fit_to_bounds(framing, max_width=12.0)

        layout = Group(
            title, plane, plane_label, clusters, rings, cluster_labels,
            goals, goal_arrows,
            sep_arrow, sep_label,
            new_dot, new_label,
            framing,
        )
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.35)

        # reveal each cluster with its label and goal badge
        for cluster, ring, lbl, goal, arr in zip(clusters, rings, cluster_labels, [goal_a, goal_b], [goal_arrow_a, goal_arrow_b]):
            self.play(FadeIn(cluster), FadeIn(ring), FadeIn(lbl), run_time=0.30)
            self.play(FadeIn(goal), GrowArrow(arr), run_time=0.30)

        # show separation between clusters
        self.play(ShowCreation(sep_arrow), FadeIn(sep_label), run_time=0.50)

        # show new identity placed by geometry
        self.play(
            FadeIn(new_dot),
            FadeIn(new_label),
            FadeIn(goal_c),
            GrowArrow(goal_arrow_c),
            run_time=0.45,
        )
        # gently bounce the new dot to indicate it can be placed
        self.play(new_dot.animate.shift(UP * 0.15), run_time=0.18)
        self.play(new_dot.animate.shift(DOWN * 0.15), run_time=0.18)
        self.play(new_dot.animate.shift(UP * 0.10), run_time=0.12)
        self.play(new_dot.animate.shift(DOWN * 0.10), run_time=0.12)

        self.play(FadeIn(framing), run_time=0.55)

        # pulsing highlight on all rings
        for ring in rings:
            self.play(ring.animate.scale(1.08), run_time=0.12)
            self.play(ring.animate.scale(1 / 1.08), run_time=0.12)
        self.wait(0.8)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def fit_group_to_frame(self, group, center=ORIGIN):
        fit_to_bounds(group, max_width=self.SAFE_WIDTH, max_height=self.SAFE_HEIGHT)
        group.move_to(center)
        return group

    def make_embedding_space_label(self, plane, size=18):
        label = latex(r"\text{embedding space}", size=size, color=MUTED)
        label.move_to(plane.get_corner(UL) + RIGHT * 0.88 + DOWN * 0.26)
        return label

    def make_enclosing_ring(self, dots, color, x_buff=0.52, y_buff=0.36, stroke_width=2.0):
        ring = Ellipse(
            width=dots.get_width() + x_buff,
            height=dots.get_height() + y_buff,
            stroke_color=color,
            stroke_width=stroke_width,
            fill_opacity=0,
        )
        ring.move_to(dots.get_center())
        return ring

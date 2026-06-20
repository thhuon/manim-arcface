from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 03 - Embedding Space
# Keeps the public class name used by existing render commands while rebuilding
# the content around PLAN.md Scene 3: how face images become geometric points.
# =============================================================================


class Scene03_EmbeddingSpace(Scene):
    SAFE_WIDTH = 12.25
    SAFE_HEIGHT = 6.80

    def construct(self):
        self.camera.background_color = DARK

        self.beat_a_manual_grouping()
        self.clear_and_wait()
        self.beat_b_network_embedding()
        self.clear_and_wait()
        self.beat_c_distance_meaning()
        self.clear_and_wait()
        self.beat_d_training_shapes_space()
        self.clear_and_wait()
        self.beat_e_loss_transition()

    # -------------------------------------------------------------------------
    # Beat A - table full of mixed faces, then human-style grouping.
    # -------------------------------------------------------------------------
    def beat_a_manual_grouping(self):
        title = make_scene_title(
            "Embedding Space",
            "A geometric way to organize face identity",
            title_size=40,
        )

        face_specs = [
            ("clusterA_1.png", BLUE), ("clusterB_1.png", GREEN), ("face_1.png", ORANGE),
            ("clusterA_2.png", BLUE), ("face_5.png", ORANGE), ("clusterB_2.png", GREEN),
            ("face_9.png", ORANGE), ("clusterA_3.png", BLUE), ("clusterB_3.png", GREEN),
            ("clusterB_4.png", GREEN), ("face_13.png", ORANGE), ("clusterA_4.png", BLUE),
        ]
        table = Group(*[
            make_image_card(filename, width=0.86, height=1.02, stroke_color=color, show_frame=False)
            for filename, color in face_specs
        ])
        for i, card in enumerate(table):
            row = i // 4
            col = i % 4
            card.move_to(np.array([
                (col - 1.5) * 1.08,
                (1 - row) * 1.18,
                0,
            ]))
        table.move_to(LEFT * 3.35 + DOWN * 0.10)

        table_label = make_badge("mixed face images", color=CYAN, font_size=18)
        table_label.next_to(table, DOWN, buff=0.18)

        plane = make_panel(width=5.25, height=4.70, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(RIGHT * 3.00 + DOWN * 0.12)
        plane_label = make_badge("identity space", color=GREEN, font_size=18)
        plane_label.next_to(plane, DOWN, buff=0.18)

        centers = [
            plane.get_center() + LEFT * 1.40 + UP * 1.10,
            plane.get_center() + RIGHT * 1.34 + UP * 0.78,
            plane.get_center() + DOWN * 1.18,
        ]
        colors = [BLUE, GREEN, ORANGE]
        labels = ["Person A", "Person B", "Person C"]
        cluster_targets = [
            [
                center + offset
                for offset in [ORIGIN, RIGHT * 0.30 + UP * 0.10, LEFT * 0.25 + UP * 0.18, RIGHT * 0.12 + DOWN * 0.26]
            ]
            for center in centers
        ]

        target_cards = Group()
        target_labels = VGroup()
        for center, color, label in zip(centers, colors, labels):
            ring = Ellipse(width=1.35, height=1.05, stroke_color=color, stroke_width=1.8, fill_opacity=0)
            ring.move_to(center)
            target_cards.add(ring)
            target_labels.add(latex(rf"\text{{{label}}}", size=17, color=color).next_to(ring, DOWN, buff=0.08))

        moving_cards = Group(*[card.copy() for card in table])
        layout = Group(title, table, table_label, plane, plane_label, target_cards, target_labels, moving_cards)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(card, scale=1.05) for card in table], lag_ratio=0.04), FadeIn(table_label), run_time=1.0)
        self.play(FadeIn(plane), FadeIn(plane_label), run_time=0.40)
        self.add(moving_cards)
        self.play(FadeOut(table), FadeOut(table_label), run_time=0.20)

        group_indices = {BLUE: 0, GREEN: 1, ORANGE: 2}
        counters = [0, 0, 0]
        animations = []
        for card, (_, color) in zip(moving_cards, face_specs):
            group_id = group_indices[color]
            target = cluster_targets[group_id][counters[group_id] % 4]
            counters[group_id] += 1
            animations.append(card.animate.set_width(0.48).move_to(target))
        self.play(LaggedStart(*animations, lag_ratio=0.035), run_time=1.55, rate_func=smooth)
        self.play(FadeIn(target_cards), FadeIn(target_labels), run_time=0.55)
        for ring in target_cards:
            self.play(ring.animate.scale(1.08), run_time=0.12)
            self.play(ring.animate.scale(1 / 1.08), run_time=0.12)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat B - neural network replaces manual sorting.
    # -------------------------------------------------------------------------
    def beat_b_network_embedding(self):
        title = make_scene_title(
            "The Network Learns To Place Faces",
            "Each image becomes an embedding vector",
            title_size=39,
        )

        input_face = make_image_card("face_normal.png", width=1.55, height=1.84, stroke_color=CYAN)
        input_face.move_to(LEFT * 4.70 + DOWN * 0.08)
        input_label = make_badge("face image", color=CYAN, font_size=18)
        input_label.next_to(input_face, DOWN, buff=0.15)

        net = make_neural_network().scale(1.35)
        net.move_to(LEFT * 1.35 + DOWN * 0.02)
        net_label = make_badge("neural network", color=ORANGE, font_size=18)
        net_label.next_to(net, DOWN, buff=0.22)

        vector = make_vector([r"0.28", r"-0.61", r"0.74", r"\vdots", r"0.19"], font_size=21)
        vector.move_to(RIGHT * 1.82 + UP * 0.82)
        vector_label = make_badge("embedding", color=GREEN, font_size=18)
        vector_label.next_to(vector, DOWN, buff=0.16)

        plane = make_panel(width=3.25, height=2.62, stroke_color=GREEN, fill_opacity=0.06)
        plane.move_to(RIGHT * 4.55 + DOWN * 0.68)
        axes = VGroup(
            Line(plane.get_left() + RIGHT * 0.25, plane.get_right() + LEFT * 0.25, color=MUTED, stroke_width=1.0),
            Line(plane.get_bottom() + UP * 0.22, plane.get_top() + DOWN * 0.22, color=MUTED, stroke_width=1.0),
        )
        point = Dot(point=plane.get_center() + RIGHT * 0.60 + UP * 0.35, color=YELLOW, radius=0.12)
        point_label = latex(r"\text{one point}", size=17, color=YELLOW)
        point_label.next_to(point, RIGHT, buff=0.10)

        arrows = VGroup(
            make_flow_arrow(input_face.get_right(), net.get_left(), color=CYAN),
            make_flow_arrow(net.get_right(), vector.get_left(), color=ORANGE),
            make_flow_arrow(vector.get_right(), point.get_center() + LEFT * 0.08, color=GREEN),
        )
        layout = Group(title, input_face, input_label, net, net_label, vector, vector_label, plane, axes, point, point_label, arrows)
        self.fit_group_to_frame(layout)

        packets = VGroup(*[
            Dot(point=input_face.get_right() + RIGHT * 0.05, color=CYAN if i < 3 else YELLOW, radius=0.045)
            for i in range(7)
        ])
        net_path = Line(input_face.get_right() + RIGHT * 0.10, net.get_right() + RIGHT * 0.20)
        layer_highlights = VGroup(*[
            RoundedRectangle(
                width=layer.get_width() + 0.20,
                height=layer.get_height() + 0.20,
                corner_radius=0.07,
                stroke_color=YELLOW,
                stroke_width=1.8,
                fill_opacity=0,
            ).move_to(layer)
            for layer in net[1]
        ])
        value_flash = VGroup(*[
            entry.copy().set_color(YELLOW)
            for entry in vector[1]
        ])

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(input_face), FadeIn(input_label), run_time=0.45)
        self.play(GrowArrow(arrows[0]), FadeIn(net), FadeIn(net_label), run_time=0.60)
        self.add(packets)
        self.play(
            LaggedStart(*[MoveAlongPath(packet, net_path) for packet in packets], lag_ratio=0.055),
            LaggedStart(*[ShowPassingFlash(box, time_width=0.85) for box in layer_highlights], lag_ratio=0.16),
            run_time=1.20,
        )
        self.play(FadeOut(packets), run_time=0.15)
        self.play(GrowArrow(arrows[1]), FadeIn(vector), FadeIn(vector_label), run_time=0.65)
        self.play(LaggedStart(*[FadeIn(v, scale=1.25) for v in value_flash], lag_ratio=0.04), run_time=0.35)
        self.play(FadeOut(value_flash), run_time=0.20)
        self.play(FadeIn(plane), ShowCreation(axes), run_time=0.45)
        self.play(GrowArrow(arrows[2]), Transform(vector.copy(), point), run_time=0.80)
        self.add(point)
        self.play(FadeIn(point_label), run_time=0.30)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat C - geometric meaning: close means similar, far means different.
    # -------------------------------------------------------------------------
    def beat_c_distance_meaning(self):
        title = make_scene_title(
            "Distances Carry The Meaning",
            "Coordinates matter less than relative geometry",
            title_size=39,
        )

        plane = make_panel(width=8.70, height=4.95, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.10)
        axes = VGroup(
            Line(plane.get_left() + RIGHT * 0.35, plane.get_right() + LEFT * 0.35, color=MUTED, stroke_width=1.0),
            Line(plane.get_bottom() + UP * 0.30, plane.get_top() + DOWN * 0.30, color=MUTED, stroke_width=1.0),
        )

        a1 = Dot(point=plane.get_center() + LEFT * 2.15 + UP * 0.70, color=BLUE, radius=0.11)
        a2 = Dot(point=plane.get_center() + LEFT * 1.70 + UP * 0.94, color=BLUE, radius=0.11)
        b1 = Dot(point=plane.get_center() + RIGHT * 2.10 + DOWN * 0.45, color=GREEN, radius=0.11)
        q = Dot(point=plane.get_center() + LEFT * 1.95 + UP * 0.36, color=YELLOW, radius=0.11)

        near = make_double_arrow(a1.get_center(), q.get_center(), color=GREEN, stroke_width=1.9)
        far = make_double_arrow(q.get_center(), b1.get_center(), color=RED, stroke_width=1.6)
        near_label = make_badge("near: likely same identity", color=GREEN, font_size=18)
        near_label.next_to(near, LEFT, buff=0.15)
        far_label = make_badge("far: likely different", color=RED, font_size=18)
        far_label.next_to(far, DOWN, buff=0.14)

        cluster_a = Ellipse(width=1.20, height=0.90, stroke_color=BLUE, stroke_width=1.7, fill_opacity=0).move_to(VGroup(a1, a2, q))
        label_a = latex(r"\text{Person A region}", size=18, color=BLUE)
        label_a.next_to(cluster_a, UP, buff=0.10)
        label_b = latex(r"\text{Person B}", size=18, color=GREEN)
        label_b.next_to(b1, DOWN, buff=0.12)

        q_label = latex(r"\text{query}", size=17, color=YELLOW)
        q_label.next_to(q, DOWN, buff=0.10)
        layout = Group(title, plane, axes, a1, a2, b1, q, near, far, near_label, far_label, cluster_a, label_a, label_b, q_label)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(plane), ShowCreation(axes), run_time=0.45)
        self.play(FadeIn(a1), FadeIn(a2), FadeIn(b1), FadeIn(label_b), run_time=0.45)
        self.play(FadeIn(q), FadeIn(q_label), run_time=0.35)
        self.play(ShowCreation(near), FadeIn(near_label), run_time=0.55)
        self.play(q.animate.move_to(a1.get_center() + RIGHT * 0.18 + DOWN * 0.10), q_label.animate.next_to(a1.get_center() + RIGHT * 0.18 + DOWN * 0.10, DOWN, buff=0.10), run_time=0.55)
        self.play(ShowCreation(cluster_a), FadeIn(label_a), run_time=0.45)
        self.play(ShowCreation(far), FadeIn(far_label), run_time=0.55)
        self.play(WiggleOutThenIn(b1, run_time=0.55), run_time=0.55)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat D - training gradually shapes the space.
    # -------------------------------------------------------------------------
    def beat_d_training_shapes_space(self):
        title = make_scene_title(
            "Embedding Space Is Learned",
            "Training moves points until identity geometry becomes useful",
            title_size=38,
        )

        plane = make_panel(width=9.50, height=5.05, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.08)
        colors = [BLUE, GREEN, ORANGE]
        targets = [
            plane.get_center() + LEFT * 2.60 + UP * 1.05,
            plane.get_center() + RIGHT * 2.20 + UP * 0.82,
            plane.get_center() + DOWN * 1.25,
        ]

        start_points = [
            plane.get_center() + np.array([-3.60, -1.55, 0]),
            plane.get_center() + np.array([-2.80, 1.60, 0]),
            plane.get_center() + np.array([-1.45, -0.55, 0]),
            plane.get_center() + np.array([-0.55, 1.35, 0]),
            plane.get_center() + np.array([0.35, -1.25, 0]),
            plane.get_center() + np.array([1.20, 1.55, 0]),
            plane.get_center() + np.array([2.05, -0.35, 0]),
            plane.get_center() + np.array([3.10, 1.10, 0]),
            plane.get_center() + np.array([3.45, -1.45, 0]),
        ]
        final_points = [
            targets[i % 3] + offset
            for i, offset in enumerate([
                LEFT * 0.20 + UP * 0.10, RIGHT * 0.26, DOWN * 0.20,
                LEFT * 0.22 + UP * 0.18, RIGHT * 0.20 + DOWN * 0.14, UP * 0.24,
                LEFT * 0.18 + DOWN * 0.12, RIGHT * 0.24 + UP * 0.10, DOWN * 0.24,
            ])
        ]
        dots = VGroup(*[
            Dot(point=point, color=colors[i % 3], radius=0.095)
            for i, point in enumerate(start_points)
        ])
        arrows = VGroup(*[
            Arrow(dot.get_center(), target, buff=0.08, color=dot.get_color(), stroke_width=1.1,
                  stroke_opacity=0.55, max_tip_length_to_length_ratio=0.16)
            for dot, target in zip(dots, final_points)
        ])
        rings = VGroup(*[
            Ellipse(width=1.32, height=1.02, stroke_color=color, stroke_width=1.7, fill_opacity=0).move_to(target)
            for color, target in zip(colors, targets)
        ])
        step_labels = VGroup(
            make_badge("prediction", color=CYAN, font_size=18),
            make_badge("loss signal", color=YELLOW, font_size=18),
            make_badge("backprop update", color=GREEN, font_size=18),
        ).arrange(RIGHT, buff=0.35)
        step_labels.to_edge(DOWN, buff=0.48)
        layout = Group(title, plane, dots, arrows, rings, step_labels)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(plane), LaggedStart(*[FadeIn(dot, scale=1.2) for dot in dots], lag_ratio=0.04), run_time=0.75)
        self.play(FadeIn(step_labels[0]), run_time=0.28)
        self.play(FadeIn(step_labels[1]), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.02), run_time=0.65)
        self.play(
            FadeIn(step_labels[2]),
            LaggedStart(*[
                dot.animate.move_to(target)
                for dot, target in zip(dots, final_points)
            ], lag_ratio=0.04),
            run_time=1.35,
            rate_func=smooth,
        )
        self.play(FadeOut(arrows), FadeIn(rings), run_time=0.45)
        for ring in rings:
            self.play(ring.animate.scale(1.07), run_time=0.10)
            self.play(ring.animate.scale(1 / 1.07), run_time=0.10)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat E - bridge to loss functions / Softmax.
    # -------------------------------------------------------------------------
    def beat_e_loss_transition(self):
        title = make_scene_title(
            "What Objective Shapes The Space?",
            "The next question is the loss function",
            title_size=38,
        )

        left = make_panel(width=4.55, height=3.65, stroke_color=RED, fill_opacity=0.06)
        left.move_to(LEFT * 2.95 + DOWN * 0.18)
        right = make_panel(width=4.55, height=3.65, stroke_color=GREEN, fill_opacity=0.06)
        right.move_to(RIGHT * 2.95 + DOWN * 0.18)

        loose = VGroup(
            make_embedding_cluster(left.get_center() + LEFT * 0.72 + UP * 0.50, BLUE, scale=1.55, count=5),
            make_embedding_cluster(left.get_center() + RIGHT * 0.78 + DOWN * 0.36, GREEN, scale=1.45, count=5),
        )
        tight = VGroup(
            make_embedding_cluster(right.get_center() + LEFT * 1.02 + UP * 0.62, BLUE, scale=0.75, count=5),
            make_embedding_cluster(right.get_center() + RIGHT * 1.05 + DOWN * 0.50, GREEN, scale=0.75, count=5),
        )
        loose_label = make_badge("weak geometry", color=RED, font_size=18)
        loose_label.next_to(left, DOWN, buff=0.16)
        tight_label = make_badge("better objective", color=GREEN, font_size=18)
        tight_label.next_to(right, DOWN, buff=0.16)

        question = latex(
            r"\text{How do we train the network to prefer the right structure?}",
            size=27,
            color=CYAN,
        )
        question.to_edge(DOWN, buff=0.50)
        fit_to_bounds(question, max_width=12.0)

        arrow = make_flow_arrow(left.get_right(), right.get_left(), color=YELLOW)
        next_label = VGroup(
            latex(r"\text{Next: Softmax Loss}", size=37, color=CYAN),
            latex(r"\text{classification first, geometry second}", size=23, color=WHITE),
        ).arrange(DOWN, buff=0.16)
        next_label.move_to(ORIGIN)
        layout = Group(title, left, right, loose, tight, loose_label, tight_label, question, arrow)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(left), LaggedStart(*[FadeIn(c) for c in loose], lag_ratio=0.10), FadeIn(loose_label), run_time=0.75)
        self.play(GrowArrow(arrow), run_time=0.35)
        self.play(FadeIn(right), LaggedStart(*[FadeIn(c) for c in tight], lag_ratio=0.10), FadeIn(tight_label), run_time=0.75)
        self.play(FadeIn(question), run_time=0.45)
        self.wait(0.7)
        clear_scene(self, run_time=0.65, wait_time=0.15)
        self.play(FadeIn(next_label), run_time=0.75)
        self.wait(1.0)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def fit_group_to_frame(self, group, center=ORIGIN):
        fit_to_bounds(group, max_width=self.SAFE_WIDTH, max_height=self.SAFE_HEIGHT)
        group.move_to(center)
        return group

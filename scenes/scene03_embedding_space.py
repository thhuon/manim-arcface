import os

from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 03 - Embedding Space
# Explains how face images become learned vectors and geometric points.
# =============================================================================


class Scene03_EmbeddingSpace(Scene):
    SAFE_WIDTH = 12.25
    SAFE_HEIGHT = 6.80

    def construct(self):
        self.camera.background_color = DARK

        card = make_centered_title_card("Embedding Space", "From faces to geometry")
        self.play(FadeIn(card), run_time=1.0)
        self.wait(0.9)
        self.play(FadeOut(card), run_time=0.5)

        self.beat_a_manual_grouping()
        self.clear_and_wait()
        self.beat_b_network_replaces_manual_sorting()
        self.clear_and_wait()
        self.beat_c_what_is_embedding()
        self.clear_and_wait()
        self.beat_d_distance_is_meaning()
        self.clear_and_wait()
        self.beat_e_before_training_random_space()
        self.clear_and_wait()
        self.beat_f_training_shapes_space()
        self.clear_and_wait()
        self.beat_g_new_face_compare_embeddings()
        self.clear_and_wait()
        self.beat_h_loss_transition()

    # -------------------------------------------------------------------------
    # Beat A - manual grouping analogy.
    # -------------------------------------------------------------------------
    def beat_a_manual_grouping(self):
        title = make_scene_title("How embedding space works?", "Manual grouping analogy", title_size=39, subtitle_size=20)

        people = self.get_person_image_groups()
        colors = [BLUE, GREEN, ORANGE, RED, CYAN, YELLOW, SHADOW, WHITE]
        for index, person_id in enumerate(people):
            people[person_id]["color"] = colors[index % len(colors)]

        mixed_order = []
        for person_id, spec in people.items():
            for filename in spec["files"]:
                mixed_order.append((person_id, filename))
        mixed_order.sort(key=lambda item: (item[0] * 17 + self.get_person_photo_index(item[1]) * 31) % 113)

        table_shadow = RoundedRectangle(
            width=12.35,
            height=5.10,
            corner_radius=0.12,
            stroke_color=MUTED,
            stroke_width=1.0,
            stroke_opacity=0.25,
            fill_color=PANEL,
            fill_opacity=0.10,
        ).move_to(DOWN * 0.12)

        def table_caption(text, color=WHITE, size=24):
            label = latex(rf"\text{{{tex_text(text)}}}", size=size, color=color)
            fit_to_bounds(label, max_width=11.75)
            label.next_to(table_shadow, DOWN, buff=0.10)
            return label

        def table_arrow_caption(left_text, right_text, color=WHITE, size=24):
            label = self.make_arrow_text(left_text, right_text, color=color, size=size)
            fit_to_bounds(label, max_width=11.75)
            label.next_to(table_shadow, DOWN, buff=0.10)
            return label

        caption = table_caption("Many photos are mixed together", color=YELLOW)

        cards = Group()
        card_people = []
        person_cards = {person_id: [] for person_id in people}
        cols = 12
        x_step = 10.85 / (cols - 1)
        y_step = 0.72
        scatter_positions = []
        angles = []
        for index in range(len(mixed_order)):
            row = index // cols
            col = index % cols
            x = -5.42 + col * x_step + 0.16 * np.sin(index * 1.73)
            y = 1.92 - row * y_step + 0.10 * np.cos(index * 2.11)
            scatter_positions.append(np.array([x, y, 0]))
            angles.append(((index * 37) % 17) - 8)

        for (person_id, filename), position, angle in zip(mixed_order, scatter_positions, angles):
            card = self.make_person_card(filename, color=MUTED, width=0.44, height=0.51)
            card.move_to(position)
            card.rotate(angle * DEGREES)
            cards.add(card)
            card_people.append(person_id)
            person_cards[person_id].append(card)

        cluster_centers = {}
        placement_order = sorted(people.keys(), key=lambda person_id: (person_id * 19) % 47)
        group_cols = 9
        for placement_index, person_id in enumerate(placement_order):
            row = placement_index // group_cols
            col = placement_index % group_cols
            x = -5.35 + col * 1.34 + 0.16 * np.sin(person_id * 1.61)
            y = 1.72 - row * 0.84 + 0.13 * np.cos(person_id * 2.17)
            cluster_centers[person_id] = np.array([x, y, 0])

        counters = {person_id: 0 for person_id in people}
        target_positions = []
        for person_id in card_people:
            index = counters[person_id]
            counters[person_id] += 1
            offsets = self.get_cluster_offsets(len(people[person_id]["files"]))
            target_positions.append(cluster_centers[person_id] + offsets[index])

        rings = VGroup()
        labels = VGroup()
        for person_id, center in cluster_centers.items():
            count = len(people[person_id]["files"])
            width, height = self.get_cluster_ring_size(count)
            ring = Ellipse(
                width=width,
                height=height,
                stroke_color=people[person_id]["color"],
                stroke_width=1.5 if count == 1 else 1.8,
                fill_opacity=0,
            ).move_to(center)
            rings.add(ring)

        for person_id, label_text in [(1, "Person A"), (2, "Person B")]:
            if person_id in cluster_centers:
                label = latex(rf"\text{{{label_text}}}", size=14, color=people[person_id]["color"])
                label.next_to(rings[placement_order.index(person_id)], DOWN, buff=0.05)
                labels.add(label)

        question_marks = VGroup(
            latex(r"\textbf{?}", size=21, color=YELLOW).next_to(person_cards[1][0], UP, buff=0.02),
            latex(r"\textbf{?}", size=20, color=YELLOW).next_to(person_cards[1][1], RIGHT, buff=0.03),
            latex(r"\textbf{?}", size=20, color=YELLOW).next_to(person_cards[2][0], UP, buff=0.02),
        )
        cursor = self.make_pointer_cursor().scale(0.95)
        cursor.move_to(person_cards[1][0].get_center() + RIGHT * 0.24 + DOWN * 0.22)

        background_cards = self.make_background_photo_cloud()
        sad_face = self.make_sad_question_face().scale(1.18)
        sad_face.move_to(UP * 0.42)
        sad_question = latex(r"\textbf{?}", size=62, color=YELLOW)
        sad_question.move_to(sad_face.get_center() + RIGHT * 0.92 + UP * 0.82)
        growth_label = latex(r"\text{The number of photos keeps growing}", size=28, color=WHITE)
        fit_to_bounds(growth_label, max_width=8.50)
        growth_label.next_to(sad_face, DOWN, buff=0.30)

        network = make_neural_network().scale(1.35)
        network.move_to(RIGHT * 2.10 + UP * 0.35)
        network_label = VGroup(
            latex(r"\text{NN learns how to}", size=25, color=CYAN),
            latex(r"\text{sort automatically}", size=25, color=CYAN),
        ).arrange(DOWN, buff=0.10)
        network_label.next_to(network, RIGHT, buff=0.36)
        network_group = VGroup(network, network_label)
        fit_to_bounds(network_group, max_width=5.80)
        network_group.move_to(RIGHT * 2.85 + UP * 0.16)

        challenge_group = VGroup(sad_face, sad_question, growth_label)
        challenge_group.move_to(ORIGIN + UP * 0.08)
        challenge_target = challenge_group.copy().move_to(LEFT * 3.35 + UP * 0.08)
        arrow_start = np.array([
            challenge_target[0].get_right()[0] + 0.25,
            challenge_target[0].get_center()[1],
            0,
        ])
        arrow_end = np.array([
            network.get_left()[0] - 0.15,
            arrow_start[1],
            0,
        ])
        nn_arrow = make_flow_arrow(
            arrow_start,
            arrow_end,
            color=YELLOW,
        )

        merged_positions = []
        merged_cols = 11
        for index in range(len(cards)):
            row = index // merged_cols
            col = index % merged_cols
            x = -5.60 + col * 1.12 + 0.12 * np.sin(index * 1.91)
            y = 2.45 - row * 0.86 + 0.10 * np.cos(index * 2.37)
            merged_positions.append(np.array([x, y, 0]))

        self.play(FadeIn(title), run_time=0.42)
        self.play(FadeIn(table_shadow), LaggedStart(*[FadeIn(card, scale=1.05) for card in cards], lag_ratio=0.025), run_time=1.00)
        self.play(FadeIn(caption), run_time=0.35)
        self.wait(0.15)

        self.play(Transform(caption, table_caption("Find identities that match", color=CYAN)), run_time=0.35)
        highlight_cards = person_cards[1][:3]
        self.play(
            LaggedStart(*[
                card[1].animate.set_stroke(people[1]["color"], width=3.0, opacity=1.0)
                for card in highlight_cards
            ], lag_ratio=0.06),
            FadeIn(question_marks),
            run_time=0.65,
        )
        self.wait(0.25)

        self.play(Transform(caption, table_caption("Group by similarity", color=GREEN)), run_time=0.35)
        move_anims = []
        for card, target, person_id, angle in zip(cards, target_positions, card_people, angles):
            move_anims.append(
                card.animate.set_width(0.39).move_to(target).rotate(-angle * DEGREES)
            )
        color_anims = [
            card[1].animate.set_stroke(people[person_id]["color"], width=1.5, opacity=0.95)
            for card, person_id in zip(cards, card_people)
        ]
        self.play(LaggedStart(*color_anims, lag_ratio=0.026), run_time=0.35)
        self.play(
            FadeOut(question_marks),
            LaggedStart(*move_anims, lag_ratio=0.026),
            run_time=1.55,
            rate_func=smooth,
        )

        first_ring = rings[placement_order.index(1)]
        rest_rings = VGroup(*[ring for index, ring in enumerate(rings) if index != placement_order.index(1)])
        self.play(Transform(caption, table_arrow_caption("Same person", "close together", color=GREEN)), run_time=0.35)
        self.play(ShowCreation(first_ring), run_time=0.45)
        self.play(first_ring.animate.scale(1.06), run_time=0.15)
        self.play(first_ring.animate.scale(1 / 1.06), run_time=0.15)

        self.play(Transform(caption, table_arrow_caption("Different people", "separated", color=YELLOW)), run_time=0.35)
        self.play(LaggedStart(*[ShowCreation(ring) for ring in rest_rings], lag_ratio=0.015), run_time=0.75)

        self.play(Transform(caption, table_caption("Each cluster = one identity", color=WHITE)), run_time=0.35)
        self.play(FadeIn(labels), run_time=0.45)
        self.wait(0.25)

        self.play(FadeIn(cursor), run_time=0.25)
        self.play(cursor.animate.move_to(cluster_centers[1] + RIGHT * 0.34 + DOWN * 0.22), run_time=0.45)
        self.play(cursor.animate.shift(LEFT * 0.24 + UP * 0.16), run_time=0.45)
        self.wait(0.15)

        scatter_back_anims = [
            card.animate.set_width(0.52).move_to(target).set_opacity(0.18)
            for card, target in zip(cards, merged_positions)
        ]
        frame_fade_anims = [
            card[1].animate.set_stroke(MUTED, width=0.6, opacity=0.12)
            for card in cards
        ]
        self.play(
            FadeOut(caption),
            FadeIn(background_cards),
            FadeOut(table_shadow),
            FadeOut(rings),
            FadeOut(labels),
            FadeOut(cursor),
            LaggedStart(*scatter_back_anims, lag_ratio=0.004),
            LaggedStart(*frame_fade_anims, lag_ratio=0.004),
            run_time=0.85,
            rate_func=smooth,
        )
        self.wait(0.30)
        self.play(FadeIn(sad_face), FadeIn(sad_question), run_time=0.45)
        self.play(FadeIn(growth_label), run_time=0.40)
        self.play(
            sad_face.animate.move_to(challenge_target[0]),
            sad_question.animate.move_to(challenge_target[1]),
            growth_label.animate.move_to(challenge_target[2]),
            run_time=0.70,
            rate_func=smooth,
        )
        self.play(GrowArrow(nn_arrow), FadeIn(network_group), run_time=0.75)
        self.wait(0.75)

    # -------------------------------------------------------------------------
    # Beat B - neural network replaces manual sorting.
    # -------------------------------------------------------------------------
    def beat_b_network_replaces_manual_sorting(self):
        title = make_scene_title("Neural network replaces manual sorting", title_size=38)
        caption = self.make_focus_caption("NN learns features", color=YELLOW)

        input_face = make_image_card("face_normal.png", width=2.28, height=2.66, stroke_color=CYAN, show_frame=False)
        input_face.move_to(LEFT * 4.80 + UP * 0.12)
        face_label = make_badge("Face image", color=CYAN, font_size=18)

        net = make_neural_network().scale(1.35)
        net.move_to(ORIGIN + UP * 0.12)
        net_label = make_badge("NN", color=ORANGE, font_size=18)

        vector = make_vector([r"0.28", r"-0.61", r"0.74", r"\vdots", r"0.19"], font_size=21)
        vector.move_to(RIGHT * 4.80 + UP * 0.12)
        vector_label = make_badge("Embedding vector", color=GREEN, font_size=18)
        dim_note = latex(r"\text{hundreds of dimensions}", size=22, color=YELLOW)
        dim_note.next_to(vector, RIGHT, buff=0.30)

        label_y = -1.95
        face_label.move_to(np.array([input_face.get_center()[0], label_y, 0]))
        net_label.move_to(np.array([net.get_center()[0], label_y, 0]))
        vector_label.move_to(np.array([vector.get_center()[0], label_y, 0]))

        arrow_y = input_face.get_center()[1]
        left_arrow_start = np.array([input_face.get_right()[0] + 0.16, arrow_y, 0])
        left_arrow_end = np.array([left_arrow_start[0] + 1.18, arrow_y, 0])
        right_arrow_end = np.array([vector.get_left()[0] - 0.16, arrow_y, 0])
        right_arrow_start = np.array([right_arrow_end[0] - 1.18, arrow_y, 0])
        arrows = VGroup(
            make_flow_arrow(left_arrow_start, left_arrow_end, color=CYAN),
            make_flow_arrow(right_arrow_start, right_arrow_end, color=ORANGE),
        )

        scan_line = Line(
            input_face.get_left() + RIGHT * 0.10 + UP * (input_face.get_height() / 2 - 0.16),
            input_face.get_right() + LEFT * 0.10 + UP * (input_face.get_height() / 2 - 0.16),
            color=CYAN,
            stroke_width=3.0,
            stroke_opacity=0.85,
        )
        scan_box = RoundedRectangle(
            width=input_face.get_width() + 0.20,
            height=input_face.get_height() + 0.20,
            corner_radius=0.08,
            stroke_color=CYAN,
            stroke_width=1.8,
            fill_opacity=0,
        ).move_to(input_face)

        particles = VGroup(*[
            Dot(point=left_arrow_start, color=CYAN if i < 4 else YELLOW, radius=0.045)
            for i in range(9)
        ])
        net_path = Line(left_arrow_start, right_arrow_start)
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

        layout = Group(title, caption, input_face, face_label, net, net_label, vector, vector_label, dim_note, arrows, scan_box, scan_line)
        self.fit_group_to_frame(layout)
        caption.next_to(Group(input_face, net, vector), DOWN, buff=0.62)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(input_face), run_time=0.40)
        self.play(FadeIn(face_label), run_time=0.30)
        self.play(ShowCreation(scan_box), FadeIn(scan_line), run_time=0.25)
        self.play(scan_line.animate.move_to(input_face.get_bottom() + UP * 0.16), run_time=0.75, rate_func=linear)
        self.play(FadeOut(scan_line), FadeOut(scan_box), run_time=0.20)
        self.play(GrowArrow(arrows[0]), FadeIn(net), run_time=0.55)
        self.play(FadeIn(net_label), FadeIn(caption), run_time=0.30)
        self.add(particles)
        self.play(
            LaggedStart(*[MoveAlongPath(particle, net_path) for particle in particles], lag_ratio=0.045),
            LaggedStart(*[ShowPassingFlash(box, time_width=0.85) for box in layer_highlights], lag_ratio=0.13),
            run_time=1.20,
        )
        self.play(FadeOut(particles), run_time=0.15)
        self.play(GrowArrow(arrows[1]), FadeIn(vector), run_time=0.55)
        self.play(FadeIn(vector_label), run_time=0.30)
        self.play(FadeIn(dim_note, scale=1.08), run_time=0.35)
        self.play(FlashAround(dim_note, color=YELLOW, run_time=0.55), run_time=0.55)
        self.wait(0.75)

    # -------------------------------------------------------------------------
    # Beat C - what is an embedding?
    # -------------------------------------------------------------------------
    def beat_c_what_is_embedding(self):
        title = make_scene_title("What is an embedding?", "A learned numeric representation", title_size=39, subtitle_size=20)
        caption = self.make_focus_caption("A face becomes a vector of numbers", color=GREEN)

        face = make_image_card("person1_1.png", width=1.95, height=2.25, stroke_color=CYAN, show_frame=False)
        face.move_to(LEFT * 4.55 + UP * 0.55)
        vector = make_vector([r"0.28", r"-0.61", r"0.74", r"\vdots", r"0.19"], font_size=22)
        vector.move_to(LEFT * 1.38 + UP * 0.55)
        vector_label = make_badge("Embedding Vector", color=GREEN, font_size=18)
        vector_label.next_to(vector, DOWN, buff=0.16)
        combination = latex(r"\text{combination}", size=22, color=YELLOW)
        combination.next_to(vector, UP, buff=0.18)

        eye_l = Circle(radius=0.13, stroke_color=YELLOW, stroke_width=2.0, fill_opacity=0)
        eye_l.move_to(face.get_center() + LEFT * 0.34 + UP * 0.38)
        eye_r = Circle(radius=0.13, stroke_color=YELLOW, stroke_width=2.0, fill_opacity=0)
        eye_r.move_to(face.get_center() + RIGHT * 0.28 + UP * 0.38)
        nose = Circle(radius=0.12, stroke_color=ORANGE, stroke_width=2.0, fill_opacity=0)
        nose.move_to(face.get_center() + UP * 0.02)
        mouth = Ellipse(width=0.48, height=0.20, stroke_color=GREEN, stroke_width=2.0, fill_opacity=0)
        mouth.move_to(face.get_center() + DOWN * 0.44)
        eye_label = make_badge("eyes", color=YELLOW, font_size=15)
        eye_label.next_to(face, UP, buff=0.10)
        nose_label = make_badge("nose", color=ORANGE, font_size=15)
        nose_label.next_to(face, RIGHT, buff=0.08)
        mouth_label = make_badge("mouth", color=GREEN, font_size=15)
        mouth_label.next_to(face, DOWN, buff=0.10)
        feature_marks = VGroup(eye_l, eye_r, nose, mouth)
        feature_labels = VGroup(eye_label, nose_label, mouth_label)

        feature_arrows = VGroup(
            make_flow_arrow(eye_label.get_right(), vector.get_left() + UP * 0.42, color=YELLOW, stroke_width=1.8),
            make_flow_arrow(nose_label.get_right(), vector.get_left(), color=ORANGE, stroke_width=1.8),
            make_flow_arrow(mouth_label.get_right(), vector.get_left() + DOWN * 0.42, color=GREEN, stroke_width=1.8),
        )

        plane = make_panel(width=4.50, height=3.35, stroke_color=GREEN, fill_opacity=0.06)
        plane.move_to(RIGHT * 3.25 + UP * 0.08)
        axes = VGroup(
            Line(plane.get_left() + RIGHT * 0.28, plane.get_right() + LEFT * 0.28, color=MUTED, stroke_width=1.0),
            Line(plane.get_bottom() + UP * 0.24, plane.get_top() + DOWN * 0.24, color=MUTED, stroke_width=1.0),
        )
        dot = Dot(point=plane.get_center() + RIGHT * 0.42 + UP * 0.35, color=YELLOW, radius=0.12)
        dot_label = latex(r"\text{one point}", size=17, color=YELLOW)
        dot_label.next_to(dot, RIGHT, buff=0.10)
        arrow_vector_space = make_flow_arrow(vector.get_right(), dot.get_center() + LEFT * 0.12, color=GREEN)
        other_points = VGroup(*[
            Dot(point=plane.get_center() + offset, color=color, radius=0.065)
            for offset, color in zip(
                [
                    LEFT * 1.45 + UP * 0.92,
                    LEFT * 0.90 + DOWN * 0.75,
                    RIGHT * 1.25 + UP * 0.72,
                    RIGHT * 1.55 + DOWN * 0.48,
                    LEFT * 1.58 + DOWN * 0.05,
                    RIGHT * 0.18 + UP * 1.05,
                    RIGHT * 0.56 + DOWN * 1.05,
                    LEFT * 0.18 + UP * 0.18,
                    RIGHT * 1.00 + UP * 0.02,
                    LEFT * 0.62 + DOWN * 1.10,
                ],
                [BLUE, GREEN, ORANGE, RED, CYAN, YELLOW, BLUE, GREEN, ORANGE, RED],
            )
        ])
        space_label = make_badge("embedding space", color=GREEN, font_size=18)
        space_label.next_to(plane, DOWN, buff=0.13)

        name_label = make_badge("Name: John", color=MUTED, font_size=20)
        name_label.move_to(LEFT * 3.70 + DOWN * 1.70)
        id_label = make_badge("ID #1042", color=MUTED, font_size=20)
        id_label.move_to(LEFT * 1.20 + DOWN * 1.70)

        no_parts = latex(r"\text{No single dimension means eyes, nose, or mouth.}", size=22, color=YELLOW)
        no_parts.next_to(caption, UP, buff=0.14)
        fit_to_bounds(no_parts, max_width=10.80)

        layout = Group(
            title, caption, face, vector, vector_label, combination,
            feature_marks, feature_labels, feature_arrows,
            plane, axes, dot, dot_label, arrow_vector_space,
            other_points, space_label, name_label, id_label, no_parts,
        )
        self.fit_group_to_frame(layout)
        name_cross = self.make_cross(name_label)
        id_cross = self.make_cross(id_label)
        vector_box = self.make_highlight_box(VGroup(vector, vector_label), color=GREEN)
        space_box = self.make_highlight_box(VGroup(plane, space_label), color=GREEN)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(face), run_time=0.45)
        self.play(ShowCreation(feature_marks), FadeIn(feature_labels), run_time=0.55)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in feature_arrows], lag_ratio=0.10), FadeIn(vector), run_time=0.75)
        self.play(FadeIn(combination, scale=1.08), FadeIn(caption), FadeIn(vector_label), run_time=0.35)
        self.play(FadeIn(no_parts), run_time=0.45)
        self.wait(0.35)
        self.play(FadeOut(no_parts), run_time=0.25)
        self.play(FadeIn(plane), ShowCreation(axes), GrowArrow(arrow_vector_space), Transform(vector.copy(), dot), run_time=0.85)
        self.add(dot)
        self.play(Transform(caption, self.make_focus_arrow_caption("One vector", "one point", color=GREEN)), FadeIn(dot_label), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(point, scale=1.25) for point in other_points], lag_ratio=0.05), run_time=0.65)
        self.play(FadeIn(space_label), run_time=0.35)

        self.play(FadeIn(name_label), ShowCreation(name_cross), run_time=0.45)
        self.play(Transform(caption, self.make_focus_caption("Not a name", color=RED)), run_time=0.25)
        self.play(FadeIn(id_label), ShowCreation(id_cross), run_time=0.45)
        self.play(Transform(caption, self.make_focus_caption("Not a hand-written ID", color=RED)), run_time=0.25)
        self.play(FadeIn(vector_box), FadeIn(space_box), run_time=0.40)
        self.play(Transform(caption, self.make_focus_caption("A learned representation", color=GREEN)), run_time=0.30)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat D - distance is the meaning.
    # -------------------------------------------------------------------------
    def beat_d_distance_is_meaning(self):
        title = make_scene_title("Distance is the meaning", title_size=39)

        plane = make_panel(width=9.00, height=4.95, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(UP * 0.10)
        axes = VGroup(
            Line(plane.get_left() + RIGHT * 0.35, plane.get_right() + LEFT * 0.35, color=MUTED, stroke_width=1.0),
            Line(plane.get_bottom() + UP * 0.30, plane.get_top() + DOWN * 0.30, color=MUTED, stroke_width=1.0),
        )
        plane_label = latex(r"\text{embedding space}", size=19, color=MUTED)
        plane_label.move_to(plane.get_corner(UL) + RIGHT * 1.20 + DOWN * 0.30)

        a1 = Dot(point=plane.get_center() + LEFT * 2.30 + UP * 0.72, color=BLUE, radius=0.11)
        a2 = Dot(point=plane.get_center() + LEFT * 1.88 + UP * 0.95, color=BLUE, radius=0.11)
        q = Dot(point=plane.get_center() + LEFT * 2.10 + UP * 0.38, color=YELLOW, radius=0.11)
        b1 = Dot(point=plane.get_center() + RIGHT * 2.25 + DOWN * 0.48, color=GREEN, radius=0.11)
        b2 = Dot(point=plane.get_center() + RIGHT * 2.62 + DOWN * 0.17, color=GREEN, radius=0.11)

        cluster_a = Ellipse(width=1.22, height=1.00, stroke_color=BLUE, stroke_width=1.8, fill_opacity=0).move_to(VGroup(a1, a2, q))
        cluster_b = Ellipse(width=1.18, height=0.92, stroke_color=GREEN, stroke_width=1.8, fill_opacity=0).move_to(VGroup(b1, b2))
        near = make_double_arrow(a1.get_center(), q.get_center(), color=GREEN, stroke_width=1.9)
        far = make_double_arrow(q.get_center(), b1.get_center(), color=RED, stroke_width=1.6)
        near_label = make_badge("small distance", color=GREEN, font_size=18)
        near_label.next_to(near, LEFT, buff=0.12)
        far_label = make_badge("large distance", color=RED, font_size=18)
        far_label.next_to(far, DOWN, buff=0.14)
        same_identity = make_badge("same identity", color=GREEN, font_size=19)
        same_identity.move_to(plane.get_center() + LEFT * 0.35 + UP * 1.48)
        same_arrow = make_flow_arrow(cluster_a.get_right(), same_identity.get_left(), color=GREEN, stroke_width=1.8)
        different_identity = make_badge("different identity", color=RED, font_size=19)
        different_identity.move_to(plane.get_center() + RIGHT * 0.38 + DOWN * 1.72)
        different_arrow = make_flow_arrow(far_label.get_bottom(), different_identity.get_top(), color=RED, stroke_width=1.8)
        identity_note = latex(r"\text{Distance compares identity, not absolute coordinates.}", size=24, color=CYAN)
        identity_note.next_to(plane, DOWN, buff=0.18)
        fit_to_bounds(identity_note, max_width=10.80)

        layout = Group(
            title, plane, plane_label, axes, a1, a2, q, b1, b2,
            cluster_a, cluster_b, near, far, near_label, far_label,
            same_identity, same_arrow, different_identity, different_arrow,
            identity_note,
        )
        self.fit_group_to_frame(layout)
        identity_note.next_to(plane, DOWN, buff=0.18)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(plane), FadeIn(plane_label), ShowCreation(axes), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(dot, scale=1.2) for dot in [a1, a2, q, b1, b2]], lag_ratio=0.05), run_time=0.65)
        self.play(ShowCreation(cluster_a), ShowCreation(near), FadeIn(near_label), run_time=0.55)
        self.play(GrowArrow(same_arrow), FadeIn(same_identity), run_time=0.45)
        self.play(ShowCreation(cluster_b), ShowCreation(far), FadeIn(far_label), run_time=0.65)
        self.play(GrowArrow(different_arrow), FadeIn(different_identity), run_time=0.45)
        self.play(FadeIn(identity_note), run_time=0.45)
        self.wait(0.8)

    # -------------------------------------------------------------------------
    # Beat E - before training: random space.
    # -------------------------------------------------------------------------
    def beat_e_before_training_random_space(self):
        title = make_scene_title("Before training: random space", title_size=39)

        plane = make_panel(width=9.70, height=5.15, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(UP * 0.10)
        plane_label = latex(r"\text{embedding space}", size=19, color=MUTED)
        plane_label.move_to(plane.get_corner(UL) + RIGHT * 1.20 + DOWN * 0.30)
        positions = [
            LEFT * 3.70 + DOWN * 1.58,
            LEFT * 2.90 + UP * 1.48,
            LEFT * 1.82 + DOWN * 0.62,
            LEFT * 0.55 + UP * 1.28,
            RIGHT * 0.22 + DOWN * 1.35,
            RIGHT * 1.14 + UP * 1.56,
            RIGHT * 2.02 + DOWN * 0.38,
            RIGHT * 3.10 + UP * 1.02,
            RIGHT * 3.56 + DOWN * 1.48,
            LEFT * 3.20 + UP * 0.20,
            RIGHT * 0.92 + UP * 0.10,
            LEFT * 0.92 + DOWN * 1.72,
        ]
        colors = [BLUE, GREEN, ORANGE, RED, CYAN, YELLOW, SHADOW, BLUE, GREEN, ORANGE, RED, CYAN]
        dots = VGroup(*[
            Dot(point=plane.get_center() + position, color=color, radius=0.10)
            for position, color in zip(positions, colors)
        ])
        caption = self.make_near_frame_caption(plane, "The space is not hand-defined", color=YELLOW, size=25)
        mixed_label = self.make_near_frame_caption(plane, "Same identities are still mixed.", color=RED, size=24)
        distance_line = make_double_arrow(dots[1].get_center(), dots[8].get_center(), color=YELLOW, stroke_width=1.7)
        distance_label = make_badge("distance?", color=YELLOW, font_size=18)
        distance_label.next_to(distance_line, UP, buff=0.12)
        unsure_face = self.make_sad_question_face().scale(0.62)
        unsure_face.next_to(plane, DOWN, buff=0.36)
        unsure_text = latex(r"\text{same identity?}", size=24, color=YELLOW)
        unsure_text.next_to(unsure_face, RIGHT, buff=0.22)
        unsure_question = latex(r"\textbf{?}", size=36, color=YELLOW)
        unsure_question.next_to(unsure_face, UP + RIGHT, buff=0.03)
        unsure_group = VGroup(unsure_face, unsure_text, unsure_question)
        manual_rule = make_badge("manual map of identities", color=MUTED, font_size=20)
        manual_rule.move_to(plane.get_center() + RIGHT * 2.25 + DOWN * 1.82)

        layout = Group(
            title, caption, mixed_label, plane, plane_label, dots,
            distance_line, distance_label, unsure_group, manual_rule,
        )
        self.fit_group_to_frame(layout)
        caption.next_to(plane, DOWN, buff=0.18)
        mixed_label.next_to(plane, DOWN, buff=0.18)
        unsure_group.next_to(plane, DOWN, buff=0.42)
        manual_cross = self.make_cross(manual_rule)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(plane), FadeIn(plane_label), LaggedStart(*[FadeIn(dot, scale=1.25) for dot in dots], lag_ratio=0.035), run_time=0.80)
        self.play(FadeIn(caption), run_time=0.35)
        self.play(ShowCreation(distance_line), FadeIn(distance_label), run_time=0.55)
        self.play(Transform(caption, mixed_label), run_time=0.40)
        self.play(FadeIn(unsure_group), run_time=0.45)
        self.play(FadeIn(manual_rule), ShowCreation(manual_cross), run_time=0.55)
        self.wait(0.85)

    # -------------------------------------------------------------------------
    # Beat F - training shapes the space.
    # -------------------------------------------------------------------------
    def beat_f_training_shapes_space(self):
        title = make_scene_title("Training shapes the space", "Useful geometry is learned", title_size=39, subtitle_size=20)
        caption = self.make_focus_caption("Training moves embeddings", color=CYAN)

        plane = make_panel(width=9.70, height=5.15, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(DOWN * 0.02)
        colors = [BLUE, GREEN, ORANGE, BLUE, ORANGE, GREEN, BLUE, ORANGE, GREEN, RED, RED, RED]
        start_offsets = [
            LEFT * 3.70 + DOWN * 1.58,
            LEFT * 2.90 + UP * 1.48,
            LEFT * 1.82 + DOWN * 0.62,
            LEFT * 0.55 + UP * 1.28,
            RIGHT * 0.22 + DOWN * 1.35,
            RIGHT * 1.14 + UP * 1.56,
            RIGHT * 2.02 + DOWN * 0.38,
            RIGHT * 3.10 + UP * 1.02,
            RIGHT * 3.56 + DOWN * 1.48,
            LEFT * 3.20 + UP * 0.20,
            RIGHT * 0.92 + UP * 0.10,
            LEFT * 0.92 + DOWN * 1.72,
        ]
        cluster_centers = [
            plane.get_center() + LEFT * 3.00 + UP * 1.05,
            plane.get_center() + RIGHT * 2.80 + UP * 1.02,
            plane.get_center() + LEFT * 2.60 + DOWN * 1.35,
            plane.get_center() + RIGHT * 2.60 + DOWN * 1.35,
        ]
        final_offsets = [
            LEFT * 0.18 + UP * 0.12,
            RIGHT * 0.22 + UP * 0.04,
            DOWN * 0.20,
            RIGHT * 0.08 + DOWN * 0.16,
        ]
        color_to_cluster = {BLUE: 0, GREEN: 1, ORANGE: 2, RED: 3}
        counters = {BLUE: 0, GREEN: 0, ORANGE: 0, RED: 0}
        dots = VGroup()
        final_points = []
        for color, start in zip(colors, start_offsets):
            dots.add(Dot(point=plane.get_center() + start, color=color, radius=0.095))
            cluster_index = color_to_cluster[color]
            offset = final_offsets[counters[color] % len(final_offsets)]
            counters[color] += 1
            final_points.append(cluster_centers[cluster_index] + offset)

        arrows = VGroup(*[
            Arrow(dot.get_center(), target, buff=0.08, color=dot.get_color(), stroke_width=1.1,
                  stroke_opacity=0.55, max_tip_length_to_length_ratio=0.16)
            for dot, target in zip(dots, final_points)
        ])
        rings = VGroup(*[
            Ellipse(width=1.20, height=0.95, stroke_color=color, stroke_width=1.8, fill_opacity=0).move_to(center)
            for color, center in zip([BLUE, GREEN, ORANGE, RED], cluster_centers)
        ])
        step_labels = VGroup(
            make_badge("prediction", color=CYAN, font_size=18),
            make_badge("loss signal", color=YELLOW, font_size=18),
            make_badge("backprop update", color=GREEN, font_size=18),
        ).arrange(RIGHT, buff=0.35)
        step_labels.next_to(caption, UP, buff=0.12)

        compact = latex(r"\text{same identity: compact}", size=23, color=GREEN)
        separated = latex(r"\text{different identities: separated}", size=23, color=YELLOW)
        quality_notes = VGroup(compact, separated).arrange(RIGHT, buff=0.45)
        quality_notes.next_to(step_labels, UP, buff=0.14)

        layout = Group(title, caption, plane, dots, arrows, rings, step_labels, quality_notes)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(plane), LaggedStart(*[FadeIn(dot, scale=1.2) for dot in dots], lag_ratio=0.035), run_time=0.75)
        self.play(FadeIn(caption), run_time=0.30)
        self.play(FadeIn(step_labels[0]), run_time=0.28)
        self.play(FadeIn(step_labels[1]), LaggedStart(*[GrowArrow(arrow) for arrow in arrows], lag_ratio=0.018), run_time=0.70)
        self.play(
            FadeIn(step_labels[2]),
            LaggedStart(*[dot.animate.move_to(target) for dot, target in zip(dots, final_points)], lag_ratio=0.035),
            run_time=1.35,
            rate_func=smooth,
        )
        self.play(FadeOut(arrows), LaggedStart(*[ShowCreation(ring) for ring in rings], lag_ratio=0.07), run_time=0.55)
        self.play(Transform(caption, self.make_focus_caption("A good space has compact clusters and clear separation", color=GREEN)), FadeIn(quality_notes), run_time=0.55)
        self.wait(0.85)

    # -------------------------------------------------------------------------
    # Beat G - new face: compare embeddings.
    # -------------------------------------------------------------------------
    def beat_g_new_face_compare_embeddings(self):
        title = make_scene_title("New face: compare embeddings", title_size=39)
        caption = self.make_focus_arrow_caption("New face", "embedding", color=CYAN)

        query_face = make_image_card("person1_4.png", width=1.15, height=1.35, stroke_color=YELLOW, show_frame=False)
        query_face.move_to(LEFT * 5.10 + UP * 0.92)
        query_label = make_badge("new face", color=YELLOW, font_size=17)
        query_label.next_to(query_face, DOWN, buff=0.14)

        net = make_neural_network().scale(0.88)
        net.move_to(LEFT * 3.05 + UP * 0.90)
        vector = make_vector([r"0.31", r"-0.58", r"0.70", r"\vdots"], font_size=18)
        vector.move_to(LEFT * 1.30 + UP * 0.90)
        plane = make_panel(width=5.65, height=4.25, stroke_color=MUTED, fill_opacity=0.06)
        plane.move_to(RIGHT * 2.45 + DOWN * 0.10)

        cluster_a = make_embedding_cluster(plane.get_center() + LEFT * 1.35 + UP * 0.85, BLUE, radius=0.075, scale=0.80, count=5)
        cluster_b = make_embedding_cluster(plane.get_center() + RIGHT * 1.45 + UP * 0.52, GREEN, radius=0.075, scale=0.80, count=5)
        cluster_c = make_embedding_cluster(plane.get_center() + DOWN * 1.10 + RIGHT * 0.18, ORANGE, radius=0.075, scale=0.80, count=5)
        rings = VGroup(
            Ellipse(width=1.02, height=0.82, stroke_color=BLUE, stroke_width=1.6, fill_opacity=0).move_to(cluster_a),
            Ellipse(width=1.02, height=0.82, stroke_color=GREEN, stroke_width=1.6, fill_opacity=0).move_to(cluster_b),
            Ellipse(width=1.02, height=0.82, stroke_color=ORANGE, stroke_width=1.6, fill_opacity=0).move_to(cluster_c),
        )
        query_dot_start = vector.get_right() + RIGHT * 0.20
        query_dot = Dot(point=plane.get_center() + LEFT * 1.02 + UP * 0.54, color=YELLOW, radius=0.11)
        query_dot_label = latex(r"\text{query}", size=16, color=YELLOW)
        query_dot_label.next_to(query_dot, RIGHT, buff=0.08)
        near = make_double_arrow(query_dot.get_center(), cluster_a.get_center(), color=GREEN, stroke_width=1.7)
        far_b = Line(query_dot.get_center(), cluster_b.get_center(), color=RED, stroke_width=1.3, stroke_opacity=0.55)
        far_c = Line(query_dot.get_center(), cluster_c.get_center(), color=RED, stroke_width=1.3, stroke_opacity=0.45)
        nearest = self.make_arrow_text("nearest cluster", "likely same identity", color=GREEN, size=18)
        nearest.next_to(plane, DOWN, buff=0.16)

        arrows = VGroup(
            make_flow_arrow(query_face.get_right(), net.get_left(), color=CYAN),
            make_flow_arrow(net.get_right(), vector.get_left(), color=ORANGE),
            make_flow_arrow(vector.get_right(), plane.get_left() + RIGHT * 0.15 + UP * 0.85, color=GREEN),
        )
        packets = VGroup(*[
            Dot(point=query_face.get_right() + RIGHT * 0.04, color=CYAN, radius=0.04)
            for _ in range(6)
        ])
        net_path = Line(query_face.get_right() + RIGHT * 0.08, net.get_right() + RIGHT * 0.10)

        layout = Group(title, caption, query_face, query_label, net, vector, plane, cluster_a, cluster_b, cluster_c, rings, query_dot, query_dot_label, near, far_b, far_c, nearest, arrows)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(query_face), GrowArrow(arrows[0]), FadeIn(net), run_time=0.60)
        self.play(FadeIn(caption), FadeIn(query_label), run_time=0.30)
        self.add(packets)
        self.play(LaggedStart(*[MoveAlongPath(packet, net_path) for packet in packets], lag_ratio=0.05), run_time=0.80)
        self.play(FadeOut(packets), GrowArrow(arrows[1]), FadeIn(vector), run_time=0.50)
        self.play(FadeIn(plane), FadeIn(cluster_a), FadeIn(cluster_b), FadeIn(cluster_c), FadeIn(rings), run_time=0.65)
        self.play(GrowArrow(arrows[2]), Transform(Dot(point=query_dot_start, color=YELLOW, radius=0.11), query_dot), run_time=0.75)
        self.add(query_dot)
        self.play(FadeIn(query_dot_label), run_time=0.25)
        self.play(Transform(caption, self.make_focus_caption("Compare distances", color=YELLOW)), ShowCreation(near), ShowCreation(far_b), ShowCreation(far_c), run_time=0.70)
        self.play(Transform(caption, self.make_focus_arrow_caption("Nearest cluster", "likely same identity", color=GREEN)), FadeIn(nearest), run_time=0.50)
        self.wait(0.85)

    # -------------------------------------------------------------------------
    # Beat H - transition to loss functions.
    # -------------------------------------------------------------------------
    def beat_h_loss_transition(self):
        title = make_scene_title("What objective shapes the space?", "This leads to the loss function", title_size=38, subtitle_size=20)
        caption = self.make_focus_caption("A good geometry must be learned", color=CYAN)

        left = make_panel(width=4.55, height=3.65, stroke_color=RED, fill_opacity=0.06)
        left.move_to(LEFT * 2.95 + DOWN * 0.18)
        right = make_panel(width=4.55, height=3.65, stroke_color=GREEN, fill_opacity=0.06)
        right.move_to(RIGHT * 2.95 + DOWN * 0.18)

        loose = VGroup(
            make_embedding_cluster(left.get_center() + LEFT * 0.72 + UP * 0.50, BLUE, scale=1.55, count=5),
            make_embedding_cluster(left.get_center() + RIGHT * 0.78 + DOWN * 0.36, GREEN, scale=1.45, count=5),
            make_embedding_cluster(left.get_center() + RIGHT * 0.08 + UP * 0.06, ORANGE, scale=1.25, count=4),
        )
        tight = VGroup(
            make_embedding_cluster(right.get_center() + LEFT * 1.08 + UP * 0.72, BLUE, scale=0.75, count=5),
            make_embedding_cluster(right.get_center() + RIGHT * 1.10 + DOWN * 0.54, GREEN, scale=0.75, count=5),
            make_embedding_cluster(right.get_center() + RIGHT * 0.72 + UP * 0.82, ORANGE, scale=0.72, count=4),
        )
        loose_label = make_badge("weak geometry", color=RED, font_size=18)
        loose_label.next_to(left, DOWN, buff=0.16)
        tight_label = make_badge("compact + separated", color=GREEN, font_size=18)
        tight_label.next_to(right, DOWN, buff=0.16)
        arrow = make_flow_arrow(left.get_right(), right.get_left(), color=YELLOW)
        loss_label = make_badge("loss function", color=YELLOW, font_size=21)
        loss_label.next_to(arrow, UP, buff=0.12)

        question = latex(r"\text{How do we train the network to prefer the right structure?}", size=26, color=WHITE)
        question.next_to(caption, UP, buff=0.14)
        fit_to_bounds(question, max_width=11.7)

        layout = Group(title, caption, left, right, loose, tight, loose_label, tight_label, arrow, loss_label, question)
        self.fit_group_to_frame(layout)

        self.play(FadeIn(title), run_time=0.40)
        self.play(FadeIn(left), LaggedStart(*[FadeIn(cluster) for cluster in loose], lag_ratio=0.10), run_time=0.70)
        self.play(FadeIn(caption), FadeIn(loose_label), run_time=0.35)
        self.play(FadeIn(question), run_time=0.45)
        self.play(GrowArrow(arrow), FadeIn(loss_label), run_time=0.50)
        self.play(FadeIn(right), LaggedStart(*[FadeIn(cluster) for cluster in tight], lag_ratio=0.10), FadeIn(tight_label), run_time=0.75)
        self.play(Transform(caption, self.make_focus_caption("Need a loss function", color=YELLOW)), run_time=0.40)
        self.wait(0.65)
        clear_scene(self, run_time=0.65, wait_time=0.15)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def make_focus_caption(self, text, color=WHITE, size=27):
        caption = latex(rf"\text{{{tex_text(text)}}}", size=size, color=color)
        fit_to_bounds(caption, max_width=11.80)
        caption.to_edge(DOWN, buff=0.68)
        return caption

    def make_arrow_text(self, left_text, right_text, color=WHITE, size=27):
        left = latex(rf"\text{{{tex_text(left_text)}}}", size=size, color=color)
        right = latex(rf"\text{{{tex_text(right_text)}}}", size=size, color=color)
        arrow = Arrow(
            LEFT * 0.36,
            RIGHT * 0.36,
            buff=0.02,
            color=color,
            stroke_width=2.3,
            max_tip_length_to_length_ratio=0.22,
        )
        group = VGroup(left, arrow, right).arrange(RIGHT, buff=0.16)
        return group

    def make_focus_arrow_caption(self, left_text, right_text, color=WHITE, size=27):
        caption = self.make_arrow_text(left_text, right_text, color=color, size=size)
        fit_to_bounds(caption, max_width=11.80)
        caption.to_edge(DOWN, buff=0.68)
        return caption

    def make_near_frame_arrow_caption(self, frame, left_text, right_text, color=WHITE, size=25):
        caption = self.make_arrow_text(left_text, right_text, color=color, size=size)
        fit_to_bounds(caption, max_width=11.40)
        caption.next_to(frame, DOWN, buff=0.18)
        return caption

    def make_near_frame_caption(self, frame, text, color=WHITE, size=25):
        caption = latex(rf"\text{{{tex_text(text)}}}", size=size, color=color)
        fit_to_bounds(caption, max_width=11.40)
        caption.next_to(frame, DOWN, buff=0.18)
        return caption

    def get_person_image_groups(self):
        decorations_dir = os.path.dirname(asset_path("face_1.png"))
        filenames = [
            filename
            for filename in os.listdir(decorations_dir)
            if filename.startswith("person") and filename.endswith(".png")
        ]
        groups = {}
        for filename in filenames:
            person_id = self.get_person_id(filename)
            groups.setdefault(person_id, {"files": []})["files"].append(filename)
        for person_id in groups:
            groups[person_id]["files"].sort(key=self.get_person_photo_index)
        return dict(sorted(groups.items()))

    def get_person_id(self, filename):
        stem = filename[:-4]
        tail = stem[len("person"):]
        return int(tail.split("_", 1)[0])

    def get_person_photo_index(self, filename):
        stem = filename[:-4]
        tail = stem[len("person"):]
        if "_" not in tail:
            return 1
        return int(tail.split("_", 1)[1])

    def get_cluster_offsets(self, count):
        if count <= 1:
            return [ORIGIN]
        if count == 2:
            return [LEFT * 0.18, RIGHT * 0.18]
        if count == 3:
            return [LEFT * 0.22 + UP * 0.13, RIGHT * 0.22 + UP * 0.13, DOWN * 0.18]
        return [
            LEFT * 0.22 + UP * 0.17,
            RIGHT * 0.22 + UP * 0.17,
            LEFT * 0.22 + DOWN * 0.17,
            RIGHT * 0.22 + DOWN * 0.17,
        ][:count]

    def get_cluster_ring_size(self, count):
        if count <= 1:
            return 0.54, 0.50
        if count == 2:
            return 0.80, 0.54
        if count == 3:
            return 0.94, 0.76
        return 0.98, 0.86

    def make_person_card(self, filename, color=MUTED, width=0.95, height=1.10):
        return make_image_card(
            filename,
            width=width,
            height=height,
            stroke_color=color,
            show_frame=True,
        )

    def make_background_photo_cloud(self):
        decorations_dir = os.path.dirname(asset_path("face_1.png"))
        filenames = [
            filename
            for filename in os.listdir(decorations_dir)
            if filename.startswith("face_") and filename[5:-4].isdigit() and filename.endswith(".png")
        ]
        filenames.sort(key=lambda filename: int(filename[5:-4]))
        cloud = Group()
        cols = 12
        for index, filename in enumerate(filenames):
            row = index // cols
            col = index % cols
            x = -5.68 + col * 1.03 + 0.12 * np.sin(index * 1.33)
            y = 2.18 - row * 0.86 + 0.10 * np.cos(index * 2.41)
            angle = ((index * 29) % 19) - 9
            position = np.array([x, y, 0])
            card = make_image_card(filename, width=0.56, height=0.66, stroke_color=MUTED, show_frame=True)
            card.move_to(position)
            card.rotate(angle * DEGREES)
            card.set_opacity(0.16)
            cloud.add(card)
        return cloud

    def make_sad_question_face(self):
        face = Circle(
            radius=0.64,
            stroke_color=WHITE,
            stroke_width=2.2,
            fill_color=PANEL,
            fill_opacity=0.22,
        )
        eye_l = Dot(point=LEFT * 0.22 + UP * 0.16, radius=0.055, color=CYAN)
        eye_r = Dot(point=RIGHT * 0.22 + UP * 0.16, radius=0.055, color=CYAN)
        brow_l = Line(LEFT * 0.35 + UP * 0.36, LEFT * 0.13 + UP * 0.29, color=WHITE, stroke_width=1.7)
        brow_r = Line(RIGHT * 0.13 + UP * 0.29, RIGHT * 0.35 + UP * 0.36, color=WHITE, stroke_width=1.7)
        mouth = Arc(
            radius=0.24,
            start_angle=25 * DEGREES,
            angle=130 * DEGREES,
            stroke_color=WHITE,
            stroke_width=2.3,
        )
        mouth.move_to(DOWN * 0.28)
        return VGroup(face, eye_l, eye_r, brow_l, brow_r, mouth)

    def make_pointer_cursor(self):
        pointer = Polygon(
            ORIGIN,
            RIGHT * 0.52 + DOWN * 0.18,
            RIGHT * 0.25 + DOWN * 0.30,
            RIGHT * 0.42 + DOWN * 0.70,
            RIGHT * 0.28 + DOWN * 0.76,
            RIGHT * 0.10 + DOWN * 0.36,
            LEFT * 0.08 + DOWN * 0.58,
        )
        pointer.set_fill(WHITE, opacity=0.92)
        pointer.set_stroke(CYAN, width=1.3, opacity=1.0)
        return pointer

    def make_cross(self, mob, color=RED):
        width = mob.get_width() + 0.18
        height = mob.get_height() + 0.16
        return VGroup(
            Line(mob.get_center() + LEFT * width / 2 + UP * height / 2, mob.get_center() + RIGHT * width / 2 + DOWN * height / 2, color=color, stroke_width=3.0),
            Line(mob.get_center() + LEFT * width / 2 + DOWN * height / 2, mob.get_center() + RIGHT * width / 2 + UP * height / 2, color=color, stroke_width=3.0),
        )

    def make_highlight_box(self, mob, color=GREEN):
        return RoundedRectangle(
            width=mob.get_width() + 0.28,
            height=mob.get_height() + 0.28,
            corner_radius=0.08,
            stroke_color=color,
            stroke_width=2.0,
            fill_opacity=0,
        ).move_to(mob)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.35)

    def fit_group_to_frame(self, group, center=ORIGIN):
        fit_to_bounds(group, max_width=self.SAFE_WIDTH, max_height=self.SAFE_HEIGHT)
        group.move_to(center)
        return group

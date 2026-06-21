from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 04 - Softmax
# Narration-aligned rewrite:
# - Loss function as a measurable training objective
# - Softmax class comparison and probability distribution
# - Decision boundaries in embedding space
# - Softmax limitation for face recognition geometry
# - Transition to margin-based losses
# =============================================================================


PURPLE = "#A855F7"
SAFE_BOTTOM = -FRAME_HEIGHT / 2 + SUBTITLE_HEIGHT + FRAME_MARGIN
CONTENT_BOTTOM = SAFE_BOTTOM + 0.08
CONTENT_TOP = FRAME_HEIGHT / 2 - FRAME_MARGIN
TITLE_Y = 3.46


def text_mob(text, size=28, color=WHITE):
    return latex(rf"\text{{{tex_text(text)}}}", size=size, color=color)


def title_block(title, subtitle=None, title_size=44, subtitle_size=21):
    main = latex(rf"\textbf{{{tex_text(title)}}}", size=title_size, color=WHITE)
    if subtitle is None:
        main.move_to(UP * TITLE_Y)
        return main
    sub = text_mob(subtitle, size=subtitle_size, color=MUTED)
    group = VGroup(main, sub).arrange(DOWN, buff=0.10)
    group.move_to(UP * 3.42)
    return group


def concept_chip(label, color=CYAN, size=20):
    txt = text_mob(label, size=size, color=color)
    box = RoundedRectangle(
        width=txt.get_width() + 0.42,
        height=txt.get_height() + 0.20,
        corner_radius=0.10,
        stroke_color=color,
        stroke_width=1.5,
        fill_color=PANEL,
        fill_opacity=0.56,
    )
    txt.move_to(box)
    return VGroup(box, txt)


def arrow_text_row(left_text, right_text, color=CYAN, size=22):
    left = text_mob(left_text, size=size, color=WHITE)
    right = text_mob(right_text, size=size, color=WHITE)
    arrow = Arrow(
        LEFT * 0.36,
        RIGHT * 0.36,
        buff=0.04,
        color=color,
        stroke_width=2.0,
        max_tip_length_to_length_ratio=0.24,
    )
    return VGroup(left, arrow, right).arrange(RIGHT, buff=0.15)


def arrow_text_chain(labels, color=CYAN, size=20):
    group = VGroup()
    for index, label in enumerate(labels):
        group.add(text_mob(label, size=size, color=WHITE))
        if index < len(labels) - 1:
            group.add(Arrow(
                LEFT * 0.34,
                RIGHT * 0.34,
                buff=0.04,
                color=color,
                stroke_width=2.0,
                max_tip_length_to_length_ratio=0.24,
            ))
    return group.arrange(RIGHT, buff=0.14)


def callout_box(lines, color=CYAN, width=4.6, size=22):
    line_mobs = VGroup()
    for line in lines:
        if isinstance(line, tuple):
            line_mobs.add(arrow_text_row(line[0], line[1], color=color, size=size))
        else:
            line_mobs.add(text_mob(line, size=size, color=WHITE))
    line_mobs.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    fit_to_bounds(line_mobs, max_width=width - 0.40)
    box = RoundedRectangle(
        width=width,
        height=max(line_mobs.get_height() + 0.46, 0.86),
        corner_radius=0.10,
        stroke_color=color,
        stroke_width=1.5,
        fill_color=PANEL,
        fill_opacity=0.36,
    )
    line_mobs.move_to(box)
    return VGroup(box, line_mobs)


def safe_group(group, max_width=12.75, max_height=5.48, center=ORIGIN + UP * 0.44):
    fit_to_bounds(group, max_width=max_width, max_height=max_height)
    group.move_to(center)
    if group.get_top()[1] > CONTENT_TOP:
        group.shift(DOWN * (group.get_top()[1] - CONTENT_TOP))
    if group.get_bottom()[1] < CONTENT_BOTTOM:
        group.shift(UP * (CONTENT_BOTTOM - group.get_bottom()[1]))
    return group


def make_probability_panel(probs, labels, colors, title="Softmax probabilities", width=3.55):
    header = text_mob(title, size=22, color=WHITE)
    rows = VGroup()
    max_bar = width * 0.54
    for index, (prob, label, color) in enumerate(zip(probs, labels, colors)):
        row = VGroup()
        name = text_mob(label, size=18, color=color)
        name.set_width(min(name.get_width(), 0.78))
        bg = RoundedRectangle(
            width=max_bar,
            height=0.24,
            corner_radius=0.04,
            stroke_width=0.7,
            stroke_color=MUTED,
            fill_color=MUTED,
            fill_opacity=0.15,
        )
        bar = RoundedRectangle(
            width=max(0.04, max_bar * prob),
            height=0.24,
            corner_radius=0.04,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.76,
        )
        bar.move_to(bg.get_left() + RIGHT * (bar.get_width() / 2))
        pct = text_mob(f"{int(round(prob * 100)):>2d}%", size=18, color=WHITE)
        bar_stack = VGroup(bg, bar)
        row.add(name, bar_stack, pct)
        row.arrange(RIGHT, buff=0.15)
        rows.add(row)
    rows.arrange(DOWN, buff=0.20, aligned_edge=LEFT)
    rows.next_to(header, DOWN, buff=0.24)
    group = VGroup(header, rows)
    panel = RoundedRectangle(
        width=width,
        height=group.get_height() + 0.58,
        corner_radius=0.12,
        stroke_color=MUTED,
        stroke_width=1.1,
        fill_color=PANEL,
        fill_opacity=0.26,
    )
    group.move_to(panel)
    return VGroup(panel, group)


def make_loss_meter(value=0.78, width=3.15, label="loss"):
    value = np.clip(value, 0.02, 1.0)
    name = text_mob(label, size=20, color=WHITE)
    bg = RoundedRectangle(
        width=width,
        height=0.26,
        corner_radius=0.06,
        stroke_color=MUTED,
        stroke_width=1.0,
        fill_color=MUTED,
        fill_opacity=0.16,
    )
    color = RED if value > 0.58 else YELLOW if value > 0.34 else GREEN
    fill = RoundedRectangle(
        width=max(0.06, width * value),
        height=0.26,
        corner_radius=0.06,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.88,
    )
    fill.move_to(bg.get_left() + RIGHT * fill.get_width() / 2)
    value_label = text_mob(f"{value:.2f}", size=18, color=color)
    bar_stack = VGroup(bg, fill)
    group = VGroup(name, bar_stack, value_label).arrange(RIGHT, buff=0.14)
    return group


def make_score_table(scores, labels, colors):
    title = text_mob("class scores", size=21, color=WHITE)
    rows = VGroup()
    for score, label, color in zip(scores, labels, colors):
        name = text_mob(label, size=17, color=color)
        eq = Tex(r"W_j^T f", font_size=23, color=color)
        score_txt = text_mob(f"{score:+.2f}", size=17, color=WHITE)
        row = VGroup(name, eq, score_txt).arrange(RIGHT, buff=0.16)
        rows.add(row)
    rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    rows.next_to(title, DOWN, buff=0.22)
    group = VGroup(title, rows)
    panel = RoundedRectangle(
        width=3.10,
        height=group.get_height() + 0.50,
        corner_radius=0.10,
        stroke_color=MUTED,
        stroke_width=1.0,
        fill_color=PANEL,
        fill_opacity=0.24,
    )
    group.move_to(panel)
    return VGroup(panel, group)


def cluster_dots(center, color, count=7, spread=0.45, seed=1, radius=0.065):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        offset = rng.normal(0, spread, size=2)
        dots.add(Dot(point=center + np.array([offset[0], offset[1], 0]), color=color, radius=radius))
    return dots


def ring_around(mob, color, buff=0.32):
    ring = Ellipse(
        width=mob.get_width() + buff,
        height=mob.get_height() + buff * 0.78,
        stroke_color=color,
        stroke_width=1.7,
        fill_opacity=0,
    )
    ring.move_to(mob)
    return ring


class Scene04_Softmax(Scene):
    def construct(self):
        self.camera.background_color = DARK

        card = make_centered_title_card("Softmax Loss", "Why classification is not enough")
        self.add(card)
        self.wait(0.7)
        self.play(FadeOut(card), run_time=0.45)

        self.beat_a_loss_function_intro()
        self.clear_and_wait()
        self.beat_b_softmax_basic_concept()
        self.clear_and_wait()
        self.beat_c_decision_boundaries()
        self.clear_and_wait()
        self.beat_d_softmax_limitations()
        self.clear_and_wait()
        self.beat_e_need_better_objectives()

    # ------------------------------------------------------------------
    # Beat A - Loss function introduction.
    # ------------------------------------------------------------------
    def beat_a_loss_function_intro(self):
        title = make_scene_title(
            "Loss Function",
            "A measurable objective for learning geometry",
            title_size=39,
            subtitle_size=20,
        )

        face = make_image_card("person1_1.png", width=1.26, height=1.48, stroke_color=CYAN)
        face_label = text_mob("face image", size=18, color=CYAN).next_to(face, DOWN, buff=0.07)
        face_group = Group(face, face_label)

        net = make_neural_network().scale(1.02)
        net_label = text_mob("neural network", size=19, color=WHITE).next_to(net, DOWN, buff=0.10)
        net_group = VGroup(net, net_label)

        emb_vec = make_vector(["0.21", "-0.64", "0.38", "..."], font_size=20)
        emb_vec.set_color(WHITE)
        emb_label = text_mob("embedding", size=19, color=GREEN).next_to(emb_vec, DOWN, buff=0.10)
        emb_group = VGroup(emb_vec, emb_label)

        probs_hi = make_probability_panel(
            [0.28, 0.52, 0.20],
            ["A", "B", "C"],
            [CYAN, GREEN, ORANGE],
            title="prediction",
            width=3.30,
        )
        target = concept_chip("target: Person A", color=YELLOW, size=18)
        loss_hi = make_loss_meter(0.78, width=3.35, label="loss")

        pipe = Group(face_group, net_group, emb_group, probs_hi)
        pipe.arrange(RIGHT, buff=0.98)
        arrows = VGroup(
            make_flow_arrow(face_group.get_right(), net_group.get_left(), color=CYAN),
            make_flow_arrow(net_group.get_right(), emb_group.get_left(), color=GREEN),
            make_flow_arrow(emb_group.get_right(), probs_hi.get_left(), color=YELLOW),
        )
        pipeline = Group(pipe, arrows)
        pipeline.move_to(UP * 1.54)

        target.next_to(probs_hi, UP, buff=0.14)

        equation = VGroup(
            text_mob("Loss measures", size=28, color=WHITE),
            Tex(r"=", font_size=28, color=YELLOW),
            text_mob("prediction", size=28, color=YELLOW),
            Tex(r"-", font_size=28, color=YELLOW),
            text_mob("target", size=28, color=YELLOW),
        ).arrange(RIGHT, buff=0.16)

        backprop_label = concept_chip("backpropagation", color=YELLOW, size=17)
        measure_row = VGroup(equation, loss_hi, backprop_label).arrange(RIGHT, buff=0.42)
        measure_row.next_to(pipeline, DOWN, buff=0.14)

        geo_panel = make_panel(width=12.45, height=1.40, stroke_color=MUTED, fill_opacity=0.08)
        geo_panel.next_to(measure_row, DOWN, buff=0.12)
        geo_panel.shift(LEFT * geo_panel.get_center()[0])
        embedding_space_label = text_mob("embedding space", size=18, color=MUTED)
        embedding_space_label.move_to(geo_panel.get_corner(UL) + RIGHT * 1.16 + DOWN * 0.21)
        after_label = text_mob("lower loss", size=18, color=GREEN)
        after_label.move_to(geo_panel.get_corner(UR) + LEFT * 1.08 + DOWN * 0.21)

        nn_to_space_arrow = make_flow_arrow(
            net_group.get_bottom() + DOWN * 0.02,
            geo_panel.get_top() + LEFT * 3.30 + UP * 0.02,
            color=GREEN,
            stroke_width=2.2,
        )
        nn_update_symbol = Tex(r"\Delta W", font_size=24, color=GREEN)
        nn_update_symbol.next_to(net_group, UP, buff=0.06)

        process_note = arrow_text_chain(
            ["Lower loss", "better parameters", "cleaner embeddings"],
            color=CYAN,
            size=18,
        )
        objective_note = text_mob("The objective shapes the space", size=17, color=WHITE)
        learning_note = VGroup(process_note, objective_note).arrange(DOWN, buff=0.06)
        learning_note.next_to(geo_panel, DOWN, buff=0.06)

        start_centers = [
            geo_panel.get_center() + LEFT * 3.66 + DOWN * 0.02,
            geo_panel.get_center() + LEFT * 0.38 + UP * 0.07,
            geo_panel.get_center() + RIGHT * 3.38 + DOWN * 0.02,
        ]
        target_centers = [
            geo_panel.get_center() + LEFT * 4.02 + UP * 0.20,
            geo_panel.get_center() + RIGHT * 0.02 + DOWN * 0.28,
            geo_panel.get_center() + RIGHT * 4.02 + UP * 0.20,
        ]
        dot_colors = [CYAN, GREEN, ORANGE]
        scattered = VGroup()
        target_markers = VGroup()
        for cls, color in enumerate(dot_colors):
            dots = cluster_dots(start_centers[cls], color, count=6, spread=0.30, seed=10 + cls, radius=0.058)
            scattered.add(dots)
            rng = np.random.default_rng(40 + cls)
            for _ in range(6):
                offset = rng.normal(0, 0.08, size=2)
                marker = Dot(point=target_centers[cls] + np.array([offset[0], offset[1], 0]), radius=0.001, color=WHITE)
                marker.set_opacity(0)
                target_markers.add(marker)
        all_dots = VGroup(*[dot for dots in scattered for dot in dots])
        rings = VGroup(*[
            Ellipse(width=0.74, height=0.52, stroke_color=color, stroke_width=1.7, fill_opacity=0).move_to(center)
            for center, color in zip(target_centers, dot_colors)
        ])

        body = Group(
            pipeline, target, measure_row, backprop_label,
            geo_panel, embedding_space_label, after_label, nn_to_space_arrow,
            nn_update_symbol, all_dots, rings, target_markers, learning_note,
        )
        safe_group(body, max_width=13.45, max_height=4.88, center=UP * 0.38)
        if body.get_top()[1] > 2.88:
            body.shift(DOWN * (body.get_top()[1] - 2.88))
        if body.get_bottom()[1] < CONTENT_BOTTOM:
            body.shift(UP * (CONTENT_BOTTOM - body.get_bottom()[1]))
        target_positions = [marker.get_center() for marker in target_markers]

        loss_fill_target = loss_hi[1][1].copy()
        loss_fill_target.set_width(loss_hi[1][0].get_width() * 0.22, stretch=True)
        loss_fill_target.set_fill(GREEN, opacity=0.88)
        loss_fill_target.move_to(loss_hi[1][0].get_left() + RIGHT * loss_fill_target.get_width() / 2)
        loss_value_target = text_mob("0.22", size=18, color=GREEN)
        loss_value_target.move_to(loss_hi[2])

        self.add(title, face_group)
        self.play(GrowArrow(arrows[0]), run_time=0.45)
        self.add(net_group)
        self.play(GrowArrow(arrows[1]), run_time=0.55)
        self.add(emb_group)
        self.play(GrowArrow(arrows[2]), run_time=0.55)
        self.add(probs_hi, target, loss_hi, equation)
        self.add(geo_panel, embedding_space_label, learning_note)
        self.play(LaggedStart(*[FadeIn(dot, scale=1.4) for dot in all_dots], lag_ratio=0.018), run_time=0.75)

        update_arrows = VGroup()
        for layer in net[1]:
            update_arrows.add(make_flow_arrow(loss_hi.get_left() + LEFT * 0.15, layer.get_bottom() + DOWN * 0.02, color=YELLOW, stroke_width=1.3))
        self.add(backprop_label)
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in update_arrows], lag_ratio=0.06), run_time=0.80)
        self.play(GrowArrow(nn_to_space_arrow), FadeIn(nn_update_symbol), run_time=0.55)
        self.play(
            Transform(loss_hi[1][1], loss_fill_target),
            Transform(loss_hi[2], loss_value_target),
            FadeOut(update_arrows),
            run_time=0.65,
        )
        self.play(*[dot.animate.move_to(pos) for dot, pos in zip(all_dots, target_positions)], run_time=1.35)
        self.add(after_label)
        self.play(LaggedStart(*[ShowCreation(ring) for ring in rings], lag_ratio=0.08), run_time=0.55)
        self.wait(0.85)

    # ------------------------------------------------------------------
    # Beat B - Basic Softmax concept.
    # ------------------------------------------------------------------
    def beat_b_softmax_basic_concept(self):
        title = title_block("Softmax Concept", "Compare one embedding with every known class")

        axes = Axes(
            x_range=[-3.25, 3.25, 1],
            y_range=[-2.70, 2.70, 1],
            width=6.15,
            height=4.35,
            axis_config={"stroke_color": MUTED, "stroke_width": 0.8},
        )
        axes.move_to(LEFT * 3.12 + UP * 0.48)
        origin = axes.c2p(0, 0)

        class_specs = [
            ("Person A", CYAN, 38 * DEGREES),
            ("Person B", GREEN, 136 * DEGREES),
            ("Person C", ORANGE, -94 * DEGREES),
        ]
        weight_arrows = VGroup()
        weight_labels = VGroup()
        class_points = VGroup()
        class_point_labels = VGroup()
        for label, color, angle in class_specs:
            end = origin + 2.08 * np.array([np.cos(angle), np.sin(angle), 0])
            arrow = Arrow(origin, end, buff=0, color=color, stroke_width=3.0, max_tip_length_to_length_ratio=0.12)
            tag = Tex(label[-1], font_size=28, color=color)
            tag.next_to(end, end - origin, buff=0.12)
            point = Dot(point=end, radius=0.075, color=color)
            point_label = text_mob(label, size=16, color=color)
            point_label.next_to(point, DOWN if angle < 0 else UP, buff=0.08)
            weight_arrows.add(arrow)
            weight_labels.add(tag)
            class_points.add(point)
            class_point_labels.add(point_label)

        emb_start = origin + 1.24 * np.array([np.cos(5 * DEGREES), np.sin(5 * DEGREES), 0])
        emb_target = origin + 1.88 * np.array([np.cos(34 * DEGREES), np.sin(34 * DEGREES), 0])
        emb_target_marker = Dot(point=emb_target, radius=0.001, color=WHITE)
        emb_target_marker.set_opacity(0)
        emb = Dot(point=emb_start, radius=0.120, color=WHITE)
        emb_label = VGroup(
            Tex(r"f", font_size=30, color=WHITE),
            text_mob("new sample", size=16, color=WHITE),
        ).arrange(RIGHT, buff=0.08).next_to(emb, DR, buff=0.08)
        emb_label_target = emb_label.copy().next_to(emb_target, DR, buff=0.08)

        compare_lines = VGroup(*[
            DashedLine(emb.get_center(), arrow.get_end(), stroke_color=arrow.get_color(), stroke_width=1.1, dash_length=0.08)
            for arrow in weight_arrows
        ])

        score_table = make_score_table([0.45, 0.15, -0.28], ["A", "B", "C"], [CYAN, GREEN, ORANGE])
        score_table.scale(1.06)
        prob_low = make_probability_panel([0.43, 0.31, 0.26], ["A", "B", "C"], [CYAN, GREEN, ORANGE], width=3.92)
        prob_high = make_probability_panel([0.82, 0.12, 0.06], ["A", "B", "C"], [CYAN, GREEN, ORANGE], width=3.92)
        right_col = VGroup(score_table, prob_low).arrange(DOWN, buff=0.38)
        right_col.move_to(RIGHT * 3.34 + UP * 0.18)
        prob_high.move_to(prob_low)

        softmax_arrow = make_flow_arrow(score_table.get_bottom() + DOWN * 0.03, prob_low.get_top() + UP * 0.03, color=YELLOW)
        space_label = text_mob("embedding space", size=18, color=MUTED)
        space_label.next_to(axes, DOWN, buff=0.08)
        line_class = text_mob("Each class has a weight vector", size=21, color=YELLOW)
        line_scores = text_mob("Scores become probabilities", size=21, color=YELLOW)
        line_train = text_mob("Training raises the true-class probability", size=21, color=GREEN)
        axis_notes = VGroup(space_label, line_class, line_scores, line_train).arrange(DOWN, buff=0.10)
        axis_notes.next_to(axes, DOWN, buff=0.10)

        layout = Group(
            title, axes, space_label, line_class, line_scores, line_train,
            weight_arrows, weight_labels, class_points, class_point_labels,
            emb, emb_label, compare_lines, right_col, softmax_arrow, emb_target_marker,
        )
        safe_group(layout, center=UP * 0.50)
        emb_target = emb_target_marker.get_center()
        emb_label_target.next_to(emb_target, DR, buff=0.08)
        compare_lines_target = VGroup(*[
            DashedLine(emb_target, arrow.get_end(), stroke_color=arrow.get_color(), stroke_width=1.1, dash_length=0.08)
            for arrow in weight_arrows
        ])
        prob_high.move_to(prob_low)
        axis_notes = VGroup(space_label, line_class, line_scores, line_train)
        winner_row_highlight = SurroundingRectangle(
            prob_high[1][1][0],
            color=GREEN,
            buff=0.06,
        )
        class_highlights = VGroup(*[
            Circle(radius=0.20, stroke_color=point.get_color(), stroke_width=2.2, fill_opacity=0).move_to(point)
            for point in class_points
        ])
        weight_highlights = VGroup(*[
            arrow.copy().set_stroke(color=arrow.get_color(), width=6.0, opacity=0.35)
            for arrow in weight_arrows
        ])

        self.add(title)
        self.play(ShowCreation(axes), run_time=0.65)
        self.add(space_label, line_class)
        for point, point_label, arrow, label, point_highlight, weight_highlight in zip(
            class_points, class_point_labels, weight_arrows, weight_labels, class_highlights, weight_highlights
        ):
            self.play(FadeIn(point, scale=1.25), FadeIn(point_label), run_time=0.30)
            self.play(ShowCreation(point_highlight), run_time=0.25)
            self.play(GrowArrow(arrow), FadeIn(label), ShowCreation(weight_highlight), run_time=0.50)
            self.play(FadeOut(point_highlight), FadeOut(weight_highlight), run_time=0.20)
        self.add(emb_label)
        self.play(FadeIn(emb, scale=1.3), run_time=0.35)
        self.play(LaggedStart(*[ShowCreation(line) for line in compare_lines], lag_ratio=0.08), run_time=0.65)
        self.add(score_table, prob_low)
        self.play(GrowArrow(softmax_arrow), run_time=0.45)
        self.add(line_scores)
        self.play(
            emb.animate.move_to(emb_target),
            Transform(compare_lines, compare_lines_target),
            Transform(prob_low, prob_high),
            run_time=1.25,
        )
        self.remove(emb_label, prob_low)
        self.add(emb_label_target, prob_high)
        self.play(ShowCreation(winner_row_highlight), run_time=0.35)
        self.add(line_train)
        self.wait(0.85)

    # ------------------------------------------------------------------
    # Beat C - Decision boundaries.
    # ------------------------------------------------------------------
    def beat_c_decision_boundaries(self):
        title = title_block("Decision Boundary", "Embedding space becomes class regions")

        plane = make_panel(width=7.05, height=4.76, stroke_color=MUTED, fill_opacity=0.05)
        plane.move_to(LEFT * 2.72 + UP * 0.24)
        center = plane.get_center()
        radius = 2.34
        sectors = VGroup(
            Sector(radius=radius, start_angle=-30 * DEGREES, angle=120 * DEGREES, arc_center=center, fill_color=CYAN, fill_opacity=0.12, stroke_width=0),
            Sector(radius=radius, start_angle=90 * DEGREES, angle=120 * DEGREES, arc_center=center, fill_color=GREEN, fill_opacity=0.12, stroke_width=0),
            Sector(radius=radius, start_angle=210 * DEGREES, angle=120 * DEGREES, arc_center=center, fill_color=ORANGE, fill_opacity=0.12, stroke_width=0),
        )
        region_labels = VGroup(
            text_mob("Person A", size=20, color=CYAN).move_to(center + RIGHT * 1.55 + UP * 0.30),
            text_mob("Person B", size=20, color=GREEN).move_to(center + LEFT * 1.36 + UP * 0.84),
            text_mob("Person C", size=20, color=ORANGE).move_to(center + DOWN * 1.58),
        )

        weight_angles = [30 * DEGREES, 150 * DEGREES, 270 * DEGREES]
        weight_colors = [CYAN, GREEN, ORANGE]
        weights = VGroup(*[
            Arrow(center, center + 1.88 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=c, stroke_width=2.7, max_tip_length_to_length_ratio=0.12)
            for a, c in zip(weight_angles, weight_colors)
        ])
        boundaries = VGroup(*[
            DashedLine(center, center + 2.46 * np.array([np.cos(a), np.sin(a), 0]), stroke_color=MUTED, stroke_width=1.7, dash_length=0.10)
            for a in [90 * DEGREES, 210 * DEGREES, 330 * DEGREES]
        ])
        boundary_label = concept_chip("decision boundary", color=YELLOW, size=19)
        boundary_label.next_to(boundaries[0], RIGHT, buff=0.10)

        dot_a_pos = center + RIGHT * 1.14 + UP * 0.26
        dot_b_pos = center + LEFT * 0.76 + UP * 1.08
        sample = Dot(point=dot_a_pos, radius=0.118, color=WHITE)
        sample_label = Tex(r"f_i", font_size=28, color=WHITE).next_to(sample, DR, buff=0.08)
        sample_label_b = Tex(r"f_i", font_size=28, color=WHITE).next_to(dot_b_pos, UL, buff=0.08)
        path = DashedLine(dot_a_pos, dot_b_pos, stroke_color=WHITE, stroke_width=1.1, dash_length=0.10)

        pred_a = concept_chip("prediction: Person A", color=CYAN, size=22)
        pred_b = concept_chip("prediction: Person B", color=GREEN, size=22).move_to(pred_a)
        pred_a.move_to(RIGHT * 3.28 + UP * 1.18)
        pred_b.move_to(pred_a)

        explanation = callout_box(
            [
                "Each region has one top class",
                ("Cross boundary", "prediction changes"),
                "Works well for closed-set classification",
            ],
            color=YELLOW,
            width=5.15,
            size=20,
        )
        explanation.move_to(RIGHT * 3.26 + DOWN * 0.22)

        layout = Group(title, plane, sectors, region_labels, weights, boundaries, boundary_label, sample, sample_label, path, pred_a, explanation)
        safe_group(layout, center=UP * 0.42)
        dot_b_pos = path.get_end()
        sample_label_b.next_to(dot_b_pos, UL, buff=0.08)
        pred_b.move_to(pred_a)

        self.add(title)
        self.play(FadeIn(plane), FadeIn(sectors), run_time=0.55)
        self.play(LaggedStart(*[GrowArrow(w) for w in weights], lag_ratio=0.10), run_time=0.75)
        self.add(region_labels)
        self.play(LaggedStart(*[ShowCreation(b) for b in boundaries], lag_ratio=0.08), run_time=0.65)
        self.add(boundary_label, sample, sample_label, pred_a)
        self.play(ShowCreation(path), sample.animate.move_to(dot_b_pos), run_time=1.05)
        self.remove(sample_label)
        self.add(sample_label_b)
        self.remove(pred_a)
        self.add(pred_b, explanation)
        self.wait(0.90)

    # ------------------------------------------------------------------
    # Beat D - Softmax limitations.
    # ------------------------------------------------------------------
    def beat_d_softmax_limitations(self):
        title = title_block("Softmax Limitation", "Correct classification is not enough")

        plane = make_panel(width=6.12, height=4.55, stroke_color=MUTED, fill_opacity=0.05)
        plane.move_to(LEFT * 3.10 + UP * 0.28)
        center = plane.get_center()
        left_region = Rectangle(width=plane.get_width() / 2, height=plane.get_height(), stroke_width=0, fill_color=CYAN, fill_opacity=0.08)
        right_region = Rectangle(width=plane.get_width() / 2, height=plane.get_height(), stroke_width=0, fill_color=GREEN, fill_opacity=0.08)
        left_region.move_to(plane.get_center() + LEFT * plane.get_width() / 4)
        right_region.move_to(plane.get_center() + RIGHT * plane.get_width() / 4)
        boundary = DashedLine(center + UP * 2.10, center + DOWN * 2.10, stroke_color=YELLOW, stroke_width=1.9, dash_length=0.10)
        danger = Rectangle(width=0.62, height=4.18, stroke_width=0, fill_color=YELLOW, fill_opacity=0.13).move_to(center)
        danger_label = text_mob("fragile zone", size=18, color=YELLOW).next_to(boundary, UP, buff=0.10)
        region_names = VGroup(
            text_mob("Person A", size=20, color=CYAN).move_to(plane.get_center() + LEFT * 1.86 + UP * 1.80),
            text_mob("Person B", size=20, color=GREEN).move_to(plane.get_center() + RIGHT * 1.86 + UP * 1.80),
        )

        point_ok = Dot(point=center + LEFT * 0.34 + DOWN * 0.28, radius=0.118, color=WHITE)
        point_bad_pos = center + RIGHT * 0.44 + DOWN * 0.12
        point_label = text_mob("correct, but close", size=18, color=WHITE).next_to(point_ok, DOWN, buff=0.10)
        noise_arrow = make_flow_arrow(point_ok.get_center(), point_bad_pos, color=RED, stroke_width=2.2)
        noise_label = text_mob("small noise", size=18, color=RED).next_to(noise_arrow, UP, buff=0.06)
        wrong = concept_chip("misclassified", color=RED, size=19).next_to(point_bad_pos, DOWN, buff=0.18)

        rule = callout_box(
            [
                "Softmax only needs:",
                "true class has the top score",
                "correct side is enough",
            ],
            color=YELLOW,
            width=4.85,
            size=20,
        )
        rule.move_to(RIGHT * 3.06 + UP * 1.48)

        cluster_panel = make_panel(width=5.38, height=2.35, stroke_color=RED, fill_opacity=0.06)
        cluster_panel.move_to(RIGHT * 3.06 + DOWN * 0.78)
        loose_a = cluster_dots(cluster_panel.get_center() + LEFT * 0.66 + UP * 0.12, CYAN, count=13, spread=0.48, seed=70, radius=0.058)
        loose_b = cluster_dots(cluster_panel.get_center() + RIGHT * 0.70 + DOWN * 0.02, GREEN, count=13, spread=0.48, seed=80, radius=0.058)
        ring_a = ring_around(loose_a, CYAN, buff=0.26)
        ring_b = ring_around(loose_b, GREEN, buff=0.26)
        overlap = Ellipse(width=1.20, height=0.78, stroke_color=RED, stroke_width=2.0, fill_color=RED, fill_opacity=0.08)
        overlap.move_to(cluster_panel.get_center() + RIGHT * 0.02 + UP * 0.02)
        spread = make_double_arrow(
            cluster_panel.get_center() + LEFT * 1.55 + DOWN * 0.78,
            cluster_panel.get_center() + LEFT * 0.32 + DOWN * 0.78,
            color=CYAN,
            stroke_width=1.5,
        )
        spread_label = text_mob("wide spread", size=17, color=CYAN).next_to(spread, DOWN, buff=0.04)
        close_label = text_mob("classes still close", size=17, color=RED).next_to(overlap, UP, buff=0.06)

        mismatch = callout_box(
            [
                "Face recognition needs:",
                "tight same-identity clusters",
                "wide gaps between identities",
            ],
            color=GREEN,
            width=5.38,
            size=18,
        )
        mismatch.next_to(cluster_panel, DOWN, buff=0.12)

        layout = Group(
            title, plane, left_region, right_region, danger, boundary, danger_label, region_names,
            point_ok, point_label, noise_arrow, noise_label, wrong, rule,
            cluster_panel, loose_a, loose_b, ring_a, ring_b, overlap, spread, spread_label, close_label, mismatch,
        )
        safe_group(layout, center=UP * 0.50)
        point_bad_pos = noise_arrow.get_end()
        wrong.next_to(point_bad_pos, DOWN, buff=0.18)

        self.add(title)
        self.play(FadeIn(plane), FadeIn(left_region), FadeIn(right_region), FadeIn(danger), ShowCreation(boundary), run_time=0.70)
        self.add(region_names, danger_label, point_label)
        self.play(FadeIn(point_ok, scale=1.25), run_time=0.30)
        self.add(noise_label)
        self.play(GrowArrow(noise_arrow), point_ok.animate.move_to(point_bad_pos), run_time=0.85)
        self.add(wrong, rule)
        self.play(FadeIn(cluster_panel), LaggedStart(*[FadeIn(dot) for dot in VGroup(*loose_a, *loose_b)], lag_ratio=0.012), run_time=0.95)
        self.add(close_label)
        self.play(ShowCreation(ring_a), ShowCreation(ring_b), FadeIn(overlap), run_time=0.70)
        self.add(spread_label, mismatch)
        self.play(ShowCreation(spread), run_time=0.45)
        self.wait(0.95)

    # ------------------------------------------------------------------
    # Beat E - Need better objectives.
    # ------------------------------------------------------------------
    def beat_e_need_better_objectives(self):
        title = title_block("Need Better Objectives?", "Classification plus geometry")

        softmax_panel = make_panel(width=5.55, height=3.52, stroke_color=YELLOW, fill_opacity=0.06)
        geometry_panel = make_panel(width=5.55, height=3.52, stroke_color=GREEN, fill_opacity=0.06)
        softmax_panel.move_to(LEFT * 3.02 + UP * 0.76)
        geometry_panel.move_to(RIGHT * 3.02 + UP * 0.76)

        soft_title = concept_chip("Softmax objective", color=YELLOW, size=21)
        geo_title = concept_chip("Face recognition objective", color=GREEN, size=21)
        soft_title.next_to(softmax_panel, UP, buff=0.12)
        geo_title.next_to(geometry_panel, UP, buff=0.12)

        soft_boundary = DashedLine(
            softmax_panel.get_center() + UP * 1.05,
            softmax_panel.get_center() + DOWN * 1.05,
            stroke_color=YELLOW,
            stroke_width=1.6,
            dash_length=0.10,
        )
        soft_dot = Dot(point=softmax_panel.get_center() + LEFT * 0.24 + DOWN * 0.10, color=WHITE, radius=0.108)
        soft_ok = concept_chip("correct side", color=CYAN, size=18).next_to(soft_dot, DOWN, buff=0.14)
        soft_notes = VGroup(
            text_mob("classification: OK", size=19, color=WHITE),
            text_mob("margin: not enforced", size=19, color=RED),
        ).arrange(DOWN, buff=0.12)
        soft_notes.move_to(softmax_panel.get_center() + DOWN * 1.05)

        tight_a = cluster_dots(geometry_panel.get_center() + LEFT * 1.25 + UP * 0.38, CYAN, count=7, spread=0.13, seed=120, radius=0.066)
        tight_b = cluster_dots(geometry_panel.get_center() + RIGHT * 1.25 + DOWN * 0.25, GREEN, count=7, spread=0.13, seed=130, radius=0.066)
        tight_c = cluster_dots(geometry_panel.get_center() + RIGHT * 0.40 + UP * 0.98, ORANGE, count=6, spread=0.12, seed=140, radius=0.066)
        rings = VGroup(ring_around(tight_a, CYAN, buff=0.18), ring_around(tight_b, GREEN, buff=0.18), ring_around(tight_c, ORANGE, buff=0.18))
        margin_arrow = make_double_arrow(
            geometry_panel.get_center() + LEFT * 0.54 + DOWN * 0.28,
            geometry_panel.get_center() + RIGHT * 0.54 + DOWN * 0.28,
            color=YELLOW,
            stroke_width=1.8,
        )
        margin_label = text_mob("large margin", size=18, color=YELLOW).next_to(margin_arrow, DOWN, buff=0.06)
        geo_notes = VGroup(
            text_mob("compact clusters", size=19, color=CYAN),
            text_mob("clear separation", size=19, color=GREEN),
        ).arrange(DOWN, buff=0.12)
        geo_notes.move_to(geometry_panel.get_center() + DOWN * 1.18)

        question = callout_box(
            [
                "Can the loss directly control",
                "the geometry of embedding space?",
            ],
            color=WHITE,
            width=6.10,
            size=22,
        )
        question.move_to(UP * -0.70)

        next_note = text_mob("Next: margin-based losses", size=24, color=WHITE)
        next_note.move_to(UP * -0.15)

        layout = Group(
            title, softmax_panel, geometry_panel, soft_title, geo_title,
            soft_boundary, soft_dot, soft_ok, soft_notes,
            tight_a, tight_b, tight_c, rings, margin_arrow, margin_label, geo_notes,
            question, next_note,
        )
        safe_group(layout, center=UP * 0.58)

        self.add(title)
        self.play(FadeIn(softmax_panel), ShowCreation(soft_boundary), FadeIn(soft_dot, scale=1.25), run_time=0.70)
        self.add(soft_title, soft_ok, soft_notes)
        self.play(FadeIn(geometry_panel), LaggedStart(*[FadeIn(dot, scale=1.3) for dot in VGroup(*tight_a, *tight_b, *tight_c)], lag_ratio=0.02), run_time=0.90)
        self.add(geo_title, margin_label, geo_notes)
        self.play(LaggedStart(*[ShowCreation(r) for r in rings], lag_ratio=0.10), ShowCreation(margin_arrow), run_time=0.70)
        self.add(question)
        self.wait(0.25)
        self.remove(question)
        self.add(next_note)
        self.wait(0.95)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.30)

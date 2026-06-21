from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 05 - Evolution
# Narration-aligned rewrite:
# - Better objectives for embedding geometry
# - FaceNet and Triplet Loss
# - Angular margin idea
# - SphereFace, CosFace, ArcFace milestones
# - Transition to ArcFace mechanism
# =============================================================================


SAFE_BOTTOM = -FRAME_HEIGHT / 2 + SUBTITLE_HEIGHT + FRAME_MARGIN
CONTENT_BOTTOM = SAFE_BOTTOM + 0.08
CONTENT_TOP = FRAME_HEIGHT / 2 - FRAME_MARGIN
TITLE_Y = 3.43


def text_mob(text, size=24, color=WHITE, bold=False):
    command = r"\textbf" if bold else r"\text"
    return latex(rf"{command}{{{tex_text(text)}}}", size=size, color=color)


def title_block(title, subtitle=None, title_size=42, subtitle_size=20):
    main = text_mob(title, size=title_size, color=WHITE, bold=True)
    if subtitle is None:
        main.move_to(UP * TITLE_Y)
        return main
    sub = text_mob(subtitle, size=subtitle_size, color=MUTED)
    group = VGroup(main, sub).arrange(DOWN, buff=0.10)
    group.move_to(UP * 3.42)
    return group


def concept_chip(label, color=CYAN, size=19):
    return make_badge(label, color=color, font_size=size, h_buff=0.22, v_buff=0.10)


def formula_box(formula, color=CYAN, size=30, width=None):
    formula_mob = Tex(formula, font_size=size, color=color)
    if width is not None:
        fit_to_bounds(formula_mob, max_width=width - 0.38)
    box = RoundedRectangle(
        width=max(formula_mob.get_width() + 0.48, 1.40) if width is None else width,
        height=formula_mob.get_height() + 0.34,
        corner_radius=0.10,
        stroke_color=color,
        stroke_width=1.4,
        fill_color=PANEL,
        fill_opacity=0.30,
    )
    formula_mob.move_to(box)
    return VGroup(box, formula_mob)


def key_points(lines, color=CYAN, width=4.65, size=19):
    rows = VGroup()
    for item in lines:
        if isinstance(item, tuple):
            label, item_color = item
        else:
            label, item_color = item, color
        bullet = Dot(radius=0.045, color=item_color)
        label_mob = text_mob(label, size=size, color=WHITE)
        row = VGroup(bullet, label_mob).arrange(RIGHT, buff=0.13)
        rows.add(row)
    rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    fit_to_bounds(rows, max_width=width - 0.38)
    panel = make_panel(
        width=width,
        height=max(rows.get_height() + 0.44, 0.72),
        stroke_color=color,
        fill_opacity=0.13,
    )
    rows.move_to(panel)
    return VGroup(panel, rows)


def arrow_chain(labels, color=CYAN, size=20):
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


def safe_group(group, max_width=12.85, max_height=5.48, center=ORIGIN + UP * 0.42):
    fit_to_bounds(group, max_width=max_width, max_height=max_height)
    group.move_to(center)
    if group.get_top()[1] > CONTENT_TOP:
        group.shift(DOWN * (group.get_top()[1] - CONTENT_TOP))
    if group.get_bottom()[1] < CONTENT_BOTTOM:
        group.shift(UP * (CONTENT_BOTTOM - group.get_bottom()[1]))
    return group


def cluster_dots(center, color, count=7, spread=0.18, seed=1, radius=0.060):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        offset = rng.normal(0, spread, size=2)
        dots.add(Dot(point=center + np.array([offset[0], offset[1], 0]), color=color, radius=radius))
    return dots


def ring_around(mob, color, buff=0.24):
    ring = Ellipse(
        width=mob.get_width() + buff,
        height=mob.get_height() + buff * 0.80,
        stroke_color=color,
        stroke_width=1.7,
        fill_opacity=0,
    )
    ring.move_to(mob)
    return ring


def timeline_node(year, name, detail, color=CYAN, width=2.48):
    year_mob = text_mob(year, size=20, color=color, bold=True)
    name_mob = text_mob(name, size=23, color=WHITE, bold=True)
    detail_mob = text_mob(detail, size=15, color=MUTED)
    labels = VGroup(year_mob, name_mob, detail_mob).arrange(DOWN, buff=0.06)
    fit_to_bounds(labels, max_width=width - 0.32)
    box = RoundedRectangle(
        width=width,
        height=1.16,
        corner_radius=0.12,
        stroke_color=color,
        stroke_width=1.5,
        fill_color=PANEL,
        fill_opacity=0.24,
    )
    labels.move_to(box)
    return VGroup(box, labels)


def make_two_class_boundary(panel, left_color=CYAN, right_color=GREEN):
    center = panel.get_center()
    left_region = Rectangle(
        width=panel.get_width() / 2,
        height=panel.get_height(),
        stroke_width=0,
        fill_color=left_color,
        fill_opacity=0.08,
    )
    right_region = Rectangle(
        width=panel.get_width() / 2,
        height=panel.get_height(),
        stroke_width=0,
        fill_color=right_color,
        fill_opacity=0.08,
    )
    left_region.move_to(center + LEFT * panel.get_width() / 4)
    right_region.move_to(center + RIGHT * panel.get_width() / 4)
    boundary = DashedLine(
        center + UP * (panel.get_height() / 2 - 0.20),
        center + DOWN * (panel.get_height() / 2 - 0.20),
        stroke_color=YELLOW,
        stroke_width=1.7,
        dash_length=0.10,
    )
    return VGroup(left_region, right_region, boundary)


class Scene05_Evolution(Scene):
    def construct(self):
        self.camera.background_color = DARK

        card = make_centered_title_card(
            "Evolution of Loss Functions",
            "From metric learning to angular margin",
            title_size=48,
            subtitle_size=23,
        )
        self.play(FadeIn(card), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.45)

        self.beat_a_better_objectives()
        self.clear_and_wait()
        self.beat_b_facenet_triplet()
        self.clear_and_wait()
        self.beat_c_angular_margin_idea()
        self.clear_and_wait()
        self.beat_d_sphereface()
        self.clear_and_wait()
        self.beat_e_cosface()
        self.clear_and_wait()
        self.beat_f_arcface()
        self.clear_and_wait()
        self.beat_g_transition()

    # ------------------------------------------------------------------
    # Beat A - Motivation for geometry-aware objectives.
    # ------------------------------------------------------------------
    def beat_a_better_objectives(self):
        title = title_block(
            "Why New Loss Functions?",
            "The loss starts shaping embedding geometry",
            title_size=40,
            subtitle_size=20,
        )

        soft_panel = make_panel(width=5.35, height=3.40, stroke_color=YELLOW, fill_opacity=0.06)
        geo_panel = make_panel(width=5.35, height=3.40, stroke_color=GREEN, fill_opacity=0.06)
        soft_panel.move_to(LEFT * 3.05 + UP * 0.64)
        geo_panel.move_to(RIGHT * 3.05 + UP * 0.64)

        soft_title = concept_chip("Softmax", color=YELLOW, size=21)
        geo_title = concept_chip("Geometry-aware loss", color=GREEN, size=21)
        soft_title.next_to(soft_panel, UP, buff=0.12)
        geo_title.next_to(geo_panel, UP, buff=0.12)

        soft_regions = make_two_class_boundary(soft_panel)
        soft_dot = Dot(point=soft_panel.get_center() + LEFT * 0.28 + DOWN * 0.20, radius=0.110, color=WHITE)
        soft_label = text_mob("correct side", size=18, color=CYAN).next_to(soft_dot, DOWN, buff=0.10)
        fragile = Rectangle(
            width=0.58,
            height=soft_panel.get_height() - 0.40,
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=0.12,
        ).move_to(soft_panel)
        fragile_label = text_mob("no enforced margin", size=17, color=YELLOW)
        fragile_label.next_to(soft_regions[2], UP, buff=0.08)

        compact_a = cluster_dots(geo_panel.get_center() + LEFT * 1.15 + UP * 0.42, CYAN, count=8, spread=0.12, seed=21)
        compact_b = cluster_dots(geo_panel.get_center() + RIGHT * 1.22 + DOWN * 0.18, GREEN, count=8, spread=0.12, seed=22)
        rings = VGroup(ring_around(compact_a, CYAN, buff=0.20), ring_around(compact_b, GREEN, buff=0.20))
        margin = make_double_arrow(
            geo_panel.get_center() + LEFT * 0.46 + DOWN * 0.70,
            geo_panel.get_center() + RIGHT * 0.56 + DOWN * 0.70,
            color=YELLOW,
            stroke_width=1.7,
        )
        margin_label = text_mob("large margin", size=18, color=YELLOW).next_to(margin, DOWN, buff=0.04)
        geo_labels = VGroup(
            text_mob("compact clusters", size=18, color=CYAN),
            text_mob("clear separation", size=18, color=GREEN),
        ).arrange(DOWN, buff=0.08)
        geo_labels.move_to(geo_panel.get_center() + DOWN * 1.28)

        question = key_points(
            [
                "Can the objective directly organize embedding space?",
                ("Same identity close together", GREEN),
                ("Different identities far apart", YELLOW),
            ],
            color=WHITE,
            width=7.05,
            size=20,
        )
        question.move_to(DOWN * 1.70)

        bridge_arrow = make_flow_arrow(
            soft_panel.get_right() + RIGHT * 0.12,
            geo_panel.get_left() + LEFT * 0.12,
            color=CYAN,
            stroke_width=2.4,
        )

        layout = Group(
            title,
            soft_panel, fragile, soft_regions, soft_title, soft_dot, soft_label, fragile_label,
            geo_panel, compact_a, compact_b, rings, margin, margin_label, geo_labels, geo_title,
            bridge_arrow, question,
        )
        safe_group(layout, center=UP * 0.54)

        self.add(title)
        self.play(
            FadeIn(soft_panel),
            FadeIn(fragile),
            FadeIn(soft_regions),
            FadeIn(soft_title),
            run_time=0.65,
        )
        self.add(fragile_label, soft_label)
        self.play(FadeIn(soft_dot, scale=1.25), run_time=0.35)
        self.play(GrowArrow(bridge_arrow), run_time=0.45)
        self.play(
            FadeIn(geo_panel),
            FadeIn(geo_title),
            LaggedStart(*[FadeIn(dot, scale=1.25) for dot in VGroup(*compact_a, *compact_b)], lag_ratio=0.02),
            run_time=0.80,
        )
        self.play(
            LaggedStart(*[ShowCreation(ring) for ring in rings], lag_ratio=0.12),
            ShowCreation(margin),
            FadeIn(margin_label),
            FadeIn(geo_labels),
            run_time=0.70,
        )
        self.add(question)
        self.wait(0.95)

    # ------------------------------------------------------------------
    # Beat B - FaceNet and metric learning.
    # ------------------------------------------------------------------
    def beat_b_facenet_triplet(self):
        title = title_block("2015: FaceNet", "Metric learning with triplet loss")

        anchor = make_image_card("person1_1.png", width=1.10, height=1.28, label="anchor", stroke_color=WHITE, label_size=15)
        positive = make_image_card("person1_2.png", width=1.10, height=1.28, label="positive", stroke_color=GREEN, label_size=15)
        negative = make_image_card("person2_1.png", width=1.10, height=1.28, label="negative", stroke_color=RED, label_size=15)
        triplet = Group(anchor, positive, negative).arrange(RIGHT, buff=0.74)
        triplet.move_to(LEFT * 3.35 + UP * 1.32)

        pull_arrow = make_flow_arrow(anchor.get_right(), positive.get_left(), color=GREEN, stroke_width=2.0)
        push_arrow = make_flow_arrow(anchor.get_right() + DOWN * 0.18, negative.get_left() + DOWN * 0.18, color=RED, stroke_width=2.0)
        pull_label = text_mob("pull close", size=17, color=GREEN).next_to(pull_arrow, UP, buff=0.06)
        push_label = text_mob("push away", size=17, color=RED).next_to(push_arrow, DOWN, buff=0.06)

        triplet_formula = formula_box(r"L=\left[d(a,p)-d(a,n)+\alpha\right]_+", color=YELLOW, size=30, width=4.45)
        triplet_formula.move_to(LEFT * 3.35 + DOWN * 0.68)

        space = make_panel(width=5.55, height=3.80, stroke_color=CYAN, fill_opacity=0.05)
        space.move_to(RIGHT * 3.08 + UP * 0.44)
        space_label = text_mob("embedding space", size=18, color=MUTED)
        space_label.move_to(space.get_corner(UL) + RIGHT * 1.05 + DOWN * 0.23)

        a_pos = space.get_center() + LEFT * 0.90 + UP * 0.24
        p_pos_start = space.get_center() + RIGHT * 0.18 + UP * 0.66
        p_pos_target = space.get_center() + LEFT * 0.48 + UP * 0.34
        n_pos_start = space.get_center() + RIGHT * 0.10 + DOWN * 0.15
        n_pos_target = space.get_center() + RIGHT * 1.58 + DOWN * 0.72

        a_dot = Dot(point=a_pos, radius=0.100, color=WHITE)
        p_dot = Dot(point=p_pos_start, radius=0.100, color=GREEN)
        n_dot = Dot(point=n_pos_start, radius=0.100, color=RED)
        a_label = Tex(r"a", font_size=24, color=WHITE).next_to(a_dot, UL, buff=0.06)
        p_label = Tex(r"p", font_size=24, color=GREEN).next_to(p_dot, UR, buff=0.06)
        n_label = Tex(r"n", font_size=24, color=RED).next_to(n_dot, DR, buff=0.06)
        p_target_marker = Dot(point=p_pos_target, radius=0.001, color=GREEN)
        p_target_marker.set_opacity(0)
        n_target_marker = Dot(point=n_pos_target, radius=0.001, color=RED)
        n_target_marker.set_opacity(0)

        pull_vec = make_flow_arrow(p_pos_start, p_pos_target, color=GREEN, stroke_width=2.2)
        push_vec = make_flow_arrow(n_pos_start, n_pos_target, color=RED, stroke_width=2.2)
        close_ring = Ellipse(width=1.00, height=0.58, stroke_color=GREEN, stroke_width=1.8, fill_opacity=0)
        close_ring.move_to((a_pos + p_pos_target) / 2)
        far_gap = make_double_arrow(a_pos + DOWN * 0.72, n_pos_target + DOWN * 0.08, color=YELLOW, stroke_width=1.5)
        far_label = text_mob("larger distance", size=17, color=YELLOW).next_to(far_gap, DOWN, buff=0.04)

        notes = key_points(
            [
                "Learns a distance metric",
                ("Same identity becomes close", GREEN),
                ("Different identity moves far", RED),
                ("Triplet mining is difficult", YELLOW),
            ],
            color=CYAN,
            width=5.55,
            size=18,
        )
        notes.next_to(space, DOWN, buff=0.18)

        layout = Group(
            title, triplet, pull_arrow, push_arrow, pull_label, push_label, triplet_formula,
            space, space_label, a_dot, p_dot, n_dot, a_label, p_label, n_label,
            pull_vec, push_vec, close_ring, far_gap, far_label, notes,
            p_target_marker, n_target_marker,
        )
        safe_group(layout, center=UP * 0.50)

        self.add(title)
        self.play(FadeIn(anchor), FadeIn(positive), FadeIn(negative), run_time=0.65)
        self.play(GrowArrow(pull_arrow), FadeIn(pull_label), run_time=0.40)
        self.play(GrowArrow(push_arrow), FadeIn(push_label), run_time=0.40)
        self.play(FadeIn(triplet_formula), run_time=0.50)
        self.play(FadeIn(space), FadeIn(space_label), FadeIn(a_dot, scale=1.25), FadeIn(p_dot, scale=1.25), FadeIn(n_dot, scale=1.25), run_time=0.70)
        self.add(a_label, p_label, n_label)
        self.play(GrowArrow(pull_vec), p_dot.animate.move_to(p_target_marker.get_center()), run_time=0.85)
        self.play(GrowArrow(push_vec), n_dot.animate.move_to(n_target_marker.get_center()), run_time=0.85)
        p_label.next_to(p_dot, UR, buff=0.06)
        n_label.next_to(n_dot, DR, buff=0.06)
        self.play(ShowCreation(close_ring), ShowCreation(far_gap), FadeIn(far_label), run_time=0.60)
        self.add(notes)
        self.wait(0.95)

    # ------------------------------------------------------------------
    # Beat C - Angular margin idea.
    # ------------------------------------------------------------------
    def beat_c_angular_margin_idea(self):
        title = title_block("Angular Margin", "Identity is organized by direction")

        circle = Circle(radius=2.18, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
        circle.move_to(LEFT * 3.18 + UP * 0.28)
        center = circle.get_center()

        w_a_angle = 28 * DEGREES
        w_b_angle = 128 * DEGREES
        f_angle = 70 * DEGREES
        boundary_angle = 78 * DEGREES
        margin_angle = 16 * DEGREES

        w_a = Arrow(center, center + 2.18 * np.array([np.cos(w_a_angle), np.sin(w_a_angle), 0]), buff=0, color=CYAN, stroke_width=2.6, max_tip_length_to_length_ratio=0.12)
        w_b = Arrow(center, center + 2.18 * np.array([np.cos(w_b_angle), np.sin(w_b_angle), 0]), buff=0, color=GREEN, stroke_width=2.6, max_tip_length_to_length_ratio=0.12)
        w_a_label = Tex(r"W_A", font_size=24, color=CYAN).next_to(w_a.get_end(), RIGHT, buff=0.08)
        w_b_label = Tex(r"W_B", font_size=24, color=GREEN).next_to(w_b.get_end(), LEFT, buff=0.08)

        emb_end = center + 1.96 * np.array([np.cos(f_angle), np.sin(f_angle), 0])
        emb = Dot(point=emb_end, radius=0.105, color=WHITE)
        emb_label = Tex(r"f_i", font_size=25, color=WHITE).next_to(emb, UP, buff=0.08)

        boundary = DashedLine(
            center + 2.42 * np.array([np.cos(boundary_angle), np.sin(boundary_angle), 0]),
            center - 2.42 * np.array([np.cos(boundary_angle), np.sin(boundary_angle), 0]),
            stroke_color=YELLOW,
            stroke_width=1.6,
            dash_length=0.10,
        )
        strict_boundary = DashedLine(
            center + 2.42 * np.array([np.cos(boundary_angle - margin_angle), np.sin(boundary_angle - margin_angle), 0]),
            center - 2.42 * np.array([np.cos(boundary_angle - margin_angle), np.sin(boundary_angle - margin_angle), 0]),
            stroke_color=GREEN,
            stroke_width=2.0,
            dash_length=0.10,
        )
        boundary_label = text_mob("decision boundary", size=17, color=YELLOW)
        boundary_label.next_to(boundary.get_start(), UP, buff=0.06)
        strict_label = text_mob("margin boundary", size=17, color=GREEN)
        strict_label.next_to(strict_boundary.get_end(), DOWN, buff=0.06)

        theta_arc = Arc(radius=0.72, start_angle=w_a_angle, angle=f_angle - w_a_angle, stroke_color=WHITE, stroke_width=2.0)
        theta_arc.shift(center)
        theta_label = Tex(r"\theta", font_size=23, color=WHITE)
        theta_label.move_to(center + 0.92 * np.array([np.cos((w_a_angle + f_angle) / 2), np.sin((w_a_angle + f_angle) / 2), 0]))
        margin_arc = Arc(radius=1.04, start_angle=f_angle, angle=margin_angle, stroke_color=YELLOW, stroke_width=2.4)
        margin_arc.shift(center)
        margin_label = Tex(r"m", font_size=23, color=YELLOW)
        margin_label.move_to(center + 1.24 * np.array([np.cos(f_angle + margin_angle / 2), np.sin(f_angle + margin_angle / 2), 0]))

        condition = VGroup(
            formula_box(r"\cos\theta_y", color=MUTED, size=30, width=2.15),
            Arrow(LEFT * 0.42, RIGHT * 0.42, buff=0.04, color=CYAN, stroke_width=2.1, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\cos(\theta_y+m)", color=YELLOW, size=30, width=2.82),
        ).arrange(RIGHT, buff=0.22)
        condition.move_to(RIGHT * 3.15 + UP * 1.50)

        notes = key_points(
            [
                "Softmax only asks for the correct side",
                ("Margin makes the condition stricter", YELLOW),
                ("Same-class embeddings become compact", GREEN),
                ("Different identities get wider gaps", CYAN),
            ],
            color=YELLOW,
            width=5.25,
            size=19,
        )
        notes.move_to(RIGHT * 3.15 + DOWN * 0.22)

        chain = arrow_chain(["classify correctly", "add margin", "shape geometry"], color=CYAN, size=18)
        chain.next_to(notes, DOWN, buff=0.18)

        layout = Group(
            title, circle, w_a, w_b, w_a_label, w_b_label, emb, emb_label,
            boundary, strict_boundary, boundary_label, strict_label,
            theta_arc, theta_label, margin_arc, margin_label, condition, notes, chain,
        )
        safe_group(layout, center=UP * 0.50)

        self.add(title)
        self.play(ShowCreation(circle), run_time=0.50)
        self.play(GrowArrow(w_a), FadeIn(w_a_label), GrowArrow(w_b), FadeIn(w_b_label), run_time=0.70)
        self.play(FadeIn(emb, scale=1.25), FadeIn(emb_label), ShowCreation(theta_arc), FadeIn(theta_label), run_time=0.60)
        self.play(ShowCreation(boundary), FadeIn(boundary_label), run_time=0.55)
        self.play(ShowCreation(margin_arc), FadeIn(margin_label), ShowCreation(strict_boundary), FadeIn(strict_label), run_time=0.75)
        self.play(FadeIn(condition), run_time=0.50)
        self.add(notes)
        self.play(FadeIn(chain), run_time=0.55)
        self.wait(1.00)

    # ------------------------------------------------------------------
    # Beat D - SphereFace milestone.
    # ------------------------------------------------------------------
    def beat_d_sphereface(self):
        title = title_block("2017: SphereFace", "First angular margin loss")

        circle = Circle(radius=2.08, stroke_color=CYAN, stroke_width=1.4, fill_opacity=0)
        circle.move_to(LEFT * 3.20 + UP * 0.30)
        center = circle.get_center()

        w_angle = 35 * DEGREES
        f_angle = 70 * DEGREES
        w_vec = Arrow(center, center + 2.08 * np.array([np.cos(w_angle), np.sin(w_angle), 0]), buff=0, color=CYAN, stroke_width=2.7, max_tip_length_to_length_ratio=0.12)
        f_vec = Arrow(center, center + 2.08 * np.array([np.cos(f_angle), np.sin(f_angle), 0]), buff=0, color=WHITE, stroke_width=2.4, max_tip_length_to_length_ratio=0.12)
        w_label = Tex(r"W_y", font_size=24, color=CYAN).next_to(w_vec.get_end(), RIGHT, buff=0.08)
        f_label = Tex(r"f_i", font_size=24, color=WHITE).next_to(f_vec.get_end(), UP, buff=0.08)

        theta_arc = Arc(radius=0.70, start_angle=w_angle, angle=f_angle - w_angle, stroke_color=WHITE, stroke_width=2.0)
        theta_arc.shift(center)
        theta_label = Tex(r"\theta", font_size=23, color=WHITE)
        theta_label.move_to(center + 0.92 * np.array([np.cos((w_angle + f_angle) / 2), np.sin((w_angle + f_angle) / 2), 0]))
        strict_arc = Arc(radius=1.05, start_angle=w_angle, angle=1.45 * (f_angle - w_angle), stroke_color=YELLOW, stroke_width=2.5)
        strict_arc.shift(center)
        strict_label = Tex(r"m\theta", font_size=23, color=YELLOW)
        strict_label.move_to(center + 1.29 * np.array([np.cos(w_angle + 0.72 * (f_angle - w_angle)), np.sin(w_angle + 0.72 * (f_angle - w_angle)), 0]))

        old_boundary = DashedLine(
            center + 2.32 * np.array([np.cos(88 * DEGREES), np.sin(88 * DEGREES), 0]),
            center - 2.32 * np.array([np.cos(88 * DEGREES), np.sin(88 * DEGREES), 0]),
            stroke_color=MUTED,
            stroke_width=1.5,
            dash_length=0.10,
        )
        new_boundary = DashedLine(
            center + 2.32 * np.array([np.cos(75 * DEGREES), np.sin(75 * DEGREES), 0]),
            center - 2.32 * np.array([np.cos(75 * DEGREES), np.sin(75 * DEGREES), 0]),
            stroke_color=YELLOW,
            stroke_width=2.0,
            dash_length=0.10,
        )

        formula = formula_box(r"\cos(m\theta_y)", color=YELLOW, size=34, width=3.35)
        formula.move_to(RIGHT * 3.15 + UP * 1.45)

        notes = key_points(
            [
                "Applies margin directly on the angle",
                ("Decision boundary becomes stricter", YELLOW),
                ("Embeddings are more discriminative", GREEN),
                ("Optimization can be difficult", RED),
            ],
            color=YELLOW,
            width=5.25,
            size=19,
        )
        notes.move_to(RIGHT * 3.15 + DOWN * 0.20)

        footer = concept_chip("Angular margin enters training", color=CYAN, size=20)
        footer.next_to(notes, DOWN, buff=0.20)

        layout = Group(
            title, circle, w_vec, f_vec, w_label, f_label,
            theta_arc, theta_label, strict_arc, strict_label,
            old_boundary, new_boundary, formula, notes, footer,
        )
        safe_group(layout, center=UP * 0.50)

        self.add(title)
        self.play(ShowCreation(circle), GrowArrow(w_vec), FadeIn(w_label), run_time=0.65)
        self.play(GrowArrow(f_vec), FadeIn(f_label), ShowCreation(theta_arc), FadeIn(theta_label), run_time=0.60)
        self.play(ShowCreation(old_boundary), run_time=0.40)
        self.play(ShowCreation(strict_arc), FadeIn(strict_label), ShowCreation(new_boundary), run_time=0.75)
        self.play(FadeIn(formula), run_time=0.45)
        self.add(notes, footer)
        self.wait(1.00)

    # ------------------------------------------------------------------
    # Beat E - CosFace milestone.
    # ------------------------------------------------------------------
    def beat_e_cosface(self):
        title = title_block("2018: CosFace", "Additive cosine margin")

        axis_panel = make_panel(width=6.15, height=3.60, stroke_color=BLUE, fill_opacity=0.05)
        axis_panel.move_to(LEFT * 2.98 + UP * 0.44)
        axis = Line(axis_panel.get_center() + LEFT * 2.34, axis_panel.get_center() + RIGHT * 2.34, stroke_color=MUTED, stroke_width=1.6)
        tick_left = Line(axis.get_start() + DOWN * 0.10, axis.get_start() + UP * 0.10, stroke_color=MUTED, stroke_width=1.2)
        tick_zero = Line(axis.get_center() + DOWN * 0.10, axis.get_center() + UP * 0.10, stroke_color=MUTED, stroke_width=1.2)
        tick_right = Line(axis.get_end() + DOWN * 0.10, axis.get_end() + UP * 0.10, stroke_color=MUTED, stroke_width=1.2)
        labels = VGroup(
            Tex(r"-1", font_size=18, color=MUTED).next_to(tick_left, DOWN, buff=0.07),
            Tex(r"0", font_size=18, color=MUTED).next_to(tick_zero, DOWN, buff=0.07),
            Tex(r"1", font_size=18, color=MUTED).next_to(tick_right, DOWN, buff=0.07),
        )

        raw_score = axis.get_center() + RIGHT * 1.38
        margin_score = axis.get_center() + RIGHT * 0.70
        raw_dot = Dot(point=raw_score, radius=0.100, color=CYAN)
        margin_dot = Dot(point=margin_score, radius=0.100, color=YELLOW)
        raw_label = Tex(r"\cos\theta_y", font_size=25, color=CYAN).next_to(raw_dot, UP, buff=0.15)
        margin_label = Tex(r"\cos\theta_y-m", font_size=25, color=YELLOW).next_to(margin_dot, DOWN, buff=0.18)
        subtract_arrow = make_flow_arrow(raw_score + UP * 0.04, margin_score + UP * 0.04, color=YELLOW, stroke_width=2.2)
        m_label = Tex(r"m", font_size=24, color=YELLOW).next_to(subtract_arrow, UP, buff=0.05)

        higher_text = text_mob("true-class score is reduced", size=20, color=WHITE)
        higher_text.move_to(axis_panel.get_center() + UP * 1.12)
        stable_text = text_mob("network must recover the margin", size=19, color=GREEN)
        stable_text.move_to(axis_panel.get_center() + DOWN * 1.16)

        formula = formula_box(r"\cos\theta_y-m", color=BLUE, size=35, width=3.50)
        formula.move_to(RIGHT * 3.28 + UP * 1.42)

        notes = key_points(
            [
                "Adds margin in cosine similarity",
                ("Simpler than angular multiplication", BLUE),
                ("Training becomes more stable", GREEN),
                ("Margin is not a fixed arc length", YELLOW),
            ],
            color=BLUE,
            width=5.05,
            size=19,
        )
        notes.move_to(RIGHT * 3.28 + DOWN * 0.16)

        bridge = arrow_chain(["angle idea", "cosine margin", "stable objective"], color=BLUE, size=18)
        bridge.next_to(notes, DOWN, buff=0.20)

        layout = Group(
            title, axis_panel, axis, tick_left, tick_zero, tick_right, labels,
            raw_dot, margin_dot, raw_label, margin_label, subtract_arrow, m_label,
            higher_text, stable_text, formula, notes, bridge,
        )
        safe_group(layout, center=UP * 0.50)

        self.add(title)
        self.play(FadeIn(axis_panel), ShowCreation(axis), FadeIn(tick_left), FadeIn(tick_zero), FadeIn(tick_right), FadeIn(labels), run_time=0.70)
        self.play(FadeIn(raw_dot, scale=1.25), FadeIn(raw_label), FadeIn(higher_text), run_time=0.50)
        self.play(GrowArrow(subtract_arrow), FadeIn(m_label), FadeIn(margin_dot, scale=1.25), FadeIn(margin_label), run_time=0.75)
        self.add(stable_text, formula, notes)
        self.play(FadeIn(bridge), run_time=0.45)
        self.wait(1.00)

    # ------------------------------------------------------------------
    # Beat F - ArcFace milestone.
    # ------------------------------------------------------------------
    def beat_f_arcface(self):
        title = title_block("2018: ArcFace", "Additive angular margin")

        sphere = Circle(radius=2.23, stroke_color=CYAN, stroke_width=1.6, fill_opacity=0)
        sphere.move_to(LEFT * 3.18 + UP * 0.32)
        center = sphere.get_center()

        w_angle = 20 * DEGREES
        theta = 42 * DEGREES
        margin = 19 * DEGREES
        w_end = center + 2.23 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
        f_end = center + 2.23 * np.array([np.cos(w_angle + theta), np.sin(w_angle + theta), 0])
        m_end = center + 2.23 * np.array([np.cos(w_angle + theta + margin), np.sin(w_angle + theta + margin), 0])

        w_vec = Arrow(center, w_end, buff=0, color=CYAN, stroke_width=2.7, max_tip_length_to_length_ratio=0.12)
        f_vec = Arrow(center, f_end, buff=0, color=WHITE, stroke_width=2.5, max_tip_length_to_length_ratio=0.12)
        margin_vec = Line(center, m_end, stroke_color=YELLOW, stroke_width=1.6, stroke_opacity=0.75)
        w_label = Tex(r"W_y", font_size=24, color=CYAN).next_to(w_end, RIGHT, buff=0.08)
        f_label = Tex(r"f_i", font_size=24, color=WHITE).next_to(f_end, UP, buff=0.08)

        theta_arc = Arc(radius=0.74, start_angle=w_angle, angle=theta, stroke_color=WHITE, stroke_width=2.0)
        theta_arc.shift(center)
        theta_label = Tex(r"\theta", font_size=23, color=WHITE)
        theta_label.move_to(center + 0.96 * np.array([np.cos(w_angle + theta / 2), np.sin(w_angle + theta / 2), 0]))
        margin_arc = Arc(radius=1.08, start_angle=w_angle + theta, angle=margin, stroke_color=YELLOW, stroke_width=2.6)
        margin_arc.shift(center)
        m_label = Tex(r"m", font_size=23, color=YELLOW)
        m_label.move_to(center + 1.30 * np.array([np.cos(w_angle + theta + margin / 2), np.sin(w_angle + theta + margin / 2), 0]))

        arc_gap = Arc(radius=2.23, start_angle=w_angle + theta, angle=margin, stroke_color=YELLOW, stroke_width=4.0)
        arc_gap.shift(center)
        gap_label = text_mob("fixed angular gap", size=18, color=YELLOW)
        gap_label.next_to(arc_gap, UP, buff=0.10)

        formula = formula_box(r"\cos(\theta_y+m)", color=YELLOW, size=35, width=3.78)
        formula.move_to(RIGHT * 3.20 + UP * 1.46)

        notes = key_points(
            [
                "Adds a fixed angle on the hypersphere",
                ("Margin has clear geometric meaning", YELLOW),
                ("Boundary is easier to interpret", CYAN),
                ("Embedding space becomes more discriminative", GREEN),
            ],
            color=YELLOW,
            width=5.25,
            size=19,
        )
        notes.move_to(RIGHT * 3.20 + DOWN * 0.12)

        influence = concept_chip("simple geometry, strong separation", color=GREEN, size=20)
        influence.next_to(notes, DOWN, buff=0.20)

        layout = Group(
            title, sphere, w_vec, f_vec, margin_vec, w_label, f_label,
            theta_arc, theta_label, margin_arc, m_label, arc_gap, gap_label,
            formula, notes, influence,
        )
        safe_group(layout, center=UP * 0.50)

        self.add(title)
        self.play(ShowCreation(sphere), GrowArrow(w_vec), FadeIn(w_label), run_time=0.65)
        self.play(GrowArrow(f_vec), FadeIn(f_label), ShowCreation(theta_arc), FadeIn(theta_label), run_time=0.65)
        self.play(ShowCreation(margin_arc), FadeIn(m_label), ShowCreation(margin_vec), ShowCreation(arc_gap), FadeIn(gap_label), run_time=0.80)
        self.play(FadeIn(formula), run_time=0.45)
        self.add(notes, influence)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat G - Transition to the next scene.
    # ------------------------------------------------------------------
    def beat_g_transition(self):
        title = title_block("The Common Conclusion", "Face recognition is geometry")

        specs = [
            ("2015", "FaceNet", "Triplet loss", GREEN),
            ("2017", "SphereFace", "Angular margin", CYAN),
            ("2018", "CosFace", "Cosine margin", BLUE),
            ("2018", "ArcFace", "Angular arc", ORANGE),
        ]
        nodes = VGroup(*[timeline_node(year, name, detail, color=color) for year, name, detail, color in specs])
        nodes.arrange(RIGHT, buff=0.60)
        nodes.move_to(UP * 1.54)

        arrows = VGroup()
        for left_node, right_node in zip(nodes[:-1], nodes[1:]):
            arrows.add(make_flow_arrow(
                left_node.get_right() + RIGHT * 0.05,
                right_node.get_left() + LEFT * 0.05,
                color=MUTED,
                stroke_width=1.9,
            ))

        conclusion = key_points(
            [
                "Correct classification is not enough",
                ("Embedding space must be organized", CYAN),
                ("Decision boundary needs a margin", YELLOW),
                ("ArcFace gives distance a clear angular meaning", ORANGE),
            ],
            color=WHITE,
            width=8.25,
            size=21,
        )
        conclusion.move_to(UP * -0.20)

        next_terms = VGroup(
            formula_box(r"\Vert f\Vert=1", color=CYAN, size=29, width=2.18),
            Arrow(LEFT * 0.38, RIGHT * 0.38, buff=0.04, color=CYAN, stroke_width=2.0, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\Vert W\Vert=1", color=GREEN, size=29, width=2.28),
            Arrow(LEFT * 0.38, RIGHT * 0.38, buff=0.04, color=CYAN, stroke_width=2.0, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\cos(\theta+m)", color=YELLOW, size=29, width=2.72),
        ).arrange(RIGHT, buff=0.15)
        next_label = text_mob("Next: ArcFace Mechanism", size=28, color=CYAN, bold=True)
        next_group = VGroup(next_label, next_terms).arrange(DOWN, buff=0.16)
        next_group.move_to(DOWN * 2.05)

        layout = Group(title, nodes, arrows, conclusion, next_group)
        safe_group(layout, max_width=12.95, max_height=5.72, center=UP * 0.46)

        self.add(title)
        self.play(FadeIn(nodes[0]), run_time=0.35)
        for arrow, node in zip(arrows, nodes[1:]):
            self.play(GrowArrow(arrow), FadeIn(node), run_time=0.40)
        self.add(conclusion)
        self.play(FadeIn(next_group), run_time=0.60)
        self.wait(1.10)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.30)

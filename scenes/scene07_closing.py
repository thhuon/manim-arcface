from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 07 - Closing
# Narration-aligned recap:
# - Modern face recognition learns a representation space, not a name list
# - Pixels become embeddings, and recognition becomes geometry
# - ArcFace changes the definition of a good embedding through angular margin
# - The opening question is answered through stable identity features
# =============================================================================


SAFE_BOTTOM = -FRAME_HEIGHT / 2 + SUBTITLE_HEIGHT + FRAME_MARGIN
CONTENT_BOTTOM = SAFE_BOTTOM + 0.08
CONTENT_TOP = FRAME_HEIGHT / 2 - FRAME_MARGIN
TITLE_Y = 3.43


def text_mob(text, size=24, color=WHITE, bold=False):
    command = r"\textbf" if bold else r"\text"
    return latex(rf"{command}{{{tex_text(text)}}}", size=size, color=color)


def title_block(title, subtitle=None, title_size=40, subtitle_size=20):
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


def formula_box(formula, color=CYAN, size=28, width=None, height=None):
    formula_mob = Tex(formula, font_size=size, color=color)
    if width is not None:
        fit_to_bounds(formula_mob, max_width=width - 0.36)
    if height is not None:
        fit_to_bounds(formula_mob, max_height=height - 0.28)
    box = RoundedRectangle(
        width=max(formula_mob.get_width() + 0.48, 1.26) if width is None else width,
        height=max(formula_mob.get_height() + 0.34, 0.68) if height is None else height,
        corner_radius=0.10,
        stroke_color=color,
        stroke_width=1.4,
        fill_color=PANEL,
        fill_opacity=0.30,
    )
    formula_mob.move_to(box)
    return VGroup(box, formula_mob)


def key_points(lines, color=CYAN, width=5.0, size=18):
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
    fit_to_bounds(rows, max_width=width)
    return rows


def safe_group(group, max_width=12.85, max_height=5.52, center=ORIGIN + UP * 0.48):
    fit_to_bounds(group, max_width=max_width, max_height=max_height)
    group.move_to(center)
    if group.get_top()[1] > CONTENT_TOP:
        group.shift(DOWN * (group.get_top()[1] - CONTENT_TOP))
    if group.get_bottom()[1] < CONTENT_BOTTOM:
        group.shift(UP * (CONTENT_BOTTOM - group.get_bottom()[1]))
    return group


def point_at(center, radius, angle):
    return center + radius * np.array([np.cos(angle), np.sin(angle), 0])


def unit_circle(center=ORIGIN, radius=1.7, color=CYAN):
    circle = Circle(radius=radius, stroke_color=color, stroke_width=1.5, fill_opacity=0)
    circle.move_to(center)
    return circle


def radial_arrow(center, radius, angle, color=CYAN, stroke_width=2.2):
    return Arrow(
        center,
        point_at(center, radius, angle),
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.12,
    )


def angle_arc(center, radius, start, end, color=WHITE, stroke_width=2.0):
    arc = Arc(
        radius=radius,
        start_angle=start,
        angle=end - start,
        stroke_color=color,
        stroke_width=stroke_width,
    )
    arc.shift(center)
    return arc


def cluster_on_circle(center, radius, base_angle, color, count=7, spread=0.10, seed=1, dot_radius=0.065):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        angle = base_angle + rng.normal(0, spread)
        radial_jitter = rng.normal(0, 0.020)
        dots.add(Dot(point=point_at(center, radius + radial_jitter, angle), radius=dot_radius, color=color))
    return dots


def free_cloud(center, color, count=8, spread=0.28, seed=1, radius=0.060):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        offset = rng.normal(0, spread, size=2)
        dots.add(Dot(point=center + np.array([offset[0], offset[1], 0]), color=color, radius=radius))
    return dots


def ring_around(mob, color, buff=0.20):
    ring = Ellipse(
        width=mob.get_width() + buff,
        height=mob.get_height() + buff * 0.82,
        stroke_color=color,
        stroke_width=1.5,
        fill_opacity=0,
    )
    ring.move_to(mob)
    return ring


def strike_through(mob, color=RED):
    return Line(
        mob.get_left() + 0.10 * RIGHT + 0.16 * DOWN,
        mob.get_right() + 0.10 * LEFT + 0.16 * UP,
        stroke_color=color,
        stroke_width=3.0,
    )


class Scene07_Closing(Scene):
    def construct(self):
        self.camera.background_color = DARK

        card = make_centered_title_card(
            "Closing",
            "Face recognition as learned geometry",
            title_size=52,
            subtitle_size=24,
        )
        self.play(FadeIn(card), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.45)

        self.beat_a_what_is_learned()
        self.clear_and_wait()
        self.beat_b_identity_geometry()
        self.clear_and_wait()
        self.beat_c_arcface_contribution()
        self.clear_and_wait()
        self.beat_d_answer_opening_question()
        self.clear_and_wait()
        self.beat_e_final_lesson()

    # ------------------------------------------------------------------
    # Beat A - Face recognition learns organization, not a name list.
    # ------------------------------------------------------------------
    def beat_a_what_is_learned(self):
        title = title_block(
            "What Does the Network Learn?",
            "Not a face list, but a representation space",
            title_size=39,
            subtitle_size=20,
        )

        face = make_image_card(
            "face_1.png",
            width=1.18,
            height=1.36,
            label="face image",
            label_color=WHITE,
            stroke_color=CYAN,
            label_size=15,
        )

        pixels = make_pixel_matrix_from_image("face_1.png", n=8, side=1.12)
        pixel_chip = concept_chip("pixels", color=YELLOW, size=17)
        pixel_group = VGroup(pixels, pixel_chip).arrange(DOWN, buff=0.14)

        nn = make_neural_network()
        fit_to_bounds(nn, max_width=1.78, max_height=1.12)
        net_chip = concept_chip("neural network", color=CYAN, size=17)
        net_group = VGroup(nn, net_chip).arrange(DOWN, buff=0.16)

        embedding = formula_box(r"f\in\mathbb{R}^{d}", color=GREEN, size=27, width=1.88, height=0.78)
        emb_chip = concept_chip("embedding", color=GREEN, size=17)
        emb_group = VGroup(embedding, emb_chip).arrange(DOWN, buff=0.15)

        geo_center = ORIGIN
        sphere = unit_circle(geo_center, radius=0.72, color=CYAN)
        geo_dots = VGroup(
            cluster_on_circle(geo_center, 0.72, 35 * DEGREES, CYAN, count=4, spread=0.07, seed=11, dot_radius=0.040),
            cluster_on_circle(geo_center, 0.72, 150 * DEGREES, GREEN, count=4, spread=0.07, seed=12, dot_radius=0.040),
            cluster_on_circle(geo_center, 0.72, 270 * DEGREES, YELLOW, count=4, spread=0.07, seed=13, dot_radius=0.040),
        )
        geometry = VGroup(sphere, geo_dots)
        geo_chip = concept_chip("geometry", color=ORANGE, size=17)
        geo_group = VGroup(geometry, geo_chip).arrange(DOWN, buff=0.15)

        flow_items = Group(face, pixel_group, net_group, emb_group, geo_group)
        flow_items.arrange(RIGHT, buff=0.48)
        flow_items.move_to(UP * 0.92)

        arrows = VGroup()
        for left, right in zip(flow_items[:-1], flow_items[1:]):
            arrows.add(make_flow_arrow(
                left.get_right() + RIGHT * 0.08,
                right.get_left() + LEFT * 0.08,
                color=CYAN,
                stroke_width=2.1,
            ))

        memory_panel = make_panel(width=4.20, height=1.58, stroke_color=RED, fill_opacity=0.05)
        memory_panel.move_to(LEFT * 3.65 + DOWN * 1.28)
        memory_title = concept_chip("not memorization", color=RED, size=18)
        memory_title.next_to(memory_panel, UP, buff=0.10)
        name_box = formula_box(r"\text{name list}", color=RED, size=24, width=1.86, height=0.72)
        image_box = formula_box(r"\text{image archive}", color=RED, size=24, width=2.08, height=0.72)
        name_box.move_to(memory_panel.get_center() + LEFT * 1.05)
        image_box.move_to(memory_panel.get_center() + RIGHT * 1.05)
        strikes = VGroup(strike_through(name_box), strike_through(image_box))

        learned_panel = make_panel(width=4.85, height=1.58, stroke_color=GREEN, fill_opacity=0.05)
        learned_panel.move_to(RIGHT * 3.38 + DOWN * 1.28)
        learned_title = concept_chip("learned structure", color=GREEN, size=18)
        learned_title.next_to(learned_panel, UP, buff=0.10)
        learned_notes = key_points(
            [
                "organize embeddings",
                ("preserve identity features", CYAN),
                ("make geometry meaningful", GREEN),
            ],
            color=GREEN,
            width=4.15,
            size=17,
        )
        learned_notes.move_to(learned_panel)

        bridge = make_flow_arrow(
            memory_panel.get_right() + RIGHT * 0.10,
            learned_panel.get_left() + LEFT * 0.10,
            color=GREEN,
            stroke_width=2.0,
        )

        layout = Group(
            title, flow_items, arrows,
            memory_panel, memory_title, name_box, image_box, strikes,
            learned_panel, learned_title, learned_notes, bridge,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(face), run_time=0.45)
        for arrow, item in zip(arrows, flow_items[1:]):
            self.play(GrowArrow(arrow), FadeIn(item), run_time=0.48)
        self.play(FadeIn(memory_panel), FadeIn(memory_title), FadeIn(name_box), FadeIn(image_box), run_time=0.55)
        self.play(ShowCreation(strikes), run_time=0.35)
        self.play(GrowArrow(bridge), FadeIn(learned_panel), FadeIn(learned_title), run_time=0.50)
        self.add(learned_notes)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat B - Identity is represented by relative position.
    # ------------------------------------------------------------------
    def beat_b_identity_geometry(self):
        title = title_block(
            "Identity Becomes Geometry",
            "Same identities are close; different identities are separated",
            title_size=40,
            subtitle_size=20,
        )

        center = LEFT * 3.05 + UP * 0.38
        radius = 2.02
        sphere = unit_circle(center, radius=radius, color=CYAN)
        faint_inner = Circle(radius=radius * 0.64, stroke_color=MUTED, stroke_width=0.8, stroke_opacity=0.20, fill_opacity=0)
        faint_inner.move_to(center)

        cluster_a = cluster_on_circle(center, radius, 34 * DEGREES, CYAN, count=8, spread=0.075, seed=21)
        cluster_b = cluster_on_circle(center, radius, 142 * DEGREES, GREEN, count=8, spread=0.075, seed=22)
        cluster_c = cluster_on_circle(center, radius, 258 * DEGREES, YELLOW, count=8, spread=0.075, seed=23)
        rings = VGroup(
            ring_around(cluster_a, CYAN, buff=0.16),
            ring_around(cluster_b, GREEN, buff=0.16),
            ring_around(cluster_c, YELLOW, buff=0.16),
        )

        label_a = Tex(r"\mathcal{I}_1", font_size=24, color=CYAN).next_to(cluster_a, RIGHT, buff=0.08)
        label_b = Tex(r"\mathcal{I}_2", font_size=24, color=GREEN).next_to(cluster_b, UP, buff=0.08)
        label_c = Tex(r"\mathcal{I}_3", font_size=24, color=YELLOW).next_to(cluster_c, DOWN, buff=0.08)

        same = make_double_arrow(
            cluster_a[0].get_center(),
            cluster_a[3].get_center(),
            color=GREEN,
            stroke_width=1.5,
        )
        same_label = Tex(r"d_{\mathrm{same}}\ \text{small}", font_size=23, color=GREEN)
        same_label.move_to(center + RIGHT * 1.55 + UP * 0.80)

        diff_arc = Arc(radius=radius, start_angle=34 * DEGREES, angle=108 * DEGREES, stroke_color=YELLOW, stroke_width=4.0)
        diff_arc.shift(center)
        diff_label = Tex(r"d_{\mathrm{diff}}\ \text{large}", font_size=23, color=YELLOW)
        diff_label.move_to(center + UP * 2.42 + RIGHT * 0.10)

        formulas = VGroup(
            formula_box(r"d(f_i,f_j)\ \text{small}", color=GREEN, size=25, width=3.30),
            formula_box(r"d(f_i,f_k)\ \text{large}", color=YELLOW, size=25, width=3.36),
            formula_box(r"\text{identity}\equiv\text{relative position}", color=ORANGE, size=24, width=4.80),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        formulas.move_to(RIGHT * 3.35 + UP * 0.78)

        notes = key_points(
            [
                "Names are not the final representation",
                ("Position carries identity information", ORANGE),
                ("Good geometry supports unseen identities", CYAN),
            ],
            color=WHITE,
            width=5.05,
            size=18,
        )
        notes.next_to(formulas, DOWN, buff=0.32)
        notes.align_to(formulas, LEFT)

        layout = Group(
            title, sphere, faint_inner, cluster_a, cluster_b, cluster_c, rings,
            label_a, label_b, label_c, same, same_label, diff_arc, diff_label, formulas, notes,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(ShowCreation(sphere), ShowCreation(faint_inner), run_time=0.55)
        self.play(FadeIn(cluster_a), FadeIn(cluster_b), FadeIn(cluster_c), run_time=0.65)
        self.play(ShowCreation(rings), FadeIn(label_a), FadeIn(label_b), FadeIn(label_c), run_time=0.50)
        self.play(GrowArrow(same[0]), GrowArrow(same[1]), FadeIn(same_label), run_time=0.45)
        self.play(ShowCreation(diff_arc), FadeIn(diff_label), run_time=0.55)
        self.play(FadeIn(formulas), run_time=0.65)
        self.add(notes)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat C - ArcFace changes the objective, not the architecture.
    # ------------------------------------------------------------------
    def beat_c_arcface_contribution(self):
        title = title_block(
            "What ArcFace Actually Changes",
            "The definition of a good embedding becomes stricter",
            title_size=39,
            subtitle_size=20,
        )

        left_panel = make_panel(width=4.30, height=3.38, stroke_color=MUTED, fill_opacity=0.05)
        right_panel = make_panel(width=6.70, height=3.38, stroke_color=ORANGE, fill_opacity=0.05)
        left_panel.move_to(LEFT * 3.88 + UP * 0.36)
        right_panel.move_to(RIGHT * 2.10 + UP * 0.36)

        left_chip = concept_chip("same backbone", color=CYAN, size=19)
        right_chip = concept_chip("better objective", color=ORANGE, size=19)
        left_chip.next_to(left_panel, UP, buff=0.12)
        right_chip.next_to(right_panel, UP, buff=0.12)

        nn = make_neural_network()
        fit_to_bounds(nn, max_width=2.08, max_height=1.35)
        nn.move_to(left_panel.get_center() + UP * 0.44)
        no_new_net = formula_box(r"\text{new network}", color=RED, size=23, width=2.50, height=0.72)
        no_new_net.move_to(left_panel.get_center() + DOWN * 0.88)
        no_new_strike = strike_through(no_new_net, color=RED)
        backbone_note = text_mob("architecture is not the key change", size=17, color=MUTED)
        backbone_note.next_to(no_new_net, DOWN, buff=0.10)

        specs = [
            ("1", "Normalize", r"\Vert f\Vert=\Vert W\Vert=1", CYAN),
            ("2", "Hypersphere", r"d_{\mathrm{arc}}\propto\theta", GREEN),
            ("3", "Angular margin", r"\cos(\theta_y+m)", YELLOW),
        ]
        cards = VGroup()
        for index, name, formula, color in specs:
            panel = make_panel(width=1.92, height=1.86, stroke_color=color, fill_opacity=0.08)
            number = Circle(radius=0.18, stroke_color=color, stroke_width=1.5, fill_color=PANEL, fill_opacity=0.88)
            number_label = Tex(index, font_size=18, color=color).move_to(number)
            number_group = VGroup(number, number_label)
            number_group.move_to(panel.get_corner(UL) + RIGHT * 0.31 + DOWN * 0.30)
            name_mob = text_mob(name, size=18, color=WHITE, bold=True)
            formula_mob = Tex(formula, font_size=22, color=color)
            body = VGroup(name_mob, formula_mob).arrange(DOWN, buff=0.12)
            fit_to_bounds(body, max_width=panel.get_width() - 0.34, max_height=panel.get_height() - 0.42)
            body.move_to(panel.get_center() + DOWN * 0.04)
            cards.add(VGroup(panel, number_group, body))
        cards.arrange(RIGHT, buff=0.30)
        cards.move_to(right_panel.get_center() + UP * 0.46)

        card_arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            card_arrows.add(make_flow_arrow(
                left.get_right() + RIGHT * 0.05,
                right.get_left() + LEFT * 0.05,
                color=MUTED,
                stroke_width=1.7,
            ))

        result = VGroup(
            formula_box(r"\text{compact same identity}", color=GREEN, size=23, width=3.32),
            Tex(r"+", font_size=27, color=MUTED),
            formula_box(r"\text{separated identities}", color=YELLOW, size=23, width=3.14),
        ).arrange(RIGHT, buff=0.14)
        fit_to_bounds(result, max_width=right_panel.get_width() - 0.52)
        result.move_to(right_panel.get_center() + DOWN * 1.10)

        main_arrow = make_flow_arrow(
            left_panel.get_right() + RIGHT * 0.13,
            right_panel.get_left() + LEFT * 0.13,
            color=ORANGE,
            stroke_width=2.2,
        )

        bottom = key_points(
            [
                "ArcFace asks for more than correct classification",
                ("The embedding space must reflect identity differences", ORANGE),
                ("A small margin changes the geometry of learning", GREEN),
            ],
            color=WHITE,
            width=8.20,
            size=18,
        )
        bottom.move_to(DOWN * 1.82)

        layout = Group(
            title,
            left_panel, right_panel, left_chip, right_chip,
            nn, no_new_net, no_new_strike, backbone_note,
            cards, card_arrows, result, main_arrow, bottom,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(left_panel), FadeIn(left_chip), ShowCreation(nn), run_time=0.60)
        self.play(FadeIn(no_new_net), ShowCreation(no_new_strike), FadeIn(backbone_note), run_time=0.55)
        self.play(GrowArrow(main_arrow), FadeIn(right_panel), FadeIn(right_chip), run_time=0.55)
        self.play(FadeIn(cards[0]), run_time=0.35)
        for arrow, card in zip(card_arrows, cards[1:]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=0.40)
        self.play(FadeIn(result), run_time=0.55)
        self.add(bottom)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat D - Answer the opening question.
    # ------------------------------------------------------------------
    def beat_d_answer_opening_question(self):
        title = title_block(
            "Back to the Opening Question",
            "Why can different photos still map to the same identity?",
            title_size=38,
            subtitle_size=20,
        )

        same_faces = Group(
            make_image_card("person1_1.png", width=1.05, height=1.26, label="light", stroke_color=CYAN, label_size=14),
            make_image_card("person1_2.png", width=1.05, height=1.26, label="pose", stroke_color=CYAN, label_size=14),
            make_image_card("person1_3.png", width=1.05, height=1.26, label="expression", stroke_color=CYAN, label_size=14),
        ).arrange(DOWN, buff=0.17)
        same_faces.move_to(LEFT * 5.45 + UP * 0.48)

        different_face = make_image_card(
            "person2_1.png",
            width=1.05,
            height=1.26,
            label="different",
            stroke_color=YELLOW,
            label_size=14,
        )
        different_face.move_to(LEFT * 5.45 + DOWN * 1.82)

        nn = make_neural_network()
        fit_to_bounds(nn, max_width=1.90, max_height=1.24)
        nn.move_to(LEFT * 3.08 + UP * 0.02)
        net_chip = concept_chip("feature extractor", color=CYAN, size=17)
        net_chip.next_to(nn, DOWN, buff=0.16)

        arrows_to_net = VGroup(
            make_flow_arrow(same_faces.get_right() + RIGHT * 0.10, nn.get_left() + LEFT * 0.10 + UP * 0.40, color=CYAN, stroke_width=1.8),
            make_flow_arrow(different_face.get_right() + RIGHT * 0.10, nn.get_left() + LEFT * 0.10 + DOWN * 0.56, color=YELLOW, stroke_width=1.8),
        )

        center = RIGHT * 0.45 + UP * 0.24
        radius = 1.88
        sphere = unit_circle(center, radius=radius, color=CYAN)
        same_cluster = cluster_on_circle(center, radius, 52 * DEGREES, CYAN, count=7, spread=0.050, seed=41, dot_radius=0.072)
        diff_cluster = cluster_on_circle(center, radius, 220 * DEGREES, YELLOW, count=6, spread=0.060, seed=42, dot_radius=0.070)
        same_ring = ring_around(same_cluster, CYAN, buff=0.18)
        diff_ring = ring_around(diff_cluster, YELLOW, buff=0.18)
        same_label = Tex(r"\text{same identity}", font_size=22, color=CYAN).next_to(same_cluster, RIGHT, buff=0.10)
        diff_label = Tex(r"\text{different identity}", font_size=22, color=YELLOW).next_to(diff_cluster, LEFT, buff=0.10)

        to_space = make_flow_arrow(
            nn.get_right() + RIGHT * 0.12,
            sphere.get_left() + LEFT * 0.12,
            color=GREEN,
            stroke_width=2.0,
        )

        pixel_panel = make_panel(width=3.72, height=1.20, stroke_color=RED, fill_opacity=0.05)
        embed_panel = make_panel(width=3.72, height=1.20, stroke_color=GREEN, fill_opacity=0.05)
        pixel_panel.move_to(RIGHT * 4.75 + UP * 0.85)
        embed_panel.move_to(RIGHT * 4.75 + DOWN * 0.72)
        pixel_formula = Tex(r"d_{\mathrm{pixel}}\ \text{large}", font_size=25, color=RED).move_to(pixel_panel)
        embed_formula = Tex(r"d_{\mathrm{embed}}\ \text{small}", font_size=25, color=GREEN).move_to(embed_panel)
        compare_arrow = make_flow_arrow(
            pixel_panel.get_bottom() + DOWN * 0.08,
            embed_panel.get_top() + UP * 0.08,
            color=GREEN,
            stroke_width=2.0,
        )
        compare_label = text_mob("compare stable features", size=17, color=WHITE)
        compare_label.next_to(compare_arrow, RIGHT, buff=0.10)

        notes = key_points(
            [
                "The system does not compare raw pixels directly",
                ("Stable identity cues are encoded as embeddings", GREEN),
                ("Good geometry keeps real variations close", CYAN),
            ],
            color=WHITE,
            width=5.72,
            size=17,
        )
        notes.move_to(RIGHT * 2.62 + DOWN * 2.10)

        layout = Group(
            title, same_faces, different_face, nn, net_chip, arrows_to_net,
            sphere, same_cluster, diff_cluster, same_ring, diff_ring, same_label, diff_label, to_space,
            pixel_panel, embed_panel, pixel_formula, embed_formula, compare_arrow, compare_label, notes,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(same_faces), FadeIn(different_face), run_time=0.55)
        self.play(GrowArrow(arrows_to_net[0]), GrowArrow(arrows_to_net[1]), ShowCreation(nn), FadeIn(net_chip), run_time=0.70)
        self.play(GrowArrow(to_space), ShowCreation(sphere), run_time=0.55)
        self.play(FadeIn(same_cluster), FadeIn(diff_cluster), ShowCreation(same_ring), ShowCreation(diff_ring), run_time=0.70)
        self.play(FadeIn(same_label), FadeIn(diff_label), run_time=0.40)
        self.play(FadeIn(pixel_panel), FadeIn(pixel_formula), run_time=0.45)
        self.play(GrowArrow(compare_arrow), FadeIn(compare_label), FadeIn(embed_panel), FadeIn(embed_formula), run_time=0.60)
        self.add(notes)
        self.wait(1.10)

    # ------------------------------------------------------------------
    # Beat E - Final lesson and thank you.
    # ------------------------------------------------------------------
    def beat_e_final_lesson(self):
        title = title_block(
            "The Core Lesson",
            "Face recognition is machine learning, geometry, and optimization",
            title_size=40,
            subtitle_size=20,
        )

        ideas = VGroup(
            concept_chip("machine learning", color=CYAN, size=20),
            concept_chip("geometry", color=GREEN, size=20),
            concept_chip("optimization", color=YELLOW, size=20),
        ).arrange(RIGHT, buff=0.64)
        ideas.move_to(UP * 1.62)

        idea_arrows = VGroup()
        for left, right in zip(ideas[:-1], ideas[1:]):
            idea_arrows.add(make_flow_arrow(
                left.get_right() + RIGHT * 0.08,
                right.get_left() + LEFT * 0.08,
                color=MUTED,
                stroke_width=1.8,
            ))

        formula = VGroup(
            formula_box(r"\cos\theta", color=CYAN, size=31, width=2.12),
            Arrow(LEFT * 0.48, RIGHT * 0.48, buff=0.04, color=ORANGE, stroke_width=2.2, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\cos(\theta+m)", color=ORANGE, size=31, width=2.88),
        ).arrange(RIGHT, buff=0.22)
        formula.move_to(UP * 0.46)
        margin_label = concept_chip("small angular margin", color=ORANGE, size=18)
        margin_label.next_to(formula[1], UP, buff=0.14)

        effect = formula_box(
            r"\text{large change in learned identity geometry}",
            color=GREEN,
            size=26,
            width=6.55,
            height=0.82,
        )
        effect.move_to(DOWN * 0.74)
        effect_arrow = make_flow_arrow(
            formula.get_bottom() + DOWN * 0.10,
            effect.get_top() + UP * 0.10,
            color=GREEN,
            stroke_width=2.0,
        )

        final_flow_items = VGroup(
            concept_chip("pixels", color=YELLOW, size=19),
            concept_chip("embedding space", color=CYAN, size=19),
            concept_chip("identity structure", color=GREEN, size=19),
        ).arrange(RIGHT, buff=0.72)
        final_flow_items.move_to(DOWN * 1.72)

        final_arrows = VGroup()
        for left, right in zip(final_flow_items[:-1], final_flow_items[1:]):
            final_arrows.add(make_flow_arrow(
                left.get_right() + RIGHT * 0.08,
                right.get_left() + LEFT * 0.08,
                color=CYAN,
                stroke_width=2.0,
            ))

        layout = Group(
            title, ideas, idea_arrows, formula, margin_label,
            effect_arrow, effect, final_flow_items, final_arrows,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(ideas[0]), run_time=0.35)
        for arrow, item in zip(idea_arrows, ideas[1:]):
            self.play(GrowArrow(arrow), FadeIn(item), run_time=0.38)
        self.play(FadeIn(formula[0]), run_time=0.35)
        self.play(GrowArrow(formula[1]), FadeIn(margin_label), FadeIn(formula[2]), run_time=0.60)
        self.play(GrowArrow(effect_arrow), FadeIn(effect), run_time=0.55)
        self.play(FadeIn(final_flow_items[0]), run_time=0.30)
        for arrow, item in zip(final_arrows, final_flow_items[1:]):
            self.play(GrowArrow(arrow), FadeIn(item), run_time=0.38)
        self.wait(1.40)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.30)

from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 06 - ArcFace Mechanism
# Narration-aligned rewrite:
# - Normalization removes the norm shortcut
# - Embeddings and class weights live on the unit hypersphere
# - Softmax compares angles, ArcFace adds an angular margin
# - Formula: cos(theta) becomes cos(theta + m), then scaled by s
# - Margin forces theta to shrink and improves open-set recognition
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


def formula_box(formula, color=CYAN, size=30, width=None, height=None):
    formula_mob = Tex(formula, font_size=size, color=color)
    if width is not None:
        fit_to_bounds(formula_mob, max_width=width - 0.38)
    if height is not None:
        fit_to_bounds(formula_mob, max_height=height - 0.28)
    box = RoundedRectangle(
        width=max(formula_mob.get_width() + 0.48, 1.36) if width is None else width,
        height=max(formula_mob.get_height() + 0.34, 0.68) if height is None else height,
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
    fit_to_bounds(rows, max_width=width)
    return rows


def arrow_chain(labels, color=CYAN, size=19, box_color=None):
    group = VGroup()
    for index, label in enumerate(labels):
        if isinstance(label, tuple):
            text, label_color = label
        else:
            text, label_color = label, WHITE
        group.add(concept_chip(text, color=box_color or label_color, size=size))
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


def point_at(center, radius, angle):
    return center + radius * np.array([np.cos(angle), np.sin(angle), 0])


def radial_arrow(center, radius, angle, color=CYAN, stroke_width=2.4):
    return Arrow(
        center,
        point_at(center, radius, angle),
        buff=0,
        color=color,
        stroke_width=stroke_width,
        max_tip_length_to_length_ratio=0.12,
    )


def radial_line(center, radius, angle, color=MUTED, stroke_width=1.6, opacity=0.75):
    line = Line(center, point_at(center, radius, angle), stroke_color=color, stroke_width=stroke_width)
    line.set_stroke(opacity=opacity)
    return line


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


def angle_label(label, center, radius, start, end, color=WHITE, size=23):
    mid = (start + end) / 2
    return Tex(label, font_size=size, color=color).move_to(point_at(center, radius, mid))


def unit_circle(center=ORIGIN, radius=1.75, color=CYAN):
    circle = Circle(radius=radius, stroke_color=color, stroke_width=1.5, fill_opacity=0)
    circle.move_to(center)
    return circle


def cluster_on_circle(center, radius, base_angle, color, count=7, spread=0.11, seed=1, dot_radius=0.065):
    rng = np.random.default_rng(seed)
    dots = VGroup()
    for _ in range(count):
        angle = base_angle + rng.normal(0, spread)
        radial_jitter = rng.normal(0, 0.018)
        dots.add(Dot(point=point_at(center, radius + radial_jitter, angle), radius=dot_radius, color=color))
    return dots


def free_cloud(center, color, count=8, spread=0.36, seed=1, radius=0.060):
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
        stroke_width=1.6,
        fill_opacity=0,
    )
    ring.move_to(mob)
    return ring


class Scene06_ArcFaceMechanism(Scene):
    def construct(self):
        self.camera.background_color = DARK

        card = make_centered_title_card(
            "ArcFace Mechanism",
            "Normalization, hypersphere, angular margin",
            title_size=48,
            subtitle_size=23,
        )
        self.play(FadeIn(card), run_time=0.9)
        self.wait(0.8)
        self.play(FadeOut(card), run_time=0.45)

        self.beat_a_norm_motivation()
        self.clear_and_wait()
        self.beat_b_feature_weight_norm()
        self.clear_and_wait()
        self.beat_c_hypersphere()
        self.clear_and_wait()
        self.beat_d_softmax_vs_arcface()
        self.clear_and_wait()
        self.beat_e_formula()
        self.clear_and_wait()
        self.beat_f_why_it_works()
        self.clear_and_wait()
        self.beat_g_open_set()
        self.clear_and_wait()
        self.beat_h_summary()

    # ------------------------------------------------------------------
    # Beat A - Normalization removes the norm shortcut.
    # ------------------------------------------------------------------
    def beat_a_norm_motivation(self):
        title = title_block(
            "Preparing the Geometry",
            "Why normalization matters",
            title_size=40,
            subtitle_size=20,
        )

        left_panel = make_panel(width=5.55, height=3.50, stroke_color=YELLOW, fill_opacity=0.05)
        right_panel = make_panel(width=5.55, height=3.50, stroke_color=GREEN, fill_opacity=0.05)
        left_panel.move_to(LEFT * 3.05 + UP * 0.55)
        right_panel.move_to(RIGHT * 3.05 + UP * 0.55)

        left_chip = concept_chip("Before normalization", color=YELLOW, size=20)
        right_chip = concept_chip("After normalization", color=GREEN, size=20)
        left_chip.next_to(left_panel, UP, buff=0.13)
        right_chip.next_to(right_panel, UP, buff=0.13)

        left_center = left_panel.get_center() + LEFT * 1.28 + DOWN * 0.35
        axes = VGroup(
            Line(left_center + LEFT * 0.12, left_center + RIGHT * 2.55, stroke_color=MUTED, stroke_width=1.0),
            Line(left_center + DOWN * 0.12, left_center + UP * 2.05, stroke_color=MUTED, stroke_width=1.0),
        )
        w_angle = 33 * DEGREES
        f_angle = 48 * DEGREES
        w_vec = radial_arrow(left_center, 1.38, w_angle, color=CYAN, stroke_width=2.5)
        f_short = radial_arrow(left_center, 1.14, f_angle, color=WHITE, stroke_width=2.1)
        f_long = radial_arrow(left_center, 2.08, f_angle, color=RED, stroke_width=2.6)
        grow_arrow = make_flow_arrow(
            point_at(left_center, 1.22, f_angle) + 0.10 * RIGHT,
            point_at(left_center, 1.92, f_angle) + 0.10 * RIGHT,
            color=RED,
            stroke_width=2.0,
        )
        w_label = Tex(r"W_y", font_size=23, color=CYAN).next_to(w_vec.get_end(), RIGHT, buff=0.06)
        f_label = Tex(r"f_i", font_size=23, color=WHITE).next_to(f_short.get_end(), UP, buff=0.04)
        long_label = Tex(r"\lambda f_i", font_size=23, color=RED).next_to(f_long.get_end(), UP, buff=0.04)
        theta = angle_arc(left_center, 0.58, w_angle, f_angle, color=WHITE, stroke_width=1.8)
        theta_label = angle_label(r"\theta", left_center, 0.78, w_angle, f_angle, color=WHITE, size=22)

        raw_formula = formula_box(
            r"W_y^T f_i=\Vert W_y\Vert\,\Vert f_i\Vert\cos\theta_y",
            color=YELLOW,
            size=25,
            width=4.72,
        )
        raw_formula.move_to(left_panel.get_center() + RIGHT * 0.12 + DOWN * 1.22)
        shortcut = text_mob("norm can become a shortcut", size=18, color=RED)
        shortcut.move_to(left_panel.get_center() + RIGHT * 0.88 + UP * 0.90)

        right_center = right_panel.get_center() + LEFT * 1.30 + DOWN * 0.22
        circle = unit_circle(right_center, radius=1.24, color=GREEN)
        norm_w = radial_arrow(right_center, 1.24, w_angle, color=CYAN, stroke_width=2.5)
        norm_f = radial_arrow(right_center, 1.24, f_angle, color=WHITE, stroke_width=2.5)
        norm_w_label = Tex(r"\hat W_y", font_size=22, color=CYAN).next_to(norm_w.get_end(), RIGHT, buff=0.06)
        norm_f_label = Tex(r"\hat f_i", font_size=22, color=WHITE).next_to(norm_f.get_end(), UP, buff=0.06)
        norm_theta = angle_arc(right_center, 0.58, w_angle, f_angle, color=WHITE, stroke_width=1.8)
        norm_theta_label = angle_label(r"\theta", right_center, 0.78, w_angle, f_angle, color=WHITE, size=22)
        one_label = Tex(r"\Vert \hat f_i\Vert=\Vert \hat W_y\Vert=1", font_size=24, color=GREEN)
        one_label.move_to(right_panel.get_center() + RIGHT * 1.08 + UP * 0.92)
        norm_formula = formula_box(
            r"\hat W_y^T\hat f_i=\cos\theta_y",
            color=GREEN,
            size=27,
            width=3.78,
        )
        norm_formula.move_to(right_panel.get_center() + RIGHT * 0.92 + DOWN * 1.22)

        notes = key_points(
            [
                "ArcFace first removes the magnitude shortcut",
                ("All vectors have the same length", GREEN),
                ("Only the angle carries identity information", CYAN),
            ],
            color=WHITE,
            width=7.50,
            size=20,
        )
        notes.move_to(DOWN * 1.78)

        layout = Group(
            title,
            left_panel, right_panel, left_chip, right_chip,
            axes, w_vec, f_short, f_long, grow_arrow, w_label, f_label, long_label,
            theta, theta_label, raw_formula, shortcut,
            circle, norm_w, norm_f, norm_w_label, norm_f_label,
            norm_theta, norm_theta_label, one_label, norm_formula, notes,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(left_panel), FadeIn(left_chip), ShowCreation(axes), run_time=0.55)
        self.play(GrowArrow(w_vec), FadeIn(w_label), GrowArrow(f_short), FadeIn(f_label), ShowCreation(theta), FadeIn(theta_label), run_time=0.70)
        self.play(GrowArrow(grow_arrow), GrowArrow(f_long), FadeIn(long_label), FadeIn(shortcut), run_time=0.75)
        self.play(FadeIn(raw_formula), run_time=0.45)
        self.play(FadeIn(right_panel), FadeIn(right_chip), ShowCreation(circle), run_time=0.55)
        self.play(
            GrowArrow(norm_w), FadeIn(norm_w_label),
            GrowArrow(norm_f), FadeIn(norm_f_label),
            ShowCreation(norm_theta), FadeIn(norm_theta_label),
            run_time=0.75,
        )
        self.play(FadeIn(one_label), FadeIn(norm_formula), run_time=0.55)
        self.add(notes)
        self.wait(1.00)

    # ------------------------------------------------------------------
    # Beat B - Feature normalization and weight normalization.
    # ------------------------------------------------------------------
    def beat_b_feature_weight_norm(self):
        title = title_block(
            "Feature and Weight Normalization",
            "ArcFace fixes length, not the representation itself",
            title_size=39,
            subtitle_size=20,
        )

        row1_left = formula_box(r"f_i", color=WHITE, size=34, width=1.55)
        row1_right = formula_box(r"\hat f_i=\dfrac{f_i}{\Vert f_i\Vert}", color=CYAN, size=31, width=3.05, height=0.95)
        row1_arrow = Arrow(LEFT * 0.44, RIGHT * 0.44, buff=0.04, color=CYAN, stroke_width=2.3, max_tip_length_to_length_ratio=0.22)
        row1 = VGroup(row1_left, row1_arrow, row1_right).arrange(RIGHT, buff=0.22)

        row2_left = formula_box(r"W_j", color=WHITE, size=34, width=1.55)
        row2_right = formula_box(r"\hat W_j=\dfrac{W_j}{\Vert W_j\Vert}", color=GREEN, size=31, width=3.18, height=0.95)
        row2_arrow = Arrow(LEFT * 0.44, RIGHT * 0.44, buff=0.04, color=GREEN, stroke_width=2.3, max_tip_length_to_length_ratio=0.22)
        row2 = VGroup(row2_left, row2_arrow, row2_right).arrange(RIGHT, buff=0.22)

        rows = VGroup(row1, row2).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        rows.move_to(LEFT * 2.85 + UP * 0.66)

        row1_badge = concept_chip("Feature normalization", color=CYAN, size=19)
        row2_badge = concept_chip("Weight normalization", color=GREEN, size=19)
        row1_badge.next_to(row1, UP, buff=0.12)
        row2_badge.next_to(row2, DOWN, buff=0.12)

        center = RIGHT * 3.05 + UP * 0.48
        circle = unit_circle(center, radius=1.56, color=CYAN)
        raw_vectors = VGroup(
            radial_line(center, 0.90, 22 * DEGREES, color=WHITE, stroke_width=1.3, opacity=0.35),
            radial_line(center, 1.30, 64 * DEGREES, color=GREEN, stroke_width=1.3, opacity=0.35),
            radial_line(center, 2.05, 128 * DEGREES, color=YELLOW, stroke_width=1.3, opacity=0.35),
            radial_line(center, 1.10, 202 * DEGREES, color=BLUE, stroke_width=1.3, opacity=0.35),
        )
        unit_vectors = VGroup(
            radial_arrow(center, 1.56, 22 * DEGREES, color=WHITE, stroke_width=2.2),
            radial_arrow(center, 1.56, 64 * DEGREES, color=GREEN, stroke_width=2.2),
            radial_arrow(center, 1.56, 128 * DEGREES, color=YELLOW, stroke_width=2.2),
            radial_arrow(center, 1.56, 202 * DEGREES, color=BLUE, stroke_width=2.2),
        )
        unit_label = Tex(r"\Vert \hat f_i\Vert=\Vert \hat W_j\Vert=1", font_size=24, color=CYAN)
        unit_label.next_to(circle, DOWN, buff=0.15)

        final_terms = VGroup(
            formula_box(r"\Vert\hat f_i\Vert=1", color=CYAN, size=25, width=2.05),
            Arrow(LEFT * 0.36, RIGHT * 0.36, buff=0.04, color=MUTED, stroke_width=1.8, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\Vert\hat W_j\Vert=1", color=GREEN, size=25, width=2.10),
            Arrow(LEFT * 0.36, RIGHT * 0.36, buff=0.04, color=MUTED, stroke_width=1.8, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\hat W_j^T\hat f_i=\cos\theta_j", color=YELLOW, size=25, width=3.08),
        ).arrange(RIGHT, buff=0.13)
        final_terms.move_to(DOWN * 1.76)

        notes = key_points(
            [
                "Embedding and class weights are still used",
                ("ArcFace only fixes their length", GREEN),
                ("Classification becomes an angular comparison", YELLOW),
            ],
            color=CYAN,
            width=3.05,
            size=15,
        )
        notes.move_to(LEFT * 5.62 + DOWN * 1.18)

        layout = Group(
            title, rows, row1_badge, row2_badge,
            circle, raw_vectors, unit_vectors, unit_label, final_terms, notes,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(row1_left), FadeIn(row2_left), FadeIn(row1_badge), FadeIn(row2_badge), run_time=0.55)
        self.play(GrowArrow(row1_arrow), FadeIn(row1_right), run_time=0.55)
        self.play(GrowArrow(row2_arrow), FadeIn(row2_right), run_time=0.55)
        self.play(ShowCreation(raw_vectors), run_time=0.45)
        self.play(ShowCreation(circle), LaggedStart(*[GrowArrow(v) for v in unit_vectors], lag_ratio=0.08), run_time=0.90)
        self.play(FadeIn(unit_label), FadeIn(final_terms), run_time=0.60)
        self.add(notes)
        self.wait(1.00)

    # ------------------------------------------------------------------
    # Beat C - Hypersphere representation and geodesic distance.
    # ------------------------------------------------------------------
    def beat_c_hypersphere(self):
        title = title_block(
            "Hypersphere Representation",
            "The embedding is described by direction",
            title_size=40,
            subtitle_size=20,
        )

        center = LEFT * 3.12 + UP * 0.36
        radius = 2.10
        sphere = unit_circle(center, radius=radius, color=CYAN)
        inner = Circle(radius=radius * 0.62, stroke_color=MUTED, stroke_width=0.8, stroke_opacity=0.20, fill_opacity=0)
        inner.move_to(center)

        before = VGroup(
            Dot(point=center + LEFT * 0.88 + UP * 0.55, radius=0.055, color=MUTED),
            Dot(point=center + RIGHT * 1.34 + DOWN * 0.50, radius=0.055, color=MUTED),
            Dot(point=center + UP * 1.10 + RIGHT * 0.28, radius=0.055, color=MUTED),
            Dot(point=center + DOWN * 1.34 + LEFT * 0.36, radius=0.055, color=MUTED),
        )
        before_label = text_mob("different radii disappear", size=17, color=MUTED)
        before_label.move_to(center + DOWN * 2.58)

        angles = [24 * DEGREES, 66 * DEGREES, 116 * DEGREES, 202 * DEGREES, 286 * DEGREES]
        colors = [WHITE, GREEN, YELLOW, BLUE, ORANGE]
        vectors = VGroup(*[radial_arrow(center, radius, a, color=c, stroke_width=2.0) for a, c in zip(angles, colors)])
        points = VGroup(*[Dot(point=point_at(center, radius, a), radius=0.080, color=c) for a, c in zip(angles, colors)])
        labels = VGroup(
            Tex(r"f_1", font_size=22, color=WHITE).next_to(points[0], RIGHT, buff=0.06),
            Tex(r"f_2", font_size=22, color=GREEN).next_to(points[1], UP, buff=0.06),
            Tex(r"f_3", font_size=22, color=YELLOW).next_to(points[2], LEFT, buff=0.06),
        )

        arc = Arc(radius=radius, start_angle=angles[0], angle=angles[1] - angles[0], stroke_color=YELLOW, stroke_width=4.0)
        arc.shift(center)
        arc_label = Tex(r"d_{\mathrm{arc}}\propto \theta", font_size=26, color=YELLOW)
        arc_label.move_to(point_at(center, radius + 0.42, (angles[0] + angles[1]) / 2))
        theta_arc = angle_arc(center, 0.72, angles[0], angles[1], color=WHITE, stroke_width=2.0)
        theta_label = angle_label(r"\theta", center, 0.94, angles[0], angles[1], color=WHITE, size=23)
        unit_label = Tex(r"\Vert f_i\Vert=1", font_size=26, color=CYAN)
        unit_label.next_to(sphere, UP, buff=0.13)

        notes = key_points(
            [
                "All embeddings lie on the unit surface",
                ("Position is now a direction", CYAN),
                ("Natural distance is the shortest arc", YELLOW),
                ("Optimizing angle optimizes hypersphere distance", GREEN),
            ],
            color=CYAN,
            width=5.55,
            size=19,
        )
        notes.move_to(RIGHT * 3.20 + UP * 0.52)

        name = VGroup(
            concept_chip("arc", color=YELLOW, size=21),
            Tex(r"+", font_size=28, color=MUTED),
            concept_chip("face", color=CYAN, size=21),
            Tex(r"=", font_size=28, color=MUTED),
            concept_chip("ArcFace", color=ORANGE, size=21),
        ).arrange(RIGHT, buff=0.12)
        name.next_to(notes, DOWN, buff=0.22)

        layout = Group(
            title, sphere, inner, before, before_label, vectors, points, labels,
            arc, arc_label, theta_arc, theta_label, unit_label, notes, name,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(ShowCreation(before), FadeIn(before_label), run_time=0.45)
        self.play(ShowCreation(sphere), ShowCreation(inner), FadeIn(unit_label), run_time=0.60)
        self.play(LaggedStart(*[GrowArrow(v) for v in vectors], lag_ratio=0.07), FadeIn(points), FadeIn(labels), run_time=0.90)
        self.play(ShowCreation(theta_arc), FadeIn(theta_label), ShowCreation(arc), FadeIn(arc_label), run_time=0.70)
        self.add(notes)
        self.play(FadeIn(name), run_time=0.50)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat D - Softmax and ArcFace differ only in the true-class condition.
    # ------------------------------------------------------------------
    def beat_d_softmax_vs_arcface(self):
        title = title_block(
            "Softmax vs ArcFace",
            "The comparison is angular, the condition becomes stricter",
            title_size=40,
            subtitle_size=20,
        )

        left_panel = make_panel(width=5.55, height=4.10, stroke_color=CYAN, fill_opacity=0.05)
        right_panel = make_panel(width=5.55, height=4.10, stroke_color=YELLOW, fill_opacity=0.05)
        left_panel.move_to(LEFT * 3.05 + UP * 0.72)
        right_panel.move_to(RIGHT * 3.05 + UP * 0.72)
        left_chip = concept_chip("Softmax on hypersphere", color=CYAN, size=19)
        right_chip = concept_chip("ArcFace on hypersphere", color=YELLOW, size=19)
        left_chip.next_to(left_panel, UP, buff=0.12)
        right_chip.next_to(right_panel, UP, buff=0.12)

        def make_comparison_panel(panel, arcface=False):
            center = panel.get_center() + DOWN * 0.10
            radius = 1.42
            circle = unit_circle(center, radius=radius, color=CYAN if not arcface else YELLOW)
            w_a_angle = 20 * DEGREES
            w_b_angle = 134 * DEGREES
            f_angle = 64 * DEGREES if not arcface else 50 * DEGREES
            boundary_angle = 77 * DEGREES
            strict_boundary_angle = 64 * DEGREES

            w_a = radial_arrow(center, radius, w_a_angle, color=CYAN, stroke_width=2.4)
            w_b = radial_arrow(center, radius, w_b_angle, color=GREEN, stroke_width=2.4)
            f_vec = radial_arrow(center, radius, f_angle, color=WHITE, stroke_width=2.3)
            w_a_label = Tex(r"W_y", font_size=21, color=CYAN).next_to(w_a.get_end(), RIGHT, buff=0.05)
            w_b_label = Tex(r"W_k", font_size=21, color=GREEN).next_to(w_b.get_end(), LEFT, buff=0.05)
            f_label = Tex(r"f_i", font_size=21, color=WHITE).next_to(f_vec.get_end(), UP, buff=0.04)

            boundary = DashedLine(
                point_at(center, radius + 0.28, boundary_angle),
                point_at(center, radius + 0.28, boundary_angle + PI),
                stroke_color=MUTED if arcface else YELLOW,
                stroke_width=1.5,
                dash_length=0.10,
            )
            theta = angle_arc(center, 0.54, w_a_angle, f_angle, color=WHITE, stroke_width=1.8)
            theta_label = angle_label(r"\theta_y", center, 0.78, w_a_angle, f_angle, color=WHITE, size=21)
            group = VGroup(circle, w_a, w_b, f_vec, w_a_label, w_b_label, f_label, boundary, theta, theta_label)

            if arcface:
                margin = 18 * DEGREES
                margin_arc = angle_arc(center, 0.84, f_angle, f_angle + margin, color=YELLOW, stroke_width=2.4)
                margin_label = angle_label(r"m", center, 1.06, f_angle, f_angle + margin, color=YELLOW, size=22)
                strict_boundary = DashedLine(
                    point_at(center, radius + 0.28, strict_boundary_angle),
                    point_at(center, radius + 0.28, strict_boundary_angle + PI),
                    stroke_color=YELLOW,
                    stroke_width=2.0,
                    dash_length=0.10,
                )
                formula = formula_box(r"\cos(\theta_y+m)", color=YELLOW, size=26, width=3.10)
                formula.move_to(panel.get_center() + DOWN * 1.66)
                label = text_mob("must move closer to the class direction", size=17, color=GREEN)
                label.next_to(formula, UP, buff=0.12)
                group.add(margin_arc, margin_label, strict_boundary, formula, label)
            else:
                formula = formula_box(r"\cos\theta_y", color=CYAN, size=27, width=2.40)
                formula.move_to(panel.get_center() + DOWN * 1.66)
                label = text_mob("correct side is enough", size=17, color=YELLOW)
                label.next_to(formula, UP, buff=0.12)
                group.add(formula, label)
            return group

        soft = make_comparison_panel(left_panel, arcface=False)
        arc = make_comparison_panel(right_panel, arcface=True)

        bottom = key_points(
            [
                "ArcFace keeps the same classifier structure",
                ("It changes only the true-class logit", YELLOW),
                ("The prediction condition becomes harder", GREEN),
            ],
            color=WHITE,
            width=6.70,
            size=17,
        )
        bottom.move_to(DOWN * 1.90)

        layout = Group(title, left_panel, right_panel, left_chip, right_chip, soft, arc, bottom)
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(left_panel), FadeIn(left_chip), ShowCreation(soft[0]), run_time=0.50)
        self.play(LaggedStart(*[GrowArrow(mob) for mob in soft[1:4]], lag_ratio=0.10), FadeIn(VGroup(*soft[4:])), run_time=0.95)
        self.play(FadeIn(right_panel), FadeIn(right_chip), ShowCreation(arc[0]), run_time=0.50)
        self.play(LaggedStart(*[GrowArrow(mob) for mob in arc[1:4]], lag_ratio=0.10), FadeIn(VGroup(*arc[4:])), run_time=1.05)
        self.add(bottom)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat E - Formula and the role of m and s.
    # ------------------------------------------------------------------
    def beat_e_formula(self):
        title = title_block(
            "Understanding the Formula",
            "The true-class score is reduced on purpose",
            title_size=40,
            subtitle_size=20,
        )

        soft_logit = formula_box(r"z_y=s\cos\theta_y", color=CYAN, size=31, width=2.95)
        arc_logit = formula_box(r"z_y=s\cos(\theta_y+m)", color=YELLOW, size=31, width=3.70)
        replace_arrow = Arrow(LEFT * 0.48, RIGHT * 0.48, buff=0.04, color=YELLOW, stroke_width=2.3, max_tip_length_to_length_ratio=0.22)
        replacement = VGroup(soft_logit, replace_arrow, arc_logit).arrange(RIGHT, buff=0.22)
        replacement.move_to(UP * 1.86)

        full_formula = formula_box(
            r"L_i=-\log\dfrac{e^{s\cos(\theta_{y_i}+m)}}{e^{s\cos(\theta_{y_i}+m)}+\sum_{j\ne y_i}e^{s\cos\theta_j}}",
            color=ORANGE,
            size=28,
            width=7.15,
            height=1.18,
        )
        full_formula.move_to(UP * 0.74)

        axis_panel = make_panel(width=6.00, height=2.30, stroke_color=BLUE, fill_opacity=0.05)
        axis_panel.move_to(LEFT * 3.20 + DOWN * 0.96)
        axis_center = axis_panel.get_center() + DOWN * 0.20
        h_axis = Line(axis_center + LEFT * 2.15, axis_center + RIGHT * 2.15, stroke_color=MUTED, stroke_width=1.5)
        v_axis = Line(axis_center + LEFT * 1.85 + DOWN * 0.62, axis_center + LEFT * 1.85 + UP * 0.92, stroke_color=MUTED, stroke_width=1.5)
        theta_x = axis_center + LEFT * 0.24
        theta_m_x = axis_center + RIGHT * 0.84
        raw_score = theta_x + UP * 0.60
        margin_score = theta_m_x + UP * 0.08
        raw_dot = Dot(point=raw_score, radius=0.075, color=CYAN)
        margin_dot = Dot(point=margin_score, radius=0.075, color=YELLOW)
        raw_v = DashedLine(theta_x + DOWN * 0.02, raw_score, stroke_color=CYAN, stroke_width=1.2, dash_length=0.08)
        margin_v = DashedLine(theta_m_x + DOWN * 0.02, margin_score, stroke_color=YELLOW, stroke_width=1.2, dash_length=0.08)
        theta_tick = Line(theta_x + DOWN * 0.09, theta_x + UP * 0.09, stroke_color=CYAN, stroke_width=1.3)
        theta_m_tick = Line(theta_m_x + DOWN * 0.09, theta_m_x + UP * 0.09, stroke_color=YELLOW, stroke_width=1.3)
        theta_txt = Tex(r"\theta", font_size=22, color=CYAN).next_to(theta_tick, DOWN, buff=0.06)
        theta_m_txt = Tex(r"\theta+m", font_size=22, color=YELLOW).next_to(theta_m_tick, DOWN, buff=0.06)
        drop_arrow = make_flow_arrow(raw_score + RIGHT * 0.12, margin_score + LEFT * 0.12, color=YELLOW, stroke_width=2.0)
        drop_label = Tex(r"\cos(\theta+m)<\cos\theta", font_size=24, color=YELLOW)
        drop_label.move_to(axis_panel.get_center() + UP * 0.82)
        score_label = text_mob("larger angle gives lower score", size=17, color=WHITE)
        score_label.move_to(axis_panel.get_center() + DOWN * 0.86)

        notes = key_points(
            [
                "m is the additive angular margin",
                ("theta plus m lowers the true-class score", YELLOW),
                ("s scales cosine values before Softmax", BLUE),
                ("The core idea is still the margin", ORANGE),
            ],
            color=YELLOW,
            width=5.40,
            size=18,
        )
        notes.move_to(RIGHT * 3.18 + DOWN * 0.96)

        layout = Group(
            title, replacement, full_formula,
            axis_panel, h_axis, v_axis, raw_dot, margin_dot, raw_v, margin_v,
            theta_tick, theta_m_tick, theta_txt, theta_m_txt, drop_arrow, drop_label, score_label,
            notes,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(soft_logit), run_time=0.45)
        self.play(GrowArrow(replace_arrow), FadeIn(arc_logit), run_time=0.65)
        self.play(FadeIn(full_formula), run_time=0.65)
        self.play(FadeIn(axis_panel), ShowCreation(h_axis), ShowCreation(v_axis), run_time=0.45)
        self.play(
            FadeIn(raw_dot), ShowCreation(raw_v), FadeIn(theta_tick), FadeIn(theta_txt),
            FadeIn(margin_dot), ShowCreation(margin_v), FadeIn(theta_m_tick), FadeIn(theta_m_txt),
            run_time=0.65,
        )
        self.play(GrowArrow(drop_arrow), FadeIn(drop_label), FadeIn(score_label), run_time=0.55)
        self.add(notes)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat F - The network recovers the lost score by shrinking theta.
    # ------------------------------------------------------------------
    def beat_f_why_it_works(self):
        title = title_block(
            "Why ArcFace Works",
            "With norm fixed, the only path is to reduce the angle",
            title_size=40,
            subtitle_size=20,
        )

        center = LEFT * 3.15 + UP * 0.35
        radius = 1.88
        circle = unit_circle(center, radius=radius, color=GREEN)
        w_angle = 22 * DEGREES
        f_start_angle = 73 * DEGREES
        f_end_angle = 44 * DEGREES
        w_vec = radial_arrow(center, radius, w_angle, color=CYAN, stroke_width=2.5)
        f_start = radial_arrow(center, radius, f_start_angle, color=WHITE, stroke_width=2.3)
        f_end = radial_line(center, radius, f_end_angle, color=GREEN, stroke_width=2.2, opacity=0.85)
        motion_arc = Arc(radius=radius, start_angle=f_start_angle, angle=f_end_angle - f_start_angle, stroke_color=GREEN, stroke_width=4.0)
        motion_arc.shift(center)
        w_label = Tex(r"W_y", font_size=24, color=CYAN).next_to(w_vec.get_end(), RIGHT, buff=0.06)
        f_label = Tex(r"f_i", font_size=24, color=WHITE).next_to(f_start.get_end(), UP, buff=0.06)
        f_new_label = Tex(r"f_i'", font_size=24, color=GREEN).next_to(point_at(center, radius, f_end_angle), UP, buff=0.05)
        theta_old = angle_arc(center, 0.62, w_angle, f_start_angle, color=WHITE, stroke_width=1.8)
        theta_new = angle_arc(center, 0.88, w_angle, f_end_angle, color=GREEN, stroke_width=2.0)
        theta_old_label = angle_label(r"\theta", center, 0.82, w_angle, f_start_angle, color=WHITE, size=22)
        theta_new_label = angle_label(r"\theta'", center, 1.08, w_angle, f_end_angle, color=GREEN, size=22)
        locked = concept_chip("norm is locked", color=GREEN, size=19)
        locked.next_to(circle, DOWN, buff=0.14)

        chain = VGroup(
            formula_box(r"\cos(\theta_y+m)", color=YELLOW, size=26, width=2.92),
            Arrow(LEFT * 0.34, RIGHT * 0.34, buff=0.04, color=YELLOW, stroke_width=2.0, max_tip_length_to_length_ratio=0.22),
            concept_chip("score drops", color=YELLOW, size=18),
            Arrow(LEFT * 0.34, RIGHT * 0.34, buff=0.04, color=GREEN, stroke_width=2.0, max_tip_length_to_length_ratio=0.22),
            formula_box(r"\theta_y\downarrow", color=GREEN, size=27, width=1.70),
        ).arrange(RIGHT, buff=0.14)
        chain.move_to(RIGHT * 3.20 + UP * 1.62)

        before_panel = make_panel(width=2.36, height=2.12, stroke_color=MUTED, fill_opacity=0.05)
        after_panel = make_panel(width=2.36, height=2.12, stroke_color=GREEN, fill_opacity=0.05)
        before_panel.move_to(RIGHT * 1.78 + DOWN * 0.24)
        after_panel.move_to(RIGHT * 4.56 + DOWN * 0.24)
        before_label = text_mob("before", size=18, color=MUTED).next_to(before_panel, UP, buff=0.08)
        after_label = text_mob("after", size=18, color=GREEN).next_to(after_panel, UP, buff=0.08)

        before_a = free_cloud(before_panel.get_center() + LEFT * 0.38 + UP * 0.18, CYAN, count=7, spread=0.22, seed=41)
        before_b = free_cloud(before_panel.get_center() + RIGHT * 0.44 + DOWN * 0.14, YELLOW, count=7, spread=0.22, seed=42)
        after_a = free_cloud(after_panel.get_center() + LEFT * 0.60 + UP * 0.36, CYAN, count=7, spread=0.09, seed=43)
        after_b = free_cloud(after_panel.get_center() + RIGHT * 0.62 + DOWN * 0.38, YELLOW, count=7, spread=0.09, seed=44)
        rings = VGroup(ring_around(after_a, CYAN, buff=0.14), ring_around(after_b, YELLOW, buff=0.14))
        margin = make_double_arrow(
            after_panel.get_center() + LEFT * 0.10 + DOWN * 0.72,
            after_panel.get_center() + RIGHT * 0.42 + DOWN * 0.72,
            color=GREEN,
            stroke_width=1.6,
        )
        margin_label = text_mob("larger gap", size=16, color=GREEN).next_to(margin, DOWN, buff=0.04)
        between_arrow = make_flow_arrow(before_panel.get_right() + RIGHT * 0.12, after_panel.get_left() + LEFT * 0.12, color=GREEN, stroke_width=2.0)

        notes = key_points(
            [
                "The model cannot recover by increasing norm",
                ("It must move embeddings toward the correct class", GREEN),
                ("Same identity becomes compact", CYAN),
                ("Different identities separate more clearly", YELLOW),
            ],
            color=GREEN,
            width=5.05,
            size=16,
        )
        notes.move_to(RIGHT * 3.18 + DOWN * 1.86)

        layout = Group(
            title, circle, w_vec, f_start, f_end, motion_arc, w_label, f_label, f_new_label,
            theta_old, theta_new, theta_old_label, theta_new_label, locked, chain,
            before_panel, after_panel, before_label, after_label, before_a, before_b, after_a, after_b,
            rings, margin, margin_label, between_arrow, notes,
        )
        safe_group(layout, center=UP * 0.52)
        title.shift(LEFT * title.get_center()[0])

        self.add(title)
        self.play(ShowCreation(circle), GrowArrow(w_vec), FadeIn(w_label), run_time=0.55)
        self.play(GrowArrow(f_start), FadeIn(f_label), ShowCreation(theta_old), FadeIn(theta_old_label), FadeIn(locked), run_time=0.70)
        self.play(FadeIn(chain), run_time=0.70)
        self.play(ShowCreation(motion_arc), ShowCreation(f_end), FadeIn(f_new_label), ShowCreation(theta_new), FadeIn(theta_new_label), run_time=0.90)
        self.play(FadeIn(before_panel), FadeIn(before_label), FadeIn(before_a), FadeIn(before_b), run_time=0.55)
        self.play(GrowArrow(between_arrow), FadeIn(after_panel), FadeIn(after_label), FadeIn(after_a), FadeIn(after_b), run_time=0.75)
        self.play(ShowCreation(rings), ShowCreation(margin), FadeIn(margin_label), run_time=0.55)
        self.add(notes)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat G - ArcFace generalizes to unseen identities through geometry.
    # ------------------------------------------------------------------
    def beat_g_open_set(self):
        title = title_block(
            "Connection to Open-Set Recognition",
            "The learned geometry is useful beyond the training identities",
            title_size=38,
            subtitle_size=20,
        )

        face = make_abstract_face()
        face.set_stroke(WHITE, 1.8)
        face.move_to(LEFT * 5.35 + UP * 0.68)
        new_chip = concept_chip("unseen face", color=ORANGE, size=18)
        new_chip.next_to(face, DOWN, buff=0.12)

        nn = make_neural_network()
        fit_to_bounds(nn, max_width=2.15, max_height=1.42)
        nn.move_to(LEFT * 2.85 + UP * 0.68)
        net_chip = concept_chip("embedding network", color=CYAN, size=18)
        net_chip.next_to(nn, DOWN, buff=0.16)

        to_net = make_flow_arrow(face.get_right() + RIGHT * 0.10, nn.get_left() + LEFT * 0.10, color=CYAN, stroke_width=2.1)

        center = RIGHT * 2.45 + UP * 0.68
        radius = 2.05
        sphere = unit_circle(center, radius=radius, color=CYAN)
        train_a = cluster_on_circle(center, radius, 32 * DEGREES, CYAN, count=7, spread=0.08, seed=61)
        train_b = cluster_on_circle(center, radius, 130 * DEGREES, GREEN, count=7, spread=0.08, seed=62)
        train_c = cluster_on_circle(center, radius, 246 * DEGREES, YELLOW, count=7, spread=0.08, seed=63)
        new_cluster = cluster_on_circle(center, radius, 72 * DEGREES, ORANGE, count=5, spread=0.055, seed=64, dot_radius=0.072)
        new_vector = radial_arrow(center, radius, 72 * DEGREES, color=ORANGE, stroke_width=2.3)
        to_sphere = make_flow_arrow(nn.get_right() + RIGHT * 0.10, point_at(center, radius, PI), color=CYAN, stroke_width=2.1)

        gallery_label = text_mob("training identities", size=18, color=MUTED)
        gallery_label.move_to(center + DOWN * 2.56)
        unseen_label = Tex(r"f_{\mathrm{new}}", font_size=24, color=ORANGE).next_to(point_at(center, radius, 72 * DEGREES), UP, buff=0.08)

        arc_to_a = Arc(radius=radius, start_angle=32 * DEGREES, angle=40 * DEGREES, stroke_color=ORANGE, stroke_width=3.4)
        arc_to_a.shift(center)
        arc_label = Tex(r"\mathrm{compare\ by\ angle}", font_size=23, color=ORANGE)
        arc_label.move_to(center + UP * 2.36 + RIGHT * 0.36)

        notes = key_points(
            [
                "New identities are not memorized as class names",
                ("They are mapped into the learned angular space", ORANGE),
                ("Recognition becomes comparison by similarity", CYAN),
                ("Better geometry improves generalization", GREEN),
            ],
            color=ORANGE,
            width=5.35,
            size=17,
        )
        notes.move_to(LEFT * 3.55 + DOWN * 1.26)

        layout = Group(
            title, face, new_chip, nn, net_chip, to_net, to_sphere,
            sphere, train_a, train_b, train_c, new_cluster, new_vector, gallery_label, unseen_label,
            arc_to_a, arc_label, notes,
        )
        safe_group(layout, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(face), FadeIn(new_chip), run_time=0.45)
        self.play(GrowArrow(to_net), ShowCreation(nn), FadeIn(net_chip), run_time=0.70)
        self.play(GrowArrow(to_sphere), ShowCreation(sphere), run_time=0.65)
        self.play(FadeIn(train_a), FadeIn(train_b), FadeIn(train_c), FadeIn(gallery_label), run_time=0.55)
        self.play(GrowArrow(new_vector), FadeIn(new_cluster), FadeIn(unseen_label), run_time=0.65)
        self.play(ShowCreation(arc_to_a), FadeIn(arc_label), run_time=0.55)
        self.add(notes)
        self.wait(1.05)

    # ------------------------------------------------------------------
    # Beat H - Final summary.
    # ------------------------------------------------------------------
    def beat_h_summary(self):
        title = title_block(
            "ArcFace in Three Ideas",
            "A compact recipe for discriminative embeddings",
            title_size=40,
            subtitle_size=20,
        )

        specs = [
            ("1", "Normalize", r"\Vert f\Vert=\Vert W\Vert=1", "remove norm shortcut", CYAN),
            ("2", "Hypersphere", r"d_{\mathrm{arc}}\propto\theta", "identity is direction", GREEN),
            ("3", "Angular margin", r"\cos(\theta_y+m)", "enforce separation", YELLOW),
        ]
        cards = VGroup()
        for index, name, formula, detail, color in specs:
            panel = make_panel(width=3.30, height=2.06, stroke_color=color, fill_opacity=0.11)
            number = Circle(radius=0.20, stroke_color=color, stroke_width=1.6, fill_color=PANEL, fill_opacity=0.88)
            number_label = Tex(index, font_size=19, color=color).move_to(number)
            number_group = VGroup(number, number_label)
            number_group.move_to(panel.get_corner(UL) + RIGHT * 0.36 + DOWN * 0.33)
            name_mob = text_mob(name, size=24, color=WHITE, bold=True)
            formula_mob = Tex(formula, font_size=28, color=color)
            detail_mob = text_mob(detail, size=17, color=MUTED)
            body = VGroup(name_mob, formula_mob, detail_mob).arrange(DOWN, buff=0.12)
            fit_to_bounds(body, max_width=panel.get_width() - 0.48, max_height=panel.get_height() - 0.42)
            body.move_to(panel.get_center() + DOWN * 0.06)
            cards.add(VGroup(panel, number_group, body))
        cards.arrange(RIGHT, buff=0.54)
        cards.move_to(UP * 0.84)

        arrows = VGroup()
        for left_card, right_card in zip(cards[:-1], cards[1:]):
            arrows.add(make_flow_arrow(
                left_card.get_right() + RIGHT * 0.08,
                right_card.get_left() + LEFT * 0.08,
                color=MUTED,
                stroke_width=1.9,
            ))

        result = VGroup(
            formula_box(r"\mathrm{compact\ same\ identity}", color=GREEN, size=25, width=3.82),
            Tex(r"+", font_size=29, color=MUTED),
            formula_box(r"\mathrm{separated\ different\ identities}", color=YELLOW, size=25, width=4.42),
        ).arrange(RIGHT, buff=0.18)
        result.move_to(DOWN * 0.88)

        final_note = key_points(
            [
                "ArcFace defines what a good face embedding should look like",
                ("stronger geometry", CYAN),
                ("more stable training signal", GREEN),
                ("better fit for face recognition", ORANGE),
            ],
            color=WHITE,
            width=8.15,
            size=20,
        )
        final_note.move_to(DOWN * 2.02)

        layout = Group(title, cards, arrows, result, final_note)
        safe_group(layout, max_width=12.90, max_height=5.62, center=UP * 0.52)

        self.add(title)
        self.play(FadeIn(cards[0]), run_time=0.40)
        for arrow, card in zip(arrows, cards[1:]):
            self.play(GrowArrow(arrow), FadeIn(card), run_time=0.45)
        self.play(FadeIn(result), run_time=0.55)
        self.add(final_note)
        self.wait(1.15)

    def clear_and_wait(self):
        clear_scene(self, run_time=0.65, wait_time=0.30)

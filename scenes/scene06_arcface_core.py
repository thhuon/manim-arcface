from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 06 — ArcFace Core
# =============================================================================


# =============================================================================
# BEAT 1: ArcFace Formula Introduction
# =============================================================================
def beat_1_arcface_intro(scene):
    """Show the full ArcFace loss formula with key term highlights."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{ArcFace: Core Idea}", font_size=54, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    formula = Tex(
        r"L = -\frac{1}{N}\sum_{i=1}^{N}"
        r"\log\frac{e^{s\cos(\theta_{y_i}+m)}}"
        r"{\,e^{s\cos(\theta_{y_i}+m)}+\sum_{j\neq y_i}e^{s\cos\theta_j}\,}",
        font_size=34, color=CYAN,
    )
    formula.move_to(UP * 0.5)
    scene.play(Write(formula), run_time=3.5)
    scene.wait(5.0)

    highlights = [
        (r"m = 0.5", r"\text{Angular margin (radians)}", YELLOW),
        (r"s = 64", r"\text{Feature scale (radius of hypersphere)}", WHITE),
        (r"\cos(\theta_{y_i}+m)", r"\text{Cosine with margin applied}", CYAN),
    ]

    y_offset = DOWN * 1.8
    for sym, desc, col in highlights:
        sym_tex = Tex(sym, font_size=26, color=col)
        desc_tex = Tex(desc, font_size=22, color=WHITE)
        row = VGroup(sym_tex, desc_tex)
        row.arrange(RIGHT, buff=0.4)
        row.next_to(formula.get_bottom(), DOWN, buff=0.3)
        row.shift(y_offset)
        scene.play(FadeIn(row, shift=UP * 0.1), run_time=1.0)
        scene.wait(4.0)
        y_offset += DOWN * 0.9

    scene.wait(10.0)


# =============================================================================
# BEAT 2: Why Angular Distance
# =============================================================================
def beat_2_why_angular_distance(scene):
    """Euclidean vs angular distance, then normalisation makes magnitude irrelevant."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Why Angular Distance?}", font_size=50, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    # ── Euclidean vs angular on a circle ────────────────────────────────────
    circle = Circle(radius=2.5, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
    circle.shift(DOWN * 0.5)
    center = circle.get_center()
    scene.play(ShowCreation(circle), run_time=1.2)

    r_label = Tex(r"\|f\| = 1", font_size=24, color=MUTED)
    r_label.next_to(circle, RIGHT, buff=0.2).shift(DOWN * 0.5)
    scene.play(Write(r_label), run_time=0.8)

    angle_a = PI / 5
    angle_b = PI / 5 + PI / 3
    pt_a = center + 2.5 * np.array([np.cos(angle_a), np.sin(angle_a), 0])
    pt_b = center + 2.5 * np.array([np.cos(angle_b), np.sin(angle_b), 0])

    dot_a = Dot(radius=0.14, color=GREEN)
    dot_b = Dot(radius=0.14, color=CYAN)
    dot_a.move_to(pt_a)
    dot_b.move_to(pt_b)
    lbl_a = Tex(r"A", font_size=22, color=GREEN)
    lbl_b = Tex(r"B", font_size=22, color=CYAN)
    lbl_a.next_to(dot_a, pt_a - center, buff=0.15)
    lbl_b.next_to(dot_b, pt_b - center, buff=0.15)

    scene.play(FadeIn(dot_a), FadeIn(dot_b), Write(lbl_a), Write(lbl_b), run_time=1.0)

    euc_line = DashedLine(pt_a, pt_b, stroke_color=MUTED, stroke_width=2)
    euc_lbl = Tex(r"\text{Euclidean: ignores direction}", font_size=22, color=MUTED)
    euc_lbl.next_to(euc_line.get_center(), DOWN, buff=0.2)
    scene.play(ShowCreation(euc_line), Write(euc_lbl), run_time=1.5)
    scene.wait(6.0)

    arc_angle = Arc(radius=0.9, start_angle=angle_a, angle=angle_b - angle_a,
                    stroke_color=GREEN, stroke_width=2.5)
    arc_angle.shift(center)
    theta_lbl = Tex(r"\theta", font_size=26, color=GREEN)
    mid_angle = (angle_a + angle_b) / 2
    theta_lbl.move_to(center + 1.1 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))

    line_a = Line(center, pt_a, stroke_color=WHITE, stroke_width=1.3)
    line_b = Line(center, pt_b, stroke_color=WHITE, stroke_width=1.3)

    scene.play(ShowCreation(line_a), ShowCreation(line_b), run_time=0.8)
    scene.play(ShowCreation(arc_angle), Write(theta_lbl), run_time=1.2)

    ang_lbl = Tex(r"\cos\theta \text{ — scale-invariant angular distance}", font_size=22, color=GREEN)
    ang_lbl.to_edge(DOWN, buff=0.5)
    scene.play(Write(ang_lbl), run_time=1.5)
    scene.wait(12.0)

    # ── L2 Normalisation makes magnitude irrelevant ──────────────────────────
    scene.play(FadeOut(euc_line), FadeOut(euc_lbl), FadeOut(ang_lbl), run_time=0.8)

    norm_title = Tex(r"\text{After L2 Normalisation: only direction matters}", font_size=28, color=CYAN)
    norm_title.next_to(title, DOWN, buff=0.4)
    scene.play(Write(norm_title), run_time=1.5)

    vec1 = Arrow(center, center + 1.5 * np.array([np.cos(angle_a), np.sin(angle_a), 0]),
                 stroke_color=WHITE, stroke_width=2)
    vec2 = Arrow(center, center + 2.5 * np.array([np.cos(angle_a), np.sin(angle_a), 0]),
                 stroke_color=CYAN, stroke_width=2)
    same_dir = Tex(r"\text{Same direction, different magnitude \textrightarrow{} same identity}", font_size=24, color=WHITE)
    same_dir.to_edge(DOWN, buff=0.5)

    scene.play(ShowCreation(vec1), ShowCreation(vec2), run_time=1.5)
    scene.play(Write(same_dir), run_time=2.0)
    scene.wait(25.0)


# =============================================================================
# BEAT 3: 2D Visual Comparison — Softmax vs ArcFace
# =============================================================================
def beat_3_2d_visual_comparison(scene):
    """Side-by-side circles showing loose softmax clusters vs tight ArcFace clusters."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Softmax vs ArcFace — 2D Comparison}", font_size=44, color=WHITE)
    title.to_edge(UP, buff=0.4)
    scene.play(Write(title), run_time=2.0)

    left_lbl = Tex(r"\text{Softmax}", font_size=30, color=MUTED)
    right_lbl = Tex(r"\text{ArcFace}", font_size=30, color=CYAN)
    left_lbl.shift(LEFT * 3.5 + UP * 1.8)
    right_lbl.shift(RIGHT * 3.5 + UP * 1.8)
    divider = Line(UP * 3.5, DOWN * 3.5, stroke_color=MUTED, stroke_width=1.0)
    scene.play(Write(left_lbl), Write(right_lbl), ShowCreation(divider), run_time=1.0)

    circle_l = Circle(radius=2.0, stroke_color=MUTED, stroke_width=1.2)
    circle_l.shift(LEFT * 3.5 + DOWN * 0.3)
    circle_r = Circle(radius=2.0, stroke_color=CYAN, stroke_width=1.5)
    circle_r.shift(RIGHT * 3.5 + DOWN * 0.3)
    scene.play(ShowCreation(circle_l), ShowCreation(circle_r), run_time=1.2)

    center_l = circle_l.get_center()
    center_r = circle_r.get_center()
    np.random.seed(5)

    cols = [CYAN, GREEN, RED]
    for angle_base, col in [(PI / 5, CYAN), (-PI / 3, GREEN), (PI, RED)]:
        for _ in range(8):
            offset_angle = angle_base + np.random.uniform(-0.7, 0.7)
            offset_r = np.random.uniform(1.0, 1.9)
            pos = center_l + offset_r * np.array([np.cos(offset_angle), np.sin(offset_angle), 0])
            d = Dot(radius=0.09, color=col)
            d.move_to(pos)
            scene.add(d)

    for angle_base, col in [(PI / 5, CYAN), (-PI / 3, GREEN), (PI, RED)]:
        for _ in range(8):
            offset_angle = angle_base + np.random.uniform(-0.22, 0.22)
            offset_r = np.random.uniform(1.7, 2.0)
            pos = center_r + offset_r * np.array([np.cos(offset_angle), np.sin(offset_angle), 0])
            d = Dot(radius=0.09, color=col)
            d.move_to(pos)
            scene.add(d)

    scene.wait(2.0)

    for i, (base_col, cen) in enumerate([(MUTED, center_l), (CYAN, center_r)]):
        for boundary_angle in [PI / 2, -PI / 6, 5 * PI / 6]:
            end1 = cen + 2.2 * np.array([np.cos(boundary_angle), np.sin(boundary_angle), 0])
            end2 = cen - 2.2 * np.array([np.cos(boundary_angle), np.sin(boundary_angle), 0])
            bl = DashedLine(end1, end2, stroke_color=base_col,
                            stroke_width=1.0 + i * 1.0, dash_length=0.12)
            scene.add(bl)

    scene.wait(3.0)

    caption_l = Tex(r"\text{Fuzzy boundaries}", font_size=22, color=MUTED)
    caption_l.next_to(circle_l, DOWN, buff=0.3)
    caption_r = Tex(r"\text{Clear angular margins}", font_size=22, color=CYAN)
    caption_r.next_to(circle_r, DOWN, buff=0.3)
    scene.play(Write(caption_l), Write(caption_r), run_time=1.5)
    scene.wait(35.0)


# =============================================================================
# BEAT 4: Angular Margin Geometric View
# =============================================================================
def beat_4_angular_margin(scene):
    """Show W_yi, embedding f_i, theta arc, and margin m on unit circle."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Angular Margin — Geometric View}", font_size=48, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    circle = Circle(radius=2.5, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
    circle.shift(DOWN * 0.4)
    center = circle.get_center()
    scene.play(ShowCreation(circle), run_time=1.2)

    w_angle = PI / 6
    w_end = center + 2.5 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
    w_arr = Arrow(center, w_end, stroke_color=WHITE, stroke_width=2.5, buff=0)
    w_lbl = Tex(r"W_{y_i}", font_size=24, color=WHITE)
    w_lbl.next_to(w_end, UR, buff=0.12)

    theta = PI / 6 + PI / 5
    emb_end = center + 2.5 * np.array([np.cos(theta), np.sin(theta), 0])
    emb_arr = Arrow(center, emb_end, stroke_color=GREEN, stroke_width=2.5, buff=0)
    emb_lbl = Tex(r"f_i", font_size=24, color=GREEN)
    emb_lbl.next_to(emb_end, UL, buff=0.12)

    scene.play(ShowCreation(w_arr), Write(w_lbl), run_time=1.0)
    scene.play(ShowCreation(emb_arr), Write(emb_lbl), run_time=1.0)

    arc_theta = Arc(radius=0.8, start_angle=w_angle, angle=theta - w_angle,
                    stroke_color=GREEN, stroke_width=2)
    arc_theta.shift(center)
    theta_lbl = Tex(r"\theta", font_size=22, color=GREEN)
    mid = (w_angle + theta) / 2
    theta_lbl.move_to(center + 1.0 * np.array([np.cos(mid), np.sin(mid), 0]))
    scene.play(ShowCreation(arc_theta), Write(theta_lbl), run_time=1.2)
    scene.wait(5.0)

    m = 0.5
    arc_margin = Arc(radius=0.5, start_angle=theta, angle=m,
                      stroke_color=YELLOW, stroke_width=2.5)
    arc_margin.shift(center)
    m_lbl = Tex(r"m", font_size=22, color=YELLOW)
    mid_m = theta + m / 2
    m_lbl.move_to(center + 0.7 * np.array([np.cos(mid_m), np.sin(mid_m), 0]))
    scene.play(ShowCreation(arc_margin), Write(m_lbl), run_time=1.2)

    constraint = Tex(
        r"\text{ArcFace requires } \theta + m < \text{boundary angle}",
        font_size=24, color=YELLOW,
    )
    constraint.to_edge(DOWN, buff=0.5)
    scene.play(Write(constraint), run_time=1.5)
    scene.wait(18.0)


# =============================================================================
# BEAT 5: Why Normalisation Matters
# =============================================================================
def beat_5_normalisation(scene):
    """Without normalisation magnitude affects similarity; after L2 normalisation only direction matters."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Why Normalisation Matters}", font_size=50, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    no_norm_lbl = Tex(r"\text{Without normalisation: magnitude affects similarity}", font_size=28, color=MUTED)
    no_norm_lbl.next_to(title, DOWN, buff=0.45)
    scene.play(Write(no_norm_lbl), run_time=1.5)

    ax = Axes(x_range=[-0.5, 4, 1], y_range=[-0.5, 4, 1],
              width=5, height=4,
              axis_config={"stroke_color": MUTED, "stroke_width": 1.0})
    ax.shift(DOWN * 0.3)
    center = ax.c2p(0, 0)
    scene.play(ShowCreation(ax), run_time=1.0)

    vecs = [(3.5, 0.8, WHITE), (1.5, 1.8, MUTED), (2.5, 2.5, CYAN)]
    arrows_grp = VGroup()
    for x, y, col in vecs:
        end = ax.c2p(x, y)
        arr = Arrow(center, end, stroke_color=col, stroke_width=2.0, buff=0)
        arrows_grp.add(arr)
    scene.play(*[ShowCreation(a) for a in arrows_grp], run_time=1.5)

    problem_text = Tex(
        r"\text{Dot product } W^T f \text{ depends on magnitude of } f",
        font_size=24, color=MUTED,
    )
    problem_text.to_edge(DOWN, buff=0.5)
    scene.play(Write(problem_text), run_time=1.5)
    scene.wait(8.0)

    scene.play(FadeOut(arrows_grp), FadeOut(no_norm_lbl), FadeOut(problem_text),
               FadeOut(ax), run_time=0.8)

    norm_lbl = Tex(r"\text{After L2 normalisation: all embeddings on unit hypersphere}", font_size=26, color=CYAN)
    norm_lbl.next_to(title, DOWN, buff=0.4)
    scene.play(Write(norm_lbl), run_time=1.5)

    sphere = Circle(radius=2.4, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
    sphere.shift(DOWN * 0.5)
    cen = sphere.get_center()
    scene.play(ShowCreation(sphere), run_time=1.0)

    np.random.seed(11)
    unit_dots = VGroup()
    for angle in np.linspace(0, 2 * PI, 20, endpoint=False):
        d = Dot(radius=0.09, color=GREEN)
        d.move_to(cen + 2.4 * np.array([np.cos(angle), np.sin(angle), 0]))
        unit_dots.add(d)
    scene.play(ShowCreation(unit_dots), run_time=2.0)

    conclusion = Tex(
        r"\|f\| = 1,\;\|W\| = 1 \;\Rightarrow\; W^T f = \cos\theta",
        font_size=30, color=GREEN,
    )
    conclusion.to_edge(DOWN, buff=0.5)
    scene.play(Write(conclusion), run_time=2.0)
    scene.wait(15.0)


# =============================================================================
# BEAT 6: ArcFace Formula Step by Step
# =============================================================================
def beat_6_formula_steps(scene):
    """Three-step build-up of the ArcFace loss formula, then the full formula."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{The ArcFace Formula — Step by Step}", font_size=46, color=WHITE)
    title.to_edge(UP, buff=0.4)
    scene.play(Write(title), run_time=2.0)

    step1 = Tex(r"\text{Step 1: } W_{y_i}^T f_i = \cos\theta_{y_i}", font_size=32, color=MUTED)
    step1.shift(UP * 1.5)
    scene.play(Write(step1), run_time=2.0)
    scene.wait(5.0)

    step2 = Tex(r"\text{Step 2: } \cos(\theta_{y_i} + m) \;\leftarrow\;\text{add margin }m", font_size=32, color=CYAN)
    step2.next_to(step1, DOWN, buff=0.6)
    scene.play(Write(step2), run_time=2.0)
    scene.wait(5.0)

    step3 = Tex(r"\text{Step 3: Multiply by scale } s", font_size=32, color=GREEN)
    step3.next_to(step2, DOWN, buff=0.6)
    scene.play(Write(step3), run_time=2.0)
    scene.wait(5.0)

    full = Tex(
        r"L = -\log\frac{e^{s\cos(\theta_{y_i}+m)}}{e^{s\cos(\theta_{y_i}+m)} + \sum_{j\neq y_i}e^{s\cos\theta_j}}",
        font_size=34, color=YELLOW,
    )
    full.next_to(step3, DOWN, buff=0.7)
    rect = SurroundingRectangle(full, color=YELLOW, buff=0.15, corner_radius=0.1)
    scene.play(Write(full), run_time=2.5)
    scene.play(ShowCreation(rect), run_time=1.0)

    insight = Tex(
        r"\text{Margin } m \text{ pushes embeddings deeper into each class region}",
        font_size=24, color=WHITE,
    )
    insight.to_edge(DOWN, buff=0.5)
    scene.play(Write(insight), run_time=2.0)
    scene.wait(15.0)


# =============================================================================
# BEAT 7: Boundary Shifting Effect
# =============================================================================
def beat_7_boundary_shift(scene):
    """Show how margin shifts the decision boundary relative to the weight vector."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Boundary Shifting Effect}", font_size=50, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    circle = Circle(radius=2.5, stroke_color=CYAN, stroke_width=1.5)
    circle.shift(DOWN * 0.4)
    center = circle.get_center()
    scene.play(ShowCreation(circle), run_time=1.0)

    w_angle = PI / 6
    w_end = center + 2.5 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
    w_arr = Arrow(center, w_end, stroke_color=WHITE, stroke_width=2.5, buff=0)
    w_lbl = Tex(r"W_{y_i}", font_size=22, color=WHITE)
    w_lbl.next_to(w_end, UR, buff=0.1)
    scene.play(ShowCreation(w_arr), Write(w_lbl), run_time=1.0)

    old_boundary_angle = w_angle + PI / 2
    old_b1 = center + 3.0 * np.array([np.cos(old_boundary_angle), np.sin(old_boundary_angle), 0])
    old_b2 = center - 3.0 * np.array([np.cos(old_boundary_angle), np.sin(old_boundary_angle), 0])
    old_boundary = DashedLine(old_b1, old_b2, stroke_color=MUTED, stroke_width=2, dash_length=0.15)
    old_label = Tex(r"\text{Softmax boundary}", font_size=20, color=MUTED)
    old_label.next_to(old_b1, UP, buff=0.1)
    scene.play(ShowCreation(old_boundary), Write(old_label), run_time=1.2)
    scene.wait(4.0)

    m = 0.5
    new_boundary_angle = w_angle + PI / 2 - m
    new_b1 = center + 3.0 * np.array([np.cos(new_boundary_angle), np.sin(new_boundary_angle), 0])
    new_b2 = center - 3.0 * np.array([np.cos(new_boundary_angle), np.sin(new_boundary_angle), 0])
    new_boundary = DashedLine(new_b1, new_b2, stroke_color=GREEN, stroke_width=2.5, dash_length=0.15)
    new_label = Tex(r"\text{ArcFace boundary (shifted by }m\text{)}", font_size=20, color=GREEN)
    new_label.next_to(new_b2, DOWN, buff=0.1)
    scene.play(ShowCreation(new_boundary), Write(new_label), run_time=1.5)

    arc_m = Arc(radius=0.55, start_angle=new_boundary_angle, angle=m,
                 stroke_color=YELLOW, stroke_width=2)
    arc_m.shift(center)
    m_lbl = Tex(r"m", font_size=20, color=YELLOW)
    m_lbl.move_to(center + 0.75 * np.array([np.cos(new_boundary_angle + m / 2),
                                              np.sin(new_boundary_angle + m / 2), 0]))
    scene.play(ShowCreation(arc_m), Write(m_lbl), run_time=1.0)

    caption = Tex(
        r"\text{Margin shifts the decision boundary, forcing embedding closer to }W_{y_i}",
        font_size=22, color=WHITE,
    )
    caption.to_edge(DOWN, buff=0.5)
    scene.play(Write(caption), run_time=2.0)
    scene.wait(12.0)


# =============================================================================
# BEAT 8: Hypersphere / Embedding Space View
# =============================================================================
def beat_8_hypersphere(scene):
    """Unit circle with coloured clusters, zoom into theta angle, zoom out full view."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Embedding Space — Hypersphere View}", font_size=46, color=WHITE)
    title.to_edge(UP, buff=0.4)
    scene.play(Write(title), run_time=2.0)

    sphere = Circle(radius=2.6, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
    sphere.shift(DOWN * 0.4)
    center = sphere.get_center()
    scene.play(ShowCreation(sphere), run_time=1.2)

    r_label = Tex(r"\text{Unit Hypersphere: } \|f\| = 1", font_size=24, color=MUTED)
    r_label.to_edge(DOWN, buff=0.5)
    scene.play(Write(r_label), run_time=1.2)

    colours = [CYAN, GREEN, RED, YELLOW]
    cluster_angles = [PI / 6, 3 * PI / 4, -PI / 3, PI + PI / 4]

    np.random.seed(17)
    all_dots = VGroup()
    for angle_base, col in zip(cluster_angles, colours):
        w_end = center + 2.6 * np.array([np.cos(angle_base), np.sin(angle_base), 0])
        w_arr = Arrow(center, w_end, stroke_color=col, stroke_width=2, buff=0)
        scene.play(ShowCreation(w_arr), run_time=0.6)
        for _ in range(7):
            offset_a = angle_base + np.random.uniform(-0.18, 0.18)
            r = np.random.uniform(2.3, 2.6)
            d = Dot(radius=0.09, color=col)
            d.move_to(center + r * np.array([np.cos(offset_a), np.sin(offset_a), 0]))
            all_dots.add(d)

    scene.play(ShowCreation(all_dots), run_time=2.0)
    scene.wait(15.0)

    scene.play(scene.camera.frame.animate.scale(0.6).move_to(center + LEFT * 0.2), run_time=2.0)

    angle_a = cluster_angles[0]
    angle_b = cluster_angles[1]
    line_a = Line(center, center + 2.6 * np.array([np.cos(angle_a), np.sin(angle_a), 0]),
                  stroke_color=WHITE, stroke_width=1.5)
    line_b = Line(center, center + 2.6 * np.array([np.cos(angle_b), np.sin(angle_b), 0]),
                  stroke_color=WHITE, stroke_width=1.5)
    arc_theta = Arc(radius=0.5, start_angle=angle_a, angle=angle_b - angle_a,
                     stroke_color=GREEN, stroke_width=2.0)
    arc_theta.shift(center)
    theta_lbl = Tex(r"\theta", font_size=20, color=GREEN)
    mid_angle = (angle_a + angle_b) / 2
    theta_lbl.move_to(center + 0.7 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))

    scene.play(ShowCreation(line_a), ShowCreation(line_b), run_time=1.0)
    scene.play(ShowCreation(arc_theta), Write(theta_lbl), run_time=1.0)
    scene.wait(18.0)

    scene.play(scene.camera.frame.animate.scale(1 / 0.6).move_to(ORIGIN), run_time=2.0)

    projection_label = Tex(
        r"\text{All embeddings projected onto the unit sphere surface}",
        font_size=24, color=CYAN,
    )
    projection_label.to_edge(DOWN, buff=0.5)
    scene.play(FadeOut(r_label), Write(projection_label), run_time=1.5)
    scene.wait(25.0)


# =============================================================================
# MAIN SCENE: plays all beats in sequence
# =============================================================================
class Scene06_ArcFaceCore(Scene):
    def construct(self):
        beat_1_arcface_intro(self)
        self.clear()
        self.wait(1.0)

        beat_2_why_angular_distance(self)
        self.clear()
        self.wait(1.0)

        beat_3_2d_visual_comparison(self)
        self.clear()
        self.wait(1.0)

        beat_4_angular_margin(self)
        self.clear()
        self.wait(1.0)

        beat_5_normalisation(self)
        self.clear()
        self.wait(1.0)

        beat_6_formula_steps(self)
        self.clear()
        self.wait(1.0)

        beat_7_boundary_shift(self)
        self.clear()
        self.wait(1.0)

        beat_8_hypersphere(self)

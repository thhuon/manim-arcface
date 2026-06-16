from manimlib import *
from scenes.utils import *


# =============================================================================
# BEAT 1: Loss Function Introduction
# =============================================================================
def beat_1_softmax_intro(scene):
    """Softmax formula + geometric intuition."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Softmax Loss Function}", font_size=52, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    formula = Tex(
        r"L = -\log\frac{e^{W_{y_i}^T f_i}}{\sum_{j=1}^{N} e^{W_j^T f_i}}",
        font_size=44, color=CYAN,
    )
    formula.move_to(UP * 0.8)
    scene.play(Write(formula), run_time=2.5)

    parts = [
        (r"W_{y_i}", r"\text{Weight vector for correct class}", CYAN),
        (r"f_i", r"\text{Embedding vector}", GREEN),
        (r"N", r"\text{Number of classes}", WHITE),
    ]
    explanation = VGroup()
    for sym, desc, col in parts:
        sym_tex = Tex(sym, font_size=26, color=col)
        desc_tex = Tex(desc, font_size=24, color=WHITE)
        row = VGroup(sym_tex, desc_tex)
        row.arrange(RIGHT, buff=0.4)
        explanation.add(row)
    explanation.arrange(DOWN, buff=0.4)
    explanation.next_to(formula, DOWN, buff=0.6)

    for row in explanation:
        scene.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.9)
    scene.wait(10.0)

    intuition = Tex(
        r"\text{Softmax pushes embedding } f_i \text{ toward weight } W_{y_i}",
        font_size=28, color=MUTED,
    )
    intuition.to_edge(DOWN, buff=0.5)
    scene.play(Write(intuition), run_time=2.0)
    scene.wait(15.0)


# =============================================================================
# BEAT 2: How Softmax Works
# =============================================================================
def beat_2_softmax_concept(scene):
    """Embedding space with weight vectors, movement, and decision boundaries."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{How Softmax Works}", font_size=50, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    # --- Embedding space with weight vectors ---
    ax = Axes(
        x_range=[-3.5, 3.5, 1], y_range=[-3.0, 3.0, 1],
        width=6.5, height=5,
        axis_config={"stroke_color": MUTED, "stroke_width": 1.0},
    )
    ax.shift(DOWN * 0.4)
    scene.play(ShowCreation(ax), run_time=1.2)

    w_colors = [CYAN, GREEN, RED]
    w_angles = [PI / 4, 3 * PI / 4, -PI / 2]
    w_labels_text = [r"W_1", r"W_2", r"W_3"]
    weights = VGroup()
    w_label_grp = VGroup()
    center = ax.get_center()

    for angle, col, lbl_text in zip(w_angles, w_colors, w_labels_text):
        endpoint = center + 2.4 * np.array([np.cos(angle), np.sin(angle), 0])
        arr = Arrow(center, endpoint, stroke_color=col, stroke_width=2.5, buff=0)
        lbl = Tex(lbl_text, font_size=24, color=col)
        lbl.next_to(endpoint, endpoint - center, buff=0.15)
        weights.add(arr)
        w_label_grp.add(lbl)

    scene.play(*[ShowCreation(w) for w in weights], run_time=1.5)
    scene.play(FadeIn(w_label_grp), run_time=0.8)

    w_caption = Tex(r"\text{Class weight vectors } W_j", font_size=26, color=WHITE)
    w_caption.to_edge(DOWN, buff=0.5)
    scene.play(Write(w_caption), run_time=1.5)
    scene.wait(10.0)

    # --- Embedding moves toward its class weight ---
    scene.play(FadeOut(w_caption), run_time=0.5)

    emb = Dot(radius=0.14, color=WHITE)
    emb_start = center + 1.2 * np.array([np.cos(PI / 8), np.sin(PI / 8), 0])
    emb.move_to(emb_start)
    emb_lbl = Tex(r"f_i", font_size=22, color=WHITE)
    emb_lbl.next_to(emb, UR, buff=0.1)

    scene.play(FadeIn(emb), Write(emb_lbl), run_time=1.0)

    move_caption = Tex(r"\text{Softmax pushes } f_i \text{ toward } W_{y_i}", font_size=26, color=CYAN)
    move_caption.to_edge(DOWN, buff=0.5)
    scene.play(Write(move_caption), run_time=1.5)

    target_pt = center + 2.0 * np.array([np.cos(w_angles[0]), np.sin(w_angles[0]), 0])
    scene.play(
        emb.animate.move_to(target_pt),
        emb_lbl.animate.next_to(target_pt, UR, buff=0.1),
        run_time=2.5,
    )
    scene.wait(12.0)

    # --- Decision boundaries ---
    scene.play(FadeOut(move_caption), run_time=0.5)

    boundary_lines = VGroup()
    for angle in [PI / 2, -PI / 12]:
        end1 = center + 3.2 * np.array([np.cos(angle), np.sin(angle), 0])
        end2 = center - 3.2 * np.array([np.cos(angle), np.sin(angle), 0])
        bl = DashedLine(end1, end2, stroke_color=MUTED, stroke_width=1.5, dash_length=0.18)
        boundary_lines.add(bl)

    scene.play(ShowCreation(boundary_lines), run_time=1.5)

    boundary_caption = Tex(
        r"\text{Decision boundaries bisect the angle between weight vectors}",
        font_size=24, color=MUTED,
    )
    boundary_caption.to_edge(DOWN, buff=0.5)
    scene.play(Write(boundary_caption), run_time=2.0)
    scene.wait(18.0)


# =============================================================================
# BEAT 3: Limitations of Standard Softmax
# =============================================================================
def beat_3_softmax_limitations(scene):
    """Softmax only cares about correct side + intra/inter class spread."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Limitations of Standard Softmax}", font_size=48, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    # --- Only requires correct side of boundary ---
    ax = Axes(
        x_range=[-3, 3, 1], y_range=[-2.8, 2.8, 1],
        width=6, height=4.8,
        axis_config={"stroke_color": MUTED, "stroke_width": 0.9},
    )
    ax.shift(DOWN * 0.4)
    center = ax.get_center()
    scene.play(ShowCreation(ax), run_time=1.0)

    w_angle = PI / 4
    w_end = center + 2.2 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
    w_arr = Arrow(center, w_end, stroke_color=CYAN, stroke_width=2.5, buff=0)
    w_lbl = Tex(r"W_1", font_size=24, color=CYAN)
    w_lbl.next_to(w_end, UR, buff=0.12)
    scene.play(ShowCreation(w_arr), Write(w_lbl), run_time=1.0)

    bnd_angle = w_angle + PI / 2
    bnd1 = center + 3.0 * np.array([np.cos(bnd_angle), np.sin(bnd_angle), 0])
    bnd2 = center - 3.0 * np.array([np.cos(bnd_angle), np.sin(bnd_angle), 0])
    boundary = DashedLine(bnd1, bnd2, stroke_color=MUTED, stroke_width=1.5)
    scene.play(ShowCreation(boundary), run_time=1.0)

    e_far = Dot(radius=0.12, color=WHITE)
    e_close = Dot(radius=0.12, color=GREEN)
    far_pos = center + 1.8 * np.array([np.cos(w_angle + 0.05), np.sin(w_angle + 0.05), 0])
    close_pos = center + 1.2 * np.array([np.cos(w_angle + 1.0), np.sin(w_angle + 1.0), 0])
    e_far.move_to(far_pos)
    e_close.move_to(close_pos)

    e_far_lbl = Tex(r"\text{Good}", font_size=20, color=WHITE)
    e_far_lbl.next_to(e_far, UR, buff=0.1)
    e_close_lbl = Tex(r"\text{Still OK?}", font_size=20, color=GREEN)
    e_close_lbl.next_to(e_close, UL, buff=0.1)

    scene.play(FadeIn(e_far), Write(e_far_lbl), run_time=0.9)
    scene.play(FadeIn(e_close), Write(e_close_lbl), run_time=0.9)

    problem_text = Tex(
        r"\text{Softmax only requires: correct side of boundary}",
        font_size=26, color=MUTED,
    )
    problem_text.to_edge(DOWN, buff=0.5)
    scene.play(Write(problem_text), run_time=2.0)
    scene.wait(15.0)

    # --- Intra-class spread / inter-class overlap ---
    scene.play(
        FadeOut(e_far), FadeOut(e_far_lbl), FadeOut(e_close),
        FadeOut(e_close_lbl), FadeOut(problem_text), FadeOut(w_arr),
        FadeOut(w_lbl), FadeOut(boundary),
        run_time=0.8,
    )

    sub_lbl = Tex(r"\text{Standard Softmax — Embedding Distribution}", font_size=28, color=WHITE)
    sub_lbl.next_to(title, DOWN, buff=0.35)
    scene.play(Write(sub_lbl), run_time=1.2)

    np.random.seed(12)
    soft_dots = VGroup()
    cols_list = [CYAN, GREEN]
    centers_list = [
        center + LEFT * 0.4 + DOWN * 0.1,
        center + RIGHT * 0.5 + UP * 0.2,
    ]

    for cen, col in zip(centers_list, cols_list):
        for _ in range(15):
            offset = np.random.randn(3) * 0.7
            offset[2] = 0
            d = Dot(radius=0.09, color=col)
            d.move_to(cen + offset)
            soft_dots.add(d)

    scene.play(ShowCreation(soft_dots), run_time=2.5)

    spread_caption = Tex(
        r"\text{Large intra-class spread, inter-class overlap}",
        font_size=26, color=RED,
    )
    spread_caption.to_edge(DOWN, buff=0.5)
    scene.play(Write(spread_caption), run_time=2.0)
    scene.wait(25.0)

    # --- Need for margin-based loss ---
    scene.play(FadeOut(soft_dots), FadeOut(sub_lbl), FadeOut(spread_caption), run_time=1.0)

    need_text = Tex(r"\text{We need tighter constraints on the embedding space}", font_size=32, color=WHITE)
    need_text.move_to(UP * 1.0)
    scene.play(Write(need_text), run_time=2.0)

    # Bullet-style solution items
    sol1 = Tex(r"\text{- Minimise intra-class variation}", font_size=26, color=CYAN)
    sol2 = Tex(r"\text{- Maximise inter-class variation}", font_size=26, color=CYAN)
    sol3 = Tex(r"\text{- Add angular margin to enforce strict boundaries}", font_size=26, color=CYAN)
    sol_group = VGroup(sol1, sol2, sol3)
    sol_group.arrange(DOWN, buff=0.45)
    sol_group.next_to(need_text, DOWN, buff=0.5)

    for item in sol_group:
        scene.play(FadeIn(item, shift=RIGHT * 0.1), run_time=1.2)
        scene.wait(3.0)

    scene.wait(20.0)


# =============================================================================
# BEAT 4: Evolution of Face Recognition Milestones
# =============================================================================
def beat_4_evolution_milestones(scene):
    """Timeline of face recognition from Eigenfaces to ArcFace."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Evolution of Face Recognition}", font_size=48, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    milestones = [
        ("1991", "Eigenfaces", MUTED, r"\text{PCA-based method}"),
        ("2014", "DeepFace", BLUE, r"\text{Facebook's deep CNN}"),
        ("2015", "FaceNet", GREEN, r"\text{Triplet loss, 99.6\% LFW}"),
        ("2017", "SphereFace", CYAN, r"\text{Multiplicative angular margin}"),
        ("2019", "ArcFace", ORANGE, r"\text{Additive angular margin}"),
    ]

    timeline_line = Line(LEFT * 5.5, RIGHT * 5.5, stroke_color=MUTED, stroke_width=1.5)
    timeline_line.shift(DOWN * 0.5)
    scene.play(ShowCreation(timeline_line), run_time=1.2)

    tick_positions = np.linspace(-4.5, 4.5, len(milestones))

    arcface_lbl = None
    for i, (year, name, col, desc) in enumerate(milestones):
        x = tick_positions[i]
        tick = Line(DOWN * 0.15, UP * 0.15, stroke_color=col, stroke_width=2.5)
        tick.move_to(timeline_line.get_center() + x * RIGHT)

        year_lbl = Tex(year, font_size=20, color=col)
        name_lbl = Tex(r"\text{" + name + r"}", font_size=22, color=col)
        desc_lbl = Tex(desc, font_size=18, color=WHITE)

        year_lbl.next_to(tick, DOWN, buff=0.2)
        if i % 2 == 0:
            name_lbl.next_to(tick, UP, buff=0.4)
            desc_lbl.next_to(name_lbl, UP, buff=0.15)
        else:
            name_lbl.next_to(tick, DOWN, buff=0.6)
            desc_lbl.next_to(name_lbl, DOWN, buff=0.15)

        scene.play(ShowCreation(tick), Write(year_lbl), run_time=0.7)
        scene.play(Write(name_lbl), Write(desc_lbl), run_time=1.0)
        scene.wait(4.0)

        if name == "ArcFace":
            arcface_lbl = name_lbl

    # Highlight ArcFace
    if arcface_lbl:
        arcface_highlight = SurroundingRectangle(arcface_lbl, color=ORANGE, buff=0.1)
        scene.play(ShowCreation(arcface_highlight), run_time=1.2)

    arcface_caption = Tex(r"\text{State-of-the-art as of 2019+}", font_size=26, color=ORANGE)
    arcface_caption.to_edge(DOWN, buff=0.5)
    scene.play(Write(arcface_caption), run_time=1.5)
    scene.wait(25.0)


# =============================================================================
# BEAT 5: Transition to ArcFace
# =============================================================================
def beat_5_transition(scene):
    """Bridge from Softmax to ArcFace via angular margin."""
    scene.camera.background_color = DARK

    bridge = Tex(r"\text{From Softmax to ArcFace}", font_size=52, color=WHITE)
    bridge.move_to(UP * 1.2)
    scene.play(Write(bridge), run_time=2.0)

    arrow = Arrow(UP * 0.4, DOWN * 0.4, stroke_color=CYAN, stroke_width=3)
    scene.play(ShowCreation(arrow), run_time=1.0)

    key = Tex(
        r"\text{The key idea: add an angular margin } m \text{ to the angle } \theta",
        font_size=30, color=CYAN,
    )
    key.next_to(arrow, DOWN, buff=0.4)
    scene.play(Write(key), run_time=2.5)
    scene.wait(5.0)

    soft_f = Tex(r"\text{Softmax: } \cos(\theta)", font_size=30, color=MUTED)
    arc_f = Tex(r"\text{ArcFace: } \cos(\theta + m)", font_size=30, color=GREEN)
    soft_f.shift(LEFT * 2.5 + DOWN * 2.0)
    arc_f.shift(RIGHT * 2.5 + DOWN * 2.0)
    vs = Tex(r"\rightarrow", font_size=36, color=WHITE)
    vs.shift(DOWN * 2.0)

    scene.play(Write(soft_f), run_time=1.2)
    scene.play(Write(vs), run_time=0.5)
    scene.play(Write(arc_f), run_time=1.2)
    scene.wait(15.0)


# =============================================================================
# MAIN SCENE: plays all beats in sequence
# =============================================================================
class Scene05_Softmax(Scene):
    def construct(self):
        # Beat 1: Softmax Loss Function Introduction
        beat_1_softmax_intro(self)
        self.clear()
        self.wait(1.0)

        # Beat 2: How Softmax Works
        beat_2_softmax_concept(self)
        self.clear()
        self.wait(1.0)

        # Beat 3: Limitations of Standard Softmax
        beat_3_softmax_limitations(self)
        self.clear()
        self.wait(1.0)

        # Beat 4: Evolution of Face Recognition
        beat_4_evolution_milestones(self)
        self.clear()
        self.wait(1.0)

        # Beat 5: Transition to ArcFace
        beat_5_transition(self)

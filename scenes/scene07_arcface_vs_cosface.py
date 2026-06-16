from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 07 — ArcFace vs CosFace / Practical Effects
# =============================================================================


# =============================================================================
# BEAT 1: ArcFace vs CosFace Comparison Table
# =============================================================================
def beat_1_arcface_vs_cosface(scene):
    """Show a comparison table: CosFace subtracts margin from cos, ArcFace adds to angle."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{ArcFace vs.\ CosFace}", font_size=50, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    rows = [
        (r"\text{Method}", r"\text{Margin Applied To}", r"\text{Formula}"),
        (r"\text{CosFace}", r"\cos\theta_{y_i}", r"\cos\theta_{y_i} - m"),
        (r"\text{ArcFace}", r"\theta_{y_i}", r"\cos(\theta_{y_i} + m)"),
    ]

    table = VGroup()
    for i, row in enumerate(rows):
        row_group = VGroup(
            *[Tex(t, font_size=26,
                   color=(WHITE if i == 0 else ([MUTED, GREEN][i - 1]))) for t in row]
        )
        row_group.arrange(RIGHT, buff=1.2)
        table.add(row_group)
    table.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    table.next_to(title, DOWN, buff=0.7)

    for row in table:
        scene.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.9)
        scene.wait(1.5)

    distinction = Tex(
        r"\text{ArcFace margin is on }\theta\text{ — direct geometric meaning on hypersphere}",
        font_size=24, color=CYAN,
    )
    distinction.to_edge(DOWN, buff=0.5)
    scene.play(Write(distinction), run_time=2.0)
    scene.wait(8.0)


# =============================================================================
# BEAT 2: ArcFace vs Triplet Loss
# =============================================================================
def beat_2_arcface_vs_triplet(scene):
    """Two-column comparison: Triplet Loss challenges vs ArcFace advantages."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{ArcFace vs.\ Triplet Loss}", font_size=48, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    triplet_label = Tex(r"\text{Triplet Loss Challenges:}", font_size=30, color=MUTED)
    triplet_label.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
    scene.play(Write(triplet_label), run_time=1.2)

    triplet_items = [
        r"\bullet\;\text{Requires careful triplet mining}",
        r"\bullet\;\text{Unstable training}",
        r"\bullet\;\text{Slow convergence}",
    ]
    t_group = VGroup(*[Tex(t, font_size=26, color=MUTED) for t in triplet_items])
    t_group.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    t_group.next_to(triplet_label, DOWN, buff=0.4)
    t_group.to_edge(LEFT, buff=1.0)
    for item in t_group:
        scene.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.8)

    scene.wait(5.0)

    divider = DashedLine(UP * 1, DOWN * 1.8, stroke_color=MUTED, stroke_width=1.5)
    divider.shift(RIGHT * 0.2)
    scene.play(ShowCreation(divider), run_time=0.8)

    arc_label = Tex(r"\text{ArcFace Advantages:}", font_size=30, color=CYAN)
    arc_label.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.8)
    scene.play(Write(arc_label), run_time=1.2)

    arc_items = [
        r"\bullet\;\text{No triplet mining needed}",
        r"\bullet\;\text{Every batch contributes}",
        r"\bullet\;\text{Stable and scalable}",
    ]
    a_group = VGroup(*[Tex(t, font_size=26, color=CYAN) for t in arc_items])
    a_group.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    a_group.next_to(arc_label, DOWN, buff=0.4)
    a_group.to_edge(RIGHT, buff=1.0)
    for item in a_group:
        scene.play(FadeIn(item, shift=LEFT * 0.1), run_time=0.8)

    scene.wait(8.0)

    bottom = Tex(r"\text{Classification-based metric learning = best of both worlds}", font_size=24, color=GREEN)
    bottom.to_edge(DOWN, buff=0.5)
    scene.play(Write(bottom), run_time=2.0)
    scene.wait(5.0)


# =============================================================================
# BEAT 3: Side-by-side Softmax vs ArcFace Clusters
# =============================================================================
def beat_3_softmax_vs_arcface_clusters(scene):
    """Left: loose softmax clusters; Right: tight ArcFace clusters."""
    scene.camera.background_color = DARK

    left_lbl = Tex(r"\text{Standard Softmax}", font_size=26, color=MUTED)
    right_lbl = Tex(r"\text{ArcFace}", font_size=26, color=CYAN)
    left_lbl.shift(LEFT * 3.5 + UP * 1.8)
    right_lbl.shift(RIGHT * 3.5 + UP * 1.8)
    divider = Line(UP * 3, DOWN * 3, stroke_color=MUTED, stroke_width=1.0)
    scene.play(Write(left_lbl), Write(right_lbl), ShowCreation(divider), run_time=1.0)

    cl = Circle(radius=2.0, stroke_color=MUTED, stroke_width=1.2)
    cl.shift(LEFT * 3.5 + DOWN * 0.3)
    cr = Circle(radius=2.0, stroke_color=CYAN, stroke_width=1.5)
    cr.shift(RIGHT * 3.5 + DOWN * 0.3)
    scene.play(ShowCreation(cl), ShowCreation(cr), run_time=1.0)

    np.random.seed(7)
    cols = [CYAN, GREEN, RED]
    bases = [PI / 5, -PI / 3, PI]
    soft_dots = VGroup()
    arc_dots = VGroup()

    for angle_base, col in zip(bases, cols):
        cl_center = cl.get_center()
        cr_center = cr.get_center()
        for _ in range(10):
            oa = angle_base + np.random.uniform(-0.65, 0.65)
            r = np.random.uniform(0.8, 1.9)
            d = Dot(radius=0.09, color=col)
            d.move_to(cl_center + r * np.array([np.cos(oa), np.sin(oa), 0]))
            soft_dots.add(d)

            oa2 = angle_base + np.random.uniform(-0.20, 0.20)
            r2 = np.random.uniform(1.7, 2.0)
            d2 = Dot(radius=0.09, color=col)
            d2.move_to(cr_center + r2 * np.array([np.cos(oa2), np.sin(oa2), 0]))
            arc_dots.add(d2)

    scene.play(ShowCreation(soft_dots), ShowCreation(arc_dots), run_time=2.0)

    soft_cap = Tex(r"\text{Loose clusters, blurred boundaries}", font_size=20, color=MUTED)
    arc_cap = Tex(r"\text{Tight clusters, clear margins}", font_size=20, color=CYAN)
    soft_cap.next_to(cl, DOWN, buff=0.3)
    arc_cap.next_to(cr, DOWN, buff=0.3)
    scene.play(Write(soft_cap), Write(arc_cap), run_time=1.5)
    scene.wait(20.0)


# =============================================================================
# BEAT 4: Robustness Under Difficult Conditions
# =============================================================================
def beat_4_robustness(scene):
    """Bullet list of difficult conditions ArcFace handles well."""
    scene.camera.background_color = DARK

    robust_lbl = Tex(r"\text{Robustness: ArcFace handles difficult conditions}", font_size=30, color=CYAN)
    robust_lbl.to_edge(UP, buff=0.5)
    scene.play(Write(robust_lbl), run_time=1.5)

    conditions = [
        r"\bullet\;\text{Different lighting conditions}",
        r"\bullet\;\text{Variations in face angle / pose}",
        r"\bullet\;\text{Different facial expressions}",
        r"\bullet\;\text{Faces with similar characteristics}",
    ]
    cond_group = VGroup(*[Tex(t, font_size=26, color=WHITE) for t in conditions])
    cond_group.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
    cond_group.to_edge(LEFT, buff=1.2)
    cond_group.shift(DOWN * 0.5)

    for cond in cond_group:
        scene.play(FadeIn(cond, shift=RIGHT * 0.1), run_time=1.0)
        scene.wait(4.0)

    scene.wait(15.0)


# =============================================================================
# BEAT 5: What ArcFace Changes
# =============================================================================
def beat_5_what_arcface_changes(scene):
    """Three-row summary: network unchanged, loss improved, embedding structure much better."""
    scene.camera.background_color = DARK

    key_title = Tex(r"\text{What ArcFace Changes:}", font_size=32, color=YELLOW)
    key_title.to_edge(UP, buff=0.5)
    scene.play(Write(key_title), run_time=1.5)

    key_items = [
        (r"\text{Network architecture}", r"\text{UNCHANGED}", MUTED, GREEN),
        (r"\text{Loss function}", r"\text{IMPROVED (+ margin)}", MUTED, CYAN),
        (r"\text{Embedding structure}", r"\text{MUCH BETTER}", MUTED, GREEN),
    ]
    keys_group = VGroup()
    for what, how, c1, c2 in key_items:
        row = VGroup(
            Tex(what, font_size=26, color=c1),
            Tex(r"\rightarrow", font_size=26, color=WHITE),
            Tex(how, font_size=26, color=c2),
        )
        row.arrange(RIGHT, buff=0.5)
        keys_group.add(row)
    keys_group.arrange(DOWN, buff=0.5)
    keys_group.shift(DOWN * 0.5)

    for row in keys_group:
        scene.play(FadeIn(row, shift=UP * 0.1), run_time=1.0)
        scene.wait(4.0)

    scene.wait(20.0)


# =============================================================================
# MAIN SCENE: plays all beats in sequence
# =============================================================================
class Scene07_ArcFaceVsCosFace(Scene):
    def construct(self):
        beat_1_arcface_vs_cosface(self)
        self.clear()
        self.wait(1.0)

        beat_2_arcface_vs_triplet(self)
        self.clear()
        self.wait(1.0)

        beat_3_softmax_vs_arcface_clusters(self)
        self.clear()
        self.wait(1.0)

        beat_4_robustness(self)
        self.clear()
        self.wait(1.0)

        beat_5_what_arcface_changes(self)

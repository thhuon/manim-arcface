from manimlib import *
from scenes.utils import *

TARGET = 85.4

class Scene10_SoftmaxConcept(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{How Softmax Works}", font_size=50, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–25s): Embedding space with decision boundaries
        # ─────────────────────────────────────────────────────────────────
        ax = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.0, 3.0, 1],
            width=6.5, height=5,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.0},
        )
        ax.shift(DOWN * 0.4)
        self.play(ShowCreation(ax), run_time=1.2)

        # Weight vectors (class representatives)
        w_colors = [CYAN, GREEN, "#FF4444"]
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

        self.play(*[ShowCreation(w) for w in weights], run_time=1.5)
        self.play(FadeIn(w_label_grp), run_time=0.8)

        w_caption = Tex(r"\text{Class weight vectors } W_j", font_size=26, color=WHITE)
        w_caption.to_edge(DOWN, buff=0.5)
        self.play(Write(w_caption), run_time=1.5)
        self.wait(10.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (25–55s): Embedding moves toward its class weight
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(w_caption), run_time=0.5)

        emb = Dot(radius=0.14, color=WHITE)
        emb_start = center + 1.2 * np.array([np.cos(PI / 8), np.sin(PI / 8), 0])
        emb.move_to(emb_start)
        emb_lbl = Tex(r"f_i", font_size=22, color=WHITE)
        emb_lbl.next_to(emb, UR, buff=0.1)

        self.play(FadeIn(emb), Write(emb_lbl), run_time=1.0)

        move_caption = Tex(r"\text{Softmax pushes } f_i \text{ toward } W_{y_i}", font_size=26, color=CYAN)
        move_caption.to_edge(DOWN, buff=0.5)
        self.play(Write(move_caption), run_time=1.5)

        target_pt = center + 2.0 * np.array([np.cos(w_angles[0]), np.sin(w_angles[0]), 0])
        self.play(emb.animate.move_to(target_pt), emb_lbl.animate.next_to(target_pt, UR, buff=0.1), run_time=2.5)
        self.wait(12.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (55–85s): Decision boundary
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(move_caption), run_time=0.5)

        # Decision lines between classes
        boundary_lines = VGroup()
        for angle in [PI / 2, -PI / 12]:
            end1 = center + 3.2 * np.array([np.cos(angle), np.sin(angle), 0])
            end2 = center - 3.2 * np.array([np.cos(angle), np.sin(angle), 0])
            bl = DashedLine(end1, end2, stroke_color=MUTED, stroke_width=1.5, dash_length=0.18)
            boundary_lines.add(bl)

        self.play(ShowCreation(boundary_lines), run_time=1.5)

        boundary_caption = Tex(r"\text{Decision boundaries bisect the angle between weight vectors}", font_size=24, color=MUTED)
        boundary_caption.to_edge(DOWN, buff=0.5)
        self.play(Write(boundary_caption), run_time=2.0)
        self.wait(18.0)
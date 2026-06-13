from manimlib import *
from scenes.utils import *

TARGET = 67.9

class Scene22_ArcfaceCoreMergedWithPartC(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{ArcFace Core Mechanism}", font_size=50, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–25s): Softmax — only correct side needed
        # ─────────────────────────────────────────────────────────────────
        soft_text = Tex(
            r"\text{Standard Softmax: only needs correct side of boundary}",
            font_size=28, color=MUTED,
        )
        soft_text.next_to(title, DOWN, buff=0.45)
        self.play(Write(soft_text), run_time=2.0)
        self.wait(8.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (25–50s): ArcFace adds margin
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(soft_text), run_time=0.5)
        arc_text = Tex(
            r"\text{ArcFace: adds angular margin } m\text{ — must be }\textit{sufficiently close}",
            font_size=26, color=CYAN,
        )
        arc_text.next_to(title, DOWN, buff=0.45)
        self.play(Write(arc_text), run_time=2.0)

        # cos(θ) → cos(θ+m) transformation
        compare = VGroup(
            Tex(r"\text{Softmax: }\cos\theta_{y_i}", font_size=30, color=MUTED),
            Tex(r"\longrightarrow", font_size=30, color=WHITE),
            Tex(r"\text{ArcFace: }\cos(\theta_{y_i}+m)", font_size=30, color=CYAN),
        )
        compare.arrange(RIGHT, buff=0.5)
        compare.shift(DOWN * 0.2)
        self.play(FadeIn(compare), run_time=1.5)
        self.wait(10.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (50–67s): Geometric effect on circle
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(arc_text), FadeOut(compare), run_time=0.8)

        circle = Circle(radius=2.2, stroke_color=CYAN, stroke_width=1.5)
        circle.shift(DOWN * 0.8)
        center = circle.get_center()
        self.play(ShowCreation(circle), run_time=1.0)

        w_angle = PI / 6
        w_end = center + 2.2 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
        w_arr = Arrow(center, w_end, stroke_color=WHITE, stroke_width=2.5, buff=0)
        emb_angle = w_angle + 0.6
        emb_end = center + 2.2 * np.array([np.cos(emb_angle), np.sin(emb_angle), 0])
        emb_arr = Arrow(center, emb_end, stroke_color=GREEN, stroke_width=2.5, buff=0)

        self.play(ShowCreation(w_arr), ShowCreation(emb_arr), run_time=1.2)

        # Animate embedding moving closer to W (effect of margin training)
        new_emb = center + 2.2 * np.array([np.cos(w_angle + 0.2), np.sin(w_angle + 0.2), 0])
        self.play(emb_arr.animate.put_start_and_end_on(center, new_emb), run_time=2.0)

        concl = Tex(
            r"\text{Training forces embedding toward class direction — clearer separation}",
            font_size=24, color=GREEN,
        )
        concl.to_edge(DOWN, buff=0.5)
        self.play(Write(concl), run_time=1.5)
        self.wait(8.0)
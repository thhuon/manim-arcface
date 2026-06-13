from manimlib import *
from scenes.utils import *

TARGET = 47.1

class Scene18_ArcfaceCoreWhyNormalizationMatters(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Why Normalisation Matters}", font_size=50, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ── Without normalisation: magnitude contaminates similarity ─────
        no_norm_lbl = Tex(r"\text{Without normalisation: magnitude affects similarity}", font_size=28, color=MUTED)
        no_norm_lbl.next_to(title, DOWN, buff=0.45)
        self.play(Write(no_norm_lbl), run_time=1.5)

        # Axes
        ax = Axes(x_range=[-0.5, 4, 1], y_range=[-0.5, 4, 1],
                  width=5, height=4,
                  axis_config={"stroke_color": MUTED, "stroke_width": 1.0})
        ax.shift(DOWN * 0.3)
        center = ax.c2p(0, 0)
        self.play(ShowCreation(ax), run_time=1.0)

        # Three vectors: same direction, different lengths
        vecs = [(3.5, 0.8, WHITE), (1.5, 1.8, MUTED), (2.5, 2.5, CYAN)]
        arrows_grp = VGroup()
        for x, y, col in vecs:
            end = ax.c2p(x, y)
            arr = Arrow(center, end, stroke_color=col, stroke_width=2.0, buff=0)
            arrows_grp.add(arr)
        self.play(*[ShowCreation(a) for a in arrows_grp], run_time=1.5)

        problem_text = Tex(
            r"\text{Dot product } W^T f \text{ depends on magnitude of } f",
            font_size=24, color=MUTED,
        )
        problem_text.to_edge(DOWN, buff=0.5)
        self.play(Write(problem_text), run_time=1.5)
        self.wait(8.0)

        # ── With normalisation: unit sphere ──────────────────────────────
        self.play(FadeOut(arrows_grp), FadeOut(no_norm_lbl), FadeOut(problem_text),
                  FadeOut(ax), run_time=0.8)

        norm_lbl = Tex(r"\text{After L2 normalisation: all embeddings on unit hypersphere}", font_size=26, color=CYAN)
        norm_lbl.next_to(title, DOWN, buff=0.4)
        self.play(Write(norm_lbl), run_time=1.5)

        sphere = Circle(radius=2.4, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
        sphere.shift(DOWN * 0.5)
        cen = sphere.get_center()
        self.play(ShowCreation(sphere), run_time=1.0)

        np.random.seed(11)
        unit_dots = VGroup()
        for angle in np.linspace(0, 2 * PI, 20, endpoint=False):
            d = Dot(radius=0.09, color=GREEN)
            d.move_to(cen + 2.4 * np.array([np.cos(angle), np.sin(angle), 0]))
            unit_dots.add(d)
        self.play(ShowCreation(unit_dots), run_time=2.0)

        conclusion = Tex(
            r"\|f\| = 1,\;\|W\| = 1 \;\Rightarrow\; W^T f = \cos\theta",
            font_size=30, color=GREEN,
        )
        conclusion.to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion), run_time=2.0)
        self.wait(15.0)
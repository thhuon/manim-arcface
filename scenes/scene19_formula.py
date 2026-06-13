from manimlib import *
from scenes.utils import *

TARGET = 49.6

class Scene19_Formula(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{The ArcFace Formula — Step by Step}", font_size=46, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=2.0)

        # Step 1: Standard softmax inner product
        step1 = Tex(r"\text{Step 1: } W_{y_i}^T f_i = \cos\theta_{y_i}", font_size=32, color=MUTED)
        step1.shift(UP * 1.5)
        self.play(Write(step1), run_time=2.0)
        self.wait(5.0)

        # Step 2: Add margin
        step2 = Tex(r"\text{Step 2: } \cos(\theta_{y_i} + m) \;\leftarrow\;\text{add margin }m", font_size=32, color=CYAN)
        step2.next_to(step1, DOWN, buff=0.6)
        self.play(Write(step2), run_time=2.0)
        self.wait(5.0)

        # Step 3: Scale
        step3 = Tex(r"\text{Step 3: Multiply by scale } s", font_size=32, color=GREEN)
        step3.next_to(step2, DOWN, buff=0.6)
        self.play(Write(step3), run_time=2.0)
        self.wait(5.0)

        # Full formula
        full = Tex(
            r"L = -\log\frac{e^{s\cos(\theta_{y_i}+m)}}{e^{s\cos(\theta_{y_i}+m)} + \sum_{j\neq y_i}e^{s\cos\theta_j}}",
            font_size=34, color="#FFD700",
        )
        full.next_to(step3, DOWN, buff=0.7)
        rect = SurroundingRectangle(full, color="#FFD700", buff=0.15, corner_radius=0.1)
        self.play(Write(full), run_time=2.5)
        self.play(ShowCreation(rect), run_time=1.0)

        insight = Tex(
            r"\text{Margin } m \text{ pushes embeddings deeper into each class region}",
            font_size=24, color=WHITE,
        )
        insight.to_edge(DOWN, buff=0.5)
        self.play(Write(insight), run_time=2.0)
        self.wait(15.0)
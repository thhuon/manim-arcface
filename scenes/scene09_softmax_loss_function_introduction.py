from manimlib import *
from scenes.utils import *

TARGET = 47.2

class Scene09_SoftmaxLossFunctionIntroduction(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Softmax Loss Function}", font_size=52, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # Softmax formula
        formula = Tex(
            r"L = -\log\frac{e^{W_{y_i}^T f_i}}{\sum_{j=1}^{N} e^{W_j^T f_i}}",
            font_size=44, color=CYAN,
        )
        formula.move_to(UP * 0.8)
        self.play(Write(formula), run_time=2.5)

        # Explanation labels
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
            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.9)
        self.wait(10.0)

        # Geometric intuition: "pushes embedding toward class weight"
        intuition = Tex(
            r"\text{Softmax pushes embedding } f_i \text{ toward weight } W_{y_i}",
            font_size=28, color=MUTED,
        )
        intuition.to_edge(DOWN, buff=0.5)
        self.play(Write(intuition), run_time=2.0)
        self.wait(15.0)

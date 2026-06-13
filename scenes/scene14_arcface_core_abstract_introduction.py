from manimlib import *
from scenes.utils import *

TARGET = 53.6

class Scene14_ArcfaceCoreAbstractIntroduction(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{ArcFace: Core Idea}", font_size=54, color="#FFD700")
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # Central formula reveal
        formula = Tex(
            r"L = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{e^{s\cos(\theta_{y_i}+m)}}{\,e^{s\cos(\theta_{y_i}+m)} + \sum_{j \neq y_i}e^{s\cos\theta_j}\,}",
            font_size=36, color=CYAN,
        )
        formula.move_to(UP * 0.4)
        self.play(Write(formula), run_time=3.5)
        self.wait(5.0)

        # Highlight key terms one by one
        highlights = [
            (r"m = 0.5", r"\text{Angular margin (radians)}", GREEN),
            (r"s = 64", r"\text{Feature scale (radius of hypersphere)}", WHITE),
            (r"\cos(\theta_{y_i} + m)", r"\text{Cosine with margin applied}", CYAN),
        ]

        for sym, desc, col in highlights:
            sym_tex = Tex(sym, font_size=28, color=col)
            desc_tex = Tex(desc, font_size=24, color=WHITE)
            row = VGroup(sym_tex, desc_tex)
            row.arrange(RIGHT, buff=0.5)
            row.next_to(formula, DOWN, buff=0.5 + highlights.index((sym, desc, col)) * 0.8)

        # animate sequentially below formula
        y_offset = DOWN * 1.8
        for sym, desc, col in highlights:
            sym_tex = Tex(sym, font_size=26, color=col)
            desc_tex = Tex(desc, font_size=22, color=WHITE)
            row = VGroup(sym_tex, desc_tex)
            row.arrange(RIGHT, buff=0.4)
            row.next_to(formula.get_bottom(), DOWN, buff=0.3)
            row.shift(y_offset)
            self.play(FadeIn(row, shift=UP * 0.1), run_time=1.0)
            self.wait(4.0)
            y_offset += DOWN * 0.9

        self.wait(10.0)

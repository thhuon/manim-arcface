from manimlib import *
from scenes.utils import *

TARGET = 29.2

class Scene23_ArcfaceVsCosface(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{ArcFace vs.\ CosFace}", font_size=50, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # Comparison table
        rows = [
            (r"\text{Method}", r"\text{Margin Applied To}", r"\text{Formula}"),
            (r"\text{CosFace}", r"\cos\theta_{y_i}", r"\cos\theta_{y_i} - m"),
            (r"\text{ArcFace}", r"\theta_{y_i}", r"\cos(\theta_{y_i} + m)"),
        ]

        table = VGroup()
        for i, row in enumerate(rows):
            row_group = VGroup(*[Tex(t, font_size=26, color=(WHITE if i == 0 else ([MUTED, GREEN][i - 1]))) for t in row])
            row_group.arrange(RIGHT, buff=1.2)
            table.add(row_group)
        table.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        table.next_to(title, DOWN, buff=0.7)

        for row in table:
            self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.9)
            self.wait(1.5)

        # Key distinction
        distinction = Tex(
            r"\text{ArcFace margin is on }\theta\text{ — direct geometric meaning on hypersphere}",
            font_size=24, color=CYAN,
        )
        distinction.to_edge(DOWN, buff=0.5)
        self.play(Write(distinction), run_time=2.0)
        self.wait(8.0)

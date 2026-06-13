from manimlib import *
from scenes.utils import *

TARGET = 45.0

class Scene13_Transition(Scene):
    def construct(self):
        self.camera.background_color = DARK

        bridge = Tex(r"\text{From Softmax to ArcFace}", font_size=52, color=WHITE)
        bridge.move_to(UP * 1.2)
        self.play(Write(bridge), run_time=2.0)

        arrow = Arrow(UP * 0.4, DOWN * 0.4, stroke_color=CYAN, stroke_width=3)
        self.play(ShowCreation(arrow), run_time=1.0)

        key = Tex(
            r"\text{The key idea: add an angular margin } m \text{ to the angle } \theta",
            font_size=30, color=CYAN,
        )
        key.next_to(arrow, DOWN, buff=0.4)
        self.play(Write(key), run_time=2.5)
        self.wait(5.0)

        # Comparison: Softmax vs ArcFace formula
        soft_f = Tex(r"\text{Softmax: } \cos\theta_{y_i}", font_size=30, color=MUTED)
        arc_f = Tex(r"\text{ArcFace: } \cos(\theta_{y_i} + m)", font_size=30, color=GREEN)
        soft_f.shift(LEFT * 2.5 + DOWN * 2.0)
        arc_f.shift(RIGHT * 2.5 + DOWN * 2.0)
        vs = Tex(r"\rightarrow", font_size=36, color=WHITE)
        vs.shift(DOWN * 2.0)

        self.play(Write(soft_f), run_time=1.2)
        self.play(Write(vs), run_time=0.5)
        self.play(Write(arc_f), run_time=1.2)
        self.wait(15.0)
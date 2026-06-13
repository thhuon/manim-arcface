
from manimlib import *
from scenes.utils import *

class Scene13_Transition(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        title = Tex(r"\text{The Core Idea of ArcFace}", font_size=72)
        title.to_edge(UP, buff=1.0)

        embedding_space = Tex(r"\text{Embedding Space}", font_size=32)
        embedding_space.next_to(title, DOWN, buff=0.8)

        compactness = Tex(r"\text{Compactness}", font_size=24)
        compactness.next_to(embedding_space, LEFT, buff=0.5)

        separation = Tex(r"\text{Separation}", font_size=24)
        separation.next_to(embedding_space, RIGHT, buff=0.5)

        self.play(Write(title), run_time=2.0)
        self.play(Write(embedding_space), run_time=1.5)
        self.play(Write(compactness), Write(separation), run_time=1.5)

        circle = Circle(radius=1.5, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
        circle.move_to(ORIGIN)

        dot1 = Dot(radius=0.05, color=WHITE).move_to(0.5 * LEFT + 0.2 * UP)
        dot2 = Dot(radius=0.05, color=WHITE).move_to(0.5 * RIGHT + 0.2 * UP)
        dot3 = Dot(radius=0.05, color=WHITE).move_to(0.5 * LEFT + 0.2 * DOWN)
        dot4 = Dot(radius=0.05, color=WHITE).move_to(0.5 * RIGHT + 0.2 * DOWN)

        self.play(ShowCreation(circle), ShowCreation(dot1), ShowCreation(dot2), ShowCreation(dot3), ShowCreation(dot4), run_time=2.0)

        margin = Tex(r"\text{Large Margin}", font_size=24)
        margin.move_to(2.5 * RIGHT)
        self.play(Write(margin), run_time=1.5)

        self.play(FadeOut(title), FadeOut(embedding_space), FadeOut(compactness), FadeOut(separation), FadeOut(circle), FadeOut(dot1), FadeOut(dot2), FadeOut(dot3), FadeOut(dot4), FadeOut(margin), run_time=2.0)
  
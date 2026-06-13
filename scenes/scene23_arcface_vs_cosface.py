
from manimlib import *
from scenes.utils import *

class Scene23_ArcfaceVsCosface(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{ArcFace vs. CosFace}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=2)

        # Hypersphere
        hypersphere = Circle(radius=2.5, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        self.play(ShowCreation(hypersphere), run_time=2.5)

        # CosFace explanation
        cosface_text = Tex(r"\text{CosFace: Margin added to cosine value}", font_size=24, color="#cccccc")
        cosface_text.next_to(title, DOWN, buff=0.8)
        self.play(Write(cosface_text), run_time=2)

        cosface_illustration = VGroup(
            Line(ORIGIN, RIGHT * 2.5, stroke_color=WHITE, stroke_width=1.5),
            Tex(r"\theta", font_size=24).move_to(RIGHT * 2.5 + 0.2 * UP),
            Tex(r"\cos(\theta)", font_size=24).move_to(RIGHT * 1.5 + 0.2 * UP),
            Tex(r"\cos(\theta) - m", font_size=24).move_to(RIGHT * 1.5 + 0.2 * DOWN)
        )
        cosface_illustration.next_to(cosface_text, DOWN, buff=0.5)
        self.play(ShowCreation(cosface_illustration), run_time=2.5)

        # ArcFace explanation
        arcface_text = Tex(r"\text{ArcFace: Margin added to angle } \theta", font_size=24, color="#cccccc")
        arcface_text.next_to(cosface_text, DOWN, buff=0.8)
        self.play(Write(arcface_text), run_time=2)

        arcface_illustration = VGroup(
            Line(ORIGIN, RIGHT * 2.5, stroke_color=WHITE, stroke_width=1.5),
            Tex(r"\theta", font_size=24).move_to(RIGHT * 2.5 + 0.2 * UP),
            Tex(r"\theta + m", font_size=24).move_to(RIGHT * 1.5 + 0.2 * UP)
        )
        arcface_illustration.next_to(arcface_text, DOWN, buff=0.5)
        self.play(ShowCreation(arcface_illustration), run_time=2.5)

        # Conclusion
        conclusion = Tex(r"\text{ArcFace has a clearer geometric meaning}", font_size=24, color="#cccccc")
        conclusion.next_to(arcface_text, DOWN, buff=0.8)
        self.play(Write(conclusion), run_time=2)

        self.wait(2)

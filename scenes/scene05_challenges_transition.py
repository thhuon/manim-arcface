from manimlib import *
from scenes.utils import *

TARGET = 37.4

class Scene05_ChallengesTransition(Scene):
    def construct(self):
        self.camera.background_color = DARK

        # Bridge: from challenges → solution
        prob_text = Tex(r"\text{The Problem:}", font_size=44, color="#FF4444")
        prob_text.shift(UP * 1.5)

        prob_body = Tex(
            r"\text{Traditional methods struggle with variability,}\\"
            r"\text{low accuracy, and poor generalisation}",
            font_size=28, color=WHITE,
        )
        prob_body.next_to(prob_text, DOWN, buff=0.5)

        self.play(Write(prob_text), run_time=1.5)
        self.play(Write(prob_body), run_time=2.5)
        self.wait(6.0)

        # Arrow transition
        arr = Arrow(ORIGIN, DOWN * 1.2, stroke_color=CYAN, stroke_width=3)
        arr.next_to(prob_body, DOWN, buff=0.5)
        self.play(ShowCreation(arr), run_time=1.0)

        sol_text = Tex(r"\text{The Solution: embedding-based metric learning}", font_size=32, color=CYAN)
        sol_text.next_to(arr, DOWN, buff=0.3)
        self.play(Write(sol_text), run_time=2.0)
        self.wait(5.0)

        # Geometric teaser
        teaser = Tex(
            r"\text{Instead of raw pixel comparison, map faces to a}\\"
            r"\text{high-dimensional geometric space}",
            font_size=26, color=MUTED,
        )
        teaser.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(teaser, shift=UP * 0.1), run_time=2.0)
        self.wait(10.0)
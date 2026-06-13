from manimlib import *
from scenes.utils import *

TARGET = 37.8

class Scene24_ClassificationBasedMetricLearningExplainWhyArcfaceIsMorePracticalThanFacenettripletLoss(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{ArcFace vs.\ Triplet Loss}", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # Triplet loss problems
        triplet_label = Tex(r"\text{Triplet Loss Challenges:}", font_size=30, color=MUTED)
        triplet_label.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        self.play(Write(triplet_label), run_time=1.2)

        triplet_items = [
            r"\bullet\;\text{Requires careful triplet mining}",
            r"\bullet\;\text{Unstable training}",
            r"\bullet\;\text{Slow convergence}",
        ]
        t_group = VGroup(*[Tex(t, font_size=26, color=MUTED) for t in triplet_items])
        t_group.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        t_group.next_to(triplet_label, DOWN, buff=0.4)
        t_group.to_edge(LEFT, buff=1.0)
        for item in t_group:
            self.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.8)

        self.wait(5.0)

        # Arrow to ArcFace
        divider = DashedLine(UP * 1, DOWN * 1.8, stroke_color=MUTED, stroke_width=1.5)
        divider.shift(RIGHT * 0.2)
        self.play(ShowCreation(divider), run_time=0.8)

        arc_label = Tex(r"\text{ArcFace Advantages:}", font_size=30, color=CYAN)
        arc_label.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.8)
        self.play(Write(arc_label), run_time=1.2)

        arc_items = [
            r"\bullet\;\text{No triplet mining needed}",
            r"\bullet\;\text{Every batch contributes}",
            r"\bullet\;\text{Stable and scalable}",
        ]
        a_group = VGroup(*[Tex(t, font_size=26, color=CYAN) for t in arc_items])
        a_group.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        a_group.next_to(arc_label, DOWN, buff=0.4)
        a_group.to_edge(RIGHT, buff=1.0)
        for item in a_group:
            self.play(FadeIn(item, shift=LEFT * 0.1), run_time=0.8)

        self.wait(8.0)

        bottom = Tex(r"\text{Classification-based metric learning = best of both worlds}", font_size=24, color=GREEN)
        bottom.to_edge(DOWN, buff=0.5)
        self.play(Write(bottom), run_time=2.0)
        self.wait(5.0)

from manimlib import *
from scenes.utils import *

class Scene16_ArcfaceCore2dVisualComparison(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Softmax 2D embeddings
        softmax_embeddings = VGroup(
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(2 * LEFT),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(LEFT),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(ORIGIN),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(RIGHT),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(2 * RIGHT)
        )
        softmax_boundary = Line(LEFT * 3, RIGHT * 3, stroke_color=GREY, stroke_width=1.5)
        softmax_label = Tex(r"\text{Softmax}", font_size=24).next_to(softmax_boundary, UP)

        # ArcFace 2D embeddings
        arcface_embeddings = VGroup(
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(2 * LEFT + 1 * UP),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(LEFT + 1 * UP),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(ORIGIN + 1 * UP),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(RIGHT + 1 * UP),
            Circle(radius=0.2, stroke_color=WHITE, stroke_width=2, fill_opacity=0).move_to(2 * RIGHT + 1 * UP)
        )
        arcface_boundary = Line(LEFT * 3 + 1 * UP, RIGHT * 3 + 1 * UP, stroke_color=GREY, stroke_width=1.5)
        arcface_label = Tex(r"\text{ArcFace}", font_size=24).next_to(arcface_boundary, UP)

        # Comparison
        comparison = VGroup(softmax_embeddings, softmax_boundary, softmax_label, arcface_embeddings, arcface_boundary, arcface_label)
        comparison.arrange(RIGHT, buff=1.5)

        self.play(
            ShowCreation(softmax_embeddings),
            ShowCreation(softmax_boundary),
            Write(softmax_label),
            run_time=2
        )

        self.play(
            Transform(softmax_embeddings, arcface_embeddings),
            Transform(softmax_boundary, arcface_boundary),
            Transform(softmax_label, arcface_label),
            run_time=2
        )

        self.play(
            FadeOut(comparison),
            run_time=1
        )

        # 3D transition hint
        cube = Cube().scale(0.5).move_to(ORIGIN)
        self.play(
            ShowCreation(cube),
            run_time=2
        )
    
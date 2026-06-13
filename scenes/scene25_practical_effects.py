
from manimlib import *
from scenes.utils import *

class Scene25_PracticalEffects(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Create title
        title = Tex(r"\text{Practical Effects of ArcFace}", font_size=72)
        title.to_edge(UP, buff=1.0)

        # Create softmax and ArcFace labels
        softmax_label = Tex(r"\text{Standard Softmax}", font_size=32)
        arcface_label = Tex(r"\text{ArcFace}", font_size=32)

        # Create left and right groups for comparison
        left_group = VGroup()
        right_group = VGroup()

        # Softmax cluster
        softmax_cluster = VGroup(
            Circle(radius=0.5, stroke_color=WHITE, stroke_width=2, fill_opacity=0),
            Dot(point=LEFT * 1.5 + UP * 0.5, radius=0.05, color=WHITE),
            Dot(point=ORIGIN, radius=0.05, color=WHITE),
            Dot(point=RIGHT * 1.5 + UP * 0.5, radius=0.05, color=WHITE),
            Dot(point=LEFT * 1.0 + DOWN * 0.5, radius=0.05, color=WHITE),
            Dot(point=RIGHT * 1.0 + DOWN * 0.5, radius=0.05, color=WHITE)
        )
        softmax_cluster.move_to(left_group)

        # ArcFace cluster
        arcface_cluster = VGroup(
            Circle(radius=0.5, stroke_color=WHITE, stroke_width=2, fill_opacity=0),
            Dot(point=LEFT * 2.5 + UP * 0.5, radius=0.05, color=WHITE),
            Dot(point=LEFT * 1.0 + UP * 0.5, radius=0.05, color=WHITE),
            Dot(point=ORIGIN, radius=0.05, color=WHITE),
            Dot(point=RIGHT * 1.0 + UP * 0.5, radius=0.05, color=WHITE),
            Dot(point=RIGHT * 2.5 + UP * 0.5, radius=0.05, color=WHITE)
        )
        arcface_cluster.move_to(right_group)

        # Decision boundary lines
        softmax_boundary = Line(left_group.get_corner(DL), left_group.get_corner(UR), stroke_color=GREY, stroke_width=1.5)
        arcface_boundary = Line(right_group.get_corner(DL), right_group.get_corner(UR), stroke_color=GREY, stroke_width=1.5)

        left_group.add(softmax_cluster, softmax_boundary, softmax_label)
        right_group.add(arcface_cluster, arcface_boundary, arcface_label)

        # Initial centered view
        comparison_group = VGroup(left_group, right_group)
        comparison_group.arrange(RIGHT, buff=1.5)
        comparison_group.move_to(ORIGIN)

        self.play(FadeIn(title), run_time=1.0)
        self.play(ShowCreation(comparison_group), run_time=2.0)

        # Split view
        self.play(
            left_group.animate.move_to([-2.5, 0, 0]),
            right_group.animate.move_to([2.5, 0, 0]),
            rate_func=smooth,
            run_time=2.5
        )

        # Pan and zoom
        frame = self.camera.frame
        self.play(
            frame.animate.scale(1.3),
            rate_func=smooth,
            run_time=2.5
        )

        # Gentle pan between the two sides
        self.play(
            frame.animate.shift(LEFT * 1.5),
            rate_func=smooth,
            run_time=1.5
        )
        self.play(
            frame.animate.shift(RIGHT * 3.0),
            rate_func=smooth,
            run_time=1.5
        )

        # Keep camera still
        self.wait(2.0)

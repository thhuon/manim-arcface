
from manimlib import *
from scenes.utils import *

class Scene19_Formula(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Introduction
        title = Tex(r"\text{ArcFace: Stricter Angle Condition}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=1.5)

        # Standard Softmax Explanation
        embedding = Dot(ORIGIN, radius=0.05, color=WHITE)
        class_A = Dot(RIGHT * 2, radius=0.05, color=WHITE)
        class_B = Dot(LEFT * 2, radius=0.05, color=WHITE)
        angle_A = Line(embedding.get_center(), class_A.get_center(), stroke_color=WHITE, stroke_width=1.5)
        angle_B = Line(embedding.get_center(), class_B.get_center(), stroke_color=WHITE, stroke_width=1.5)

        softmax_group = VGroup(embedding, class_A, class_B, angle_A, angle_B)
        softmax_group.arrange(RIGHT, buff=0.5)

        self.play(
            ShowCreation(embedding),
            ShowCreation(class_A),
            ShowCreation(class_B),
            ShowCreation(angle_A),
            ShowCreation(angle_B),
            run_time=2.0
        )

        # Narration: Standard softmax compares cosine values
        narration = Tex(r"\text{Standard Softmax: } \cos(\theta_A) > \cos(\theta_B)", font_size=28)
        narration.next_to(softmax_group, DOWN, buff=0.5)
        self.play(Write(narration), run_time=1.5)

        # ArcFace Explanation
        arcface_group = softmax_group.copy()
        correct_class = arcface_group[1]
        incorrect_class = arcface_group[2]

        margin = 0.5
        arcface_angle = Line(embedding.get_center(), correct_class.get_center(), stroke_color=CYAN, stroke_width=1.5)
        arcface_group.add(arcface_angle)

        self.play(
            Transform(arcface_group[3], arcface_angle),
            run_time=1.5
        )

        # Narration: ArcFace uses cos(theta + m)
        arcface_narration = Tex(r"\text{ArcFace: } \cos(\theta + m)", font_size=28)
        arcface_narration.next_to(arcface_group, DOWN, buff=0.5)
        self.play(Write(arcface_narration), run_time=1.5)

        # Conclusion
        conclusion = Tex(r"\text{Stricter Condition for Correct Classification}", font_size=36)
        conclusion.to_edge(DOWN, buff=1.0)
        self.play(Write(conclusion), run_time=1.5)

        self.wait(2.0)
    
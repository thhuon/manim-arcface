
from manimlib import *
from scenes.utils import *

class Scene10_SoftmaxConcept(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Softmax formula
        formula = Tex(r"\text{softmax}(z) = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}", font_size=72)
        formula.move_to(ORIGIN)
        self.play(Write(formula), run_time=2)

        # Zoom into the numerator
        numerator = Tex(r"e^{z_i}", font_size=72)
        numerator.move_to(formula.get_part_by_tex("e^{z_i}").get_center())
        self.play(TransformMatchingShapes(formula.get_part_by_tex("e^{z_i}"), numerator), run_time=1.5)

        # Zoom into the denominator
        denominator = Tex(r"\sum_{j=1}^{K} e^{z_j}", font_size=72)
        denominator.move_to(formula.get_part_by_tex("\sum_{j=1}^{K} e^{z_j}").get_center())
        self.play(TransformMatchingShapes(formula.get_part_by_tex("\sum_{j=1}^{K} e^{z_j}"), denominator), run_time=1.5)

        # Transition to 2D plane view
        self.play(FadeOut(formula), run_time=1)

        # 2D plane view
        plane = Rectangle(width=10, height=6, fill_opacity=0, stroke_color=WHITE, stroke_width=1)
        plane.move_to(ORIGIN)
        self.play(ShowCreation(plane), run_time=2)

        # Identity classes as vectors
        identity_vectors = VGroup()
        for i in range(5):
            vector = Line(ORIGIN, RIGHT * 2, stroke_color=CYAN, stroke_width=2)
            vector.rotate(PI * i / 2)
            identity_vectors.add(vector)
        identity_vectors.arrange(RIGHT, buff=1.5)
        identity_vectors.move_to(ORIGIN)
        self.play(ShowCreation(identity_vectors), run_time=2)

        # Embedding vector
        embedding_vector = Line(ORIGIN, UP * 2, stroke_color=WHITE, stroke_width=2)
        self.play(ShowCreation(embedding_vector), run_time=1.5)

        # Decision boundary
        decision_boundary = Line(LEFT * 5, RIGHT * 5, stroke_color=GREY, stroke_width=1, stroke_opacity=0.5)
        decision_boundary.move_to(ORIGIN)
        self.play(ShowCreation(decision_boundary), run_time=1.5)

        # Probability distribution
        probabilities = VGroup()
        for i in range(5):
            dot = Dot(radius=0.1, color=CYAN)
            dot.move_to(identity_vectors[i].get_end())
            probabilities.add(dot)
        probabilities.arrange(RIGHT, buff=0.5)
        probabilities.move_to(UP * 3)
        self.play(ShowCreation(probabilities), run_time=2)

        self.wait(2)
    
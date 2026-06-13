from manimlib import *
from scenes.utils import *

TARGET = 38.5

class Scene26_InferenceStage(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Inference Stage}", font_size=52, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # Pipeline: new face → embedding → compare → decision
        new_face = make_abstract_face()
        new_face.scale(1.2).shift(LEFT * 4.5)

        nn = make_neural_network()
        nn.scale(1.1).shift(LEFT * 1.5)

        vec_new = make_vector([r"f_\text{new}"], font_size=22)
        vec_new.shift(RIGHT * 0.8)

        db_box = make_box([r"\text{Face Database}", r"\text{(stored embeddings)}"], width=2.8, height=1.5, stroke=MUTED, font_size=22)
        db_box.shift(RIGHT * 4.0)

        arr1 = Arrow(new_face.get_right(), nn.get_left(), stroke_color=CYAN, stroke_width=2)
        arr2 = Arrow(nn.get_right(), vec_new.get_left(), stroke_color=CYAN, stroke_width=2)
        arr3 = Arrow(vec_new.get_right(), db_box.get_left(), stroke_color=CYAN, stroke_width=2)

        self.play(ShowCreation(new_face), run_time=1.0)
        self.play(ShowCreation(nn), ShowCreation(arr1), run_time=1.0)
        self.play(FadeIn(vec_new), ShowCreation(arr2), run_time=0.8)
        self.play(FadeIn(db_box), ShowCreation(arr3), run_time=1.0)
        self.wait(4.0)

        # Decision
        cos_score = Tex(r"\cos\theta = \frac{f_\text{new} \cdot f_\text{stored}}{\|f_\text{new}\|\|f_\text{stored}\|}", font_size=30, color=GREEN)
        cos_score.shift(DOWN * 1.5)
        self.play(Write(cos_score), run_time=2.0)
        self.wait(3.0)

        decision_yes = Tex(r"\cos\theta > \tau \;\Rightarrow\;\text{SAME person}", font_size=26, color=GREEN)
        decision_no = Tex(r"\cos\theta \leq \tau \;\Rightarrow\;\text{DIFFERENT person}", font_size=26, color="#FF4444")
        decision_yes.shift(DOWN * 2.4 + LEFT * 1.5)
        decision_no.shift(DOWN * 2.9 + LEFT * 1.5)

        self.play(Write(decision_yes), run_time=1.2)
        self.play(Write(decision_no), run_time=1.2)
        self.wait(10.0)

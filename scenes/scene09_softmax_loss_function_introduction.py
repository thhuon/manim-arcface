
from manimlib import *
from scenes.utils import *

class Scene09_SoftmaxLossFunctionIntroduction(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Softmax Loss Function Introduction}", font_size=72)
        title.to_edge(UP, buff=1.0)

        # Loss Function Definition
        loss_def = Tex(r"\text{Loss Function:} \\ f(y, \hat{y}) = -\sum_{i=1}^{n} y_i \log(\hat{y}_i)", font_size=48)
        loss_def.next_to(title, DOWN, buff=0.8)

        # Neural Network and Prediction
        neural_network = make_neural_network()
        neural_network.next_to(loss_def, RIGHT, buff=1.2)
        prediction = Tex(r"\hat{y}", font_size=36)
        prediction.next_to(neural_network, RIGHT, buff=0.2)

        # True Result
        true_result = Tex(r"y", font_size=36)
        true_result.next_to(neural_network, LEFT, buff=0.2)

        # Loss Minimization
        loss_minimization = Tex(r"\text{Minimize Loss}", font_size=36)
        loss_minimization.next_to(loss_def, DOWN, buff=0.6)

        # Softmax Introduction
        softmax_intro = Tex(r"\text{Softmax:} \\ \sigma(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{n} e^{z_j}}", font_size=48)
        softmax_intro.next_to(loss_minimization, DOWN, buff=0.8)

        # Animation
        self.play(Write(title), run_time=2)
        self.play(Write(loss_def), run_time=2)
        self.play(ShowCreation(neural_network), run_time=1.5)
        self.play(Write(prediction), run_time=1)
        self.play(Write(true_result), run_time=1)
        self.play(Write(loss_minimization), run_time=2)
        self.play(Write(softmax_intro), run_time=2)

        self.wait(2)

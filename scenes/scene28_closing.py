
from manimlib import *
from scenes.utils import *

class Scene28_Closing(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Create an embedding space
        embedding_space = VGroup()
        dots = VGroup()
        for _ in range(10):
            dot = Dot(radius=0.05, color=WHITE)
            dot.shift(np.random.uniform(-2, 2) * RIGHT + np.random.uniform(-2, 2) * UP)
            dots.add(dot)
        embedding_space.add(dots)

        # Create a neural network
        neural_network = make_neural_network()
        neural_network.to_edge(UP, buff=2)

        # Initial zoomed-in view
        zoomed_in_view = embedding_space.copy()
        zoomed_in_view.move_to(ORIGIN)

        # Zoom out to reveal the entire embedding space
        self.play(FadeIn(zoomed_in_view), run_time=1)
        self.play(zoomed_in_view.animate.scale(2), run_time=2)

        # Zoom out to reveal the neural network
        self.play(zoomed_in_view.animate.scale(1.5), neural_network.animate.shift(DOWN * 2), run_time=2)

        # Final zoom out
        self.play(zoomed_in_view.animate.scale(1.5), neural_network.animate.shift(DOWN * 3), run_time=2)

        # Fade to black
        self.play(FadeOut(zoomed_in_view), FadeOut(neural_network), run_time=1)

        # End screen
        end_screen = Tex(r"\text{Thank you for watching!}", font_size=48)
        end_screen.move_to(ORIGIN)
        self.play(Write(end_screen), run_time=2)
        self.play(FadeOut(end_screen), run_time=1)

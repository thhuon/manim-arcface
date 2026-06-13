from manimlib import *
from scenes.utils import *

TARGET = 24.3

class Scene28_Closing(Scene):
    def construct(self):
        self.camera.background_color = DARK

        # Final embedding space reveal
        sphere = Circle(radius=2.4, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
        sphere.shift(DOWN * 0.5)
        center = sphere.get_center()

        np.random.seed(99)
        colours = [CYAN, GREEN, "#FF4444", "#FFD700"]
        bases = [PI / 5, 2 * PI / 3, -PI / 3, PI + PI / 4]
        dots = VGroup()
        for angle_base, col in zip(bases, colours):
            for _ in range(8):
                a = angle_base + np.random.uniform(-0.18, 0.18)
                r = np.random.uniform(2.1, 2.4)
                d = Dot(radius=0.10, color=col)
                d.move_to(center + r * np.array([np.cos(a), np.sin(a), 0]))
                dots.add(d)

        nn = make_neural_network()
        nn.scale(1.2).shift(UP * 2.5)

        self.play(ShowCreation(nn), run_time=1.5)
        self.play(ShowCreation(sphere), run_time=1.0)
        self.play(ShowCreation(dots), run_time=1.5)
        self.wait(2.0)

        # Zoom out
        self.play(self.camera.frame.animate.scale(1.15), run_time=1.5)

        # Closing words
        closing = Tex(
            r"\text{From pixels } \rightarrow \text{ geometry } \rightarrow \text{ identity}",
            font_size=34, color=WHITE,
        )
        closing.to_edge(DOWN, buff=0.8)
        self.play(Write(closing), run_time=2.0)
        self.wait(3.0)

        thankyou = Tex(r"\text{Thank you for watching!}", font_size=44, color="#FFD700")
        thankyou.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(closing), FadeIn(thankyou, shift=UP * 0.2), run_time=1.5)
        self.wait(4.0)

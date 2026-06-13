
from manimlib import *
from scenes.utils import *

class Scene17_ArcfaceCoreTransition(Scene):
    def construct(self):
        self.camera.background_color = '#111111'

        # Title and Subtitle
        title = Tex(r'\text{ArcFace Core: Embeddings on a Hypersphere}', font_size=72)
        subtitle = Tex(r'\text{Normalized Embeddings }', font_size=32)
        title_block = VGroup(title, subtitle)
        title_block.arrange(DOWN, buff=0.4)
        title_block.to_edge(UP, buff=1.0)

        # Hypersphere Visualization
        sphere = Circle(radius=2.0, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        self.play(ShowCreation(sphere), run_time=2.5)

        # Embeddings (Points on the Sphere)
        embeddings = VGroup(
            Dot(point=2.0 * RIGHT, radius=0.08, color=CYAN),
            Dot(point=2.0 * LEFT + 0.5 * UP, radius=0.08, color=CYAN),
            Dot(point=2.0 * LEFT + 0.5 * DOWN, radius=0.08, color=CYAN),
            Dot(point=2.0 * UP, radius=0.08, color=CYAN),
            Dot(point=2.0 * DOWN, radius=0.08, color=CYAN),
        )
        self.play(ShowCreation(embeddings), run_time=2.0)

        # Lines connecting embeddings to center
        center = Dot(point=ORIGIN, radius=0.08, color=WHITE)
        lines = VGroup(
            Line(center.get_center(), embeddings[0].get_center(), stroke_color=WHITE, stroke_width=0.7),
            Line(center.get_center(), embeddings[1].get_center(), stroke_color=WHITE, stroke_width=0.7),
            Line(center.get_center(), embeddings[2].get_center(), stroke_color=WHITE, stroke_width=0.7),
            Line(center.get_center(), embeddings[3].get_center(), stroke_color=WHITE, stroke_width=0.7),
            Line(center.get_center(), embeddings[4].get_center(), stroke_color=WHITE, stroke_width=0.7),
        )
        self.play(ShowCreation(lines), run_time=2.0)

        # Narration and Fade
        self.play(FadeOut(title_block), run_time=1.5)
        self.wait(2)
    
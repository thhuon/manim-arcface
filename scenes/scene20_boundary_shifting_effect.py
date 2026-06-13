
from manimlib import *
from scenes.utils import *

class Scene20_BoundaryShiftingEffect(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Boundary Shifting Effect in ArcFace}", font_size=72)
        title.to_edge(UP, buff=1.0)

        # Softmax boundary explanation
        softmax_boundary = Tex(r"\text{Softmax: Embedding just needs to be on the correct side}", font_size=32)
        softmax_boundary.next_to(title, DOWN, buff=0.8)

        # Draw softmax boundary
        softmax_line = Line(LEFT * 3, RIGHT * 3, stroke_color=WHITE, stroke_width=1.5)
        softmax_line.next_to(softmax_boundary, DOWN, buff=0.5)

        # ArcFace boundary explanation
        arcface_boundary = Tex(r"\text{ArcFace: Embedding must move deeper into the correct region}", font_size=32)
        arcface_boundary.next_to(softmax_boundary, DOWN, buff=0.8)

        # Draw ArcFace boundary
        arcface_line = Line(LEFT * 2.5, RIGHT * 2.5, stroke_color=CYAN, stroke_width=1.5, stroke_opacity=0.7)
        arcface_line.next_to(arcface_boundary, DOWN, buff=0.5)

        # Buffer zone explanation
        buffer_zone = Tex(r"\text{Additional buffer zone between classes}", font_size=32)
        buffer_zone.next_to(arcface_line, DOWN, buff=0.8)

        # Draw buffer zone
        buffer_zone_rect = Rectangle(width=1.0, height=0.2, stroke_color=WHITE, stroke_width=1.5, fill_color=WHITE, fill_opacity=0.2)
        buffer_zone_rect.next_to(arcface_line, DOWN, buff=0.5)

        # Animation
        self.play(Write(title), run_time=2)
        self.play(Write(softmax_boundary), run_time=2)
        self.play(ShowCreation(softmax_line), run_time=2)
        self.play(Write(arcface_boundary), run_time=2)
        self.play(ShowCreation(arcface_line), run_time=2)
        self.play(Write(buffer_zone), run_time=2)
        self.play(ShowCreation(buffer_zone_rect), run_time=2)

        self.wait(2)
    
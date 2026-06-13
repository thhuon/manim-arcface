
from manimlib import *
from scenes.utils import *

class Scene14_ArcfaceCoreAbstractIntroduction(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{ArcFace Core: Abstract Introduction}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=2.0)

        # ArcFace concept
        arcface_concept = Tex(r"\text{ArcFace: Enhance embedding separation}", font_size=48)
        arcface_concept.next_to(title, DOWN, buff=0.8)
        self.play(Write(arcface_concept), run_time=1.8)

        # Embedding space
        embedding_space = Tex(r"\text{Embedding Space}", font_size=48)
        embedding_space.next_to(arcface_concept, DOWN, buff=0.6)
        self.play(Write(embedding_space), run_time=1.5)

        # Angular margin concept
        angular_margin = Tex(r"\text{Angular Margin: Sufficiently different}", font_size=48)
        angular_margin.next_to(embedding_space, DOWN, buff=0.6)
        self.play(Write(angular_margin), run_time=2.0)

        # Camera movement
        self.camera.frame.shift(UP * 0.5)
        self.wait(2.0)
        self.camera.frame.shift(DOWN * 0.5)

        # Pan to left and right
        self.camera.frame.shift(LEFT * 1.0)
        self.wait(2.0)
        self.camera.frame.shift(RIGHT * 2.0)
        self.wait(2.0)
        self.camera.frame.shift(LEFT * 1.0)

        # End screen
        end_screen = Tex(r"\text{Scene 14: ArcFace Core}", font_size=48)
        end_screen.to_edge(DOWN, buff=1.0)
        self.play(Write(end_screen), run_time=1.5)
        self.wait(1.0)

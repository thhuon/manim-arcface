
from manimlib import *
from scenes.utils import *

class Scene15_ArcfaceCoreWhyAngle(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Why Angle?}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=2.0)

        # Subtitle
        subtitle = Tex(r"\text{Euclidean Distance vs. Angular Distance}", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(subtitle), run_time=1.8)

        # Face images
        face_A = ImageMobject(asset_path("face_A.png")).set_height(1.5)
        face_B = ImageMobject(asset_path("face_B.png")).set_height(1.5)
        face_A.move_to(LEFT * 2.5)
        face_B.move_to(RIGHT * 2.5)
        self.play(FadeIn(face_A), FadeIn(face_B), run_time=1.5)

        # Embeddings
        embedding_A = Dot(radius=0.05, color=WHITE).move_to(face_A.get_center() + DOWN * 1.5)
        embedding_B = Dot(radius=0.05, color=WHITE).move_to(face_B.get_center() + DOWN * 1.5)
        self.play(FadeIn(embedding_A), FadeIn(embedding_B), run_time=1.2)

        # Euclidean distance
        euclidean_distance = Line(embedding_A.get_center(), embedding_B.get_center(), stroke_color=WHITE, stroke_width=1.5)
        self.play(ShowCreation(euclidean_distance), run_time=1.5)
        euclidean_label = Tex(r"\text{Euclidean Distance}", font_size=24).next_to(euclidean_distance, DOWN, buff=0.2)
        self.play(Write(euclidean_label), run_time=1.2)

        # Angular distance
        angular_distance = DashedLine(embedding_A.get_center(), embedding_B.get_center(), stroke_color=CYAN, stroke_width=1.5, positive_space_ratio=0.5)
        self.play(ShowCreation(angular_distance), run_time=1.8)
        angular_label = Tex(r"\text{Angular Distance}", font_size=24).next_to(angular_distance, DOWN, buff=0.2)
        self.play(Write(angular_label), run_time=1.5)

        # Why angular distance?
        explanation = Tex(r"\text{Direction is more stable than magnitude}", font_size=28)
        explanation.move_to(ORIGIN)
        self.play(Write(explanation), run_time=2.5)

        # Closing
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(face_A), FadeOut(face_B), 
                  FadeOut(embedding_A), FadeOut(embedding_B), FadeOut(euclidean_distance), 
                  FadeOut(euclidean_label), FadeOut(angular_distance), FadeOut(angular_label), 
                  FadeOut(explanation), run_time=2.0)

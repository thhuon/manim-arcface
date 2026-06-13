
from manimlib import *
from scenes.utils import *

class Scene24_ClassificationBasedMetricLearningExplainWhyArcfaceIsMorePracticalThanFacenettripletLoss(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        title = Tex(r"\text{Classification-Based Metric Learning: Why ArcFace Excels}", font_size=72)
        title.to_edge(UP, buff=1.0)

        # Introduction to ArcFace and FaceNet/Triplet Loss
        arcface_icon = white_svg("face-id.svg", height=1.5)
        arcface_icon.next_to(title, DOWN, buff=0.5)

        facenet_icon = ImageMobject(asset_path("face_24.png")).set_height(1.5)
        facenet_icon.next_to(arcface_icon, RIGHT, buff=0.8)

        triplet_loss_icon = Tex(r"\text{Triplet Loss}", font_size=36)
        triplet_loss_icon.next_to(facenet_icon, RIGHT, buff=0.8)

        self.play(ShowCreation(title), ShowCreation(arcface_icon), ShowCreation(facenet_icon), ShowCreation(triplet_loss_icon))

        # Explain Triplet Loss limitations
        triplet_loss_text = Tex(r"\text{Triplet Loss requires manual selection of difficult triplets}", font_size=28)
        triplet_loss_text.next_to(triplet_loss_icon, DOWN, buff=0.5)

        self.play(Write(triplet_loss_text))

        # Introduce ArcFace advantages
        arcface_text = Tex(r"\text{ArcFace uses classification-based metric learning}", font_size=28)
        arcface_text.next_to(arcface_icon, DOWN, buff=0.5)

        self.play(Write(arcface_text))

        # Highlight ArcFace's stability and scalability
        stability_text = Tex(r"\text{More stable and scalable training process}", font_size=28)
        stability_text.next_to(arcface_text, DOWN, buff=0.5)

        self.play(Write(stability_text))

        self.wait(2)
    
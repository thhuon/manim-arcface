
from manimlib import *
from scenes.utils import *

class Scene29_Scene29(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title screen
        title = Tex(r"\text{Understanding ArcFace}", font_size=72)
        subtitle = Tex(r"\text{The Geometry of Face Recognition}", font_size=32)
        title_block = VGroup(title, subtitle)
        title_block.arrange(DOWN, buff=0.4)
        title_block.to_edge(UP, buff=1.0)
        self.play(Write(title), Write(subtitle))
        self.wait(2)

        # Simple face recognition diagram
        face = make_abstract_face().scale(0.8)
        face.shift(UP * 2)
        self.play(ShowCreation(face))

        # Add landmarks
        landmarks = make_landmarks()
        landmarks.shift(UP * 2)
        self.play(ShowCreation(landmarks))

        # Transition to ArcFace explanation
        arcface_text = Tex(r"\text{ArcFace: A Deep Face Recognition Approach}", font_size=36)
        arcface_text.shift(DOWN * 2)
        self.play(Write(arcface_text))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(face), FadeOut(landmarks), FadeOut(arcface_text))
    
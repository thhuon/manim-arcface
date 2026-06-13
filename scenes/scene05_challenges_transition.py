
from manimlib import *
from scenes.utils import *

class Scene05_ChallengesTransition(Scene):
    def construct(self):
        # Create a grid of face images
        face_grid = Group()
        face_images = [
            ImageMobject(asset_path('face_23.png')),
            ImageMobject(asset_path('face_C.png')),
            ImageMobject(asset_path('face_14.png')),
            ImageMobject(asset_path('face_26.png')),
            ImageMobject(asset_path('face_41.png')),
            ImageMobject(asset_path('face_42.png')),
            ImageMobject(asset_path('face_15.png')),
            ImageMobject(asset_path('face_2.png')),
        ]
        for face in face_images:
            face.set_height(1.5)
        face_grid = Group(*face_images)
        face_grid.arrange(RIGHT, buff=0.5)
        face_grid.arrange(DOWN, buff=0.5)
        face_grid.move_to(ORIGIN)

        # Zoom into each face image
        self.play(FadeIn(face_grid))
        for face in face_images:
            self.play(self.camera.frame.animate.move_to(face).set_width(face.get_width() * 1.2), run_time=2)

        # Transition to embedding space explanation
        embedding_space_text = Tex(r'\text{Embedding Space}', font_size=48)
        embedding_space_text.move_to(UP * 2)
        self.play(FadeOut(face_grid), ShowCreation(embedding_space_text), run_time=2)
        self.wait(2)

        # Explain embedding space concept
        embedding_space_explanation = Tex(r'\text{A way to represent faces such that different images of the same person produce nearby representations, while faces of different people produce representations that are sufficiently distinct.}', font_size=24)
        embedding_space_explanation.move_to(DOWN * 2)
        self.play(ShowCreation(embedding_space_explanation), run_time=3)
        self.wait(2)

        # Transition to next scene
        self.play(FadeOut(embedding_space_text), FadeOut(embedding_space_explanation), run_time=2)


from manimlib import *
from scenes.utils import *

class Scene06_EmbeddingSpaceCityMapAnalogy(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Load face image
        face_img = ImageMobject(asset_path("face_23.png"))

        # Create city map analogy title
        title = Tex(r"\text{City Map Analogy}", font_size=32)
        title.to_edge(UP, buff=1.0)

        # Introduce face image
        self.play(FadeIn(face_img), run_time=1.5)
        self.play(FadeIn(title), run_time=1.5)

        # Zoom in and morph face into a point
        point = Dot(radius=0.05, color=WHITE)
        point.move_to(face_img.get_center())
        self.play(FadeOut(face_img), ShowCreation(point), run_time=2.0)

        # Create embedding space plane
        plane = Rectangle(width=6.0, height=4.0, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        plane.move_to(ORIGIN)
        self.play(ShowCreation(plane), run_time=2.0)

        # Add glowing effect to point
        glow = glow_copy(point, color=CYAN, width=7, opacity=0.18)
        self.add(glow)

        # Pan camera to show clusters
        self.camera.rotation = 40 * DEGREES
        clusters = VGroup(
            Dot(radius=0.05, color=CYAN).move_to(1.5 * LEFT + 0.5 * UP),
            Dot(radius=0.05, color=CYAN).move_to(1.5 * LEFT + 0.5 * DOWN),
            Dot(radius=0.05, color=CYAN).move_to(1.5 * RIGHT + 0.5 * UP),
            Dot(radius=0.05, color=CYAN).move_to(1.5 * RIGHT + 0.5 * DOWN),
        )
        self.play(ShowCreation(clusters), run_time=2.5)

        # Narration and outro
        self.wait(2.0)


from manimlib import *
from scenes.utils import *

class Scene11_SoftmaxLimitation(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Initial clusters
        clusters = VGroup()
        for i in range(5):
            cluster = VGroup(*[Circle(radius=0.15, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0) for _ in range(5)])
            cluster.arrange(RIGHT, buff=0.4)
            cluster.shift(RIGHT * i * 2.5)
            clusters.add(cluster)

        # Add some face images to clusters
        face_images = [ImageMobject(asset_path("face_" + str(i) + ".png")) for i in range(1, 6)]
        for i, face_image in enumerate(face_images):
            face_image.scale(0.6)
            face_image.shift(clusters[i].get_center())

        # Group everything
        group = Group(clusters, *face_images)

        # Initial view
        self.play(FadeIn(group), run_time=1.5)

        # Zoom into boundary region
        boundary_region = group.copy().scale(2.5).move_to(ORIGIN)
        self.play(Transform(group, boundary_region), run_time=2)

        # Pan across boundary regions
        for _ in range(4):
            self.play(group.animate.shift(RIGHT * 2.5), run_time=1)

        # Pull back to bird's-eye view
        self.play(Transform(group, group.copy().scale(0.4).move_to(ORIGIN)), run_time=2)

        # Highlight uncertainty region
        uncertainty_region = Rectangle(width=3, height=1, stroke_color=CYAN, stroke_width=2, fill_color=CYAN, fill_opacity=0.2)
        uncertainty_region.move_to(ORIGIN)
        self.play(FadeIn(uncertainty_region), run_time=1)

        # Classroom analogy text
        text = Tex(r"\text{Imagine a classroom where students are divided into groups.}", font_size=24)
        text.to_edge(UP, buff=1)
        self.play(Write(text), run_time=1.5)

        # Cleanup
        self.play(FadeOut(group), FadeOut(uncertainty_region), FadeOut(text), run_time=1.5)
  
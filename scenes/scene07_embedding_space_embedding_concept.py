
from manimlib import *
from scenes.utils import *

class Scene07_EmbeddingSpaceEmbeddingConcept(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Embedding Space Concept}", font_size=72)
        title.to_edge(UP, buff=1.0)

        # Embedding Space Introduction
        embedding_space_tex = Tex(r"\text{Embedding Space}", font_size=48)
        embedding_space_tex.next_to(title, DOWN, buff=0.8)

        embeddings_group = VGroup()
        for i in range(5):
            dot = Dot(radius=0.05, color=WHITE)
            dot.shift(RIGHT * (i - 2) + UP * 0.5)
            embeddings_group.add(dot)

        embeddings_group.next_to(embedding_space_tex, DOWN, buff=0.8)

        self.play(Write(title), run_time=2)
        self.play(Write(embedding_space_tex), run_time=2)
        self.play(ShowCreation(embeddings_group), run_time=2)

        # How embeddings are created
        creation_tex = Tex(r"\text{Embeddings created from face images}", font_size=48)
        creation_tex.next_to(embeddings_group, DOWN, buff=0.8)

        face_image = ImageMobject(asset_path("face_23.png"))
        face_image.shift(LEFT * 2)
        face_image.set_height(1.5)

        self.play(Write(creation_tex), run_time=2)
        self.play(FadeIn(face_image), run_time=2)

        # Optimization of embedding space
        optimization_tex = Tex(r"\text{Optimization via backpropagation}", font_size=48)
        optimization_tex.next_to(creation_tex, DOWN, buff=0.8)

        arrow = Arrow(face_image.get_center(), embeddings_group.get_center(), stroke_color=CYAN, stroke_width=2)
        self.play(ShowCreation(arrow), run_time=2)
        self.play(Write(optimization_tex), run_time=2)

        # Key Takeaway
        takeaway_tex = Tex(r"\text{Face recognition: measuring distances in embedding space}", font_size=48)
        takeaway_tex.to_edge(DOWN, buff=1.0)

        self.play(Write(takeaway_tex), run_time=2)

        self.wait(4)
    
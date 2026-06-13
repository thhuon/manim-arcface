
from manimlib import *
from scenes.utils import *

class Scene08_EmbeddingSpaceTransition(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Embedding Space Transition}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=2.0)

        # Subtitle
        subtitle = Tex(r"\text{Organizing Face Embeddings}", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(subtitle), run_time=1.5)

        # High-dimensional space
        space = VGroup()
        dots = VGroup()
        for _ in range(10):
            dot = Dot(radius=0.05, color=WHITE)
            dot.shift(RIGHT * np.random.uniform(-2.0, 2.0) + UP * np.random.uniform(-2.0, 2.0))
            dots.add(dot)
        space.add(dots)

        # Embedding points
        embeddings = VGroup()
        for i in range(5):
            embedding = Circle(radius=0.1, stroke_color=CYAN, fill_color=CYAN, fill_opacity=0.5)
            embedding.shift(RIGHT * np.random.uniform(-2.0, 2.0) + UP * np.random.uniform(-2.0, 2.0))
            embeddings.add(embedding)
        space.add(embeddings)

        self.play(ShowCreation(space), run_time=3.0)

        # Narration and labels
        label = Tex(r"\text{Face Embeddings}", font_size=24)
        label.next_to(space, DOWN, buff=0.5)
        self.play(Write(label), run_time=1.5)

        # Optimization objective
        objective = Tex(r"\text{Optimization Objective: Classify Correct Identity}", font_size=24)
        objective.next_to(label, DOWN, buff=0.4)
        self.play(Write(objective), run_time=2.0)

        # Loss function
        loss_function = Tex(r"\text{Loss Function:}", font_size=24)
        loss_function.next_to(objective, DOWN, buff=0.4)
        self.play(Write(loss_function), run_time=1.5)

        self.wait(2.0)
  
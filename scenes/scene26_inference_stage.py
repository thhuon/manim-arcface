
from manimlib import *
from scenes.utils import *

class Scene26_InferenceStage(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Inference Stage}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=2.0)

        # Neural Network as Embedding Extractor
        neural_network = make_neural_network()
        neural_network.next_to(title, DOWN, buff=1.0)
        self.play(ShowCreation(neural_network), run_time=2.5)

        # New Face Embedding
        face_img = ImageMobject(asset_path("face_26.png"))
        face_img.next_to(neural_network, RIGHT, buff=1.0)
        self.play(FadeIn(face_img), run_time=1.5)

        # Embedding Generation
        embedding = Tex(r"\text{Embedding}", font_size=24)
        embedding.next_to(face_img, RIGHT, buff=0.5)
        self.play(Write(embedding), run_time=1.5)

        # Comparison with Stored Embeddings
        stored_embeddings = Tex(r"\text{Stored Embeddings}", font_size=24)
        stored_embeddings.next_to(embedding, RIGHT, buff=1.0)
        self.play(Write(stored_embeddings), run_time=2.0)

        # Cosine Similarity
        similarity = Tex(r"\text{Cosine Similarity}", font_size=24)
        similarity.next_to(stored_embeddings, RIGHT, buff=0.5)
        self.play(Write(similarity), run_time=1.5)

        # Decision
        decision = Tex(r"\text{Same Identity?}", font_size=24)
        decision.next_to(similarity, RIGHT, buff=1.0)
        self.play(Write(decision), run_time=1.5)

        # Threshold
        threshold = Tex(r"\text{Threshold}", font_size=24)
        threshold.next_to(decision, RIGHT, buff=0.5)
        self.play(Write(threshold), run_time=1.5)

        self.wait(2.0)

from manimlib import *
from scenes.utils import *

TARGET = 173.1  # longest embedding scene

class Scene07_EmbeddingSpaceEmbeddingConcept(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Embedding Space}", font_size=54, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–35s): What is an embedding space?
        # ─────────────────────────────────────────────────────────────────
        defn = Tex(
            r"\text{A geometric space learned by a neural network during training.}",
            font_size=30, color=WHITE,
        )
        defn.next_to(title, DOWN, buff=0.45)
        self.play(Write(defn), run_time=2.5)

        nn = make_neural_network()
        nn.scale(1.4).shift(DOWN * 0.5 + LEFT * 2)

        face_in = make_abstract_face()
        face_in.scale(1.2).to_edge(LEFT, buff=0.5)
        face_in.shift(DOWN * 0.5)

        vec = make_vector([r"v_1", r"v_2", r"\vdots", r"v_{512}"], font_size=20)
        vec.shift(RIGHT * 2.8 + DOWN * 0.5)

        arr1 = Arrow(face_in.get_right(), nn.get_left(), stroke_color=CYAN, stroke_width=2)
        arr2 = Arrow(nn.get_right(), vec.get_left(), stroke_color=CYAN, stroke_width=2)

        self.play(ShowCreation(face_in), run_time=1.5)
        self.play(ShowCreation(nn), run_time=1.5)
        self.play(ShowCreation(arr1), ShowCreation(arr2), run_time=1.2)
        self.play(FadeIn(vec, shift=LEFT * 0.2), run_time=1.2)

        emb_label = Tex(r"\text{Embedding: numerical representation of a face identity}", font_size=26, color=CYAN)
        emb_label.to_edge(DOWN, buff=0.5)
        self.play(Write(emb_label), run_time=2.0)
        self.wait(15.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (35–80s): Initially random distribution
        # ─────────────────────────────────────────────────────────────────
        self.play(
            FadeOut(defn), FadeOut(face_in), FadeOut(nn),
            FadeOut(arr1), FadeOut(arr2), FadeOut(vec), FadeOut(emb_label),
            run_time=1.0,
        )

        ax = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-2.5, 2.5, 1],
            width=6, height=4,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.0},
        )
        ax.shift(DOWN * 0.4)
        self.play(ShowCreation(ax), run_time=1.2)

        rand_label = Tex(r"\text{Initial: embeddings are nearly random}", font_size=28, color=MUTED)
        rand_label.next_to(title, DOWN, buff=0.4)
        self.play(Write(rand_label), run_time=1.5)

        np.random.seed(7)
        colours_map = {0: CYAN, 1: GREEN, 2: "#FF4444"}
        dots_init = VGroup()
        identities = []
        for _ in range(30):
            identity = np.random.randint(0, 3)
            identities.append(identity)
            pos = np.random.uniform(-3, 3, 3)
            pos[2] = 0
            d = Dot(radius=0.10, color=colours_map[identity])
            d.move_to(pos)
            dots_init.add(d)

        self.play(ShowCreation(dots_init), run_time=2.5)
        self.wait(20.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (80–140s): Optimisation → clusters form
        # ─────────────────────────────────────────────────────────────────
        opt_label = Tex(r"\text{After training: same identity clusters together}", font_size=28, color=CYAN)
        opt_label.next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(rand_label), Write(opt_label), run_time=1.5)

        cluster_targets = {0: LEFT * 2 + UP * 1.2, 1: RIGHT * 2 + UP * 1.2, 2: ORIGIN + DOWN * 1.5}

        np.random.seed(99)
        anims = []
        for dot, identity in zip(dots_init, identities):
            target_center = cluster_targets[identity]
            offset = np.random.randn(3) * 0.3
            offset[2] = 0
            anims.append(dot.animate.move_to(target_center + offset))

        self.play(*anims, run_time=3.5)
        self.wait(25.0)

        # Cluster circles highlight
        for identity, center in cluster_targets.items():
            ring = Circle(radius=0.7, stroke_color=colours_map[identity], stroke_width=2, stroke_opacity=0.5, fill_opacity=0)
            ring.move_to(center)
            self.play(ShowCreation(ring), run_time=0.8)

        self.wait(15.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 4 (140–173s): Key takeaway
        # ─────────────────────────────────────────────────────────────────
        takeaway = Tex(
            r"\text{Face recognition} = \text{measuring distances in embedding space}",
            font_size=28, color=GREEN,
        )
        takeaway.to_edge(DOWN, buff=0.5)
        self.play(Write(takeaway), run_time=2.0)
        self.wait(20.0)
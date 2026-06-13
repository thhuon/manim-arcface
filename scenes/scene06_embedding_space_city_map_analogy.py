from manimlib import *
from scenes.utils import *

TARGET = 32.0

class Scene06_EmbeddingSpaceCityMapAnalogy(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Embedding Space — A City Map Analogy}", font_size=46, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # City-map: axes
        ax = Axes(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            width=7, height=5,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.2},
        )
        ax.shift(DOWN * 0.3)
        self.play(ShowCreation(ax), run_time=1.5)

        # Clusters (city neighbourhoods)
        colours = [CYAN, GREEN, "#FF4444", WHITE]
        cluster_centers = [LEFT * 2 + UP * 1.2, RIGHT * 2 + UP * 1.2,
                           LEFT * 2 + DOWN * 1.2, RIGHT * 2 + DOWN * 1.2]
        cluster_labels_text = [r"\text{Person A}", r"\text{Person B}",
                                r"\text{Person C}", r"\text{Person D}"]

        all_dots = VGroup()
        all_labels = VGroup()
        np.random.seed(42)
        for cen, col, lbl_text in zip(cluster_centers, colours, cluster_labels_text):
            for _ in range(6):
                offset = np.random.randn(3) * 0.28
                offset[2] = 0
                d = Dot(radius=0.10, color=col)
                d.move_to(cen + offset)
                all_dots.add(d)
            lbl = Tex(lbl_text, font_size=20, color=col)
            lbl.next_to(cen, UP, buff=0.12)
            all_labels.add(lbl)

        self.play(ShowCreation(all_dots), run_time=2.0)
        self.play(FadeIn(all_labels), run_time=1.2)

        # Analogy text
        analogy = Tex(
            r"\text{Similar faces } \rightarrow \text{ close together in space}",
            font_size=26, color=CYAN,
        )
        analogy.to_edge(DOWN, buff=0.5)
        self.play(Write(analogy), run_time=2.0)
        self.wait(8.0)

        # Distance arrow between two clusters
        d_arrow = Arrow(cluster_centers[0], cluster_centers[1], stroke_color=GREEN, stroke_width=2.5)
        d_label = Tex(r"\text{far apart} = \text{different people}", font_size=22, color=GREEN)
        d_label.next_to(d_arrow, UP, buff=0.15)
        self.play(ShowCreation(d_arrow), Write(d_label), run_time=1.5)
        self.wait(6.0)

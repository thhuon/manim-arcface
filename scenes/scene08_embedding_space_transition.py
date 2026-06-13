from manimlib import *
from scenes.utils import *

TARGET = 48.3

class Scene08_EmbeddingSpaceTransition(Scene):
    def construct(self):
        self.camera.background_color = DARK

        recap = Tex(r"\text{Recap: Faces mapped to embedding vectors}", font_size=40, color=WHITE)
        recap.to_edge(UP, buff=0.5)
        self.play(Write(recap), run_time=2.0)

        # Embedding circle (hypersphere cross-section)
        sphere = Circle(radius=2.5, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
        sphere.shift(DOWN * 0.5)
        self.play(ShowCreation(sphere), run_time=1.5)

        # Points on the circle
        np.random.seed(3)
        points_on_sphere = VGroup()
        labels_sphere = VGroup()
        colours = [CYAN, GREEN, "#FF4444", WHITE, BLUE]
        angle_list = np.linspace(0, 2 * PI, 5, endpoint=False)
        for i, angle in enumerate(angle_list):
            pt = sphere.get_center() + 2.5 * np.array([np.cos(angle), np.sin(angle), 0])
            d = Dot(radius=0.13, color=colours[i])
            d.move_to(pt)
            lbl = Tex(f"\\text{{ID {i+1}}}", font_size=20, color=colours[i])
            lbl.next_to(d, pt - sphere.get_center(), buff=0.18)
            points_on_sphere.add(d)
            labels_sphere.add(lbl)

        self.play(ShowCreation(points_on_sphere), run_time=1.5)
        self.play(FadeIn(labels_sphere), run_time=1.0)

        # "All embeddings on unit hypersphere"
        sphere_label = Tex(r"\text{Unit Hypersphere: } \|f\| = 1", font_size=28, color=CYAN)
        sphere_label.to_edge(DOWN, buff=0.5)
        self.play(Write(sphere_label), run_time=1.5)
        self.wait(10.0)

        # Angle between two points
        pt0 = sphere.get_center() + 2.5 * np.array([np.cos(angle_list[0]), np.sin(angle_list[0]), 0])
        pt1 = sphere.get_center() + 2.5 * np.array([np.cos(angle_list[1]), np.sin(angle_list[1]), 0])
        angle_line0 = Line(sphere.get_center(), pt0, stroke_color=WHITE, stroke_width=1.5)
        angle_line1 = Line(sphere.get_center(), pt1, stroke_color=WHITE, stroke_width=1.5)
        angle_arc = Arc(radius=0.7, start_angle=angle_list[0], angle=angle_list[1] - angle_list[0],
                        stroke_color=GREEN, stroke_width=2)
        angle_arc.shift(sphere.get_center())
        theta_label = Tex(r"\theta", font_size=26, color=GREEN)
        theta_label.move_to(sphere.get_center() + 0.9 * np.array([np.cos((angle_list[0] + angle_list[1]) / 2),
                                                                     np.sin((angle_list[0] + angle_list[1]) / 2), 0]))

        self.play(ShowCreation(angle_line0), ShowCreation(angle_line1), run_time=1.0)
        self.play(ShowCreation(angle_arc), Write(theta_label), run_time=1.2)

        cos_label = Tex(r"\text{Distance} = \cos\theta \text{ (angular distance)}", font_size=26, color=GREEN)
        cos_label.next_to(sphere_label, UP, buff=0.25)
        self.play(Write(cos_label), run_time=1.5)
        self.wait(15.0)
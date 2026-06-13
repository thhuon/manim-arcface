
from manimlib import *
from scenes.utils import *

class Scene21_ArcfaceCore3dVisualization(Scene):
    def construct(self):
        self.camera.background_color = '#111111'

        # Create a hypersphere
        sphere = Circle(radius=1.5, stroke_color=WHITE, stroke_width=0.5, fill_opacity=0)
        self.add(sphere)

        # Create a vector for an identity class
        identity_vector = Arrow(ORIGIN, 1.5 * UP, color=CYAN, stroke_width=1.5)
        self.add(identity_vector)

        # Create a label for the identity vector
        identity_label = Tex(r'\text{Class Direction}', font_size=20, color=WHITE)
        identity_label.next_to(identity_vector, RIGHT, buff=0.2)
        self.add(identity_label)

        # Create an embedding point
        embedding = Dot(radius=0.05, color=CYAN).move_to(1.2 * RIGHT + 0.5 * UP)
        self.add(embedding)

        # Create a line to represent the angle theta
        theta_line = Line(ORIGIN, embedding.get_center(), color=WHITE, stroke_width=1.0, stroke_opacity=0.5)
        self.add(theta_line)

        # Label the angle theta
        theta_label = Tex(r'\theta', font_size=20, color=WHITE)
        theta_label.move_to(0.5 * (ORIGIN + embedding.get_center()))
        self.add(theta_label)

        # Narration: Now let us examine the embedding space from a geometric perspective.
        self.play(ShowCreation(sphere), ShowCreation(identity_vector), ShowCreation(identity_label), ShowCreation(embedding), ShowCreation(theta_line), ShowCreation(theta_label), run_time=2)

        # Create a group for rotation/scaling
        scene_elements = Group(sphere, identity_vector, identity_label, embedding, theta_line, theta_label)

        # Camera movement simulation: zoom in by scaling down the camera frame
        self.play(self.camera.frame.animate.scale(0.7), run_time=3)

        # Rotate the scene elements instead of the camera
        self.play(Rotate(scene_elements, angle=30 * DEGREES), run_time=2)

        # Zoom in further and rotate
        self.play(
            self.camera.frame.animate.scale(0.8),
            Rotate(scene_elements, angle=15 * DEGREES),
            run_time=2
        )

        # Narration: ArcFace adds an angular margin to this angle, forcing the embedding of the correct class to move closer toward that class direction in order to be classified correctly.
        arcface_label = Tex(r'\text{ArcFace adds angular margin}', font_size=20, color=WHITE)
        arcface_label.next_to(embedding, DOWN, buff=0.2)
        self.play(Write(arcface_label), run_time=2)

        # Zoom out to show the full structure and rotate back
        self.play(
            self.camera.frame.animate.scale(1.78), # 1 / (0.7 * 0.8) ≈ 1.78 to return to normal scale
            Rotate(scene_elements, angle=-45 * DEGREES),
            run_time=2
        )

        self.wait(2)

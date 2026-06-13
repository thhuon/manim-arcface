from manimlib import *
from scenes.utils import *

class Scene22_ArcfaceCoreMergedWithPartC(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Initialize sphere
        sphere = Circle(radius=2, stroke_color=WHITE, stroke_width=1, fill_opacity=0)

        # Initialize embedding points
        embedding_points = Group(
            Dot(point=2 * RIGHT, radius=0.05, color=CYAN),
            Dot(point=2 * UP, radius=0.05, color=CYAN),
            Dot(point=2 * LEFT, radius=0.05, color=CYAN),
            Dot(point=2 * DOWN, radius=0.05, color=CYAN)
        )

        # Initialize class representative vectors
        class_vectors = Group(
            Arrow(ORIGIN, 2 * RIGHT, stroke_color=WHITE, stroke_width=1.5),
            Arrow(ORIGIN, 2 * UP, stroke_color=WHITE, stroke_width=1.5),
            Arrow(ORIGIN, 2 * LEFT, stroke_color=WHITE, stroke_width=1.5),
            Arrow(ORIGIN, 2 * DOWN, stroke_color=WHITE, stroke_width=1.5)
        )

        # Group them
        all_elements = Group(sphere, embedding_points, class_vectors)
        self.add(all_elements)

        # Text label at the bottom to display explanation text nicely without overlapping
        text_label = Tex(r"\text{Now we will examine the core mechanism of ArcFace.}", font_size=20)
        text_label.to_edge(DOWN, buff=0.8)
        self.play(Write(text_label), run_time=2.0)

        # Simulate camera zoom in (scale down frame)
        self.play(
            self.camera.frame.animate.scale(0.8),
            run_time=2.0
        )

        # Rotate the elements to simulate camera rotation
        self.play(
            Rotate(all_elements, angle=30 * DEGREES),
            run_time=2.0
        )

        # Update text for next narration
        new_text = Tex(
            r"\text{In standard softmax, the model only requires an embedding to lie on the correct side}",
            r"\text{of the decision boundary in order to be classified correctly.}",
            font_size=18
        )
        new_text.arrange(DOWN, buff=0.1)
        new_text.to_edge(DOWN, buff=0.8)
        
        self.play(
            Transform(text_label, new_text),
            run_time=2.0
        )
        self.wait(1.5)

        # Zoom in further
        self.play(
            self.camera.frame.animate.scale(0.8),
            run_time=1.5
        )

        # Stricter condition explanation text
        new_text_2 = Tex(
            r"\text{ArcFace makes this condition stricter. Instead of merely requiring correct classification,}",
            r"\text{ArcFace adds an angular margin to the classification process.}",
            font_size=18
        )
        new_text_2.arrange(DOWN, buff=0.1)
        new_text_2.to_edge(DOWN, buff=0.8)

        self.play(
            Transform(text_label, new_text_2),
            run_time=2.0
        )

        # Show angular margin line
        margin_line = DashedLine(
            class_vectors[0].get_end(),
            class_vectors[0].get_end() + 0.5 * RIGHT,
            stroke_color=CYAN,
            stroke_width=1.5
        )
        all_elements.add(margin_line) # add to group so it scales/rotates with others
        self.play(ShowCreation(margin_line), run_time=1.5)

        # Formula text
        new_text_3 = Tex(
            r"\text{Mathematically, ArcFace changes } \cos(\theta) \text{ to } \cos(\theta + m)\text{, where } \theta \text{ is the angle}",
            r"\text{between the embedding and the class-representative vector, and } m \text{ is the angular margin.}",
            font_size=18
        )
        new_text_3.arrange(DOWN, buff=0.1)
        new_text_3.to_edge(DOWN, buff=0.8)

        self.play(
            Transform(text_label, new_text_3),
            run_time=2.0
        )
        self.wait(1.5)

        # Zoom out (scale up frame)
        self.play(
            self.camera.frame.animate.scale(1.5625), # 1 / (0.8 * 0.8) = 1.5625
            Rotate(all_elements, angle=-30 * DEGREES),
            run_time=1.5
        )

        # Final text
        new_text_4 = Tex(
            r"\text{To be classified correctly, the embedding must move closer toward the corresponding class direction,}",
            r"\text{rather than merely lying on the correct side of the decision boundary.}",
            font_size=18
        )
        new_text_4.arrange(DOWN, buff=0.1)
        new_text_4.to_edge(DOWN, buff=0.8)

        self.play(
            Transform(text_label, new_text_4),
            run_time=2.0
        )
        self.wait(2.5)

        # Clean up
        self.play(
            FadeOut(all_elements),
            FadeOut(text_label),
            run_time=1.5
        )
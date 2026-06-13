
from manimlib import *
from scenes.utils import *

class Scene18_ArcfaceCoreWhyNormalizationMatters(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # Title
        title = Tex(r"\text{Why Normalization Matters?}", font_size=72)
        title.to_edge(UP, buff=1.0)
        self.play(Write(title), run_time=2.0)

        # Subtitle
        subtitle = Tex(r"\text{Normalization in ArcFace}", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(subtitle), run_time=1.5)

        # Vector without normalization
        vector_no_norm = Line(ORIGIN, 2 * RIGHT, stroke_color=WHITE, stroke_width=2)
        vector_no_norm_label = Tex(r"\text{No Normalization}", font_size=24)
        vector_no_norm_label.next_to(vector_no_norm, DOWN, buff=0.3)

        # Vector with normalization
        vector_norm = Line(ORIGIN, 2 * RIGHT, stroke_color=CYAN, stroke_width=2)
        vector_norm.scale(0.5)
        vector_norm_label = Tex(r"\text{Normalization}", font_size=24)
        vector_norm_label.next_to(vector_norm, DOWN, buff=0.3)

        # Group for vectors and labels
        vectors = VGroup(vector_no_norm, vector_no_norm_label, vector_norm, vector_norm_label)
        vectors.arrange(DOWN, buff=1.0)
        vectors.move_to(ORIGIN)

        self.play(ShowCreation(vector_no_norm), ShowCreation(vector_no_norm_label), run_time=2.0)
        self.wait(1.0)

        # Highlighting magnitude
        magnitude_highlight = Line(ORIGIN, 4 * RIGHT, stroke_color=WHITE, stroke_width=2, stroke_opacity=0.5)
        magnitude_highlight_label = Tex(r"\text{Magnitude}", font_size=24)
        magnitude_highlight_label.next_to(magnitude_highlight, DOWN, buff=0.3)

        self.play(ShowCreation(magnitude_highlight), ShowCreation(magnitude_highlight_label), run_time=1.5)

        # Transition to normalized vectors
        self.play(FadeOut(magnitude_highlight), FadeOut(magnitude_highlight_label), run_time=1.0)
        self.play(Transform(vector_no_norm, vector_norm), Transform(vector_no_norm_label, vector_norm_label), run_time=2.0)

        # Angle highlight
        angle_highlight = Arc(radius=1.0, start_angle=0 * DEGREES, angle=45 * DEGREES, stroke_color=CYAN, stroke_width=2)
        angle_highlight_label = Tex(r"\text{Angle}", font_size=24)
        angle_highlight_label.next_to(angle_highlight, UP, buff=0.3)

        self.play(ShowCreation(angle_highlight), ShowCreation(angle_highlight_label), run_time=2.0)

        self.wait(2.0)
    
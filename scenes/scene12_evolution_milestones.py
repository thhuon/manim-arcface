from manimlib import *
from scenes.utils import *

TARGET = 97.1

class Scene12_EvolutionMilestones(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Evolution of Face Recognition}", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # Timeline
        milestones = [
            ("1991", "Eigenfaces", MUTED, r"\text{PCA-based method}"),
            ("2014", "DeepFace", BLUE, r"\text{Facebook's deep CNN}"),
            ("2015", "FaceNet", GREEN, r"\text{Triplet loss, 99.6\% LFW}"),
            ("2017", "SphereFace", CYAN, r"\text{Multiplicative angular margin}"),
            ("2019", "ArcFace", "#FFD700", r"\text{Additive angular margin}"),
        ]

        timeline_line = Line(LEFT * 5.5, RIGHT * 5.5, stroke_color=MUTED, stroke_width=1.5)
        timeline_line.shift(DOWN * 0.5)
        self.play(ShowCreation(timeline_line), run_time=1.2)

        tick_positions = np.linspace(-4.5, 4.5, len(milestones))

        for i, (year, name, col, desc) in enumerate(milestones):
            x = tick_positions[i]
            tick = Line(DOWN * 0.15, UP * 0.15, stroke_color=col, stroke_width=2.5)
            tick.move_to(timeline_line.get_center() + x * RIGHT)

            year_lbl = Tex(year, font_size=20, color=col)
            name_lbl = Tex(r"\text{" + name + r"}", font_size=22, color=col)
            desc_lbl = Tex(desc, font_size=18, color=WHITE)

            year_lbl.next_to(tick, DOWN, buff=0.2)
            if i % 2 == 0:
                name_lbl.next_to(tick, UP, buff=0.4)
                desc_lbl.next_to(name_lbl, UP, buff=0.15)
            else:
                name_lbl.next_to(tick, DOWN, buff=0.6)
                desc_lbl.next_to(name_lbl, DOWN, buff=0.15)

            self.play(
                ShowCreation(tick),
                Write(year_lbl),
                run_time=0.7,
            )
            self.play(Write(name_lbl), Write(desc_lbl), run_time=1.0)
            self.wait(4.0)

        # Highlight ArcFace
        arcface_highlight = SurroundingRectangle(
            VGroup(*[t for t in self.mobjects if isinstance(t, Tex) and "ArcFace" in t.get_tex_string()]),
            color="#FFD700", buff=0.1,
        )
        arcface_caption = Tex(r"\text{State-of-the-art as of 2019+}", font_size=26, color="#FFD700")
        arcface_caption.to_edge(DOWN, buff=0.5)

        self.play(ShowCreation(arcface_highlight), run_time=1.2)
        self.play(Write(arcface_caption), run_time=1.5)
        self.wait(25.0)
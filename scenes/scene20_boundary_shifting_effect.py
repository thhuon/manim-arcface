from manimlib import *
from scenes.utils import *

TARGET = 37.8

class Scene20_BoundaryShiftingEffect(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Boundary Shifting Effect}", font_size=50, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        circle = Circle(radius=2.5, stroke_color=CYAN, stroke_width=1.5)
        circle.shift(DOWN * 0.4)
        center = circle.get_center()
        self.play(ShowCreation(circle), run_time=1.0)

        # Weight vector
        w_angle = PI / 6
        w_end = center + 2.5 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
        w_arr = Arrow(center, w_end, stroke_color=WHITE, stroke_width=2.5, buff=0)
        w_lbl = Tex(r"W_{y_i}", font_size=22, color=WHITE)
        w_lbl.next_to(w_end, UR, buff=0.1)
        self.play(ShowCreation(w_arr), Write(w_lbl), run_time=1.0)

        # Softmax boundary (old)
        old_boundary_angle = w_angle + PI / 2
        old_b1 = center + 3.0 * np.array([np.cos(old_boundary_angle), np.sin(old_boundary_angle), 0])
        old_b2 = center - 3.0 * np.array([np.cos(old_boundary_angle), np.sin(old_boundary_angle), 0])
        old_boundary = DashedLine(old_b1, old_b2, stroke_color=MUTED, stroke_width=2, dash_length=0.15)
        old_label = Tex(r"\text{Softmax boundary}", font_size=20, color=MUTED)
        old_label.next_to(old_b1, UP, buff=0.1)
        self.play(ShowCreation(old_boundary), Write(old_label), run_time=1.2)
        self.wait(4.0)

        # ArcFace boundary (shifted by m)
        m = 0.5
        new_boundary_angle = w_angle + PI / 2 - m
        new_b1 = center + 3.0 * np.array([np.cos(new_boundary_angle), np.sin(new_boundary_angle), 0])
        new_b2 = center - 3.0 * np.array([np.cos(new_boundary_angle), np.sin(new_boundary_angle), 0])
        new_boundary = DashedLine(new_b1, new_b2, stroke_color=GREEN, stroke_width=2.5, dash_length=0.15)
        new_label = Tex(r"\text{ArcFace boundary (shifted by }m\text{)}", font_size=20, color=GREEN)
        new_label.next_to(new_b2, DOWN, buff=0.1)
        self.play(ShowCreation(new_boundary), Write(new_label), run_time=1.5)

        # Margin arc
        arc_m = Arc(radius=0.55, start_angle=new_boundary_angle, angle=m,
                     stroke_color="#FFD700", stroke_width=2)
        arc_m.shift(center)
        m_lbl = Tex(r"m", font_size=20, color="#FFD700")
        m_lbl.move_to(center + 0.75 * np.array([np.cos(new_boundary_angle + m / 2),
                                                  np.sin(new_boundary_angle + m / 2), 0]))
        self.play(ShowCreation(arc_m), Write(m_lbl), run_time=1.0)

        caption = Tex(
            r"\text{Margin shifts the decision boundary, forcing embedding closer to }W_{y_i}",
            font_size=22, color=WHITE,
        )
        caption.to_edge(DOWN, buff=0.5)
        self.play(Write(caption), run_time=2.0)
        self.wait(12.0)
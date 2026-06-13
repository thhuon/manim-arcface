from manimlib import *
from scenes.utils import *

TARGET = 47.7

class Scene17_ArcfaceCoreTransition(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Angular Margin — Geometric View}", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        circle = Circle(radius=2.5, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
        circle.shift(DOWN * 0.4)
        center = circle.get_center()
        self.play(ShowCreation(circle), run_time=1.2)

        # Class weight vector
        w_angle = PI / 6
        w_end = center + 2.5 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
        w_arr = Arrow(center, w_end, stroke_color=WHITE, stroke_width=2.5, buff=0)
        w_lbl = Tex(r"W_{y_i}", font_size=24, color=WHITE)
        w_lbl.next_to(w_end, UR, buff=0.12)

        # Embedding without margin
        theta = PI / 6 + PI / 5
        emb_end = center + 2.5 * np.array([np.cos(theta), np.sin(theta), 0])
        emb_arr = Arrow(center, emb_end, stroke_color=GREEN, stroke_width=2.5, buff=0)
        emb_lbl = Tex(r"f_i", font_size=24, color=GREEN)
        emb_lbl.next_to(emb_end, UL, buff=0.12)

        self.play(ShowCreation(w_arr), Write(w_lbl), run_time=1.0)
        self.play(ShowCreation(emb_arr), Write(emb_lbl), run_time=1.0)

        # Theta arc
        arc_theta = Arc(radius=0.8, start_angle=w_angle, angle=theta - w_angle,
                         stroke_color=GREEN, stroke_width=2)
        arc_theta.shift(center)
        theta_lbl = Tex(r"\theta", font_size=22, color=GREEN)
        mid = (w_angle + theta) / 2
        theta_lbl.move_to(center + 1.0 * np.array([np.cos(mid), np.sin(mid), 0]))
        self.play(ShowCreation(arc_theta), Write(theta_lbl), run_time=1.2)
        self.wait(5.0)

        # Margin arc
        m = 0.5  # radians
        arc_margin = Arc(radius=0.5, start_angle=theta, angle=m,
                          stroke_color="#FFD700", stroke_width=2.5)
        arc_margin.shift(center)
        m_lbl = Tex(r"m", font_size=22, color="#FFD700")
        mid_m = theta + m / 2
        m_lbl.move_to(center + 0.7 * np.array([np.cos(mid_m), np.sin(mid_m), 0]))
        self.play(ShowCreation(arc_margin), Write(m_lbl), run_time=1.2)

        constraint = Tex(
            r"\text{ArcFace requires } \theta + m < \text{boundary angle}",
            font_size=24, color="#FFD700",
        )
        constraint.to_edge(DOWN, buff=0.5)
        self.play(Write(constraint), run_time=1.5)
        self.wait(18.0)
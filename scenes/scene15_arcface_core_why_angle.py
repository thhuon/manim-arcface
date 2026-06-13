from manimlib import *
from scenes.utils import *

TARGET = 77.3

class Scene15_ArcfaceCoreWhyAngle(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Why Angular Distance?}", font_size=50, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–25s): Euclidean vs Angular distance on circle
        # ─────────────────────────────────────────────────────────────────
        circle = Circle(radius=2.5, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
        circle.shift(DOWN * 0.5)
        center = circle.get_center()
        self.play(ShowCreation(circle), run_time=1.2)

        r_label = Tex(r"\|f\| = 1", font_size=24, color=MUTED)
        r_label.next_to(circle, RIGHT, buff=0.2).shift(DOWN * 0.5)
        self.play(Write(r_label), run_time=0.8)

        # Two points on circle
        angle_a = PI / 5
        angle_b = PI / 5 + PI / 3
        pt_a = center + 2.5 * np.array([np.cos(angle_a), np.sin(angle_a), 0])
        pt_b = center + 2.5 * np.array([np.cos(angle_b), np.sin(angle_b), 0])

        dot_a = Dot(radius=0.14, color=GREEN)
        dot_b = Dot(radius=0.14, color=CYAN)
        dot_a.move_to(pt_a)
        dot_b.move_to(pt_b)
        lbl_a = Tex(r"A", font_size=22, color=GREEN)
        lbl_b = Tex(r"B", font_size=22, color=CYAN)
        lbl_a.next_to(dot_a, pt_a - center, buff=0.15)
        lbl_b.next_to(dot_b, pt_b - center, buff=0.15)

        self.play(FadeIn(dot_a), FadeIn(dot_b), Write(lbl_a), Write(lbl_b), run_time=1.0)

        # Euclidean line
        euc_line = DashedLine(pt_a, pt_b, stroke_color=MUTED, stroke_width=2)
        euc_lbl = Tex(r"\text{Euclidean: ignores magnitude}", font_size=22, color=MUTED)
        euc_lbl.next_to(euc_line.get_center(), DOWN, buff=0.2)
        self.play(ShowCreation(euc_line), Write(euc_lbl), run_time=1.5)
        self.wait(6.0)

        # Angle arc
        arc_angle = Arc(radius=0.9, start_angle=angle_a, angle=angle_b - angle_a,
                         stroke_color=GREEN, stroke_width=2.5)
        arc_angle.shift(center)
        theta_lbl = Tex(r"\theta", font_size=26, color=GREEN)
        mid_angle = (angle_a + angle_b) / 2
        theta_lbl.move_to(center + 1.1 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))

        line_a = Line(center, pt_a, stroke_color=WHITE, stroke_width=1.3)
        line_b = Line(center, pt_b, stroke_color=WHITE, stroke_width=1.3)

        self.play(ShowCreation(line_a), ShowCreation(line_b), run_time=0.8)
        self.play(ShowCreation(arc_angle), Write(theta_lbl), run_time=1.2)

        ang_lbl = Tex(r"\cos\theta \text{ — scale-invariant angular distance}", font_size=22, color=GREEN)
        ang_lbl.to_edge(DOWN, buff=0.5)
        self.play(Write(ang_lbl), run_time=1.5)
        self.wait(12.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (25–77s): Normalization means magnitude doesn't matter
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(euc_line), FadeOut(euc_lbl), FadeOut(ang_lbl), run_time=0.8)

        norm_title = Tex(r"\text{After L2 Normalisation: only direction matters}", font_size=28, color=CYAN)
        norm_title.next_to(title, DOWN, buff=0.4)
        self.play(Write(norm_title), run_time=1.5)

        # Two vectors with different magnitudes but same direction
        vec1 = Arrow(center, center + 1.5 * np.array([np.cos(angle_a), np.sin(angle_a), 0]),
                     stroke_color=WHITE, stroke_width=2)
        vec2 = Arrow(center, center + 2.5 * np.array([np.cos(angle_a), np.sin(angle_a), 0]),
                     stroke_color=CYAN, stroke_width=2)
        same_dir = Tex(r"\text{Same direction, different magnitude \textrightarrow{} same identity}", font_size=24, color=WHITE)
        same_dir.to_edge(DOWN, buff=0.5)

        self.play(ShowCreation(vec1), ShowCreation(vec2), run_time=1.5)
        self.play(Write(same_dir), run_time=2.0)
        self.wait(25.0)

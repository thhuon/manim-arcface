from manimlib import *
from scenes.utils import *

TARGET = 97.7

class Scene21_ArcfaceCore3dVisualization(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Embedding Space — Hypersphere View}", font_size=46, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–30s): Unit circle with clusters
        # ─────────────────────────────────────────────────────────────────
        sphere = Circle(radius=2.6, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
        sphere.shift(DOWN * 0.4)
        center = sphere.get_center()
        self.play(ShowCreation(sphere), run_time=1.2)

        r_label = Tex(r"\text{Unit Hypersphere: } \|f\| = 1", font_size=24, color=MUTED)
        r_label.to_edge(DOWN, buff=0.5)
        self.play(Write(r_label), run_time=1.2)

        colours = [CYAN, GREEN, "#FF4444", "#FFD700"]
        cluster_angles = [PI / 6, 3 * PI / 4, -PI / 3, PI + PI / 4]

        np.random.seed(17)
        all_dots = VGroup()
        for angle_base, col in zip(cluster_angles, colours):
            w_end = center + 2.6 * np.array([np.cos(angle_base), np.sin(angle_base), 0])
            w_arr = Arrow(center, w_end, stroke_color=col, stroke_width=2, buff=0)
            self.play(ShowCreation(w_arr), run_time=0.6)
            for _ in range(7):
                offset_a = angle_base + np.random.uniform(-0.18, 0.18)
                r = np.random.uniform(2.3, 2.6)
                d = Dot(radius=0.09, color=col)
                d.move_to(center + r * np.array([np.cos(offset_a), np.sin(offset_a), 0]))
                all_dots.add(d)

        self.play(ShowCreation(all_dots), run_time=2.0)
        self.wait(15.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (30–65s): Zoom into one angle theta
        # ─────────────────────────────────────────────────────────────────
        self.play(self.camera.frame.animate.scale(0.6).move_to(center + LEFT * 0.2), run_time=2.0)

        angle_a = cluster_angles[0]
        angle_b = cluster_angles[1]
        pt_a = center + 2.6 * np.array([np.cos(angle_a), np.sin(angle_a), 0])
        pt_b = center + 2.6 * np.array([np.cos(angle_b), np.sin(angle_b), 0])

        line_a = Line(center, pt_a, stroke_color=WHITE, stroke_width=1.5)
        line_b = Line(center, pt_b, stroke_color=WHITE, stroke_width=1.5)
        mid_angle = (angle_a + angle_b) / 2
        arc_theta = Arc(radius=0.5, start_angle=angle_a, angle=angle_b - angle_a,
                         stroke_color=GREEN, stroke_width=2.0)
        arc_theta.shift(center)
        theta_lbl = Tex(r"\theta", font_size=20, color=GREEN)
        theta_lbl.move_to(center + 0.7 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0]))

        self.play(ShowCreation(line_a), ShowCreation(line_b), run_time=1.0)
        self.play(ShowCreation(arc_theta), Write(theta_lbl), run_time=1.0)
        self.wait(18.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (65–97s): Zoom out — full hypersphere view
        # ─────────────────────────────────────────────────────────────────
        self.play(self.camera.frame.animate.scale(1 / 0.6).move_to(ORIGIN), run_time=2.0)

        projection_label = Tex(
            r"\text{All embeddings projected onto the unit sphere surface}",
            font_size=24, color=CYAN,
        )
        projection_label.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(r_label), Write(projection_label), run_time=1.5)
        self.wait(25.0)

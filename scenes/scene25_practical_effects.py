from manimlib import *
from scenes.utils import *

TARGET = 132.4

class Scene25_PracticalEffects(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Practical Effects of ArcFace}", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–40s): Side-by-side softmax vs arcface clusters
        # ─────────────────────────────────────────────────────────────────
        left_lbl = Tex(r"\text{Standard Softmax}", font_size=26, color=MUTED)
        right_lbl = Tex(r"\text{ArcFace}", font_size=26, color=CYAN)
        left_lbl.shift(LEFT * 3.5 + UP * 1.8)
        right_lbl.shift(RIGHT * 3.5 + UP * 1.8)
        divider = Line(UP * 3, DOWN * 3, stroke_color=MUTED, stroke_width=1.0)
        self.play(Write(left_lbl), Write(right_lbl), ShowCreation(divider), run_time=1.0)

        # Circles
        cl = Circle(radius=2.0, stroke_color=MUTED, stroke_width=1.2)
        cl.shift(LEFT * 3.5 + DOWN * 0.3)
        cr = Circle(radius=2.0, stroke_color=CYAN, stroke_width=1.5)
        cr.shift(RIGHT * 3.5 + DOWN * 0.3)
        self.play(ShowCreation(cl), ShowCreation(cr), run_time=1.0)

        np.random.seed(7)
        cols = [CYAN, GREEN, "#FF4444"]
        bases = [PI / 5, -PI / 3, PI]

        soft_dots = VGroup()
        arc_dots = VGroup()

        for angle_base, col in zip(bases, cols):
            cl_center = cl.get_center()
            cr_center = cr.get_center()
            for _ in range(10):
                # Softmax: spread
                oa = angle_base + np.random.uniform(-0.65, 0.65)
                r = np.random.uniform(0.8, 1.9)
                d = Dot(radius=0.09, color=col)
                d.move_to(cl_center + r * np.array([np.cos(oa), np.sin(oa), 0]))
                soft_dots.add(d)
                # ArcFace: tight
                oa2 = angle_base + np.random.uniform(-0.20, 0.20)
                r2 = np.random.uniform(1.7, 2.0)
                d2 = Dot(radius=0.09, color=col)
                d2.move_to(cr_center + r2 * np.array([np.cos(oa2), np.sin(oa2), 0]))
                arc_dots.add(d2)

        self.play(ShowCreation(soft_dots), ShowCreation(arc_dots), run_time=2.0)

        soft_cap = Tex(r"\text{Loose clusters, blurred boundaries}", font_size=20, color=MUTED)
        arc_cap = Tex(r"\text{Tight clusters, clear margins}", font_size=20, color=CYAN)
        soft_cap.next_to(cl, DOWN, buff=0.3)
        arc_cap.next_to(cr, DOWN, buff=0.3)
        self.play(Write(soft_cap), Write(arc_cap), run_time=1.5)
        self.wait(20.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (40–90s): Difficult cases: lighting, angle, expression
        # ─────────────────────────────────────────────────────────────────
        self.play(
            FadeOut(soft_dots), FadeOut(arc_dots), FadeOut(cl), FadeOut(cr),
            FadeOut(left_lbl), FadeOut(right_lbl), FadeOut(divider),
            FadeOut(soft_cap), FadeOut(arc_cap), run_time=0.8,
        )

        robust_lbl = Tex(r"\text{Robustness: ArcFace handles difficult conditions}", font_size=30, color=CYAN)
        robust_lbl.next_to(title, DOWN, buff=0.5)
        self.play(Write(robust_lbl), run_time=1.5)

        conditions = [
            r"\bullet\;\text{Different lighting conditions}",
            r"\bullet\;\text{Variations in face angle / pose}",
            r"\bullet\;\text{Different facial expressions}",
            r"\bullet\;\text{Faces with similar characteristics}",
        ]
        cond_group = VGroup(*[Tex(t, font_size=26, color=WHITE) for t in conditions])
        cond_group.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        cond_group.next_to(robust_lbl, DOWN, buff=0.5)
        cond_group.to_edge(LEFT, buff=1.0)

        for cond in cond_group:
            self.play(FadeIn(cond, shift=RIGHT * 0.1), run_time=1.0)
            self.wait(4.0)

        self.wait(15.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (90–132s): Key result — geometry unchanged, loss improved
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(cond_group), FadeOut(robust_lbl), run_time=0.8)

        key_title = Tex(r"\text{What ArcFace Changes:}", font_size=32, color="#FFD700")
        key_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(key_title), run_time=1.5)

        key_items = [
            (r"\text{Network architecture}", r"\text{UNCHANGED}", MUTED, GREEN),
            (r"\text{Loss function}", r"\text{IMPROVED (+ margin)}", MUTED, CYAN),
            (r"\text{Embedding structure}", r"\text{MUCH BETTER}", MUTED, GREEN),
        ]
        keys_group = VGroup()
        for what, how, c1, c2 in key_items:
            row = VGroup(
                Tex(what, font_size=26, color=c1),
                Tex(r"\rightarrow", font_size=26, color=WHITE),
                Tex(how, font_size=26, color=c2),
            )
            row.arrange(RIGHT, buff=0.5)
            keys_group.add(row)
        keys_group.arrange(DOWN, buff=0.5)
        keys_group.next_to(key_title, DOWN, buff=0.5)

        for row in keys_group:
            self.play(FadeIn(row, shift=UP * 0.1), run_time=1.0)
            self.wait(4.0)

        self.wait(20.0)

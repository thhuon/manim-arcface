from manimlib import *
from scenes.utils import *

TARGET = 79.5

class Scene04_ChallengesWhyAccuracyMatters(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Why Accuracy Matters}", font_size=52, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–25s): Low-accuracy model — mistakes
        # ─────────────────────────────────────────────────────────────────
        low_label = Tex(r"\text{Low-Accuracy Model}", font_size=30, color=MUTED)
        low_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(low_label), run_time=1.5)

        # Two faces, wrong match
        face_a = make_abstract_face()
        face_a.scale(1.3).shift(LEFT * 2.5 + DOWN * 0.8)
        face_b = make_abstract_face()
        face_b.scale(1.3).shift(RIGHT * 2.5 + DOWN * 0.8)

        lbl_a = Tex(r"\text{Alice}", font_size=26, color=WHITE)
        lbl_a.next_to(face_a, DOWN, buff=0.2)
        lbl_b = Tex(r"\text{Bob}", font_size=26, color=WHITE)
        lbl_b.next_to(face_b, DOWN, buff=0.2)

        wrong_arrow = Arrow(face_a.get_right(), face_b.get_left(), stroke_color="#FF4444", stroke_width=3, buff=0.15)
        wrong_label = Tex(r"\text{False Match!}", font_size=28, color="#FF4444")
        wrong_label.next_to(wrong_arrow, UP, buff=0.2)

        self.play(ShowCreation(face_a), ShowCreation(face_b), run_time=1.5)
        self.play(Write(lbl_a), Write(lbl_b), run_time=1.0)
        self.play(ShowCreation(wrong_arrow), run_time=1.0)
        self.play(Write(wrong_label), run_time=1.2)
        self.wait(8.0)

        # Real-world consequence labels
        consequences = [
            r"\text{Security breach}",
            r"\text{Wrong person identified}",
            r"\text{Privacy violation}",
        ]
        cons_group = VGroup(*[Tex(t, font_size=24, color="#FF4444") for t in consequences])
        cons_group.arrange(DOWN, buff=0.3)
        cons_group.to_edge(DOWN, buff=0.7)
        for c in cons_group:
            self.play(FadeIn(c, shift=UP * 0.1), run_time=0.7)
        self.wait(5.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (25–55s): The 1-in-a-million problem
        # ─────────────────────────────────────────────────────────────────
        self.play(
            FadeOut(low_label), FadeOut(face_a), FadeOut(face_b),
            FadeOut(lbl_a), FadeOut(lbl_b), FadeOut(wrong_arrow),
            FadeOut(wrong_label), FadeOut(cons_group),
            run_time=1.0,
        )

        mil_text = Tex(r"\text{1 in 1{,}000{,}000 faces}", font_size=44, color=CYAN)
        mil_text.move_to(UP * 0.8)
        self.play(Write(mil_text), run_time=2.0)

        context = Tex(
            r"\text{Security systems, airports, banking —}\\"
            r"\text{even a 0.001\% error is unacceptable}",
            font_size=28, color=WHITE,
        )
        context.next_to(mil_text, DOWN, buff=0.5)
        self.play(Write(context), run_time=2.5)
        self.wait(12.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (55–79s): High-accuracy model — correct match
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(mil_text), FadeOut(context), run_time=1.0)

        hi_label = Tex(r"\text{High-Accuracy Model (ArcFace)}", font_size=30, color=GREEN)
        hi_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(hi_label), run_time=1.5)

        face_c = make_abstract_face()
        face_c.scale(1.3).shift(LEFT * 2.5 + DOWN * 0.8)
        face_d = make_abstract_face()
        face_d.scale(1.3).shift(RIGHT * 2.5 + DOWN * 0.8)
        lbl_c = Tex(r"\text{Alice}", font_size=26, color=WHITE)
        lbl_c.next_to(face_c, DOWN, buff=0.2)
        lbl_d = Tex(r"\text{Alice (verified)}", font_size=26, color=WHITE)
        lbl_d.next_to(face_d, DOWN, buff=0.2)

        ok_arrow = Arrow(face_c.get_right(), face_d.get_left(), stroke_color=GREEN, stroke_width=3, buff=0.15)
        ok_label = Tex(r"\checkmark\;\text{Correct Match}", font_size=28, color=GREEN)
        ok_label.next_to(ok_arrow, UP, buff=0.2)

        self.play(ShowCreation(face_c), ShowCreation(face_d), run_time=1.5)
        self.play(Write(lbl_c), Write(lbl_d), run_time=1.0)
        self.play(ShowCreation(ok_arrow), run_time=1.0)
        self.play(Write(ok_label), run_time=1.2)
        self.wait(12.0)

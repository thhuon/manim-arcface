from manimlib import *
from scenes.utils import *

TARGET = 39.2  # seconds

class Scene01_HumanVsComputer(Scene):
    def construct(self):
        self.camera.background_color = DARK

        # ── Labels ────────────────────────────────────────────────────────
        human_lbl = Tex(r"\text{HUMAN}", font_size=34, color=GREEN)
        computer_lbl = Tex(r"\text{COMPUTER}", font_size=34, color=CYAN)
        human_lbl.to_corner(UL, buff=0.5)
        computer_lbl.to_corner(UR, buff=0.5)

        divider = Line(UP * 3.5, DOWN * 3.5, stroke_color=MUTED, stroke_width=1.5)
        divider.move_to(ORIGIN)

        # ── Human side ───────────────────────────────────────────────────
        face = make_abstract_face()
        face.scale(1.5).shift(LEFT * 3.2)

        eye_flash = Circle(radius=0.06, fill_color=GREEN, fill_opacity=1, stroke_width=0)
        eye_flash.move_to(face.get_center() + 0.22 * LEFT + 0.16 * UP)

        human_tag = Tex(r"\text{Instant recognition}", font_size=24, color=WHITE)
        human_tag.next_to(face, DOWN, buff=0.45)

        # ── Computer side ─────────────────────────────────────────────────
        grid = make_pixel_grid(size=2.2, n=8)
        grid.shift(RIGHT * 3.2)

        face_img = make_abstract_face()
        face_img.scale(1.0).shift(RIGHT * 3.2)
        face_img.set_stroke(WHITE, 1.0)

        pixels_label = Tex(r"\text{Collection of pixels}", font_size=24, color=WHITE)
        pixels_label.next_to(grid, DOWN, buff=0.45)

        # ── Arrow across ─────────────────────────────────────────────────
        transform_arrow = Arrow(LEFT * 0.7, RIGHT * 0.7, stroke_color=CYAN, stroke_width=2.5)
        transform_label = Tex(r"\text{Mathematical representation}", font_size=22, color=CYAN)
        transform_label.next_to(transform_arrow, UP, buff=0.12)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–10s): "Humans recognise faces instantly"
        # ─────────────────────────────────────────────────────────────────
        self.play(Write(human_lbl), Write(computer_lbl), run_time=1.5)
        self.play(ShowCreation(divider), run_time=0.8)
        self.play(ShowCreation(face), run_time=2.0)
        self.play(FadeIn(eye_flash), run_time=0.5)
        self.play(FadeOut(eye_flash), run_time=0.5)
        self.play(Write(human_tag), run_time=1.5)
        self.wait(3.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (10–22s): "For a computer, a face is pixels"
        # ─────────────────────────────────────────────────────────────────
        self.play(ShowCreation(grid), run_time=1.5)
        self.play(FadeIn(face_img), run_time=1.0)
        self.play(Write(pixels_label), run_time=1.5)

        num_text = Tex(r"[128, 240, 196, \ldots]", font_size=22, color=MUTED)
        num_text.next_to(face_img, UP, buff=0.3)
        self.play(FadeIn(num_text, shift=DOWN * 0.1), run_time=1.2)
        self.wait(5.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (22–35s): "Convert face info → mathematical representation"
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(human_tag), FadeOut(pixels_label), FadeOut(num_text), run_time=0.8)
        self.play(ShowCreation(transform_arrow), run_time=1.2)
        self.play(Write(transform_label), run_time=1.5)

        vec = make_vector([r"0.42", r"-0.87", r"0.13", r"\vdots"], font_size=20)
        vec.shift(RIGHT * 4.6)
        self.play(FadeIn(vec, shift=LEFT * 0.3), run_time=1.5)
        self.wait(5.5)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 4 (35–39s): Final hold
        # ─────────────────────────────────────────────────────────────────
        question = Tex(r"\text{What happens when you look into the camera?}", font_size=26, color=CYAN)
        question.to_edge(DOWN, buff=0.5)
        self.play(Write(question), run_time=2.0)
        self.wait(2.2)

from manimlib import *
from scenes.utils import *

TARGET = 30.7  # seconds (narration duration)

class Scene00_Introduction(Scene):
    def construct(self):
        self.camera.background_color = DARK

        # ── Background grid ──────────────────────────────────────────────
        grid = make_pixel_grid(size=8, n=16)
        grid.set_opacity(0.08)
        self.add(grid)

        # ── Camera icon top-left ─────────────────────────────────────────
        cam = make_camera_icon()
        cam.scale(1.4).to_corner(UL, buff=0.5)

        # ── Face + landmarks center ──────────────────────────────────────
        face = make_abstract_face()
        face.scale(1.6).move_to(ORIGIN)
        lm = make_landmarks()
        lm.scale(1.6).move_to(face.get_center())

        # ── Neural network right ─────────────────────────────────────────
        nn = make_neural_network()
        nn.scale(1.1).to_edge(RIGHT, buff=0.6)

        # ── Title ────────────────────────────────────────────────────────
        title = Tex(r"\text{ArcFace: Modern Face Recognition}", font_size=52, color=WHITE)
        title.to_edge(UP, buff=0.4)

        sub = Tex(r"\text{How computers see and recognize human faces}", font_size=28, color=MUTED)
        sub.next_to(title, DOWN, buff=0.25)

        # ── Accent line under title ──────────────────────────────────────
        accent = Line(LEFT * 4, RIGHT * 4, stroke_color=CYAN, stroke_width=2)
        accent.next_to(sub, DOWN, buff=0.18)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–8s): Title + camera icon appear
        # ─────────────────────────────────────────────────────────────────
        self.play(Write(title), run_time=2.5)
        self.play(FadeIn(sub, shift=UP * 0.15), run_time=1.5)
        self.play(ShowCreation(accent), run_time=1.0)
        self.play(FadeIn(cam), run_time=1.0)
        self.wait(2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (8–18s): Face + landmarks emerge — "how do these systems work?"
        # ─────────────────────────────────────────────────────────────────
        self.play(ShowCreation(face), run_time=2.0)
        self.play(FadeIn(lm), run_time=1.2)

        q_text = Tex(r"\text{How does a computer recognise a face?}", font_size=30, color=CYAN)
        q_text.next_to(face, DOWN, buff=0.55)
        self.play(Write(q_text), run_time=2.0)
        self.wait(2.8)
        self.play(FadeOut(q_text), run_time=0.8)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (18–28s): Neural network appears — "mathematical representation"
        # ─────────────────────────────────────────────────────────────────
        self.play(ShowCreation(nn), run_time=2.0)

        # Arrow: face → nn
        arr = Arrow(face.get_right(), nn.get_left(), stroke_color=CYAN, stroke_width=2, buff=0.15)
        self.play(ShowCreation(arr), run_time=1.2)

        vec_label = Tex(r"\text{512-D embedding}", font_size=24, color=GREEN)
        vec_label.next_to(arr, UP, buff=0.15)
        self.play(FadeIn(vec_label, shift=UP * 0.1), run_time=1.0)
        self.wait(2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 4 (28–30s): Camera zoom-in hold
        # ─────────────────────────────────────────────────────────────────
        self.play(
            self.camera.frame.animate.scale(0.85).move_to(face.get_center()),
            run_time=1.5,
        )
        self.wait(0.7)

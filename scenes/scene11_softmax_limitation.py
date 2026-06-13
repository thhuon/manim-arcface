from manimlib import *
from scenes.utils import *

TARGET = 133.2

class Scene11_SoftmaxLimitation(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Limitations of Standard Softmax}", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–35s): Softmax only cares about correct side of boundary
        # ─────────────────────────────────────────────────────────────────
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-2.8, 2.8, 1],
            width=6, height=4.8,
            axis_config={"stroke_color": MUTED, "stroke_width": 0.9},
        )
        ax.shift(DOWN * 0.4)
        center = ax.get_center()
        self.play(ShowCreation(ax), run_time=1.0)

        # Weight vector W1
        w_angle = PI / 4
        w_end = center + 2.2 * np.array([np.cos(w_angle), np.sin(w_angle), 0])
        w_arr = Arrow(center, w_end, stroke_color=CYAN, stroke_width=2.5, buff=0)
        w_lbl = Tex(r"W_1", font_size=24, color=CYAN)
        w_lbl.next_to(w_end, UR, buff=0.12)
        self.play(ShowCreation(w_arr), Write(w_lbl), run_time=1.0)

        # Boundary line
        bnd_angle = w_angle + PI / 2
        bnd1 = center + 3.0 * np.array([np.cos(bnd_angle), np.sin(bnd_angle), 0])
        bnd2 = center - 3.0 * np.array([np.cos(bnd_angle), np.sin(bnd_angle), 0])
        boundary = DashedLine(bnd1, bnd2, stroke_color=MUTED, stroke_width=1.5)
        self.play(ShowCreation(boundary), run_time=1.0)

        # Two embeddings on correct side — close vs far
        e_far = Dot(radius=0.12, color=WHITE)
        e_close = Dot(radius=0.12, color=GREEN)
        far_pos = center + 1.8 * np.array([np.cos(w_angle + 0.05), np.sin(w_angle + 0.05), 0])
        close_pos = center + 1.2 * np.array([np.cos(w_angle + 1.0), np.sin(w_angle + 1.0), 0])
        e_far.move_to(far_pos)
        e_close.move_to(close_pos)

        e_far_lbl = Tex(r"\text{Good}", font_size=20, color=WHITE)
        e_far_lbl.next_to(e_far, UR, buff=0.1)
        e_close_lbl = Tex(r"\text{Still OK?}", font_size=20, color=GREEN)
        e_close_lbl.next_to(e_close, UL, buff=0.1)

        self.play(FadeIn(e_far), Write(e_far_lbl), run_time=0.9)
        self.play(FadeIn(e_close), Write(e_close_lbl), run_time=0.9)

        problem_text = Tex(
            r"\text{Softmax only requires: correct side of boundary}",
            font_size=26, color=MUTED,
        )
        problem_text.to_edge(DOWN, buff=0.5)
        self.play(Write(problem_text), run_time=2.0)
        self.wait(15.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (35–80s): Intra-class spread / inter-class overlap
        # ─────────────────────────────────────────────────────────────────
        self.play(
            FadeOut(e_far), FadeOut(e_far_lbl), FadeOut(e_close),
            FadeOut(e_close_lbl), FadeOut(problem_text), FadeOut(w_arr),
            FadeOut(w_lbl), FadeOut(boundary),
            run_time=0.8,
        )

        sub_lbl = Tex(r"\text{Standard Softmax — Embedding Distribution}", font_size=28, color=WHITE)
        sub_lbl.next_to(title, DOWN, buff=0.35)
        self.play(Write(sub_lbl), run_time=1.2)

        np.random.seed(12)
        soft_dots = VGroup()
        cols_list = [CYAN, GREEN]
        centers_list = [center + LEFT * 0.4 + DOWN * 0.1, center + RIGHT * 0.5 + UP * 0.2]

        for cen, col in zip(centers_list, cols_list):
            for _ in range(15):
                offset = np.random.randn(3) * 0.7  # large spread
                offset[2] = 0
                d = Dot(radius=0.09, color=col)
                d.move_to(cen + offset)
                soft_dots.add(d)

        self.play(ShowCreation(soft_dots), run_time=2.5)

        spread_caption = Tex(
            r"\text{Large intra-class spread, inter-class overlap}",
            font_size=26, color="#FF4444",
        )
        spread_caption.to_edge(DOWN, buff=0.5)
        self.play(Write(spread_caption), run_time=2.0)
        self.wait(25.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (80–133s): Need for margin-based loss
        # ─────────────────────────────────────────────────────────────────
        self.play(FadeOut(soft_dots), FadeOut(sub_lbl), FadeOut(spread_caption), run_time=1.0)

        need_text = Tex(r"\text{We need tighter constraints on the embedding space}", font_size=32, color=WHITE)
        need_text.move_to(UP * 1.0)
        self.play(Write(need_text), run_time=2.0)

        solution_items = [
            r"\bullet\;\text{Minimise intra-class variation (same person \textrightarrow{} close)}",
            r"\bullet\;\text{Maximise inter-class variation (different people \textrightarrow{} far)}",
            r"\bullet\;\text{Add angular margin to enforce strict boundaries}",
        ]
        sol_group = VGroup(*[Tex(t, font_size=26, color=CYAN) for t in solution_items])
        sol_group.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        sol_group.next_to(need_text, DOWN, buff=0.5)
        sol_group.to_edge(LEFT, buff=0.8)

        for item in sol_group:
            self.play(FadeIn(item, shift=RIGHT * 0.1), run_time=1.2)
            self.wait(3.0)

        self.wait(20.0)
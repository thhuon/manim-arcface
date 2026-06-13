from manimlib import *
from scenes.utils import *

TARGET = 79.6

class Scene16_ArcfaceCore2dVisualComparison(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Softmax vs ArcFace — 2D Comparison}", font_size=44, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=2.0)

        left_lbl = Tex(r"\text{Softmax}", font_size=30, color=MUTED)
        right_lbl = Tex(r"\text{ArcFace}", font_size=30, color=CYAN)
        left_lbl.shift(LEFT * 3.5 + UP * 1.8)
        right_lbl.shift(RIGHT * 3.5 + UP * 1.8)
        divider = Line(UP * 3.5, DOWN * 3.5, stroke_color=MUTED, stroke_width=1.0)
        self.play(Write(left_lbl), Write(right_lbl), ShowCreation(divider), run_time=1.0)

        circle_l = Circle(radius=2.0, stroke_color=MUTED, stroke_width=1.2)
        circle_l.shift(LEFT * 3.5 + DOWN * 0.3)
        circle_r = Circle(radius=2.0, stroke_color=CYAN, stroke_width=1.5)
        circle_r.shift(RIGHT * 3.5 + DOWN * 0.3)
        self.play(ShowCreation(circle_l), ShowCreation(circle_r), run_time=1.2)

        center_l = circle_l.get_center()
        center_r = circle_r.get_center()
        np.random.seed(5)

        # Softmax: loose clusters
        for angle_base, col in [(PI / 5, CYAN), (-PI / 3, GREEN), (PI, "#FF4444")]:
            for _ in range(8):
                offset_angle = angle_base + np.random.uniform(-0.7, 0.7)
                offset_r = np.random.uniform(1.0, 1.9)
                pos = center_l + offset_r * np.array([np.cos(offset_angle), np.sin(offset_angle), 0])
                d = Dot(radius=0.09, color=col)
                d.move_to(pos)
                self.add(d)

        # ArcFace: tight clusters
        for angle_base, col in [(PI / 5, CYAN), (-PI / 3, GREEN), (PI, "#FF4444")]:
            for _ in range(8):
                offset_angle = angle_base + np.random.uniform(-0.22, 0.22)
                offset_r = np.random.uniform(1.7, 2.0)
                pos = center_r + offset_r * np.array([np.cos(offset_angle), np.sin(offset_angle), 0])
                d = Dot(radius=0.09, color=col)
                d.move_to(pos)
                self.add(d)

        # Animate adding them with a flash
        self.wait(2.0)

        # Boundary lines — Softmax blurry, ArcFace clear
        for i, (base_col, center) in enumerate([(MUTED, center_l), (CYAN, center_r)]):
            for boundary_angle in [PI / 2, -PI / 6, 5 * PI / 6]:
                end1 = center + 2.2 * np.array([np.cos(boundary_angle), np.sin(boundary_angle), 0])
                end2 = center - 2.2 * np.array([np.cos(boundary_angle), np.sin(boundary_angle), 0])
                bl = DashedLine(end1, end2, stroke_color=base_col,
                                stroke_width=1.0 + i * 1.0, dash_length=0.12)
                self.add(bl)

        self.wait(3.0)

        caption_l = Tex(r"\text{Fuzzy boundaries}", font_size=22, color=MUTED)
        caption_l.next_to(circle_l, DOWN, buff=0.3)
        caption_r = Tex(r"\text{Clear angular margins}", font_size=22, color=CYAN)
        caption_r.next_to(circle_r, DOWN, buff=0.3)
        self.play(Write(caption_l), Write(caption_r), run_time=1.5)
        self.wait(35.0)
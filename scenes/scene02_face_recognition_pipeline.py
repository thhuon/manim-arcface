from manimlib import *
from scenes.utils import *

TARGET = 150.5  # seconds — the longest scene

class Scene02_FaceRecognitionPipeline(Scene):
    def construct(self):
        self.camera.background_color = DARK

        # ─────────────────────────────────────────────────────────────────
        # BEAT 1 (0–20s): Title — "4 stages of face recognition"
        # ─────────────────────────────────────────────────────────────────
        title = Tex(r"\text{Face Recognition Pipeline}", font_size=54, color=WHITE)
        title.to_edge(UP, buff=0.5)
        sub = Tex(r"\text{4 main stages}", font_size=30, color=CYAN)
        sub.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=2.0)
        self.play(FadeIn(sub, shift=UP * 0.1), run_time=1.2)
        self.wait(3.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 2 (5–40s): The 4 stages appear as boxes with arrows
        # ─────────────────────────────────────────────────────────────────
        stage_data = [
            (r"\text{1. Face}\\\text{Detection}", CYAN),
            (r"\text{2. Alignment}\\\text{\& Crop}", GREEN),
            (r"\text{3. Feature}\\\text{Extraction}", BLUE),
            (r"\text{4. Matching}\\\text{\& Decision}", WHITE),
        ]

        boxes = VGroup()
        for text, color in stage_data:
            box = make_box([text], width=2.4, height=1.5, stroke=color, font_size=24)
            boxes.add(box)
        boxes.arrange(RIGHT, buff=0.7)
        boxes.next_to(sub, DOWN, buff=0.6)

        arrows = VGroup()
        for i in range(len(boxes) - 1):
            a = Arrow(boxes[i].get_right(), boxes[i + 1].get_left(),
                      stroke_color=MUTED, stroke_width=2, buff=0.05)
            arrows.add(a)

        for i, (box, color) in enumerate(zip(boxes, [d[1] for d in stage_data])):
            self.play(FadeIn(box, shift=UP * 0.2), run_time=1.0)
            if i < len(arrows):
                self.play(ShowCreation(arrows[i]), run_time=0.6)
            self.wait(1.5)

        self.wait(5.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 3 (40–70s): Stage 1 highlight — Detection
        # ─────────────────────────────────────────────────────────────────
        # Fade everything except stage 1
        self.play(
            *[box.animate.set_opacity(0.2) for box in boxes[1:]],
            *[arr.animate.set_opacity(0.1) for arr in arrows],
            run_time=1.0,
        )

        face = make_abstract_face()
        face.scale(1.8).shift(DOWN * 1.5)

        # Bounding box
        bbox = Rectangle(width=face.get_width() * 1.15, height=face.get_height() * 1.15,
                         stroke_color=CYAN, stroke_width=2.5)
        bbox.move_to(face)

        det_label = Tex(r"\text{Locate face region in image}", font_size=26, color=WHITE)
        det_label.to_edge(DOWN, buff=0.5)

        self.play(ShowCreation(face), run_time=1.5)
        self.play(ShowCreation(bbox), run_time=1.0)
        self.play(Write(det_label), run_time=1.5)
        self.wait(10.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 4 (70–100s): Stage 2 — Alignment & Crop
        # ─────────────────────────────────────────────────────────────────
        self.play(
            boxes[0].animate.set_opacity(0.2),
            boxes[1].animate.set_opacity(1.0),
            FadeOut(det_label),
            run_time=1.0,
        )

        lm = make_landmarks()
        lm.scale(1.8).move_to(face.get_center())

        align_label = Tex(r"\text{Detect landmarks \& align to standard pose}", font_size=26, color=WHITE)
        align_label.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(lm), run_time=1.2)
        self.play(Write(align_label), run_time=1.5)
        self.wait(12.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 5 (100–125s): Stage 3 — Feature Extraction via CNN
        # ─────────────────────────────────────────────────────────────────
        self.play(
            boxes[1].animate.set_opacity(0.2),
            boxes[2].animate.set_opacity(1.0),
            FadeOut(align_label),
            run_time=1.0,
        )

        nn = make_neural_network()
        nn.scale(1.3).move_to(DOWN * 1.5)

        cnn_arrow = Arrow(face.get_right() + LEFT * 0.5, nn.get_left(), stroke_color=CYAN, stroke_width=2)
        vec = make_vector([r"0.42", r"-0.87", r"0.13", r"\vdots"], font_size=19)
        vec.next_to(nn, RIGHT, buff=0.4)

        feat_label = Tex(r"\text{CNN extracts 512-D embedding vector}", font_size=26, color=WHITE)
        feat_label.to_edge(DOWN, buff=0.5)

        self.play(
            FadeOut(face), FadeOut(bbox), FadeOut(lm),
            ShowCreation(nn), run_time=1.5,
        )
        self.play(ShowCreation(cnn_arrow), FadeIn(vec), run_time=1.2)
        self.play(Write(feat_label), run_time=1.5)
        self.wait(12.0)

        # ─────────────────────────────────────────────────────────────────
        # BEAT 6 (125–150s): Stage 4 — Matching & Decision
        # ─────────────────────────────────────────────────────────────────
        self.play(
            boxes[2].animate.set_opacity(0.2),
            boxes[3].animate.set_opacity(1.0),
            FadeOut(feat_label), FadeOut(cnn_arrow), FadeOut(nn), FadeOut(vec),
            run_time=1.0,
        )

        # Two embedding vectors with similarity score
        v1 = make_vector([r"0.42", r"-0.87", r"0.13"], font_size=20)
        v1.shift(LEFT * 2.5 + DOWN * 1.0)
        v2 = make_vector([r"0.40", r"-0.85", r"0.14"], font_size=20)
        v2.shift(RIGHT * 2.5 + DOWN * 1.0)

        sim_arr = Arrow(v1.get_right(), v2.get_left(), stroke_color=GREEN, stroke_width=2.5)
        sim_label = Tex(r"\cos\theta = 0.998\;\Rightarrow\;\text{SAME PERSON}", font_size=26, color=GREEN)
        sim_label.next_to(sim_arr, UP, buff=0.2)

        match_label = Tex(r"\text{Compare embeddings using cosine similarity}", font_size=26, color=WHITE)
        match_label.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(v1), FadeIn(v2), run_time=1.2)
        self.play(ShowCreation(sim_arr), run_time=1.0)
        self.play(Write(sim_label), run_time=1.5)
        self.play(Write(match_label), run_time=1.5)
        self.wait(10.0)
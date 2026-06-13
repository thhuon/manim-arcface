from manimlib import *
from scenes.utils import *

TARGET = 42.5

class Scene03_Challenges(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Challenges in Face Recognition}", font_size=48, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        # ── 4 challenge cards ─────────────────────────────────────────────
        challenges = [
            (r"\text{Lighting}\\\text{Variation}", CYAN),
            (r"\text{Pose \&}\\\text{Angle}", GREEN),
            (r"\text{Occlusion}", BLUE),
            (r"\text{Aging}", WHITE),
        ]
        cards = VGroup()
        for text, color in challenges:
            c = make_box([text], width=2.2, height=1.4, stroke=color, font_size=24)
            cards.add(c)
        cards.arrange(RIGHT, buff=0.55)
        cards.next_to(title, DOWN, buff=0.7)

        for i, card in enumerate(cards):
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
            self.wait(1.5)

        self.wait(3.0)

        # ── Variability demo: same face, different conditions ─────────────
        demo_label = Tex(r"\text{Same person — different conditions}", font_size=28, color=CYAN)
        demo_label.next_to(cards, DOWN, buff=0.6)
        self.play(Write(demo_label), run_time=1.5)

        # Show faces from assets
        face_imgs = VGroup()
        for i in [3, 12, 24, 35]:
            img = ImageMobject(asset_path(f"face_{i}.png"))
            img.set_height(1.6)
            face_imgs.add(img)
        face_imgs.arrange(RIGHT, buff=0.4)
        face_imgs.next_to(demo_label, DOWN, buff=0.4)

        self.play(FadeIn(face_imgs), run_time=2.0)
        self.wait(5.0)

        # ── Key message ───────────────────────────────────────────────────
        key_msg = Tex(r"\text{A robust system must handle all these variations}", font_size=26, color=WHITE)
        key_msg.to_edge(DOWN, buff=0.5)
        self.play(Write(key_msg), run_time=2.0)
        self.wait(8.0)

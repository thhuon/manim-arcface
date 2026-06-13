from manimlib import *
from scenes.utils import *

TARGET = 33.6

class Scene27_Applications(Scene):
    def construct(self):
        self.camera.background_color = DARK

        title = Tex(r"\text{Real-World Applications}", font_size=52, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=2.0)

        applications = [
            (r"\text{Smartphones}", r"\text{Face ID unlock}", CYAN),
            (r"\text{Banking / ATM}", r"\text{Customer recognition}", GREEN),
            (r"\text{Airports}", r"\text{Automated check-in}", BLUE),
            (r"\text{Social Networks}", r"\text{Auto-tagging friends}", WHITE),
            (r"\text{Medical}", r"\text{Genetic disorder diagnosis}", "#FFD700"),
        ]

        icons = VGroup()
        for i, (name, use, col) in enumerate(applications):
            cam = make_camera_icon() if i == 0 else make_abstract_face()
            cam.scale(0.8)
            name_tex = Tex(name, font_size=26, color=col)
            use_tex = Tex(use, font_size=22, color=WHITE)
            item = VGroup(cam, name_tex, use_tex)
            item.arrange(RIGHT, buff=0.4)
            icons.add(item)

        icons.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        icons.next_to(title, DOWN, buff=0.5)
        icons.to_edge(LEFT, buff=0.8)

        for item in icons:
            self.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.8)
            self.wait(2.0)

        self.wait(6.0)
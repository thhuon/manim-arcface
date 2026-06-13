from manimlib import *
from scenes.utils import *

class Scene27_Applications(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        title = Tex(r"\text{Applications of Face Embedding Systems}", font_size=72)
        title.to_edge(UP, buff=1.0)

        self.play(Write(title), run_time=2.0)

        # Face ID on smartphones
        smartphone = ImageMobject(asset_path("smartphone.png")).set_height(2.5)
        face_id = SVGMobject(asset_path("face-id.svg"), height=1.5)
        smartphone_group = Group(smartphone, face_id)
        smartphone_group.arrange(DOWN, buff=0.2)
        smartphone_group.to_edge(LEFT, buff=1.5)

        self.play(FadeIn(smartphone), ShowCreation(face_id), run_time=2.0)
        self.play(smartphone_group.animate.to_edge(RIGHT, buff=1.5), run_time=1.5)

        # Automated check-in at airports
        airport_icon = ImageMobject(asset_path("security_camera.png")).set_height(2.0)
        airport_icon.to_edge(RIGHT, buff=1.5)

        self.play(FadeIn(airport_icon), run_time=2.0)

        # Tagging friends on social networks
        social_network_icon = ImageMobject(asset_path("face_scan.png")).set_height(2.0)
        social_network_icon.next_to(airport_icon, DOWN, buff=0.5)

        self.play(FadeIn(social_network_icon), run_time=2.0)

        # Medical applications
        medical_icon = SVGMobject(asset_path("brain.svg"), height=2.0)
        medical_icon.next_to(social_network_icon, DOWN, buff=0.5)

        self.play(ShowCreation(medical_icon), run_time=2.0)

        self.wait(2.0)

        self.play(FadeOut(title), FadeOut(smartphone_group), FadeOut(airport_icon), FadeOut(social_network_icon), FadeOut(medical_icon), run_time=2.0)
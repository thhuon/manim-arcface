from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 08 — Closing
# =============================================================================


# =============================================================================
# BEAT 1: Real-World Applications
# =============================================================================
def beat_1_applications(scene):
    """Grid of application domains with icons and descriptions."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Real-World Applications}", font_size=52, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    applications = [
        (r"\text{Smartphones}", r"\text{Face ID unlock}", CYAN),
        (r"\text{Banking / ATM}", r"\text{Customer recognition}", GREEN),
        (r"\text{Airports}", r"\text{Automated check-in}", BLUE),
        (r"\text{Social Networks}", r"\text{Auto-tagging friends}", WHITE),
        (r"\text{Medical}", r"\text{Genetic disorder diagnosis}", YELLOW),
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
        scene.play(FadeIn(item, shift=RIGHT * 0.1), run_time=0.8)
        scene.wait(2.0)

    scene.wait(6.0)


# =============================================================================
# BEAT 2: Closing — Final Embedding Space Reveal
# =============================================================================
def beat_2_closing(scene):
    """Neural network feeding into tight embedding clusters on the unit hypersphere."""
    scene.camera.background_color = DARK

    sphere = Circle(radius=2.4, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0)
    sphere.shift(DOWN * 0.5)
    center = sphere.get_center()

    np.random.seed(99)
    colours = [CYAN, GREEN, RED, YELLOW]
    bases = [PI / 5, 2 * PI / 3, -PI / 3, PI + PI / 4]
    dots = VGroup()
    for angle_base, col in zip(bases, colours):
        for _ in range(8):
            a = angle_base + np.random.uniform(-0.18, 0.18)
            r = np.random.uniform(2.1, 2.4)
            d = Dot(radius=0.10, color=col)
            d.move_to(center + r * np.array([np.cos(a), np.sin(a), 0]))
            dots.add(d)

    nn = make_neural_network()
    nn.scale(1.2).shift(UP * 2.5)

    scene.play(ShowCreation(nn), run_time=1.5)
    scene.play(ShowCreation(sphere), run_time=1.0)
    scene.play(ShowCreation(dots), run_time=1.5)
    scene.wait(2.0)

    scene.play(scene.camera.frame.animate.scale(1.15), run_time=1.5)

    closing = Tex(
        r"\text{From pixels } \rightarrow \text{ geometry } \rightarrow \text{ identity}",
        font_size=34, color=WHITE,
    )
    closing.to_edge(DOWN, buff=0.8)
    scene.play(Write(closing), run_time=2.0)
    scene.wait(3.0)

    thankyou = Tex(r"\text{Thank you for watching!}", font_size=44, color=YELLOW)
    thankyou.to_edge(DOWN, buff=0.3)
    scene.play(FadeOut(closing), FadeIn(thankyou, shift=UP * 0.2), run_time=1.5)
    scene.wait(4.0)


# =============================================================================
# MAIN SCENE: plays all beats in sequence
# =============================================================================
class Scene08_Closing(Scene):
    def construct(self):
        beat_1_applications(self)
        self.clear()
        self.wait(1.0)

        beat_2_closing(self)

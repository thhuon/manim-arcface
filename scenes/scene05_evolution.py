from manimlib import *
from scenes.utils import *


# =============================================================================
# SCENE 05 - Evolution
# Implements Scene 5 (Evolution) per PLAN.md:
# - Beat A: Milestones (FaceNet → SphereFace → CosFace → ArcFace)
# - Beat B: Transition to ArcFace Mechanism
# =============================================================================




# =============================================================================
# BEAT 0: Evolution Timeline (Scene 5 Beat A)
# =============================================================================
def beat_0_evolution_timeline(scene):
    """Timeline of face recognition milestones."""
    scene.camera.background_color = DARK

    title = Tex(r"\text{Evolution of Face Recognition}", font_size=48, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

    milestones = [
        ("2015", "FaceNet", GREEN, r"\text{Triplet loss}"),
        ("2017", "SphereFace", CYAN, r"\text{Multiplicative angular margin}"),
        ("2018", "CosFace", BLUE, r"\text{Additive cosine margin}"),
        ("2018", "ArcFace", ORANGE, r"\text{Additive angular margin}"),
    ]

    timeline_line = Line(LEFT * 5.5, RIGHT * 5.5, stroke_color=MUTED, stroke_width=1.5)
    timeline_line.shift(DOWN * 0.5)
    scene.play(ShowCreation(timeline_line), run_time=1.2)

    tick_positions = np.linspace(-4.5, 4.5, len(milestones))

    arcface_lbl = None
    for i, (year, name, col, desc) in enumerate(milestones):
        x = tick_positions[i]
        tick = Line(DOWN * 0.15, UP * 0.15, stroke_color=col, stroke_width=2.5)
        tick.move_to(timeline_line.get_center() + x * RIGHT)

        year_lbl = Tex(year, font_size=20, color=col)
        name_lbl = Tex(r"\text{" + name + r"}", font_size=22, color=col)
        desc_lbl = Tex(desc, font_size=18, color=WHITE)

        year_lbl.next_to(tick, DOWN, buff=0.2)
        if i % 2 == 0:
            name_lbl.next_to(tick, UP, buff=0.4)
            desc_lbl.next_to(name_lbl, UP, buff=0.15)
        else:
            name_lbl.next_to(tick, DOWN, buff=0.6)
            desc_lbl.next_to(name_lbl, DOWN, buff=0.15)

        scene.play(ShowCreation(tick), Write(year_lbl), run_time=0.7)
        scene.play(Write(name_lbl), Write(desc_lbl), run_time=1.0)
        scene.wait(2.0)

        if name == "ArcFace":
            arcface_lbl = name_lbl

    if arcface_lbl:
        arcface_highlight = SurroundingRectangle(arcface_lbl, color=ORANGE, buff=0.1)
        scene.play(ShowCreation(arcface_highlight), run_time=1.2)

    arcface_caption = Tex(r"\text{State-of-the-art: Additive Angular Margin}", font_size=26, color=ORANGE)
    arcface_caption.to_edge(DOWN, buff=0.5)
    scene.wait(3.0)

    clear_scene(scene, run_time=0.65, wait_time=0.15)

    next_label = VGroup(
        latex(r"\text{Next: ArcFace Mechanism}", size=37, color=CYAN),
        latex(r"\text{How ArcFace works — geometry and formula}", size=23, color=WHITE),
    ).arrange(DOWN, buff=0.16)
    next_label.move_to(ORIGIN)
    scene.play(FadeIn(next_label), run_time=0.75)
    scene.wait(1.0)


# =============================================================================
# MAIN SCENE
# =============================================================================
class Scene05_Evolution(Scene):
    def construct(self):
        beat_0_evolution_timeline(self)
        clear_scene(self, run_time=0.65, wait_time=0.15)

        next_label = VGroup(
            latex(r"\text{Next: ArcFace Mechanism}", size=37, color=CYAN),
            latex(r"\text{How ArcFace works — geometry and formula}", size=23, color=WHITE),
        ).arrange(DOWN, buff=0.16)
        next_label.move_to(ORIGIN)
        self.play(FadeIn(next_label), run_time=0.75)
        self.wait(1.0)

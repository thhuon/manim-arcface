from manimlib import *
from scenes.utils import *

DARK_BG = "#090D14"


# =============================================================================
# BEAT 1: Challenges in Face Recognition
# =============================================================================
def beat_1_challenges(scene):
    """Show 4 challenge cards + variability demo."""
    scene.camera.background_color = DARK_BG

    title = Tex(r"\text{Challenges in Face Recognition}", font_size=48, color=WHITE)
    title.to_edge(UP, buff=0.5)
    scene.play(Write(title), run_time=2.0)

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

    for card in cards:
        scene.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)
        scene.wait(1.5)

    scene.wait(3.0)

    demo_label = Tex(r"\text{Same person — different conditions}", font_size=28, color=CYAN)
    demo_label.next_to(cards, DOWN, buff=0.6)
    scene.play(Write(demo_label), run_time=1.5)

    face_imgs = Group()
    for i in [3, 12, 24, 35]:
        img = ImageMobject(asset_path(f"face_{i}.png"))
        img.set_height(1.6)
        face_imgs.add(img)
    face_imgs.arrange(RIGHT, buff=0.4)
    face_imgs.next_to(demo_label, DOWN, buff=0.4)

    scene.play(FadeIn(face_imgs), run_time=2.0)
    scene.wait(5.0)

    key_msg = Tex(r"\text{A robust system must handle all these variations}", font_size=26, color=WHITE)
    key_msg.to_edge(DOWN, buff=0.5)
    scene.play(Write(key_msg), run_time=2.0)
    scene.wait(3.0)


# =============================================================================
# BEAT 2: Embedding Space Concept
# =============================================================================
def beat_2_embedding_concept(scene):
    """What is an embedding space + random vs clustered embeddings."""
    scene.camera.background_color = DARK_BG

    title = Tex(r"\text{Embedding Space}", font_size=54, color=WHITE)
    title.to_edge(UP, buff=0.4)
    scene.play(Write(title), run_time=2.0)

    # --- What is an embedding space ---
    defn = Tex(
        r"\text{A geometric space learned by a neural network during training.}",
        font_size=30, color=WHITE,
    )
    defn.next_to(title, DOWN, buff=0.45)
    scene.play(Write(defn), run_time=2.5)

    nn = make_neural_network()
    nn.scale(1.4).shift(DOWN * 0.5 + LEFT * 2)

    face_in = make_abstract_face()
    face_in.scale(1.2).to_edge(LEFT, buff=0.5)
    face_in.shift(DOWN * 0.5)

    vec = make_vector([r"v_1", r"v_2", r"\vdots", r"v_{512}"], font_size=20)
    vec.shift(RIGHT * 2.8 + DOWN * 0.5)

    arr1 = Arrow(face_in.get_right(), nn.get_left(), stroke_color=CYAN, stroke_width=2)
    arr2 = Arrow(nn.get_right(), vec.get_left(), stroke_color=CYAN, stroke_width=2)

    scene.play(ShowCreation(face_in), run_time=1.5)
    scene.play(ShowCreation(nn), run_time=1.5)
    scene.play(ShowCreation(arr1), ShowCreation(arr2), run_time=1.2)
    scene.play(FadeIn(vec, shift=LEFT * 0.2), run_time=1.2)

    emb_label = Tex(r"\text{Embedding: numerical representation of a face identity}", font_size=26, color=CYAN)
    emb_label.to_edge(DOWN, buff=0.5)
    scene.play(Write(emb_label), run_time=2.0)
    scene.wait(15.0)

    # --- Random distribution ---
    scene.play(
        FadeOut(defn), FadeOut(face_in), FadeOut(nn),
        FadeOut(arr1), FadeOut(arr2), FadeOut(vec), FadeOut(emb_label),
        run_time=1.0,
    )

    ax = Axes(
        x_range=[-3.5, 3.5, 1], y_range=[-2.5, 2.5, 1],
        width=6, height=4,
        axis_config={"stroke_color": MUTED, "stroke_width": 1.0},
    )
    ax.shift(DOWN * 0.4)
    scene.play(ShowCreation(ax), run_time=1.2)

    rand_label = Tex(r"\text{Initial: embeddings are nearly random}", font_size=28, color=MUTED)
    rand_label.next_to(title, DOWN, buff=0.4)
    scene.play(Write(rand_label), run_time=1.5)

    np.random.seed(7)
    colours_map = {0: CYAN, 1: GREEN, 2: "#FF4444"}
    dots_init = VGroup()
    identities = []
    for _ in range(30):
        identity = np.random.randint(0, 3)
        identities.append(identity)
        pos = np.random.uniform(-3, 3, 3)
        pos[2] = 0
        d = Dot(radius=0.10, color=colours_map[identity])
        d.move_to(pos)
        dots_init.add(d)

    scene.play(ShowCreation(dots_init), run_time=2.5)
    scene.wait(10.0)

    # --- Clusters form ---
    opt_label = Tex(r"\text{After training: same identity clusters together}", font_size=28, color=CYAN)
    opt_label.next_to(title, DOWN, buff=0.4)
    scene.play(FadeOut(rand_label), Write(opt_label), run_time=1.5)

    cluster_targets = {
        0: LEFT * 2 + UP * 1.2,
        1: RIGHT * 2 + UP * 1.2,
        2: ORIGIN + DOWN * 1.5,
    }

    np.random.seed(99)
    anims = []
    for dot, identity in zip(dots_init, identities):
        target_center = cluster_targets[identity]
        offset = np.random.randn(3) * 0.3
        offset[2] = 0
        anims.append(dot.animate.move_to(target_center + offset))

    scene.play(*anims, run_time=3.5)
    scene.wait(15.0)

    for identity, center in cluster_targets.items():
        ring = Circle(
            radius=0.7,
            stroke_color=colours_map[identity],
            stroke_width=2, stroke_opacity=0.5, fill_opacity=0,
        )
        ring.move_to(center)
        scene.play(ShowCreation(ring), run_time=0.8)

    scene.wait(5.0)

    # --- Key takeaway ---
    takeaway = Tex(
        r"\text{Face recognition} = \text{measuring distances in embedding space}",
        font_size=28, color=GREEN,
    )
    takeaway.to_edge(DOWN, buff=0.5)
    scene.play(Write(takeaway), run_time=2.0)
    scene.wait(5.0)


# =============================================================================
# BEAT 3: Embedding Transition / Hypersphere
# =============================================================================
def beat_3_hypersphere(scene):
    """Unit hypersphere and angular distance."""
    scene.camera.background_color = DARK_BG

    recap = Tex(r"\text{Recap: Faces mapped to embedding vectors}", font_size=40, color=WHITE)
    recap.to_edge(UP, buff=0.5)
    scene.play(Write(recap), run_time=2.0)

    sphere = Circle(radius=2.5, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
    sphere.shift(DOWN * 0.5)
    scene.play(ShowCreation(sphere), run_time=1.5)

    np.random.seed(3)
    points_on_sphere = VGroup()
    labels_sphere = VGroup()
    colours = [CYAN, GREEN, "#FF4444", WHITE, BLUE]
    angle_list = np.linspace(0, 2 * PI, 5, endpoint=False)
    for i, angle in enumerate(angle_list):
        pt = sphere.get_center() + 2.5 * np.array([np.cos(angle), np.sin(angle), 0])
        d = Dot(radius=0.13, color=colours[i])
        d.move_to(pt)
        lbl = Tex(f"\\text{{ID {i+1}}}", font_size=20, color=colours[i])
        lbl.next_to(d, pt - sphere.get_center(), buff=0.18)
        points_on_sphere.add(d)
        labels_sphere.add(lbl)

    scene.play(ShowCreation(points_on_sphere), run_time=1.5)
    scene.play(FadeIn(labels_sphere), run_time=1.0)

    sphere_label = Tex(r"\text{Unit Hypersphere: } \lVert f \rVert = 1", font_size=28, color=CYAN)
    sphere_label.to_edge(DOWN, buff=0.5)
    scene.play(Write(sphere_label), run_time=1.5)
    scene.wait(10.0)

    # Angle between two points
    pt0 = sphere.get_center() + 2.5 * np.array([np.cos(angle_list[0]), np.sin(angle_list[0]), 0])
    pt1 = sphere.get_center() + 2.5 * np.array([np.cos(angle_list[1]), np.sin(angle_list[1]), 0])
    angle_line0 = Line(sphere.get_center(), pt0, stroke_color=WHITE, stroke_width=1.5)
    angle_line1 = Line(sphere.get_center(), pt1, stroke_color=WHITE, stroke_width=1.5)
    angle_arc = Arc(
        radius=0.7,
        start_angle=angle_list[0],
        angle=angle_list[1] - angle_list[0],
        stroke_color=GREEN, stroke_width=2,
    )
    angle_arc.shift(sphere.get_center())
    theta_label = Tex(r"\theta", font_size=26, color=GREEN)
    theta_label.move_to(
        sphere.get_center()
        + 0.9 * np.array([
            np.cos((angle_list[0] + angle_list[1]) / 2),
            np.sin((angle_list[0] + angle_list[1]) / 2),
            0,
        ])
    )

    scene.play(ShowCreation(angle_line0), ShowCreation(angle_line1), run_time=1.0)
    scene.play(ShowCreation(angle_arc), Write(theta_label), run_time=1.2)

    cos_label = Tex(r"\text{Distance} = \cos\theta \text{ (angular distance)}", font_size=26, color=GREEN)
    cos_label.next_to(sphere_label, UP, buff=0.25)
    scene.play(Write(cos_label), run_time=1.5)
    scene.wait(15.0)


# =============================================================================
# MAIN SCENE: plays all beats in sequence
# =============================================================================
class Scene04_EmbeddingSpace(Scene):
    def construct(self):
        # Beat 1: Challenges
        beat_1_challenges(self)
        self.clear()
        self.wait(1.0)

        # Beat 2: Embedding Space Concept
        beat_2_embedding_concept(self)
        self.clear()
        self.wait(1.0)

        # Beat 3: Hypersphere
        beat_3_hypersphere(self)

from manimlib import *
import os
from scenes.utils import *


# =============================================================================
# SCENE-SPECIFIC HELPERS - For scene04_EmbeddingSpace
# =============================================================================

ACCENT = "#4A7DFF"
PURPLE = "#A855F7"


def get_face_image(filename: str, height: float = 1.0):
    """Load face image with consistent styling."""
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    img = ImageMobject(path)
    img.set_height(height)
    return img


def create_building(width=0.4, height=0.6, style="modern", stroke_color=CYAN, fill_opacity=0.1):
    """Create a building rectangle with optional roof based on style."""
    if style == "modern":
        # Tall, clean rectangle
        building = Rectangle(
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=PANEL,
            fill_opacity=fill_opacity
        )
    elif style == "classical":
        # Rectangle with triangular roof
        base = Rectangle(
            width=width,
            height=height * 0.7,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=PANEL,
            fill_opacity=fill_opacity
        )
        roof_height = height * 0.35
        roof = Polygon(
            base.get_corner(DL),
            base.get_corner(DR),
            [0, base.get_corner(UL)[1] + roof_height, 0],
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=PANEL,
            fill_opacity=fill_opacity
        )
        building = VGroup(base, roof)
    else:  # industrial
        # Wide, shorter rectangle with flat top
        building = Rectangle(
            width=width * 1.3,
            height=height * 0.5,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=PANEL,
            fill_opacity=fill_opacity
        )
    return building


def create_cluster_circle(center, radius=1.0, color=CYAN, fill_opacity=0.03, stroke_opacity=0.4):
    """Create a soft glowing cluster circle."""
    circle = Circle(
        radius=radius,
        stroke_color=color,
        stroke_width=2,
        fill_color=color,
        fill_opacity=fill_opacity
    )
    circle.move_to(center)
    # Add outer glow ring
    glow = Circle(
        radius=radius * 1.15,
        stroke_color=color,
        stroke_width=4,
        stroke_opacity=stroke_opacity * 0.3,
        fill_opacity=0
    )
    glow.move_to(center)
    return VGroup(glow, circle)


def create_neural_network_faded():
    """Create a neural network with muted edges for background use."""
    layers = [3, 5, 5, 3]
    groups = VGroup()
    for count in layers:
        col = VGroup(*[Circle(radius=0.105, stroke_color=CYAN, stroke_width=1.5, fill_opacity=0) for _ in range(count)])
        col.arrange(DOWN, buff=0.15)
        groups.add(col)
    groups.arrange(RIGHT, buff=0.46)

    edges = VGroup()
    for a, b in zip(groups[:-1], groups[1:]):
        for n1 in a:
            for n2 in b:
                edges.add(Line(n1.get_center(), n2.get_center(), stroke_color=WHITE, stroke_width=0.7, stroke_opacity=0.15))
    return VGroup(edges, groups)


def create_embedding_point(position, color=CYAN, radius=0.12):
    """Create a glowing embedding point."""
    point = Dot(position, color=color, radius=radius)
    glow = Circle(radius=radius * 2.5, stroke_color=color, stroke_width=3, fill_opacity=0, stroke_opacity=0.25)
    glow.move_to(position)
    return VGroup(glow, point)


def create_training_loop(center, scale=1.0):
    """Create a visual training loop: Face -> Network -> Embedding -> Loss -> Update."""
    loop_group = VGroup()

    # Define positions in a loop
    radius = 1.5 * scale
    angle_offset = -90 * DEGREES

    positions = [
        center + radius * np.array([np.cos(angle_offset), np.sin(angle_offset), 0]),  # top
        center + radius * np.array([np.cos(angle_offset + 90 * DEGREES), np.sin(angle_offset + 90 * DEGREES), 0]),  # right
        center + radius * np.array([np.cos(angle_offset + 180 * DEGREES), np.sin(angle_offset + 180 * DEGREES), 0]),  # bottom
        center + radius * np.array([np.cos(angle_offset + 270 * DEGREES), np.sin(angle_offset + 270 * DEGREES), 0]),  # left
    ]

    # Node 1: Face icon (simplified)
    face_circle = Circle(radius=0.25 * scale, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
    face_label = Tex(r"\mathbf{I}", font_size=18 * scale)
    face_label.move_to(face_circle)
    face_node = VGroup(face_circle, face_label)
    face_node.move_to(positions[0])

    # Node 2: Network
    net_box = RoundedRectangle(
        width=0.8 * scale,
        height=0.4 * scale,
        corner_radius=0.08 * scale,
        stroke_color=CYAN,
        stroke_width=2,
        fill_color=PANEL,
        fill_opacity=0.2
    )
    net_label = Tex(r"f_\theta", font_size=16 * scale)
    net_label.move_to(net_box)
    net_node = VGroup(net_box, net_label)
    net_node.move_to(positions[1])

    # Node 3: Embedding
    emb_circle = Circle(radius=0.2 * scale, stroke_color=WHITE, stroke_width=2, fill_opacity=0)
    emb_label = Tex(r"\mathbf{x}", font_size=16 * scale)
    emb_label.move_to(emb_circle)
    emb_node = VGroup(emb_circle, emb_label)
    emb_node.move_to(positions[2])

    # Node 4: Loss
    loss_box = RoundedRectangle(
        width=0.7 * scale,
        height=0.35 * scale,
        corner_radius=0.08 * scale,
        stroke_color=GREEN,
        stroke_width=2,
        fill_color=PANEL,
        fill_opacity=0.2
    )
    loss_label = Tex(r"\mathcal{L}", font_size=16 * scale, color=GREEN)
    loss_label.move_to(loss_box)
    loss_node = VGroup(loss_box, loss_label)
    loss_node.move_to(positions[3])

    # Curved arrows between nodes
    arrows = VGroup()
    arrow_colors = [CYAN, CYAN, GREEN, CYAN]  # Last one goes back with update color

    for i in range(4):
        start = positions[i]
        end = positions[(i + 1) % 4]
        mid = (start + end) / 2

        # Determine which direction for the curve
        if i == 0:  # Face to Network
            arrow = Arrow(start + DOWN * 0.3 * scale, end + LEFT * 0.3 * scale, buff=0.05, color=CYAN, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        elif i == 1:  # Network to Embedding
            arrow = Arrow(start + LEFT * 0.3 * scale, end + UP * 0.3 * scale, buff=0.05, color=CYAN, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        elif i == 2:  # Embedding to Loss
            arrow = Arrow(start + UP * 0.3 * scale, end + RIGHT * 0.3 * scale, buff=0.05, color=GREEN, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        else:  # Loss to Face (update)
            arrow = Arrow(start + RIGHT * 0.3 * scale, end + UP * 0.3 * scale, buff=0.05, color=PURPLE, stroke_width=2, max_tip_length_to_length_ratio=0.2)

        arrows.add(arrow)

    loop_group.add(face_node, net_node, emb_node, loss_node, arrows)
    return loop_group


# =============================================================================
# MAIN SCENE CLASS - Scene 04: Embedding Space
# =============================================================================

class Scene04_EmbeddingSpace(Scene):

    def construct(self):
        self.camera.background_color = DARK

        # =====================================================================
        # PART A — CITY MAP ANALOGY
        # =====================================================================
        self.part_a_title_and_intro()
        self.part_a_city_map_creation()
        self.part_a_scattered_buildings()
        self.part_a_reorganization()
        self.part_a_morph_to_embedding()

        # =====================================================================
        # PART B — EMBEDDING CONCEPT
        # =====================================================================
        self.part_b_embedding_pipeline()
        self.part_b_unstructured_representation()

        # =====================================================================
        # PART C — TRAINING SHAPES THE SPACE
        # =====================================================================
        self.part_c_training_signal()
        self.part_c_training_animation()
        self.part_c_network_learns()

        # =====================================================================
        # PART D — DISTANCE IN EMBEDDING SPACE
        # =====================================================================
        self.part_d_distance_comparison()

        # =====================================================================
        # PART E — TRANSITION TO SOFTMAX / ARCFACE
        # =====================================================================
        self.part_e_transition_to_softmax()

    # =========================================================================
    # PART A: TITLE AND INTRO
    # =========================================================================

    def part_a_title_and_intro(self):
        """Show title card: Embedding Space with subtitle."""
        self.wait(0.3)

        # Title
        title = Tex(r"\textbf{Embedding Space}", font_size=72, color=CYAN)
        title.center()
        title.move_to(UP * 1.0)
        self.add(title)
        self.play(Write(title), run_time=0.6)

        # Subtitle
        subtitle = Tex(r"\text{A geometry for comparing faces}", font_size=28, color=WHITE)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.add(subtitle)
        self.play(Write(subtitle), run_time=0.5)

        # Accent line
        line = Line(LEFT * 3.5, RIGHT * 3.5, stroke_color=CYAN, stroke_width=1.5, stroke_opacity=0.5)
        line.next_to(subtitle, DOWN, buff=0.35)
        self.add(line)
        self.play(Write(line), run_time=0.3)

        self.wait(0.8)

        # Fade out title for city map
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(line), run_time=0.5)
        self.wait(0.3)

    # =========================================================================
    # PART A: CITY MAP CREATION
    # =========================================================================

    def part_a_city_map_creation(self):
        """Create the 2D city map with roads and buildings."""
        # Create road network (thin cyan lines)
        roads = VGroup()

        # Horizontal roads
        for y in np.linspace(-2.5, 2.5, 5):
            road = Line(LEFT * 6.5, RIGHT * 6.5, stroke_color=CYAN, stroke_width=0.8, stroke_opacity=0.4)
            road.move_to(UP * y)
            roads.add(road)

        # Vertical roads
        for x in np.linspace(-6.5, 6.5, 9):
            road = Line(DOWN * 3.5, UP * 3.5, stroke_color=CYAN, stroke_width=0.8, stroke_opacity=0.4)
            road.move_to(RIGHT * x)
            roads.add(road)

        self.add(roads)
        self.play(FadeIn(roads), run_time=0.5)
        self.wait(0.3)

        # Create buildings in 3 styles
        self.buildings = VGroup()
        building_positions = [
            # Modern buildings (left area)
            (-4.5, 1.5), (-4.0, 1.5), (-3.5, 1.5),
            (-4.5, 0.5), (-4.0, 0.5),
            (-4.5, -0.5), (-4.0, -0.5),

            # Classical buildings (center)
            (0.5, 1.5), (1.0, 1.5), (1.5, 1.5),
            (0.5, 0.5), (1.0, 0.5),
            (0.5, -0.5), (1.0, -0.5),

            # Industrial buildings (right area)
            (4.5, 1.5), (5.0, 1.5),
            (4.5, 0.5), (5.0, 0.5),
            (4.5, -0.5), (5.0, -0.5),
        ]

        for i, (x, y) in enumerate(building_positions):
            if i < 7:
                style = "modern"
                color = CYAN
            elif i < 14:
                style = "classical"
                color = WHITE
            else:
                style = "industrial"
                color = MUTED

            building = create_building(
                width=0.35 + (i % 3) * 0.05,
                height=0.5 + (i % 4) * 0.15,
                style=style,
                stroke_color=color
            )
            building.move_to(RIGHT * x + UP * y)
            self.buildings.add(building)

        self.add(self.buildings)
        self.play(LaggedStart(*[FadeIn(b) for b in self.buildings], lag_ratio=0.08), run_time=0.8)
        self.wait(0.3)

        self.roads = roads

    # =========================================================================
    # PART A: SCATTERED BUILDINGS
    # =========================================================================

    def part_a_scattered_buildings(self):
        """Show buildings randomly scattered, then show the chaos message."""
        # Animate buildings to random positions
        random.seed(42)
        scattered_positions = [
            (random.uniform(-5, 5), random.uniform(-2, 2)) for _ in range(len(self.buildings))
        ]

        for building, (x, y) in zip(self.buildings, scattered_positions):
            building.generate_target()
            building.target.move_to(RIGHT * x + UP * y)

        self.play(*[MoveToTarget(b) for b in self.buildings], run_time=1.0)
        self.wait(0.4)

        # Show chaos message
        chaos_msg = Tex(r"\text{Without structure, distance means little.}", font_size=32, color=MUTED)
        chaos_msg.move_to(DOWN * 3.0)
        self.add(chaos_msg)
        self.play(Write(chaos_msg), run_time=0.5)
        self.wait(0.8)

        self.chaos_msg = chaos_msg

    # =========================================================================
    # PART A: REORGANIZATION
    # =========================================================================

    def part_a_reorganization(self):
        """Reorganize buildings into three neighborhoods with cluster circles."""
        # Fade out chaos message
        self.play(FadeOut(self.chaos_msg), run_time=0.3)

        # Define target positions for each neighborhood
        modern_targets = [
            (-3.5, 1.2), (-3.0, 1.2), (-2.5, 1.2),
            (-3.5, 0.2), (-3.0, 0.2),
            (-3.5, -0.8), (-2.5, -0.8),
        ]

        classical_targets = [
            (0.0, 1.2), (0.5, 1.2), (1.0, 1.2),
            (0.0, 0.2), (0.5, 0.2),
            (0.0, -0.8), (1.0, -0.8),
        ]

        industrial_targets = [
            (3.5, 1.2), (4.0, 1.2),
            (3.5, 0.2), (4.0, 0.2),
            (3.5, -0.8), (4.0, -0.8),
        ]

        all_targets = modern_targets + classical_targets + industrial_targets

        # Animate buildings to their neighborhood positions
        for building, (x, y) in zip(self.buildings, all_targets):
            building.generate_target()
            building.target.move_to(RIGHT * x + UP * y)

        self.play(*[MoveToTarget(b) for b in self.buildings], run_time=1.2)
        self.wait(0.3)

        # Create and show cluster circles
        modern_center = np.mean([np.array([x, y, 0]) for x, y in modern_targets], axis=0)
        classical_center = np.mean([np.array([x, y, 0]) for x, y in classical_targets], axis=0)
        industrial_center = np.mean([np.array([x, y, 0]) for x, y in industrial_targets], axis=0)

        modern_cluster = create_cluster_circle(modern_center, radius=1.3, color=CYAN)
        classical_cluster = create_cluster_circle(classical_center, radius=1.3, color=WHITE)
        industrial_cluster = create_cluster_circle(industrial_center, radius=1.3, color=MUTED)

        self.add(modern_cluster, classical_cluster, industrial_cluster)
        self.play(
            FadeIn(modern_cluster),
            FadeIn(classical_cluster),
            FadeIn(industrial_cluster),
            run_time=0.5
        )

        # Show structure messages
        msg1 = Tex(r"\text{similar structure}", font_size=24, color=CYAN)
        arrow1 = Tex(r"\rightarrow", font_size=24, color=CYAN)
        msg2 = Tex(r"\text{nearby}", font_size=24, color=CYAN)
        group1 = VGroup(msg1, arrow1, msg2).arrange(RIGHT, buff=0.15)
        group1.move_to(UP * 2.5 + LEFT * 3.5)

        msg3 = Tex(r"\text{different structure}", font_size=24, color=MUTED)
        arrow2 = Tex(r"\rightarrow", font_size=24, color=MUTED)
        msg4 = Tex(r"\text{far apart}", font_size=24, color=MUTED)
        group2 = VGroup(msg3, arrow2, msg4).arrange(RIGHT, buff=0.15)
        group2.move_to(UP * 2.5 + RIGHT * 2.5)

        self.play(Write(group1), run_time=0.4)
        self.play(Write(group2), run_time=0.4)
        self.wait(0.5)

        # Meaning message
        meaning = Tex(r"\text{A useful map makes distance meaningful.}", font_size=30, color=WHITE)
        meaning.move_to(DOWN * 3.2)
        self.add(meaning)
        self.play(Write(meaning), run_time=0.5)
        self.wait(0.8)

        # Store elements for morphing
        self.city_elements = VGroup(
            self.roads, self.buildings,
            modern_cluster, classical_cluster, industrial_cluster,
            group1, group2, meaning
        )
        self.modern_cluster = modern_cluster
        self.classical_cluster = classical_cluster
        self.industrial_cluster = industrial_cluster

    # =========================================================================
    # PART A: MORPH TO EMBEDDING SPACE
    # =========================================================================

    def part_a_morph_to_embedding(self):
        """Morph the city map into an embedding space with face icons."""
        # Fade out structure messages
        for elem in [self.modern_cluster, self.classical_cluster, self.industrial_cluster]:
            self.play(FadeOut(elem), run_time=0.3)

        # Keep roads as background grid, fade out some
        for road in self.roads:
            road.generate_target()
            road.target.set_opacity(0.15)

        self.play(*[MoveToTarget(r) for r in self.roads], run_time=0.5)

        # Fade out buildings
        for building in self.buildings:
            building.generate_target()
            building.target.set_opacity(0)

        self.play(*[MoveToTarget(b) for b in self.buildings], run_time=0.6)
        self.wait(0.3)

        # Create face icons (abstract Manim faces)
        face_icons = VGroup()
        face_positions = [
            (-3.0, 0.5), (-2.5, 0.2), (-2.0, 0.5), (-2.5, -0.3),  # Person A cluster
            (0.0, 0.5), (0.5, 0.2), (1.0, 0.5), (0.5, -0.3),     # Person B cluster
            (3.0, 0.5), (3.5, 0.2), (4.0, 0.5), (3.5, -0.3),    # Person C cluster
        ]

        for i, (x, y) in enumerate(face_positions):
            if i < 4:
                color = CYAN
            elif i < 8:
                color = BLUE
            else:
                color = PURPLE

            face = make_abstract_face().scale(0.5)
            face.set_stroke(color=color, width=2)
            face[1].set_color(color)  # Eyes
            face[2].set_stroke(color=color)  # Nose
            face[3].set_stroke(color=color)  # Mouth
            face.move_to(RIGHT * x + UP * y)
            face_icons.add(face)

        self.add(face_icons)
        self.play(LaggedStart(*[FadeIn(f) for f in face_icons], lag_ratio=0.1), run_time=0.6)

        # Create cluster circles for face groups
        a_center = np.mean([np.array([x, y, 0]) for x, y in face_positions[:4]], axis=0)
        b_center = np.mean([np.array([x, y, 0]) for x, y in face_positions[4:8]], axis=0)
        c_center = np.mean([np.array([x, y, 0]) for x, y in face_positions[8:12]], axis=0)

        cluster_a = create_cluster_circle(a_center, radius=1.0, color=CYAN)
        cluster_b = create_cluster_circle(b_center, radius=1.0, color=BLUE)
        cluster_c = create_cluster_circle(c_center, radius=1.0, color=PURPLE)

        self.add(cluster_a, cluster_b, cluster_c)
        self.play(FadeIn(cluster_a), FadeIn(cluster_b), FadeIn(cluster_c), run_time=0.4)

        # Identity labels
        label_a = Tex(r"\text{Person A}", font_size=22, color=CYAN)
        label_a.move_to(a_center + DOWN * 1.3)

        label_b = Tex(r"\text{Person B}", font_size=22, color=BLUE)
        label_b.move_to(b_center + DOWN * 1.3)

        label_c = Tex(r"\text{Person C}", font_size=22, color=PURPLE)
        label_c.move_to(c_center + DOWN * 1.3)

        labels = VGroup(label_a, label_b, label_c)
        self.play(Write(labels), run_time=0.4)

        # Title and projection note
        title = Tex(r"\textbf{Embedding Space}", font_size=48, color=CYAN)
        title.move_to(UP * 3.2)
        self.add(title)
        self.play(Write(title), run_time=0.5)

        note = Tex(r"\text{2D projection of a high-dimensional space}", font_size=18, color=MUTED)
        note.move_to(DOWN * 3.5)
        self.add(note)
        self.play(Write(note), run_time=0.4)

        self.wait(0.8)

        # Store for next part
        self.embedding_scene = VGroup(
            self.roads, face_icons, cluster_a, cluster_b, cluster_c,
            labels, title, note
        )

        # Fade out for Part B
        self.play(FadeOut(self.embedding_scene), run_time=0.6)
        self.wait(0.3)

    # =========================================================================
    # PART B: EMBEDDING PIPELINE
    # =========================================================================

    def part_b_embedding_pipeline(self):
        """Show the face -> network -> embedding pipeline."""
        # Title
        title = Tex(r"\textbf{From Image to Embedding}", font_size=40, color=WHITE)
        title.move_to(UP * 3.2)
        self.add(title)
        self.play(Write(title), run_time=0.5)
        self.wait(0.3)

        # Create pipeline elements
        # Face image (use PNG or abstract face)
        face_img = get_face_image("face_1.png", height=1.5)
        if face_img is None:
            face_img = make_abstract_face().scale(1.5)
            face_img.set_stroke(color=WHITE, width=2.5)
            face_img[1].set_color(CYAN)
        else:
            face_img.scale(2.0)

        face_label = Tex(r"\mathbf{I}", font_size=28)
        face_label.next_to(face_img, DOWN, buff=0.3)

        face_group = VGroup(face_img, face_label)
        face_group.move_to(LEFT * 4.0)

        # Neural network
        network = make_neural_network().scale(1.3)
        network_label = Tex(r"f_\theta", font_size=26)
        network_label.next_to(network, DOWN, buff=0.2)

        network_group = VGroup(network, network_label)
        network_group.move_to(ORIGIN)

        # Embedding vector
        vec_entries = [
            Tex(r"0.12", font_size=20),
            Tex(r"-0.45", font_size=20),
            Tex(r"0.83", font_size=20),
            Tex(r"\vdots", font_size=20),
            Tex(r"0.23", font_size=20),
        ]
        vec = VGroup(*vec_entries)
        vec.arrange(DOWN, buff=0.08)

        left_bracket = Line(UP * 1.0, DOWN * 1.0, stroke_color=WHITE, stroke_width=2)
        right_bracket = Line(UP * 1.0, DOWN * 1.0, stroke_color=WHITE, stroke_width=2)
        left_bracket.next_to(vec, LEFT, buff=0.1)
        right_bracket.next_to(vec, RIGHT, buff=0.1)

        vec_group = VGroup(left_bracket, vec, right_bracket)
        vec_label = Tex(r"\mathbf{x}", font_size=28)
        vec_label.next_to(vec_group, DOWN, buff=0.2)

        emb_group = VGroup(vec_group, vec_label)
        emb_group.move_to(RIGHT * 4.0)

        # Arrows
        arrow1 = Arrow(face_group.get_right(), network_group.get_left(), buff=0.3, color=CYAN, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
        arrow2 = Arrow(network_group.get_right(), emb_group.get_left(), buff=0.3, color=CYAN, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)

        # Main formula
        main_formula = Tex(r"f_\theta(\mathbf{I}) = \mathbf{x}", font_size=32)
        main_formula.move_to(DOWN * 2.8)
        self.add(main_formula)
        self.play(Write(main_formula), run_time=0.4)

        # Dimension label
        dim_label = Tex(r"\mathbf{x} \in \mathbb{R}^d", font_size=24, color=MUTED)
        dim_label.next_to(main_formula, DOWN, buff=0.2)
        self.add(dim_label)
        self.play(Write(dim_label), run_time=0.3)

        # Show pipeline
        self.add(face_group, arrow1, network_group, arrow2, emb_group)
        self.play(
            FadeIn(face_group),
            run_time=0.4
        )
        self.wait(0.2)

        self.play(
            GrowArrow(arrow1),
            FadeIn(network_group),
            run_time=0.4
        )
        self.wait(0.2)

        self.play(
            GrowArrow(arrow2),
            FadeIn(emb_group),
            run_time=0.4
        )
        self.wait(0.6)

        # 2D projection note
        note = Tex(r"\text{For visualization, we project embeddings into 2D.}", font_size=20, color=MUTED)
        note.move_to(DOWN * 3.8)
        self.add(note)
        self.play(Write(note), run_time=0.4)
        self.wait(0.5)

        # Store elements
        self.pipeline_elements = VGroup(
            title, face_group, arrow1, network_group, arrow2,
            emb_group, main_formula, dim_label, note
        )

    # =========================================================================
    # PART B: UNSTRUCTURED REPRESENTATION
    # =========================================================================

    def part_b_unstructured_representation(self):
        """Show multiple faces processing into unstructured points."""
        # Fade out main pipeline
        self.play(FadeOut(self.pipeline_elements), run_time=0.5)
        self.wait(0.3)

        # Create embedding plane background
        plane_lines = VGroup()
        for i in range(-5, 6):
            h_line = Line(LEFT * 5, RIGHT * 5, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            h_line.move_to(UP * i * 0.6)
            v_line = Line(DOWN * 3, UP * 3, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            v_line.move_to(RIGHT * i * 0.6)
            plane_lines.add(h_line, v_line)
        self.add(plane_lines)

        # Title
        title = Tex(r"\text{At the beginning,}", font_size=34, color=WHITE)
        title.move_to(UP * 3.0)
        self.add(title)

        title2 = Tex(r"\text{the representation is unstructured.}", font_size=34, color=MUTED)
        title2.next_to(title, DOWN, buff=0.2)
        self.add(title2)
        self.play(Write(title), run_time=0.4)
        self.play(Write(title2), run_time=0.4)
        self.wait(0.5)

        # Process multiple faces
        face_files = ["face_1.png", "face_5.png", "face_9.png", "face_2.png", "face_6.png", "face_10.png"]
        colors = [CYAN, CYAN, CYAN, BLUE, BLUE, BLUE]
        identities = [0, 0, 0, 1, 1, 1]  # A, A, A, B, B, B

        # Random-looking positions (but grouped by identity)
        unstructured_positions = [
            (-2.5, 1.2), (-1.5, -0.8), (-0.5, 1.5),  # A (scattered)
            (1.5, 0.5), (2.0, -1.0), (2.8, 0.8),  # B (scattered)
        ]

        points = VGroup()
        point_labels = VGroup()

        for i, (x, y) in enumerate(unstructured_positions):
            color = colors[i]
            pos = RIGHT * x + UP * y

            point = create_embedding_point(pos, color=color)
            points.add(point)

            label = Tex(f"P{identities[i]+1}", font_size=16, color=color)
            label.next_to(point, DOWN, buff=0.15)
            point_labels.add(label)

        # Animate faces appearing and becoming points
        face_images = []
        for i, filename in enumerate(face_files[:3]):
            face = get_face_image(filename, height=0.8)
            if face:
                face.scale(2.0)
                face.move_to(unstructured_positions[i])
                face.set_opacity(0)
                face_images.append(face)
                self.add(face)
                self.play(FadeIn(face), run_time=0.2)
                self.wait(0.1)

        self.wait(0.3)

        # Transform to points
        for i, (point, label) in enumerate(zip(points[:3], point_labels[:3])):
            self.play(FadeIn(point), FadeIn(label), run_time=0.2)
            if i < len(face_images):
                self.play(face_images[i].animate.set_opacity(0), run_time=0.2)

        self.wait(0.3)

        # Add remaining points
        for i, (point, label) in enumerate(zip(points[3:], point_labels[3:])):
            self.play(FadeIn(point), FadeIn(label), run_time=0.2)

        self.wait(0.6)

        # Store for next part
        self.unstructured_scene = VGroup(plane_lines, title, title2, points, point_labels)

        # Fade out
        self.play(FadeOut(self.unstructured_scene), run_time=0.6)
        self.wait(0.3)

    # =========================================================================
    # PART C: TRAINING SIGNAL
    # =========================================================================

    def part_c_training_signal(self):
        """Show identity labels provide the training signal."""
        # Create plane
        plane_lines = VGroup()
        for i in range(-5, 6):
            h_line = Line(LEFT * 5, RIGHT * 5, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            h_line.move_to(UP * i * 0.6)
            v_line = Line(DOWN * 3, UP * 3, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            v_line.move_to(RIGHT * i * 0.6)
            plane_lines.add(h_line, v_line)
        self.add(plane_lines)

        # Title
        title = Tex(r"\textbf{Training Shapes the Space}", font_size=42, color=CYAN)
        title.move_to(UP * 3.2)
        self.add(title)
        self.play(Write(title), run_time=0.5)
        self.wait(0.3)

        # Create points with identity labels
        a_positions = [(-3.0, 0.8), (-2.5, 0.2), (-2.0, -0.4)]
        b_positions = [(0.5, 1.0), (1.0, 0.3), (1.5, -0.5)]
        c_positions = [(3.0, 0.6), (3.5, -0.2), (4.0, 0.3)]

        points = VGroup()
        labels = VGroup()

        for x, y in a_positions:
            point = create_embedding_point(RIGHT * x + UP * y, color=CYAN)
            points.add(point)
            label = Tex(r"\text{A}", font_size=18, color=CYAN)
            label.next_to(point, DOWN, buff=0.15)
            labels.add(label)

        for x, y in b_positions:
            point = create_embedding_point(RIGHT * x + UP * y, color=BLUE)
            points.add(point)
            label = Tex(r"\text{B}", font_size=18, color=BLUE)
            label.next_to(point, DOWN, buff=0.15)
            labels.add(label)

        for x, y in c_positions:
            point = create_embedding_point(RIGHT * x + UP * y, color=PURPLE)
            points.add(point)
            label = Tex(r"\text{C}", font_size=18, color=PURPLE)
            label.next_to(point, DOWN, buff=0.15)
            labels.add(label)

        # Show points
        self.add(points, labels)
        for point, label in zip(points, labels):
            self.play(FadeIn(point), FadeIn(label), run_time=0.15)

        # Message about training signal
        signal_msg = Tex(r"\text{Identity labels provide the training signal.}", font_size=28)
        signal_msg.move_to(DOWN * 2.8)
        self.add(signal_msg)
        self.play(Write(signal_msg), run_time=0.5)
        self.wait(0.6)

        self.training_scene_start = VGroup(plane_lines, title, points, labels, signal_msg)

    # =========================================================================
    # PART C: TRAINING ANIMATION
    # =========================================================================

    def part_c_training_animation(self):
        """Animate same-identity points moving closer, different identities moving apart."""
        # Create cluster circles
        a_center = np.mean([np.array(p) for p in [(-3.0, 0.8), (-2.5, 0.2), (-2.0, -0.4)]], axis=0)
        b_center = np.mean([np.array(p) for p in [(0.5, 1.0), (1.0, 0.3), (1.5, -0.5)]], axis=0)
        c_center = np.mean([np.array(p) for p in [(3.0, 0.6), (3.5, -0.2), (4.0, 0.3)]], axis=0)

        # Target positions (tighter clusters)
        a_targets = [(-2.5, 0.3), (-2.5, 0.0), (-2.5, -0.3)]
        b_targets = [(1.0, 0.3), (1.0, 0.0), (1.0, -0.3)]
        c_targets = [(3.5, 0.3), (3.5, 0.0), (3.5, -0.3)]

        all_targets = a_targets + b_targets + c_targets

        # Get points and labels from previous scene
        points = self.training_scene_start[2]
        labels = self.training_scene_start[3]

        # Animate points to target positions
        for i, point in enumerate(points):
            target = all_targets[i]
            point.generate_target()
            # Move both glow and dot
            for subpoint in point:
                subpoint.generate_target()
                subpoint.target.move_to(RIGHT * target[0] + UP * target[1])
            point.target.move_to(RIGHT * target[0] + UP * target[1])

        # Update labels
        label_targets = []
        for target in all_targets:
            label = Tex(r"\text{A}", font_size=18, color=CYAN)
            label.move_to(RIGHT * target[0] + UP * target[1] + DOWN * 0.25)
            label_targets.append(label)

        # Cross-cluster distances should increase - animate them apart
        # A cluster moves left, B cluster stays, C cluster moves right

        # New positions (clusters tighter and more separated)
        a_new = [(-3.0, 0.2), (-3.0, 0.0), (-3.0, -0.2)]
        b_new = [(0.5, 0.1), (0.5, -0.1), (0.5, -0.3)]
        c_new = [(4.0, 0.2), (4.0, 0.0), (4.0, -0.2)]

        final_targets = a_new + b_new + c_new

        for i, point in enumerate(points):
            target = final_targets[i]
            for subpoint in point:
                subpoint.generate_target()
                subpoint.target.move_to(RIGHT * target[0] + UP * target[1])
            point.generate_target()
            point.target.move_to(RIGHT * target[0] + UP * target[1])

        self.play(*[MoveToTarget(p) for p in points], run_time=1.2)
        self.wait(0.3)

        # Update labels to final positions
        final_labels = VGroup()
        colors = [CYAN, CYAN, CYAN, BLUE, BLUE, BLUE, PURPLE, PURPLE, PURPLE]
        for i, target in enumerate(final_targets):
            label = Tex(f"P{colors[i].name if hasattr(colors[i], 'name') else 'WHITE'}", font_size=18, color=colors[i])
            if i < 3:
                label_text = r"\text{A}"
            elif i < 6:
                label_text = r"\text{B}"
            else:
                label_text = r"\text{C}"
            label = Tex(label_text, font_size=18, color=colors[i])
            label.move_to(RIGHT * target[0] + UP * target[1] + DOWN * 0.25)
            final_labels.add(label)

        # Fade old labels and show new ones
        self.play(FadeOut(labels), run_time=0.2)
        self.add(final_labels)
        self.play(FadeIn(final_labels), run_time=0.3)

        # Create cluster circles
        a_center_final = np.mean([np.array(p) for p in a_new], axis=0)
        b_center_final = np.mean([np.array(p) for p in b_new], axis=0)
        c_center_final = np.mean([np.array(p) for p in c_new], axis=0)

        cluster_a = create_cluster_circle(a_center_final, radius=0.8, color=CYAN)
        cluster_b = create_cluster_circle(b_center_final, radius=0.8, color=BLUE)
        cluster_c = create_cluster_circle(c_center_final, radius=0.8, color=PURPLE)

        self.add(cluster_a, cluster_b, cluster_c)
        self.play(FadeIn(cluster_a), FadeIn(cluster_b), FadeIn(cluster_c), run_time=0.4)

        # Messages about clustering
        msg1 = Tex(r"\text{same identity}", font_size=24, color=CYAN)
        arrow1 = Tex(r"\rightarrow", font_size=24, color=CYAN)
        msg2 = Tex(r"\text{close}", font_size=24, color=CYAN)
        group1 = VGroup(msg1, arrow1, msg2).arrange(RIGHT, buff=0.15)
        group1.move_to(DOWN * 2.5 + LEFT * 3.0)

        msg3 = Tex(r"\text{different identities}", font_size=24, color=PURPLE)
        arrow2 = Tex(r"\rightarrow", font_size=24, color=PURPLE)
        msg4 = Tex(r"\text{far apart}", font_size=24, color=PURPLE)
        group2 = VGroup(msg3, arrow2, msg4).arrange(RIGHT, buff=0.15)
        group2.move_to(DOWN * 2.5 + RIGHT * 2.5)

        self.play(Write(group1), run_time=0.4)
        self.play(Write(group2), run_time=0.4)
        self.wait(0.6)

        self.clustering_scene = VGroup(cluster_a, cluster_b, cluster_c, group1, group2)

    # =========================================================================
    # PART C: NETWORK LEARNS
    # =========================================================================

    def part_c_network_learns(self):
        """Show that the network learns the mapping, not just the points."""
        # Fade out clustering scene
        self.play(FadeOut(self.clustering_scene), run_time=0.4)

        # Message
        msg = Tex(r"\text{The network learns the mapping, not just the points.}", font_size=30)
        msg.move_to(UP * 2.5)
        self.add(msg)
        self.play(Write(msg), run_time=0.5)
        self.wait(0.4)

        # Show formula with theta highlighted
        formula = Tex(r"f_\theta(\mathbf{I}) = \mathbf{x}", font_size=36)
        formula.move_to(UP * 1.5)
        self.add(formula)
        self.play(Write(formula), run_time=0.4)

        # Highlight theta
        theta_box = SurroundingRectangle(formula[0][1:4], buff=0.1, stroke_color=CYAN, stroke_width=2, fill_opacity=0.2, fill_color=PANEL)
        self.add(theta_box)
        self.play(FadeIn(theta_box), run_time=0.3)
        self.wait(0.3)

        # Message about theta
        update_msg = Tex(r"\text{Training updates } \theta \text{ so that distances become meaningful.}", font_size=26, color=CYAN)
        update_msg.move_to(DOWN * 1.0)
        self.add(update_msg)
        self.play(Write(update_msg), run_time=0.5)
        self.wait(0.5)

        # Training loop visualization
        loop = create_training_loop(ORIGIN + DOWN * 2.8, scale=1.2)
        self.add(loop)
        self.play(FadeIn(loop), run_time=0.5)

        # Loss to update message
        loss_msg = Tex(r"\mathcal{L} \rightarrow \text{update } \theta", font_size=24)
        loss_msg.move_to(DOWN * 4.2)
        self.add(loss_msg)
        self.play(Write(loss_msg), run_time=0.4)

        self.wait(0.8)

        # Store and fade
        self.learning_scene = VGroup(msg, formula, theta_box, update_msg, loop, loss_msg)

        self.play(FadeOut(self.learning_scene), run_time=0.6)
        self.wait(0.3)

    # =========================================================================
    # PART D: DISTANCE COMPARISON
    # =========================================================================

    def part_d_distance_comparison(self):
        """Show distance comparison between same and different identities."""
        # Create plane
        plane_lines = VGroup()
        for i in range(-6, 7):
            h_line = Line(LEFT * 6, RIGHT * 6, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            h_line.move_to(UP * i * 0.5)
            v_line = Line(DOWN * 3.5, UP * 3.5, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            v_line.move_to(RIGHT * i * 0.5)
            plane_lines.add(h_line, v_line)
        self.add(plane_lines)

        # Title
        title = Tex(r"\textbf{Distance in Embedding Space}", font_size=38, color=WHITE)
        title.move_to(UP * 3.0)
        self.add(title)
        self.play(Write(title), run_time=0.5)
        self.wait(0.3)

        # Same identity distance (left side)
        same_a = create_embedding_point(LEFT * 2.5 + UP * 0.3, color=CYAN, radius=0.15)
        same_b = create_embedding_point(LEFT * 2.0 + DOWN * 0.3, color=CYAN, radius=0.15)

        same_label_a = Tex(r"\text{A}", font_size=18, color=CYAN)
        same_label_a.next_to(same_a, UP, buff=0.1)
        same_label_b = Tex(r"\text{A}", font_size=18, color=CYAN)
        same_label_b.next_to(same_b, DOWN, buff=0.1)

        same_line = DashedLine(LEFT * 2.5 + UP * 0.3, LEFT * 2.0 + DOWN * 0.3, stroke_color=CYAN, stroke_width=2)
        same_dist_label = Tex(r"\text{small distance}", font_size=22, color=CYAN)
        same_dist_label.move_to(LEFT * 2.25 + DOWN * 1.5)

        self.add(same_a, same_b, same_label_a, same_label_b, same_line, same_dist_label)
        self.play(FadeIn(same_a), FadeIn(same_b), run_time=0.3)
        self.play(Write(same_label_a), Write(same_label_b), run_time=0.2)
        self.play(Write(same_line), run_time=0.3)
        self.play(Write(same_dist_label), run_time=0.3)

        # Different identity distance (right side)
        diff_a = create_embedding_point(RIGHT * 2.5 + UP * 0.5, color=CYAN, radius=0.15)
        diff_c = create_embedding_point(RIGHT * 4.0 + DOWN * 0.5, color=PURPLE, radius=0.15)

        diff_label_a = Tex(r"\text{A}", font_size=18, color=CYAN)
        diff_label_a.next_to(diff_a, UP, buff=0.1)
        diff_label_c = Tex(r"\text{C}", font_size=18, color=PURPLE)
        diff_label_c.next_to(diff_c, DOWN, buff=0.1)

        diff_line = DashedLine(RIGHT * 2.5 + UP * 0.5, RIGHT * 4.0 + DOWN * 0.5, stroke_color=PURPLE, stroke_width=2)
        diff_dist_label = Tex(r"\text{large distance}", font_size=22, color=PURPLE)
        diff_dist_label.move_to(RIGHT * 3.25 + DOWN * 1.5)

        self.add(diff_a, diff_c, diff_label_a, diff_label_c, diff_line, diff_dist_label)
        self.play(FadeIn(diff_a), FadeIn(diff_c), run_time=0.3)
        self.play(Write(diff_label_a), Write(diff_label_c), run_time=0.2)
        self.play(Write(diff_line), run_time=0.3)
        self.play(Write(diff_dist_label), run_time=0.3)

        self.wait(0.5)

        # Key message
        key_msg = Tex(r"\text{Face recognition becomes a geometric problem.}", font_size=30, color=WHITE)
        key_msg.move_to(DOWN * 2.8)
        self.add(key_msg)
        self.play(Write(key_msg), run_time=0.5)
        self.wait(0.8)

        # Hypersphere hint (subtle circular outline)
        sphere = Circle(radius=3.5, stroke_color=CYAN, stroke_width=1, stroke_opacity=0.2, fill_opacity=0)
        sphere.move_to(ORIGIN)
        self.add(sphere)
        self.play(FadeIn(sphere), run_time=0.4)

        # Transition question
        question = Tex(r"\text{But which geometry should the loss enforce?}", font_size=26, color=MUTED)
        question.move_to(DOWN * 3.5)
        self.add(question)
        self.play(Write(question), run_time=0.5)
        self.wait(0.8)

        # Store and fade
        self.distance_scene = VGroup(
            plane_lines, title,
            same_a, same_b, same_label_a, same_label_b, same_line, same_dist_label,
            diff_a, diff_c, diff_label_a, diff_label_c, diff_line, diff_dist_label,
            key_msg, sphere, question
        )

        self.play(FadeOut(self.distance_scene), run_time=0.6)
        self.wait(0.3)

    # =========================================================================
    # PART E: TRANSITION TO SOFTMAX / ARCFACE
    # =========================================================================

    def part_e_transition_to_softmax(self):
        """Transition to Softmax and prepare for ArcFace."""
        # Create clean embedding space
        plane_lines = VGroup()
        for i in range(-6, 7):
            h_line = Line(LEFT * 6, RIGHT * 6, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            h_line.move_to(UP * i * 0.5)
            v_line = Line(DOWN * 3.5, UP * 3.5, stroke_color=WHITE, stroke_width=0.5, stroke_opacity=0.1)
            v_line.move_to(RIGHT * i * 0.5)
            plane_lines.add(h_line, v_line)
        self.add(plane_lines)

        # Create three clusters
        a_center = np.array([-3.0, 0.0, 0.0])
        b_center = np.array([0.0, 0.0, 0.0])
        c_center = np.array([3.0, 0.0, 0.0])

        # Points for each cluster
        a_points = [create_embedding_point(a_center + np.array([x, y, 0]), color=CYAN) for x, y in [(-0.2, 0.3), (0.1, -0.2), (-0.1, 0.1)]]
        b_points = [create_embedding_point(b_center + np.array([x, y, 0]), color=BLUE) for x, y in [(-0.2, 0.2), (0.2, -0.1), (0.0, 0.2)]]
        c_points = [create_embedding_point(c_center + np.array([x, y, 0]), color=PURPLE) for x, y in [(-0.1, 0.3), (0.2, -0.2), (0.1, 0.0)]]

        all_points = VGroup(*a_points, *b_points, *c_points)

        # Cluster circles
        cluster_a = create_cluster_circle(a_center, radius=0.7, color=CYAN)
        cluster_b = create_cluster_circle(b_center, radius=0.7, color=BLUE)
        cluster_c = create_cluster_circle(c_center, radius=0.7, color=PURPLE)

        # Identity labels
        label_a = Tex(r"\text{Person A}", font_size=20, color=CYAN)
        label_a.move_to(a_center + DOWN * 1.0)
        label_b = Tex(r"\text{Person B}", font_size=20, color=BLUE)
        label_b.move_to(b_center + DOWN * 1.0)
        label_c = Tex(r"\text{Person C}", font_size=20, color=PURPLE)
        label_c.move_to(c_center + DOWN * 1.0)

        # Fade in elements
        self.add(cluster_a, cluster_b, cluster_c, all_points, label_a, label_b, label_c)
        self.play(
            FadeIn(cluster_a), FadeIn(cluster_b), FadeIn(cluster_c),
            run_time=0.3
        )
        self.play(
            *[FadeIn(p) for p in all_points],
            run_time=0.2
        )
        self.play(
            Write(label_a), Write(label_b), Write(label_c),
            run_time=0.3
        )

        # Objective statement
        obj_msg = Tex(r"\text{To shape this space, the network needs a training objective.}", font_size=26)
        obj_msg.move_to(UP * 3.0)
        self.add(obj_msg)
        self.play(Write(obj_msg), run_time=0.5)
        self.wait(0.6)

        # Fade out clusters slightly
        all_points.generate_target()
        for point in all_points:
            point.target.set_opacity(0.3)

        self.play(*[MoveToTarget(p) for p in all_points], run_time=0.4)

        # Softmax section
        softmax_title = Tex(r"\textbf{Softmax}", font_size=44, color=WHITE)
        softmax_title.move_to(ORIGIN)
        self.add(softmax_title)
        self.play(Write(softmax_title), run_time=0.5)

        softmax_desc = Tex(r"\text{A first attempt: classify each embedding.}", font_size=24, color=MUTED)
        softmax_desc.next_to(softmax_title, DOWN, buff=0.3)
        self.add(softmax_desc)
        self.play(Write(softmax_desc), run_time=0.4)

        self.wait(0.6)

        # Key distinction
        classify_msg = Tex(r"\text{Softmax classifies.}", font_size=28, color=CYAN)
        classify_msg.move_to(LEFT * 2.5 + DOWN * 2.0)
        self.add(classify_msg)
        self.play(Write(classify_msg), run_time=0.4)

        # Arrow
        arrow = Arrow(classify_msg.get_right() + RIGHT * 0.3, LEFT * 1.0 + DOWN * 2.0, buff=0.1, color=CYAN, stroke_width=2)
        self.add(arrow)
        self.play(GrowArrow(arrow), run_time=0.3)

        # ArcFace transformation
        arcface_msg = Tex(r"\text{ArcFace reshapes the geometry.}", font_size=28, color=PURPLE)
        arcface_msg.move_to(RIGHT * 2.0 + DOWN * 2.0)
        self.add(arcface_msg)
        self.play(Write(arcface_msg), run_time=0.4)

        self.wait(0.6)

        # Fade out for final title
        self.play(
            FadeOut(plane_lines),
            FadeOut(cluster_a), FadeOut(cluster_b), FadeOut(cluster_c),
            FadeOut(label_a), FadeOut(label_b), FadeOut(label_c),
            FadeOut(obj_msg),
            FadeOut(softmax_title), FadeOut(softmax_desc),
            FadeOut(classify_msg), FadeOut(arrow), FadeOut(arcface_msg),
            run_time=0.5
        )
        self.wait(0.3)

        # Final title card
        final_title = Tex(r"\textbf{Next: Softmax and Angular Margins}", font_size=48, color=CYAN)
        final_title.center()
        self.add(final_title)
        self.play(Write(final_title), run_time=0.6)

        self.wait(1.0)

        # Fade out
        self.play(FadeOut(final_title), run_time=0.5)
        self.wait(0.3)

        # End screen
        self.wait(0.5)

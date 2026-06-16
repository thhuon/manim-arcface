from manimlib import *
import os
from scenes.utils import *


# =============================================================================
# SCENE-SPECIFIC HELPERS - For scene03_Challenges
# =============================================================================

ACCENT = "#4A7DFF"

def get_face_image(filename: str, height: float = 1.0):
    """Load face image with consistent styling."""
    path = asset_path(filename)
    if not os.path.exists(path):
        return None
    img = ImageMobject(path)
    img.set_height(height)
    return img


def create_pixel_grid(width=2.0, height=2.0, n=6):
    """Create a grid overlay to represent pixelation concept."""
    grid = VGroup()
    step_x = width / n
    step_y = height / n

    for i in range(n + 1):
        x = -width / 2 + i * step_x
        grid.add(Line(
            [x, -height/2, 0],
            [x, height/2, 0],
            stroke_color=WHITE,
            stroke_width=0.5,
            stroke_opacity=0.3
        ))

    for j in range(n + 1):
        y = -height / 2 + j * step_y
        grid.add(Line(
            [-width/2, y, 0],
            [width/2, y, 0],
            stroke_color=WHITE,
            stroke_width=0.5,
            stroke_opacity=0.3
        ))

    return grid


def create_block_pixels(width=1.6, height=1.6, n=5):
    """Create blocky pixel representation for animation."""
    pixels = VGroup()
    step_x = width / n
    step_y = height / n

    for i in range(n):
        for j in range(n):
            rect = Rectangle(
                width=step_x * 0.88,
                height=step_y * 0.88,
                stroke_color=WHITE,
                stroke_width=0.25,
                stroke_opacity=0.4,
                fill_color=DARK,
                fill_opacity=0.7
            )
            rect.move_to([
                -width/2 + step_x/2 + i * step_x,
                -height/2 + step_y/2 + j * step_y,
                0
            ])
            pixels.add(rect)

    return pixels


# =============================================================================
# MAIN SCENE CLASS - Scene 03: Challenges
# =============================================================================

class Scene03_Challenges(Scene):

    def construct(self):
        self.camera.background_color = DARK

        # =====================================================================
        # BEAT 0: TITLE / HOOK
        # =====================================================================
        # Part 1: Human recognition - face grid appears rapidly
        self.beat_0_part_1_human_recognition()

        # Part 2: Pixel comparison problem
        self.beat_0_part_2_pixel_comparison()

        # Part 3: The central question
        self.beat_0_part_3_central_question()

        # Part 4: Scene title
        self.beat_0_part_4_scene_title()

        # =====================================================================
        # BEAT 1: VARIABILITY AS A STRESS TEST
        # =====================================================================
        self.beat_1_variability_stress_test()

        # =====================================================================
        # BEAT 2: WHAT IF THERE IS MISLEADING?
        # =====================================================================
        self.beat_2_misleading_system()

        # =====================================================================
        # BEAT 3: TRANSITION TO EMBEDDING SPACE
        # =====================================================================
        self.beat_3_transition_to_embedding()

    # =========================================================================
    # BEAT 0 - PART 1: Human Recognition
    # =========================================================================

    def beat_0_part_1_human_recognition(self):
        """
        Show face grid rapidly: face_1.png to face_12.png
        Then show "They are the same person?" and human ability text.
        """
        self.wait(0.3)

        # Load 48 face images for 8x6 grid
        face_files = [
            "face_1.png", "face_2.png", "face_3.png", "face_4.png",
            "face_5.png", "face_6.png", "face_7.png", "face_8.png",
            "face_9.png", "face_10.png", "face_11.png", "face_12.png",
            "face_13.png", "face_14.png", "face_15.png", "face_16.png",
            "face_17.png", "face_18.png", "face_19.png", "face_20.png",
            "face_21.png", "face_22.png", "face_23.png", "face_24.png",
            "face_25.png", "face_26.png", "face_27.png", "face_28.png",
            "face_29.png", "face_30.png", "face_31.png", "face_32.png",
            "face_33.png", "face_34.png", "face_35.png", "face_36.png",
            "face_37.png", "face_38.png", "face_39.png", "face_40.png",
            "face_41.png", "face_42.png", "face_43.png", "face_44.png",
            "face_45.png", "face_46.png", "face_47.png", "face_48.png"
        ]

        # Fallback if files don't exist
        available_faces = []
        for f in face_files:
            path = asset_path(f)
            if os.path.exists(path):
                available_faces.append(f)

        # Grid layout: 6 rows x 8 columns (48 images)
        # 408x408 pixels each - fit to frame with no gaps
        rows, cols = 6, 8

        # Calculate img size to fill frame (no gaps)
        # FRAME_WIDTH ≈ 14.22, FRAME_HEIGHT ≈ 8.0
        # Height: 8 * img_size ≤ 7.5 (leave room for text at top)
        img_size = 1.5  # each image size in manim units
        spacing = img_size  # no gaps between images

        face_images = []
        for idx in range(min(len(available_faces), rows * cols)):
            row = idx // cols
            col = idx % cols

            img = get_face_image(available_faces[idx], height=img_size)
            if img is None:
                continue

            # Position in grid with no gaps
            x = (col - (cols - 1) / 2) * spacing
            y = ((rows - 1) / 2 - row) * spacing
            img.move_to([x, y, 0])
            face_images.append(img)
            img.move_to([x, y, 0])
            face_images.append(img)

        # Animate: each face appears one by one rapidly
        for img in face_images:
            img.save_state()
            self.add(img)
            self.wait(0.05)

        # Wait for 0.3 seconds after all faces appear
        self.wait(0.3)

        # Store grid for next part
        self.face_grid = Group(*face_images)
        self.face_grid.scale(0.85) 
        self.wait(0.5)
        self.face_grid.move_to(ORIGIN)
        

        # Fade all the faces to low opacity
        other_faces = Group(*[self.face_grid[i] for i in range(0, len(self.face_grid))])
        self.play(other_faces.animate.set_opacity(0.1), run_time=0.3)
        self.wait(0.3)

        # Question text ABOVE grid (grid now fills most of screen) and centered
        question = latex(r"\textbf{They are the same person?}", size=55)
        question.center()
        self.add(question)
        self.play(Write(question), run_time=0.4)

        # Human ability text 
        ability = latex(r"\textbf{Humans are able to recognize this instantly.}", size=26, color=CYAN)
        ability.next_to(question, DOWN, buff=0.4)

        self.add(ability)
        self.play(Write(ability), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(question), FadeOut(ability), run_time=0.3)
        self.wait(0.5)

        # Store references
        self.question_text = question
        self.ability_text = ability

    # =========================================================================
    # BEAT 0 - PART 2: Pixel Comparison Problem
    # =========================================================================

    def beat_0_part_2_pixel_comparison(self):
        # =====================================================================
        # PART 2: RAW PIXELS AND MISLEADING DISTANCE
        # =====================================================================

        # STEP 0: Clear the face grid
        # Fade out the face grid to make room for the new comparison cards
        self.play(FadeOut(self.face_grid), run_time=0.5)
        self.wait(0.3)

        # Part 2 title
        part_2_title = Tex(r"\textbf{A Subtle Problem}", color=CYAN, font_size=30)
        part_2_subtitle = Tex(r"\text{Which faces should be considered close?}", color=WHITE, font_size=40)
        part_2_title.move_to(UP * 3.8)
        part_2_subtitle.next_to(part_2_title, DOWN, buff=0.15)
        self.add(part_2_title, part_2_subtitle)
        self.play(Write(part_2_title), Write(part_2_subtitle), run_time=0.5)
        self.wait(0.5)


        # STEP 1: Create and position face cards A and B (LARGE, CENTER)
        # Get face images A and B - initially at LARGE size (height=2.5)
        face_a = get_face_image("face_A.png", height=2.5)
        face_a.scale(2.0)
        face_b = get_face_image("face_B.png", height=2.5)
        face_b.scale(2.0)

        # Create labels under A and B
        label_a = Tex(r"\text{A: same identity}", font_size=30, color=WHITE)
        label_b = Tex(r"\text{B: same identity, different conditions}", font_size=30, color=WHITE)

        # Create card groups (face + label) to move them together
        card_a = Group(face_a, label_a)
        card_b = Group(face_b, label_b)

        # Position labels below faces
        label_a.next_to(face_a, DOWN, buff=0.5)
        label_b.next_to(face_b, DOWN, buff=0.5)

        # Initially position A and B at CENTER, close to each other
        # A at LEFT*1.5, B at RIGHT*1.5 (they overlap slightly in the middle)
        card_a.move_to(LEFT * 3.0)
        card_b.move_to(RIGHT * 1.5)

        # Add cards to scene and fade in (they appear large at center)
        self.add(card_a, card_b)
        self.play(FadeIn(card_a), FadeIn(card_b), run_time=0.6)

        self.wait(0.4)

        # STEP 2: Shrink and move A, B to the LEFT
        # Effect: "Extract" A and B from center, shrink them, and move left
        # This creates space on the right side for face C to appear
        #
        # Movement:
        #   A: (LEFT*1.5) → (LEFT*3.5 + UP*0.5)  [moves left and up slightly]
        #   B: (RIGHT*1.5) → (ORIGIN + UP*0.5)    [moves to center-left and up]
        #
        # Size: scale down to 70% (0.7) of original
        target_a_pos = LEFT * 3.5 + UP * 0.5
        target_b_pos = ORIGIN + UP * 0.5

        self.play(
            card_a.animate.scale(0.7).move_to(target_a_pos),
            card_b.animate.scale(0.7).move_to(target_b_pos),
            run_time=0.8
        )

        self.wait(0.3)

        # STEP 3: Show face C on the RIGHT
        # C appears at RIGHT side, same size as A and B after shrinking 
        # C represents a DIFFERENT person with SAME conditions as A
        face_c = get_face_image("face_C.png", height=2.5)
        face_c.scale(1.4)  # Same size of A and B after shrinking

        label_c = Tex(
            r"\begin{array}{l}"
            r"\text{C: same conditions,}\\"
            r"\text{different identity}"
            r"\end{array}",
            font_size=27,
            color=WHITE
        )

        card_c = Group(face_c, label_c)
        card_c.move_to(RIGHT * 3.5 + UP * 0.5)  # 
        label_c.next_to(face_c, DOWN, buff=0.5)

        # Fade in C with a simple animation
        self.add(card_c)
        self.play(FadeIn(card_c), run_time=0.5)

        self.wait(0.5)

        # Fade out part 2 title and subtitle
        self.play(FadeOut(part_2_title), FadeOut(part_2_subtitle), run_time=0.3)
        self.wait(0.3)

        # STEP 4: Show pixel vectors below each face
        # Create simplified illustrative pixel vectors to show raw pixel representation
        p_a = Tex(r"\mathbf{p}_A = [23,\ 41,\ 88,\ \cdots]", font_size=24)
        p_b = Tex(r"\mathbf{p}_B = [4,\ 12,\ 35,\ \cdots]", font_size=24)
        p_c = Tex(r"\mathbf{p}_C = [25,\ 39,\ 84,\ \cdots]", font_size=24)

        # Position vectors below each card
        p_a.next_to(card_a, DOWN, buff=0.8)
        p_b.next_to(card_b, DOWN, buff=0.8)
        p_c.next_to(card_c, DOWN, buff=0.8)

        # Show the notation label explaining the vector representation
        notation_label = Tex(r"\mathbf{p}=\operatorname{flatten}(\mathbf{I})", font_size=20, color=MUTED)
        notation_label.move_to(DOWN * 2.2)
        self.add(notation_label)

        dim_label = Tex(r"\mathbf{p}\in\mathbb{R}^{H\times W\times 3}", font_size=18, color=MUTED)
        dim_label.next_to(notation_label, DOWN, buff=0.1)

        # Animate: cards shift up slightly while pixel vectors and labels appear
        self.play(
            card_a.animate.shift(UP * 0.15).set_opacity(0.85),
            card_b.animate.shift(UP * 0.15).set_opacity(0.85),
            card_c.animate.shift(UP * 0.15).set_opacity(0.85),
            Write(p_a), Write(p_b), Write(p_c),
            Write(notation_label),
            Write(dim_label),
            run_time=0.6
        )

        # Add note showing that A and C have similar first pixel values
        closer_note = Tex(r"\text{(first entries of } \mathbf{p}_A \text{ and } \mathbf{p}_C \text{ are similar)}", font_size=16, color=MUTED)
        closer_note.move_to(DOWN * 3.8)
        self.add(closer_note)
        self.play(Write(closer_note), run_time=0.4)
        self.wait(0.6)

        # STEP 5: Create 2D coordinate plane (raw-pixel space)
        # Fade cards and vectors to 30% opacity as background for the plane
        self.play(
            card_a.animate.set_opacity(0.3),
            card_b.animate.set_opacity(0.3),
            card_c.animate.set_opacity(0.3),
            p_a.animate.set_opacity(0.3),
            p_b.animate.set_opacity(0.3),
            p_c.animate.set_opacity(0.3),
            notation_label.animate.set_opacity(0.3),
            dim_label.animate.set_opacity(0.3),
            closer_note.animate.set_opacity(0.3),
            run_time=0.5
        )

        # Create 2D coordinate plane title
        plane_title = Tex(r"\text{2D projection of raw-pixel space}", font_size=28)
        plane_title.move_to(UP * 3.8)
        self.add(plane_title)

        plane_subtitle = Tex(r"\text{conceptual view}", font_size=18, color=MUTED)
        plane_subtitle.next_to(plane_title, DOWN, buff=0.15)
        self.add(plane_subtitle)

        # Draw axes with generic pixel dimension labels
        axis_length = 3.5
        h_line = Line(LEFT * axis_length, RIGHT * axis_length, stroke_color=WHITE, stroke_width=1.5)
        v_line = Line(DOWN * axis_length, UP * axis_length, stroke_color=WHITE, stroke_width=1.5)
        h_line.move_to(ORIGIN)
        v_line.move_to(ORIGIN)

        # Axis labels (pixel dimensions, not identity/pose/lighting)
        axis_label_i = Tex(r"p_i", font_size=20)
        axis_label_i.next_to(h_line, RIGHT, buff=0.2)
        axis_label_j = Tex(r"p_j", font_size=20)
        axis_label_j.next_to(v_line, UP, buff=0.2)

        # Group and display the plane
        plane_group = VGroup(h_line, v_line, axis_label_i, axis_label_j, plane_title, plane_subtitle)
        self.add(plane_group)
        self.play(Write(plane_group), run_time=0.5)

        # STEP 6: Transform face cards into points on the 2D plane
        # Define positions on the 2D plane:
        #   A and B: far apart (same identity, different appearance)
        #   A and C: closer (different identity, similar conditions)
        #
        # Final layout:
        #       C (1.2, 0.2)
        #   A (-2.0, 0.3)
        #           B (-0.3, -1.5)
        point_a_pos = LEFT * 2.0 + UP * 0.3
        point_b_pos = LEFT * 0.3 + DOWN * 1.5
        point_c_pos = RIGHT * 1.2 + UP * 0.2

        # Create colored dots to represent each face
        dot_a = Dot(point_a_pos, color=CYAN, radius=0.12)
        dot_b = Dot(point_b_pos, color=CYAN, radius=0.12)
        dot_c = Dot(point_c_pos, color="#CC8855", radius=0.12)

        # Labels for each point
        point_label_a = Tex(r"A", font_size=22)
        point_label_b = Tex(r"B", font_size=22)
        point_label_c = Tex(r"C", font_size=22)
        point_label_a.next_to(dot_a, UP + LEFT, buff=0.1)
        point_label_b.next_to(dot_b, DOWN + RIGHT, buff=0.1)
        point_label_c.next_to(dot_c, UP + RIGHT, buff=0.1)

        # Shrink cards down to tiny dots and move them to point positions
        # This creates a visual effect of faces "collapsing" into points
        self.play(
            card_a.animate.scale(0.06).move_to(point_a_pos),
            card_b.animate.scale(0.06).move_to(point_b_pos),
            card_c.animate.scale(0.06).move_to(point_c_pos),
            run_time=0.7
        )

        # Fade in the dots at the point positions
        self.play(
            FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_c),
            Write(point_label_a), Write(point_label_b), Write(point_label_c),
            run_time=0.4
        )

        # STEP 7: Draw dashed lines showing distances between points
        # Draw dashed line between A and B (large distance - same identity)
        line_ab = DashedLine(point_a_pos, point_b_pos, stroke_color=WHITE, stroke_width=1.5)

        # Draw dashed line between A and C (small distance - different identity)
        line_ac = DashedLine(point_a_pos, point_c_pos, stroke_color=WHITE, stroke_width=1.5)

        # Animate the lines appearing
        self.play(Write(line_ab), Write(line_ac), run_time=0.4)

        # Add distance labels explaining the distances
        dist_ab_label = Tex(r"\text{same identity, large pixel distance}", font_size=18, color=CYAN)
        dist_ab_label.move_to((point_a_pos + point_b_pos) / 2 + DOWN * 0.4)
        dist_ab_label.shift(RIGHT * 0.5)

        dist_ac_label = Tex(r"\text{different identity, smaller pixel distance}", font_size=18, color="#CC8855")
        dist_ac_label.move_to((point_a_pos + point_c_pos) / 2 + UP * 0.35)

        self.play(Write(dist_ab_label), Write(dist_ac_label), run_time=0.4)
        self.wait(0.5)

        # STEP 8: Display the key conclusion
        # Show the main takeaway: raw pixel distance can be misleading
        conclusion1 = Tex(r"\textbf{Raw-pixel distance can be misleading.}", font_size=32)
        conclusion1.center()
        conclusion1.move_to(DOWN * 3.8)
        self.add(conclusion1)
        self.play(Write(conclusion1), run_time=0.5)
        self.wait(0.8)

        # Transform to a stronger statement
        conclusion1.generate_target()
        conclusion1.target.become(
            Tex(r"\textbf{Raw pixels do not preserve identity distance.}", font_size=32)
        )
        conclusion1.target.move_to(DOWN * 3.8)

        self.play(Transform(conclusion1, conclusion1.target), run_time=0.5)
        self.wait(0.8)

        # STEP 9: Store elements for Part 3
        # Store all part 2 elements for use in Part 3 (identity-aware representation)
        self.points_ab = VGroup(dot_a, dot_b, dot_c, line_ab, line_ac, point_label_a, point_label_b, point_label_c)
        self.dist_labels = VGroup(dist_ab_label, dist_ac_label)
        self.conclusion1 = conclusion1
        self.plane_group = plane_group

        # Store all part 2 elements including card groups
        self.all_part2_elements = [
            card_a, card_b, card_c,
            p_a, p_b, p_c, notation_label, dim_label, closer_note
        ]

        # Store individual references for Part 3 animation
        self.dot_a = dot_a
        self.dot_b = dot_b
        self.dot_c = dot_c
        self.point_label_a = point_label_a
        self.point_label_b = point_label_b
        self.point_label_c = point_label_c

    # =========================================================================
    # BEAT 0 - PART 3: Link to Next Chapter
    # =========================================================================

    def beat_0_part_3_central_question(self):
        """
        Transition from raw-pixel space to identity-aware representation.
        Shows that we need a new space where identity (not appearance) defines distance.
        """
        # STEP 1: Create identity-aware representation space (on the RIGHT)
        # Create second space labeled "Identity-aware representation"
        # This represents what we WANT: a space where identity distance is preserved
        new_space_title = Tex(r"\text{Identity-aware representation}", font_size=26)
        new_space_title.move_to(RIGHT * 4.5 + UP * 3.2)

        # Draw axes for the new space
        new_axis_length = 2.5
        new_h_line = Line(LEFT * new_axis_length, RIGHT * new_axis_length, stroke_color=WHITE, stroke_width=1.5)
        new_v_line = Line(DOWN * new_axis_length, UP * new_axis_length, stroke_color=WHITE, stroke_width=1.5)
        new_h_line.move_to(RIGHT * 4.5)
        new_v_line.move_to(RIGHT * 4.5)

        # Axis labels for feature dimensions
        new_label_1 = Tex(r"f_i", font_size=18)
        new_label_1.next_to(new_h_line, RIGHT, buff=0.15).shift(RIGHT * 4.5)
        new_label_2 = Tex(r"f_j", font_size=18)
        new_label_2.next_to(new_v_line, UP, buff=0.15).shift(RIGHT * 4.5)

        new_space_group = VGroup(new_h_line, new_v_line, new_label_1, new_label_2, new_space_title)

        # -------------------------------------------------------------------------
        # STEP 2: Define new positions for points (DESIRED behavior)
        # -------------------------------------------------------------------------
        # In identity-aware space:
        #   A and B should be CLOSE (same identity, despite different appearance)
        #   C should be FAR from A and B (different identity)
        #
        # Positions:
        #   A: (4.3, 0.3) - upper left of new space
        #   B: (4.5, -0.3) - lower left of new space (close to A)
        #   C: (6.5, 0.2) - far right (different identity)
        new_pos_a = RIGHT * 4.3 + UP * 0.3
        new_pos_b = RIGHT * 4.5 + DOWN * 0.3
        new_pos_c = RIGHT * 6.5 + UP * 0.2

        # Create new dots at desired positions
        new_dot_a = Dot(new_pos_a, color=CYAN, radius=0.12)
        new_dot_b = Dot(new_pos_b, color=CYAN, radius=0.12)
        new_dot_c = Dot(new_pos_c, color="#CC8855", radius=0.12)

        # Labels for new dots
        new_label_a = Tex(r"A", font_size=20)
        new_label_b = Tex(r"B", font_size=20)
        new_label_c = Tex(r"C", font_size=20)
        new_label_a.next_to(new_dot_a, UP + LEFT, buff=0.08)
        new_label_b.next_to(new_dot_b, DOWN + RIGHT, buff=0.08)
        new_label_c.next_to(new_dot_c, UP + RIGHT, buff=0.08)

        # -------------------------------------------------------------------------
        # STEP 3: Animate transition to new space
        # -------------------------------------------------------------------------
        # Show the new space appearing
        self.play(Write(new_space_group), run_time=0.5)
        self.wait(0.3)

        # Move existing points to new positions in identity-aware space
        # Points will animate from raw-pixel positions to identity-aware positions
        self.play(
            self.dot_a.animate.move_to(new_pos_a),
            self.dot_b.animate.move_to(new_pos_b),
            self.dot_c.animate.move_to(new_pos_c),
            self.point_label_a.animate.next_to(new_dot_a, UP + LEFT, buff=0.08),
            self.point_label_b.animate.next_to(new_dot_b, DOWN + RIGHT, buff=0.08),
            self.point_label_c.animate.next_to(new_dot_c, UP + RIGHT, buff=0.08),
            run_time=0.8
        )

        # -------------------------------------------------------------------------
        # STEP 4: Show relationship lines and annotations
        # -------------------------------------------------------------------------
        # Draw solid lines showing relationships in identity-aware space
        new_line_ab = Line(new_pos_a, new_pos_b, stroke_color=CYAN, stroke_width=2.0)  # A-B: close
        new_line_ac = Line(new_pos_a, new_pos_c, stroke_color="#CC8855", stroke_width=2.0)  # A-C: far
        new_line_bc = Line(new_pos_b, new_pos_c, stroke_color="#CC8855", stroke_width=2.0)  # B-C: far

        self.play(Write(new_line_ab), Write(new_line_ac), Write(new_line_bc), run_time=0.4)

        # Draw circle around A and B to show they form a cluster (same identity)
        center_ab = (new_pos_a + new_pos_b) / 2
        compactness_circle = Circle(radius=0.6, stroke_color=CYAN, stroke_width=2.0, fill_opacity=0)
        compactness_circle.move_to(center_ab)
        self.play(FadeIn(compactness_circle), run_time=0.3)

        # Draw arrow showing separation from A/B cluster to C
        separation_arrow = Arrow(
            center_ab + RIGHT * 0.5,
            new_pos_c + LEFT * 0.5,
            buff=0.1,
            stroke_color="#CC8855",
            stroke_width=2.0
        )
        self.play(Write(separation_arrow), run_time=0.3)

        # STEP 5: Show behavior labels
        # Label for same identity → close
        same_label = Tex(r"\text{same identity}", font_size=20, color=CYAN)
        same_arrow = Tex(r"\rightarrow", font_size=20, color=CYAN)
        same_arrow.next_to(same_label, RIGHT, buff=0.1)
        close_word = Tex(r"\text{close}", font_size=20, color=CYAN)
        close_word.next_to(same_arrow, RIGHT, buff=0.1)

        same_identity_group = VGroup(same_label, same_arrow, close_word)
        same_identity_group.move_to(DOWN * 3.5 + LEFT * 2.5)

        # Label for different identities → far apart
        different_label = Tex(r"\text{different identities}", font_size=20, color="#CC8855")
        different_arrow = Tex(r"\rightarrow", font_size=20, color="#CC8855")
        different_arrow.next_to(different_label, RIGHT, buff=0.1)
        far_word = Tex(r"\text{far apart}", font_size=20, color="#CC8855")
        far_word.next_to(different_arrow, RIGHT, buff=0.1)

        different_identity_group = VGroup(different_label, different_arrow, far_word)
        different_identity_group.move_to(DOWN * 3.5 + RIGHT * 2.5)

        self.play(Write(same_identity_group), Write(different_identity_group), run_time=0.4)

        # STEP 6: Display linking statement
        # Show the key message: we need representation where identity defines distance
        linking_statement = Tex(
            r"\textbf{We need a representation where identity,}",
            font_size=30
        )
        linking_statement2 = Tex(
            r"\textbf{not appearance, defines distance.}",
            font_size=30
        )
        linking_statement.center()
        linking_statement2.next_to(linking_statement, DOWN, buff=0.2)
        linking_statement.move_to(UP * 1.8)
        linking_statement2.move_to(UP * 1.3)

        self.play(Write(linking_statement), Write(linking_statement2), run_time=0.5)
        self.wait(1.0)

        # STEP 7: Fade out all elements for scene title
        # Prepare all elements for transition to Part 4 (scene title)
        fade_out_list = list(self.points_ab) + list(self.dist_labels) + [self.conclusion1, self.plane_group]
        fade_out_list.extend(self.all_part2_elements)
        fade_out_list.extend([
            new_space_group,
            new_dot_a, new_dot_b, new_dot_c,
            new_label_a, new_label_b, new_label_c,
            new_line_ab, new_line_ac, new_line_bc,
            compactness_circle, separation_arrow,
            same_identity_group, different_identity_group,
            linking_statement, linking_statement2
        ])

        self.play(*[FadeOut(obj) for obj in fade_out_list], run_time=0.6)
        self.wait(0.3)

        # Clear the grid for Part 4
        self.face_grid.set_opacity(0)

        self.play(*[FadeOut(obj) for obj in fade_out_list], run_time=0.6)
        self.wait(0.3)

        # Store for Part 4
        self.face_grid.set_opacity(0)  # Clear the grid

    # =========================================================================
    # BEAT 0 - PART 4: Scene Title
    # =========================================================================

    def beat_0_part_4_scene_title(self):
        """
        Display the scene title "Challenges" with subtitle and key points,
        then fade out to prepare for the next section.
        """
        # STEP 1: Display main title
        # Large bold title at the top center of the screen
        title = Tex(r"\textbf{Challenges}", font_size=72)
        title.center()
        title.move_to(UP * 1.5)
        self.add(title)
        self.play(Write(title), run_time=0.55)

        # STEP 2: Display subtitle
        # Subtitle explaining the theme of this scene
        subtitle = Tex(r"\text{Why Face Recognition Is Harder Than It Looks}", font_size=26, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.45)
        self.add(subtitle)
        self.play(Write(subtitle), run_time=0.4)

        # STEP 3: Draw accent line under subtitle
        # Cyan accent line to visually separate title from content
        line = Line(
            LEFT * 3.2,
            RIGHT * 3.2,
            stroke_color=CYAN,
            stroke_width=1.2,
            stroke_opacity=0.45
        )
        line.next_to(subtitle, DOWN, buff=0.35)
        self.add(line)
        self.play(Write(line), run_time=0.3)

        # STEP 4: Display key points (compact lines)
        # Three concise statements about the challenges
        compact1 = Tex(r"\text{Appearance changes.}", font_size=24)
        compact1.next_to(line, DOWN, buff=0.5)

        compact2 = Tex(r"\text{Mistakes have consequences.}", font_size=24)
        compact2.next_to(compact1, DOWN, buff=0.3)

        compact3 = Tex(r"\text{A better representation is needed.}", font_size=24)
        compact3.next_to(compact2, DOWN, buff=0.3)

        # Animate each line appearing
        self.play(Write(compact1), run_time=0.3)
        self.play(Write(compact2), run_time=0.3)
        self.play(Write(compact3), run_time=0.3)

        self.wait(1.2)

        # STEP 5: Fade out all title elements
        # Clear the screen for the next scene content
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(line),
            FadeOut(compact1),
            FadeOut(compact2),
            FadeOut(compact3),
            run_time=0.45
        )
        self.wait(0.3)

    # =========================================================================
    # BEAT 1: VARIABILITY AS A STRESS TEST
    # =========================================================================

    def beat_1_variability_stress_test(self):
        """
        Beat 1: Show how appearance changes challenge face recognition.
        - Reference face with variation cards (lighting, pose, expression, etc.)
        - Transformation arrows from reference to each variation
        - All map to same identity
        - Key message about invariance
        """
        # STEP 1: Fade in title
        title = Tex(r"\textbf{Variability}", font_size=56, color=CYAN)
        title.move_to(UP * 3.2)
        self.add(title)
        self.play(Write(title), run_time=0.5)
        self.wait(0.4)

        # STEP 2: Show reference face (center-left)
        ref_face = get_face_image("face_normal.png", height=1.8)
        if ref_face is None:
            ref_face = get_face_image("face_1.png", height=1.8)
        
        ref_frame = RoundedRectangle(
            width=2.2,
            height=2.2,
            corner_radius=0.15,
            stroke_color=CYAN,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.15
        )
        ref_frame.move_to(ref_face)
        
        ref_label = Tex(r"\text{Reference Image}", font_size=20, color=MUTED)
        ref_label.next_to(ref_frame, DOWN, buff=0.2)
        
        ref_group = VGroup(ref_face, ref_frame, ref_label)
        ref_group.move_to(LEFT * 2.5 + UP * 0.3)
        self.add(ref_group)
        self.play(FadeIn(ref_group), run_time=0.5)
        self.wait(0.4)

        # STEP 3: Load available face images for variations
        variation_files = [
            "face_1.png", "face_2.png", "face_3.png", "face_4.png",
            "face_5.png", "face_6.png", "face_7.png", "face_8.png",
            "face_9.png", "face_10.png", "face_11.png", "face_12.png"
        ]
        
        available_variations = []
        for f in variation_files:
            path = asset_path(f)
            if os.path.exists(path):
                img = ImageMobject(path)
                img.set_height(0.85)
                available_variations.append((f, img))
        
        # Define variation types with labels
        variation_labels = [
            (r"\text{Lighting}", "light"),
            (r"\text{Pose}", "pose"),
            (r"\text{Expression}", "expression"),
            (r"\text{Occlusion}", "occlusion"),
            (r"\text{Blur}", "blur"),
            (r"\text{Shadow}", "shadow"),
            (r"\text{Age}", "age"),
            (r"\text{Camera}", "camera")
        ]

        # STEP 4: Arrange variations in arc layout on the right
        num_variations = min(len(available_variations), len(variation_labels))
        arc_radius = 2.8
        center_angle = -30 * DEGREES
        angle_spread = 100 * DEGREES
        
        variation_cards = []
        variation_groups = []
        
        for i in range(num_variations):
            if i >= len(available_variations):
                break
                
            filename, img = available_variations[i]
            label_text, vtype = variation_labels[i]
            
            # Calculate position in arc
            angle = center_angle + (i / max(num_variations - 1, 1)) * angle_spread - angle_spread / 2
            x = RIGHT * 2.5 + RIGHT * arc_radius * np.cos(angle)
            y = UP * 0.3 + UP * arc_radius * 0.45 * np.sin(angle)
            pos = np.array([x, y, 0])
            
            # Create card frame
            card = RoundedRectangle(
                width=1.1,
                height=1.1,
                corner_radius=0.1,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=PANEL,
                fill_opacity=0.08
            )
            card.move_to(pos)
            img.move_to(pos)
            
            # Label below card
            label = Tex(label_text, font_size=16, color=MUTED)
            label.next_to(card, DOWN, buff=0.12)
            
            group = VGroup(card, img, label)
            group.save_state()
            variation_cards.append(card)
            variation_groups.append(group)
            self.add(group)

        # Fade in variations one by one
        for group in variation_groups:
            self.play(FadeIn(group), run_time=0.15)
        self.wait(0.3)

        # STEP 5: Draw transformation arrows from reference to each variation
        transformation_labels = [
            (r"T_{\text{light}}", "light"),
            (r"T_{\text{pose}}", "pose"),
            (r"T_{\text{expression}}", "expression"),
            (r"T_{\text{occlusion}}", "occlusion"),
            (r"T_{\text{blur}}", "blur"),
            (r"T_{\text{shadow}}", "shadow"),
            (r"T_{\text{age}}", "age"),
            (r"T_{\text{camera}}", "camera")
        ]

        arrows = []
        for i, (tlabel_text, _) in enumerate(transformation_labels[:len(variation_groups)]):
            if i >= len(variation_groups):
                break
                
            start_pos = ref_group.get_center() + RIGHT * 1.2
            end_pos = variation_groups[i].get_center() + LEFT * 0.6
            
            arrow = Arrow(
                start_pos,
                end_pos,
                buff=0.1,
                stroke_color=CYAN,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.15
            )
            
            # Transform label positioned along arrow
            tlabel = Tex(tlabel_text, font_size=15, color=CYAN)
            mid_pos = (start_pos + end_pos) / 2 + UP * 0.25
            tlabel.move_to(mid_pos)
            
            arrow_group = VGroup(arrow, tlabel)
            arrows.append(arrow_group)
            self.add(arrow_group)

        # Animate arrows appearing
        for arrow in arrows:
            self.play(FadeIn(arrow), run_time=0.2)
        self.wait(0.4)

        # STEP 6: Show simple overlays for each variation type
        # Create overlay effects (simplified vector graphics)
        overlays = []
        overlay_types = ["light", "pose", "expression", "occlusion", "blur", "shadow", "age", "camera"]
        
        for i, (vtype, card) in enumerate(zip(overlay_types[:len(variation_groups)], variation_cards)):
            overlay = self.create_variation_overlay(card, vtype)
            if overlay:
                overlays.append(overlay)
                self.add(overlay)
        
        # Animate overlays briefly
        for overlay in overlays[:4]:  # Show first 4 overlays
            self.play(FadeIn(overlay), run_time=0.15)
        self.wait(0.3)
        for overlay in overlays[:4]:
            self.play(FadeOut(overlay), run_time=0.1)

        # STEP 7: Show identity label and convergence arrows
        identity_label = Tex(r"y = \text{Person A}", font_size=24, color=GREEN)
        identity_label.move_to(DOWN * 2.8)
        self.add(identity_label)
        self.play(Write(identity_label), run_time=0.4)

        # Draw cyan arrows from all variation cards converging to identity label
        convergence_arrows = []
        for group in variation_groups:
            start = group.get_center()
            end = identity_label.get_center() + UP * 0.5
            conv_arrow = Arrow(
                start + DOWN * 0.3,
                end,
                buff=0.1,
                stroke_color=GREEN,
                stroke_width=1.2,
                max_tip_length_to_length_ratio=0.12
            )
            convergence_arrows.append(conv_arrow)
            self.add(conv_arrow)

        for arrow in convergence_arrows:
            self.play(FadeIn(arrow), run_time=0.12)
        self.wait(0.4)

        # STEP 8: Display "Many observations → one identity"
        many_text = Tex(r"\text{Many observations}", font_size=28)
        arrow_text = Tex(r"\rightarrow", font_size=28)
        one_text = Tex(r"\text{one identity}", font_size=28, color=GREEN)
        
        many_text.move_to(LEFT * 2.5 + DOWN * 1.8)
        arrow_text.next_to(many_text, RIGHT, buff=0.3)
        one_text.next_to(arrow_text, RIGHT, buff=0.3)
        
        mapping_group = VGroup(many_text, arrow_text, one_text)
        self.add(mapping_group)
        self.play(Write(mapping_group), run_time=0.4)
        self.wait(0.5)

        # STEP 9: Key message about invariance
        key_msg1 = Tex(r"\textbf{The representation must be}", font_size=26)
        key_msg2 = Tex(r"\textbf{invariant to appearance changes.}", font_size=26, color=CYAN)
        
        key_msg1.move_to(DOWN * 3.8)
        key_msg2.next_to(key_msg1, DOWN, buff=0.15)
        
        key_msg_group = VGroup(key_msg1, key_msg2)
        self.add(key_msg_group)
        self.play(Write(key_msg_group), run_time=0.5)
        self.wait(0.6)

        # STEP 10: Explanatory line
        explain = Tex(
            r"\text{Lighting, pose, blur, and occlusion should not change who the person is.}",
            font_size=18,
            color=MUTED
        )
        explain.move_to(DOWN * 4.4)
        self.add(explain)
        self.play(Write(explain), run_time=0.4)
        self.wait(0.5)

        # STEP 11: Fade out all except 2-3 difficult examples
        fade_out_elements = [title, ref_group] + arrows + convergence_arrows + [mapping_group, key_msg_group, explain]
        self.play(*[FadeOut(obj) for obj in fade_out_elements], run_time=0.4)

        # Keep only 2-3 difficult examples (low light, mask, side pose)
        keep_indices = [0, 3, 1]  # First few variations as "difficult" examples
        for i, group in enumerate(variation_groups):
            if i not in keep_indices:
                self.play(FadeOut(group), run_time=0.2)
        self.wait(0.3)

        # Fade out remaining difficult examples
        for i in keep_indices:
            if i < len(variation_groups):
                self.play(FadeOut(variation_groups[i]), run_time=0.2)
        self.wait(0.3)

        # STEP 12: Transition warning line
        transition_line = Tex(
            r"\text{But if the system handles these variations incorrectly,}",
            font_size=22,
            color=WHITE
        )
        transition_line2 = Tex(
            r"\text{the result is not just a small visual error.}",
            font_size=22,
            color=WHITE
        )
        
        transition_line.move_to(UP * 0.5)
        transition_line2.next_to(transition_line, DOWN, buff=0.2)
        
        transition_group = VGroup(transition_line, transition_line2)
        self.add(transition_group)
        self.play(Write(transition_group), run_time=0.5)
        self.wait(0.8)

        # Fade out transition
        self.play(FadeOut(transition_group), run_time=0.4)
        self.wait(0.3)

    def create_variation_overlay(self, card, vtype):
        """Create a simple overlay effect for variation type."""
        card_center = card.get_center()
        card_width = 1.1
        
        if vtype == "light":
            # Dark gradient overlay
            overlay = Rectangle(
                width=card_width,
                height=card_width,
                stroke_width=0,
                fill_color=DARK,
                fill_opacity=0.4
            )
            overlay.move_to(card_center)
            return overlay
            
        elif vtype == "pose":
            # Slight rotation indicator (arc)
            arc = Arc(
                radius=0.4,
                start_angle=30 * DEGREES,
                angle=60 * DEGREES,
                stroke_color=CYAN,
                stroke_width=1.5
            )
            arc.move_to(card_center + 0.5 * RIGHT)
            return arc
            
        elif vtype == "expression":
            # Highlight region for mouth/eyes
            highlight = Circle(
                radius=0.15,
                stroke_color=YELLOW,
                stroke_width=1.5,
                fill_opacity=0
            )
            highlight.move_to(card_center + 0.25 * DOWN)
            return highlight
            
        elif vtype == "occlusion":
            # Mask-like overlay
            mask = Rectangle(
                width=0.35,
                height=0.25,
                stroke_color=MUTED,
                stroke_width=1.5,
                fill_color=DARK,
                fill_opacity=0.6
            )
            mask.move_to(card_center + 0.25 * UP)
            return mask
            
        elif vtype == "blur":
            # Grid overlay for blur effect
            blur_grid = VGroup()
            for j in range(3):
                line_h = Line(
                    card_center + LEFT * 0.4 + UP * (-0.3 + j * 0.3),
                    card_center + RIGHT * 0.4 + UP * (-0.3 + j * 0.3),
                    stroke_color=WHITE,
                    stroke_width=0.5,
                    stroke_opacity=0.3
                )
                blur_grid.add(line_h)
            return blur_grid
            
        elif vtype == "shadow":
            # Half-face dark overlay
            shadow = Rectangle(
                width=card_width * 0.5,
                height=card_width,
                stroke_width=0,
                fill_color=DARK,
                fill_opacity=0.5
            )
            shadow.move_to(card_center + 0.25 * RIGHT)
            return shadow
        
        return None

    # =========================================================================
    # BEAT 2: WHAT IF THERE IS MISLEADING?
    # =========================================================================

    def beat_2_misleading_system(self):
        """
        Beat 2: Show different types of face recognition errors.
        - False Reject: correct user rejected
        - False Accept: wrong person accepted
        - Identity Mismatch: ambiguous comparison
        """
        # STEP 1: Fade in title
        title = Tex(r"\textbf{WHAT IF THERE IS MISLEADING IN THE SYSTEM?}", font_size=38, color=WHITE)
        title.move_to(UP * 3.4)
        self.add(title)
        self.play(Write(title), run_time=0.5)
        self.wait(0.4)

        # STEP 2: Create three scenario cards
        card_width = 3.8
        card_height = 3.5
        card_spacing = 4.2

        # Card 1: False Reject (Smartphone Unlock)
        card1 = self.create_false_reject_card(card_width, card_height)
        card1.move_to(LEFT * card_spacing + DOWN * 0.5)

        # Card 2: False Accept (Security Camera)
        card2 = self.create_false_accept_card(card_width, card_height)
        card2.move_to(DOWN * 0.5)

        # Card 3: Identity Mismatch (eKYC Verification)
        card3 = self.create_identity_mismatch_card(card_width, card_height)
        card3.move_to(RIGHT * card_spacing + DOWN * 0.5)

        # STEP 3: Fade in all cards with muted opacity initially
        all_cards = VGroup(card1, card2, card3)
        all_cards.set_opacity(0.4)
        self.add(all_cards)
        
        self.play(FadeIn(all_cards), run_time=0.5)
        self.wait(0.3)

        # STEP 4: Zoom into Card 1 (False Reject)
        self.play(
            card2.animate.set_opacity(0.2),
            card3.animate.set_opacity(0.2),
            card1.animate.set_opacity(1.0).scale(1.15).move_to(ORIGIN + UP * 0.3),
            run_time=0.6
        )
        self.wait(0.4)

        # Show score vs threshold animation
        score_bar1 = self.get_score_bar(0.42, card1)
        self.add(score_bar1)
        self.play(FadeIn(score_bar1), run_time=0.3)

        # Show threshold line
        threshold_line1 = Line(LEFT * 1.8, RIGHT * 1.8, stroke_color=RED, stroke_width=2)
        threshold_line1.move_to(DOWN * 0.8)
        threshold_label1 = Tex(r"\tau = 0.60", font_size=18, color=RED)
        threshold_label1.next_to(threshold_line1, RIGHT, buff=0.2)
        self.add(threshold_line1, threshold_label1)
        self.play(Write(threshold_line1), Write(threshold_label1), run_time=0.3)

        # Reveal False Reject label
        fr_label = Tex(r"\textbf{False Reject}", font_size=32, color=YELLOW)
        fr_label.move_to(DOWN * 1.6)
        fr_meaning = Tex(r"\text{The real user is rejected.}", font_size=20, color=MUTED)
        fr_meaning.next_to(fr_label, DOWN, buff=0.15)
        self.play(Write(fr_label), run_time=0.4)
        self.play(Write(fr_meaning), run_time=0.3)
        self.wait(0.5)

        # Return to full layout
        self.play(
            FadeOut(score_bar1),
            FadeOut(threshold_line1),
            FadeOut(threshold_label1),
            FadeOut(fr_label),
            FadeOut(fr_meaning),
            card1.animate.scale(1/1.15).move_to(LEFT * card_spacing + DOWN * 0.5).set_opacity(0.4),
            card2.animate.set_opacity(0.4),
            card3.animate.set_opacity(0.4),
            run_time=0.5
        )
        self.wait(0.3)

        # STEP 5: Zoom into Card 2 (False Accept)
        self.play(
            card1.animate.set_opacity(0.2),
            card3.animate.set_opacity(0.2),
            card2.animate.set_opacity(1.0).scale(1.15).move_to(ORIGIN + UP * 0.3),
            run_time=0.6
        )
        self.wait(0.4)

        # Show score crossing threshold
        score_bar2 = self.get_score_bar(0.81, card2)
        self.add(score_bar2)
        self.play(FadeIn(score_bar2), run_time=0.3)

        threshold_line2 = Line(LEFT * 1.8, RIGHT * 1.8, stroke_color=RED, stroke_width=2)
        threshold_line2.move_to(DOWN * 0.3)
        threshold_label2 = Tex(r"\tau = 0.60", font_size=18, color=RED)
        threshold_label2.next_to(threshold_line2, RIGHT, buff=0.2)
        self.add(threshold_line2, threshold_label2)
        self.play(Write(threshold_line2), Write(threshold_label2), run_time=0.3)

        # Warning indicator
        warning = Tex(r"!", font_size=48, color=RED)
        warning.move_to(RIGHT * 1.8 + UP * 0.5)
        self.play(Write(warning), run_time=0.3)

        # Reveal False Accept label
        fa_label = Tex(r"\textbf{False Accept}", font_size=32, color=RED)
        fa_label.move_to(DOWN * 1.6)
        fa_meaning = Tex(r"\text{The wrong person is accepted.}", font_size=20, color=MUTED)
        fa_meaning.next_to(fa_label, DOWN, buff=0.15)
        self.play(Write(fa_label), run_time=0.4)
        self.play(Write(fa_meaning), run_time=0.3)
        self.wait(0.5)

        # Return to full layout
        self.play(
            FadeOut(score_bar2),
            FadeOut(threshold_line2),
            FadeOut(threshold_label2),
            FadeOut(warning),
            FadeOut(fa_label),
            FadeOut(fa_meaning),
            card2.animate.scale(1/1.15).move_to(DOWN * 0.5).set_opacity(0.4),
            card1.animate.set_opacity(0.4),
            card3.animate.set_opacity(0.4),
            run_time=0.5
        )
        self.wait(0.3)

        # STEP 6: Zoom into Card 3 (Identity Mismatch)
        self.play(
            card1.animate.set_opacity(0.2),
            card2.animate.set_opacity(0.2),
            card3.animate.set_opacity(1.0).scale(1.15).move_to(ORIGIN + UP * 0.3),
            run_time=0.6
        )
        self.wait(0.4)

        # Show ambiguous score
        amb_score = Tex(r"s \approx \tau", font_size=24, color=YELLOW)
        amb_score.move_to(DOWN * 0.5)
        self.play(Write(amb_score), run_time=0.4)

        # Reveal Identity Mismatch label
        im_label = Tex(r"\textbf{Identity Mismatch}", font_size=32, color=YELLOW)
        im_label.move_to(DOWN * 1.6)
        im_meaning = Tex(r"\text{Selfie and document do not match clearly.}", font_size=20, color=MUTED)
        im_meaning.next_to(im_label, DOWN, buff=0.15)
        self.play(Write(im_label), run_time=0.4)
        self.play(Write(im_meaning), run_time=0.3)
        self.wait(0.5)

        # STEP 7: Summary below all cards
        self.play(
            FadeOut(amb_score),
            FadeOut(im_label),
            FadeOut(im_meaning),
            card1.animate.scale(1/1.15).move_to(LEFT * card_spacing + DOWN * 0.5).set_opacity(1.0),
            card2.animate.scale(1/1.15).move_to(DOWN * 0.5).set_opacity(1.0),
            card3.animate.scale(1/1.15).move_to(RIGHT * card_spacing + DOWN * 0.5).set_opacity(1.0),
            run_time=0.5
        )
        self.wait(0.3)

        # STEP 8: Compact summary
        summary_line1 = Tex(r"\text{A small error in similarity}", font_size=24)
        summary_arrow = Tex(r"\Downarrow", font_size=28, color=CYAN)
        summary_line2 = Tex(r"\textbf{can become a large identity risk.}", font_size=28, color=RED)
        
        summary_line1.move_to(DOWN * 2.5)
        summary_arrow.next_to(summary_line1, DOWN, buff=0.1)
        summary_line2.next_to(summary_arrow, DOWN, buff=0.1)
        
        summary_group = VGroup(summary_line1, summary_arrow, summary_line2)
        self.add(summary_group)
        self.play(Write(summary_group), run_time=0.5)
        self.wait(0.6)

        # STEP 9: Final message
        msg1 = Tex(r"\text{Recognition is not only about finding similar images.}", font_size=22)
        msg2 = Tex(r"\text{It is about making reliable identity decisions.}", font_size=22, color=CYAN)
        
        msg1.move_to(DOWN * 3.6)
        msg2.next_to(msg1, DOWN, buff=0.2)
        
        msg_group = VGroup(msg1, msg2)
        self.add(msg_group)
        self.play(Write(msg_group), run_time=0.5)
        self.wait(0.8)

        # STEP 10: Fade out all
        fade_out_all = [title, all_cards, summary_group, msg_group]
        self.play(*[FadeOut(obj) for obj in fade_out_all], run_time=0.5)
        self.wait(0.3)

    def create_false_reject_card(self, width, height):
        """Create False Reject scenario card."""
        card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.15
        )
        
        # Title
        card_title = Tex(r"\text{Smartphone Unlock}", font_size=22, color=WHITE)
        card_title.move_to(card.get_center() + UP * 1.3)
        
        # Phone icon (simple rectangle with notch)
        phone = RoundedRectangle(
            width=1.2,
            height=2.0,
            corner_radius=0.15,
            stroke_color=CYAN,
            stroke_width=2,
            fill_opacity=0
        )
        phone.move_to(card.get_center() + UP * 0.3)
        
        # Face inside phone
        phone_face = Circle(radius=0.5, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        phone_face.move_to(phone.get_center() + UP * 0.3)
        
        # Lock icon
        lock = Tex(r"\Lock{}", font_size=32, color=RED)
        lock.move_to(phone.get_center() + DOWN * 0.5)
        
        # Score display
        score_text = Tex(r"s = 0.42", font_size=18, color=MUTED)
        score_text.move_to(card.get_center() + DOWN * 1.2)
        
        card_group = VGroup(card, card_title, phone, phone_face, lock, score_text)
        return card_group

    def create_false_accept_card(self, width, height):
        """Create False Accept scenario card."""
        card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            stroke_color=RED,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.15
        )
        
        # Title
        card_title = Tex(r"\text{Security Camera}", font_size=22, color=WHITE)
        card_title.move_to(card.get_center() + UP * 1.3)
        
        # Camera icon (using existing helper)
        camera = make_camera_icon()
        camera.scale(1.5)
        camera.move_to(card.get_center() + UP * 0.3)
        
        # Two face cards
        face1 = Circle(radius=0.35, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        face1.move_to(card.get_center() + LEFT * 0.8 + DOWN * 0.4)
        
        face2 = Circle(radius=0.35, stroke_color=RED, stroke_width=2, fill_opacity=0)
        face2.move_to(card.get_center() + RIGHT * 0.8 + DOWN * 0.4)
        
        # Comparison arrow
        comp_arrow = Arrow(
            face1.get_center() + RIGHT * 0.4,
            face2.get_center() + LEFT * 0.4,
            buff=0.05,
            stroke_color=YELLOW,
            stroke_width=1.5
        )
        
        # Score display
        score_text = Tex(r"s = 0.81", font_size=18, color=GREEN)
        score_text.move_to(card.get_center() + DOWN * 1.2)
        
        card_group = VGroup(card, card_title, camera, face1, face2, comp_arrow, score_text)
        return card_group

    def create_identity_mismatch_card(self, width, height):
        """Create Identity Mismatch scenario card."""
        card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.15
        )
        
        # Title
        card_title = Tex(r"\text{eKYC Verification}", font_size=22, color=WHITE)
        card_title.move_to(card.get_center() + UP * 1.3)
        
        # Selfie card
        selfie_card = RoundedRectangle(
            width=1.3,
            height=1.5,
            corner_radius=0.1,
            stroke_color=CYAN,
            stroke_width=1.5,
            fill_color=PANEL,
            fill_opacity=0.2
        )
        selfie_card.move_to(card.get_center() + LEFT * 0.9 + DOWN * 0.2)
        
        selfie_face = Circle(radius=0.4, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        selfie_face.move_to(selfie_card.get_center())
        
        selfie_label = Tex(r"\text{Selfie}", font_size=14, color=MUTED)
        selfie_label.next_to(selfie_card, DOWN, buff=0.1)
        
        # Document card
        doc_card = RoundedRectangle(
            width=1.3,
            height=1.5,
            corner_radius=0.1,
            stroke_color=CYAN,
            stroke_width=1.5,
            fill_color=PANEL,
            fill_opacity=0.2
        )
        doc_card.move_to(card.get_center() + RIGHT * 0.9 + DOWN * 0.2)
        
        doc_face = Circle(radius=0.4, stroke_color=WHITE, stroke_width=1.5, fill_opacity=0)
        doc_face.move_to(doc_card.get_center())
        
        doc_label = Tex(r"\text{Document}", font_size=14, color=MUTED)
        doc_label.next_to(doc_card, DOWN, buff=0.1)
        
        # Question mark between cards
        question = Tex(r"?", font_size=36, color=YELLOW)
        question.move_to(card.get_center() + DOWN * 0.3)
        
        card_group = VGroup(
            card, card_title,
            selfie_card, selfie_face, selfie_label,
            doc_card, doc_face, doc_label,
            question
        )
        return card_group

    def get_score_bar(self, score, card):
        """Create a visual score bar based on similarity score."""
        bar_width = 2.5
        bar_height = 0.25
        
        # Background bar
        bg_bar = Rectangle(
            width=bar_width,
            height=bar_height,
            stroke_color=WHITE,
            stroke_width=1,
            fill_opacity=0
        )
        bg_bar.move_to(card.get_center() + DOWN * 1.0)
        
        # Filled portion based on score
        fill_width = bar_width * score
        fill_bar = Rectangle(
            width=fill_width,
            height=bar_height,
            stroke_width=0,
            fill_color=GREEN if score > 0.6 else YELLOW,
            fill_opacity=0.7
        )
        fill_bar.move_to(bg_bar.get_center())
        fill_bar.align_to(bg_bar, LEFT)
        
        # Score label
        score_label = Tex(f"s = {score:.2f}", font_size=18)
        score_label.next_to(bg_bar, DOWN, buff=0.1)
        
        return VGroup(bg_bar, fill_bar, score_label)

    # =========================================================================
    # BEAT 3: TRANSITION TO EMBEDDING SPACE
    # =========================================================================

    def beat_3_transition_to_embedding(self):
        """
        Beat 3: Transition from face images to embedding space visualization.
        - Show face images
        - Transform to glowing points
        - Form clusters
        - Reveal embedding space concept
        """
        # STEP 1: Show face images in grid
        face_files = [
            "face_1.png", "face_2.png", "face_3.png", "face_4.png",
            "face_5.png", "face_6.png", "face_7.png", "face_8.png"
        ]
        
        face_images = []
        for i, f in enumerate(face_files):
            path = asset_path(f)
            if os.path.exists(path):
                img = ImageMobject(path)
                img.set_height(1.0)
                
                # Position in two rows
                row = i // 4
                col = i % 4
                x = (col - 1.5) * 1.4
                y = (0.5 - row) * 1.3
                img.move_to(np.array([x, y, 0]))
                face_images.append(img)
                self.add(img)
        
        self.wait(0.3)
        
        # Fade in title
        title = Tex(r"\text{Pixel values are unstable}", font_size=32, color=MUTED)
        title.move_to(UP * 3.0)
        self.add(title)
        self.play(Write(title), run_time=0.4)
        self.wait(0.5)

        # STEP 2: Transform images to glowing points
        points = []
        for img in face_images:
            center = img.get_center()
            # Create glowing dot
            dot = Dot(center, color=CYAN, radius=0.15)
            
            # Glow effect (larger transparent circle behind)
            glow = Circle(radius=0.3, stroke_color=CYAN, stroke_width=2, fill_opacity=0)
            glow.move_to(center)
            
            points.append((img, dot, glow))
        
        # Animate transformation
        for img, dot, glow in points:
            self.play(
                img.animate.set_opacity(0),
                FadeIn(glow),
                FadeIn(dot),
                run_time=0.15
            )
        self.wait(0.3)

        # STEP 3: Form two clusters
        # Cluster 1: same identity (left side, cyan)
        cluster1_positions = [
            LEFT * 2.5 + UP * 0.8,
            LEFT * 2.2 + UP * 0.2,
            LEFT * 2.8 + DOWN * 0.3,
            LEFT * 2.0 + DOWN * 0.6
        ]
        
        # Cluster 2: different identities (right side, orange)
        cluster2_positions = [
            RIGHT * 2.5 + UP * 0.6,
            RIGHT * 2.2 + UP * 0.1,
            RIGHT * 2.8 + DOWN * 0.2,
            RIGHT * 2.0 + DOWN * 0.5
        ]
        
        # Move first 4 points to cluster 1
        for i, (img, dot, glow) in enumerate(points[:4]):
            if i < len(cluster1_positions):
                self.play(
                    dot.animate.move_to(cluster1_positions[i]),
                    glow.animate.move_to(cluster1_positions[i]),
                    run_time=0.5
                )
        
        # Move remaining points to cluster 2
        for i, (img, dot, glow) in enumerate(points[4:8]):
            if i < len(cluster2_positions):
                self.play(
                    dot.animate.move_to(cluster2_positions[i]),
                    glow.animate.move_to(cluster2_positions[i]),
                    run_time=0.5
                )
        
        self.wait(0.4)

        # STEP 4: Draw cluster circles
        cluster1_center = np.mean(cluster1_positions, axis=0)
        cluster2_center = np.mean(cluster2_positions, axis=0)
        
        cluster1_circle = Circle(
            radius=1.0,
            stroke_color=CYAN,
            stroke_width=2,
            fill_color=CYAN,
            fill_opacity=0.05
        )
        cluster1_circle.move_to(cluster1_center)
        
        cluster2_circle = Circle(
            radius=1.0,
            stroke_color="#CC8855",
            stroke_width=2,
            fill_color="#CC8855",
            fill_opacity=0.05
        )
        cluster2_circle.move_to(cluster2_center)
        
        self.play(FadeIn(cluster1_circle), FadeIn(cluster2_circle), run_time=0.4)
        self.wait(0.3)

        # Cluster labels
        cluster1_label = Tex(r"\text{Same Identity}", font_size=20, color=CYAN)
        cluster1_label.move_to(cluster1_center + DOWN * 1.2)
        
        cluster2_label = Tex(r"\text{Different Identities}", font_size=20, color="#CC8855")
        cluster2_label.move_to(cluster2_center + DOWN * 1.2)
        
        self.play(Write(cluster1_label), Write(cluster2_label), run_time=0.4)
        self.wait(0.4)

        # STEP 5: Message cascade
        # Fade out title and update
        self.play(FadeOut(title), run_time=0.3)
        
        msg1 = Tex(r"\text{Pixel values are unstable}", font_size=26, color=MUTED)
        msg1.move_to(UP * 3.0)
        self.add(msg1)
        self.play(Write(msg1), run_time=0.4)
        self.wait(0.5)

        # Arrow down
        arrow1 = Tex(r"\downarrow", font_size=28, color=WHITE)
        arrow1.move_to(UP * 2.5)
        self.add(arrow1)
        self.play(Write(arrow1), run_time=0.3)
        self.wait(0.3)

        # Message 2
        msg2 = Tex(r"\text{We need a better representation}", font_size=26, color=WHITE)
        msg2.move_to(UP * 2.0)
        self.add(msg2)
        self.play(Write(msg2), run_time=0.4)
        self.wait(0.5)

        # Arrow down
        arrow2 = Tex(r"\downarrow", font_size=28, color=WHITE)
        arrow2.move_to(UP * 1.5)
        self.add(arrow2)
        self.play(Write(arrow2), run_time=0.3)
        self.wait(0.3)

        # Message 3 - Embedding Space
        msg3 = Tex(r"\textbf{Embedding Space}", font_size=36, color=CYAN)
        msg3.move_to(UP * 1.0)
        self.add(msg3)
        self.play(Write(msg3), run_time=0.5)
        self.wait(0.8)

        # STEP 6: Fade out everything except final frame
        fade_out_elements = [
            cluster1_circle, cluster2_circle,
            cluster1_label, cluster2_label,
            msg1, arrow1, msg2, arrow2
        ]
        for img, dot, glow in points:
            fade_out_elements.extend([img, dot, glow])
        
        self.play(*[FadeOut(obj) for obj in fade_out_elements], run_time=0.6)
        self.wait(0.3)

        # STEP 7: Final frame - only Embedding Space
        self.play(FadeOut(msg3), run_time=0.3)
        
        final_title = Tex(r"\textbf{Embedding Space}", font_size=56, color=CYAN)
        final_title.center()
        self.add(final_title)
        self.play(Write(final_title), run_time=0.6)
        self.wait(1.0)

        # Fade out final title
        self.play(FadeOut(final_title), run_time=0.5)
        self.wait(0.3)

    # =========================================================================
    # (Future beats will be added here as separate methods)
    # =========================================================================
